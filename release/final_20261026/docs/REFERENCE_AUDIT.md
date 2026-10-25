# AUDIT REFERENSI SKRIPSI

**Tanggal audit:** 2026-10-26  
**Cakupan:** 32 referensi pada DAFTAR PUSTAKA dan seluruh sitasi Bab I–V  
**Sumber data:** `05_Source_Code/generators/reference_data.py`  
**Manifest:** `04_Referensi_Ilmiah/references_manifest.csv`

## 1. Hasil Ringkas

- Jumlah referensi: **32**.
- PDF lokal tervalidasi: **21**; tidak tersedia: **0**; tidak berlaku: **11**.
- Semua karya yang disitasi di Bab I–V memiliki entri DAFTAR PUSTAKA.
- Semua entri DAFTAR PUSTAKA disitasi minimal satu kali di Bab I–V.
- Tidak ada lagi nama jurnal/korporasi yang dipakai sebagai penulis sitasi.
- Tidak ada lagi entri fiktif atau metadata DOI yang menunjuk ke makalah lain.

## 2. Koreksi Utama

| Masalah lama | Tindakan |
|---|---|
| Empat entri jurnal tanpa penulis dan tanpa bukti bibliografis | Dihapus dari daftar 32 |
| Tiga karya nyata tetapi tidak pernah disitasi | Dihapus dari daftar 32 |
| Tujuh karya disitasi tetapi tidak ada di daftar | Ditambahkan dengan metadata terverifikasi |
| Sitasi korporat (JUTIF, Bit-Tech, BRIN, Ganesha, Sakarya, IJEECS) | Diganti nama penulis dan tahun yang benar |
| Aswadi & Ependi (2022) tidak cocok dengan isi | Dikoreksi menjadi Aswadi & Ependi (2025) |
| DOI Khumaidi dkk. dan Ula dkk. salah | Dikoreksi ke DOI dan halaman yang benar |
| PDF Bouthillier, Feurer, Gu, Makridakis berisi makalah lain | Tiga diganti dengan versi benar; satu dihapus karena paywall |
| Sitasi Falkner (2018), Li (2017), Lipton (2015), Pedregosa (2011), Vaswani (2017) | Klaim diankerkan ulang ke Akiba (2019), Optuna docs, Greff (2017), dan Lim & Zohren (2021) |

## 3. Verifikasi Metadata

| No | Penulis utama | Tahun | DOI/URL | Status PDF | Verifikasi |
|---:|---|---:|---|---|---|
| 1 | Hochreiter | 1997 | https://doi.org/10.1162/neco.1997.9.8.1735 | available | Crossref DOI |
| 2 | Greff | 2017 | https://doi.org/10.1109/TNNLS.2016.2582924 | available | Crossref DOI |
| 3 | Goodfellow | 2016 | https://www.deeplearningbook.org/ | not_applicable | Buku (MIT Press) |
| 4 | Kingma | 2014 | https://doi.org/10.48550/arXiv.1412.6980 | available | arXiv |
| 5 | Srivastava | 2014 | https://jmlr.org/papers/v15/srivastava14a.html | available | JMLR |
| 6 | Akiba | 2019 | https://doi.org/10.1145/3292500.3330701 | available | Crossref DOI |
| 7 | Bergstra | 2011 | https://papers.nips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html | available | NeurIPS proceedings |
| 8 | Feurer | 2019 | https://doi.org/10.1007/978-3-030-05318-5_1 | available | Crossref DOI; PDF bab akses terbuka |
| 9 | Bouthillier | 2021 | https://doi.org/10.48550/arXiv.2103.03098 | available | arXiv; MLSys 2021 |
| 10 | Breuel | 2015 | https://doi.org/10.48550/arXiv.1508.02774 | available | arXiv |
| 11 | Lim | 2021 | https://doi.org/10.1098/rsta.2020.0209 | available | Crossref DOI |
| 12 | Gu | 2020 | https://doi.org/10.1093/rfs/hhaa009 | available | Crossref DOI |
| 13 | Makridakis | 2018 | https://doi.org/10.1016/j.ijforecast.2018.06.001 | not_applicable | Crossref DOI |
| 14 | Aldo | 2026 | https://doi.org/10.52436/1.jutif.2026.7.3.5355 | available | Crossref DOI |
| 15 | Khumaidi | 2024 | https://doi.org/10.33096/ilkom.v16i1.1831.38-45 | available | Crossref DOI |
| 16 | Fawzi | 2025 | https://doi.org/10.52436/1.jutif.2025.6.5.5168 | available | Crossref DOI |
| 17 | Ula | 2024 | https://doi.org/10.30812/matrik.v23i2.3267 | not_applicable | Crossref DOI |
| 18 | Aswadi | 2025 | https://doi.org/10.51519/journalisi.v7i3.1228 | available | Crossref DOI |
| 19 | Widad | 2026 | https://doi.org/10.32877/bt.v9i1.3887 | available | Crossref DOI |
| 20 | Kervancı | 2023 | https://doi.org/10.35377/saucis...1172027 | available | Crossref DOI |
| 21 | Wahyuddin | 2025 | https://doi.org/10.1016/j.joitmc.2024.100458 | available | Crossref DOI |
| 22 | Boongasame | 2023 | https://doi.org/10.11591/ijeecs.v30.i1.pp435-443 | available | DOI pada artikel; Crossref belum mengindeks |
| 23 | López de Prado | 2018 | — | not_applicable | Buku (Wiley) |
| 24 | Arlot | 2010 | https://doi.org/10.1214/09-SS054 | available | Crossref DOI |
| 25 | Tashman | 2000 | https://doi.org/10.1016/S0169-2070(00)00065-0 | not_applicable | Crossref DOI |
| 26 | Hyndman | 2018 | https://otexts.com/fpp2/ | not_applicable | Buku akses terbuka (OTexts) |
| 27 | Willmott | 2005 | https://doi.org/10.3354/cr030079 | available | Crossref DOI |
| 28 | Creswell | 2018 | — | not_applicable | Buku (SAGE) |
| 29 | Optuna | 2024 | https://optuna.readthedocs.io/ | not_applicable | Dokumentasi resmi |
| 30 | TensorFlow | 2024 | https://www.tensorflow.org/ | not_applicable | Dokumentasi resmi |
| 31 | Binance | 2024 | https://binance-docs.github.io/apidocs/spot/en/ | not_applicable | Dokumentasi resmi |
| 32 | Universitas | 2023 | — | not_applicable | Dokumen institusi |

## 4. Pemeriksaan Isi PDF

Setiap PDF yang tersedia diperiksa tanda tangan `%PDF-`, ukuran minimum, jumlah halaman, dan teks halaman pertama. Empat berkas lama yang isinya tidak cocok ditemukan melalui pemeriksaan ini:

| Berkas lama | Isi yang ditemukan | Tindakan |
|---|---|---|
| `Bouthillier_2020_Survey_Machine_Learning_Evaluation.pdf` | Makalah fisika AWAKE | Diganti arXiv:2103.03098 |
| `Feurer_2019_Hyperparameter_Optimization_Book_Chapter.pdf` | Makalah PID Lagrangian | Diganti bab AutoML resmi |
| `Gu_2020_Empirical_Asset_Pricing_via_Machine_Learning.pdf` | Makalah matematika Prancis | Diganti NBER w25398 |
| `Makridakis_2018_M4_Competition_Results_and_Findings.pdf` | Makalah asma | Dihapus; artikel paywall |

## 5. Keterbatasan

- Makridakis dkk. (2018), Tashman (2000), dan Ula dkk. (2024) tidak memiliki PDF akses terbuka di repositori; metadata tetap terverifikasi melalui Crossref.
- PDF Gu dkk. adalah versi NBER Working Paper w25398, bukan PDF versi RFS 2020. DOI dan volume/halaman yang dicantumkan merujuk versi terbit.
- Buku (Goodfellow dkk., Hyndman & Athanasopoulos, López de Prado, Creswell & Creswell) dan dokumen daring (Optuna, TensorFlow, Binance, UNISNU) tidak disertakan sebagai PDF.
- Verifikasi DOI tidak menjamin akses penuh; yang diverifikasi adalah kecocokan judul, penulis, tahun, dan wadah terbit.

## 6. Reproduksi

```powershell
python 05_Source_Code/generators/build_reference_manifest.py
python 05_Source_Code/generators/generate_all.py
python -m pytest tests/test_references.py -q
```

Skrip manifest menghitung ulang SHA-256 dan status setiap PDF. Perubahan metadata harus dilakukan di `reference_data.py`, bukan langsung di DOCX atau katalog.
