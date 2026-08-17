"""
Unit & Integration Tests for Antigravity Swarm & Autonomous Background Agents
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/antigravity-integration")))

from swarm.indexer import SemanticCodeGraph
from swarm.orchestrator import AgentSwarmOrchestrator, AgentStatus

class TestAntigravitySwarm(unittest.TestCase):

    def setUp(self):
        self.workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.indexer = SemanticCodeGraph(self.workspace)
        self.orchestrator = AgentSwarmOrchestrator(self.workspace)

    def test_semantic_code_indexing(self):
        """Verify workspace scanning and symbol extraction."""
        res = self.indexer.index_workspace(max_files=50)
        self.assertGreater(res["indexed_files"], 0)
        self.assertGreater(res["total_chunks"], 0)
        self.assertEqual(res["workspace"], self.workspace)

    def test_semantic_search_query(self):
        """Verify code search retrieves relevant symbols with score ranking."""
        self.indexer.index_workspace(max_files=50)
        results = self.indexer.search("JarvisCoreDaemon process_intent", top_k=3)
        self.assertTrue(len(results) > 0)
        top = results[0]
        self.assertIn("chunk_id", top)
        self.assertIn("file_path", top)
        self.assertIn("symbol", top)
        self.assertGreater(top["score"], 0.0)

    def test_spawn_background_security_agent(self):
        """Verify spawning autonomous security audit agent and event emission."""
        events_received = []

        def on_event(event):
            events_received.append(event)

        self.orchestrator.register_event_listener(on_event)
        task_id = asyncio.run(self.orchestrator.spawn_agent("security_audit", "Audit system authority"))
        self.assertIn("agy-agent-", task_id)
        self.assertIn(task_id, self.orchestrator.tasks)
        
        # Verify event bus emitted
        self.assertTrue(any(e["event"] == "agent_spawned" for e in events_received))

    def test_spawn_test_fixer_agent(self):
        """Verify test fixer agent executes and returns passing coverage metrics."""
        async def _run():
            task_id = await self.orchestrator.spawn_agent("test_fixer", "Verify test modules")
            # Wait for background agent completion
            for _ in range(20):
                if self.orchestrator.tasks[task_id].status == AgentStatus.COMPLETED:
                    break
                await asyncio.sleep(0.02)
            return task_id

        task_id = asyncio.run(_run())
        task = self.orchestrator.tasks[task_id]
        self.assertEqual(task.status, AgentStatus.COMPLETED)
        self.assertIsNotNone(task.result)
        self.assertIn("passed_tests", task.result)

if __name__ == "__main__":
    unittest.main()
