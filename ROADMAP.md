# Roadmap

## P0 - Base Documental

Objetivo: preparar o projeto antes de codigo.

- Criar `AGENTS.md` raiz. Concluido localmente.
- Criar specs iniciais. Concluido localmente.
- Criar `CONTRIBUTING.md`. Concluido localmente.
- Confirmar nome do repositorio remoto. Concluido: `cereusia/angenteze`.
- Inicializar Git local. Concluido localmente.
- Conectar remoto. Concluido.
- Adicionar `LICENSE` com GNU AGPL v3. Concluido localmente.
- Normalizar `README.md`. Concluido e publicado.

## P1 - Fundacao do Repositorio

Objetivo: deixar o projeto pronto para contribuicao.

- Definir estrutura final de pastas.
- Criar `docs/adr/`. Concluido localmente.
- Criar template de ADR. Concluido localmente.
- Criar GitHub Actions minimo para checks de documentacao. Concluido localmente.
- Definir convencao de commits e PRs.

## P2 - App macOS Minimo

Objetivo: criar o shell SwiftUI.

- Menu bar app. Concluido localmente.
- Janela/painel de prompt. Concluido localmente.
- Hotkey global. Concluido localmente.
- Estado basico de conexao com backend local. Concluido localmente.
- Configuracao local minima. Parcial.

## P3 - Agent Core Minimo

Objetivo: criar o nucleo Python local.

- Entrada de prompt. Concluido localmente.
- Resposta estruturada. Concluido localmente.
- Registro de eventos. Concluido localmente.
- Politica inicial de permissao. Parcial.
- API local simples para o app. Concluido como processo local JSON.
- Comandos slash locais. Parcial: `/help`, `/status`, `/doctor`, `/git`, `/memory`, `/mcp`.

## P4 - Memoria Local

Objetivo: persistir contexto minimo com SQLite.

- Schema inicial. Concluido localmente.
- Configuracoes. Parcial.
- Historico. Concluido localmente.
- Eventos de ferramenta. Parcial.
- Retencao e exclusao. Pendente.

## P5 - MCP Inicial

Objetivo: conectar ferramentas por contrato.

- Cliente MCP. Concluido como contrato local.
- Registry de ferramentas. Concluido localmente.
- Primeira ferramenta de leitura segura. Parcial: contrato local de baixo risco.
- Logs auditaveis. Parcial.
- Confirmacao para execucao sensivel. Parcial: policy e UI de confirmacao criadas; execucao real pendente.

## P6 - Agentes Especialistas

Objetivo: organizar especialistas sem autonomia excessiva.

- Definir manifestos dos agentes.
- Integrar gates documentais.
- Adicionar criterios de aceite por agente.

## P7 - Release Open Source

Objetivo: preparar distribuicao inicial.

- README completo. Concluido.
- Licenca AGPL v3. Concluido.
- CI com testes reais. Concluido inicial.
- Guia de instalacao local. Concluido inicial.
- Politica de seguranca. Concluido inicial.
- Release notes. Concluido para `v0.1.0-alpha.1`.
- Clone limpo de release. Pendente.
- Tag `v0.1.0-alpha.1`. Pendente.

## Criterio de Avanco

Cada fase deve terminar com:

- documentacao atualizada;
- validacao proporcional;
- riscos conhecidos registrados;
- decisao tecnica importante registrada como ADR.
