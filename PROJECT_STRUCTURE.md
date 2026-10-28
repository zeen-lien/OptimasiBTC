# PROJECT STRUCTURE - Skripsi LSTM + Optuna (Study 1 & Study 2)

Peta ini menjelaskan apa yang ada di repo, mana yang **final**, mana yang
**reproducible**, dan mana yang **historis**. Tujuan: tracking mudah, tidak
ada file nyasar, dan tidak ada duplikasi berat.

## 1. Peta tingkat atas

```
jurnal/
├── 01_Panduan_Kampus/        # panduan & template kampus (docx)
├── 02_Pengajuan_Judul/       # formulir pengajuan judul (Study 1 & Study 2)
├── 03_Naskah_Skripsi/        # naskah BAB 1-5 (Study 1, docx)
├── 04_Referensi_Ilmiah/      # PDF referensi + manifest (41 MB, wajib)
├── 05_Source_Code/           # kode, data, hasil (Study 1 & Study 2)
├── archive/                  # arsip historis (gitignored, tidak dipakai klaim)
├── docs/                     # protokol, audit, catatan, outline Study 2
├── release/final_20261026/   # paket rilis Study 1 (DOCX/PDF/hashes)
├── tests/                    # test Study 1 + Study 2
├── README.md                 # ringkasan proyek
├── TODOFUTURES.MD            # status & keputusan per fase
└── requirements.txt
```

## 2. Study 1 (`v1.0-final`, beku)

| Lokasi | Isi | Status |
|---|---|---|
| `05_Source_Code/model_experiment/` | pipeline harga harian (Tier 1-3, Optuna, analisis) | **final, jangan diubah** |
| `05_Source_Code/data/raw/BTCUSDT_daily_2020_2025.csv` | data harian 2.192 baris | final |
| `05_Source_Code/results/summary_final.json` | angka final Study 1 | final |
| `05_Source_Code/results/runs/final_matrix_20261025/` | run final: metrics, predictions, figures, logs, manifest | final (bobot model dihapus, lihat `MODELS_REMOVED.md`) |
| `release/final_20261026/` | DOCX/PDF + manifest + SHA-256 | **paket rilis** |
| `03_Naskah_Skripsi/` | BAB 1-5 + full naskah | final |
| `docs/PROTOCOL.md`, `NUMBER_AUDIT.md`, dll. | audit Study 1 | final |

## 3. Study 2 (branch `study2-volatility`, target: volatilitas)

| Lokasi | Isi | Status |
|---|---|---|
| `docs/STUDY2_PROTOCOL.md` + `STUDY2_PROTOCOL_HASH.txt` | protokol pre-registered + hash `72c75880…` | **beku** |
| `docs/STUDY2_GAP.md` | gap & arah penelitian | final |
| `docs/STUDY2_PROVENANCE.md` | timeline apa-dilihat-kapan | final |
| `05_Source_Code/study2_volatility/` | kode: config, data, stats, models, HPO, final run, analyze | final |
| `05_Source_Code/data/study2/btc_1h_daily_rv_2020_2026.csv` | 2.464 hari RV harian | **beku** (hash `ec2e3fb4…`) |
| `05_Source_Code/data/study2/raw_zips_manifest.json` | hash 81 file Binance Vision | final |
| `05_Source_Code/results/study2/runs/20261028_094124_optuna_hpo_5be039/` | HPO: 50 trial, best trial 26 | final |
| `05_Source_Code/results/study2/runs/20261028_101839_final_ab5d93/` | final run + `results_analysis.json/md` | **final / verdict** |

**Zip mentah 1h tidak disimpan** (3.3 MB, re-downloadable dari Binance Vision);
hash-nya sudah tercatat di `raw_zips_manifest.json`. Untuk rebuild:
`python 05_Source_Code/study2_volatility/s2_data.py`.

## 4. Cara verifikasi cepat

```powershell
# Study 2: protokol + data + hasil
python 05_Source_Code/study2_volatility/s2_data.py --verify
python -m pytest tests/test_study2.py -q

# Study 1 (jika perlu)
python -m pytest tests -q
```

## 5. Kebijakan penyimpanan

- **Disimpan:** kode, protokol, hash, data turunan (CSV), prediksi, metrik,
  figur, manifest, naskah, referensi.
- **Dihapus:** cache (`__pycache__`, `.pytest_cache`), run smoke/scratch,
  bobot model Study 1 (17.6 MB, dapat dilatih ulang deterministik), zip mentah
  Study 2 (re-downloadable).
- **Diarsipkan (gitignored):** dokumen historis pra-perbaikan di `archive/`.
- **Tidak pernah ditulis ulang:** history git Study 1 (agar tag `v1.0-final`
  dan hash rilis tetap valid).
