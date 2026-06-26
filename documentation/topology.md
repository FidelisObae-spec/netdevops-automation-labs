# Corporate Network Infrastructure Topology

This document outlines the logical design and IP addressing architecture for the automated network environments targeted by our Ansible playbooks.

---

## 🗺️ Logical Network Mapping

```text
               +-----------------------+
               |  Primary Edge Router  | (192.168.100.1)
               +-----------+-----------+
                           |
                           | Uplink trunk
                           |
               +-----------+-----------+
               |   Core Switch 01      | (10.10.10.5)
               +-----+-----------+-----+
                     |           |
       +-------------+           +-------------+
       |                                       |
+------+--------------+                 +------+--------------+
| VLAN 10: Engineering|                 |  VLAN 20: Guest WiFi|
| Subnet: 10.10.10.0/24|                 | Subnet: 172.16.20.0/24|
+---------------------+                 +---------------------+

📌 Subnet Allocations & VLAN Matrix
Device Hostname,Interface,Assigned IP,VLAN,Description
hq-core-sw01,Gi0/1,10.10.10.5,10,Core Gateway - Engineering
hq-core-sw01,Gi0/2,172.16.20.1,20,Core Gateway - Guest Network
branch-router-01,Gi0/0,192.168.100.1,N/A,Primary WAN Edge Interface

🔐 Automation Access Control
Management Protocol: SSHv2

Authentication: AAA Local Database / TACACS+

Execution Account: netadmin (Privilege Level 15)


