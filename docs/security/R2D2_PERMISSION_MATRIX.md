# Matriz de Permissoes do R2D2

Versao documental: `0.1.0-draft.8`.

## Principio

R2D2 pode consultar metadados sanitizados do catalogo de capacidades. Catalogo
nao inclui segredo, credencial, configuracao privada, conectividade, ferramenta
habilitada ou permissao de execucao.

A permissao efetiva e a intersecao de:

```text
escopo autorizado
  + perfil ativo
  + ambiente permitido
  + identidade temporaria
  + gate humano
  + controles de auditoria
```

Na duvida, a decisao e `DENY` ou `BLOCKED_SCOPE`.

## Precedencia fail-closed

A politica executavel mais restritiva sempre prevalece. Nenhum perfil, ROE,
incidente, confirmacao ou manifesto documental pode sobrepor:

1. `runtime_enabled: false`;
2. registry e allowlist do projeto;
3. sandbox e fronteiras do sistema operacional;
4. politica MCP executavel;
5. `critical: DENY` do MVP v0.1.

Se qualquer camada negar, a decisao final e `DENY`. No MVP, todos os perfis
deste documento permanecem especificacoes sem consumidor de runtime.

## Perfis

### `READ_ONLY_AUDIT`

Perfil padrao para pesquisa local, inventario, leitura, threat model e producao
de resposta nao persistida. Nao autoriza escrita, alteracao de runtime, scan
ativo, rede automatica ou acesso a segredo.

### `DOCUMENTATION_WRITER`

Permite persistir SPECs, ADRs, manifestos e relatorios somente em worktree e
pathset documentais declarados. Nao autoriza codigo, runtime, rede automatica,
instalacao ou acesso a segredos.

### `SECURITY_ENGINEERING`

Permite escrita em worktree e pathset exclusivos para desenvolvimento ou
remediacao. Exige baton, testes proporcionais e revisao independente.

### `BLUE_DEFENSE_LAB`

Permite implementar e testar controles defensivos em ambiente isolado com dados
sinteticos. Nao concede acesso automatico a producao.

### `CYBER_LAB_RED`

Permite somente as tecnicas registradas em uma ROE `AUTHORIZED`, dentro de
laboratorio efemero e alvos enumerados.

### `INCIDENT_RESPONSE`

Permite preparar, analisar e apoiar um incidente declarado. O perfil sozinho
nunca concede producao. Qualquer acao em producao exige o contrato break-glass,
Roberto, Tereza, ativo exato, janela, credencial temporaria, logging, rollback e
encerramento definidos em `R2D2_INCIDENT_RESPONSE.md`.

`PRODUCTION_CHANGE` nao e perfil de R2D2. Alteracoes de producao pertencem ao
baton separado de Tereza.

## Matriz

| Capacidade | READ_ONLY_AUDIT | DOCUMENTATION_WRITER | SECURITY_ENGINEERING | BLUE_DEFENSE_LAB | CYBER_LAB_RED | INCIDENT_RESPONSE |
|---|---|---|---|---|---|---|
| Ler docs e codigo autorizado | `ALLOW` | `ALLOW` | `ALLOW` | `ALLOW` | `ALLOW_ROE` | `ALLOW_INCIDENT` |
| Pesquisa publica usando rede | `CONFIRM_NETWORK` | `CONFIRM_NETWORK` | `CONFIRM_NETWORK` | `CONFIRM_NETWORK_LAB` | `ALLOW_ROE` | `ALLOW_INCIDENT` |
| Persistir SPEC, ADR ou relatorio | `DENY` | `ALLOW_PATHSET` | `ALLOW_PATHSET` | `ALLOW_PATHSET` | `ALLOW_EVIDENCE_PATH_ROE` | `ALLOW_EVIDENCE_PATH_INCIDENT` |
| Alterar codigo | `DENY` | `DENY` | `ALLOW_PATHSET` | `ALLOW_PATHSET` | `DENY` | `DENY_BY_DEFAULT` |
| Alterar configuracao nao produtiva | `DENY` | `DENY` | `CONFIRM_PATHSET` | `ALLOW_LAB_ONLY` | `ALLOW_TARGET_LAB_ROE` | `ALLOW_INCIDENT_NONPROD` |
| Alterar producao | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `REQUIRES_BREAK_GLASS_TEREZA_ROBERTO` |
| Instalar dependencia | `DENY` | `DENY` | `CONFIRM_LAB` | `CONFIRM_LAB` | `CONFIRM_LAB_ROE` | `DENY_BY_DEFAULT` |
| Instalar ou atualizar plugin | `DENY` | `DENY` | `CONFIRM_SEPARATE_GATE` | `CONFIRM_SEPARATE_GATE` | `CONFIRM_SEPARATE_GATE_ROE` | `DENY_BY_DEFAULT` |
| Scan passivo | `CONFIRM_TARGET` | `DENY` | `CONFIRM_TARGET` | `ALLOW_LAB` | `ALLOW_ROE` | `ALLOW_INCIDENT` |
| Scan ativo de rede | `DENY` | `DENY` | `DENY` | `CONFIRM_LAB` | `ALLOW_ROE` | `REQUIRES_BREAK_GLASS_IF_PROD` |
| Explorar vulnerabilidade | `DENY` | `DENY` | `DENY` | `DENY` | `ALLOW_ROE` | `DENY` |
| Simular phishing ou engenharia social | `DENY` | `DENY` | `DENY` | `DENY` | `CONFIRM_EXPLICIT_ROE` | `DENY` |
| Testar negacao de servico | `DENY` | `DENY` | `DENY` | `DENY` | `DENY_BY_DEFAULT` | `DENY` |
| Ler segredo | `DENY` | `DENY` | `JUST_IN_TIME_MINIMUM` | `LAB_SECRET_ONLY` | `LAB_SECRET_ONLY_ROE` | `REQUIRES_BREAK_GLASS_IF_PROD` |
| Exibir ou persistir segredo | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| Acessar dados pessoais reais | `DENY` | `DENY` | `CONFIRM_DONEDA` | `DENY` | `DENY` | `REQUIRES_BREAK_GLASS_DONEDA_IF_PROD` |
| Persistencia em alvo | `DENY` | `DENY` | `DENY` | `DENY` | `DENY_BY_DEFAULT` | `REQUIRES_BREAK_GLASS_IF_ESSENTIAL` |
| Escrever na branch de integracao | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| Fazer merge de integracao | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| Fazer release ou deploy | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |
| Aceitar risco residual | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` | `DENY` |

Significados:

- `ALLOW_ROE`: tecnica, alvo, ambiente e janela constam na ROE autorizada e o
  digest corresponde ao pacote executado.
- `ALLOW_INCIDENT`: leitura ou evidencia consta no incidente autorizado, sem
  conceder mutacao produtiva.
- `REQUIRES_BREAK_GLASS_*`: o perfil nao basta; todos os requisitos do contrato
  de incidente devem passar antes da acao.
- `DENY_BY_DEFAULT`: somente uma futura decisao normativa mais especifica pode
  propor excecao; confirmacao generica nao altera a negacao.

## Credenciais e dados

- Credenciais sao concedidas por capacidade e ambiente, nunca por conveniencia.
- Usar identidades temporarias, escopos minimos e expiracao automatica.
- Valores nao entram em prompt, Git, manifestos, logs, prints ou evidencias.
- Evidencias usam dados sinteticos ou mascarados sempre que possivel.
- O contrato de custodia registra classificacao, finalidade, base, criptografia,
  ACL, hash, retencao e owner de exclusao.
- Doneda revisa qualquer evidencia com dado pessoal.
- O encerramento revoga credenciais, processos e acessos temporarios.

## Instalacoes e atualizacoes

Antes de instalar plugin, distro, scanner ou dependencia de seguranca:

1. R2D2 registra finalidade, origem, versao, licenca e permissoes.
2. Cristine avalia superficie, egress, segredos e supply chain.
3. A origem, assinatura ou proveniencia e checksum sao verificados.
4. Dependencias diretas e transitivas ficam fixadas em lockfile.
5. SBOM, politica de egress e quarentena do artefato sao registrados.
6. A ferramenta e validada em laboratorio isolado antes e depois da instalacao.
7. Eliane verifica o resultado e o comportamento de falha.
8. C3PO/CEPO registra changelog, versao e rollback.
9. O owner humano autoriza a promocao quando a capacidade for sensivel.

Esta matriz nao autoriza nenhuma instalacao.

## Condicoes de parada

Parar e retornar `BLOCKED` quando:

- o alvo ou owner nao puder ser provado;
- a execucao atingir sistema excluido;
- uma credencial exceder o escopo;
- houver vazamento ou acesso inesperado a dados;
- os logs independentes falharem;
- o kill switch nao funcionar;
- ocorrer sobreposicao de writer;
- um comando destrutivo nao estiver explicitamente autorizado;
- a evidencia nao puder ser atribuida ao ambiente e versao corretos;
- qualquer camada mais restritiva negar a acao.
