"""Tests for YAML-driven pad-ring placement preparation."""

from __future__ import annotations

from pathlib import Path

import pytest

from pad_ring_gds import (
    build_placements_from_yaml,
    find_cell_gds,
    load_io_sizes,
    resolve_metal_stack,
)


def test_load_io_sizes_parses_cells() -> None:
    """Ensure IO YAML cell dimensions are converted to CellSize values."""

    io_yaml = {
        "cells": {
            "cor": {"width": 355.0, "height": 355.0},
            "fill1": {"width": 1.0, "height": 350.0},
        }
    }
    sizes = load_io_sizes(io_yaml)

    assert sizes["cor"].width == 355.0
    assert sizes["fill1"].height == 350.0


def test_build_placements_from_yaml_with_small_ring() -> None:
    """Ensure placements are generated from io/pad YAML structures."""

    io_yaml = {
        "cells": {
            "cor": {"width": 355.0, "height": 355.0},
            "fill10": {"width": 10.0, "height": 350.0},
            "fill5": {"width": 5.0, "height": 350.0},
            "fill1": {"width": 1.0, "height": 350.0},
            "fillnc": {"width": 0.1, "height": 350.0},
            "in_c": {"width": 75.0, "height": 350.0},
            "bi_t": {"width": 75.0, "height": 350.0},
            "dvdd": {"width": 75.0, "height": 350.0},
            "dvss": {"width": 75.0, "height": 350.0},
        }
    }
    pad_yaml = {
        "die": {"width": 2000, "height": 2000},
        "sides": {
            "north": [{"name": "U_N0", "cell": "in_c"}],
            "south": [{"name": "U_S0", "cell": "bi_t"}],
            "east": [{"name": "U_E0", "cell": "dvdd"}],
            "west": [{"name": "U_W0", "cell": "dvss"}],
        },
        "corners": {"nw": "cor", "ne": "cor", "se": "cor", "sw": "cor"},
        "filler_cells": ["fill10", "fill5", "fill1", "fillnc"],
    }

    die_width, die_height, placements = build_placements_from_yaml(
        io_yaml=io_yaml,
        pad_yaml=pad_yaml,
        die_width_override=None,
        die_height_override=None,
        placement_method="packed",
    )

    assert die_width == 2000.0
    assert die_height == 2000.0
    assert len([item for item in placements if item.kind == "corner"]) == 4
    assert len([item for item in placements if item.kind == "pad"]) == 4


def test_build_placements_raises_on_missing_cells() -> None:
    """Ensure missing referenced cells in io.yaml raise a clear error."""

    io_yaml = {"cells": {"cor": {"width": 355.0, "height": 355.0}}}
    pad_yaml = {
        "die": {"width": 2000, "height": 2000},
        "sides": {"north": [{"name": "U_N0", "cell": "in_c"}]},
    }

    with pytest.raises(ValueError, match="Missing cells in io.yaml"):
        build_placements_from_yaml(
            io_yaml=io_yaml,
            pad_yaml=pad_yaml,
            die_width_override=None,
            die_height_override=None,
            placement_method="packed",
        )


def test_resolve_metal_stack_defaults_to_3lm() -> None:
    """Ensure default metal stack is 3lm when io.yaml has no default."""

    assert resolve_metal_stack(io_yaml={}, cli_metal_stack=None) == "3lm"


def test_resolve_metal_stack_prefers_cli() -> None:
    """Ensure CLI metal stack override takes precedence over io.yaml."""

    io_yaml = {"default_metal_stack": "3lm"}
    assert resolve_metal_stack(io_yaml=io_yaml, cli_metal_stack="5lm") == "5lm"


def test_find_cell_gds_returns_none_when_missing(tmp_path: Path) -> None:
    """Ensure GDS lookup returns None when no matching layout file exists."""

    assert find_cell_gds(tools_root=tmp_path, cell_name="in_c", metal_stack="3lm") is None
