# Paket Rilis Final — Skripsi Zaini Leon Musthofa Kamal

**Tanggal:** 26 Oktober 2026  
**Versi:** `v1.0-final`  
**Run acuan:** `final_matrix_20261025`  
**Judul:** Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin

---

## 1. Isi paket

| Berkas/Direktori | Keterangan |
| :--- | :--- |
| `SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx` | Naskah lengkap editable, 77 halaman, 6 gambar, 29 objek OMML |
| `SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.pdf` | PDF final hasil ekspor Word, 77 halaman |
| `summary_final.json` | Sumber angka tunggal seluruh naskah |
| `run_manifest.json` | Manifest 11 stage run final |
| `run_config.json` | Konfigurasi run final |
| `requirements.txt` | Pin environment Python |
| `references_manifest.csv` | Manifest 32 referensi |
| `docs/` | Protokol, keputusan, audit angka, audit referensi, laporan reproduksi, catatan sidang |
| `code/pipeline_code.zip` | Kode pipeline, generator, dan test (tanpa artefak hasil) |
| `HASHES_SHA256.txt` | SHA256 seluruh berkas paket |

---

## 2. Hasil utama

| Run | MAE (USD) | RMSE (USD) | MAPE (%) |
| :--- | ---: | ---: | ---: |
| E0 Persistence | **1.579,80** | 2.167,24 | 1,62 |
| E1 Tier 1 default | 1.968,00 | 2.519,46 | 1,98 |
| E2 Tier 2 manual | 2.892,27 | 3.491,05 | 2,87 |
| E3 Tier 3 MSE, no scheduler | 2.452,53 | 2.994,73 | 2,43 |
| E4 Tier 3 MAE, no scheduler | 1.763,47 | 2.328,70 | 1,79 |
| E5 Tier 3 MSE, plateau | 2.043,10 | 2.591,70 | 2,05 |
| E6 Tier 3 MAE, plateau | **1.667,26** | 2.234,46 | 1,70 |
| E7 Full Optuna HPO | 1.687,49 | 2.250,06 | 1,72 |

**Verdict:** `proposed_not_better_than_persistence`.

- E7 − persistence = **+107,69 USD** (6,82% lebih buruk), CI 95% **+50,82 s.d. +170,90**, seluruhnya di atas nol.
- E7 − E6 = **+20,23 USD**, CI 95% **+1,22 s.d. +40,37**.
- E6 adalah LSTM terbaik, tetapi masih di atas persistence.

Hasil negatif ini dilaporkan secara eksplisit. Paket ini tidak boleh dipresentasikan sebagai bukti bahwa E7 mengalahkan baseline.

---

## 3. Cara memeriksa integritas

Di PowerShell, dari direktori paket:

```powershell
Get-FileHash .\SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx -Algorithm SHA256
Get-FileHash .\SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.pdf -Algorithm SHA256
Get-FileHash .\summary_final.json -Algorithm SHA256
```

Bandingkan hasilnya dengan `HASHES_SHA256.txt`.

---

## 4. Cara mereproduksi pipeline

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q

python 05_Source_Code/model_experiment/experiment_matrix.py \
  --run-id final_matrix_20261025 \
  --seeds 42,123,2024,7,99 \
  --trials 50 --epochs 100 --screening-epochs 25 \
  --cv-splits 5 --patience 12 --analyze --publish
```

Ekstrak `code/pipeline_code.zip` ke root repositori terlebih dahulu. Pipeline lengkap membutuhkan waktu komputasi signifikan; clean-room verification dengan environment baru belum diselesaikan dan statusnya dicatat di `docs/REPRODUCTION_REPORT.md`.

---

## 5. Cara membangun ulang naskah

```bash
python 05_Source_Code/generators/generate_all.py
```

Perintah ini menjalankan seluruh generator, verifier naskah, dan audit sitasi. Verifier akan gagal dengan exit code non-zero bila ada angka legacy, caption stale, gambar hilang, raw `$`, atau OMML yang hilang.

---

## 6. Catatan eksternal

Item berikut **belum** diselesaikan dan tidak diklaim selesai:

- verifikasi clean-room dengan virtual environment baru (ditunda karena unduhan TensorFlow besar);
- pemeriksaan Turnitin/plagiarisme;
- persetujuan pembimbing atas framing dan split;
- backup media eksternal/cloud.

---

## 7. Dokumen pendukung

- `docs/PROTOCOL.md` — protokol evaluasi beku, hash `75f60620ab16ec57741c178e33021325cd1c624875adf08c0d0c1cdb0cf62660`.
- `docs/DECISIONS.md` — keputusan D1–D14.
- `docs/NUMBER_AUDIT.md` — pemetaan angka naskah ke `summary_final.json`.
- `docs/REFERENCE_AUDIT.md` — audit 32 referensi dan status PDF.
- `docs/REPRODUCTION_REPORT.md` — environment, hash, perintah, status reproduksi.
- `docs/DEFENSE_NOTES.md` — bahan sidang dan antisipasi pertanyaan.

---

*Dikelola dengan penuh tanggung jawab akademik oleh Zaini Leon Musthofa Kamal (231240001455), Teknik Informatika, UNISNU Jepara.*
