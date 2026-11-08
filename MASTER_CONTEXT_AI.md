# 🧠 MASTER CONTEXT — Skripsi Zaini Leon Musthofa Kamal
> **File ini adalah "otak" proyek.** Baca seluruh isi file ini terlebih dahulu sebelum membantu penulis. File ini memuat identitas penulis, judul & topik penelitian, struktur folder lengkap, standar penulisan akademik, aturan anti-Turnitin, lokasi semua dokumen penting, status progres, dan ketentuan Mendeley. Tidak perlu menebak-nebak — semua ada di sini.

---

## 1. 👤 Identitas Penulis & Institusi

| Item | Isi |
|---|---|
| **Nama Lengkap** | Zaini Leon Musthofa Kamal |
| **NIM** | `231240001455` *(WAJIB dipakai, bukan NIM lama `221240001290`)* |
| **Program Studi** | S1 Teknik Informatika |
| **Fakultas** | Fakultas Sains dan Teknologi (FST) |
| **Universitas** | Universitas Islam Nahdlatul Ulama (UNISNU) Jepara |
| **Dosen Pembimbing** | Teguh Tamrin, S.Kom., M.Kom. (NIDN: 0620127603) |
| **Tahun** | 2026 |
| **GitHub Repo** | https://github.com/zeen-lien/OptimasiBTC |
| **Branch Aktif** | `study2-volatility` |

---

## 2. 📌 Judul & Topik Penelitian

**Judul Resmi:**
> *Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin*

**Deskripsi Singkat:**
Penelitian ini menguji apakah optimasi hyperparameter LSTM berbasis Optuna (TPE + MedianPruner) dapat meningkatkan akurasi peramalan **Realized Volatility (RV)** harian Bitcoin, dibandingkan baseline ekonometrika klasik (HAR-RV, GARCH) dan model naif (Persistence).

Ini adalah **Study 2** — Study 1 (prediksi harga penutupan/closing price) sudah diarsipkan karena terbukti secara statistik gagal mengungguli model naif.

---

## 3. 🔬 Desain Eksperimen (Ringkasan Teknis)

| Komponen | Spesifikasi |
|---|---|
| **Sumber Data** | Kline 1 jam BTC/USDT dari Binance Vision |
| **Periode Data** | 2020-01-01 s.d. 2026-09-30 (2.464 hari) |
| **Target Prediksi** | `log_rv_{t+1}` — log realized variance hari berikutnya |
| **Fitur (6)** | `log_rv`, `log_range`, `log_volume`, `log_absret`, `rv_mean_5`, `rv_mean_22` |
| **Split Data** | Dev 2020–2023 · Val 2024–2025 · **Test 2026** (273 hari) |
| **Metrik Utama** | QLIKE (quasi-likelihood, semakin rendah semakin baik) |
| **Metrik Sekunder** | MAE, RMSE (skala log_rv) |
| **HPO** | Optuna TPE Sampler, 50 trial, 5-fold Purged Rolling-Origin CV |
| **Final Run** | 5 seed (42, 123, 2024, 7, 99) → prediksi = rata-rata seed |
| **Inferensi** | Diebold-Mariano (HAC Newey-West lag 5), Moving-Block Bootstrap (blok 20, 10.000 reps) |

**Baseline Model:**

| Model | QLIKE (Test 2026) | Keterangan |
|---|---|---|
| Persistence | 0,80521 | Prediksi = nilai terakhir |
| HAR-RV (Corsi, 2009) | 0,46846 | Model ekonometrika heterogen |
| GARCH(1,1) (Bollerslev, 1986) | 0,44898 | Model ARCH klasik |
| **LSTM-Optuna** | **0,40333** | Model utama penelitian |
| LSTM Untuned | 0,34422 | LSTM tanpa optimasi |

**Verdict: Kategori MIXED** — LSTM-Optuna mengungguli Persistence secara signifikan (DM *p* = 5,18×10⁻⁶), namun keunggulan vs HAR-RV belum signifikan pada α = 0,05 (DM *p* = 0,05344). Ini dilaporkan apa adanya, **tidak ada manipulasi hasil**.

---

## 4. 🗂️ Struktur Folder Project (Root: `D:\OneDrive\Desktop\jurnal\`)

```
jurnal/
│
├── 01_Panduan_Kampus/              # Pedoman resmi FST UNISNU
│   ├── panduan-skripsi.docx        # 📋 BUKU PANDUAN SKRIPSI UNISNU (acuan format utama)
│   ├── file contoh pengajuan judul.docx  # Template pengajuan judul resmi
│   └── contoh temen/               # 📁 Contoh proposal milik teman sebagai ACUAN FORMAT
│       ├── contoh Proposal dany.pdf    # ⭐ Proposal lengkap Dany Akmallun Ni'am (ACC)
│       └── DAFTAR ISI ghei.docx        # Contoh daftar isi dari teman lain
│
├── 02_Pengajuan_Judul/             # Berkas pengajuan judul Study 2
│   ├── PENGAJUAN_JUDUL_STUDY2.md   # Source of truth (Markdown)
│   ├── PENGAJUAN_JUDUL_STUDY2.docx # Output Word resmi
│   └── done/                       # ✅ Pengajuan judul sudah ACC dospem
│       └── Optimasi Hyperparameter LSTM... .pdf  # Bukti persetujuan
│
├── 03_Naskah_Skripsi/study2/       # 📝 NASKAH UTAMA (Markdown = source of truth)
│   ├── BAB_1_PENDAHULUAN.md/.docx
│   ├── BAB_2_LANDASAN_TEORI.md/.docx
│   ├── BAB_3_METODE_PENELITIAN.md/.docx
│   ├── BAB_4_HASIL_DAN_PEMBAHASAN.md  ← BELUM FINAL
│   ├── BAB_5_PENUTUP.md               ← BELUM FINAL
│   ├── DAFTAR_REFERENSI_STUDY2.md  # 36 referensi APA 7th
│   ├── PROPOSAL_SEMPRO_BAB_I_III.docx  # ⭐ Bundel SEMPRO (Bab 1–3 + Cover + Daftar Pustaka)
│   ├── PROPOSAL_SEMPRO_BAB_I_III.md
│   ├── SKRIPSI_STUDY2_DRAFT.docx   # Draft gabungan Bab 1–5
│   └── figures/
│       ├── gambar_2_1_arsitektur_lstm.png
│       ├── gambar_2_2_kerangka_pemikiran.png
│       ├── gambar_3_1_alur_penelitian.png
│       ├── logo_unisnu.png
│       └── KODE_DIAGRAM_DRAWIO.md  # Kode draw.io & Mermaid untuk diagram
│
├── 04_Referensi_Ilmiah/            # 📚 33 PDF referensi terverifikasi
│   ├── Referensi_Utama/            # 18 paper inti (Bitcoin, LSTM, RV, HPO)
│   ├── Referensi_Tambahan/         # 15 paper pendukung (statistik, optimizer, dll)
│   └── Arsip_Tidak_Dipakai/        # ⚠️ JANGAN dilampirkan ke Mendeley!
│
├── 05_Source_Code/
│   ├── data/study2/                # Data RV harian beku (hash SHA-256 terkunci)
│   ├── generators/                 # Kompilator Markdown → DOCX standar UNISNU
│   │   ├── generate_sempro_study2.py    # Generator PROPOSAL_SEMPRO_BAB_I_III.docx
│   │   ├── generate_bab1_study2.py
│   │   ├── generate_bab2_study2.py
│   │   ├── generate_bab3_study2.py
│   │   └── generate_skripsi_study2.py   # Generator draft gabungan Bab 1–5
│   ├── study2_volatility/          # 9 modul pipeline aktif
│   │   ├── s2_config.py     # Konfigurasi path & parameter
│   │   ├── s2_data.py       # Download & agregasi data Binance
│   │   ├── s2_models.py     # Arsitektur LSTM, HAR-RV, GARCH, Persistence
│   │   ├── s2_stats.py      # QLIKE, Diebold-Mariano, Bootstrap
│   │   ├── s2_optuna_search.py  # HPO Optuna TPE + Purged CV
│   │   ├── s2_final_run.py  # Final run multi-seed
│   │   ├── s2_analyze.py    # Validasi & komparasi metrik
│   │   ├── s2_figures.py    # Figur Bab 4
│   │   └── s2_runlog.py     # Provenance & audit jejak eksekusi
│   └── results/study2/     # Hasil eksperimen (BEKU, tidak diubah lagi)
│
├── archive/study1/         # 🗄️ ARSIP Study 1 (prediksi harga) — tidak aktif
│
├── docs/                   # Dokumen protokol & audit
│   ├── STUDY2_PROTOCOL.md           # Protokol pre-registered
│   ├── AUDIT_FINDINGS_STUDY2_20261029.md
│   ├── TRACEABILITY.md              # Keterlacakan kode ↔ bab
│   └── REFERENCE_AUDIT_STUDY2.md   # Audit 36 referensi
│
├── references/             # 📦 Paket Mendeley siap impor
│   ├── study2_references.ris       # ⭐ Import ke Mendeley (RIS format)
│   ├── study2_references.bib       # BibTeX format
│   ├── literature_matrix.csv       # Matriks 36 paper
│   └── README_MENDELEY.md          # Panduan lengkap import Mendeley
│
├── tests/                  # 34 unit test (100% PASS)
│
├── MASTER_CONTEXT_AI.md    # 📌 FILE INI — baca pertama kali!
├── PROJECT_STRUCTURE.md    # Detail struktur teknis
├── TODO.MD                 # Roadmap & checklist progres
├── README.md               # Dokumentasi utama repo
└── requirements.txt        # Dependensi Python
```

---

## 5. ✍️ STANDAR PENULISAN AKADEMIK (WAJIB DIPATUHI)

### 5.1 Panjang Paragraf: Minimum 120–140 Kata Per Paragraf

Setiap paragraf **wajib mengandung minimal 120 kata, idealnya 130–140 kata**. Ini bukan pilihan — ini standar yang sudah disepakati dengan penulis. Paragraf pendek di bawah 100 kata harus diperpanjang dengan:
- Elaborasi konsep yang lebih mendalam
- Contoh konkret atau analogi
- Penjelasan implikasi dari pernyataan

### 5.2 Sitasi Wajib di Setiap Paragraf

**Setiap paragraf substantif wajib mengandung minimal 1 sitasi** dari 36 referensi terverifikasi. Format sitasi mengikuti **APA 7th Edition**:
- Satu penulis: `(Corsi, 2009)`
- Dua penulis: `(Andersen & Bollerslev, 1998)`
- Tiga+ penulis (pertama kali): `(Andersen et al., 2003)`
- Dua sitasi sekaligus: `(Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002)`

**Sitasi yang sering dipakai (hafal ini):**
- Volatilitas Bitcoin: Katsiampa (2017), Ardia et al. (2019)
- Realized Variance: Andersen et al. (2003), Barndorff-Nielsen & Shephard (2002), Andersen & Bollerslev (1998)
- HAR-RV: Corsi (2009)
- GARCH: Bollerslev (1986), Engle (1982)
- LSTM: Hochreiter & Schmidhuber (1997)
- Optuna/TPE: Akiba et al. (2019), Bergstra et al. (2011)
- QLIKE: Patton (2011)
- Diebold-Mariano: Diebold & Mariano (1995)
- Bootstrap: Künsch (1989)
- HAC: Newey & West (1987)
- Volatility forecasting ML: Christensen et al. (2023), Lim & Zohren (2021)
- Multi-seed benchmarking: Bouthillier et al. (2021)
- Advances in Financial ML: López de Prado (2018)
- Studi nasional LSTM Bitcoin: Khumaidi et al. (2024), Aswadi & Ependi (2025), Fawzi et al. (2025), Ula et al. (2024)
- Conrad GARCH-MIDAS Bitcoin: Conrad et al. (2018)
- Kim & Won LSTM+GARCH: Kim & Won (2018)

### 5.3 Gaya Penulisan: Academic Storytelling

Naskah harus terasa seperti **pembaca sedang diajak memahami cerita**, bukan membaca laporan teknis kering. Caranya:
- **Mulai dengan konteks besar**, lalu perlahan-lahan masuk ke detail teknis
- Setiap konsep baru dijelaskan dengan analogi atau frasa penjelas sebelum definisi formal
- Gunakan **transisi naratif** antar paragraf agar pembaca merasa alurnya mengalir
- Istilah teknis berbahasa Inggris ditulis **miring (*italic*)** dan didampingi penjelasan Bahasa Indonesia pertama kali muncul. Contoh: *realized variance* (varians terealisasi)
- Rumus matematika dipakai **setelah** konsep dijelaskan secara naratif

### 5.4 Hierarki Heading Standar FST UNISNU

```
BAB I PENDAHULUAN           ← Uppercase, tanpa heading markdown biasa
  A. Latar Belakang         ← Huruf kapital awal, huruf besar setelah titik
  B. Rumusan Masalah
  C. Batasan Masalah
  D. Tujuan Penelitian
  E. Manfaat Penelitian
  F. Sistematika Penulisan

BAB II LANDASAN TEORI
  A. Volatilitas dan Realized Variance
  B. Model GARCH
  C. Model HAR-RV
  ... dst

BAB III METODE PENELITIAN
  A. Jenis dan Rancangan Penelitian
  B. Data Penelitian dan Pra-Pemrosesan
  ... dst
```

Mengacu pada proposal ACC milik **Dany Akmallun Ni'am** (`01_Panduan_Kampus/contoh temen/contoh Proposal dany.pdf`) sebagai contoh format yang sudah disetujui.

### 5.5 Format Penulisan Rumus Matematika

- Rumus **display** (berdiri sendiri): ditulis dengan label nomor di kanan, contoh: `(3.1)`
- Variabel dalam teks: ditulis dalam format *italic* seperti $f_t$, $C_t$, $\sigma^2$
- Simbol nilai mutlak: gunakan `\lvert ... \rvert` (BUKAN `|`) untuk menghindari bug tabel Markdown
- Rumus tidak boleh mengandung token LaTeX mentah seperti `\begin{cases}`, `\frac`, `\widehat` yang tidak ter-render

### 5.6 Format Tabel

- Setiap tabel **wajib punya header kolom yang terisi** (tidak boleh ada kolom kosong)
- Tabel diberi nomor dan judul di atas: `Tabel 3.1 Nama Tabel`
- Kolom `|` di dalam konten tabel di-escape menggunakan `\|` atau tanda lain

### 5.7 Format Penulisan Angka

- Angka desimal: pakai koma (`,`) bukan titik (`.`) → contoh: `0,40333` bukan `0.40333`
- Angka ribuan: pakai titik (`.`) → contoh: `2.464 hari`
- Satuan: dipisah spasi → `273 hari`, `10.000 repetisi`

---

## 6. 🚫 ATURAN ANTI-TURNITIN (Substitusi Kata Wajib)

Kata-kata berikut sering terdeteksi plagiarisme Turnitin dan **harus diganti** dengan padanannya:

### Penghubung & Transisi

| ❌ Jangan Pakai | ✅ Ganti Dengan |
|---|---|
| Oleh karena itu | Atas dasar tersebut |
| Selain itu | Di samping hal tersebut |
| Dengan demikian | Maka dari itu |
| Tidak hanya itu | Lebih lanjut |
| Selanjutnya | Tahap berikutnya |
| Dalam hal ini | Pada konteks tersebut |
| Pada dasarnya | Secara umum |
| Seiring dengan perkembangan | Mengikuti perubahan yang terjadi |
| Hal tersebut disebabkan oleh | Kondisi tersebut terjadi karena |
| Sebagai salah satu upaya | Sebagai bentuk usaha |
| Menurut pendapat | Sebagaimana dijelaskan oleh |
| Berdasarkan penjelasan tersebut | Mengacu pada pemaparan tersebut |
| Berdasarkan uraian di atas | Merujuk pada penjelasan sebelumnya |

### Penelitian & Kesimpulan

| ❌ Jangan Pakai | ✅ Ganti Dengan |
|---|---|
| Berdasarkan hasil penelitian | Dari temuan penelitian ini |
| Hasil penelitian menunjukkan | Temuan studi memperlihatkan |
| Dalam penelitian ini | Pada studi yang dilakukan |
| Bertujuan untuk mengetahui | Dilakukan untuk mengidentifikasi |
| Hal ini menunjukkan bahwa | Temuan tersebut mengindikasikan bahwa |
| Dapat dilihat bahwa | Hal tersebut terlihat dari |
| Dapat dikatakan bahwa | Hal ini dapat diartikan bahwa |
| Dapat disimpulkan bahwa | Kesimpulan yang diperoleh adalah |
| Memiliki pengaruh terhadap | Berpengaruh pada |
| Sangat penting untuk | Memegang peranan penting dalam |
| Salah satu faktor yang memengaruhi | Salah satu aspek yang berperan dalam |
| Untuk mencapai tujuan tersebut | Guna mewujudkan tujuan tersebut |

---

## 7. 📋 STATUS PROGRES SAAT INI

| Tahap | Status | File |
|---|---|---|
| Pengajuan Judul | ✅ **ACC Dospem** | `02_Pengajuan_Judul/done/` |
| Bab 1 Pendahuluan | ✅ **Selesai** | `BAB_1_PENDAHULUAN.md/.docx` |
| Bab 2 Landasan Teori | ✅ **Selesai** | `BAB_2_LANDASAN_TEORI.md/.docx` |
| Bab 3 Metode Penelitian | ✅ **Selesai** | `BAB_3_METODE_PENELITIAN.md/.docx` |
| Proposal SEMPRO Bab 1–3 | ✅ **Selesai (di-push ke GitHub)** | `PROPOSAL_SEMPRO_BAB_I_III.docx` |
| Bab 4 Hasil & Pembahasan | ⬜ **Belum dikerjakan** | `BAB_4_HASIL_DAN_PEMBAHASAN.md` |
| Bab 5 Penutup | ⬜ **Belum dikerjakan** | `BAB_5_PENUTUP.md` |
| Setting Mendeley Manual | ⬜ **Belum — NEXT STEP** | `references/README_MENDELEY.md` |

**Next step yang harus dikerjakan:**
1. Setting Mendeley — import `references/study2_references.ris` (36 referensi)
2. Lampirkan 33 PDF ke Mendeley sesuai panduan di `references/README_MENDELEY.md`
3. Setelah Mendeley beres → kerjakan Bab 4 dan Bab 5

---

## 8. 📚 MENDELEY — Panduan Singkat

> Panduan lengkap ada di: `references/README_MENDELEY.md`

**File yang diimpor:**
- `references/study2_references.ris` ← **pakai ini** (lebih stabil di Mendeley)
- `references/study2_references.bib` (alternatif BibTeX)

**PDF yang dilampirkan:** 33 file di `04_Referensi_Ilmiah/Referensi_Utama/` dan `Referensi_Tambahan/`

**JANGAN dilampirkan:** File di `04_Referensi_Ilmiah/Arsip_Tidak_Dipakai/` (konten salah/duplikat)

**Catatan tahun yang sering keliru:**

| Referensi | Tahun Benar |
|---|---|
| Corsi | 2009 (bukan 2008) |
| Christensen et al. | 2023 (bukan 2022) |
| Kingma & Ba | 2014 (bukan 2015) |
| Wahyuddin et al. | 2025 (bukan 2024) |

---

## 9. 🏗️ FORMAT DOKUMEN WORD (UNISNU)

Setiap dokumen `.docx` yang dihasilkan generator mengikuti standar ini:

| Properti | Nilai |
|---|---|
| **Font** | Times New Roman 12pt |
| **Spasi** | 1,5 baris |
| **Margin** | Atas 4cm · Kiri 4cm · Bawah 3cm · Kanan 3cm |
| **Ukuran Kertas** | A4 |
| **Nomor Halaman** | Angka arab di kanan bawah (Bab 1–5), Romawi kecil (bagian awal) |
| **Heading Bab** | Uppercase, center, bold |
| **Sub-heading** | Huruf besar tiap kata, left-aligned |

---

## 10. 🔧 PERINTAH PENTING (Quick Reference)

```powershell
# Jalankan semua unit test
python -m pytest tests/ -v -p no:cacheprovider

# Generate PROPOSAL SEMPRO (Bab 1–3 + Cover)
python 05_Source_Code/generators/generate_sempro_study2.py

# Generate draft gabungan Bab 1–5
python 05_Source_Code/generators/generate_skripsi_study2.py

# Generate per-bab
python 05_Source_Code/generators/generate_bab1_study2.py
python 05_Source_Code/generators/generate_bab2_study2.py
python 05_Source_Code/generators/generate_bab3_study2.py

# Git push ke GitHub
git add -A
git commit -m "pesan commit"
git push origin study2-volatility

# Verifikasi hash data beku
python -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv').read_bytes()).hexdigest())"
# Hash benar: ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b
```

---

## 11. 📂 DOKUMEN ACUAN PENTING

| Dokumen | Lokasi | Fungsi |
|---|---|---|
| **Panduan Skripsi UNISNU** | `01_Panduan_Kampus/panduan-skripsi.docx` | Referensi format & aturan penulisan resmi kampus |
| **Contoh Proposal Dany (ACC)** | `01_Panduan_Kampus/contoh temen/contoh Proposal dany.pdf` | ⭐ Acuan susunan, format, dan gaya penulisan proposal |
| **Daftar ISI Ghei** | `01_Panduan_Kampus/contoh temen/DAFTAR ISI ghei.docx` | Referensi format daftar isi |
| **Template Pengajuan Judul** | `01_Panduan_Kampus/file contoh pengajuan judul.docx` | Template resmi formulir pengajuan judul |
| **Daftar 36 Referensi** | `03_Naskah_Skripsi/study2/DAFTAR_REFERENSI_STUDY2.md` | Master list referensi APA 7th |
| **Audit Referensi** | `docs/REFERENCE_AUDIT_STUDY2.md` | Status verifikasi setiap referensi |
| **Panduan Mendeley** | `references/README_MENDELEY.md` | Langkah impor + lampirkan PDF |
| **Roadmap TODO** | `TODO.MD` | Checklist progres & rencana kerja |
| **Protokol Pre-registered** | `docs/STUDY2_PROTOCOL.md` | Desain eksperimen yang dikunci sebelum melihat hasil |
| **Traceability** | `docs/TRACEABILITY.md` | Peta kode ↔ bab skripsi |

---

## 12. ⚠️ HAL-HAL YANG WAJIB DIINGAT

> [!IMPORTANT]
> **NIM penulis adalah `231240001455`** — jika ada dokumen yang masih memakai `221240001290`, itu harus dikoreksi.

> [!WARNING]
> **Data eksperimen BEKU** — tidak boleh mengubah hash data, seed, split, baseline, atau metrik setelah hasil terlihat. Ini komitmen integritas ilmiah.

> [!CAUTION]
> **PDF di `04_Referensi_Ilmiah/Arsip_Tidak_Dipakai/` JANGAN dilampirkan ke Mendeley** — kontennya salah (isi PDF tidak sesuai judul).

> [!NOTE]
> **Markdown adalah source of truth** — `.docx` di-generate dari `.md` menggunakan skrip generator. Jika ada perubahan naskah, selalu ubah file `.md` terlebih dahulu, lalu re-generate `.docx`.

> [!TIP]
> **Hasil penelitian dikategorikan "mixed"** — JANGAN mendeskripsikan hasil sebagai "berhasil penuh" atau "unggul signifikan vs semua baseline". Pelaporan jujur adalah nilai metodologis utama penelitian ini.

---

## 13. 🏛️ STRUKTUR NASKAH (Outline Lengkap)

### Bab 1: Pendahuluan (✅ Selesai)
`A` Latar Belakang (10 paragraf, mengalir dari pasar kripto → prediksi harga gagal → RV → LSTM → Optuna → gap penelitian)
`B` Rumusan Masalah (3 butir: *Bagaimana* rancang model, *Sejauh mana* efektivitas vs Persistence, *Apakah* LSTM-Optuna kompetitif vs HAR-RV/GARCH)
`C` Batasan Masalah (7 butir: hanya BTC/USDT, hanya RV harian, hanya LSTM vanilla, 50 trial Optuna, split temporal fixed, QLIKE sebagai metrik utama, tanpa trading simulation)
`D` Tujuan Penelitian (3 butir simetris dengan Rumusan Masalah)
`E` Manfaat Penelitian (Teoretis, Praktis, Metodologis)
`F` Sistematika Penulisan (Bab 1–5)

### Bab 2: Landasan Teori (✅ Selesai)
`A` Konsep Dasar Volatilitas & Realized Variance
`B` Model GARCH(1,1) — Bollerslev (1986)
`C` Model HAR-RV — Corsi (2009)
`D` Arsitektur LSTM — Hochreiter & Schmidhuber (1997)
`E` Algoritma Optuna TPE — Akiba et al. (2019), Bergstra et al. (2011)
`F` Fungsi Kerugian QLIKE — Patton (2011)
`G` Uji Diebold-Mariano & Bootstrap — Diebold & Mariano (1995), Künsch (1989)
`H` Penelitian Terdahulu + Matriks Sintesis (Nasional & Internasional)
`I` Kerangka Pemikiran (Gambar 2.2)
`J` Hipotesis Penelitian (H1: vs Persistence, H2: vs HAR-RV/GARCH, H3: Stabilitas)

### Bab 3: Metode Penelitian (✅ Selesai)
`A` Jenis dan Rancangan Penelitian
`B` Data Penelitian & Pra-Pemrosesan
`C` Pengembangan Fitur dan Target
`D` Pembagian Data Temporal Kronologis
`E` Optimasi Hyperparameter LSTM Berbasis Optuna
`F` Pelatihan Model Final dan Multi-Seed
`G` Implementasi Baseline Pembanding
`H` Protokol Evaluasi dan Inferensi Statistik
`I` Validitas dan Pengendalian Data Leakage
`J` Robustness, Reproduksibilitas, dan Alur Penelitian (Gambar 3.1)
`K` Jadwal Penelitian (Tabel 3.6)

### Bab 4: Hasil & Pembahasan (⬜ Belum)
`A` Statistik Deskriptif Data (Tabel 4.1)
`B` Hasil HPO Optuna (Trial 26 terbaik)
`C` Evaluasi Out-of-Sample 2026 (Tabel komparasi 5 model)
`D` Uji Inferensi Statistik (DM test, Bootstrap)
`E` Pembahasan Kritis (Selection Noise, Regime Shift, Refleksi Metodologis)

### Bab 5: Penutup (⬜ Belum)
`A` Kesimpulan (5 poin, menjawab 3 Rumusan Masalah)
`B` Kontribusi Ilmiah
`C` Keterbatasan Penelitian
`D` Saran Riset Lanjutan

---

*File ini di-maintain di `D:\OneDrive\Desktop\jurnal\MASTER_CONTEXT_AI.md` dan di-push ke GitHub branch `study2-volatility`. Terakhir diperbarui: 2026-11-08.*
