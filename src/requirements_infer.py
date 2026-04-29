"""Infer Python runtime requirements from imports in ``src/``.

This module provides a lightweight (heuristic) way to derive a dependency set
from the project's Python source code. It is intentionally conservative and
primarily targets import-based dependencies that are directly used by the
runtime code.

It does *not* execute the project code and therefore cannot capture dynamic
imports or optional dependencies selected only at runtime.
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class InferenceOptions:
    """Options controlling requirements inference."""

    src_dir: Path
    local_module_names: set[str]
    module_to_package: Mapping[str, str]
    exclude_top_level_modules: set[str]


def _get_stdlib_module_names() -> set[str]:
    """Return the interpreter's best-effort set of standard-library modules."""

    stdlib_names = getattr(sys, "stdlib_module_names", None)
    if stdlib_names is None:
        return set()
    return set(stdlib_names)


def _iter_python_files(src_dir: Path) -> Iterable[Path]:
    """Yield all ``.py`` files directly under ``src_dir`` (recursively)."""

    for path in src_dir.rglob("*.py"):
        if path.is_file():
            yield path


def _collect_import_top_level_modules(file_path: Path) -> set[str]:
    """Collect import top-level module names from a single Python file."""

    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    found: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not alias.name:
                    continue
                found.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            # Skip relative imports (e.g., ``from .foo import bar``).
            if getattr(node, "level", 0):
                continue
            if not node.module:
                continue
            found.add(node.module.split(".", 1)[0])

    return found


def infer_top_level_import_modules(options: InferenceOptions) -> set[str]:
    """Infer third-party top-level modules imported by the project.

    Args:
        options: Inference options.

    Returns:
        A set of top-level imported module names (e.g., ``{"yaml", "gdstk"}``).
    """

    stdlib_modules = _get_stdlib_module_names()
    inferred: set[str] = set()

    for py_file in _iter_python_files(options.src_dir):
        inferred.update(_collect_import_top_level_modules(py_file))

    inferred.difference_update(options.local_module_names)
    inferred.difference_update(stdlib_modules)
    inferred.difference_update(options.exclude_top_level_modules)
    inferred.discard("__future__")
    return inferred


def infer_requirement_packages(
    top_level_modules: set[str],
    *,
    module_to_package: Mapping[str, str],
) -> set[str]:
    """Map top-level imported modules to installable package names.

    Args:
        top_level_modules: Imported top-level modules.
        module_to_package: Mapping from module name to PyPI package name.

    Returns:
        A set of package names suitable for ``pip install``.
    """

    packages: set[str] = set()
    for module_name in top_level_modules:
        packages.add(module_to_package.get(module_name, module_name))
    return packages


def infer_packages_from_src_dir(
    *,
    src_dir: Path,
    module_to_package: Mapping[str, str] | None = None,
    exclude_top_level_modules: Iterable[str] | None = None,
    local_module_names: Iterable[str] | None = None,
) -> list[str]:
    """Infer required pip packages from imports under ``src_dir``.

    Args:
        src_dir: Source directory containing project's ``.py`` files.
        module_to_package: Optional mapping from module name to pip package name.
            Defaults to a small built-in mapping (e.g., ``yaml -> PyYAML``).
        exclude_top_level_modules: Optional modules to exclude from inference.
        local_module_names: Optional local modules to exclude. If not provided,
            it is inferred from ``src_dir``'s ``*.py`` file stems.

    Returns:
        Sorted list of inferred package names.
    """

    if module_to_package is None:
        module_to_package = {"yaml": "PyYAML"}
    exclude_set = set(exclude_top_level_modules or [])

    if local_module_names is None:
        local_module_names = {path.stem for path in _iter_python_files(src_dir)}

    options = InferenceOptions(
        src_dir=src_dir,
        local_module_names=set(local_module_names),
        module_to_package=module_to_package,
        exclude_top_level_modules=exclude_set,
    )
    top_level_modules = infer_top_level_import_modules(options)
    packages = infer_requirement_packages(
        top_level_modules,
        module_to_package=options.module_to_package,
    )
    return sorted(packages)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for this module."""

    parser = argparse.ArgumentParser(
        description="Infer pip packages from imports in src/",
    )
    parser.add_argument("--src-dir", type=Path, required=True)
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Top-level module names to exclude (repeatable).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint.

    Prints one inferred package per line to stdout.
    """

    args = _parse_args(argv)
    packages = infer_packages_from_src_dir(
        src_dir=args.src_dir,
        exclude_top_level_modules=args.exclude,
    )

    for pkg in packages:
        print(pkg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

