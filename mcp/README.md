# MCP

Contratos MCP iniciais do Agente Ze.

## v0.1

O MVP carrega um registry local de ferramentas para estabelecer o contrato entre backend e MCP.

Ainda nao ha servidor MCP real nem automacao de sistema operacional.

## Politica

- Toda ferramenta deve declarar risco.
- Acoes sensiveis exigem confirmacao.
- O backend deve registrar eventos auditaveis.
- Nenhum segredo deve aparecer em logs.

## Permissoes

Riscos iniciais:

- `low`: permitido quando nao exige confirmacao.
- `medium`: exige confirmacao.
- `high`: exige confirmacao.
- `critical`: negado no MVP v0.1.

Ferramentas sem nome, com risco invalido ou marcadas como `enabled: false` sao negadas.

## Confirmacao no App

Ferramentas `medium` e `high` ativadas por intencao retornam `confirmation_required`.

O app macOS pode reenviar a mesma requisicao com `--confirm-tool <nome>` para marcar a ferramenta como `confirmed`.

No MVP v0.1, confirmacao nao executa ferramentas reais.
