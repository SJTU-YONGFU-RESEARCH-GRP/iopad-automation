#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

VENV_DIR="${VENV_DIR:-venv}"
REQUIREMENTS_OUT="${REQUIREMENTS_OUT:-requirements.txt}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

# If 1, exclude pip/setuptools/wheel from requirements output.
EXCLUDE_PACKAGING_TOOLS="${EXCLUDE_PACKAGING_TOOLS:-1}"

# If 1, include gdstk when it's inferred from source imports.
INSTALL_GDSTK="${INSTALL_GDSTK:-1}"

# If 1, recreate the venv when its python executable is missing or empty.
RECREATE_IF_VENV_BROKEN="${RECREATE_IF_VENV_BROKEN:-1}"

# If 1, generate requirements in a temporary clean venv.
# This avoids polluting requirements.txt with unrelated packages already
# present in your working venv (e.g., pytest).
USE_TEMP_VENV_FOR_FREEZE="${USE_TEMP_VENV_FOR_FREEZE:-1}"
usage() {
  cat <<'EOF'
Generate requirements.txt based on import scanning in src/ and pinned via pip freeze.

Environment variables:
  VENV_DIR                     Venv directory to use (default: venv)
  REQUIREMENTS_OUT            Where to write requirements.txt (default: requirements.txt)
  PYTHON_BIN                  Python executable name used for inference (default: python3)
  EXCLUDE_PACKAGING_TOOLS     1 to exclude pip/setuptools/wheel from output (default: 1)
  INSTALL_GDSTK               1 to include inferred gdstk (default: 1)
  RECREATE_IF_VENV_BROKEN     1 to recreate venv if venv python is missing/empty (default: 1)

Example:
  ./scripts/generate_requirements.sh
  INSTALL_GDSTK=1 RECREATE_IF_VENV_BROKEN=1 ./scripts/generate_requirements.sh
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

VENV_PY="${VENV_DIR}/bin/python"

VENV_DIR_FOR_FREEZE="${VENV_DIR}"
TEMP_VENV_DIR=""
if [[ "${USE_TEMP_VENV_FOR_FREEZE}" == "1" ]]; then
  TEMP_VENV_DIR="$(mktemp -d -t iopad-reqgen-venv-XXXXXX)"
  VENV_DIR_FOR_FREEZE="${TEMP_VENV_DIR}"
  trap 'rm -rf "${TEMP_VENV_DIR}"' EXIT
fi

VENV_PY="${VENV_DIR_FOR_FREEZE}/bin/python"

if [[ ! -x "${VENV_PY}" || ! -s "${VENV_PY}" ]]; then
  if [[ "${RECREATE_IF_VENV_BROKEN}" == "1" ]]; then
    echo "Creating venv for requirements: ${VENV_DIR_FOR_FREEZE}"
    rm -rf "${VENV_DIR_FOR_FREEZE}"
    "${PYTHON_BIN}" -m venv "${VENV_DIR_FOR_FREEZE}"
  else
    echo "Error: venv python not found or empty at ${VENV_PY}. Create the venv first." >&2
    exit 1
  fi
fi

if [[ ! -x "${VENV_PY}" ]]; then
  echo "Error: venv python not found at ${VENV_PY} after creation." >&2
  exit 1
fi

# Ensure pip tooling exists before installing inferred packages.
"${VENV_PY}" -m pip --version >/dev/null 2>&1 || {
  echo "Error: pip is unavailable in venv at ${VENV_PY}." >&2
  exit 1
}

echo "Inferring third-party packages from src/..."
mapfile -t inferred_packages < <("${PYTHON_BIN}" "${ROOT_DIR}/src/requirements_infer.py" --src-dir "${ROOT_DIR}/src")

filtered_packages=()
for pkg in "${inferred_packages[@]}"; do
  if [[ "${pkg}" == "gdstk" && "${INSTALL_GDSTK}" != "1" ]]; then
    continue
  fi
  filtered_packages+=("${pkg}")
done

if [[ "${#filtered_packages[@]}" -gt 0 ]]; then
  echo "Installing inferred packages into venv..."
  for pkg in "${filtered_packages[@]}"; do
    echo "  Installing: ${pkg}"
    "${VENV_PY}" -m pip install --upgrade "${pkg}"
  done
else
  echo "No third-party packages inferred from src/ (or all filtered out)."
fi

echo "Generating ${REQUIREMENTS_OUT}..."
if [[ "${EXCLUDE_PACKAGING_TOOLS}" == "1" ]]; then
  "${VENV_PY}" -m pip freeze | sort | awk '!/^(pip==|setuptools==|wheel==)/{print}' >"${REQUIREMENTS_OUT}"
else
  "${VENV_PY}" -m pip freeze | sort >"${REQUIREMENTS_OUT}"
fi

echo "Done."

