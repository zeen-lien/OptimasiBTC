"""Update KODE_DIAGRAM_DRAWIO.md with new Gambar 2.2 Mermaid code."""
import re

mermaid_22 = """## 2. GAMBAR 2.2: KERANGKA PEMIKIRAN PENELITIAN (DENGAN DECISION DIAMOND & FEEDBACK LOOP)
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

    A["<b>1. Identifikasi Masalah & Perumusan Target</b><br/>• Masalah: Fluktuasi ekstrem Bitcoin & keterbatasan model linier konvensional<br/>• Target: Log proksi Realized Volatility harian satu hari ke depan (t+1)"]:::stageBox

    B["<b>2. Akuisisi & Pra-pemrosesan Data</b><br/>• Sumber: Binance Vision SPOT BTC/USDT kline 1 jam (1 Jan 2020 – 30 Sep 2026)<br/>• Rekayasa 6 Fitur Kausal (log RV, RV lag-5, RV lag-22, return, Parkinson, Garman-Klass)"]:::stageBox

    C["<b>3. Partisi Waktu Kronologis & Pengendalian Kebocoran Data</b><br/>• Data Pengembangan (2020–2023) | Train Pool (2020–2025) | Evaluasi Temporal (2026)*<br/>• Purge Gap = lookback + 1 untuk memutus autokorelasi serial"]:::stageBox

    subgraph Pemodelan ["<b>Tahap Penalaan & Pelatihan Model</b>"]
        D1["<b>Model Usulan: LSTM + Optuna TPE</b><br/>• Optimasi Bayesian TPE (50 trial)<br/>• 5-fold Purged Rolling-Origin CV<br/>• Fungsi Kerugian: Asimetris QLIKE"]:::stageBox
        D2["<b>Model Pembanding (Baselines)</b><br/>• Primer: Persistence & HAR-RV<br/>• Sekunder: GARCH(1,1) & LSTM Untuned<br/>• Tanpa refit pada evaluasi temporal"]:::stageBox
    end

    DECISION{"<b>Apakah Kriteria Validasi<br/>& Konvergensi Terpenuhi?</b><br/>(Loss QLIKE Minimum & Konvergen)"}:::decision

    LOOP["<b>Mekanisme Umpan Balik (Feedback Loop):</b><br/>• Penyesuaian Ruang Pencarian Hyperparameter<br/>• Pembaruan Distribusi Probabilitas Parzen (TPE)<br/>• Talaan Ulang Bobot & Arsitektur LSTM"]:::loopBox

    FINAL["<b>Pelatihan Model Final LSTM Terpilih</b><br/>• Dilatih pada Train Pool 2020–2025 (90% fit, 10% early stopping)<br/>• Menggunakan konfigurasi hyperparameter terbaik"]:::successBox

    E["<b>4. Pengujian Kinerja pada Periode Evaluasi Temporal 2026*</b><br/>• Evaluasi performa generalisasi model pada 273 observasi valid tahun 2026<br/>• Metrik Primer: Asimetris QLIKE | Metrik Sekunder: MAE & RMSE"]:::stageBox

    F["<b>5. Uji Statistik Inferensial & Pengujian Hipotesis (H0 vs H1)</b><br/>• Uji Diebold–Mariano satu sisi dengan koreksi HAC Newey–West (α = 0,05)<br/>• Uji Ketahanan: Stationary Moving-Block Bootstrap 95% CI (< 0)<br/>• Keputusan Statistik: Penerimaan H1 (Keunggulan signifikan model usulan)"]:::stageBox

    N["* Keterbatasan Paparan: Karena sebagian periode 2026 pernah ditinjau pada analisis awal, hasil ditafsirkan sebagai evaluasi temporal terisolasi dengan keterbatasan paparan historis tersebut, bukan pure unseen external holdout."]:::note

    %% Alur Panah
    A --> B
    B --> C
    C --> D1
    C --> D2
    D1 --> DECISION
    DECISION -- "<b>TIDAK</b><br/>(Belum Optimal / Overfit)" --> LOOP
    LOOP --> D1
    DECISION -- "<b>YA</b><br/>(Konvergen & Optimal)" --> FINAL
    FINAL --> E
    D2 --> E
    E --> F
    F -.-> N
```
"""

path = "03_Naskah_Skripsi/study2/figures/KODE_DIAGRAM_DRAWIO.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"## 2\. GAMBAR 2\.2:.*?(?=## 3\.|\Z)"
new_text = re.sub(pattern, mermaid_22 + "\n\n---\n\n", text, flags=re.DOTALL)
with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("[OK] KODE_DIAGRAM_DRAWIO.md updated successfully.")
