"""Tests for requirement inference from source imports."""

from __future__ import annotations

from pathlib import Path

from requirements_infer import infer_packages_from_src_dir


def test_infer_packages_maps_yaml_and_gdstk(tmp_path: Path) -> None:
    """Ensure inference maps module names to pip package names."""

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # Local modules should be ignored.
    (src_dir / "pad_ring_generator.py").write_text("CellSize = object\n", encoding="utf-8")

    # stdlib modules should be ignored; third-party imports should be kept.
    (src_dir / "app.py").write_text(
        "import os\n"
        "import yaml\n"
        "from gdstk import Library\n"
        "from pad_ring_generator import CellSize\n",
        encoding="utf-8",
    )

    packages = infer_packages_from_src_dir(src_dir=src_dir)
    assert set(packages) == {"PyYAML", "gdstk"}


def test_infer_packages_excludes_top_level_module(tmp_path: Path) -> None:
    """Ensure inference can exclude specific top-level modules."""

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    (src_dir / "local_mod.py").write_text("X = 1\n", encoding="utf-8")
    (src_dir / "app.py").write_text(
        "import yaml\n"
        "import gdstk\n"
        "from local_mod import X\n",
        encoding="utf-8",
    )

    packages = infer_packages_from_src_dir(
        src_dir=src_dir,
        exclude_top_level_modules=["gdstk"],
    )
    assert set(packages) == {"PyYAML"}

