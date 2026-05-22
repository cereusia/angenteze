from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import MCPEvent
from .paths import mcp_registry_path, project_root
from .permissions import MCPPermissionPolicy


class MCPClient:
    def __init__(
        self,
        registry_path: Path | None = None,
        root: Path | None = None,
        permission_policy: MCPPermissionPolicy | None = None,
    ) -> None:
        self.root = root or project_root()
        self.registry_path = registry_path or mcp_registry_path(self.root)
        self.permission_policy = permission_policy or MCPPermissionPolicy()

    def registry(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def tools(self) -> list[dict[str, Any]]:
        return list(self.registry().get("tools", []))

    def describe_available_tools(
        self,
        prompt: str = "",
        confirmed_tools: list[str] | None = None,
    ) -> list[MCPEvent]:
        events: list[MCPEvent] = []
        confirmed = set(confirmed_tools or [])
        for tool in self.tools():
            if not self._is_active_for_prompt(tool, prompt):
                continue

            decision = self.permission_policy.evaluate(tool, confirmed_tools=confirmed)
            status = "available" if decision.effect == "allow" else decision.effect
            events.append(
                MCPEvent(
                    tool_name=decision.tool_name,
                    status=status,
                    risk=decision.risk,
                    message=str(tool.get("description", "MCP tool contract loaded.")),
                    permission=decision.effect,
                    reason=decision.reason,
                    requires_confirmation=decision.requires_confirmation,
                )
            )
        return events

    def health(self) -> dict[str, object]:
        tools = self.tools()
        return {
            "status": "ready",
            "registry": str(self.registry_path),
            "tool_count": len(tools),
            "tools": [
                self.permission_policy.evaluate(tool).to_dict()
                for tool in tools
            ],
        }

    def _is_active_for_prompt(self, tool: dict[str, Any], prompt: str) -> bool:
        activation = tool.get("activation")
        if not activation:
            return True

        prompt_contains = activation.get("prompt_contains", [])
        normalized_prompt = prompt.lower()
        return any(str(term).lower() in normalized_prompt for term in prompt_contains)
