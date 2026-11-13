"""Unit tests for inventory parsing and safe reachability checks."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python-scripts"))
import verify_hosts


class LoadNetworkInventoryTests(unittest.TestCase):
    def load_text(self, text):
        with tempfile.TemporaryDirectory() as temp_dir:
            inventory_file = Path(temp_dir) / "inventory.yaml"
            inventory_file.write_text(text, encoding="utf-8")
            return verify_hosts.load_network_inventory(inventory_file)

    def test_reads_inventory_and_normalizes_ip(self):
        inventory = self.load_text(
            "infrastructure_devices:\n"
            "  - hostname: edge-1\n"
            "    ip: 192.0.2.1\n"
        )
        self.assertEqual(inventory, {"edge-1": "192.0.2.1"})

    def test_rejects_invalid_ip(self):
        with self.assertRaisesRegex(ValueError, "invalid IP address"):
            self.load_text(
                "infrastructure_devices:\n"
                "  - hostname: edge-1\n"
                "    ip: '127.0.0.1; echo unsafe'\n"
            )

    def test_rejects_duplicate_hostnames(self):
        with self.assertRaisesRegex(ValueError, "Duplicate hostname"):
            self.load_text(
                "infrastructure_devices:\n"
                "  - hostname: edge-1\n"
                "    ip: 192.0.2.1\n"
                "  - hostname: edge-1\n"
                "    ip: 192.0.2.2\n"
            )


class CheckDeviceStatusTests(unittest.TestCase):
    @patch("verify_hosts.subprocess.run")
    def test_uses_argument_list_and_returns_status(self, run):
        run.return_value.returncode = 0
        self.assertTrue(verify_hosts.check_device_status("192.0.2.1"))
        self.assertEqual(run.call_args.args[0], ["ping", "-c", "1", "-W", "1", "192.0.2.1"])
        self.assertFalse(run.call_args.kwargs["check"])

    @patch("verify_hosts.subprocess.run")
    def test_invalid_address_is_rejected_before_command(self, run):
        with self.assertRaises(ValueError):
            verify_hosts.check_device_status("192.0.2.1; echo unsafe")
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
