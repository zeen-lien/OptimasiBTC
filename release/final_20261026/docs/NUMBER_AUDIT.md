# Audit Angka Naskah

Dokumen ini dihasilkan otomatis oleh
`05_Source_Code/generators/build_number_audit.py` dari
`05_Source_Code/results/summary_final.json`. Jangan mengedit manual.

## 1. Sumber Tunggal

| Item | Nilai |
|---|---|
| Run ID | `final_matrix_20261025` |
| Summary | `D:\OneDrive\Desktop\jurnal\05_Source_Code\results\summary_final.json` |
| SHA-256 summary | `b9274477bed648e3f45c89d1f15325c5432a2694945b71329914190005f8f7fb` |
| Jumlah observasi | 1.753 in-sample + 439 holdout = 2.192 |
| Periode data | 2020-01-01 s.d. 2025-12-31 |
| Periode holdout | 2024-10-19 s.d. 2025-12-31 |
| Bootstrap | moving block 7 hari, 2.000 resample, CI 95% |
| Seed | 5 seed |

## 2. Statistik Deskriptif Data

| Parameter | Nilai | Sumber |
|---|---:|---|
| Harga minimum | USD 4.800,00 | `data.statistics.min` |
| Tanggal minimum | 2020-03-12 | `data.statistics.min_date` |
| Harga maksimum | USD 124.658,54 | `data.statistics.max` |
| Tanggal maksimum | 2025-10-06 | `data.statistics.max_date` |
| Rata-rata | USD 47.182,88 | `data.statistics.mean` |
| Median | USD 39.732,62 | `data.statistics.median` |
| Simpangan baku | USD 31.418,23 | `data.statistics.std` |

## 3. Baseline dan Model

| Run | Model | RMSE | MAE | MAPE | CI 95% MAE | Std MAE antar-seed | n seed |
|---|---|---:|---:|---:|---:|---:|---:|
| E0 | Persistence | USD 2.167,24 | USD 1.579,80 | 1,62% | USD 1.437,83–USD 1.742,58 | 0,00 | 1 |
| E1 | Tier 1 default | USD 2.519,46 | USD 1.968,00 | 1,98% | USD 1.823,08–USD 2.150,40 | 196,57 | 5 |
| E2 | Tier 2 manual | USD 3.491,05 | USD 2.892,27 | 2,87% | USD 2.688,41–USD 3.169,33 | 399,48 | 5 |
| E3 | Ablasi MSE / tanpa scheduler | USD 2.994,73 | USD 2.452,53 | 2,43% | USD 2.280,41–USD 2.672,47 | 163,11 | 5 |
| E4 | Ablasi MAE / tanpa scheduler | USD 2.328,70 | USD 1.763,47 | 1,79% | USD 1.633,82–USD 1.927,38 | 167,38 | 5 |
| E5 | Ablasi MSE / ReduceLROnPlateau | USD 2.591,70 | USD 2.043,10 | 2,05% | USD 1.902,38–USD 2.225,68 | 78,61 | 5 |
| E6 | Ablasi MAE / ReduceLROnPlateau | USD 2.234,46 | USD 1.667,26 | 1,70% | USD 1.537,90–USD 1.825,72 | 67,48 | 5 |
| E7 | Tier 3 HPO penuh (usulan) | USD 2.250,06 | USD 1.687,49 | 1,72% | USD 1.560,55–USD 1.841,42 | 89,97 | 5 |

Sumber: `models.{E0..E7}.metrics`, `models.{E0..E7}.confidence_intervals.MAE`, dan `models.{E1..E7}.multi_seed.aggregate.MAE`.

## 4. Baseline Naif

| Baseline | RMSE | MAE | MAPE | Sumber |
|---|---:|---:|---:|---|
| persistence | USD 2.167,24 | USD 1.579,80 | 1,62% | `baselines.persistence.metrics` |
| drift | USD 2.166,82 | USD 1.579,59 | 1,62% | `baselines.drift.metrics` |
| seasonal_naive_7 | USD 5.404,67 | USD 4.128,13 | 4,22% | `baselines.seasonal_naive_7.metrics` |
| moving_average_7 | USD 3.484,84 | USD 2.645,28 | 2,71% | `baselines.moving_average_7.metrics` |

## 5. Ablasi Loss dan Scheduler

| Run | Loss | Scheduler | RMSE | MAE | MAPE | Delta MAE vs E3 |
|---|---|---|---:|---:|---:|---:|
| E3 | mse | none | USD 2.994,73 | USD 2.452,53 | 2,43% | +0,00% |
| E4 | mae | none | USD 2.328,70 | USD 1.763,47 | 1,79% | +28,10% |
| E5 | mse | plateau | USD 2.591,70 | USD 2.043,10 | 2,05% | +16,69% |
| E6 | mae | plateau | USD 2.234,46 | USD 1.667,26 | 1,70% | +32,02% |

Delta positif berarti MAE lebih rendah daripada E3. Sumber: `models.{E3..E6}.metrics` dan `improvement_vs.e3`.

## 6. Perbandingan Berpasangan

| Perbandingan | Arah | Selisih MAE (B - A) | CI 95% | Perubahan relatif |
|---|---|---:|---:|---:|
| E7_vs_persistence | E0 → E7 | USD +107,69 | USD +50,82–USD +170,90 | +6,82% |
| E7_vs_tier1 | E1 → E7 | USD -280,50 | USD -358,95–USD -210,94 | -14,25% |
| E7_vs_tier2 | E2 → E7 | USD -1.204,78 | USD -1.418,25–USD -1.013,51 | -41,66% |
| E7_vs_E6 | E6 → E7 | USD +20,23 | USD +1,22–USD +40,37 | +1,21% |
| E1_vs_E3 | E1 → E3 | USD +484,54 | USD +349,10–USD +627,30 | +24,62% |
| E4_vs_E3 | E3 → E4 | USD -689,06 | USD -839,71–USD -552,16 | -28,10% |
| E5_vs_E3 | E3 → E5 | USD -409,43 | USD -533,89–USD -293,39 | -16,69% |
| E6_vs_E3 | E3 → E6 | USD -785,27 | USD -960,55–USD -627,88 | -32,02% |
| E6_vs_E4 | E4 → E6 | USD -96,21 | USD -131,59–USD -65,43 | -5,46% |
| E6_vs_E5 | E5 → E6 | USD -375,84 | USD -472,32–USD -291,98 | -18,40% |

Selisih negatif berarti model B lebih baik. CI adalah moving-block bootstrap pada tanggal yang sama; `p_value` bukan uji formal.

## 7. Verdict Ilmiah

| Item | Nilai | Sumber |
|---|---|---|
| Status | `proposed_not_better_than_persistence` | `headline.status` |
| Metrik utama | MAE | `primary_metric` |
| MAE E7 vs persistence | -6,82% | `models.E7.metrics.MAE` vs `models.E0.metrics.MAE` |
| CI selisih E7-persistence | USD +50,82–USD +170,90 | `paired_comparisons.E7_vs_persistence.metrics.MAE` |
| Terbaik keseluruhan (MAE) | E0 (USD 1.579,80) | `best_by_mae` |
| LSTM terbaik (MAE) | E6 (USD 1.667,26) | `lstm_ranking_by_mae[0]` |

> E7 memiliki MAE lebih tinggi daripada persistence dan CI selisih berpasangan seluruhnya di atas nol, sehingga hasil ini secara statistik lebih buruk. Laporkan hasil negatif ini secara eksplisit dan jangan memilih baseline yang menguntungkan.

## 8. Konfigurasi Final E7

| Parameter | Nilai | Sumber |
|---|---:|---|
| Lookback | 25 hari | `final_configuration.hyperparameters.lookback` |
| Units | 112 | `final_configuration.hyperparameters.units` |
| Dropout | 0,10 | `final_configuration.hyperparameters.dropout` |
| Learning rate | 0,00128 | `final_configuration.hyperparameters.learning_rate` |
| Batch size | 16 | `final_configuration.hyperparameters.batch_size` |
| Layers | 1 | `final_configuration.hyperparameters.layers` |
| Epoch berjalan | 100 | `final_configuration.epochs_run` |
| Total trials | 50 | `final_configuration.total_trials` |
| Trial terbaik | 27 | `final_configuration.best_trial_number` |
| CV loss terbaik | 1.092,79 | `final_configuration.best_cv_loss` |
| Waktu optimasi | 2.427,0 detik | `final_configuration.optimization_time_seconds` |
| Waktu latih final | 237,9 detik | `final_configuration.training_time_seconds` |

## 9. Environment

| Paket | Versi |
|---|---|
| python_version | 3.14.7 |
| tensorflow | 2.22.0rc0 |
| optuna | 5.0.0 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| matplotlib | 3.11.2 |
| python-docx | 1.2.0 |

## 10. Larangan Angka Lama

Angka berikut berasal dari snapshot pra-perbaikan dan **tidak boleh** muncul sebagai hasil final:

| Angka lama | Konteks | Status |
|---|---|---|
| RMSE 2.338,22 / MAE 1.784,27 / MAPE 1,81% | Tier 3 pra-perbaikan | Diganti angka E7 final |
| Best trial #44, lookback 14, units 80 | Konfigurasi pra-perbaikan | Diganti konfigurasi E7 final |
| Split 85% | Replikasi Tier 2 lama | Diganti split 80:20 (1.753/439) |
| Batch 10 / units 128 sebagai klaim kausal | Narasi lama | Dihapus atau dijadikan deskriptif |

Verifikasi otomatis ada di `verify_full_skripsi.py`.
