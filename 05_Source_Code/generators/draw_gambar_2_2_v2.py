"""
Script generator Gambar 2.2 Kerangka Pemikiran Konseptual Penelitian (Versi Sempurna)
- Penomoran Tahap 1 s.d. 6 Sinkron 100% dengan Narasi Teks Naskah
- Keterangan disusun vertikal ke bawah (bullet points), tidak menyamping
- Bahasa jelas, lugas, dan mudah dimengerti penguji
- Decision Diamond & Feedback Loop (Umpan Balik) terhubung rapi
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

ROOT = Path(__file__).resolve().parents[2]
FIG_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "figures" / "gambar_2_2_kerangka_pemikiran.png"

# Setup font standar skripsi
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

def draw_diagram():
    # Dimensi kanvas proporsional (lebar x tinggi)
    fig, ax = plt.subplots(figsize=(11.0, 15.2))
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 15.2)
    ax.axis("off")

    # Palet Warna Elegan Akademis
    NAVY = "#1F3864"
    BLUE = "#2E5EAA"
    AMBER = "#B45309"
    RED = "#B91C1C"
    GREEN = "#15803D"
    TEXT_DARK = "#0F172A"
    TEXT_MUTED = "#334155"

    def draw_box(x, y, w, h, title, lines=None, edge=BLUE, face="#F8FAFC", title_color=NAVY):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.14",
            linewidth=1.4, edgecolor=edge, facecolor=face, zorder=2
        )
        ax.add_patch(patch)
        
        # Posisi Title
        if lines:
            title_y = y + h - 0.28
            ax.text(x + w/2, title_y, title, ha="center", va="center", fontsize=11, fontweight="bold", color=title_color, zorder=3)
            # Render lines secara vertikal ke bawah
            line_y = title_y - 0.28
            line_step = (h - 0.50) / len(lines)
            for l in lines:
                ax.text(x + 0.35, line_y, l, ha="left", va="center", fontsize=9.2, color=TEXT_MUTED, zorder=3)
                line_y -= line_step
        else:
            ax.text(x + w/2, y + h/2, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color=title_color, zorder=3)

    def draw_diamond(cx, cy, w, h, text, edge=AMBER, face="#FEF3C7", text_color="#92400E"):
        pts = [
            [cx, cy + h/2],
            [cx + w/2, cy],
            [cx, cy - h/2],
            [cx - w/2, cy]
        ]
        diamond = Polygon(pts, closed=True, edgecolor=edge, facecolor=face, linewidth=1.5, zorder=2)
        ax.add_patch(diamond)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=9.2, fontweight="bold", color=text_color, zorder=3, linespacing=1.2)

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

    # Judul Utama Diagram
    ax.text(5.5, 14.85, "KERANGKA PEMIKIRAN KONSEPTUAL PENELITIAN", ha="center", va="center", fontsize=13.5, fontweight="bold", color=NAVY)

    # -------------------------------------------------------------
    # TAHAP 1: Identifikasi Masalah & Target
    # -------------------------------------------------------------
    draw_box(1.0, 13.40, 9.0, 1.15,
             "1. Identifikasi Masalah dan Perumusan Target Peramalan",
             lines=[
                 "• Masalah: Fluktuasi ekstrem Bitcoin & ketidakmampuan model linier menangkap volatilitas non-linear.",
                 "• Target Prediksi: Log proksi Realized Volatility harian satu hari ke depan (t+1) berbasis data intrahari."
             ])

    # -------------------------------------------------------------
    # TAHAP 2: Pengumpulan & Pra-pemrosesan Data
    # -------------------------------------------------------------
    draw_box(1.0, 11.80, 9.0, 1.25,
             "2. Pengumpulan dan Pra-pemrosesan Data Frekuensi Tinggi",
             lines=[
                 "• Sumber Data: Transaksi SPOT BTC/USDT kline 1 jam Binance Vision (1 Jan 2020 – 30 Sep 2026).",
                 "• Audit Integritas: Filter data cacat (hanya hari dengan ≥ 20 bar yang dipertahankan).",
                 "• Rekayasa 6 Fitur Kausal: log RV, RV lag-5, RV lag-22, return harian, Parkinson, dan Garman-Klass."
             ])

    # -------------------------------------------------------------
    # TAHAP 3: Partisi Deret Waktu Kronologis
    # -------------------------------------------------------------
    draw_box(1.0, 9.95, 9.0, 1.50,
             "3. Partisi Deret Waktu dan Pengendalian Kebocoran Data",
             lines=[
                 "• Data Pengembangan (2020–2023 / 1.460 hari): Digunakan untuk penalaan hyperparameter (HPO).",
                 "• Train Pool (2020–2025 / 2.191 hari): Digunakan untuk pelatihan model final (90% fit, 10% early stopping).",
                 "• Data Evaluasi Temporal (2026 / 273 hari)*: Pengujian generalisasi kinerja model di masa depan.",
                 "• Purge Gap = lookback + 1 hari: Penyangga ketat untuk memutus autokorelasi serial antar-sampel."
             ])

    # -------------------------------------------------------------
    # TAHAP 4: Pemodelan (Model Usulan vs Baseline)
    # -------------------------------------------------------------
    # Header Sub-tahap
    ax.text(5.5, 9.60, "4. Penalaan Hyperparameter (Optuna TPE) dan Model Pembanding", ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)

    # Box Kiri: Model Usulan LSTM + Optuna
    draw_box(0.8, 7.80, 4.6, 1.55,
             "Model Usulan: LSTM + Optuna TPE",
             lines=[
                 "• Algoritma: Bayesian TPE (Tree-structured Parzen)",
                 "• Search Space: Lookback (5–30), Units (16–128),",
                 "  Dropout (0.0–0.4), Learning Rate (1e-4–1e-2).",
                 "• Validasi: 5-Fold Purged Rolling-Origin CV (50 trial).",
                 "• Fungsi Objektif: Minimasi loss asimetris QLIKE."
             ],
             edge="#1E3A8A", face="#EFF6FF", title_color="#1E3A8A")

    # Box Kanan: Model Baseline Pembanding
    draw_box(5.8, 7.80, 4.4, 1.55,
             "Model Pembanding (Baselines)",
             lines=[
                 "• Pembanding Primer:",
                 "  1. Random Walk Persistence (Naïve Benchmark)",
                 "  2. Heterogeneous Autoregressive (HAR-RV)",
                 "• Pembanding Sekunder:",
                 "  3. Generalized Autoregressive (GARCH(1,1))",
                 "  4. Long Short-Term Memory tanpa talaan (Untuned)"
             ],
             edge="#475569", face="#F1F5F9", title_color="#334155")

    # Decision Diamond (Pengecekan Validasi di bawah Model Usulan)
    draw_diamond(3.1, 5.85, 3.8, 1.35,
                 "Apakah Kriteria Validasi\n& Konvergensi Terpenuhi?\n(Early Stopping & Minimasi QLIKE)")

    # Box Feedback Loop (Umpan Balik)
    draw_box(0.3, 4.35, 2.3, 0.95,
             "Umpan Balik (Loop)",
             lines=[
                 "• Perbarui Model Parzen",
                 "• Eksplorasi Parameter Baru"
             ],
             edge=RED, face="#FEF2F2", title_color=RED)

    # -------------------------------------------------------------
    # TAHAP 5: Pelatihan Model Final
    # -------------------------------------------------------------
    draw_box(5.2, 5.25, 5.0, 1.20,
             "5. Pelatihan Model Final pada Train Pool (2020–2025)",
             lines=[
                 "• Arsitektur: Konfigurasi hyperparameter terbaik hasil Optuna.",
                 "• Pembagian Data: 90% Pelatihan Fit (1.972 hari) dan",
                 "  10% Validasi Internal Early Stopping (219 hari).",
                 "• Pelatihan mandiri tanpa refit pada periode evaluasi 2026."
             ],
             edge=GREEN, face="#F0FDF4", title_color=GREEN)

    # -------------------------------------------------------------
    # TAHAP 6: Evaluasi & Uji Hipotesis Statistik
    # -------------------------------------------------------------
    draw_box(1.0, 1.80, 9.0, 1.95,
             "6. Evaluasi Kinerja (2026) dan Uji Hipotesis Statistik (H0 vs H1)",
             lines=[
                 "• Data Pengujian: Periode Evaluasi Temporal 2026 (273 observasi harian valid).",
                 "• Evaluasi Kerugian: Metrik Asimetris QLIKE (Primer) serta metrik simetris MAE dan RMSE (Sekunder).",
                 "• Uji Inferensial Primer: Uji Diebold–Mariano satu sisi dengan estimasi HAC Newey–West (α = 0,05).",
                 "• Uji Robustness: Stationary Moving-Block Bootstrap 95% Confidence Interval (< 0).",
                 "• Keputusan Statistik: Penolakan Hipotesis Nol (H0) dan Penerimaan Hipotesis Alternatif (H1) secara formal."
             ],
             edge="#1E3A8A", face="#EEF2FF", title_color="#1E3A8A")

    # Catatan Kaki Metodologis
    ax.text(1.0, 1.25,
            "* Catatan Keterbatasan Paparan: Karena sebagian periode 2026 pernah ditinjau pada analisis eksplorasi awal, hasil pengujian\n  secara metodologis ditafsirkan sebagai evaluasi temporal terisolasi, bukan holdout eksternal yang murni independen.",
            fontsize=8.5, color="#64748B", style="italic", va="top")

    # -------------------------------------------------------------
    # PANAH ALUR DIAGRAM
    # -------------------------------------------------------------
    # 1 -> 2
    draw_arrow(5.5, 13.40, 5.5, 13.05)
    # 2 -> 3
    draw_arrow(5.5, 11.80, 5.5, 11.45)
    # 3 -> 4 (Header)
    draw_arrow(5.5, 9.95, 5.5, 9.75)
    
    # 4 -> Cabang ke Kiri (LSTM) dan Kanan (Baselines)
    draw_arrow(4.0, 9.45, 3.1, 9.35)
    draw_arrow(7.0, 9.45, 8.0, 9.35)

    # Model Usulan -> Decision Diamond
    draw_arrow(3.1, 7.80, 3.1, 6.55)

    # Decision Diamond -> TIDAK (Feedback Loop)
    draw_arrow(1.2, 5.85, 1.2, 5.30, color=RED, lw=1.4)
    ax.text(1.05, 6.00, "TIDAK\n(Belum Konvergen)", ha="right", va="center", fontsize=8.5, fontweight="bold", color=RED)
    
    # Loop box -> Kembali memutar ke HPO Optuna
    draw_arrow(0.8, 5.30, 0.8, 8.50, color=RED, lw=1.3, ls="--", rad=-0.2)
    draw_arrow(0.8, 8.50, 0.8, 8.50, color=RED, lw=1.3)
    ax.text(0.18, 7.00, "Feedback Loop:\nTala Ulang HPO", ha="left", va="center", fontsize=8.5, color=RED, style="italic")

    # Decision Diamond -> YA (Lanjut ke Pelatihan Final)
    draw_arrow(5.0, 5.85, 5.2, 5.85, color=GREEN, lw=1.4)
    ax.text(4.45, 6.05, "YA (Optimal)", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=GREEN)

    # Pelatihan Final -> Tahap 6
    draw_arrow(7.7, 5.25, 7.7, 3.75)

    # Baselines -> Tahap 6
    draw_arrow(8.0, 7.80, 8.0, 3.75)

    plt.tight_layout()
    fig.savefig(FIG_PATH, dpi=300)
    plt.close(fig)
    print(f"[OK] Gambar 2.2 berhasil diperbarui di: {FIG_PATH}")

if __name__ == "__main__":
    draw_diagram()
