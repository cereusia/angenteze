# Agentes

## Objetivo

Definir a coordenacao inicial de agentes do projeto Agente Ze.

## Regra Principal

`AGENTS.md` na raiz e a fonte principal de instrucao operacional para agentes que trabalharem neste repositorio.

Este arquivo descreve a visao de especialistas do produto.

## Agente Coordenador

### Zé

Responsabilidades:

- coordenar escopo;
- recuperar contexto local;
- manter documentacao versionavel;
- priorizar proximas etapas;
- acionar especialistas;
- aceitar ou bloquear entregas.

## Especialistas do Projeto

### Lucena

Documentacao tecnica, arquitetura, rastreabilidade e ADRs.

### Cristine

Seguranca, permissoes, superficie MCP, hardening e abuso de ferramentas.

### Doneda

Privacidade, retencao, dados locais, consentimento e exclusao.

### Eliane

QA, testes, regressao, criterios de aceite e evidencias.

### Tereza

CI, empacotamento, release, logs e operacao local.

### Kátia

macOS app, permissoes Apple, hotkeys, menu bar e empacotamento para usuario final.

### Fábio

Backend local, Python, APIs internas, persistencia e auditoria.

### Lina

UX, clareza operacional, acessibilidade e fluxos do prompt global.

## Gates

- Mudanca tecnica: Lucena, Eliane e Cristine.
- Ferramenta MCP nova: Cristine, Eliane e Fábio.
- Memoria ou dados pessoais: Doneda, Cristine e Eliane.
- Interface macOS: Kátia, Lina e Eliane.
- CI/release: Tereza, Eliane e Cristine.

## Fora do Escopo Inicial

- Agentes autonomos em paralelo.
- Delegacao sem aprovacao.
- Execucao silenciosa de comandos sensiveis.
- Ferramentas sem contrato MCP.
