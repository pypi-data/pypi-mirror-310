# PhaseFront

PQ strEEm Exploratory Data Analysis tool

This software lists, downloads, and plots two types of data from a PQ strEEm host:
1. continuous voltage and current waveform files ("wave"), and
2. power monitor data ("pmon") including RMS voltages and currents, active and reactive power, and frequency

Both types of data are stored as Parquet files for compact and efficient storage and access.

## Installation

Requires Python 3.8 or later:
```bash
pip install phasefront
```

## Quick Start

1. Establish a network connection to the host.  Typically, the host is a PQ strEEm gateway accessed through one of these methods:

   a. Direct Ethernet connection (recommended):
      - Connect to the gateway's ETH 2 port
      - Configure your network adapter:
        * IP address: 192.168.1.100
        * Subnet mask: 255.255.255.0
      - Gateway will be available at 192.168.1.2

   b. Local Area Network:
      - Connect gateway's ETH 2 port to your computer first
      - Follow provided instructions to:
        * Access gateway configuration
        * Change ETH 2's IP settings for your network
        * Enable DHCP if required
      - After configuration, connect ETH 2 to your network
      - Use network-assigned IP address in configuration
      - Coordinate with network administrator

   c. VPN connection:
      - Configure VPN client (provided separately)
      - Connect using assigned credentials
      - Use VPN-assigned IP address

2. Copy or use a text editor to create a configuration file named `phasefront.toml` in your current directory with your host credentials:
```toml
[host]
address = "192.168.1.2" # IP address of your PQ strEEm gateway
username = "user"       # User name provided by PhaseFront
password = "secret"     # Password provided by PhaseFront
```

3. Use the `wave-list` and `pmon-list` scripts to match and list files on the host that match a datetime expression. Waveform files are named in the form of `YYYYMMDD_hhmmss.sss.parquet` and typically cover one minute.  Power monitor files are named in the form of `YYYYMMDD_hhmm.parquet` and typically cover one day. Datetime stamps are in UTC time.

```bash
# List all available waveform files
wave-list '*.parquet'

# List all available power monitor files from the month of November 2024:
pmon-list '202411*.parquet'
```

When using patterns on Windows PowerShell, be sure to wrap them in single quotes to prevent glob expansion.

4. Use `wave-fetch` and `pmon-fetch` to download the files of interest. By default the files will Go to a `streem-data` folder in your current directory. In selecting files be aware of the storage and bandwidth requirements; each file is typically 20-40 MB.

```bash
# Download waveform files from the first ten minutes of afternoon UTC time on November 13, 2024:
wave-fetch '20241113_120*.parquet'

# Download power monitor files from the first nine days of November 2024:
pmon-fetch '2024110*.parquet'
```

If the file already exists in your local folder, you will be prompted to skip once (s), skip all (S), force once (f), or force all (F).

5. Use `wave-plot` and `pmon-plot` to create plots for selected files. The plots for waveform data include timeseries voltage and current, histograms of voltage and current, and first-order derivatives of voltage and current.  The plots for power monitor data include RMS voltage and current, power, and frequency.
```bash
# Create plots for all downloaded waveform data
wave-plot

# Plot active and reactive power for the first 2 hours of afternoon UTC for all downloaded days of November 2024
pmon-plot --power --start 12:00 --duration-hrs 2 '202411*.parquet'
```

6. Commands can be chained to list, fetch, and plot files in a combined operation using pipelines:
```bash
# Download and plot the latest 10 minutes of waveform data:
wave-list | tail -n 10 | wave-fetch | wave-plot

# Download and plot power data for November 13th:
pmon-fetch '20241113*.parquet' | pmon-plot --power
```

## Key Features

- Remote file management (list, fetch)
- Waveform analysis and plotting
- Power quality monitoring
- Flexible file pattern matching
- Pipeline support for command chaining
- Multiple plot types and metrics
- Time slice selection
- Download progress bars

## Configuration

The software looks for `phasefront.toml` in these locations (in order):
1. Path specified by `--config` argument
2. Path in `PHASEFRONT_CONFIG` environment variable
3. `./phasefront.toml` (current directory)
4. `~/.config/phasefront.toml`
5. `/etc/phasefront.toml`

## Documentation

View the documentation in your browser:
```bash
bash
phasefront-docs # Opens HTML documentation (recommended)
phasefront-docs --pdf # Opens PDF documentation
```

Use `-h` with any command to see additional options, e.g.:
```bash
wave-list -h
wave-fetch -h
pmon-plot -h
```

## License

Copyright 2024 PhaseFront and Renewable Edge LLC