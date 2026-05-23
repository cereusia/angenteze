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

from agenteze_core.audit import AuditLogger
from agenteze_core.contracts import AgentRequest
from agenteze_core.memory import MemoryStore
from agenteze_core.permissions import MCPPermissionPolicy
from agenteze_core.runtime import AgentRuntime


class AgentCoreTests(unittest.TestCase):
    def test_runtime_returns_ok_and_records_interaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            response = runtime.handle(AgentRequest.from_prompt("status do MVP"))

            self.assertEqual(response.status, "ok")
            self.assertIn("backend local", response.message)
            self.assertEqual(len(response.mcp_events), 1)
            self.assertEqual(response.mcp_events[0].permission, "allow")
            self.assertIn("status do MVP", store.recent_summary())

    def test_runtime_requests_confirmation_for_medium_tool_intent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            response = runtime.handle(
                AgentRequest.from_prompt("gravar memoria: checkpoint MCP")
            )

            permissions = {event.tool_name: event.permission for event in response.mcp_events}
        self.assertEqual(
            permissions["agenteze.memory.capture_note"],
            "confirmation_required",
        )

    def test_runtime_handles_slash_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            help_response = runtime.handle(AgentRequest.from_prompt("/help"))
            status_response = runtime.handle(AgentRequest.from_prompt("/status"))
            context_response = runtime.handle(AgentRequest.from_prompt("/context"))
            doctor_response = runtime.handle(AgentRequest.from_prompt("/doctor"))
            git_response = runtime.handle(AgentRequest.from_prompt("/git"))
            memory_response = runtime.handle(AgentRequest.from_prompt("/memory"))
            mcp_response = runtime.handle(AgentRequest.from_prompt("/mcp"))

            self.assertIn("/status", help_response.message)
            self.assertIn("/context", help_response.message)
            self.assertIn("/doctor", help_response.message)
            self.assertIn("/git", help_response.message)
            self.assertIn("Status local", status_response.message)
            self.assertIn("Contexto local", context_response.message)
            self.assertIn("Memoria documental", context_response.message)
            self.assertIn("Proximas acoes", context_response.message)
            self.assertIn("Doctor local", doctor_response.message)
            self.assertIn("mcp/registry.json", doctor_response.message)
            self.assertIn("Resumo Git local", git_response.message)
            self.assertIn("Branch:", git_response.message)
            self.assertIn("Interacoes recentes", memory_response.message)
            self.assertIn("Contratos MCP", mcp_response.message)

    def test_runtime_handles_unknown_slash_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            response = runtime.handle(AgentRequest.from_prompt("/nao-existe"))

            self.assertEqual(response.status, "ok")
            self.assertIn("Comando desconhecido", response.message)

    def test_runtime_executes_readonly_context_tool_and_writes_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = MemoryStore(db_path=temp_path / "memory.sqlite3", root=ROOT)
            audit = AuditLogger(log_path=temp_path / "audit.jsonl", root=ROOT)
            runtime = AgentRuntime(memory_store=store, audit_logger=audit)

            response = runtime.handle(AgentRequest.from_prompt("contexto do projeto"))

            self.assertEqual(response.status, "ok")
            self.assertIn("Ferramentas MCP executadas", response.message)
            self.assertIn("Contexto local do Agente Ze", response.message)
            permissions = {
                event.tool_name: event.permission
                for event in response.mcp_events
            }
            self.assertEqual(permissions["agenteze.workspace.context_read"], "allow")

            audit_lines = (temp_path / "audit.jsonl").read_text(encoding="utf-8")
            self.assertIn("mcp.executed", audit_lines)
            self.assertIn("agenteze.workspace.context_read", audit_lines)
            self.assertIn("prompt_length", audit_lines)
            self.assertNotIn("contexto do projeto", audit_lines)

    def test_runtime_accepts_confirmed_medium_tool(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(db_path=Path(temp_dir) / "memory.sqlite3", root=ROOT)
            runtime = AgentRuntime(memory_store=store)

            response = runtime.handle(
                AgentRequest.from_prompt(
                    "gravar memoria: checkpoint MCP",
                    confirmed_tools=["agenteze.memory.capture_note"],
                )
            )

            permissions = {event.tool_name: event.permission for event in response.mcp_events}
            self.assertEqual(permissions["agenteze.memory.capture_note"], "confirmed")

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
        self.assertEqual(payload["mcp"]["tools"][0]["effect"], "allow")

    def test_cli_accepts_confirm_tool_argument(self) -> None:
        command = [
            sys.executable,
            "-m",
            "agenteze_core",
            "run",
            "--prompt",
            "gravar memoria: teste",
            "--confirm-tool",
            "agenteze.memory.capture_note",
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
        permissions = {
            event["tool_name"]: event["permission"]
            for event in payload["mcp_events"]
        }
        self.assertEqual(permissions["agenteze.memory.capture_note"], "confirmed")

    def test_mcp_permission_policy_gates_risk_levels(self) -> None:
        policy = MCPPermissionPolicy()

        low = policy.evaluate(
            {"name": "safe.read", "risk": "low", "requires_confirmation": False}
        )
        medium = policy.evaluate(
            {"name": "files.write", "risk": "medium", "requires_confirmation": False}
        )
        confirmed_medium = policy.evaluate(
            {"name": "files.write", "risk": "medium", "requires_confirmation": False},
            confirmed_tools={"files.write"},
        )
        critical = policy.evaluate(
            {"name": "system.delete", "risk": "critical", "requires_confirmation": True}
        )
        invalid = policy.evaluate(
            {"name": "bad.tool", "risk": "unknown", "requires_confirmation": False}
        )

        self.assertEqual(low.effect, "allow")
        self.assertEqual(medium.effect, "confirmation_required")
        self.assertEqual(confirmed_medium.effect, "confirmed")
        self.assertEqual(critical.effect, "deny")
        self.assertEqual(invalid.effect, "deny")


if __name__ == "__main__":
    unittest.main()
