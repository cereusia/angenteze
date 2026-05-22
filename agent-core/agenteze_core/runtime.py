from __future__ import annotations

from .contracts import AgentRequest, AgentResponse
from .mcp_client import MCPClient
from .memory import MemoryStore


class AgentRuntime:
    def __init__(
        self,
        memory_store: MemoryStore | None = None,
        mcp_client: MCPClient | None = None,
    ) -> None:
        self.memory_store = memory_store or MemoryStore()
        self.mcp_client = mcp_client or MCPClient()

    def handle(self, request: AgentRequest) -> AgentResponse:
        try:
            request.validate()
            memory_summary = self.memory_store.recent_summary()
            mcp_events = self.mcp_client.describe_available_tools()
            tool_count = len(mcp_events)

            message = (
                "Ze recebeu a intencao e esta operando no backend local do MVP v0.1.\n\n"
                f"Entrada: {request.prompt}\n\n"
                f"{memory_summary}\n"
                f"MCP client carregado com {tool_count} contrato(s) de ferramenta.\n\n"
                "Escopo atual: sem voz, sem browser, sem automacao ampla e sem multiagente."
            )

            response = AgentResponse(
                request_id=request.request_id,
                status="ok",
                message=message,
                memory_summary=memory_summary,
                mcp_events=mcp_events,
            )
            self.memory_store.record_interaction(request, response)
            return response
        except Exception as exc:
            return AgentResponse(
                request_id=request.request_id,
                status="error",
                message="Falha no backend local do Agente Ze.",
                memory_summary="Memoria indisponivel para esta requisicao.",
                errors=[str(exc)],
            )

    def status(self) -> dict[str, object]:
        return {
            "status": "ready",
            "agent": "Agente Ze",
            "version": "0.1.0",
            "memory": self.memory_store.health(),
            "mcp": self.mcp_client.health(),
        }
