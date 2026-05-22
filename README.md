# Agente Ze

Agente Ze e um projeto open source da CereusIA para criar um assistente global de macOS baseado em Codex, MCP, automacao local, memoria persistente e agentes especialistas.

## Visao

Transformar intencao em acao com um operador local, auditavel e seguro.

## Stack Pretendida

- SwiftUI para app macOS/menu bar.
- Python para o nucleo local do agente.
- SQLite para memoria local inicial.
- MCP como protocolo principal de ferramentas.
- GitHub Actions para CI.

## Status

Projeto em fase inicial executavel do MVP v0.1.

Ja existe:

- backend local Python;
- memoria SQLite inicial;
- registry MCP local;
- politica local de permissao MCP;
- UI de confirmacao MCP;
- app macOS SwiftUI via SwiftPM;
- menu bar app;
- hotkey global;
- prompt principal;
- CI inicial.

## Documentos Principais

- `AGENTS.md`
- `DIAGNOSTICO_INICIAL.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `specs/VISION.md`
- `specs/ARCHITECTURE.md`
- `specs/MCP.md`
- `specs/SECURITY.md`

## Escopo v0.1

- Menu bar app.
- Hotkey global.
- Prompt global.
- Backend local.
- Memoria local.
- MCP client.

Fora do v0.1: voz, browser embutido, automacao ampla e multiagente completo.

## Execucao Local

Backend:

```bash
./scripts/run-agent-core.sh run --prompt "status"
```

Testes Python:

```bash
./scripts/test-python.sh
```

Build macOS:

```bash
./scripts/build-macos.sh
```

Run macOS:

```bash
./script/build_and_run.sh
```

## Comandos Locais

O prompt aceita comandos slash reimplementados no `agent-core`:

- `/help`
- `/status`
- `/memory`
- `/mcp`

## Licenca

GNU Affero General Public License v3.0. Veja `LICENSE`.
