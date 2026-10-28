# BAB III METODE PENELITIAN

## 3.1 Desain Penelitian

Penelitian ini menggunakan pendekatan kuantitatif dengan desain eksperimental komputasional. Pendekatan kuantitatif dipilih karena tujuan penelitian adalah mengukur akurasi peramalan, membandingkan model, dan menguji signifikansi perbedaan kinerja secara statistik. Desain eksperimental komputasional dipilih karena seluruh prosedur—pengunduhan data, agregasi, optimasi hyperparameter, pelatihan model, dan evaluasi—dijalankan melalui pipeline perangkat lunak yang dapat direproduksi.

Penelitian ini menerapkan prinsip pre-registration. Protokol penelitian dikunci dan di-hash sebelum data uji 2026 dibangun dan sebelum satu pun model Study 2 dilatih. Protokol memuat definisi data, target, fitur, pembagian data, model, baseline, ruang hyperparameter, metrik, prosedur inferensi, dan kriteria keberhasilan. Setelah protokol dikunci, tidak ada perubahan pada baseline, metrik, split, seed, atau test window. Data harian juga dibekukan dan di-hash. Dengan demikian, urutan analisis dapat diaudit: pembaca dapat memverifikasi bahwa keputusan metodologis tidak dibuat setelah melihat hasil.

Desain penelitian dapat digambarkan sebagai alur sebagai berikut. Data mentah kline 1 jam diunduh, diverifikasi, dan diagregasi menjadi data harian. Dari data harian dihitung realized variance dan enam fitur. Data dibagi menjadi periode pengembangan, validasi, dan uji eksternal. Pada periode pengembangan, Optuna mencari hyperparameter LSTM yang optimal melalui purged rolling-origin cross-validation. Hyperparameter terbaik digunakan untuk melatih model final pada train pool dengan lima seed. Model final dan empat baseline dievaluasi pada periode validasi dan periode uji. Perbedaan kinerja diuji dengan Diebold-Mariano dan moving-block bootstrap. Hasilnya digunakan untuk menjawab rumusan masalah dan menguji hipotesis.

## 3.2 Data dan Sumber

Data yang digunakan adalah data kline 1 jam pasangan BTC/USDT dari Binance Vision (Binance, 2024). Binance Vision menyediakan file bulanan yang berisi data OHLCV (open, high, low, close, volume) untuk setiap jam. Periode data mencakup Januari 2020 sampai September 2026, sehingga terdapat 81 file bulanan. Setiap file diunduh dari sumber resmi, lalu hash SHA-256-nya dicatat dalam `raw_zips_manifest.json`. File mentah tidak disimpan di repositori karena dapat diunduh ulang dan berukuran relatif besar; hash dan prosedur pengunduhan tetap tersedia untuk reproduksi.

Timestamp pada file Binance Vision dapat berupa milidetik atau mikrodetik, tergantung periode file. Pada pipeline penelitian ini, timestamp dinormalisasi ke UTC, lalu setiap bar ditempatkan pada tanggal UTC yang sesuai. Agregasi dilakukan per tanggal UTC, bukan per tanggal lokal, agar konsisten dengan konvensi pasar kripto yang beroperasi 24 jam. Setiap hari seharusnya memiliki tepat 24 bar 1 jam. Jika jumlah bar kurang dari 24, integritas data perlu diperiksa sebelum perhitungan target dilakukan.

Pada pemeriksaan awal ditemukan 15 hari pada periode 2020-01 sampai 2023-03 yang memiliki 19–23 bar akibat jendela maintenance Binance. Tidak ditemukan hari cacat pada periode validasi 2024–2025 maupun periode uji 2026. Sebelum satu pun nilai RV, fitur, atau metrik model dihitung, ditetapkan amandemen data A1: hari dengan jumlah bar kurang dari 20 dikeluarkan dari dataset, sedangkan hari dengan 20–23 bar dipertahankan dan dihitung dari bar yang tersedia. Dari aturan ini, hanya 2020-02-19 yang dikeluarkan karena memiliki 19 bar. Hari-hari dengan 20–23 bar tetap memiliki kolom `n_bars` sebagai provenance. Kalender hari yang tersisa harus kontinu, dan seluruh hari pada periode validasi serta uji harus memiliki tepat 24 bar; jika tidak, pipeline berhenti.

Setelah prosedur tersebut, dataset harian berisi 2.464 hari, mencakup 2020-01-01 sampai 2026-09-30. Hash SHA-256 file CSV harian adalah `ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b`. Hash protokol adalah `72c7588046b4ab644d814031e3329702ed884c6d9f0d0ff3c5d27660e36caba3`. Kedua hash tersebut tercatat pada manifest setiap run dan diverifikasi ulang sebelum model final dijalankan. Test window berakhir pada 2026-09-30 karena file bulanan Oktober 2026 belum diterbitkan oleh Binance pada saat penelitian dilakukan. Batas ini merupakan kendala ketersediaan data eksternal, bukan keputusan yang diambil setelah melihat hasil.

## 3.3 Target dan Fitur

Target penelitian adalah \(\log RV_{t+1}\), yaitu logaritma natural realized variance hari berikutnya. Untuk setiap hari \(t\), realized variance dihitung dari 24 bar 1 jam:

\[
RV_t = \sum_{h=1}^{24}\left[\ln\left(\frac{C_{t,h}}{O_{t,h}}\right)\right]^2.
\]

Nilai RV kemudian ditransformasi dengan \(\log RV_t = \ln(RV_t + 10^{-12})\). Enam fitur input dihitung dari informasi sampai hari \(t\) saja, sehingga tidak ada informasi masa depan yang masuk ke model. Definisi fitur disajikan pada Tabel 3.1.

**Tabel 3.1 Definisi Fitur Input**

| No | Fitur | Definisi | Alasan |
|---:|---|---|---|
| 1 | \(\log RV_t\) | \(\ln(RV_t + 10^{-12})\) | Level volatilitas hari ini; menangkap persistensi |
| 2 | \(\log range_t\) | \(\ln(H_t / L_t)\), dengan \(H_t = \max_h H_{t,h}\) dan \(L_t = \min_h L_{t,h}\) | Rentang harga intraday sebagai proksi volatilitas |
| 3 | \(\log volume_t\) | \(\ln(V_t + 10^{-12})\), dengan \(V_t = \sum_h V_{t,h}\) | Aktivitas perdagangan yang berkorelasi dengan volatilitas |
| 4 | \(\log absret_t\) | \(\ln(\lvert \ln(C_t/C_{t-1}) \rvert + 10^{-12})\) | Magnitudo pengembalian harian |
| 5 | \(rv\_mean\_5_t\) | \(\frac{1}{5}\sum_{i=0}^{4}\log RV_{t-i}\) | Komponen mingguan |
| 6 | \(rv\_mean\_22_t\) | \(\frac{1}{22}\sum_{i=0}^{21}\log RV_{t-i}\) | Komponen bulanan |

Fitur \(\log range\) dan \(\log volume\) bersifat positif dan biasanya memiliki distribusi yang menceng ke kanan; transformasi log membuat skalanya lebih sebanding dengan fitur lain. Fitur \(\log absret\) dapat bernilai negatif karena merupakan log dari nilai absolut, tetapi tetap terdefinisi selama pengembalian tidak nol. Rata-rata bergerak 5 dan 22 hari memberikan informasi tentang level volatilitas jangka pendek dan jangka menengah, sehingga model tidak hanya melihat satu titik waktu.

Standardisasi fitur dan target dilakukan dengan StandardScaler. Agar tidak terjadi kebocoran, scaler di-fit hanya pada data training fold, kemudian digunakan untuk mentransformasi data validasi dan uji. Pada pelatihan final, scaler di-fit pada bagian training dari train pool, bukan pada seluruh data. Target distandarisasi dengan rata-rata dan simpangan baku yang sama dari training set; setelah prediksi dihasilkan, nilai tersebut dikembalikan ke skala \(\log RV\) sebelum metrik dihitung. Dengan cara ini, informasi dari periode uji tidak pernah memengaruhi skala data pelatihan.

## 3.4 Pembagian Data

Data dibagi secara temporal, bukan secara acak. Pembagian acak tidak sesuai untuk deret waktu karena observasi yang berdekatan saling berkorelasi; jika data acak, model dapat melihat informasi dari masa depan secara tidak langsung. Pembagian temporal memastikan bahwa model selalu dilatih pada masa lalu dan diuji pada masa depan, sehingga skenario yang diuji menyerupai penggunaan nyata. Tabel 3.2 merangkum pembagian data.

**Tabel 3.2 Pembagian Data**

| Periode | Rentang | Jumlah hari | Peran |
|---|---|---:|---|
| Pengembangan/HPO | 2020-01-01 – 2023-12-31 | 1.460 | Pelatihan fold dan optimasi hyperparameter |
| Validasi | 2024-01-01 – 2025-12-31 | 731 | Checkpoint pipeline dan baseline; tidak dipakai memilih model |
| Train pool | 2020-01-01 – 2025-12-31 | 2.191 | Refit model final sebelum uji |
| Test eksternal | 2026-01-01 – 2026-09-30 | 273 | Evaluasi akhir; dijalankan satu kali |

Periode pengembangan digunakan untuk optimasi hyperparameter melalui purged rolling-origin cross-validation. Periode validasi digunakan sebagai checkpoint untuk memeriksa apakah pipeline menghasilkan prediksi yang wajar dan apakah baseline berjalan sebagaimana mestinya. Periode validasi tidak digunakan untuk memilih hyperparameter, epoch, atau seed. Model final dilatih ulang pada train pool 2020–2025, yang mencakup periode pengembangan dan validasi, lalu diuji pada 2026. Dengan demikian, periode uji benar-benar berada di luar data pelatihan dan data optimasi.

Sampel dibentuk dengan pendekatan sliding window. Untuk setiap hari target \(t+1\), input adalah matriks berukuran \(L \times 6\), dengan \(L\) adalah lookback. Sampel hanya dibuat jika seluruh fitur pada jendela tersebut tersedia dan tidak melintasi celah kalender yang tidak valid. Karena fitur rata-rata bergerak 22 hari membutuhkan waktu pemanasan, jumlah sampel efektif lebih kecil daripada jumlah hari. Sebagai contoh, pada model Optuna dengan lookback 16, pelatihan final menggunakan 1.923 sampel untuk fit dan 214 sampel terakhir untuk early stopping. Pada model untuned dengan lookback 21, digunakan 1.914 sampel untuk fit dan 213 sampel untuk early stopping.

## 3.5 Optimasi Hyperparameter

Optimasi hyperparameter dilakukan dengan Optuna menggunakan TPESampler dan seed 42 (Optuna Development Team, 2024). Jumlah trial ditetapkan 50. Setiap trial menjalankan purged rolling-origin cross-validation dengan lima fold pada periode pengembangan 2020–2023. Objective yang diminimalkan adalah rata-rata QLIKE dari kelima fold. Pemilihan QLIKE sebagai objective konsisten dengan metrik utama penelitian; menggunakan metrik yang berbeda untuk optimasi dan evaluasi dapat menghasilkan model yang tidak optimal pada kriteria yang sebenarnya diuji.

Purged rolling-origin cross-validation bekerja sebagai berikut. Data pengembangan diurutkan secara kronologis. Setiap fold memiliki periode training dan periode validasi yang berurutan. Antara akhir training dan awal validasi disisipkan gap sebesar lookback. Gap ini mencegah kebocoran yang dapat terjadi karena sampel target pada awal validasi menggunakan fitur dari hari-hari yang berdekatan dengan akhir training. Setelah fold pertama, jendela training diperluas dan jendela validasi bergeser ke depan, sehingga setiap fold menguji model pada periode yang belum pernah dilihat pada fold tersebut. Pendekatan ini lebih realistis daripada k-fold acak dan lebih ketat daripada single split.

Ruang pencarian hyperparameter disajikan pada Tabel 3.3. Ruang ini ditetapkan sebelum eksperimen dan tidak diubah setelah hasil terlihat. Batas bawah dan atas dipilih untuk menjaga kapasitas model tetap wajar pada data harian yang terbatas: lookback 10–30 hari, units 16–128, dan maksimal dua lapisan LSTM. Dropout dibatasi 0,05–0,40 agar regularisasi tidak terlalu lemah atau terlalu agresif. Learning rate dibatasi \(3 \times 10^{-4}\) sampai \(2 \times 10^{-3}\) karena rentang ini umumnya stabil untuk Adam pada data berskala. Batch size dibatasi pada 16, 32, atau 64 untuk menjaga efisiensi komputasi.

**Tabel 3.3 Ruang Pencarian Hyperparameter**

| Hyperparameter | Tipe | Rentang/Nilai | Keterangan |
|---|---|---|---|
| lookback | Integer | 10–30 | Panjang sekuens input |
| units | Integer | 16–128 | Jumlah unit per lapisan LSTM |
| layers | Kategorikal | 1, 2 | Jumlah lapisan LSTM |
| dropout | Float | 0,05–0,40; langkah 0,05 | Regularisasi setelah lapisan LSTM |
| learning_rate | Float (log) | \(3\times10^{-4}\) – \(2\times10^{-3}\) | Laju pembelajaran Adam |
| batch_size | Kategorikal | 16, 32, 64 | Ukuran batch pelatihan |

Setiap trial menggunakan maksimum 100 epoch, EarlyStopping dengan patience 10, dan restore best weights berdasarkan loss validasi fold. Loss yang diminimalkan adalah MSE pada \(\log RV\) terstandarisasi. MedianPruner digunakan dengan \(n_{\text{startup\_trials}} = 10\) dan \(n_{\text{warmup\_steps}} = 2\); trial yang kinerjanya jauh di bawah median pada tahap awal dapat dihentikan lebih cepat. Pruning tidak mengubah objective atau data; pruning hanya menghemat komputasi untuk konfigurasi yang tidak menjanjikan.

Pemilihan hyperparameter terbaik didasarkan pada mean CV QLIKE terendah. Nilai ini kemudian dilaporkan sebagai `best_value`. Perlu ditegaskan bahwa nilai tersebut adalah estimasi pada data pengembangan, bukan estimasi kinerja out-of-sample. Kinerja sebenarnya diukur pada periode validasi dan periode uji eksternal. Perbedaan antara mean CV QLIKE dan QLIKE test merupakan bagian dari hasil penelitian, bukan kesalahan yang perlu disembunyikan.

## 3.6 Pelatihan Final dan Multi-Seed

Setelah hyperparameter terbaik diperoleh, model final dilatih ulang pada train pool 2020–2025. Pelatihan dilakukan secara terpisah untuk setiap seed: 42, 123, 2024, 7, dan 99. Seed yang sama juga digunakan pada studi pilot, sehingga perbandingan antarstudi dapat dilakukan secara konsisten. Untuk setiap seed, data training diurutkan secara kronologis; 90% pertama digunakan untuk fit, dan 10% terakhir digunakan sebagai early-stopping set internal. Pemilihan 10% terakhir, bukan periode validasi 2024–2025, dilakukan agar periode validasi tetap bersih sebagai checkpoint dan tidak memengaruhi pelatihan model final.

Arsitektur model mengikuti hyperparameter yang dipilih Optuna. Pada penelitian ini, hyperparameter terbaik adalah lookback 16, units 22, layers 1, dropout 0,1, learning rate \(5{,}117 \times 10^{-4}\), dan batch size 16. Model menerima input \(16 \times 6\), memprosesnya melalui satu lapisan LSTM dengan 22 unit, menerapkan dropout 0,1, lalu menghasilkan satu nilai melalui lapisan dense. Pelatihan menggunakan Adam dengan learning rate tersebut, batch size 16, maksimum 100 epoch, dan EarlyStopping patience 10. Bobot terbaik dari early-stopping set dipulihkan sebelum prediksi.

Prediksi akhir untuk setiap periode adalah rata-rata prediksi kelima seed:

\[
\widehat{\log RV}_{t+1} = \frac{1}{5}\sum_{s \in \{42,123,2024,7,99\}} \widehat{\log RV}_{t+1}^{(s)}.
\]

Rata-rata seed digunakan karena model jaringan saraf memiliki variabilitas inisialisasi dan urutan batch. Memilih seed terbaik berdasarkan data uji akan menimbulkan bias seleksi; merata-ratakan seluruh seed memberikan estimasi yang lebih stabil dan lebih jujur. QLIKE per seed juga dilaporkan sebagai analisis sekunder untuk menunjukkan sebaran kinerja. Prediksi per seed disimpan dalam file CSV, sehingga pembaca dapat menghitung ulang metrik dan memverifikasi hasil.

## 3.7 Baseline

Penelitian ini menggunakan empat baseline. Baseline pertama adalah persistence, yaitu model naif yang memprediksi \(\log RV_{t+1} = \log RV_t\). Persistence penting karena menjadi patokan minimal: model yang tidak mampu mengalahkan persistence tidak memiliki nilai tambah yang jelas. Baseline kedua adalah HAR-RV, yang diestimasi dengan OLS pada train pool menggunakan komponen harian, mingguan, dan bulanan. Baseline ketiga adalah GARCH(1,1) pada log-return harian, dengan distribusi Normal dan estimasi QML. GARCH di-fit pada train pool, lalu di-refit secara expanding setiap awal bulan selama periode uji; peramalan varians satu langkah ke depan ditransformasi ke skala log. Baseline keempat adalah LSTM tanpa optimasi, dengan konfigurasi tetap lookback 21, units 64, dropout 0,2, learning rate \(10^{-3}\), batch size 32, dan satu lapisan.

Keempat baseline dipilih untuk mewakili jenis pembanding yang berbeda. Persistence mewakili baseline naif tanpa model. HAR-RV mewakili baseline ekonometrik yang menggunakan informasi intraday dan long memory. GARCH(1,1) mewakili baseline ekonometrik klasik yang menjadi standar literatur. LSTM untuned mewakili model machine learning dengan konfigurasi wajar tetapi tanpa optimasi. Dengan demikian, evaluasi tidak hanya menjawab apakah LSTM lebih baik daripada model naif, tetapi juga apakah optimasi hyperparameter memberi nilai tambah dibandingkan LSTM default.

**Tabel 3.4 Konfigurasi Baseline**

| Baseline | Spesifikasi | Estimasi |
|---|---|---|
| Persistence | \(\widehat{\log RV}_{t+1} = \log RV_t\) | Tidak ada parameter |
| HAR-RV | OLS pada \(\log RV_t\), rata-rata 7 hari, rata-rata 22 hari | Train pool 2020–2025 |
| GARCH(1,1) | Log-return harian \(\times 100\), Normal, QML | Train pool; refit expanding per bulan |
| LSTM untuned | Lookback 21, units 64, dropout 0,2, lr \(10^{-3}\), batch 32 | Train pool; 5 seed |

## 3.8 Protokol Evaluasi

Evaluasi dilakukan pada dua periode: validasi 2024–2025 dan uji eksternal 2026. Periode validasi berfungsi sebagai checkpoint untuk memastikan pipeline berjalan wajar; periode uji eksternal adalah dasar pengambilan keputusan. Metrik utama adalah QLIKE, dengan metrik sekunder MAE dan RMSE pada skala \(\log RV\). QLIKE dipilih karena merupakan loss yang robust untuk peramalan variance dan konsisten dalam peringkat model ketika proksi volatilitas mengandung noise (Patton, 2011). MAE dan RMSE dilaporkan untuk memberikan gambaran kesalahan dalam satuan log, tetapi tidak digunakan untuk menentukan keberhasilan.

Perbedaan kinerja antara model dan baseline diuji dengan Diebold-Mariano satu sisi. Loss harian yang digunakan adalah QLIKE per observasi. Untuk perbandingan model \(A\) melawan baseline \(B\), didefinisikan \(d_t = QLIKE_{A,t} - QLIKE_{B,t}\). Hipotesis nol adalah \(E[d_t] = 0\); hipotesis alternatif adalah \(E[d_t] < 0\), yang berarti model \(A\) memiliki loss lebih rendah. Statistik DM dihitung dengan estimator Newey-West lag 5 untuk mengakomodasi heteroskedastisitas dan autokorelasi. Tingkat signifikansi yang digunakan adalah \(\alpha = 0,05\).

Sebagai pelengkap, dilakukan moving-block bootstrap dengan panjang blok 20 hari, 10.000 resampel, dan seed 42. Untuk setiap resampel dihitung rata-rata \(\Delta QLIKE\), lalu diambil interval kepercayaan persentil 95%. Block bootstrap dipilih karena observasi volatilitas tidak independen; resampling per observasi akan merusak struktur autokorelasi dan menghasilkan interval yang terlalu sempit. Dengan block length 20, dependensi jangka pendek tetap terjaga dalam setiap blok. Interpretasi yang digunakan: jika batas atas interval kepercayaan berada di bawah nol, maka model secara konsisten lebih baik daripada baseline pada seluruh rentang nilai yang plausible.

Kriteria keberhasilan ditetapkan sebelum eksperimen. Model dianggap **positive** jika seluruh kondisi berikut terpenuhi pada test 2026: (1) QLIKE model lebih rendah daripada QLIKE persistence dan HAR-RV; (2) uji DM satu sisi menghasilkan \(p < 0,05\) untuk kedua perbandingan primary; dan (3) batas atas interval kepercayaan 95% block bootstrap berada di bawah nol untuk kedua perbandingan primary. Jika hanya sebagian kondisi terpenuhi, hasil dikategorikan **mixed**. Jika model kalah dari persistence atau HAR-RV, hasil dikategorikan **negative**. Kategori ini dilaporkan apa adanya; tidak ada perubahan baseline, metrik, split, seed, atau test window setelah hasil terlihat.

**Tabel 3.5 Protokol Evaluasi**

| Komponen | Pengaturan |
|---|---|
| Metrik utama | QLIKE pada skala \(\log RV\) |
| Metrik sekunder | MAE dan RMSE pada \(\log RV\) |
| Uji utama | Diebold-Mariano satu sisi, HAC Newey-West lag 5, \(\alpha = 0,05\) |
| Interval kepercayaan | Moving-block bootstrap, block 20, 10.000 resampel, seed 42 |
| Perbandingan primary | LSTM Optuna vs persistence; LSTM Optuna vs HAR-RV |
| Perbandingan sekunder | LSTM Optuna vs GARCH(1,1); LSTM Optuna vs LSTM untuned |
| Keputusan | Positive, mixed, atau negative sesuai kriteria di atas |

## 3.9 Reproduksibilitas

Reproduksibilitas merupakan bagian dari desain, bukan pelengkap. Setiap run menyimpan manifest yang memuat run ID, waktu pembuatan, commit git, hash protokol, hash data, konfigurasi lingkungan, dan daftar seed. Run ID berupa timestamp dan suffix acak, misalnya `20261028_101839_final_ab5d93`, sehingga run dapat diidentifikasi secara unik. Manifest HPO menyimpan jumlah trial, jumlah epoch maksimum, dan penanda `dev_only`; manifest final menyimpan path run HPO, daftar seed, dan penanda smoke test. Environment mencatat versi Python dan paket utama: Python 3.14.7, TensorFlow 2.22.0rc0, Optuna 5.0.0, scikit-learn 1.9.1, NumPy 2.5.3, pandas 3.0.6, arch 8.0.0, dan statsmodels 0.15.0.

Kode penelitian dipisahkan menjadi modul-modul dengan tanggung jawab yang jelas: `s2_config.py` untuk konfigurasi dan hash, `s2_data.py` untuk pengunduhan dan agregasi data, `s2_stats.py` untuk metrik dan uji statistik, `s2_models.py` untuk arsitektur dan pelatihan LSTM, `s2_optuna_search.py` untuk HPO, `s2_final_run.py` untuk pelatihan final dan baseline, `s2_analyze.py` untuk analisis one-shot, dan `s2_figures.py` untuk figur. Pemisahan ini memudahkan audit dan mengurangi risiko perubahan yang tidak disengaja. Terdapat 15 unit test yang mencakup integritas data, perhitungan QLIKE, konsistensi split, dan perilaku uji statistik. Seluruh test lulus pada saat penelitian dilakukan.

Data dan protokol di-hash sebelum eksperimen. Hash protokol yang tercatat adalah `72c7588046b4ab644d814031e3329702ed884c6d9f0d0ff3c5d27660e36caba3`, sedangkan hash CSV harian adalah `ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b`. Manifest HPO dan manifest final mencantumkan kedua hash tersebut. Sebelum model final dijalankan, pipeline memverifikasi bahwa hash protokol dan hash data masih cocok dengan yang tercatat. Jika ada perubahan, pipeline berhenti. Setelah model final selesai, analisis test dijalankan satu kali melalui `s2_analyze.py`; hasilnya disimpan sebagai `results_analysis.json` dan `results_analysis.md`. Dengan demikian, angka yang dilaporkan dalam Bab IV dapat ditelusuri kembali ke run, manifest, dan file prediksi yang sesuai.
