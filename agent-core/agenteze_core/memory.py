from __future__ import annotations

import sqlite3
from pathlib import Path

from .contracts import AgentRequest, AgentResponse, utc_now_iso
from .paths import default_database_path, project_root, schema_path


class MemoryStore:
    def __init__(self, db_path: Path | None = None, root: Path | None = None) -> None:
        self.root = root or project_root()
        self.db_path = db_path or default_database_path(self.root)

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        schema = schema_path(self.root).read_text(encoding="utf-8")
        with sqlite3.connect(self.db_path) as connection:
            connection.executescript(schema)
            connection.execute(
                "insert or ignore into kv_store(key, value, updated_at) values (?, ?, ?)",
                ("schema_version", "1", utc_now_iso()),
            )

    def record_interaction(self, request: AgentRequest, response: AgentResponse) -> None:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert into interactions(
                    request_id,
                    source,
                    prompt,
                    response_status,
                    response_message,
                    created_at
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (
                    request.request_id,
                    request.source,
                    request.prompt,
                    response.status,
                    response.message,
                    utc_now_iso(),
                ),
            )

    def recent_summary(self, limit: int = 3) -> str:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                select prompt, response_status
                from interactions
                order by id desc
                limit ?
                """,
                (limit,),
            ).fetchall()

        if not rows:
            return "Memoria local pronta; nenhuma interacao anterior registrada."

        entries = [f"{status}: {prompt[:80]}" for prompt, status in rows]
        return "Interacoes recentes: " + " | ".join(entries)

    def health(self) -> dict[str, str]:
        self.initialize()
        return {
            "status": "ready",
            "path": str(self.db_path),
        }
