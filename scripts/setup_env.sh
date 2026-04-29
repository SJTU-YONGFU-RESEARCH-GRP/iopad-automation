#!/usr/bin/env bash
set -euo pipefail

# Convenience wrapper: create venv + install deps + generate requirements.txt

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${DIR}/.." && pwd)"

export VENV_DIR="${VENV_DIR:-demo/.venv}"
export REQUIREMENTS_OUT="${REQUIREMENTS_OUT:-requirements.txt}"
export INSTALL_GDSTK="${INSTALL_GDSTK:-1}"
export RECREATE="${RECREATE:-0}"
export PYTHON_BIN="${PYTHON_BIN:-python3}"

"${ROOT_DIR}/scripts/setup_venv.sh" "$@"

