import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Sequence

import paramiko
from tqdm import tqdm

from phasefront.config import HostConfig, load_config, CONFIG_HELP
from phasefront.ssh import get_ssh_client
from phasefront.utils import FileAction, get_overwrite_choice, ExitCode

def fetch_remote_files(config: HostConfig, remote_paths: list[str], local_dir: str,
                       force: bool = False, subdir: str = "pmon") -> tuple[list[str], list[str]]:
    """Download files from remote host using config.

    Args:
        config: Host configuration object containing connection and path info
        remote_paths: List of remote file paths. Can be:
                     - Absolute paths (used as-is)
                     - Relative paths (prefixed with {config.host.data_dir}/{subdir}/)
                     - Patterns (will be matched against files in remote directory)
        local_dir: Base directory for downloads
        force: If True, overwrite existing files without prompting
        subdir: Subdirectory name for relative paths and local storage

    Returns tuple of (downloaded_files, skipped_files)
    """
    ssh = get_ssh_client(config)
    local_dir = Path(local_dir) / subdir
    local_dir.mkdir(parents=True, exist_ok=True)

    downloaded_files = []
    skipped_files = []
    skip_all = force_all = False

    try:
        sftp = ssh.open_sftp()
        channel = sftp.get_channel()
        channel.settimeout(30)  # 30s timeout for control operations
        channel.get_transport().set_keepalive(60)  # Send keepalive every 60s during transfers

        # If any paths look like patterns, resolve them first
        if any('*' in p or '?' in p or '[' in p or '{' in p for p in remote_paths):
            remote_dir = f"{config.get('data_dir', '/mnt/pqdata')}/{subdir}"
            matched_paths = []
            for pattern in remote_paths:
                if pattern.startswith('/'):
                    matched_paths.append(pattern)  # Keep absolute paths as-is
                    continue
                try:
                    for f in sftp.listdir_attr(remote_dir):
                        if Path(f.filename).match(pattern):
                            matched_paths.append(f"{remote_dir}/{f.filename}")
                except IOError as e:
                    print(f"\nError listing remote directory: {e}", file=sys.stderr)
                    continue
            remote_paths = matched_paths

        def callback(transferred: int, total: int, pbar: tqdm) -> None:
            pbar.update(transferred - pbar.n)

        for remote_path in remote_paths:
            try:
                if remote_path.startswith('/'):
                    remote_str = remote_path
                else:
                    remote_dir = f"{config.get('data_dir', '/mnt/pqdata')}/{subdir}"
                    remote_str = f"{remote_dir}/{remote_path}"

                remote_name = remote_str.rsplit('/', 1)[-1]
                local_file = local_dir / remote_name

                if local_file.exists() and not force:
                    if skip_all:
                        print(f"Skipping {remote_name} (skip all)", file=sys.stderr)
                        skipped_files.append(str(local_file))
                        continue
                    if force_all:
                        print(f"Overwriting {remote_name} (force all)", file=sys.stderr)
                    else:
                        # Flush stderr before prompting to ensure proper order
                        sys.stderr.flush()
                        choice = get_overwrite_choice(remote_name)
                        if choice == FileAction.SKIP_ONCE:
                            print(f"Skipping {remote_name}", file=sys.stderr)
                            skipped_files.append(str(local_file))
                            continue
                        elif choice == FileAction.SKIP_ALL:
                            print(f"Skipping {remote_name} (and all future conflicts)", file=sys.stderr)
                            skip_all = True
                            skipped_files.append(str(local_file))
                            continue
                        elif choice == FileAction.FORCE_ALL:
                            print(f"Overwriting {remote_name} (and all future conflicts)", file=sys.stderr)
                            force_all = True
                        else:  # FORCE_ONCE
                            print(f"Overwriting {remote_name}", file=sys.stderr)

                # Get file size for progress bar
                stats = sftp.stat(str(remote_str))
                with tqdm(total=stats.st_size,
                         unit='B',
                         unit_scale=True,
                         desc=f"Downloading {remote_name}",
                         file=sys.stderr) as pbar:

                    sftp.get(str(remote_str),
                            str(local_file),
                            callback=lambda x, y: callback(x, y, pbar))

                downloaded_files.append(str(local_file))

            except IOError as e:
                print(f"\nError downloading {remote_name}: {e}", file=sys.stderr)
                continue

        return downloaded_files, skipped_files
    finally:
        ssh.close()

def main(
    argv: Sequence[str] = sys.argv[1:],
    description: str = "Download power monitor (pmon) Parquet files from remote host",
    subdir: str = "pmon",
    **kwargs
) -> None:
    """Download Parquet files from remote host.

    Downloads Parquet files from the specified subdirectory on the remote host.
    Reads remote paths from arguments or stdin and outputs local paths to stdout
    for piping to other commands.

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        description: Help text description (default: pmon-specific description)
        subdir: Remote subdirectory to search (default: "pmon")
        **kwargs: Additional arguments passed to ArgumentParser

    Returns:
        None. Prints downloaded file paths to stdout and status messages to stderr.
        Exit codes:
            0: All files downloaded successfully
            1: No files downloaded or error occurred
            2: Some files downloaded, others skipped
    """
    parser = ArgumentParser(
        description=description,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=f"Reads remote paths from arguments or stdin.\n"
               f"Outputs local paths to stdout for piping.\n\n"
               f"Directory structure:\n"
               f"  Remote: <data_dir>/{subdir}/...\n"
               f"  Local:  <local_dir>/{subdir}/...\n\n"
               f"Exit codes:\n"
               f"  0: All files downloaded successfully\n"
               f"  1: No files downloaded or error\n"
               f"  2: Some files downloaded, others skipped\n\n"
               f"{CONFIG_HELP}",
        **kwargs
    )
    parser.add_argument('files', nargs='*',
                       help="remote file paths or patterns. Absolute paths are used as-is, "
                            "relative paths are prefixed with {data_dir}/{subdir}/. "
                            "If omitted, reads paths from stdin (one per line).")
    parser.add_argument('--config',
                       help="path to config file (see Configuration section below)")
    parser.add_argument('--local-dir', default="streem-data",
                       help="local directory to store downloads. Files will be stored in <local-dir>/<subdir>/ "
                            "(default: './phasefront')")
    parser.add_argument('-f', '--force', action='store_true',
                       help="overwrite existing files without prompting")
    args = parser.parse_args(argv)

    # Get files from arguments or stdin
    files = args.files or [line.strip() for line in sys.stdin if line.strip()]
    if not files:
        parser.error("No input files specified")

    try:
        config = load_config(args.config)
        downloaded, skipped = fetch_remote_files(config['host'], files, args.local_dir, args.force, subdir)

        # Print all files to stdout for piping
        try:
            for f in downloaded + skipped:
                print(f)
        except BrokenPipeError:
            # Suppress the error when the pipe is closed
            sys.stderr.close()
            return

        # Print status to stderr
        if not downloaded and not skipped:
            print("No files downloaded", file=sys.stderr)
            sys.exit(ExitCode.FAILURE)
        if len(downloaded) < len(files):
            skipped_count = len(files) - len(downloaded)
            print(f"Downloaded {len(downloaded)} files, skipped {skipped_count}", file=sys.stderr)
            sys.exit(ExitCode.PARTIAL)
        print(f"Successfully downloaded {len(downloaded)} files", file=sys.stderr)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(ExitCode.PARTIAL)
    except paramiko.SSHException as e:
        print(f"SSH error: {e}", file=sys.stderr)
        sys.exit(ExitCode.PARTIAL)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(ExitCode.PARTIAL)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(ExitCode.PARTIAL)

if __name__ == '__main__':
    main()