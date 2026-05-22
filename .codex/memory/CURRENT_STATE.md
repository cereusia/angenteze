# Current State

Data: 2026-05-22

## Estado Atual

- Workspace local: `/Users/roberto/ProjetosCereus/AgenteZe`.
- Fase: primeira base executavel do MVP v0.1.
- Codigo de app: SwiftPM em `apps/macos`.
- Codigo Python: backend local em `agent-core/agenteze_core`.
- MCP real: contrato/registry local inicial em `mcp/registry.json`; sem servidor MCP real.
- Permissao MCP: policy local inicial no `agent-core`, com `low` permitido, `medium`/`high` pendentes de confirmacao e `critical` negado.
- Confirmacao MCP: UI no prompt macOS para confirmar/negar ferramentas pendentes; confirmacao reenvia o prompt com `--confirm-tool`, sem execucao real.
- Referencia `claude-code`: analisada em modo clean-room; codigo nao deve ser copiado nem versionado.
- Comandos locais: `/help`, `/status`, `/memory` e `/mcp` implementados no `agent-core`.
- Memoria SQLite real: schema inicial em `memory/schema.sql`, runtime em `.ze/agenteze.sqlite3`.
- Personagem 3D: especificacao, blueprint Blender, referencias, contrato de interacao, mapa de emocoes/animacoes e manifest JSON criados em `docs/character/` e `assets/character/agente-ze/`.
- Git local: inicializado na branch `main`.
- Commit inicial local: criado com a mensagem `docs: bootstrap Agente Ze project`.
- Remoto: ainda nao configurado.

## Documentos Criados

- `AGENTS.md`
- `DIAGNOSTICO_INICIAL.md`
- `LICENSE`
- `README.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `specs/VISION.md`
- `specs/ARCHITECTURE.md`
- `specs/AGENTS.md`
- `specs/MCP.md`
- `specs/SECURITY.md`
- `docs/adr/0000-template.md`
- `docs/adr/0001-base-local-first.md`
- `.github/workflows/docs.yml`
- `.github/workflows/ci.yml`
- `apps/macos/Package.swift`
- `agent-core/agenteze_core/`
- `memory/schema.sql`
- `mcp/registry.json`
- `scripts/run-agent-core.sh`
- `scripts/test-python.sh`
- `scripts/build-macos.sh`
- `script/build_and_run.sh`
- `docs/adr/0002-swiftui-python-process-bridge.md`
- `docs/adr/0003-mcp-permission-model.md`
- `docs/adr/0004-mcp-confirmation-ui.md`
- `docs/adr/0005-clean-room-reference-boundary.md`
- `docs/research/claude-code-reference-analysis.md`
- `docs/character/agente-ze-character-spec.md`
- `docs/character/agente-ze-emotion-system.md`
- `docs/character/agente-ze-animation-map.md`
- `docs/character/agente-ze-interaction-contract.md`
- `docs/character/agente-ze-implementation-plan.md`
- `docs/character/agente-ze-specialists.md`
- `assets/character/agente-ze/agente-ze.character.json`
- `assets/character/agente-ze/blender/BLENDER_MODEL_BLUEPRINT.md`
- `assets/character/agente-ze/references/`

## Riscos Abertos

- Confirmar nome definitivo do remoto: `angenteze` ou `agenteze`.
- Definir empacotamento final do Python junto ao app macOS.
- Expandir comandos locais seguros e contexto Git/memoria.
- Implementar execucao real de ferramentas MCP atras da confirmacao.
- Definir retencao/exclusao de memoria.
- Evoluir logs auditaveis.
- Iniciar modelagem Blender a partir do board visual e do blueprint.
