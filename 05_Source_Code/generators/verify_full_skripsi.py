"""Audit the assembled thesis against the published final results.

The verifier is intentionally strict: it returns a non-zero exit code when the
document contains stale captions, missing figures, legacy numbers, raw math
delimiters, or metric values that do not match ``summary_final.json``.

Run after ``generate_master_skripsi.py``::

    python 05_Source_Code/generators/verify_full_skripsi.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import docx

from doc_paths import NASKAH_DIR
from results_context import FinalResults, format_pct, format_usd

FORBIDDEN_LITERALS = (
    "RMSE 2.338,22",
    "MAE 1.784,27",
    "MAPE 1,81%",
    "trial #44",
    "Best trial #44",
    "lookback 14",
    "units 80",
    "Split=85%",
    "juara mutlak",
    "Juara Mutlak",
    "2.25%",
    "225%",
)

KEY_MARKERS = (
    "OPTIMASI HYPERPARAMETER LONG SHORT-TERM MEMORY",
    "SURAT PERNYATAAN KEASLIAN KARYA TULIS SKRIPSI",
    "LEMBAR PERSETUJUAN PEMBIMBING",
    "LEMBAR PENGESAHAN SKRIPSI",
    "HALAMAN PERSEMBAHAN",
    "HALAMAN MOTTO",
    "KATA PENGANTAR",
    "ABSTRAK",
    "ABSTRACT",
    "DAFTAR ISI",
    "DAFTAR TABEL",
    "DAFTAR GAMBAR",
    "DAFTAR LAMPIRAN",
    "BAB I\nPENDAHULUAN",
    "BAB II\nLANDASAN TEORI",
    "BAB III\nMETODE PENELITIAN",
    "BAB IV\nHASIL PENELITIAN DAN PEMBAHASAN",
    "BAB V\nPENUTUP",
    "DAFTAR PUSTAKA",
    "LAMPIRAN 1",
    "LAMPIRAN 2",
    "LAMPIRAN 3",
)

SAMPLE_AUTHORS = (
    "Akiba",
    "Bergstra",
    "Hochreiter",
    "Khumaidi",
    "Goodfellow",
    "Kingma",
    "Srivastava",
    "Hyndman",
    "López de Prado",
    "Creswell",
)

CAPTION_RE = re.compile(r"^(Tabel|Gambar)\s+(\d+\.\d+)\s+(.+)$")
PAGE_TOKEN_RE = re.compile(r"\s+\d+$")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _strip_page(text: str) -> str:
    """Remove the trailing page number from a front-matter list entry."""
    return PAGE_TOKEN_RE.sub("", text).strip()


def _extract_lists(doc: docx.Document):
    """Return caption entries from DAFTAR TABEL and DAFTAR GAMBAR."""
    tables: list[str] = []
    figures: list[str] = []
    section: str | None = None
    for paragraph in doc.paragraphs:
        text = _normalize(paragraph.text)
        if text == "DAFTAR TABEL":
            section = "tables"
            continue
        if text == "DAFTAR GAMBAR":
            section = "figures"
            continue
        if text in {"DAFTAR LAMPIRAN", "BAB I PENDAHULUAN"}:
            section = None
            continue
        if section and re.match(r"^(Tabel|Gambar)\s+\d+\.\d+", text):
            entry = _strip_page(text)
            if section == "tables":
                tables.append(entry)
            else:
                figures.append(entry)
    return tables, figures


def _extract_body_captions(doc: docx.Document):
    """Return captions that appear in the body after BAB I."""
    tables: list[str] = []
    figures: list[str] = []
    body_started = False
    for paragraph in doc.paragraphs:
        text = _normalize(paragraph.text)
        if text == "BAB I PENDAHULUAN":
            body_started = True
            continue
        if not body_started or "DAFTAR PUSTAKA" in text:
            continue
        match = CAPTION_RE.match(text)
        if not match:
            continue
        kind, _number, _title = match.groups()
        (tables if kind == "Tabel" else figures).append(text)
    return tables, figures


def _caption_map(entries: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for entry in entries:
        match = CAPTION_RE.match(entry)
        if match:
            kind, number, title = match.groups()
            mapping[f"{kind} {number}"] = _normalize(title)
    return mapping


def _check_metrics(text: str, results: FinalResults) -> list[str]:
    errors: list[str] = []
    for key in ("E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7"):
        metrics = results.metrics(key)
        for metric in ("RMSE", "MAE"):
            expected = format_usd(metrics[metric])
            if expected not in text:
                errors.append(f"Angka {key} {metric} tidak ditemukan: {expected}")
        expected_mape = format_pct(metrics["MAPE"])
        if expected_mape not in text:
            errors.append(f"Angka {key} MAPE tidak ditemukan: {expected_mape}")
    return errors


def _check_best_trial(text: str, results: FinalResults) -> list[str]:
    config = results.final_configuration()
    hyper = config.get("hyperparameters") or {}
    errors: list[str] = []
    trial = config.get("best_trial_number")
    if trial is not None and f"#{trial}" not in text:
        errors.append(f"Trial terbaik #{trial} tidak ditemukan di naskah")
    lookback = hyper.get("lookback")
    if lookback is not None and f"lookback {lookback} hari" not in text:
        errors.append(f"Lookback final {lookback} hari tidak ditemukan di naskah")
    learning_rate = hyper.get("learning_rate")
    if learning_rate is not None:
        formatted = f"{learning_rate:.5f}".replace(".", ",")
        if formatted not in text:
            errors.append(f"Learning rate final {formatted} tidak ditemukan di naskah")
    return errors


def _check_caption_lists(doc: docx.Document) -> list[str]:
    list_tables, list_figures = _extract_lists(doc)
    body_tables, body_figures = _extract_body_captions(doc)
    list_table_map = _caption_map(list_tables)
    list_figure_map = _caption_map(list_figures)
    body_table_map = _caption_map(body_tables)
    body_figure_map = _caption_map(body_figures)

    errors: list[str] = []
    for kind, listed, body in (
        ("tabel", list_table_map, body_table_map),
        ("gambar", list_figure_map, body_figure_map),
    ):
        missing_in_list = sorted(set(body) - set(listed))
        missing_in_body = sorted(set(listed) - set(body))
        if missing_in_list:
            errors.append(f"{kind.title()} ada di badan tetapi tidak di daftar: {missing_in_list}")
        if missing_in_body:
            errors.append(f"{kind.title()} ada di daftar tetapi tidak di badan: {missing_in_body}")
        for number in sorted(set(listed) & set(body)):
            if listed[number].lower() != body[number].lower():
                errors.append(
                    f"Caption {kind} {number} berbeda: daftar={listed[number]!r}, "
                    f"badan={body[number]!r}"
                )
    return errors


def _check_references(doc: docx.Document) -> list[str]:
    paragraphs = [p.text for p in doc.paragraphs]
    try:
        start = next(i for i, text in enumerate(paragraphs) if text.strip() == "DAFTAR PUSTAKA")
        end = next(
            i
            for i, text in enumerate(paragraphs[start:], start)
            if "LAMPIRAN 1" in text
        )
    except StopIteration:
        return ["Bagian DAFTAR PUSTAKA/LAMPIRAN 1 tidak ditemukan"]

    entries = [
        text
        for text in paragraphs[start + 1 : end]
        if re.search(r"\((?:19|20)\d{2}[a-z]?\)", text)
    ]
    errors: list[str] = []
    if len(entries) != 32:
        errors.append(f"Jumlah referensi {len(entries)}, seharusnya 32")
    return errors


def verify_full_skripsi() -> bool:
    doc_path = NASKAH_DIR / "SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx"
    print("=== AUDIT MASTER NASKAH SKRIPSI LENGKAP ===")
    print(f"File Target: {doc_path}")

    if not doc_path.exists():
        print(f"[FAIL] Berkas {doc_path} tidak ditemukan!")
        return False

    try:
        results = FinalResults.load()
    except Exception as exc:  # noqa: BLE001 - the audit reports the exact failure
        print(f"[FAIL] Summary final tidak dapat dibaca: {exc}")
        return False

    file_size_kb = doc_path.stat().st_size / 1024
    print(f"[OK] Ukuran Berkas: {file_size_kb:.2f} KB ({file_size_kb / 1024:.2f} MB)")

    doc = docx.Document(doc_path)
    print(f"[OK] Total Paragraf: {len(doc.paragraphs)}")
    print(f"[OK] Total Tabel: {len(doc.tables)}")
    print(f"[OK] Total Section: {len(doc.sections)}")

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Section and pagination setup.
    sec0 = doc.sections[0]
    pgnum0 = sec0._sectPr.find(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType"
    )
    fmt0 = (
        pgnum0.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fmt")
        if pgnum0 is not None
        else None
    )
    if fmt0 != "lowerRoman":
        errors.append(f"Section 0 memakai format {fmt0!r}, seharusnya lowerRoman")
    if len(doc.sections) > 1:
        sec1 = doc.sections[1]
        pgnum1 = sec1._sectPr.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType"
        )
        fmt1 = (
            pgnum1.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fmt")
            if pgnum1 is not None
            else None
        )
        if fmt1 != "decimal":
            errors.append(f"Section 1 memakai format {fmt1!r}, seharusnya decimal")

    # 2. Embedded images.
    image_relationships = [
        rel for rel in doc.part.rels.values() if "image" in rel.target_ref
    ]
    expected_figures = len(_extract_body_captions(doc)[1])
    if len(image_relationships) < expected_figures + 1:
        errors.append(
            f"Gambar ter-embed {len(image_relationships)}, minimal "
            f"{expected_figures + 1} (logo + caption badan)"
        )
    else:
        print(
            f"[OK] Gambar ter-embed: {len(image_relationships)} "
            f"(logo + {expected_figures} gambar Bab IV)"
        )

    # 3. OMML and raw delimiters.
    omml_count = 0
    raw_math: list[tuple[int, list[str]]] = []
    for idx, paragraph in enumerate(doc.paragraphs):
        if "m:oMath" in paragraph._element.xml:
            omml_count += 1
        matches = re.findall(r"(?<!\\)\$[^$]+\$", paragraph.text)
        if matches:
            raw_math.append((idx, matches))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if "m:oMath" in paragraph._element.xml:
                        omml_count += 1
                    matches = re.findall(r"(?<!\\)\$[^$]+\$", paragraph.text)
                    if matches:
                        raw_math.append((-1, matches))
    if raw_math:
        errors.append(f"Ditemukan raw $ pada {len(raw_math)} lokasi: {raw_math[:3]}")
    if omml_count == 0:
        errors.append("Tidak ada objek OMML matematika di naskah")
    print(f"[OK] Objek OMML: {omml_count}")

    # 4. Structural markers. Table cells are included because the benchmark
    # table is the primary location of per-model metric values.
    text_parts = [paragraph.text for paragraph in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text_parts.append(cell.text)
    full_text = "\n".join(text_parts)
    missing_markers = [marker for marker in KEY_MARKERS if marker not in full_text]
    if missing_markers:
        errors.append(f"Penanda bab hilang: {missing_markers}")

    # 5. Metric numbers must match summary_final.json.
    errors.extend(_check_metrics(full_text, results))
    errors.extend(_check_best_trial(full_text, results))

    # 6. No frozen legacy claims.
    for literal in FORBIDDEN_LITERALS:
        if literal in full_text:
            errors.append(f"Angka/klaim lama masih muncul: {literal!r}")

    # 7. Caption lists must match body captions.
    errors.extend(_check_caption_lists(doc))

    # 8. References.
    errors.extend(_check_references(doc))
    found_authors = sum(1 for author in SAMPLE_AUTHORS if author in full_text)
    if found_authors < len(SAMPLE_AUTHORS):
        warnings.append(
            f"Sampel penulis terdeteksi {found_authors}/{len(SAMPLE_AUTHORS)}"
        )

    # 9. Verdict must be present.
    verdict_status = results.verdict.get("status")
    if verdict_status and verdict_status not in full_text:
        errors.append(f"Status verdict {verdict_status!r} tidak ditemukan di naskah")

    print("\n--- Verifikasi Penanda Bab & Komponen Skripsi ---")
    for marker in KEY_MARKERS:
        status = "[OK]" if marker in full_text else "[MISSING]"
        print(f"  {status} {marker.replace(chr(10), ' - ')}")

    print("\n--- Verifikasi Angka & Caption ---")
    if errors:
        for error in errors:
            print(f"  [FAIL] {error}")
    else:
        print("  [OK] Angka metrik, trial terbaik, caption, dan struktur konsisten")
    for warning in warnings:
        print(f"  [WARNING] {warning}")

    print("\n=======================================================")
    if errors:
        print(f" HASIL AUDIT: {len(errors)} masalah ditemukan. Naskah belum siap.")
    else:
        print(" HASIL AUDIT: LULUS. Angka, caption, gambar, dan struktur konsisten.")
    print("=======================================================\n")
    return not errors


if __name__ == "__main__":
    sys.exit(0 if verify_full_skripsi() else 1)
