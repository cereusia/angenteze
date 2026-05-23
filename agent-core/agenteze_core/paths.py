from __future__ import annotations

import os
from pathlib import Path


def project_root(start: Path | None = None) -> Path:
    env_root = os.environ.get("AGENTEZE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "agent-core").is_dir():
            return candidate

    return Path.cwd().resolve()


def runtime_dir(root: Path | None = None) -> Path:
    base = root or project_root()
    path = base / ".ze"
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_database_path(root: Path | None = None) -> Path:
    return runtime_dir(root) / "agenteze.sqlite3"


def audit_log_path(root: Path | None = None) -> Path:
    return runtime_dir(root) / "logs" / "audit.jsonl"


def schema_path(root: Path | None = None) -> Path:
    return (root or project_root()) / "memory" / "schema.sql"


def mcp_registry_path(root: Path | None = None) -> Path:
    return (root or project_root()) / "mcp" / "registry.json"
