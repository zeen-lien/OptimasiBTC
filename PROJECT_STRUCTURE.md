# PROJECT STRUCTURE - Skripsi Volatilitas Bitcoin (Study 2)

Repositori ini difokuskan penuh pada **Study 2**: *Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Prediksi Volatilitas Bitcoin*. Seluruh artefak historis dari **Study 1** (prediksi tingkat harga) telah dipindahkan dan disimpan secara aman di direktori `archive/study1/`.

---

## 1. Peta Direktori Utama

```
jurnal/
├── 01_Panduan_Kampus/        # Pedoman skripsi & template resmi FST UNISNU Jepara
├── 02_Pengajuan_Judul/       # Berkas pengajuan judul Study 2 (MD & DOCX)
├── 03_Naskah_Skripsi/        # Naskah akademik Study 2 (Bab 1–5 Markdown & draft DOCX)
│   └── study2/
├── 04_Referensi_Ilmiah/      # 33 PDF aktif terverifikasi + 4 arsip; 0 referensi via akses kampus
├── 05_Source_Code/           # Kode, data, dan hasil eksperimen Study 2
│   ├── data/study2/          # Data Realized Volatility harian (2020–2026) & manifest SHA-256
│   ├── generators/           # Skrip kompilasi naskah Study 2 ke format DOCX standar UNISNU
│   ├── results/study2/       # Hasil HPO Optuna, final run, metrik, dan figur Bab 4
│   └── study2_volatility/    # Modul aktif peramalan volatilitas (Bahasa Indonesia & tag bab)
├── archive/
│   └── study1/               # Seluruh kode, data, naskah, dan tes Study 1 (prediksi harga)
├── docs/                     # Protokol pre-registered, audit numerik, matriks gap & keterlacakan
├── references/               # Paket bibliografi Mendeley (RIS, BibTeX, matriks 36 paper, panduan)
├── release/                  # Arsip rilis historis
├── tests/                    # 34 unit test sintetis & validasi kontrak Study 2 (100% PASS)
├── PROJECT_STRUCTURE.md      # Peta struktur repositori aktif
├── README.md                 # Dokumentasi utama proyek skripsi
├── requirements.txt          # Dependensi Python
└── pytest.ini                # Konfigurasi pengujian pytest
```

---

## 2. Struktur Modul & Naskah Study 2 (Aktif)

| Kebutuhan Akademik | Berkas / Direktori Sumber | Deskripsi |
|---|---|---|
| **Pengajuan Judul** | `02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2.md` | Formulir resmi pengajuan judul, latar belakang, rumusan masalah, hipotesis, dan metodologi ringkas. |
| **SEMPRO (Bab 1–3)** | `03_Naskah_Skripsi/study2/BAB_1_PENDAHULUAN.md`<br>`03_Naskah_Skripsi/study2/BAB_2_LANDASAN_TEORI.md`<br>`03_Naskah_Skripsi/study2/BAB_3_METODE_PENELITIAN.md` | Fondasi teoretis (RV, GARCH, HAR-RV, LSTM, Optuna, QLIKE), perancangan data Binance Vision 1 jam, dan protokol evaluasi bebas bocor. |
| **SEMHAS (Bab 4–5)** | `03_Naskah_Skripsi/study2/BAB_4_HASIL_DAN_PEMBAHASAN.md`<br>`03_Naskah_Skripsi/study2/BAB_5_PENUTUP.md`<br>`03_Naskah_Skripsi/study2/DAFTAR_REFERENSI_STUDY2.md` | Analisis hasil empiris: QLIKE out-of-sample 2026, uji Diebold-Mariano, moving-block bootstrap, interpretasi hasil mixed, dan kontribusi ilmiah. |
| **Naskah Lengkap (DOCX)** | `03_Naskah_Skripsi/study2/SKRIPSI_STUDY2_DRAFT.docx` | Draf naskah gabungan Bab 1–5 berformat UNISNU (Margins 4-4-3-3, TNR 12 pt, 1.5 spasi). |
| **Koleksi Mendeley** | `references/study2_references.ris`<br>`references/study2_references.bib`<br>`references/README_MENDELEY.md` | Berkas siap impor ke Mendeley Reference Manager / Mendeley Desktop (36 entri), beserta 33 PDF lokal terverifikasi. |

---

## 3. Modul Komputasi (`05_Source_Code/study2_volatility/`)

Seluruh kode aktif telah diberi komentar bahasa Indonesia dan tag keterlacakan bab skripsi `[BAB 3 §3.x]` dan `[BAB 4 §4.x]`:

- `s2_config.py`: Definisi parameter path, split temporal (2020-2023 dev, 2024-2025 val, 2026 test), dan hyperparameter baseline.
- `s2_data.py`: Pengunduhan kline 1 jam Binance Vision, agregasi realized variance harian UTC, dan pembersihan amandemen A1.
- `s2_models.py`: Arsitektur LSTM vanilla TensorFlow/Keras, baseline HAR-RV (OLS), GARCH(1,1) rolling origin, dan Naive Persistence.
- `s2_stats.py`: Perhitungan kerugian asimetris QLIKE, uji signifikansi Diebold-Mariano dengan estimasi HAC Newey-West, dan Moving-Block Bootstrap.
- `s2_optuna_search.py`: Optimasi hyperparameter Optuna (TPE Sampler & MedianPruner) berbasis 5-fold Purged TimeSeriesSplit.
- `s2_final_run.py`: Runner evaluasi final multi-seed (5 seed acak) pada data uji eksternal 2026; status paparan operasional dibahas di Bab IV.
- `s2_analyze.py`: Validasi integritas metrik, penyusunan tabel komparasi, dan verifikasi alignment tanggal target.
- `s2_figures.py`: Pembuatan figur ilmiah Bab IV dari hasil eksperimen.
- `s2_runlog.py`: Pencatatan provenance, hash, versi pustaka, dan jejak audit eksekusi.

---

## 4. Lokasi Arsip Historis Study 1 (`archive/study1/`)

Semua artefak yang terkait dengan eksperimen awal prediksi harga penutupan Bitcoin telah diamankan pada:
- `archive/study1/02_Pengajuan_Judul/`
- `archive/study1/03_Naskah_Skripsi/`
- `archive/study1/04_Referensi_Ilmiah/`
- `archive/study1/05_Source_Code/` (berisi `model_experiment/`, `models/`, `data/raw/`, `data/processed/`, `results/`, `generators/`)
- `archive/study1/docs/`
- `archive/study1/tests/`
