"""Tests for pad ring filler placement behavior."""

from __future__ import annotations

import pytest

from pad_ring_generator import CellSize, make_fillers, resolve_die_size


def test_make_fillers_closes_gap_exactly() -> None:
    """Ensure filler generation closes a simple horizontal gap exactly."""

    size_by_cell: dict[str, CellSize] = {
        "fill10": CellSize(width=10.0, height=350.0),
        "fill5": CellSize(width=5.0, height=350.0),
        "fill1": CellSize(width=1.0, height=350.0),
    }

    placements = make_fillers(
        side="south",
        start=0.0,
        fixed_coord=0.0,
        gap=16.0,
        filler_cells=["fill10", "fill5", "fill1"],
        size_by_cell=size_by_cell,
    )

    cells: list[str] = [item.cell for item in placements]
    total_width: float = sum(item.width for item in placements)

    assert cells == ["fill10", "fill5", "fill1"]
    assert total_width == 16.0


def test_resolve_die_size_from_yaml() -> None:
    """Ensure die size can be fully sourced from YAML config."""

    die_width, die_height = resolve_die_size(
        config={"die": {"width": 1000, "height": 800}},
        cli_die_width=None,
        cli_die_height=None,
    )

    assert die_width == 1000.0
    assert die_height == 800.0


def test_resolve_die_size_cli_overrides_yaml() -> None:
    """Ensure CLI die size values override YAML die dimensions."""

    die_width, die_height = resolve_die_size(
        config={"die": {"width": 1000, "height": 800}},
        cli_die_width=1200.0,
        cli_die_height=900.0,
    )

    assert die_width == 1200.0
    assert die_height == 900.0


def test_resolve_die_size_requires_values() -> None:
    """Ensure missing die dimensions raises a clear error."""

    with pytest.raises(ValueError, match="Die size is required"):
        resolve_die_size(config={}, cli_die_width=None, cli_die_height=None)
