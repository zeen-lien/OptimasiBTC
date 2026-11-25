"""
Script untuk menghasilkan Gambar 2.2 Kerangka Pemikiran Konseptual Penelitian
dengan Decision Diamond dan Feedback Loop (Umpan Balik) saat validasi belum optimal.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

ROOT = Path(__file__).resolve().parents[2]
FIG_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "figures" / "gambar_2_2_kerangka_pemikiran.png"

# Setup font
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10.5,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

def draw_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 12.8))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 12.8)
    ax.axis("off")

    # Colors
    NAVY = "#1F3864"
    BLUE = "#2E5EAA"
    AMBER = "#B45309"
    RED = "#B91C1C"
    GREEN = "#15803D"
    BG_BOX = "#F8FAFC"
    BORDER = "#1E3A8A"

    def draw_box(x, y, w, h, title, subtitle="", edge=BORDER, face="#F8FAFC", title_color=NAVY):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            linewidth=1.4, edgecolor=edge, facecolor=face, zorder=2
        )
        ax.add_patch(patch)
        if subtitle:
            ax.text(x + w/2, y + h*0.64, title, ha="center", va="center", fontsize=11, fontweight="bold", color=title_color, zorder=3)
            ax.text(x + w/2, y + h*0.30, subtitle, ha="center", va="center", fontsize=9.5, color="#334155", zorder=3, linespacing=1.25)
        else:
            ax.text(x + w/2, y + h*0.50, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color=title_color, zorder=3)

    def draw_diamond(cx, cy, w, h, text, edge=AMBER, face="#FEF3C7", text_color="#92400E"):
        pts = [
            [cx, cy + h/2],
            [cx + w/2, cy],
            [cx, cy - h/2],
            [cx - w/2, cy]
        ]
        diamond = Polygon(pts, closed=True, edgecolor=edge, facecolor=face, linewidth=1.5, zorder=2)
        ax.add_patch(diamond)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=9.5, fontweight="bold", color=text_color, zorder=3, linespacing=1.2)

    def draw_arrow(x1, y1, x2, y2, color="#475569", lw=1.3, style="-|>", rad=0.0, ls="-"):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style,
            mutation_scale=12,
            linewidth=lw,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=ls,
            zorder=4
        ))

    # Judul Header Diagram
    ax.text(5.25, 12.45, "KERANGKA PEMIKIRAN KONSEPTUAL PENELITIAN", ha="center", va="center", fontsize=13, fontweight="bold", color=NAVY)

    # 1. Masalah & Tujuan
    draw_box(1.2, 11.15, 8.1, 0.95,
             "1. Identifikasi Masalah & Perumusan Target Peramalan",
             "Masalah: Fluktuasi ekstrem Bitcoin & keterbatasan model linier konvensional\nTarget: Log proksi Realized Volatility harian satu hari ke depan (t+1)")

    # 2. Akuisisi & Pra-pemrosesan Data
    draw_box(1.2, 9.75, 8.1, 0.95,
             "2. Akuisisi & Pra-pemrosesan Data Frekuensi Tinggi",
             "Sumber: Binance Vision SPOT BTC/USDT kline 1 jam (1 Jan 2020 – 30 Sep 2026)\nRekayasa 6 Fitur Kausal (log RV, RV lag-5, RV lag-22, return, Parkinson, Garman-Klass)")

    # 3. Partisi Waktu Kronologis
    draw_box(1.2, 8.35, 8.1, 0.95,
             "3. Partisi Deret Waktu Kronologis & Pengendalian Kebocoran Data",
             "Data Pengembangan (2020–2023) | Train Pool (2020–2025) | Evaluasi Temporal (2026)*\nPurge Gap = lookback + 1 untuk memutus autokorelasi serial antar-sampel")

    # 4. HPO Optuna TPE (Dua Kolom: Model Usulan vs Pembanding)
    draw_box(0.7, 6.75, 4.6, 1.15,
             "Model Usulan: LSTM + Optuna TPE",
             "• Penalaan Bayesian TPE (50 trial)\n• 5-fold Purged Rolling-Origin CV\n• Fungsi Kerugian: Asimetris QLIKE",
             edge="#1E3A8A", face="#EFF6FF", title_color="#1E3A8A")

    draw_box(5.7, 6.75, 4.1, 1.15,
             "Model Pembanding (Baselines)",
             "• Primer: Persistence & HAR-RV\n• Sekunder: GARCH(1,1) & LSTM Untuned\n• Tanpa refit pada evaluasi temporal",
             edge="#475569", face="#F1F5F9", title_color="#334155")

    # 5. Decision Diamond: Apakah Kriteria Validasi Terpenuhi?
    draw_diamond(3.0, 5.05, 3.8, 1.25,
                 "Apakah Kriteria Validasi\n& Konvergensi Terpenuhi?\n(Loss QLIKE Minimum & Konvergen)")

    # Box Umpan Balik (Feedback Loop)
    draw_box(0.3, 3.80, 2.4, 0.85,
             "Umpan Balik (Loop)",
             "Tala Ulang Parameter\nUpdate Probabilitas TPE",
             edge=RED, face="#FEF2F2", title_color=RED)

    # 6. Pelatihan Model Final
    draw_box(5.0, 4.55, 4.8, 0.95,
             "Pelatihan Final Model LSTM Terpilih",
             "Dilatih pada Train Pool 2020–2025 (90% fit, 10% early stopping)\nMenggunakan arsitektur hyperparameter terbaik hasil penalaan",
             edge=GREEN, face="#F0FDF4", title_color=GREEN)

    # 7. Pengujian pada Evaluasi Temporal 2026
    draw_box(1.2, 2.95, 8.1, 0.95,
             "4. Pengujian Kinerja pada Periode Evaluasi Temporal 2026*",
             "Evaluasi performa generalisasi model pada 273 observasi valid tahun 2026\nMetrik Primer: QLIKE (penalti asimetris) | Metrik Sekunder: MAE & RMSE")

    # 8. Inferensi Statistik & Uji Hipotesis (H0 vs H1)
    draw_box(1.2, 1.45, 8.1, 1.05,
             "5. Uji Statistik Inferensial & Pengujian Hipotesis (H0 vs H1)",
             "• Uji Diebold–Mariano satu sisi dengan estimasi HAC Newey–West (α = 0,05)\n• Stationary Moving-Block Bootstrap 95% Confidence Interval (< 0)\n• Penarikan kesimpulan ilmiah penerimaan H1 (keunggulan signifikan)",
             edge="#1E3A8A", face="#EEF2FF", title_color="#1E3A8A")

    # Catatan Kaki Metodologis
    ax.text(1.2, 0.90,
            "* Catatan Keterbatasan: Karena sebagian data 2026 pernah ditinjau pada analisis awal, hasil ditafsirkan sebagai\n  evaluasi temporal terisolasi dengan keterbatasan paparan historis tersebut, bukan pure unseen external holdout.",
            fontsize=8.5, color="#64748B", style="italic", va="top")

    # PANAH PENGHUBUNG ALUR
    # 1 -> 2
    draw_arrow(5.25, 11.15, 5.25, 10.70)
    # 2 -> 3
    draw_arrow(5.25, 9.75, 5.25, 9.30)
    # 3 -> 4 (Cabang ke LSTM dan ke Baselines)
    draw_arrow(4.0, 8.35, 3.0, 7.90)
    draw_arrow(6.5, 8.35, 7.5, 7.90)

    # 4 (LSTM) -> Decision Diamond
    draw_arrow(3.0, 6.75, 3.0, 5.70)

    # Decision Diamond -> TIDAK (Feedback Loop)
    draw_arrow(1.1, 5.05, 1.1, 4.65, color=RED, lw=1.4)
    ax.text(0.9, 5.20, "TIDAK\n(Belum Optimal)", ha="right", va="center", fontsize=8.5, fontweight="bold", color=RED)
    
    # Loop box -> Kembali ke HPO Optuna
    draw_arrow(0.7, 4.65, 0.7, 7.30, color=RED, lw=1.3, ls="--", rad=-0.2)
    draw_arrow(0.7, 7.30, 0.7, 7.30, color=RED, lw=1.3) # hook
    # Label loop
    ax.text(0.15, 6.0, "Feedback Loop:\nEksplorasi Ruang\nParameter Baru", ha="left", va="center", fontsize=8.5, color=RED, style="italic")

    # Decision Diamond -> YA (Lanjut ke Pelatihan Final)
    draw_arrow(4.9, 5.05, 5.0, 5.05, color=GREEN, lw=1.4)
    ax.text(4.4, 5.30, "YA (Konvergen)", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=GREEN)

    # Baselines -> Pengujian 2026
    draw_arrow(7.75, 6.75, 7.75, 3.90)

    # Pelatihan Final -> Pengujian 2026
    draw_arrow(7.4, 4.55, 6.5, 3.90)

    # Pengujian 2026 -> Uji Inferensial (H0 vs H1)
    draw_arrow(5.25, 2.95, 5.25, 2.50)

    plt.tight_layout()
    fig.savefig(FIG_PATH, dpi=300)
    plt.close(fig)
    print(f"[OK] Gambar 2.2 berhasil diperbarui di: {FIG_PATH}")

if __name__ == "__main__":
    draw_diagram()
