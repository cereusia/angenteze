from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .paths import project_root


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    status: str
    detail: str

    def line(self) -> str:
        return f"- {self.name}: {self.status} - {self.detail}"


class Doctor:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or project_root()

    def run(self) -> list[DoctorCheck]:
        return [
            self._python(),
            self._swift(),
            self._script("scripts/run-agent-core.sh"),
            self._script("scripts/test-python.sh"),
            self._script("scripts/build-macos.sh"),
            self._script("script/build_and_run.sh"),
            self._file("memory/schema.sql"),
            self._mcp_registry(),
            self._git_repo(),
            self._git_remote(),
        ]

    def summary(self) -> str:
        checks = self.run()
        failures = [check for check in checks if check.status != "ok"]
        header = "Doctor local do Agente Ze"
        if failures:
            header += f"\n\nPendencias: {len(failures)}"
        else:
            header += "\n\nAmbiente base pronto."

        return header + "\n\n" + "\n".join(check.line() for check in checks)

    def _python(self) -> DoctorCheck:
        return DoctorCheck(
            name="python",
            status="ok",
            detail=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        )

    def _swift(self) -> DoctorCheck:
        swift = shutil.which("swift")
        if not swift:
            return DoctorCheck("swift", "missing", "swift nao encontrado no PATH")

        completed = self._run([swift, "--version"])
        if completed.returncode != 0:
            return DoctorCheck("swift", "error", completed.stderr.strip() or "falha")

        first_line = completed.stdout.splitlines()[0] if completed.stdout else swift
        return DoctorCheck("swift", "ok", first_line)

    def _script(self, relative_path: str) -> DoctorCheck:
        path = self.root / relative_path
        if not path.is_file():
            return DoctorCheck(relative_path, "missing", "arquivo ausente")
        if not path.stat().st_mode & 0o111:
            return DoctorCheck(relative_path, "warning", "script nao executavel")
        return DoctorCheck(relative_path, "ok", "presente e executavel")

    def _file(self, relative_path: str) -> DoctorCheck:
        path = self.root / relative_path
        if not path.is_file():
            return DoctorCheck(relative_path, "missing", "arquivo ausente")
        if path.stat().st_size == 0:
            return DoctorCheck(relative_path, "warning", "arquivo vazio")
        return DoctorCheck(relative_path, "ok", "presente")

    def _mcp_registry(self) -> DoctorCheck:
        path = self.root / "mcp" / "registry.json"
        if not path.is_file():
            return DoctorCheck("mcp/registry.json", "missing", "arquivo ausente")

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return DoctorCheck("mcp/registry.json", "error", str(exc))

        tools = payload.get("tools", [])
        if not isinstance(tools, list):
            return DoctorCheck("mcp/registry.json", "error", "tools deve ser lista")

        return DoctorCheck("mcp/registry.json", "ok", f"{len(tools)} contrato(s)")

    def _git_repo(self) -> DoctorCheck:
        completed = self._run(["git", "rev-parse", "--is-inside-work-tree"])
        if completed.returncode != 0:
            return DoctorCheck("git", "missing", "nao e repositorio Git")
        return DoctorCheck("git", "ok", "repositorio local")

    def _git_remote(self) -> DoctorCheck:
        completed = self._run(["git", "remote", "-v"])
        if completed.returncode != 0:
            return DoctorCheck("git remote", "error", completed.stderr.strip() or "falha")
        if not completed.stdout.strip():
            return DoctorCheck("git remote", "warning", "origin ainda nao configurado")
        return DoctorCheck("git remote", "ok", "remoto configurado")

    def _run(self, command: list[str]) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                command,
                cwd=self.root,
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return subprocess.CompletedProcess(command, 1, "", str(exc))
