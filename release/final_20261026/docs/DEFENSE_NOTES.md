# Catatan Persiapan Sidang — LSTM + Optuna Bitcoin

**Dokumen:** bahan pembelaan sidang munaqasyah  
**Run acuan:** `final_matrix_20261025`  
**Sumber angka:** `05_Source_Code/results/summary_final.json`  
**Status hasil:** `proposed_not_better_than_persistence`

---

## 1. Kalimat kunci yang harus dihafal

> “Penelitian ini membangun pipeline optimasi hyperparameter LSTM yang bebas kebocoran dan menguji delapan konfigurasi terkontrol pada 439 hari holdout. Model usulan E7 mencapai MAE 1.687,49 USD, sedangkan baseline persistence mencapai 1.579,80 USD. Selisih berpasangan +107,69 USD dengan CI 95% +50,82 sampai +170,90 USD, seluruhnya di atas nol. Artinya E7 **secara statistik lebih buruk** daripada persistence. Saya melaporkan hasil negatif ini apa adanya. Kontribusi penelitian adalah pipeline evaluasi terkontrol, bukan klaim keunggulan model.”

Kalimat alternatif yang lebih singkat:

> “Model usulan tidak mengalahkan baseline naif, dan saya tidak mengubah baseline atau metrik untuk memaksa kemenangan.”

---

## 2. Angka final satu halaman

### 2.1 Holdout seed utama (439 hari)

| Run | Perlakuan | RMSE (USD) | MAE (USD) | MAPE (%) |
| :--- | :--- | ---: | ---: | ---: |
| **E0** | Persistence | 2.167,24 | **1.579,80** | 1,62 |
| E1 | Tier 1 default | 2.519,46 | 1.968,00 | 1,98 |
| E2 | Tier 2 manual | 3.491,05 | 2.892,27 | 2,87 |
| E3 | Tier 3, MSE, tanpa scheduler | 2.994,73 | 2.452,53 | 2,43 |
| E4 | Tier 3, MAE, tanpa scheduler | 2.328,70 | 1.763,47 | 1,79 |
| E5 | Tier 3, MSE, plateau | 2.591,70 | 2.043,10 | 2,05 |
| E6 | Tier 3, MAE, plateau | 2.234,46 | **1.667,26** | 1,70 |
| **E7** | HPO penuh Optuna | 2.250,06 | 1.687,49 | 1,72 |

### 2.2 Agregat lima seed (MAE, mean ± std)

| Run | MAE (USD) |
| :--- | ---: |
| E1 | 2.058,81 ± 196,57 |
| E2 | 3.048,39 ± 399,48 |
| E3 | 2.281,38 ± 163,11 |
| E4 | 1.790,80 ± 167,39 |
| E5 | 2.116,59 ± 78,61 |
| E6 | 1.712,07 ± 67,48 |
| **E7** | **1.756,11 ± 89,97** |

### 2.3 Perbandingan berpasangan utama (selisih B − A)

| Perbandingan | Selisih MAE (USD) | CI 95% | Interpretasi |
| :--- | ---: | :--- | :--- |
| E7 − persistence | **+107,69** | **+50,82 s.d. +170,90** | E7 lebih buruk; signifikan |
| E7 − E6 | **+20,23** | **+1,22 s.d. +40,37** | E7 lebih buruk dari LSTM terbaik |
| E7 − E1 | −280,50 | −358,95 s.d. −210,94 | E7 lebih baik dari Tier 1 |
| E7 − E2 | −1.204,78 | −1.418,25 s.d. −1.013,51 | E7 jauh lebih baik dari Tier 2 |
| E4 − E3 | −689,06 | −839,71 s.d. −552,16 | Loss MAE membantu |
| E5 − E3 | −409,43 | −533,89 s.d. −293,39 | Scheduler membantu pada MSE |
| E6 − E3 | −785,27 | −960,55 s.d. −627,88 | Gabungan loss + scheduler membantu |

### 2.4 Konfigurasi E7

| Item | Nilai |
| :--- | :--- |
| Lookback | 25 hari |
| Units | 112 |
| Dropout | 0,10 |
| Learning rate | 0,001280918 |
| Batch size | 16 |
| Layer | 1 |
| Epoch maksimum | 100 (berjalan 100) |
| Loss | MAE |
| Scheduler | ReduceLROnPlateau |
| Early stopping | `val_loss`, patience 12 |
| Trials | 50 (13 COMPLETE, 37 PRUNED) |
| Trial terbaik | #27 |
| CV MAE trial terbaik | 1.092,794350 USD |
| Waktu optimasi | 2.427,02 detik |

### 2.5 Analisis pendukung

| Pemeriksaan | Hasil |
| :--- | :--- |
| MAE rezim bull | 1.658,64 USD |
| MAE rezim bear | 1.908,72 USD |
| MAE rezim sideways | 1.549,76 USD |
| MAE volatilitas tinggi | 3.099,31 USD |
| Akurasi arah agregat | 50,57% (222/439) |
| Akurasi pada hari naik | 3,59% |
| Akurasi pada hari turun | 99,07% |

Akurasi arah agregat yang mendekati 50% **bukan** bukti kemampuan prediksi arah yang seimbang. Model sangat bias ke arah turun: hampir semua hari naik salah diprediksi, sedangkan hampir semua hari turun benar. Ini harus disampaikan sebagai bias arah, bukan sebagai keunggulan.

---

## 3. Tiga pesan utama untuk penguji

1. **Protokolnya ketat.** Holdout 439 hari tidak pernah dipakai untuk tuning. CV berpurge dengan scaler per fold. Baseline naif dihitung kausal. CI berpasangan memakai tanggal yang identik.
2. **Hasilnya negatif dan itu dilaporkan.** E7 kalah dari persistence secara statistik. E6, LSTM terbaik, juga kalah. Tidak ada klaim superiority yang dipaksakan.
3. **Kontribusinya metodologis.** Matriks E0–E7 memisahkan efek HPO, loss, dan scheduler. Publikasi hasil negatif yang terverifikasi lebih jujur daripada klaim berlebihan.

---

## 4. Anatomi matriks E0–E7

| Run | Fungsi | Yang diisolasi |
| :--- | :--- | :--- |
| E0 | Baseline persistence | Ambang minimum |
| E1 | Tier 1 default | Kontrol default |
| E2 | Tier 2 manual | Rujukan literatur |
| E3 | Tier 3 parameters, MSE, no scheduler | Referensi ablasi |
| E4 | Tier 3 parameters, MAE, no scheduler | Efek loss |
| E5 | Tier 3 parameters, MSE, plateau | Efek scheduler |
| E6 | Tier 3 parameters, MAE, plateau | Efek gabungan |
| E7 | Full Optuna HPO, MAE, plateau | Efek HPO penuh |

**E1 vs E3** mengisolasi hyperparameter hasil pencarian pada loss/scheduler yang sama (MSE, tanpa scheduler). **E4/E5 vs E3** mengisolasi loss dan scheduler pada parameter Tier 3 yang dibekukan. **E7 vs E6** mengisolasi HPO penuh.

---

## 5. Pertanyaan yang paling mungkin muncul

### Q1. “Kenapa model usulan kalah dari persistence? Apakah penelitian gagal?”

**Jawab:** Tidak gagal sebagai penelitian, tetapi gagal sebagai klaim keunggulan model. Harga Bitcoin harian sangat mendekati random walk; perubahan satu hari sering lebih kecil daripada noise. Persistence adalah baseline yang sangat kuat untuk horizon satu hari. Yang gagal adalah asumsi bahwa HPO otomatis menghasilkan model yang lebih baik. Penelitian justru menunjukkan bahwa pada protokol bersih, HPO penuh tidak cukup untuk mengalahkan baseline naif. Ini adalah temuan yang valid dan dilaporkan secara eksplisit.

### Q2. “Kalau E7 kalah, apa kontribusi ilmiahnya?”

**Jawab:** Ada tiga kontribusi. Pertama, pipeline evaluasi terkontrol E0–E7 yang memisahkan efek HPO, loss, dan scheduler. Kedua, bukti empiris bahwa HPO penuh dapat lebih buruk daripada konfigurasi manual yang lebih sederhana (E6) dan tetap kalah dari persistence. Ketiga, demonstrasi pelaporan hasil negatif yang dapat diaudit: verdict ditentukan otomatis dari data, bukan dari narasi penulis.

### Q3. “Apakah ada kebocoran data yang membuat hasilnya aneh?”

**Jawab:** Tidak ada holdout leakage. Holdout 439 hari hanya dipakai untuk evaluasi akhir. CV berpurge 5 fold dilakukan di dalam 1.753 observasi in-sample, dengan gap sebesar lookback dan scaler yang di-fit ulang pada setiap fold. Early stopping memantau validation loss di dalam in-sample. Yang mungkin terjadi adalah *distribution shift* antara 2024-10-19 dan 2025-12-31, bukan kebocoran.

### Q4. “Kenapa E6 lebih baik daripada E7? Bukankah HPO seharusnya lebih baik?”

**Jawab:** HPO mengoptimalkan CV MAE di in-sample, bukan MAE holdout. Trial terbaik #27 memiliki CV MAE 1.092,79 USD, tetapi performanya pada holdout 1.687,49 USD. E6 memakai parameter Tier 3 yang sudah terbukti stabil dan mencapai 1.667,26 USD. Ini adalah kasus *overfitting pada prosedur seleksi* atau setidaknya ketidakcocokan antara distribusi CV dan holdout. Selisih E7 − E6 = +20,23 USD dengan CI +1,22 s.d. +40,37, jadi bukan noise semata.

### Q5. “Kenapa memakai MAE, bukan RMSE atau MAPE?”

**Jawab:** MAE adalah metrik utama karena satuannya USD dan langsung terbaca sebagai rata-rata kesalahan absolut. RMSE dan MAPE dilaporkan sebagai pemeriksaan pendukung. Arah verdict tetap sama pada ketiga metrik: E7 lebih buruk dari persistence. Kami tidak memilih metrik setelah melihat hasil untuk memaksa kemenangan.

### Q6. “Apakah CI bootstrap bisa dipercaya?”

**Jawab:** CI memakai moving-block bootstrap 7 hari dengan 2.000 resample, sehingga menjaga autokorelasi harian dan efek mingguan. Ini mengukur ketidakpastian sampling pada 439 hari holdout, bukan variasi antar-seed. Variasi antar-seed dilaporkan terpisah (E7 MAE 1.756,11 ± 89,97). `p_value` yang dilaporkan bersifat deskriptif, bukan uji formal.

### Q7. “Kenapa hanya satu aset dan satu periode uji?”

**Jawab:** Ini adalah batasan yang diakui. Studi difokuskan pada Bitcoin karena volatilitas dan likuiditasnya, serta pada satu horizon satu langkah ke depan. Generalisasi ke aset lain, horizon lebih panjang, atau pasar dengan rezim berbeda belum diuji. Klaim karena itu dibatasi pada konfigurasi dan periode yang diuji.

### Q8. “Apakah model ini layak dipakai untuk trading?”

**Jawab:** Tidak berdasarkan penelitian ini. Evaluasi tidak memasukkan transaction costs, slippage, likuiditas, atau manajemen risiko. Selain itu akurasi arah sangat bias ke bawah. Model ini adalah objek studi akademik, bukan sistem trading.

### Q9. “Kenapa Optuna hanya 50 trials? Apakah cukup?”

**Jawab:** 50 trials adalah kompromi antara anggaran komputasi dan cakupan search space. Dari 50 trials, 13 selesai dan 37 dipangkas oleh MedianPruner. Trial terbaik ditemukan pada #27. Jumlah ini cukup untuk menunjukkan arah efek pada protokol yang diuji, tetapi tidak menjamin optimum global. Penambahan trials adalah agenda lanjutan, bukan klaim yang sudah dibuktikan.

### Q10. “Kenapa hasil E7 pada beberapa seed bisa lebih baik, tetapi verdict tetap negatif?”

**Jawab:** Verdict memakai perbandingan berpasangan pada seed utama dengan tanggal holdout yang identik, sesuai aturan klaim yang ditetapkan sebelum melihat hasil. Agregat lima seed dilaporkan sebagai pemeriksaan variabilitas. Rata-rata E7 (1.756,11) tetap di atas persistence (1.579,80). Kami tidak memilih seed yang menguntungkan.

### Q11. “Apa perbedaan Tier 1, Tier 2, dan Tier 3?”

**Jawab:** Tier 1 adalah konfigurasi default sederhana (lookback 30, units 50, dropout 0,2, LR 0,001, batch 32). Tier 2 adalah replikasi manual konfigurasi Khumaidi dkk. (lookback 60, units 128, dropout 0,2, LR 0,001, batch 10). Tier 3 adalah parameter acuan yang dipakai untuk ablasi (lookback 22, units 100, dropout 0,1, LR 0,001966, batch 16). E7 melakukan pencarian penuh dan memilih lookback 25, units 112, dropout 0,10, LR 0,001281, batch 16.

### Q12. “Kenapa E3–E6 memakai parameter yang sama?”

**Jawab:** Untuk isolasi kausal. Jika parameter berubah bersamaan dengan loss atau scheduler, efeknya tidak bisa dipisahkan. E3–E6 membekukan parameter Tier 3 dan hanya mengubah loss/scheduler. E1 vs E3 memisahkan efek hyperparameter hasil pencarian pada loss/scheduler yang sama.

### Q13. “Apakah pruning MedianPruner dilakukan per epoch atau per fold?”

**Jawab:** Per fold. MedianPruner menerima nilai validasi di akhir setiap fold CV, bukan setiap epoch. Ini mencegah keputusan pruning berdasarkan epoch awal yang belum stabil. Implementasinya dapat diperiksa di `05_optimize_optuna_tier3.py` dan dijelaskan di Bab III.

### Q14. “Apakah scaler di-fit pada seluruh data?”

**Jawab:** Tidak. Scaler di-fit ulang pada window training setiap fold CV, lalu diterapkan ke validation fold. Untuk holdout, scaler di-fit pada seluruh in-sample dan diterapkan ke holdout. Tidak ada informasi holdout yang masuk ke proses fitting.

### Q15. “Apa yang akan dilakukan jika diberi waktu lebih?”

**Jawab:** Empat arah yang masuk akal: (1) fitur return/differencing atau target perubahan harga, (2) model multivariat dengan fitur on-chain/makro, (3) horizon lebih panjang dan evaluasi biaya transaksi, (4) perluasan search space dan trials dengan protokol seleksi yang lebih tahan overfitting. Semua itu adalah agenda lanjutan, bukan hasil yang sudah diklaim.

### Q16. “Mengapa hasil negatif tetap layak dijadikan skripsi?”

**Jawab:** Karena pertanyaan penelitiannya dijawab dengan bukti. Skripsi tidak harus menghasilkan model yang menang; skripsi harus menghasilkan kesimpulan yang valid. Justru klaim kemenangan tanpa baseline naif dan tanpa CI berpasangan akan lebih lemah secara ilmiah. Hasil negatif ini juga memberikan pesan praktis: HPO bukan jaminan, dan baseline naif wajib diuji.

### Q17. “Apakah 32 referensi cukup dan relevan?”

**Jawab:** Ya. Seluruh 32 referensi sudah diverifikasi metadata dan PDF-nya (21 PDF tersedia, 11 metadata-only yang statusnya dicatat). Audit sitasi dua arah memastikan tidak ada referensi yang tidak dikutip dan tidak ada sitasi yang tidak ada di daftar pustaka. Referensi mencakup LSTM, Optuna/TPE, evaluasi time series, bootstrap, baseline naif, dan konteks Bitcoin.

### Q18. “Apa yang membuat penelitian ini berbeda dari penelitian sebelumnya?”

**Jawab:** Kebanyakan penelitian LSTM+Optuna melaporkan RMSE pada satu split dan membandingkan dengan baseline yang lemah. Penelitian ini menambahkan baseline persistence/drift/seasonal naive, CV berpurge, scaler per fold, lima seed, CI berpasangan, dan matriks ablasi E0–E7. Perbedaannya bukan pada arsitektur baru, tetapi pada disiplin evaluasi.

---

## 6. Limitations yang harus disebut tanpa diminta

1. Satu aset (Bitcoin), satu pasangan (BTC/USDT), satu horizon (satu hari).
2. Satu periode holdout (2024-10-19 s.d. 2025-12-31); rezim pasar lain belum diuji.
3. Univariat; hanya harga close historis.
4. Tanpa transaction costs, slippage, atau manajemen risiko.
5. HPO mengoptimalkan CV MAE in-sample, yang tidak identik dengan holdout MAE.
6. Lima seed memberikan gambaran variabilitas, tetapi bukan distribusi lengkap.
7. Bootstrap CI mengukur ketidakpastian sampling, bukan variasi model.
8. TensorFlow 2.22.0rc0 adalah versi pra-rilis; reproducibility jangka panjang perlu dipantau.
9. Clean-room reproduction dengan environment baru belum diselesaikan.
10. Hasil tidak boleh digeneralisasi menjadi rekomendasi investasi.

---

## 7. Hal yang tidak boleh dilakukan saat sidang

- Jangan mengatakan E7 “lebih baik” atau “mendekati” persistence tanpa menyebut CI yang seluruhnya di atas nol.
- Jangan memakai angka legacy (RMSE 2.338,22; MAE 1.784,27; MAPE 1,81%) sebagai hasil final.
- Jangan mengklaim akurasi arah 50,57% sebagai kemampuan prediksi dua arah; jelaskan bias 3,59% vs 99,07%.
- Jangan mengklaim HPO “menemukan konfigurasi optimal”; katakan “trial terbaik dalam search space dan anggaran yang diuji”.
- Jangan mengklaim model siap trading.
- Jangan menyembunyikan bahwa E6 lebih baik daripada E7.

---

## 8. Referensi yang paling relevan untuk metodologi

| Topik | Referensi |
| :--- | :--- |
| LSTM | Hochreiter & Schmidhuber (1997); Greff dkk. (2017) |
| Optuna/TPE | Akiba dkk. (2019); Bergstra dkk. (2011); dokumentasi Optuna (2024) |
| Evaluasi time series | Hyndman & Athanasopoulos (2021); Tashman (2000); Makridakis dkk. (2018) |
| Purged CV / leakage | López de Prado (2018) |
| Bootstrap | Bouthillier dkk. (2021) |
| Baseline naif | Hyndman & Athanasopoulos (2021); Makridakis dkk. (2018) |
| Deep learning | Goodfellow dkk. (2016); Srivastava dkk. (2014) |
| Bitcoin | Aldo dkk. (2026); Widad dkk. (2026); Wahyuddin dkk. (2025) |

Daftar lengkap 32 referensi ada di `docs/REFERENCE_AUDIT.md` dan `04_Referensi_Ilmiah/DAFTAR_32_REFERENSI_SKRIPSI.md`.

---

## 9. Checklist sebelum masuk ruang sidang

- [ ] Baca ulang Bagian 1 dan 2 sampai angka utama hafal.
- [ ] Siapkan `summary_final.json` dan `docs/NUMBER_AUDIT.md` di laptop.
- [ ] Siapkan `docs/REPRODUCTION_REPORT.md` untuk pertanyaan reproducibility.
- [ ] Siapkan `docs/REFERENCE_AUDIT.md` untuk pertanyaan referensi.
- [ ] Pastikan master DOCX dan PDF final versi terbaru.
- [ ] Buka `docs/DECISIONS.md` untuk menjelaskan alasan metodologis.
- [ ] Latih jawaban Q1, Q3, Q4, dan Q8 minimal dua kali.
- [ ] Siapkan kalimat penutup: hasil negatif dilaporkan jujur, kontribusi ada pada pipeline dan bukti.

---

*Dokumen ini adalah bahan persiapan, bukan pengganti naskah skripsi. Semua angka bersumber dari `05_Source_Code/results/summary_final.json`.*
