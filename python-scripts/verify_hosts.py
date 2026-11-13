"""Check reachability of hosts listed in the YAML inventory."""

from ipaddress import ip_address
from pathlib import Path
import subprocess
import sys

import yaml


def load_network_inventory(file_path):
    """Return a hostname-to-IP mapping from the inventory YAML file."""
    path = Path(file_path)
    with path.open(encoding="utf-8") as inventory_file:
        document = yaml.safe_load(inventory_file) or {}

    if not isinstance(document, dict):
        raise ValueError("Inventory must be a YAML mapping.")

    devices = document.get("infrastructure_devices", [])
    if not isinstance(devices, list):
        raise ValueError("'infrastructure_devices' must be a list.")

    inventory = {}
    for index, device in enumerate(devices, start=1):
        if not isinstance(device, dict):
            raise ValueError(f"Device entry {index} must be a mapping.")

        hostname = device.get("hostname")
        address = device.get("ip")
        if not isinstance(hostname, str) or not hostname.strip():
            raise ValueError(f"Device entry {index} needs a hostname.")
        if hostname in inventory:
            raise ValueError(f"Duplicate hostname: {hostname}")
        if not isinstance(address, str):
            raise ValueError(f"Device {hostname} needs an IP address.")

        try:
            inventory[hostname] = str(ip_address(address))
        except ValueError as error:
            raise ValueError(f"Device {hostname} has an invalid IP address.") from error

    return inventory


def check_device_status(ip_address_value):
    """Ping one valid IP address without passing it through a shell."""
    address = str(ip_address(ip_address_value))
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", address],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        raise RuntimeError("The 'ping' command is not installed.") from None
    return result.returncode == 0


def run_network_audit():
    print("=========================================")
    print("  NETDEVOPS DATA-DRIVEN HEALTH CHECK     ")
    print("=========================================\n")

    inventory_path = Path(__file__).resolve().parent.parent / "data" / "inventory.yaml"
    try:
        network_inventory = load_network_inventory(inventory_path)
    except (OSError, ValueError, yaml.YAMLError, RuntimeError) as error:
        print(f"Error loading inventory: {error}", file=sys.stderr)
        return 1

    if not network_inventory:
        print("No devices found in inventory.")
        return 0

    active_devices = 0
    for hostname, address in network_inventory.items():
        print(f"Checking {hostname} [{address}]...")
        try:
            is_online = check_device_status(address)
        except (ValueError, RuntimeError) as error:
            print(f"Error checking {hostname}: {error}", file=sys.stderr)
            return 1

        if is_online:
            print(" -> STATUS: REACHABLE\n")
            active_devices += 1
        else:
            print(" -> STATUS: UNREACHABLE\n")

    total_devices = len(network_inventory)
    print("-----------------------------------------")
    print(f"Audit complete: {active_devices}/{total_devices} devices reachable.")
    print("-----------------------------------------")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_network_audit())
