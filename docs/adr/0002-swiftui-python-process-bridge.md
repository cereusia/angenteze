# ADR 0002 - Bridge SwiftUI/Python por Processo Local

Status: Proposto

Data: 2026-05-22

## Contexto

O MVP v0.1 precisa conectar o app macOS em SwiftUI ao backend local em Python sem introduzir servidor HTTP, dependencias externas ou empacotamento complexo antes da hora.

## Decisao

Usar um processo local Python chamado pelo app macOS:

- SwiftUI envia o prompt ao `agent-core`.
- `agent-core` responde JSON em stdout.
- O app decodifica `AgentResponse`.
- `AGENTEZE_ROOT` e `PYTHONPATH` definem o contexto local.

## Consequencias

- A base compila e roda sem dependencias externas.
- O contrato entre UI e backend fica claro e testavel.
- A latencia e aceitavel para o MVP.
- O empacotamento final ainda precisara decidir como distribuir Python e recursos locais.

## Alternativas Consideradas

- Servidor HTTP local.
- XPC.
- Backend embutido em Swift.
- WebSocket local.

## Validacao

- `./scripts/test-python.sh`
- `./scripts/build-macos.sh`
- `./scripts/run-agent-core.sh run --prompt "status"`
