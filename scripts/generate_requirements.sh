#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-venv}"
REQUIREMENTS_OUT="${REQUIREMENTS_OUT:-requirements.txt}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
EXCLUDE_PACKAGING_TOOLS="${EXCLUDE_PACKAGING_TOOLS:-1}"

usage() {
  cat <<'EOF'
Generate requirements.txt by running 'pip freeze' inside an existing venv.

Environment variables:
  VENV_DIR          Venv directory to use (default: demo/.venv)
  REQUIREMENTS_OUT Where to write requirements.txt (default: requirements.txt)
  PYTHON_BIN       Python executable name (default: python3) - not used directly
  EXCLUDE_PACKAGING_TOOLS 1 to exclude pip/setuptools/wheel from output (default: 1)

Example:
  VENV_DIR=demo/.venv ./scripts/generate_requirements.sh
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

VENV_PY="${VENV_DIR}/bin/python"

if [[ ! -x "${VENV_PY}" ]]; then
  echo "Error: venv python not found at ${VENV_PY}. Create the venv first." >&2
  exit 1
fi

echo "Generating ${REQUIREMENTS_OUT}..."
if [[ "${EXCLUDE_PACKAGING_TOOLS}" == "1" ]]; then
  "${VENV_PY}" -m pip freeze | sort | awk '!/^(pip==|setuptools==|wheel==)/{print}' >"${REQUIREMENTS_OUT}"
else
  "${VENV_PY}" -m pip freeze | sort >"${REQUIREMENTS_OUT}"
fi

echo "Done."

