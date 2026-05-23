# ADR 0006 - Venv Python Embutido no App macOS

Status: Proposto

Data: 2026-05-23

## Contexto

O app macOS chama o `agent-core` Python por processo local. Para evoluir para instalacao real, o app nao deve depender indefinidamente do Python global do usuario.

## Decisao

Usar um venv embutido como estrategia de empacotamento inicial:

- caminho de desenvolvimento: `apps/macos/Resources/python/.venv`;
- script de preparo: `scripts/bootstrap-embedded-venv.sh`;
- o app macOS deve preferir `AGENTEZE_PYTHON_EXECUTABLE` quando definido;
- se nao houver variavel, deve preferir o Python do venv embutido;
- se o venv ainda nao existir, deve cair para `/usr/bin/env python3`.

O venv real nao sera versionado. Apenas scripts e documentacao entram no Git.

## Consequencias

- O MVP continua rodando em desenvolvimento sem empacotamento completo.
- A decisao prepara assinatura/notarizacao futura.
- O tamanho do app empacotado aumentara quando o venv for incluido.
- Dependencias Python devem ser minimas e auditaveis.

## Alternativas Consideradas

- Exigir Python global do usuario.
- Empacotar Python diretamente sem venv.
- Reescrever o backend em Swift.
- Usar servidor local separado.

## Validacao

- `./scripts/bootstrap-embedded-venv.sh`
- `./scripts/test-python.sh`
- `./scripts/build-macos.sh`
