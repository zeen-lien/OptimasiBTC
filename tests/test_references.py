"""Audit tests for the 32-reference thesis bibliography.

These tests protect the single source of truth (`reference_data.py`) and the
generated artifacts that depend on it. They do not require a network
connection.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

import download_references
from reference_data import CLUSTERS, REFERENCES, apa_reference, reference_keys

ROOT = Path(__file__).resolve().parents[1]
GENERATORS = ROOT / "05_Source_Code" / "generators"
MANIFEST = ROOT / "04_Referensi_Ilmiah" / "references_manifest.csv"
CATALOG = ROOT / "04_Referensi_Ilmiah" / "DAFTAR_32_REFERENSI_SKRIPSI.md"
AUDIT = ROOT / "docs" / "REFERENCE_AUDIT.md"
MASTER = ROOT / "03_Naskah_Skripsi" / "SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx"

ALIASES = {
    "Binance": ("Binance",),
    "López de Prado": ("López de Prado",),
    "Optuna": ("Optuna",),
    "TensorFlow": ("TensorFlow",),
    "Universitas": ("UNISNU",),
}

FORBIDDEN_CITATIONS = (
    "JUTIF, 2026",
    "JUTIF (2026)",
    "Bit-Tech, 2026",
    "Bit-Tech (2026)",
    "BRIN, 2025",
    "BRIN (2025)",
    "Sakarya University, 2023",
    "IJEECS, 2023",
    "Aswadi & Ependi, 2022",
    "Bouthillier et al., 2020",
    "Falkner et al., 2018",
    "Li et al., 2017",
    "Lipton et al., 2015",
    "Pedregosa et al., 2011",
    "Vaswani et al., 2017",
    "Applied Soft Computing",
    "Expert Systems with Applications",
    "IEEE Access",
    "JOIV",
    "University of Warsaw",
    "Gunarto",
)

FORBIDDEN_FILES = (
    "Bouthillier_2020_Survey_Machine_Learning_Evaluation.pdf",
    "Makridakis_2018_M4_Competition_Results_and_Findings.pdf",
)


def _generator_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(GENERATORS.glob("generate_bab*.py"))
    )


def test_reference_count_and_identity():
    assert len(REFERENCES) == 32
    assert len({ref["id"] for ref in REFERENCES}) == 32
    assert len(reference_keys()) == 32
    assert {ref["cluster"] for ref in REFERENCES} <= set(CLUSTERS)


def test_reference_fields_are_complete():
    for ref in REFERENCES:
        for field in ("authors", "first_author", "title", "venue", "role", "verification"):
            assert ref[field].strip(), f"Reference {ref['id']} has empty {field}"
        assert isinstance(ref["year"], int)
        assert 1900 <= ref["year"] <= 2030
        assert ref["first_author"] in ref["authors"]


def test_reference_keys_are_unique():
    keys = [(ref["first_author"], ref["year"]) for ref in REFERENCES]
    assert len(keys) == len(set(keys))


def test_dois_are_unique():
    dois = [ref["doi"].lower() for ref in REFERENCES if ref["doi"]]
    assert len(dois) == len(set(dois))


def test_apa_format_contains_author_year_and_locator():
    for ref in REFERENCES:
        text = apa_reference(ref)
        assert ref["authors"].rstrip(".") in text
        assert f"({ref['year']})" in text
        assert ref["title"].rstrip(".") in text or ref["title"] in text
        if ref["doi"]:
            assert f"https://doi.org/{ref['doi']}" in text
        elif ref["url"]:
            assert ref["url"] in text


def test_all_references_are_cited_in_chapter_generators():
    text = _generator_text()
    for ref in REFERENCES:
        names = ALIASES.get(ref["first_author"], (ref["first_author"],))
        assert any(name in text for name in names), (
            f"Reference {ref['first_author']} ({ref['year']}) is not cited "
            "in any chapter generator"
        )


def test_no_forbidden_legacy_citations_in_chapter_generators():
    text = _generator_text()
    for token in FORBIDDEN_CITATIONS:
        assert token not in text, f"Legacy citation still present: {token}"
    assert "Kervanc?" not in text
    assert "Kervancı" in text


def test_local_pdf_paths_exist_and_are_pdf():
    for ref in REFERENCES:
        raw = ref.get("pdf", "").strip()
        if not raw:
            continue
        path = ROOT / raw
        assert path.exists(), f"Missing PDF for {ref['first_author']}: {raw}"
        assert path.stat().st_size > 10_000
        assert path.read_bytes()[:5] == b"%PDF-"


def test_downloader_is_synchronized_with_references():
    pdf_names = {
        Path(ref["pdf"]).name
        for ref in REFERENCES
        if ref.get("pdf", "").strip()
    }
    direct_names = {name for name, _ in download_references.DIRECT_PDFS}
    assert direct_names <= pdf_names, direct_names - pdf_names

    # Ula (2024) is cited metadata-only; the OJS attempt is allowed to target it.
    allowed_manual = {"Ula_2024_MATRIK_LSTM_RandomForest_Bitcoin.pdf"}
    ojs_names = {name for _, name in download_references.OJS_LIST}
    assert ojs_names <= pdf_names | allowed_manual

    combined = " ".join(name for name, _ in download_references.DIRECT_PDFS)
    for old in FORBIDDEN_FILES:
        assert old not in combined
    urls = " ".join(url for _, url in download_references.DIRECT_PDFS)
    assert "1905.07406" not in urls
    assert "2007.03964" not in urls
    assert "2103.03098" in urls


def test_manifest_has_32_rows_and_valid_hashes():
    assert MANIFEST.exists(), "Run build_reference_manifest.py first"
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 32
    assert {row["id"] for row in rows} == {str(ref["id"]) for ref in REFERENCES}
    for row in rows:
        if row["pdf_status"] == "available":
            assert re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), row["id"]
            assert (ROOT / row["local_pdf"]).exists(), row["local_pdf"]
        else:
            assert row["sha256"] == ""


def test_generated_catalog_and_audit_exist():
    assert CATALOG.exists()
    assert AUDIT.exists()
    catalog = CATALOG.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "Referensi dalam daftar | 32" in catalog
    assert "Jumlah referensi: **32**" in audit
    assert "Kervancı" in catalog


@pytest.mark.skipif(not MASTER.exists(), reason="Master DOCX has not been rebuilt")
def test_master_bibliography_and_citations():
    from docx import Document

    doc = Document(str(MASTER))
    paragraphs = [p.text for p in doc.paragraphs]
    full = "\n".join(paragraphs)
    assert "DAFTAR PUSTAKA" in full
    body, refs_text = full.rsplit("DAFTAR PUSTAKA", 1)
    ref_block = refs_text.split("LAMPIRAN 1")[0]

    entries = [line.strip() for line in ref_block.splitlines() if re.search(r"\((19|20)\d{2}[a-z]?\)", line)]
    assert len(entries) == 32, f"Found {len(entries)} reference entries"

    for ref in REFERENCES:
        names = ALIASES.get(ref["first_author"], (ref["first_author"],))
        assert any(name in body for name in names), (
            f"Body does not cite {ref['first_author']} ({ref['year']})"
        )

    for token in FORBIDDEN_CITATIONS:
        assert token not in full, f"Legacy citation still present in DOCX: {token}"
    assert "Kervanc?" not in full
    assert "Kervancı" in full


@pytest.mark.skipif(not MASTER.exists(), reason="Master DOCX has not been rebuilt")
def test_citation_auditor_passes_on_master():
    import audit_citations

    assert audit_citations.audit() == []
