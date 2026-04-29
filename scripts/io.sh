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
REPORT_MD_PATH="${REPORT_MD_PATH:-$OUT_DIR/report.md}"
NETLIST_PATH="${NETLIST_PATH:-$OUT_DIR/pad_ring_extracted.cir}"
LVS_REPORT_PATH="${LVS_REPORT_PATH:-$OUT_DIR/pad_ring.lvsdb}"
DRC_REPORT_PATH="${DRC_REPORT_PATH:-$OUT_DIR/pad_ring_drc.lyrdb}"
TOP_CELL="${TOP_CELL:-PAD_RING_TOP}"

STEP="both" # placement | gds | both (gds stage will also try netlist extraction)
MODE="auto" # auto | real | abstract (for pad_ring_gds)
NETLIST_REQUEST="auto" # auto | on | off
DRC_REQUEST="auto" # auto | on | off
METAL_STACK="" # optional override: 3lm | 4lm | 5lm
LVS_THR="" # optional override for klayout threads (thr). Default: nproc*2
DRC_THR="" # optional override for klayout threads (thr). Default: nproc*2
LVS_SUBSTRATE_NAME="${LVS_SUBSTRATE_NAME:-gf180mcu_gnd}"
GF180MCU_LVS_RULESET_PATH="${GF180MCU_LVS_RULESET_PATH:-$ROOT_DIR/tools/globalfoundries-pdk-libs-gf180mcu_fd_pr/rules/klayout/lvs/gf180mcu.lvs}"
DRC_RUNSET_PATH="${DRC_RUNSET_PATH:-$ROOT_DIR/tools/globalfoundries-pdk-libs-gf180mcu_fd_pr/rules/klayout/drc/gf180mcu.drc}"
LVS_SUB_CLI_SET=0
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
  --drc                      Force DRC execution (requires klayout).
  --no-drc                   Disable DRC execution.
  --report-md PATH           Markdown report path. Default: $REPORT_MD_PATH.
  --netlist-path PATH        Output extracted netlist path. Default: $NETLIST_PATH.
  --lvs-report-path PATH     Output LVS report database path. Default: $LVS_REPORT_PATH.
  --drc-report-path PATH     DRC report database path for report tracking. Default: $DRC_REPORT_PATH.
  --lvs-thr N                KLayout thread count for LVS deck (thr). Default: nproc*2.
  --drc-thr N                KLayout thread count for DRC deck (thr). Default: nproc*2.
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
      REPORT_MD_PATH="$OUT_DIR/report.md"
      NETLIST_PATH="$OUT_DIR/pad_ring_extracted.cir"
      LVS_REPORT_PATH="$OUT_DIR/pad_ring.lvsdb"
      DRC_REPORT_PATH="$OUT_DIR/pad_ring_drc.lyrdb"
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
    --drc)
      DRC_REQUEST="on"; shift 1
      ;;
    --no-drc)
      DRC_REQUEST="off"; shift 1
      ;;
    --report-md)
      REPORT_MD_PATH="${2:-}"; shift 2
      ;;
    --netlist-path)
      NETLIST_PATH="${2:-}"; shift 2
      ;;
    --lvs-report-path)
      LVS_REPORT_PATH="${2:-}"; shift 2
      ;;
    --drc-report-path)
      DRC_REPORT_PATH="${2:-}"; shift 2
      ;;
    --lvs-thr)
      LVS_THR="${2:-}"; shift 2
      ;;
    --drc-thr)
      DRC_THR="${2:-}"; shift 2
      ;;
    --lvs-sub)
      LVS_SUBSTRATE_NAME="${2:-}"; LVS_SUB_CLI_SET=1; shift 2
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

# Resolve signoff defaults from io.yaml (with safe fallback to script defaults).
yaml_runset_and_sub="$(
  "$PYTHON_BIN" -c 'import sys,yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
signoff = d.get("signoff", {}) if isinstance(d, dict) else {}
lvs = signoff.get("lvs", {}) if isinstance(signoff, dict) else {}
runset = lvs.get("runset", "")
substrate = lvs.get("substrate_name", "")
if isinstance(runset, str) and runset:
    print(f"runset={runset}")
if isinstance(substrate, str) and substrate:
    print(f"substrate={substrate}")' \
    "$IO_YAML" 2>/dev/null || true
)"

while IFS='=' read -r key value; do
  case "$key" in
    runset)
      if [[ -n "$value" ]]; then
        if [[ "$value" = /* ]]; then
          GF180MCU_LVS_RULESET_PATH="$value"
        else
          GF180MCU_LVS_RULESET_PATH="$ROOT_DIR/$value"
        fi
      fi
      ;;
    substrate)
      if [[ -n "$value" && "$LVS_SUB_CLI_SET" -eq 0 ]]; then
        LVS_SUBSTRATE_NAME="$value"
      fi
      ;;
  esac
done <<< "$yaml_runset_and_sub"

drc_yaml_settings="$(
  "$PYTHON_BIN" -c 'import sys,yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
signoff = d.get("signoff", {}) if isinstance(d, dict) else {}
drc = signoff.get("drc", {}) if isinstance(signoff, dict) else {}
if isinstance(drc, dict):
    runset = drc.get("runset")
    if isinstance(runset, str) and runset:
        print(f"runset={runset}")
    run_mode = drc.get("run_mode")
    if isinstance(run_mode, str) and run_mode:
        print(f"run_mode={run_mode}")
    enabled = drc.get("enabled")
    if isinstance(enabled, bool):
        print(f"enabled={str(enabled).lower()}")
    switches = drc.get("switches", {})
    if isinstance(switches, dict):
        for key in ("feol", "beol", "offgrid", "conn_drc", "density", "antenna"):
            value = switches.get(key)
            if isinstance(value, bool):
                print(f"{key}={str(value).lower()}")' \
    "$IO_YAML" 2>/dev/null || true
)"

DRC_ENABLED_FROM_YAML="false"
DRC_RUN_MODE="flat"
DRC_FEOL="true"
DRC_BEOL="true"
DRC_OFFGRID="true"
DRC_CONN_DRC="false"
DRC_DENSITY="false"
DRC_ANTENNA="false"
while IFS='=' read -r key value; do
  case "$key" in
    runset)
      if [[ -n "$value" ]]; then
        if [[ "$value" = /* ]]; then
          DRC_RUNSET_PATH="$value"
        else
          DRC_RUNSET_PATH="$ROOT_DIR/$value"
        fi
      fi
      ;;
    run_mode) DRC_RUN_MODE="$value" ;;
    enabled) DRC_ENABLED_FROM_YAML="$value" ;;
    feol) DRC_FEOL="$value" ;;
    beol) DRC_BEOL="$value" ;;
    offgrid) DRC_OFFGRID="$value" ;;
    conn_drc) DRC_CONN_DRC="$value" ;;
    density) DRC_DENSITY="$value" ;;
    antenna) DRC_ANTENNA="$value" ;;
  esac
done <<< "$drc_yaml_settings"

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

NETLIST_STATUS="not-requested"
LVS_STATUS="not-run"
DRC_STATUS="not-run"
if [[ "$DRC_REQUEST" == "off" ]]; then
  DRC_STATUS="disabled"
fi
LVS_EFFECTIVE_STACK=""
LVS_EFFECTIVE_METAL_TOP=""
LVS_EFFECTIVE_METAL_LEVEL=""
LVS_EFFECTIVE_MIM_OPTION=""
LVS_EFFECTIVE_POLY_RES=""
LVS_EFFECTIVE_MIM_CAP=""
DRC_EFFECTIVE_STACK=""
DRC_EFFECTIVE_METAL_TOP=""
DRC_EFFECTIVE_METAL_LEVEL=""
DRC_EFFECTIVE_MIM_OPTION=""

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
    --report-md "$REPORT_MD_PATH" \
    --top-cell "$TOP_CELL" \
    --mode "$MODE" \
    "${maybe_metal_stack_args[@]}" \
    "${maybe_die_width_args[@]}" \
    "${maybe_die_height_args[@]}" \
    "${maybe_placement_method_args[@]}"
  echo "Wrote: $GDS_PATH"
  echo "Wrote: $REPORT_MD_PATH"

  if [[ "$NETLIST_REQUEST" != "off" ]]; then
    NETLIST_STATUS="requested"
    if ! command -v klayout >/dev/null 2>&1; then
      if [[ "$NETLIST_REQUEST" == "on" ]]; then
        echo "klayout is required for netlist extraction, but was not found in PATH." >&2
        echo "Install: sudo apt install klayout" >&2
        exit 1
      fi
      echo "Warning: klayout not found; skipping netlist extraction (set --netlist to fail hard)." >&2
      NETLIST_STATUS="skipped-missing-klayout"
      LVS_STATUS="skipped-missing-klayout"
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

      metal_deck_values="$(
        "$PYTHON_BIN" -c 'import sys,yaml
io_yaml_path, stack = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(io_yaml_path, encoding="utf-8")) or {}
signoff = d.get("signoff", {}) if isinstance(d, dict) else {}
lvs = signoff.get("lvs", {}) if isinstance(signoff, dict) else {}
by_stack = lvs.get("by_metal_stack", {}) if isinstance(lvs, dict) else {}
entry = by_stack.get(stack, {}) if isinstance(by_stack, dict) else {}
defaults = {
    "3lm": {"metal_top": "30K", "metal_level": "3LM", "mim_option": "A", "poly_res": "1K", "mim_cap": "2"},
    "4lm": {"metal_top": "11K", "metal_level": "4LM", "mim_option": "B", "poly_res": "1K", "mim_cap": "2"},
    "5lm": {"metal_top": "9K",  "metal_level": "5LM", "mim_option": "B", "poly_res": "1K", "mim_cap": "2"},
}
base = defaults.get(stack)
if base is None:
    raise SystemExit(1)
if isinstance(entry, dict):
    for key in ("metal_top", "metal_level", "mim_option", "poly_res", "mim_cap"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            base[key] = value
for key in ("metal_top", "metal_level", "mim_option", "poly_res", "mim_cap"):
    print(f"{key}={base[key]}")' \
          "$IO_YAML" "$metal_stack_resolved" 2>/dev/null || true
      )"

      if [[ -z "$metal_deck_values" ]]; then
        echo "Unsupported metal stack for LVS deck: '$metal_stack_resolved' (expected 3lm|4lm|5lm)" >&2
        exit 2
      fi

      metal_top=""
      metal_level=""
      mim_option=""
      poly_res=""
      mim_cap=""
      while IFS='=' read -r key value; do
        case "$key" in
          metal_top) metal_top="$value" ;;
          metal_level) metal_level="$value" ;;
          mim_option) mim_option="$value" ;;
          poly_res) poly_res="$value" ;;
          mim_cap) mim_cap="$value" ;;
        esac
      done <<< "$metal_deck_values"
      LVS_EFFECTIVE_STACK="$metal_stack_resolved"
      LVS_EFFECTIVE_METAL_TOP="$metal_top"
      LVS_EFFECTIVE_METAL_LEVEL="$metal_level"
      LVS_EFFECTIVE_MIM_OPTION="$mim_option"
      LVS_EFFECTIVE_POLY_RES="$poly_res"
      LVS_EFFECTIVE_MIM_CAP="$mim_cap"

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
        -rd poly_res="$poly_res" \
        -rd mim_cap="$mim_cap" \
        -rd spice_net_names=true \
        -rd spice_comments=false \
        -rd lvs_sub="$LVS_SUBSTRATE_NAME"

      echo "Wrote extracted netlist: $NETLIST_PATH"
      NETLIST_STATUS="generated"
      LVS_STATUS="generated"
    fi
  else
    NETLIST_STATUS="disabled"
    LVS_STATUS="disabled"
  fi

  should_run_drc="false"
  if [[ "$DRC_REQUEST" == "on" ]]; then
    should_run_drc="true"
  elif [[ "$DRC_REQUEST" == "auto" && "$DRC_ENABLED_FROM_YAML" == "true" ]]; then
    should_run_drc="true"
  fi

  if [[ "$should_run_drc" == "true" ]]; then
    if ! command -v klayout >/dev/null 2>&1; then
      if [[ "$DRC_REQUEST" == "on" ]]; then
        echo "klayout is required for DRC, but was not found in PATH." >&2
        echo "Install: sudo apt install klayout" >&2
        exit 1
      fi
      echo "Warning: klayout not found; skipping DRC (set --drc to fail hard)." >&2
      DRC_STATUS="skipped-missing-klayout"
    else
      metal_stack_resolved="$METAL_STACK"
      if [[ -z "$metal_stack_resolved" ]]; then
        metal_stack_resolved="$(
          "$PYTHON_BIN" -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1], encoding="utf-8")); print(d.get("default_metal_stack","3lm"))' \
            "$IO_YAML" 2>/dev/null || true
        )"
      fi
      metal_stack_resolved="${metal_stack_resolved:-3lm}"

      drc_stack_values="$(
        "$PYTHON_BIN" -c 'import sys,yaml
io_yaml_path, stack = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(io_yaml_path, encoding="utf-8")) or {}
signoff = d.get("signoff", {}) if isinstance(d, dict) else {}
drc = signoff.get("drc", {}) if isinstance(signoff, dict) else {}
by_stack = drc.get("by_metal_stack", {}) if isinstance(drc, dict) else {}
entry = by_stack.get(stack, {}) if isinstance(by_stack, dict) else {}
defaults = {
    "3lm": {"metal_top": "30K", "metal_level": "3LM", "mim_option": "A"},
    "4lm": {"metal_top": "11K", "metal_level": "4LM", "mim_option": "B"},
    "5lm": {"metal_top": "9K",  "metal_level": "5LM", "mim_option": "B"},
}
base = defaults.get(stack)
if base is None:
    raise SystemExit(1)
if isinstance(entry, dict):
    for key in ("metal_top", "metal_level", "mim_option"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            base[key] = value
for key in ("metal_top", "metal_level", "mim_option"):
    print(f"{key}={base[key]}")' \
          "$IO_YAML" "$metal_stack_resolved" 2>/dev/null || true
      )"
      if [[ -z "$drc_stack_values" ]]; then
        echo "Unsupported metal stack for DRC deck: '$metal_stack_resolved' (expected 3lm|4lm|5lm)" >&2
        exit 2
      fi

      drc_metal_top=""
      drc_metal_level=""
      drc_mim_option=""
      while IFS='=' read -r key value; do
        case "$key" in
          metal_top) drc_metal_top="$value" ;;
          metal_level) drc_metal_level="$value" ;;
          mim_option) drc_mim_option="$value" ;;
        esac
      done <<< "$drc_stack_values"
      DRC_EFFECTIVE_STACK="$metal_stack_resolved"
      DRC_EFFECTIVE_METAL_TOP="$drc_metal_top"
      DRC_EFFECTIVE_METAL_LEVEL="$drc_metal_level"
      DRC_EFFECTIVE_MIM_OPTION="$drc_mim_option"

      drc_thr_count="$DRC_THR"
      if [[ -z "$drc_thr_count" ]]; then
        drc_thr_base="$(nproc 2>/dev/null || echo 8)"
        drc_thr_count="$((drc_thr_base * 2))"
      fi

      if [[ ! -f "$DRC_RUNSET_PATH" ]]; then
        echo "Missing GF180MCU DRC runset deck: $DRC_RUNSET_PATH" >&2
        exit 2
      fi

      echo "Running KLayout DRC (GF180MCU DRC deck)..."
      klayout -b -r "$DRC_RUNSET_PATH" \
        -rd input="$GDS_PATH" \
        -rd report="$DRC_REPORT_PATH" \
        -rd thr="$drc_thr_count" \
        -rd run_mode="$DRC_RUN_MODE" \
        -rd metal_top="$drc_metal_top" \
        -rd metal_level="$drc_metal_level" \
        -rd mim_option="$drc_mim_option" \
        -rd feol="$DRC_FEOL" \
        -rd beol="$DRC_BEOL" \
        -rd offgrid="$DRC_OFFGRID" \
        -rd conn_drc="$DRC_CONN_DRC" \
        -rd density="$DRC_DENSITY" \
        -rd antenna="$DRC_ANTENNA"

      echo "Wrote DRC report DB: $DRC_REPORT_PATH"
      DRC_STATUS="generated"
    fi
  elif [[ "$DRC_REQUEST" == "off" ]]; then
    DRC_STATUS="disabled"
  else
    DRC_STATUS="not-requested"
  fi
fi

if [[ -f "$DRC_REPORT_PATH" ]]; then
  DRC_STATUS="present"
fi

if [[ "$STEP" == "gds" || "$STEP" == "both" ]]; then
  should_run_drc_effective="false"
  if [[ "$DRC_REQUEST" == "on" ]]; then
    should_run_drc_effective="true"
  elif [[ "$DRC_REQUEST" == "auto" && "$DRC_ENABLED_FROM_YAML" == "true" ]]; then
    should_run_drc_effective="true"
  fi

  {
    echo "## Effective Signoff Config"
    echo ""
    echo "| Item | Value |"
    echo "|---|---|"
    echo "| LVS runset | \`$GF180MCU_LVS_RULESET_PATH\` |"
    echo "| LVS substrate | \`$LVS_SUBSTRATE_NAME\` |"
    echo "| LVS stack | \`${LVS_EFFECTIVE_STACK:-n/a}\` |"
    echo "| LVS metal_top | \`${LVS_EFFECTIVE_METAL_TOP:-n/a}\` |"
    echo "| LVS metal_level | \`${LVS_EFFECTIVE_METAL_LEVEL:-n/a}\` |"
    echo "| LVS mim_option | \`${LVS_EFFECTIVE_MIM_OPTION:-n/a}\` |"
    echo "| LVS poly_res | \`${LVS_EFFECTIVE_POLY_RES:-n/a}\` |"
    echo "| LVS mim_cap | \`${LVS_EFFECTIVE_MIM_CAP:-n/a}\` |"
    echo "| DRC enabled (effective) | \`$should_run_drc_effective\` |"
    echo "| DRC runset | \`$DRC_RUNSET_PATH\` |"
    echo "| DRC run_mode | \`$DRC_RUN_MODE\` |"
    echo "| DRC feol | \`$DRC_FEOL\` |"
    echo "| DRC beol | \`$DRC_BEOL\` |"
    echo "| DRC offgrid | \`$DRC_OFFGRID\` |"
    echo "| DRC conn_drc | \`$DRC_CONN_DRC\` |"
    echo "| DRC density | \`$DRC_DENSITY\` |"
    echo "| DRC antenna | \`$DRC_ANTENNA\` |"
    echo "| DRC stack | \`${DRC_EFFECTIVE_STACK:-n/a}\` |"
    echo "| DRC metal_top | \`${DRC_EFFECTIVE_METAL_TOP:-n/a}\` |"
    echo "| DRC metal_level | \`${DRC_EFFECTIVE_METAL_LEVEL:-n/a}\` |"
    echo "| DRC mim_option | \`${DRC_EFFECTIVE_MIM_OPTION:-n/a}\` |"
    echo ""
    echo "## Signoff Artifacts"
    echo ""
    echo "| Item | Status | Path |"
    echo "|---|---|---|"
    echo "| GDS | $( [[ -f "$GDS_PATH" ]] && echo "generated" || echo "missing" ) | \`$GDS_PATH\` |"
    echo "| Netlist (extracted) | $( [[ -f "$NETLIST_PATH" ]] && echo "generated" || echo "$NETLIST_STATUS" ) | \`$NETLIST_PATH\` |"
    echo "| LVS report DB | $( [[ -f "$LVS_REPORT_PATH" ]] && echo "generated" || echo "$LVS_STATUS" ) | \`$LVS_REPORT_PATH\` |"
    echo "| DRC report DB | $( [[ -f "$DRC_REPORT_PATH" ]] && echo "present" || echo "$DRC_STATUS" ) | \`$DRC_REPORT_PATH\` |"
    echo ""
    echo "### Notes"
    echo ""
    echo "- DRC execution is controlled by \`--drc/--no-drc\` or \`signoff.drc.enabled\` in \`io.yaml\`."
    echo "- LVS row reflects the KLayout extraction step used for netlist generation."
    echo ""
  } >> "$REPORT_MD_PATH"
  echo "Updated report with signoff artifacts: $REPORT_MD_PATH"
fi

