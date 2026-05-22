# Arquitetura

## Objetivo

Definir uma arquitetura inicial simples para evoluir o Agente Ze sem acoplar app macOS, nucleo de agente, memoria e ferramentas.

## Componentes

```text
apps/macos      -> SwiftUI menu bar, hotkey e interface local
agent-core      -> nucleo Python de orquestracao
memory          -> SQLite local e politicas de retencao
mcp             -> clientes, servidores e contratos MCP
agents          -> definicoes de agentes especialistas
docs/adr        -> decisoes tecnicas importantes
tests           -> testes proporcionais por modulo
```

## Fluxo Inicial

```text
Usuario
  -> Hotkey/Menu Bar SwiftUI
  -> Prompt local
  -> agent-core Python
  -> Memoria SQLite
  -> Cliente MCP
  -> Ferramenta permitida
  -> Resultado auditado
  -> App macOS
```

## App macOS

Responsabilidades:

- abrir o prompt global;
- mostrar estado do agente;
- enviar comandos ao backend local;
- exibir resultado;
- solicitar confirmacao para acoes sensiveis;
- manter configuracao minima.

Nao deve conter:

- logica complexa de agente;
- regras de memoria;
- implementacao direta de ferramentas sensiveis.

## Agent Core

Responsabilidades:

- receber intencoes do app;
- montar contexto;
- consultar memoria;
- chamar ferramentas MCP;
- aplicar politicas de permissao;
- devolver resposta estruturada;
- registrar eventos auditaveis.

## Memoria Local

Memoria inicial em SQLite, com separacao logica entre:

- configuracoes;
- historico de interacoes;
- eventos de ferramenta;
- preferencias;
- indices futuros.

Qualquer dado sensivel deve ter politica de retencao e exclusao.

## MCP

MCP sera o protocolo principal para ferramentas. O nucleo deve tratar ferramentas como capacidades externas com contrato, permissao e auditoria.

## CI

GitHub Actions deve ser introduzido de forma incremental:

- lint/documentacao primeiro;
- testes Python quando `agent-core` existir;
- build macOS quando o projeto SwiftUI existir;
- checks de seguranca quando houver dependencias reais.

## ADRs

Toda decisao tecnica importante deve virar ADR em `docs/adr/`.

Exemplos:

- escolha de comunicacao entre SwiftUI e Python;
- formato do banco SQLite;
- modelo de permissao MCP;
- estrategia de empacotamento macOS;
- politica de logs e retencao.
