from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .context import ProjectContextProvider
from .doctor import Doctor
from .mcp_client import MCPClient
from .memory import MemoryStore


@dataclass(frozen=True)
class CommandResult:
    name: str
    message: str


CommandHandler = Callable[[str], CommandResult]


class CommandRegistry:
    def __init__(
        self,
        memory_store: MemoryStore,
        mcp_client: MCPClient,
        context_provider: ProjectContextProvider | None = None,
    ) -> None:
        self.memory_store = memory_store
        self.mcp_client = mcp_client
        self.context_provider = context_provider or ProjectContextProvider()
        self._handlers: dict[str, CommandHandler] = {
            "/help": self._help,
            "/status": self._status,
            "/doctor": self._doctor,
            "/git": self._git,
            "/memory": self._memory,
            "/mcp": self._mcp,
        }

    def can_handle(self, prompt: str) -> bool:
        return prompt.strip().startswith("/")

    def handle(self, prompt: str) -> CommandResult:
        command, _, args = prompt.strip().partition(" ")
        handler = self._handlers.get(command)
        if handler is None:
            return CommandResult(
                name=command,
                message=(
                    f"Comando desconhecido: {command}\n\n"
                    f"{self._available_commands()}"
                ),
            )

        return handler(args.strip())

    def _help(self, _args: str) -> CommandResult:
        return CommandResult(name="/help", message=self._available_commands())

    def _status(self, _args: str) -> CommandResult:
        context = self.context_provider.snapshot()
        memory = self.memory_store.health()
        mcp = self.mcp_client.health()
        return CommandResult(
            name="/status",
            message=(
                "Status local do Agente Ze\n\n"
                f"{context.summary()}\n"
                f"Memoria: {memory['status']} ({memory['path']})\n"
                f"MCP: {mcp['status']} ({mcp['tool_count']} contrato(s))"
            ),
        )

    def _memory(self, _args: str) -> CommandResult:
        return CommandResult(
            name="/memory",
            message=self.memory_store.recent_summary(limit=5),
        )

    def _doctor(self, _args: str) -> CommandResult:
        return CommandResult(
            name="/doctor",
            message=Doctor().summary(),
        )

    def _git(self, _args: str) -> CommandResult:
        return CommandResult(
            name="/git",
            message=self.context_provider.git_summary().summary(),
        )

    def _mcp(self, _args: str) -> CommandResult:
        tools = self.mcp_client.health()["tools"]
        lines = [
            f"- {tool['tool_name']}: {tool['effect']} ({tool['risk']})"
            for tool in tools
        ]
        return CommandResult(
            name="/mcp",
            message="Contratos MCP registrados:\n" + "\n".join(lines),
        )

    def _available_commands(self) -> str:
        return (
            "Comandos disponiveis:\n"
            "- /help: lista comandos locais\n"
            "- /status: mostra contexto local\n"
            "- /doctor: diagnostica ambiente local\n"
            "- /git: resume estado Git local\n"
            "- /memory: mostra resumo da memoria local\n"
            "- /mcp: mostra contratos MCP registrados"
        )
