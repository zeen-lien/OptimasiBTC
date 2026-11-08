"""
[BAB 1 | GENERATOR DOKUMEN DOCX RESMI]
Skrip ini merakit BAB 1 PENDAHULUAN ke format Microsoft Word (.docx)
sesuai pedoman penulisan skripsi FST UNISNU Jepara:
- Kertas A4, Margin: Atas 4 cm, Kiri 4 cm, Bawah 3 cm, Kanan 3 cm
- Font Times New Roman 12 pt, Spasi 1.5, First Line Indent 1 cm
- Heading Bab 14 pt Bold Kapital Rata Tengah
- Heading Subbab 12 pt Bold Rata Kiri
- Penulisan simbol/rumus matematika inline: log tegak, variabel miring (italic),
  indeks waktu (subscript) menggunakan format font native Word (bukan kode mentah LaTeX).

Sumber teks: 03_Naskah_Skripsi/study2/BAB_1_PENDAHULUAN.md
Output: 03_Naskah_Skripsi/study2/BAB_1_PENDAHULUAN.docx
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from math_typesetter import (
    render_math_to_runs_academic,
    set_run_font_academic,
)

ROOT = Path(__file__).resolve().parents[2]
SRC_MD = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_1_PENDAHULUAN.md"
OUT_DOCX = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_1_PENDAHULUAN.docx"

GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η",
    r"\theta": "θ", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ",
    r"\tau": "τ", r"\phi": "φ", r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ",
    r"\Sigma": "Σ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
}


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


def render_math_to_runs(p, math_expr: str, default_size=12, base_bold=False):
    """Render inline math expressions cleanly as formatted runs in Word."""
    s = math_expr.strip()
    if s.startswith("$") and s.endswith("$"):
        s = s[1:-1].strip()
    elif s.startswith(r"\(") and s.endswith(r"\)"):
        s = s[2:-2].strip()

    s = s.replace(r"\_", "_")
    s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", s)
    for k, v in GREEK.items():
        s = s.replace(k, v)

    # Prefix operators like log, ln, exp, max, min
    for fn in ["log", "ln", "exp", "max", "min"]:
        if s.startswith("\\" + fn + " ") or s.startswith(fn + " "):
            r_fn = p.add_run(fn + " ")
            set_run_font(r_fn, size=default_size, bold=base_bold, italic=False)
            s = re.sub(r"^\\" + fn + r"\s+|^" + fn + r"\s+", "", s)
            break

    # Match base with optional subscript and superscript
    # Examples: RV_{t+1}, RV_t, range_t, volume_t, rv_mean_5_t, \sigma_t^2
    m = re.search(r"^(.*?)_(?:\{([^}]+)\}|([a-zA-Z0-9+-]+))(?:\^\{([^}]+)\}|\^([a-zA-Z0-9+-]+))?$", s)
    if not m:
        # Check without subscript, only superscript
        m_sup = re.search(r"^(.*?)(?:\^\{([^}]+)\}|\^([a-zA-Z0-9+-]+))$", s)
        if m_sup:
            base = m_sup.group(1).replace("\\", "").strip()
            sup = m_sup.group(2) or m_sup.group(3)
            r_base = p.add_run(base)
            set_run_font(r_base, size=default_size, bold=base_bold, italic=True)
            r_sup = p.add_run(sup)
            set_run_font(r_sup, size=default_size, bold=base_bold, italic=False, superscript=True)
            return
        # Plain variable without subscript or superscript
        r_plain = p.add_run(s.replace("\\", "").strip())
        set_run_font(r_plain, size=default_size, bold=base_bold, italic=True)
        return

    base = m.group(1).replace("\\", "").strip()
    sub = m.group(2) or m.group(3)
    sup = m.group(4) or m.group(5)

    r_b = p.add_run(base)
    set_run_font(r_b, size=default_size, bold=base_bold, italic=True)

    if sub:
        r_sub = p.add_run(sub)
        set_run_font(r_sub, size=default_size, bold=base_bold, italic=True, subscript=True)

    if sup:
        r_sup = p.add_run(sup)
        set_run_font(r_sup, size=default_size, bold=base_bold, italic=False, superscript=True)


def add_inline_formatting(p, text: str, default_size=12, default_italic=False, default_bold=False):
    pattern = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\\\(.+?\\\)|(?<!\\)\$[^$\n]+?\$)")
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


def generate_bab1_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(4.0)
    sec.left_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # Set normal style
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
        if not line:
            i += 1
            continue

        # Bab heading
        if line.startswith("# BAB I "):
            p1 = doc.add_paragraph()
            p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1.paragraph_format.space_before = Pt(0)
            p1.paragraph_format.space_after = Pt(4)
            p1.paragraph_format.line_spacing = 1.15
            run1 = p1.add_run("BAB I")
            set_run_font(run1, size=14, bold=True)

            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(18)
            p2.paragraph_format.line_spacing = 1.15
            run2 = p2.add_run("PENDAHULUAN")
            set_run_font(run2, size=14, bold=True)
            i += 1
            continue

        # Subheading 1.x
        if line.startswith("## 1."):
            subhead = line.replace("## ", "").strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.5
            run = p.add_run(subhead)
            set_run_font(run, size=12, bold=True)
            i += 1
            continue

        # Numbered list or bullet list
        num_match = re.match(r"^(\d+)\.\s+(.*)", line)
        bullet_match = re.match(r"^\*\s+(.*)", line)

        if num_match:
            num = num_match.group(1)
            content = num_match.group(2)
            item_text = content
            while i + 1 < len(lines) and lines[i + 1].startswith("   "):
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

    doc.core_properties.title = "BAB I PENDAHULUAN - Skripsi Study 2"
    doc.core_properties.author = "Zaini Leon Musthofa Kamal"
    doc.core_properties.subject = "Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin"
    doc.save(OUT_DOCX)
    print(f"[OK] Berhasil merakit DOCX: {OUT_DOCX} ({OUT_DOCX.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generate_bab1_docx()
