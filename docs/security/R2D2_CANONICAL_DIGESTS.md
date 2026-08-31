# Canonicalizacao de Digests do R2D2

Versao documental: `0.1.0-draft.8`.

## Estado

Este contrato define somente a representacao documental usada para calcular e
comparar digests. Nao ativa parser, runtime, agente, ferramenta ou acesso.

Identificador da representacao: `r2d2-c14n-v1`.

## Algoritmo

1. Selecionar exatamente os campos enumerados para o tipo de payload.
2. Remover somente o digest autorreferente explicitamente nomeado na secao do
   payload e o envelope externo de autorizacao. Digests aninhados enumerados
   fazem parte do payload e devem ser preservados. Assinaturas, segredos e
   valores de credencial nunca entram, salvo referencia ou fingerprint publico
   expressamente enumerado.
3. Normalizar texto para UTF-8, Unicode NFC, quebras de linha LF e sem BOM.
4. Representar timestamps em RFC 3339 UTC, com segundos e sufixo `Z`.
5. Ordenar chaves de objetos lexicograficamente pelo texto normalizado.
6. Preservar a ordem de listas operacionais; listas declaradas como conjuntos
   sao deduplicadas e ordenadas lexicograficamente.
7. Usar JSON compacto, sem espacos, com booleanos e `null` nativos. Numeros de
   ponto flutuante sao proibidos nesta versao.
8. Calcular SHA-256 sobre os bytes UTF-8 e registrar 64 caracteres hexadecimais
   minusculos.

Qualquer campo ausente, tipo inesperado, texto sem normalizacao, algoritmo ou
versao desconhecida produz `DENY_INVALID_DIGEST_INPUT`.

## Payloads cobertos

### `red_team_scope_actions_v1`

- `engagement_id`;
- `objective`;
- `scope.included_assets` e `scope.excluded_assets` como conjuntos;
- `scope.ownership_or_permission_evidence`;
- `environment`;
- `techniques.allowed` e `techniques.prohibited` como conjuntos;
- `limits`;
- categorias e expiracao de `credentials`, nunca seus valores.

### `incident_scope_actions_v1`

- `incident_id` e `severity`;
- `scope.environment`;
- `scope.exact_assets`, `excluded_assets`, `allowed_actions` e
  `prohibited_actions` como conjuntos;
- janela, runbook, rollback e kill switch de `execution`;
- identidade e escopos de `credentials`, nunca seus valores.

Roberto e Tereza aprovam individualmente o mesmo digest
`incident_scope_actions_v1`. Divergencia entre qualquer aprovacao, o registro e
o valor recalculado produz `BLOCKED_INCIDENT`.

### `r2d2_gate_catalog_v1`

- `identity.canonical_id` e `identity.version` do manifesto R2D2;
- para cada gate: `id`, `when`, `fact`, `owner`, `evidence` e
  `pass_condition`;
- gates ordenados por `id`.

O handoff registra versao e digest desse catalogo. Gate desconhecido, duplicado,
ausente ou catalogo divergente produz `BLOCKED_INTEGRATION`.

### `r2d2_state_transition_record_v1`

- os sete campos fechados de `r2d2-state-transition-record.schema.json`;
- `record_schema`, `record_type`, `record_id`, `revision` e `state`;
- `artifact_ref` imutavel contendo o SHA Git e `artifact_digest_sha256`.

O digest prova qual revisao anterior originou a transicao; ele nao autoriza uma
transicao fora da maquina de estados. O consumidor resolve a referencia no
store/commit imutavel, valida o objeto fechado, recalcula o digest e extrai
`state` desse objeto. Objeto fornecido ao lado da referencia ou escalar alegando
o estado anterior e rejeitado como side channel. Alem do digest, a cadeia exige
que o `record_id` do predecessor seja o ID do registro atual e que a revisao do
predecessor seja exatamente a revisao atual menos um. O primeiro `DRAFT` usa
revisao 1 e nao possui predecessor; isso impede replay entre cadeias e revisoes.

### `r2d2_task_context_v1`

- objeto completo validado por `r2d2-task-context.schema.json`;
- identidade e versao do extrator;
- repositorio, base SHA, HEAD e digest do exact pathset;
- conjunto completo de fatos de aplicabilidade;
- `source_bundle_ref`, `source_bundle_digest_sha256` e
  `extractor_digest_sha256`; esses digests aninhados sao preservados.

O contexto e um artefato externo ao handoff. O handoff guarda sua referencia,
ID, digest, producer e a referencia/digest do recibo de verificacao
independente. O consumidor resolve e recalcula contexto, source bundle, recibo,
policy de confianca e atestado de identidade; o extrator deterministico deriva
os fatos do source bundle. Verifier fora da allowlist, credential fingerprint
divergente, autoverificacao ou source bundle adulterado falham fechados.

### `r2d2_context_verification_receipt_v1`

Payload fechado pelos campos de
`r2d2-context-verification-receipt.schema.json`, exceto exclusivamente
`receipt_digest_sha256`, que e o digest autorreferente. Todos os demais campos,
inclusive digests do contexto, source bundle, extrator, trust policy e atestado
de identidade, sao preservados no calculo. Campo extra, ausente ou digest
divergente produz `BLOCKED_INTEGRATION`.

### `r2d2_c3po_handoff_v1`

- objeto completo validado por `r2d2-c3po-cepo-handoff.schema.json`;
- digest calculado sem adicionar o proprio digest externo de binding;
- arrays preservam a ordem registrada, exceto conjuntos explicitamente
  definidos por este contrato.

### `exact_pathset_v1`

- paths absolutos resolvidos por realpath;
- cada item normalizado pelas regras gerais;
- itens deduplicados e ordenados lexicograficamente antes do JSON compacto.

### `c3po_validation_scope_v1`

- binding integral do handoff: referencia imutavel, ID, digest, owner, target,
  repositorio, HEAD, branch, worktree e digest do pathset;
- repositorio, HEAD, branch, worktree, fronteira de integracao, working
  directory, source root, `.git` e output root;
- policy e identidade do runner, executable realpath/digest, execucao direta,
  shell arbitrario e inline code negados;
- `command_argv`, indice nao negativo da fonte, path/realpath da fonte e digest
  recalculado;
- source pathset e writable output pathset, com seus digests;
- outputs e exit codes esperados, timeout e ambiente isolado;
- politicas de rede, segredos, instalacao, runtime e read-only.

O objeto de autorizacao nao entra no payload. Ele registra o digest
`c3po_validation_scope_v1`, owner, vigencia, revogacao e evidencia. Qualquer
mudanca em argv, source root, worktree, boundary, pathset, output, timeout ou
politica depois da aprovacao altera o digest e produz `BLOCKED_VALIDATION`.

## Evidencia

O valor recalculado deve ser produzido a partir do artefato exato vinculado ao
SHA ou versao revisada. A comparacao e de bytes/digest, nao apenas de texto
descritivo. Nenhum digest substitui autorizacao, ownership ou gate humano.
