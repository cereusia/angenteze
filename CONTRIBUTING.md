# Contribuindo

Obrigado por considerar contribuir com o Agente Ze.

## Estado do Projeto

O projeto esta em fase inicial. A prioridade atual e documentacao, arquitetura e seguranca antes de codigo.

## Licenca

A licenca pretendida e GNU AGPL v3. O arquivo `LICENSE` ainda deve ser adicionado antes de aceitar contribuicoes externas relevantes.

## Antes de Contribuir

- Leia `AGENTS.md`.
- Leia os arquivos em `specs/`.
- Mantenha mudancas pequenas.
- Documente decisoes tecnicas importantes como ADR.
- Nao adicione dependencias sem justificativa.

## Padrao de Mudanca

Toda contribuicao deve explicar:

- problema;
- solucao;
- impacto;
- validacao executada;
- riscos conhecidos.

## Documentacao

Mudancas em arquitetura, seguranca, MCP, memoria, agentes ou UX devem atualizar a documentacao correspondente.

## Codigo

Ainda nao ha codigo base. Quando houver:

- Python deve ter testes proporcionais.
- SwiftUI deve ter build validado.
- Ferramentas MCP devem ter contrato e politica de permissao.
- Logs nao devem expor segredos.

## Seguranca

Nao publique segredos, tokens, chaves, dados pessoais ou informacoes sensiveis em issues, PRs ou logs.

Relatos de vulnerabilidade devem ser tratados com cuidado ate existir uma politica formal de seguranca.

## Pull Requests

PRs devem ser pequenos e revisaveis.

Checklist minimo:

- documentacao atualizada;
- testes ou validacao manual descritos;
- riscos de seguranca considerados;
- nenhuma dependencia desnecessaria;
- nenhum comando destrutivo executado sem aprovacao.
