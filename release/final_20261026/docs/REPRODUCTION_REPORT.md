# Laporan Reproduksi — Skripsi LSTM + Optuna Bitcoin

**Tanggal laporan:** 26 Oktober 2026  
**Run acuan:** `final_matrix_20261025`  
**Status:** run utama lengkap dan terverifikasi; verifikasi *clean-room* dengan virtual environment baru **ditunda** dan tidak diklaim selesai.

---

## 1. Ringkasan status

| Komponen | Status | Bukti |
| :--- | :--- | :--- |
| Pipeline E0–E7 lengkap | **Lulus** | `manifest.json`: 11/11 stage `success` |
| Summary final diterbitkan | **Lulus** | `05_Source_Code/results/summary_final.json`, status `complete` |
| Publish gate | **Lulus** | Tidak ada `missing_models`, `seed_coverage_issues`, atau `protocol_hash_issues` |
| Verifier naskah | **Lulus** | `verify_full_skripsi.py` → `LULUS` |
| Audit sitasi dua arah | **Lulus** | `audit_citations.py` → 32 referensi, seluruh sitasi cocok |
| Test suite | **Lulus** | `python -m pytest -q` → 86 test lulus |
| Pagination Word | **Lulus** | 77 halaman fisik, 2 section, 0 field TOC, 1.744 paragraf |
| Clean-room install baru | **Ditunda** | Menunggu unduhan TensorFlow; prosedur di Bagian 8 |

---

## 2. Lingkungan aktual

Data dari `05_Source_Code/results/runs/final_matrix_20261025/env.json`:

| Item | Nilai |
| :--- | :--- |
| Python | 3.14.7 (MSC v.1944 64-bit) |
| Executable | `C:\Python314\python.exe` |
| Platform | Windows-11-10.0.26200-SP0 |
| Prosesor | AMD64 Family 25 Model 80 Stepping 0 |
| TensorFlow | 2.22.0rc0 |
| Optuna | 5.0.0 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| NumPy | 2.5.3 |
| Matplotlib | 3.11.2 |
| joblib | 1.6.0 |
| python-docx | 1.2.0 |
| docxcompose | 2.2.0 |
| pytest | 9.1.1 |

**Catatan:** TensorFlow 2.22.0rc0 adalah versi pra-rilis. Pin ini dipertahankan agar hasil yang dilaporkan dapat direproduksi persis. Keputusan apakah akan bermigrasi ke pasangan Python/TensorFlow stabil diserahkan kepada pembimbing (D1 di `docs/DECISIONS.md`).

Environment flag `TF_DETERMINISTIC_OPS`, `PYTHONHASHSEED`, dan `CUDA_VISIBLE_DEVICES` tidak diset pada run ini. Tidak ada GPU yang dikonfigurasi eksplisit; eksekusi berjalan pada CPU.

---

## 3. Identitas run dan konfigurasi

| Item | Nilai |
| :--- | :--- |
| Run ID | `final_matrix_20261025` |
| Dibuat | 2026-10-25T16:46:48+00:00 |
| Git commit saat run | `dfe0e843c0f6615b13bc2656e984a9d4506ebd8d` (status: dirty) |
| Total durasi manifest | 4.891 detik untuk orkestrasi matriks |
| Jumlah model | 8 (E0–E7) |
| Seed | `42, 123, 2024, 7, 99` |
| Split in-sample / holdout | 1.753 / 439 |
| Holdout | 2024-10-19 s.d. 2025-12-31 |
| Metrik utama | MAE (USD) |
| CV | Purged TimeSeriesSplit, 5 fold, gap = lookback |
| Bootstrap | Moving block 7 hari, 2.000 resample, CI 95% |
| Optuna | TPESampler seed 42, MedianPruner |
| Trials | 50 (13 COMPLETE, 37 PRUNED) |
| Trial terbaik | #27, CV MAE 1.092,794350 USD |
| Waktu optimasi | 2.427,02 detik |
| Konfigurasi E7 | lookback 25, units 112, dropout 0,10, LR 0,001280918, batch 16, 1 layer, 100 epoch |

Konfigurasi lengkap per model tersimpan di `config.json`, `experiment_matrix_plan.json`, dan `summary_final.json` → `training`.

---

## 4. Hash integritas

### 4.1 Data dan protokol

| Berkas | SHA256 |
| :--- | :--- |
| `05_Source_Code/data/raw/BTCUSDT_daily_2020_2025.csv` | `35ad9016f094a3c9afe0fcc87d64f3448e75390e8eef4a8976e1db7978d0b33d` |
| `05_Source_Code/data/processed/train_insample.csv` | `d1e7ddc85c04cb75d08440dfad521df75a3632aedd68ad4fec019373a5f3abb7` |
| `05_Source_Code/data/processed/test_outofsample.csv` | `fd5448f12f9c76fb09dbddcf59f7e5d4fb96140f04884df3addd37cfa4739dae` |
| `05_Source_Code/data/processed/minmax_scaler.joblib` | `9da4f7a04d2638bd1d96cef91cec28f5c5491e3a524d719b0d4774e01f15d2c4` |
| `docs/PROTOCOL.md` | `75f60620ab16ec57741c178e33021325cd1c624875adf08c0d0c1cdb0cf62660` |
| `requirements.txt` | `7be3752a1a588bd88cf4a2e41af7fe238e36cbe94d6c6948e50fd1a5f0363014` |

### 4.2 Artefak hasil

| Berkas | SHA256 |
| :--- | :--- |
| `05_Source_Code/results/summary_final.json` | `b9274477bed648e3f45c89d1f15325c5432a2694945b71329914190005f8f7fb` |
| `03_Naskah_Skripsi/SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx` | `c805ca31f57f4875c92478154173be871647e2ffc0a73a91be86a97b4a4201eb` |

Hash seluruh berkas pada direktori run tersimpan di `data_hash.json` dan `data_hash.txt`. Hash paket rilis final ada di `release/final_20261026/HASHES_SHA256.txt`.

---

## 5. Status seluruh stage

Dari `05_Source_Code/results/runs/final_matrix_20261025/manifest.json`:

| Stage | Status | Durasi |
| :--- | :--- | ---: |
| `baseline` | success | 8 detik |
| `tier1` | success | 219 detik |
| `tier2` | success | 543 detik |
| `ablation_e3_mse_none` | success | 272 detik |
| `ablation_e4_mae_none` | success | 206 detik |
| `ablation_e5_mse_plateau` | success | 212 detik |
| `ablation_e6_mae_plateau` | success | 275 detik |
| `tier3` | success | 3.122 detik |
| `matrix` | success | 4.891 detik |
| `eval` | success | 23 detik |
| `analysis` | success | 73 detik |

Tidak ada stage yang gagal, dilewati, atau berstatus parsial.

---

## 6. Hasil final yang direproduksi

Seed utama (42), holdout 439 hari:

| Run | RMSE (USD) | MAE (USD) | MAPE (%) |
| :--- | ---: | ---: | ---: |
| E0 Persistence | 2.167,24 | **1.579,80** | 1,62 |
| E1 Tier 1 default | 2.519,46 | 1.968,00 | 1,98 |
| E2 Tier 2 manual | 3.491,05 | 2.892,27 | 2,87 |
| E3 Tier 3 MSE, no scheduler | 2.994,73 | 2.452,53 | 2,43 |
| E4 Tier 3 MAE, no scheduler | 2.328,70 | 1.763,47 | 1,79 |
| E5 Tier 3 MSE, plateau | 2.591,70 | 2.043,10 | 2,05 |
| E6 Tier 3 MAE, plateau | 2.234,46 | 1.667,26 | 1,70 |
| E7 Full Optuna HPO | 2.250,06 | 1.687,49 | 1,72 |

Agregat lima seed untuk MAE (mean ± std): E1 2.058,81 ± 196,57; E2 3.048,39 ± 399,48; E3 2.281,38 ± 163,11; E4 1.790,80 ± 167,39; E5 2.116,59 ± 78,61; E6 1.712,07 ± 67,48; E7 1.756,11 ± 89,97.

**Verdict:** `proposed_not_better_than_persistence`.

- E7 − persistence = **+107,69 USD** (E7 lebih buruk 6,82%); CI 95% **+50,82 s.d. +170,90**; seluruhnya di atas nol.
- E7 − E6 = **+20,23 USD**; CI 95% **+1,22 s.d. +40,37**; E7 juga lebih buruk daripada LSTM terbaik.
- E6 adalah LSTM terbaik (MAE 1.667,26 USD), tetapi masih di atas persistence.

---

## 7. Perintah reproduksi

Jalankan dari root repositori, dengan environment pada Bagian 2.

### 7.1 Instalasi

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 7.2 Test

```bash
python -m pytest -q
```

### 7.3 Pipeline matriks penuh

```bash
python 05_Source_Code/model_experiment/experiment_matrix.py \
  --run-id final_matrix_20261025 \
  --seeds 42,123,2024,7,99 \
  --trials 50 \
  --epochs 100 \
  --screening-epochs 25 \
  --cv-splits 5 \
  --patience 12 \
  --analyze \
  --publish
```

Perintah di atas menulis ke `05_Source_Code/results/runs/final_matrix_20261025/` dan menerbitkan `05_Source_Code/results/summary_final.json`. Gunakan `--run-id` baru untuk percobaan lain; **jangan** memakai `--legacy` kecuali memang ingin menimpa artefak lama.

### 7.4 Rebuild dan audit naskah

```bash
python 05_Source_Code/generators/generate_all.py
```

Perintah ini menjalankan generator front matter, Bab 1–5, back matter, master assembler, `verify_full_skripsi.py`, dan `audit_citations.py`. Kegagalan salah satu tahap menghentikan proses dengan exit code non-zero.

---

## 8. Clean-room reproduction (ditunda)

### 8.1 Alasan penundaan

Verifikasi *clean-room* membutuhkan unduhan TensorFlow 2.22.0rc0 beserta dependensi Scientific Python dalam virtual environment baru. Unduhan tersebut besar dan belum diselesaikan pada lingkungan penyusunan laporan ini. Karena itu, statusnya **ditunda**, bukan lulus.

### 8.2 Prosedur yang harus dijalankan

1. Buat virtual environment baru di luar folder proyek.
2. `pip install -r requirements.txt` tanpa mengubah pin.
3. Catat `pip freeze` dan versi Python.
4. Jalankan pipeline dengan `--run-id cleanroom_YYYYMMDD` (jangan menimpa run final).
5. Bandingkan `summary_final.json` baru dengan run acuan pada metrik seed utama dan agregat lima seed.
6. Bandingkan hash data dan konfigurasi.
7. Simpan hasil dan selisihnya ke laporan ini.

### 8.3 Kriteria penerimaan

| Kriteria | Toleransi |
| :--- | :--- |
| Hash data train/test/scaler | Harus identik |
| Hash `docs/PROTOCOL.md` | Harus identik |
| Status seluruh stage | Semua `success` |
| Seed coverage | 5/5 seed untuk setiap model |
| Metrik MAE/RMSE/MAPE | Selisih ≤ 1% relatif terhadap run acuan |
| Arah verdict | Harus sama: `proposed_not_better_than_persistence` |

Jika ada perbedaan, penyebab yang harus diperiksa: non-determinisme operasi TensorFlow di CPU, urutan thread/BLAS, versi driver, perbedaan versi paket, dan pengaruh `PYTHONHASHSEED`. Perbedaan yang mengubah arah verdict harus dilaporkan sebagai kegagalan reproduksi, bukan disamarkan.

---

## 9. Keterbatasan dan kejujuran pelaporan

- Tidak ada klaim bahwa E7 mengalahkan persistence. Hasil final menunjukkan sebaliknya secara statistik.
- Verifikasi clean-room, Turnitin, persetujuan pembimbing, dan backup cloud adalah item eksternal/tertunda dan tidak diklaim selesai.
- Git commit yang tercatat pada run adalah commit awal; perubahan perbaikan masih berupa working tree saat run dilakukan. Ini dicatat sebagai keterbatasan provenance, bukan disembunyikan.
- Bootstrap CI mengukur ketidakpastian sampling 439 hari holdout, bukan variasi antar-seed. Variasi antar-seed dilaporkan terpisah.
- `p_value` paired bootstrap adalah ukuran stabilitas deskriptif, bukan uji formal.
- Label rezim dan volatilitas tinggi bersifat *ex-ante* untuk analisis, bukan input model.

---

## 10. Lokasi artefak kunci

| Artefak | Lokasi |
| :--- | :--- |
| Summary final | `05_Source_Code/results/summary_final.json` |
| Manifest run | `05_Source_Code/results/runs/final_matrix_20261025/manifest.json` |
| Konfigurasi run | `05_Source_Code/results/runs/final_matrix_20261025/config.json` |
| Environment | `05_Source_Code/results/runs/final_matrix_20261025/env.json` |
| Hash data | `05_Source_Code/results/runs/final_matrix_20261025/data_hash.json` |
| Study Optuna | `05_Source_Code/results/runs/final_matrix_20261025/optuna_study.db` |
| Riwayat trial | `05_Source_Code/results/runs/final_matrix_20261025/optuna_trials_history.csv` |
| Prediksi | `05_Source_Code/results/runs/final_matrix_20261025/predictions/` |
| Figur | `05_Source_Code/results/runs/final_matrix_20261025/figures/` |
| Audit angka | `docs/NUMBER_AUDIT.md` |
| Audit referensi | `docs/REFERENCE_AUDIT.md` |
| Paket rilis | `release/final_20261026/` |
