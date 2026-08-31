# ADR 0011 - Governanca de R2D2 e C3PO/CEPO

Status: Aceito documentalmente

Data: 2026-08-31

Versao documental: `0.1.0-draft.8`

## Contexto

O Agente Ze preve agentes especialistas, mas o P6 ainda nao possui um contrato
completo de identidade, autoridade, equipes subordinadas, permissao e integracao.

Foi definido que R2D2 sera o lider tecnico e de ciberseguranca, incluindo SPECs,
pesquisa, ambientes, engenharia, evolucao e coordenacao de Red e Blue Team.
Tambem foi esclarecido que C3PO e CEPO se referem ao mesmo agente de
documentacao, versionamento, lint e integracao.

Concentrar desenvolvimento, ataque, revisao, integracao, release e aceite em uma
identidade criaria autorrevisao e privilegio excessivo. A existencia de
manifestos tambem nao pode ativar multiagente ou ferramentas sensiveis no MVP.

## Decisao

Adotar os seguintes contratos documentais:

- `r2d2-global` como lider tecnico e de ciberseguranca;
- `r2d2-red-team` como equipe ofensiva sob demanda e desabilitada por padrao;
- `r2d2-blue-team` como equipe defensiva sob demanda;
- `c3po-cepo` como uma identidade unica, com invocacoes `C3PO` e `CEPO`;
- Cristine como garantia independente de seguranca;
- Eliane como QA e reproducao independente;
- Doneda como gate de dados e privacidade;
- Tereza como owner separado de release e producao;
- Roberto como autoridade de risco e aceite humano;
- Zé como coordenador de ownership, batons e gates.

R2D2 recebe acesso ao catalogo de capacidades, nao execucao irrestrita. Cada
atividade opera por perfil, escopo, ambiente, tempo e autorizacao.

O catalogo expoe apenas metadados sanitizados. A politica executavel mais
restritiva prevalece, inclusive `runtime_enabled: false`, registry, allowlist,
sandbox, politica MCP e `critical: DENY`.

C3PO/CEPO e o unico writer da fronteira de integracao declarada. Ele nao
implementa features, nao aprova o proprio trabalho e nao faz deploy.

`READ_ONLY_AUDIT` nunca persiste arquivos. Escrita de SPEC, ADR ou relatorio usa
o perfil separado `DOCUMENTATION_WRITER`.

Red Team exige ROE versionada, autorizada, com digest imutavel, identidade e
revogacao. Incident Response nao concede producao sem contrato break-glass de
Roberto e Tereza. Lint e testes do C3PO/CEPO seguem um contrato de execucao
segura sem rede, segredos ou instalacao implicita.

## Consequencias

### Positivas

- Responsabilidades e conflitos de interesse ficam explicitos.
- Red e Blue Team passam a ter limites e artefatos verificaveis.
- C3PO e CEPO nao podem divergir como duas identidades.
- Ferramentas ofensivas e producao permanecem fechadas por padrao.
- A integracao recebe ownership e rastreabilidade serial.

### Custos

- Atividades sensiveis exigem mais de um gate.
- Red Team depende de laboratorio e regras de engajamento.
- R2D2 nao pode aprovar sozinho uma correcao que implementou.
- Manifestos precisam de validadores antes de ativacao futura.

## Fora do escopo desta decisao

- Criar ou iniciar processos de agentes.
- Instalar Codex Security, Kali Linux, plugins, scanners ou dependencias.
- Alterar runtime, registry MCP ou politica executavel.
- Conceder credenciais, internet irrestrita ou acesso de producao.
- Criar release, publicar ou ativar producao.
- Declarar o P6 concluido.

## Validacao requerida antes da ativacao

- schema formal e parser fail-closed para manifestos de runtime;
- parser fail-closed;
- testes de identidade unica C3PO/CEPO;
- testes dos perfis de permissao;
- teste de negacao para atividade critica;
- laboratorio isolado descartavel;
- logs independentes e kill switch;
- piloto read-only em repositorio isolado;
- revisao de Cristine, Eliane, Doneda e Tereza conforme o perfil;
- aceite humano de Roberto.

## Revisao documental independente

A primeira revisao de Lucena, Cristine e Eliane encontrou conflitos de menor
privilegio, rede, `critical: DENY`, ownership, gates, autorizacao Red Team,
Incident Response e execucao de validadores pelo C3PO/CEPO.

A revisao `0.1.0-draft.2` corrigiu documentalmente esses pontos e adicionou:

- perfil `DOCUMENTATION_WRITER`;
- gates condicionais com owner, evidencia e estado `NOT_APPLICABLE`;
- ROE verificavel e schema fail-closed;
- contrato de Incident Response;
- contrato de execucao segura do C3PO/CEPO;
- schema do handoff R2D2 para C3PO/CEPO;
- controles de supply chain, kill switch e custodia de evidencias.

A segunda revisao independente encontrou lacunas de estado e prova que ainda
permitiam handoff vazio, autorizacao expirada ou revogada, encerramento precoce
e validacao do C3PO/CEPO sem prova de zero mutacao. A revisao
`0.1.0-draft.3` acrescenta:

- invariantes condicionais no schema de handoff;
- schema proprio para Incident Response e dupla autorizacao atribuivel;
- schema de validacao segura do C3PO/CEPO com arvore, indice e output pathset;
- regras semanticas versionadas para identidade, tempo, revogacao e digests;
- casos positivos e negativos executaveis sem instalar dependencias;
- um unico contrato canonico de entrada do C3PO/CEPO.

A terceira revisao independente encontrou residuos de autoridade, transicao,
catalogo de gates, digest de aprovacao e isolamento de outputs. A revisao
`0.1.0-draft.4` fecha documentalmente esses pontos com:

- autorizacao ofensiva e break-glass direta, sem delegacao implicita;
- maquinas de estado Red Team e Incident Response validadas semanticamente;
- dupla aprovacao individual vinculada ao mesmo digest canonico;
- catalogo de gates versionado, completo, sem IDs desconhecidos ou duplicados;
- estado agregado `COMMITTED` somente com todos os artefatos commitados;
- ciclo honesto de validacao C3PO/CEPO, sem resultado `after` antecipado;
- prova de HEAD, branch, refs, stage, fronteira e isolamento realpath do output;
- vinculacao entre manifesto de regras, implementacao e casos versionados.

A quarta revisao confirmou esses fechamentos, mas encontrou autodeclaracao de
aplicabilidade/owner, estado anterior nao extraido do registro e validacao C3PO
desvinculada do handoff. A revisao `0.1.0-draft.5` acrescenta:

- fatos estruturados para derivar os onze gates e owners comparados ao catalogo;
- integracao obrigatoriamente aplicavel e `PASS` no estado `COMMITTED`;
- comparacao de `from_state` com o estado extraido da revisao anterior;
- binding C3PO por ID/digest de handoff, owner, repo, HEAD, branch e pathset;
- autorizacao temporal e digest recalculado do comando C3PO;
- casos negativos para todos N/A, owner divergente, salto de estado, handoff
  expirado/desvinculado e comando alterado.

A quinta revisao demonstrou que ainda era possivel forjar contexto, estado
anterior e escopo C3PO por escalares internamente consistentes. A revisao
`0.1.0-draft.6` substitui esses atalhos por artefatos canonicalizados:

- `r2d2-task-context-v1` externo ao handoff, ligado a repo/HEAD/pathset, com
  evidencia por fato e recibo independente recalculado;
- submissao e conclusao da integracao como fatos distintos;
- objeto anterior completo carregado por referencia, com digest recalculado e
  estado extraido do proprio objeto;
- `c3po_validation_scope_v1` cobrindo handoff, worktree, boundary, source root,
  working directory, argv, fonte, outputs, timeout, ambiente e politicas;
- autorizacao C3PO atual, nao revogada e vinculada ao digest integral do escopo;
- casos negativos para contexto adulterado/autoverificado, registro anterior
  adulterado, argv/fonte divergente, source root externo, worktree divergente,
  revogacao, digest de escopo e PRECHECK fabricado.

Essas correcoes nao ativam agentes nem fecham os testes de runtime exigidos antes
da ativacao futura.

A sexta revisao independente encontrou tres classes residuais: verifier apenas
nominal, registro anterior ainda fornecido pelo chamador e handoff C3PO aceito
por escalares coerentes; tambem demonstrou shell arbitrario e indice negativo de
argv. A revisao `0.1.0-draft.7` fecha o desenho documental com:

- source bundle resolvido, extrator deterministico, recibo fechado, trust policy
  e atestado externo de identidade;
- registro anterior fechado por schema e resolvido em referencia contendo SHA,
  rejeitando objeto lateral fornecido pelo chamador;
- `handoff_ref` imutavel, digest recalculado do handoff completo e campos de
  autoridade derivados desse artefato;
- policy de runner com execucao direta, executable realpath/digest, shell e
  codigo inline negados e indice de argv nao negativo;
- casos adversariais novamente autorizados para shell, indice negativo e
  handoff autoforjado, todos bloqueados.

Resolver real, autenticacao criptografica, sandbox e execucao continuam
`NOT_STARTED`; os fixtures apenas tornam o contrato documental reproduzivel.

A setima revisao independente encontrou replay possivel do predecessor entre
engajamentos ou incidentes diferentes e apontou que parte da cobertura descrita
nao estava individualizada na suite versionada. A revisao
`0.1.0-draft.8` acrescenta:

- vinculacao obrigatoria entre `record_id` anterior e o ID do registro atual;
- continuidade estrita de revisao, com primeiro `DRAFT` em revisao 1;
- schemas fechados para source bundle e atestado de identidade;
- casos versionados para ID divergente, revisao repetida ou saltada e para
  divergencias do binding e do digest recalculado do recibo;
- separacao explicita entre os 54 casos executados e os probes acumulados das
  revisoes independentes.

Esses fechamentos permanecem documentais e nao alteram runtime ou autoridade.

## Rollback

Como esta decisao e apenas documental, o rollback consiste em remover os novos
manifestos e documentos ou substituir este ADR por uma decisao posterior. Nao
ha runtime, plugin, credencial ou ambiente para desativar.
