"""Compile the Study 2 Markdown chapters into a single DOCX draft.

The Markdown files in 03_Naskah_Skripsi/study2/ are the source of truth.
This script renders headings, paragraphs, tables, figures, lists, and
(simplified) equations with UNISNU-style page formatting:

  A4, margins 4/4/3/3 cm, Times New Roman 12 pt, 1.5 line spacing,
  justified body text, 1 cm first-line indent.

Output: 03_Naskah_Skripsi/study2/SKRIPSI_STUDY2_DRAFT.docx
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "03_Naskah_Skripsi" / "study2"
OUT = SRC / "SKRIPSI_STUDY2_DRAFT.docx"

CHAPTERS = [
    "BAB_1_PENDAHULUAN.md",
    "BAB_2_LANDASAN_TEORI.md",
    "BAB_3_METODE_PENELITIAN.md",
    "BAB_4_HASIL_DAN_PEMBAHASAN.md",
    "BAB_5_PENUTUP.md",
    "DAFTAR_REFERENSI_STUDY2.md",
]

GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η",
    r"\theta": "θ", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ",
    r"\tau": "τ", r"\phi": "φ", r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ",
    r"\Sigma": "Σ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
}

SYMBOLS = {
    r"\cdot": "·", r"\times": "×", r"\leq": "≤", r"\le": "≤",
    r"\geq": "≥", r"\ge": "≥", r"\approx": "≈", r"\neq": "≠",
    r"\in": "∈", r"\notin": "∉", r"\rightarrow": "→", r"\to": "→",
    r"\infty": "∞", r"\pm": "±", r"\mid": "|", r"\odot": "⊙",
    r"\sum": "Σ", r"\prod": "Π", r"\int": "∫", r"\partial": "∂",
    r"\nabla": "∇", r"\propto": "∝", r"\sim": "∼", r"\equiv": "≡",
    r"\ldots": "…", r"\dots": "…", r"\quad": "  ", r"\qquad": "    ",
    r"\{": "{", r"\}": "}", r"\%": "%", r"\&": "&", r"\#": "#",
    r"\_": "_", r"\,": " ", r"\;": " ", r"\!": "", r"\ ": " ",
    r"\log": "log", r"\ln": "ln", r"\exp": "exp", r"\max": "max",
    r"\min": "min", r"\arg": "arg", r"\lim": "lim", r"\sin": "sin",
    r"\cos": "cos", r"\tan": "tan",
}

SUB = str.maketrans("0123456789+-=()aeoxhklmnpst", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ")
SUP = str.maketrans("0123456789+-=()nT", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿᵀ")


def _replace_braced(s: str, cmd: str, fmt) -> str:
    """Replace \\cmd{...} with fmt(inner), handling nested braces."""
    pattern = re.compile(re.escape(cmd) + r"\{")
    while True:
        m = pattern.search(s)
        if not m:
            return s
        start = m.end()
        depth = 1
        i = start
        while i < len(s) and depth:
            if s[i] == "{":
                depth += 1
            elif s[i] == "}":
                depth -= 1
            i += 1
        if depth:
            return s
        inner = s[start:i - 1]
        s = s[:m.start()] + fmt(inner) + s[i:]


def _read_group(s: str, start: int):
    """Read a {...} group whose opening brace is at s[start]."""
    depth = 1
    i = start + 1
    while i < len(s) and depth:
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
        i += 1
    return s[start + 1:i - 1], i


def _replace_frac(s: str) -> str:
    token = r"\frac"
    pos = 0
    while True:
        idx = s.find(token, pos)
        if idx == -1:
            return s
        j = idx + len(token)
        while j < len(s) and s[j] == " ":
            j += 1
        if j >= len(s) or s[j] != "{":
            pos = idx + len(token)
            continue
        num, j = _read_group(s, j)
        while j < len(s) and s[j] == " ":
            j += 1
        if j >= len(s) or s[j] != "{":
            pos = idx + len(token)
            continue
        den, j = _read_group(s, j)
        s = s[:idx] + f"({num})/({den})" + s[j:]
        pos = idx


def latex_to_unicode(src: str) -> str:
    s = src.strip()
    s = s.replace("\\\\", " ").replace("&", " ")
    s = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", s)
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = _replace_frac(s)
    s = _replace_braced(s, r"\sqrt", lambda x: f"√({x})")
    s = _replace_braced(s, r"\overline", lambda x: f"mean({x})")
    s = _replace_braced(s, r"\widehat", lambda x: x + "\u0302")
    s = _replace_braced(s, r"\hat", lambda x: x + "\u0302")
    s = _replace_braced(s, r"\bar", lambda x: x + "\u0304")
    s = _replace_braced(s, r"\tilde", lambda x: x + "\u0303")
    s = _replace_braced(s, r"\text", lambda x: x)
    s = _replace_braced(s, r"\mathrm", lambda x: x)
    for cmd, ch in sorted({**GREEK, **SYMBOLS}.items(), key=lambda kv: -len(kv[0])):
        s = s.replace(cmd, ch)
    s = re.sub(r"\\[a-zA-Z]+", "", s)

    # subscripts / superscripts
    def sub_repl(m):
        body = m.group(1)
        try:
            return body.translate(SUB)
        except Exception:
            return f"_{body}"

    def sup_repl(m):
        body = m.group(1)
        try:
            return body.translate(SUP)
        except Exception:
            return f"^{body}"

    s = re.sub(r"_\{([^{}]+)\}", sub_repl, s)
    s = re.sub(r"\^\{([^{}]+)\}", sup_repl, s)
    s = re.sub(r"_([A-Za-z0-9])", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\^([A-Za-z0-9])", lambda m: m.group(1).translate(SUP), s)
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def set_run(run, size=12, bold=False, italic=False, font="Times New Roman", subscript=False, superscript=False):
    run.font.name = font
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
        rfonts.set(qn(attr), font)


def render_inline_math(par, math_expr: str, size=12, base_bold=False):
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
            r_fn = par.add_run(fn + " ")
            set_run(r_fn, size=size, bold=base_bold, italic=False)
            s = re.sub(r"^\\" + fn + r"\s+|^" + fn + r"\s+", "", s)
            break

    # Match base with optional subscript and superscript
    m = re.search(r"^(.*?)_(?:\{([^}]+)\}|([a-zA-Z0-9+-]+))(?:\^\{([^}]+)\}|\^([a-zA-Z0-9+-]+))?$", s)
    if not m:
        m_sup = re.search(r"^(.*?)(?:\^\{([^}]+)\}|\^([a-zA-Z0-9+-]+))$", s)
        if m_sup:
            base = m_sup.group(1).replace("\\", "").strip()
            sup = m_sup.group(2) or m_sup.group(3)
            r_base = par.add_run(base)
            set_run(r_base, size=size, bold=base_bold, italic=True)
            r_sup = par.add_run(sup)
            set_run(r_sup, size=size, bold=base_bold, italic=False, superscript=True)
            return
        r_plain = par.add_run(latex_to_unicode(s))
        set_run(r_plain, size=size, bold=base_bold, italic=True)
        return

    base = m.group(1).replace("\\", "").strip()
    sub = m.group(2) or m.group(3)
    sup = m.group(4) or m.group(5)

    r_b = par.add_run(base)
    set_run(r_b, size=size, bold=base_bold, italic=True)

    if sub:
        r_sub = par.add_run(sub)
        set_run(r_sub, size=size, bold=base_bold, italic=True, subscript=True)

    if sup:
        r_sup = par.add_run(sup)
        set_run(r_sup, size=size, bold=base_bold, italic=False, superscript=True)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    fld_text = OxmlElement("w:t")
    fld_text.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(fld_text)
    run._r.append(fld_end)
    set_run(run, size=10)


def add_inline(par, text, size=12, base_bold=False, base_italic=False):
    """Render a small subset of Markdown inline formatting."""
    pattern = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\\\(.+?\\\)|(?<!\\)\$[^$\n]+?\$)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            set_run(par.add_run(text[pos:m.start()]), size, base_bold, base_italic)
        tok = m.group(0)
        if tok.startswith("**"):
            add_inline(par, tok[2:-2], size, True, base_italic)
        elif tok.startswith("*"):
            add_inline(par, tok[1:-1], size, base_bold, True)
        elif tok.startswith("`"):
            set_run(par.add_run(tok[1:-1]), size - 1, base_bold, base_italic, font="Consolas")
        elif tok.startswith(r"\(") or tok.startswith("$"):
            render_inline_math(par, tok, size=size, base_bold=base_bold)
        pos = m.end()
    if pos < len(text):
        set_run(par.add_run(text[pos:]), size, base_bold, base_italic)


def body_paragraph(doc, text, indent=True, spacing=1.5, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = spacing
    pf.space_after = Pt(6)
    pf.space_before = Pt(0)
    if indent:
        pf.first_line_indent = Cm(1.0)
    add_inline(p, text, size=size)
    return p


def add_heading_chapter(doc, text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for i, ln in enumerate(lines):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4 if i < len(lines) - 1 else 12)
        p.paragraph_format.line_spacing = 1.15
        set_run(p.add_run(ln.upper()), size=14, bold=True)


def add_heading_section(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.keep_with_next = True
    add_inline(p, text, size=12, base_bold=True)


def parse_table(lines):
    rows = []
    for ln in lines:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def add_table(doc, rows, caption=None):
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        add_inline(p, caption, size=10, base_bold=True)
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            txt = row[j] if j < len(row) else ""
            add_inline(p, txt, size=9, base_bold=(i == 0))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_figure(doc, path, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(14.0))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(2)
        add_inline(cp, caption, size=10, base_italic=True)


def add_cover(doc):
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("SKRIPSI"), size=16, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.5
    set_run(p.add_run("Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna "
                      "pada Prediksi Volatilitas Bitcoin"), size=16, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("Diajukan sebagai salah satu syarat untuk memperoleh gelar "
                      "Sarjana Komputer (S.Kom.)"), size=12)
    for _ in range(3):
        doc.add_paragraph()
    for text in [
        "ZAINI LEON MUSTHOFA KAMAL",
        "NIM. 231240001455",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(p.add_run(text), size=14, bold=True)
    for _ in range(4):
        doc.add_paragraph()
    for text in [
        "PROGRAM STUDI TEKNIK INFORMATIKA",
        "FAKULTAS SAINS DAN TEKNOLOGI",
        "UNIVERSITAS ISLAM NAHDLATUL ULAMA JEPARA",
        "2026",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(p.add_run(text), size=12, bold=(text == "2026"))
    doc.add_page_break()


def render_file(doc, path: Path, first_chapter: bool):
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    pending_table = []
    in_references = path.name.startswith("DAFTAR_REFERENSI")
    chapter_started = False

    def flush_table():
        nonlocal pending_table
        if pending_table:
            # caption was consumed separately
            add_table(doc, parse_table(pending_table))
            pending_table = []

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            flush_table()
            i += 1
            continue

        if stripped.startswith("# "):
            flush_table()
            if not chapter_started:
                if not first_chapter:
                    doc.add_page_break()
                chapter_started = True
            add_heading_chapter(doc, stripped[2:])
            i += 1
            continue

        if stripped.startswith("## "):
            flush_table()
            add_heading_section(doc, stripped[3:])
            i += 1
            continue

        if stripped.startswith("|"):
            pending_table.append(stripped)
            i += 1
            continue

        flush_table()

        # display equation
        if stripped == r"\[" or stripped.startswith(r"\["):
            eq_lines = []
            if stripped != r"\[":
                eq_lines.append(stripped[2:])
            i += 1
            while i < len(lines) and r"\]" not in lines[i]:
                eq_lines.append(lines[i].strip())
                i += 1
            if i < len(lines):
                tail = lines[i].strip().replace(r"\]", "")
                if tail:
                    eq_lines.append(tail)
                i += 1
            eq = latex_to_unicode(" ".join(eq_lines))
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            set_run(p.add_run(eq), size=12, italic=True)
            continue

        # image
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if m:
            caption, rel = m.group(1), m.group(2)
            img = (path.parent / rel).resolve()
            if img.exists():
                cap = re.sub(r"\\\((.+?)\\\)", lambda mm: latex_to_unicode(mm.group(1)), caption)
                add_figure(doc, img, latex_to_unicode(cap))
            else:
                body_paragraph(doc, f"[Gambar tidak ditemukan: {rel}]", indent=False)
            i += 1
            continue

        # table caption (bold line starting with **Tabel)
        if stripped.startswith("**Tabel") and stripped.endswith("**"):
            caption = stripped[2:-2]
            # collect following table lines
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            table_lines = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                table_lines.append(lines[j].strip())
                j += 1
            if table_lines:
                cap = re.sub(r"\\\((.+?)\\\)", lambda mm: latex_to_unicode(mm.group(1)), caption)
                add_table(doc, parse_table(table_lines), caption=latex_to_unicode(cap))
                i = j
                continue

        # source line
        if stripped.lower().startswith("sumber:"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.line_spacing = 1.0
            add_inline(p, stripped, size=9)
            i += 1
            continue

        # numbered list
        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.75)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, f"{m.group(1)}. {m.group(2)}", size=12)
            i += 1
            continue

        # bullet
        if stripped.startswith("- "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.75)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, "• " + stripped[2:], size=12)
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.right_indent = Cm(0.75)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            add_inline(p, stripped.lstrip("> ").strip(), size=10, base_italic=True)
            i += 1
            continue

        # horizontal rule
        if stripped in ("---", "***"):
            i += 1
            continue

        # reference entry (hanging indent)
        if in_references:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-1.0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            add_inline(p, stripped, size=11)
            i += 1
            continue

        body_paragraph(doc, stripped)
        i += 1

    flush_table()


def main() -> None:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(4.0)
    section.left_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(6)

    add_page_number(section.footer.paragraphs[0])
    add_cover(doc)

    for n, name in enumerate(CHAPTERS):
        render_file(doc, SRC / name, first_chapter=(n == 0))

    doc.core_properties.title = ("Optimasi Hyperparameter LSTM Menggunakan Algoritma "
                                 "Optuna pada Prediksi Volatilitas Bitcoin")
    doc.core_properties.author = "Zaini Leon Musthofa Kamal"
    doc.core_properties.subject = "Skripsi Study 2 - draf Bab 1-5"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"written: {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
