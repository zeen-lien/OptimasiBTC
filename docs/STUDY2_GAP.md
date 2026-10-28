# FRESH GAP STUDY 2 - Peramalan Volatilitas Bitcoin (2026)

**Status:** Dikunci pada 2026-10-28 sebelum data test 2026 baru dibangun.
**Branch aktif:** `study2-volatility`
**Bukan pengganti:** Study 1 (`v1.0-final`) tetap beku sebagai hasil studi harga.

## 1. Kenapa arah ini "fresh"

Study 1 menunjukkan kejujuran hasil harga harian. Namun mengejar keuntungan point-forecast harga harian sangat sulit. Study 2 pindah ke target yang secara literatur jelas lebih **prediktif dan sudah stabil**:

- **Volatilitas berkelompok** (volatility clustering).
- Ada future test **2026** yang belum pernah disentuh Study 1.
- Banyak literatur LSTM+Optuna masih memakai **forecast harga** dan split tunggal; sedikit yang secara eksplisit menyiapkan **HPO + walk-forward terpurge** untuk **realized volatility** berbasis intraday.

Ini bukan nol termalin; ini gap **metodologis**:

> LSTM+Optuna yang diterapkan pada **realized volatility harian Bitcoin** dengan protokol **purged rolling-origin CV** dan **external test 2026**.

## 2. Pertanyaan penelitian Study 2

**RQ.** Apakah LSTM yang dioptimasi Optuna, dipakai untuk peramalan **daily realized volatility Bitcoin**, bisa lebih baik daripada baseline persistence dan HAR-RV pada external test 2026 dengan protokol bebas leakage?

## 3. Novelty Study 2 dibanding Study 1

| Aspek | Study 1 | Study 2 |
|---|---|---|
| Target | Harga harian | **Log realized variance** |
| Data harian | Binance daily close | **Binance 1h monthly kline**, agregasi harian |
| CV | Purged TimeSeriesSplit | **Purged rolling-origin CV** |
| Test | 2024-10-19 s.d. 2025-12-31 | **2026-01-01 s.d. 2026-09-30** |
| Success criteria | Model tidak mengalahkan persistence | **QLIKE LSTM < persistence dan HAR-RV**, CI 95% seluruhnya di bawah nol |

Ini bukan pivot kosong. Study 1 tetap jadi **eviden bahwa HPO bukan jaminan**; Study 2 menguji apakah pada target yang sinyalnya jelas, LSTM+Optuna bisa positif tanpa kebocoran.

## 4. Kenapa ini bisa jadi "positive result" yang defensible

1. **Target punya memori** jauh lebih kuat dari harga.
2. **Baseline HAR-RV** adalah baseline standar di literatur volatilitas.
3. **External test 2026** belum digunakan untuk apa pun selain penyediaan data mentah.
4. **Success criteria diungkap sebelum eksperimen**, bukan setelah lihat hasil.
5. **Multi-seed** dimainkan, tapi primary endpoint memakai **seed-averaged forecast**, bukan seed terbaik.

## 5. Klaim yang boleh ditulis dari hasil ini

Kalau **sukses**:

- LSTM+Optuna dapat meningkatkan QLIKE secara signifikan dibanding persistence dan HAR-RV.
- Bisa diklaim sebagai **positive result** pada pertanyaan utama Study 2.

Kalau **gagal**:

- Tetap jujur. Kita laporkan bahwa LSTM+Optuna tidak mengalahkan baseline ongkos target ini.
- Tidak ada pengubahan baseline atau metrik setelah lihat hasil.

---
