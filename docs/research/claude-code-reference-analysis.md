# Analise Clean-Room: `ReferenciasTecnicas/claude-code`

Data: 2026-05-22

## Decisao de Licenca

O projeto em `ReferenciasTecnicas/claude-code` nao pode ser incorporado diretamente ao Agente Ze.

Motivo: o arquivo `LICENSE` da referencia declara `UNLICENSED` e informa que o codigo e proprietario, nao open source e nao redistribuivel.

Regra para este repositorio:

- nao copiar codigo fonte;
- nao copiar arquivos;
- nao importar dependencias por imitacao;
- nao versionar a pasta de referencia;
- usar apenas padroes arquiteturais genericos, reimplementados do zero.

## Especialistas Acionados

- Lucena: arquitetura, rastreabilidade e ADR.
- Fábio: backend local e contratos.
- Cristine: licenca, seguranca e permissao de ferramentas.
- Lina: fluxo de uso e comandos.
- Eliane: validacao e regressao.

## Estrutura Observada em Alto Nivel

Sem copiar implementacao, a referencia contem cerca de 2.500 arquivos fora de `.git`, com diretorios de comandos, ferramentas, UI terminal, MCP, memoria, plugins, servidor, bridge, estado, configuracao e testes.

Pastas observadas em alto nivel:

- `src/commands/`: comandos slash e operacionais.
- `src/tools/`: ferramentas do agente.
- `src/components/`: componentes de UI terminal.
- `src/services/`: integracoes e servicos internos.
- `src/services/mcp/`: integracao MCP.
- `src/memdir/` e `src/services/SessionMemory`: memoria persistente.
- `src/bridge/`: comunicacao com ambientes externos.
- `src/coordinator/`: coordenacao multiagente.
- `src/context/`: coleta de contexto.
- `src/keybindings/`: atalhos e entrada.
- `src/screens/`: telas de fluxo.
- `src/server/`: modo servidor/daemon.
- `docs/`: documentacao de arquitetura, comandos, ferramentas, bridge e subsistemas.

Padroes uteis identificados:

- registry de comandos;
- registry de ferramentas;
- camada de permissao por ferramenta;
- coleta de contexto do projeto;
- memoria global/projeto;
- comandos locais e comandos que viram prompt;
- integracao MCP;
- separacao entre UI, servicos, comandos, ferramentas e estado;
- validacao e gates por risco.

## O Que Foi Incorporado

Incorporado por reimplementacao propria no Agente Ze:

- sistema minimo de comandos slash no `agent-core`;
- comandos `/help`, `/status`, `/memory` e `/mcp`;
- snapshot de contexto local do projeto;
- documentacao de fronteira de referencia externa;
- protecao para nao versionar `ReferenciasTecnicas/`.

## Mapeamento para Agente Ze

| Padrao da referencia | Adoção no Agente Ze |
|---|---|
| Registry de comandos | `agent-core/agenteze_core/commands.py` |
| Contexto local | `agent-core/agenteze_core/context.py` |
| Registry de ferramentas | `mcp/registry.json` |
| Permissoes por ferramenta | `agent-core/agenteze_core/permissions.py` |
| Memoria persistente | `memory/schema.sql` + `MemoryStore` |
| UI de confirmacao | `PromptView` no app macOS |
| Documentacao de decisoes | `docs/adr/` |

## O Que Nao Foi Incorporado

- codigo TypeScript;
- React/Ink;
- Bun;
- SDKs proprietarios;
- servidor MCP da referencia;
- sistema de plugins;
- telemetria externa;
- OAuth;
- voice;
- bridge IDE;
- qualquer arquivo do projeto de referencia.

## Backlog Seguro

Possiveis proximas incorporacoes clean-room:

1. Historico de sessoes.
2. Registry de ferramentas executaveis atras de confirmacao MCP.
3. Comandos de diagnostico local.
4. Contexto Git resumido.
5. Templates de prompts operacionais.
6. Configuracao por projeto em `.agenteze/`.

## Gates

- Qualquer novo comportamento inspirado em referencia externa deve ter ADR.
- Qualquer ferramenta que escreva arquivos deve passar por confirmacao MCP.
- Qualquer codigo novo deve ser escrito no estilo do Agente Ze, em Python/Swift, sem copiar trechos da referencia.
