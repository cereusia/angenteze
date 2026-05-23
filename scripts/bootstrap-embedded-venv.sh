#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/apps/macos/Resources/python/.venv"

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --no-deps -e "$ROOT_DIR/agent-core"

printf 'Embedded venv ready: %s\n' "$VENV_DIR"
