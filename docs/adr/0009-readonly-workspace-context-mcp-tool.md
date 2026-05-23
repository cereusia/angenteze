# ADR 0009 - Primeira Ferramenta MCP Real Somente Leitura

Status: Proposto

Data: 2026-05-23

## Contexto

O registry MCP ja existe, mas ate agora as ferramentas eram contratos sem execucao real. A primeira ferramenta real deve ser de baixo risco, local, sem rede, sem escrita e util para continuidade.

## Decisao

Implementar `agenteze.workspace.context_read` como ferramenta MCP real de leitura segura.

Escopo:

- risco `low`;
- sem rede;
- sem escrita em filesystem;
- sem execucao de processo externo;
- leitura apenas de caminhos documentais esperados;
- resultado: resumo de Git, modulos principais, memoria documental, specs e proximas acoes.

## Consequencias

- O fluxo MCP passa a executar uma capacidade real com baixo risco.
- A ferramenta ajuda continuidade entre sessoes.
- Ferramentas com escrita ou automacao continuam exigindo confirmacao e ADR especifico.

## Alternativas Consideradas

- Comecar por ferramenta de escrita em memoria.
- Comecar por ferramenta de shell local.
- Manter MCP apenas documental por mais uma etapa.

## Validacao

- Teste Python cobre execucao da ferramenta.
- Auditoria registra decisao e execucao.
- A ferramenta nao cria arquivos, nao chama rede e nao executa subprocesso.
