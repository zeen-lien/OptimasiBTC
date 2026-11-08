"""Modul Tipografi Matematika Akademik Internasional untuk Naskah Skripsi FST UNISNU.

Mengimplementasikan aturan standar tipografi matematika ilmiah (ISO 80000-2, APA 7th, AMS):
1. Variabel aljabar Latin & parameter Yunani tunggal: Miring (Italic).
2. Nama fungsi (log, ln, exp, tanh, Var, dll.): Tegak (Roman / Non-Italic).
3. Akronim & variabel majemuk (RV, QLIKE, DM, HAR, GARCH, OLS, dll.): Tegak (Roman).
4. Angka, tanda kurung, kurung siku, koma, titik dua: Tegak (Roman).
5. Operator matematika (+, −, =, ·, ⊙, ≤, ≥, ∈, ∝, dll.): Tegak (Roman) dengan spasi proporsional.
6. Subskrip & superskrip menggunakan formatting Word native (w:vertAlign), bukan fallback unicode.
7. Subskrip kata (usulan, baseline, mean): Tegak (Roman). Subskrip variabel (t, i, j): Miring.

Dibuat untuk Study 2: Volatilitas Bitcoin (Zaini Leon Musthofa Kamal).
"""

from __future__ import annotations

import re
from typing import List
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ---------------------------------------------------------------- kamus simbol
MATH_FUNCS = {
    "log", "ln", "exp", "tanh", "max", "min", "sin", "cos", "lim",
    "sup", "inf", "Var", "Cov", "E", "dim", "sign", "diag", "std",
}

ACRONYMS = {
    "RV", "QLIKE", "DM", "HAR", "GARCH", "ARCH", "OLS", "HAC",
    "MAE", "RMSE", "TPE", "EI", "BPTT", "RNN", "LSTM", "UTC",
    "OHLCV", "TRX", "KOSPI", "DJIA", "H1", "H2", "H3", "RQ1", "RQ2", "RQ3",
    "usulan", "baseline", "mean", "range", "volume", "absret",
}

GREEK_LOWER = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η",
    r"\theta": "θ", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ",
    r"\tau": "τ", r"\phi": "φ", r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\ell": "ℓ",
}

GREEK_UPPER = {
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ",
    r"\Sigma": "Σ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
}

MATH_SYMBOLS = {
    r"\odot": " ⊙ ",
    r"\cdot": " · ",
    r"\times": " × ",
    r"\approx": " ≈ ",
    r"\ge": " ≥ ",
    r"\le": " ≤ ",
    r"\ne": " ≠ ",
    r"\propto": " ∝ ",
    r"\in": " ∈ ",
    r"\sim": " ∼ ",
    r"\dots": "…",
    r"\ldots": "…",
    r"\pm": " ± ",
    r"\sum": "Σ",
    r"\mathbb{R}": "ℝ",
    r"\infty": "∞",
}


class MathToken:
    """Representasi token matematika dengan atribut gaya font Word."""
    __slots__ = ("text", "italic", "bold", "subscript", "superscript")

    def __init__(
        self,
        text: str,
        italic: bool = False,
        bold: bool = False,
        subscript: bool = False,
        superscript: bool = False,
    ):
        self.text = text
        self.italic = italic
        self.bold = bold
        self.subscript = subscript
        self.superscript = superscript

    def __repr__(self):
        styles = []
        if self.italic: styles.append("it")
        if self.bold: styles.append("bf")
        if self.subscript: styles.append("sub")
        if self.superscript: styles.append("sup")
        st_str = ",".join(styles) if styles else "norm"
        return f"({self.text!r}:{st_str})"


def set_run_font_academic(
    run,
    name: str = "Times New Roman",
    size: float = 12.0,
    bold: bool = False,
    italic: bool = False,
    subscript: bool = False,
    superscript: bool = False,
    color: RGBColor | None = None,
):
    """Menerapkan konfigurasi font Word secara lengkap dan native."""
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if subscript:
        run.font.subscript = True
    if superscript:
        run.font.superscript = True
    if color is not None:
        run.font.color.rgb = color

    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)


def parse_math_to_academic_tokens(math_expr: str, base_bold: bool = False) -> List[MathToken]:
    """Menguraikan ekspresi matematika LaTeX menjadi serangkaian MathToken berstandar internasional."""
    s = math_expr.strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) >= 4:
        s = s[2:-2].strip()
    elif s.startswith("$") and s.endswith("$") and len(s) >= 2:
        s = s[1:-1].strip()
    elif s.startswith(r"\(") and s.endswith(r"\)"):
        s = s[2:-2].strip()

    # Bersihkan formatting dasar LaTeX
    s = s.replace(r"\qquad", "   ").replace(r"\quad", " ")
    s = s.replace(r"\,", "").replace(r"\!", "")
    s = s.replace(r"\left", "").replace(r"\right", "")
    s = re.sub(r"(\d+)\{,\}(\d+)", r"\1,\2", s)  # 0{,}05 -> 0,05

    # Simpan escaped underscore sebelum tokenisasi
    s = s.replace(r"\_", "@@UNDERSCORE@@")

    # Bersihkan backslash dari fungsi baku
    for fn in ("log", "ln", "exp", "tanh", "max", "min", "sin", "cos", "sum", "dim"):
        s = re.sub(rf"\\{fn}\b", fn, s)

    # Tangani pecahan sederhana \frac{a}{b} -> (a) / (b) jika ada di inline
    while r"\frac" in s:
        m_frac = re.search(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", s)
        if m_frac:
            arg1, arg2 = m_frac.group(1), m_frac.group(2)
            # Bila argumen angka sederhana seperti \frac{1}{7} -> (1/7)
            if arg1.isdigit() and arg2.isdigit():
                s = s.replace(m_frac.group(0), f"({arg1}/{arg2})")
            else:
                s = s.replace(m_frac.group(0), f"({arg1}) / ({arg2})")
        else:
            break

    # Tangani aksen/topi/garis khusus
    s = s.replace(r"\widehat{\log RV}", "log RV̂")
    s = s.replace(r"\widehat{RV}", "RV̂")
    s = s.replace(r"\widehat{\text{Var}}", "Var̂")
    s = s.replace(r"\widehat{Var}", "Var̂")
    s = re.sub(r"\\widehat\{([^}]+)\}", r"\1̂", s)
    s = re.sub(r"\\hat\{([^}]+)\}", r"\1̂", s)
    s = re.sub(r"\\bar\{([^}]+)\}", r"\1̄", s)
    s = re.sub(r"\\tilde\{([^}]+)\}", r"\1̃", s)
    s = s.replace(r"\bar{d}", "d̄").replace(r"\tilde{c}", "c̃")
    s = s.replace(r"\overline{\log RV}", "log RV̅")
    s = re.sub(r"\\overline\{([^}]+)\}", r"\1̅", s)

    # Bersihkan \text{...} dan \mathrm{...}
    s = re.sub(r"\\(?:text|mathrm|operatorname)\{([^}]+)\}", r"\1", s)

    # Ganti operator & simbol
    for k, v in MATH_SYMBOLS.items():
        s = s.replace(k, v)

    for k, v in GREEK_UPPER.items():
        s = s.replace(k, v)

    for k, v in GREEK_LOWER.items():
        s = s.replace(k, v)

    # Rapikan spasi relasi biner (=, <, >, dll)
    s = re.sub(r"(?<=[a-zA-Z0-9α-ω])\s*=\s*(?=[a-zA-Z0-9α-ω\-+])", " = ", s)
    s = re.sub(r"(?<=[a-zA-Z0-9α-ω])\s*<\s*(?=[a-zA-Z0-9α-ω\-+])", " < ", s)
    s = re.sub(r"(?<=[a-zA-Z0-9α-ω])\s*>\s*(?=[a-zA-Z0-9α-ω\-+])", " > ", s)

    # Tokenisasi
    token_pattern = re.compile(
        r"(_\{[^}]+\}|_[A-Za-z0-9α-ω]|"
        r"\^\{[^}]+\}|\^[A-Za-z0-9α-ω*]|"
        r"[A-Za-zα-ωΑ-Ω][A-Za-z0-9]*[̂̃̄]?|"
        r"\d+(?:[.,]\d+)?|"
        r"@@UNDERSCORE@@|"
        r"\s+|"
        r"[^\s])"
    )

    raw_tokens = token_pattern.findall(s)
    tokens: List[MathToken] = []

    for raw in raw_tokens:
        if not raw:
            continue

        if raw == "@@UNDERSCORE@@":
            tokens.append(MathToken("_", italic=False, bold=base_bold))
            continue

        # Subskrip
        if raw.startswith("_"):
            sub_content = raw[2:-1] if raw.startswith("_{") else raw[1:]
            sub_pieces = re.findall(r"([A-Za-zα-ω][A-Za-z0-9]*[̂̃̄]?|\d+|[^\sA-Za-zα-ω\d]+|\s+)", sub_content)
            for sp in sub_pieces:
                if not sp:
                    continue
                # Kata subskrip multi-karakter (usulan, baseline, mean, max) -> TEGAK
                if sp in ACRONYMS or len(sp) > 1:
                    tokens.append(MathToken(sp, italic=False, bold=base_bold, subscript=True))
                elif re.match(r"^[A-Za-zα-ω][̂̃̄]?$", sp):
                    # Karakter tunggal variabel -> MIRING
                    tokens.append(MathToken(sp, italic=True, bold=base_bold, subscript=True))
                else:
                    # Angka, tanda baca, simbol minus matematis -> TEGAK
                    clean_sp = sp.replace("-", "−")
                    tokens.append(MathToken(clean_sp, italic=False, bold=base_bold, subscript=True))
            continue

        # Superskrip
        if raw.startswith("^"):
            sup_content = raw[2:-1] if raw.startswith("^{") else raw[1:]
            sup_pieces = re.findall(r"([A-Za-zα-ω][A-Za-z0-9]*[̂̃̄]?|\d+|[^\sA-Za-zα-ω\d]+|\s+)", sup_content)
            for sp in sup_pieces:
                if not sp:
                    continue
                if sp in ACRONYMS or len(sp) > 1:
                    tokens.append(MathToken(sp, italic=False, bold=base_bold, superscript=True))
                elif re.match(r"^[A-Za-zα-ω][̂̃̄]?$", sp):
                    tokens.append(MathToken(sp, italic=True, bold=base_bold, superscript=True))
                else:
                    clean_sp = sp.replace("-", "−")
                    tokens.append(MathToken(clean_sp, italic=False, bold=base_bold, superscript=True))
            continue

        # Spasi murni
        if raw.isspace():
            tokens.append(MathToken(raw, italic=False, bold=base_bold))
            continue

        # Angka murni
        if re.match(r"^\d+(?:[.,]\d+)?$", raw):
            tokens.append(MathToken(raw, italic=False, bold=base_bold))
            continue

        # Fungsi matematika (log, ln, exp, tanh, Var, dll.) -> TEGAK
        if raw in MATH_FUNCS:
            tokens.append(MathToken(raw, italic=False, bold=base_bold))
            continue

        # Akronim / Variabel Majemuk (RV, QLIKE, DM, HAR, GARCH, dll.) -> TEGAK
        clean_raw = raw.rstrip("̂̃̄")
        if clean_raw in ACRONYMS:
            tokens.append(MathToken(raw, italic=False, bold=base_bold))
            continue

        # Variabel Latin / Yunani tunggal -> MIRING (ITALIC)
        if re.match(r"^[A-Za-zα-ω][̂̃̄]?$", raw):
            tokens.append(MathToken(raw, italic=True, bold=base_bold))
            continue

        # Huruf Yunani kapital (Γ, Δ, Θ, Σ, dll.) -> TEGAK
        if re.match(r"^[Α-Ω]$", raw):
            tokens.append(MathToken(raw, italic=False, bold=base_bold))
            continue

        # Tanda kurung, pembatas, operator, tanda baca -> TEGAK
        char = raw
        if char == "-":
            char = "−"
        tokens.append(MathToken(char, italic=False, bold=base_bold))

    # Gabungkan token bertetangga yang formatnya identik agar Word run efisien
    merged: List[MathToken] = []
    for tok in tokens:
        if not tok.text:
            continue
        if (
            merged and
            merged[-1].italic == tok.italic and
            merged[-1].bold == tok.bold and
            merged[-1].subscript == tok.subscript and
            merged[-1].superscript == tok.superscript
        ):
            merged[-1].text += tok.text
        else:
            merged.append(tok)

    return merged


def render_math_to_runs_academic(
    p,
    math_expr: str,
    default_size: float = 12.0,
    base_bold: bool = False,
    font_name: str = "Times New Roman",
):
    """Menambahkan run matematika berstandar akademik ke dalam paragraf Word."""
    tokens = parse_math_to_academic_tokens(math_expr, base_bold=base_bold)
    for tok in tokens:
        if not tok.text:
            continue
        run = p.add_run(tok.text)
        set_run_font_academic(
            run,
            name=font_name,
            size=default_size,
            bold=tok.bold or base_bold,
            italic=tok.italic,
            subscript=tok.subscript,
            superscript=tok.superscript,
        )
