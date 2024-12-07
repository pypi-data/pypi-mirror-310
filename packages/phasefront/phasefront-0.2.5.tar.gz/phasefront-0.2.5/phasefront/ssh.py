import sys
import time
import paramiko

from phasefront.config import HostConfig, parse_address

def get_ssh_client(config: HostConfig) -> paramiko.SSHClient:
    """Create and connect an SSH client using config settings.

    Args:
        config: Gateway configuration object containing connection info

    Returns:
        Connected SSHClient

    Raises:
        paramiko.SSHException: If connection or authentication fails
    """
    host, port = parse_address(config['address'])
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Default timeouts optimized for direct Ethernet
    connect_kwargs = {
        'hostname': host,
        'port': port,
        'username': config.get('username'),
        'password': config.get('password'),
        'key_filename': config.get('key_filename'),
        'timeout': 10,  # Connection timeout
        'banner_timeout': 10,  # SSH banner timeout
        'auth_timeout': 10,  # Authentication timeout
        'look_for_keys': True,
        'allow_agent': True
    }

    # Try twice with a short delay - helps with both direct and VPN
    last_error = None
    for attempt in range(2):
        try:
            if attempt > 0:
                print(f"Connection failed, retrying...", file=sys.stderr)
                time.sleep(1)
            ssh.connect(**connect_kwargs)

            # Enable keepalive only if configured (default: disabled)
            if config.get('keepalive_interval'):
                ssh.get_transport().set_keepalive(config['keepalive_interval'])

            return ssh
        except Exception as e:
            last_error = e

    raise last_error or paramiko.SSHException("Failed to establish connection")