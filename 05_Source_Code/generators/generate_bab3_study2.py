"""
[BAB 3 | GENERATOR DOKUMEN DOCX RESMI]
Skrip ini merakit BAB 3 METODE PENELITIAN ke format Microsoft Word (.docx)
sesuai pedoman resmi penulisan skripsi FST UNISNU Jepara:
- Kertas A4, Margin: Atas 4 cm, Kiri 4 cm, Bawah 3 cm, Kanan 3 cm
- Font Times New Roman 12 pt, Spasi 1.5, First Line Indent 1 cm
- Heading Bab 14 pt Bold Kapital Rata Tengah
- Heading Subbab (3.x) 12 pt Bold Rata Kiri
- Heading Anak Subbab (3.x.x) 12 pt Bold Rata Kiri
- Persamaan matematis display berpenomoran (3.x) rata tengah
- Tabel formal dengan header shading abu-abu dan teks sel rapi
- Gambar diagram dari folder figures/ disisipkan rata tengah dengan caption 10 pt italic.

Sumber teks: 03_Naskah_Skripsi/study2/BAB_3_METODE_PENELITIAN.md
Output: 03_Naskah_Skripsi/study2/BAB_3_METODE_PENELITIAN.docx
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
SRC_MD = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_3_METODE_PENELITIAN.md"
OUT_DOCX = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_3_METODE_PENELITIAN.docx"

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


def latex_to_unicode_display(src: str) -> str:
    s = src.strip()
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathcal\{([^}]+)\}", r"\1", s)
    s = s.replace(r"\ln", "ln").replace(r"\log", "log").replace(r"\exp", "exp")
    s = s.replace(r"\sum", "Σ").replace(r"\odot", "⊙").replace(r"\cdot", "·")
    s = s.replace(r"\ge", "≥").replace(r"\le", "≤").replace(r"\sim", "∼")
    s = s.replace(r"\times", "×").replace(r"\sqrt", "√")
    for k, v in GREEK.items():
        s = s.replace(k, v)

    # replace fractions \frac{a}{b} -> (a)/(b)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)

    # subscripts & superscripts
    s = re.sub(r"_\{([^{}]+)\}", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\^\{([^{}]+)\}", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"_([A-Za-z0-9])", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\^([A-Za-z0-9])", lambda m: m.group(1).translate(SUP), s)

    s = s.replace(r"\_", "_").replace("{", "").replace("}", "").replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def render_inline_math(p, math_expr: str, default_size=12, base_bold=False):
    s = math_expr.strip()
    if s.startswith("$") and s.endswith("$"):
        s = s[1:-1].strip()
    elif s.startswith(r"\(") and s.endswith(r"\)"):
        s = s[2:-2].strip()

    s = s.replace(r"\_", "_")

    # Tokens: Greek letters, subscripts, superscripts, functions, plain identifiers
    pattern = re.compile(
        r"(\\[A-Za-z]+|"
        r"\^\{[^}]+\}|\^[A-Za-z0-9*]|"
        r"_\{[^}]+\}|_[A-Za-z0-9]|"
        r"[A-Za-z]+|\d+|[^\sA-Za-z0-9])"
    )

    tokens = pattern.findall(s)
    if not tokens:
        tokens = [s]

    for tok in tokens:
        if tok in (r"\log", r"\ln", r"\exp", r"\sin", r"\cos", r"\min", r"\max"):
            fn_name = tok[1:]
            run = p.add_run(fn_name)
            set_run_font(run, size=default_size, bold=base_bold, italic=False)
        elif tok in GREEK:
            g_char = GREEK[tok]
            run = p.add_run(g_char)
            set_run_font(run, size=default_size, bold=base_bold, italic=True)
        elif tok.startswith("_{") and tok.endswith("}"):
            sub_content = tok[2:-1]
            sub_content = sub_content.replace(r"\_", "_")
            run = p.add_run(sub_content)
            set_run_font(run, size=default_size - 2, bold=base_bold, italic=False, subscript=True)
        elif tok.startswith("_") and len(tok) == 2:
            run = p.add_run(tok[1])
            set_run_font(run, size=default_size - 2, bold=base_bold, italic=False, subscript=True)
        elif tok.startswith("^{") and tok.endswith("}"):
            sup_content = tok[2:-1]
            run = p.add_run(sup_content)
            set_run_font(run, size=default_size - 2, bold=base_bold, italic=False, superscript=True)
        elif tok.startswith("^") and len(tok) == 2:
            run = p.add_run(tok[1])
            set_run_font(run, size=default_size - 2, bold=base_bold, italic=False, superscript=True)
        elif tok.isalpha():
            run = p.add_run(tok)
            set_run_font(run, size=default_size, bold=base_bold, italic=True)
        else:
            run = p.add_run(tok)
            set_run_font(run, size=default_size, bold=base_bold, italic=False)


def add_inline_formatting(p, text: str, default_size=12, default_bold=False, default_italic=False):
    pattern = re.compile(
        r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\\\(.+?\\\)|(?<!\\)\$[^$\n]+?\$)"
    )
    tokens = pattern.split(text)

    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            run = p.add_run(tok[2:-2])
            set_run_font(run, size=default_size, bold=True, italic=default_italic)
        elif tok.startswith("*") and tok.endswith("*"):
            run = p.add_run(tok[1:-1])
            set_run_font(run, size=default_size, bold=default_bold, italic=True)
        elif tok.startswith("`") and tok.endswith("`"):
            run = p.add_run(tok[1:-1])
            set_run_font(run, name="Consolas", size=default_size - 1, bold=default_bold, italic=default_italic)
        elif (tok.startswith(r"\(") and tok.endswith(r"\)")) or (tok.startswith("$") and tok.endswith("$")):
            render_math_to_runs_academic(p, tok, default_size=default_size, base_bold=default_bold)
        else:
            run = p.add_run(tok)
            set_run_font(run, size=default_size, bold=default_bold, italic=default_italic)


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

    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True

    # Header row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        add_inline_formatting(p, h, default_size=9.5, default_bold=True)
        # Shading
        shading = OxmlElement("w:shd")
        shading.set(qn("w:val"), "clear")
        shading.set(qn("w:color"), "auto")
        shading.set(qn("w:fill"), "EAEAEA")
        hdr_cells[i]._element.get_or_add_tcPr().append(shading)

    # Data rows
    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_inline_formatting(p, val, default_size=9.5)


def generate_bab3_docx():
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
    style.paragraph_format.space_after = Pt(6)

    text = SRC_MD.read_text(encoding="utf-8")
    lines = text.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("---"):
            i += 1
            continue

        # Bab Heading
        if line.startswith("# BAB III "):
            p1 = doc.add_paragraph()
            p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1.paragraph_format.space_before = Pt(0)
            p1.paragraph_format.space_after = Pt(4)
            p1.paragraph_format.line_spacing = 1.15
            run1 = p1.add_run("BAB III")
            set_run_font(run1, size=14, bold=True)

            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(18)
            p2.paragraph_format.line_spacing = 1.15
            run2 = p2.add_run("METODE PENELITIAN")
            set_run_font(run2, size=14, bold=True)
            i += 1
            continue

        # Subheading 3.x
        if line.startswith("## 3."):
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

        # Sub-subheading 3.x.x
        if line.startswith("### 3."):
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

        # Multi-line display math $$ ... $$
        if line == "$$" or (line.startswith("$$") and not line.endswith("$$")):
            math_lines = []
            if line != "$$":
                math_lines.append(line[2:].strip())
            i += 1
            while i < len(lines) and lines[i].strip() != "$$":
                math_lines.append(lines[i].strip())
                i += 1
            i += 1 # skip closing $$
            full_math = " ".join(math_lines)
            
            tag_match = re.search(r"\\tag\{([^}]+)\}", full_math)
            tag_str = ""
            if tag_match:
                tag_str = f"({tag_match.group(1)})"
                full_math = full_math.replace(tag_match.group(0), "").strip()

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            render_math_to_runs_academic(p, full_math, default_size=11)
            if tag_str:
                r_space = p.add_run("      ")
                set_run_font_academic(r_space, size=11, italic=False)
                r_tag = p.add_run(tag_str)
                set_run_font_academic(r_tag, size=11, italic=False, bold=False)
            continue

        # Single-line display math $$ ... $$
        if line.startswith("$$") and line.endswith("$$") and len(line) > 2:
            raw_eq = line[2:-2].strip()
            tag_match = re.search(r"\\tag\{([^}]+)\}", raw_eq)
            tag_str = ""
            if tag_match:
                tag_str = f"({tag_match.group(1)})"
                raw_eq = raw_eq.replace(tag_match.group(0), "").strip()

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            render_math_to_runs_academic(p, raw_eq, default_size=11)
            if tag_str:
                r_space = p.add_run("      ")
                set_run_font_academic(r_space, size=11, italic=False)
                r_tag = p.add_run(tag_str)
                set_run_font_academic(r_tag, size=11, italic=False, bold=False)
            i += 1
            continue

        # Image ![caption](path)
        img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if img_match:
            caption = img_match.group(1)
            rel_path = img_match.group(2)
            full_img_path = (SRC_MD.parent / rel_path).resolve()
            if full_img_path.exists():
                add_figure(doc, full_img_path, caption)
            else:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_inline_formatting(p, f"*[Gambar belum disematkan: {rel_path}]*", default_size=10, default_italic=True)
            i += 1
            continue

        # Table caption & parse
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
                raw_headers = [c.strip() for c in tbl_lines[0].split("|")[1:-1]]
                raw_rows = []
                for tl in tbl_lines[2:]:
                    cols = [c.strip() for c in tl.split("|")[1:-1]]
                    if len(cols) == len(raw_headers):
                        raw_rows.append(cols)
                add_table_docx(doc, raw_headers, raw_rows, cap_text)
            continue

        # Numbered list or bullet list
        num_match = re.match(r"^(\d+)\.\s+(.*)", line)
        bullet_match = re.match(r"^\*\s+(.*)", line)

        if num_match:
            num = num_match.group(1)
            content = num_match.group(2)
            item_text = content
            while i + 1 < len(lines) and (lines[i + 1].startswith("   ") or lines[i + 1].startswith("\t")):
                i += 1
                item_text += " " + lines[i].strip()

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-1.0)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.space_before = Pt(0)
            
            run_num = p.add_run(f"{num}.\t")
            set_run_font(run_num, size=12, bold=False)
            add_inline_formatting(p, item_text, default_size=12)
            i += 1
            continue

        if bullet_match:
            content = bullet_match.group(1)
            item_text = content
            while i + 1 < len(lines) and lines[i + 1].startswith("  "):
                i += 1
                item_text += " " + lines[i].strip()

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.space_before = Pt(0)

            run_b = p.add_run("•\t")
            set_run_font(run_b, size=12, bold=False)
            add_inline_formatting(p, item_text, default_size=12)
            i += 1
            continue

        # Regular body paragraph
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Cm(1.0)
        add_inline_formatting(p, line, default_size=12)
        i += 1

    doc.core_properties.title = "BAB III METODE PENELITIAN - Skripsi Study 2"
    doc.core_properties.author = "Zaini Leon Musthofa Kamal"
    doc.core_properties.subject = "Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin"
    doc.save(OUT_DOCX)
    print(f"[OK] Berhasil merakit DOCX: {OUT_DOCX} ({OUT_DOCX.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generate_bab3_docx()

