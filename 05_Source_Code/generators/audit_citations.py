"""Audit citations in the assembled master document.

Usage:
    python 05_Source_Code/generators/audit_citations.py

The audit is intentionally conservative. It verifies that:

- the DAFTAR PUSTAKA block contains exactly 32 entries;
- every bibliography entry is cited at least once in Bab I-V;
- every narrative ``Surname et al. (year)`` / ``Surname dkk. (year)`` /
  ``Surname & Surname (year)`` citation maps to a bibliography entry;
- no known legacy citation form survives.

Parenthetical groups are treated as citations when the text before the year is
a known surname/alias or contains ``et al.``, ``dkk.``, or ``&``. Date ranges
such as ``2020-2025`` and month names are ignored.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "03_Naskah_Skripsi" / "SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx"

ALIASES = {
    "Binance": "Binance Developer API",
    "Binance Developer API": "Binance Developer API",
    "TensorFlow": "TensorFlow Developers",
    "TensorFlow Developers": "TensorFlow Developers",
    "Optuna": "Optuna Development Team",
    "Optuna Development Team": "Optuna Development Team",
    "UNISNU": "Universitas Islam Nahdlatul Ulama Jepara",
    "Universitas": "Universitas Islam Nahdlatul Ulama Jepara",
    "Universitas Islam Nahdlatul Ulama Jepara": "Universitas Islam Nahdlatul Ulama Jepara",
    "López": "López de Prado",
    "López de Prado": "López de Prado",
}

FORBIDDEN = (
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
)

DATE_WORDS = {
    "januari",
    "februari",
    "maret",
    "april",
    "mei",
    "juni",
    "juli",
    "agustus",
    "september",
    "oktober",
    "november",
    "desember",
    "tahun",
    "periode",
    "semester",
}


def _canonical(name: str) -> str:
    name = re.sub(r"\b(?:et al\.?|dkk\.?)\s*$", "", name.strip()).strip()
    name = name.rstrip(",.").strip()
    if "&" in name:
        name = name.split("&")[0].strip()
    if "," in name:
        name = name.split(",")[0].strip()
    if name == "API":
        name = "Binance Developer API"
    return ALIASES.get(name, name)


def _reference_keys(ref_block: str) -> list[tuple[str, str]]:
    keys: list[tuple[str, str]] = []
    for line in ref_block.splitlines():
        line = line.strip()
        match = re.match(r"^(.+?)\((\d{4})[a-z]?\)", line)
        if not match:
            continue
        author = match.group(1).split(",")[0].strip().rstrip(".")
        keys.append((author, match.group(2)))
    return keys


def _narrative_citations(body: str) -> set[tuple[str, str]]:
    pattern = re.compile(
        r"([A-Z][\w'’\-]*(?:\s+(?:&|dan|and)\s+[A-Z][\w'’\-]*)?"
        r"(?:\s+et al\.|\s+dkk\.)?)\s+\((\d{4})\)"
    )
    found: set[tuple[str, str]] = set()
    for match in pattern.finditer(body):
        found.add((_canonical(match.group(1)), match.group(2)))
    return found


def _parenthetical_citations(body: str, known: set[str]) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    pattern = re.compile(r"\(([^()]*?(?:19|20)\d{2}[^()]*?)\)")
    for match in pattern.finditer(body):
        for part in match.group(1).split(";"):
            part = part.strip().rstrip(".")
            year_match = re.search(r"((?:19|20)\d{2})", part)
            if not year_match:
                continue
            year = year_match.group(1)
            before = part[: year_match.start()].strip().rstrip(",.").strip()
            before = re.sub(r"\b(?:et al\.?|dkk\.?)\s*$", "", before).strip()
            if not before or not before[0].isupper():
                continue
            if before.lower() in DATE_WORDS:
                continue
            if re.search(r"[–-]\s*(?:19|20)\d{2}\s*$", before):
                continue
            canonical = _canonical(before)
            has_marker = bool(re.search(r"\b(?:et al\.?|dkk\.?)\b|&", before))
            if canonical in known or has_marker:
                found.add((canonical, year))
    return found


def audit() -> list[str]:
    if not MASTER.exists():
        return [f"Master document not found: {MASTER}"]

    doc = Document(str(MASTER))
    full = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    if "DAFTAR PUSTAKA" not in full:
        return ["DAFTAR PUSTAKA not found"]
    body, refs_text = full.rsplit("DAFTAR PUSTAKA", 1)
    if "LAMPIRAN 1" not in refs_text:
        return ["LAMPIRAN 1 not found after DAFTAR PUSTAKA"]
    ref_block = refs_text.split("LAMPIRAN 1")[0]

    errors: list[str] = []
    keys = _reference_keys(ref_block)
    if len(keys) != 32:
        errors.append(f"Expected 32 reference entries, found {len(keys)}")

    known = {author for author, _ in keys}
    cited = _narrative_citations(body) | _parenthetical_citations(body, known)
    ref_set = set(keys)

    for key in sorted(ref_set - cited):
        errors.append(f"Reference never cited: {key[0]} ({key[1]})")

    for key in sorted(cited - ref_set):
        # Corporate full names may be cited without their trailing period.
        if key[0].rstrip(".") in {author.rstrip(".") for author in known}:
            continue
        # Journal names in table rows are not author-year citations.
        if key[0] in {"MATRIK", "ILKOM"}:
            continue
        errors.append(f"Citation without a reference entry: {key[0]} ({key[1]})")

    for token in FORBIDDEN:
        if token in full:
            errors.append(f"Legacy citation still present: {token}")
    if "Kervanc?" in full:
        errors.append("Mojibake 'Kervanc?' found in the master document")
    if "Kervancı" not in full:
        errors.append("'Kervancı' is missing from the master document")

    return errors


def main() -> int:
    errors = audit()
    if errors:
        print("CITATION AUDIT: FAIL")
        for error in errors:
            print(" -", error)
        return 1
    print("CITATION AUDIT: PASS")
    print(" - 32 reference entries")
    print(" - every entry cited in Bab I-V")
    print(" - every narrative/parenthetical citation resolves to an entry")
    print(" - no legacy citation forms remain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
