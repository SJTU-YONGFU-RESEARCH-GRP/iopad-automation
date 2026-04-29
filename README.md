# IOPad Automation

![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)

Automates IO pad-ring placement, GDS generation, and optional signoff artifact generation (LVS/DRC) for GF180MCU-based flows.

## Project Structure

- `config/`: YAML configuration inputs used by the flow.
  - `config/io.yaml`: IO library metadata, default metal stack, and signoff settings.
  - `config/pad.yaml`: pad-ring topology and placement constraints.
- `scripts/io.sh`: main entrypoint for placement, GDS generation, and optional signoff tasks.
- `src/`: Python implementation of placement and GDS generators.
- `artifacts/`: generated outputs (placement JSON, GDS, reports, extracted netlist, DRC/LVS DB).

## Prerequisites

- Python 3.10+
- Bash
- Python dependencies in `requirements.txt`
- Optional:
  - `gdstk` for GDS writing
  - `klayout` for netlist extraction and DRC

## Quick Start

Install dependencies (example):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run full flow (placement + GDS):

```bash
bash scripts/io.sh --step both
```

Run placement only:

```bash
bash scripts/io.sh --step placement
```

## Using `config/`

The flow reads both config files by default:

- `IO_YAML` defaults to `config/io.yaml`
- `PAD_YAML` defaults to `config/pad.yaml`

Override them from CLI:

```bash
bash scripts/io.sh --io-yaml config/io.yaml --pad-yaml config/pad.yaml
```

Useful knobs in `config/io.yaml`:

- `default_metal_stack`: default process stack (`3lm`, `4lm`, `5lm`)
- `signoff.lvs`: LVS runset, substrate, and stack-specific deck variables
- `signoff.drc`: DRC enable flag, runset, and switches

Useful knobs in `config/pad.yaml`:

- `die.width` / `die.height`
- `placement_method` (`packed` or `even`)
- side placements under `sides.*`
- `corners` and `filler_cells`

## Using `scripts/io.sh`

Main options:

- `--step placement|gds|both`
- `--out-dir <dir>`
- `--mode auto|real|abstract`
- `--metal-stack 3lm|4lm|5lm`
- `--placement-method packed|even`
- `--die-width <um>` / `--die-height <um>`
- `--netlist` / `--no-netlist`
- `--drc` / `--no-drc`

Example with custom output and signoff:

```bash
bash scripts/io.sh \
  --step both \
  --out-dir artifacts \
  --metal-stack 3lm \
  --netlist \
  --drc
```

Show all script options:

```bash
bash scripts/io.sh --help
```

## Outputs

Default generated files in `artifacts/`:

- `pad_ring_placement.json`
- `pad_ring_abstract.gds` (or configured GDS path)
- `report.md`
- `pad_ring_extracted.cir` (if netlist extraction runs)
- `pad_ring.lvsdb` (if LVS extraction runs)
- `pad_ring_drc.lyrdb` (if DRC runs)

## License

This project is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
See `LICENSE` for the full text.
