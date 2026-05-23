# MVP v0.1 Release Checklist

Data: 2026-05-23

## Alvo

- Versao: `v0.1.0-alpha.1`.
- Branch: `main`.
- Remoto: `git@github.com:cereusia/angenteze.git`.
- Escopo: primeira base executavel do Agente Ze.

## Escopo Incluido

- App macOS SwiftUI via SwiftPM.
- Menu bar app.
- Hotkey global: `Control + Option + Command + Space`.
- Janela de prompt principal.
- Backend local Python via processo local.
- Memoria SQLite inicial.
- Registry MCP local.
- Politica MCP local de permissao.
- UI de confirmacao MCP.
- Comandos slash: `/help`, `/status`, `/doctor`, `/git`, `/memory`, `/mcp`.
- CI inicial com testes Python e build macOS.
- README publico com logo e personagem.
- Specs, ADRs e memoria local do projeto.

## Fora do Escopo

- Voz.
- Browser embutido.
- Automacao ampla no macOS.
- Execucao real de ferramentas MCP sensiveis.
- Multiagente completo.
- Empacotamento assinado/notarizado.
- Distribuicao para usuario final.

## Gates de Release

| Gate | Status | Evidencia |
| --- | --- | --- |
| Worktree local limpo antes da release | Pendente | `git status --short --branch` |
| Testes Python locais | Pendente | `./scripts/test-python.sh` |
| Build macOS local | Pendente | `./scripts/build-macos.sh` |
| Clone limpo do GitHub | Pendente | clone temporario de `origin/main` |
| Testes Python em clone limpo | Pendente | `./scripts/test-python.sh` |
| Build macOS em clone limpo | Pendente | `./scripts/build-macos.sh` |
| Documentacao de permissao macOS | Concluido | `docs/security/MACOS_PERMISSIONS.md` |
| Release notes | Concluido | `docs/release/MVP_V0_1_RELEASE_NOTES.md` |
| Tag `v0.1.0-alpha.1` | Pendente | `git tag` e `git push origin v0.1.0-alpha.1` |

## Validacao Local

```bash
git diff --check
./scripts/test-python.sh
./scripts/build-macos.sh
```

## Validacao por Clone Limpo

```bash
git clone git@github.com:cereusia/angenteze.git agenteze-release-check
cd agenteze-release-check
./scripts/test-python.sh
./scripts/build-macos.sh
```

## Criterio de Aceite

A release `v0.1.0-alpha.1` so pode ser publicada quando:

- os checks locais passarem;
- o clone limpo do GitHub passar;
- o README apontar para assets versionados;
- a memoria local refletir o estado publicado;
- a tag apontar para um commit ja enviado ao remoto.
