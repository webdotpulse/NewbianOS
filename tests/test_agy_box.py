"""
Unit & Integration Tests for Ephemeral Micro-Containers (agy-box)
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/antigravity-integration")))

from containers.agy_box import AgyBoxEngine, ContainerStatus

class TestAgyBox(unittest.TestCase):

    def setUp(self):
        self.workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.engine = AgyBoxEngine(self.workspace)

    def test_devcontainer_parsing(self):
        """Verify devcontainer configuration generation."""
        cfg = self.engine.parse_devcontainer()
        self.assertEqual(cfg.name, "NewbianOS")
        self.assertIn("dev.local", cfg.local_domain)
        self.assertTrue(cfg.enable_wayland_gui)
        self.assertTrue(cfg.enable_gpu)

    def test_launch_arguments_generation(self):
        """Verify Docker/Podman arguments include Wayland, GPU, and volume mounts."""
        cfg = self.engine.parse_devcontainer()
        args = self.engine.generate_launch_arguments(cfg)
        self.assertIn("run", args)
        self.assertIn("-d", args)
        self.assertTrue(any("WAYLAND_DISPLAY" in a for a in args))
        self.assertTrue(any("ELECTRON_OZONE_PLATFORM_HINT" in a for a in args))

    def test_box_lifecycle(self):
        """Verify launching, listing, stopping, and destroying micro-container."""
        res = asyncio.run(self.engine.up())
        self.assertTrue(res["success"])
        box_id = res["box_id"]
        self.assertIn("box-newbianos", box_id)

        boxes = self.engine.list_boxes()
        self.assertEqual(len(boxes), 1)
        self.assertEqual(boxes[0]["status"], "running")

        stop_res = asyncio.run(self.engine.stop(box_id))
        self.assertTrue(stop_res["success"])
        self.assertEqual(stop_res["status"], "stopped")

        destroy_res = asyncio.run(self.engine.destroy(box_id))
        self.assertTrue(destroy_res["success"])
        self.assertEqual(len(self.engine.list_boxes()), 0)

if __name__ == "__main__":
    unittest.main()
