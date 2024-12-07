# PhaseFront

PQ strEEm Exploratory Data Analysis tool

## Installation

Use pip to automatically download and install the `phasefront` package [from its hosted location on PyPI](https://pypi.org/project/phasefront/).

```bash
pip install phasefront
```

## Configuration

Configuration is through a TOML file named `phasefront.toml` and placed in an accessible location. The software will check the following locations in priority order:
1. Path specified by `--config` argument
2. Path in `PHASEFRONT_CONFIG` environment variable
3. `./phasefront.toml` (current directory)
4. `~/.config/phasefront.toml`
5. `/etc/phasefront.toml`

If you do not have `phasefront.toml` file, you can create one in a text editor using the following entries:
```toml
[host]
address = "192.168.1.2"
username = "admin"
password = "secret"
```

## Connection

The

 with your host credentials.  Typically the host is a PQ strEEm gateway but it can be any computer that supports SSH access and hosts PQ strEEM waveform and power monitor files 'wave' and 'pmon' folders respectively.

with SSH acc that possible hosts include but are not limited to PQ strEEm gateways.


## Usage

### Basic Commands

List remote files:
```bash
wave-list --config phasefront.toml '*.parquet'
```

Download files:
```bash
wave-fetch --config phasefront.toml '202411*.parquet'
```

Create plots:
```bash
wave-plot data.parquet
```

### Windows PowerShell Usage

When using patterns on Windows PowerShell, be sure to wrap them in single quotes to prevent glob expansion:
```bash
wave-list '*.parquet'
wave-list '20241113_*.parquet'
```

### Remote File Patterns

The `wave-list` command supports flexible file matching patterns:

```bash
# List all Parquet files in a directory
wave-list '*.parquet'
# List files for a specific date
wave-list '20241113_*.parquet'
# List files for a specific hour
wave-list '20241113_12*.parquet'
# List files within a time range
wave-list '20241113_{12,13,14}*.parquet'
```

The pattern matching uses Python's `Path.match()` function, which supports:
- `*`: Matches any number of characters except slashes
- `?`: Matches any single character except slashes
- `[seq]`: Matches any character in seq
- `[!seq]`: Matches any character not in seq
- `{a,b,c}`: Matches any of the comma-separated alternatives

### Pipeline Usage

Chain commands together:
```bash
wave-list '24111*.parquet' | wave-fetch | wave-plot
```

### Plot Options

#### Wave Plot Options
Wave Plot supports multiple plot types that can be combined

```bash
# All plots (default)
wave-plot data.parquet

# Combine any plot types
wave-plot --wave --vhist data.parquet # Show waveforms and voltage histograms
wave-plot --vhist --ihist data.parquet # Show both histogram types
wave-plot --vderiv --ideriv data.parquet # Show both derivative plots

# Available plot types:
--wave # Voltage and current waveforms
--vhist # Voltage histograms
--ihist # Current histograms
--vderiv # Voltage derivative histograms
--ideriv # Current derivative histograms

# Show metadata for each file
wave-plot --verbose data.parquet
```

#### Power Monitoring Plot Options

Power monitoring plots support different metrics that can be combined:

```bash
# All plots (default)
pmon-plot data.parquet

# Combine any metrics
pmon-plot --freq --voltage data.parquet # Show frequency and voltage
pmon-plot --current --power data.parquet # Show current and power

# Available metrics:
--freq Frequency over time
--voltage RMS voltage
--current RMS current
--power Active and reactive power

# Show metadata for each file
pmon-plot --verbose data.parquet
```

### Time Slicing

```bash
# First 100ms (default for wave plots)
wave-plot data.parquet

# Start at 2.0 seconds, show 500ms
wave-plot --start 2.0 --duration-millis 500 data.parquet

# Show 2 hours of power monitoring data starting at 14:00 UTC
pmon-plot --start 14:00 --duration-hrs 2 data.parquet
```

### File Handling

When downloading files that already exist:
- `wave-fetch` will prompt for action:
  - `[s]kip once`: Skip this file
  - `[S]kip all`: Skip all existing files
  - `[f]orce once`: Overwrite this file
  - `[F]orce all`: Overwrite all existing files
- Use `-f` or `--force` to always overwrite without prompting

## Exit Codes

All commands:
- `0`: Success
- `1`: Complete failure
- `2`: Partial success (some files processed)

