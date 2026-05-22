# Diagnostico Inicial

Data: 2026-05-22

## Resumo

O workspace local existe em `/Users/roberto/ProjetosCereus/AgenteZe`. Na verificacao inicial, ele ainda nao estava inicializado como repositorio Git. Depois da preparacao local, foi inicializado em `main`, sem remoto configurado e sem publicacao.

A estrutura atual e um esqueleto de projeto com diretorios para app macOS, nucleo Python, MCP, agentes, memoria, scripts, testes e assets.

Nao ha codigo de aplicacao ainda. Na varredura inicial havia tres arquivos versionaveis encontrados:

- `.gitignore`
- `.codex/PROJECT_RULES.md`
- `specs/MILESTONE_V0_1.md`

Durante a validacao final, tambem foi observado `README.md`. Ele precisa ser normalizado porque contem marcadores de comando shell dentro do proprio Markdown.

O remoto informado, `https://github.com/cereusia/angenteze.git`, respondeu a `git ls-remote`, mas nao retornou refs de branches ou tags no momento da verificacao.

## Estrutura Atual Encontrada

```text
.
├── .codex/
│   └── PROJECT_RULES.md
├── .github/
│   └── workflows/
├── .ze/
├── agent-core/
├── agents/
│   ├── architect/
│   ├── browser/
│   ├── developer/
│   ├── mcp/
│   ├── researcher/
│   └── ze/
├── apps/
│   └── macos/
├── assets/
│   ├── branding/
│   ├── character/
│   └── logo/
├── docs/
├── mcp/
├── memory/
├── scripts/
├── specs/
│   └── MILESTONE_V0_1.md
└── tests/
```

## O Que Ja Existe

- Identidade inicial em `.codex/PROJECT_RULES.md`: Agente Ze, CereusIA, "transformar intencao em acao".
- Direcao arquitetural inicial: modular, escalavel, open source, MCP First, API First.
- Stack desejada ja registrada: SwiftUI, Python e automacoes em Python.
- Regras iniciais de seguranca: nao executar comandos destrutivos sem confirmacao, automacao auditavel e logs estruturados.
- Marco `v0.1` em `specs/MILESTONE_V0_1.md` com foco em menu bar, hotkey global, prompt global, backend local, memoria local e MCP client.
- Diretorios preparados para separacao modular, mas ainda vazios.

## O Que Falta

- Inicializacao Git local ou clonagem correta do remoto.
- `AGENTS.md` raiz como fonte principal de instrucao para agentes.
- Licenca `GNU AGPL v3` materializada em `LICENSE`.
- README publico normalizado.
- Especificacoes minimas de visao, arquitetura, MCP, seguranca e agentes.
- ADRs para decisoes importantes.
- Estrutura real do app SwiftUI.
- Estrutura real do `agent-core` Python.
- Contrato inicial do SQLite local.
- Contrato MCP: ferramentas permitidas, permissao, auditoria, logs e erros.
- CI em GitHub Actions.
- Politica de contribuicao, testes e seguranca.
- Testes automatizados.
- Processo de release.

## Lacunas e Riscos

- **Git local recem-inicializado:** ha commit inicial local, mas ainda nao ha remoto configurado.
- **Remoto possivelmente vazio:** `git ls-remote --heads --tags` nao retornou refs.
- **Nome do remoto:** a URL usa `angenteze`; confirmar se esse e o nome definitivo ou se deveria ser `agenteze`.
- **Escopo v0.1 precisa ficar pequeno:** voz, navegador, automacao ampla e multiagente ja estao fora do primeiro marco.
- **Permissoes locais no macOS:** hotkey global, menu bar e automacao futura exigem politica clara de consentimento.
- **MCP pode virar superficie de risco:** ferramentas locais devem ter allowlist, auditoria e confirmacao para acoes sensiveis.
- **Memoria local exige privacidade desde o inicio:** SQLite deve separar configuracao, historico, logs e dados sensiveis.

## Estrutura Inicial Ideal

```text
.
├── AGENTS.md
├── CONTRIBUTING.md
├── DIAGNOSTICO_INICIAL.md
├── LICENSE
├── README.md
├── ROADMAP.md
├── .codex/
│   └── PROJECT_RULES.md
├── .github/
│   └── workflows/
├── agent-core/
├── apps/
│   └── macos/
├── docs/
│   └── adr/
├── mcp/
├── memory/
├── scripts/
├── specs/
│   ├── VISION.md
│   ├── ARCHITECTURE.md
│   ├── AGENTS.md
│   ├── MCP.md
│   ├── SECURITY.md
│   └── MILESTONE_V0_1.md
└── tests/
```

## Fronteiras do Escopo Inicial

Dentro do escopo:

- Documentacao inicial.
- Definicao de arquitetura modular.
- Definicao de seguranca local-first.
- Preparacao para SwiftUI, Python, SQLite e MCP.
- Preparacao para contribuicao open source.

Fora do escopo da primeira base executavel:

- Acabamento visual.
- Servidores MCP reais.
- Automacao de sistema operacional.
- Browser, voz e multiagente completo.
- Publicacao de release.

## Especialistas e Gates

- Zé: coordenacao e aceite final.
- Lucena: consistencia tecnica e rastreabilidade documental.
- Cristine: seguranca, permissoes, hardening e abuso de ferramentas.
- Doneda: privacidade, retencao e dados locais.
- Eliane: QA, criterios de aceite e evidencias.
- Tereza: CI, release, logs e operacao local.
- Kátia: app macOS, permissoes do sistema e empacotamento Apple.

## Proximo Passo Recomendado

Confirmar o nome definitivo do repositorio remoto antes de conectar `origin`.
