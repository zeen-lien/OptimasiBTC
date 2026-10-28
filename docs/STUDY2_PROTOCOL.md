# PROTOKOL STUDY 2 (FINAL, PRE-REGISTERED) — LSTM + Optuna untuk Peramalan Realized Volatility Bitcoin

**Dikunci:** 2026-10-28, sebelum data test 2026 dibangun dan sebelum satu pun model Study 2 dilatih.
**Branch:** `study2-volatility` (dari `main` @ `f3f9763`).
**Study 1:** tetap beku pada tag `v1.0-final`; tidak ada file/angka Study 1 yang diubah.

## 0. Catatan provenance pra-kunci

Sebelum protokol ini dikunci, dilakukan **validasi format** terhadap sejumlah file bulanan
Binance Vision (termasuk 2026-09): memeriksa jumlah baris, satuan timestamp (ms vs µs),
dan kelengkapan 24 bar/jam. **Tidak ada** statistik target (RV), fitur, atau hasil model
yang dihitung pada tahap itu. Setelah protokol dikunci dan di-hash, data diproses penuh dan dibekukan.

## 1. Data

- Sumber tunggal: Binance Vision, kline bulanan 1h spot `BTCUSDT`, 2020-01 s.d. 2026-09 (81 file).
- Timestamp dinormalisasi dari ms/µs ke UTC; agregasi per tanggal UTC.
- Syarat integritas: setiap hari memiliki tepat 24 bar 1h; kalender 2020-01-01..2026-09-30
  kontinu (2.465 hari) tanpa NaN. Jika dilanggar → pipeline berhenti (fail loudly), bukan diam-diam diperbaiki.
- Test window berakhir 2026-09-30 karena zip bulanan 2026-10 **belum diterbitkan** Binance
  (diperiksa 2026-10-28). Ini kendala data eksternal, bukan keputusan post-hoc.

## 2. Target dan fitur harian (definisi presisi)

Per hari UTC `t`, dari 24 bar 1h:

- `rv_t = Σ_h (log(close_h) − log(open_h))²`
- `log_rv_t = log(rv_t + 1e-12)` ← **target**
- `log_range_t = log(high_t / low_t)` dengan `high_t = max_h high_h`, `low_t = min_h low_h`
- `log_volume_t = log(volume_t + 1e-12)`, `volume_t = Σ_h volume_h`
- `log_absret_t = log(|log(close_t) − log(close_{t−1})| + 1e-12)`
- `rv_mean_5_t = mean(log_rv_{t−4..t})` (5 hari berakhir di t)
- `rv_mean_22_t = mean(log_rv_{t−21..t})` (22 hari berakhir di t)

Model memprediksi **`log_rv_{t+1}`** dari fitur hari ≤ t. Fitur input (6, tetap):
`log_rv, log_range, log_volume, log_absret, rv_mean_5, rv_mean_22`.

Aturan anti-leakage:
- Scaler (StandardScaler) dan standarisasi target di-fit **hanya pada data training fold**.
- Tidak ada fitur yang memakai informasi > t.
- Data 2026 tidak pernah dipakai untuk memilih hyperparameter, epoch, atau seed.

## 3. Split temporal

| Periode | Peran |
|---|---|
| 2020-01-01 .. 2023-12-31 | **Dev/HPO**: purged rolling-origin CV (5 fold, gap = lookback) |
| 2024-01-01 .. 2025-12-31 | **Validasi**: checkpoint pipeline & baseline; dilaporkan, tidak dipakai memilih apa pun |
| 2020-01-01 .. 2025-12-31 | **Train pool** untuk refit final semua model |
| 2026-01-01 .. 2026-09-30 | **Test eksternal** — dieksekusi satu kali setelah protokol & data di-hash |

## 4. Model / baseline (tetap, tidak boleh bertambah setelah lihat hasil)

1. **Persistence**: `ŷ_{t+1} = log_rv_t`.
2. **HAR-RV**: OLS `log_rv_{t+1} ~ log_rv_t + mean(log_rv_{t−6..t}) + mean(log_rv_{t−21..t})`, fit pada train pool.
3. **GARCH(1,1)**: pada log-return harian close ×100, dist Normal, QML; fit pada train pool,
   **refit expanding per awal bulan** selama test, one-step conditional variance → `log_var`.
4. **Untuned LSTM**: konfigurasi tetap `lookback=21, units=64, dropout=0.20, lr=1e-3, batch=32, layers=1`, tanpa Optuna.
5. **Optuna-LSTM (usulan)**: hyperparameter dari HPO bagian 5.

Baseline 1–2 adalah **primary baselines** (harus dikalahkan untuk sukses);
3–4 adalah secondary (dilaporkan, tidak menentukan sukses/gagal).

## 5. HPO (Optuna)

- `TPESampler(seed=42)`, **50 trial**, `MedianPruner(n_startup_trials=10, n_warmup_steps=2)`.
- Objective: **mean CV QLIKE** di 5 fold dev (2020–2023). Bukan MAE, bukan RMSE.
- Search space (tetap):
  - `lookback ∈ [10, 30]` (int)
  - `units ∈ [16, 128]` (int)
  - `layers ∈ {1, 2}`
  - `dropout ∈ [0.05, 0.40]` step 0.05
  - `learning_rate` log-uniform `[3e-4, 2e-3]`
  - `batch_size ∈ {16, 32, 64}`
- Pelatihan: `max_epochs=100`, EarlyStopping(patience=10, restore_best_weight pada val fold),
  loss MSE pada log-RV terstandarisasi.

## 6. Multi-seed

- Seeds: **42, 123, 2024, 7, 99** (identik Study 1).
- Hyperparameter terbaik dari HPO dipakai melatih ulang model final **per seed** pada train pool 2020–2025.
- **Primary endpoint memakai rata-rata forecast 5 seed** (mean of `ŷ_log_rv`), bukan seed terbaik.
- Metrik per-seed (mean/std/min/max) dilaporkan sebagai secondary.

## 7. Metrik evaluasi

- **Primary: QLIKE** pada skala log-variance (bentuk robust Patton):
  `QLIKE = mean_t [ exp(e_t) − e_t − 1 ]`, dengan `e_t = log_rv_t − ŷ_log_rv_t`.
  Selalu ≥ 0 per observasi; **lebih rendah lebih baik**.
- Secondary: MAE dan RMSE pada `log_rv`.

## 8. Inferensi statistik (pre-registered)

- **Diebold-Mariano**: pada selisih loss harian `d_t = QLIKE_t(model) − QLIKE_t(baseline)`,
  HAC Newey-West (Bartlett) **lag 5**, uji **satu sisi** (H1: model lebih baik → mean(d) < 0), α = 0.05.
- **Moving-block bootstrap**: block length **20 hari**, **10.000 reps**, seed **42**,
  CI 95% persentil untuk mean ΔQLIKE. Sukses menuntut **batas atas CI < 0**.
- Koreksi multi-perbandingan tidak diterapkan; hanya 2 uji primary (vs persistence, vs HAR-RV).

## 9. Kriteria sukses

**Positive** jika SEMUA terpenuhi pada test 2026 (seed-averaged forecast):
1. QLIKE(Optuna-LSTM) < QLIKE(persistence) **dan** < QLIKE(HAR-RV);
2. DM one-sided p < 0.05 untuk kedua perbandingan primary;
3. Batas atas CI 95% block-bootstrap ΔQLIKE < 0 untuk kedua perbandingan primary.

Selain itu dilaporkan apa adanya: `mixed` (beat sebagian baseline), `negative` (kalah dari persistence
atau HAR-RV). **Tidak ada** perubahan baseline, metrik, split, seed, atau test window setelah
hasil validasi/test terlihat. Hasil negatif tetap dilaporkan penuh.

## 10. Eksekusi & enforcement

1. Protokol ini di-hash SHA-256 → `docs/STUDY2_PROTOCOL_HASH.txt` sebelum data dibangun.
2. Fetch + agregasi + integrity check → CSV harian dibekukan + hash (raw & derived).
3. Smoke test (1 trial, 2 epoch) → lalu HPO penuh di dev; validasi 2024–2025; **test 2026 satu kali terakhir**.
4. Setiap run: `run_id`, manifest (git commit, hash data, hash protokol, env), seed tetap.
5. Verifier akhir: ulang-hitung hash protokol & data, cocokkan dengan manifest.

## 11. Amandemen (dicatat sebelum ada statistik target atau hasil model)

### A1 — Data integrity (2026-10-28)
Konteks: percobaan build pertama **gagal** pada integrity check sebelum nilai RV/fitur
terhitung — ditemukan 15 hari (2020-01..2023-03) dengan 19–23 bar 1h akibat jendela
maintenance Binance; tidak ada hari cacat di 2024-01-01..2026-09-30 (window validasi dan
test 100% 24 bar).

Aturan yang ditetapkan:
1. Hari dengan **n_bars < 20** dikeluarkan dari dataset (realisasi: hanya `2020-02-19`, 19 bar).
2. Hari dengan n_bars 20–23 **dipertahankan**; `rv`, `log_range` dihitung dari bar yang tersedia;
   kolom `n_bars` disimpan sebagai provenance.
3. Kalender hari yang tersisa harus kontinu kecuali hari yang dikeluarkan pada poin 1.
4. `log_absret` (butuh close_{t−1}) dan sampel sekuens yang melintasi celah kalender
   ditandai tidak-valid dan **dikeluarkan dari semua set training/evaluasi**.
   Window rolling (`rv_mean_5`, `rv_mean_22`) dihitung atas baris hari yang dipertahankan.
5. Persyaratan tambahan: semua hari di window validasi (2024–2025) dan test (2026)
   harus tepat 24 bar — jika tidak, pipeline berhenti.
6. Semua perubahan ini dilakukan **sebelum** satu pun nilai RV, fitur, atau metrik model
   dihitung/dilihat. Setelah hash protokol diperbarui (A1), data dibekukan dan tidak
   disentuh lagi hingga test 2026 dieksekusi.

