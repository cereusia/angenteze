from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class AgentRequest:
    request_id: str
    prompt: str
    source: str
    created_at: str
    confirmed_tools: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_prompt(
        cls,
        prompt: str,
        source: str = "macos",
        confirmed_tools: list[str] | None = None,
    ) -> "AgentRequest":
        return cls(
            request_id=str(uuid4()),
            prompt=prompt.strip(),
            source=source,
            created_at=utc_now_iso(),
            confirmed_tools=confirmed_tools or [],
        )

    def validate(self) -> None:
        if not self.prompt:
            raise ValueError("prompt is required")
        if len(self.prompt) > 8000:
            raise ValueError("prompt is too long")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "prompt": self.prompt,
            "source": self.source,
            "created_at": self.created_at,
            "confirmed_tools": self.confirmed_tools,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class MCPEvent:
    tool_name: str
    status: str
    risk: str
    message: str
    permission: str
    reason: str
    requires_confirmation: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "tool_name": self.tool_name,
            "status": self.status,
            "risk": self.risk,
            "message": self.message,
            "permission": self.permission,
            "reason": self.reason,
            "requires_confirmation": self.requires_confirmation,
        }


@dataclass(frozen=True)
class AgentResponse:
    request_id: str
    status: str
    message: str
    memory_summary: str
    mcp_events: list[MCPEvent] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status,
            "message": self.message,
            "memory_summary": self.memory_summary,
            "mcp_events": [event.to_dict() for event in self.mcp_events],
            "errors": self.errors,
        }
