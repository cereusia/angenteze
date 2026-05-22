# MCP

## Objetivo

Usar MCP como protocolo principal de ferramentas do Agente Ze.

## Principios

- Ferramentas devem ser explicitas.
- Ferramentas devem ter contrato claro.
- Acoes sensiveis exigem confirmacao.
- Toda execucao relevante deve ser auditavel.
- Servidores locais devem usar transporte local por padrao.
- Nenhuma ferramenta deve receber segredos sem necessidade.

## Modelo Inicial

```text
agent-core
  -> registro de ferramentas
  -> politica de permissao
  -> cliente MCP
  -> servidor MCP local
  -> resultado estruturado
  -> log auditavel
```

## Classes de Ferramentas

### Leitura

Baixo risco quando limitada ao workspace autorizado.

Exemplos futuros:

- listar arquivos;
- ler metadados;
- consultar memoria local.

### Escrita

Risco medio. Deve ter escopo e registro.

Exemplos futuros:

- criar arquivo;
- atualizar documento;
- gravar memoria.

### Execucao

Risco alto. Deve exigir confirmacao quando puder alterar sistema, rede, processos, credenciais ou arquivos fora do workspace.

Exemplos futuros:

- rodar comando shell;
- instalar dependencia;
- acionar automacao macOS.

## Politica de Permissao

Cada ferramenta deve declarar:

- nome;
- descricao;
- entradas;
- saidas;
- escopo permitido;
- nivel de risco;
- necessidade de confirmacao;
- politica de log;
- erros esperados.

Modelo inicial:

- `low`: permitido quando `requires_confirmation` for `false`.
- `medium`: pendente de confirmacao.
- `high`: pendente de confirmacao.
- `critical`: negado no MVP v0.1.
- risco invalido, ferramenta sem nome ou ferramenta desabilitada: negado.

## Auditoria

Registrar, no minimo:

- horario;
- ferramenta chamada;
- entrada resumida;
- decisao de permissao;
- resultado;
- erro, se houver.

Nao registrar segredos em claro.

## Decisoes Futuras

Virar ADR:

- biblioteca MCP Python;
- modelo de registry;
- transporte padrao;
- formato de logs;
- UI de confirmacao;
- politica de sandbox.
