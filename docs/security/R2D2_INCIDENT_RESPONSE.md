# Contrato de Incident Response do R2D2

Versao documental: `0.1.0-draft.8`.

## Estado

Este contrato e documental. `INCIDENT_RESPONSE` nao esta ativado no runtime e
nao concede acesso a producao.

## Regra break-glass

Uma acao em producao durante incidente exige simultaneamente:

- incidente real identificado;
- Roberto como autoridade humana direta, sem delegacao neste contrato;
- Tereza como owner operacional da producao;
- R2D2 como lider tecnico do incidente;
- Cristine como garantia de seguranca;
- Doneda quando houver dados pessoais;
- ativo, acao, identidade, janela e rollback exatos;
- credencial temporaria e minima;
- logging independente;
- encerramento e revogacao obrigatorios.

O perfil `INCIDENT_RESPONSE`, uma confirmacao generica ou a urgencia do incidente
nao substitui nenhum desses requisitos.

## Estados

```text
DRAFT -> AUTHORIZED -> ACTIVE -> CONTAINED -> RECOVERED -> CLOSED
              |           |
              +-> REVOKED <-+
```

Somente `AUTHORIZED` pode entrar em `ACTIVE`. `REVOKED` interrompe novas acoes e
inicia contencao segura. `CLOSED` exige revogacao e recibo.

Cada transicao registra a referencia imutavel com SHA da revisao anterior, o
digest canonico recalculado, horario, identidade e evidencia. O primeiro
`DRAFT` usa estado, referencia e digest anterior nulos. O consumidor resolve o
envelope fechado por `r2d2-state-transition-record.schema.json`, recalcula o
digest e extrai dele o estado; objeto lateral, referencia ausente, schema
incompleto, digest divergente ou escalar contraditorio bloqueia a transicao.
O `record_id` resolvido deve ser igual a `incident_id`; em toda transicao
posterior, a revisao anterior deve ser exatamente `revision - 1`. O primeiro
`DRAFT` nao referencia predecessor e usa `revision: 1`.

## Registro minimo

```yaml
schema_version: 1
incident_id: REQUIRED
revision: REQUIRED_POSITIVE_INTEGER
state: AUTHORIZED
transition:
  from_state: DRAFT
  to_state: AUTHORIZED
  previous_record_ref: REQUIRED_GIT_SHA256_URI
  previous_record_digest_sha256: REQUIRED
  changed_at: REQUIRED
  changed_by_identity: roberto
  transition_evidence: REQUIRED
severity: REQUIRED

authorization:
  scope_actions_digest_sha256: REQUIRED
  executor_identity: REQUIRED
  executor_must_differ_from_approvers: true
  roberto_approval:
    approval_id: REQUIRED
    identity: roberto
    approved_scope_actions_digest_sha256: REQUIRED
    evidence: REQUIRED
    approved_at: REQUIRED
    expires_at: REQUIRED
    revoked_at: null
    revoked_by_identity: null
  tereza_approval:
    approval_id: REQUIRED
    identity: tereza
    approved_scope_actions_digest_sha256: REQUIRED
    evidence: REQUIRED
    approved_at: REQUIRED
    expires_at: REQUIRED
    revoked_at: null
    revoked_by_identity: null

ownership:
  incident_lead: r2d2-global
  production_owner: tereza
  security_assurance: cristine
  privacy_reviewer: doneda_or_not_applicable
  qa_reviewer: eliane

scope:
  scope_digest_sha256: REQUIRED
  canonicalization_version: r2d2-c14n-v1
  payload_type: incident_scope_actions_v1
  environment: REQUIRED
  exact_assets:
    - REQUIRED
  excluded_assets:
    - REQUIRED
  allowed_actions:
    - REQUIRED
  prohibited_actions:
    - REQUIRED

credentials:
  identity: REQUIRED
  scopes:
    - REQUIRED
  issued_at: REQUIRED
  expires_at: REQUIRED
  revocation_owner: REQUIRED
  values_must_not_be_recorded: true

execution:
  start_at: REQUIRED
  stop_at: REQUIRED
  exact_commands_or_runbook: REQUIRED
  independent_log_destination: REQUIRED
  rollback_plan: REQUIRED
  rollback_owner: tereza
  kill_switch:
    method: REQUIRED
    channel_or_endpoint: REQUIRED
    operator_identity: REQUIRED
    operator_must_differ_from_executor: true
    tested_at: REQUIRED
    test_valid_until: REQUIRED
    test_result: PASS
    automatic_stop_on_control_loss: true

data:
  classification: REQUIRED
  personal_data: false
  doneda_gate: NOT_APPLICABLE
  evidence_location: REQUIRED
  evidence_digest_sha256: REQUIRED
  retention_until: REQUIRED
  deletion_owner: REQUIRED
```

Um registro `DRAFT` omite `authorization` e `closure`. Para entrar em
`AUTHORIZED`, as duas aprovacoes acima devem estar presentes, validas, nao
expiradas, nao revogadas e vinculadas ao mesmo digest de escopo e acoes. O
executor deve ser diferente dos dois aprovadores. `closure` so existe em
`CLOSED` ou `REVOKED`:

```yaml
closure:
  credentials_revoked: REQUIRED
  processes_stopped: REQUIRED
  persistence_removed: REQUIRED
  rollback_or_recovery_result: REQUIRED
  residual_risk_owner: roberto
  c3po_cepo_handoff_v1: REQUIRED
```

Schema estrutural: `agents/schemas/incident-response.schema.json`.
Comparacoes de identidade, tempo, revogacao e digest usam
`agents/validation/r2d2-semantic-rules.yaml`. Os tres valores de digest —
registro, aprovacao de Roberto e aprovacao de Tereza — devem corresponder ao
payload recalculado conforme `docs/security/R2D2_CANONICAL_DIGESTS.md`.

## Acoes permitidas

- Leitura e coleta minimizada previstas no escopo.
- Contencao reversivel prevista no runbook.
- Mudanca produtiva exata aprovada por Roberto e executada sob ownership de
  Tereza, com aprovacao atribuivel de ambos.
- Recuperacao, verificacao e coleta de evidencias vinculadas ao incidente.

## Acoes proibidas

- Usar o incidente para obter acesso amplo ou permanente.
- Executar exploracao ofensiva em producao.
- Ampliar ativos ou comandos sem nova autorizacao e novo digest.
- Registrar valores de segredo.
- Desabilitar logging, monitoramento ou kill switch.
- Manter credencial, processo ou persistencia depois do encerramento.
- Fazer release fora do baton de Tereza.
- Aceitar risco em nome de Roberto.

## Encerramento

Antes de `CLOSED`:

1. Revogar identidades e credenciais temporarias.
2. Parar processos e acessos emergenciais.
3. Remover persistencia temporaria.
4. Confirmar recuperacao ou rollback.
5. Preservar evidencia minimizada e cadeia de custodia.
6. Registrar risco residual e decisoes humanas.
7. Encaminhar o handoff ao C3PO/CEPO.
8. Produzir pos-incidente e testes de regressao.
