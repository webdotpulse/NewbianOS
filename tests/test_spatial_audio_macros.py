"""
Unit & Integration Tests for PipeWire 3D Spatial Audio & Voice Macro Engine
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))

from jarvis.daemon.voice.spatial_audio import SpatialAudioEngine, SpatialPosition3D
from jarvis.daemon.voice.macros import VoiceMacroEngine
from jarvis.daemon.core import JarvisCoreDaemon

class TestSpatialAudioMacros(unittest.TestCase):

    def setUp(self):
        self.spatial = SpatialAudioEngine(screen_width=1920, screen_height=1080)
        self.macros = VoiceMacroEngine()

    def test_window_spatial_binaural_coordinates(self):
        """Verify 3D coordinate mapping from Wayland window geometry."""
        # Left-side window
        left_win = {"x": 100, "y": 200, "w": 600, "h": 500}
        pos_left = self.spatial.calculate_window_spatial_position(left_win)
        self.assertLess(pos_left.x, 0.0)
        self.assertLess(pos_left.azimuth_deg, 0.0)

        # Right-side window
        right_win = {"x": 1200, "y": 200, "w": 600, "h": 500}
        pos_right = self.spatial.calculate_window_spatial_position(right_win)
        self.assertGreater(pos_right.x, 0.0)
        self.assertGreater(pos_right.azimuth_deg, 0.0)

    def test_pipewire_spatial_args_generation(self):
        """Verify generation of PipeWire spatializer filter-chain properties."""
        pos = SpatialPosition3D(x=-0.5, y=0.2, z=0.75, azimuth_deg=-22.5, elevation_deg=4.0, gain=1.0)
        args = self.spatial.generate_pipewire_spatial_args(pos)
        self.assertIn("--property", args)
        self.assertTrue(any("spatial.position.x=-0.5" in a for a in args))
        self.assertTrue(any("spatial.azimuth=-22.5" in a for a in args))

    def test_git_rebase_push_voice_macro(self):
        """Verify matching Git workflow voice shortcuts."""
        matched = self.macros.match_macro("Jarvis, rebase on main and force push")
        self.assertIsNotNone(matched)
        macro, cmd = matched
        self.assertEqual(macro.macro_id, "git_rebase_push")
        self.assertIn("git pull --rebase", cmd)
        self.assertIn("git push --force-with-lease", cmd)

    def test_swarm_audit_voice_macro(self):
        """Verify matching Swarm and Devcontainer voice gestures."""
        matched = self.macros.match_macro("Hey Jarvis, run security swarm audit")
        self.assertIsNotNone(matched)
        macro, cmd = matched
        self.assertEqual(macro.category, "swarm")
        self.assertIn("agy-swarm spawn security", cmd)

    def test_core_daemon_macro_execution(self):
        """Verify Jarvis core routes voice macro to execution."""
        daemon = JarvisCoreDaemon()
        resp = asyncio.run(daemon.process_intent("split terminal and tail docker logs"))
        self.assertIn("Executing voice macro", resp)
        self.assertIn("docker logs", resp)

if __name__ == "__main__":
    unittest.main()
