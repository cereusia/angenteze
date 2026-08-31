# Regras de Engajamento do R2D2 Red Team

Versao documental: `0.1.0-draft.8`.

## Regra principal

Nenhuma atividade ofensiva, exploracao, scan ativo ou simulacao adversarial pode
comecar apenas por existir um manifesto, ferramenta, plugin, modelo ou acesso ao
host. E obrigatoria uma ROE imutavel em estado `AUTHORIZED`, aprovada diretamente
por Roberto. Esta autoridade ofensiva nao e delegavel.

O executor nao pode ser o aprovador. Divergencia de identidade, versao, digest,
estado, alvo, janela ou revogacao produz `BLOCKED_ROE`.

## Estados e transicoes

```text
DRAFT -> AUTHORIZED -> ACTIVE -> CLOSED
              |           |
              +-> REVOKED <-+
```

- Somente `AUTHORIZED` pode iniciar um exercicio.
- A entrada em `ACTIVE` registra executor, ambiente e horario reais.
- `REVOKED` interrompe imediatamente qualquer atividade.
- `CLOSED` exige limpeza e recibo de encerramento.
- Qualquer transicao diferente das listadas e invalida.

## Registro obrigatorio para inicio

O template possui schema em
`agents/schemas/red-team-engagement.schema.json`.

```yaml
schema_version: 1
roe_version: 0.1.0
engagement_id: REQUIRED
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

authorization:
  authorization_id: REQUIRED
  approved_by_identity: roberto
  executor_identity: REQUIRED
  executor_must_differ_from_approver: true
  approved_at: REQUIRED
  expires_at: REQUIRED
  revoked_at: null
  revoked_by_identity: null
  authorization_evidence: REQUIRED

objective:
  description: REQUIRED
  success_criteria: REQUIRED

scope:
  scope_digest_sha256: REQUIRED
  canonicalization_version: r2d2-c14n-v1
  payload_type: red_team_scope_actions_v1
  immutable_after_authorized: true
  included_assets:
    - REQUIRED
  excluded_assets:
    - REQUIRED
  ownership_or_permission_evidence: REQUIRED

environment:
  lab_id: REQUIRED
  attacker_environment: REQUIRED
  target_environment: REQUIRED
  network_boundary: REQUIRED
  production: false

techniques:
  allowed:
    - REQUIRED
  prohibited:
    - destructive_payloads
    - uncontrolled_denial_of_service
    - real_data_exfiltration
    - unauthorized_persistence
    - target_expansion

limits:
  start_at: REQUIRED
  stop_at: REQUIRED
  request_rate: REQUIRED
  resource_limit: REQUIRED
  data_handling: REQUIRED

credentials:
  required_categories: []
  temporary: true
  expires_at: REQUIRED
  values_must_not_be_recorded: true

monitoring:
  independent_log_destination: REQUIRED
  observers:
    - REQUIRED
  kill_switch:
    method: REQUIRED
    channel_or_endpoint: REQUIRED
    operator_identity: REQUIRED
    operator_must_differ_from_executor: true
    tested_at: REQUIRED
    test_valid_until: REQUIRED
    test_result: PASS
    automatic_stop_on_control_loss: true
  emergency_contact: REQUIRED

evidence:
  allowed_location: REQUIRED
  classification: REQUIRED
  purpose: REQUIRED
  legal_or_operational_basis: REQUIRED
  sanitization: REQUIRED
  encryption: REQUIRED
  access_control: REQUIRED
  digest_sha256: REQUIRED
  retention_until: REQUIRED
  deletion_owner: REQUIRED
  chain_of_custody: REQUIRED
  contains_personal_data: false
  doneda_gate: NOT_APPLICABLE

cleanup:
  revoke_credentials: true
  terminate_processes: true
  remove_persistence: true
  restore_or_destroy_lab: true
  cleanup_evidence: REQUIRED
```

Um registro `DRAFT` omite `authorization` e `closure`. A transicao para
`AUTHORIZED` adiciona a autorizacao acima. `closure` so pode existir em
`CLOSED` ou `REVOKED`:

Cada mudanca registra referencia imutavel com SHA, estado anterior, novo estado,
digest canonico do envelope anterior, horario, identidade e evidencia. O
primeiro `DRAFT` usa `from_state`, `previous_record_ref` e digest anterior
nulos. A regra semantica resolve o objeto fechado por
`r2d2-state-transition-record.schema.json`, recalcula seu digest e extrai o
`state`; objeto lateral fornecido pelo chamador, referencia ausente ou schema
incompleto falham fechados. `transition.to_state` deve ser igual ao `state`
atual. O `record_id` resolvido deve ser igual a `engagement_id`; em toda
transicao posterior, a revisao anterior deve ser exatamente `revision - 1`.
O primeiro `DRAFT` nao referencia predecessor e usa `revision: 1`.

```yaml
closure:
  execution_occurred: REQUIRED
  findings_count: REQUIRED
  cleanup_receipt: REQUIRED
  # campos abaixo somente quando findings_count > 0
  findings_reproduced_by: REQUIRED
  reviewer_differs_from_executor: true
  reviewer_did_not_author_finding: true
  reviewer_mode: READ_ONLY_AUDIT
  reviewed_evidence_digest_sha256: REQUIRED
  residual_risk_owner: roberto
  c3po_cepo_handoff_v1: REQUIRED
```

Se `findings_count` for zero, os campos de reproducao de achado sao omitidos;
isso permite revogar e limpar um exercicio antes de qualquer achado sem fabricar
evidencia. Se for maior que zero, todos os campos de reproducao sao obrigatorios.

`approved_by_identity` deve ser `roberto`; esta autorizacao ofensiva nao e
delegavel. O owner do risco residual tambem permanece `roberto`.

## Preflight

Antes do inicio, confirmar:

- estado exatamente `AUTHORIZED`;
- autorizacao valida, autenticada, nao revogada e ainda nao expirada;
- executor diferente do aprovador;
- `roe_version` e `scope_digest_sha256` iguais aos artefatos executados;
- comparacao semantica confirma aprovador, executor, operador do kill switch e
  revisor como identidades distintas onde exigido;
- `approved_at < agora < expires_at`;
- propriedade ou permissao documentada para todos os alvos;
- ativos excluidos e limites de rede aplicados tecnicamente;
- separacao entre ambiente atacante, alvo e host pessoal;
- inexistencia de dados reais desnecessarios;
- credenciais temporarias e revogaveis;
- logs fora do controle exclusivo do executor;
- snapshot ou estado restauravel;
- kill switch operado por identidade independente e testado com `PASS`;
- parada automatica diante de perda do controle;
- canal de comunicacao ativo;
- criterio de parada compreendido por todos os participantes.

Qualquer item ausente produz `BLOCKED_ROE`.

## Durante o exercicio

- Executar somente tecnicas e alvos enumerados.
- Revalidar estado, expiracao, revogacao e digest antes de cada fase sensivel.
- Respeitar limites de horario, trafego, recursos e dados.
- Nao expandir o alvo com base em descobertas.
- Nao coletar conteudo quando metadados ou prova sintetica bastarem.
- Interromper imediatamente diante de instabilidade nao prevista, vazamento,
  sistema excluido, perda de logging ou falha do kill switch.
- Registrar fatos, horario, ferramenta, versao, alvo e resultado sem segredos.

## Achados e custodia

Cada achado deve conter:

- identificador;
- ativo e versao afetados;
- pre-condicoes;
- passos minimos de reproducao;
- resultado esperado e observado;
- impacto e explorabilidade separados;
- evidencia minimizada e seu digest;
- classificacao e cadeia de custodia;
- recomendacao de remediacao;
- risco de regressao;
- estado de verificacao independente.

Doneda revisa finalidade, base, retencao e exclusao quando houver dado pessoal.

Um achado do Red Team nao e automaticamente uma vulnerabilidade aceita. Eliane
ou outro revisor independente, sem autoria e em `READ_ONLY_AUDIT`, reproduz a
evidencia vinculada ao digest. Cristine faz a garantia de seguranca; Roberto
decide diretamente o risco residual, sem delegacao neste contrato.

## Encerramento

Ao terminar:

1. Mudar o estado para `CLOSED` ou `REVOKED`.
2. Parar ferramentas e processos.
3. Revogar credenciais e tokens temporarios.
4. Remover qualquer persistencia autorizada no laboratorio.
5. Restaurar ou destruir os ambientes efemeros.
6. Confirmar ausencia de alvo, processo ou acesso residual.
7. Sanitizar, hashear e registrar evidencias e cadeia de custodia.
8. Devolver achados e riscos para R2D2.
9. Encaminhar o handoff v1 ao C3PO/CEPO.
10. Emitir recibo de encerramento.

## Proibicoes permanentes

- Testar alvo de terceiro sem autorizacao verificavel.
- Usar o exercicio como autorizacao para pesquisa ofensiva externa ampla.
- Ocultar impacto, persistencia ou acesso obtido.
- Manter acesso depois da janela.
- Publicar achado, PoC, dado ou identidade sem gate proprio.
- Usar producao por conveniencia quando um laboratorio puder cumprir o objetivo.
- Declarar `HUMAN_ACCEPTED` ou aceitar risco sem Roberto.
- Permitir que o executor seja o unico operador do kill switch.

## Validacao estrutural e semantica

O JSON Schema valida estrutura, tipos, enums, propriedades desconhecidas,
estados e proibições minimas. Comparacoes entre identidades, tempo atual,
revogacao, digest recalculado e transicoes sao obrigatoriamente validadas pelas
regras versionadas em `agents/validation/r2d2-semantic-rules.yaml`. A
canonicalizacao do digest segue `docs/security/R2D2_CANONICAL_DIGESTS.md`.

Schema estrutural isolado nunca autoriza o Red Team.
