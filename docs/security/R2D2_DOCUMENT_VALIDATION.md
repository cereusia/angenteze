# Validacao Documental de R2D2 e C3PO/CEPO

Data: 2026-08-31

Versao avaliada: `0.1.0-draft.8`

## Fronteira

Validacao exclusivamente documental. Nenhum agente, plugin, distro, ferramenta,
servidor, credencial, rede, laboratorio ou runtime foi ativado.

## Resultados

| Verificacao | Resultado |
|---|---|
| Parse dos quatro manifestos com Ruby Psych | `PASS` |
| Parse dos nove JSON Schemas com Ruby JSON e rejeicao de chave duplicada | `PASS` |
| Parse dos templates YAML de ROE, Incident Response e C3PO/CEPO | `PASS` |
| `runtime_enabled: false` em todos os manifestos | `PASS` |
| Red Team `DISABLED` | `PASS` |
| Identidade unica `c3po-cepo` | `PASS` |
| Gates com `id`, `when`, `owner`, `evidence` e `pass_condition` | `PASS` |
| Nomes de perfil identicos entre manifesto e matriz | `PASS` |
| Escrita negada em `READ_ONLY_AUDIT` | `PASS` |
| Rede dependente de confirmacao/ROE/incidente | `PASS` |
| Precedencia de `critical: DENY` | `PASS` |
| Producao em incidente dependente de break-glass | `PASS` |
| C3PO/CEPO com rede, segredos e instalacao negados | `PASS` |
| Suite semantica declarativa com casos positivos e negativos | `PASS (54/54; 18 regras)` |
| Catalogo real de 11 gates, owners, fatos e digest | `PASS` |
| Trailing whitespace e `git diff --check` no pathset | `PASS` |
| Engine completo de JSON Schema | `NOT_RUN` |

O engine completo de JSON Schema nao estava instalado. Nenhuma dependencia foi
instalada para esta validacao. Os schemas foram analisados sintaticamente e os
invariantes criticos receberam uma suite semantica reproduzivel e fail-closed.

## Reproducao

Execute a partir da raiz do repositorio, sem instalar dependencias:

```sh
ruby -e 'document = File.read("agents/validation/SEMANTIC_VALIDATOR.md"); code = document.match(/```ruby\n(.*?)\n```/m)&.captures&.first; abort "VALIDATOR_CODE_NOT_FOUND" unless code; eval(code, TOPLEVEL_BINDING, "agents/validation/SEMANTIC_VALIDATOR.md")'
```

Resultado observado:

```text
SEMANTIC_VALIDATION_PASS cases=54 rules=18
```

As regras, vetores de teste e implementacao documental ficam separados em:

- `agents/validation/r2d2-semantic-rules.yaml`;
- `agents/validation/semantic-cases.yaml`;
- `agents/validation/SEMANTIC_VALIDATOR.md`.

O snapshot candidato, algoritmo do agregado e digests individuais dos arquivos
revisados estao em `agents/validation/review-snapshot.yaml`. O manifesto exclui
a si proprio para evitar digest autorreferente.

## Vetores versionados da candidata

Os 54 casos em `semantic-cases.yaml` cobrem nominal e negativamente as 18
regras. Entre os vetores negativos persistidos estao identidade, tempo,
revogacao, kill switch, digests, proibicoes, transicoes, dupla autorizacao,
catalogo/contexto/handoff, zero mutacao, runner, pathset, resultado e PRECHECK.
Em particular, a candidata inclui divergencia de ID, revisao repetida e revisao
saltada para Red Team e Incident Response; divergencia do binding e do digest
recalculado do recibo; shell e argv negativo reautorizados; e handoff forjado
reautorizado.

## Cobertura negativa acumulada

A lista abaixo registra tambem invariantes estruturais e probes read-only das
rodadas independentes. Ela nao declara que cada item e um case nominal separado
da suite draft.8; a regressao versionada e somente a enumerada acima.

- escrita solicitada em `READ_ONLY_AUDIT` -> negada;
- alias de perfil nao declarado -> rejeitado;
- rede sem confirmacao, ROE ou incidente -> rejeitada;
- tentativa de sobrepor `critical: DENY` -> negada pelo contrato de precedencia;
- Red Team com runtime desativado ou estado diferente de `AUTHORIZED` -> negado;
- producao por `INCIDENT_RESPONSE` sem break-glass -> negada;
- propriedade superior desconhecida no schema Red Team -> rejeitada pelo schema;
- estado Red Team desconhecido -> rejeitado pelo enum.
- aprovador e executor Red Team iguais -> `BLOCKED_ROE`;
- autorizacao Red Team expirada ou revogada -> `BLOCKED_ROE`;
- digest de escopo divergente -> `BLOCKED_ROE`;
- Incident Response sem dupla autorizacao atual -> `BLOCKED_INCIDENT`;
- handoff `COMMITTED` vazio, bloqueado ou em conflito -> `BLOCKED_INTEGRATION`;
- validacao C3PO/CEPO que altera stage -> `BLOCKED_VALIDATION`.
- transicao Red Team ou Incident Response fora da maquina de estados -> bloqueada;
- kill switch Red Team ou Incident Response sem operador independente e teste
  vigente -> bloqueado;
- dupla aprovacao de incidente com digest divergente -> `BLOCKED_INCIDENT`;
- gate desconhecido, duplicado, ausente ou aplicabilidade inconsistente ->
  `BLOCKED_INTEGRATION`;
- pacote `COMMITTED` com artefato apenas `TESTED` -> `BLOCKED_INTEGRATION`;
- alteracao de HEAD, branch, refs ou fronteira durante validacao ->
  `BLOCKED_VALIDATION`;
- output dentro da fonte, `.git`, com `..` ou escape por symlink ->
  `BLOCKED_VALIDATION`;
- exit code divergente ou output esperado ausente -> `BLOCKED_VALIDATION`;
- regra desconhecida, input ausente e tipo invalido -> negacao fail-closed.
- todos os gates marcados nao aplicaveis em `COMMITTED`, owner divergente ou
  fato aplicavel omitido -> `BLOCKED_INTEGRATION`;
- `from_state` diferente do estado extraido da revisao anterior -> bloqueado;
- registro anterior ausente ou com digest divergente -> bloqueado;
- contexto de aplicabilidade com referencia/digest divergente ou autoverificado
  pelo owner -> `BLOCKED_INTEGRATION`;
- verifier fora da policy confiavel, recibo com campo extra ou referencia de
  recibo inexistente -> negacao fail-closed;
- source bundle divergente dos fatos ou de seu digest -> `BLOCKED_INTEGRATION`;
- registro anterior fornecido como side channel, ausente do commit imutavel ou
  divergente do digest -> bloqueado;
- validacao C3PO com handoff expirado, ID/owner de origem/worktree divergente,
  autorizacao revogada, argv/fonte alterado, source root externo ou digest de
  escopo divergente -> `BLOCKED_VALIDATION`;
- handoff integralmente autoforjado sem corresponder ao artefato resolvido ->
  `BLOCKED_VALIDATION`;
- `/bin/sh -c`, codigo inline e indice de argv negativo, inclusive apos nova
  autorizacao do escopo adulterado -> `BLOCKED_VALIDATION`;
- PRECHECK com execucao, timestamp, exit code, output ou tree proof fabricado ->
  `BLOCKED_VALIDATION`.

Digest recalculado do catalogo `r2d2-global@0.1.0-draft.8`:
`e4c026b0f63b96020163d86f62ff7338d26af8e87e61f15248045cc3221ef869`.

## Limitacao

Este `PASS` valida coerencia documental, nao implementacao. Parser fail-closed de
runtime, resolver real de store/commit, verificacao criptografica de identidade,
sandbox, laboratorio, kill switch, logging independente, integracao Git e
Incident Response real continuam `NOT_STARTED` e sao gates futuros de ativacao.

## Gate independente

A revisao independente desta versao deve ser executada por Lucena, Cristine e
Eliane em modo `READ_ONLY`, sem escrever nos artefatos. O resultado agregado e
o commit de encerramento devem ser registrados em recibo separado para evitar
declarar o gate antes de ele ocorrer.
