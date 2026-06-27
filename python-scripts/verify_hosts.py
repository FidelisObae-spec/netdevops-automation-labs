import os

def load_network_inventory(file_path):
    """
    Parses the inventory.yaml file dynamically without external dependencies.
    Returns a dictionary mapping hostnames to IP addresses.
    """
    inventory = {}
    if not os.path.exists(file_path):
        print(f"Error: Inventory file not found at {file_path}")
        return inventory

    current_hostname = None
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("- hostname:") or line.startswith("hostname:"):
                current_hostname = line.split(":", 1)[1].strip()
            elif (line.startswith("ip:") or line.startswith("- ip:")) and current_hostname:
                ip_address = line.split(":", 1)[1].strip()
                inventory[current_hostname] = ip_address
                current_hostname = None
                
    return inventory

def check_device_status(ip_address):
    """
    Executes a system ping to verify infrastructure device availability.
    """
    response = os.system(f"ping -c 1 -W 1 {ip_address} > /dev/null 2>&1")
    return response == 0

def run_network_audit():
    print("=========================================")
    print("  NETDEVOPS DATA-DRIVEN HEALTH CHECK     ")
    print("=========================================\n")
    
    inventory_path = os.path.join(os.path.dirname(__file__), "..", "data", "inventory.yaml")
    network_inventory = load_network_inventory(inventory_path)
    
    if not network_inventory:
        print("No devices found in inventory. Exiting audit.")
        return
        
    active_devices = 0
    total_devices = len(network_inventory)
    
    for hostname, ip in network_inventory.items():
        print(f"Checking {hostname} [{ip}]...")
        is_online = check_device_status(ip)
        
        if is_online:
            print(f" -> STATUS: ONLINE MATCHED\n")
            active_devices += 1
        else:
            print(f" -> STATUS: UNREACHABLE TIMEOUT\n")
            
    print("-----------------------------------------")
    print(f"Audit Complete: {active_devices}/{total_devices} Devices Reachable.")
    print("-----------------------------------------")

if __name__ == "__main__":
    run_network_audit()
