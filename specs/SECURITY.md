# Seguranca

## Objetivo

Definir a linha minima de seguranca para um agente local que pode operar ferramentas do macOS.

## Principios

- Local-first.
- Menor privilegio.
- Confirmacao antes de risco.
- Auditoria sem vazamento de segredo.
- Ferramentas em allowlist.
- Falha segura.
- Dados sensiveis com retencao clara.

## Ameacas Iniciais

- Prompt injection contra ferramentas locais.
- Execucao de comando destrutivo.
- Leitura indevida de arquivos fora do escopo.
- Vazamento de segredos em logs.
- Persistencia excessiva na memoria SQLite.
- Ferramenta MCP mal definida ou permissiva demais.
- Confusao entre sugestao e execucao.

## Regras Minimas

- Nao executar comandos destrutivos sem confirmacao explicita.
- Nao mover, apagar ou sobrescrever arquivos sem justificativa.
- Nao armazenar tokens, chaves ou senhas em claro.
- Nao enviar dados locais para servicos externos sem aprovacao.
- Toda ferramenta MCP deve ter nivel de risco definido.
- Toda acao sensivel deve gerar evento auditavel.

## Memoria SQLite

A memoria inicial deve separar:

- configuracao;
- historico;
- eventos de ferramenta;
- preferencias;
- dados temporarios.

Campos sensiveis devem ser evitados. Quando inevitaveis, precisam de retencao, exclusao e mascaramento.

## macOS

Permissoes como acessibilidade, automacao, arquivos, notificacoes e hotkeys devem ser solicitadas apenas quando necessarias.

O app deve explicar o motivo operacional da permissao antes de solicitar.

## MCP

Ferramentas devem comecar restritas.

Padrao inicial:

- leitura local: permitida dentro do workspace;
- escrita local: permitida apenas em escopo aprovado;
- execucao: confirmacao obrigatoria;
- rede: confirmacao obrigatoria ate haver politica clara.
- risco `critical`: negado no MVP v0.1.

Nenhum perfil de agente, regra de engajamento, incidente, confirmacao ou
manifesto documental pode sobrepor o registry, a allowlist, o sandbox ou a
decisao `critical: DENY` do MVP. A politica executavel mais restritiva sempre
prevalece.

## Responsaveis

- R2D2: coordenacao e execucao tecnica do programa de seguranca, sempre sob
  perfil, escopo e gate aprovados.
- Cristine: garantia independente de seguranca, abuso e risco; nao substitui o
  executor e nao revisa trabalho de sua propria autoria.
- Doneda: privacidade e retencao.
- Eliane: validacao e regressao.
- Tereza: operacao, logs e release.

## ADRs Necessarios

- Politica de permissao.
- Modelo de auditoria.
- Retencao de memoria.
- Sandbox de ferramentas.
- Comunicacao SwiftUI/Python.
