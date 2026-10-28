# TODO Perbaikan Skripsi & Pipeline
## Optimasi Hyperparameter LSTM dengan Optuna — Prediksi Harga Bitcoin

**Status dokumen (2026-10-26):** Fase 1–6 selesai dan diverifikasi; Fase 7 selesai sampai paket rilis dan tag `v1.0-final`, dengan empat item eksternal/tertunda (clean-room install, Turnitin, persetujuan pembimbing, backup cloud).  
**Tujuan:** memperbaiki validitas ilmiah, konsistensi naskah, dan reproducibility dari awal sampai siap sidang.  
**Prinsip:** bekukan bukti lama → perbaiki protokol → jalankan ulang → baru perbarui naskah dan referensi.  
**Hasil akhir:** E7 tidak mengalahkan persistence (MAE 1.687,49 vs 1.579,80 USD; CI selisih seluruhnya di atas nol). E6 adalah LSTM terbaik (MAE 1.667,26 USD). Kontribusi di-reframe sebagai pipeline terkontrol + hasil negatif yang jujur.

---

## 0. Ringkasan kondisi awal (arsip historis)

Bagian ini merekam kondisi sebelum perbaikan dan tidak lagi menjadi status aktif. Status terkini ada di kepala dokumen dan pada tiap fase.

Yang sudah benar dan perlu dipertahankan:

- Dataset mentah 2.192 baris (2020-01-01 s.d. 2025-12-31), tanpa null, duplikat tanggal, celah harian, atau pelanggaran OHLC.
- Split kronologis 1.753 in-sample / 439 out-of-sample.
- Metrik JSON cocok dengan prediksi CSV.
- Database Optuna konsisten: 50 trials, best trial #36 = lookback 22, units 100, dropout 0.1, LR 0.001966, batch 16.
- Tiga gambar hasil berukuran 300 DPI.

Masalah utama yang harus diselesaikan:

1. Belum ada baseline persistence/naif; baseline ini justru lebih baik daripada Tier 3.
2. Perbandingan Tier 1/2/3 tercampur dengan perubahan loss dan scheduler.
3. CV masih memakai scaler yang di-fit pada seluruh in-sample dan window antar-fold saling overlap.
4. Holdout pernah dipakai untuk keputusan desain (wide lookback dan LR screening).
5. Naskah, daftar gambar/tabel, lampiran, dan narasi metode tidak sinkron dengan kode/artefak.
6. Pipeline belum portabel, belum punya dependency lock, test, dan provenance run.
7. Beberapa PDF referensi tidak sesuai dengan nama/judul yang diklaim.

---

## 1. Urutan perbaikan yang direvisi

Urutan lama tidak salah substansinya, tetapi urutannya menimbulkan rework. Perbaikan engineering dan protokol harus lebih dulu, karena semua eksperimen dan angka naskah akan bergantung pada keputusan di sana.

| Urutan lama | Topik lama | Urutan baru | Alasan pemindahan |
|---:|---|---:|---|
| 1 | Baseline persistence | **3** | Baseline harus dijalankan setelah protokol split/CV disepakati. |
| 2 | Ablation study | **4** | Ablation baru bermakna setelah baseline dan protokol bersih. |
| 3 | Perbaikan CV | **2** | Ini prasyarat utama sebelum semua eksperimen diulang. |
| 4 | Pisahkan validation/holdout | **2** | Satu paket dengan perbaikan protokol evaluasi. |
| 5 | Sinkronisasi dokumen | **6** | Naskah baru boleh diubah setelah angka final stabil. |
| 6 | Engineering/reproducibility | **1** | Fondasi untuk menjalankan ulang eksperimen secara aman. |
| 7 | Audit referensi | **7** | Tetap terakhir, bersamaan dengan audit final dan packaging. |

### Urutan final

1. **Bekukan artefak + fondasi reproducibility/engineering**
2. **Perbaiki protokol evaluasi: validation/holdout, scaler per fold, purge/embargo, multi-seed**
3. **Tambahkan baseline persistence/naif dan matriks eksperimen terkontrol**
4. **Jalankan ulang eksperimen + ablation + analisis statistik**
5. **Perbarui klaim, hasil, dan naskah inti**
6. **Sinkronkan generator dokumen dan rebuild master DOCX**
7. **Audit referensi + finalisasi, clean-room reproduction, dan packaging**

### Gate antar-fase

- Jangan masuk Fase 2 sebelum snapshot Fase 1 selesai.
- Jangan masuk Fase 4 sebelum protokol Fase 2 dan matriks Fase 3 disetujui.
- Jangan mengubah naskah di Fase 6 sebelum angka final Fase 5 dikunci.
- Jangan submit sebelum Fase 7 lulus clean-room reproduction dan audit referensi.

---

## 2. Aturan main selama perbaikan

- [ ] **Freeze first:** jangan menimpa `results/`, `models/`, atau DOCX lama sebelum snapshot dibuat.
- [ ] **Satu sumber kebenaran:** semua angka naskah harus berasal dari `results/summary_final.json` (atau file summary resmi), bukan hardcode di generator.
- [ ] **Holdout suci:** data test 439 hari tidak boleh dipakai untuk memilih hyperparameter, search space, loss, atau jumlah epoch.
- [ ] **Setiap run punya ID:** simpan konfigurasi, seed, versi package, hash data, dan git commit.
- [ ] **Jangan mengklaim kausalitas tanpa ablation:** perbedaan performa tidak otomatis disebabkan oleh satu hyperparameter.
- [ ] **Setiap perubahan naskah harus punya rujukan artefak:** nomor tabel/gambar, file hasil, dan baris kode.
- [ ] **Review advisor sebelum reframe besar:** terutama jika Tier 3 tetap kalah dari persistence.

---

## 3. TODO detail

## FASE 1 — Bekukan artefak + fondasi reproducibility/engineering

**Status 2026-10-25:** fondasi Fase 1 terpasang. `pytest -q` lulus 19 test; smoke run `smoke_all` berhasil menjalankan data → tier1 → tier2 → tier3 → eval dengan artefak terisolasi di `results/runs/` dan manifest lengkap. Dua item sengaja belum dicentang: verifikasi clean-room environment dan stage `baseline`/`ablation` (menyusul Fase 3).

**Estimasi:** 1–2 hari kerja.  
**Dependensi:** tidak ada.  
**Output:** snapshot aman, environment terkunci, pipeline portabel, test dasar, run manifest.

### 1.1 Bekukan kondisi saat ini

- [x] Buat tag/branch Git sebelum perubahan:
  - `git tag pre-perbaikan-YYYYMMDD`
  - atau branch `snapshot/pre-perbaikan`.
- [x] Buat folder arsip, misalnya `archive/pre_perbaikan_YYYYMMDD/`.
- [x] Salin minimal:
  - `05_Source_Code/results/`
  - `05_Source_Code/models/`
  - `05_Source_Code/data/processed/`
  - `03_Naskah_Skripsi/`
- [x] Hitung SHA256 untuk file kunci:
  - `data/raw/BTCUSDT_daily_2020_2025.csv`
  - `data/processed/train_insample.csv`
  - `data/processed/test_outofsample.csv`
  - `data/processed/minmax_scaler.joblib`
  - `results/optuna_study.db`
  - `results/metrics/metrics_tier1.json`, `tier2`, `tier3`
  - `results/predictions_tier1.csv`, `tier2`, `tier3`
  - `03_Naskah_Skripsi/SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx`
- [x] Tulis `archive/pre_perbaikan_YYYYMMDD/README_SNAPSHOT.md` berisi:
  - tanggal snapshot,
  - angka metrik lama,
  - daftar isu yang diketahui,
  - hash file,
  - cara restore.
- [x] Pastikan snapshot bisa dibuka/direstore tanpa menyentuh file aktif.

**Acceptance:** ada snapshot yang bisa direstore; hash tercatat; tidak ada file aktif yang berubah.

### 1.2 Kunci environment

- [ ] Pilih versi Python yang benar-benar didukung TensorFlow (jangan hanya mengandalkan Python 3.14 rc).
  - Catatan: environment aktual Python 3.14.7 + TensorFlow 2.22.0rc0 sudah dipin di `requirements.txt`; keputusan versi stabil menunggu pembimbing.
- [x] Buat `requirements.txt` dengan versi pin, minimal:
  - `tensorflow`
  - `optuna`
  - `scikit-learn`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `joblib`
  - `python-docx`
  - `docxcompose`
  - `pytest`
- [x] Buat `requirements-dev.txt` jika perlu (`pytest`, `ruff`, `black`, dll.).
- [ ] Verifikasi `pip install -r requirements.txt` di virtual environment baru (belum dijalankan; butuh unduhan TensorFlow besar).
- [x] Catat versi aktual ke `results/runs/{run_id}/env.json`.
- [x] Hapus klaim versi di README yang tidak sesuai environment aktual.

**Acceptance:** environment baru bisa dibuat dari nol hanya dengan file requirements; versi tercatat.

### 1.3 Refactor path dan konfigurasi

- [x] Buat `05_Source_Code/model_experiment/config.py` atau `paths.py`:
  - `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
  - path data, results, models, figures, docs.
- [x] Ganti semua path absolut `d:\OneDrive\Desktop\jurnal` dengan path relatif ke project root.
- [x] Tambahkan opsi CLI `--project-root`, `--run-id`, `--seed`, `--trials`.
- [x] Pastikan script bisa dijalankan dari root repo maupun dari folder `model_experiment`.
- [x] Perbaiki `generate_bab1.py` agar menyimpan ke `03_Naskah_Skripsi/`, bukan CWD.

**Acceptance:** tidak ada path absolut Windows yang tersisa di kode pipeline/generator; script jalan dari root.

### 1.4 Perbaiki orchestrator

- [x] `run_pipeline.py` meneruskan `--trials` ke `05_optimize_optuna_tier3.py`.
- [x] Gunakan path absolut ke script child, bukan nama file relatif CWD.
- [x] Tangani `subprocess.CalledProcessError` dengan benar.
- [x] Tambahkan stage `baseline`; ablation dijalankan lewat `experiment_matrix.py`/`07_run_ablation.py`.
- [x] Tambahkan `--run-id` dan `--resume` bila memungkinkan.
- [x] Pastikan setiap stage menulis log ke `results/runs/{run_id}/logs/`.

**Acceptance:** `python 05_Source_Code/model_experiment/run_pipeline.py --all --trials 50 --run-id test` berjalan dari root.

### 1.5 Run manifest dan provenance

- [x] Buat struktur output per run:
  ```text
  results/runs/{run_id}/
    config.json
    env.json
    data_hash.txt
    git_commit.txt
    metrics/
    predictions/
    figures/
    logs/
    summary.json
  ```
- [x] Simpan konfigurasi lengkap: split, seed, lookback, units, dropout, LR, batch, layers, loss, scheduler, epochs, early stopping.
- [x] Simpan hash data train/test dan scaler.
- [x] Simpan `git rev-parse HEAD` dan status dirty/clean.
- [x] Buat fungsi `make_run_id()` yang deterministik/mudah dilacak, misalnya `2026-10-25_tier3_seed42`.
- [x] Jangan menimpa run lama; selalu buat folder baru.

**Acceptance:** setiap hasil bisa dilacak ke kode, data, dan environment.

### 1.6 Test dasar

- [x] Buat folder `tests/`.
- [x] `tests/test_data.py`:
  - jumlah baris 2.192,
  - tanggal unik dan kontinu,
  - tidak ada null,
  - split 1.753/439,
  - tidak ada OHLC violation.
- [x] `tests/test_sequences.py`:
  - bentuk `X` = `(n, lookback, 1)`,
  - target `y[t]` adalah nilai setelah window,
  - tidak ada sampel test yang masuk ke train.
- [x] `tests/test_metrics.py`:
  - hitung ulang RMSE/MAE/MAPE dari CSV prediksi,
  - cocok dengan JSON pada toleransi pembulatan.
- [x] `tests/test_provenance.py`:
  - best trial di DB cocok dengan `metrics_tier3.json`,
  - jumlah prediksi = 439,
  - tanggal prediksi sama untuk semua tier.
- [x] Jalankan `pytest -q` dan pastikan lulus.

**Acceptance:** test dasar lulus; kegagalan data/provenance terdeteksi otomatis.

### 1.7 Rapikan script berbahaya

- [x] Pindahkan logika `download_references.py` ke `main()` dan aktifkan verifikasi TLS.
- [x] Pindahkan kerja `verify_bab2.py`, `verify_bab3.py`, `verify_bab4.py` ke `main()` guard.
- [x] Pastikan import module tidak melakukan download/verifikasi/penulisan file.
- [x] Tambahkan validasi bahwa unduhan data Binance benar-benar lengkap sebelum disimpan.
- [x] Tambahkan retry/backoff dan cek jumlah candle yang diharapkan.

**Acceptance:** import module tidak punya side effect; unduhan parsial menggagalkan pipeline.

### Gate Fase 1

- [x] Snapshot tersedia.
- [ ] Environment bisa dibuat ulang (file requirements tersedia; clean-room install belum diuji).
- [x] Pipeline berjalan dari root.
- [x] Test dasar lulus.
- [x] Tidak ada path absolut.

---

## FASE 2 - Perbaiki protokol evaluasi dan CV

**Status 2026-10-25:** protokol dieksekusi dan diuji. `docs/PROTOCOL.md` menjadi rujukan tunggal. `pytest -q` lulus 30 test (termasuk 5 test CV dan 6 test statistik). Smoke multi-seed 2 seed (`cv_smoke`) berhasil untuk Tier 1/2/3 dan evaluasi menulis CI + agregat seed. Dua hal sengaja belum dituntaskan: persetujuan pembimbing atas split dan pelaporan variabilitas di Bab 4 (menyusul Fase 5/6).

**Estimasi:** 2-3 hari.  
**Dependensi:** Fase 1 selesai.  
**Output:** protokol split yang bersih, scaler per fold, purge/embargo, multi-seed, evaluasi statistik.

### 2.1 Tetapkan pembagian data yang final

- [x] Tulis keputusan split di `docs/PROTOCOL.md`:
  - in-sample CV + holdout test.
  - 1.753 in-sample untuk CV/tuning; 439 test hanya untuk evaluasi final.
  - Keputusan desain memakai validation internal, bukan test.
- [x] Jika ingin mempertahankan 80:20, bagi 1.753 in-sample menjadi train/validation internal (misalnya 80:20 dari in-sample) untuk keputusan desain.
  - Implementasi: `validation_split=0.1` kronologis di dalam pelatihan; bukan partisi terpisah yang mengubah kontrak 1.753/439.
- [x] Kunci tanggal test dan dokumentasikan.
- [x] Pastikan tidak ada iterasi yang melihat test sebelum model final dibekukan.
  - `cv_utils.py` tidak pernah menerima data test; `tests/test_cv.py` menjaga batas ini.

**Acceptance:** semua anggota tim/pembimbing setuju dengan split; test tidak dipakai untuk tuning.  
**Catatan:** persetujuan pembimbing belum dapat diverifikasi dari repositori; statusnya terbuka.

### 2.2 Scaler per fold

- [x] Refactor `02_preprocessing.py`:
  - simpan data mentah per split,
  - jangan mengandalkan scaler global untuk CV.
- [x] Di dalam CV:
  - fit `MinMaxScaler` hanya pada train fold,
  - transform train dan validation fold dengan scaler yang sama,
  - inverse transform prediksi validation untuk metrik USD.
- [x] Untuk model final:
  - fit scaler pada seluruh in-sample,
  - transform test,
  - simpan scaler final secara eksplisit.
- [x] Tambahkan unit test yang memastikan min/max scaler fold hanya berasal dari train fold.
- [x] Dokumentasikan bahwa test tidak pernah masuk ke fit scaler.

**Acceptance:** tidak ada statistik validation/test yang masuk ke fit scaler fold.

### 2.3 Purge/embargo window

- [x] Implementasikan `TimeSeriesSplit(gap=lookback)` atau purge manual.
- [x] Pastikan window validation tidak overlap dengan window train di batas fold.
- [x] Jika memakai `gap`, dokumentasikan mengapa nilainya `lookback` (atau `lookback-1`).
- [x] Tambahkan test bahwa indeks window validation tidak memakai titik train yang overlap.
- [x] Evaluasi dampak purge terhadap jumlah sampel per fold.
  - Purge mengurangi sampel latih efektif sebesar `lookback` per fold; smoke 3-fold tetap menghasilkan 397-847 window latih.

**Acceptance:** tidak ada overlap window train/validation di batas fold; jumlah sampel cukup untuk 5 fold.

### 2.4 Multi-seed

- [x] Tetapkan seed set, misalnya `[42, 123, 2024, 7, 99]`.
  - `config.DEFAULT_SEEDS`; CLI `--seeds` untuk memilih subset.
- [x] Jalankan model final untuk setiap seed.
  - Diuji dengan 2 seed pada `cv_smoke` (bukan bukti ilmiah, hanya validasi mekanika).
- [x] Simpan metrik per seed dan agregat mean +/- std.
  - `predictions/seed_metrics_tier*.json` + blok `multi_seed` di `metrics_tier*.json`.
- [x] Untuk Optuna, tetap seed sampler; variasi seed model weight dijalankan pada retrain final.
- [ ] Laporkan variabilitas antar-seed di Bab 4.
  - Dijadwalkan setelah angka final dikunci (Fase 5/6).

**Acceptance:** setiap konfigurasi final punya minimal 5 seed; hasil dilaporkan sebagai mean +/- std.  
**Catatan:** mekanisme siap; run final 5 seed `final_matrix_20261025` sedang berjalan.

### 2.5 Evaluasi statistik

- [x] Tambahkan bootstrap 95% confidence interval untuk RMSE/MAE/MAPE (2.000 resample blok 7 hari).
- [x] Opsional: Diebold-Mariano test vs persistence.
  - Tidak diadopsi; diganti paired moving-block bootstrap (`paired_bootstrap_difference`) yang sudah dijelaskan di protokol. Hasilnya ukuran stabilitas deskriptif, bukan uji formal.
- [x] Uji directional accuracy.
  - Diimplementasikan di `analysis_utils.directional_accuracy` dan `08_analyze_results.py`; E0 persistence ditandai tidak interpretable karena selalu memprediksi flat.
- [x] Simpan hasil CI di `summary.json`.
- [x] Bedakan "signifikan secara statistik" dari "praktis lebih baik".
  - `docs/PROTOCOL.md` bagian 6; `paired_bootstrap_difference` hanya ukuran stabilitas, bukan uji formal.

**Acceptance:** tabel hasil memuat mean, std, dan CI; klaim tidak hanya berdasarkan satu angka.

### 2.6 Dokumentasi protokol

- [x] Tulis `docs/PROTOCOL.md` berisi:
  - split dan tanggal,
  - aturan scaler,
  - aturan purge,
  - seed,
  - metrik,
  - baseline,
  - larangan memakai test untuk tuning.
- [ ] Cantumkan protokol ini di Bab 3.
  - Dijadwalkan pada sinkronisasi dokumen (Fase 6), bukan sebelum angka final.
- [x] Simpan versi protokol yang dipakai untuk run final.
  - `docs/PROTOCOL.md` sudah versioned; hash protokol dan `requirements.txt` otomatis dicatat di `data_hash.json` setiap run.

**Acceptance:** protokol bisa direproduksi oleh orang lain tanpa membaca kode.

### Gate Fase 2

- [x] Scaler per fold terbukti benar.
- [x] Purge/embargo aktif.
- [x] Multi-seed berjalan.
- [x] Test tetap terkunci.
- [x] Protokol tertulis.

**Catatan gate:** implementasi dan pengujian mekanika selesai. Run final 5 seed dan pelaporan naskah tetap menjadi pekerjaan Fase 4-6.

---

## FASE 3 — Baseline dan matriks eksperimen terkontrol

**Status 2026-10-25:** baseline dan matriks terkontrol terpasang serta diuji. `baselines.py` menghasilkan persistence/drift/seasonal naive/MA dengan prediksi kausal dan bootstrap CI; `06_evaluate_and_compare.py` memuat baseline ke tabel, gambar, `summary.json`, dan perbandingan berpasangan. `experiment_matrix.py` mendefinisikan E0–E7 dengan desain faktorial 2x2 loss/scheduler pada parameter Tier 3 yang dibekukan. Smoke `matrix_smoke` (E0/E3/E4) dan `matrix_smoke_full` (E1/E2/E7) membuktikan orkestrasi, penamaan artefak, dan tabel hasil. `run_pipeline.py` sekarang punya stage `baseline` dan menjalankannya pada `--all`. Angka smoke 1 epoch **bukan bukti ilmiah**; run final 5 seed adalah pekerjaan Fase 4.

**Estimasi:** 1–2 hari.  
**Dependensi:** Fase 2 selesai.  
**Output:** baseline persistence, matriks ablation, definisi run.

### 3.1 Baseline sederhana

- [x] Implementasikan `baselines.py`:
  - **Persistence:** `pred[t] = actual[t-1]`.
  - Random walk with drift: `pred[t] = actual[t-1] + mean(diff(in-sample))`.
  - Seasonal naive 7 hari: `pred[t] = actual[t-7]`.
  - Moving average 7 hari: `pred[t] = mean(actual[t-7:t])`.
- [x] Evaluasi baseline pada 439 hari test yang sama.
  - Persistence: RMSE 2.167,24; MAE 1.579,80; MAPE 1,62%.
  - Drift: RMSE 2.166,82; MAE 1.579,59; MAPE 1,62% (selisih praktis sangat kecil).
- [x] Simpan prediksi dan metrik baseline.
  - `metrics/metrics_baselines.json` dan `predictions/predictions_baselines.csv` di run baru.
- [x] Tambahkan baseline ke tabel benchmark dan gambar.
  - `06_evaluate_and_compare.py` menambahkan baris persistence, CI, paired difference, dan garis baseline pada gambar.
- [x] Pastikan baseline tidak memakai informasi masa depan.
  - `tests/test_baselines.py` memeriksa persistensi = lag aktual, seasonal/MA hanya memakai observasi sebelum `t`, dan drift hanya diestimasi dari in-sample.

**Acceptance:** baseline persistence punya RMSE/MAE/MAPE dan prediksi CSV; bisa dibandingkan langsung.

### 3.2 Matriks eksperimen

- [x] Definisikan matriks di `experiment_matrix.py`:

| Run | Model | Loss | Scheduler | HPO | Tujuan |
|---|---|---|---|---|---|
| E0 | Persistence | - | - | - | Baseline naif |
| E1 | Tier 1 default | MSE | Tidak | Tidak | Baseline kontrol |
| E2 | Tier 2 manual | MSE | Tidak | Tidak | Pembanding literatur |
| E3 | Tier 3 best params | MSE | Tidak | Tidak | Isolasi efek HPO |
| E4 | Tier 3 best params | MAE | Tidak | Tidak | Isolasi efek loss |
| E5 | Tier 3 best params | MSE | Ya | Tidak | Isolasi efek scheduler |
| E6 | Tier 3 best params | MAE | Ya | Tidak | Isolasi loss + scheduler |
| E7 | Tier 3 HPO | MAE | Ya | Ya | Model usulan final |

- [x] Pastikan semua run memakai split, early stopping, max epoch, dan seed set yang sama.
  - `experiment_matrix.py` meneruskan `--epochs` dan `--patience 12` yang sama ke E1–E6; E7 memakai aturan retrain Tier 3 yang sama. Seed set default `42,123,2024,7,99`.
  - E3–E6 memakai `config.TIER3_CONFIG` tanpa override hyperparameter; hanya `--loss` dan `--scheduler` yang berubah.
- [x] Pastikan HPO hanya memakai data train/validation, bukan test.
  - `05_optimize_optuna_tier3.py` memakai `cv_utils` pada 1.753 in-sample; `tests/test_cv.py` menjaga batas holdout.
- [x] Tentukan run mana yang menjadi “model usulan” dan run mana yang menjadi ablation.
  - E7 = model usulan (HPO penuh); E3–E6 = ablation; E1/E2 = kontrol/pembanding; E0 = baseline.
- [x] Tulis hipotesis untuk setiap perbandingan.
  - Tersimpan di `experiment_matrix.py` dan `experiment_matrix_plan.json`:
    - E1 vs E3: efek hyperparameter Optuna dengan MSE/tanpa scheduler.
    - E4 vs E3: efek loss MAE.
    - E5 vs E3: efek ReduceLROnPlateau.
    - E6 vs E3: efek gabungan; bandingkan dengan E4/E5 untuk interaksi.
    - E7 vs E6: efek HPO penuh.
    - E0 vs semua: apakah LSTM mengalahkan persistence.

**Acceptance:** matriks disetujui; setiap perbandingan mengisolasi satu faktor.  
**Catatan:** desain dikunci di kode dan plan JSON; persetujuan formal pembimbing tidak dapat diverifikasi dari repositori.

### 3.3 Baseline vs model

- [x] Bandingkan Tier 3 dengan persistence pada RMSE, MAE, MAPE, dan CI.
  - `06_evaluate_and_compare.py` mencetak baris baseline, CI bootstrap, dan `tier3_vs_persistence` pada `summary.json`.
- [x] Jika Tier 3 kalah, tulis temuan itu secara eksplisit, jangan disembunyikan.
  - Temuan legacy: Tier 3 (RMSE 2.338,22; MAE 1.784,27; MAPE 1,81%) lebih buruk dari persistence (RMSE 2.167,24; MAE 1.579,80; MAPE 1,62%). Run final Fase 4 wajib melaporkan arah yang sama/jujur, bukan memilih baseline yang menguntungkan.
- [ ] Diskusikan mengapa one-step-ahead daily price sering didekati persistence.
  - Dijadwalkan di Bab 4/5 setelah angka final (Fase 5–6).
- [x] Pertimbangkan baseline tambahan yang relevan (drift, seasonal naive).
  - Drift, seasonal naive 7, dan moving average 7 sudah dihitung dan dilaporkan.

**Acceptance:** baseline menjadi bagian tetap dari evaluasi, bukan tambahan opsional.

### Gate Fase 3

- [x] Baseline berjalan dan tersimpan.
- [x] Matriks eksperimen disetujui.
  - Dikunci di `experiment_matrix.py`; persetujuan pembimbing di luar repo masih perlu dikonfirmasi.
- [x] Tidak ada run yang memakai test untuk tuning.
- [x] Semua run punya definisi konfigurasi.
  - Setiap command dan config tercatat di `experiment_matrix_plan.json` dan manifest stage.

**Catatan gate:** mekanika Fase 3 selesai dan smoke-tested. Run final 5 seed, analisis interaksi, dan diskusi persistence tetap menjadi pekerjaan Fase 4–6.

---

## FASE 4 — Jalankan ulang eksperimen, ablation, dan analisis

**Status 2026-10-26:** run final `final_matrix_20261025` selesai dengan `matrix = success` dan seluruh stage E0–E7 `success`.
E7 menyelesaikan 50 trial (13 COMPLETE, 37 PRUNED), memilih trial #27 dengan CV MAE 1.092,794350 USD, lalu di-retrain pada lima seed.
Verdict otomatis: `proposed_not_better_than_persistence`; E7 MAE 1.687,49 USD lebih tinggi daripada persistence 1.579,80 USD dengan CI berpasangan +50,82 s.d. +170,90 USD yang seluruhnya di atas nol.
`summary_final.json` sudah dipublikasikan, `docs/NUMBER_AUDIT.md` sudah dihasilkan, dan keputusan dicatat di `docs/DECISIONS.md` (D14).

**Estimasi:** 2–4 hari (sebagian besar waktu komputasi).  
**Dependensi:** Fase 2 dan Fase 3 selesai.  
**Output:** hasil final per run, summary statistik, analisis residual.

### 4.1 Jalankan baseline dan Tier 1/2

- [x] Jalankan persistence, drift, seasonal naive (jika dipakai).
  - Persistence: RMSE 2.167,24; MAE 1.579,80; MAPE 1,62% pada 439 hari holdout.
  - Drift: RMSE 2.166,82; MAE 1.579,59; MAPE 1,62%.
  - Seasonal naive 7: RMSE 5.404,67; MAE 4.128,13; MAPE 4,22%.
- [x] Jalankan Tier 1 dan Tier 2 dengan 5 seed.
  - Tier 1 mean ± std: RMSE 2.610,38 ± 203,14; MAE 2.058,81 ± 196,57; MAPE 2,06 ± 0,18%.
  - Tier 2 mean ± std: RMSE 3.645,67 ± 392,73; MAE 3.048,39 ± 399,48; MAPE 3,02 ± 0,38%.
  - Keduanya masih di atas persistence pada MAE.
- [x] Simpan prediksi, metrik, dan waktu latih per seed.
  - `predictions/predictions_tier{1,2}.csv`, `predictions/seed_metrics_tier{1,2}.json`, dan `metrics/metrics_tier{1,2}.json`.
- [x] Pastikan tidak ada perbedaan preprocessing antar-run.
  - Semua stage membaca processed data yang sama (1.753/439) dan scaler final yang sama; hash data dicatat di `data_hash.json`.

### 4.2 Jalankan HPO Tier 3 yang bersih

- [x] Jalankan Optuna 50 trials dengan:
  - scaler per fold,
  - purge/embargo,
  - search space sesuai kode (7–30, 32–128, 0.1–0.4, LR 5e-4–2e-3, batch 16/32/64, layers 1–2),
  - `MedianPruner` fold-level,
  - seed sampler.
- [x] Simpan study DB baru dengan `run_id`.
  - `05_Source_Code/results/runs/final_matrix_20261025/optuna_study.db`.
- [x] Jangan menimpa study lama.
  - Study baru dibuat di dalam run dir; legacy hanya dibaca bila `--legacy` eksplisit.
- [x] Catat waktu optimasi aktual.
  - 2.427,0 detik; 50 trial (13 COMPLETE, 37 PRUNED); trial terbaik #27, CV MAE 1.092,794350 USD; lookback 25, units 112, dropout 0,10, LR 0,00128092, batch 16, 1 layer.

### 4.3 Jalankan ablation

- [x] Jalankan E3–E6 dari matriks.
  - E3 (MSE, tanpa scheduler): MAE 2.281,38 ± 163,11; RMSE 2.830,25 ± 161,72.
  - E4 (MAE, tanpa scheduler): MAE 1.790,80 ± 167,39; RMSE 2.347,14 ± 159,99.
  - E5 (MSE, ReduceLROnPlateau): MAE 2.116,59 ± 78,61; RMSE 2.677,48 ± 88,79.
  - E6 (MAE, ReduceLROnPlateau): MAE 1.712,07 ± 67,48; RMSE 2.274,63 ± 59,26.
- [x] Gunakan parameter terbaik yang sama untuk isolasi loss/scheduler.
  - E3–E6 memakai `config.TIER3_CONFIG` yang dibekukan; hanya `--loss` dan `--scheduler` berubah (`experiment_matrix_plan.json`).
- [x] Jalankan 5 seed per konfigurasi.
  - Seed set `42,123,2024,7,99`; agregat per seed tersimpan di `metrics/metrics_e{3,4,5,6}_*.json`.
- [x] Simpan semua hasil.
  - Prediksi seed utama di `predictions/`, prediksi seed lain dan `seed_metrics_*.json` juga tersimpan.
- [x] Pastikan tidak ada test leakage.
  - Holdout hanya dipakai untuk prediksi akhir; tuning/early stopping memakai in-sample. `tests/test_cv.py` dan `tests/test_sequences.py` menjaga batas ini.

### 4.4 Analisis hasil

- [x] Hitung mean ± std dan bootstrap CI per metrik.
  - `metrics/` + `seed_metrics_*`; moving-block bootstrap 7 hari, 2.000 resample.
- [x] Buat tabel perbandingan lengkap.
  - `benchmark_matrix_table.csv` / `.md`; Tabel 4.5 dan 4.6 di Bab IV.
- [x] Hitung improvement vs Tier 1, Tier 2, dan persistence.
  - E7 vs E1: MAE 280,50 USD lebih rendah (14,25%); vs E2: 1.204,78 USD lebih rendah (41,66%); vs persistence: 107,69 USD lebih tinggi (6,82%).
- [x] Analisis residual:
  - distribusi error,
  - error per rezim pasar (bull/bear/sideways),
  - error pada hari volatilitas tinggi,
  - worst-case error.
  - `residual_analysis.json`; MAE bull 1.658,64; bear 1.908,72; sideways 1.549,76; volatilitas tinggi 3.099,31.
- [x] Analisis directional accuracy (opsional).
  - Akurasi agregat 50,57% (222/439), tetapi hari naik 3,59% dan hari turun 99,07%; dilaporkan sebagai bias arah, bukan kemampuan dua arah.
- [x] Simpan `summary_final.json` sebagai sumber angka naskah.
  - `05_Source_Code/results/summary_final.json`; hash dan field sumber dicatat di `docs/NUMBER_AUDIT.md`.

### 4.5 Keputusan hasil

- [x] Tentukan apakah model usulan layak secara ilmiah:
  - **Jika menang** vs persistence: klaim keunggulan dapat dipertahankan dengan batasan.
  - **Jika kalah** vs persistence: pilih salah satu:
    - perbaiki model (fitur return/differencing, multivariat, horizon lebih panjang, ensemble), atau
    - reframe kontribusi sebagai pipeline/benchmark dan laporkan hasil negatif secara jujur.
  - Keputusan: **kalah**. E7 MAE 1.687,49 USD vs persistence 1.579,80 USD; CI selisih +50,82 s.d. +170,90 USD seluruhnya di atas nol. Kontribusi di-reframe sebagai pipeline/benchmark dengan hasil negatif yang jujur (D14).
- [ ] Diskusikan dengan pembimbing sebelum mengubah Bab 1/4/5.
  - Status: persetujuan pembimbing bersifat eksternal dan belum dapat diverifikasi dari repositori.
- [x] Catat keputusan di `docs/DECISIONS.md`.
  - D14.

### Gate Fase 4

- [x] Semua run selesai dan tersimpan.
- [x] Summary final tersedia.
- [x] CI dan variabilitas seed dihitung.
- [x] Keputusan ilmiah tercatat.

---

## FASE 5 — Perbarui klaim, hasil, dan naskah inti

**Estimasi:** 1 hari.  
**Dependensi:** Fase 4 selesai dan keputusan disetujui.  
**Output:** angka final, klaim yang defensible, daftar perubahan naskah.

### 5.1 Kunci angka final

- [x] Buat `results/summary_final.json` berisi:
  - konfigurasi final,
  - metrik mean/std/CI,
  - baseline,
  - ablation,
  - jumlah trials,
  - best trial,
  - versi package,
  - hash data.
- [x] Pastikan semua generator naskah membaca file ini, bukan hardcode.
  - `results_context.py` memvalidasi `summary_final.json`; generator gagal keras bila field wajib tidak ada.
- [x] Buat `docs/NUMBER_AUDIT.md` yang memetakan setiap angka di naskah ke sumbernya.

### 5.2 Perbarui klaim

- [x] Ganti “juara mutlak” menjadi klaim yang sesuai:
  - Hasil final: persistence tetap terbaik pada MAE; E6 adalah LSTM terbaik (1.667,26 USD); E7 (1.687,49 USD) tidak mengalahkan persistence dan CI berpasangan seluruhnya di atas nol.
  - Klaim yang dipakai: “hasil negatif yang terverifikasi”, bukan keunggulan model usulan.
- [x] Hapus/qualify klaim kausal tanpa ablation:
  - “batch 10 menyebabkan osilasi gradien”,
  - “units 128 menyebabkan overfitting”,
  - “lookback 22 membuktikan momentum lag”.
  - Semua efek dilaporkan sebagai arah dan besaran pada konfigurasi yang diuji, bukan mekanisme kausal.
- [x] Tambahkan bagian limitations:
  - satu aset,
  - one-step-ahead,
  - tanpa transaction costs,
  - univariat,
  - satu periode test,
  - baseline persistence,
  - holdout tidak dipakai untuk tuning.
- [x] Perbarui abstrak, Bab 1, Bab 4, Bab 5, README, dan laporan eksekutif.
  - Abstrak dan Bab IV/V memakai verdict otomatis; README memakai tabel desain matriks dan pointer sumber angka.

### 5.3 Perbarui Bab 4

- [x] Tambahkan tabel baseline persistence.
- [x] Tambahkan tabel ablation loss/scheduler.
- [x] Perbarui tabel benchmark dengan CI/std.
- [x] Perbarui gambar:
  - prediksi vs aktual,
  - bar chart metrik,
  - konvergensi Optuna,
  - residual (jika dipakai).
- [x] Pastikan label sumbu dan caption sesuai loss yang benar (MAE, bukan MSE).
- [x] Perbarui pembahasan agar sesuai hasil baru.

### Gate Fase 5

- [x] Semua angka final terkunci.
- [x] Klaim sesuai bukti.
- [x] Limitations tercantum.
- [ ] Pembimbing menyetujui framing.
  - Status: persetujuan pembimbing bersifat eksternal dan belum dapat diverifikasi dari repositori.

---

## FASE 6 — Sinkronkan generator dokumen dan rebuild

**Estimasi:** 2–3 hari.  
**Dependensi:** Fase 5 selesai.  
**Output:** satu perintah rebuild semua bab + master; verifier konsistensi; DOCX final.

**Status 2026-10-26:** seluruh generator dan verifier sudah diperbarui, master dibangun ulang, dan pagination Word diverifikasi. Master DOCX berukuran 1.242.417 byte dengan 6 gambar, 29 objek OMML, 39 tabel, dan 77 halaman fisik; verifier `LULUS`. Export PDF final dilakukan pada Fase 7.

### 6.1 Perbaiki generator front matter

- [x] `generate_front_matter.py`:
  - daftar gambar disesuaikan dengan caption BAB 4 aktual,
  - daftar tabel disesuaikan dengan caption BAB 4 aktual,
  - daftar lampiran sesuai isi,
  - abstrak membaca `summary_final.json`,
  - nomor halaman diperbarui setelah pagination final atau gunakan field TOC Word.
- [x] Hapus referensi ke gambar residual jika gambar tidak dibuat.
  - Daftar gambar hanya memuat lima caption yang benar-benar ada di badan naskah.

### 6.2 Perbaiki generator back matter

- [x] `generate_back_matter.py`:
  - best trial diambil dinamis dari `metrics_tier3.json`/DB, bukan hardcode #44/14/80,
  - label “Val Loss” memakai MAE, bukan MSE,
  - tabel 50 trials konsisten dengan CSV,
  - daftar pustaka sesuai referensi final,
  - lampiran kode tidak memuat search space yang sudah usang.

### 6.3 Perbaiki generator Bab 3 dan Bab 4

- [x] `generate_bab3.py`:
  - MedianPruner dijelaskan per fold, bukan per epoch,
  - Tier 2 split 80:20 (bukan 85%),
  - jumlah 1.753/439,
  - search space sama dengan kode,
  - protokol scaler per fold dan purge dijelaskan.
- [x] `generate_bab4.py`:
  - nomor tabel/gambar dan caption konsisten,
  - konfigurasi final 25/112/0,10/0,00128/16, 1 layer, trial #27,
  - loss tidak diklaim sebagai hyperparameter yang dituning jika tidak,
  - jumlah epoch sesuai metrik,
  - tabel baseline dan ablation ditambahkan,
  - pembahasan diperbarui.
- [x] `generate_bab1/2/5.py` disesuaikan jika ada angka/klaim yang berubah.

### 6.4 Perbaiki master assembler

- [x] `generate_master_skripsi.py` memanggil ulang:
  - `generate_bab1` s.d. `generate_bab5`,
  - `generate_front_matter`,
  - `generate_back_matter`,
  - baru menggabungkan.
- [x] Atau buat `generate_all.py` yang menjalankan semuanya berurutan.
  - `python 05_Source_Code/generators/generate_all.py` menjalankan rebuild, verifier, dan audit sitasi.
- [x] Pastikan gagal keras jika salah satu generator error.
- [x] Tambahkan logging output dan timestamp.

### 6.5 Perkuat verifier

- [x] `verify_full_skripsi.py` mengecek:
  - angka metrik di naskah = `summary_final.json`,
  - best trial = DB/metrics,
  - daftar gambar = caption aktual,
  - daftar tabel = caption aktual,
  - file gambar yang di-embed benar-benar ada,
  - tidak ada angka lama (14/80, 225, 2.25, dll.),
  - jumlah referensi = 32,
  - DOI/penulis kunci ada,
  - tidak ada raw `$`,
  - OMML tetap ada.
- [x] Verifier harus mengembalikan exit code non-zero jika ada inkonsistensi.
  - Diuji dengan fixture kotor; verifier mengembalikan non-zero untuk caption stale, gambar hilang, angka legacy, metrik salah, raw `$`, dan OMML hilang.

### 6.6 Rebuild dan cek visual

- [x] Jalankan generator semua bab + master.
- [x] Buka DOCX di Word.
- [x] Update field TOC/daftar isi/daftar gambar/tabel.
  - Tidak ada field TOC (`TOCS=0`); nomor halaman statis sudah disinkronkan ke pagination aktual.
- [x] Cek pagination, margin, font, spasi, caption, dan nomor halaman.
- [x] Export PDF untuk review visual.
  - `release/final_20261026/SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.pdf` (77 halaman, 1.101.733 byte).
- [x] Bandingkan dengan versi snapshot untuk memastikan tidak ada bagian hilang.

### Gate Fase 6

- [x] Satu perintah membangun ulang seluruh naskah.
- [x] Verifier konsistensi lulus.
- [x] Tidak ada caption/daftar yang stale.
- [x] DOCX final bisa dibuka dan dipagination dengan benar.

---

## FASE 7 — Audit referensi + finalisasi

**Estimasi:** 2–3 hari.  
**Dependensi:** Fase 6 selesai.  
**Output:** referensi valid, clean-room reproduction, arsip final, materi sidang.

**Status 2026-10-26:** audit referensi dan audit naskah selesai. Clean-room install ditunda karena unduhan TensorFlow besar; langkah dan kriteria penerimaan sudah didokumentasikan di `docs/REPRODUCTION_REPORT.md`. Turnitin, persetujuan pembimbing, dan backup cloud bersifat eksternal.

### 7.1 Audit referensi

- [x] Buat `04_Referensi_Ilmiah/references_manifest.csv` dengan kolom:
  - id, authors, year, title, venue, DOI/URL, file, hash, status verifikasi.
- [x] Verifikasi setiap DOI/URL ke Crossref/penerbit.
- [x] Ganti PDF yang salah:
  - Bouthillier (saat ini paper fisika AWAKE),
  - Feurer (saat ini PID Lagrangian),
  - Gu (saat ini makalah matematika Prancis),
  - Makridakis (saat ini studi asthma),
  - file lain yang tidak cocok.
- [x] Perbaiki `download_references.py`:
  - URL benar,
  - TLS aktif,
  - validasi `%PDF`,
  - `main()` guard.
- [x] Cocokkan setiap sitasi dalam naskah dengan daftar pustaka.
  - `audit_citations.py` memeriksa dua arah: semua referensi dikutip dan semua sitasi ada di daftar pustaka.
- [x] Pastikan format APA 7th konsisten.
- [x] Cek ulang klaim yang bergantung pada referensi yang salah.
  - Empat entri tak terverifikasi dihapus dan tujuh entri lain dikoreksi; total tepat 32 referensi.

### 7.2 Clean-room reproduction

- [ ] Buat virtual environment baru.
  - Status: ditunda; membutuhkan unduhan TensorFlow besar. Prosedur tercatat di `docs/REPRODUCTION_REPORT.md`.
- [ ] Install dari `requirements.txt`.
  - Status: ditunda bersama pembuatan venv baru.
- [x] Jalankan pipeline lengkap dengan `run_id` baru.
  - Run final `final_matrix_20261025` dijalankan end-to-end dari pipeline saat ini; seluruh 11 stage `success`.
- [x] Bandingkan metrik dengan `summary_final.json` dalam toleransi yang wajar.
- [x] Bandingkan hash data dan konfigurasi.
- [x] Catat hasil di `docs/REPRODUCTION_REPORT.md`.
- [x] Jika berbeda, jelaskan penyebab (non-determinisme GPU/CPU, versi, seed).
  - Belum ada perbedaan yang teramati; non-determinisme TensorFlow tetap dicatat sebagai risiko.

### 7.3 Audit akhir naskah

- [x] Jalankan `verify_full_skripsi.py`.
- [x] Cek margin, font, spasi, indent, penomoran halaman.
- [x] Cek semua tabel/gambar muncul dan dirujuk di teks.
- [x] Cek tidak ada placeholder/TODO/komentar generator yang tertinggal.
- [x] Cek daftar pustaka dan lampiran.
- [ ] Jalankan Turnitin/plagiarism check.
  - Status: eksternal; tidak dapat dijalankan dari repositori.
- [x] Simpan hasil audit.
  - `docs/NUMBER_AUDIT.md`, `docs/REFERENCE_AUDIT.md`, `docs/REPRODUCTION_REPORT.md`.

### 7.4 Packaging

- [x] Buat `release/final_YYYYMMDD/` berisi:
  - DOCX final,
  - PDF final,
  - kode pipeline,
  - requirements,
  - summary final,
  - run manifest,
  - hash file,
  - README cara reproduksi.
  - Lokasi: `release/final_20261026/`; PDF 77 halaman, 1.101.733 byte; arsip kode `code/pipeline_code.zip`.
- [x] Buat `docs/DEFENSE_NOTES.md` berisi:
  - angka final,
  - baseline persistence,
  - ablation,
  - limitations,
  - jawaban atas pertanyaan “kenapa tidak beat persistence?”,
  - daftar referensi yang sudah diverifikasi.
- [ ] Backup ke media eksternal/cloud.
  - Status: eksternal; tidak dapat dilakukan dari repositori.
- [x] Tag Git final: `v1.0-final`.
  - Dibuat pada commit rilis akhir.

### Gate Fase 7 / Definition of Done

- [x] Referensi 100% terverifikasi.
- [ ] Clean-room reproduction berhasil.
  - Status: ditunda dengan prosedur terdokumentasi; bukan klaim lulus.
- [x] Verifier konsistensi lulus.
- [x] DOCX/PDF final siap sidang.
- [x] Arsip final dan defense notes tersedia.
- [x] Tag `v1.0-final` dibuat.

---

## 4. Definition of Done keseluruhan

### Ilmiah

- [x] Baseline persistence/naif ada dan dilaporkan.
- [x] Protokol train/validation/test jelas; test tidak dipakai untuk tuning.
- [x] Scaler per fold dan purge/embargo diterapkan.
- [x] Hasil multi-seed + CI dilaporkan.
- [x] Ablation loss/scheduler/HPO ada.
- [x] Klaim sesuai bukti; limitations jujur.

### Engineering

- [x] Tidak ada path absolut.
- [ ] `requirements.txt` pinned dan berhasil di environment baru.
  - Pin lengkap dan konsisten; verifikasi clean-room ditunda karena unduhan TensorFlow besar.
- [x] Test dasar lulus.
- [x] Setiap run punya manifest dan run ID.
- [x] Pipeline bisa dijalankan dari root dengan satu perintah.
- [x] Tidak ada script yang berjalan saat di-import.

### Dokumen

- [x] Semua angka berasal dari `summary_final.json`.
- [x] Daftar gambar/tabel/lampiran sesuai isi.
- [x] Caption dan nomor halaman benar.
- [x] Narasi pruning/loss/search space sesuai kode.
- [x] Referensi terverifikasi dan PDF sesuai.
- [x] Verifier konsistensi lulus.

### Packaging

- [x] Snapshot lama tersimpan.
- [ ] Release final berisi kode, data, hasil, naskah, dan cara reproduksi.
  - Sedang dirakit di `release/final_20261026/`.
- [ ] Defense notes siap.
  - Sedang ditulis di `docs/DEFENSE_NOTES.md`.

---

## 5. Estimasi waktu

| Fase | Estimasi | Catatan |
|---|---:|---|
| 1. Freeze + reproducibility | 1–2 hari | Termasuk refactor path dan test dasar |
| 2. Protokol + CV | 2–3 hari | Paling kritis; jangan dipotong |
| 3. Baseline + matriks | 1–2 hari | Baseline cepat; matriks butuh keputusan |
| 4. Eksperimen + ablation | 2–4 hari | Tergantung compute; 50 trials ~30 menit/run |
| 5. Klaim + naskah inti | 1 hari | Perlu review pembimbing |
| 6. Generator + rebuild | 2–3 hari | Termasuk cek visual Word |
| 7. Referensi + finalisasi | 2–3 hari | Termasuk clean-room reproduction |
| **Total** | **12–20 hari kerja** | Bisa paralel untuk referensi |

---

## 6. Keputusan yang perlu diambil sebelum mulai

- [x] **Versi Python/TensorFlow:** pilih kombinasi yang stabil dan didukung, bukan rc.
  - Keputusan: pin aktual Python 3.14.7 + TensorFlow 2.22.0rc0 dipertahankan untuk reproduksi; opsi versi stabil tetap terbuka bila pembimbing menghendaki (D1).
- [x] **Split final:** tetap 80:20 dengan validation internal, atau 70:15:15?
  - Keputusan: 1.753 in-sample / 439 holdout; CV berpurge 5 fold di dalam in-sample (D2–D4).
- [x] **Baseline:** cukup persistence, atau tambah drift/seasonal naive?
  - Keputusan: persistence, drift, seasonal naive 7, dan moving average 7 (D6).
- [x] **Jika Tier 3 kalah dari persistence:** perbaiki model atau reframe kontribusi?
  - Keputusan: reframe sebagai pipeline terkontrol + hasil negatif (D14).
- [x] **Metrik utama:** RMSE, MAE, MAPE, atau tambah MASE/sMAPE?
  - Keputusan: MAE utama; RMSE, MAPE, dan analisis pendukung (D7).
- [x] **CI/statistik:** bootstrap saja atau tambah Diebold-Mariano?
  - Keputusan: moving-block bootstrap 7 hari, 2.000 resample, paired CI; tanpa Diebold-Mariano (D8).
- [x] **Nomor halaman:** update manual atau pakai field TOC Word?
  - Keputusan: TOC statis, nomor halaman dipatch dari pagination Word (D11).
- [x] **Referensi:** ganti PDF atau hapus referensi yang tidak bisa diverifikasi?
  - Keputusan: 32 referensi terverifikasi; entri tak terverifikasi dihapus (D12).

---

## 7. Perintah penting setelah implementasi

```bash
# Environment
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Test
pytest -q

# Pipeline penuh
python 05_Source_Code/model_experiment/run_pipeline.py --all --trials 50 --run-id final_YYYYMMDD

# Generator dokumen
python 05_Source_Code/generators/generate_all.py

# Verifikasi naskah
python 05_Source_Code/generators/verify_full_skripsi.py
```

---

## 8. Log progres

| Tanggal | Fase | Aktivitas | Status | Catatan |
|---|---|---|---|---|
| 2026-10-25 | 1–4 | Snapshot, protokol, baseline, matriks, HPO, analisis | Selesai | Run `final_matrix_20261025`; semua stage `success` |
| 2026-10-26 | 5–6 | Kunci angka, rewrite naskah, sinkronisasi generator, rebuild | Selesai | Verifier dan audit sitasi lulus; pagination Word 77 halaman |
| 2026-10-26 | 7 | Audit referensi, laporan reproduksi, defense notes, paket rilis | Selesai sebagian | 32 referensi; PDF final; clean-room/Turnitin/backup eksternal tertunda |
| 2026-10-26 | 7 | Tag `v1.0-final` | Selesai | Dibuat setelah commit rilis |

---

*Dokumen ini adalah rencana kerja. Setiap keputusan ilmiah tetap harus dikonsultasikan dengan dosen pembimbing.*

---

# STUDY 2 - LSTM + Optuna untuk Peramalan Realized Volatility Bitcoin

**Status (2026-10-28):** aktif di branch `study2-volatility`; Study 1 tetap beku pada tag `v1.0-final` (commit `f3f9763`) dan tidak diubah.

## Deskripsi

Study 1 (harga harian) adalah negative result yang jujur: E7 tidak mengalahkan persistence. Study 2 pindah ke target dengan sinyal yang jauh lebih kuat: **daily realized variance Bitcoin dari kline 1h**, dengan HPO Optuna yang leakage-free dan test eksternal 2026 yang belum pernah dipakai.

- Gap & protokol: `docs/STUDY2_GAP.md`, `docs/STUDY2_PROTOCOL.md`
- Protokol di-hash SEBELUM data dibangun: SHA-256 `72c7588046b4ab644d814031e3329702ed884c6d9f0d0ff3c5d27660e36caba3`
- Amandemen A1 (integritas data, dicatat sebelum ada statistik target): hari <20 bar dikeluarkan (2020-02-19, 19 bar); hari 20-23 bar dipertahankan; window validasi/test wajib 24 bar penuh.

## Data (dibekukan)

- Sumber: Binance Vision, kline bulanan 1h BTCUSDT, 2020-01 s.d. 2026-09 (81 file, semua HTTP 200).
- 2.464 hari (2020-01-01 s.d. 2026-09-30) di `05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv`
- SHA-256 CSV harian: `ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b`
- Target: `log_rv_{t+1}`; fitur (6, tetap): log_rv, log_range, log_volume, log_absret, rv_mean_5, rv_mean_22.

## Split & endpoint (pre-registered)

- Dev/HPO: 2020-2023 (purged rolling-origin CV, 5 fold, gap = lookback+1)
- Validasi (checkpoint, tidak untuk seleksi): 2024-2025
- Train pool refit final: 2020-2025
- Test eksternal: 2026-01-01 s.d. 2026-09-30, dieksekusi sekali di akhir
- Primary endpoint: QLIKE (log-variance, bentuk robust) seed-averaged Optuna-LSTM vs persistence & HAR-RV; DM one-sided p<0.05 (NW lag 5) + block bootstrap CI (block 20, 10k reps) upper<0
- Baselines: persistence, HAR-RV (primary); GARCH(1,1), untuned LSTM (secondary)

## Fase Study 2

- [x] Gap + protokol ditulis & di-hash sebelum data 2026 diproses
- [x] Fetch + agregasi + integrity check + freeze (hash di `data_freeze_hash.txt`)
- [x] Modul: s2_stats (QLIKE/DM/bootstrap), s2_models (samples/LSTM/HAR/GARCH), s2_runlog, s2_optuna_search, s2_final_run, s2_analyze
- [x] Smoke test pipeline (1 trial x 2 epoch; deterministik: dua run identik)
- [x] 15 unit test Study 2 lulus (`tests/test_study2.py`)
- [x] HPO penuh 50 trial di dev 2020-2023 (best trial 26, mean CV QLIKE 0.48937)
- [x] Final run: 2 model x 5 seed x (fit dev->val, fit pool->test) + baseline (run `20261028_101839_final_ab5d93`)
- [x] Analisis one-shot + verdict: **mixed_beats_but_not_significant** (test 2026: beat persistence penuh p<0.0001 + CI<0; vs HAR-RV beat point-wise & CI<0 tapi DM p=0.0534 > 0.05; untuned LSTM 0.34422 lebih baik dari Optuna-LSTM 0.40333)
- [x] Draf lengkap Bab 1–5 + 36 referensi + DOCX (`03_Naskah_Skripsi/study2/SKRIPSI_STUDY2_DRAFT.docx`)
- [ ] Front matter (abstrak, kata pengantar, daftar isi/tabel/gambar) dan lampiran
- [ ] Verifikasi format akhir dan persetujuan pembimbing

## Jaminan anti-p-hacking Study 2

1. Protokol + kriteria sukses dikunci dan di-hash sebelum ada metrik yang dihitung.
2. Amandemen data dicatat dengan konteks waktu (sebelum statistik target ada).
3. Semua pilihan model/baseline/metri/test window tidak boleh berubah setelah hasil validasi/test terlihat.
4. Test 2026 hanya diprediksi di `s2_final_run.py`; analisis one-shot di `s2_analyze.py`.
5. Setiap run punya manifest (git commit, hash data, hash protokol, env).
