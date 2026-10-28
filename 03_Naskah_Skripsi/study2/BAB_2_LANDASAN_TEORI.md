# BAB II LANDASAN TEORI

## 2.1 Volatilitas dan Realized Variance

Volatilitas adalah ukuran seberapa besar nilai suatu aset bergerak dalam suatu periode. Dalam analisis keuangan, volatilitas biasanya dinyatakan sebagai simpangan baku bersyarat dari pengembalian aset. Jika \(P_t\) adalah harga aset pada waktu \(t\), maka log-return harian didefinisikan sebagai

\[
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right).
\]

Volatilitas harian \(\sigma_t\) adalah simpangan baku kondisional dari \(r_t\) diberikan informasi sampai \(t-1\). Berbeda dengan harga, volatilitas tidak teramati secara langsung; yang dapat dihitung hanyalah proksi. Salah satu proksi yang paling banyak digunakan adalah realized variance (RV), yaitu jumlah kuadrat pengembalian intraday dalam satu hari (Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002).

Pada penelitian ini, data yang tersedia adalah kline 1 jam. Setiap hari UTC terdiri atas 24 bar, masing-masing dengan harga open, high, low, close, dan volume. Realized variance harian dihitung sebagai

\[
RV_t = \sum_{h=1}^{24} \left[\ln\left(\frac{C_{t,h}}{O_{t,h}}\right)\right]^2,
\]

dengan \(C_{t,h}\) dan \(O_{t,h}\) adalah harga close dan open pada jam ke-\(h\) di hari \(t\). Karena target peramalan mencakup nilai yang sangat kecil dan sangat besar, RV ditransformasi ke skala logaritma:

\[
\log RV_t = \ln(RV_t + 10^{-12}).
\]

Penambahan \(10^{-12}\) mencegah logaritma dari nol ketika tidak ada pergerakan harga dalam satu hari. Transformasi log membuat distribusi RV lebih simetris, menstabilkan varians, dan mengurangi pengaruh outlier ekstrem. Pada data penelitian ini, \(\log RV\) memiliki rata-rata \(-7{,}6232\) dan simpangan baku \(1{,}1841\), jauh lebih teratur dibandingkan RV mentah yang memiliki rata-rata \(0{,}001017\) dan simpangan baku \(0{,}002733\).

Volatilitas memiliki beberapa sifat khas yang membedakannya dari harga. Pertama, volatility clustering: perubahan besar cenderung diikuti perubahan besar, dan perubahan kecil cenderung diikuti perubahan kecil. Kedua, mean reversion: volatilitas tidak bergerak menjauh tanpa batas, tetapi kembali ke tingkat jangka panjangnya. Ketiga, long memory: shock volatilitas dapat memengaruhi periode yang panjang, sehingga autokorelasi RV meluruh secara lambat. Keempat, leverage effect: pada banyak aset, shock negatif meningkatkan volatilitas lebih besar daripada shock positif dengan magnitudo yang sama. Sifat-sifat ini menjadi dasar mengapa volatilitas dapat dimodelkan dan diprediksi, berbeda dengan harga yang mendekati random walk.

Pada data Bitcoin, sifat-sifat tersebut tidak selalu identik dengan saham. Katsiampa (2017) membandingkan beberapa model GARCH pada Bitcoin dan menemukan bahwa model yang mengakomodasi komponen autoregresif dan asimetri memberikan fit terbaik, yang mengindikasikan bahwa dinamika volatilitas Bitcoin memiliki struktur yang lebih kaya daripada GARCH(1,1) standar. Ardia et al. (2019) menunjukkan adanya perubahan rezim dalam dinamika volatilitas Bitcoin, sehingga parameter model dapat berbeda antarperiode. Temuan-temuan ini relevan untuk desain penelitian: model harus dievaluasi pada periode yang berbeda dari periode pelatihan, dan asumsi stasioneritas parameter perlu diperiksa.

## 2.2 GARCH(1,1)

Generalized Autoregressive Conditional Heteroskedasticity (GARCH) diperkenalkan oleh Bollerslev (1986) sebagai generalisasi dari ARCH. Model GARCH(1,1) menyatakan bahwa varians kondisional bergantung pada residual kuadrat periode sebelumnya dan varians kondisional periode sebelumnya. Bentuk umumnya adalah

\[
r_t = \mu + \varepsilon_t, \qquad \varepsilon_t = \sigma_t z_t, \qquad z_t \sim N(0,1),
\]

\[
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2,
\]

dengan \(\omega > 0\), \(\alpha \geq 0\), \(\beta \geq 0\), dan \(\alpha + \beta < 1\) agar varians tidak eksplosif. Parameter \(\alpha\) mengukur reaksi volatilitas terhadap shock baru, sedangkan \(\beta\) mengukur persistensi volatilitas. Jumlah \(\alpha + \beta\) mendekati satu menunjukkan bahwa shock volatilitas memiliki dampak yang bertahan lama.

Estimasi parameter GARCH biasanya dilakukan dengan quasi-maximum likelihood (QML), yaitu memaksimumkan fungsi log-likelihood Gaussian meskipun distribusi residual sebenarnya tidak harus normal. QML tetap konsisten dan asimtotik normal di bawah kondisi tertentu, sehingga banyak digunakan dalam praktik. Untuk peramalan satu langkah ke depan, varians kondisional dapat dihitung secara rekursif:

\[
\hat{\sigma}_{t+1|t}^2 = \omega + \alpha \varepsilon_t^2 + \beta \sigma_t^2.
\]

Pada penelitian ini, GARCH(1,1) diestimasi pada log-return harian close Bitcoin yang dikalikan 100, dengan distribusi Normal dan estimasi QML. Model di-fit pada train pool 2020–2025, kemudian di-refit secara expanding setiap awal bulan selama periode uji 2026. Setiap refit menghasilkan peramalan varians satu langkah ke depan, yang kemudian ditransformasi ke skala logaritma agar sebanding dengan target \(\log RV\).

GARCH(1,1) memiliki keunggulan interpretasi dan stabilitas. Namun, model ini memiliki keterbatasan yang relevan untuk penelitian. Pertama, hubungan antara shock dan varians bersifat linear dan simetris, kecuali jika ditambahkan komponen asimetris. Kedua, GARCH bekerja pada pengembalian harian, sehingga informasi intraday hanya masuk melalui residual harian dan tidak digunakan secara langsung. Ketiga, model mengasumsikan bentuk fungsional yang tetap; jika hubungan antarwaktu berubah secara non-linear atau bergantung pada rezim, GARCH dapat tertinggal. Karena itu, GARCH(1,1) diposisikan sebagai baseline ekonometrik, bukan sebagai model yang diharapkan kalah secara otomatis.

## 2.3 HAR-RV

Heterogeneous Autoregressive Realized Volatility (HAR-RV) dikembangkan oleh Corsi (2009) untuk menangkap long memory volatilitas secara parsimonius. Ide utamanya adalah bahwa pelaku pasar memiliki horizon yang berbeda—harian, mingguan, dan bulanan—sehingga volatilitas hari ini dipengaruhi oleh volatilitas pada beberapa horizon tersebut. Model HAR-RV standar dapat ditulis sebagai

\[
RV_{t+1} = \beta_0 + \beta_d RV_t + \beta_w \bar{RV}_{t-5,t} + \beta_m \bar{RV}_{t-22,t} + \varepsilon_{t+1},
\]

dengan \(\bar{RV}_{t-5,t}\) adalah rata-rata RV selama lima hari terakhir dan \(\bar{RV}_{t-22,t}\) adalah rata-rata RV selama 22 hari terakhir. Dengan hanya tiga komponen, HAR-RV mampu menghasilkan autokorelasi yang menyerupai long memory, sehingga model ini sering menjadi baseline kuat dalam literatur realized volatility (Andersen et al., 2003).

Pada penelitian ini, HAR-RV diestimasi dengan ordinary least squares (OLS) pada skala logaritma:

\[
\log RV_{t+1} = \beta_0 + \beta_1 \log RV_t + \beta_2 \overline{\log RV}_{t-6,t} + \beta_3 \overline{\log RV}_{t-21,t} + \varepsilon_{t+1}.
\]

Komponen mingguan didefinisikan sebagai rata-rata tujuh hari terakhir termasuk hari \(t\), yaitu \(t-6\) sampai \(t\), sedangkan komponen bulanan adalah rata-rata 22 hari terakhir termasuk hari \(t\), yaitu \(t-21\) sampai \(t\). Spesifikasi ini berbeda dari HAR-RV standar Corsi (2009), yang menggunakan jendela lima hari untuk komponen mingguan. Jendela tujuh hari dipilih agar sesuai dengan kalender mingguan dan telah ditetapkan dalam protokol sebelum eksperimen; perbedaan ini dicatat karena dapat memengaruhi perbandingan dengan baseline HAR-RV pada studi lain. Model di-fit pada train pool 2020–2025 dan digunakan untuk memprediksi seluruh periode uji 2026 tanpa refit. Pemilihan OLS didasarkan pada kesederhanaan, interpretabilitas, dan sifatnya yang deterministik, sehingga cocok sebagai pembanding yang stabil.

HAR-RV memiliki keunggulan dibandingkan GARCH karena menggunakan RV intraday secara langsung dan menangkap komponen jangka panjang. Namun, HAR-RV tetap merupakan model linear dengan koefisien konstan. Jika hubungan antarfitur berubah menurut rezim atau jika terdapat interaksi non-linear, HAR-RV tidak dapat menyesuaikan diri secara otomatis. Selain itu, HAR-RV mengasumsikan bahwa koefisien yang diestimasi pada data pelatihan berlaku untuk periode uji; pada periode dengan perubahan struktur pasar, asumsi ini dapat dilanggar. Oleh karena itu, HAR-RV juga diposisikan sebagai baseline, bukan sebagai model yang harus dikalahkan dengan cara apa pun.

## 2.4 Long Short-Term Memory (LSTM)

Long Short-Term Memory (LSTM) adalah arsitektur recurrent neural network yang dirancang untuk mengatasi masalah vanishing gradient pada pemodelan dependensi jangka panjang (Hochreiter & Schmidhuber, 1997). Pada recurrent neural network biasa, informasi dari masa lalu diolah melalui hidden state yang diperbarui pada setiap langkah waktu. Ketika urutan semakin panjang, gradien yang mengalir ke belakang dapat mengecil secara eksponensial, sehingga model sulit mempelajari dependensi jangka panjang. LSTM mengatasi masalah ini dengan menambahkan cell state dan mekanisme gerbang yang mengatur aliran informasi.

Secara formal, pada langkah waktu \(t\), LSTM menerima input \(x_t\) dan hidden state sebelumnya \(h_{t-1}\). Gerbang forget \(f_t\) menentukan seberapa banyak informasi dari cell state sebelumnya yang dipertahankan; gerbang input \(i_t\) menentukan seberapa banyak informasi baru yang disimpan; dan gerbang output \(o_t\) menentukan seberapa banyak cell state yang diteruskan ke hidden state. Persamaannya adalah

\[
f_t = \sigma(W_f [h_{t-1}, x_t] + b_f),
\]

\[
i_t = \sigma(W_i [h_{t-1}, x_t] + b_i),
\]

\[
\tilde{c}_t = \tanh(W_c [h_{t-1}, x_t] + b_c),
\]

\[
c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t,
\]

\[
o_t = \sigma(W_o [h_{t-1}, x_t] + b_o),
\]

\[
h_t = o_t \odot \tanh(c_t),
\]

dengan \(\sigma\) adalah fungsi sigmoid, \(\odot\) adalah perkalian elemen-wise, \(W\) adalah matriks bobot, dan \(b\) adalah bias. Cell state \(c_t\) berfungsi sebagai memori jangka panjang yang dapat dipertahankan atau diperbarui secara selektif, sedangkan hidden state \(h_t\) adalah representasi yang diteruskan ke lapisan berikutnya atau ke output.

Pada penelitian ini, LSTM digunakan sebagai model regresi deret waktu. Input model adalah sekuens dengan panjang lookback \(L\) dan enam fitur per hari: \(\log RV\), \(\log range\), \(\log volume\), \(\log absret\), rata-rata \(\log RV\) 5 hari, dan rata-rata \(\log RV\) 22 hari. Dengan demikian, bentuk input adalah matriks \(L \times 6\). Output model adalah satu nilai skalar, yaitu prediksi \(\log RV_{t+1}\). Arsitektur model terdiri atas satu atau dua lapisan LSTM, dropout setelah lapisan LSTM, dan satu lapisan dense dengan satu unit. Fungsi aktivasi pada lapisan output adalah linear karena target berada pada skala kontinu.

Pelatihan model diimplementasikan dengan TensorFlow/Keras (TensorFlow Developers, 2024) menggunakan fungsi loss mean squared error (MSE) pada \(\log RV\) yang telah distandarisasi. Standarisasi dilakukan dengan rata-rata dan simpangan baku yang dihitung hanya dari data training fold, kemudian diterapkan pada data validasi dan uji. Optimizer yang digunakan adalah Adam, yang mengadaptasi laju pembelajaran per parameter dan umum digunakan untuk pelatihan jaringan saraf (Kingma & Ba, 2014). Dropout diterapkan untuk mengurangi overfitting dengan cara menonaktifkan sebagian unit secara acak selama pelatihan (Srivastava et al., 2014). Early stopping digunakan untuk menghentikan pelatihan ketika loss validasi tidak membaik selama sejumlah epoch, dan bobot terbaik dipulihkan.

LSTM memiliki keunggulan dalam menangkap pola non-linear dan dependensi temporal, tetapi juga memiliki risiko. Dengan data harian yang terbatas—sekitar 2.464 observasi—model dengan kapasitas besar dapat dengan mudah menghafal noise. Greff et al. (2017) menunjukkan bahwa kinerja LSTM sangat bergantung pada pilihan arsitektur dan hyperparameter, sementara Bouthillier et al. (2021) menunjukkan bahwa variabilitas akibat seed dan konfigurasi dapat menutupi perbedaan kinerja yang tampak signifikan. Oleh karena itu, penelitian ini menggunakan multi-seed, rata-rata prediksi antarseed, dan evaluasi pada periode eksternal untuk mengurangi risiko klaim yang berlebihan.

## 2.5 Optimasi Hyperparameter dan Optuna

Hyperparameter adalah parameter yang tidak dipelajari langsung dari data, tetapi ditetapkan sebelum pelatihan, seperti panjang lookback, jumlah unit, jumlah layer, dropout, laju pembelajaran, dan ukuran batch. Pemilihan hyperparameter yang tepat sangat penting karena dapat mengubah kapasitas model, kecepatan konvergensi, dan kemampuan generalisasi. Pendekatan sederhana seperti grid search mencoba seluruh kombinasi yang telah ditentukan; pendekatan ini mudah dipahami tetapi tidak efisien ketika ruang pencarian besar dan sebagian besar kombinasi tidak menjanjikan. Random search memilih kombinasi secara acak dan sering lebih efisien daripada grid search, tetapi tidak memanfaatkan informasi dari trial sebelumnya.

Bayesian optimization menawarkan pendekatan yang lebih adaptif. Secara umum, Bayesian optimization membangun model probabilistik dari fungsi objektif dan menggunakan model tersebut untuk memilih titik evaluasi berikutnya. Tree-structured Parzen Estimator (TPE) adalah salah satu metode Bayesian optimization yang populer karena cocok untuk ruang pencarian campuran (kontinu, diskret, kategorikal) dan relatif efisien secara komputasi (Bergstra et al., 2011). TPE membagi observasi menjadi dua kelompok berdasarkan nilai objektif: kelompok "baik" dengan nilai di bawah kuantil \(\gamma\), dan kelompok "buruk" di atasnya. TPE kemudian memodelkan distribusi \(l(x)\) untuk kelompok baik dan \(g(x)\) untuk kelompok buruk. Expected improvement dapat ditulis sebagai

\[
EI_{y^*}(x) \propto \left[\gamma + (1-\gamma)\frac{g(x)}{l(x)}\right]^{-1}.
\]

Untuk memaksimumkan expected improvement, TPE memilih \(x\) yang meminimumkan rasio \(g(x)/l(x)\), yaitu titik yang lebih mungkin berasal dari kelompok baik daripada kelompok buruk. Dengan cara ini, TPE menyeimbangkan eksplorasi area baru dan eksploitasi area yang sudah terbukti baik.

Optuna adalah implementasi TPE yang menyediakan API untuk mendefinisikan ruang pencarian, menjalankan trial, menyimpan riwayat, dan memangkas trial yang tidak menjanjikan (Akiba et al., 2019). Pada penelitian ini, Optuna digunakan dengan pengaturan sebagai berikut. Sampler yang dipakai adalah TPESampler dengan seed 42. Jumlah trial ditetapkan 50. Pruner yang dipakai adalah MedianPruner dengan \(n_{\text{startup\_trials}} = 10\) dan \(n_{\text{warmup\_steps}} = 2\). Objective yang diminimalkan adalah rata-rata QLIKE dari lima fold validasi. Ruang pencarian mencakup lookback 10–30, units 16–128, layers 1–2, dropout 0,05–0,40 dengan langkah 0,05, learning rate log-uniform \(3 \times 10^{-4}\) sampai \(2 \times 10^{-3}\), dan batch size 16, 32, atau 64.

Agar optimasi tidak bocor ke data uji, validasi silang dilakukan dengan skema purged rolling-origin. Data pengembangan 2020–2023 dibagi menjadi lima fold yang berurutan. Setiap fold menggunakan data sebelum periode validasi sebagai training dan data setelahnya sebagai validasi, dengan gap sebesar lookback di antara keduanya. Gap ini diperlukan karena sampel dibentuk dari sekuens; jika tidak ada gap, fitur pada awal periode validasi dapat berasal dari hari-hari yang berdekatan dengan target training, sehingga terjadi kebocoran temporal. Pendekatan purged cross-validation untuk data keuangan dibahas secara rinci oleh López de Prado (2018).

Pemilihan model berdasarkan validasi silang memiliki keterbatasan. Ketika banyak konfigurasi dicoba, nilai terbaik pada validasi dapat merupakan hasil dari selection noise, bukan sinyal yang benar-benar dapat digeneralisasi. Fenomena ini dikenal sebagai winner's curse dan menjadi salah satu alasan mengapa evaluasi pada test eksternal sangat penting. Oleh karena itu, hyperparameter terbaik dari Optuna tidak langsung diklaim sebagai model terbaik; model tersebut harus diuji pada periode yang belum pernah dilihat, dengan baseline yang jelas dan inferensi statistik yang memadai.

## 2.6 Evaluasi Peramalan Volatilitas

Evaluasi peramalan volatilitas tidak dapat menggunakan metrik yang sama dengan evaluasi peramalan harga. Volatilitas adalah variance, sehingga kesalahan pada nilai yang besar memiliki bobot yang jauh lebih besar daripada kesalahan pada nilai yang kecil. Selain itu, target yang digunakan hanyalah proksi dari volatilitas sebenarnya, sehingga metrik harus robust terhadap noise pengukuran. Patton (2011) menunjukkan bahwa tidak semua loss function konsisten dalam peringkat model ketika proksi volatilitas tidak sempurna. Dua loss yang robust adalah MSE dan QLIKE.

Pada penelitian ini, metrik utama adalah QLIKE. Untuk target \(\log RV\), QLIKE didefinisikan sebagai

\[
QLIKE = \frac{1}{T}\sum_{t=1}^{T}\left[\exp(e_t) - e_t - 1\right],
\]

dengan \(e_t = \log RV_t - \widehat{\log RV}_t\). Bentuk ini ekuivalen dengan QLIKE standar pada skala variance,

\[
QLIKE = \frac{1}{T}\sum_{t=1}^{T}\left[\frac{RV_t}{\widehat{RV}_t} - \ln\left(\frac{RV_t}{\widehat{RV}_t}\right) - 1\right],
\]

karena \(\ln(RV_t/\widehat{RV}_t) = e_t\) dan \(RV_t/\widehat{RV}_t = \exp(e_t)\). QLIKE selalu bernilai tidak negatif untuk setiap observasi, dan semakin kecil nilainya semakin baik. Keunggulan QLIKE adalah memberikan penalti yang lebih seimbang terhadap overprediksi dan underprediksi, serta tetap konsisten ketika proksi volatilitas mengandung noise (Patton, 2011).

Sebagai metrik sekunder, digunakan mean absolute error (MAE) dan root mean squared error (RMSE) pada skala \(\log RV\):

\[
MAE = \frac{1}{T}\sum_{t=1}^{T}\left|\log RV_t - \widehat{\log RV}_t\right|,
\]

\[
RMSE = \sqrt{\frac{1}{T}\sum_{t=1}^{T}\left(\log RV_t - \widehat{\log RV}_t\right)^2}.
\]

MAE dan RMSE memberikan gambaran tentang besaran kesalahan dalam satuan log, tetapi keduanya tidak secara langsung memperhitungkan sifat variance. Oleh karena itu, MAE dan RMSE dilaporkan sebagai pelengkap, bukan sebagai dasar utama pengambilan keputusan.

Untuk menguji apakah perbedaan kinerja antara dua model signifikan secara statistik, digunakan uji Diebold-Mariano (Diebold & Mariano, 1995). Misalkan \(L_{1,t}\) dan \(L_{2,t}\) adalah loss model pertama dan kedua pada waktu \(t\), dan \(d_t = L_{1,t} - L_{2,t}\). Hipotesis nol uji DM adalah \(E[d_t] = 0\), yang berarti kedua model memiliki akurasi rata-rata yang sama. Statistik DM adalah

\[
DM = \frac{\bar{d}}{\sqrt{\widehat{Var}(\bar{d})}},
\]

dengan \(\bar{d}\) adalah rata-rata \(d_t\) dan \(\widehat{Var}(\bar{d})\) adalah estimasi varians yang konsisten terhadap heteroskedastisitas dan autokorelasi. Pada penelitian ini digunakan estimator Newey-West dengan lag 5 (Newey & West, 1987). Uji dilakukan satu sisi dengan hipotesis alternatif \(E[d_t] < 0\), yaitu model pertama memiliki loss lebih rendah daripada model kedua. Nilai \(p < 0,05\) menunjukkan bukti yang cukup untuk menolak hipotesis nol pada tingkat signifikansi 5%.

Uji DM mengasumsikan bahwa statistik mengikuti distribusi normal asimtotik. Pada sampel terbatas dengan dependensi serial, asumsi ini dapat menjadi terlalu optimistis. Untuk melengkapi uji DM, digunakan moving-block bootstrap (Künsch, 1989). Blok data dengan panjang 20 hari diambil secara acak dengan pengembalian, lalu rata-rata \(\Delta QLIKE\) dihitung pada setiap resampel. Prosedur ini mengawetkan dependensi lokal dalam blok dan menghasilkan interval kepercayaan persentil 95%. Pada penelitian ini digunakan 10.000 resampel dengan seed 42. Model dianggap lebih baik secara meyakinkan jika batas atas interval kepercayaan berada di bawah nol, yang berarti seluruh rentang nilai yang plausible menunjukkan \(\Delta QLIKE < 0\).

## 2.7 Penelitian Terdahulu dan Gap

Penelitian tentang peramalan Bitcoin dapat dikelompokkan menjadi tiga arus. Arus pertama berfokus pada pemodelan volatilitas dengan model ekonometrik. Katsiampa (2017) membandingkan beberapa spesifikasi GARCH pada Bitcoin dan menemukan bahwa model dengan komponen autoregresif dan asimetri memberikan fit terbaik. Ardia et al. (2019) memperluas analisis dengan model Markov-switching GARCH dan menunjukkan adanya perubahan rezim dalam volatilitas Bitcoin. Conrad et al. (2018) menggunakan GARCH-MIDAS untuk memisahkan komponen volatilitas jangka pendek dan jangka panjang, sedangkan Aalborg et al. (2019) menghubungkan volatilitas Bitcoin dengan volume perdagangan dan faktor pasar. Studi-studi ini memberi dasar kuat tentang sifat volatilitas Bitcoin, tetapi umumnya tidak membandingkan model machine learning dan tidak menggunakan periode uji eksternal yang benar-benar terpisah.

Arus kedua berfokus pada peramalan harga dengan LSTM dan optimasi hyperparameter. Khumaidi et al. (2024) menggunakan LSTM untuk memprediksi harga Bitcoin dengan tuning manual dan melaporkan peningkatan akurasi, tetapi evaluasi dilakukan pada satu split dan tanpa baseline naif. Kervancı dan Akay (2023) menguji pengaruh delapan hyperparameter LSTM pada prediksi harga Bitcoin dan menunjukkan bahwa pemilihan hyperparameter memengaruhi hasil, tetapi belum memisahkan periode tuning dan periode uji secara ketat. Aldo et al. (2026) membandingkan enam metode optimasi hyperparameter untuk LSTM pada TRX–USD dan menemukan bahwa metode yang berbeda dapat menghasilkan peringkat yang berbeda, yang mengindikasikan pentingnya protokol evaluasi. Widad et al. (2026) membandingkan LSTM dan GRU dengan grid search pada harga Bitcoin, sedangkan Wahyuddin et al. (2025) menggunakan walk-forward validation dan sentimen pasar. Studi-studi tersebut menunjukkan minat yang besar terhadap LSTM dan HPO, tetapi targetnya masih harga dan baseline-nya belum mencakup persistence serta model ekonometrik secara bersamaan.

Arus ketiga berfokus pada peramalan volatilitas dengan machine learning. Kim dan Won (2018) menggabungkan LSTM dengan beberapa model GARCH untuk memprediksi volatilitas indeks saham dan menemukan bahwa hybrid LSTM-GARCH lebih baik daripada model tunggal. Christensen et al. (2023) menggunakan machine learning pada data frekuensi tinggi untuk meramalkan realized volatility dan menunjukkan bahwa model non-linear dapat menangkap informasi yang tidak tertangkap model linear. Studi-studi ini mendukung gagasan bahwa LSTM dapat berguna untuk volatilitas, tetapi belum menjawab pertanyaan spesifik tentang Bitcoin, optimasi Optuna, dan transfer hyperparameter ke periode eksternal.

Tabel 2.1 merangkum penelitian terdahulu yang paling relevan dan posisi penelitian ini.

**Tabel 2.1 Matriks Penelitian Terdahulu**

| No | Peneliti (tahun) | Target | Data dan model | Protokol evaluasi | Baseline | Keterbatasan untuk penelitian ini |
|---:|---|---|---|---|---|---|
| 1 | Katsiampa (2017) | Volatilitas Bitcoin | Harian; GARCH, AR-CGARCH | Satu periode; perbandingan fit | Beberapa varian GARCH | Tidak ada LSTM/HPO; tanpa test eksternal |
| 2 | Ardia et al. (2019) | Volatilitas Bitcoin | Harian; MSGARCH | Satu periode; regime switching | GARCH standar | Fokus ekonometrik; tanpa ML |
| 3 | Conrad et al. (2018) | Volatilitas kripto | Harian; GARCH-MIDAS | Satu periode; komponen jangka panjang | GARCH-MIDAS dasar | Tanpa LSTM; tanpa QLIKE |
| 4 | Aalborg et al. (2019) | Harga, volatilitas, volume | Harian; VAR | Satu periode; analisis determinan | – | Bukan peramalan out-of-sample |
| 5 | Kim dan Won (2018) | Volatilitas indeks saham | Harian; hybrid LSTM-GARCH | Satu split; tanpa HPO | GARCH, LSTM | Bukan Bitcoin; tanpa test eksternal |
| 6 | Christensen et al. (2023) | Realized volatility | Frekuensi tinggi; ML | Beberapa periode; evaluasi ketat | Model linear | Bukan Bitcoin; tanpa Optuna |
| 7 | Khumaidi et al. (2024) | Harga Bitcoin | Harian; LSTM | Satu split; tuning manual | LSTM dasar | Target harga; tanpa baseline naif |
| 8 | Kervancı dan Akay (2023) | Harga Bitcoin | Harian; LSTM + Hparam | Satu split; delapan hyperparameter | LSTM default | Target harga; tanpa test eksternal |
| 9 | Aldo et al. (2026) | Harga TRX–USD | Harian; LSTM + enam metode HPO | Satu split; perbandingan HPO | LSTM tanpa HPO | Target harga; bukan Bitcoin |
| 10 | Widad et al. (2026) | Harga Bitcoin | Harian; LSTM, GRU, grid search | Satu split | LSTM, GRU | Target harga; tanpa QLIKE |
| 11 | Wahyuddin et al. (2025) | Deret waktu umum | Walk-forward; LSTM + sentimen | Walk-forward | LSTM dasar | Bukan volatilitas Bitcoin |
| 12 | Boongasame dan Songram (2023) | Harga kripto | Harian; LSTM parameter time-varying | Satu split; variasi lookback | LSTM standar | Target harga; tanpa baseline ekonometrik |
| 13 | Aswadi dan Ependi (2025) | Harga Bitcoin dan Ethereum | Harian; LSTM | Satu split | LSTM dasar | Target harga; tanpa HPO ketat |
| 14 | Fawzi et al. (2025) | Harga Bitcoin | Harian; LSTM + Streamlit | Satu split; implementasi aplikasi | – | Fokus implementasi; evaluasi terbatas |
| 15 | Ula et al. (2024) | Harga Bitcoin | Harian; LSTM vs Random Forest | Satu split | Random Forest | Target harga; tanpa HPO |
| 16 | Patton (2011) | Metodologi | Evaluasi loss volatilitas | Kajian teoretis | – | Bukan studi empiris Bitcoin |
| 17 | Bouthillier et al. (2021) | Metodologi | Variabilitas benchmark ML | Kajian multi-seed | – | Bukan studi volatilitas |

Dari matriks tersebut, terlihat tiga celah yang menjadi dasar penelitian ini. Pertama, studi volatilitas Bitcoin yang kuat secara ekonometrik belum banyak diuji melawan LSTM yang dioptimasi secara sistematis. Kedua, studi LSTM-Bitcoin yang menggunakan Optuna umumnya menargetkan harga, bukan realized volatility, dan sering mengevaluasi pada periode yang sama dengan periode tuning. Ketiga, belum ada studi yang menggabungkan purged rolling-origin cross-validation, baseline persistence dan HAR-RV, QLIKE, uji DM, block bootstrap, dan test eksternal 2026 dalam satu protokol yang pre-registered dan dapat diaudit.

Celah tersebut dirumuskan sebagai berikut: belum ada bukti empiris yang cukup tentang apakah hyperparameter LSTM yang dipilih melalui Optuna pada data pengembangan 2020–2023 dapat bertransfer ke periode eksternal 2026 pada target realized volatility Bitcoin, ketika dibandingkan dengan baseline naif dan baseline ekonometrik. Penelitian ini mengisi celah tersebut dengan membangun pipeline yang memisahkan data pengembangan, validasi, dan uji, serta melaporkan hasil apa adanya, termasuk jika optimasi tidak memberikan keunggulan out-of-sample.

## 2.8 Kerangka Berpikir

Kerangka berpikir penelitian ini menghubungkan data, target, model, evaluasi, dan kesimpulan dalam satu alur yang dapat diaudit. Data mentah berupa kline 1 jam BTC/USDT diagregasi menjadi data harian, lalu dihitung realized variance dan fitur-fitur turunannya. Data dibagi secara temporal menjadi periode pengembangan 2020–2023, validasi 2024–2025, dan uji eksternal 2026. Pada periode pengembangan, Optuna mencari hyperparameter LSTM yang meminimalkan mean QLIKE melalui purged rolling-origin cross-validation. Hyperparameter terbaik kemudian digunakan untuk melatih model final pada train pool 2020–2025 dengan lima seed. Prediksi akhir adalah rata-rata prediksi kelima seed, bukan prediksi seed terbaik.

Model final dibandingkan dengan empat baseline: persistence, HAR-RV, GARCH(1,1), dan LSTM tanpa optimasi. Perbandingan dilakukan pada periode validasi dan periode uji eksternal. Metrik utama adalah QLIKE; metrik sekunder adalah MAE dan RMSE. Perbedaan kinerja diuji dengan Diebold-Mariano dan moving-block bootstrap. Hasil evaluasi kemudian digunakan untuk menjawab rumusan masalah: apakah pipeline bebas kebocoran berhasil dibangun, apakah model mengungguli persistence, apakah model menyaingi HAR-RV dan GARCH, dan apakah kinerja konsisten pada periode eksternal.

Secara ringkas, alur penelitian adalah:

1. Unduh dan agregasi data kline 1 jam menjadi data harian.
2. Hitung realized variance, log RV, dan enam fitur input.
3. Bagi data menjadi pengembangan, validasi, dan uji eksternal.
4. Optimasi hyperparameter LSTM dengan Optuna dan purged rolling-origin CV.
5. Latih model final dengan lima seed pada train pool.
6. Latih baseline persistence, HAR-RV, GARCH(1,1), dan LSTM default.
7. Evaluasi QLIKE, MAE, dan RMSE pada validasi dan uji.
8. Uji signifikansi dengan DM dan block bootstrap.
9. Tarik kesimpulan sesuai kriteria yang ditetapkan sebelum eksperimen.

## 2.9 Hipotesis

Berdasarkan teori dan penelitian terdahulu, hipotesis penelitian ini dirumuskan sebagai berikut.

**H1:** Model LSTM yang dioptimasi Optuna menghasilkan QLIKE lebih rendah daripada baseline persistence pada periode uji eksternal 2026.

Hipotesis ini didasarkan pada sifat volatility clustering dan long memory. Persistence menggunakan nilai \(\log RV_t\) sebagai prediksi \(\log RV_{t+1}\), sehingga hanya memanfaatkan informasi satu hari terakhir. LSTM menggunakan sekuens lima hari atau lebih dan enam fitur, sehingga memiliki kesempatan untuk menangkap pola yang tidak tertangkap persistence.

**H2:** Model LSTM yang dioptimasi Optuna menghasilkan QLIKE tidak lebih buruk daripada baseline HAR-RV dan GARCH(1,1) pada periode uji eksternal 2026.

Hipotesis ini tidak menyatakan bahwa LSTM pasti lebih baik, tetapi bahwa LSTM mampu menyaingi baseline ekonometrik yang kuat. HAR-RV dan GARCH(1,1) adalah baseline yang telah terbukti dalam literatur, sehingga klaim yang lebih realistis adalah daya saing, bukan dominasi. Jika QLIKE LSTM lebih rendah secara point estimate, maka hipotesis didukung secara deskriptif; jika perbedaannya juga signifikan secara statistik, maka dukungannya lebih kuat.

**H3:** Kinerja model LSTM yang dioptimasi Optuna pada periode uji eksternal 2026 konsisten dengan kinerja pada periode validasi 2024–2025, dalam arti tidak terjadi degradasi yang ekstrem.

Hipotesis ini menguji apakah hyperparameter yang dipilih pada data pengembangan bertransfer ke periode yang berbeda. Konsistensi tidak berarti nilai QLIKE identik, tetapi bahwa model tetap kompetitif terhadap baseline dan tidak mengalami kegagalan prediksi yang sistematis. Jika QLIKE test jauh lebih buruk daripada QLIKE validasi atau model kalah dari baseline naif, maka H3 tidak didukung.
