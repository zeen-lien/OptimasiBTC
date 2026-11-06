# Matriks Keterlacakan (Traceability Matrix) Study 2: Volatilitas Bitcoin

Dokumen ini memetakan hubungan dua arah antara **Subbab Naskah Skripsi**, **Ketentuan Protokol Praregistrasi**, **Implementasi Kode Sumber**, **Pengujian Unit**, dan **Artefak Bukti**.

---

## 1. Matriks Penelusuran Metode Skripsi (Bab 3)

| ID | Bagian Skripsi | Bagian Protokol | Modul & Simbol Kode | Pengujian Unit | Artefak Bukti |
|---|---|---|---|---|---|
| TR-01 | **Bab 3 §3.1** — Desain Penelitian & Alur Eksperimen | Protokol §0, §10 | `s2_config.py`<br>`s2_runlog.py:new_run` | `tests/test_study2.py`<br>`tests/test_provenance.py` | `docs/STUDY2_PROTOCOL.md`<br>`docs/STUDY2_PROTOCOL_HASH.txt` |
| TR-02 | **Bab 3 §3.2** — Sumber Data, Pengunduhan & Amandemen A1 | Protokol §1, §11 (A1) | `s2_data.py:download_month`<br>`s2_data.py:load_month_zip`<br>`s2_data.py:aggregate_daily` | `tests/test_study2.py:test_daily_shape_and_boundaries`<br>`tests/test_s2_split_scaler.py:test_build_samples_rejects_gaps_and_nans_in_fixtures` | `05_Source_Code/data/study2/raw_zips_manifest.json`<br>`05_Source_Code/data/study2/data_freeze_hash.txt`<br>`05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv` |
| TR-03 | **Bab 3 §3.3** — Definisi Target & Rekayasa Fitur Volatilitas | Protokol §2 | `s2_data.py:aggregate_rv`<br>`s2_models.py:build_samples` | `tests/test_study2.py:test_features_no_future_leakage`<br>`tests/test_s2_split_scaler.py:test_build_samples_target_and_date_invariants` | `05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv` |
| TR-04 | **Bab 3 §3.4** — Pembagian Temporal & Kontrak Anti-Leakage | Protokol §3 | `s2_config.py:DEV_START..TEST_END`<br>`s2_models.py:fit_scaler`<br>`s2_models.py:transform_xy`<br>`s2_final_run.py:internal_val_split` | `tests/test_s2_split_scaler.py:test_scaler_fit_strictly_isolated_to_training`<br>`tests/test_s2_split_scaler.py:test_internal_val_split_contract` | `05_Source_Code/study2_volatility/s2_config.py` |
| TR-05 | **Bab 3 §3.5** — Baseline Primer: Persistence | Protokol §4 (1) | `s2_final_run.py:persistence_predictions` | `tests/test_s2_calendar.py:test_persistence_skips_target_when_prior_observation_crosses_gap` | `results/study2/runs/*/predictions_baselines_*.csv` |
| TR-06 | **Bab 3 §3.5** — Baseline Primer: HAR-RV (Corsi 2009) | Protokol §4 (2) | `s2_models.py:har_design`<br>`s2_models.py:har_fit_predict` | `tests/test_study2.py:test_har_beta_plausible`<br>`tests/test_s2_calendar.py:test_har_design_skips_windows_crossing_missing_calendar_day` | `results/study2/runs/*/predictions_baselines_*.csv` |
| TR-07 | **Bab 3 §3.5** — Baseline Sekunder: GARCH(1,1) Expanding | Protokol §4 (3) | `s2_models.py:daily_log_returns_after_last_gap`<br>`s2_models.py:garch_forecasts` | `tests/test_s2_calendar.py:test_garch_daily_returns_restart_after_gap_without_multiday_return`<br>`tests/test_s2_calendar.py:test_garch_forecasts_causal_to_future_gaps` | `results/study2/runs/*/predictions_baselines_*.csv` |
| TR-08 | **Bab 3 §3.5** — Model Usulan: Arsitektur LSTM | Protokol §4 (4, 5) | `s2_models.py:build_lstm_model`<br>`s2_models.py:train_one` | `tests/test_study2.py`<br>`tests/test_s2_split_scaler.py` | `results/study2/runs/*/metrics_lstm_*.json` |
| TR-09 | **Bab 3 §3.6** — HPO: Optuna TPE & Purged CV | Protokol §5 | `s2_optuna_search.py:sample_params`<br>`s2_optuna_search.py:cv_qlike` | `tests/test_s2_split_scaler.py:test_timeseries_split_purge_gap_exact_count_and_causal_boundaries` | `results/study2/runs/*/best_params.json`<br>`results/study2/runs/*/trials.csv` |
| TR-10 | **Bab 3 §3.6** — Pelatihan Final Multi-Seed (5 Seed) | Protokol §6 | `s2_final_run.py:run_lstm_variant`<br>`s2_config.py:SEEDS` | `tests/test_study2.py` | `results/study2/runs/*/predictions_lstm_*.csv` |
| TR-11 | **Bab 3 §3.7** — Metrik Primer QLIKE (Patton 2011) & Sekunder | Protokol §7 | `s2_stats.py:qlike_per_obs`<br>`s2_stats.py:qlike`<br>`s2_stats.py:mae_rmse_logrv` | `tests/test_study2.py:test_qlike_zero_at_perfect_and_nonnegative`<br>`tests/test_study2.py:test_qlike_asymmetric_penalty` | `results/study2/runs/*/metrics_*.json` |
| TR-12 | **Bab 3 §3.7** — Uji Hipotesis Diebold-Mariano (HAC Newey-West) | Protokol §8 | `s2_stats.py:dm_test` | `tests/test_study2.py:test_dm_test_sign_and_p` | `results/study2/runs/*/results_analysis.json` |
| TR-13 | **Bab 3 §3.7** — Moving-Block Bootstrap CI (Künsch 1989) | Protokol §8 | `s2_stats.py:moving_block_bootstrap_mean_ci` | `tests/test_study2.py:test_bootstrap_ci_contains_mean_and_p_direction` | `results/study2/runs/*/results_analysis.json` |

---

## 2. Matriks Penelusuran Hasil dan Pembahasan (Bab 4)

| ID | Bagian Skripsi | Ketentuan Protokol | Modul & Simbol Kode | Pengujian Unit | Artefak Bukti |
|---|---|---|---|---|---|
| TR-14 | **Bab 4 §4.1** — Validasi Penyelarasan Prediksi | Fail-Closed Check | `s2_analyze.py:validate_prediction_alignment` | `tests/test_s2_analyze.py:test_validate_prediction_alignment_accepts_equal_date_sets_and_targets`<br>`tests/test_s2_analyze.py:test_validate_prediction_alignment_rejects_invalid_frames` | `results/study2/runs/*/results_analysis.json` |
| TR-15 | **Bab 4 §4.2** — Evaluasi Performa Out-of-Sample 2026 | Protokol §9 | `s2_analyze.py:eval_pair`<br>`s2_analyze.py:analyze_window` | `tests/test_study2.py`<br>`tests/test_s2_analyze.py` | `results/study2/runs/*/results_analysis.json`<br>`results/study2/runs/*/results_analysis.md` |
| TR-16 | **Bab 4 §4.3** — Analisis Diagnostik & Stabilitas Seed | Protokol §6, §9 | `s2_analyze.py:analyze_window` (per-seed metrics) | `tests/test_study2.py` | `results/study2/runs/*/results_analysis.json` |
| TR-17 | **Bab 4 §4.4** — Keterbatasan dan Provenance Riwayat Paparan | Protokol §10 | `docs/STUDY2_PROVENANCE.md`<br>`docs/AUDIT_FINDINGS_STUDY2_20261029.md` | `tests/test_provenance.py` | `docs/STUDY2_PROVENANCE.md` |

---

## 3. Catatan Kepatuhan dan Batasan Metodologi Terbuka

1. **Purge Gap CV:** `docs/STUDY2_PROTOCOL.md` menuliskan `gap = lookback` (0 overlap target-fitur). Kode operasional menggunakan `gap = lookback + 1` (membuang 1 hari ekstra). Keduanya telah diuji di `tests/test_s2_split_scaler.py:test_timeseries_split_purge_gap_exact_count_and_causal_boundaries`.
2. **Refit Final:** Kode final melatih LSTM pada 90% kumpulan data latih dan menggunakan 10% untuk early stopping kronologis internal (`internal_val_split`), diuji di `tests/test_s2_split_scaler.py:test_internal_val_split_contract`.
3. **Celah Kalender GARCH:** Peramalan GARCH dibatasi ke `<= window_end` untuk mencegah celah masa depan memotong data historis, diuji di `tests/test_s2_calendar.py:test_garch_forecasts_causal_to_future_gaps`.

