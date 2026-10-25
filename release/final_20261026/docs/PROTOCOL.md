# PROTOKOL EVALUASI — LSTM + Optuna Bitcoin

**Status:** dikunci pada 2026-10-25 (Fase 2).  
**Berlaku untuk:** seluruh eksperimen baru di `05_Source_Code/results/runs/{run_id}/`.  
**Tidak berlaku surut:** angka pada `results/` lama tetap dibekukan dan diberi label pra-perbaikan.

---

## 1. Dataset dan pembagian data

| Partisi | Jumlah | Periode | Fungsi |
|---|---:|---|---|
| Mentah | 2.192 | 2020-01-01 s.d. 2025-12-31 | Sumber tunggal, harian, tanpa celah |
| In-sample | 1.753 | 2020-01-01 s.d. 2024-10-18 | CV, tuning, pelatihan akhir |
| Out-of-sample (holdout) | 439 | 2024-10-19 s.d. 2025-12-31 | Evaluasi final saja |

Aturan:

1. Split bersifat kronologis 80:20, tanpa pengacakan.
2. Holdout **hanya** dibaca pada evaluasi model final. Tidak boleh dipakai untuk memilih lookback, arsitektur, learning rate, epoch, threshold, atau varian fitur.
3. Semua keputusan desain memakai data in-sample saja.
4. Tanggal, jumlah baris, dan hash data dicatat di `manifest.json`, `data_hash.json`, dan `preprocessing_metadata.json`.
5. Jika ada data baru setelah 2025-12-31, protokol ini harus ditinjau ulang; jangan menambal holdout secara diam-diam.

Kontrak dataset dijaga oleh `tests/test_data.py` dan `config.py` (`EXPECTED_*`, `TEST_START_DATE`, `TEST_END_DATE`).

---

## 2. Cross-validation untuk tuning (Tier 3)

Tier 3 memakai *purged expanding-window* time-series cross-validation:

- Deret masukan: harga penutupan **mentah (USD)** in-sample, bukan data yang sudah diskalakan global.
- `TimeSeriesSplit(n_splits=5)`: setiap fold melatih pada masa lalu dan memvalidasi pada blok setelahnya.
- **Purge gap = lookback trial tersebut.** Tidak ada observasi mentah yang dipakai bersama oleh window latih dan window validasi.
- **Scaler per fold:** `MinMaxScaler` di-fit hanya pada nilai mentah fold latih. Fold validasi ditransformasi dengan scaler yang sama.
- Prediksi validasi di-*inverse transform* ke USD, lalu dihitung MAE. Objective Optuna = rata-rata MAE USD antar fold.
- Window validasi boleh memakai observasi tepat sebelum blok validasi sebagai sejarah masukan (tersedia saat peramalan), tetapi observasi tersebut tidak termasuk blok latih karena adanya gap.
- Holdout tidak pernah masuk ke `cv_utils.py`.

Bukti implementasi: `cv_utils.py`, `tests/test_cv.py`, dan atribut trial `fold_metrics_usd`, `cv_protocol`, `cv_gap` pada database Optuna.

### Mengapa bukan scaler global?

Scaler global pada seluruh in-sample membuat statistik min/max masa depan (relative to each fold) bocor ke fold yang lebih awal. Per-fold scaler menghilangkan kebocoran itu. Konsekuensinya, nilai CV antar-trial hanya sebanding jika protokol ini dipakai untuk semua trial.

---

## 3. Pelatihan model final

| Tahap | Data latih | Validasi internal | Data uji |
|---|---|---|---|
| Tier 1 | 1.753 in-sample | `validation_split=0.1` dari in-sample | 439 holdout |
| Tier 2 | 1.753 in-sample | `validation_split=0.1` dari in-sample | 439 holdout |
| Tier 3 | 1.753 in-sample | `validation_split=0.1` dari in-sample | 439 holdout |

- Scaler final di-fit pada 1.753 harga in-sample saja, lalu dipakai untuk holdout.
- `validation_split=0.1` dipakai untuk EarlyStopping/ModelCheckpoint; ini bukan data uji.
- Model terbaik dipilih berdasarkan `val_loss`, bukan performa holdout.
- Holdout dievaluasi satu kali setelah model dibekukan.

Catatan keterbatasan: `validation_split=0.1` mengambil 10% terakhir secara kronologis, sehingga masih ada kemungkinan optimism kecil pada pemilihan epoch. Untuk klaim final, variasi ini harus dilaporkan, bukan disembunyikan.

---

## 4. Multi-seed

- Seed utama: `--seed` (default 42).
- Repetisi: `--seeds 42,123,2024,7,99`.
- Tier 1/2/3 melatih ulang konfigurasi final untuk setiap seed dan menyimpan prediksi per seed.
- Artefak utama (`metrics_tier*.json`, `predictions_tier*.csv`) tetap memakai seed utama agar kompatibel.
- Agregat ditulis ke `predictions/seed_metrics_tier*.json`:

```json
{
  "seeds": [42, 123, 2024],
  "per_seed": {"42": {"RMSE": 0, "MAE": 0, "MAPE": 0}},
  "aggregate": {"RMSE": {"mean": 0, "std": 0, "min": 0, "max": 0, "n_seeds": 3}}
}
```

- Angka yang dilaporkan di naskah harus menyebut jumlah seed dan statistik yang dipakai (mean ± std). Jangan memilih seed terbaik.
- Perbedaan antar-seed adalah variasi inisialisasi/pelatihan, bukan ketidakpastian sampling holdout.

---

## 5. Metrik

Untuk setiap hari uji \(t\):

\[
e_t = y_t - \hat{y}_t
\]

\[
\mathrm{RMSE} = \sqrt{\frac{1}{n}\sum_{t=1}^{n} e_t^2}, \quad
\mathrm{MAE} = \frac{1}{n}\sum_{t=1}^{n} |e_t|, \quad
\mathrm{MAPE} = \frac{100}{n}\sum_{t=1}^{n} \left|\frac{e_t}{y_t}\right|
\]

- Satuan RMSE/MAE: USD. MAPE: persen.
- Semua metrik dihitung pada 439 prediksi holdout yang tanggalnya identik antar tier.
- `06_evaluate_and_compare.py` menghitung ulang metrik dari CSV prediksi dan menolak JSON yang tidak konsisten (> 0.05 selisih).
- MAPE dilaporkan karena lazim di literatur, tetapi tidak dipakai sebagai satu-satunya dasar pemilihan model; harga Bitcoin mendekati nol secara relatif tidak terjadi pada periode uji, namun tetap perlu kehati-hatian.

---

## 6. Ketidakpastian dan perbandingan

### 6.1 Bootstrap CI

- Metode: *moving-block bootstrap percentile*.
- Blok: 7 hari (menjaga dependensi serial jangka pendek).
- Resample: 2.000.
- Tingkat kepercayaan: 95%.
- Seed bootstrap: 42 (deterministik).
- Output: `estimate`, `ci_low`, `ci_high`, `std_error` untuk RMSE/MAE/MAPE tiap tier.
- CI ini menggambarkan ketidakpastian sampling pada 439 hari holdout, **bukan** variasi antar-seed.

### 6.2 Perbandingan berpasangan

- `paired_bootstrap_difference` menghitung CI untuk `metric(B) - metric(A)` pada tanggal yang sama.
- Nilai negatif berarti B lebih baik.
- `p_value` adalah ukuran stabilitas bootstrap dua sisi; bukan pengganti uji formal dan tidak boleh disebut "signifikan" tanpa desain uji yang sesuai.
- Perbandingan harus menyebut pasangan model, metrik, dan arah selisih.

---

## 7. Aturan pelaporan

1. Jangan menyebut Tier 3 "juara" atau "lebih baik" hanya dari titik estimasi. Gunakan CI dan perbandingan berpasangan.
2. Jangan membandingkan Tier 1/2/3 yang masih berbeda loss/scheduler sebagai bukti efek Optuna. Perbedaan itu adalah *confound* dan harus dihilangkan pada matriks eksperimen Fase 3.
3. Baseline persistence/naif wajib ada sebelum klaim peningkatan.
4. Setiap angka di naskah harus dapat dilacak ke `run_id`, file metrik, dan hash data.
5. Angka pra-perbaikan hanya boleh muncul dengan label "sebelum perbaikan" dan tidak boleh dicampur dengan angka baru.
6. Jangan menulis ulang naskah sebelum angka final dikunci (Fase 5–6).

---

## 8. Reproduksi

```bash
# Uji cepat mekanika pipeline (bukan bukti ilmiah)
python 05_Source_Code/model_experiment/run_pipeline.py --all --reuse-data \
  --run-id smoke_check --trials 1 --epochs 1 --screening-epochs 1 --cv-splits 2

# Eksperimen penuh dengan multi-seed
python 05_Source_Code/model_experiment/run_pipeline.py --all \
  --run-id final_tier3 --trials 50 --epochs 100 --seeds 42,123,2024,7,99
```

Setiap run menghasilkan:

```
results/runs/{run_id}/
  manifest.json          # status, konfigurasi, hash input/output
  config.json            # konfigurasi per stage
  env.json               # versi Python/paket
  git.json / git_commit.txt
  data_hash.json / data_hash.txt
  metrics/
  predictions/
  figures/
  models/
  logs/
  optuna_study.db
  optuna_trials_history.csv
  summary.json
  benchmark_comparison_table.csv
```

---

## 9. Matriks eksperimen terkontrol

Perbandingan Tier 1 vs Tier 3 tidak boleh dipakai sebagai bukti efek Optuna karena loss dan scheduler berbeda. `experiment_matrix.py` mendefinisikan desain faktorial berikut pada parameter Tier 3 yang dibekukan (`config.TIER3_CONFIG`):

| Run | Model | Loss | Scheduler | HPO | Peran |
|---|---|---|---|---|---|
| E0 | Persistence | - | - | - | Baseline naif |
| E1 | Tier 1 default | MSE | Tidak | Tidak | Kontrol |
| E2 | Tier 2 manual | MSE | Tidak | Tidak | Pembanding literatur |
| E3 | Tier 3 params | MSE | Tidak | Tidak | Referensi ablation |
| E4 | Tier 3 params | MAE | Tidak | Tidak | Efek loss |
| E5 | Tier 3 params | MSE | Ya | Tidak | Efek scheduler |
| E6 | Tier 3 params | MAE | Ya | Tidak | Efek gabungan |
| E7 | Tier 3 HPO | MAE | Ya | Ya | Model usulan |

Aturan:

1. E3–E6 hanya boleh berbeda pada `--loss` dan `--scheduler`.
2. Semua run memakai split 1.753/439, `validation_split=0.1`, max epoch, `patience` yang sama (default 12), dan seed set yang sama.
3. E1 vs E3 mengisolasi hyperparameter; E4/E5 vs E3 mengisolasi loss/scheduler; E7 vs E6 mengisolasi HPO penuh.
4. E7 adalah model usulan; E3–E6 adalah ablation dan tidak boleh dipresentasikan sebagai kandidat model final.
5. Hasil ditulis ke `experiment_matrix_plan.json`, `experiment_matrix_results.json`, dan `experiment_matrix_results.csv` di run yang sama.

```bash
python 05_Source_Code/model_experiment/experiment_matrix.py --list
python 05_Source_Code/model_experiment/experiment_matrix.py --dry-run
python 05_Source_Code/model_experiment/experiment_matrix.py \
  --run-id matrix_final --seeds 42,123,2024,7,99
```

---

## 10. Analisis residual, rezim, dan arah

`08_analyze_results.py` menghasilkan analisis tambahan dari prediksi holdout:

1. **Residual:** `e_t = y_t - yhat_t`, ringkasan mean/std/min/max, kuantil 5/25/50/75/95, skewness, excess kurtosis, share error dalam 1%/2%/5%, dan 5 worst-case.
2. **Rezim ex-ante:** label hari `t` memakai trailing 30-day return sampai `t-1`:
   - bull: > +5%,
   - bear: < -5%,
   - sideways: selain itu.
3. **Volatilitas tinggi:** standar deviasi 7 return log harian sampai `t-1`, dibandingkan ambang persentil ke-75 in-sample. Label ini hanya untuk analisis, bukan input model.
4. **Directional accuracy:** `sign(yhat_t - y_{t-1})` dibandingkan `sign(y_t - y_{t-1})`; hari dengan `y_t = y_{t-1}` dikeluarkan. Baseline persistence selalu memprediksi flat, sehingga directional accuracy-nya tidak bermakna dan tidak boleh dibandingkan seolah-olah sama.
5. **Output:** `summary_final.json`, `residual_analysis.json`, `benchmark_matrix_table.csv/.md`, dan tiga figure. `--publish` hanya diizinkan bila seluruh E0–E7 tersedia dan status matriks `success`.

`summary_final.json` adalah sumber angka untuk naskah (Fase 5), bukan `README` lama atau angka pra-perbaikan.

---

## 11. Keputusan yang masih terbuka

| Keputusan | Status | Catatan |
|---|---|---|
| Versi Python/TensorFlow stabil | terbuka | environment sekarang Python 3.14.7 + TF 2.22.0rc0 |
| Clean-room install | belum diuji | butuh unduhan TensorFlow besar |
| Baseline persistence | selesai Fase 3 | masuk tabel, gambar, CI, dan paired difference |
| Matriks eksperimen loss/scheduler | selesai Fase 3 | E0–E7 di `experiment_matrix.py`; run final Fase 4 |
| Uji statistik formal | dipertimbangkan Fase 4 | bootstrap sudah tersedia |
| Jumlah seed final | rekomendasi 5 | `42,123,2024,7,99` |

Perubahan protokol setelah tanggal ini harus dicatat di bagian ini dan di `TODOFUTURES.MD`, bukan dilakukan diam-diam.
