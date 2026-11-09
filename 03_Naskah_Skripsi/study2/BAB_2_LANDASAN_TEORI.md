# BAB II LANDASAN TEORI

## A. Volatilitas dan Realized Volatility

### 1. Karakteristik Pasar Kripto dan Data Deret Waktu Bitcoin

Pasar aset kripto, khususnya Bitcoin (BTC), beroperasi secara terdesentralisasi tanpa keberadaan otoritas perbankan terpusat serta aktif secara kontinu selama 24 jam sehari dan tujuh hari seminggu tanpa hari libur bursa. Dalam sudut pandang sains komputasi dan analisis deret waktu (*time series*), pergerakan transaksi perdagangan Bitcoin menghasilkan aliran data kronologis berfrekuensi tinggi yang sangat masif, dinamis, dan kompleks. Karakteristik perdagangan tanpa henti ini menyebabkan akumulasi informasi pasar berlangsung tanpa jeda antar-sesi perdagangan, sehingga dinamika harga aset digital memperlihatkan tingkat volatilitas yang jauh lebih tajam dibandingkan instrumen pasar modal konvensional (Lim & Zohren, 2021). Kondisi operasional 24/7 tersebut menuntut penetapan batas penanggalan harian yang konsisten dan seragam secara universal. Pada studi yang dilakukan, standardisasi batas waktu harian ditetapkan secara ketat mengacu pada zona waktu *Coordinated Universal Time* (UTC) guna menjamin keselarasan kronologis data yang dianalisis.

Penelitian terdahulu yang berfokus pada pasar kripto sering kali memusatkan perhatian pada peramalan arah atau nominal harga penutupan Bitcoin menggunakan arsitektur jaringan saraf tiruan (Aswadi & Ependi, 2025; Fawzi et al., 2025; Khumaidi et al., 2024). Namun demikian, deret harga pasar keuangan yang efisien cenderung mengikuti lintasan acak (*random walk*), di mana perubahan harga dari waktu ke waktu memiliki rasio sinyal terhadap derau (*signal-to-noise ratio*) yang sangat rendah sehingga sangat sulit diproyeksikan secara konsisten. Sebaliknya, besaran dispersi fluktuasi harga atau volatilitas memiliki dependensi temporal yang jauh lebih terstruktur dan persistensi yang tinggi (Katsiampa, 2017). Mengalihkan fokus peramalan dari estimasi nominal harga menuju estimasi volatilitas merupakan langkah strategis dalam rekayasa komputasi finansial, karena volatilitas merepresentasikan ukuran risiko pasar yang esensial bagi pengelolaan portofolio, lindung nilai, dan penetapan batas toleransi kerugian finansial.

Guna menangkap dinamika pergerakan pasar secara akurat, data penelitian dihimpun dari arsip publik Binance Vision yang menyediakan rekaman data *Open, High, Low, Close, and Volume* (OHLCV) pada frekuensi 1 jam untuk pasangan perdagangan BTC/USDT periode 1 Januari 2020 hingga 30 September 2026. Pemanfaatan data berfrekuensi intra-hari ini memungkinkan ekstraksi informasi pergerakan harga yang lebih mendalam dibandingkan hanya mengandalkan data penutupan harian semata. Struktur data deret waktu yang tersusun secara kronologis ini menjadi fondasi empiris dalam mengonstruksi proksi volatilitas pasar yang objektif dan bebas dari manipulasi sesaat, sebagaimana direkomendasikan dalam literatur ekonometrika keuangan modern (Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002).

### 2. Teori Volatilitas Finansial dan Sifat Khasnya

Dalam teori keuangan kuantitatif, volatilitas didefinisikan sebagai ukuran variabilitas atau dispersi imbal hasil (*return*) suatu aset finansial dalam rentang waktu tertentu. Volatilitas memegang peranan krusial sebagai barometer ketidakpastian pasar dan indikator risiko sistemik. Salah satu karakteristik empiris paling mendasar dari volatilitas aset keuangan adalah keberadaan fenomena pengelompokan volatilitas (*volatility clustering*), di mana gejolak fluktuasi harga yang besar cenderung diikuti oleh gejolak besar berikutnya, dan pergerakan harga yang tenang cenderung diikuti oleh periode tenang serupa (Bollerslev, 1986). Fenomena ini mengindikasikan bahwa varians imbal hasil tidak bersifat konstan sepanjang waktu (*heteroskedastic*), melainkan memiliki dependensi bersyarat yang berubah secara dinamis mengikuti informasi masa lalu.

Keberadaan *volatility clustering* membuktikan bahwa volatilitas mengandung memori temporal yang dapat dipodelkan secara matematis dan komputasional (Andersen & Bollerslev, 1998). Pada pasar aset kripto, persistensi volatilitas tersebut kerap disertai dengan lonjakan ekstrem mendadak (*volatility jumps*) dan perubahan rezim struktural yang dipicu oleh dinamika likuiditas maupun sentimen pasar global. Ardia et al. (2019) membuktikan bahwa struktur volatilitas Bitcoin mengalami pergeseran rezim dinamis antara periode tenang dan periode krisis yang sangat tajam. Karakteristik non-linear dan heteroskedastisitas bersyarat ini menuntut penerapan model komputasi yang fleksibel dan mampu beradaptasi terhadap perubahan pola temporal tanpa terbebani oleh asumsi distribusi normal yang kaku.

### 3. Proksi Realized Variance dan Transformasi Logaritmik

Secara teoretis, volatilitas laten (*latent volatility*) tidak dapat diamati secara langsung di pasar keuangan riil, sehingga besaran nilainya harus diestimasi menggunakan variabel proksi kuantitatif yang representatif. Pendekatan ekonometrika modern menunjukkan bahwa, di bawah kondisi pasar tanpa friksi, penjumlahan kuadrat imbal hasil intra-hari berfrekuensi tinggi merupakan estimator tanpa bias dari variasi kuadratik terintegrasi (*integrated variance*) dalam satu hari perdagangan penuh (Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002). Besaran kuantitatif ini dikenal sebagai *Realized Variance* (RV). Pada studi yang dilakukan, nilai $RV_t$ harian dihitung dari jumlahan kuadrat return logaritmik *open-to-close* dari 24 bar kline berdurasi 1 jam pada setiap hari UTC, sebagaimana diformulasikan pada Persamaan (2.1):

$$RV_t = \sum_{h \in \mathcal{H}_t} \left[ \ln\left(\frac{C_{t,h}}{O_{t,h}}\right) \right]^2 \tag{2.1}$$

Pada Persamaan (2.1), $C_{t,h}$ dan $O_{t,h}$ masing-masing menyatakan harga penutupan dan harga pembukaan pada bar kline ke-$h$ dalam hari kalender UTC ke-$t$, sedangkan $\mathcal{H}_t$ merepresentasikan himpunan indeks bar yang tersedia pada hari tersebut. Penggunaan formulasi *open-to-close* per bar intra-hari ini mengeliminasi distorsi fluktuasi antar-bar dan menangkap lintasan variabilitas harga secara terperinci. Mengacu pada pemaparan tersebut, proksi *realized variance* menyediakan estimasi variabilitas pasar yang jauh lebih bersih dan kaya informasi dibandingkan varians harian konvensional yang hanya bertumpu pada harga penutupan harian.

Distribusi empiris dari nilai $RV_t$ pada pasar keuangan umumnya memiliki derajat kemencengan (*skewness*) yang sangat positif dan kurtosis tinggi yang tebal pada sisi kanan (*heavy-tailed*). Guna menstabilkan varians dan memfasilitasi proses pemodelan matematis, nilai $RV_t$ ditransformasikan ke dalam skala logaritma natural ($\log RV_t$). Untuk menjaga stabilitas numerik pada saat nilai $RV$ mendekati nol, ditambahkan konstanta regularisasi kecil sebesar $10^{-12}$ ke dalam fungsi logaritma, sebagaimana dinyatakan pada Persamaan (2.2):

$$\log RV_t = \ln\left(RV_t + 10^{-12}\right) \tag{2.2}$$

Transformasi logaritmik ini mengubah sebaran data menjadi mendekati distribusi normal simetris, meredam efek pencilan ekstrem, serta mengubah relasi multiplikatif menjadi aditif yang lebih mudah dipelajari oleh model komputasional. Pada studi yang dilakukan, variabel $\log RV_t$ bertindak sebagai fitur autoregresif historis, sementara $\log RV_{t+1}$ ditetapkan sebagai target peramalan satu langkah ke depan.

## B. Model GARCH(1,1)

Model *Generalized Autoregressive Conditional Heteroskedasticity* (GARCH) yang dirumuskan oleh Bollerslev (1986) merupakan pengembangan teoretis dari model ARCH buatan Engle (1982). Model GARCH(1,1) memodelkan varians kondisional masa kini ($\sigma_t^2$) sebagai fungsi linier dari konstanta dasar ($\omega$), kuadrat residual imbal hasil satu periode sebelumnya ($\varepsilon_{t-1}^2$), dan varians kondisional satu periode sebelumnya ($\sigma_{t-1}^2$). Spesifikasi ini menjadi standar baku dalam ekonometrika keuangan untuk menangkap persistensi dan heteroskedastisitas bersyarat pada data deret waktu imbal hasil aset finansial. Struktur matematis model GARCH(1,1) didefinisikan melalui persamaan berikut:

$$r_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0, 1) \tag{2.3}$$

$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2 \tag{2.4}$$

Pada Persamaan (2.3) dan (2.4), $r_t$ menyatakan imbal hasil logaritmik harian, $\mu$ adalah rata-rata imbal hasil, $\varepsilon_t$ merupakan inovasi residual, dan $z_t$ adalah variabel acak berdistribusi normal baku independen. Parameter $\omega > 0$ merupakan konstanta varians dasar, $\alpha \ge 0$ adalah koefisien reaksi terhadap guncangan baru (*ARCH parameter*), dan $\beta \ge 0$ merepresentasikan persistensi volatilitas masa lalu (*GARCH parameter*). Syarat kestasioneran kovarians dipenuhi apabila $\alpha + \beta < 1$. Pada pasar Bitcoin, penjumlahan koefisien $\alpha + \beta$ kerap mendekati satu, yang mengindikasikan bahwa guncangan volatilitas memiliki daya tahan yang sangat lama di pasar (Katsiampa, 2017). Estimasi parameter GARCH(1,1) dilakukan menggunakan metode *Quasi-Maximum Likelihood* (QML). Pada studi yang dilakukan, model GARCH(1,1) diimplementasikan dengan skema jendela meluas (*expanding window*) bulanan sebagai salah satu model baseline pembanding ekonometrika klasik.

## C. Model HAR-RV

Model *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) yang diperkenalkan oleh Corsi (2009) dirancang untuk memodelkan struktur dependensi volatilitas jangka panjang secara parsimonis. Corsi mendasarkan formulasinya pada *Heterogeneous Market Hypothesis*, yang menyatakan bahwa pelaku pasar keuangan terbagi ke dalam berbagai kelompok dengan horizon perdagangan berbeda, mulai dari pedagang harian (*day traders*), investor mingguan, hingga institusi jangka panjang. Model HAR-RV menyusun regresi linier aditif yang menghubungkan volatilitas hari esok dengan rata-rata volatilitas pada tiga horizon waktu yang berbeda, yaitu horizon harian, mingguan, dan bulanan. Formulasi matematis model HAR-RV pada skala logaritmik dirumuskan sebagai berikut:

$$\log RV_{t+1} = \beta_0 + \beta_d \log RV_t + \beta_w \overline{\log RV}_{t-6:t} + \beta_m \overline{\log RV}_{t-21:t} + \varepsilon_{t+1} \tag{2.5}$$

Pada Persamaan (2.5), $\log RV_t$ mewakili komponen volatilitas harian, $\overline{\log RV}_{t-6:t} = (1/7)\sum_{i=0}^6 \log RV_{t-i}$ merepresentasikan komponen volatilitas mingguan yang dihitung dari rata-rata tujuh observasi harian terakhir, dan $\overline{\log RV}_{t-21:t} = (1/22)\sum_{i=0}^{21} \log RV_{t-i}$ merupakan komponen bulanan berbasis rata-rata 22 observasi harian. Parameter $\beta_0, \beta_d, \beta_w,$ dan $\beta_m$ diestimasi menggunakan metode *Ordinary Least Squares* (OLS). Model HAR-RV terbukti sangat tangguh dalam menangkap fenomena memori panjang (*long memory*) semu tanpa memerlukan estimasi fraksional yang rumit. Namun demikian, karena sifat formulasinya yang linier, model ini memiliki keterbatasan mendasar dalam merespons interaksi non-linear yang kompleks dan pergeseran rezim dinamis pada pasar aset kripto (Christensen et al., 2023; Conrad et al., 2018).

## D. Arsitektur Long Short-Term Memory (LSTM)

### 1. Keterbatasan RNN Konvensional dan Masalah Vanishing Gradient

Jaringan saraf tiruan berulang (*Recurrent Neural Network* atau RNN) dirancang khusus untuk memproses data sekuensial dengan cara meneruskan status tersembunyi (*hidden state*) dari satu langkah waktu ke langkah berikutnya. Akan tetapi, pelatihan RNN konvensional menggunakan algoritma *Backpropagation Through Time* (BPTT) menghadapi kendala teoretis yang sangat berat berupa fenomena hilangnya gradien (*vanishing gradient*) atau ledakan gradien (*exploding gradient*) ketika memproses sekuens temporal yang panjang (Hochreiter & Schmidhuber, 1997). Kondisi tersebut terjadi karena proses perambatan balik melibatkan perkalian matriks bobot secara berulang di sepanjang rantai waktu, sehingga sinyal gradien melemah secara eksponensial menuju nol. Akibatnya, RNN konvensional kehilangan kemampuan untuk mempelajari pola ketergantungan jangka panjang (*long-term dependencies*) dan hanya mampu mengingat informasi beberapa langkah ke belakang.

### 2. Anatomi Mekanisme Gerbang Sel LSTM

Guna mengatasi keterbatasan fatal pada RNN konvensional, Hochreiter dan Schmidhuber (1997) merancang arsitektur *Long Short-Term Memory* (LSTM). Inovasi utama LSTM terletak pada pengenalan jalur memori khusus yang disebut status sel (*cell state*, $c_t$) yang berfungsi sebagai jalan tol informasi temporal bergradien konstan, serta status tersembunyi (*hidden state*, $h_t$) sebagai luaran representasi sekuensial. Aliran informasi ke dalam, di dalam, dan ke luar sel memori diatur secara adaptif melalui tiga gerbang logika komputasi berbasis fungsi aktivasi non-linear sigmoid ($\sigma$) dan tangen hiperbolik ($\tanh$), sebagaimana diilustrasikan pada Gambar 2.1 (Greff et al., 2017).

![Gambar 2.1 Arsitektur Sel dan Aliran Informasi LSTM](figures/gambar_2_1_arsitektur_lstm.png)

Tahapan operasi komputasi internal pada sebuah sel LSTM pada setiap langkah waktu $t$ berlangsung melalui rangkaian formulasi matematis berikut:

1. **Gerbang Lupa (*Forget Gate*, $f_t$):** Menentukan proporsi informasi dari status sel sebelumnya ($c_{t-1}$) yang harus dibuang atau dipertahankan berdasarkan masukan saat ini ($x_t$) dan luaran status tersembunyi sebelumnya ($h_{t-1}$):
   $$f_t = \sigma\left(W_f \cdot [h_{t-1}, x_t] + b_f\right) \tag{2.6}$$

2. **Gerbang Masuk (*Input Gate*, $i_t$) dan Kandidat Sel ($\tilde{c}_t$):** Menyeleksi informasi baru yang relevan untuk disimpan ke dalam status sel:
   $$i_t = \sigma\left(W_i \cdot [h_{t-1}, x_t] + b_i\right) \tag{2.7}$$
   $$\tilde{c}_t = \tanh\left(W_c \cdot [h_{t-1}, x_t] + b_c\right) \tag{2.8}$$

3. **Pembaruan Status Sel (*Cell State Update*, $c_t$):** Memperbarui memori jangka panjang dengan menggabungkan informasi masa lalu yang dipertahankan dan kandidat informasi baru melalui operasi perkalian elemen-demi-elemen ($\odot$):
   $$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \tag{2.9}$$

4. **Gerbang Keluar (*Output Gate*, $o_t$) dan Status Tersembunyi ($h_t$):** Menentukan informasi status sel yang akan diproyeksikan sebagai status tersembunyi untuk langkah waktu saat ini:
   $$o_t = \sigma\left(W_o \cdot [h_{t-1}, x_t] + b_o\right) \tag{2.10}$$
   $$h_t = o_t \odot \tanh(c_t) \tag{2.11}$$

Pada Persamaan (2.6) hingga (2.11), $W_f, W_i, W_c,$ dan $W_o$ bertindak sebagai matriks bobot sinaptik, sedangkan $b_f, b_i, b_c,$ dan $b_o$ merupakan vektor bias untuk masing-masing gerbang. Simbol $\sigma$ merepresentasikan fungsi aktivasi non-linear sigmoid yang memetakan nilai ke dalam rentang $[0, 1]$, $\tanh$ adalah fungsi tangen hiperbolik dengan rentang luaran $[-1, 1]$, dan operator $\odot$ melambangkan perkalian elemen-demi-elemen (*Hadamard product*). Melalui mekanisme gerbang interaktif tersebut, LSTM mampu mempertahankan sinyal ketergantungan temporal jangka panjang secara stabil sekaligus menyaring derau sesaat, menjadikannya model yang sangat adaptif dalam memodelkan dinamika volatilitas finansial non-linear (Kim & Won, 2018).

### 3. Algoritma Optimasi Adam dan Regularisasi Dropout

Pelatihan bobot sinaptik jaringan saraf LSTM memerlukan algoritma optimasi gradien yang efisien dan stabil. Pada studi yang dilakukan, pembaruan bobot model dilatih menggunakan algoritma *Adaptive Moment Estimation* (Adam) yang dikembangkan oleh Kingma dan Ba (2014). Algoritma Adam menggabungkan keunggulan metode momentum dan *Root Mean Square Propagation* (RMSProp) dengan cara menghitung estimasi momen pertama (rata-rata terbobot gradien) dan estimasi momen kedua (rata-rata terbobot kuadrat gradien) secara adaptif untuk setiap parameter bobot. Mekanisme penyesuaian laju pembelajaran mandiri ini membuat algoritma Adam sangat tangguh dalam menghadapi lanskap fungsi kerugian yang bising dan memiliki permukaan gradien yang tidak merata.

Di samping hal tersebut, guna mencegah terjadinya fenomena lewat-jenuh (*overfitting*) pada data pelatihan, diterapkan teknik regularisasi *Dropout* yang dirumuskan oleh Srivastava et al. (2014). Regularisasi *Dropout* bekerja dengan cara menonaktifkan sejumlah unit neuron tersembunyi secara acak pada setiap iterasi pelatihan sesuai dengan probabilitas tertentu ($p$). Proses penonaktifan stokastik ini memutus ketergantungan ko-adaptasi antar-neuron yang berlebihan, sehingga mendorong jaringan saraf tiruan untuk mengekstraksi representasi fitur yang lebih kokoh, mandiri, dan mampu bergeneralisasi dengan baik pada data uji yang belum pernah dilihat sebelumnya.

## E. Optimasi Hyperparameter Berbasis Bayesian dengan Optuna

### 1. Paradigma Hyperparameter Optimization (HPO)

Kinerja prediktif model pembelajaran mendalam LSTM sangat ditentukan oleh konfigurasi parameter eksternal atau *hyperparameter*, meliputi panjang jendela historis (*lookback window*, $L$), jumlah unit neuron tersembunyi ($U$), kedalaman lapisan, tingkat regularisasi *dropout*, laju pembelajaran (*learning rate*), dan ukuran *batch*. Pendekatan penalaan tradisional seperti *Grid Search* memerlukan biaya komputasi yang sangat masif karena mengevaluasi seluruh kombinasi secara diskret dan tidak fleksibel terhadap penambahan dimensi parameter. Sementara itu, *Random Search* mengeksplorasi kombinasi secara acak tanpa memanfaatkan riwayat informasi percobaan sebelumnya (Bergstra et al., 2011). Kondisi tersebut menyebabkan pencarian hyperparameter sering kali terjebak pada konfigurasi suboptimal atau menghabiskan sumber daya komputasi yang tidak sebanding dengan peningkatan performa yang diperoleh.

### 2. Algoritma Tree-structured Parzen Estimator (TPE)

Guna mengatasi kelemahan metode penalaan konvensional, Bergstra et al. (2011) mengembangkan algoritma *Tree-structured Parzen Estimator* (TPE) sebagai pendekatan optimasi berbasis Bayesian sekuensial. Berbeda dengan pendekatan regresi proses Gaussian standar yang memodelkan fungsi objektif $P(y|x)$ secara langsung, algoritma TPE memodelkan probabilitas konfigurasi parameter $x$ bersyarat terhadap nilai fungsi objektif $y$, yaitu $P(x|y)$, menggunakan estimator densitas kernel Parzen. Algoritma ini membagi ruang konfigurasi parameter menjadi dua kelompok kepadatan probabilitas berdasarkan ambang batas kuantil performa $y^*$:

$$P(x|y) = \ell(x) \quad \text{untuk } y < y^*, \qquad P(x|y) = g(x) \quad \text{untuk } y \ge y^* \tag{2.12}$$

Pada Persamaan (2.12), $\ell(x)$ mewakili distribusi konfigurasi hyperparameter yang menghasilkan nilai fungsi kerugian rendah (kelompok berperforma unggul), sedangkan $g(x)$ merepresentasikan distribusi dari konfigurasi yang menghasilkan performa buruk. Algoritma TPE mengoptimalkan kriteria *Expected Improvement* (EI) dengan cara memaksimalkan rasio kepadatan probabilitas $\ell(x) / g(x)$:

$$EI_{y^*}(x) \propto \left( \gamma + \frac{g(x)}{\ell(x)}(1 - \gamma) \right)^{-1} \tag{2.13}$$

Melalui formulasi Persamaan (2.13), kandidat konfigurasi baru akan disampel dari wilayah ruang parameter yang memiliki rasio $\ell(x) / g(x)$ tinggi, yaitu area yang memiliki kemungkinan besar menghasilkan peningkatan akurasi terbaik sekaligus mempertahankan eksplorasi pada wilayah yang belum terpetakan secara seimbang dan efisien.

### 3. Kerangka Kerja Optuna dan Mekanisme MedianPruner

Implementasi algoritma TPE pada studi yang dilakukan dieksekusi melalui kerangka kerja optimasi mutakhir Optuna (Akiba et al., 2019). Optuna dirancang dengan paradigma arsitektur *define-by-run* yang memungkinkan ruang pencarian hyperparameter didefinisikan secara dinamis selama proses eksekusi kode berlangsung. Kerangka kerja ini mengintegrasikan sampler Bayesian terpandu (*TPESampler*) dengan mekanisme pemangkasan dini (*pruning*) otomatis guna meningkatkan efisiensi komputasi eksperimen secara drastis.

Mekanisme pemangkasan yang diterapkan adalah *MedianPruner*, yang bertugas menghentikan uji coba (*trial*) yang terindikasi berkinerja buruk pada tahap awal evaluasi (Akiba et al., 2019; Optuna Development Team, 2024). *MedianPruner* membandingkan nilai evaluasi sementara (*intermediate loss*) dari suatu *trial* pada lipatan validasi berjalan dengan nilai median dari seluruh *trial* sebelumnya pada langkah yang sama. Apabila nilai kerugian sementara *trial* tersebut berada di atas nilai median, proses pelatihan untuk kombinasi parameter tersebut akan dihentikan seketika tanpa perlu menyelesaikan seluruh lipatan validasi. Penghentian dini ini menghemat alokasi waktu dan daya komputasi secara signifikan, sehingga anggaran evaluasi dapat dialihkan sepenuhnya untuk mengeksplorasi kandidat konfigurasi parameter yang lebih potensial.

## F. Evaluasi Peramalan dan Inferensi Statistik

### 1. Validasi Temporal dan Pengendalian Kebocoran Data (Purged Cross-Validation)

Validasi silang konvensional (*k-fold cross-validation*) yang membagi observasi secara acak tidak dapat diterapkan pada data deret waktu finansial karena melanggar urutan kausalitas alami data dan memicu kebocoran informasi masa depan (*look-ahead bias*) ke dalam data pelatihan masa lalu. Guna menjamin integritas evaluasi, penelitian ini mengadopsi prinsip *Purged Cross-Validation* yang diperkenalkan oleh López de Prado (2018). Skema validasi ini menyusun lipatan secara kronologis (*rolling-origin TimeSeriesSplit*) di mana data pelatihan selalu mendahului data validasi, disertai penyisipan jeda pemisah (*purge gap*) di antara kedua subset tersebut. Jeda pemisah ini mengeliminasi sampel observasi yang memiliki irisan jendela fitur historis dengan data validasi, sehingga interaksi informasi antar-partisi dapat dicegah secara total.

Di samping hal tersebut, pengendalian kebocoran data juga diterapkan secara disiplin pada tahapan standardisasi fitur (*StandardScaler*). Parameter penskalaan, yaitu nilai rata-rata ($\mu$) dan simpangan baku ($\sigma$), wajib diestimasi murni hanya dari data pelatihan pada masing-masing lipatan validasi. Parameter penstandar tersebut kemudian diterapkan pada data validasi dan data uji tanpa pernah melibatkan informasi statistik dari subset evaluasi (López de Prado, 2018). Protokol isolasi skala ini menjamin bahwa model peramalan tidak terpapar distribusi data masa depan sebelum evaluasi performa berlangsung.

### 2. Fungsi Kerugian Asimetris Quasi-Likelihood (QLIKE)

Evaluasi akurasi model peramalan volatilitas memerlukan fungsi kerugian yang tepat dan selaras dengan karakteristik proksi varians. Patton (2011) membuktikan secara matematis bahwa metrik kesalahan simetris konvensional seperti *Mean Squared Error* (MSE) menghasilkan perankingan model yang bias dan tidak konsisten ketika dihadapkan pada proksi volatilitas yang mengandung derau (*noisy volatility proxy*). Patton menurunkan kondisi bahwa evaluasi varians memerlukan fungsi kerugian dalam kelas homogenitas derajat nol yang tahan terhadap derau proksi, di mana fungsi kerugian *Quasi-Likelihood* (QLIKE) terbukti menjadi estimator yang paling robust dan konsisten. Formulasi matematis QLIKE dirumuskan sebagai berikut:

$$QLIKE = \frac{1}{T} \sum_{t=1}^T \left[ \frac{RV_t + 10^{-12}}{\widehat{RV}_t} - \ln\left(\frac{RV_t + 10^{-12}}{\widehat{RV}_t}\right) - 1 \right] \tag{2.14}$$

Pada Persamaan (2.14), $RV_t$ menyatakan nilai varians terealisasi aktual dan $\widehat{RV}_t = \exp(\widehat{\log RV}_t)$ adalah nilai proyeksi varians dari model. Dalam skala kesalahan logaritmik $e_t = \log RV_t - \widehat{\log RV}_t$, formulasi QLIKE ekuivalen dengan ekspresi:

$$QLIKE = \frac{1}{T} \sum_{t=1}^T \left[ \exp(e_t) - e_t - 1 \right] \tag{2.15}$$

Fungsi kerugian QLIKE bersifat asimetris: kesalahan peramalan yang meremehkan volatilitas aktual (*under-prediction*, $e_t > 0$) akan dikenai penalti kerugian yang jauh lebih berat secara eksponensial dibandingkan kesalahan yang melebih-lebihkan volatilitas (*over-prediction*, $e_t < 0$). Sifat asimetri ini sangat relevan dalam manajemen risiko finansial, karena kegagalan mengantisipasi lonjakan volatilitas pasar berpotensi menimbulkan kerugian finansial yang fatal.

### 3. Uji Signifikansi Asimtotik Diebold-Mariano (Koreksi HAC Newey-West)

Perbedaan nilai rata-rata metrik evaluasi antar-model peramalan belum cukup membuktikan keunggulan ilmiah suatu algoritma tanpa pengujian signifikansi statistik yang terukur. Guna menguji apakah perbedaan akurasi peramalan antara model usulan dan model baseline berbeda secara signifikan dari nol, diterapkan uji komparasi Diebold dan Mariano (1995). Misalkan $d_t = L(y_t, \hat{y}_{\text{usulan}, t}) - L(y_t, \hat{y}_{\text{baseline}, t})$ menyatakan deret selisih kerugian harian (*loss differential*) antara model LSTM-Optuna dan model baseline berdasarkan fungsi kerugian QLIKE. Statistik uji Diebold-Mariano (DM) dirumuskan sebagai:

$$DM = \frac{\bar{d}}{\sqrt{\widehat{\text{Var}}(\bar{d})}} \tag{2.16}$$

Pada Persamaan (2.16), $\bar{d} = (1/T)\sum_{t=1}^T d_t$ merepresentasikan nilai rata-rata selisih kerugian dan $\widehat{\text{Var}}(\bar{d})$ adalah varians asimtotik dari rata-rata selisih tersebut. Karena deret diferensial kerugian runtun waktu finansial kerap memperlihatkan autokorelasi serial dan heteroskedastisitas, varians $\bar{d}$ diestimasi menggunakan estimator *Heteroskedasticity and Autocorrelation Consistent* (HAC) Newey dan West (1987) dengan panjang kelambatan (*lag truncation*) sebesar 5 hari. Uji statistik dilakukan secara satu sisi dengan hipotesis alternatif $H_1: E[d_t] < 0$ pada ambang signifikansi $\alpha = 0{,}05$. Nilai statistik $DM$ yang bernilai negatif dengan nilai-$p < 0{,}05$ mengindikasikan bahwa model LSTM-Optuna secara signifikan menghasilkan kesalahan peramalan yang lebih rendah dibandingkan model pembanding.

### 4. Estimasi Non-Parametrik Moving-Block Bootstrap

Sebagai penopang uji asimtotik parametrik pada sampel berhingga, diterapkan metode estimasi non-parametrik *Moving-Block Bootstrap* yang dirumuskan oleh Künsch (1989). Uji bootstrap konvensional yang meresampel observasi secara acak individual akan merusak struktur autokorelasi serial pada deret diferensial kerugian. Sebaliknya, metode *Moving-Block Bootstrap* mempertahankan dependensi temporal runtun waktu dengan cara mengambil cuplikan blok-blok data yang berurutan sepanjang $b = 20$ hari secara berulang sebanyak 10.000 repetisi (Künsch, 1989; Patton, 2011).

Dari distribusi empiris rata-rata selisih kerugian ($\Delta QLIKE$) hasil resampel 10.000 kali tersebut, disusun interval kepercayaan persentil 95% secara cermat. Kriteria keunggulan model terpenuhi secara kuat apabila batas atas (*upper bound*) dari interval kepercayaan persentil 95% tersebut berada sepenuhnya di bawah angka nol, yang membuktikan bahwa keunggulan model LSTM-Optuna konsisten dan tidak dipicu oleh fluktuasi acak sampel.

### 5. Pengendalian Variabilitas Multi-Seed

Bouthillier et al. (2021) menunjukkan bahwa inisialisasi bobot acak awal dan urutan pengacakan batch pelatihan menimbulkan variasi performa yang signifikan pada tolok ukur pembelajaran mesin. Mengandalkan hasil evaluasi dari satu kali inisialisasi benih acak (*single seed*) rentan memicu bias keberuntungan (*cherry-picking*). Guna memastikan ketahanan dan reproduksibilitas komputasi, penelitian ini mengadopsi protokol evaluasi *multi-seed* dengan melatih model LSTM secara independen menggunakan lima nilai benih acak yang ditetapkan secara apriori, yaitu *seed* 42, 123, 2024, 7, dan 99. Proyeksi akhir model merupakan rata-rata ansambel (*ensemble average*) dari kelima model tersebut, sehingga kestabilan estimasi dapat dipertanggungjawabkan secara ilmiah.

## G. Penelitian Terdahulu

Kajian kepustakaan terhadap penelitian terdahulu difokuskan pada tiga ranah keilmuan utama: ekonometrika volatilitas klasik, peramalan harga aset kripto berbasis *deep learning*, serta peramalan volatilitas menggunakan *machine learning*. Ringkasan komparatif dari penelitian terdahulu yang relevan disajikan pada Tabel 2.1.

**Tabel 2.1 Ringkasan Sintesis Penelitian Terdahulu**

| No | Peneliti & Tahun | Objek & Target | Metode / Model | Protokol Validasi | Model Baseline | Keterbatasan & Kesenjangan (*Research Gap*) |
|:--:|---|---|---|---|---|---|
| 1 | Katsiampa (2017) | Volatilitas Bitcoin | Ragam Model GARCH (AR-CGARCH) | In-sample estimation | Spesifikasi GARCH | Bersifat in-sample, model linier simetris, tanpa evaluasi *out-of-sample* terstandarisasi. |
| 2 | Ardia et al. (2019) | Volatilitas Bitcoin | Markov-Switching GARCH (MSGARCH) | Rolling estimation | GARCH standar tunggal | Terfokus pada pergeseran rezim linier ekonometrika, tidak mengeksplorasi deep learning. |
| 3 | Conrad et al. (2018) | Volatilitas kripto | GARCH-MIDAS | In-sample & Out-of-sample | GARCH klasik | Memerlukan kovariat makroekonomi eksternal; terbatas pada formulasi ekonometrika parametrik. |
| 4 | Kim & Won (2018) | Volatilitas KOSPI 200 | Hibrida LSTM-GARCH | Train-Test chronological | GARCH-type & LSTM tunggal | Diterapkan pada indeks saham tradisional, tanpa optimasi hyperparameter Bayesian terpadu. |
| 5 | Christensen et al. (2023) | Realized Variance Saham DJIA | Machine Learning (RF, GBDT, DNN) vs HAR | Out-of-sample forecasting | HAR-RV | Objek saham AS reguler; belum menguji dinamika volatilitas ekstrem aset kripto 24/7. |
| 6 | Khumaidi et al. (2024) | Harga Bitcoin | LSTM | Train-Test split konvensional | Tanpa baseline kuat | Menargetkan harga acak (*random walk*); tanpa *Purged CV* dan metrik asimetris risiko. |
| 7 | Kervancı & Akay (2023) | Harga Bitcoin | LSTM & Hparam tuning | K-Fold konvensional | Default LSTM | Menargetkan harga penutupan; rentan kebocoran temporal akibat *K-Fold* acak standar. |
| 8 | Aldo et al. (2026) | Harga TRX-USD | Komparasi HPO LSTM | Train-Validation split | Random Search | Berfokus pada harga altcoin; evaluasi bertumpu pada metrik simetris MSE/MAE standar. |
| 9 | Widad et al. (2026) | Harga Bitcoin | Komparasi LSTM vs GRU teroptimasi | Train-Test chronologic | Model default | Target peramalan nominal harga; tidak memodelkan dependensi volatilitas terealisasi. |
| 10 | Ula et al. (2024) | Harga Bitcoin | LSTM vs Random Forest | Train-Test split | Random Forest | Target harga penutupan; tanpa penalaan hyperparameter Bayesian dan fungsi loss asimetris. |
| 11 | Aswadi & Ependi (2025) | Harga BTC & ETH | Jaringan LSTM | Split 80:20 konvensional | Naive forecast | Target nominal harga aset; normalisasi global rentan memicu *look-ahead bias*. |
| 12 | Fawzi et al. (2025) | Harga Bitcoin | LSTM & Deployment Streamlit | Train-Test 80:20 | Tanpa baseline formal | Terfokus pada antarmuka web; tidak menguji signifikansi statistik inferensial (DM test). |
| 13 | Wahyuddin et al. (2025) | Deret Waktu Finansial | LSTM & Walk-Forward Validation | Walk-Forward rolling | Default LSTM | Mengkaji validasi walk-forward; belum mengintegrasikan loss QLIKE dan bootstrap blok. |

### 1. Sintesis Penelitian dan Posisi Riset

Merujuk pada telaah kritis terhadap 13 penelitian terdahulu pada Tabel 2.1, teridentifikasi sejumlah kesenjangan riset (*research gap*) mendasar:

1. **Kesenjangan Target Pemodelan:** Mayoritas studi *machine learning* nasional berfokus pada peramalan harga nominal penutupan Bitcoin yang memiliki rasio sinyal terhadap derau sangat rendah dan mendekati *random walk*. Penelitian ini mengalihkan target pemodelan menuju *realized variance* (RV) berbasis data intra-day 1 jam yang terbukti memiliki dependensi temporal dan persistensi terstruktur.
2. **Kesenjangan Protokol Validasi:** Sebagian besar penelitian terdahulu menerapkan pembagian data acak atau *K-Fold* standar yang memicu kebocoran data (*data leakage*). Penelitian ini mengimplementasikan skema *Purged Cross-Validation* dengan jeda pemisah (*purge gap*) dan *fold-specific scaler* guna menjamin ketiadaan informasi masa depan yang bocor.
3. **Kesenjangan Efisiensi Optimasi:** Penalaan parameter pada riset terdahulu umumnya bertumpu pada *manual trial* atau *random search* yang tidak efisien. Penelitian ini menerapkan algoritma Bayesian *Tree-structured Parzen Estimator* (TPE) yang dipadukan dengan *MedianPruner* dalam kerangka kerja Optuna untuk penalaan parameter yang efisien dan terarah.
4. **Kesenjangan Evaluasi dan Inferensi:** Evaluasi pada penelitian terdahulu didominasi oleh metrik simetris (MSE/MAE) tanpa pengujian signifikansi statistik inferensial. Penelitian ini mengintegrasikan fungsi kerugian asimetris QLIKE, uji hipotesis Diebold-Mariano dengan koreksi HAC Newey-West, estimasi *Moving-Block Bootstrap*, serta pengujian *multi-seed ensemble* untuk menjamin kesimpulan ilmiah yang kuat dan bebas dari bias seleksi.

## H. Kerangka Pemikiran

Kerangka pemikiran konseptual penelitian ini menguraikan alur logis perancangan pipeline komputasi peramalan *realized volatility* Bitcoin, mulai dari identifikasi masalah dinamika pasar hingga penarikan kesimpulan statistik inferensial yang terstandarisasi. Hubungan antar-komponen metodologi tersebut disajikan secara skematis pada Gambar 2.2.

![Gambar 2.2 Alur Kerangka Pemikiran Konseptual Penelitian](figures/gambar_2_2_kerangka_pemikiran.png)

Alur kerangka pemikiran konseptual tersebut diorganisasikan ke dalam lima tahapan utama:

1. **Tahap Identifikasi Masalah:** Berangkat dari fenomena ekstremnya fluktuasi pasar Bitcoin dan kegagalan prediksi harga acak, penelitian merumuskan urgensi pemodelan *realized volatility* non-linear menggunakan LSTM yang dioptimasi Optuna bebas kebocoran data.
2. **Tahap Akuisisi dan Rekayasa Fitur:** Mengagregasi data kline 1 jam Binance Vision periode 2020–2026 menjadi *realized variance* harian UTC, mengeliminasi sampel cacat berdasarkan Amandemen A1, serta mengekstraksi enam fitur teknikal kausal tanpa *look-ahead bias*.
3. **Tahap Partisi Temporal dan Penalaan Hyperparameter:** Membagi data secara kronologis menjadi Development (2020–2023), Validation (2024–2025), dan Test (2026). Menala hyperparameter LSTM menggunakan Optuna TPE dengan skema 5-fold *Purged Cross-Validation* dan *MedianPruner* pada data pengembangan.
4. **Tahap Pelatihan Final dan Pemodelan Baseline:** Melatih ulang arsitektur LSTM terbaik pada *Train Pool* (2020–2025) menggunakan protokol *multi-seed* (lima nilai benih acak), serta mengimplementasikan empat model baseline pembanding (*Persistence*, HAR-RV, GARCH(1,1), dan LSTM *untuned*).
5. **Tahap Evaluasi dan Inferensi Statistik:** Menguji performa generalisasi seluruh model pada data uji eksternal 2026 menggunakan metrik asimetris QLIKE, uji signifikansi Diebold-Mariano dengan estimasi HAC Newey-West, serta *Moving-Block Bootstrap* untuk pembuktian hipotesis penelitian secara objektif.

## I. Hipotesis Penelitian

Berdasarkan landasan teori, tinjauan penelitian terdahulu, dan kerangka pemikiran konseptual yang telah dipaparkan, dirumuskan tiga hipotesis penelitian yang akan diuji secara empiris selaras dengan rumusan masalah yang ditetapkan:

* **Hipotesis 1 (H1):**
  Integrasi skema 5-fold *Purged Cross-Validation* dengan jeda pemisah (*purge gap*) dan penalaan Bayesian Optuna TPE mampu menghasilkan model *Long Short-Term Memory* (LSTM) yang stabil dan bebas dari degradasi performa yang dipicu oleh kebocoran informasi temporal (*data leakage*).

* **Hipotesis 2 (H2):**
  Model LSTM teroptimasi Optuna menghasilkan nilai fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) yang secara signifikan lebih rendah dibandingkan model *baseline Random Walk Persistence* pada data uji eksternal tahun 2026, yang dibuktikan melalui uji signifikansi Diebold-Mariano satu sisi dengan nilai-$p < 0{,}05$ dan batas atas interval kepercayaan *Moving-Block Bootstrap* 95% berada di bawah nol.

* **Hipotesis 3 (H3):**
  Model LSTM teroptimasi Optuna mampu menghasilkan nilai fungsi kerugian QLIKE yang kompetitif dan menyaingi akurasi model ekonometrika klasik *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) dan GARCH(1,1) dalam memproyeksikan dinamika *realized volatility* Bitcoin pada data uji eksternal tahun 2026.
