import sys
from typing import Sequence
from phasefront.pmon.fetch import main as pmon_fetch_main

def main(
    argv: Sequence[str] = sys.argv[1:],
    description: str = "Download waveform (wave) Parquet files from remote host",
    subdir: str = "wave",
    **kwargs
) -> None:
    """Download Parquet files from remote host.

    Downloads waveform Parquet files from the wave subdirectory on the remote host.
    Reads remote paths from arguments or stdin and outputs local paths to stdout
    for piping to other commands like wave-plot.

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        description: Help text description (default: wave-specific description)
        subdir: Remote subdirectory to search (default: "wave")
        **kwargs: Additional arguments passed to ArgumentParser

    Returns:
        None. Prints downloaded file paths to stdout and status messages to stderr.
        Exit codes:
            0: All files downloaded successfully
            1: No files downloaded or error occurred
            2: Some files downloaded, others skipped
    """
    return pmon_fetch_main(argv, description=description, subdir=subdir, **kwargs)

if __name__ == '__main__':
    main()