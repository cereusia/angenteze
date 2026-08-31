# Manifestos de Agentes

Este diretorio guarda contratos declarativos dos agentes especialistas do
Agente Ze.

Os manifestos descrevem identidade, responsabilidade, autoridade, entradas,
saidas, gates e condicoes de parada. A existencia de um manifesto nao cria um
processo, nao instala ferramentas e nao ativa autonomia.

## Estado inicial

- `R2D2`: lider tecnico e de ciberseguranca em estado `SPEC`.
- `Red Team`: equipe subordinada a R2D2, desabilitada por padrao.
- `Blue Team`: equipe subordinada a R2D2, sem acesso automatico a producao.
- `C3PO/CEPO`: uma unica identidade para documentacao, versionamento, lint e
  integracao serial.

## Regras comuns

- Zé coordena escopo, ownership, batons e gates.
- Roberto conserva a autoridade humana para risco, producao, publicacao e
  aceite.
- Um manifesto nunca amplia a permissao concedida para uma tarefa concreta.
- Cada writer recebe worktree, branch e pathset exclusivos.
- C3PO e CEPO sao duas formas de invocacao do mesmo agente `c3po-cepo`.
- Estados `SPEC`, `LOCAL`, `TESTED`, `COMMITTED`, `PUBLISHED`, `LIVE_E2E` e
  `HUMAN_ACCEPTED` permanecem independentes.

## Documentos normativos

- `docs/security/R2D2_SECURITY_GOVERNANCE.md`
- `docs/security/R2D2_PERMISSION_MATRIX.md`
- `docs/security/R2D2_RULES_OF_ENGAGEMENT.md`
- `docs/security/R2D2_INCIDENT_RESPONSE.md`
- `docs/security/C3PO_CEPO_SAFE_EXECUTION.md`
- `docs/security/R2D2_DOCUMENT_VALIDATION.md`
- `docs/security/R2D2_CANONICAL_DIGESTS.md`
- `docs/adr/0011-r2d2-c3po-cepo-governance.md`

Contratos estruturados:

- `agents/schemas/red-team-engagement.schema.json`
- `agents/schemas/incident-response.schema.json`
- `agents/schemas/r2d2-c3po-cepo-handoff.schema.json`
- `agents/schemas/r2d2-task-context.schema.json`
- `agents/schemas/r2d2-context-verification-receipt.schema.json`
- `agents/schemas/r2d2-context-source.schema.json`
- `agents/schemas/r2d2-identity-attestation.schema.json`
- `agents/schemas/r2d2-state-transition-record.schema.json`
- `agents/schemas/c3po-integration-validation.schema.json`

Validacao semantica reproduzivel:

- `agents/validation/r2d2-semantic-rules.yaml`
- `agents/validation/semantic-cases.yaml`
- `agents/validation/SEMANTIC_VALIDATOR.md`
- `agents/validation/trusted-verifiers.yaml`
- `agents/validation/c3po-runner-policy.yaml`
- `agents/validation/review-snapshot.yaml`
