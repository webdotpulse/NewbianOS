"""
Unit & Integration Tests for Cloud Workstation Streaming & Spatial WebXR
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))

from jarvis.daemon.streaming.manager import CloudStreamerManager, StreamQuality

class TestCloudStreamingSpatial(unittest.TestCase):

    def setUp(self):
        self.streamer = CloudStreamerManager()

    def test_encoder_detection(self):
        """Verify encoder discovery and default stream parameters."""
        self.assertTrue(len(self.streamer.encoder_backend) > 0)
        self.assertEqual(self.streamer.pairing_pin, "739201")
        self.assertEqual(self.streamer.stream_port, 47989)

    def test_start_and_stop_streaming_lifecycle(self):
        """Verify starting and stopping WebRTC stream pipeline."""
        start_res = asyncio.run(self.streamer.start_stream(StreamQuality.SPATIAL_4K_120))
        self.assertTrue(start_res["success"])
        self.assertEqual(start_res["status"], "active")
        self.assertTrue(self.streamer.is_streaming)

        status = self.streamer.get_stream_status()
        self.assertTrue(status["is_streaming"])
        self.assertTrue(status["wayland_direct_scanout"])
        self.assertEqual(len(status["active_clients"]), 1)

        stop_res = asyncio.run(self.streamer.stop_stream())
        self.assertTrue(stop_res["success"])
        self.assertFalse(self.streamer.is_streaming)

    def test_spatial_head_pose_matrix_update(self):
        """Verify updating 6-DoF spatial head pose orientation."""
        asyncio.run(self.streamer.start_stream(StreamQuality.SPATIAL_4K_120))
        pose = {"yaw": 12.5, "pitch": -4.2, "roll": 0.5, "x": 0.1, "y": 0.05, "z": -0.6}
        self.streamer.update_spatial_head_pose("client-xr-01", pose)
        self.assertEqual(self.streamer.active_clients["client-xr-01"].spatial_head_pose["yaw"], 12.5)

    def test_hud_html_spatial_tags(self):
        """Verify hologram_ui.html contains WebXR 3D spatial elements."""
        hud_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant/jarvis/hud/hologram_ui.html"))
        with open(hud_path, "r") as f:
            content = f.read()
        self.assertIn("WebXR 3D", content)
        self.assertIn("ATOMIC BTRFS", content)
        self.assertIn("48 TOPS", content)

if __name__ == "__main__":
    unittest.main()
