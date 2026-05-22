# ADR 0004 - UI de Confirmacao MCP

Status: Proposto

Data: 2026-05-22

## Contexto

O Agente Ze ja possui uma politica local de permissao MCP. Ferramentas `medium` e `high` ficam pendentes de confirmacao, mas o usuario precisa de uma superficie explicita no app macOS para aprovar ou negar essas ferramentas.

O MVP v0.1 ainda nao deve executar ferramentas reais. A confirmacao deve apenas fechar o contrato UI -> backend -> policy.

## Decisao

Adicionar um painel de confirmacao MCP no prompt macOS.

Fluxo:

1. O usuario envia um prompt.
2. O backend ativa ferramentas MCP por contrato e intencao.
3. Ferramentas `medium` ou `high` retornam `permission = confirmation_required`.
4. O app mostra botoes `Confirmar` e `Negar`.
5. Ao confirmar, o app reenvia o mesmo prompt com `--confirm-tool`.
6. O backend retorna `permission = confirmed`.

Nenhuma ferramenta real e executada nesta etapa.

## Consequencias

- O app tem uma superficie clara para acoes sensiveis.
- O backend passa a ter contrato para confirmacoes por requisicao.
- A proxima etapa pode implementar execucao real atras dessa confirmacao.
- Negacoes ainda sao estado local da UI, sem persistencia no backend.

## Alternativas Consideradas

- Confirmar tudo automaticamente.
- Bloquear ferramentas `medium` e `high` sem UI.
- Implementar execucao real junto com a UI.

## Validacao

- Testes Python cobrem ferramenta media pendente e confirmada.
- Build SwiftPM valida o painel no app macOS.
- O registry MCP inclui uma ferramenta media ativada por intencao de memoria.
