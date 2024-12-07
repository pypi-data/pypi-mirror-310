"""Shared utilities for PhaseFront plotting tools."""

from enum import Enum, IntEnum, auto
import sys

class ExitCode(IntEnum):
    """Standard exit codes for all commands."""
    SUCCESS = 0
    FAILURE = 1
    PARTIAL = 2

class FileAction(Enum):
    SKIP_ONCE = auto()
    SKIP_ALL = auto()
    FORCE_ONCE = auto()
    FORCE_ALL = auto()

def get_overwrite_choice(filename: str) -> FileAction:
    """Prompt user for file handling choice when file exists.

    Args:
        filename: Name of file being processed

    Returns:
        FileAction enum indicating user's choice
    """
    # Save original stdin file descriptor
    old_stdin = sys.stdin

    try:
        if sys.platform == 'win32':
            import msvcrt
            while True:
                print(f"File {filename} already exists. Choose action:", file=sys.stderr)
                print("[s]kip once   [S]kip all", file=sys.stderr)
                print("[f]orce once  [F]orce all", file=sys.stderr)
                print("Choice [s/S/f/F]: ", end="", file=sys.stderr)
                sys.stderr.flush()

                choice = msvcrt.getch().decode()
                if choice in ('s', 'S', 'f', 'F'):
                    print(choice, file=sys.stderr)  # Echo the choice
                    if choice == 's':
                        return FileAction.SKIP_ONCE
                    elif choice == 'S':
                        return FileAction.SKIP_ALL
                    elif choice == 'f':
                        return FileAction.FORCE_ONCE
                    else:  # choice == 'F'
                        return FileAction.FORCE_ALL
                print("Invalid choice. Please try again.", file=sys.stderr)
        else:
            # Reopen stdin from terminal on Unix-like systems
            sys.stdin = open('/dev/tty')
            while True:
                print(f"File {filename} already exists. Choose action:", file=sys.stderr)
                print("[s]kip once   [S]kip all", file=sys.stderr)
                print("[f]orce once  [F]orce all", file=sys.stderr)
                print("Choice [s/S/f/F]: ", end="", file=sys.stderr)
                sys.stderr.flush()

                choice = sys.stdin.readline().strip()
                if choice in ('s', 'S', 'f', 'F'):
                    if choice == 's':
                        return FileAction.SKIP_ONCE
                    elif choice == 'S':
                        return FileAction.SKIP_ALL
                    elif choice == 'f':
                        return FileAction.FORCE_ONCE
                    else:  # choice == 'F'
                        return FileAction.FORCE_ALL
                print("Invalid choice. Please try again.", file=sys.stderr)
    finally:
        # Restore original stdin
        sys.stdin = old_stdin

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string."""
    if seconds < 0:
        raise ValueError("Duration cannot be negative")
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    return f"{hours:.1f}h"