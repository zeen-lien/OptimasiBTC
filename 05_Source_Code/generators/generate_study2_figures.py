"""Generate diagram Bab 2 dan Bab 3 untuk Study 2.

Menghasilkan tiga berkas PNG 300 DPI di 03_Naskah_Skripsi/study2/figures/:
  - gambar_2_1_arsitektur_lstm.png
  - gambar_2_2_kerangka_pemikiran.png
  - gambar_3_1_alur_penelitian.png

Jalankan: python 05_Source_Code/generators/generate_study2_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "03_Naskah_Skripsi" / "study2" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "custom",
        "mathtext.rm": "Times New Roman",
        "mathtext.it": "Times New Roman:italic",
        "mathtext.bf": "Times New Roman:bold",
        "font.size": 11,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.06,
    }
)

INK = "#1F2933"
MUTED = "#52606D"
LINE = "#7B8794"

NAVY = "#1F3864"
BLUE = "#2E5EAA"
TEAL = "#1B6E63"
GREEN = "#2F6B3A"
AMBER = "#9A5B00"
MAROON = "#8C2F39"
PURPLE = "#4B3F87"

TINT = {
    NAVY: "#EDF1F8",
    BLUE: "#EBF1FA",
    TEAL: "#E8F3F1",
    GREEN: "#ECF4ED",
    AMBER: "#FBF2E4",
    MAROON: "#F8EAEC",
    PURPLE: "#EFECF7",
}


def canvas(width: float, height: float):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    edge: str = BLUE,
    face: str | None = None,
    lw: float = 1.2,
    radius: float = 0.10,
    zorder: int = 2,
):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face if face is not None else TINT.get(edge, "#FFFFFF"),
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, *, color: str = LINE, lw: float = 1.1, rad: float = 0.0, style: str = "-|>"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=11,
            linewidth=lw,
            color=color,
            shrinkA=2,
            shrinkB=2,
            connectionstyle=f"arc3,rad={rad}",
            zorder=1,
        )
    )


def label(ax, x, y, text, *, size=11, color=INK, weight="normal", ha="center", va="center", style="normal", wrap=False, zorder=5):
    ax.text(
        x,
        y,
        text,
        fontsize=size,
        color=color,
        fontweight=weight,
        ha=ha,
        va=va,
        fontstyle=style,
        linespacing=1.25,
        wrap=wrap,
        zorder=zorder,
    )


def stage_band(ax, y: float, h: float, number: int, title: str, color: str, width: float = 11.5, x0: float = 0.25):
    box(ax, x0, y, width, h, edge=color, face=TINT[color], lw=1.1, radius=0.10, zorder=1)
    badge = plt.Circle((x0 + 0.42, y + h - 0.30), 0.20, facecolor=color, edgecolor=color, zorder=3)
    ax.add_patch(badge)
    label(ax, x0 + 0.42, y + h - 0.30, str(number), size=10.2, color="white", weight="bold", zorder=4)
    label(ax, x0 + 0.80, y + h - 0.30, title, size=11, color=color, weight="bold", ha="left", zorder=4)


def chip(ax, x: float, y: float, w: float, h: float, text: str, color: str, *, size=9.6):
    box(ax, x, y, w, h, edge=color, face="#FFFFFF", lw=1.0, radius=0.07, zorder=3)
    label(ax, x + w / 2, y + h / 2, text, size=size, color=INK)


def circle_op(ax, x: float, y: float, symbol: str, r: float = 0.28, edge: str = BLUE, face: str = "#FFFFFF", lw: float = 1.3, zorder: int = 4):
    c = Circle((x, y), r, edgecolor=edge, facecolor=face, linewidth=lw, zorder=zorder)
    ax.add_patch(c)
    ax.text(x, y, symbol, fontsize=12, fontweight="bold", ha="center", va="center", color=edge, zorder=zorder + 1)


# ---------------------------------------------------------------- Gambar 2.1
def gambar_2_1() -> Path:
    """Diagram Arsitektur Sel dan Aliran Informasi LSTM Kanonikal (Standar Olah & Persamaan 2.6-2.11)."""
    W, H = 14.2, 8.4
    fig, ax = canvas(W, H)

    # Batas luar sel LSTM t
    outer = FancyBboxPatch(
        (2.15, 0.45), 10.35, 7.50,
        boxstyle="round,pad=0,rounding_size=0.25",
        linewidth=1.4, linestyle="--", edgecolor="#A0AEC0", facecolor="#F8FAFC", zorder=1
    )
    ax.add_patch(outer)
    label(ax, 2.35, 7.68, "Batas Internal Komputasi Sel LSTM (Langkah Waktu $t$)", size=9.8, color="#4A5568", weight="bold", ha="left")

    # =========================================================================
    # 1. JALUR STATUS SEL (CELL STATE FREEWAY / JALAN TOL MEMORI) - BARIS ATAS
    # =========================================================================
    cy = 6.75
    # Masukan c_{t-1}
    box(ax, 0.20, cy - 0.45, 1.65, 0.90, edge=NAVY, lw=1.3)
    label(ax, 1.025, cy + 0.16, "Status Sel Masa Lalu", size=8.2, color=NAVY, weight="bold")
    label(ax, 1.025, cy - 0.18, r"$c_{t-1}$", size=12.0, weight="bold")

    # Simpul Operasi 1: Perkalian elemen forget gate (x=4.20)
    op1_x = 4.20
    circle_op(ax, op1_x, cy, r"$\odot$", r=0.28, edge=MAROON, lw=1.4)

    # Simpul Operasi 2: Penjumlahan update memori baru (x=6.95)
    op2_x = 6.95
    circle_op(ax, op2_x, cy, r"$+$", r=0.28, edge=NAVY, lw=1.5)

    # Titik Percabangan c_t ke tanh dan keluaran (x=11.15)
    split_c_x = 11.15

    # Aliran jalan tol c:
    arrow(ax, (1.85, cy), (op1_x - 0.32, cy), color=NAVY, lw=1.5)
    arrow(ax, (op1_x + 0.32, cy), (op2_x - 0.32, cy), color=NAVY, lw=1.5)
    ax.plot([op2_x + 0.32, split_c_x], [cy, cy], color=NAVY, lw=1.5, zorder=2)
    # Titik cabang c_t
    dot_c = Circle((split_c_x, cy), 0.08, facecolor=NAVY, edgecolor=NAVY, zorder=4)
    ax.add_patch(dot_c)
    # Lanjut ke keluaran c_t
    arrow(ax, (split_c_x, cy), (12.75, cy), color=NAVY, lw=1.5)

    # Keluaran c_t di kanan
    box(ax, 12.80, cy - 0.45, 1.25, 0.90, edge=NAVY, lw=1.3)
    label(ax, 13.425, cy + 0.16, "Status Sel Baru", size=8.2, color=NAVY, weight="bold")
    label(ax, 13.425, cy - 0.18, r"$c_t$", size=12.0, weight="bold")

    # Formula Persamaan (2.9) di atas rel
    label(ax, 6.95, 7.30, r"Pembaruan Status Sel: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$", size=10.5, color=NAVY, weight="bold")

    # =========================================================================
    # 2. MASUKAN x_t DAN h_{t-1} SERTA BLOK KONKATENASI
    # =========================================================================
    # Masukan x_t
    box(ax, 0.20, 0.70, 1.65, 1.15, edge=BLUE, lw=1.3)
    label(ax, 1.025, 1.55, "Fitur Masukan Baru", size=8.0, color=BLUE, weight="bold")
    label(ax, 1.025, 1.22, r"$x_t \in \mathbb{R}^6$", size=11.0, weight="bold")
    label(ax, 1.025, 0.92, "(6 fitur kausal)", size=7.8, color=MUTED)

    # Masukan h_{t-1}
    box(ax, 0.20, 2.25, 1.65, 0.95, edge=GREEN, lw=1.3)
    label(ax, 1.025, 2.85, "Status Tersembunyi Lalu", size=7.8, color=GREEN, weight="bold")
    label(ax, 1.025, 2.50, r"$h_{t-1}$", size=11.5, weight="bold")

    # Blok Konkatenasi [h_{t-1}, x_t]
    box(ax, 2.35, 1.40, 1.40, 1.50, edge=BLUE, lw=1.4, face="#EBF4FF")
    label(ax, 3.05, 2.52, "Konkatenasi", size=8.2, color=BLUE, weight="bold")
    label(ax, 3.05, 2.12, r"$[h_{t-1}, x_t]$", size=11.8, weight="bold")
    label(ax, 3.05, 1.70, "Penggabungan Vektor", size=7.2, color=MUTED)

    arrow(ax, (1.85, 2.72), (2.35, 2.30), color=GREEN, lw=1.3)
    arrow(ax, (1.85, 1.30), (2.35, 1.90), color=BLUE, lw=1.3)

    # =========================================================================
    # 3. EMPAT GERBANG KOMPUTASI (FOUR PARALLEL GATES)
    # =========================================================================
    # Jalur Bus Konkatenasi
    bus_y = 2.15
    line_bus = "#2B6CB0"
    ax.plot([3.75, 9.40], [bus_y, bus_y], color=line_bus, lw=1.5, zorder=2)
    label(ax, 3.82, bus_y + 0.16, r"$[h_{t-1}, x_t]$", size=8.5, color=BLUE, ha="left")

    # --- Gate 1: Gerbang Lupa (Forget Gate) ---
    g1_x = 4.20
    box(ax, 3.35, 3.45, 1.70, 1.90, edge=MAROON, lw=1.3)
    label(ax, g1_x, 5.08, "Gerbang Lupa (Forget)", size=8.5, color=MAROON, weight="bold")
    label(ax, g1_x, 4.68, r"$\sigma$", size=14.0, color=MAROON, weight="bold")
    label(ax, g1_x, 4.12, r"$f_t = \sigma\left(W_f [h_{t-1}, x_t] + b_f\right)$", size=8.0)
    label(ax, g1_x, 3.70, "(Persamaan 2.6)", size=7.5, color=MUTED)

    # Cabang Bus ke Gate 1
    arrow(ax, (g1_x, bus_y), (g1_x, 3.45), color=MAROON, lw=1.3)
    # Output Gate 1 naik ke op1 pada jalan tol c
    arrow(ax, (g1_x, 5.35), (op1_x, cy - 0.32), color=MAROON, lw=1.4)
    label(ax, g1_x + 0.22, 5.85, r"$f_t$", size=9.5, color=MAROON, weight="bold")

    # --- Gate 2: Gerbang Masuk (Input Gate) ---
    g2_x = 5.95
    box(ax, 5.15, 3.45, 1.60, 1.90, edge=AMBER, lw=1.3)
    label(ax, g2_x, 5.08, "Gerbang Masuk (Input)", size=8.5, color=AMBER, weight="bold")
    label(ax, g2_x, 4.68, r"$\sigma$", size=14.0, color=AMBER, weight="bold")
    label(ax, g2_x, 4.12, r"$i_t = \sigma\left(W_i [h_{t-1}, x_t] + b_i\right)$", size=8.0)
    label(ax, g2_x, 3.70, "(Persamaan 2.7)", size=7.5, color=MUTED)

    arrow(ax, (g2_x, bus_y), (g2_x, 3.45), color=AMBER, lw=1.3)

    # --- Gate 3: Kandidat Status Sel (Candidate Cell State) ---
    g3_x = 7.80
    box(ax, 7.00, 3.45, 1.60, 1.90, edge=TEAL, lw=1.3)
    label(ax, g3_x, 5.08, "Kandidat Status Sel", size=8.5, color=TEAL, weight="bold")
    label(ax, g3_x, 4.68, r"$\tanh$", size=13.0, color=TEAL, weight="bold")
    label(ax, g3_x, 4.12, r"$\tilde{c}_t = \tanh\left(W_c [h_{t-1}, x_t] + b_c\right)$", size=7.8)
    label(ax, g3_x, 3.70, "(Persamaan 2.8)", size=7.5, color=MUTED)

    arrow(ax, (g3_x, bus_y), (g3_x, 3.45), color=TEAL, lw=1.3)

    # Pertemuan i_t dan \tilde{c}_t pada simpul perkalian elemen \odot
    mult_i_c_y = 5.80
    circle_op(ax, op2_x, mult_i_c_y, r"$\odot$", r=0.26, edge=AMBER, lw=1.3)
    arrow(ax, (g2_x, 5.35), (op2_x - 0.28, mult_i_c_y - 0.05), color=AMBER, lw=1.2, rad=0.08)
    label(ax, g2_x + 0.28, 5.62, r"$i_t$", size=9.0, color=AMBER, weight="bold")

    arrow(ax, (g3_x, 5.35), (op2_x + 0.28, mult_i_c_y - 0.05), color=TEAL, lw=1.2, rad=-0.08)
    label(ax, g3_x - 0.28, 5.62, r"$\tilde{c}_t$", size=9.0, color=TEAL, weight="bold")

    # Hasil perkalian (i_t \odot \tilde{c}_t) naik ke op2 (+) pada jalan tol c
    arrow(ax, (op2_x, mult_i_c_y + 0.28), (op2_x, cy - 0.32), color=NAVY, lw=1.4)
    label(ax, op2_x + 0.45, 6.22, r"$i_t \odot \tilde{c}_t$", size=8.5, color=NAVY)

    # --- Gate 4: Gerbang Keluar (Output Gate) ---
    g4_x = 9.40
    box(ax, 8.60, 3.45, 1.60, 1.90, edge=PURPLE, lw=1.3)
    label(ax, g4_x, 5.08, "Gerbang Keluar (Output)", size=8.5, color=PURPLE, weight="bold")
    label(ax, g4_x, 4.68, r"$\sigma$", size=14.0, color=PURPLE, weight="bold")
    label(ax, g4_x, 4.12, r"$o_t = \sigma\left(W_o [h_{t-1}, x_t] + b_o\right)$", size=8.0)
    label(ax, g4_x, 3.70, "(Persamaan 2.10)", size=7.5, color=MUTED)

    arrow(ax, (g4_x, bus_y), (g4_x, 3.45), color=PURPLE, lw=1.3)

    # =========================================================================
    # 4. STATUS TERSEMBUNYI h_t DAN KELUARAN MODEL
    # =========================================================================
    # Jalur c_t turun ke blok aktivasi \tanh(c_t)
    tanh_c_y = 4.40
    box(ax, split_c_x - 0.50, tanh_c_y - 0.35, 1.00, 0.70, edge=GREEN, lw=1.3, face="#F0FFF4")
    label(ax, split_c_x, tanh_c_y, r"$\tanh$", size=13.0, color=GREEN, weight="bold")

    # Garis c_t turun ke tanh
    arrow(ax, (split_c_x, cy), (split_c_x, tanh_c_y + 0.38), color=GREEN, lw=1.3)
    label(ax, split_c_x + 0.28, 5.50, r"$c_t$", size=9.5, color=GREEN, weight="bold")

    # Simpul perkalian o_t \odot tanh(c_t)
    op_h_y = 2.45
    circle_op(ax, split_c_x, op_h_y, r"$\odot$", r=0.28, edge=GREEN, lw=1.4)

    # tanh(c_t) turun ke operator perkalian
    arrow(ax, (split_c_x, tanh_c_y - 0.38), (split_c_x, op_h_y + 0.32), color=GREEN, lw=1.3)

    # Output Gate (o_t) keluar dari sisi kanan Gate 4 (x=10.20, y=3.80) lalu turun ke simpul op_h_y
    ax.plot([10.20, 10.55, 10.55], [3.80, 3.80, op_h_y], color=PURPLE, lw=1.3, zorder=2)
    arrow(ax, (10.55, op_h_y), (split_c_x - 0.32, op_h_y), color=PURPLE, lw=1.3)
    label(ax, 10.35, 4.02, r"$o_t$", size=9.5, color=PURPLE, weight="bold")

    # Dari operator perkalian dihasilkan h_t (Persamaan 2.11)
    label(ax, split_c_x, op_h_y - 0.45, r"$h_t = o_t \odot \tanh(c_t)$", size=9.2, color=GREEN, weight="bold")

    # Titik cabang h_t (ke kanan keluar sel dan ke bawah ke lapisan prediksi)
    split_h_x = 12.00
    ax.plot([split_c_x + 0.32, split_h_x], [op_h_y, op_h_y], color=GREEN, lw=1.5, zorder=2)
    dot_h = Circle((split_h_x, op_h_y), 0.08, facecolor=GREEN, edgecolor=GREEN, zorder=4)
    ax.add_patch(dot_h)

    # 1. h_t keluar ke kanan (ke sel t+1)
    arrow(ax, (split_h_x, op_h_y), (12.75, op_h_y), color=GREEN, lw=1.5)
    box(ax, 12.80, op_h_y - 0.45, 1.25, 0.90, edge=GREEN, lw=1.3)
    label(ax, 13.425, op_h_y + 0.16, "Status Tersembunyi", size=7.8, color=GREEN, weight="bold")
    label(ax, 13.425, op_h_y - 0.18, r"$h_t$", size=12.0, weight="bold")

    # 2. h_t turun ke Lapisan Luaran Linier (Dense / Linear Projection)
    box(ax, 4.80, 0.70, 5.50, 0.95, edge=LINE, lw=1.3, face="#FFFFFF")
    label(ax, 7.55, 1.35, "Lapisan Luaran Linier (Dense Layer / Proyeksi Regresi Volatilitas)", size=8.5, color=INK, weight="bold")
    label(ax, 7.55, 0.95, r"$\hat{y}_{t+1} = \log RV_{t+1} = W_y \cdot h_t + b_y$", size=10.5, color=NAVY, weight="bold")

    # Garis dari split_h_x turun dan belok ke Lapisan Luaran Linier
    ax.plot([split_h_x, split_h_x, 10.35], [op_h_y, 1.15, 1.15], color=NAVY, lw=1.3, zorder=2)
    arrow(ax, (10.50, 1.15), (10.35, 1.15), color=NAVY, lw=1.3)
    label(ax, split_h_x + 0.22, 1.80, r"$h_t$", size=9.0, color=GREEN, weight="bold")

    # =========================================================================
    # 5. KETERANGAN LEGENDA NOTASI
    # =========================================================================
    label(
        ax, 0.20, 0.15,
        r"Notasi Matematis: $\sigma$ = fungsi aktivasi sigmoid $[0,1]$; $\tanh$ = tangen hiperbolik $[-1,1]$; $\odot$ = perkalian elemen (Hadamard product); $+$ = penjumlahan vektor; $[h_{t-1}, x_t]$ = konkatenasi vektor.",
        size=8.0, color=MUTED, ha="left"
    )

    out = FIG_DIR / "gambar_2_1_arsitektur_lstm.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Gambar 2.2
def gambar_2_2() -> Path:
    W, H = 12.0, 8.9
    fig, ax = canvas(W, H)

    x0, width = 0.25, 11.5
    band_h, gap = 1.42, 0.34
    top = H - 0.18

    stages = [
        (
            1,
            "Identifikasi masalah dan celah riset",
            MAROON,
            [
                "Volatilitas Bitcoin\n24/7 sangat ekstrem",
                "Prediksi harga gagal:\nmendekati random walk",
                "Model linear kaku,\nparameter statis",
                "Celah: tuning rawan\nleakage, metrik bias",
            ],
        ),
        (
            2,
            "Data historis dan rekayasa fitur",
            BLUE,
            [
                "2.464 hari kline 1 jam\nBTC/USDT (2020–2026)",
                "Target $\\log RV_{t+1}$ dari\n24 bar intra-hari",
                "6 fitur kausal tanpa\nlook-ahead bias",
                "Partisi 2020–2023 |\n2024–2025 | 2026",
            ],
        ),
        (
            3,
            "Pemodelan usulan dan baseline pembanding",
            PURPLE,
            [
                "Model usulan: LSTM + Optuna TPE\n(50 trial, 5-fold purged CV)",
                "Baseline: Persistence, HAR-RV,\nGARCH(1,1), LSTM untuned",
            ],
        ),
        (
            4,
            "Evaluasi akurasi dan inferensi statistik",
            TEAL,
            [
                "QLIKE (utama)\nMAE dan RMSE (pelengkap)",
                "Diebold-Mariano satu sisi\nkoreksi HAC Newey-West",
                "Moving-block bootstrap\n10.000 repetisi",
            ],
        ),
        (
            5,
            "Luaran ilmiah dan kesimpulan",
            GREEN,
            [
                "Jawaban RQ1–RQ3 dan pengujian H1–H3,\ndilaporkan apa adanya tanpa p-hacking",
            ],
        ),
    ]

    y = top - band_h
    centers = []
    for number, title, color, cards in stages:
        stage_band(ax, y, band_h, number, title, color, width=width, x0=x0)
        card_y = y + 0.18
        card_h = band_h - 0.62
        n = len(cards)
        inner_x0 = x0 + 0.30
        inner_w = width - 0.60
        card_gap = 0.16
        card_w = (inner_w - card_gap * (n - 1)) / n
        for i, text in enumerate(cards):
            cx = inner_x0 + i * (card_w + card_gap)
            chip(ax, cx, card_y, card_w, card_h, text, color)
        centers.append(y)
        y -= band_h + gap

    # Panah antartahap
    for upper, lower in zip(centers, centers[1:]):
        arrow(ax, (x0 + width / 2, upper - 0.02), (x0 + width / 2, lower + band_h + 0.02), lw=1.3)

    out = FIG_DIR / "gambar_2_2_kerangka_pemikiran.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Gambar 3.1
def gambar_3_1() -> Path:
    W, H = 12.0, 10.5
    fig, ax = canvas(W, H)

    x0, width = 0.25, 11.5
    band_h, gap = 1.26, 0.20
    top = H - 0.20

    stages = [
        (
            1,
            "Akuisisi dan audit kualitas data",
            BLUE,
            [
                "81 berkas kline 1 jam\nBinance Vision",
                "Audit 24 bar per hari UTC,\nAmandemen Data A1",
                "Kunci integritas SHA-256\n(2.464 hari final)",
            ],
        ),
        (
            2,
            "Rekayasa fitur dan target",
            GREEN,
            [
                r"RV harian 24 bar, target $\log RV_{t+1}$",
                "6 fitur kausal tanpa\nlook-ahead bias",
                "StandardScaler fit per fold\n(hanya data latih)",
            ],
        ),
        (
            3,
            "Partisi temporal kronologis",
            AMBER,
            [
                "Pengembangan 2020–2023\n(1.460 hari)",
                "Validasi internal 2024–2025\n(731 hari)",
                "Uji eksternal 2026\n(273 hari)",
            ],
        ),
        (
            4,
            "Optimasi hyperparameter Optuna",
            PURPLE,
            [
                "TPE, 50 trial terarah",
                "5-fold purged rolling-origin CV\ndengan gap lookback",
                "MedianPruner untuk\ntrial suboptimal",
            ],
        ),
        (
            5,
            "Pelatihan final dan baseline",
            MAROON,
            [
                "Refit train pool 2020–2025",
                "5-seed ensemble\n(42, 123, 2024, 7, 99)",
                "4 baseline pembanding",
            ],
        ),
        (
            6,
            "Evaluasi dan inferensi statistik",
            TEAL,
            [
                "QLIKE, MAE, RMSE",
                "Diebold-Mariano satu sisi,\nHAC lag 5",
                "Bootstrap blok 20,\n10.000 repetisi",
            ],
        ),
        (
            7,
            "Kesimpulan dan reproduksibilitas",
            NAVY,
            [
                "Jawaban RQ1–RQ3",
                "Pengujian H1–H3",
                "Provenance, hash, dan\nmanifest eksekusi",
            ],
        ),
    ]

    y = top - band_h
    centers = []
    for number, title, color, cards in stages:
        stage_band(ax, y, band_h, number, title, color, width=width, x0=x0)
        card_y = y + 0.14
        card_h = band_h - 0.66
        n = len(cards)
        inner_x0 = x0 + 0.30
        inner_w = width - 0.60
        card_gap = 0.16
        card_w = (inner_w - card_gap * (n - 1)) / n
        for i, text in enumerate(cards):
            cx = inner_x0 + i * (card_w + card_gap)
            chip(ax, cx, card_y, card_w, card_h, text, color, size=9.3)
        centers.append(y)
        y -= band_h + gap

    for upper, lower in zip(centers, centers[1:]):
        arrow(ax, (x0 + width / 2, upper - 0.02), (x0 + width / 2, lower + band_h + 0.02), lw=1.2)

    out = FIG_DIR / "gambar_3_1_alur_penelitian.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


if __name__ == "__main__":
    for path in (gambar_2_1(), gambar_2_2(), gambar_3_1()):
        print("wrote", path.relative_to(ROOT))
