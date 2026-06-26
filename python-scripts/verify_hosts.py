import subprocess
import json

def check_device_status(ip_address):
    """
    Simulates a network reachability check using system ping.
    Returns True if the host responds, False otherwise.
    """
    # Running a single ping command (-c 1 for Linux/macOS, change to -n 1 for Windows)
    # stdout and stderr are piped to DEVNULL to keep the terminal output clean
    try:
        output = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip_address],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return output.returncode == 0
    except Exception:
        return False

def main():
    # A dictionary representing our critical network assets (simulating an API response or inventory)
    network_inventory = {
        "core-firewall-01": "192.168.1.1",
        "distribution-switch-01": "192.168.1.2",
        "primary-dns-server": "8.8.8.8",
        "backup-dns-server": "8.8.4.4"
    }
    
    print("==================================================")
    print("STARTING AUTOMATED NETWORK REACHABILITY VERIFICATION")
    print("==================================================\n")
    
    report = {"online": [], "offline": []}
    
    for hostname, ip in network_inventory.items():
        print(f"Checking {hostname} [{ip}]...")
        is_online = check_device_status(ip)
        
        if is_online:
            print(f"   🟢 [ONLINE] {hostname} is reachable.")
            report["online"].append(hostname)
        else:
            print(f"   🔴 [OFFLINE] {hostname} failed to respond!")
            report["offline"].append(hostname)
            
    print("\n==================================================")
    print("AUTOMATION SUMMARY REPORT")
    print(f"Successfully reached: {len(report['online'])} devices.")
    print(f"Failed connections: {len(report['offline'])} devices.")
    print("==================================================")

if __name__ == "__main__":
    main()
