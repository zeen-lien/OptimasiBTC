# 🎓 Skripsi: Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.14-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.18%2B-orange.svg)](https://tensorflow.org/)
[![Optuna](https://img.shields.io/badge/Optuna-5.0.0-blueviolet.svg)](https://optuna.org/)
[![Status](https://img.shields.io/badge/Status-100%25%20Completed%20%26%20Verified-brightgreen.svg)]()
[![Campus](https://img.shields.io/badge/UNISNU-Fakultas%20Sains%20%26%20Teknologi-darkgreen.svg)](https://unisnu.ac.id)

Repositori ini memuat seluruh artefak komputasi, pipeline eksperimen, naskah akademik (BAB I s.d. BAB V), dan berkas dokumen master utuh untuk Skripsi Sarjana Komputer (S.Kom.) Program Studi Teknik Informatika, Fakultas Sains dan Teknologi, **Universitas Islam Nahdlatul Ulama (UNISNU) Jepara**.

---

## 👤 Informasi Mahasiswa & Proyek
* **Nama Penulis:** Zaini Leon Musthofa Kamal
* **Nomor Induk Mahasiswa (NIM):** 231240001455
* **Program Studi:** S1 Teknik Informatika
* **Fakultas / Instansi:** Fakultas Sains dan Teknologi, Universitas Islam Nahdlatul Ulama (UNISNU) Jepara
* **Dosen Pembimbing:** Teguh Tamrin, S.Kom., M.Kom. (NIDN: 0620127603 / NIY: 4 761220 17 235)
* **Ketua Program Studi TI:** Gentur Wahyu Nyipto Wibowo, S.Kom., M.Kom. (NIDN: 0623117902 / NIY: 4 791123 19 255)
* **Dekan FST:** Dr. Arif Mustofa, S.T., M.Si. (NIY: 3 730617 13 124 / NIDN: 0617067302)
* **Tahun Penyelesaian:** 2026
* **Judul Skripsi Resmi:**  
  *Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin* (12 kata)

---

## 🌟 Ringkasan Eksekutif & Temuan Empiris

Penelitian ini memecahkan kelemahan metode penalaan *trial-and-error* manual dan pencarian konvensional (*Grid/Random Search*) pada model *Deep Learning* peramalan harga Bitcoin. Dengan mengintegrasikan algoritma Bayesian Optimization berbasis **Tree-structured Parzen Estimator (TPE)** dan mekanisme pemangkasan **MedianPruner** (Optuna 50 trials) dengan skema validasi **Time-Series Split 5-fold**, model yang diusulkan (**Tier 3**) terbukti menghasilkan akurasi superior pada data uji *out-of-sample holdout* (439 hari: Oktober 2024 – Desember 2025):

| Tingkatan Model (*Tier*) | Konfigurasi Hyperparameter Optimal | RMSE (USD) | MAE (USD) | MAPE (%) | Kategori Akurasi |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Tier 1 (Baseline Default)** | Lookback: 30, Units: 50, Dropout: 0.20, LR: 0.001, Batch: 32 | $2.947,60 | $2.378,56 | 2,36% | Sangat Baik |
| **Tier 2 (Manual Khumaidi dkk., 2024)** | Lookback: 60, Units: 128, Dropout: 0.20, LR: 0.001, Batch: 10 | $3.904,15 | $3.182,86 | 3,16% | Sangat Baik |
| **Tier 3 (Optuna-TPE Usulan)** | **Lookback: 22, Units: 100, Dropout: 0.10, LR: 0.00197 + Scheduler, Batch: 16 (MAE Loss)** | **$2.338,22** | **$1.784,27** | **1,81%** | **Sangat Baik (Juara Mutlak)** |

### 🚀 Persentase Peningkatan Performa (*Positive Improvement*):
* **Tier 3 vs. Tier 2 (Replikasi Khumaidi dkk., SINTA 2 - Rujukan Utama):**
  * Penurunan RMSE: **+40,11%** (turun dari $3.904,15 ke $2.338,22)
  * Penurunan MAE: **+43,94%** (turun dari $3.182,86 ke $1.784,27)
  * Penurunan MAPE: **+42,72%** (turun dari 3,16% ke 1,81%)
* **Tier 3 vs. Tier 1 (Baseline Default Kontrol):**
  * Penurunan RMSE: **+20,67%** (turun dari $2.947,60 ke $2.338,22)
  * Penurunan MAE: **+24,99%** (turun dari $2.378,56 ke $1.784,27)
  * Penurunan MAPE: **+23,31%** (turun dari 2,36% ke 1,81%)
  * *Hasil:* Tier 3 adalah **Juara Umum Mutlak** yang mengungguli seluruh model pembanding!

---

## 💡 Kebaruan Ilmiah (*Novelty*) & Kontribusi Utama
1. **Otomasi Ruang Pencarian Non-Konveks Multidimensi:** Menggantikan penalaan manual rentan bias dengan pemodelan probabilistik $P(x|y)$ rasio Parzen Estimator, menghemat biaya komputasi tanpa mengorbankan kedalaman eksplorasi parameter.
2. **Protokol Validasi Deret Waktu Anti-Bocor (*No Data Leakage*):** Menerapkan normalisasi skalar tunggal *Min-Max fit* hanya pada data latih *in-sample*, dipadukan dengan *Walk-Forward Time-Series Split*, menjamin model tidak pernah melihat masa depan (*lookahead bias*).
3. **Penemuan Ilmiah *Momentum Lag* & Domain-Guided HPO:** Membuktikan secara empiris bahwa penentuan jendela historis harus berlandaskan *Adaptive Market Hypothesis* (Lo, 2004) dan dinamika *Cell State* LSTM (Fischer & Krauss, 2018). Jendela historis teroptimasi (**22 hari**) mengungguli jendela panjang konvensional (**60 hari**) yang menderita *momentum drag* saat volatilitas tinggi.
4. **Pembuktian Fenomena *Overfitting* pada Model Terdahulu:** Mengungkap bahwa konfigurasi unit besar (128) dan batch kecil (10) pada model manual Khumaidi dkk. (2024) memicu osilasi gradien liar yang gagal menggeneralisasi pada rezim pasar baru (*regime shift*).

---

## 📁 Struktur Lengkap Direktori Proyek

```text
jurnal/
├── README.md                                            # Ringkasan proyek & panduan eksekusi
├── LAPORAN_LENGKAP_EKSEKUTIF_DAN_PANDUAN_SIDANG.md     # Buku putih & dossier pembelaan sidang munaqasyah
│
├── 01_Panduan_Kampus/
│   ├── panduan-skripsi.docx                             # Pedoman resmi UNISNU (SK Rektor 57/PR/UNISNU/V/2023)
│   └── file contoh pengajuan judul.docx                 # Template pengajuan judul FST UNISNU
│
├── 02_Pengajuan_Judul/
│   └── Proposal_Skripsi_Optimasi_LSTM_Optuna_Zaini.docx # Outline proposal resmi siap diajukan
│
├── 03_Naskah_Skripsi/
│   ├── SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx      # MASTER NASKAH LENGKAP (Cover s.d. Lampiran, 1.08 MB)
│   ├── BAB_1_PENDAHULUAN_ZAINI_LEON.docx                # Naskah Bab 1 (Latar Belakang, Masalah, SPECH)
│   ├── BAB_2_LANDASAN_TEORI_ZAINI_LEON.docx             # Naskah Bab 2 (7 Paper Terdahulu, LSTM, Optuna, OMML)
│   ├── BAB_3_METODE_PENELITIAN_ZAINI_LEON.docx          # Naskah Bab 3 (3-Tier Pipeline, 5 Tabel, OMML)
│   ├── BAB_4_HASIL_DAN_PEMBAHASAN_ZAINI_LEON.docx       # Naskah Bab 4 (5 Tabel, 3 Gambar 300 DPI, Pembahasan)
│   └── BAB_5_PENUTUP_ZAINI_LEON.docx                    # Naskah Bab 5 (Simpulan A.1-A.5 & Saran B.1-B.3)
│
├── 04_Referensi_Ilmiah/
│   ├── DAFTAR_32_REFERENSI_SKRIPSI.md                   # Katalog 32 referensi APA 7th & pemetaan bab
│   ├── Referensi_Utama/                                 # 10 Paper PDF Utama (SINTA 1, 2, Scopus Q1)
│   └── Referensi_Tambahan/                              # 21 Paper PDF Seminal & Teori Fundamental
│
└── 05_Source_Code/
    ├── data/
    │   ├── raw/BTCUSDT_daily_2020_2025.csv              # 2.192 data transaksi harian Binance API
    │   └── processed/                                   # Partisi 80:20 & file data terskala
    ├── extracted_logo/
    │   └── img_3.png                                    # Logo resmi UNISNU Jepara beresolusi tinggi
    ├── generators/                                      # Skrip Python perakit naskah Word & OMML
    │   ├── generate_front_matter.py                     # Pembuat Cover, Abstrak, Pengesahan, TOC
    │   ├── generate_bab1.py s.d. generate_bab5.py       # Pembuat naskah bab 1-5 dengan formula SPECH
    │   ├── generate_back_matter.py                      # Pembuat Daftar Pustaka (32 Ref) & Lampiran 1-3
    │   ├── generate_master_skripsi.py                   # Master assembler penggabung seluruh naskah
    │   └── verify_full_skripsi.py                       # Skrip audit validator kelengkapan format naskah
    ├── model_experiment/                                # Pipeline komputasi eksperimen Machine Learning
    │   ├── 01_fetch_binance_data.py                     # REST API collector (2020-2025)
    │   ├── 02_preprocessing.py                          # Partisi kronologis & MinMax anti-leakage
    │   ├── 03_train_baseline_tier1.py                   # Pelatihan Baseline Default Tier 1
    │   ├── 04_train_manual_tier2.py                     # Replikasi Manual Khumaidi dkk. Tier 2
    │   ├── 05_optimize_optuna_tier3.py                  # Optimasi Bayesian TPE 50 trials Tier 3
    │   └── 06_evaluate_and_compare.py                   # Evaluasi komparatif metrik & grafik 300 DPI
    └── results/
        ├── figures/                                     # 3 Gambar grafik akademik 300 DPI (Bab 4)
        ├── metrics/                                     # JSON metrik evaluasi Tier 1, 2, 3
        ├── optuna_trials_history.csv                    # Log riwayat lengkap 50 trials Optuna
        └── benchmark_comparison_summary.json            # Ringkasan kuantitatif komparasi final
```

---

## 🛠️ Panduan Menjalankan Kode Eksperimen (*Reproduction Guide*)

### 1. Persiapan Lingkungan (*Virtual Environment*)
Pastikan Python 3.10 atau versi di atasnya telah terinstal pada sistem:
```bash
# Masuk ke direktori proyek
cd d:/OneDrive/Desktop/jurnal

# Instalasi paket pustaka yang dibutuhkan
pip install tensorflow optuna scikit-learn pandas numpy matplotlib requests python-docx docxcompose pillow
```

### 2. Menjalankan Pipeline Eksperimen (Urut dari Tahap 1 s.d. 6)
```bash
# Tahap 1: Mengunduh data historis Binance BTC/USDT (2020-2025)
python 05_Source_Code/model_experiment/01_fetch_binance_data.py

# Tahap 2: Pra-pemrosesan data bebas kebocoran (Train-Test Split 80:20)
python 05_Source_Code/model_experiment/02_preprocessing.py

# Tahap 3: Melatih Model Baseline Default (Tier 1)
python 05_Source_Code/model_experiment/03_train_baseline_tier1.py

# Tahap 4: Melatih Model Manual Tuning Khumaidi dkk. (Tier 2)
python 05_Source_Code/model_experiment/04_train_manual_tier2.py

# Tahap 5: Menjalankan Optimasi Bayesian Optuna-TPE 50 Trials (Tier 3)
python 05_Source_Code/model_experiment/05_optimize_optuna_tier3.py

# Tahap 6: Evaluasi Komparatif & Pembuatan Grafik Visualisasi 300 DPI
python 05_Source_Code/model_experiment/06_evaluate_and_compare.py
```

### 3. Kompilasi & Audit Dokumen Master Skripsi (.docx)
Untuk membangun ulang berkas master skripsi dari awal secara otomatis:
```bash
# Merakit seluruh bagian skripsi menjadi Master Dokumen
python 05_Source_Code/generators/generate_master_skripsi.py

# Menjalankan audit verifikasi standar akademik (SPECH, OMML, Halaman, Tabel, Gambar)
python 05_Source_Code/generators/verify_full_skripsi.py
```

---

## 📑 Spesifikasi Kepatuhan Standar Akademik UNISNU Jepara
* **Format Paragraf:** Formula **SPECH** (*State, Premise/Problem, Evidence/Explanation, Citation, Hook*) dengan rentang ketat **100 – 140 kata/paragraf** (terbukti bebas plagiasi Turnitin).
* **Tipografi & Margin:** Times New Roman 12pt, spasi 1.5, *first-line indent* 1.0 cm, perataan rata kanan-kiri (*Justified*), Margin 4 cm (Top), 4 cm (Left), 3 cm (Bottom), 3 cm (Right) pada kertas A4.
* **Notasi Matematika:** **100% Native Microsoft Word OMML** (`<m:oMath>` / `<m:oMathPara>`) tanpa ada raw delimiter `$` yang tertinggal.
* **Penomoran Halaman (*Multi-Section*):** 
  * Bagian Awal (*Front Matter*): Angka Romawi kecil (`i, ii, iii...`).
  * Bagian Isi (*Main Body & Back Matter*): Angka Arab (`1, 2, 3...`) berlanjut hingga Lampiran 3.
* **Sitasi & Referensi:** 32 referensi kredibel terindeks SINTA 1, 2, Scopus Q1, dan seminar internasional terkemuka, disusun berdasarkan pedoman **APA 7th Edition**.

---
*Dikelola dengan penuh tanggung jawab akademik oleh **Zaini Leon Musthofa Kamal (231240001455)** — Teknik Informatika UNISNU Jepara.*
