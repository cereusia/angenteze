# Execucao Segura do C3PO/CEPO

Versao documental: `0.1.0-draft.8`.

## Objetivo

C3PO/CEPO pode validar documentacao, versao, lint, testes e arvore combinada sem
transformar o papel de integracao em executor arbitrario ou instalador.

Este contrato permanece `SPEC`; nao ativa runtime.

## Perfil `INTEGRATION_VALIDATION`

- Um unico owner por branch de integracao.
- Comandos exatos declarados no baton.
- Somente scripts pertencentes ao repositorio e vinculados ao SHA revisado.
- Rede `DENY` por padrao.
- Segredos `DENY`.
- Instalacao implicita `DENY`.
- Comando shell arbitrario `DENY`.
- Alteracao de runtime `DENY`.
- Arvore fonte e metadados `.git` read-only durante validadores.
- Outputs gravaveis limitados a pathset separado e declarado.
- Output root efemero fora da arvore fonte e de `.git`, usando realpaths
  canonicalizados, sem `..`, escape por symlink ou path nao resolvido.
- HEAD, branch, fronteira de integracao, refs, status, stage e digests comparados
  antes e depois.
- Build em ambiente isolado quando executar codigo do repositorio.
- Politica MCP e `critical: DENY` continuam soberanas.

## Manifesto de comando

```yaml
schema_version: 1
validation_id: REQUIRED
state: AUTHORIZED
handoff_binding:
  handoff_ref: REQUIRED_IMMUTABLE_GIT_SHA_REFERENCE
  handoff_id: REQUIRED
  handoff_digest_sha256: REQUIRED
  source_owner_id: REQUIRED
  target_agent: c3po-cepo
  repository_id: REQUIRED
  head_sha: REQUIRED
  branch: REQUIRED
  worktree_id: REQUIRED
  source_root_realpath: REQUIRED
  exact_pathset_digest_sha256: REQUIRED
repository_id: REQUIRED
head_sha: REQUIRED
branch: REQUIRED
worktree_id: REQUIRED
integration_boundary_id: REQUIRED
working_directory: REQUIRED
source_root_realpath: REQUIRED
git_metadata_realpath: REQUIRED
output_root_realpath: REQUIRED
output_root_ephemeral: true
runner_policy_id: c3po-direct-runner-policy-v1
runner_policy_digest_sha256: REQUIRED
runner_id: ruby-script-v1
runner_executable_realpath: /usr/bin/ruby
runner_executable_digest_sha256: REQUIRED
direct_exec_only: true
arbitrary_shell: DENY
inline_code: DENY
command_argv:
  - REQUIRED
command_source_argv_index: REQUIRED
command_source_path: REQUIRED
command_source_realpath: REQUIRED
command_source_digest_sha256: REQUIRED
authorized_source_pathset:
  - REQUIRED
authorized_source_pathset_digest_sha256: REQUIRED
expected_outputs:
  - REQUIRED
expected_exit_codes:
  - 0
timeout_seconds: REQUIRED
network: DENY
secrets: DENY
installation: DENY
runtime_mutation: DENY
isolated_environment: REQUIRED
source_tree_read_only: true
git_metadata_read_only: true
writable_output_pathset:
  - REQUIRED
before:
  head_sha: REQUIRED
  branch: REQUIRED
  integration_boundary_id: REQUIRED
  worktree_digest_sha256: REQUIRED
  git_status_digest_sha256: REQUIRED
  stage_digest_sha256: REQUIRED
  git_refs_digest_sha256: REQUIRED
  output_inventory_digest_sha256: REQUIRED
authorization:
  owner_identity: REQUIRED
  approval_id: REQUIRED
  validation_scope_digest_sha256: REQUIRED
  evidence: REQUIRED
  approved_at: REQUIRED
  expires_at: REQUIRED
  revoked_at: null
```

`DRAFT` omite `authorization`, `before`, `after` e `observed`. `AUTHORIZED` e
`RUNNING` exigem somente autorizacao vigente e prova `before`; eles proíbem
fabricar `after` ou resultado antecipado. Ao terminar, o registro muda para
`PASS` ou `BLOCKED` e acrescenta:

```yaml
after:
  head_sha: REQUIRED
  branch: REQUIRED
  integration_boundary_id: REQUIRED
  worktree_digest_sha256: REQUIRED
  git_status_digest_sha256: REQUIRED
  stage_digest_sha256: REQUIRED
  git_refs_digest_sha256: REQUIRED
  output_inventory_digest_sha256: REQUIRED
  source_mutation_count: REQUIRED
  git_metadata_mutation_count: REQUIRED
  outside_output_root_mutation_count: REQUIRED
observed:
  result: PASS_OR_BLOCKED_OR_NOT_RUN
  exit_code: REQUIRED_OR_NULL
  started_at: REQUIRED
  finished_at: REQUIRED
  stdout_digest_sha256: REQUIRED
  stderr_digest_sha256: REQUIRED
  output_artifacts:
    - identifier: REQUIRED
      realpath: REQUIRED
      digest_sha256: REQUIRED
```

`PASS` exige os tres contadores de mutacao iguais a zero, HEAD, branch,
fronteira, refs, arvore, status e stage invariaveis, exit code permitido e todos
os outputs esperados presentes. Uma divergencia deve ser registrada como
`BLOCKED`, nunca apagada para satisfazer o schema.

Um bloqueio de preflight usa `state: BLOCKED`, `blocked_phase: PRECHECK`,
`observed.result: NOT_RUN`, timestamps nulos e lista de outputs vazia; ele nao
fabrica provas `before` ou `after`. Bloqueios em `RUN` ou `POSTCHECK` registram
as provas reais antes/depois e `observed.result: BLOCKED`.

Schema: `agents/schemas/c3po-integration-validation.schema.json`.

O binding resolve `handoff_ref` no commit imutavel, valida o
`c3po_cepo_handoff_v1` completo e recalcula seu digest. ID, owner, repositorio,
HEAD, branch, worktree e pathset sao derivados desse artefato e devem coincidir.
O source root, working
directory, `.git`, comando, argv, indice da fonte, outputs, timeout, ambiente e
politicas integram o payload canonico `c3po_validation_scope_v1`. A autorizacao
aprova o digest desse payload completo e exige `approved_at < agora <
expires_at` e `revoked_at: null`. Qualquer divergencia ou handoff obsoleto
produz `BLOCKED_VALIDATION`.

Argumentos sao representados como lista, e `command_source_argv_index` e inteiro
nao negativo que aponta exatamente para o realpath da fonte autorizada. O
primeiro argumento deve ser o executable realpath do runner permitido. O
executor usa chamada direta equivalente a `execve`, sem shell, expansao ou
codigo inline; `sh -c`, `ruby -e`, `python -c` e equivalentes falham fechados
mesmo quando o digest do escopo foi novamente aprovado. A fonte, o
working directory, o `.git` e todo pathset fonte devem estar dentro do source
root do repositorio. Substituicao de comando, fonte externa, glob amplo,
variavel nao resolvida, download, `curl | shell`, instalacao dinamica e execucao
fora do working directory declarado falham fechados.

O validador nao possui permissao de integrar. Depois que a execucao terminar e
provar zero mutacao fora do output root, C3PO/CEPO pode receber um baton Git
separado para integrar os commits ja atribuiveis.

## Isolamento do output

O owner resolve `source_root_realpath`, `git_metadata_realpath`,
`output_root_realpath` e cada item do pathset antes da autorizacao. O output root
deve ser efemero, externo e disjunto da arvore fonte e de `.git`; todos os
outputs observados devem permanecer dentro dele. Segmento `..`, link simbolico
que escape, path inexistente sem parent resolvido ou mutacao fora da raiz produz
`BLOCKED_VALIDATION`.

## Categorias permitidas

- Parser de YAML ou JSON ja disponivel no ambiente.
- Lint documental ja versionado no repositorio.
- Teste unitario ou de integracao declarado pelo owner.
- Build reproduzivel sem rede e sem instalacao implicita.
- Verificacao Git read-only e `git diff --check`.

A categoria permitida nao autoriza automaticamente qualquer comando; o argv,
fonte e SHA continuam obrigatorios.

Politica documental dos runners: `agents/validation/c3po-runner-policy.yaml`.
Ela permanece com `runtime_enabled: false`.

## Condicoes de parada

- comando nao declarado ou fonte divergente;
- tentativa de rede, segredo ou instalacao;
- script alterado depois da aprovacao;
- mudanca na arvore fonte, `.git`, status ou stage causada pelo validador;
- pathset ou working directory fora da fronteira;
- timeout, falha de isolamento ou output inesperado;
- teste que tenta alterar servico, banco, credencial ou producao;
- HEAD, branch, stage ou owner divergente.

## Saida

C3PO/CEPO registra comando, ambiente, SHA, resultado, outputs minimizados,
falhas, drift e proximo gate. Ele nao corrige silenciosamente a causa da falha.
