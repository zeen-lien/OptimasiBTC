"""
[RENDERER BAB TUNGGAL STUDY 2]

Menghasilkan DOCX per bab (BAB I, BAB II, BAB III) memakai renderer yang sama
dengan PROPOSAL_SEMPRO_BAB_I_III.docx, sehingga konversi LaTeX, tabel, gambar,
dan format paragrafnya identik dengan dokumen proposal.

Pemakaian:
    python generate_bab_study2.py            # hasilkan ketiga bab
    python generate_bab_study2.py 2          # hanya BAB II
"""

from __future__ import annotations

import sys

from docx import Document
from docx.shared import Cm, Pt

from generate_sempro_study2 import SRC_DIR, render_markdown_files

CHAPTERS = {
    "1": ("BAB_1_PENDAHULUAN.md", "BAB_1_PENDAHULUAN.docx", "BAB I PENDAHULUAN"),
    "2": ("BAB_2_LANDASAN_TEORI.md", "BAB_2_LANDASAN_TEORI.docx", "BAB II LANDASAN TEORI"),
    "3": ("BAB_3_METODE_PENELITIAN.md", "BAB_3_METODE_PENELITIAN.docx", "BAB III METODE PENELITIAN"),
}


def build(chapter_key: str) -> None:
    md_name, docx_name, title = CHAPTERS[chapter_key]
    md_path = SRC_DIR / md_name
    out_path = SRC_DIR / docx_name

    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(4.0)
    sec.left_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(4)

    render_markdown_files(doc, [md_path])

    doc.core_properties.title = f"{title} - Skripsi Study 2"
    doc.core_properties.author = "Zaini Leon Musthofa Kamal"
    doc.save(out_path)
    size_kb = out_path.stat().st_size / 1024
    print(f"[OK] {out_path.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["1", "2", "3"]
    for key in targets:
        build(key)
