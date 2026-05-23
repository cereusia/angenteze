# ADR 0007 - Retencao e Exclusao da Memoria SQLite

Status: Proposto

Data: 2026-05-23

## Contexto

A memoria local SQLite registra interacoes e eventos MCP. Mesmo local-first, historico pode conter dados sensiveis se o usuario inserir esse conteudo no prompt.

## Decisao

Adotar uma politica inicial conservadora:

- nao gravar segredos, tokens, chaves ou senhas intencionalmente;
- tratar prompts e respostas como dados locais sensiveis;
- manter `.ze/agenteze.sqlite3` fora do Git;
- implementar comando futuro de limpeza seletiva antes de ampliar memoria;
- separar configuracao, historico, eventos MCP e preferencias;
- registrar dados minimos suficientes para continuidade e auditoria.

Retencao padrao proposta para MVP:

- historico de interacoes: local, sem sync, ate limpeza explicita;
- eventos MCP: local, sem sync, ate limpeza explicita;
- logs auditaveis: local, rotacionaveis futuramente, fora do Git;
- segredos: nao armazenar.

## Consequencias

- O projeto preserva continuidade sem expor dados no repositorio.
- O usuario continua responsavel pelo conteudo sensivel digitado localmente.
- Antes de automacao real, sera necessario criar exclusao/limpeza e mascaramento mais fortes.

## Alternativas Consideradas

- Nao persistir historico.
- Persistir tudo sem politica de retencao.
- Criptografar a SQLite ja no MVP v0.1.

## Validacao

- `.ze/` e arquivos SQLite continuam ignorados por Git.
- Testes confirmam persistencia basica.
- Auditoria nao deve registrar segredos em claro.
