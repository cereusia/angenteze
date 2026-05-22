# ADR 0005 - Fronteira Clean-Room para Referencias Externas

Status: Proposto

Data: 2026-05-22

## Contexto

O repositorio local contem `ReferenciasTecnicas/claude-code`, um projeto externo usado como referencia tecnica.

O arquivo de licenca da referencia declara que o codigo e `UNLICENSED`, proprietario e nao redistribuivel. O Agente Ze pretende ser open source sob GNU AGPL v3.

## Decisao

Nao incorporar codigo, arquivos ou implementacoes diretas da referencia.

Permitir apenas:

- analise de arquitetura em alto nivel;
- padroes genericos reimplementados do zero;
- documentacao de decisoes;
- validacao propria no Agente Ze.

Adicionar `ReferenciasTecnicas/` ao `.gitignore` para reduzir risco de commit acidental.

## Consequencias

- O Agente Ze preserva caminho open source.
- O projeto evita dependencia legal de codigo proprietario vazado.
- Ideias uteis podem entrar por reimplementacao limpa.
- O trabalho exige documentar origem da inspiracao e manter diffs proprios.

## Validacao

- `git status` deve manter `ReferenciasTecnicas/` fora do versionamento.
- Commits de codigo nao devem incluir arquivos da referencia.
- Novos comportamentos inspirados devem ter testes proprios.
