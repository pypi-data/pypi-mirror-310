"""Configuration management for strEEm shot.

Handles loading and validation of SSH access configuration from TOML files.
Configuration file contains host access and software update credentials.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, TypedDict

import tomli

CONFIG_HELP = """
Configuration file (TOML format) contains host access settings:

[host]
address = "hostname[:port]"     # Required (default port: 22)
username = "admin"              # Optional: SSH username
password = "secret"             # Optional: SSH password
key_filename = "~/.ssh/id_rsa"  # Optional: SSH private key path
data_dir = "/mnt/pqdata"        # Optional: Remote data directory

Configuration file locations (in priority order):
1. Path specified by --config argument
2. Path in PHASEFRONT_CONFIG environment variable
3. ./phasefront.toml (current directory)
4. ~/.config/phasefront.toml
5. /etc/phasefront.toml
"""

class HostConfig(TypedDict):
    """ connection configuration.

    Required:
        address: Host address in format 'hostname[:port]' (default port: 22)
               Examples: '192.168.1.100', 'host.local:2222'

    Optional:
        username: SSH username
        password: SSH password
        key_filename: Path to SSH private key file
        data_dir: Remote data directory (default: /mnt/pqdata)
    """
    address: str
    username: str
    password: str | None
    key_filename: str | None
    data_dir: str

class UpdateConfig(TypedDict):
    """Update service configuration. Files are hosted in a Blackblaze B2 bucket.

    All fields are required:
        app_key_id: B2 application key ID
        app_key: B2 application key
        bucket_name: B2 bucket name
    """
    app_key_id: str
    app_key: str
    bucket_name: str

class Config(TypedDict):
    """Complete configuration."""
    host: HostConfig
    # updates: UpdateConfig

DEFAULT_CONFIG_PATHS = [
    Path.cwd().joinpath("phasefront.toml"),
    (Path.home().joinpath("AppData").joinpath("Local").joinpath("phasefront").joinpath("phasefront.toml")
        if os.name == 'nt' else Path.home().joinpath(".config").joinpath("phasefront.toml")),
    (Path(os.environ.get("ProgramData", "C:/ProgramData")).joinpath("phasefront").joinpath("phasefront.toml")
        if os.name == 'nt' else Path("/etc").joinpath("phasefront.toml"))
]

def parse_address(address: str) -> tuple[str, int]:
    """Parse host address string into host and port.

    Format: hostname[:port] where port defaults to 22 if not specified
    """
    if ':' in address:
        host, port_str = address.rsplit(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError(f"Invalid port number in address: {address}")
        return host, port
    return address, 22

def validate_config(config: Dict[str, Any]) -> Config:
    """Validate configuration structure and required fields.

    Args:
        config: Raw configuration dictionary from TOML

    Returns:
        Validated configuration dictionary

    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Validate host section
    if 'host' not in config:
        raise ValueError("Required section 'host' missing from configuration")

    host = config['host']
    if 'address' not in host:
        raise ValueError("Required field 'address' missing from host configuration")

    # Convert to typed dict
    validated: Config = {
        'host': {
            'address': host['address'],
            'data_dir': host.get('data_dir', '/mnt/pqdata')
        },
    }

    # Optional host fields
    for field in ['username', 'password', 'key_filename', 'data_dir']:
        if field in host:
            validated['host'][field] = host[field]

    # # Validate updates section
    # if 'updates' not in config:
    #     print("Warning: 'updates' missing from configuration", stderr)

    # updates = config['updates']
    # for field in ['app_key_id', 'app_key', 'bucket_name']:
    #     if field not in updates:
    #         raise ValueError(f"Required field '{field}' missing from updates configuration")

    # validatated:
    #     'updates': {
    #         'app_key_id': updates['app_key_id'],
    #         'app_key': updates['app_key'],
    #         'bucket_name': updates['bucket_name']
    #     }

    return validated

def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from TOML file with priority handling.

    Priority (highest to lowest):
    1. Explicitly provided config path
    2. Environment variable PHASEFRONT_CONFIG
    3. ./phasefront.toml
    4. ~/.config/phasefront.toml
    5. /etc/phasefront.toml

    Args:
        config_path: Optional explicit path to config file

    Returns:
        Validated configuration dictionary

    Raises:
        FileNotFoundError: If no config file found
        tomli.TOMLDecodeError: If config file has invalid TOML syntax
        KeyError: If required config keys are missing
    """
    # Try config locations in priority order
    paths = []
    if config_path:
        try:
            p = Path(config_path)
            abs_p = p.resolve(strict=True)  # Will raise if file doesn't exist
            paths.append(abs_p)
        except Exception as e:
            print(f"Error resolving config path '{config_path}': {e}", file=sys.stderr)

    if 'PHASEFRONT_CONFIG' in os.environ:
        try:
            p = Path(os.environ['PHASEFRONT_CONFIG'])
            abs_p = p.resolve(strict=True)
            paths.append(abs_p)
        except Exception as e:
            print(f"Error resolving env path: {e}", file=sys.stderr)

    # Add default paths
    paths.extend([p.resolve() for p in DEFAULT_CONFIG_PATHS])

    # Try each path until we find one that exists
    config_file = None
    for path in paths:
        try:
            if path.is_file():
                with open(path, 'rb') as f:
                    content = f.read()
                    config_file = path
                    break
        except Exception as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)

    if not config_file:
        tried = '\n  '.join(str(p) for p in paths)
        raise FileNotFoundError(
            f"No config file found. Create a phasefront.toml file in the current directory "
            f"or specify path with --config.\n\nSearched locations:\n  {tried}"
        )

    try:
        with open(config_file, 'rb') as f:
            raw_config = tomli.load(f)
    except tomli.TOMLDecodeError as e:
        raise tomli.TOMLDecodeError(f"Invalid TOML syntax in {config_file}: {e}",
                                   e.line, e.col)
    except Exception as e:
        raise RuntimeError(f"Error reading {config_file}: {e}")

    return validate_config(raw_config)
