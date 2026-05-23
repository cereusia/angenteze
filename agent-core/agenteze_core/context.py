from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .paths import project_root


@dataclass(frozen=True)
class ProjectContext:
    root: str
    git_branch: str
    git_status: str

    def to_dict(self) -> dict[str, str]:
        return {
            "root": self.root,
            "git_branch": self.git_branch,
            "git_status": self.git_status,
        }

    def summary(self) -> str:
        return (
            f"Projeto: {self.root}\n"
            f"Branch: {self.git_branch}\n"
            f"Git: {self.git_status}"
        )


@dataclass(frozen=True)
class GitSummary:
    branch: str
    upstream: str
    remote: str
    pending_count: int
    pending_items: list[str]
    recent_commits: list[str]

    def summary(self) -> str:
        pending = "clean" if self.pending_count == 0 else f"{self.pending_count} item(s)"
        lines = [
            "Resumo Git local",
            "",
            f"Branch: {self.branch}",
            f"Upstream: {self.upstream}",
            f"Remote: {self.remote}",
            f"Pendencias: {pending}",
        ]

        if self.pending_items:
            lines.append("")
            lines.append("Arquivos pendentes:")
            lines.extend(f"- {item}" for item in self.pending_items)

        if self.recent_commits:
            lines.append("")
            lines.append("Ultimos commits:")
            lines.extend(f"- {commit}" for commit in self.recent_commits)

        return "\n".join(lines)


class ProjectContextProvider:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or project_root()

    def snapshot(self) -> ProjectContext:
        return ProjectContext(
            root=str(self.root),
            git_branch=self._git(["branch", "--show-current"]) or "unknown",
            git_status=self._status_summary(),
        )

    def git_summary(self) -> GitSummary:
        pending_items = self._git(["status", "--short"]).splitlines()
        return GitSummary(
            branch=self._git(["branch", "--show-current"]) or "unknown",
            upstream=self._git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
            or "nao configurado",
            remote=self._git(["remote", "-v"]) or "nao configurado",
            pending_count=len(pending_items),
            pending_items=pending_items[:12],
            recent_commits=self._git(["log", "--oneline", "--decorate", "-5"]).splitlines(),
        )

    def project_summary(self) -> str:
        git = self.git_summary()
        tags = self._git(["tag", "--points-at", "HEAD"]).splitlines()
        tag_summary = ", ".join(tags) if tags else "nenhuma tag no HEAD"
        pending = "clean" if git.pending_count == 0 else f"{git.pending_count} item(s)"

        lines = [
            "Contexto local do Agente Ze",
            "",
            "Git",
            f"- Branch: {git.branch}",
            f"- Upstream: {git.upstream}",
            f"- Pendencias: {pending}",
            f"- Tags no HEAD: {tag_summary}",
            "",
            "Modulos principais",
            *self._path_lines(
                [
                    "apps/macos/Package.swift",
                    "agent-core/agenteze_core",
                    "memory/schema.sql",
                    "mcp/registry.json",
                    "tests/test_agent_core.py",
                ]
            ),
            "",
            "Memoria documental",
            *self._path_lines(
                [
                    "AGENTS.md",
                    ".codex/PROJECT_RULES.md",
                    ".codex/memory/PROJECT_SUMMARY.md",
                    ".codex/memory/CURRENT_STATE.md",
                    ".codex/memory/NEXT_ACTIONS.md",
                ]
            ),
            "",
            "Specs e release",
            *self._path_lines(
                [
                    "specs/VISION.md",
                    "specs/ARCHITECTURE.md",
                    "specs/MCP.md",
                    "specs/SECURITY.md",
                    "docs/adr",
                    "docs/release/MVP_V0_1_RELEASE_NOTES.md",
                ]
            ),
        ]

        next_actions = self._section_items(
            ".codex/memory/NEXT_ACTIONS.md",
            "Lista Curta",
            limit=5,
        )
        if next_actions:
            lines.extend(["", "Proximas acoes"])
            lines.extend(next_actions)

        return "\n".join(lines)

    def _path_lines(self, relative_paths: list[str]) -> list[str]:
        return [
            f"- {relative_path}: {self._path_status(relative_path)}"
            for relative_path in relative_paths
        ]

    def _path_status(self, relative_path: str) -> str:
        path = self.root / relative_path
        if path.is_dir():
            item_count = len(
                [item for item in path.iterdir() if not item.name.startswith(".")]
            )
            return f"ok ({item_count} item(s))"
        if path.is_file():
            return "ok"
        return "ausente"

    def _section_items(self, relative_path: str, section: str, limit: int) -> list[str]:
        path = self.root / relative_path
        if not path.is_file():
            return []

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return []

        items: list[str] = []
        in_section = False
        marker = f"## {section}"
        for line in lines:
            stripped = line.strip()
            if stripped == marker:
                in_section = True
                continue
            if in_section and stripped.startswith("## "):
                break
            if in_section and stripped:
                items.append(stripped)
            if len(items) >= limit:
                break

        return items

    def _status_summary(self) -> str:
        status = self._git(["status", "--short"])
        if not status:
            return "clean"

        lines = status.splitlines()
        return f"{len(lines)} pending item(s)"

    def _git(self, args: list[str]) -> str:
        try:
            completed = subprocess.run(
                ["git", *args],
                cwd=self.root,
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            return ""

        if completed.returncode != 0:
            return ""

        return completed.stdout.strip()
