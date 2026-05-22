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


class ProjectContextProvider:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or project_root()

    def snapshot(self) -> ProjectContext:
        return ProjectContext(
            root=str(self.root),
            git_branch=self._git(["branch", "--show-current"]) or "unknown",
            git_status=self._status_summary(),
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
            )
        except OSError:
            return ""

        if completed.returncode != 0:
            return ""

        return completed.stdout.strip()
