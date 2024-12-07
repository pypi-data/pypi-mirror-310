import sys
from typing import Sequence
from phasefront.pmon.list import main as pmon_list_main

def main(
    argv: Sequence[str] = sys.argv[1:],
    description: str = "List matching waveform (wave) Parquet files on remote host",
    subdir: str = "wave",
    **kwargs
) -> None:
    """List matching Parquet files from remote host.

    Lists waveform Parquet files from the wave subdirectory on the remote host.
    Supports pattern matching and outputs file paths to stdout for piping
    to other commands like wave-fetch or wave-plot.

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        description: Help text description (default: wave-specific description)
        subdir: Remote subdirectory to search (default: "wave")
        **kwargs: Additional arguments passed to ArgumentParser
    """
    return pmon_list_main(argv, description=description, subdir=subdir, **kwargs)

if __name__ == '__main__':
    main()