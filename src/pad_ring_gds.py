"""Generate pad-ring GDS from YAML inputs.

This script consumes:
- `io.yaml`: IO cell dimensions and metadata.
- `pad.yaml`: Die size and pad-ring intent (sides/corners/fillers).

It computes placements using the same logic as `pad_ring_generator.py` and
supports two output modes:
- Real mode: instantiate per-cell GDS references (when layout views exist).
- Abstract mode: emit rectangle boundaries as placeholders.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
from dataclasses import dataclass

import yaml

from pad_ring_generator import (
    CellSize,
    InstanceRequest,
    Placement,
    build_corner_placements,
    place_side,
    resolve_die_size,
    to_instance_requests,
)


@dataclass(frozen=True)
class GenerationStats:
    """Summary statistics for a GDS generation run."""

    total_instances: int
    real_placed: int
    abstract_fallback: int
    by_kind: dict[str, int]
    by_cell: dict[str, int]
    fallback_cells: list[str]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for GDS generation."""

    parser = argparse.ArgumentParser(description="Generate pad-ring GDS.")
    parser.add_argument("--io-yaml", type=Path, required=True, help="Path to io.yaml.")
    parser.add_argument("--pad-yaml", type=Path, required=True, help="Path to pad.yaml.")
    parser.add_argument(
        "--tools-root",
        type=Path,
        default=Path("tools/globalfoundries-pdk-libs-gf180mcu_fd_io"),
        help="IO library root path used for LEF/GDS view lookup.",
    )
    parser.add_argument(
        "--output-gds",
        type=Path,
        default=Path("pad_ring_abstract.gds"),
        help="Output GDS file path.",
    )
    parser.add_argument(
        "--top-cell",
        type=str,
        default="PAD_RING_TOP",
        help="Top-level GDS cell name.",
    )
    parser.add_argument(
        "--die-width",
        type=float,
        default=None,
        help="Optional die width override in um.",
    )
    parser.add_argument(
        "--die-height",
        type=float,
        default=None,
        help="Optional die height override in um.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["auto", "real", "abstract"],
        default="auto",
        help="GDS output mode. 'auto' tries real-cell mode then falls back to abstract.",
    )
    parser.add_argument(
        "--metal-stack",
        type=str,
        default=None,
        help="Layout view selector (e.g. 3lm/4lm/5lm). Defaults to io.yaml default.",
    )
    parser.add_argument(
        "--report-md",
        type=Path,
        default=None,
        help="Optional Markdown report output path.",
    )
    parser.add_argument(
        "--placement-method",
        type=str,
        choices=["packed", "even"],
        default=None,
        help=(
            "Pad placement style per side: packed (legacy) or even spacing. "
            "Overrides pad.yaml placement_method when set."
        ),
    )
    return parser.parse_args()


def read_yaml(path: Path) -> dict[str, Any]:
    """Read YAML file and validate root mapping."""

    content: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return content


def load_io_sizes(io_yaml: dict[str, Any]) -> dict[str, CellSize]:
    """Load `CellSize` map from `io.yaml`.

    Args:
        io_yaml: Parsed io.yaml content.

    Returns:
        Mapping of cell name to cell size.

    Raises:
        ValueError: If required fields are missing or invalid.
    """

    cells_any: Any = io_yaml.get("cells")
    if not isinstance(cells_any, dict):
        raise ValueError("io.yaml requires a 'cells' mapping.")

    size_by_cell: dict[str, CellSize] = {}
    for cell_name, cell_info_any in cells_any.items():
        if not isinstance(cell_name, str) or not isinstance(cell_info_any, dict):
            raise ValueError("Invalid cell entry in io.yaml.")
        width_any: Any = cell_info_any.get("width")
        height_any: Any = cell_info_any.get("height")
        if not isinstance(width_any, (int, float)) or not isinstance(height_any, (int, float)):
            raise ValueError(f"io.yaml cell '{cell_name}' requires numeric width/height.")
        width: float = float(width_any)
        height: float = float(height_any)
        if width <= 0.0 or height <= 0.0:
            raise ValueError(f"io.yaml cell '{cell_name}' has non-positive dimensions.")
        size_by_cell[cell_name] = CellSize(width=width, height=height)
    return size_by_cell


def resolve_metal_stack(io_yaml: dict[str, Any], cli_metal_stack: str | None) -> str:
    """Resolve selected metal stack from CLI or io.yaml default."""

    if cli_metal_stack is not None:
        return cli_metal_stack
    default_any: Any = io_yaml.get("default_metal_stack")
    if isinstance(default_any, str) and default_any:
        return default_any
    return "3lm"


def resolve_placement_method(pad_yaml: dict[str, Any], cli_placement_method: str | None) -> str:
    """Resolve placement method from CLI or pad.yaml.

    Args:
        pad_yaml: Parsed pad.yaml content.
        cli_placement_method: Optional CLI override.

    Returns:
        Resolved placement method.

    Raises:
        ValueError: If pad.yaml placement method is invalid.
    """

    if cli_placement_method is not None:
        return cli_placement_method
    placement_method_any: Any = pad_yaml.get("placement_method", "packed")
    if placement_method_any not in {"packed", "even"}:
        raise ValueError("pad.yaml placement_method must be one of: packed, even.")
    return placement_method_any


def build_placements_from_yaml(
    *,
    io_yaml: dict[str, Any],
    pad_yaml: dict[str, Any],
    die_width_override: float | None,
    die_height_override: float | None,
    placement_method: str,
) -> tuple[float, float, list[Placement]]:
    """Build complete placement list from io/pad YAML inputs."""

    die_width, die_height = resolve_die_size(pad_yaml, die_width_override, die_height_override)
    size_by_cell: dict[str, CellSize] = load_io_sizes(io_yaml)

    raw_sides: dict[str, Any] = pad_yaml.get("sides", {})
    if not isinstance(raw_sides, dict):
        raise ValueError("pad.yaml 'sides' must be a mapping.")

    filler_cells_any: Any = pad_yaml.get("filler_cells", ["fill10", "fill5", "fill1", "fillnc"])
    if not isinstance(filler_cells_any, list) or not all(
        isinstance(item, str) for item in filler_cells_any
    ):
        raise ValueError("pad.yaml 'filler_cells' must be a list[str].")
    filler_cells: list[str] = filler_cells_any

    corners_any: Any = pad_yaml.get("corners", {})
    corner_cells: dict[str, str] = {"sw": "cor", "se": "cor", "ne": "cor", "nw": "cor"}
    if isinstance(corners_any, dict):
        for key in corner_cells:
            value: Any = corners_any.get(key)
            if value is not None:
                if not isinstance(value, str):
                    raise ValueError(f"pad.yaml corners.{key} must be a string.")
                corner_cells[key] = value

    sides: dict[str, list[InstanceRequest]] = {
        "north": to_instance_requests(raw_sides.get("north", []), "north"),
        "south": to_instance_requests(raw_sides.get("south", []), "south"),
        "east": to_instance_requests(raw_sides.get("east", []), "east"),
        "west": to_instance_requests(raw_sides.get("west", []), "west"),
    }

    required_cells: set[str] = set(filler_cells)
    required_cells.update(corner_cells.values())
    for entries in sides.values():
        required_cells.update(item.cell for item in entries)

    missing_cells: list[str] = sorted(cell for cell in required_cells if cell not in size_by_cell)
    if missing_cells:
        raise ValueError(f"Missing cells in io.yaml: {missing_cells}")

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
    return die_width, die_height, placements


def write_abstract_gds(
    *,
    output_path: Path,
    top_cell_name: str,
    die_width: float,
    die_height: float,
    placements: list[Placement],
) -> None:
    """Write abstract GDS with rectangles per instance.

    Raises:
        RuntimeError: If `gdstk` is unavailable in the environment.
    """

    try:
        import gdstk  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "gdstk is required to write GDS. Install with: pip install gdstk"
        ) from exc

    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    top = lib.new_cell(top_cell_name)

    # Draw die boundary on marker layer.
    top.add(gdstk.rectangle((0.0, 0.0), (die_width, die_height), layer=255, datatype=0))

    for placement in placements:
        x0: float = placement.x
        y0: float = placement.y
        x1: float = placement.x + placement.width
        y1: float = placement.y + placement.height
        layer: int = 10 if placement.kind == "pad" else 11 if placement.kind == "corner" else 12
        top.add(gdstk.rectangle((x0, y0), (x1, y1), layer=layer, datatype=0))
        top.add(gdstk.Label(f"{placement.name}:{placement.cell}", (x0, y0), layer=layer))

    lib.write_gds(str(output_path))


def find_cell_gds(
    *,
    tools_root: Path,
    cell_name: str,
    metal_stack: str,
) -> Path | None:
    """Find a GDS file for a cell and selected metal stack.

    Supported patterns:
    - cells/<cell>/gf180mcu_fd_io__<cell>_<stack>.gds
    - cells/<cell>/gf180mcu_fd_io__<cell>_<stack>.gds.gz
    - cells/<cell>/<cell>_<stack>.gds
    - cells/<cell>/<cell>.gds
    """

    candidates: list[Path] = [
        tools_root / "cells" / cell_name / f"gf180mcu_fd_io__{cell_name}_{metal_stack}.gds",
        tools_root / "cells" / cell_name / f"gf180mcu_fd_io__{cell_name}_{metal_stack}.gds.gz",
        tools_root / "cells" / cell_name / f"{cell_name}_{metal_stack}.gds",
        tools_root / "cells" / cell_name / f"{cell_name}.gds",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def orientation_to_rotation_deg(orientation: str) -> float:
    """Map orientation label to clockwise angle in degrees."""

    mapping: dict[str, float] = {"R0": 0.0, "R90": 90.0, "R180": 180.0, "R270": 270.0}
    return mapping.get(orientation, 0.0)


def _rotate_point_orthogonal(x_value: float, y_value: float, orientation: str) -> tuple[float, float]:
    """Rotate a point around origin by orthogonal orientation.

    Args:
        x_value: Source x coordinate.
        y_value: Source y coordinate.
        orientation: One of R0/R90/R180/R270.

    Returns:
        Rotated (x, y) point.
    """

    if orientation == "R90":
        return -y_value, x_value
    if orientation == "R180":
        return -x_value, -y_value
    if orientation == "R270":
        return y_value, -x_value
    return x_value, y_value


def reference_origin_for_bbox(
    *,
    placement: Placement,
    ref_bbox: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[float, float]:
    """Compute reference origin so rotated bbox lower-left matches placement.

    Args:
        placement: Target placement rectangle.
        ref_bbox: Unrotated referenced cell bbox ((xmin, ymin), (xmax, ymax)).

    Returns:
        Reference origin for gdstk.Reference.
    """

    (x_min, y_min), (x_max, y_max) = ref_bbox
    corners: list[tuple[float, float]] = [
        (x_min, y_min),
        (x_min, y_max),
        (x_max, y_min),
        (x_max, y_max),
    ]
    rotated: list[tuple[float, float]] = [
        _rotate_point_orthogonal(x_value=pt[0], y_value=pt[1], orientation=placement.orientation)
        for pt in corners
    ]
    rotated_min_x: float = min(point[0] for point in rotated)
    rotated_min_y: float = min(point[1] for point in rotated)
    return placement.x - rotated_min_x, placement.y - rotated_min_y


def write_real_or_abstract_gds(
    *,
    output_path: Path,
    top_cell_name: str,
    die_width: float,
    die_height: float,
    placements: list[Placement],
    tools_root: Path,
    mode: str,
    metal_stack: str,
) -> GenerationStats:
    """Write GDS in real-cell mode when possible, else abstract fallback.

    Args:
        output_path: Output GDS path.
        top_cell_name: Top-level cell name.
        die_width: Die width in microns.
        die_height: Die height in microns.
        placements: Computed placements.
        tools_root: IO library root path.
        mode: One of auto/real/abstract.
        metal_stack: Selected layout view (3lm/4lm/5lm).

    Raises:
        RuntimeError: If `gdstk` is unavailable or real mode cannot be fulfilled.
    """

    by_kind: dict[str, int] = {}
    by_cell: dict[str, int] = {}

    for placement in placements:
        by_kind[placement.kind] = by_kind.get(placement.kind, 0) + 1
        by_cell[placement.cell] = by_cell.get(placement.cell, 0) + 1

    if mode == "abstract":
        write_abstract_gds(
            output_path=output_path,
            top_cell_name=top_cell_name,
            die_width=die_width,
            die_height=die_height,
            placements=placements,
        )
        return GenerationStats(
            total_instances=len(placements),
            real_placed=0,
            abstract_fallback=len(placements),
            by_kind=by_kind,
            by_cell=by_cell,
            fallback_cells=sorted(by_cell.keys()),
        )

    try:
        import gdstk  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "gdstk is required to write GDS. Install with: pip install gdstk"
        ) from exc

    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    top = lib.new_cell(top_cell_name)
    top.add(gdstk.rectangle((0.0, 0.0), (die_width, die_height), layer=255, datatype=0))

    loaded_cells: dict[str, Any] = {}
    imported_cell_names: set[str] = set()
    real_placed: int = 0
    abstract_fallback: int = 0
    fallback_cells: set[str] = set()

    for placement in placements:
        if placement.cell not in loaded_cells:
            gds_path: Path | None = find_cell_gds(
                tools_root=tools_root,
                cell_name=placement.cell,
                metal_stack=metal_stack,
            )
            loaded_cells[placement.cell] = gds_path

        gds_path_any: Any = loaded_cells[placement.cell]
        if isinstance(gds_path_any, Path):
            src_lib = gdstk.read_gds(str(gds_path_any))
            # Import all source cells so nested references are resolvable in output GDS.
            for src_cell in src_lib.cells:
                if src_cell.name not in imported_cell_names:
                    lib.add(src_cell)
                    imported_cell_names.add(src_cell.name)
            candidate_names: list[str] = [
                f"gf180mcu_fd_io__{placement.cell}_{metal_stack}",
                f"gf180mcu_fd_io__{placement.cell}",
                placement.cell,
            ]
            ref_cell = None
            cell_map: dict[str, Any] = {item.name: item for item in src_lib.cells}
            for candidate in candidate_names:
                ref_cell = cell_map.get(candidate)
                if ref_cell is not None:
                    break
            if ref_cell is None:
                cells = src_lib.top_level()
                if cells:
                    ref_cell = cells[0]
            if ref_cell is not None:
                rotation_deg: float = orientation_to_rotation_deg(placement.orientation)
                ref_bbox = ref_cell.bounding_box()
                if ref_bbox is None:
                    raise RuntimeError(f"Referenced cell '{ref_cell.name}' has empty geometry.")
                ref_origin_x, ref_origin_y = reference_origin_for_bbox(
                    placement=placement,
                    ref_bbox=ref_bbox,
                )
                top.add(
                    gdstk.Reference(
                        ref_cell,
                        origin=(ref_origin_x, ref_origin_y),
                        rotation=rotation_deg * 3.141592653589793 / 180.0,
                    )
                )
                real_placed += 1
                continue

        if mode == "real":
            raise RuntimeError(
                f"Real mode failed for cell '{placement.cell}' with stack '{metal_stack}'. "
                "Cell GDS view was not found or had no readable top cell."
            )

        x0: float = placement.x
        y0: float = placement.y
        x1: float = placement.x + placement.width
        y1: float = placement.y + placement.height
        layer: int = 10 if placement.kind == "pad" else 11 if placement.kind == "corner" else 12
        top.add(gdstk.rectangle((x0, y0), (x1, y1), layer=layer, datatype=0))
        top.add(gdstk.Label(f"{placement.name}:{placement.cell}", (x0, y0), layer=layer))
        abstract_fallback += 1
        fallback_cells.add(placement.cell)

    lib.write_gds(str(output_path))
    print(
        f"Placed real refs: {real_placed}, abstract fallbacks: {abstract_fallback}, "
        f"metal_stack: {metal_stack}, mode: {mode}"
    )
    return GenerationStats(
        total_instances=len(placements),
        real_placed=real_placed,
        abstract_fallback=abstract_fallback,
        by_kind=by_kind,
        by_cell=by_cell,
        fallback_cells=sorted(fallback_cells),
    )


def write_markdown_report(
    *,
    report_path: Path,
    output_gds: Path,
    top_cell_name: str,
    mode: str,
    metal_stack: str,
    placement_method: str,
    die_width: float,
    die_height: float,
    placements: list[Placement],
    stats: GenerationStats,
) -> None:
    """Write a Markdown report for generated pad-ring GDS."""

    lines: list[str] = []
    lines.append("# Pad Ring GDS Generation Report")
    lines.append("")
    lines.append("## Run Settings")
    lines.append("")
    lines.append(f"- Output GDS: `{output_gds}`")
    lines.append(f"- Top Cell: `{top_cell_name}`")
    lines.append(f"- Mode: `{mode}`")
    lines.append(f"- Metal Stack: `{metal_stack}`")
    lines.append(f"- Placement Method: `{placement_method}`")
    lines.append(f"- Die Size (um): `{die_width} x {die_height}`")
    lines.append("")
    lines.append("## Placement Summary")
    lines.append("")
    lines.append(f"- Total instances: `{stats.total_instances}`")
    lines.append(f"- Real-cell references: `{stats.real_placed}`")
    lines.append(f"- Abstract fallbacks: `{stats.abstract_fallback}`")
    lines.append("")
    lines.append("## Instance Kinds")
    lines.append("")
    for kind in sorted(stats.by_kind.keys()):
        lines.append(f"- {kind}: `{stats.by_kind[kind]}`")
    lines.append("")
    lines.append("## Cell Usage")
    lines.append("")
    lines.append("| Cell | Count |")
    lines.append("|---|---:|")
    for cell_name in sorted(stats.by_cell.keys()):
        lines.append(f"| {cell_name} | {stats.by_cell[cell_name]} |")
    lines.append("")
    lines.append("## Fallback Cells")
    lines.append("")
    if stats.fallback_cells:
        for cell_name in stats.fallback_cells:
            lines.append(f"- `{cell_name}`")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Per-Instance Placement")
    lines.append("")
    lines.append(
        "| Instance | Cell | Kind | Side | X (um) | Y (um) | Width (um) | Height (um) | Orientation |"
    )
    lines.append("|---|---|---|---|---:|---:|---:|---:|---|")
    for placement in placements:
        lines.append(
            f"| {placement.name} | {placement.cell} | {placement.kind} | {placement.side} | "
            f"{placement.x:.6f} | {placement.y:.6f} | {placement.width:.6f} | "
            f"{placement.height:.6f} | {placement.orientation} |"
        )
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run the YAML-to-GDS flow."""

    args = parse_args()
    io_yaml: dict[str, Any] = read_yaml(args.io_yaml)
    pad_yaml: dict[str, Any] = read_yaml(args.pad_yaml)

    if not args.tools_root.exists():
        raise FileNotFoundError(f"tools root not found: {args.tools_root}")

    placement_method: str = resolve_placement_method(pad_yaml, args.placement_method)
    die_width, die_height, placements = build_placements_from_yaml(
        io_yaml=io_yaml,
        pad_yaml=pad_yaml,
        die_width_override=args.die_width,
        die_height_override=args.die_height,
        placement_method=placement_method,
    )
    metal_stack: str = resolve_metal_stack(io_yaml, args.metal_stack)
    stats: GenerationStats = write_real_or_abstract_gds(
        output_path=args.output_gds,
        top_cell_name=args.top_cell,
        die_width=die_width,
        die_height=die_height,
        placements=placements,
        tools_root=args.tools_root,
        mode=args.mode,
        metal_stack=metal_stack,
    )
    print(f"Wrote GDS: {args.output_gds}")
    if args.report_md is not None:
        write_markdown_report(
            report_path=args.report_md,
            output_gds=args.output_gds,
            top_cell_name=args.top_cell,
            mode=args.mode,
            metal_stack=metal_stack,
            placement_method=placement_method,
            die_width=die_width,
            die_height=die_height,
            placements=placements,
            stats=stats,
        )
        print(f"Wrote Markdown report: {args.report_md}")


if __name__ == "__main__":
    main()
