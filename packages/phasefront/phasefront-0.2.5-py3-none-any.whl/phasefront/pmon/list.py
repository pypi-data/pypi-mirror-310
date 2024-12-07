import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Sequence
from datetime import datetime

import tomli
import paramiko

from phasefront.config import HostConfig, load_config, CONFIG_HELP
from phasefront.ssh import get_ssh_client

def list_remote_files(config: HostConfig, pattern: str, verbose: bool = False, subdir: str = "pmon") -> list[str]:
    """List matching files in remote directory.

    Args:
        config: Host configuration
        pattern: File pattern to match
        verbose: If True, show file details
        subdir: Subdirectory to search

    Returns:
        List of matching filenames (not full paths)
    """
    ssh = get_ssh_client(config)
    try:
        sftp = ssh.open_sftp()
        remote_dir = f"{config.get('data_dir', '/mnt/pqdata')}/{subdir}"
        if verbose:
            print(f"Checking remote directory: {remote_dir}", file=sys.stderr)

        try:
            files = []
            for f in sftp.listdir_attr(remote_dir):
                if Path(f.filename).match(pattern):
                    files.append(f.filename)
            return sorted(files)
        except IOError as e:
            print(f"Error accessing remote directory: {e}", file=sys.stderr)
            raise
    finally:
        ssh.close()

def main(
    argv: Sequence[str] = sys.argv[1:],
    description: str = "List matching power monitor (pmon) Parquet files on remote host",
    subdir: str = "pmon",
    **kwargs
) -> None:
    """List matching Parquet files from remote host.

    Lists Parquet files from the specified subdirectory on the remote host.
    Supports pattern matching and outputs file paths to stdout for piping
    to other commands like pmon-fetch or pmon-plot.

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        description: Help text description (default: pmon-specific description)
        subdir: Remote subdirectory to search (default: "pmon")
        **kwargs: Additional arguments passed to ArgumentParser
    """
    parser = ArgumentParser(
        description=description,
        epilog=f"Outputs matching file paths to stdout for piping.\n\n"
               f"Exit codes:\n"
               f"  0: Success\n"
               f"  1: No files found or error\n\n"
               f"{CONFIG_HELP}",
        formatter_class=RawDescriptionHelpFormatter,
        **kwargs
    )
    parser.add_argument('pattern', nargs='?', default='*.parquet',
                        help="file pattern to match (e.g., '*.parquet', '20241113_*.parquet'). "
                             "Supports wildcards (*, ?), character classes ([abc]), and "
                             "alternatives ({a,b,c})")
    parser.add_argument('--config',
                        help="path to config file (see Configuration section below)")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="show detailed file information")
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        try:
            if 'host' not in config:
                print(f"Error: Missing 'host' section in config file", file=sys.stderr)
                sys.exit(1)

            files = list_remote_files(config['host'], args.pattern, args.verbose, subdir)
            for f in files:
                print(f)
        except KeyError as e:
            print(f"Error: Missing required host config key: {e}", file=sys.stderr)
            print("Required keys are: address", file=sys.stderr)
            print("Optional keys are: username, password, key_filename, data_dir", file=sys.stderr)
            sys.exit(1)
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"Network error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error connecting to host: {e.__class__.__name__}: {str(e)}", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: Config file not found: {e}", file=sys.stderr)
        sys.exit(1)
    except tomli.TOMLDecodeError as e:
        print(f"Error: Invalid TOML config file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading config: {str(e)}", file=sys.stderr)
        sys.exit(1)

    if not files:
        print("No matching files found", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()