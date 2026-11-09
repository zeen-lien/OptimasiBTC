"""
[SIMULASI SEMPRO | GENERATOR DOKUMEN TANYA JAWAB UJIAN PROPOSAL]
Skrip ini merakit PANDUAN SIMULASI TANYA JAWAB UJIAN PROPOSAL SKRIPSI
ke dalam satu berkas Microsoft Word (.docx) profesional dan berbobot akademis:
- Identitas Lengkap Mahasiswa & Dospem
- Petunjuk Mental & Formula 3 Langkah Menjawab Penguji
- Bagian 1: Fondasi, Urgensi, & Motivasi Penelitian (5 Pertanyaan)
- Bagian 2: Landasan Teori & Arsitektur Model (3 Pertanyaan)
- Bagian 3: Optimasi Hyperparameter dengan Optuna (3 Pertanyaan)
- Bagian 4: Metodologi, Anti-Leakage, & Statistik Inferensial (4 Pertanyaan)
- Bagian 5: Menghadapi Pertanyaan Jebakan Dosen (3 Pertanyaan)
- Rangkuman Cheat-Sheet Angka Kunci Skripsi

Input : 03_Naskah_Skripsi/study2/SIMULASI_UJIAN_SEMPRO.md
Output: 03_Naskah_Skripsi/study2/SIMULASI_UJIAN_SEMPRO.docx
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from math_typesetter import (
    render_math_to_runs_academic,
    set_run_font_academic,
)

ROOT = Path(__file__).resolve().parents[2]
SRC_MD = ROOT / "03_Naskah_Skripsi" / "study2" / "SIMULASI_UJIAN_SEMPRO.md"
OUT_DOCX = ROOT / "03_Naskah_Skripsi" / "study2" / "SIMULASI_UJIAN_SEMPRO.docx"


def set_run_font(run, name="Calibri", size=11, bold=False, italic=False, color_rgb=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)


def add_inline_formatting(p, text: str, default_size=11, default_font="Calibri", default_color=None):
    pattern = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\\\(.+?\\\)|(?<!\\)\$[^$\n]+?\$)")
    tokens = pattern.split(text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            inner = tok[2:-2]
            run = p.add_run(inner)
            set_run_font(run, name=default_font, size=default_size, bold=True, color_rgb=default_color)
        elif tok.startswith("*") and tok.endswith("*"):
            inner = tok[1:-1]
            run = p.add_run(inner)
            set_run_font(run, name=default_font, size=default_size, italic=True, color_rgb=default_color)
        elif tok.startswith("`") and tok.endswith("`"):
            inner = tok[1:-1]
            run = p.add_run(inner)
            set_run_font(run, name="Consolas", size=default_size - 0.5, color_rgb=RGBColor(180, 40, 40))
        elif (tok.startswith(r"\(") and tok.endswith(r"\)")) or (tok.startswith("$") and tok.endswith("$")):
            render_math_to_runs_academic(p, tok, default_size=default_size)
        else:
            run = p.add_run(tok)
            set_run_font(run, name=default_font, size=default_size, color_rgb=default_color)


def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='FF0000', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)

    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = "w:{}".format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn("w:{}".format(key)), str(val))


def add_callout_box(doc, text: str, title: str = "TIPS MENTAL"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Cm(15.5)

    # Shading
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F0F4F8")
    cell._tc.get_or_add_tcPr().append(shd)

    # Left thick border, others none
    set_cell_border(
        cell,
        left=dict(val="single", sz=24, color="1F4E79", space=0),
        top=dict(val="none", sz=0, color="auto", space=0),
        bottom=dict(val="none", sz=0, color="auto", space=0),
        right=dict(val="none", sz=0, color="auto", space=0),
    )

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"📌 {title}:\n")
    set_run_font(r_title, name="Calibri", size=11, bold=True, color_rgb=RGBColor(31, 78, 121))

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        p_l = cell.add_paragraph()
        p_l.paragraph_format.space_before = Pt(2)
        p_l.paragraph_format.space_after = Pt(2)
        p_l.paragraph_format.line_spacing = 1.15
        add_inline_formatting(p_l, line, default_size=10.5)


def generate_simulasi_docx():
    doc = Document()

    # Page Margins: 3 cm everywhere
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(3.0)
    sec.left_margin = Cm(3.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # Base style
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.line_spacing = 1.2
    style.paragraph_format.space_after = Pt(4)

    text = SRC_MD.read_text(encoding="utf-8")
    lines = text.splitlines()

    i = 0
    in_callout = False
    callout_lines = []

    while i < len(lines):
        line = lines[i].strip()

        # Handle callout block > [!TIP]
        if line.startswith("> [!TIP]") or line.startswith(">"):
            if not in_callout:
                in_callout = True
                callout_lines = []
            clean_line = re.sub(r"^>\s*(\[\!TIP\])?\s*", "", line)
            if clean_line:
                callout_lines.append(clean_line)
            i += 1
            continue
        elif in_callout:
            in_callout = False
            add_callout_box(doc, "\n".join(callout_lines), title="PETUNJUK FORMULA 3 LANGKAH")
            callout_lines = []
            # continue evaluating current line

        if not line or line.startswith("---"):
            i += 1
            continue

        # Header 1: Document Title
        if line.startswith("# "):
            title = line[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(title)
            set_run_font(r, name="Calibri", size=15, bold=True, color_rgb=RGBColor(26, 54, 93))
            i += 1
            continue

        # Header 2: Major Section
        if line.startswith("## "):
            sec_title = line[3:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run(sec_title)
            set_run_font(r, name="Calibri", size=13, bold=True, color_rgb=RGBColor(31, 78, 121))
            i += 1
            continue

        # Header 3: Question or Sub-part
        if line.startswith("### "):
            q_title = line[4:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(q_title)
            set_run_font(r, name="Calibri", size=11.5, bold=True, color_rgb=RGBColor(192, 0, 0) if "Jebakan" in q_title else RGBColor(15, 34, 64))
            i += 1
            continue

        # Display Math $$ ... $$
        if line.startswith("$$") and line.endswith("$$") and len(line) > 2:
            eq = line[2:-2].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            render_math_to_runs_academic(p, eq, default_size=11)
            i += 1
            continue

        # Bullet List Items (* or -)
        if line.startswith("* ") or line.startswith("- "):
            item_text = line[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            run_pfx = p.add_run("▪  ")
            set_run_font(run_pfx, name="Calibri", size=10, bold=True, color_rgb=RGBColor(31, 78, 121))
            add_inline_formatting(p, item_text, default_size=11)
            i += 1
            continue

        # Numbered List Items
        num_m = re.match(r"^(\d+\.)\s+(.+)$", line)
        if num_m:
            pfx = num_m.group(1)
            body = num_m.group(2)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            run_pfx = p.add_run(f"{pfx} ")
            set_run_font(run_pfx, name="Calibri", size=11, bold=True, color_rgb=RGBColor(31, 78, 121))
            add_inline_formatting(p, body, default_size=11)
            i += 1
            continue

        # Normal Paragraph
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        add_inline_formatting(p, line, default_size=11)
        i += 1

    # Save Document
    doc.save(OUT_DOCX)
    print(f"[OK] Berhasil menghasilkan berkas Word Simulasi Sempro: {OUT_DOCX}")


if __name__ == "__main__":
    generate_simulasi_docx()

