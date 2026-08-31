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

## Especialistas em Especificacao P6

Os agentes desta secao possuem somente contrato documental. Eles nao estao
ativados no runtime, nao alteram o escopo inicial e nao autorizam itens fora
dele.

### R2D2

Lider tecnico e de ciberseguranca responsavel por pesquisa, levantamento,
SPECs, arquitetura, ambientes, engenharia segura, acompanhamento evolutivo e
coordenacao sob demanda de Red Team e Blue Team.

R2D2 opera por perfis de menor privilegio. Nao recebe acesso irrestrito, nao
executa atividade ofensiva sem regras de engajamento e nao aprova sozinho uma
correcao que implementou.

Manifestos:

- `agents/r2d2/manifest.yaml`;
- `agents/r2d2/red-team.yaml`;
- `agents/r2d2/blue-team.yaml`.

### C3PO/CEPO

C3PO e CEPO sao duas formas de invocacao da mesma identidade canônica
`c3po-cepo`.

Responsavel por documentacao, versionamento, lint, rastreabilidade e integracao
Git serial. Deve existir uma unica instancia escritora por fronteira de
integracao. Nao implementa features, nao substitui QA ou seguranca e nao faz
release ou deploy.

Manifesto:

- `agents/c3po-cepo/manifest.yaml`.

## Gates

- Mudanca tecnica: Lucena, Eliane e Cristine.
- Ferramenta MCP nova: Cristine, Eliane e Fábio.
- Memoria ou dados pessoais: Doneda, Cristine e Eliane.
- Interface macOS: Kátia, Lina e Eliane.
- CI/release: Tereza, Eliane e Cristine.
- SPEC, arquitetura ou desenvolvimento de R2D2: Lucena, Eliane e Cristine.
- Red Team: Roberto, R2D2, Cristine e revisor independente, com regras de
  engajamento e laboratorio isolado.
- Blue Team: R2D2, Eliane e Cristine; adicionar Doneda quando houver dados.
- Integracao C3PO/CEPO: owner de origem, gates proporcionais e Zé; release
  permanece com Tereza.

## Fora do Escopo Inicial

- Agentes autonomos em paralelo.
- Delegacao sem aprovacao.
- Execucao silenciosa de comandos sensiveis.
- Ferramentas sem contrato MCP.
- Teste ofensivo sem alvo e autorizacao explicitos.
- Instalacao automatica de plugins, distros ou scanners.
- Acesso irrestrito ou permanente a producao.
