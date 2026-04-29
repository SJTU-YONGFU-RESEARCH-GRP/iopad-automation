#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python3}"
IO_LIB_PATH="${IO_LIB_PATH:-$ROOT_DIR/tools/globalfoundries-pdk-libs-gf180mcu_fd_io/cells}"
IO_YAML="${IO_YAML:-$ROOT_DIR/config/io.yaml}"
PAD_YAML="${PAD_YAML:-$ROOT_DIR/config/pad.yaml}"
TOOLS_ROOT="${TOOLS_ROOT:-$ROOT_DIR/tools/globalfoundries-pdk-libs-gf180mcu_fd_io}"

OUT_DIR="${OUT_DIR:-$ROOT_DIR/artifacts}"
PLACEMENT_JSON="${PLACEMENT_JSON:-$OUT_DIR/pad_ring_placement.json}"
GDS_PATH="${GDS_PATH:-$OUT_DIR/pad_ring.gds}"
NETLIST_PATH="${NETLIST_PATH:-$OUT_DIR/pad_ring_extracted.cir}"
LVS_REPORT_PATH="${LVS_REPORT_PATH:-$OUT_DIR/pad_ring.lvsdb}"
TOP_CELL="${TOP_CELL:-PAD_RING_TOP}"

STEP="both" # placement | gds | both (gds stage will also try netlist extraction)
MODE="auto" # auto | real | abstract (for pad_ring_gds)
NETLIST_REQUEST="auto" # auto | on | off
METAL_STACK="" # optional override: 3lm | 4lm | 5lm
LVS_THR="" # optional override for klayout threads (thr). Default: nproc*2
LVS_SUBSTRATE_NAME="${LVS_SUBSTRATE_NAME:-gf180mcu_gnd}"
GF180MCU_LVS_RULESET_PATH="${GF180MCU_LVS_RULESET_PATH:-$ROOT_DIR/tools/globalfoundries-pdk-libs-gf180mcu_fd_pr/rules/klayout/lvs/gf180mcu.lvs}"
PLACEMENT_METHOD="" # optional override (packed | even)
DIE_WIDTH="" # optional override
DIE_HEIGHT="" # optional override

usage() {
  cat <<EOF
Usage: $0 [--step placement|gds|both] [--out-dir DIR] [options...]

Default inputs:
  IO_YAML:  $IO_YAML
  PAD_YAML: $PAD_YAML

Options:
  --step placement|gds|both   Which stage(s) to run. Default: both.
  --out-dir DIR               Output directory. Default: $OUT_DIR.
  --mode MODE                 GDS mode for pad_ring_gds.py: auto|real|abstract. Default: $MODE.
  --metal-stack STACK        Metal stack used by pad_ring_gds.py (3lm|4lm|5lm). Default: from io.yaml.
  --top-cell NAME            Top-level GDS cell name. Default: $TOP_CELL.
  --placement-method METHOD  packed|even (overrides YAML placement_method).
  --die-width UM             Override die width (um).
  --die-height UM            Override die height (um).

  --netlist                  Force netlist extraction (requires klayout). Default behavior: auto.
  --no-netlist               Disable netlist extraction.
  --netlist-path PATH        Output extracted netlist path. Default: $NETLIST_PATH.
  --lvs-report-path PATH     Output LVS report database path. Default: $LVS_REPORT_PATH.
  --lvs-thr N                KLayout thread count for LVS deck (thr). Default: nproc*2.
  --lvs-sub NAME             Substrate name for LVS deck. Default: $LVS_SUBSTRATE_NAME.

  --io-lib-path PATH         IO cell LEF root for pad_ring_generator.py.
  --tools-root PATH          Tools root for pad_ring_gds.py. (contains cells/)
  --io-yaml PATH             Path to io.yaml.
  --pad-yaml PATH            Path to pad.yaml.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --step)
      STEP="${2:-}"; shift 2
      ;;
    --out-dir)
      OUT_DIR="${2:-}"; shift 2
      PLACEMENT_JSON="$OUT_DIR/pad_ring_placement.json"
      GDS_PATH="$OUT_DIR/pad_ring_abstract.gds"
      ;;
    --mode)
      MODE="${2:-}"; shift 2
      ;;
    --metal-stack)
      METAL_STACK="${2:-}"; shift 2
      ;;
    --top-cell)
      TOP_CELL="${2:-}"; shift 2
      ;;
    --placement-method)
      PLACEMENT_METHOD="${2:-}"; shift 2
      ;;
    --netlist)
      NETLIST_REQUEST="on"; shift 1
      ;;
    --no-netlist)
      NETLIST_REQUEST="off"; shift 1
      ;;
    --netlist-path)
      NETLIST_PATH="${2:-}"; shift 2
      ;;
    --lvs-report-path)
      LVS_REPORT_PATH="${2:-}"; shift 2
      ;;
    --lvs-thr)
      LVS_THR="${2:-}"; shift 2
      ;;
    --lvs-sub)
      LVS_SUBSTRATE_NAME="${2:-}"; shift 2
      ;;
    --die-width)
      DIE_WIDTH="${2:-}"; shift 2
      ;;
    --die-height)
      DIE_HEIGHT="${2:-}"; shift 2
      ;;
    --io-lib-path)
      IO_LIB_PATH="${2:-}"; shift 2
      ;;
    --tools-root)
      TOOLS_ROOT="${2:-}"; shift 2
      ;;
    --io-yaml)
      IO_YAML="${2:-}"; shift 2
      ;;
    --pad-yaml)
      PAD_YAML="${2:-}"; shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$STEP" != "placement" && "$STEP" != "gds" && "$STEP" != "both" ]]; then
  echo "Invalid --step: $STEP (expected placement|gds|both)" >&2
  exit 2
fi

if [[ ! -f "$PAD_YAML" ]]; then
  echo "Missing pad YAML: $PAD_YAML" >&2
  exit 2
fi

if [[ ! -f "$IO_YAML" ]]; then
  echo "Missing IO YAML: $IO_YAML" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"

maybe_die_width_args=()
maybe_die_height_args=()
if [[ -n "$DIE_WIDTH" ]]; then
  maybe_die_width_args=(--die-width "$DIE_WIDTH")
fi
if [[ -n "$DIE_HEIGHT" ]]; then
  maybe_die_height_args=(--die-height "$DIE_HEIGHT")
fi

maybe_placement_method_args=()
if [[ -n "$PLACEMENT_METHOD" ]]; then
  maybe_placement_method_args=(--placement-method "$PLACEMENT_METHOD")
fi

maybe_metal_stack_args=()
if [[ -n "$METAL_STACK" ]]; then
  maybe_metal_stack_args=(--metal-stack "$METAL_STACK")
fi

if [[ "$STEP" == "placement" || "$STEP" == "both" ]]; then
  echo "Running pad-ring placement generation..."
  "$PYTHON_BIN" "$ROOT_DIR/src/pad_ring_generator.py" \
    --config "$PAD_YAML" \
    --io-lib-path "$IO_LIB_PATH" \
    --output "$PLACEMENT_JSON" \
    "${maybe_die_width_args[@]}" \
    "${maybe_die_height_args[@]}" \
    "${maybe_placement_method_args[@]}"
  echo "Wrote: $PLACEMENT_JSON"
fi

if [[ "$STEP" == "gds" || "$STEP" == "both" ]]; then
  if ! "$PYTHON_BIN" -c "import gdstk" >/dev/null 2>&1; then
    echo "gdstk is required to write GDS, but it is not installed." >&2
    echo "Install: pip install gdstk" >&2
    echo "Or run placement-only: $0 --step placement" >&2
    exit 1
  fi

  echo "Running pad-ring GDS generation..."
  "$PYTHON_BIN" "$ROOT_DIR/src/pad_ring_gds.py" \
    --io-yaml "$IO_YAML" \
    --pad-yaml "$PAD_YAML" \
    --tools-root "$TOOLS_ROOT" \
    --output-gds "$GDS_PATH" \
    --top-cell "$TOP_CELL" \
    --mode "$MODE" \
    "${maybe_metal_stack_args[@]}" \
    "${maybe_die_width_args[@]}" \
    "${maybe_die_height_args[@]}" \
    "${maybe_placement_method_args[@]}"
  echo "Wrote: $GDS_PATH"

  if [[ "$NETLIST_REQUEST" != "off" ]]; then
    if ! command -v klayout >/dev/null 2>&1; then
      if [[ "$NETLIST_REQUEST" == "on" ]]; then
        echo "klayout is required for netlist extraction, but was not found in PATH." >&2
        echo "Install: sudo apt install klayout" >&2
        exit 1
      fi
      echo "Warning: klayout not found; skipping netlist extraction (set --netlist to fail hard)." >&2
    else
      # Resolve metal stack for LVS deck configuration.
      metal_stack_resolved="$METAL_STACK"
      if [[ -z "$metal_stack_resolved" ]]; then
        metal_stack_resolved="$(
          "$PYTHON_BIN" -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1], encoding="utf-8")); print(d.get("default_metal_stack","3lm"))' \
            "$IO_YAML" 2>/dev/null || true
        )"
      fi
      metal_stack_resolved="${metal_stack_resolved:-3lm}"

      metal_top=""
      metal_level=""
      mim_option=""
      case "$metal_stack_resolved" in
        3lm)
          metal_top="30K"
          metal_level="3LM"
          mim_option="A"
          ;;
        4lm)
          metal_top="11K"
          metal_level="4LM"
          mim_option="B"
          ;;
        5lm)
          metal_top="9K"
          metal_level="5LM"
          mim_option="B"
          ;;
        *)
          echo "Unsupported metal stack for LVS deck: '$metal_stack_resolved' (expected 3lm|4lm|5lm)" >&2
          exit 2
          ;;
      esac

      thr_count="$LVS_THR"
      if [[ -z "$thr_count" ]]; then
        thr_base="$(nproc 2>/dev/null || echo 8)"
        thr_count="$((thr_base * 2))"
      fi

      if [[ ! -f "$GF180MCU_LVS_RULESET_PATH" ]]; then
        echo "Missing GF180MCU LVS runset deck: $GF180MCU_LVS_RULESET_PATH" >&2
        exit 2
      fi

      echo "Running KLayout netlist extraction (GF180MCU LVS deck)..."
      klayout -b -r "$GF180MCU_LVS_RULESET_PATH" \
        -rd input="$GDS_PATH" \
        -rd report="$LVS_REPORT_PATH" \
        -rd target_netlist="$NETLIST_PATH" \
        -rd thr="$thr_count" \
        -rd run_mode=deep \
        -rd metal_top="$metal_top" \
        -rd metal_level="$metal_level" \
        -rd mim_option="$mim_option" \
        -rd poly_res=1K \
        -rd mim_cap=2 \
        -rd spice_net_names=true \
        -rd spice_comments=false \
        -rd lvs_sub="$LVS_SUBSTRATE_NAME"

      echo "Wrote extracted netlist: $NETLIST_PATH"
    fi
  fi
fi

