# FORMULIR PENGAJUAN JUDUL SKRIPSI (STUDY 2)

**Program Studi:** S1 Teknik Informatika
**Fakultas:** Sains dan Teknologi
**Universitas:** Universitas Islam Nahdlatul Ulama (UNISNU) Jepara

| Item | Isi |
|---|---|
| **Nama** | Zaini Leon Musthofa Kamal |
| **NIM** | 231240001455 |
| **Judul Penelitian** | **Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Prediksi Volatilitas Bitcoin** |
| **Bidang** | Kecerdasan Buatan / Pembelajaran Mesin |

## 1. Latar Belakang

Bitcoin merupakan aset kripto dengan kapitalisasi pasar terbesar dan salah satu
aset dengan volatilitas tertinggi. Volatilitas bukan sekadar ukuran risiko:
besaran ini dipakai untuk manajemen risiko, perhitungan Value-at-Risk (VaR),
alokasi portofolio, hingga penentuan harga instrumen derivatif. Berbeda dengan
asumsi volatilitas konstan, volatilitas Bitcoin menunjukkan *volatility
clustering* — periode tenang dan periode gejolak cenderung mengelompok — sehingga
volatilitas memiliki struktur yang dapat dimodelkan dan diprediksi.

Pendekatan klasik untuk peramalan volatilitas adalah GARCH(1,1) dan model
HAR-RV (*Heterogeneous Autoregressive Realized Volatility*). Keduanya kuat
secara interpretasi, tetapi terbatas pada hubungan linear dan bentuk fungsional
yang telah ditentukan. Di sisi lain, *Long Short-Term Memory* (LSTM) mampu
menangkap pola non-linear dan dependensi jangka panjang dari data deret waktu.
Namun, kinerja LSTM sangat sensitif terhadap hyperparameter — panjang
*lookback*, jumlah unit, dropout, laju pembelajaran, dan ukuran batch — sehingga
diperlukan strategi optimasi yang sistematis.

Optuna dengan algoritma *Tree-structured Parzen Estimator* (TPE) adalah salah
satu kerangka optimasi hyperparameter yang populer karena efisien dan mudah
direproduksi. Meskipun demikian, banyak penelitian menerapkan optimasi dan
evaluasi pada periode data yang sama, tanpa baseline naif, tanpa metrik yang
sesuai untuk volatilitas, dan tanpa periode uji eksternal. Akibatnya, klaim
peningkatan akurasi berisiko *optimistic bias* dan belum tentu bertahan pada
data baru. Kesenjangan inilah yang menjadi fokus penelitian: membangun pipeline
optimasi hyperparameter LSTM berbasis Optuna yang **bebas kebocoran data**,
lalu menguji kinerjanya pada **periode eksternal 2026** yang tidak digunakan
dalam pelatihan maupun optimasi.

Penelitian ini menggunakan data kline 1 jam BTC/USDT dari Binance untuk
mengestimasi *realized variance* (RV) harian, dengan target `log_rv_{t+1}`.
Evaluasi utama memakai **QLIKE**, *loss* yang robust untuk peramalan variance,
dilengkapi uji Diebold-Mariano dan *block bootstrap*. Baseline yang digunakan
adalah persistence, HAR-RV, GARCH(1,1), dan LSTM tanpa optimasi. Dengan
demikian, penelitian ini tidak hanya menghasilkan model, tetapi juga bukti
empiris yang dapat diaudit tentang nilai optimasi hyperparameter pada target
volatilitas.

## 2. Rumusan Masalah

1. Bagaimana merancang pipeline optimasi hyperparameter LSTM berbasis Optuna
   yang bebas kebocoran data untuk prediksi *realized volatility* Bitcoin?
2. Sejauh mana model LSTM yang dioptimasi Optuna mampu mengungguli baseline
   persistence dalam memprediksi *realized volatility* Bitcoin pada periode
   uji eksternal 2026?
3. Apakah model LSTM yang dioptimasi Optuna mampu menyaingi baseline
   ekonometrik HAR-RV dan GARCH(1,1) pada periode uji eksternal?
4. Bagaimana konsistensi kinerja model LSTM yang dioptimasi Optuna antara
   periode validasi 2024–2025 dan periode uji eksternal 2026 yang tidak
   digunakan dalam pelatihan maupun optimasi?

## 3. Tujuan Penelitian

1. Merancang dan mengimplementasikan pipeline optimasi hyperparameter LSTM
   berbasis Optuna dengan protokol validasi bebas kebocoran.
2. Mengukur dan membandingkan akurasi model terhadap baseline persistence.
3. Menilai daya saing model terhadap baseline HAR-RV dan GARCH(1,1).
4. Menguji konsistensi kinerja model pada periode uji eksternal 2026.
5. Sebagai analisis tambahan, mengevaluasi kontribusi optimasi hyperparameter
   Optuna dibandingkan konfigurasi LSTM default.

## 4. Hipotesis

- **H1:** Model LSTM yang dioptimasi Optuna menghasilkan QLIKE lebih rendah
  daripada baseline persistence pada periode uji 2026.
- **H2:** Model LSTM yang dioptimasi Optuna menghasilkan QLIKE tidak lebih
  buruk daripada baseline HAR-RV dan GARCH(1,1) pada periode uji 2026.
- **H3:** Kinerja model pada periode uji eksternal 2026 konsisten dengan
  kinerja pada periode validasi 2024–2025 (tidak terjadi degradasi ekstrem).

## 5. Manfaat Penelitian

**Teoretis:** memperkaya bukti empiris tentang penerapan LSTM dan optimasi
hyperparameter pada target *realized volatility* aset kripto, serta menunjukkan
pentingnya protokol evaluasi yang bebas kebocoran.

**Praktis:** menyediakan pipeline yang dapat direproduksi untuk peramalan
volatilitas Bitcoin, yang berguna untuk manajemen risiko dan analisis kuantitatif.

**Metodologis:** menjadi contoh penerapan QLIKE, uji Diebold-Mariano, dan
*block bootstrap* dalam evaluasi model volatilitas, termasuk penggunaan
periode uji eksternal yang belum pernah dipakai.

## 6. Batasan Masalah

- Satu aset: BTC/USDT; satu sumber data: Binance Vision kline 1 jam.
- Periode data 2020-01-01 s.d. 2026-09-30; uji eksternal 2026-01-01 s.d. 2026-09-30.
- Target: `log_rv_{t+1}` (realized variance harian).
- Model: LSTM dengan ruang hyperparameter yang telah ditetapkan; optimasi Optuna (TPE).
- Baseline: persistence, HAR-RV, GARCH(1,1), LSTM default.
- Metrik utama: QLIKE; metrik sekunder: MAE/RMSE pada `log_rv`.
- Tidak mencakup strategi trading, portofolio multi-aset, data order book,
  atau analisis faktor makroekonomi.

## 7. Metodologi Ringkas

1. **Data:** unduh kline 1 jam BTC/USDT (Binance Vision), agregasi per hari UTC,
   hitung RV = Σ(log(close_h) − log(open_h))²; verifikasi 24 bar/hari.
2. **Fitur (6):** `log_rv`, `log_range`, `log_volume`, `log_absret`,
   `rv_mean_5`, `rv_mean_22`; target `log_rv_{t+1}`.
3. **Split:** dev/HPO 2020–2023; validasi 2024–2025; uji eksternal 2026;
   refit final pada 2020–2025.
4. **Optimasi:** Optuna TPE, 50 trial, *purged rolling-origin* CV (5 fold,
   gap = lookback), objective mean CV QLIKE.
5. **Pelatihan final:** 5 seed (42, 123, 2024, 7, 99); prediksi = rata-rata seed.
6. **Evaluasi:** QLIKE, MAE/RMSE `log_rv`; Diebold-Mariano (HAC lag 5) dan
   *moving-block bootstrap* (block 20, 10.000 reps).
7. **Reproducibility:** protokol dan data di-hash; setiap run memiliki manifest.

## 8. Referensi/Pustaka Utama

1. Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735–1780.
2. Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. *KDD '19*.
3. Andersen, T. G., & Bollerslev, T. (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. *International Economic Review*, 39(4), 885–905.
4. Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics*, 7(2), 174–196.
5. Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327.
6. Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. *Journal of Econometrics*, 160(1), 246–256.
7. Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263.
8. Bergmeir, C., & Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. *Information Sciences*, 191, 192–213.
9. Bouthillier, X., et al. (2021). Accounting for variance in machine learning benchmarks. *MLSys 2021*.

---

Jepara, ............................

Pengusul,


Zaini Leon Musthofa Kamal
NIM. 231240001455
