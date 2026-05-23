from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import utc_now_iso
from .paths import audit_log_path, project_root


SENSITIVE_KEY_PARTS = ("secret", "token", "password", "passphrase", "key", "credential")


class AuditLogger:
    def __init__(self, log_path: Path | None = None, root: Path | None = None) -> None:
        self.root = root or project_root()
        self.log_path = log_path or audit_log_path(self.root)

    def record(
        self,
        event_type: str,
        request_id: str | None = None,
        fields: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "created_at": utc_now_iso(),
            "event_type": event_type,
            "request_id": request_id,
            "fields": self._sanitize(fields or {}),
        }

        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True))
                handle.write("\n")
        except OSError:
            return

    def _sanitize(self, value: Any) -> Any:
        if isinstance(value, dict):
            sanitized: dict[str, Any] = {}
            for key, item in value.items():
                key_text = str(key)
                if self._is_sensitive_key(key_text):
                    sanitized[key_text] = "<redacted>"
                else:
                    sanitized[key_text] = self._sanitize(item)
            return sanitized

        if isinstance(value, list):
            return [self._sanitize(item) for item in value[:20]]

        if isinstance(value, str):
            return self._truncate(value)

        if value is None or isinstance(value, (bool, int, float)):
            return value

        return self._truncate(str(value))

    def _is_sensitive_key(self, key: str) -> bool:
        normalized = key.lower()
        return any(part in normalized for part in SENSITIVE_KEY_PARTS)

    def _truncate(self, value: str, limit: int = 500) -> str:
        if len(value) <= limit:
            return value
        return value[:limit] + "...<truncated>"
