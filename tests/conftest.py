"""Pytest configuration: make project modules importable from the repo root."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / "05_Source_Code" / "model_experiment",
             ROOT / "05_Source_Code" / "study2_volatility",
             ROOT / "05_Source_Code" / "generators"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
