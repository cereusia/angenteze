# Permissoes macOS

Data: 2026-05-23

## Objetivo

Registrar as permissoes esperadas do app macOS no MVP v0.1 e as permissoes que podem ser necessarias no futuro.

## Estado Atual

O app macOS atual:

- roda como app SwiftUI via SwiftPM;
- usa `RegisterEventHotKey` para a hotkey global;
- chama o backend Python com `Process`;
- resolve o diretorio do projeto localmente;
- nao solicita permissao de acessibilidade;
- nao solicita automacao de outros apps;
- nao solicita acesso amplo a arquivos fora do workspace;
- nao solicita notificacoes.

## Hotkey Global

Atalho atual:

```text
Control + Option + Command + Space
```

Implementacao:

- arquivo: `apps/macos/Sources/AgenteZe/Services/HotKeyController.swift`;
- API: Carbon `RegisterEventHotKey`;
- uso: abrir ou ocultar a janela principal do prompt.

Risco:

- baixo no MVP, porque a hotkey apenas abre a interface;
- deve haver tratamento de falha quando o atalho ja estiver em uso.

## Acessibilidade

Status atual: nao usada.

Quando pode ser necessaria:

- controlar outros apps;
- ler elementos da UI;
- clicar, digitar ou automatizar interfaces de terceiros;
- implementar operador local amplo.

Regra:

- pedir apenas quando houver uma funcionalidade concreta;
- explicar a finalidade operacional antes de solicitar;
- manter acao sensivel atras de confirmacao explicita.

## Automacao Apple Events

Status atual: nao usada.

Quando pode ser necessaria:

- controlar Finder, Terminal, navegador ou apps de produtividade;
- executar tarefas inter-app.

Regra:

- manter allowlist por app e acao;
- registrar eventos auditaveis;
- negar por padrao em caso de ambiguidade.

## Execucao Local do Python

Status atual: usada.

Implementacao:

- arquivo: `apps/macos/Sources/AgenteZe/Services/BackendClient.swift`;
- executavel: `/usr/bin/env python3`;
- modulo: `agenteze_core`;
- ambiente: define `AGENTEZE_ROOT` e `PYTHONPATH`.

Riscos:

- Python ausente ou versao incompativel;
- path local incorreto;
- stderr ou stdout contendo dados sensiveis;
- empacotamento futuro sem runtime Python definido.

Regras:

- manter respostas estruturadas em JSON;
- nao imprimir segredos em logs;
- validar ambiente com `/doctor`;
- decidir empacotamento em ADR antes de distribuicao para usuario final.

## Arquivos e Memoria Local

Status atual:

- runtime SQLite em `.ze/agenteze.sqlite3`;
- schema versionado em `memory/schema.sql`;
- `.ze/` ignorado por Git.

Regras:

- nao versionar memoria runtime;
- definir retencao e exclusao antes de armazenar dados sensiveis;
- mascarar segredos em logs e respostas.

## Proximas Decisoes

- ADR de empacotamento Python no app macOS.
- ADR de politica de acessibilidade e automacao.
- ADR de auditoria local.
- ADR de retencao/exclusao de memoria.
