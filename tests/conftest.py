"""Pytest configuration for this repository.

The unit tests import modules from ``src/`` as top-level modules (e.g.
``pad_ring_generator``). To make that work consistently in local runs, we
prepend ``src/`` to ``sys.path``.
"""

from __future__ import annotations

import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC_DIR = _REPO_ROOT / "src"

if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

