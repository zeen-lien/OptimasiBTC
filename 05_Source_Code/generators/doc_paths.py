"""Shared project paths for document generators (no CWD assumptions)."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NASKAH_DIR = PROJECT_ROOT / "03_Naskah_Skripsi"
SOURCE_ROOT = PROJECT_ROOT / "05_Source_Code"
RESULTS_ROOT = SOURCE_ROOT / "results"
LEGACY_FIGURES_DIR = RESULTS_ROOT / "figures"
REFERENCES_DIR = PROJECT_ROOT / "04_Referensi_Ilmiah"
ADDITIONAL_REFERENCES_DIR = REFERENCES_DIR / "Referensi_Tambahan"
MAIN_REFERENCES_DIR = REFERENCES_DIR / "Referensi_Utama"
ARCHIVE_REFERENCES_DIR = REFERENCES_DIR / "Arsip_Tambahan"


def ensure_naskah_dir() -> Path:
    NASKAH_DIR.mkdir(parents=True, exist_ok=True)
    return NASKAH_DIR
