"""
Unit Tests for Google Drive Sync Engine
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/google-drive-sync")))

from gdrive.daemon import GoogleDriveSyncDaemon

class TestGoogleDriveSync(unittest.TestCase):

    def test_gdrive_init_and_status(self):
        """Test daemon initialization and status schema."""
        daemon = GoogleDriveSyncDaemon(mount_point="/tmp/test_gdrive")
        asyncio.run(daemon.initialize())
        status = daemon.get_sync_status()
        self.assertEqual(status["mount_point"], "/tmp/test_gdrive")
        self.assertIn("stats", status)
        self.assertTrue(status["stats"]["storage_total_gb"] > 0)

    def test_trigger_sync(self):
        """Test immediate sync execution pass."""
        daemon = GoogleDriveSyncDaemon(mount_point="/tmp/test_gdrive")
        res = asyncio.run(daemon.trigger_immediate_sync())
        self.assertEqual(res["status"], "synced")
        self.assertGreater(res["timestamp"], 0)

if __name__ == "__main__":
    unittest.main()
