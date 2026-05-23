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
