from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent-core"))

from agenteze_core.contracts import AgentRequest
from agenteze_core.memory import MemoryStore
from agenteze_core.runtime import AgentRuntime


class AgentCoreTests(unittest.TestCase):
    def test_runtime_returns_ok_and_records_interaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            response = runtime.handle(AgentRequest.from_prompt("status do MVP"))

            self.assertEqual(response.status, "ok")
            self.assertIn("backend local", response.message)
            self.assertGreaterEqual(len(response.mcp_events), 1)
            self.assertIn("status do MVP", store.recent_summary())

    def test_cli_status_outputs_json(self) -> None:
        command = [
            sys.executable,
            "-m",
            "agenteze_core",
            "status",
        ]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env={
                **os.environ,
                "PYTHONPATH": str(ROOT / "agent-core"),
                "AGENTEZE_ROOT": str(ROOT),
            },
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ready")
        self.assertEqual(payload["agent"], "Agente Ze")
        self.assertGreaterEqual(payload["mcp"]["tool_count"], 1)


if __name__ == "__main__":
    unittest.main()
