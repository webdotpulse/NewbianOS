"""
Unit Tests for NewbianOS Interactive Installer Engine
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../installer/interactive-installer")))

from installer_backend import InstallerBackend

class TestInteractiveInstaller(unittest.TestCase):

    def test_hardware_detection(self):
        """Verify hardware detection returns valid system profile."""
        backend = InstallerBackend()
        hw = backend.detect_hardware()
        self.assertIn("kernel", hw)
        self.assertIn("memory_gb", hw)
        self.assertIn("cpu_cores", hw)
        self.assertTrue(hw["kernel_v7_compliant"])

    def test_disk_detection(self):
        """Verify disk enumeration returns storage devices."""
        backend = InstallerBackend()
        disks = backend.detect_disks()
        self.assertTrue(len(disks) > 0)
        self.assertIn("device", disks[0])
        self.assertIn("size_gb", disks[0])

    def test_installation_pipeline(self):
        """Verify simulated installation execution steps."""
        backend = InstallerBackend()
        progress_records = []

        def on_prog(pct, desc):
            progress_records.append((pct, desc))

        backend.register_progress_callback(on_prog)
        success = asyncio.run(backend.execute_installation({
            "target_disk": "/dev/nvme0n1",
            "preset": "full-ai",
            "username": "lead-dev"
        }))
        self.assertTrue(success)
        self.assertTrue(len(progress_records) > 5)
        self.assertEqual(progress_records[-1][0], 100)

if __name__ == "__main__":
    unittest.main()
