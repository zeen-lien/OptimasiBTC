"""
[SEMPRO | GENERATOR DOKUMEN PROPOSAL BAB I - III + DAFTAR PUSTAKA]
Skrip ini merakit PROPOSAL SEMINAR PROPOSAL (SEMPRO) BAB I - III LENGKAP
ke dalam satu berkas Microsoft Word (.docx) resmi sesuai pedoman FST UNISNU Jepara:
- Sampul Luar (Cover Depan Resmi dengan Logo UNISNU)
- Sampul Dalam (Halaman Judul - Halaman i)
- Lembar Persetujuan Pembimbing Seminar Proposal (Halaman ii)
- DAFTAR ISI (Halaman iii) dengan titik-titik pemimpin (dot leaders)
- DAFTAR TABEL (Halaman vi) dengan titik-titik pemimpin
- DAFTAR GAMBAR (Halaman vii) dengan titik-titik pemimpin
- BAB I PENDAHULUAN (A. Latar Belakang s.d. F. Sistematika Penulisan)
- BAB II LANDASAN TEORI (A. Volatilitas dan Realized Volatility s.d. I. Hipotesis Penelitian,
  Tabel 2.1, Gambar 2.1 & 2.2)
- BAB III METODE PENELITIAN (A. Jenis dan Desain Penelitian s.d. K. Jadwal Penelitian,
  Tabel 3.1 - 3.6, Gambar 3.1)
- DAFTAR PUSTAKA (36 referensi APA 7th Edition dengan 1 cm hanging indent)

Identitas Resmi Pengusul:
Nama : ZAINI LEON MUSTHOFA KAMAL
NIM  : 231240001455
Prodi: Teknik Informatika - FST UNISNU Jepara (Tahun 2026)

Output: 03_Naskah_Skripsi/study2/PROPOSAL_SEMPRO_BAB_I_III.docx
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "03_Naskah_Skripsi" / "study2"
OUT_DOCX = SRC_DIR / "PROPOSAL_SEMPRO_BAB_I_III.docx"
OUT_MD = SRC_DIR / "PROPOSAL_SEMPRO_BAB_I_III.md"
LOGO_PATH = SRC_DIR / "figures" / "logo_unisnu.png"

CHAPTER_FILES = [
    SRC_DIR / "BAB_1_PENDAHULUAN.md",
    SRC_DIR / "BAB_2_LANDASAN_TEORI.md",
    SRC_DIR / "BAB_3_METODE_PENELITIAN.md",
    SRC_DIR / "DAFTAR_REFERENSI_STUDY2.md",
]

# Pemetaan nomor halaman untuk DAFTAR ISI / TABEL / GAMBAR.
# Berkas ini dihasilkan oleh update_toc_pages_sempro.ps1 (Word COM).
# Bila belum ada, generator menulis tanda "?" agar tetap bisa dijalankan.
PAGE_MAP_PATH = Path(__file__).resolve().parent / "toc_pages_sempro.json"
TOC_KEYS_PATH = Path(__file__).resolve().parent / "toc_keys_sempro.json"


def load_page_map():
    if PAGE_MAP_PATH.exists():
        try:
            return json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            return {}
    return {}


def page_of(page_map, key, default="?"):
    return str(page_map.get(key, default))


def heading_entries():
    """Ambil struktur bab/subbab langsung dari Markdown agar DAFTAR ISI
    selalu sinkron dengan naskah."""
    entries = []
    for ch_file in CHAPTER_FILES:
        for raw in ch_file.read_text(encoding="utf-8").splitlines():
            line = raw.rstrip()
            if line.startswith("# BAB "):
                title = line[2:].strip()
                entries.append((0, title, title.split(" ", 2)[-1]))
            elif line.startswith("# DAFTAR PUSTAKA"):
                entries.append((0, "DAFTAR PUSTAKA", "DAFTAR PUSTAKA"))
            elif line.startswith("## "):
                title = line[3:].strip()
                entries.append((1, title, title))
            elif line.startswith("### "):
                title = line[4:].strip()
                entries.append((2, title, title))
    return entries


def table_captions():
    caps = []
    for ch_file in CHAPTER_FILES:
        for raw in ch_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("**Tabel ") and line.endswith("**"):
                caps.append(line[2:-2].strip())
    return caps


def figure_captions():
    caps = []
    for ch_file in CHAPTER_FILES:
        for raw in ch_file.read_text(encoding="utf-8").splitlines():
            m = re.match(r"!\[([^\]]+)\]\(", raw.strip())
            if m:
                caps.append(m.group(1).strip())
    return caps

GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η",
    r"\theta": "θ", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ",
    r"\tau": "τ", r"\phi": "φ", r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ",
    r"\Sigma": "Σ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
}

SUB = str.maketrans("0123456789+-=()aeoxhklmnpst", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ")
SUP = str.maketrans("0123456789+-=()nT*", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿᵀ*")


def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, subscript=False, superscript=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if subscript:
        run.font.subscript = True
    if superscript:
        run.font.superscript = True
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)


def replace_fractions(text: str) -> str:
    while r"\frac" in text:
        idx = text.find(r"\frac")
        arg1_start = text.find("{", idx)
        if arg1_start == -1:
            break
        depth = 0
        arg1_end = -1
        for i in range(arg1_start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    arg1_end = i
                    break
        if arg1_end == -1:
            break
        arg2_start = text.find("{", arg1_end)
        if arg2_start == -1:
            break
        depth = 0
        arg2_end = -1
        for i in range(arg2_start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    arg2_end = i
                    break
        if arg2_end == -1:
            break
        arg1 = text[arg1_start + 1:arg1_end]
        arg2 = text[arg2_start + 1:arg2_end]
        frac_expr = text[idx:arg2_end + 1]
        text = text.replace(frac_expr, f"({arg1}) / ({arg2})", 1)
    return text


def preprocess_latex(s: str) -> str:
    """Normalisasi perintah LaTeX yang tidak tertangani konverter utama."""
    s = s.replace(r"\qquad", "      ").replace(r"\quad", "   ")
    s = s.replace(r"\dots", "…").replace(r"\ldots", "…")
    s = s.replace(r"\ell", "ℓ")
    s = s.replace(r"\overline{\log RV}", "log RV̅")
    s = re.sub(r"\\overline\{([^{}]+)\}", lambda m: m.group(1) + "\u0305", s)
    s = re.sub(r"\\hat\{([^{}]+)\}", lambda m: m.group(1) + "\u0302", s)
    s = re.sub(r"\\bar\{([^{}]+)\}", lambda m: m.group(1) + "\u0304", s)
    s = re.sub(r"\\tilde\{([^{}]+)\}", lambda m: m.group(1) + "\u0303", s)
    s = s.replace(r"\tanh", "tanh").replace(r"\max", "max").replace(r"\min", "min")
    return s


def latex_to_unicode_display(src: str) -> str:
    s = src.strip()
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = preprocess_latex(s)
    
    # Handle cases environment
    cases_match = re.search(r"\\begin\{cases\}(.*?)\\end\{cases\}", s, re.DOTALL)
    if cases_match:
        inner = cases_match.group(1).strip()
        branches = [b.strip() for b in inner.split(r"\\")]
        formatted_branches = []
        for b in branches:
            b_clean = b.replace("&", "").strip()
            b_clean = re.sub(r"\s+", " ", b_clean)
            formatted_branches.append(b_clean)
        cases_str = "{ " + "   ;   ".join(formatted_branches) + " }"
        s = s.replace(cases_match.group(0), cases_str)

    # Clean text blocks
    s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathcal\{([^}]+)\}", r"\1", s)

    # Common functions & operators
    s = s.replace(r"\ln", "ln").replace(r"\log", "log").replace(r"\exp", "exp")
    s = s.replace(r"\sum", "Σ").replace(r"\odot", "⊙").replace(r"\cdot", "·")
    s = s.replace(r"\ge", "≥").replace(r"\le", "≤").replace(r"\sim", "∼")
    s = s.replace(r"\times", "×").replace(r"\sqrt", "√")
    s = s.replace(r"\propto", "∝").replace(r"\ell", "ℓ").replace(r"\in", "∈")
    s = s.replace(r"\lvert", "|").replace(r"\rvert", "|").replace(r"\mid", "|")

    # Accents & Hats
    s = s.replace(r"\widehat{\log RV}", "log RV̂").replace(r"\widehat{RV}", "RV̂")
    s = s.replace(r"\widehat{\text{Var}}", "Var̂").replace(r"\widehat{Var}", "Var̂")
    s = re.sub(r"\\widehat\{([^}]+)\}", r"\1̂", s)
    s = s.replace(r"\bar{d}", "d̄").replace(r"\tilde{c}", "c̃")

    for k, v in GREEK.items():
        s = s.replace(k, v)

    # Fractions
    s = replace_fractions(s)

    # Subscripts & superscripts
    s = re.sub(r"_\{([^{}]+)\}", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\^\{([^{}]+)\}", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"_([A-Za-z0-9])", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\^([A-Za-z0-9*])", lambda m: m.group(1).translate(SUP), s)

    s = s.replace(r"\_", "_").replace("{", "").replace("}", "").replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def render_inline_math(p, math_expr: str, default_size=12, base_bold=False):
    s = math_expr.strip()
    if s.startswith("$") and s.endswith("$"):
        s = s[1:-1].strip()
    elif s.startswith(r"\(") and s.endswith(r"\)"):
        s = s[2:-2].strip()

    s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", s)
    s = preprocess_latex(s)
    s = s.replace(r"\ln", "ln").replace(r"\log", "log").replace(r"\odot", "⊙").replace(r"\cdot", "·")
    s = s.replace(r"\ge", "≥").replace(r"\le", "≤").replace(r"\approx", "≈").replace(r"\propto", "∝")
    s = s.replace(r"\lvert", "|").replace(r"\rvert", "|").replace(r"\mid", "|")
    s = s.replace(r"\_", "_")

    # Accents & Hats
    s = s.replace(r"\widehat{\log RV}", "log RV̂").replace(r"\widehat{RV}", "RV̂")
    s = s.replace(r"\widehat{\text{Var}}", "Var̂").replace(r"\widehat{Var}", "Var̂")
    s = re.sub(r"\\widehat\{([^}]+)\}", r"\1̂", s)
    s = s.replace(r"\bar{d}", "d̄").replace(r"\tilde{c}", "c̃")
    s = s.replace(r"y^*", "y*")
    s = s.replace("rv_mean_5_t", "rv_mean_5ₜ").replace("rv_mean_22_t", "rv_mean_22ₜ")

    for k, v in GREEK.items():
        s = s.replace(k, v)

    tokens = re.split(r"(_\{[^}]+\}|\^\{[^}]+\}|_[A-Za-z0-9+-]|\^[A-Za-z0-9*+-])", s)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("_{") and tok.endswith("}"):
            sub_text = tok[2:-1]
            r = p.add_run(sub_text)
            set_run_font(r, size=default_size, bold=base_bold, italic=True, subscript=True)
        elif tok.startswith("^{") and tok.endswith("}"):
            sup_text = tok[2:-1]
            r = p.add_run(sup_text)
            set_run_font(r, size=default_size, bold=base_bold, italic=True, superscript=True)
        elif tok.startswith("_") and len(tok) == 2:
            r = p.add_run(tok[1])
            set_run_font(r, size=default_size, bold=base_bold, italic=True, subscript=True)
        elif tok.startswith("^") and len(tok) == 2:
            r = p.add_run(tok[1])
            set_run_font(r, size=default_size, bold=base_bold, italic=True, superscript=True)
        else:
            clean_tok = tok.replace("{", "").replace("}", "").replace("\\", "")
            r = p.add_run(clean_tok)
            set_run_font(r, size=default_size, bold=base_bold, italic=True)


def add_inline_formatting(p, text: str, default_size=12, default_bold=False, default_italic=False, depth=0):
    if not text:
        return
    if depth > 5:
        clean_text = text.replace(r"\_", "_")
        run = p.add_run(clean_text)
        set_run_font(run, size=default_size, bold=default_bold, italic=default_italic)
        return

    pattern = re.compile(
        r"(\*\*.+?\*\*|(?<!\\)\$[^$\n]+?\$|\\\(.+?\\\)|`[^`]+`|\*[^*\n]+?\*)"
    )
    tokens = pattern.split(text)

    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) >= 4:
            add_inline_formatting(p, tok[2:-2], default_size=default_size, default_bold=True, default_italic=default_italic, depth=depth + 1)
        elif tok.startswith("*") and tok.endswith("*") and len(tok) >= 2 and not tok.startswith("**"):
            add_inline_formatting(p, tok[1:-1], default_size=default_size, default_bold=default_bold, default_italic=True, depth=depth + 1)
        elif (tok.startswith("$") and tok.endswith("$")) or (tok.startswith(r"\(") and tok.endswith(r"\)")):
            render_inline_math(p, tok, default_size=default_size, base_bold=default_bold)
        elif tok.startswith("`") and tok.endswith("`"):
            run = p.add_run(tok[1:-1])
            set_run_font(run, name="Consolas", size=default_size - 1, bold=default_bold, italic=default_italic)
        else:
            clean_tok = tok.replace(r"\_", "_")
            run = p.add_run(clean_tok)
            set_run_font(run, size=default_size, bold=default_bold, italic=default_italic)


def set_table_borders(table):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        tblBorders = OxmlElement('w:tblBorders')
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '4')  # 0.5 pt
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), 'B0B0B0')
            tblBorders.append(border)
        tblPr[0].append(tblBorders)


def add_figure(doc, img_path: Path, caption: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(img_path), width=Cm(14.5))

    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(2)
    cp.paragraph_format.space_after = Pt(8)
    add_inline_formatting(cp, caption, default_size=10, default_italic=True)


def add_table_docx(doc, headers: list[str], rows: list[list[str]], caption: str):
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(8)
    cp.paragraph_format.space_after = Pt(4)
    run_cap = cp.add_run(caption)
    set_run_font(run_cap, size=11, bold=True)

    num_cols = len(headers)
    tbl = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i in range(num_cols):
        h = headers[i] if i < len(headers) else ""
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        add_inline_formatting(p, h, default_size=9.5, default_bold=True)
        shading = OxmlElement("w:shd")
        shading.set(qn("w:val"), "clear")
        shading.set(qn("w:color"), "auto")
        shading.set(qn("w:fill"), "E8EEF5")
        hdr_cells[i]._element.get_or_add_tcPr().append(shading)

    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        for c_idx in range(num_cols):
            val = row[c_idx] if c_idx < len(row) else ""
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or len(val) <= 4 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_inline_formatting(p, val, default_size=9.5)


def add_cover_page(doc):
    p_sempro = doc.add_paragraph()
    p_sempro.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sempro.paragraph_format.space_before = Pt(0)
    p_sempro.paragraph_format.space_after = Pt(8)
    r_sp = p_sempro.add_run("PROPOSAL SKRIPSI")
    set_run_font(r_sp, size=14, bold=True)

    p_judul = doc.add_paragraph()
    p_judul.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_judul.paragraph_format.space_before = Pt(6)
    p_judul.paragraph_format.space_after = Pt(28)
    p_judul.paragraph_format.line_spacing = 1.15
    r_j = p_judul.add_run("OPTIMASI HYPERPARAMETER LSTM MENGGUNAKAN ALGORITMA OPTUNA PADA PERAMALAN REALIZED VOLATILITY BITCOIN")
    set_run_font(r_j, size=14, bold=True)

    if LOGO_PATH.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(36)
        r_l = p_logo.add_run()
        r_l.add_picture(str(LOGO_PATH), width=Cm(5.0))

    p_oleh = doc.add_paragraph()
    p_oleh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_oleh.paragraph_format.space_before = Pt(12)
    p_oleh.paragraph_format.space_after = Pt(4)
    r_o1 = p_oleh.add_run("Disusun Oleh:\n")
    set_run_font(r_o1, size=12)
    r_o2 = p_oleh.add_run("ZAINI LEON MUSTHOFA KAMAL\n")
    set_run_font(r_o2, size=12, bold=True)
    r_o3 = p_oleh.add_run("NIM: 231240001455")
    set_run_font(r_o3, size=12, bold=True)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(48)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS ISLAM NAHDLATUL ULAMA JEPARA\n2026")
    set_run_font(r_inst, size=12, bold=True)

    doc.add_page_break()


def add_inner_title_page(doc):
    p_judul = doc.add_paragraph()
    p_judul.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_judul.paragraph_format.space_before = Pt(0)
    p_judul.paragraph_format.space_after = Pt(12)
    p_judul.paragraph_format.line_spacing = 1.15
    r_j = p_judul.add_run("OPTIMASI HYPERPARAMETER LSTM MENGGUNAKAN ALGORITMA OPTUNA PADA PERAMALAN REALIZED VOLATILITY BITCOIN")
    set_run_font(r_j, size=14, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Halaman Judul\n")
    set_run_font(r_sub, size=12, italic=True, bold=True)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(4)
    p_req.paragraph_format.space_after = Pt(28)
    p_req.paragraph_format.line_spacing = 1.15
    r_req = p_req.add_run("Diajukan untuk Memenuhi Persyaratan Seminar Proposal Skripsi\nProgram Strata Satu (S-1) Program Studi Teknik Informatika")
    set_run_font(r_req, size=11, italic=True)

    if LOGO_PATH.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(36)
        r_l = p_logo.add_run()
        r_l.add_picture(str(LOGO_PATH), width=Cm(4.5))

    p_oleh = doc.add_paragraph()
    p_oleh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_oleh.paragraph_format.space_before = Pt(12)
    p_oleh.paragraph_format.space_after = Pt(4)
    r_o1 = p_oleh.add_run("Disusun Oleh:\n")
    set_run_font(r_o1, size=12)
    r_o2 = p_oleh.add_run("ZAINI LEON MUSTHOFA KAMAL\n")
    set_run_font(r_o2, size=12, bold=True)
    r_o3 = p_oleh.add_run("NIM: 231240001455")
    set_run_font(r_o3, size=12, bold=True)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(48)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS ISLAM NAHDLATUL ULAMA JEPARA\n2026")
    set_run_font(r_inst, size=12, bold=True)

    doc.add_page_break()


def add_approval_page(doc):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(28)
    r_t = p_title.add_run("PERSETUJUAN PEMBIMBING")
    set_run_font(r_t, size=14, bold=True)

    p_text = doc.add_paragraph()
    p_text.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_text.paragraph_format.line_spacing = 1.5
    p_text.paragraph_format.space_after = Pt(12)
    r_txt = p_text.add_run("Proposal Skripsi dengan judul:")
    set_run_font(r_txt, size=12)

    p_judul = doc.add_paragraph()
    p_judul.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_judul.paragraph_format.space_before = Pt(4)
    p_judul.paragraph_format.space_after = Pt(20)
    p_judul.paragraph_format.line_spacing = 1.15
    r_j = p_judul.add_run("OPTIMASI HYPERPARAMETER LSTM MENGGUNAKAN ALGORITMA OPTUNA PADA PERAMALAN REALIZED VOLATILITY BITCOIN")
    set_run_font(r_j, size=12, bold=True)

    tbl_bio = doc.add_table(rows=4, cols=3)
    tbl_bio.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bio.autofit = True
    bio_data = [
        ("Nama Lengkap", ":", "Zaini Leon Musthofa Kamal"),
        ("Nomor Induk Mahasiswa (NIM)", ":", "231240001455"),
        ("Program Studi", ":", "Teknik Informatika"),
        ("Fakultas", ":", "Sains dan Teknologi"),
    ]
    for row_idx, (k, sep, val) in enumerate(bio_data):
        cells = tbl_bio.rows[row_idx].cells
        for col_idx, text_val in enumerate([k, sep, val]):
            p = cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(text_val)
            set_run_font(run, size=12, bold=(col_idx == 2 and row_idx in [0, 1]))

    p_acc = doc.add_paragraph()
    p_acc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_acc.paragraph_format.space_before = Pt(24)
    p_acc.paragraph_format.space_after = Pt(36)
    p_acc.paragraph_format.line_spacing = 1.5
    r_acc = p_acc.add_run("Telah diperiksa dan disetujui oleh Dosen Pembimbing untuk diajukan dalam Seminar Proposal (Sempro) Skripsi Program Studi Teknik Informatika Fakultas Sains dan Teknologi Universitas Islam Nahdlatul Ulama Jepara.")
    set_run_font(r_acc, size=12)

    tbl_ttd = doc.add_table(rows=1, cols=2)
    tbl_ttd.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ttd.autofit = True
    
    cell_left = tbl_ttd.rows[0].cells[0]
    p_kiri = cell_left.paragraphs[0]
    p_kiri.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kiri.paragraph_format.line_spacing = 1.15
    p_kiri.add_run("Mengetahui,\nKetua Program Studi Teknik Informatika\n\n\n\n\n\n(......................................................)\nNIP/NIY. ")
    for r in p_kiri.runs:
        set_run_font(r, size=12)

    cell_right = tbl_ttd.rows[0].cells[1]
    p_kanan = cell_right.paragraphs[0]
    p_kanan.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kanan.paragraph_format.line_spacing = 1.15
    p_kanan.add_run("Jepara, .............................. 2026\nPembimbing Proposal,\n\n\n\n\n\n(......................................................)\nNIP/NIY. ")
    for r in p_kanan.runs:
        set_run_font(r, size=12)

    doc.add_page_break()


def add_leader_entry(doc, title: str, page_str: str, bold=False, italic=False, space_before=1, space_after=1, indent_cm=0.0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if indent_cm > 0:
        p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(14.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    
    r1 = p.add_run(title)
    set_run_font(r1, size=12, bold=bold, italic=italic)
    r2 = p.add_run(f"\t{page_str}")
    set_run_font(r2, size=12, bold=bold)


def add_table_of_contents(doc):
    page_map = load_page_map()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(18)
    r_t = p_title.add_run("DAFTAR ISI")
    set_run_font(r_t, size=14, bold=True)

    add_leader_entry(doc, "Halaman Judul", "i", bold=True, space_after=2)
    add_leader_entry(doc, "PERSETUJUAN PEMBIMBING", "ii", bold=True, space_after=2)
    add_leader_entry(doc, "DAFTAR ISI", "iii", bold=True, space_after=2)
    add_leader_entry(doc, "DAFTAR TABEL", page_of(page_map, "DAFTAR TABEL", "iv"), bold=True, space_after=2)
    add_leader_entry(doc, "DAFTAR GAMBAR", page_of(page_map, "DAFTAR GAMBAR", "v"), bold=True, space_after=6)

    for level, title, search_key in heading_entries():
        if level == 0:
            add_leader_entry(
                doc,
                title,
                page_of(page_map, search_key),
                bold=True,
                space_before=4,
                space_after=2,
            )
        elif level == 1:
            add_leader_entry(doc, title, page_of(page_map, search_key), indent_cm=0.5)
        else:
            add_leader_entry(
                doc,
                title,
                page_of(page_map, search_key),
                indent_cm=1.0,
                italic=True,
            )

    doc.add_page_break()


def add_list_of_tables(doc):
    page_map = load_page_map()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(18)
    r_t = p_title.add_run("DAFTAR TABEL")
    set_run_font(r_t, size=14, bold=True)

    for caption in table_captions():
        add_leader_entry(doc, caption, page_of(page_map, caption))

    doc.add_page_break()


def add_list_of_figures(doc):
    page_map = load_page_map()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(18)
    r_t = p_title.add_run("DAFTAR GAMBAR")
    set_run_font(r_t, size=14, bold=True)

    for caption in figure_captions():
        add_leader_entry(doc, caption, page_of(page_map, caption))

    doc.add_page_break()


def render_markdown_files(doc, chapter_files):
    """Render daftar berkas Markdown ke dalam objek Document.

    Dipakai ulang oleh generator proposal maupun generator bab tunggal.
    """
    md_combined_blocks = []

    for ch_idx, ch_file in enumerate(chapter_files):
        text = ch_file.read_text(encoding="utf-8")
        lines = text.split("\n")
        in_references = (ch_file.name == "DAFTAR_REFERENSI_STUDY2.md")

        md_combined_blocks.append(text)

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("---"):
                i += 1
                continue

            # Bab / Main Heading
            if line.startswith("# BAB ") or line.startswith("# DAFTAR PUSTAKA"):
                if ch_idx > 0 and i == 0:
                    doc.add_page_break()

                if line.startswith("# DAFTAR PUSTAKA"):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(18)
                    r = p.add_run("DAFTAR PUSTAKA")
                    set_run_font(r, size=14, bold=True)
                    i += 1
                    continue

                # E.g. # BAB I PENDAHULUAN
                parts = line.replace("# ", "").split(" ", 2)
                bab_num = f"{parts[0]} {parts[1]}"
                bab_title = parts[2] if len(parts) > 2 else ""

                p1 = doc.add_paragraph()
                p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p1.paragraph_format.space_before = Pt(0)
                p1.paragraph_format.space_after = Pt(4)
                p1.paragraph_format.line_spacing = 1.15
                r1 = p1.add_run(bab_num)
                set_run_font(r1, size=14, bold=True)

                p2 = doc.add_paragraph()
                p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p2.paragraph_format.space_before = Pt(0)
                p2.paragraph_format.space_after = Pt(18)
                p2.paragraph_format.line_spacing = 1.15
                r2 = p2.add_run(bab_title)
                set_run_font(r2, size=14, bold=True)
                i += 1
                continue

            # Subheading Level 2 (## A. ...)
            if line.startswith("## "):
                subhead = line.replace("## ", "").strip()
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(14)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.5
                run = p.add_run(subhead)
                set_run_font(run, size=12, bold=True)
                i += 1
                continue

            # Subheading Level 3 (### 1. ...)
            if line.startswith("### "):
                subsubhead = line.replace("### ", "").strip()
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.line_spacing = 1.5
                run = p.add_run(subsubhead)
                set_run_font(run, size=12, bold=True, italic=True)
                i += 1
                continue

            # Subheading Level 4 (#### a. ...)
            if line.startswith("#### "):
                subsubsubhead = line.replace("#### ", "").strip()
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.5
                run = p.add_run(subsubsubhead)
                set_run_font(run, size=12, bold=False, italic=True)
                i += 1
                continue

            # Multi-line display math $$ ... $$
            if line == "$$" or (line.startswith("$$") and not line.endswith("$$")):
                math_lines = []
                if line != "$$":
                    math_lines.append(line[2:].strip())
                i += 1
                while i < len(lines) and lines[i].strip() != "$$":
                    math_lines.append(lines[i].strip())
                    i += 1
                i += 1
                full_math = " ".join(math_lines)

                tag_match = re.search(r"\\tag\{([^}]+)\}", full_math)
                tag_str = ""
                if tag_match:
                    tag_str = f"({tag_match.group(1)})"
                    full_math = full_math.replace(tag_match.group(0), "").strip()

                eq_text = latex_to_unicode_display(full_math)
                if tag_str:
                    eq_text = f"{eq_text}      {tag_str}"

                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(eq_text)
                set_run_font(run, size=11, italic=True)
                continue

            # Single-line display math $$ ... $$
            if line.startswith("$$") and line.endswith("$$") and len(line) > 2:
                raw_eq = line[2:-2].strip()
                tag_match = re.search(r"\\tag\{([^}]+)\}", raw_eq)
                tag_str = ""
                if tag_match:
                    tag_str = f"({tag_match.group(1)})"
                    raw_eq = raw_eq.replace(tag_match.group(0), "").strip()

                eq_text = latex_to_unicode_display(raw_eq)
                if tag_str:
                    eq_text = f"{eq_text}      {tag_str}"

                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(eq_text)
                set_run_font(run, size=11, italic=True)
                i += 1
                continue

            # Images
            img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if img_match:
                caption = img_match.group(1)
                rel_path = img_match.group(2)
                full_img_path = (SRC_DIR / rel_path).resolve()
                if full_img_path.exists():
                    add_figure(doc, full_img_path, caption)
                else:
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_inline_formatting(p, f"*[Gambar belum disematkan: {rel_path}]*", default_size=10, default_italic=True)
                i += 1
                continue

            # Tables
            if line.startswith("**Tabel ") and line.endswith("**"):
                cap_text = line[2:-2].strip()
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                tbl_lines = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    tbl_lines.append(lines[i].strip())
                    i += 1

                if len(tbl_lines) >= 3:
                    headers = [c.strip() for c in tbl_lines[0].strip("|").split("|")]
                    rows = []
                    for r_line in tbl_lines[2:]:
                        cells = [c.strip() for c in r_line.strip("|").split("|")]
                        rows.append(cells)
                    add_table_docx(doc, headers, rows, cap_text)
                continue

            # Bullet / Numbered lists
            list_match = re.match(r"^(\*|\-|\d+\.)\s+(.+)$", line)
            if list_match and not in_references:
                prefix = list_match.group(1)
                body = list_match.group(2)
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Cm(1.0)
                p.paragraph_format.first_line_indent = Cm(-0.5)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.line_spacing = 1.5
                if prefix in ["*", "-"]:
                    run_pfx = p.add_run("•  ")
                    set_run_font(run_pfx, size=12, bold=True)
                else:
                    run_pfx = p.add_run(f"{prefix} ")
                    set_run_font(run_pfx, size=12, bold=True)
                add_inline_formatting(p, body)
                i += 1
                continue

            # References paragraph with hanging indent
            if in_references and re.match(r"^\d+\.\s+", line):
                ref_text = re.sub(r"^\d+\.\s+", "", line)
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Cm(1.0)
                p.paragraph_format.first_line_indent = Cm(-1.0)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15
                add_inline_formatting(p, ref_text)
                i += 1
                continue

            # Normal body paragraph
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(1.0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.5
            add_inline_formatting(p, line)
            i += 1

    return md_combined_blocks


def generate_sempro_bundle():
    doc = Document()

    # Section 1: Front Matter (Cover, Sampul Dalam, Lembar Persetujuan, Daftar Isi, Tabel, Gambar)
    sec1 = doc.sections[0]
    sec1.page_width = Cm(21.0)
    sec1.page_height = Cm(29.7)
    sec1.top_margin = Cm(4.0)
    sec1.left_margin = Cm(4.0)
    sec1.bottom_margin = Cm(3.0)
    sec1.right_margin = Cm(3.0)

    # Set page number format to roman lower for sec1
    secPr1 = sec1._sectPr
    pgNumType1 = OxmlElement('w:pgNumType')
    pgNumType1.set(qn('w:fmt'), 'lowerRoman')
    secPr1.append(pgNumType1)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(4)

    # Build Front Matter
    add_cover_page(doc)
    add_inner_title_page(doc)
    add_approval_page(doc)
    add_table_of_contents(doc)
    add_list_of_tables(doc)
    add_list_of_figures(doc)

    # Section 2: Body (Bab I, Bab II, Bab III, Daftar Pustaka)
    sec2 = doc.add_section()
    sec2.top_margin = Cm(4.0)
    sec2.left_margin = Cm(4.0)
    sec2.bottom_margin = Cm(3.0)
    sec2.right_margin = Cm(3.0)

    secPr2 = sec2._sectPr
    pgNumType2 = OxmlElement('w:pgNumType')
    pgNumType2.set(qn('w:start'), '1')
    pgNumType2.set(qn('w:fmt'), 'decimal')
    secPr2.append(pgNumType2)

    md_combined_blocks = render_markdown_files(doc, CHAPTER_FILES)

    # Save Bundled DOCX
    doc.core_properties.title = "PROPOSAL SKRIPSI (BAB I - III) - Zaini Leon Musthofa Kamal"
    doc.core_properties.author = "Zaini Leon Musthofa Kamal"
    doc.save(OUT_DOCX)
    print(f"[OK] Berhasil menghasilkan berkas proposal Sempro: {OUT_DOCX}")

    # Kunci pencarian untuk penghitung nomor halaman DAFTAR ISI (Word COM)
    keys = [{"key": k, "scope": "front"} for k in ("DAFTAR TABEL", "DAFTAR GAMBAR")]
    keys += [{"key": search_key, "scope": "body"} for _, _, search_key in heading_entries()]
    keys += [{"key": cap, "scope": "body"} for cap in table_captions() + figure_captions()]
    TOC_KEYS_PATH.write_text(json.dumps(keys, ensure_ascii=False, indent=2), encoding="utf-8")

    # Save Bundled Markdown
    OUT_MD.write_text("\n\n---\n\n".join(md_combined_blocks), encoding="utf-8")
    print(f"[OK] Berhasil menyatukan Markdown Sempro: {OUT_MD}")


if __name__ == "__main__":
    generate_sempro_bundle()
