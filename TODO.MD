# TODO — Master Plan Penyusunan Skripsi Study 2 (Realized Volatility Bitcoin)

**Dokumen Pengendali Utama:** Dokumen ini memuat peta kerja nyata, terukur, dan berurutan agar seluruh proses penyusunan naskah akademik (Pengajuan Judul, Sempro Bab 1–3, dan Semhas Bab 4–5) berjalan transparan, berbasis bukti empiris yang ada, bebas halusinasi, dan sesuai pedoman FST UNISNU Jepara.

---

## 📌 STATUS SAAT INI (Kondisi Nyata Repositori)

- [x] **Pembersihan Repositori:** Seluruh modul, hasil, naskah, generator, data, release, dan konfigurasi Study 1 (prediksi harga) telah dipindahkan ke `archive/study1/`.
- [x] **Integritas Kode Eksperimen:** 9 modul aktif di `05_Source_Code/study2_volatility/` telah memiliki komentar Bahasa Indonesia, perbaikan kausalitas kalender, dan penandaan bab skripsi `[BAB 3 §3.x]` & `[BAB 4 §4.x]`.
- [x] **Verifikasi Unit Test:** 34/34 unit test di `tests/` lulus 100% (isolasi scaler, kausalitas, purged gap CV, dan evaluasi alignment).
- [x] **Status Hasil Eksperimen:** Hasil holdout 2026 telah beku dan terkunci (`results/study2/`):
  - QLIKE LSTM-Optuna: **0,40333**
  - QLIKE HAR-RV: **0,46846** (LSTM unggul point estimate ~13,9%; DM $p = 0,05344$)
  - QLIKE GARCH(1,1): **0,44898** (LSTM unggul point estimate)
  - QLIKE Persistence: **0,80521** (LSTM unggul telak; DM $p = 5,18 \times 10^{-6}$)
  - QLIKE LSTM Untuned: **0,34422** (Selisih tidak signifikan dua-sisi; fenomena *selection noise* & *regime shift*)
- [x] **Inventaris Pustaka:** 35 referensi resmi (31 file PDF lokal terverifikasi di `04_Referensi_Ilmiah/` + 4 dokumen resmi/buku). Telah dibedah secara mendalam di 6 klaster.

---

## 🚀 DAFTAR TUGAS BERURUTAN (EXECUTION ROADMAP)

### TAHAP 1: Finalisasi Pengajuan Judul & Praproposal (Target File 1)
*Dokumen target: `02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2.md` & `.docx`*
- [x] **1.1.** Sinkronkan judul resmi: *"Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin"*.
- [x] **1.2.** Masukkan 3 Rumusan Masalah yang telah disepakati (non-duplikatif: *Bagaimana, Sejauh mana, Apakah*).
- [x] **1.3.** Masukkan 3 Hipotesis terukur yang selaras dengan temuan empiris (H1 vs Persistence, H2 vs HAR-RV/GARCH, H3 Stabilitas Out-of-Sample).
- [x] **1.4.** Rumuskan Latar Belakang berbasis *research gap* (5 paragraf, 122–134 kata/paragraf, sitasi terverifikasi).
- [x] **1.5.** Batasi Pustaka Utama pada 14 paper inti paling representatif dengan format penulisan akademik resmi.
- [x] **1.6.** Kompilasi langsung ke format resmi Word FST UNISNU via `05_Source_Code/generators/generate_pengajuan_study2.py` (bersih tanpa file sisa).

---

### TAHAP 2: Pemantapan Naskah SEMPRO Bab 1 s.d. Bab 3 (Target File 2)
*Dokumen target: `03_Naskah_Skripsi/study2/` (Bab 1, Bab 2, Bab 3, dan Daftar Pustaka)*

#### A. Bab 1: Pendahuluan
- [x] **2.1.** Telaah & susun `BAB_1_PENDAHULUAN.md` dengan standar narasi buku (*academic storytelling*), istilah TI dijelaskan gamblang, dan per paragraf 120–140 kata.
- [x] **2.2.** Pastikan alur 10 paragraf latar belakang mengerucut dengan minimal 1 sitasi per paragraf (Andersen 2003, Corsi 2009, Patton 2011, Hochreiter 1997, Akiba 2019, López de Prado 2018, Bouthillier 2021, Diebold-Mariano 1995, Binance Vision 2024, dll.).
- [x] **2.3.** Sinkronkan rumusan masalah (3 butir non-duplikatif), tujuan penelitian (3 butir simetris), manfaat (teoretis, praktis, metodologis), batasan masalah (7 butir presisi), dan sistematika penulisan (Bab 1–5).
- [x] **2.4.** Kompilasi berkas resmi Word `BAB_1_PENDAHULUAN.docx` via `05_Source_Code/generators/generate_bab1_study2.py` dan perbarui `SKRIPSI_STUDY2_DRAFT.docx` tanpa file sisa/sementara.

#### B. Bab 2: Landasan Teori & Tinjauan Pustaka
- [x] **2.5.** Susun naskah komprehensif `BAB_2_LANDASAN_TEORI.md` (10 subbab standar panduan FST UNISNU: Konsep Dasar, GARCH, HAR-RV, LSTM, Optuna TPE, Evaluasi QLIKE/DM/Bootstrap, Penelitian Terdahulu + Matriks Sintesis, Posisi Penelitian, Kerangka Pemikiran, Hipotesis, dan Kesimpulan).
- [x] **2.6.** Sediakan skrip diagram resmi draw.io di `03_Naskah_Skripsi/study2/figures/KODE_DIAGRAM_DRAWIO.md` dan tautkan Gambar 2.1 (Arsitektur LSTM) serta Gambar 2.2 (Kerangka Pemikiran).
- [x] **2.7.** Kompilasi berkas resmi Word `BAB_2_LANDASAN_TEORI.docx` via `05_Source_Code/generators/generate_bab2_study2.py` (tabel formal shading, rumus matematis rapi, dan gambar diagram otomatis tersemat).
- [x] **2.8.** Sinkronkan draf naskah gabungan `SKRIPSI_STUDY2_DRAFT.docx`.
  - Inferensi Statistik: Uji Diebold-Mariano (1995), Koreksi HAC Newey-West (1987), Moving-Block Bootstrap (Künsch 1989), dan Variabilitas Multi-seed (Bouthillier et al. 2021).
- [ ] **2.5.** Perbarui Tabel Sintesis Penelitian Terdahulu (Tabel Matriks Gap) memuat studi global (Christensen 2023, Katsiampa 2017, Ardia 2019, Conrad 2018, Kim & Won 2018) dan studi nasional SINTA (Khumaidi 2024, Aldo 2026, Aswadi 2025, Fawzi 2025, Widad 2026, Ula 2024, Boongasame 2023, Wahyuddin 2025).
- [ ] **2.6.** Rumuskan Kerangka Berpikir dan Hipotesis Penelitian yang kokoh.

#### C. Bab 3: Metode Penelitian
- [x] **2.7.** Perbarui `BAB_3_METODE_PENELITIAN.md` (10 subbab standar panduan FST UNISNU: 3.1 Jenis dan Rancangan Penelitian, 3.2 Data Penelitian dan Pra-Pemrosesan, 3.3 Pengembangan Fitur dan Target, 3.4 Pembagian Data Temporal Kronologis, 3.5 Optimasi Hyperparameter LSTM Berbasis Optuna, 3.6 Pelatihan Model Final dan Multi-Seed, 3.7 Implementasi Baseline Pembanding, 3.8 Protokol Evaluasi dan Inferensi Statistik, 3.9 Validitas dan Pengendalian Data Leakage, 3.10 Robustness, Reproduksibilitas, dan Alur Penelitian).
- [x] **2.8.** Verifikasi 68 paragraf isi Bab 3 (100% memenuhi 110–140 kata per paragraf dan minimal 1 sitasi terverifikasi per paragraf dalam *prospective tense*).
- [x] **2.9.** Sediakan skrip Mermaid draw.io Gambar 3.1 (Alur Tahapan Penelitian Komputasional) pada `03_Naskah_Skripsi/study2/figures/KODE_DIAGRAM_DRAWIO.md` dan hasilkan gambar 300 DPI di `figures/gambar_3_1_alur_penelitian.png`.
- [x] **2.10.** Kompilasi berkas resmi Word `BAB_3_METODE_PENELITIAN.docx` via `05_Source_Code/generators/generate_bab3_study2.py` (5 tabel formal, 15 persamaan display, diagram tersemat rapi).
- [x] **2.11.** Sinkronkan draf naskah gabungan `SKRIPSI_STUDY2_DRAFT.docx` (1.458 KB, Bab I–V lengkap).

#### D. Sinkronisasi Daftar Pustaka Sempro
- [x] **2.12.** Sinkronkan `03_Naskah_Skripsi/study2/DAFTAR_REFERENSI_STUDY2.md` tepat menjadi 35 referensi terverifikasi (100% dikutip di Bab 1–3).
- [x] **2.13.** Sinkronkan file Mendeley `references/study2_references.ris` dan `references/study2_references.bib` (35 entri terverifikasi, siap impor 1-klik).
- [x] **2.14.** Bundel resmi naskah Sempro `03_Naskah_Skripsi/study2/PROPOSAL_SEMPRO_BAB_I_III.docx` (Cover + Bab 1 + Bab 2 + Bab 3 + Daftar Pustaka).

---

### TAHAP 3: Pemantapan Naskah SEMHAS Bab 4 s.d. Bab 5 (Target File 3)
*Dokumen target: `03_Naskah_Skripsi/study2/` (Bab 4 & Bab 5)*

#### A. Bab 4: Hasil dan Pembahasan
- [ ] **3.1.** Verifikasi seluruh angka statistik deskriptif data 2.464 hari (Tabel 4.1).
- [ ] **3.2.** Sajikan hasil HPO Optuna: Trial terbaik 26 (lookback 16, units 22, dropout 0.10, lr 0.0005117, batch 16, mean CV QLIKE 0,48937).
- [ ] **3.3.** Sajikan evaluasi out-of-sample 2026 pada 5 model (Tabel komparasi metrik QLIKE, MAE, RMSE).
- [ ] **3.4.** Sajikan hasil uji statistik inferensial:
  - LSTM Optuna vs Persistence: $DM = -4,410$, $p = 5,18 \times 10^{-6}$ (Signifikan mengungguli).
  - LSTM Optuna vs HAR-RV: $DM = -1,618$, $p = 0,05344$ (Unggul point estimate 13,9%, bootstrap CI negatif penuh).
  - LSTM Optuna vs GARCH(1,1): $DM = -0,909$, $p = 0,18217$.
- [ ] **3.5.** Tuliskan Pembahasan Kritis (Discussion) mengapa kategori hasil adalah *mixed*:
  - Analisis *Selection Noise* dan *Winner's Curse* (Bouthillier et al. 2021).
  - Analisis *Regime Shift* dinamika volatilitas Bitcoin antara 2020–2023 vs 2026 (Ardia et al. 2019).
  - Perbandingan kapasitas model (model ramping Optuna vs model besar untuned).
  - Refleksi metodologis: Keunggulan pelaporan jujur pra-registrasi dibandingkan fabrikasi hasil (*p-hacking*).

#### B. Bab 5: Penutup
- [ ] **3.6.** Rumuskan 5 Kesimpulan yang menjawab langsung 3 Rumusan Masalah tanpa klaim berlebihan.
- [ ] **3.7.** Uraikan Kontribusi Ilmiah (Empiris, Metodologis, Praktis).
- [ ] **3.8.** Paparkan Keterbatasan Penelitian (keterbatasan horizon uji 273 hari, tanpa biaya transaksi/slippage, model univariat).
- [ ] **3.9.** Susun Saran Riset Lanjutan yang aplikatif (adaptive rolling re-tuning, penambahan data order book, integrasi transformer/informer).

---

### TAHAP 4: Verifikasi Akhir, Kompilasi & Quality Control
- [ ] **4.1.** Jalankan pengujian ulang suite test `pytest tests/` memastikan tidak ada regresi logika.
- [ ] **4.2.** Jalankan `s2_figures.py` untuk memastikan seluruh 5 figur PNG di Bab 4 telah ter-render tajam dan presisi.
- [ ] **4.3.** Verifikasi format kompilator naskah di `05_Source_Code/generators/generate_skripsi_study2.py`.
- [ ] **4.4.** Lakukan audit silang sitasi dua arah (memastikan setiap sitasi di naskah ada di daftar pustaka 35 referensi, dan sebaliknya).
- [ ] **4.5.** Periksa status git bersih (`git diff --check`, tanpa menimpa berkas terproteksi).

---

*Dokumen TODO ini menjadi kompas absolut agar setiap langkah berjalan presisi, berurutan, dan terhindar dari disorientasi/halusinasi.*
