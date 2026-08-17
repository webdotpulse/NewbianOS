"""
Jarvis IPC Server - High Speed UNIX Socket & JSON-RPC Gateway
Connects Jarvis Daemon with Holographic HUD, CLI, and KDE Plasma Applets.
"""

import asyncio
import json
import logging
import os
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("jarvis.ipc")

SOCKET_PATH = os.path.expanduser("~/.jarvis/jarvis.sock")

class JarvisIPCServer:
    def __init__(self, core_daemon):
        self.core = core_daemon
        self.clients: List[asyncio.StreamWriter] = []
        self.server: Optional[asyncio.Server] = None

    async def start(self):
        """Bind and start UNIX socket server."""
        os.makedirs(os.path.dirname(SOCKET_PATH), exist_ok=True)
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        self.server = await asyncio.start_unix_server(self._handle_client, path=SOCKET_PATH)
        os.chmod(SOCKET_PATH, 0o600)
        logger.info(f"Jarvis IPC Server active on {SOCKET_PATH}")

    async def stop(self):
        """Close socket server and disconnect clients."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

    async def broadcast_event(self, event_type: str, data: Any):
        """Broadcast real-time event to all connected HUDs, CLI sessions, and plugins."""
        payload = json.dumps({"event": event_type, "data": data}) + "\n"
        for writer in list(self.clients):
            try:
                writer.write(payload.encode("utf-8"))
                await writer.drain()
            except Exception:
                if writer in self.clients:
                    self.clients.remove(writer)

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client requests."""
        self.clients.append(writer)
        logger.debug("New client connected to Jarvis IPC")
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                try:
                    request = json.loads(line.decode("utf-8").strip())
                    response = await self._process_request(request)
                    writer.write((json.dumps(response) + "\n").encode("utf-8"))
                    await writer.drain()
                except json.JSONDecodeError:
                    err = {"error": "Invalid JSON format"}
                    writer.write((json.dumps(err) + "\n").encode("utf-8"))
                    await writer.drain()
        except Exception as e:
            logger.debug(f"Client disconnected: {e}")
        finally:
            if writer in self.clients:
                self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch JSON-RPC commands to Jarvis Core."""
        cmd = request.get("cmd")
        args = request.get("args", {})

        if cmd == "ping":
            return {"status": "ok", "time": os.times()}
        elif cmd == "telemetry":
            vitals = await self.core.executor.get_hardware_telemetry()
            perception = self.core.camera.get_current_perception()
            return {"status": "ok", "telemetry": vitals, "perception": perception}
        elif cmd == "ask":
            prompt = args.get("prompt", "")
            response = await self.core.process_intent(prompt)
            return {"status": "ok", "response": response}
        elif cmd == "execute":
            command = args.get("command", [])
            use_pkexec = args.get("use_pkexec", False)
            res = await self.core.executor.execute_privileged_task(command, use_pkexec)
            return {"status": "ok", "result": res}
        elif cmd == "service":
            srv = args.get("name")
            act = args.get("action")
            res = await self.core.executor.manage_systemd_service(srv, act)
            return {"status": "ok", "result": res}
        elif cmd == "containers":
            act = args.get("action")
            target = args.get("target")
            res = await self.core.executor.manage_containers(act, target)
            return {"status": "ok", "result": res}
        elif cmd == "screen_look":
            ctx = await self.core.screen.get_active_window_context()
            return {"status": "ok", "context": ctx}
        elif cmd == "speak":
            text = args.get("text", "")
            asyncio.create_task(self.core.voice.synthesize_speech(text))
            return {"status": "ok", "speaking": True}
        else:
            return {"error": f"Unknown command {cmd}"}
