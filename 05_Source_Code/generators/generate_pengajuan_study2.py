"""
[BAB 1 & PENGAJUAN JUDUL | GENERATOR PROPOSAL]
Skrip ini merakit Formulir Pengajuan Judul Skripsi (Outline Praproposal)
ke format tabel resmi Microsoft Word (.docx) sesuai standar FST UNISNU Jepara.

Sumber teks: 02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2.md
Output: 02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2_GENERATED.docx
(Disimpan terpisah agar tidak menimpa dokumen asli pengguna).
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[2]
SRC_MD = ROOT / "02_Pengajuan_Judul" / "PENGAJUAN_JUDUL_STUDY2.md"
OUT_DOCX = ROOT / "02_Pengajuan_Judul" / "PENGAJUAN_JUDUL_STUDY2.docx"


def set_cell_font(cell, text: str, font_size: int = 11, bold: bool = False, italic: bool = False) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic


def parse_markdown_content(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    
    # Extract Title
    title_match = re.search(r"\*\*Judul Penelitian\*\*\s*\|\s*:\s*\|\s*\*\*([^\*]+)\*\*", text)
    title = title_match.group(1).strip() if title_match else "Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin"
    
    # Extract Background Paragraphs
    bg_section = text.split("### Latar Belakang (Poinnya)")[1].split("### Rumusan Masalah")[0].strip()
    raw_paras = [p.strip() for p in bg_section.split("\n\n") if p.strip()]
    bg_paras = []
    for p in raw_paras:
        clean_p = re.sub(r"\s*\(\d+\s*kata\)", "", p).strip()
        if clean_p and not clean_p.startswith("---"):
            bg_paras.append(clean_p)
            
    # Extract Research Questions
    rq_section = text.split("### Rumusan Masalah")[1].split("### Referensi / Pustaka Utama")[0].strip()
    rq_lines = [re.sub(r"^\d+\.\s*", "", l).strip() for l in rq_section.split("\n") if l.strip().startswith(("1.", "2.", "3.", "4."))]
    
    # Extract References
    ref_section = text.split("### Referensi / Pustaka Utama")[1].split("---")[0].strip()
    ref_lines = [re.sub(r"^\d+\.\s*", "", l).strip() for l in ref_section.split("\n") if l.strip() and l[0].isdigit()]
    
    return title, bg_paras, rq_lines, ref_lines


def generate_docx():
    title, bg_paras, rq_lines, ref_lines = parse_markdown_content(SRC_MD)
    
    doc = Document()
    sec = doc.sections[0]
    sec.page_height = Cm(29.7)
    sec.page_width = Cm(21.0)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)
    
    # Header
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = p_head.add_run("OUTLINE PROPOSAL SKRIPSI\n")
    r_h1.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.name = "Times New Roman"
    
    r_h2 = p_head.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS ISLAM NAHDLATUL ULAMA (UNISNU) JEPARA")
    r_h2.bold = True
    r_h2.font.size = Pt(11)
    r_h2.font.name = "Times New Roman"
    p_head.paragraph_format.space_after = Pt(12)
    
    # Table Structure (Matching Campus Outline Template)
    rows_data = [
        ("Nama", ":", "Zaini Leon Musthofa Kamal"),
        ("NIM", ":", "231240001455"),
        ("Judul Penelitian", ":", title),
        ("Latar Belakang (Poinnya)", ":", "\n\n".join(bg_paras)),
        ("Rumusan Masalah", ":", "\n".join(f"{i}. {q}" for i, q in enumerate(rq_lines, 1))),
        ("Referensi/Pustaka Utama", ":", "\n".join(f"[{i}] {ref}" for i, ref in enumerate(ref_lines, 1))),
    ]
    
    table = doc.add_table(rows=len(rows_data), cols=4)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, (label, colon, content) in enumerate(rows_data):
        cells = table.rows[i].cells
        set_cell_font(cells[0], label, font_size=10, bold=True)
        set_cell_font(cells[1], colon, font_size=10, bold=True)
        merged = cells[2].merge(cells[3])
        set_cell_font(merged, content, font_size=10, bold=False)
        cells[0].width = Cm(3.8)
        cells[1].width = Cm(0.5)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Signature block
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s = p_sign.add_run("Jepara, ................................\n\nPengusul,\n\n\n\n\n")
    r_s.font.name = "Times New Roman"
    r_s.font.size = Pt(11)
    
    r_name = p_sign.add_run("Zaini Leon Musthofa Kamal\nNIM. 231240001455")
    r_name.bold = True
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(11)
    
    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_DOCX)
    print(f"Berhasil dibuat: {OUT_DOCX}")


if __name__ == "__main__":
    generate_docx()
