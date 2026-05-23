# Agente Ze v0.1.0-alpha.1

Data: 2026-05-23

Primeira release alpha do Agente Ze, projeto open source da CereusIA para criar um agente global local-first para macOS.

## Destaques

- App macOS SwiftUI com menu bar.
- Hotkey global `Control + Option + Command + Space`.
- Prompt principal para enviar intencoes ao backend local.
- Backend Python com respostas JSON estruturadas.
- Memoria local inicial com SQLite.
- Registry MCP inicial e politica de permissao por risco.
- Fluxo de confirmacao para ferramentas MCP que exigem aprovacao.
- Comandos locais `/help`, `/status`, `/doctor`, `/git`, `/memory` e `/mcp`.
- Documentacao base de arquitetura, seguranca, MCP, agentes e roadmap.
- Identidade visual inicial com logo e personagem Agente Ze.

## Instalacao Local

```bash
git clone git@github.com:cereusia/angenteze.git
cd angenteze
./scripts/test-python.sh
./scripts/build-macos.sh
```

## Execucao

Backend local:

```bash
./scripts/run-agent-core.sh run --prompt "status"
```

App macOS:

```bash
./script/build_and_run.sh
```

## Limites Conhecidos

- O app ainda nao e empacotado, assinado ou notarizado.
- O backend Python ainda depende da toolchain local.
- MCP ainda opera como contrato local; execucao real de ferramentas fica para etapa futura.
- A memoria SQLite ainda nao possui politica completa de retencao/exclusao.
- Automacao ampla, voz, browser e multiagente completo estao fora desta alpha.

## Validacao Esperada

- `git diff --check`
- `./scripts/test-python.sh`
- `./scripts/build-macos.sh`
- clone limpo do GitHub com os mesmos checks.
