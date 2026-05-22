# Agente Ze - Instrucoes para Agentes

## Identidade

Voce esta trabalhando no Agente Ze, projeto open source da CereusIA para criar um agente global de macOS baseado em Codex, MCP, automacao local, memoria persistente e agentes especialistas.

Missao do produto: transformar intencao em acao com controle, auditoria e seguranca local-first.

## Ordem de Contexto

Antes de agir, leia nesta ordem:

1. `AGENTS.md`
2. `.codex/PROJECT_RULES.md`
3. `specs/`
4. `ROADMAP.md`
5. documentos em `docs/`
6. codigo existente

## Regras Gerais

- Seja minimalista.
- Prefira documentacao clara a abstracao prematura.
- Nao escreva codigo quando a tarefa pedir apenas diagnostico ou especificacao.
- Nao adicione dependencias sem justificativa.
- Nao execute comandos destrutivos sem confirmacao explicita.
- Nao mova nem delete arquivos sem justificar.
- Nao armazene segredos, tokens, chaves ou senhas.
- Toda decisao tecnica importante deve virar ADR futuramente.

## Stack Pretendida

- SwiftUI para app macOS/menu bar.
- Python para `agent-core`.
- SQLite para memoria local inicial.
- MCP como protocolo principal de ferramentas.
- GitHub Actions para CI.
- GNU AGPL v3 como licenca pretendida.

## Arquitetura Esperada

- `apps/macos/`: app SwiftUI.
- `agent-core/`: nucleo Python local.
- `memory/`: SQLite, schemas e politicas de memoria.
- `mcp/`: contratos e integracoes MCP.
- `agents/`: especialistas e manifestos.
- `specs/`: especificacoes versionadas.
- `docs/adr/`: decisoes tecnicas.
- `tests/`: validacoes automatizadas.

## Gates

- Mudancas tecnicas exigem validacao proporcional.
- Mudancas de MCP exigem revisao de seguranca.
- Mudancas de memoria exigem revisao de privacidade.
- Mudancas de UX exigem criterio de aceite claro.
- Mudancas de CI/release exigem reproducibilidade.

## Especialistas

- Zé: coordenacao, memoria e aceite final.
- Lucena: documentacao tecnica e arquitetura.
- Cristine: seguranca.
- Doneda: privacidade.
- Eliane: QA.
- Tereza: CI, release e operacao.
- Kátia: app macOS e permissoes.
- Fábio: backend local Python.
- Lina: UX e acessibilidade.

## Estado Inicial

O projeto esta em fase documental. Antes de implementar SwiftUI, Python, SQLite ou MCP real, mantenha as specs atualizadas e registre decisoes relevantes.
