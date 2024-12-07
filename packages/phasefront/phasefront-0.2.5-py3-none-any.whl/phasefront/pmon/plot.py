# Plot power, RMS, and frequency data from 3-phase power quality meter
#
# Copyright 2024 Renewable Edge LLC, Honolulu, HI

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from glob import glob
from typing import Sequence, Any, NoReturn
from multiprocessing import Pool, cpu_count

import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from phasefront.utils import ExitCode, format_duration

# Try to restore memory more quickly to avoid failure when processing a lot of files.
try:
    pa.jemalloc_set_decay_ms(0)
except (AttributeError, pa.lib.ArrowNotImplementedError):
    pass

def plot_data(file_path: str, verbose: bool = False,
              start_time: str = "00:00",  # HH:MM format
              duration_sec: float = 86400.0,  # 24 hours default
              plot_frequency: bool = True,
              plot_voltage: bool = True,
              plot_current: bool = True,
              plot_power: bool = True) -> None:
    """Create visualization plots from power monitoring data.

    Generates selected plots from:
    - Frequency over time
    - RMS voltage for all phases
    - RMS current for all phases and neutral
    - Active and reactive power for all phases

    Args:
        file_path: Path to the Parquet file containing power monitoring data
        verbose: If True, prints detailed file metadata and schema
        start_time: Start time in HH:MM format (24-hour clock)
        duration_sec: Duration of the time range in seconds
        plot_frequency: If True, plot frequency over time
        plot_voltage: If True, plot RMS voltage
        plot_current: If True, plot RMS current
        plot_power: If True, plot active and reactive power

    Raises:
        FileNotFoundError: If the input file doesn't exist
        pyarrow.lib.ArrowInvalid: If the file format is invalid
    """
    print(f"Creating plots for {file_path}...", file=sys.stderr)

    # Read table before time operations
    table = pq.read_table(file_path)

    # Set output base path once
    file_base = file_path.rsplit('.', maxsplit=1)[0]

    if verbose:
        parquet_file = pq.ParquetFile(file_path)
        print("\nFile Metadata\n-------------", file=sys.stderr)
        print(parquet_file.metadata, file=sys.stderr)
        print("\nSchema\n------", file=sys.stderr)
        print(parquet_file.schema, file=sys.stderr)
        print("\nSchema as Arrow Types\n---------------------", file=sys.stderr)
        print(parquet_file.schema_arrow, file=sys.stderr)

    # Handle datetime and time slicing
    time = np.array(table['time_us'])
    time = np.array(time/1000000, dtype='datetime64[s]')

    # Convert start_time to seconds since midnight
    hours, minutes = map(int, start_time.split(':'))
    start_sec = hours * 3600 + minutes * 60

    # Get time slice
    day_start = np.datetime64(time[0], 'D')  # Midnight of first sample
    start_idx = np.searchsorted(time, day_start + np.timedelta64(start_sec, 's'))
    end_idx = np.searchsorted(time, day_start + np.timedelta64(start_sec + int(duration_sec), 's'))

    # Validate time range
    if start_idx >= len(time) or end_idx > len(time):
        raise ValueError(f"Time range {start_time} + {format_duration(duration_sec)} UTC "
                        f"exceeds data range {time[0].astype('datetime64[s]')} to "
                        f"{time[-1].astype('datetime64[s]')}")
    if start_idx >= end_idx:
        raise ValueError(f"Invalid time range: {start_time} + {duration_sec}s results in empty selection")

    # Slice all data
    time = time[start_idx:end_idx]
    table = table.slice(start_idx, end_idx - start_idx)

    date_fmt = '%Y-%m-%d %H:%M'
    date_formatter = mdate.DateFormatter(date_fmt)

    # Only create plots that are enabled
    try:
        if plot_frequency:
            # Frequency
            fig, ax = plt.subplots()
            ax.set_title(f"Frequency\n{start_time} UTC + {format_duration(duration_sec)}")
            ax.set_ylabel("Frequency [Hz]")
            ax.plot(time, table['FREQ'])
            ax.xaxis.set_major_formatter(date_formatter)
            fig.autofmt_xdate()
            fig.savefig(file_base + "_frequency.png")
            plt.close(fig)

        if plot_voltage:
            # Voltage
            fig, ax = plt.subplots()
            ax.set_title(f"Voltage\n{start_time} UTC + {format_duration(duration_sec)}")
            ax.set_ylabel("RMS voltage [V]")
            for x in ['AVRMS', 'BVRMS', 'CVRMS', 'AFVRMS', 'BFVRMS', 'CFVRMS']:
                ax.plot(time, table[x], label=x)
            ax.xaxis.set_major_formatter(date_formatter)
            fig.autofmt_xdate()
            ax.legend(loc='best', ncol=2)
            fig.savefig(file_base + "_voltage.png")
            plt.close(fig)

        if plot_current:
            # Current
            fig, ax = plt.subplots()
            ax.set_title(f"Current\n{start_time} UTC + {format_duration(duration_sec)}")
            ax.set_ylabel("RMS current [A]")
            for x in ['AIRMS', 'BIRMS', 'CIRMS', 'NIRMS', 'AFIRMS', 'BFIRMS', 'CFIRMS']:
                ax.plot(time, table[x], label=x)
            ax.xaxis.set_major_formatter(date_formatter)
            fig.autofmt_xdate()
            ax.legend(loc='best', ncol=2)
            fig.savefig(file_base + "_current.png")
            plt.close(fig)

        if plot_power:
            # Power
            fig, ax = plt.subplots()
            ax.set_title(f"Power\n{start_time} UTC + {format_duration(duration_sec)}")
            ax.set_ylabel("Active power [W]")
            for x in ['AWATT', 'BWATT', 'CWATT', 'AFWATT', 'BFWATT', 'CFWATT']:
                ax.plot(time, table[x], label=x)
            ax2 = ax.twinx()
            ax2.set_ylabel("Reactive power [var]")
            for x in ['AFVAR', 'BFVAR', 'CFVAR']:
                ax2.plot(time, table[x], label=x)
            ax.xaxis.set_major_formatter(date_formatter)
            fig.autofmt_xdate()
            ax.legend(loc='center left', ncol=2)
            ax2.legend(loc='center right')
            plt.subplots_adjust(right=0.88)
            fig.savefig(file_base + "_power.png")
            plt.close(fig)

    except plt.Error as e:
        print(f"Error: Matplotlib plotting failed: {e}", file=sys.stderr)
        raise RuntimeError(f"Plotting failed: {e}")

def process_file(args):
    """Process a single file for plotting.

    Args:
        args: Tuple of (filepath, plot_args)

    Returns:
        Tuple of (filepath, success_bool)
    """
    filepath, plot_args = args
    try:
        print(f"Creating plots for {filepath}...", file=sys.stderr)
        plot_data(filepath, **plot_args)
        return filepath, True
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return filepath, False

def main(argv: Sequence[str] = sys.argv[1:], files: Sequence[str] = None, **kwargs: Any) -> NoReturn:
    """Plot power monitoring data from Parquet files.

    Reads file paths from arguments or stdin and outputs successful paths to stdout
    for piping to other commands.

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        **kwargs: Additional arguments passed to ArgumentParser

    Returns:
        None. Prints processed file paths to stdout and status messages to stderr.
        Exit codes:
            0: All files processed successfully
            1: No files processed or error occurred
            2: Some files processed, others failed
    """
    parser = ArgumentParser(
        description="Plot power monitor (pmon) data from Parquet files",
        formatter_class=RawDescriptionHelpFormatter,
        epilog="Reads file paths from arguments or stdin.\n"
               "Outputs successful paths to stdout for piping.\n\n"
               "Exit codes:\n"
               "  0: All files processed successfully\n"
               "  1: No files processed or error\n"
               "  2: Some files processed, others failed",
        **kwargs
    )
    parser.add_argument('files', nargs='*',
                       help="Path(s) to local Parquet file(s). Glob patterns are accepted. "
                            "If omitted, reads paths from stdin (one per line).")
    parser.add_argument('-v', '--verbose', action='store_true',
                       help="Show detailed metadata for each file")

    # Plot type flags
    plot_group = parser.add_argument_group('plot types (all enabled by default; specifying any option disables the others unless explicitly enabled)')
    plot_group.add_argument('--freq', action='store_true',
        help="Plot frequency over time")
    plot_group.add_argument('--voltage', action='store_true',
        help="Plot RMS voltage")
    plot_group.add_argument('--current', action='store_true',
        help="Plot RMS current")
    plot_group.add_argument('--power', action='store_true',
        help="Plot active and reactive power")

    parser.add_argument('--start', default="00:00",
                       help="Start time in HH:MM format UTC (default: 00:00)")
    parser.add_argument('--duration-secs', type=float, default=86400.0,
                       help="Duration in seconds (default: 86400.0 = 24 hours)")
    parser.add_argument('--duration-mins', type=float,
                       help="Duration in minutes (overrides --duration-secs if specified)")
    parser.add_argument('--duration-hrs', type=float,
                       help="Duration in hours (overrides --duration-mins if specified)")
    parser.add_argument('--workers', type=int, default=cpu_count(),
                       help=f"Number of parallel workers (default: {cpu_count()})")

    args = parser.parse_args(argv)

    # Validate start time format
    try:
        hours, minutes = map(int, args.start.split(':'))
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            raise ValueError
    except (ValueError, TypeError):
        parser.error("Start time must be in HH:MM format (24-hour clock, default: 00:00)")

    # Convert duration to seconds
    if args.duration_hrs is not None:
        args.duration_secs = args.duration_hrs * 3600
    elif args.duration_mins is not None:
        args.duration_secs = args.duration_mins * 60

    # If no plot types specified, enable all
    if not any([args.freq, args.voltage, args.current, args.power]):
        args.all = True

    # Get files from arguments or stdin
    files = args.files
    if not files:
        files = [line.strip() for line in sys.stdin if line.strip()]

    if not files:
        parser.error("No input files specified")

    # Prepare plot arguments dictionary
    plot_args = {
        'verbose': args.verbose,
        'start_time': args.start,
        'duration_sec': args.duration_secs,
        'plot_frequency': args.all or args.freq,
        'plot_voltage': args.all or args.voltage,
        'plot_current': args.all or args.current,
        'plot_power': args.all or args.power
    }

    # Collect all file paths first
    all_files = []
    if args.files:
        # Handle command-line files with glob patterns
        for pattern in args.files:
            matched = list(glob(pattern))
            if not matched:
                print(f"No files matched {pattern}", file=sys.stderr)
            all_files.extend(matched)
    else:
        # Read paths from stdin without globbing
        all_files = files  # Already read from stdin above

    if not all_files:
        print("No files were found", file=sys.stderr)
        sys.exit(ExitCode.FAILURE)

    # Process files in parallel
    with Pool(args.workers) as pool:
        try:
            results = pool.map(process_file, [(f, plot_args) for f in all_files])
        except Exception as e:
            print(f"Error in parallel processing: {e}", file=sys.stderr)
            # Fall back to serial processing
            print("Falling back to serial processing...", file=sys.stderr)
            results = []
            for f in all_files:
                results.append(process_file((f, plot_args)))

    # Count successes
    success_count = sum(1 for _, success in results if success)
    total_count = len(all_files)

    if success_count == 0:
        print("No files were successfully processed", file=sys.stderr)
        sys.exit(ExitCode.FAILURE)
    elif success_count < total_count:
        print(f"Warning: Only {success_count} of {total_count} files were processed",
              file=sys.stderr)
        sys.exit(ExitCode.PARTIAL)
    else:
        sys.exit(ExitCode.SUCCESS)

if __name__ == "__main__":
    main()
