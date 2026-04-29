"""Generate IO pad-ring placement from a YAML specification.

This script reads a user-provided YAML file and die dimensions, then:
1. Places corner pads.
2. Places user-specified IO pads per side.
3. Inserts filler cells to close remaining side gaps.

Output is emitted as JSON for easy downstream processing.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class CellSize:
    """Physical cell size parsed from LEF.

    Attributes:
        width: Cell width in microns.
        height: Cell height in microns.
    """

    width: float
    height: float


@dataclass(frozen=True)
class InstanceRequest:
    """User-requested IO pad instance.

    Attributes:
        name: Instance name.
        cell: IO cell name.
    """

    name: str
    cell: str


@dataclass(frozen=True)
class Placement:
    """Single placed object in the pad ring.

    Attributes:
        name: Instance name.
        cell: Library cell name.
        side: Ring side or corner tag.
        kind: Placement kind, e.g. "corner", "pad", or "filler".
        x: Lower-left x-coordinate in microns.
        y: Lower-left y-coordinate in microns.
        width: Placed width in microns.
        height: Placed height in microns.
        orientation: Orientation hint for PnR flow.
    """

    name: str
    cell: str
    side: str
    kind: str
    x: float
    y: float
    width: float
    height: float
    orientation: str


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Pad-ring and filler generator.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to YAML config file.",
    )
    parser.add_argument(
        "--die-width",
        type=float,
        default=None,
        help="Die width in um. Overrides YAML die.width.",
    )
    parser.add_argument(
        "--die-height",
        type=float,
        default=None,
        help="Die height in um. Overrides YAML die.height.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("pad_ring_placement.json"),
        help="Output JSON path.",
    )
    parser.add_argument(
        "--io-lib-path",
        type=Path,
        default=Path("tools/globalfoundries-pdk-libs-gf180mcu_fd_io/cells"),
        help="Path to IO cell directories containing LEF files.",
    )
    parser.add_argument(
        "--placement-method",
        type=str,
        choices=["packed", "even"],
        default=None,
        help=(
            "Pad placement style per side: packed (legacy) or even spacing. "
            "Overrides config placement_method when set."
        ),
    )
    return parser.parse_args()


def read_yaml(path: Path) -> dict[str, Any]:
    """Read and validate YAML config.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML mapping.

    Raises:
        ValueError: If YAML is empty or not a dictionary.
    """

    content: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError("YAML root must be a mapping.")
    return content


def resolve_die_size(
    config: dict[str, Any],
    cli_die_width: float | None,
    cli_die_height: float | None,
) -> tuple[float, float]:
    """Resolve die size from YAML and optional CLI overrides.

    Args:
        config: Parsed YAML configuration dictionary.
        cli_die_width: Optional CLI die width.
        cli_die_height: Optional CLI die height.

    Returns:
        Resolved die width and height in microns.

    Raises:
        ValueError: If die dimensions are missing or invalid.
    """

    die_any: Any = config.get("die", {})
    yaml_die_width: float | None = None
    yaml_die_height: float | None = None
    if die_any:
        if not isinstance(die_any, dict):
            raise ValueError("config.die must be a mapping when provided.")
        yaml_width_any: Any = die_any.get("width")
        yaml_height_any: Any = die_any.get("height")
        if yaml_width_any is not None:
            if not isinstance(yaml_width_any, (float, int)):
                raise ValueError("config.die.width must be numeric.")
            yaml_die_width = float(yaml_width_any)
        if yaml_height_any is not None:
            if not isinstance(yaml_height_any, (float, int)):
                raise ValueError("config.die.height must be numeric.")
            yaml_die_height = float(yaml_height_any)

    die_width: float | None = cli_die_width if cli_die_width is not None else yaml_die_width
    die_height: float | None = (
        cli_die_height if cli_die_height is not None else yaml_die_height
    )

    if die_width is None or die_height is None:
        raise ValueError(
            "Die size is required. Provide --die-width/--die-height or config.die.width/height."
        )
    if die_width <= 0.0 or die_height <= 0.0:
        raise ValueError("Die dimensions must be > 0.")
    return die_width, die_height


def parse_cell_size(io_lib_path: Path, cell: str) -> CellSize:
    """Parse size from the cell's 5LM LEF file.

    Args:
        io_lib_path: Root path containing per-cell directories.
        cell: Cell name, e.g. "bi_t".

    Returns:
        Parsed CellSize.

    Raises:
        FileNotFoundError: If LEF file cannot be found.
        ValueError: If SIZE line is missing.
    """

    lef_path: Path = io_lib_path / cell / f"gf180mcu_fd_io__{cell}_5lm.lef"
    if not lef_path.exists():
        raise FileNotFoundError(f"LEF not found for cell '{cell}': {lef_path}")

    text: str = lef_path.read_text(encoding="utf-8")
    match: re.Match[str] | None = re.search(
        r"^\s*SIZE\s+([0-9.]+)\s+BY\s+([0-9.]+)\s*;\s*$",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"Could not parse SIZE in {lef_path}")
    width: float = float(match.group(1))
    height: float = float(match.group(2))
    return CellSize(width=width, height=height)


def to_instance_requests(raw: list[dict[str, Any]], side: str) -> list[InstanceRequest]:
    """Convert side entries to typed requests.

    Args:
        raw: YAML list for a side.
        side: Side name used for error context.

    Returns:
        Typed instance requests.

    Raises:
        ValueError: If entries are malformed.
    """

    requests: list[InstanceRequest] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"Invalid entry at {side}[{index}]; expected mapping.")
        name: Any = entry.get("name")
        cell: Any = entry.get("cell")
        if not isinstance(name, str) or not isinstance(cell, str):
            raise ValueError(f"{side}[{index}] requires string fields: name, cell.")
        requests.append(InstanceRequest(name=name, cell=cell))
    return requests


def resolve_placement_method(config: dict[str, Any], cli_placement_method: str | None) -> str:
    """Resolve placement method from CLI override or YAML config.

    Args:
        config: Parsed YAML configuration dictionary.
        cli_placement_method: Optional CLI override.

    Returns:
        Placement method, one of "packed" or "even".

    Raises:
        ValueError: If the configured placement method is invalid.
    """

    if cli_placement_method is not None:
        return cli_placement_method
    placement_method_any: Any = config.get("placement_method", "packed")
    if placement_method_any not in {"packed", "even"}:
        raise ValueError("config placement_method must be one of: packed, even.")
    return placement_method_any


def make_fillers(
    side: str,
    start: float,
    fixed_coord: float,
    gap: float,
    filler_cells: list[str],
    size_by_cell: dict[str, CellSize],
    filler_start_index: int = 0,
) -> tuple[list[Placement], int]:
    """Generate filler placements greedily to close a side gap.

    Args:
        side: Side name, one of north/south/east/west.
        start: Start coordinate along side axis.
        fixed_coord: Orthogonal coordinate.
        gap: Gap length in microns.
        filler_cells: Filler cells from large to small preference.
        size_by_cell: Cell size lookup.

    Returns:
        List of filler placements.

    Raises:
        ValueError: If the gap cannot be closed with available fillers.
    """

    placements: list[Placement] = []
    cursor: float = start
    remaining: float = gap
    filler_count: int = filler_start_index
    tol: float = 1e-6

    while remaining > tol:
        placed: bool = False
        for filler_cell in filler_cells:
            size: CellSize = size_by_cell[filler_cell]
            span: float = size.width
            if span <= remaining + tol:
                name: str = f"{side}_filler_{filler_count}"
                if side in {"north", "south"}:
                    placed_width: float = size.width
                    placed_height: float = size.height
                else:
                    placed_width = size.height
                    placed_height = size.width
                if side in {"north", "south"}:
                    x_value: float = cursor
                    y_value: float = fixed_coord
                else:
                    x_value = fixed_coord
                    y_value = cursor
                placements.append(
                    Placement(
                        name=name,
                        cell=filler_cell,
                        side=side,
                        kind="filler",
                        x=round(x_value, 6),
                        y=round(y_value, 6),
                        width=placed_width,
                        height=placed_height,
                        orientation=side_orientation(side),
                    )
                )
                cursor += span
                remaining -= span
                filler_count += 1
                placed = True
                break
        if not placed:
            raise ValueError(
                f"Unfillable gap on {side}: remaining={remaining:.6f} um. "
                "Provide a smaller filler cell."
            )
    return placements, filler_count


def side_orientation(side: str) -> str:
    """Map side name to a default orientation label."""

    mapping: dict[str, str] = {
        "south": "R0",
        "east": "R90",
        "north": "R180",
        "west": "R270",
    }
    return mapping.get(side, "R0")


def place_side(
    *,
    side: str,
    requests: list[InstanceRequest],
    die_width: float,
    die_height: float,
    corner_span_start: float,
    corner_span_end: float,
    filler_cells: list[str],
    size_by_cell: dict[str, CellSize],
    placement_method: str = "packed",
) -> list[Placement]:
    """Place pads and fillers for one side.

    Args:
        side: Side name, one of north/south/east/west.
        requests: Ordered pad list for this side.
        die_width: Die width in microns.
        die_height: Die height in microns.
        corner_span_start: Reserved corner span at side start.
        corner_span_end: Reserved corner span at side end.
        filler_cells: Filler cells from large to small preference.
        size_by_cell: Size lookup for all cells used.
        placement_method: Placement method, one of "packed" or "even".

    Returns:
        Ordered placements for this side.

    Raises:
        ValueError: If fixed cells exceed available side length.
    """

    side_length: float = die_width if side in {"north", "south"} else die_height
    side_start: float = corner_span_start
    side_end: float = side_length - corner_span_end
    available: float = side_end - side_start

    fixed_span: float = 0.0
    for request in requests:
        size: CellSize = size_by_cell[request.cell]
        fixed_span += size.width

    if fixed_span - available > 1e-6:
        raise ValueError(
            f"Pads on {side} exceed available side length: fixed={fixed_span}, "
            f"available={available}"
        )

    placements: list[Placement] = []

    if side == "south":
        filler_fixed_coord: float = 0.0
    elif side == "north":
        filler_fixed_coord = die_height - size_by_cell[filler_cells[0]].height
    elif side == "east":
        filler_fixed_coord = die_width - size_by_cell[filler_cells[0]].height
    else:
        filler_fixed_coord = 0.0

    if placement_method == "even":
        gap_count: int = len(requests) + 1
        total_gap: float = available - fixed_span
        min_filler_span: float = min(size_by_cell[cell].width for cell in filler_cells)
        if min_filler_span <= 0.0:
            raise ValueError("Filler cells must have positive width.")
        raw_units: float = total_gap / min_filler_span
        total_units: int = int(round(raw_units))
        if abs(raw_units - total_units) > 1e-6:
            raise ValueError(
                f"Even gap budget on {side} is not fillable with filler pitch {min_filler_span}: "
                f"total_gap={total_gap:.6f}."
            )
        base_units: int = total_units // gap_count
        extra_units: int = total_units % gap_count
        gap_targets: list[float] = [
            (base_units + (1 if index < extra_units else 0)) * min_filler_span
            for index in range(gap_count)
        ]
        cursor: float = side_start
        filler_index: int = 0

        for index, request in enumerate(requests):
            gap_value: float = gap_targets[index]
            if gap_value > 1e-6:
                gap_fillers, filler_index = make_fillers(
                    side=side,
                    start=cursor,
                    fixed_coord=filler_fixed_coord,
                    gap=gap_value,
                    filler_cells=filler_cells,
                    size_by_cell=size_by_cell,
                    filler_start_index=filler_index,
                )
                placements.extend(gap_fillers)
                cursor += gap_value

            size = size_by_cell[request.cell]
            if side in {"north", "south"}:
                placed_width: float = size.width
                placed_height: float = size.height
            else:
                placed_width = size.height
                placed_height = size.width
            if side == "south":
                x_value: float = cursor
                y_value: float = 0.0
            elif side == "north":
                x_value = cursor
                y_value = die_height - placed_height
            elif side == "east":
                x_value = die_width - placed_width
                y_value = cursor
            else:
                x_value = 0.0
                y_value = cursor

            placements.append(
                Placement(
                    name=request.name,
                    cell=request.cell,
                    side=side,
                    kind="pad",
                    x=round(x_value, 6),
                    y=round(y_value, 6),
                    width=placed_width,
                    height=placed_height,
                    orientation=side_orientation(side),
                )
            )
            cursor += size.width

        final_gap_value: float = gap_targets[-1]
        if final_gap_value > 1e-6:
            gap_fillers, filler_index = make_fillers(
                side=side,
                start=cursor,
                fixed_coord=filler_fixed_coord,
                gap=final_gap_value,
                filler_cells=filler_cells,
                size_by_cell=size_by_cell,
                filler_start_index=filler_index,
            )
            placements.extend(gap_fillers)
        return placements

    cursor: float = side_start
    for request in requests:
        size = size_by_cell[request.cell]
        if side in {"north", "south"}:
            placed_width: float = size.width
            placed_height: float = size.height
        else:
            placed_width = size.height
            placed_height = size.width
        if side == "south":
            x_value: float = cursor
            y_value: float = 0.0
        elif side == "north":
            x_value = cursor
            y_value = die_height - placed_height
        elif side == "east":
            x_value = die_width - placed_width
            y_value = cursor
        else:
            x_value = 0.0
            y_value = cursor

        placements.append(
            Placement(
                name=request.name,
                cell=request.cell,
                side=side,
                kind="pad",
                x=round(x_value, 6),
                y=round(y_value, 6),
                width=placed_width,
                height=placed_height,
                orientation=side_orientation(side),
            )
        )
        cursor += size.width

    remaining_gap: float = available - fixed_span
    if remaining_gap > 1e-6:
        tail_fillers, _ = make_fillers(
            side=side,
            start=cursor,
            fixed_coord=filler_fixed_coord,
            gap=remaining_gap,
            filler_cells=filler_cells,
            size_by_cell=size_by_cell,
        )
        placements.extend(tail_fillers)

    return placements


def build_corner_placements(
    die_width: float,
    die_height: float,
    corner_cells: dict[str, str],
    size_by_cell: dict[str, CellSize],
) -> list[Placement]:
    """Create placements for four corner pads."""

    sw_cell: str = corner_cells["sw"]
    se_cell: str = corner_cells["se"]
    ne_cell: str = corner_cells["ne"]
    nw_cell: str = corner_cells["nw"]

    sw_size: CellSize = size_by_cell[sw_cell]
    se_size: CellSize = size_by_cell[se_cell]
    ne_size: CellSize = size_by_cell[ne_cell]
    nw_size: CellSize = size_by_cell[nw_cell]

    return [
        Placement(
            name="corner_sw",
            cell=sw_cell,
            side="corner_sw",
            kind="corner",
            x=0.0,
            y=0.0,
            width=sw_size.width,
            height=sw_size.height,
            orientation="R0",
        ),
        Placement(
            name="corner_se",
            cell=se_cell,
            side="corner_se",
            kind="corner",
            x=round(die_width - se_size.width, 6),
            y=0.0,
            width=se_size.width,
            height=se_size.height,
            orientation="R90",
        ),
        Placement(
            name="corner_ne",
            cell=ne_cell,
            side="corner_ne",
            kind="corner",
            x=round(die_width - ne_size.width, 6),
            y=round(die_height - ne_size.height, 6),
            width=ne_size.width,
            height=ne_size.height,
            orientation="R180",
        ),
        Placement(
            name="corner_nw",
            cell=nw_cell,
            side="corner_nw",
            kind="corner",
            x=0.0,
            y=round(die_height - nw_size.height, 6),
            width=nw_size.width,
            height=nw_size.height,
            orientation="R270",
        ),
    ]


def main() -> None:
    """Run pad-ring generation from CLI inputs."""

    args = parse_args()
    config: dict[str, Any] = read_yaml(args.config)
    die_width, die_height = resolve_die_size(config, args.die_width, args.die_height)
    placement_method: str = resolve_placement_method(config, args.placement_method)

    raw_sides: dict[str, Any] = config.get("sides", {})
    if not isinstance(raw_sides, dict):
        raise ValueError("config.sides must be a mapping.")

    filler_cells_any: Any = config.get("filler_cells", ["fill10", "fill5", "fill1", "fillnc"])
    if not isinstance(filler_cells_any, list) or not all(
        isinstance(item, str) for item in filler_cells_any
    ):
        raise ValueError("config.filler_cells must be a list[str].")
    filler_cells: list[str] = filler_cells_any

    corners_any: Any = config.get("corners", {})
    corner_cells: dict[str, str] = {
        "sw": "cor",
        "se": "cor",
        "ne": "cor",
        "nw": "cor",
    }
    if isinstance(corners_any, dict):
        for key in corner_cells:
            value: Any = corners_any.get(key)
            if value is not None:
                if not isinstance(value, str):
                    raise ValueError(f"corners.{key} must be a string.")
                corner_cells[key] = value

    sides: dict[str, list[InstanceRequest]] = {
        "north": to_instance_requests(raw_sides.get("north", []), "north"),
        "south": to_instance_requests(raw_sides.get("south", []), "south"),
        "east": to_instance_requests(raw_sides.get("east", []), "east"),
        "west": to_instance_requests(raw_sides.get("west", []), "west"),
    }

    all_cells: set[str] = set(filler_cells)
    all_cells.update(corner_cells.values())
    for side_entries in sides.values():
        all_cells.update(item.cell for item in side_entries)

    size_by_cell: dict[str, CellSize] = {
        cell: parse_cell_size(args.io_lib_path, cell) for cell in sorted(all_cells)
    }

    corners: list[Placement] = build_corner_placements(
        die_width=die_width,
        die_height=die_height,
        corner_cells=corner_cells,
        size_by_cell=size_by_cell,
    )

    sw_width: float = size_by_cell[corner_cells["sw"]].width
    se_width: float = size_by_cell[corner_cells["se"]].width
    nw_width: float = size_by_cell[corner_cells["nw"]].width
    ne_width: float = size_by_cell[corner_cells["ne"]].width
    sw_height: float = size_by_cell[corner_cells["sw"]].height
    nw_height: float = size_by_cell[corner_cells["nw"]].height
    se_height: float = size_by_cell[corner_cells["se"]].height
    ne_height: float = size_by_cell[corner_cells["ne"]].height

    placements: list[Placement] = []
    placements.extend(corners)
    placements.extend(
        place_side(
            side="south",
            requests=sides["south"],
            die_width=die_width,
            die_height=die_height,
            corner_span_start=sw_width,
            corner_span_end=se_width,
            filler_cells=filler_cells,
            size_by_cell=size_by_cell,
            placement_method=placement_method,
        )
    )
    placements.extend(
        place_side(
            side="north",
            requests=sides["north"],
            die_width=die_width,
            die_height=die_height,
            corner_span_start=nw_width,
            corner_span_end=ne_width,
            filler_cells=filler_cells,
            size_by_cell=size_by_cell,
            placement_method=placement_method,
        )
    )
    placements.extend(
        place_side(
            side="west",
            requests=sides["west"],
            die_width=die_width,
            die_height=die_height,
            corner_span_start=sw_height,
            corner_span_end=nw_height,
            filler_cells=filler_cells,
            size_by_cell=size_by_cell,
            placement_method=placement_method,
        )
    )
    placements.extend(
        place_side(
            side="east",
            requests=sides["east"],
            die_width=die_width,
            die_height=die_height,
            corner_span_start=se_height,
            corner_span_end=ne_height,
            filler_cells=filler_cells,
            size_by_cell=size_by_cell,
            placement_method=placement_method,
        )
    )

    payload: dict[str, Any] = {
        "die": {"width": die_width, "height": die_height},
        "placements": [placement.__dict__ for placement in placements],
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote placement: {args.output}")


if __name__ == "__main__":
    main()
