# Plot continuous point on wave (CPOW) data from the PQ strEEm sensor
#
# Copyright 2024 Renewable Edge LLC, Honolulu, HI

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from glob import glob
from typing import Sequence, Any, NoReturn

import iso8601
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq

from phasefront.utils import ExitCode

SAMPLE_RATE = 32_000  # Hz
SAMPLES_PER_CYCLE = 533  # assuming 60 Hz. TODO: Generalize or better yet do zero-crossing detection

def get_sample_slice(start_sec: float = 0.0, duration_ms: float = 100.0) -> slice:
    """Convert time parameters to sample indices.

    Args:
        start_sec: Start time in seconds
        duration_ms: Duration in milliseconds

    Returns:
        slice: Sample index range
    """
    start_sample = int(start_sec * SAMPLE_RATE)
    num_samples = int((duration_ms / 1000.0) * SAMPLE_RATE)
    return slice(start_sample, start_sample + num_samples)

def plot_data(file_path: str, show_metadata: bool = False,
              start_sec: float = 0.0, duration_ms: float = 100.0,
              plot_waveform: bool = True,
              plot_voltage_hist: bool = True,
              plot_current_hist: bool = True,
              plot_voltage_deriv: bool = True,
              plot_current_deriv: bool = True) -> None:
    """Create plots from waveform data stored in a Parquet file.

    Args:
        file_path: Path to the Parquet file containing waveform data
        show_metadata: If True, prints detailed file metadata
        start_sec: Start time in seconds (default: 0.0)
        duration_ms: Duration in milliseconds (default: 100.0)
        plot_waveform: If True, create voltage/current waveform plot
        plot_voltage_hist: If True, create voltage histogram
        plot_current_hist: If True, create current histogram
        plot_voltage_deriv: If True, create voltage derivative histogram
        plot_current_deriv: If True, create current derivative histogram

    Returns:
        bool: True if plotting succeeded, False otherwise

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file format is invalid
        KeyError: If required metadata fields are missing
    """
    try:
        print(f"Creating plots for {file_path}...", file=sys.stderr)
        table = pq.read_table(file_path)

        # Set output base path once
        file_base = file_path.rsplit('.', maxsplit=1)[0]

        # Get metadata
        parquet_file = pq.ParquetFile(file_path)
        file_metadata = parquet_file.metadata
        user_metadata = file_metadata.metadata

        # Parse metadata values
        start_time_str = user_metadata[b'start_time'].decode()
        start_time = iso8601.parse_date(start_time_str)
        start_time_str = str(start_time)

        # Check if we need scaling (i.e., if data is I32)
        is_i32 = table['VA'].type == 'int32'

        # Only parse scaling factors if we're dealing with I32 data
        if is_i32:
            vscale = float(user_metadata[b'vscale'].decode())
            iscale = float(user_metadata[b'iscale'].decode())

        # Helper functions to apply scaling if needed
        if is_i32:
            scale_voltage = lambda data: data.to_numpy() * vscale
            scale_current = lambda data: data.to_numpy() * iscale
            # IN has 30x more sensitive CT for recent installations. TODO: Include the actual scaling factor in metadata!!!
            scale_neutral_current = lambda data: data.to_numpy() * (iscale / 30)
        else:
            scale_voltage = lambda data: data.to_numpy()
            scale_current = lambda data: data.to_numpy()
            scale_neutral_current = lambda data: data.to_numpy()

        if show_metadata:
            print("\nFile Metadata\n-------------")
            print(file_metadata)

            print("\nUser Metadata\n-------------")
            print(f'Start time: {start_time} (from "{start_time_str}")')
            if is_i32:
                print(f'vscale: {vscale}')
                print(f'iscale: {iscale}')
            else:
                print("Data is F32, no scaling needed")

            print("\nSchema\n------")
            print(parquet_file.schema)

            print("\nSchema as Arrow Types\n---------------------")
            print(parquet_file.schema_arrow)

        for batch in table.to_batches():
            # The metadata should be in the batch's schema
            if batch.schema.metadata:
                ts_nanos = int(batch.schema.metadata[b'timestamp'].decode())
                ts_secs = ts_nanos / 1_000_000_000
                print(f"Batch timestamp: {ts_secs:.3f}s ({ts_nanos} ns)")

        # Replace the hardcoded SLICE with calculated one
        SLICE = get_sample_slice(start_sec, duration_ms)

        try:
            # Waveforms
            if plot_waveform:
                fig, (ax1, ax2) = plt.subplots(2)
                fig.subplots_adjust(left=0.15, right=0.95, top=0.83)
                fig.suptitle(f"AC Waveforms @ {SAMPLE_RATE/1000:.0f} kHz (~{SAMPLES_PER_CYCLE} pts/cycle)\n"
                            f"Starting {start_time_str} + {start_sec:.3f}s for {duration_ms:.1f} ms")
                ax1.set_title("Voltage")
                #ax1.set_xlabel("Elapsed time [s]")
                ax1.xaxis.set_tick_params(labelbottom=False)
                ax1.set_xticks([])
                ax1.set_ylabel("Voltage [V]")
                x = np.arange(0, len(table['VA'][SLICE])/SAMPLE_RATE, 1/SAMPLE_RATE)
                ax1.plot(x, scale_voltage(table['VA'][SLICE]), label='VA')
                ax1.plot(x, scale_voltage(table['VB'][SLICE]), label='VB')
                ax1.plot(x, scale_voltage(table['VC'][SLICE]), label='VC')
                ax1.legend()
                #
                # Current
                ax2.set_title("Current")
                ax2.set_xlabel("Elapsed time [s]")
                ax2.set_ylabel("Current [A]")
                ax2.plot(x, scale_current(table['IA'][SLICE]), label='IA')
                ax2.plot(x, scale_current(table['IB'][SLICE]), label='IB')
                ax2.plot(x, scale_current(table['IC'][SLICE]), label='IC')
                ax2.plot(x, scale_neutral_current(table['IN'][SLICE]), label='IN')
                ax2.legend()
                fig.savefig(file_base + "_waveform.png")
                plt.close(fig)

            # Voltage histogram
            if plot_voltage_hist:
                num_samples = len(table['VA'])
                duration = num_samples/32000
                fig, ax = plt.subplots()
                ax.set_title(f"Voltage Histogram\n{num_samples:,} samples over {duration:.3} s\nStarting {start_time_str}")
                ax.set_xlabel("Voltage [V]")
                for phase in ['VA', 'VB', 'VC']:
                    hist, bin_edges = np.histogram(scale_voltage(table[phase]), bins=250)
                    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
                    # Use bin centers rather than edges.
                    plt.plot(bin_centers, hist, label=phase)
                bin_size = bin_edges[1] - bin_edges[0]
                ax.set_ylabel(f"# occurrences (on bin size {bin_size:.3} V)")
                ax.legend()
                plt.subplots_adjust(top=0.87)
                fig.savefig(file_base + "_voltage_hist.png")
                plt.close(fig)

            # Current histogram
            if plot_current_hist:
                fig, ax = plt.subplots()
                ax.set_title(f"Current Histogram\n{num_samples:,} samples over {duration:.3} s\nStarting {start_time_str}")
                ax.set_xlabel("Current [A]")
                for phase in ['IA', 'IB', 'IC', 'IN']:
                    if phase == 'IN':
                        hist, bin_edges = np.histogram(scale_neutral_current(table[phase]), bins=250)
                    else:
                        hist, bin_edges = np.histogram(scale_current(table[phase]), bins=250)
                    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
                    # Use bin centers rather than edges.
                    plt.plot(bin_centers, hist, label=phase)
                bin_size = bin_edges[1] - bin_edges[0]
                ax.set_ylabel(f"# occurrences (on bin size {bin_size:.3} A)")
                ax.legend()
                plt.subplots_adjust(top=0.87)
                fig.savefig(file_base + "_current_hist.png")
                plt.close(fig)

            # Voltage derivative histogram
            if plot_voltage_deriv:
                fig, ax = plt.subplots()
                ax.set_title(f"Histogram of Voltage Derivative\n{num_samples:,} samples over {duration:.3} s\nStarting {start_time_str}")
                ax.set_xlabel("Rate of Change of Voltage [mV/s]")
                for phase in ['VA', 'VB', 'VC']:
                    y = np.diff(scale_voltage(table[phase]))*SAMPLE_RATE
                    hist, bin_edges = np.histogram(y/1000, bins=250)
                    # Use bin centers rather than edges.
                    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
                    plt.plot(bin_centers, hist, label=phase)
                bin_size = bin_edges[1] - bin_edges[0]
                ax.set_ylabel(f"# occurrences (on bin size {bin_size*1000:.0f} mV/s)")
                ax.legend()
                plt.subplots_adjust(top=0.87)
                fig.savefig(file_base + "_voltage_deriv_hist.png")
                plt.close(fig)

            # Current derivative histogram
            if plot_current_deriv:
                fig, ax = plt.subplots()
                ax.set_title(f"Histogram of Current Derivative\n{num_samples:,} samples over {duration:.3} s\nStarting {start_time_str}")
                ax.set_xlabel("Rate of Change of Current [mA/s]")
                for phase in ['IA', 'IB', 'IC', 'IN']:
                    if phase == 'IN':
                        y = np.diff(scale_neutral_current(table[phase]))*SAMPLE_RATE
                    else:
                        y = np.diff(scale_current(table[phase]))*SAMPLE_RATE
                    hist, bin_edges = np.histogram(y/1000, bins=250)
                    # Use bin centers rather than edges.
                    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
                    plt.plot(bin_centers, hist, label=phase)
                bin_size = bin_edges[1] - bin_edges[0]
                ax.set_ylabel(f"# occurrences (on bin size {bin_size*1000:f} mA/s)")
                ax.legend()
                plt.subplots_adjust(top=0.87)
                fig.savefig(file_base + "_current_deriv_hist.png")
                plt.close(fig)

        except plt.Error as e:
            print(f"Error: Matplotlib plotting failed: {e}", file=sys.stderr)
            raise RuntimeError(f"Plotting failed: {e}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
        return False

def process_file(args):
    """Helper function to process a single file with plot arguments"""
    file_path, plot_args = args
    try:
        plot_data(file_path, **plot_args)
        print(file_path)
        return (file_path, True)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
        return (file_path, False)

def main(argv: Sequence[str] = sys.argv[1:], **kwargs: Any) -> NoReturn:
    """Plot waveform data from Parquet files.

    Reads file paths from arguments or stdin and outputs successful paths to stdout
    for piping to other commands. Creates various plots based on the enabled plot types:
    - Voltage/current waveforms
    - Voltage/current histograms
    - Voltage/current derivative histograms

    Args:
        argv: Command line arguments (default: sys.argv[1:])
        **kwargs: Additional arguments passed to ArgumentParser

    Returns:
        None. Prints processed file paths to stdout and status messages to stderr.
        Exit codes:
            0: All files processed successfully
            1: No files processed or error occurred
            2: Some files processed, others failed

    Plot Types:
        --wave: Voltage and current waveforms
        --vhist: Voltage histogram
        --ihist: Current histogram
        --vderiv: Voltage derivative histogram
        --ideriv: Current derivative histogram
        --all: Enable all plot types (default if none specified)

    Time Range:
        --start: Start time in seconds (default: 0.0)
        --duration-millis: Duration in milliseconds (default: 100.0)

    Example Usage:
        # Plot first 100ms of data (default)
        wave-plot data.parquet

        # Plot 500ms starting at 2.0 seconds
        wave-plot --start 2.0 --duration-millis 500 data.parquet

        # Only plot voltage histogram
        wave-plot --vhist data.parquet
    """
    parser = ArgumentParser(
        description="Plot waveform data from Parquet file(s)",
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
    parser.add_argument('--start', type=float, default="0.0",
        help="Start time in seconds (default: 0.0)")
    parser.add_argument('--duration-millis', type=float, default=100.0,
        help="Duration in milliseconds (default: 100.0)")

    # Plot type flags
    plot_group = parser.add_argument_group('plot types (all enabled by default; specifying any option disables the others unless explicitly enabled)')
    plot_group.add_argument('--wave', action='store_true',
        help="Plot voltage/current waveforms")
    plot_group.add_argument('--vhist', action='store_true',
        help="Plot voltage histograms")
    plot_group.add_argument('--ihist', action='store_true',
        help="Plot current histograms")
    plot_group.add_argument('--vderiv', action='store_true',
        help="Plot voltage derivative histograms")
    plot_group.add_argument('--ideriv', action='store_true',
        help="Plot current derivative histograms")

    # Add imports at top of file
    from multiprocessing import Pool, cpu_count

    # Add to existing argument parser
    parser.add_argument('--workers', type=int, default=cpu_count(),
                       help=f"Number of parallel workers (default: {cpu_count()})")

    args = parser.parse_args(argv)

    # If no plot types specified, enable all
    all_enabled = not any([args.wave, args.vhist, args.ihist, args.vderiv, args.ideriv])

    # Prepare plot arguments dictionary
    plot_args = {
        'show_metadata': args.verbose,
        'start_sec': args.start,
        'duration_ms': args.duration_millis,
        'plot_waveform': all_enabled or args.wave,
        'plot_voltage_hist': all_enabled or args.vhist,
        'plot_current_hist': all_enabled or args.ihist,
        'plot_voltage_deriv': all_enabled or args.vderiv,
        'plot_current_deriv': all_enabled or args.ideriv
    }

    # Get files from arguments or stdin
    files = args.files
    if not files:
        files = [line.strip() for line in sys.stdin if line.strip()]

    if not files:
        parser.error("No input files specified")

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
        results = pool.map(process_file, [(f, plot_args) for f in all_files])

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
