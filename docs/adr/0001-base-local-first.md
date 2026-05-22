# ADR 0001 - Base Local-First e MCP-First

Status: Proposto

Data: 2026-05-22

## Contexto

O Agente Ze precisa operar no macOS como assistente local, com memoria persistente, ferramentas auditaveis e caminho de evolucao open source.

O projeto ainda esta em fase documental. A primeira decisao arquitetural deve limitar o escopo para evitar automacao perigosa ou dependencia excessiva de servicos externos.

## Decisao

Adotar uma base local-first e MCP-first:

- SwiftUI cuida da interface macOS.
- Python cuida do nucleo de agente.
- SQLite guarda a memoria local inicial.
- MCP e o protocolo principal para ferramentas.
- Acoes sensiveis exigem confirmacao e auditoria.

## Consequencias

- O app pode evoluir com menor acoplamento entre UI, agente e ferramentas.
- O nucleo Python pode ser testado sem depender da interface macOS.
- Ferramentas MCP precisam de politica de permissao desde o inicio.
- A comunicacao SwiftUI/Python ainda precisa de ADR especifico.

## Alternativas Consideradas

- App monolitico SwiftUI com toda a logica local.
- Backend remoto como dependencia primaria.
- Automacao direta sem contrato MCP.

## Validacao

Esta decisao sera validada quando o projeto tiver:

- app macOS minimo chamando backend local;
- backend Python respondendo a comandos simples;
- memoria SQLite inicial;
- primeira ferramenta MCP de baixo risco;
- logs auditaveis sem segredos.
