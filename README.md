# NetDevOps Automation Labs

A hands-on learning repository for network automation with Ansible, Python, and YAML. The inventory contains private IP addresses; confirm they are the intended devices and that you are authorized before running the ping check or configuration playbooks.

## What's here

- `ansible-playbooks/configure_vlans.yml` — sample Cisco IOS VLAN and interface configuration.
- `ansible-playbooks/verify_network_health.yml` — gathers router facts and command output, then writes a report on the control machine.
- `ansible-playbooks/inventory.ini` — sample Ansible inventory; no working password is included.
- `data/inventory.yaml` — sample hosts for the Python reachability check.
- `python-scripts/verify_hosts.py` — validates the YAML inventory and pings each listed IP.
- `tests/` — unit tests for inventory validation and safe command handling.
- `documentation/topology.md` — example logical topology.

## Run the Python check

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python python-scripts/verify_hosts.py
```

The host check actively pings every address in the inventory, so review the file before running it. The addresses may be reachable on a network connected to your machine.

## Run the Ansible examples

Install Ansible and the Cisco IOS collection, review the playbook and inventory, and replace the sample addresses with equipment you are authorized to manage:

```bash
ansible-galaxy collection install cisco.ios
ansible-playbook -i ansible-playbooks/inventory.ini ansible-playbooks/configure_vlans.yml --syntax-check
```

Do not commit real device passwords. Keep credentials in Ansible Vault or another approved secret store, and confirm the target inventory before running configuration tasks.

## Continuous integration

GitHub Actions currently runs focused Python lint checks and unit tests on pushes and pull requests to `main`. It does not connect to or validate live network devices.

## Learning roadmap

- [x] Create the repository and sample network inventory.
- [x] Add Python inventory validation, reachability checks, and unit tests.
- [x] Run Python linting and tests in GitHub Actions.
- [ ] Add automated syntax validation for the Ansible playbooks.
- [ ] Expand the playbooks with safe, documented configuration examples.
