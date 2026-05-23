# Agent Core

Backend local do Agente Ze.

## Execucao

```bash
./scripts/run-agent-core.sh run --prompt "status"
./scripts/run-agent-core.sh run --prompt "/context"
./scripts/run-agent-core.sh status
```

## Responsabilidades

- Receber intencoes do app macOS.
- Consultar e atualizar memoria local SQLite.
- Expor respostas JSON estaveis para o app.
- Carregar o registry MCP local.
- Resumir contexto local seguro para continuidade.
- Registrar auditoria local em `.ze/logs/audit.jsonl`.
- Manter acoes sensiveis fora do v0.1.

## Fora do v0.1

- Automacao ampla do sistema.
- Browser.
- Voz.
- Multiagente autonomo.
