"""Update KODE_DIAGRAM_DRAWIO.md with exact 6-stage vertical Mermaid diagram."""
from pathlib import Path
import re

MD_PATH = Path("03_Naskah_Skripsi/study2/figures/KODE_DIAGRAM_DRAWIO.md")
text = MD_PATH.read_text(encoding="utf-8")

mermaid_22 = """## 2. GAMBAR 2.2: KERANGKA PEMIKIRAN PENELITIAN (VERSI VERTIKAL 6 TAHAP SINKRON 1:1)
* **File Target:** `03_Naskah_Skripsi/study2/figures/gambar_2_2_kerangka_pemikiran.png`
* **Penempatan Naskah:** Bab II Sub-bab H (Kerangka Pemikiran)

```mermaid
flowchart TD
    %% Styling Global
    classDef default font-family:'Segoe UI',Arial,sans-serif,font-size:12px;
    classDef stageBox fill:#F8FAFC,stroke:#1E3A8A,stroke-width:2px,color:#0F172A,rx:6px,ry:6px;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#92400E,rx:4px,ry:4px;
    classDef loopBox fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#991B1B,rx:6px,ry:6px;
    classDef successBox fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#14532D,rx:6px,ry:6px;
    classDef note fill:none,stroke:none,color:#64748B,font-size:11px,text-align:left;

    A["<b>1. Identifikasi Masalah dan Perumusan Target Peramalan</b><br/>• Masalah: Fluktuasi ekstrem Bitcoin & ketidakmampuan model linier menangkap volatilitas non-linear.<br/>• Target Prediksi: Log proksi Realized Volatility harian satu hari ke depan (t+1) berbasis data intrahari."]:::stageBox

    B["<b>2. Pengumpulan dan Pra-pemrosesan Data Frekuensi Tinggi</b><br/>• Sumber Data: Transaksi SPOT BTC/USDT kline 1 jam Binance Vision (1 Jan 2020 – 30 Sep 2026).<br/>• Audit Integritas: Filter data cacat (hanya hari dengan ≥ 20 bar yang dipertahankan).<br/>• Rekayasa 6 Fitur Kausal: log RV, RV lag-5, RV lag-22, return harian, Parkinson, dan Garman-Klass."]:::stageBox

    C["<b>3. Partisi Deret Waktu dan Pengendalian Kebocoran Data</b><br/>• Data Pengembangan (2020–2023 / 1.460 hari): Digunakan untuk penalaan hyperparameter (HPO).<br/>• Train Pool (2020–2025 / 2.191 hari): Digunakan untuk pelatihan model final.<br/>• Data Evaluasi Temporal (2026 / 273 hari)*: Pengujian generalisasi kinerja model di masa depan.<br/>• Purge Gap = lookback + 1 hari: Penyangga ketat untuk memutus autokorelasi serial antar-sampel."]:::stageBox

    subgraph Tahap4 ["<b>4. Penalaan Hyperparameter (Optuna TPE) dan Model Pembanding</b>"]
        D1["<b>Model Usulan: LSTM + Optuna TPE</b><br/>• Algoritma: Bayesian TPE (Tree-structured Parzen)<br/>• Search Space: Lookback (5–30), Units (16–128),<br/>  Dropout (0.0–0.4), Learning Rate (1e-4–1e-2).<br/>• Validasi: 5-Fold Purged Rolling-Origin CV (50 trial).<br/>• Fungsi Objektif: Minimasi loss asimetris QLIKE."]:::stageBox
        D2["<b>Model Pembanding (Baselines)</b><br/>• Pembanding Primer:<br/>  1. Random Walk Persistence (Naïve Benchmark)<br/>  2. Heterogeneous Autoregressive (HAR-RV)<br/>• Pembanding Sekunder:<br/>  3. Generalized Autoregressive (GARCH(1,1))<br/>  4. Long Short-Term Memory tanpa talaan (Untuned)"]:::stageBox
    end

    DECISION{"<b>Apakah Kriteria Validasi<br/>& Konvergensi Terpenuhi?</b><br/>(Early Stopping & Minimasi QLIKE)"}:::decision

    LOOP["<b>Mekanisme Umpan Balik (Feedback Loop):</b><br/>• Perbarui Model Probabilitas Parzen<br/>• Eksplorasi Kombinasi Parameter Baru<br/>• Talaan Ulang Arsitektur LSTM"]:::loopBox

    FINAL["<b>5. Pelatihan Model Final pada Train Pool (2020–2025)</b><br/>• Arsitektur: Konfigurasi hyperparameter terbaik hasil Optuna.<br/>• Pembagian Data: 90% Pelatihan Fit (1.972 hari) dan<br/>  10% Validasi Internal Early Stopping (219 hari).<br/>• Pelatihan mandiri tanpa refit pada periode evaluasi 2026."]:::successBox

    E["<b>6. Evaluasi Kinerja (2026) dan Uji Hipotesis Statistik (H0 vs H1)</b><br/>• Data Pengujian: Periode Evaluasi Temporal 2026 (273 observasi harian valid).<br/>• Evaluasi Kerugian: Metrik Asimetris QLIKE (Primer) serta metrik simetris MAE dan RMSE (Sekunder).<br/>• Uji Inferensial Primer: Uji Diebold–Mariano satu sisi dengan estimasi HAC Newey–West (α = 0,05).<br/>• Uji Robustness: Stationary Moving-Block Bootstrap 95% Confidence Interval (&lt; 0).<br/>• Keputusan Statistik: Penolakan Hipotesis Nol (H0) dan Penerimaan Hipotesis Alternatif (H1) secara formal."]:::stageBox

    N["* Catatan Keterbatasan Paparan: Karena sebagian periode 2026 pernah ditinjau pada analisis eksplorasi awal, hasil pengujian secara metodologis ditafsirkan sebagai evaluasi temporal terisolasi, bukan holdout eksternal yang murni independen."]:::note

    %% Alur Panah
    A --> B
    B --> C
    C --> D1
    C --> D2
    D1 --> DECISION
    DECISION -- "<b>TIDAK</b><br/>(Belum Konvergen)" --> LOOP
    LOOP --> D1
    DECISION -- "<b>YA</b><br/>(Optimal)" --> FINAL
    FINAL --> E
    D2 --> E
    E -.-> N
```
"""

pattern = r"## 2\. GAMBAR 2\.2:.*?(?=## 3\.|\Z)"
text = re.sub(pattern, mermaid_22 + "\n\n---\n\n", text, flags=re.DOTALL)
MD_PATH.write_text(text, encoding="utf-8")
print("[OK] KODE_DIAGRAM_DRAWIO.md updated.")
