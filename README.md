# 🎓 Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Prediksi Volatilitas Bitcoin

[![Python Version](https://img.shields.io/badge/Python-3.14.7-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.22.0rc0-orange.svg)](https://tensorflow.org/)
[![Optuna](https://img.shields.io/badge/Optuna-5.0.0-blueviolet.svg)](https://optuna.org/)
[![Campus](https://img.shields.io/badge/UNISNU-Fakultas%20Sains%20%26%20Teknologi-darkgreen.svg)](https://unisnu.ac.id)

Repositori ini memuat seluruh artefak komputasi, pipeline eksperimen, naskah akademik (Bab I–V), dan koleksi referensi ilmiah untuk Skripsi Sarjana Komputer (S.Kom.), Program Studi Teknik Informatika, Fakultas Sains dan Teknologi, **Universitas Islam Nahdlatul Ulama (UNISNU) Jepara**.

> **Fokus penelitian:** Peramalan **Realized Volatility (RV)** harian Bitcoin menggunakan LSTM yang dioptimasi Optuna, dengan baseline HAR-RV, GARCH(1,1), dan Persistence. Data kline 1 jam BTC/USDT dari Binance Vision diagregasi menjadi RV harian; target peramalan adalah `log_rv_{t+1}`.
>
> **Protokol pre-registered:** `docs/STUDY2_PROTOCOL.md` (SHA-256 `72c75880…ba3`), data beku di `05_Source_Code/data/study2/` (SHA-256 `ec2e3fb4…08b`). Periode uji eksternal: 2026-01-01 s.d. 2026-09-30 (273 hari).
>
> **Hasil utama (jujur, kategori mixed):** LSTM-Optuna menghasilkan QLIKE 0,40333 — lebih rendah dari persistence (0,80521, DM *p* = 5,18×10⁻⁶) dan HAR-RV (0,46846, DM *p* = 0,05344). Superioritas terhadap HAR-RV belum signifikan pada α = 0,05. LSTM untuned justru memiliki QLIKE terendah (0,34422). Tidak ada perubahan baseline, metrik, split, seed, atau test window setelah hasil terlihat. Hasil dilaporkan apa adanya.
>
> **Naskah draf:** Bab 1–5 + 36 referensi di `03_Naskah_Skripsi/study2/` (Markdown = source of truth). DOCX: `SKRIPSI_STUDY2_DRAFT.docx`.
>
> **Peta repo:** lihat `PROJECT_STRUCTURE.md`.

---

## 👤 Informasi Mahasiswa & Proyek

| Item | Isi |
|---|---|
| **Nama** | Zaini Leon Musthofa Kamal |
| **NIM** | 231240001455 |
| **Program Studi** | S1 Teknik Informatika |
| **Fakultas** | Fakultas Sains dan Teknologi, UNISNU Jepara |
| **Dosen Pembimbing** | Teguh Tamrin, S.Kom., M.Kom. (NIDN: 0620127603) |
| **Tahun** | 2026 |
| **Judul** | Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Prediksi Volatilitas Bitcoin |

---

## 🌟 Ringkasan Penelitian

Penelitian ini menguji apakah optimasi hyperparameter LSTM berbasis Optuna (TPE + MedianPruner) dapat meningkatkan akurasi peramalan **realized volatility** harian Bitcoin, dibandingkan baseline ekonometrika klasik dan model naif.

### Desain Eksperimen

| Komponen | Spesifikasi |
|---|---|
| **Data** | Kline 1 jam BTC/USDT Binance Vision, 2020-01-01 s.d. 2026-09-30 |
| **Target** | `log_rv_{t+1}` — logaritma realized variance hari berikutnya |
| **Fitur (6)** | `log_rv`, `log_range`, `log_volume`, `log_absret`, `rv_mean_5`, `rv_mean_22` |
| **Split** | Dev 2020–2023 · Val 2024–2025 · Test 2026 (273 hari) |
| **HPO** | Optuna TPE, 50 trial, 5-fold purged rolling-origin CV |
| **Final** | 5 seed (42, 123, 2024, 7, 99), prediksi = rata-rata seed |
| **Metrik** | QLIKE (utama), MAE/RMSE log_rv (sekunder) |
| **Inferensi** | Diebold-Mariano (HAC lag 5), Moving-Block Bootstrap (block 20, 10.000 reps) |

### Baseline

| Model | Deskripsi |
|---|---|
| **Persistence** | Prediksi = nilai terakhir yang diketahui |
| **HAR-RV** | Heterogeneous Autoregressive Realized Volatility (Corsi, 2009) |
| **GARCH(1,1)** | Generalized ARCH (Bollerslev, 1986), rolling-origin |
| **LSTM Untuned** | LSTM dengan konfigurasi default tanpa optimasi |

### Hasil Test 2026 (QLIKE, semakin rendah semakin baik)

| Model | QLIKE | vs Persistence (DM *p*) |
|---|---|---|
| Persistence | 0,80521 | — |
| HAR-RV | 0,46846 | — |
| GARCH(1,1) | 0,44898 | — |
| **LSTM-Optuna** | **0,40333** | 5,18×10⁻⁶ ✓ |
| LSTM Untuned | 0,34422 | — |

**Verdict: mixed** — mengungguli persistence secara signifikan, menyaingi HAR-RV/GARCH secara *point estimate*, tetapi DM vs HAR-RV *p* = 0,05344 > 0,05.

---

## 📁 Struktur Direktori

```
jurnal/
├── 01_Panduan_Kampus/           # Pedoman skripsi UNISNU & template pengajuan judul
├── 02_Pengajuan_Judul/          # Formulir pengajuan judul Study 2
├── 03_Naskah_Skripsi/study2/    # Naskah Bab 1–5 (Markdown + DOCX draft)
├── 04_Referensi_Ilmiah/         # 19 PDF referensi ilmiah terverifikasi
├── 05_Source_Code/
│   ├── data/study2/             # Data RV harian beku (2.464 hari) + manifest hash
│   ├── generators/              # Kompilator Markdown → DOCX format UNISNU
│   ├── results/study2/          # Hasil HPO, final run, metrik, dan figur Bab 4
│   └── study2_volatility/       # Modul aktif: config, data, models, stats, HPO, final run, analyze
├── archive/study1/              # Arsip lengkap Study 1 (prediksi harga) — tidak aktif
├── docs/                        # Protokol, audit, gap, provenance, keterlacakan
├── references/                  # Paket Mendeley (RIS/BibTeX), matriks literatur 36 paper
├── tests/                       # 34 unit test Study 2 (100% PASS)
├── PROJECT_STRUCTURE.md         # Peta struktur detail
├── TODO.MD                      # Rencana kerja berurutan & checklist
└── requirements.txt             # Dependensi Python
```

Detail lengkap: [`PROJECT_STRUCTURE.md`](file:///d:/OneDrive/Desktop/jurnal/PROJECT_STRUCTURE.md)

---

## 🛠️ Panduan Reproduksi

### 1. Instalasi
```bash
pip install -r requirements.txt
```

### 2. Verifikasi Data & Test
```powershell
# Jalankan seluruh unit test Study 2
python -m pytest tests/ -v -p no:cacheprovider

# Verifikasi hash data beku
python -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv').read_bytes()).hexdigest())"
# Harus: ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b
```

### 3. Kompilasi Naskah DOCX
```bash
python 05_Source_Code/generators/generate_skripsi_study2.py
```
Output: `03_Naskah_Skripsi/study2/SKRIPSI_STUDY2_DRAFT.docx`

### 4. Impor Referensi ke Mendeley
Lihat panduan lengkap di [`references/README_MENDELEY.md`](file:///d:/OneDrive/Desktop/jurnal/references/README_MENDELEY.md).

---

## 📑 Dokumen Penting

| Dokumen | Isi |
|---|---|
| [`docs/STUDY2_PROTOCOL.md`](file:///d:/OneDrive/Desktop/jurnal/docs/STUDY2_PROTOCOL.md) | Protokol pre-registered (hash `72c75880…ba3`) |
| [`docs/STUDY2_PROVENANCE.md`](file:///d:/OneDrive/Desktop/jurnal/docs/STUDY2_PROVENANCE.md) | Timeline apa-dilihat-kapan |
| [`docs/AUDIT_FINDINGS_STUDY2_20261029.md`](file:///d:/OneDrive/Desktop/jurnal/docs/AUDIT_FINDINGS_STUDY2_20261029.md) | Temuan audit kode & metodologi |
| [`docs/TRACEABILITY.md`](file:///d:/OneDrive/Desktop/jurnal/docs/TRACEABILITY.md) | Matriks keterlacakan kode ↔ bab skripsi |
| [`docs/REFERENCE_AUDIT_STUDY2.md`](file:///d:/OneDrive/Desktop/jurnal/docs/REFERENCE_AUDIT_STUDY2.md) | Audit 36 referensi Study 2 |

---

## ⚠️ Catatan Integritas

- Hasil dikategorikan **mixed**, bukan positif penuh. Label ini dilaporkan apa adanya.
- Tidak ada perubahan baseline, metrik, split, seed, atau test window setelah hasil terlihat.
- Study 1 (prediksi harga penutupan) telah diarsipkan di `archive/study1/` dengan README provenance.
- Pemeriksaan Turnitin dan persetujuan pembimbing belum dapat diverifikasi dari repositori ini.

---

*Dikelola oleh **Zaini Leon Musthofa Kamal (231240001455)** — Teknik Informatika, UNISNU Jepara, 2026.*
