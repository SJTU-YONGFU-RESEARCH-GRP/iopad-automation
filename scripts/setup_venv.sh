#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-demo/.venv}"
REQUIREMENTS_OUT="${REQUIREMENTS_OUT:-requirements.txt}"
INSTALL_GDSTK="${INSTALL_GDSTK:-0}"
RECREATE="${RECREATE:-0}"
UPGRADE_PIP_TOOLS="${UPGRADE_PIP_TOOLS:-0}"
EXCLUDE_PACKAGING_TOOLS="${EXCLUDE_PACKAGING_TOOLS:-1}"

PYTHON_BIN="${PYTHON_BIN:-python3}"

usage() {
  cat <<'EOF'
Create a virtual environment and install runtime dependencies.

Environment variables:
  VENV_DIR            Venv directory to create/use (default: demo/.venv)
  REQUIREMENTS_OUT   Where to write the generated requirements.txt (default: requirements.txt)
  INSTALL_GDSTK      1 to install gdstk (optional dependency), 0 otherwise (default: 0)
  RECREATE           1 to delete/recreate VENV_DIR if it exists (default: 0)
  UPGRADE_PIP_TOOLS  1 to upgrade pip/setuptools/wheel (default: 0)
  PYTHON_BIN         Python executable (default: python3)

Example:
  INSTALL_GDSTK=1 RECREATE=1 ./scripts/setup_venv.sh
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Error: '${PYTHON_BIN}' not found in PATH." >&2
  exit 1
fi

if [[ "${RECREATE}" == "1" && -d "${VENV_DIR}" ]]; then
  echo "Recreating venv: ${VENV_DIR}"
  rm -rf "${VENV_DIR}"
fi

mkdir -p "$(dirname "${VENV_DIR}")"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Creating venv: ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

VENV_PY="${VENV_DIR}/bin/python"

if [[ ! -x "${VENV_PY}" ]]; then
  echo "Error: venv python not found at ${VENV_PY}" >&2
  exit 1
fi

if [[ "${UPGRADE_PIP_TOOLS}" == "1" ]]; then
  echo "Upgrading pip/setuptools/wheel..."
  "${VENV_PY}" -m pip install --upgrade pip setuptools wheel
fi

echo "Installing required dependencies..."
"${VENV_PY}" -m pip install --upgrade "PyYAML"

if [[ "${INSTALL_GDSTK}" == "1" ]]; then
  echo "Installing optional dependency: gdstk"
  # gdstk will pull in numpy automatically.
  "${VENV_PY}" -m pip install --upgrade "gdstk"
fi

echo "Generating ${REQUIREMENTS_OUT} from current venv..."
if [[ "${EXCLUDE_PACKAGING_TOOLS}" == "1" ]]; then
  "${VENV_PY}" -m pip freeze | sort | awk '!/^(pip==|setuptools==|wheel==)/{print}' >"${REQUIREMENTS_OUT}"
else
  "${VENV_PY}" -m pip freeze | sort >"${REQUIREMENTS_OUT}"
fi

echo "Done."

