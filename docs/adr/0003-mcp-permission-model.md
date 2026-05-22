# ADR 0003 - Modelo de Permissao MCP

Status: Proposto

Data: 2026-05-22

## Contexto

O Agente Ze deve usar MCP como protocolo principal de ferramentas, mas o MVP v0.1 ainda nao deve executar automacoes amplas, comandos destrutivos, browser ou multiagente autonomo.

Mesmo sem servidor MCP real, o backend precisa validar contratos de ferramenta antes de trata-los como disponiveis para o app macOS.

## Decisao

Adicionar uma politica local de permissao MCP no `agent-core`.

Cada ferramenta registrada deve declarar:

- `name`;
- `description`;
- `category`;
- `risk`;
- `requires_confirmation`;
- `scope`;
- `audit`;
- schemas de entrada e saida.

A politica inicial usa quatro riscos:

- `low`: permitido no MVP quando nao exigir confirmacao;
- `medium`: exige confirmacao antes de execucao;
- `high`: exige confirmacao antes de execucao;
- `critical`: negado no MVP v0.1.

Ferramentas desabilitadas, sem nome ou com risco invalido sao negadas.

## Consequencias

- O app pode mostrar ferramentas MCP com decisao de permissao explicita.
- O backend ja diferencia ferramenta disponivel, pendente de confirmacao e negada.
- A base continua sem executar ferramentas reais.
- A UI de confirmacao ainda precisa ser definida antes de ferramentas `medium` ou `high`.

## Alternativas Consideradas

- Permitir qualquer ferramenta registrada.
- Bloquear todo MCP ate existir servidor real.
- Delegar permissao somente para UI macOS.

## Validacao

- Testes Python cobrem ferramenta `low`, ferramenta `medium`, ferramenta `critical` e risco invalido.
- O runtime registra eventos MCP em SQLite para auditoria inicial.
