"""
Unit & Integration Tests for Jarvis AI Multimodal Assistant
"""

import asyncio
import os
import sys
import unittest

# Add packages to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))

from jarvis.daemon.core import JarvisCoreDaemon
from jarvis.daemon.voice.engine import JarvisVoiceEngine
from jarvis.daemon.vision.camera import JarvisCameraTracker
from jarvis.daemon.vision.screen import JarvisScreenSensor
from jarvis.daemon.executor.system_authority import SystemAuthorityExecutor

class TestJarvisAssistant(unittest.TestCase):

    def test_voice_engine_callbacks(self):
        """Test audio spectrum and callback registrations."""
        engine = JarvisVoiceEngine()
        spectrum_received = []

        def on_spectrum(vol, spec):
            spectrum_received.append((vol, spec))

        engine.register_audio_spectrum_callback(on_spectrum)
        self.assertEqual(len(engine.audio_callbacks), 1)

    def test_camera_perception(self):
        """Test camera tracking coordinates and proximity structure."""
        tracker = JarvisCameraTracker()
        perception = tracker.get_current_perception()
        self.assertIn("face", perception)
        self.assertIn("user_present", perception)
        self.assertIn("gaze", perception)
        self.assertIn("distance_cm", perception)

    def test_system_authority_telemetry(self):
        """Test hardware telemetry and OS info retrieval."""
        executor = SystemAuthorityExecutor()
        telemetry = asyncio.run(executor.get_hardware_telemetry())
        self.assertIn("cpu_percent", telemetry)
        self.assertIn("memory", telemetry)
        self.assertIn("gpu", telemetry)
        self.assertIn("os", telemetry)
        self.assertTrue(telemetry["memory"]["total_gb"] > 0)

    def test_screen_sensor(self):
        """Test active window context sensing."""
        sensor = JarvisScreenSensor()
        ctx = asyncio.run(sensor.get_active_window_context())
        self.assertIn("active_app", ctx)
        self.assertIn("window_title", ctx)
        self.assertIn("detected_technologies", ctx)

    def test_core_daemon_intent_processing(self):
        """Test Jarvis intent processing and agent reasoning."""
        daemon = JarvisCoreDaemon()
        resp = asyncio.run(daemon.process_intent("system status"))
        self.assertIn("NewbianOS", resp)
        self.assertIn("CPU", resp)

        screen_resp = asyncio.run(daemon.process_intent("look at screen"))
        self.assertIn("Antigravity", screen_resp)

if __name__ == "__main__":
    unittest.main()
