"""
Unit & Integration Tests for Atomic Core & Instant Btrfs Rollbacks
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../installer/interactive-installer")))

from jarvis.daemon.executor.atomic_manager import AtomicCoreManager
from installer_backend import InstallerBackend

class TestAtomicRollbacks(unittest.TestCase):

    def setUp(self):
        self.mgr = AtomicCoreManager()

    def test_subvolume_isolation_layout(self):
        """Verify standard Btrfs subvolume layout and roles."""
        subvols = self.mgr.list_subvolumes()
        names = [s["name"] for s in subvols]
        self.assertIn("@", names)
        self.assertIn("@home", names)
        self.assertIn("@var", names)
        self.assertIn("@snapshots", names)

    def test_snapshot_creation_and_listing(self):
        """Verify snapshot creation and metadata tracking."""
        initial_count = len(self.mgr.list_snapshots())
        res = self.mgr.create_snapshot("Pre-Upgrade Test Snapshot", snapshot_type="pre")
        self.assertTrue(res["success"])
        self.assertEqual(res["snapshot_id"], initial_count + 1)

        snapshots = self.mgr.list_snapshots()
        self.assertEqual(len(snapshots), initial_count + 1)
        self.assertEqual(snapshots[-1]["description"], "Pre-Upgrade Test Snapshot")

    def test_rollback_execution(self):
        """Verify instant rollback updates active snapshot target."""
        self.mgr.create_snapshot("Target Point", snapshot_type="single")
        target_id = len(self.mgr.list_snapshots())
        rollback_res = self.mgr.rollback(target_id)
        self.assertTrue(rollback_res["success"])
        self.assertEqual(rollback_res["target_snapshot"], target_id)

    def test_sysext_layers_listing(self):
        """Verify systemd-sysext transactional layer inspection."""
        layers = self.mgr.list_sysext_layers()
        self.assertTrue(len(layers) > 0)
        self.assertTrue(all("name" in l and "path" in l for l in layers))

    def test_installer_subvolume_layout(self):
        """Verify installer backend includes Btrfs subvolume plan."""
        installer = InstallerBackend()
        layout = installer.get_subvolume_layout()
        subvol_names = [l["subvol"] for l in layout]
        self.assertIn("@", subvol_names)
        self.assertIn("@home", subvol_names)
        self.assertIn("@snapshots", subvol_names)

if __name__ == "__main__":
    unittest.main()
