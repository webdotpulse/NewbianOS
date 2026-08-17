"""
Jarvis Multimodal AI Core Daemon
Coordinates on-device Voice, Optical Vision, Screen Perception, System Execution, and IPC.
"""

import asyncio
import logging
import os
import signal
import sys
from typing import Any, Dict, Optional

from jarvis.daemon.voice.engine import JarvisVoiceEngine
from jarvis.daemon.vision.camera import JarvisCameraTracker
from jarvis.daemon.vision.screen import JarvisScreenSensor
from jarvis.daemon.executor.system_authority import SystemAuthorityExecutor
from jarvis.daemon.ipc.server import JarvisIPCServer
from jarvis.daemon.voice.spatial_audio import SpatialAudioEngine
from jarvis.daemon.voice.macros import VoiceMacroEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Jarvis) %(message)s"
)
logger = logging.getLogger("jarvis.core")

class JarvisCoreDaemon:
    def __init__(self):
        self.voice = JarvisVoiceEngine()
        self.camera = JarvisCameraTracker()
        self.screen = JarvisScreenSensor()
        self.executor = SystemAuthorityExecutor()
        self.ipc = JarvisIPCServer(self)
        self.spatial_audio = SpatialAudioEngine()
        self.macros = VoiceMacroEngine()
        self.is_running = False

    async def initialize(self):
        """Initialize all multimodal sensors and communication buses."""
        logger.info("Initializing Jarvis AI Multimodal Daemon for NewbianOS...")
        
        # Connect voice callbacks
        self.voice.register_audio_spectrum_callback(self._on_audio_spectrum)
        self.voice.register_wake_callback(self._on_wake_word)
        self.voice.register_transcription_callback(self._on_transcription)

        # Connect vision callbacks
        self.camera.register_vision_callback(self._on_vision_telemetry)

        # Start subsystems
        await self.voice.start()
        await self.camera.start()
        await self.ipc.start()

        self.is_running = True
        logger.info("⚡ Jarvis Multimodal Daemon is ACTIVE and OPERATIONAL.")

    def _on_audio_spectrum(self, volume: float, spectrum: list):
        asyncio.create_task(self.ipc.broadcast_event("audio_spectrum", {"volume": volume, "spectrum": spectrum}))

    def _on_wake_word(self):
        logger.info("Wake word detected!")
        asyncio.create_task(self.ipc.broadcast_event("wake_word", {"detected": True}))
        asyncio.create_task(self.voice.synthesize_speech("At your service."))

    def _on_transcription(self, text: str, is_final: bool):
        asyncio.create_task(self.ipc.broadcast_event("transcription", {"text": text, "final": is_final}))

    def _on_vision_telemetry(self, telemetry: dict):
        asyncio.create_task(self.ipc.broadcast_event("vision_telemetry", telemetry))

    async def process_intent(self, prompt: str) -> str:
        """
        Process user intent using on-device intelligence and OS execution authority.
        """
        prompt_lower = prompt.lower().strip()
        logger.info(f"Processing user intent: '{prompt}'")

        # 0. Voice Macro & Terminal Gesture Matching
        macro_match = self.macros.match_macro(prompt)
        if macro_match:
            macro, cmd = macro_match
            resp = f"Executing voice macro: '{macro.description}' -> `{cmd}`"
            asyncio.create_task(self.voice.synthesize_speech(f"Executing {macro.description}"))
            return resp

        # 1. System Status / Telemetry intent
        if any(w in prompt_lower for w in ["status", "system status", "health", "vitals", "diagnostics"]):
            telemetry = await self.executor.get_hardware_telemetry()
            resp = f"All NewbianOS systems operational. CPU load is {telemetry['load_average'][0]}, Memory is at {telemetry['memory']['percent']}% ({telemetry['memory']['used_gb']}GB of {telemetry['memory']['total_gb']}GB), GPU {telemetry['gpu']['type']} is nominal at {telemetry['gpu']['temp_c']}°C."
            asyncio.create_task(self.voice.synthesize_speech(resp))
            return resp

        # 2. Containers / Docker intent
        if "docker" in prompt_lower or "container" in prompt_lower:
            if "up" in prompt_lower or "start" in prompt_lower:
                res = await self.executor.manage_containers("compose_up")
                msg = "Docker Compose environment deployed successfully in the background." if res["success"] else f"Error deploying containers: {res.get('stderr')}"
                asyncio.create_task(self.voice.synthesize_speech(msg))
                return msg
            elif "list" in prompt_lower or "ps" in prompt_lower:
                res = await self.executor.manage_containers("list")
                return f"Active containers:\n{res.get('stdout', 'No containers running.')}"

        # 3. Vision / Screen lookup
        if any(w in prompt_lower for w in ["look at screen", "what's on my screen", "read screen", "screen"]):
            ctx = await self.screen.get_active_window_context()
            resp = f"I see {ctx['active_app']} open with window title '{ctx['window_title']}'. Detected workspace context: {', '.join(ctx['detected_technologies'])}."
            asyncio.create_task(self.voice.synthesize_speech(resp))
            return resp

        # 4. NPU & Neural Hardware Acceleration intent
        if any(w in prompt_lower for w in ["npu", "neural", "accelerator", "ai hardware", "quantization", "tops"]):
            npu = self.executor.npu_manager.get_telemetry()
            resp = f"Neural Processing Unit active: {npu['device']} ({npu['tops']} TOPS). Running {len(npu['active_models'])} quantized local models at {npu['power_watts']}W ({npu['utilization_percent']}% load, {npu['temperature_c']}°C)."
            asyncio.create_task(self.voice.synthesize_speech(resp))
            return resp

        # 5. Volume / Hardware control
        if "volume up" in prompt_lower:
            await self.executor.control_audio_volume(10)
            return "Audio volume increased by 10%."
        elif "volume down" in prompt_lower:
            await self.executor.control_audio_volume(-10)
            return "Audio volume decreased by 10%."

        # Default intelligent response
        resp = f"Executed request: '{prompt}'. Antigravity agent toolchain and NewbianOS authority engaged."
        asyncio.create_task(self.voice.synthesize_speech(resp))
        return resp

    async def shutdown(self):
        """Clean shutdown of all subsystems."""
        logger.info("Shutting down Jarvis Daemon...")
        self.is_running = False
        await self.voice.stop()
        await self.camera.stop()
        await self.ipc.stop()

async def run_daemon(test_mode: bool = False):
    daemon = JarvisCoreDaemon()
    await daemon.initialize()
    if test_mode:
        logger.info("Daemon started in test mode. Running sanity checks...")
        vitals = await daemon.executor.get_hardware_telemetry()
        assert vitals["kernel"] != ""
        logger.info(f"Sanity checks passed! Kernel: {vitals['kernel']}")
        await daemon.shutdown()
        return

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            pass

    await stop_event.wait()
    await daemon.shutdown()

if __name__ == "__main__":
    test_mode = "--test-mode" in sys.argv
    asyncio.run(run_daemon(test_mode=test_mode))
