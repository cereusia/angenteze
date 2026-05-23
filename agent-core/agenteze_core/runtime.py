from __future__ import annotations

from .audit import AuditLogger
from .commands import CommandRegistry
from .contracts import AgentRequest, AgentResponse
from .mcp_client import MCPClient, MCPToolResult
from .memory import MemoryStore


class AgentRuntime:
    def __init__(
        self,
        memory_store: MemoryStore | None = None,
        mcp_client: MCPClient | None = None,
        command_registry: CommandRegistry | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.memory_store = memory_store or MemoryStore()
        self.mcp_client = mcp_client or MCPClient()
        self.audit_logger = audit_logger or AuditLogger(root=self.memory_store.root)
        self.command_registry = command_registry or CommandRegistry(
            memory_store=self.memory_store,
            mcp_client=self.mcp_client,
        )

    def handle(self, request: AgentRequest) -> AgentResponse:
        try:
            request.validate()
            self.audit_logger.record(
                "request.received",
                request_id=request.request_id,
                fields={
                    "source": request.source,
                    "prompt_length": len(request.prompt),
                    "is_slash_command": request.prompt.strip().startswith("/"),
                    "confirmed_tools_count": len(request.confirmed_tools),
                },
            )

            if self.command_registry.can_handle(request.prompt):
                command_result = self.command_registry.handle(request.prompt)
                self.audit_logger.record(
                    "command.handled",
                    request_id=request.request_id,
                    fields={"command": command_result.name},
                )
                response = AgentResponse(
                    request_id=request.request_id,
                    status="ok",
                    message=command_result.message,
                    memory_summary=self.memory_store.recent_summary(),
                    mcp_events=[],
                )
                self.memory_store.record_interaction(request, response)
                self.audit_logger.record(
                    "response.completed",
                    request_id=request.request_id,
                    fields={"status": response.status, "mcp_event_count": 0},
                )
                return response

            memory_summary = self.memory_store.recent_summary()
            mcp_events = self.mcp_client.describe_available_tools(
                prompt=request.prompt,
                confirmed_tools=request.confirmed_tools,
            )
            for event in mcp_events:
                self.audit_logger.record(
                    "mcp.decision",
                    request_id=request.request_id,
                    fields=event.to_dict(),
                )

            mcp_results = self.mcp_client.execute_allowed_tools(mcp_events)
            for result in mcp_results:
                self.audit_logger.record(
                    "mcp.executed",
                    request_id=request.request_id,
                    fields={
                        "tool_name": result.tool_name,
                        "status": result.status,
                        "message": result.message,
                    },
                )

            tool_count = len(mcp_events)
            pending_count = sum(
                1 for event in mcp_events if event.permission == "confirmation_required"
            )
            confirmed_count = sum(1 for event in mcp_events if event.permission == "confirmed")
            tool_output = self._mcp_result_summary(mcp_results)

            message = (
                "Ze recebeu a intencao e esta operando no backend local do MVP v0.1.\n\n"
                f"Entrada: {request.prompt}\n\n"
                f"{memory_summary}\n"
                f"MCP client carregado com {tool_count} contrato(s) de ferramenta.\n\n"
                f"Confirmacoes MCP pendentes: {pending_count}. Confirmadas: {confirmed_count}.\n\n"
                f"{tool_output}"
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
            self.audit_logger.record(
                "response.completed",
                request_id=request.request_id,
                fields={
                    "status": response.status,
                    "mcp_event_count": len(mcp_events),
                    "mcp_result_count": len(mcp_results),
                },
            )
            return response
        except Exception as exc:
            self.audit_logger.record(
                "response.failed",
                request_id=request.request_id,
                fields={"error": str(exc)},
            )
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

    def _mcp_result_summary(self, results: list[MCPToolResult]) -> str:
        if not results:
            return ""

        lines = ["Ferramentas MCP executadas:"]
        for result in results:
            lines.append(f"- {result.tool_name}: {result.message}")
            summary = result.output.get("summary")
            if summary:
                lines.append(summary)
        lines.append("")
        return "\n".join(lines) + "\n"
