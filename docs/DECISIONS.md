# Catatan Keputusan Ilmiah

Dokumen ini mencatat keputusan yang mengubah arah eksperimen, beserta alasannya.
Keputusan yang sudah dikunci tidak boleh diubah diam-diam; perubahan harus
ditambahkan sebagai entri baru dan disinkronkan ke `TODOFUTURES.MD` serta
`docs/PROTOCOL.md`.

| ID | Tanggal | Keputusan | Alasan | Dampak |
|---|---|---|---|---|
| D1 | 2026-10-25 | Membekukan seluruh artefak lama di `archive/pre_perbaikan_20261025/` dan menandainya dengan tag `pre-perbaikan-20261025`. | Angka lama tidak boleh tertimpa atau tercampur dengan hasil perbaikan. | Semua run baru wajib menulis ke `05_Source_Code/results/runs/{run_id}/`; mode `--legacy` hanya untuk reproduksi eksplisit. |
| D2 | 2026-10-25 | Memisahkan data in-sample (1.753 hari) untuk CV/tuning dan holdout (439 hari) hanya untuk evaluasi akhir. | Tuning yang menyentuh holdout membuat metrik uji optimistis dan tidak sah. | Optuna, pemilihan parameter, dan early stopping internal CV tidak pernah membaca holdout. |
| D3 | 2026-10-25 | CV tuning memakai `TimeSeriesSplit` berpurge dengan `gap = lookback` dan scaler `MinMaxScaler` yang di-fit ulang pada setiap fold. | Window fitur dan target dapat berbagi observasi mentah; scaler global membocorkan informasi masa depan. | Setiap fold memiliki scaler sendiri; prediksi validasi di-inverse-transform ke USD sebelum dihitung MAE. |
| D4 | 2026-10-25 | Metrik evaluasi dihitung dalam USD, bukan pada skala ternormalisasi. | RMSE/MAE pada skala 0–1 tidak dapat ditafsirkan dan tidak sebanding dengan baseline. | RMSE/MAE bersatuan USD; MAPE dalam persen. Objective Optuna tetap MAE USD. |
| D5 | 2026-10-25 | Interval kepercayaan memakai moving-block bootstrap 7 hari, 2.000 resample, tingkat 95%, seed 42. | Residual deret waktu berkorelasi; bootstrap i.i.d. terlalu sempit. | CI menggambarkan ketidakpastian sampling holdout, bukan variasi antar-seed. |
| D6 | 2026-10-25 | Seed utama (`--seed`, default 42) menghasilkan artefak kanonik; seed repetisi (`--seeds`, default `42,123,2024,7,99`) dilaporkan sebagai mean ± std terpisah. | Variasi inisialisasi/pelatihan harus terlihat tanpa mengaburkan artefak utama. | Prediksi/metrik seed utama menjadi dasar tabel; agregat multi-seed disimpan di `multi_seed`/`seed_metrics_*`. |
| D7 | 2026-10-25 | Perbandingan Tier 1 vs Tier 3 lama tidak dipakai sebagai bukti efek Optuna karena loss dan scheduler berbeda. | Perbedaan itu confound, bukan efek hyperparameter. | Efek Optuna diisolasi oleh E1 vs E3 (MSE, tanpa scheduler, split dan aturan latih sama). |
| D8 | 2026-10-25 | Matriks E3–E6 memakai parameter Tier 3 yang dibekukan dan hanya memvariasikan loss/scheduler dalam desain faktorial 2x2. | Satu perbandingan harus mengisolasi satu faktor. | E3 = MSE/tanpa scheduler; E4 = MAE/tanpa scheduler; E5 = MSE/plateau; E6 = MAE/plateau. E7 adalah HPO penuh dan model usulan. |
| D9 | 2026-10-25 | Semua run matriks memakai `--epochs` dan `--patience 12` yang sama; standalone Tier 1/2 tetap default patience 10. | Early stopping yang berbeda dapat menciptakan perbedaan artefak, bukan efek faktor. | E1–E6 setara dalam aturan berhenti; E7 memakai aturan retrain Tier 3 yang sama. |
| D10 | 2026-10-25 | Label rezim dan volatilitas bersifat ex-ante: trailing 30-day return dan 7-day log-return std berakhir di `t-1`; ambang volatilitas = persentil 75 in-sample. | Label yang memakai data hari `t` akan membocorkan informasi dan membuat analisis error tidak valid. | Label hanya untuk analisis pasca-hoc, bukan input model atau klaim kausal. |
| D11 | 2026-10-25 | `08_analyze_results.py --publish` hanya menulis `results/summary_final.json` bila seluruh E0–E7 tersedia dan status matriks `success`. | Angka parsial atau gagal tidak boleh menjadi sumber klaim naskah. | Ringkasan parsial tetap boleh dibuat untuk smoke test dengan `--allow-partial`, tetapi tidak dipublikasikan. |
| D12 | 2026-10-25 | Verdict ilmiah memakai MAE sebagai metrik utama, dengan RMSE/MAPE dan CI berpasangan sebagai pendukung. | MAE adalah objective Optuna dan lebih robust terhadap outlier ekstrem dibanding RMSE. | Klaim "lebih baik" hanya boleh bila MAE titik lebih rendah dan CI selisih berpasangan tidak melewati nol; jika tidak, hasil dilaporkan negatif. |
| D13 | 2026-10-26 | Publikasi `summary_final.json` diverifikasi terhadap cakupan seed di `experiment_matrix_plan.json` dan hash `docs/PROTOCOL.md`/`requirements.txt` yang tercatat di `data_hash.json`. | Run dengan seed kurang atau protokol yang berubah setelah mulai tidak boleh menjadi sumber angka naskah. | `--publish` menolak run yang gagal verifikasi; protokol tidak boleh diedit selama run final berlangsung. |
| D14 | 2026-10-26 | Hasil final E0–E7 diambil dari `final_matrix_20261025`; E7 tidak mengalahkan persistence dan kontribusi di-reframe sebagai pipeline evaluasi dengan hasil negatif yang jujur. | E7 MAE 1.687,49 USD vs persistence 1.579,80 USD; CI selisih berpasangan +50,82 s.d. +170,90 USD seluruhnya di atas nol, sehingga E7 secara statistik lebih buruk. E6 adalah LSTM terbaik (1.667,26 USD). | Bab I/IV/V memakai verdict otomatis; klaim keunggulan model usulan dihapus. |

## Keputusan hasil Fase 4

**Status:** selesai pada 2026-10-26. Run `final_matrix_20261025` berstatus `matrix = success`; seluruh stage E0–E7 `success`; `summary_final.json` dipublikasikan.

### Status run

| Stage | Status |
|---|---|
| baseline (E0) | success |
| tier1 (E1) | success |
| tier2 (E2) | success |
| ablation E3–E6 | success |
| tier3 (E7) | success |
| matrix | success |

### Metrik holdout seed utama (439 hari)

| Run | RMSE (USD) | MAE (USD) | MAPE |
|---|---:|---:|---:|
| E0 persistence | 2.167,24 | 1.579,80 | 1,62% |
| E1 Tier 1 | 2.519,46 | 1.968,00 | 1,98% |
| E2 Tier 2 | 3.491,05 | 2.892,27 | 2,87% |
| E3 MSE / tanpa scheduler | 2.994,73 | 2.452,53 | 2,43% |
| E4 MAE / tanpa scheduler | 2.328,70 | 1.763,47 | 1,79% |
| E5 MSE / plateau | 2.591,70 | 2.043,10 | 2,05% |
| E6 MAE / plateau | 2.234,46 | 1.667,26 | 1,70% |
| E7 HPO penuh | 2.250,06 | 1.687,49 | 1,72% |

E7 multi-seed mean ± std: RMSE 2.321,54 ± 89,60; MAE 1.756,11 ± 89,97; MAPE 1,79 ± 0,09%.

### Perbandingan berpasangan utama (MAE, B − A)

| Perbandingan | Selisih (USD) | CI 95% (USD) | Arah |
|---|---:|---:|---|
| E7 vs persistence | +107,69 | +50,82 s.d. +170,90 | E7 lebih buruk |
| E7 vs E6 | +20,23 | +1,22 s.d. +40,37 | E7 lebih buruk |
| E1 vs E3 | +484,54 | +349,10 s.d. +627,30 | E3 lebih buruk |
| E4 vs E3 | -689,06 | -839,71 s.d. -552,16 | E4 lebih baik |
| E5 vs E3 | -409,43 | -533,89 s.d. -293,39 | E5 lebih baik |
| E6 vs E3 | -785,27 | -960,55 s.d. -627,88 | E6 lebih baik |

### Verdict

`proposed_not_better_than_persistence`. E7 memiliki MAE lebih tinggi daripada persistence dan CI selisih berpasangan seluruhnya di atas nol. Hasil dilaporkan sebagai negatif yang terverifikasi; kontribusi utama adalah pipeline evaluasi terkontrol, audit angka, dan bukti bahwa HPO tidak otomatis mengalahkan baseline naif pada horizon satu hari.

Keputusan ini tidak boleh diubah tanpa run baru dan pencatatan keputusan tambahan. Persetujuan pembimbing atas framing tetap bersifat eksternal.
