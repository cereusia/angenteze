from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_RISKS = {"low", "medium", "high", "critical"}


@dataclass(frozen=True)
class PermissionDecision:
    tool_name: str
    risk: str
    effect: str
    reason: str
    requires_confirmation: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "tool_name": self.tool_name,
            "risk": self.risk,
            "effect": self.effect,
            "reason": self.reason,
            "requires_confirmation": self.requires_confirmation,
        }


class MCPPermissionPolicy:
    """Local-first permission gate for MCP tool contracts."""

    def evaluate(self, tool: dict[str, Any]) -> PermissionDecision:
        name = str(tool.get("name", "")).strip()
        risk = str(tool.get("risk", "")).strip().lower()
        requires_confirmation = bool(tool.get("requires_confirmation", False))

        if not name:
            return PermissionDecision(
                tool_name="<missing>",
                risk=risk or "unknown",
                effect="deny",
                reason="tool name is required",
                requires_confirmation=True,
            )

        if tool.get("enabled", True) is False:
            return PermissionDecision(
                tool_name=name,
                risk=risk or "unknown",
                effect="deny",
                reason="tool is disabled in registry",
                requires_confirmation=True,
            )

        if risk not in ALLOWED_RISKS:
            return PermissionDecision(
                tool_name=name,
                risk=risk or "unknown",
                effect="deny",
                reason="tool risk must be low, medium, high, or critical",
                requires_confirmation=True,
            )

        if risk == "critical":
            return PermissionDecision(
                tool_name=name,
                risk=risk,
                effect="deny",
                reason="critical tools are outside MVP v0.1",
                requires_confirmation=True,
            )

        if requires_confirmation or risk in {"medium", "high"}:
            return PermissionDecision(
                tool_name=name,
                risk=risk,
                effect="confirmation_required",
                reason="tool requires explicit user confirmation before execution",
                requires_confirmation=True,
            )

        return PermissionDecision(
            tool_name=name,
            risk=risk,
            effect="allow",
            reason="low-risk tool allowed by MVP v0.1 policy",
            requires_confirmation=False,
        )
