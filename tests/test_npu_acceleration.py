"""
Unit & Integration Tests for Jarvis NPU & Local Neural Hardware Acceleration
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))

from jarvis.daemon.npu.manager import NPUManager, NPUVendor, QuantizationFormat
from jarvis.daemon.executor.system_authority import SystemAuthorityExecutor
from jarvis.daemon.core import JarvisCoreDaemon

class TestNPUAcceleration(unittest.TestCase):

    def setUp(self):
        self.npu = NPUManager()

    def test_npu_detection_and_specs(self):
        """Verify NPU hardware vendor detection and default model registration."""
        self.assertIsInstance(self.npu.active_vendor, NPUVendor)
        self.assertTrue(len(self.npu.device_name) > 0)
        self.assertGreaterEqual(self.npu.tops_rating, 10.0)
        self.assertIn("whisper-stt", self.npu.models)
        self.assertIn("piper-tts", self.npu.models)
        self.assertIn("reasoning-llm", self.npu.models)

    def test_npu_telemetry_schema(self):
        """Verify NPU telemetry contains required performance, power, and thermal fields."""
        telemetry = self.npu.get_telemetry()
        self.assertIn("vendor", telemetry)
        self.assertIn("tops", telemetry)
        self.assertIn("power_watts", telemetry)
        self.assertIn("temperature_c", telemetry)
        self.assertIn("memory_used_mb", telemetry)
        self.assertIn("active_models", telemetry)
        self.assertGreaterEqual(telemetry["tops"], 10.0)

    def test_system_authority_npu_integration(self):
        """Verify SystemAuthorityExecutor includes NPU telemetry in overall vitals."""
        executor = SystemAuthorityExecutor()
        telemetry = asyncio.run(executor.get_hardware_telemetry())
        self.assertIn("npu", telemetry)
        self.assertIn("device", telemetry["npu"])
        self.assertIn("tops", telemetry["npu"])

    def test_quantized_inference_execution(self):
        """Verify quantized inference pipeline runs with low-latency NPU offload."""
        res = asyncio.run(self.npu.execute_quantized_inference("whisper-stt", b"audio_bytes"))
        self.assertTrue(res["success"])
        self.assertTrue(res["npu_offloaded"])
        self.assertLessEqual(res["latency_ms"], 10.0)

    def test_core_daemon_npu_intent(self):
        """Verify Jarvis core responds to NPU queries."""
        daemon = JarvisCoreDaemon()
        resp = asyncio.run(daemon.process_intent("tell me about npu acceleration"))
        self.assertIn("Neural Processing Unit", resp)
        self.assertIn("TOPS", resp)

if __name__ == "__main__":
    unittest.main()
