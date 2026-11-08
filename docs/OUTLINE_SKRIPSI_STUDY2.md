# OUTLINE SKRIPSI STUDY 2

**Judul:** Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Prediksi Volatilitas Bitcoin
**Fokus:** satu studi (Study 2). Study 1 hanya menjadi *pilot study* di Bab 1.
**Status:** draf lengkap Bab 1–5 + daftar referensi selesai; DOCX dikompilasi dari Markdown. Angka final diambil dari run `20261028_101839_final_ab5d93`.

---

## Prinsip penulisan (penting)

1. **Satu pertanyaan besar, satu dataset, satu test.** Jangan memasukkan eksperimen harga (Study 1) sebagai bab hasil; cukup sebagai motivasi.
2. **Klaim positif yang sah:** LSTM mengungguli persistence secara signifikan; LSTM menyaingi/mengungguli HAR-RV dan GARCH secara *point estimate*; kinerja stabil di test eksternal 2026.
3. **Wajib jujur:** uji DM vs HAR-RV *near-miss* (p = 0.0534) dan LSTM *untuned* lebih baik dari Optuna-LSTM. Ini masuk Bab 4/5 sebagai temuan, bukan disembunyikan.
4. **Jangan menulis** "Optuna terbukti meningkatkan akurasi" — tidak didukung hasil.

---

## BAB 1 — PENDAHULUAN

### 1.1 Latar Belakang (5–6 paragraf)
1. Bitcoin & volatilitas: kapitalisasi, risiko, kebutuhan peramalan (VaR, portofolio, derivatif).
2. Volatility clustering → volatilitas predictable; beda dengan harga yang mendekati random walk.
3. Model klasik: GARCH(1,1) dan HAR-RV; kekuatan & keterbatasan linearitas.
4. LSTM: kemampuan non-linear & long memory; sensitivitas hyperparameter.
5. Optuna/TPE: optimasi sistematis; **gap**: banyak studi tuning & evaluasi di periode sama, tanpa baseline naif, tanpa QLIKE, tanpa uji eksternal.
6. Solusi penelitian: pipeline LSTM+Optuna bebas kebocoran + baseline + QLIKE + test eksternal 2026. Sebutkan Study 1 (pilot) secara singkat: hasil harga negatif → memotivasi pemilihan target volatilitas.

### 1.2 Rumusan Masalah
- RQ1: Bagaimana merancang pipeline optimasi hyperparameter LSTM berbasis Optuna yang bebas kebocoran untuk prediksi RV Bitcoin?
- RQ2: Sejauh mana model mengungguli baseline persistence pada test eksternal 2026?
- RQ3: Apakah model menyaingi baseline HAR-RV dan GARCH(1,1)?

*Catatan:* analisis konsistensi kinerja validasi 2024–2025 vs uji eksternal 2026 tetap disajikan sebagai **analisis tambahan** di Bab 4, bukan RQ resmi. Outline yang di-ACC dosen memuat 3 RQ.

### 1.3 Tujuan Penelitian
Turunkan langsung dari RQ1–RQ3 + tujuan tambahan (analisis kontribusi optimasi vs LSTM default).

### 1.4 Manfaat Penelitian
Teoretis (bukti empiris RV + HPO), praktis (pipeline risk management), metodologis (template evaluasi leakage-free).

### 1.5 Batasan Masalah
BTC/USDT saja; data 1h Binance 2020-01–2026-09; target `log_rv`; test 2026 Jan–Sep; baseline & search space tetap; QLIKE utama; tanpa strategi trading/multi-aset.

### 1.6 Sistematika Penulisan
Bab 1 pendahuluan; Bab 2 landasan teori; Bab 3 metode; Bab 4 hasil & pembahasan; Bab 5 penutup.

---

## BAB 2 — LANDASAN TEORI

### 2.1 Volatilitas dan Realized Variance
- Definisi volatilitas, *volatility clustering*, *stylized facts*.
- RV dari data intraday: `RV_t = Σ (log(close_h) − log(open_h))²`.
- Kenapa log RV: stasioneritas & skala.

### 2.2 GARCH(1,1)
- Persamaan conditional variance; QML; keterbatasan (linear, distribusi).
- Perannya sebagai baseline ekonometrik.

### 2.3 HAR-RV
- Komponen harian/mingguan/bulanan (Corsi, 2009).
- Bentuk regresi yang dipakai: `log_rv_{t+1} ~ log_rv_t + mean7 + mean22`.

### 2.4 Long Short-Term Memory (LSTM)
- Gate input/forget/output; alasan cocok untuk deret waktu.
- Input sekuens: `lookback × 6 fitur`; output skalar `log_rv_{t+1}`.
- Risiko overfitting pada data harian terbatas.

### 2.5 Optimasi Hyperparameter dan Optuna
- Grid/random/TPE; kenapa TPE.
- Search space: lookback, units, layers, dropout, learning rate, batch size.
- *Purged rolling-origin CV* dan gap untuk mencegah kebocoran.

### 2.6 Evaluasi Peramalan Volatilitas
- QLIKE (Patton, 2011): `mean(exp(e) − e − 1)`, `e = y − ŷ`; sifat robust.
- MAE/RMSE pada log RV sebagai metrik sekunder.
- Diebold-Mariano (HAC/Bartlett) dan *moving-block bootstrap*.

### 2.7 Penelitian Terdahulu dan Gap
Tabel matriks (wajib): kolom = studi, target, data/frekuensi, protokol tuning, baseline, metrik, test eksternal. Baris = 15–25 studi.
**Gap statement:** belum ada studi yang menguji secara pre-registered apakah HPO Optuna bertransfer ke periode eksternal pada target RV Bitcoin dengan baseline ekonometrik dan QLIKE.

### 2.8 Kerangka Berpikir
Diagram: data 1h → RV → fitur → HPO (purged CV) → model final (5 seed) → baseline → QLIKE/DM/bootstrap → test 2026 → kesimpulan.

### 2.9 Hipotesis
H1 (vs persistence), H2 (menyaingi HAR/GARCH), H3 (konsisten di test eksternal).

---

## BAB 3 — METODE PENELITIAN

### 3.1 Desain Penelitian
Pipeline end-to-end + prinsip pre-registration (protokol & data di-hash).

### 3.2 Data dan Sumber
- Binance Vision kline 1h BTC/USDT, 2020-01–2026-09 (81 file).
- Agregasi UTC; syarat 24 bar/hari; amandemen A1 (hari <20 bar dikeluarkan; 2020-02-19).
- 2.464 hari; hash CSV `ec2e3fb4…`.

### 3.3 Target dan Fitur
Rumus lengkap 6 fitur + target; aturan anti-leakage; standardisasi hanya pada training fold.

### 3.4 Pembagian Data
- Dev/HPO 2020–2023; validasi 2024–2025; train pool 2020–2025; test 2026-01-01–2026-09-30.
- Purge gap = lookback + 1.

### 3.5 Optimasi Hyperparameter
- Optuna TPE seed 42; 50 trial; MedianPruner; objective mean CV QLIKE.
- Tabel search space.
- Pelatihan: max 100 epoch, early stopping patience 10.

### 3.6 Pelatihan Final dan Multi-Seed
- Refit pada train pool; 5 seed (42, 123, 2024, 7, 99); prediksi = rata-rata seed.
- Early stopping internal: 10% terakhir data training.

### 3.7 Baseline
Persistence, HAR-RV (OLS), GARCH(1,1) walk-forward, LSTM default (untuned).

### 3.8 Protokol Evaluasi
QLIKE, MAE/RMSE, DM (NW lag 5, one-sided), block bootstrap (block 20, 10k reps, seed 42).

### 3.9 Reproducibility
Hash protokol/data, manifest per run, environment, struktur kode.

---

## BAB 4 — HASIL DAN PEMBAHASAN

### 4.1 Statistik Deskriptif
- Tabel 4.1: mean/std/min/max RV & log RV; n hari; cakupan data.
- Gambar 4.1: time series `log_rv` 2020–2026 (tandai batas dev/val/test).

### 4.2 Hasil Optimasi Hyperparameter
- Tabel 4.2: 50 trial (ringkas), best trial 26 (lookback 16, units 22, layers 1, dropout 0.1, LR 5.12e-4, batch 16), mean CV QLIKE 0.48937.
- Gambar 4.2: riwayat nilai trial / konvergensi.

### 4.3 Hasil Validasi 2024–2025
- Tabel 4.3: QLIKE & MAE/RMSE semua model.
- Catatan: model fitting hanya pada dev; val sebagai checkpoint, bukan seleksi.

### 4.4 Hasil Uji Eksternal 2026 (utama)
- **Tabel 4.4 (wajib):**

| Model | QLIKE | MAE_logRV | RMSE_logRV |
|---|---|---|---|
| LSTM untuned | 0.34422 | 0.58659 | 0.76144 |
| LSTM Optuna | 0.40333 | 0.66620 | 0.88531 |
| GARCH(1,1) | 0.44898 | 0.93533 | 1.18944 |
| HAR-RV | 0.46846 | 0.68046 | 0.90767 |
| Persistence | 0.80521 | 0.85026 | 1.09996 |

- Gambar 4.3: prediksi vs aktual `log_rv` pada test (pilih 3 model utama).

### 4.5 Uji Signifikansi
- **Tabel 4.5:** ΔQLIKE, DM p (one-sided), CI bootstrap.
  - vs persistence: −0.40188; p<0.0001; CI [−0.55787, −0.22960].
  - vs HAR-RV: −0.06513; **p=0.0534**; CI [−0.14468, −0.00840].
  - vs GARCH: −0.04564; p=0.1822; CI [−0.11977, 0.04563].
- Narasi: menang signifikan vs persistence; *near-miss* vs HAR (tetap dilaporkan); vs GARCH belum signifikan.

### 4.6 Analisis Tambahan: Kontribusi Optimasi
- Bandingkan Optuna-LSTM vs LSTM default: 0.40333 vs 0.34422.
- Temuan: optimasi tidak meningkatkan kinerja out-of-sample pada kasus ini; diskusikan selection noise, ukuran data, pergeseran rezim 2026.
- Ini **bukan** kegagalan penelitian; ini temuan yang memperkuat pesan utama.

### 4.7 Ringkasan Jawaban RQ
- RQ1: pipeline berhasil dibangun & terverifikasi hash.
- RQ2: **jelas signifikan** vs persistence.
- RQ3: **ya** secara point estimate & CI vs HAR; kompetitif vs GARCH.
- Analisis tambahan (bukan RQ): konsistensi validasi vs uji 2026 — kinerja test tidak mengalami degradasi ekstrem dan tetap kompetitif.

---

## BAB 5 — PENUTUP

### 5.1 Kesimpulan
1. Pipeline LSTM+Optuna bebas kebocoran berhasil diimplementasikan dan direproduksi.
2. LSTM mengungguli persistence secara signifikan pada prediksi RV Bitcoin.
3. LSTM menyaingi HAR-RV dan GARCH; keunggulan vs HAR belum signifikan secara DM (p=0.0534) meski CI bootstrap mendukung.
4. Optimasi Optuna tidak memberi keunggulan out-of-sample dibanding LSTM default — temuan penting tentang batas HPO.

### 5.2 Diskusi
- Mengapa RV lebih predictable daripada harga.
- Mengapa HPO tidak transfer: variance selection, data terbatas, perubahan rezim.
- Implikasi: evaluasi ketat & baseline lebih penting daripada tuning agresif.
- Kaitan dengan Study 1 (pilot): dua target, kesimpulan konsisten tentang HPO.

### 5.3 Kontribusi
Empiris, metodologis, praktis.

### 5.4 Keterbatasan
Satu aset; test 273 hari (power); QLIKE saja; RV 1h tanpa jump; GARCH normal; DM lag 5 konservatif; search space terbatas.

### 5.5 Saran
Multi-aset (BTC+ETH); forecast probabilistik/quantile; test lebih panjang; model alternatif (GRU/Transformer); perluasan fitur (order flow, on-chain).

---

## Lampiran (rencana)

- Lampiran A: protokol + hash.
- Lampiran B: daftar 81 file data + hash.
- Lampiran C: manifest run & environment.
- Lampiran D: tabel hyperparameter lengkap 50 trial.
- Lampiran E: struktur kode & perintah reproduksi.

---

## Peta artefak → bab

| Artefak | Dipakai di |
|---|---|
| `docs/STUDY2_PROTOCOL.md` | Bab 1, Bab 3, Lampiran A |
| `docs/STUDY2_PROVENANCE.md` | Bab 3, Bab 5 (integritas) |
| `data/study2/btc_1h_daily_rv_2020_2026.csv` | Bab 3, Bab 4.1 |
| `results/study2/runs/...optuna_hpo.../trials.csv` | Bab 4.2 |
| `results/study2/runs/...final.../predictions_*.csv` | Bab 4.3–4.5 |
| `results/study2/runs/...final.../results_analysis.json/md` | Bab 4.5, Bab 5 |
| `05_Source_Code/study2_volatility/*.py` | Bab 3, Lampiran E |
| `tests/test_study2.py` | Bab 3 (validitas), Lampiran E |
