# ADR 0008 - Auditoria Local em JSONL

Status: Proposto

Data: 2026-05-23

## Contexto

O Agente Ze precisa registrar comandos, decisoes MCP, confirmacoes e erros antes de executar automacao real. Esses logs ajudam QA e seguranca, mas nao podem virar artefato publico acidental.

## Decisao

Adicionar auditoria local em JSONL:

- caminho padrao: `.ze/logs/audit.jsonl`;
- formato: um JSON por linha;
- logs fora do Git;
- campos sensiveis devem ser mascarados por chave;
- prompts nao devem ser gravados em claro; registrar apenas metadados como tamanho e tipo;
- mensagens de ferramenta devem ser resumidas/truncadas;
- falha de escrita de log nao deve derrubar o backend.

## Consequencias

- A execucao fica mais observavel.
- Os logs podem ser usados em debugging local.
- Ainda sera necessario rotacionar e limpar logs em etapa futura.
- Logs nunca devem ser commitados.

## Alternativas Consideradas

- Registrar apenas em SQLite.
- Usar logs livres em texto.
- Nao ter auditoria ate MCP real.

## Validacao

- Testes Python verificam escrita de evento.
- `.ze/logs/` permanece ignorado.
- `git status` nao deve listar logs runtime.
