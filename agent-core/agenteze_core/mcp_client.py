from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import MCPEvent
from .paths import mcp_registry_path, project_root


class MCPClient:
    def __init__(self, registry_path: Path | None = None, root: Path | None = None) -> None:
        self.root = root or project_root()
        self.registry_path = registry_path or mcp_registry_path(self.root)

    def registry(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def tools(self) -> list[dict[str, Any]]:
        return list(self.registry().get("tools", []))

    def describe_available_tools(self) -> list[MCPEvent]:
        events: list[MCPEvent] = []
        for tool in self.tools():
            events.append(
                MCPEvent(
                    tool_name=str(tool["name"]),
                    status="available",
                    risk=str(tool.get("risk", "unknown")),
                    message=str(tool.get("description", "MCP tool contract loaded.")),
                )
            )
        return events

    def health(self) -> dict[str, object]:
        tools = self.tools()
        return {
            "status": "ready",
            "registry": str(self.registry_path),
            "tool_count": len(tools),
            "tools": [tool["name"] for tool in tools],
        }
