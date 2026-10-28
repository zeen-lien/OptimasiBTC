# 🎓 Skripsi: Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin

[![Python Version](https://img.shields.io/badge/Python-3.14.7-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.22.0rc0-orange.svg)](https://tensorflow.org/)
[![Optuna](https://img.shields.io/badge/Optuna-5.0.0-blueviolet.svg)](https://optuna.org/)
[![Status](https://img.shields.io/badge/Status-Fase%201--6%20selesai%20%7C%20Fase%207%20rilis-brightgreen.svg)]()
[![Campus](https://img.shields.io/badge/UNISNU-Fakultas%20Sains%20%26%20Teknologi-darkgreen.svg)](https://unisnu.ac.id)

Repositori ini memuat seluruh artefak komputasi, pipeline eksperimen, naskah akademik (BAB I s.d. BAB V), dan berkas dokumen master utuh untuk Skripsi Sarjana Komputer (S.Kom.) Program Studi Teknik Informatika, Fakultas Sains dan Teknologi, **Universitas Islam Nahdlatul Ulama (UNISNU) Jepara**.

> **Status hasil:** seluruh angka final berasal dari run `final_matrix_20261025` dan diterbitkan ke `05_Source_Code/results/summary_final.json`. Ringkasan audit angka yang dapat ditelusuri per field berada di `docs/NUMBER_AUDIT.md`; audit referensi ada di `docs/REFERENCE_AUDIT.md`; prosedur dan status reproduksi ada di `docs/REPRODUCTION_REPORT.md`. Angka pra-perbaikan di `archive/pre_perbaikan_20261025/` dibekukan dan **tidak boleh** dipakai sebagai klaim final.
>
> **Hasil utama (jujur):** persistence tetap unggul pada MAE (1.579,80 USD). Model usulan E7 mencapai MAE 1.687,49 USD dan **secara statistik lebih buruk** daripada persistence (selisih berpasangan +107,69 USD; CI 95% +50,82 s.d. +170,90 USD). E6 adalah LSTM terbaik (MAE 1.667,26 USD), tetapi juga tidak mengalahkan persistence. Kontribusi penelitian adalah pipeline evaluasi terkontrol dan pelaporan hasil negatif yang terverifikasi.
>
> **Study 2 (branch `study2-volatility`, aktif):** arah baru — peramalan **realized volatility harian Bitcoin** dari kline 1h (target `log_rv`), HPO Optuna leakage-free, test eksternal 2026-01-01..2026-09-30. Protokol pre-registered ber-hash (`docs/STUDY2_PROTOCOL.md`, SHA-256 `72c75880…ba3`), data dibekukan (`05_Source_Code/data/study2/`), endpoint QLIKE vs persistence & HAR-RV. Timeline provenance: `docs/STUDY2_PROVENANCE.md`. Study 1 pada `v1.0-final` tidak diubah.

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

## 🌟 Ringkasan Eksekutif & Desain Bukti

Penelitian ini mengevaluasi optimasi hyperparameter LSTM berbasis **Tree-structured Parzen Estimator (TPE)** dan **MedianPruner** Optuna dengan protokol yang memisahkan data tuning dari data uji. Seluruh model diuji pada **439 hari holdout** (19 Oktober 2024 – 31 Desember 2025), sedangkan **1.753 observasi in-sample** dipakai untuk pelatihan, validasi silang berpurge, dan pemilihan hyperparameter. Data tidak diacak, scaler di-fit ulang pada setiap fold, dan purge gap disetel sebesar lookback untuk mencegah kebocoran temporal.

Matriks eksperimen terkontrol E0–E7 memisahkan empat pertanyaan yang sering tercampur dalam klaim optimasi:

| Run | Perlakuan | Peran |
| :--- | :--- | :--- |
| **E0** | Persistence (harga besok = harga hari ini) | Baseline naif; ambang minimum |
| **E1** | Tier 1 default (MSE, tanpa scheduler) | Kontrol default |
| **E2** | Tier 2 manual Khumaidi dkk. (MSE, tanpa scheduler) | Rujukan literatur |
| **E3** | Parameter Tier 3 acuan (MSE, tanpa scheduler) | Referensi ablasi |
| **E4** | Parameter Tier 3 acuan (MAE, tanpa scheduler) | Isolasi efek loss |
| **E5** | Parameter Tier 3 acuan (MSE, ReduceLROnPlateau) | Isolasi efek scheduler |
| **E6** | Parameter Tier 3 acuan (MAE, ReduceLROnPlateau) | Efek gabungan loss + scheduler |
| **E7** | HPO penuh Optuna-TPE (MAE, ReduceLROnPlateau) | Model usulan |

MAE adalah metrik utama karena langsung terbaca dalam USD. Sebuah model baru disebut lebih baik hanya jika MAE titiknya lebih rendah **dan** interval kepercayaan 95% dari selisih berpasangan tidak melewati nol. RMSE, MAPE, variabilitas lima seed (`42, 123, 2024, 7, 99`), analisis residual, rezim pasar, dan akurasi arah dilaporkan sebagai pemeriksaan pendukung. Jika E7 tidak mengalahkan persistence, hasil negatif dilaporkan apa adanya dan kontribusi digeser ke pipeline evaluasi yang terkontrol.

**Hasil holdout seed utama (439 hari):**

| Run | RMSE (USD) | MAE (USD) | MAPE (%) | MAE multi-seed (mean ± std) |
| :--- | ---: | ---: | ---: | ---: |
| **E0** Persistence | 2.167,24 | **1.579,80** | 1,62 | — |
| E1 Tier 1 default | 2.519,46 | 1.968,00 | 1,98 | 2.058,81 ± 196,57 |
| E2 Tier 2 manual | 3.491,05 | 2.892,27 | 2,87 | 3.048,39 ± 399,48 |
| E3 Tier 3 MSE, no scheduler | 2.994,73 | 2.452,53 | 2,43 | 2.281,38 ± 163,11 |
| E4 Tier 3 MAE, no scheduler | 2.328,70 | 1.763,47 | 1,79 | 1.790,80 ± 167,39 |
| E5 Tier 3 MSE, plateau | 2.591,70 | 2.043,10 | 2,05 | 2.116,59 ± 78,61 |
| E6 Tier 3 MAE, plateau | 2.234,46 | 1.667,26 | 1,70 | 1.712,07 ± 67,48 |
| **E7** Full Optuna HPO | 2.250,06 | 1.687,49 | 1,72 | 1.756,11 ± 89,97 |

**Verdict otomatis:** `proposed_not_better_than_persistence`. Selisih MAE E7 − persistence = +107,69 USD (6,82% lebih buruk), CI 95% +50,82 s.d. +170,90 USD, seluruhnya di atas nol. E7 juga lebih buruk daripada E6 (selisih +20,23 USD; CI +1,22 s.d. +40,37 USD).

**Sumber angka tunggal:** `05_Source_Code/results/summary_final.json` (diterbitkan oleh `08_analyze_results.py --publish`). **Audit angka:** `docs/NUMBER_AUDIT.md` (dihasilkan oleh `build_number_audit.py`). **Protokol beku:** `docs/PROTOCOL.md` (hash diverifikasi oleh publish gate).

---

## 💡 Kebaruan Ilmiah (*Novelty*) & Kontribusi Utama
1. **Matriks eksperimen E0–E7 yang memisahkan efek:** HPO penuh (E7 vs E6), hyperparameter hasil pencarian (E1 vs E3), fungsi kerugian (E4 vs E3), scheduler (E5 vs E3), dan efek gabungan (E6 vs E3) diuji pada tanggal holdout yang sama dengan lima seed.
2. **Protokol evaluasi bebas kebocoran:** Purged Time-Series Split dengan scaler per fold, holdout terkunci, moving-block bootstrap 7 hari, dan perbandingan berpasangan pada tanggal yang identik.
3. **Baseline naif sebagai ambang klaim:** Persistence, drift, dan seasonal naive dihitung secara kausal sebelum model LSTM dibandingkan, sehingga klaim tidak bergantung pada baseline yang lemah.
4. **Pelaporan hasil negatif yang terverifikasi:** Verdict ilmiah ditentukan otomatis dari data dan ditolak oleh publish gate bila run parsial, seed tidak lengkap, atau hash protokol berubah.

---

## 📁 Struktur Lengkap Direktori Proyek

```text
jurnal/
├── README.md                                            # Ringkasan proyek & panduan eksekusi
├── LAPORAN_LENGKAP_EKSEKUTIF_DAN_PANDUAN_SIDANG.md     # ARSIP HISTORIS — memuat angka lama; jangan dipakai
├── TODOFUTURES.MD                                       # Rencana kerja & status per fase
├── docs/
│   ├── PROTOCOL.md                                      # Protokol evaluasi beku (hash diverifikasi)
│   ├── DECISIONS.md                                     # Keputusan ilmiah D1–D14
│   ├── NUMBER_AUDIT.md                                  # Pemetaan angka naskah → summary_final.json
│   ├── REFERENCE_AUDIT.md                               # Audit 32 referensi & status PDF
│   ├── REPRODUCTION_REPORT.md                           # Lingkungan, hash, perintah, status reproduksi
│   └── DEFENSE_NOTES.md                                 # Bahan sidang & jawaban pertanyaan
│
├── 01_Panduan_Kampus/
│   ├── panduan-skripsi.docx                             # Pedoman resmi UNISNU (SK Rektor 57/PR/UNISNU/V/2023)
│   └── file contoh pengajuan judul.docx                 # Template pengajuan judul FST UNISNU
│
├── 02_Pengajuan_Judul/
│   └── Proposal_Skripsi_Optimasi_LSTM_Optuna_Zaini.docx # Outline proposal resmi siap diajukan
│
├── 03_Naskah_Skripsi/
│   ├── SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx      # MASTER NASKAH LENGKAP (Cover s.d. Lampiran, 1,18 MB)
│   ├── BAB_1_PENDAHULUAN_ZAINI_LEON.docx                # Naskah Bab 1 (Latar Belakang, Masalah, SPECH)
│   ├── BAB_2_LANDASAN_TEORI_ZAINI_LEON.docx             # Naskah Bab 2 (32 referensi, LSTM, Optuna, OMML)
│   ├── BAB_3_METODE_PENELITIAN_ZAINI_LEON.docx          # Naskah Bab 3 (protokol, matriks E0–E7, OMML)
│   ├── BAB_4_HASIL_DAN_PEMBAHASAN_ZAINI_LEON.docx       # Naskah Bab 4 (7 Tabel, 5 Gambar, verdict otomatis)
│   └── BAB_5_PENUTUP_ZAINI_LEON.docx                    # Naskah Bab 5 (simpulan berbasis hasil final)
│
├── 04_Referensi_Ilmiah/
│   ├── DAFTAR_32_REFERENSI_SKRIPSI.md                   # Katalog 32 referensi APA 7th & pemetaan bab
│   ├── references_manifest.csv                          # Manifest metadata, DOI/URL, hash, status PDF
│   ├── Referensi_Utama/                                 # 8 PDF paper utama (SINTA/Scopus)
│   ├── Referensi_Tambahan/                              # 13 PDF paper seminal & teori fundamental
│   └── Arsip_Tambahan/                                  # 10 PDF latar belakang yang tidak dikutip
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
    │   ├── 05_optimize_optuna_tier3.py                  # Optimasi TPE 50 trials (E7)
    │   ├── 06_evaluate_and_compare.py                   # Evaluasi komparatif & grafik 300 DPI
    │   ├── 07_run_ablation.py                           # Runner ablasi E3–E6
    │   ├── 08_analyze_results.py                        # Analisis akhir, CI, publish gate
    │   ├── experiment_matrix.py                         # Orkestrator matriks E0–E7
    │   └── baselines.py                                 # Persistence, drift, seasonal naive
    └── results/
        ├── summary_final.json                           # Sumber angka tunggal (hasil publish)
        └── runs/{run_id}/                               # Artefak per run (metrik, figur, model, log)

release/final_20261026/                                  # Paket rilis: DOCX, PDF, kode, hash, README
```

**Dokumen audit yang perlu dibaca lebih dulu:**

| Dokumen | Isi |
| :--- | :--- |
| `docs/PROTOCOL.md` | Protokol evaluasi beku; hash `75f60620…66260` diverifikasi publish gate |
| `docs/DECISIONS.md` | 14 keputusan ilmiah beserta alasannya |
| `docs/NUMBER_AUDIT.md` | Setiap angka naskah dan sumber field-nya |
| `docs/REFERENCE_AUDIT.md` | 32 referensi: metadata, PDF, hash, dan hasil audit sitasi |
| `docs/REPRODUCTION_REPORT.md` | Environment, hash, perintah, hasil verifikasi, dan clean-room yang ditunda |
| `docs/DEFENSE_NOTES.md` | Ringkasan angka, limitations, dan antisipasi pertanyaan sidang |

---

## 🛠️ Panduan Menjalankan Kode Eksperimen (*Reproduction Guide*)

### 1. Persiapan Lingkungan (*Virtual Environment*)
Environment yang terverifikasi: **Python 3.14.7 + TensorFlow 2.22.0rc0**. TensorFlow tersebut masih pra-rilis; sebelum submit, putuskan bersama pembimbing apakah memakai pasangan Python/TensorFlow stabil. Versi lengkap ada di `requirements.txt`.
```bash
# Jalankan dari root repositori
pip install -r requirements.txt
```

### 2. Menjalankan Pipeline Eksperimen
Satu perintah menjalankan seluruh tahap dan menyimpan semua artefak baru ke `05_Source_Code/results/runs/{run_id}/` agar hasil lama tidak tertimpa:
```bash
# Pipeline lengkap (50 trial Optuna)
python 05_Source_Code/model_experiment/run_pipeline.py --all --trials 50

# Uji cepat offline dengan data mentah yang sudah ada
python 05_Source_Code/model_experiment/run_pipeline.py --all --reuse-data --trials 1 --epochs 1

# Atau satu stage tertentu
python 05_Source_Code/model_experiment/run_pipeline.py --stage data --reuse-data
python 05_Source_Code/model_experiment/run_pipeline.py --stage baseline --run-id <run_id>
python 05_Source_Code/model_experiment/run_pipeline.py --stage eval --run-id <run_id>
```

Matriks eksperimen terkontrol E0–E7 dijalankan terpisah karena E7 melakukan HPO penuh:
```bash
# Lihat definisi dan hipotesis
python 05_Source_Code/model_experiment/experiment_matrix.py --list

# Uji mekanika cepat (bukan bukti ilmiah)
python 05_Source_Code/model_experiment/experiment_matrix.py \
  --run-id matrix_smoke --only E0,E3,E4 --seeds 42 --epochs 1

# Run final semua eksperimen dengan 5 seed, lalu analisis + publish summary
python 05_Source_Code/model_experiment/experiment_matrix.py \
  --run-id final_matrix_20261025 --seeds 42,123,2024,7,99 \
  --trials 50 --epochs 100 --screening-epochs 25 --cv-splits 5 \
  --patience 12 --analyze --publish
```

`08_analyze_results.py` juga bisa dijalankan terpisah:
```bash
python 05_Source_Code/model_experiment/08_analyze_results.py \
  --run-id final_matrix_20261025 --publish
```

Setiap run menghasilkan `manifest.json`, `config.json`, `env.json`, `git_commit.txt`, `data_hash.txt`, metrik, prediksi, figure, model, dan log. Gunakan `--legacy` hanya jika memang ingin menimpa artefak lama.

### 3. Kompilasi, Audit, dan Verifikasi Dokumen Master (.docx)
Satu perintah membangun ulang seluruh naskah, menjalankan verifier, dan mengaudit sitasi:
```bash
python 05_Source_Code/generators/generate_all.py
```

Perintah terpisah bila diperlukan:
```bash
# Merakit seluruh bagian skripsi menjadi Master Dokumen
python 05_Source_Code/generators/generate_master_skripsi.py

# Audit verifikasi standar akademik (SPECH, OMML, halaman, tabel, gambar, angka)
python 05_Source_Code/generators/verify_full_skripsi.py

# Audit dua arah: 32 referensi ↔ sitasi dalam naskah
python 05_Source_Code/generators/audit_citations.py

# Seluruh test
python -m pytest -q
```

### 4. Ekspor PDF dan Paket Rilis
PDF final diekspor dari Word ke `release/final_20261026/`. Hash SHA256 seluruh artefak rilis dicatat di `release/final_20261026/HASHES_SHA256.txt`; petunjuk reproduksi ada di `release/final_20261026/README_RELEASE.md`.

---

## 📑 Spesifikasi Kepatuhan Standar Akademik UNISNU Jepara
* **Format Paragraf:** Formula **SPECH** (*State, Premise/Problem, Evidence/Explanation, Citation, Hook*) dengan rentang **100 – 140 kata/paragraf**; kepatuhan diverifikasi oleh `verify_full_skripsi.py`.
* **Tipografi & Margin:** Times New Roman 12pt, spasi 1.5, *first-line indent* 1.0 cm, perataan rata kanan-kiri (*Justified*), Margin 4 cm (Top), 4 cm (Left), 3 cm (Bottom), 3 cm (Right) pada kertas A4.
* **Notasi Matematika:** **100% Native Microsoft Word OMML** (`<m:oMath>` / `<m:oMathPara>`) tanpa ada raw delimiter `$` yang tertinggal.
* **Penomoran Halaman (*Multi-Section*):** 
  * Bagian Awal (*Front Matter*): Angka Romawi kecil (`i, ii, iii...`).
  * Bagian Isi (*Main Body & Back Matter*): Angka Arab (`1, 2, 3...`) berlanjut hingga Lampiran 3.
* **Sitasi & Referensi:** 32 referensi kredibel terindeks SINTA/Scopus dan sumber resmi, disusun menurut **APA 7th Edition**; seluruh sitasi dan referensi diaudit dua arah.
* **Catatan eksternal:** pemeriksaan Turnitin dan persetujuan pembimbing belum dapat diverifikasi dari repositori ini dan tidak diklaim sebagai selesai.

---
*Dikelola dengan penuh tanggung jawab akademik oleh **Zaini Leon Musthofa Kamal (231240001455)** — Teknik Informatika UNISNU Jepara.*
