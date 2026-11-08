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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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


# ---------------------------------------------------------------- Gambar 2.1
def gambar_2_1() -> Path:
    W, H = 12.0, 7.4
    fig, ax = canvas(W, H)

    # Kolom masukan
    box(ax, 0.25, 1.15, 1.85, 5.55, edge=BLUE, lw=1.2)
    label(ax, 1.175, 6.18, "Masukan pada\nwaktu $t$", size=10.5, color=BLUE, weight="bold")
    label(ax, 1.175, 5.13, r"$x_t$", size=12.5)
    label(ax, 1.175, 4.72, "(6 fitur kausal)", size=8.8, color=MUTED)
    label(ax, 1.175, 3.15, r"$h_{t-1}$", size=12.5)
    label(ax, 1.175, 1.92, r"$c_{t-1}$", size=12.5)

    # Kartu gerbang
    gates = [
        ("Gerbang lupa (forget gate)", r"$f_t=\sigma\left(W_f\,[h_{t-1},x_t]+b_f\right)$", 5.55, MAROON),
        ("Gerbang masuk (input gate)", r"$i_t=\sigma\left(W_i\,[h_{t-1},x_t]+b_i\right)$", 4.15, AMBER),
        ("Kandidat status sel", r"$\tilde{c}_t=\tanh\left(W_c\,[h_{t-1},x_t]+b_c\right)$", 2.75, TEAL),
        ("Gerbang keluar (output gate)", r"$o_t=\sigma\left(W_o\,[h_{t-1},x_t]+b_o\right)$", 1.35, PURPLE),
    ]
    gx, gw, gh = 2.95, 4.75, 1.12
    for title, eq, y, color in gates:
        box(ax, gx, y, gw, gh, edge=color, lw=1.2)
        label(ax, gx + gw / 2, y + gh - 0.26, title, size=9.6, color=color, weight="bold")
        label(ax, gx + gw / 2, y + 0.38, eq, size=11.3)

    # Kartu hasil
    box(ax, 8.55, 4.35, 3.2, 1.35, edge=NAVY, lw=1.3)
    label(ax, 10.15, 5.42, "Pembaruan status sel", size=9.8, color=NAVY, weight="bold")
    label(ax, 10.15, 4.83, r"$c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t$", size=11.8)

    box(ax, 8.55, 2.35, 3.2, 1.35, edge=GREEN, lw=1.3)
    label(ax, 10.15, 3.42, "Status tersembunyi", size=9.8, color=GREEN, weight="bold")
    label(ax, 10.15, 2.83, r"$h_t=o_t\odot\tanh\left(c_t\right)$", size=11.8)

    box(ax, 8.55, 0.55, 3.2, 0.95, edge=LINE, lw=1.0, face="#F5F7FA")
    label(ax, 10.15, 1.02, r"Keluaran linear: $\hat{y}_{t+1}=\log RV_{t+1}$", size=10.4)

    # Aliran masukan ke gerbang
    for _, _, y, _ in gates:
        arrow(ax, (2.10, y + gh / 2), (gx, y + gh / 2), rad=0.0)

    # Gerbang ke hasil
    arrow(ax, (gx + gw, 6.11), (8.55, 5.35), rad=-0.08, color=MAROON)
    arrow(ax, (gx + gw, 4.71), (8.55, 4.95), rad=0.04, color=AMBER)
    arrow(ax, (gx + gw, 3.31), (8.55, 4.62), rad=0.10, color=TEAL)
    arrow(ax, (gx + gw, 1.91), (8.55, 3.20), rad=0.12, color=PURPLE)

    # c_{t-1} dirutekan di atas gerbang menuju kartu status sel
    ax.plot([1.175, 1.175, 10.15], [6.70, 7.02, 7.02], color=NAVY, lw=1.0, zorder=1)
    arrow(ax, (10.15, 7.02), (10.15, 5.72), color=NAVY, lw=1.0)

    # c_t -> h_t
    arrow(ax, (10.15, 4.35), (10.15, 3.70), color=NAVY)
    arrow(ax, (10.15, 2.35), (10.15, 1.50), color=GREEN)

    label(ax, 0.28, 0.36, r"$\sigma$ = sigmoid; $\tanh$ = tangen hiperbolik; $\odot$ = perkalian elemen; $[\,\cdot\,,\,\cdot\,]$ = konkatenasi vektor",
          size=8.4, color=MUTED, ha="left")

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
