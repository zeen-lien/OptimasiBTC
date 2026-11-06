# Temuan Audit Study 2 — 2026-10-29

## Cakupan dan batas

Audit read-only atas protokol, kode, dokumen provenance, dan struktur artefak. Tidak menjalankan HPO, runner final, analyzer, atau statistik test 2026. Tidak mengubah protokol/hash maupun hasil historis. Perubahan user pada berkas skripsi dan pengajuan tetap dipertahankan.

## Temuan terverifikasi

| ID | Area | Bukti | Dampak/status |
|---|---|---|---|
| T1 | Purge CV | `docs/STUDY2_PROTOCOL.md:47` menetapkan `gap = lookback`; `05_Source_Code/study2_volatility/s2_optuna_search.py:50,99` memakai `lookback + 1`. `s2_models.py:38-60` menyatakan fitur sampai T−1 dan target T. | Dua jalur CV konsisten satu sama lain, tetapi menyimpang satu sampel dari protokol. Audit indeks matematis membuktikan: pada `gap = lookback`, awal fitur validasi berada pada $T_{tr} + 1$ (0 overlap hari target-fitur). Pada `gap = lookback + 1`, awal fitur validasi berada pada $T_{tr} + 2$ (membuang 1 observasi tambahan). Opsi: 1) Kembalikan kode ke protokol (`gap = lookback`); 2) Pertahankan kode dan dokumentasikan deviasi/erratum di Bab 3; 3) Buat parameter konfigurasi. Status: **TERBUKA (Menunggu persetujuan pembimbing/pengguna)**. Jangan ubah kode/protokol sepihak. |
| T2 | Final refit | Protokol `docs/STUDY2_PROTOCOL.md:49,81` menyebut refit pada train pool 2020–2025. `s2_final_run.py:51-53,67-89` menyisihkan sekitar 10% akhir sebagai early stopping, fit scaler dan model pada sekitar 90%, dan tidak refit ulang pada gabungan 100%. | Prosedur aktual berbeda dari bunyi literal protokol. Model tidak pernah dilatih pada ~7 bulan terakhir 2025, dan scaler tidak mencakup 10% akhir. Opsi: A) Pertahankan 90/10 fit/ES sebagai prosedur operasional skripsi (Bab 3); B) Refit dua-tahap pada 100% data dengan epoch tetap dari tahap 1; C) Refit pada 100% data dengan median epoch HPO. Status: **TERBUKA (Menunggu persetujuan pembimbing/pengguna)**. Jangan melatih ulang sekarang. |
| T3 | Hari yang dikeluarkan | A1 `docs/STUDY2_PROTOCOL.md:127-139` menyatakan sampel lintas gap dikeluarkan dari semua set. LSTM `s2_models.py:50-56` menolak jendela yang tidak kontigu. Persistence `s2_final_run.py:116-125` menolak target lintas gap; HAR `s2_models.py:146-184` menolak span 23-hari nonkontigu. GARCH `s2_models.py:212-256` membuang return lintas gap dan mengambil segmen kontigu setelah gap terakhir. Ditemukan bug kausalitas: GARCH sebelumnya memproses `dates` tak terbatas sehingga celah di masa depan memotong data historis; kini dibatasi `<= window_end`. | Perbaikan batas kausal `window_end` pada GARCH telah diuji secara sintetis. Batasan metodologis tetap ada: membuang data sebelum gap mendiskualifikasi 48 hari awal 2020, dan jika ada gap mendekati window evaluasi, kecukupan sampel GARCH (<250) dapat memicu kegagalan konvergensi. Status: **TERBUKA untuk tinjauan metodologis pembimbing**. |
| T4 | Alignment prediksi | `s2_analyze.py:36-44` membaca CSV tanpa validasi tanggal; `:70-73` melakukan inner merge dan mengambil `y_true` tanpa memeriksa duplikasi, cakupan, urutan, atau nilai truth antar-arm. | Join dapat membuang tanggal yang tidak cocok atau menggandakan sampel; analyzer tidak fail-closed pada target tak identik. Hasil lama tidak dihitung ulang. Perlu tes kontrak dengan fixture sintetis sebelum analyzer dipakai lagi.
| T5 | Paparan periode 2026 | `docs/STUDY2_PROVENANCE.md:41-49,55-68` mencatat baseline test terlihat saat smoke, lalu prediksi dan analisis final test dilihat. Runner `s2_final_run.py:65-80,98-110` dan analyzer `s2_analyze.py:137-143` memang menggunakan test 2026. | Periode 2026 sudah terekspos, bukan holdout untouched dan tidak boleh dipakai ulang sebagai konfirmasi. Hasil lama hanya boleh dibahas sesuai provenance dan batas yang disetujui pembimbing. Jangan menjalankan ulang analyzer/runner atau membaca ulang metrik test untuk pemilihan.
| T6 | Kriteria hasil | Protokol `docs/STUDY2_PROTOCOL.md:100-109` mensyaratkan QLIKE mengalahkan kedua baseline utama, DM satu sisi dan batas atas bootstrap CI untuk keduanya. `s2_analyze.py:102-115` mengimplementasikan verdict ini. | Kriteria tercatat di protokol dan kode analyzer selaras; hasil campuran lama tidak mengubah kriteria. Tetap audit bahwa dokumen skripsi menarasikan syarat yang sama tanpa klaim inferensial berlebihan.

## Audit referensi — temuan pembatas

`docs/REFERENCE_AUDIT_STUDY2.md` mencatat 36 karya aktif dan 16 PDF lokal, sedangkan `04_Referensi_Ilmiah/references_manifest.csv` adalah daftar 32 referensi Study 1. Jangan memakai manifest Study 1 sebagai bibliografi Study 2.

Pemeriksaan file lokal read-only memverifikasi 31 PDF di folder referensi memiliki magic bytes `%PDF-` dan ukuran nontrivial. Ini hanya membuktikan bentuk berkas, bukan bahwa tiap PDF adalah artikel yang diklaim. Pemetaan satu-per-satu PDF ke judul/DOI dan full text belum diverifikasi dalam audit ini. Dokumen audit Study 2 juga mengklaim seluruh 36 referensi disitasi; pemeriksaan string sederhana tidak mereproduksi seluruh hit, sehingga perlu audit sitasi berbasis alias/naratif yang terstruktur sebelum jumlah tersebut dikunci.

Kandidat SINTA yang sudah ditemukan di sumber resmi/laman jurnal termasuk Aswadi & Ependi (2025) sebagai konteks lokal LSTM untuk prediksi harga (bukan realized volatility), serta Khumaidi et al. (2024), Ula et al. (2024), dan beberapa studi LSTM/HPO kripto dengan target harga. Rank jurnal SINTA bukan bukti bahwa paper merupakan comparator realized-volatility yang langsung sebanding. Status periode akreditasi untuk setiap artikel belum seluruhnya diperiksa.

Status literatur saat ini: **audit awal**, bukan screening sistematis dan belum cukup untuk menyatakan novelty/gap final. Paper internasional dasar RV/HAR-RV/QLIKE tetap dibutuhkan untuk definisi dan metode; paper SINTA relevan untuk konteks nasional tetapi yang teridentifikasi sejauh ini berfokus pada prediksi harga.

Audit lanjutan read-only memperkuat klasifikasi selektif berikut: Andersen et al. (2003), Christensen et al. (2023), dan Corsi (2009) adalah kandidat langsung untuk realized volatility; Kim & Won (2018) membahas volatilitas dengan hybrid LSTM-GARCH, tetapi bukan comparator RV Bitcoin yang sudah dikonfirmasi. Katsiampa (2017), Ardia et al. (2019), dan Conrad et al. (2018) memberi konteks volatilitas kripto berbasis GARCH. Studi Aswadi & Ependi (2025), Khumaidi et al. (2024), Ula et al. (2024), serta sejumlah studi LSTM/HPO lokal lain menargetkan harga kripto, bukan realized volatility; gunakan sebagai konteks metode/nasional saja, bukan bukti langsung gap RV.

Temuan status SINTA selektif dari sumber resmi/jurnal: JUTIF dilaporkan SINTA 2 untuk periode Juni 2023–Februari 2028; bit-Tech SINTA 4 untuk Vol. 6 No. 1 2023–Vol. 10 No. 2 2027. Profil SINTA saat ini menunjukkan ILKOM Jurnal Ilmiah dan MATRIK pada S2, tetapi periode tepat yang berlaku untuk artikel terkait belum dipastikan. JISI menunjukkan konflik antara profil SINTA saat ini S2 dan pengumuman jurnal 2024 yang menyebut S3; peringkat/periode yang berlaku saat artikel 2025 terbit belum diputuskan. Ini bukan penilaian seluruh jurnal/36 entri; klaim SINTA perlu periode SK akreditasi yang cocok dengan volume/tahun paper.

Audit selektif ini tidak mencakup full text semua karya, dan sejumlah klaim metode/hasil masih berdasarkan metadata serta uraian Bab 2. Novelty/gap belum siap difinalisasi.

## Audit kelayakan arsip

Pemeriksaan referensi read-only atas inventaris 361 path dan pencarian Markdown/Python belum menghasilkan kandidat yang aman dipindah sekarang. Delapan belas skrip `05_Source_Code/model_experiment/` ditandai kandidat Study 1 historis, tetapi direferensikan oleh dokumentasi, test, generator, dan/atau release; data, hasil, manifest, protokol, serta release juga memiliki fungsi bukti historis. Tidak semua format non-Markdown/Python seperti DOCX, ZIP, dan manifest telah diperiksa untuk dependensi tersembunyi. Karena TODO mensyaratkan cross-reference lengkap, keputusan lokasi arsip dan jalur pemulihan, tidak ada file yang dipindahkan. Keputusan yang aman: pertahankan seluruh artefak; arsipkan hanya setelah pemetaan semua format dan persetujuan pengguna atas lokasi/tata letak.

## Status pekerjaan dan batas

- Suite repositori lulus; helper generator diuji; sintaks kode terkompilasi. Temuan ini tidak menutup kebutuhan fixture kontrak khusus Study 2.
- Tidak ada paper yang diunduh, file yang dipindah, generator penuh yang dijalankan, atau DOCX skripsi yang dibangun ulang.
- Persetujuan pembimbing atas judul, metode/deviations, dan framing test 2026 tetap dibutuhkan sebelum menyatakan proposal/hasil final atau mengubah metode.
- Inventaris dan hasil audit bukan pengganti validasi bersih/reproduksi penuh.

Sumber SINTA/jurnal yang diperiksa pada audit lanjutan: https://sinta.kemdikbud.go.id/journals/profile/8538 ; https://jutif.if.unsoed.ac.id/index.php/jurnal/faq-update ; https://sinta.kemdikbud.go.id/journals/profile/9935 ; https://jurnal.kdi.or.id/index.php/bt/announcement/view/23 ; https://sinta.kemdikbud.go.id/journals/profile/1698 ; https://sinta.kemdikbud.go.id/journals/profile/3962 ; https://sinta.kemdikbud.go.id/journals/profile/7045 ; http://www.journal-isi.org/index.php/isi/announcement/view/10 .

Catatan: sumber ini menunjukkan informasi yang ditemukan, bukan bukti SK/periode akreditasi untuk setiap artikel. Verifikasi penuh tetap terbuka.

#### Referensi methods

- Andersen et al. (2003): https://doi.org/10.1111/1468-0262.00418
- Christensen et al. (2023): https://doi.org/10.1093/jjfinec/nbac020
- Corsi (2009): https://doi.org/10.1093/jjfinec/nbp001
- Kim & Won (2018): https://doi.org/10.1016/j.eswa.2018.03.002
- Katsiampa (2017): https://doi.org/10.1016/j.econlet.2017.06.023
- Ardia et al. (2019): https://doi.org/10.1016/j.frl.2018.08.009
- Conrad et al. (2018): https://doi.org/10.3390/jrfm11020023
- Aalborg et al. (2019): https://doi.org/10.1016/j.frl.2018.08.010

Metadata/DOI membantu identifikasi, tetapi tidak menggantikan verifikasi full text.

#### Kandidat skrip historis yang belum aman dipindah

`05_Source_Code/model_experiment/01_fetch_binance_data.py`, `02_preprocessing.py`, `03_train_baseline_tier1.py`, `04_train_manual_tier2.py`, `05_optimize_optuna_tier3.py`, `06_evaluate_and_compare.py`, `07_run_ablation.py`, `08_analyze_results.py`, `analysis_utils.py`, `baselines.py`, `config.py`, `cv_utils.py`, `data_utils.py`, `experiment_matrix.py`, `experiment_utils.py`, `run_pipeline.py`, `run_utils.py`, `stats_utils.py`.

Daftar ini kondisional, bukan instruksi pemindahan: path tersebut masih disebut/dirujuk dan berguna untuk bukti historis Study 1.
## Tes yang aman sebelum keputusan metodologi

1. Fixture sintetis pembentukan target T memakai fitur sampai T−1, penolakan sequence lintas gap, dan penolakan NaN — ditambahkan di `tests/test_s2_split_scaler.py` (`test_build_samples_target_and_date_invariants`, `test_build_samples_rejects_gaps_and_nans_in_fixtures`).
2. Fixture sintetis isolasi scaler fit training-only dan internal validation split 90/10 tanpa melatih model TensorFlow — ditambahkan di `tests/test_s2_split_scaler.py` (`test_scaler_fit_strictly_isolated_to_training`, `test_internal_val_split_contract`).
3. Fixture sintetis tanggal duplikat, hilang, berlebih, tidak terurut, dan `y_true` berbeda — ditambahkan di `tests/test_s2_analyze.py`; validator `validate_prediction_alignment` menolak kondisi tersebut sebelum merge/metrik (6 tes).
4. Gap kalender baseline — `har_design` dan `har_fit_predict` hanya menerima window historis-target yang kalender-kontigu; persistence hanya memprediksi jika ada hari sebelumnya; GARCH membuang return lintas gap dan kini membatasi tanggal input `<= window_end` agar tidak bocor ke masa depan. Diuji di `tests/test_s2_calendar.py` (7 tes, termasuk `test_garch_forecasts_causal_to_future_gaps`).
5. Purge gap TimeSeriesSplit aktual — ditambahkan di `tests/test_s2_split_scaler.py` (`test_timeseries_split_purge_gap_exact_count_and_causal_boundaries`), membandingkan matematis `gap = lookback` (0 overlap target-fitur) vs `gap = lookback + 1` (purge 1 observasi tambahan).
6. Batas dev loader boundary enforcement — ditambahkan di `tests/test_s2_split_scaler.py` (`test_dev_loader_boundary_enforcement`), membuktikan pipeline fail loudly pada batas data yang salah.

Verifikasi saat ini:
- Tes fokus Study 2: `C:/Python314/python.exe -m pytest tests/test_s2_calendar.py tests/test_s2_analyze.py tests/test_s2_split_scaler.py -v -p no:cacheprovider --basetemp C:/Users/R1N0C/AppData/Local/hermes/cache/scratch/pytest-focused-all` lulus (19 tes, 2.93s).
- Full test suite: `C:/Python314/python.exe -m pytest tests -v -p no:cacheprovider --basetemp C:/Users/R1N0C/AppData/Local/hermes/cache/scratch/pytest-full-suite` lulus (120 tes, 5.97s).
- Kompilasi sintaks: `C:/Python314/python.exe` via `py_compile` berhasil mengompilasi 51 file Python.
- Git diff whitespace: `git diff --check` lulus tanpa error.
Tidak ada training, HPO, smoke/final runner, atau evaluasi test 2026 yang dijalankan. Tes ini memverifikasi integritas kontrak perangkat lunak dan batasan data, bukan keabsahan ilmiah metodologi.

Perbaikan aman:
- `05_Source_Code/generators/generate_bab3.py:61-64`: memetakan `\\leq` ke `≤` dan `\\geq` ke `≥`.
- `05_Source_Code/study2_volatility/s2_models.py:222-228`: `garch_forecasts` memfilter input `dates` dan `closes` ke `<= pd.Timestamp(window_end)` untuk mencegah celah kalender di masa depan memotong data historis secara non-kausal.

## Keputusan yang belum dapat diambil otomatis (Tetap Terbuka)

- **Keputusan 1 (Purge CV)**: Apakah mengubah kode `gap = lookback + 1` menjadi `gap = lookback` agar persis sesuai protokol, atau mempertahankan kode dengan mencatatnya sebagai erratum/deviasi terjustifikasi di naskah skripsi Bab 3.
- **Keputusan 2 (Final Refit)**: Apakah mempertahankan skema 90% fit / 10% early stopping yang telah tereksekusi secara historis dengan mendokumentasikannya secara transparan di naskah Bab 3, atau melakukan refit penuh 100% (yang memerlukan keputusan epoch dan rerun training baru).
- **Keputusan 3 (Kecukupan Sampel GARCH Pasca-Gap)**: Apakah strategi membuang data sebelum gap (sehingga mengabaikan data Januari–Februari 2020) dapat diterima secara ekonometrika, atau perlu pemodelan alternatif bila ada gap baru.
- **Keputusan 4 (Framing Akademik Hasil 2026 yang Terekspos)**: Bagaimana membingkai hasil test 2026 yang telah terekspos sebelumnya (status 'mixed' QLIKE 0.40333 vs HAR 0.46846, DM p=0.05344) tanpa overclaiming atau pemilihan post-hoc.

Tidak ada keputusan di atas yang diselesaikan dengan menjalankan ulang test 2026, tuning ulang, atau mengubah protokol lama secara diam-diam.
