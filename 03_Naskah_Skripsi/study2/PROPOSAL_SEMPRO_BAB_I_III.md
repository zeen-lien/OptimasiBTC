# BAB I PENDAHULUAN

## A. Latar Belakang

Pasar aset kripto, khususnya Bitcoin (BTC), merupakan salah satu instrumen keuangan digital dengan tingkat kapitalisasi pasar terbesar di dunia yang mencatatkan derajat fluktuasi harga sangat ekstrem, dinamis, serta beroperasi tanpa henti selama 24 jam sehari tanpa otoritas pengatur terpusat (Lim & Zohren, 2021). Dalam disiplin ilmu Teknik Informatika, rekaman riwayat transaksi perdagangan Bitcoin terekam secara kronologis sebagai data deret waktu (*time series*) masif yang menarik perhatian banyak peneliti untuk merancang model komputasi cerdas, seperti studi yang dilakukan oleh Khumaidi et al. (2024), Aswadi dan Ependi (2025), serta Fawzi et al. (2025). Akan tetapi, mayoritas penelitian komputasi tersebut secara keliru menargetkan harga penutupan nominal (*closing price*). Memprediksi tingkat harga nominal terbukti memiliki rasio sinyal terhadap derau (*signal-to-noise ratio*) yang sangat rendah karena deret harga di pasar yang efisien bergerak mendekati lintasan acak (*random walk*), sehingga hampir mustahil diproyeksikan secara konsisten dan rentan gagal mengungguli model naif sederhana (Ula et al., 2024). Sebaliknya, besaran fluktuasi pasar atau volatilitas justru memperlihatkan keteraturan statistik berupa pengelompokan volatilitas (*volatility clustering*), di mana fase varians tinggi cenderung saling berkelompok secara terstruktur (Andersen & Bollerslev, 1998; Bollerslev, 1986). Kesenjangan mendasar antara ketidakpastian harga acak dan keteraturan pola volatilitas inilah yang mendasari perlunya pergeseran paradigma riset komputasi finansial: bukan lagi berspekulasi menebak arah harga nominal, melainkan memodelkan besaran volatilitas sebagai proksi risiko objektif yang sangat krusial bagi manajemen risiko pasar, penetapan batas toleransi *Value-at-Risk*, dan alokasi lindung nilai aset digital (Kim & Won, 2018).

Meskipun memiliki persistensi temporal yang kuat, volatilitas pasar secara teoretis merupakan variabel laten (*unobservable variable*) yang tidak dapat diamati secara langsung pada data harian biasa, sehingga menuntut proksi kalkulasi kuantitatif yang akurat (Katsiampa, 2017). Perkembangan ekonometrika modern membuktikan bahwa estimasi volatilitas paling presisi diperoleh melalui *realized variance* (RV), yakni penjumlahan kuadrat imbal hasil logaritmik intra-hari berfrekuensi tinggi dalam satu siklus perdagangan harian (Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002). Secara tradisional, pemodelan volatilitas dan *realized variance* mengandalkan formulasi ekonometrika runtun waktu linier seperti *Generalized Autoregressive Conditional Heteroskedasticity* GARCH(1,1) oleh Bollerslev (1986) dan *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) oleh Corsi (2009) yang mengurai dinamika volatilitas ke dalam tiga horizon waktu (harian, mingguan, dan bulanan). Kendati memiliki landasan matematis yang transparan, model GARCH dan HAR-RV memiliki kelemahan fundamental berupa asumsi stasioneritas dan hubungan linier kaku antar-variabel masukan. Pada kenyataannya, pasar aset kripto kerap mengalami lonjakan ekstrem mendadak (*volatility jumps*), asimetri informasi, dan pergeseran rezim struktural (*regime shifts*) yang bersifat non-linear dinamis, sehingga tidak mampu diakomodasi secara memadai oleh formulasi linier klasik tersebut (Ardia et al., 2019; Conrad et al., 2018).

Keterbatasan model ekonometrika linier tersebut membuka peluang ilmiah bagi penerapan algoritma pembelajaran mendalam (*deep learning*), khususnya arsitektur jaringan saraf tiruan berulang *Long Short-Term Memory* (LSTM) yang dirancang oleh Hochreiter dan Schmidhuber (1997) untuk memodelkan dependensi non-linear sekuensial jangka panjang. Melalui mekanisme internal gerbang logika komputasi—meliputi gerbang masuk (*input gate*), gerbang lupa (*forget gate*), dan gerbang keluar (*output gate*)—LSTM secara adaptif mampu mempertahankan memori temporal relevan sekaligus mengeliminasi masalah hilangnya gradien (*vanishing gradient*) pada deret panjang (Christensen et al., 2023). Namun demikian, performa peramalan LSTM sangat sensitif terhadap kombinasi *hyperparameter* eksternal arsitektur, meliputi panjang jendela historis (*lookback*), jumlah unit neuron (*units*), tingkat regulasi *dropout*, laju pembelajaran (*learning rate*), dan ukuran *batch*. Studi empiris pada data kripto oleh Aldo et al. (2026), Kervancı dan Akay (2023), serta Widad et al. (2026) mengungkapkan bahwa pemilihan kombinasi parameter tersebut umumnya masih dilakukan melalui *trial-and-error* manual atau pencarian acak (*random search*). Pendekatan heuristik semacam ini tidak hanya sangat memboroskan sumber daya komputasi (*computationally expensive*), melainkan juga rentan terjebak pada konfigurasi suboptimal karena menjelajahi ruang pencarian berdimensi tinggi secara acak tanpa panduan probabilitas.

Guna mengatasi inefisiensi eksplorasi parameter tersebut, algoritma *Tree-structured Parzen Estimator* (TPE) yang diintegrasikan dalam kerangka kerja Optuna (Akiba et al., 2019; Bergstra et al., 2011) menawarkan paradigma optimasi berbasis Bayesian yang secara terarah memodelkan probabilitas konfigurasi masa lalu untuk memandu pencarian berikutnya, dipadukan dengan mekanisme *MedianPruner* untuk memangkas evaluasi berkinerja buruk secara dini (*early stopping*). Kendati demikian, penalaan arsitektur *deep learning* yang canggih sekalipun akan kehilangan validitas ilmiahnya apabila tidak disertai protokol pencegahan kebocoran data (*data leakage*) yang ketat. Banyak penelitian komputasi sebelumnya secara keliru membagi data secara acak atau menerapkan penskalaan fitur global (*global scaling*), yang secara tidak disadari menyusupkan informasi masa depan ke data masa lalu dan menghasilkan akurasi semu yang bias (López de Prado, 2018). Oleh karena itu, validasi finansial yang sahih wajib mempertahankan integritas kronologis melalui skema *Purged Cross-Validation* dengan jeda pemisah (*purge gap*) dan standarisasi fitur spesifik per *fold*. Di samping itu, evaluasi akurasi volatilitas tidak tepat jika hanya mengandalkan metrik kesalahan simetris seperti *Mean Squared Error* (MSE) yang rentan terdistorsi derau proksi, melainkan memerlukan fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) yang secara matematis terbukti *robust* terhadap derau proksi *realized variance* (Patton, 2011), serta diperkuat dengan uji signifikansi asimtotik Diebold-Mariano berkoreksi kovarians HAC Newey dan West (1987) dan interval kepercayaan empiris *Moving-Block Bootstrap* multi-seed (Bouthillier et al., 2021; Diebold & Mariano, 1995; Künsch, 1989).

Bertolak dari rangkaian kesenjangan penelitian (*research gaps*) teoretis, komputasional, dan metodologis tersebut, penelitian ini berfokus merancang, membangun, dan menguji *pipeline* komputasi peramalan *realized volatility* harian Bitcoin yang terintegrasi secara utuh, terstandarisasi, dan bebas kebocoran data. Penelitian ini memanfaatkan data historis kline 1 jam Binance Vision rentang 2020 hingga 2026 (total 2.464 hari observasi terverifikasi) yang diagregasi menjadi target *log realized variance* harian UTC dengan enam fitur masukan teknikal kausal. Arsitektur model LSTM ditala secara optimal menggunakan algoritma Optuna-TPE sebanyak 50 *trials* di bawah skema 5-fold *Purged Cross-Validation* pada data pengembangan 2020–2023, divalidasi pada periode 2024–2025, dan diuji secara ketat pada data uji eksternal *out-of-sample* tahun 2026. Kinerja model dievaluasi secara komprehensif menggunakan fungsi kerugian asimetris QLIKE serta diuji signifikansinya terhadap tiga model *baseline* pembanding (*persistence*, HAR-RV, dan GARCH(1,1)) melalui uji statistik Diebold-Mariano berkoreksi HAC dan bootstrap multi-seed lima nilai acak apriori. Melalui perancangan yang mengerucut dan terarah ini, penelitian diharapkan memberikan kontribusi nyata dalam penerapan *machine learning* sekuensial yang bebas dari bias kebocoran data pada ranah volatilitas aset digital.


## B. Rumusan Masalah

Merujuk pada penjelasan sebelumnya mengenai latar belakang permasalahan yang telah diuraikan, rumusan masalah pada studi yang dilakukan dirumuskan sebagai berikut:

1. **Bagaimana** merancang arsitektur model *Long Short-Term Memory* (LSTM) teroptimasi Optuna dengan skema *Purged Cross-Validation* untuk mencegah kebocoran data (*data leakage*) pada peramalan *realized volatility* Bitcoin?
2. **Sejauh mana** peningkatan akurasi peramalan yang dihasilkan oleh model LSTM teroptimasi Optuna dibandingkan dengan *baseline persistence* berdasarkan fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) pada data uji eksternal 2026?
3. **Apakah** model LSTM teroptimasi Optuna mampu menyaingi performa model ekonometrika klasik *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) dan GARCH(1,1) dalam memproyeksikan volatilitas pasar kripto?


## C. Batasan Masalah

Guna menjaga fokus penelitian agar tetap terarah, terukur, dan mendalam, ditetapkan batasan-batasan masalah sebagai berikut:

1. Data yang digunakan merupakan data historis kline 1 jam pasangan perdagangan Bitcoin terhadap Tether (BTC/USDT) dari arsip publik Binance Vision untuk rentang waktu 1 Januari 2020 hingga 30 September 2026. Rentang data ini mencakup berbagai kondisi pasar yang beragam, mulai dari periode bull market, bear market, hingga fase konsolidasi pasar kripto global.
2. Target peramalan dibatasi pada nilai *log realized variance* satu langkah ke depan ($\log RV_{t+1}$), dengan RV harian dihitung dari kuadrat return logaritmik *open-to-close* bar kline 1 jam yang tersedia pada hari UTC. Hari lengkap memiliki 24 bar; hari dengan 20–23 bar tetap dipertahankan untuk menjaga kelengkapan deret waktu, sedangkan hari dengan kurang dari 20 bar akan dieliminasi dari dataset.
3. Fitur masukan model dibatasi pada enam variabel teknikal terukur yang diturunkan dari informasi historis, meliputi $\log RV_t$, $\log range_t$, $\log volume_t$, $\log absret_t$, rata-rata bergerak 5 hari ($rv\_mean\_5_t$), dan rata-rata bergerak 22 hari ($rv\_mean\_22_t$). Seluruh fitur dikonstruksi secara kausal dari informasi yang tersedia hingga hari $t$ tanpa menggunakan informasi masa depan.
4. Model utama dibatasi pada LSTM multivariat-sekuensial dengan enam fitur, yang akan ditala melalui algoritma Optuna menggunakan TPE Sampler sebanyak 50 trial dengan MedianPruner untuk efisiensi komputasi. Ruang pencarian meliputi *lookback* 10–30 hari, 16–128 unit neuron, 1–2 lapisan, *dropout* 0,05–0,40, *learning rate* $3\times10^{-4}$–$2\times10^{-3}$, dan *batch size* 16, 32, atau 64.
5. Pembagian data temporal diatur secara kronologis menjadi tiga jendela yang terpisah: data pengembangan 2020–2023 (1.460 hari kalender) untuk pelatihan fold dan penalaan CV, data validasi 2024–2025 (731 hari kalender) untuk pemeriksaan pipeline dan baseline tanpa pemilihan hyperparameter, serta data uji eksternal 1 Januari–30 September 2026 (273 hari kalender) yang tidak akan digunakan dalam proses pelatihan maupun optimasi sama sekali.
6. Evaluasi akan menggunakan QLIKE sebagai metrik primer serta MAE dan RMSE sebagai metrik sekunder pada skala log-RV. Inferensi statistik dilakukan untuk dua perbandingan primer: LSTM-Optuna terhadap *persistence* dan LSTM-Optuna terhadap HAR-RV, menggunakan uji Diebold–Mariano satu sisi dengan koreksi HAC Newey–West pada tingkat signifikansi $\alpha = 0{,}05$ dan *moving-block bootstrap* 10.000 repetisi. GARCH(1,1) dan LSTM *untuned* akan dilaporkan sebagai pembanding sekunder.
7. Penelitian ini murni berfokus pada akurasi peramalan statistik komputasional deret waktu dan tidak mencakup simulasi eksekusi strategi perdagangan (*trading system*), analisis biaya transaksi (*slippage* dan komisi bursa), pembentukan portofolio multi-aset, maupun analisis sentimen media sosial dan faktor makroekonomi eksternal.


## D. Tujuan Penelitian

Sesuai dengan rumusan masalah yang ditetapkan, tujuan yang hendak dicapai pada studi yang dilakukan adalah sebagai berikut:

1. Merancang dan mengimplementasikan arsitektur model *Long Short-Term Memory* (LSTM) yang terintegrasi dengan algoritma penalaan Optuna (TPE) serta skema 5-fold *Purged Cross-Validation* guna menjamin proses peramalan bebas dari kebocoran data temporal pada peramalan *realized volatility* Bitcoin.
2. Mengukur dan menganalisis efektivitas peningkatan akurasi model LSTM teroptimasi Optuna terhadap *baseline persistence* menggunakan metrik asimetris QLIKE dan uji signifikansi Diebold-Mariano pada data uji eksternal tahun 2026.
3. Menilai dan membuktikan daya saing komparatif model LSTM teroptimasi Optuna terhadap model ekonometrika klasik HAR-RV dan GARCH(1,1) dalam memodelkan dinamika *realized volatility* Bitcoin.


## E. Manfaat Penelitian

Penelitian ini diharapkan mampu memberikan kontribusi nyata yang terbagi ke dalam tiga aspek manfaat utama:

### 1. Manfaat Teoretis

Penelitian ini memperkaya khazanah keilmuan Teknik Informatika dan sains data komputasional, khususnya dalam penerapan *deep learning* sekuensial pada data deret waktu berfluktuasi tinggi. Penelitian ini akan membuktikan secara empiris dinamika penerapan algoritma LSTM dan optimasi Bayesian TPE pada target *realized volatility*, sekaligus mengalihkan fokus riset kripto dari prediksi harga yang rentan kegagalan menuju pemodelan risiko yang memiliki dependensi temporal terstruktur (Christensen et al., 2023). Di samping hal tersebut, integrasi antara skema *Purged Cross-Validation* dan fungsi kerugian asimetris QLIKE dalam satu pipeline yang utuh diharapkan menjadi referensi metodologis bagi penelitian *deep learning* finansial berikutnya. Temuan studi memperlihatkan peluang pengembangan lebih lanjut untuk membangun model peramalan volatilitas yang lebih akurat dan dapat diandalkan secara ilmiah.

### 2. Manfaat Praktis

Bagi praktisi teknologi finansial, analis kuantitatif, dan pengelola risiko aset digital, *pipeline* komputasi yang akan dihasilkan pada studi yang dilakukan dapat dimanfaatkan sebagai modul inti sistem peringatan dini (*early warning system*) terhadap lonjakan risiko pasar. Proyeksi volatilitas yang akurat membantu pelaku industri dalam menentukan batas toleransi risiko (*Value-at-Risk*), alokasi lindung nilai (*hedging*), serta penetapan ukuran posisi perdagangan yang lebih terukur (Kim & Won, 2018). Tahap berikutnya, dokumentasi metodologi yang rinci dan terstandarisasi juga akan memudahkan praktisi untuk mengadaptasi pipeline ini ke berbagai kelas aset atau bursa digital lainnya yang memiliki karakteristik volatilitas serupa. Transparansi kode dan data yang terdokumentasi lengkap mendukung proses audit independen serta validasi ulang oleh pihak eksternal.

### 3. Manfaat Metodologis

Penelitian ini menyajikan standar protokol eksperimen komputasi finansial yang ketat, transparan, dan dapat direproduksi secara utuh (*fully reproducible*). Integrasi antara *Purged Cross-Validation* untuk mencegah kebocoran data, fungsi kerugian asimetris QLIKE yang *robust* terhadap derau proksi, pengujian multi-seed, serta inferensi statistik Diebold-Mariano dan *Moving-Block Bootstrap* akan menjadi rujukan baku bagi penelitian sejenis (Bouthillier et al., 2021). Maka dari itu, standar protokol ini diharapkan dapat mengurangi prevalensi bias optimisme semu (*publication bias*) yang kerap muncul akibat pelaporan selektif hasil terbaik tanpa mempertimbangkan variasi eksperimental yang sesungguhnya. Kontribusi metodologis ini memegang peranan penting dalam mendorong budaya riset komputasi yang bertanggung jawab, jujur, dan berorientasi pada reproduksibilitas ilmiah jangka panjang (López de Prado, 2018).


## F. Sistematika Penulisan

Penyusunan naskah skripsi ini diorganisasikan ke dalam lima bab utama dengan sistematika pembahasan sebagai berikut:

* **BAB I PENDAHULUAN**
  Menguraikan konteks latar belakang permasalahan dinamika pasar Bitcoin, transformasi orientasi riset dari prediksi harga ke *realized volatility*, urgensi optimasi *hyperparameter* LSTM bebas kebocoran, perumusan masalah, tujuan penelitian, manfaat teoretis dan praktis, batasan masalah, serta sistematika penulisan naskah.

* **BAB II LANDASAN TEORI**
  Membahas kajian teoretis dan matematis mengenai konsep volatilitas dan *realized variance*, model ekonometrika runtun waktu klasik GARCH(1,1) dan HAR-RV, arsitektur jaringan saraf tiruan LSTM, algoritma penalaan Bayesian Optuna-TPE, fungsi kerugian asimetris QLIKE, protokol *Purged Cross-Validation*, uji statistik Diebold-Mariano dan bootstrap, tinjauan komprehensif penelitian terdahulu berskala nasional dan internasional, kerangka pemikiran konseptual, serta perumusan hipotesis penelitian.

* **BAB III METODE PENELITIAN**
  Memaparkan rancangan dan metodologi komputasional secara rinci: sumber dan spesifikasi data Binance Vision, prosedur audit kualitas data, pembentukan fitur dan target peramalan, partisi data temporal kronologis, skema 5-fold *Purged Cross-Validation*, konfigurasi dan optimasi LSTM berbasis Optuna TPE, protokol pelatihan multi-seed, implementasi empat model baseline pembanding, serta metrik evaluasi dan prosedur inferensi statistik yang akan diterapkan.

* **BAB IV HASIL DAN PEMBAHASAN**
  Menyajikan temuan empiris hasil pengujian, mencakup statistik deskriptif karakteristik data, hasil penalaan hyperparameter terbaik Optuna, evaluasi kinerja peramalan pada data uji eksternal 2026, analisis komparatif performa terhadap model *baseline*, pengujian hipotesis statistik, visualisasi grafik sekuens prediksi dan galat, serta pembahasan mendalam (*discussion*) mengenai implikasi temuan ilmiah.

* **BAB V PENUTUP**
  Memuat kesimpulan menyeluruh yang menjawab seluruh rumusan masalah penelitian, penjabaran kontribusi ilmiah yang berhasil dicapai, identifikasi keterbatasan penelitian, serta rekomendasi saran strategis untuk pengembangan penelitian lanjutan di masa mendatang.


---

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


---

# BAB III METODE PENELITIAN

## A. Jenis dan Desain Penelitian

### 1. Pendekatan dan Desain Eksperimental Komputasional

Penelitian ini dirancang menggunakan pendekatan kuantitatif dengan desain eksperimental komputasional yang berfokus pada pemodelan runtun waktu finansial secara objektif dan sistematis. Pendekatan kuantitatif dipilih karena fenomena dinamika volatilitas pasar aset digital direpresentasikan melalui metrik numerik terukur yang memerlukan pembuktian empiris berbasis data historis transaksi (Lim & Zohren, 2021). Desain eksperimental komputasional memanfaatkan perangkat lunak untuk menjalankan seluruh tahapan penelitian, meliputi pra-pemrosesan data, rekayasa fitur kausal, pencarian ruang hyperparameter, pelatihan model multi-seed, hingga inferensi statistik komparatif menurut prosedur yang terdokumentasi secara transparan. Otomasi alur kerja ini mendukung konsistensi dan integritas eksperimen, sehingga proses peramalan dapat dievaluasi secara adil pada periode evaluasi yang sama untuk seluruh model pembanding yang diuji.

Guna menjamin integritas ilmiah dan mencegah terjadinya bias seleksi data (*data snooping*) maupun manipulasi hasil (*p-hacking*), seluruh protokol komputasional dirancang dan dikunci secara ketat sebelum proses pelatihan model dieksekusi (Bouthillier et al., 2021). Protokol ini menetapkan batasan ruang pencarian hyperparameter, skema validasi temporal bebas bocor, fungsi kerugian asimetris, dan kriteria inferensi statistik secara apriori. Pendekatan pra-penguncian protokol ini memastikan bahwa seluruh keputusan metodologis diambil secara independen dan tidak dipengaruhi oleh hasil evaluasi akhir. Tahap berikutnya, seluruh eksekusi eksperimen akan dicatat secara terprogram melalui manifes komputasi dan verifikasi kode hash kriptografis guna menjamin keterlacakan (*traceability*) dan keterulangan (*reproducibility*) hasil penelitian secara menyeluruh.

### 2. Objek Penelitian dan Ruang Lingkup

Objek yang diteliti pada studi yang dilakukan adalah *realized volatility* harian dari pasangan perdagangan Bitcoin terhadap Tether (BTC/USDT) pada bursa aset digital global. Bitcoin dipilih sebagai objek penelitian karena memegang peranan sebagai aset kripto dengan tingkat likuiditas dan kapitalisasi pasar terbesar di dunia, serta memiliki struktur volatilitas yang sangat dinamis dan menjadi barometer pergerakan pasar aset digital secara keseluruhan (Katsiampa, 2017). Pengukuran volatilitas berbasis data intra-day berfrekuensi tinggi menyediakan resolusi informasi yang jauh lebih kaya mengenai variasi dispersi harga dalam satu hari perdagangan dibandingkan hanya mengandalkan satu kuadrat imbal hasil harian konvensional (Andersen et al., 2003; Barndorff-Nielsen & Shephard, 2002). Dengan demikian, target yang diramalkan mampu merepresentasikan intensitas fluktuasi pasar secara autentik dan terbebas dari derau mikrostruktur sesaat.

Ruang lingkup penelitian ini dibatasi secara tegas pada peramalan nilai *log realized variance* satu langkah ke depan ($t+1$) pada skala temporal harian. Horizon satu hari dipilih sebagai fokus pemodelan karena relevan bagi kebutuhan manajemen risiko harian, alokasi posisi perdagangan, dan penetapan batas toleransi *Value-at-Risk* (VaR). Evaluasi model diarahkan murni pada akurasi statistik komputasional menggunakan metrik asimetris *Quasi-Likelihood* (QLIKE) dan inferensi statistik formal, serta tidak mencakup simulasi eksekusi sistem perdagangan otomatis (*trading strategy*), perhitungan biaya komisi bursa, pembentukan portofolio multi-aset, maupun analisis sentimen eksternal.

## B. Data Penelitian dan Pra-Pemrosesan

### 1. Sumber dan Pengumpulan Data

Data mentah yang digunakan pada studi yang dilakukan bersumber dari arsip repositori publik resmi Binance Vision (Binance, 2024). Data yang diunduh mencakup data pasar spot historis untuk pasangan perdagangan BTC/USDT pada resolusi bar kline 1 jam (*1-hour interval*) yang terbentang sepanjang periode 1 Januari 2020 hingga 30 September 2026. Pemilihan rentang waktu observasi selama lebih dari enam tahun ini dirancang untuk mencakup beragam rezim pasar yang heterogen, meliputi fase kenaikan ekstrem (*bull market*), penurunan tajam (*bear market*), hingga periode konsolidasi mendatar (*sideways*), sehingga model komputasi yang dibangun dapat diuji ketahanannya pada berbagai dinamika pasar yang berbeda.

Pengumpulan data dilakukan secara otomatis melalui skrip terprogram yang mengunduh 81 berkas arsip bulanan bursa Binance Vision. Setiap berkas arsip yang diunduh langsung dicatat integritasnya menggunakan algoritma *hash* kriptografis SHA-256 guna memastikan keaslian data mentah dan mencegah adanya kerusakan berkas selama proses transfer data berlangsung. Data mentah kline 1 jam tersebut memuat atribut lengkap, meliputi stempel waktu pembukaan (*open time*), harga pembukaan (*open*), harga tertinggi (*high*), harga terendah (*low*), harga penutupan (*close*), dan volume transaksi (*volume*) yang menjadi masukan fundamental bagi tahap pra-pemrosesan data berikutnya.

### 2. Audit Kualitas dan Integritas Data

Tahap awal pra-pemrosesan data difokuskan pada pelaksanaan audit kualitas dan verifikasi integritas struktur bar harga intra-hari secara menyeluruh pada seluruh runtun waktu observasi. Karena pasar aset digital beroperasi tanpa henti selama 24 jam sehari dan tujuh hari seminggu, maka setiap unit hari kalender secara ideal wajib memiliki tepat 24 bar kline berdurasi 1 jam (Binance, 2024). Keberadaan bar harga yang hilang atau terdistorsi akibat kendala teknis jaringan bursa berpotensi memicu bias kalkulasi pada nilai *realized variance* harian, sehingga verifikasi struktur kalender menjadi prasyarat mutlak sebelum fitur dan target peramalan dihitung.

Berdasarkan pemeriksaan struktur data historis, teridentifikasi 15 hari kalender pada rentang awal observasi yang memiliki jumlah bar tidak lengkap, yaitu antara 19 hingga 23 bar. Guna menangani anomali tersebut tanpa merusak kontinuitas deret waktu secara berlebihan, ditetapkan aturan Amandemen Data A1 secara apriori. Aturan ini menetapkan bahwa hari kalender dengan jumlah bar kurang dari 20 bar akan dieliminasi dari dataset penelitian, sedangkan hari dengan ketersediaan 20 hingga 23 bar tetap dipertahankan dengan menghitung *realized variance* dari bar yang tersedia serta menyematkan label penanda integritas data. Berdasarkan kriteria operasional tersebut, hanya satu hari kalender yang dieliminasi, yaitu tanggal 19 Februari 2020 yang hanya memuat 19 bar. Eliminasi satu hari ini menghasilkan total 2.464 observasi harian valid dari keseluruhan 2.465 hari kalender yang diteliti.

### 3. Normalisasi Timestamp dan Agregasi Bar Harian UTC

Stempel waktu transaksi pada berkas historis bursa Binance memiliki variasi format penomoran, mulai dari presisi milidetik hingga mikrodetik yang mengikuti perkembangan pembaruan infrastruktur mesin pencocokan transaksi bursa (Binance, 2024). Seluruh stempel waktu pembukaan bar dinormalisasi ke format waktu universal UTC (*Coordinated Universal Time*). Penetapan zona waktu UTC secara ketat menjamin konsistensi batas pergantian hari kalender yang dimulai tepat pada pukul 00:00:00 UTC hingga berakhir pada pukul 23:59:59 UTC pada setiap tanggal transaksi.

Setelah normalisasi stempel waktu selesai, bar kline 1 jam diagregasikan menurut tanggal UTC menjadi ringkasan harian yang memuat harga pembukaan harian, harga tertinggi intra-hari ($H_t$), harga terendah intra-hari ($L_t$), harga penutupan harian ($C_t$), total volume perdagangan harian ($V_t$), serta nilai *realized variance* ($RV_t$). Seluruh sampel sekuensial yang melintasi jeda kalender tanggal 19 Februari 2020 ditandai dan dikeluarkan dari pembentukan jendela sekuens guna mencegah distorsi imbal hasil yang melintasi celah waktu yang tidak berkesinambungan.

## C. Pengembangan Fitur dan Target Peramalan

### 1. Kalkulasi Realized Variance dan Transformasi Logaritmik

Variabel target yang diramalkan pada studi yang dilakukan dirumuskan melalui perhitungan *realized variance* harian yang mengagregasikan kuadrat imbal hasil logaritmik intra-hari berfrekuensi tinggi (Andersen & Bollerslev, 1998; Barndorff-Nielsen & Shephard, 2002). Untuk setiap hari kalender UTC $t$, nilai *realized variance* harian ($RV_t$) dihitung sebagai jumlahan kuadrat return logaritmik *open-to-close* dari setiap bar 1 jam yang tersedia pada hari tersebut, sebagaimana diformulasikan pada Persamaan (3.1):

$$RV_t = \sum_{h \in \mathcal{H}_t} \left[ \ln\left( \frac{C_{t,h}}{O_{t,h}} \right) \right]^2 \tag{3.1}$$

Pada Persamaan (3.1), $C_{t,h}$ dan $O_{t,h}$ merepresentasikan harga penutupan dan harga pembukaan pada jam perdagangan ke-$h$ dalam hari kalender $t$, sementara $\mathcal{H}_t$ adalah himpunan indeks bar yang tersedia pada hari tersebut. Formulasi *open-to-close* intra-bar ini secara efektif menangkap lintasan dispersi harga yang terjadi di dalam setiap jam perdagangan tanpa terdistorsi oleh lonjakan diskontinuitas antar-bar.

Distribusi empiris dari nilai $RV_t$ pada data keuangan memiliki derajat kemencengan yang tinggi. Guna memfasilitasi kestabilan konvergensi gradien matematika pada jaringan saraf tiruan, nilai $RV_t$ ditransformasikan ke dalam skala logaritma natural ($\log RV_t$) dengan penambahan konstanta regularisasi numerik $10^{-12}$, sebagaimana dinyatakan pada Persamaan (3.2):

$$\log RV_t = \ln\left( RV_t + 10^{-12} \right) \tag{3.2}$$

Target yang akan diprediksi oleh seluruh model komputasi adalah nilai log *realized variance* satu hari ke depan, yaitu $\log RV_{t+1}$. Prediksi ini kemudian dikembalikan ke skala varians positif melalui transformasi eksponensial $\widehat{RV}_{t+1} = \exp(\widehat{\log RV}_{t+1})$ sebelum dievaluasi menggunakan metrik fungsi kerugian asimetris.

### 2. Pembentukan Enam Fitur Masukan Teknikal Kausal

Model komputasi yang dirancang memanfaatkan enam fitur masukan teknikal yang dikonstruksi secara kausal dari informasi yang telah terbentuk sempurna hingga hari ke-$t$ tanpa melibatkan informasi masa depan sama sekali (Aalborg et al., 2019; Christensen et al., 2023). Fitur pertama adalah log realized variance hari ini ($\log RV_t$) yang berfungsi menangkap derajat persistensi volatilitas terkini. Fitur kedua adalah log rentang harga intra-hari ($\log range_t$) yang mengukur selisih logaritmik antara harga tertinggi dan terendah intra-hari sebagaimana diformulasikan pada Persamaan (3.3):

$$\log range_t = \ln\left( \frac{H_t}{L_t} \right) = \ln\left( \frac{\max_{h} H_{t,h}}{\min_{h} L_{t,h}} \right) \tag{3.3}$$

Fitur ketiga merepresentasikan volume perdagangan logaritmik kumulatif harian, yang dirumuskan sebagai $\log volume_t = \ln(\sum_{h \in \mathcal{H}_t} V_{t,h} + 10^{-12})$. Fitur keempat adalah logaritmik imbal hasil absolut penutupan harian ($\log absret_t$) pada Persamaan (3.4), yang menangkap magnitudo guncangan pergerakan harga tanpa memperhitungkan arah kenaikan atau penurunan:

$$\log absret_t = \ln\left( \lvert \ln(C_t / C_{t-1}) \rvert + 10^{-12} \right) \tag{3.4}$$

Fitur kelima dan keenam dirumuskan sebagai rata-rata bergerak log *realized variance* untuk horizon jangka menengah (5 hari) dan jangka panjang (22 hari), sebagaimana disajikan pada Persamaan (3.5) dan Persamaan (3.6):

$$rv\_mean\_5_t = \frac{1}{5} \sum_{i=0}^{4} \log RV_{t-i} \tag{3.5}$$

$$rv\_mean\_22_t = \frac{1}{22} \sum_{i=0}^{21} \log RV_{t-i} \tag{3.6}$$

Pada Persamaan (3.3) hingga (3.6), $H_{t,h}$ dan $L_{t,h}$ menyatakan harga tertinggi dan terendah pada bar jam ke-$h$, $V_{t,h}$ adalah volume perdagangan per jam, $C_t$ dan $C_{t-1}$ merepresentasikan harga penutupan harian pada hari $t$ dan $t-1$, serta indeks $i$ menyatakan kelambatan (*lag*) hari ke belakang. Ringkasan formulasi matematis, tipe variabel, dan peran teoretis dari keenam fitur masukan disajikan secara komprehensif pada Tabel 3.1.

**Tabel 3.1 Definisi Fitur Masukan Teknikal Kausal**

| No | Nama Fitur | Formulasi Matematis | Peran dan Justifikasi Teoretis |
|:--:|---|---|---|
| 1 | $\log RV_t$ | $\ln(RV_t + 10^{-12})$ | Menangkap persistensi autoregresif volatilitas harian terkini |
| 2 | $\log range_t$ | $\ln(\max_h H_{t,h} / \min_h L_{t,h})$ | Mengukur rentang dispersi harga ekstrem intra-hari |
| 3 | $\log volume_t$ | $\ln(\sum_{h \in \mathcal{H}_t} V_{t,h} + 10^{-12})$ | Mengukur intensitas likuiditas dan aktivitas transaksi pasar |
| 4 | $\log absret_t$ | $\ln(\lvert \ln(C_t / C_{t-1}) \rvert + 10^{-12})$ | Menangkap besaran guncangan imbal hasil absolut harian |
| 5 | $rv\_mean\_5_t$ | $(1/5)\sum_{i=0}^{4} \log RV_{t-i}$ | Merepresentasikan komponen volatilitas mingguan (5 hari kerja) |
| 6 | $rv\_mean\_22_t$ | $(1/22)\sum_{i=0}^{21} \log RV_{t-i}$ | Merepresentasikan komponen volatilitas bulanan (22 hari kerja) |

### 3. Skalasi Fitur Tanpa Kebocoran (StandardScaler Fold-Specific)

Pelatihan jaringan saraf tiruan berbasis perambatan mundur (*backpropagation*) sangat sensitif terhadap disparitas rentang nilai antar-variabel masukan (Hochreiter & Schmidhuber, 1997; Kingma & Ba, 2014). Apabila variabel dengan magnitudo besar—seperti volume perdagangan yang bernilai jutaan—dicampurkan dengan variabel berangka desimal kecil tanpa standarisasi, pembaruan bobot model akan didominasi secara keliru oleh gradien fitur bervolume besar. Atas dasar tersebut, seluruh fitur masukan dan target ditransformasikan menggunakan algoritma *StandardScaler* guna menyelaraskan rata-rata menjadi nol dan varians menjadi satu demi kestabilan perambatan gradien matematika.

Guna mencegah kebocoran informasi masa depan (*information leakage*) secara mutlak, parameter penstandar—yaitu nilai rata-rata ($\mu$) dan simpangan baku ($\sigma$)—hanya diestimasi (*fit*) dari subset data pelatihan pada masing-masing lipatan validasi silang (López de Prado, 2018). Statistik penskalaan yang diperoleh dari data latih kemudian diaplikasikan (*transform*) ke subset validasi dan data uji tanpa pembaruan ulang parameter. Penskalaan terpisah juga diterapkan pada variabel target. Sebelum metrik evaluasi dihitung, hasil prediksi model dikembalikan ke skala logaritmik aslinya melalui operasi transformasi balik (*inverse transform*) guna menjamin objektivitas evaluasi galat.

## D. Pembagian Data Temporal Kronologis (Temporal Window)

### 1. Pembagian Dataset: Pengembangan, Validasi, dan Uji Eksternal

Penelitian runtun waktu finansial melarang keras penerapan pembagian data secara acak (*random split*) atau pengacakan silang (*shuffling*), karena data keuangan memuat korelasi serial dan kausalitas waktu yang kuat (López de Prado, 2018). Pengacakan data akan menempatkan informasi masa depan ke dalam subset pelatihan masa lalu, sehingga menciptakan ilusi akurasi optimis yang semu (*look-ahead bias*). Oleh karena itu, penelitian ini mengimplementasikan partisi data temporal kronologis yang membagi keseluruhan 2.464 hari observasi menjadi tiga jendela waktu yang saling terpisah secara sekuensial, sebagaimana dirangkum pada Tabel 3.2.

**Tabel 3.2 Pembagian Jendela Temporal Dataset Penelitian**

| Jendela Temporal | Rentang Tanggal Kalender | Jumlah Hari | Peran Fungsional dalam Metodologi |
|---|---|---:|---|
| Pengembangan (*Development*) | 1 Jan 2020 – 31 Des 2023 | 1.460 | Pelatihan lipatan internal dan penalaan ruang hyperparameter Optuna |
| Validasi Internal (*Validation*) | 1 Jan 2024 – 31 Des 2025 | 731 | Pos pemeriksaan stabilitas (*checkpoint*) pipeline dan pembanding baseline |
| Kumpulan Latih Final (*Train Pool*) | 1 Jan 2020 – 31 Des 2025 | 2.191 | Pelatihan ulang arsitektur final terpilih dengan skema *early stopping* |
| Uji Eksternal (*Out-of-Sample*) | 1 Jan 2026 – 30 Sep 2026 | 273 | Evaluasi performa generalisasi model yang terisolasi secara ketat |

Jendela pengembangan (2020–2023, 1.460 hari) dialokasikan khusus untuk proses penalaan hyperparameter Optuna menggunakan skema 5-fold *Purged Cross-Validation*. Jendela validasi internal (2024–2025, 731 hari) digunakan sebagai pos pemeriksaan stabilitas model. Selanjutnya, kedua jendela tersebut digabungkan menjadi *Train Pool* (2020–2025, 2.191 hari) untuk melatih ulang arsitektur model terbaik yang dihasilkan Optuna, di mana 10% sampel terakhir secara kronologis dialokasikan sebagai subset pemantau penghentian dini (*early stopping*). Terakhir, jendela 1 Januari hingga 30 September 2026 (273 hari) dialokasikan sebagai data uji eksternal murni (*holdout out-of-sample*) yang tidak disentuh sama sekali selama proses pelatihan maupun penalaan hyperparameter berlangsung.

### 2. Pembentukan Sampel Sekuensial Sliding Window

Struktur masukan bagi model LSTM dibentuk menggunakan teknik jendela bergeser (*sliding window*) temporal yang merangkum informasi masa lalu sepanjang parameter *lookback* ($L$) secara berurutan (Lim & Zohren, 2021). Untuk setiap tanggal target prediksi $T$, masukan model berupa matriks berdimensi $L \times 6$, yang memuat $L$ baris observasi fitur historis dari hari-hari sebelum $T$ dan enam kolom fitur teknikal per hari. Jendela masukan bergeser maju satu hari kalender untuk membentuk sampel pelatihan berikutnya.

Pembentukan sampel memerlukan periode pemanasan (*warm-up*) minimal 22 hari untuk mengakomodasi kalkulasi fitur rata-rata bergerak $rv\_mean\_22_t$. Setiap kandidat sampel hanya diterima ke dalam dataset apabila seluruh tanggal di dalam jendela $L$ tersusun kontinu tanpa jeda kalender dan seluruh nilai fitur serta target tersedia lengkap tanpa nilai hilang (*NaN*). Seluruh jendela sampel yang melintasi jeda tanggal 19 Februari 2020 dieliminasi secara otomatis guna menjamin kontinuitas urutan temporal yang valid.

## E. Pemodelan Usulan (LSTM) dan Optimasi Hyperparameter Optuna

### 1. Arsitektur Jaringan Vanilla LSTM Multivariat-Sekuensial

Arsitektur model usulan dibangun menggunakan jaringan saraf tiruan *vanilla Long Short-Term Memory* (LSTM) multivariat-sekuensial berbasis kerangka kerja komputasi *deep learning* TensorFlow/Keras (Greff et al., 2017; Hochreiter & Schmidhuber, 1997; TensorFlow Developers, 2024). Tensor masukan berdimensi `[batch_size, lookback, 6]` dialirkan ke dalam satu atau dua lapisan tersembunyi LSTM yang dilengkapi lapisan regularisasi *Dropout*. Lapisan keluaran akhir berupa satu neuron linear padat (*dense layer*) yang memproyeksikan representasi status tersembunyi akhir ($h_T$) menjadi nilai skalar prediksi $\log RV_{t+1}$.

Interaksi antar-gerbang logika internal LSTM—meliputi gerbang lupa ($f_t$), gerbang masuk ($i_t$), dan gerbang keluar ($o_t$)—berfungsi menyaring arus informasi volatilitas secara adaptif (Hochreiter & Schmidhuber, 1997; Kim & Won, 2018). Gerbang lupa mengeliminasi derau fluktuasi usang, gerbang masuk memperbarui memori sel dengan sinyal guncangan volatilitas baru, dan gerbang keluar mengontrol proyeksi representasi risiko. Arsitektur sekuensial ini memberikan kapasitas pemodelan non-linear yang sangat fleksibel dalam mengenali dinamika ketergantungan temporal jangka panjang pasar Bitcoin.

### 2. Ruang Pencarian Hyperparameter

Kinerja model LSTM sangat sensitif terhadap penetapan hyperparameter arsitektural dan pelatihan. Oleh karena itu, dirancang ruang pencarian (*search space*) yang mencakup enam hyperparameter krusial berdasarkan landasan teoretis komputasi deret waktu (Greff et al., 2017; Kervancı & Akay, 2023). Batasan domain pencarian ditetapkan secara cermat guna mencegah risiko *overfitting* serta menjaga efisiensi proses eksplorasi parameter, sebagaimana dirangkum pada Tabel 3.3.

**Tabel 3.3 Ruang Pencarian Hyperparameter Model LSTM**

| Nama Hyperparameter | Tipe Variabel | Batasan Domain Pencarian | Rasional dan Peran Fungsional |
|---|---|---|---|
| *lookback* ($L$) | Integer | 10 – 30 hari (langkah: 1) | Menentukan panjang horizon memori historis sekuensial masukan |
| *units* ($U$) | Integer | 16 – 128 sel (langkah: 1) | Mengatur kapasitas dimensi representasi non-linear ruang tersembunyi |
| *layers* | Kategorikal | 1 atau 2 lapisan | Menentukan kedalaman hierarki abstraksi representasi fitur temporal |
| *dropout* ($p$) | Float | 0,05 – 0,40 (langkah: 0,05) | Mengontrol intensitas regularisasi penonaktifan bobot pencegah *overfitting* |
| *learning_rate* | Float (Log) | $3 \times 10^{-4}$ – $2 \times 10^{-3}$ | Mengatur besaran langkah pembaruan bobot pada pengoptimal gradien Adam |
| *batch_size* | Kategorikal | 16, 32, 64 sampel | Mengatur ukuran blok data pada estimasi gradien per iterasi pelatihan |

### 3. Skema 5-Fold Purged Rolling-Origin Cross-Validation

Proses pencarian hyperparameter dijalankan pada data pengembangan (2020–2023) menggunakan skema 5-fold *rolling-origin TimeSeriesSplit*. Pada setiap lipatan validasi, data pelatihan selalu mendahului data validasi secara kronologis dengan ukuran jendela pelatihan yang semakin meluas pada setiap lipatan berikutnya. Rancangan *rolling-origin* ini mereplikasi kondisi peramalan dunia nyata di mana masa lalu digunakan untuk meramalkan masa depan secara bertahap.

Guna mengeliminasi potensi kebocoran informasi temporal antar-lipatan akibat tumpang tindih jendela masukan sekuensial, disisipkan jeda pemisah (*purge gap*) sebesar $gap = lookback + 1$ observasi di antara batas akhir data pelatihan dan batas awal data validasi (López de Prado, 2018). Sampel observasi yang berada di dalam zona jeda pemisah dikeluarkan dari evaluasi lipatan tersebut. Kinerja setiap kandidat konfigurasi parameter pada setiap *trial* dinilai berdasarkan rata-rata fungsi kerugian QLIKE dari kelima lipatan validasi silang (Patton, 2011), di mana konfigurasi dengan rata-rata kerugian terendah dipilih sebagai konfigurasi optimal.

### 4. Algoritma Tree-structured Parzen Estimator (TPE) dan MedianPruner

Penalaan hyperparameter dieksekusi menggunakan algoritma Bayesian *Tree-structured Parzen Estimator* (TPE) sebanyak 50 *trial* terarah di bawah kerangka kerja Optuna (Akiba et al., 2019; Bergstra et al., 2011). Algoritma TPE memodelkan distribusi probabilitas konfigurasi parameter bersyarat terhadap performa fungsi objektif, membagi observasi menjadi kelompok berkinerja unggul $\ell(x)$ dan kelompok berkinerja buruk $g(x)$, serta mengarahkan pencarian kandidat baru ke area yang memaksimalkan kriteria *Expected Improvement* (EI).

Guna mengoptimalkan alokasi daya komputasi, algoritma TPE dipadukan dengan mekanisme pemangkasan dini *MedianPruner* (Akiba et al., 2019; Optuna Development Team, 2024). Pengaturan pemangkasan dikonfigurasikan dengan 10 uji coba awal tanpa pemangkasan (*n_startup_trials* = 10) dan dua langkah evaluasi pemanasan (*n_warmup_steps* = 2). Pada setiap lipatan validasi silang yang selesai dievaluasi, *MedianPruner* membandingkan nilai kerugian sementara *trial* berjalan dengan nilai median dari seluruh *trial* sebelumnya pada lipatan yang sama. *Trial* yang memperlihatkan performa di bawah median akan dihentikan secara otomatis, sehingga waktu komputasi dialihkan untuk mengevaluasi kombinasi hyperparameter lain yang lebih potensial.

## F. Pelatihan Model Final dan Protokol Multi-Seed

### 1. Pelatihan Ulang pada Train Pool (2020–2025)

Setelah konfigurasi hyperparameter terbaik diidentifikasi melalui proses optimasi Optuna TPE pada data pengembangan, arsitektur model final dilatih ulang menggunakan seluruh data yang terhimpun dalam *Train Pool* periode 2020 hingga 2025 (Wahyuddin et al., 2025). Penggabungan jendela pengembangan dan validasi internal ini menyediakan 2.191 hari observasi historis, memberikan paparan rezim pasar yang lebih kaya bagi model sebelum menghadapi evaluasi *out-of-sample*.

Pelatihan ulang model final menggunakan optimizer Adam dengan *learning rate* optimal hasil penalaan (Kingma & Ba, 2014) dan fungsi kerugian pelatihan MSE pada skala target yang distandarisasi. Pelatihan dibatasi maksimal 100 epoch dengan mekanisme *EarlyStopping* berpatokan pada *patience* 10 epoch untuk memulihkan bobot sinaptik terbaik (*restore best weights*). Sebanyak 10% sampel terakhir secara kronologis dari *Train Pool* dialokasikan sebagai data pemantau validasi internal *early stopping*, sehingga bobot model tidak mengalami lewat-jenuh pada data latih.

### 2. Protokol Multi-Seed Ensemble

Inisialisasi bobot sinaptik secara acak dan urutan pengacakan batch pelatihan kerap menimbulkan variabilitas performa pada jaringan saraf tiruan (Bouthillier et al., 2021). Menilai kualitas model hanya dari satu kali inisialisasi acak (*single seed*) sangat berisiko memicu bias keberuntungan (*cherry-picking*). Oleh karena itu, penelitian ini menerapkan protokol *multi-seed ensemble* dengan melatih lima model LSTM secara independen menggunakan lima nilai benih acak yang ditetapkan secara apriori, yaitu *seed* 42, 123, 2024, 7, dan 99.

Proyeksi akhir model LSTM untuk setiap langkah peramalan $t+1$ dihasilkan melalui agregasi rata-rata aritmatika (*ensemble average*) dari kelima prediksi model multi-seed tersebut, sebagaimana dirumuskan pada Persamaan (3.7) (Bouthillier et al., 2021; Fawzi et al., 2025):

$$\widehat{\log RV}_{t+1} = \frac{1}{5} \sum_{s \in \{42, 123, 2024, 7, 99\}} \widehat{\log RV}_{t+1}^{(s)} \tag{3.7}$$

Pada Persamaan (3.7), $\widehat{\log RV}_{t+1}^{(s)}$ menyatakan nilai proyeksi satu hari ke depan yang dihasilkan oleh model dengan inisialisasi benih acak $s \in \{42, 123, 2024, 7, 99\}$, sedangkan $\widehat{\log RV}_{t+1}$ merupakan proyeksi akhir hasil rata-rata ansambel. Agregasi multi-seed ini mereduksi varians estimasi individual dan meningkatkan stabilitas prediksi model secara signifikan saat menghadapi dinamika data uji yang belum pernah dipelajari sebelumnya.

## G. Implementasi Model Baseline Pembanding

### 1. Baseline Naif: Random Walk Persistence

Sebagai patokan kelayakan ilmiah paling mendasar (*sanity benchmark*), diimplementasikan model naif *Random Walk Persistence* (Andersen et al., 2003; Patton, 2011). Model *persistence* memproyeksikan bahwa nilai log *realized variance* hari esok sama persis dengan nilai hari ini tanpa melalui estimasi parameter statistik apa pun, sebagaimana dirumuskan pada Persamaan (3.8):

$$\widehat{\log RV}_{t+1} = \log RV_t \tag{3.8}$$

Karena deret volatilitas memiliki ketergantungan temporal autoregresif yang sangat kuat, model *machine learning* yang tidak mampu mengungguli akurasi model *persistence* pada data uji secara statistik dianggap tidak memiliki nilai praktis dalam peramalan deret waktu finansial (Corsi, 2009). Pada studi yang dilakukan, model *persistence* bertindak sebagai salah satu baseline primer penentu keberhasilan penelitian.

### 2. Baseline Ekonometrika High-Frequency: HAR-RV

Model pembanding kedua adalah *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) yang dirumuskan oleh Corsi (2009). Model HAR-RV memodelkan dinamika log *realized variance* melalui kombinasi linier dari komponen harian, komponen mingguan (rata-rata tujuh observasi terakhir), dan komponen bulanan (rata-rata 22 observasi terakhir), sebagaimana dirumuskan pada Persamaan (3.9):

$$\log RV_{t+1} = \beta_0 + \beta_d \log RV_t + \beta_w \left( \frac{1}{7}\sum_{i=0}^{6} \log RV_{t-i} \right) + \beta_m \left( \frac{1}{22}\sum_{i=0}^{21} \log RV_{t-i} \right) + \varepsilon_{t+1} \tag{3.9}$$

Parameter regresi linier Persamaan (3.9) diestimasi menggunakan metode *Ordinary Least Squares* (OLS) pada kumpulan data *Train Pool* (2020–2025). Model HAR-RV memegang peranan sebagai baseline primer kedua untuk membuktikan apakah model non-linear LSTM teroptimasi mampu melampaui standar baku model ekonometrika volatilitas berfrekuensi tinggi.

### 3. Baseline Volatilitas Klasik: GARCH(1,1) Expanding Window

Sebagai representasi model varians bersyarat ekonometrika klasik, diimplementasikan model GARCH(1,1) yang diestimasi dari imbal hasil penutupan harian Bitcoin ($r_t = \ln(C_t/C_{t-1}) \times 100$) (Bollerslev, 1986). Persamaan varians bersyarat GARCH(1,1) dirumuskan sebagai berikut:

$$\sigma_{t+1}^2 = \omega + \alpha \varepsilon_t^2 + \beta \sigma_t^2 \tag{3.10}$$

Parameter model diestimasi menggunakan metode *Quasi-Maximum Likelihood* (QML) dengan skema jendela meluas (*expanding window*) yang diestimasi ulang secara berkala pada setiap awal bulan kalender sepanjang periode evaluasi 2026. Proyeksi varians bersyarat satu langkah ke depan kemudian ditransformasikan ke dalam skala log-varians agar setara dengan target evaluasi. Model GARCH(1,1) diposisikan sebagai baseline sekunder.

### 4. Baseline Deep Learning Heuristik: LSTM Untuned

Baseline sekunder keempat adalah model LSTM dengan konfigurasi heuristik tetap (*untuned*) tanpa melalui proses optimasi Bayesian Optuna. Model ini dikonfigurasikan dengan parameter standar industri: *lookback* 21 hari, 64 unit LSTM satu lapisan, *dropout* 0,20, *learning rate* Adam $10^{-3}$, dan *batch size* 32 sampel. Model ini dilatih pada *Train Pool* menggunakan protokol multi-seed dan *early stopping* yang identik dengan model usulan. Perbandingan terhadap LSTM *untuned* bertujuan mengisolasi dan membuktikan secara empiris kontribusi penalaan hyperparameter terpandu Optuna terhadap peningkatan akurasi peramalan.

Ringkasan formulasi, kategori paradigma, dan konfigurasi dari keempat model baseline disajikan pada Tabel 3.4.

**Tabel 3.4 Konfigurasi Spesifikasi Model Baseline Pembanding**

| Nama Model Baseline | Kategori Paradigma | Formulasi dan Konfigurasi Spesifikasi | Prosedur Estimasi Parameter |
|---|---|---|---|
| *Random Walk Persistence* | Model Naif Statis | $\widehat{\log RV}_{t+1} = \log RV_t$ | Tanpa estimasi parameter statistik |
| HAR-RV (Corsi, 2009) | Ekonometrika RV | Regresi linier 3 skala waktu: harian, mingguan (7 hari), bulanan (22 hari) | Estimasi OLS pada data *Train Pool* (2020–2025) |
| GARCH(1,1) *Expanding* | Ekonometrika Return | Model varians bersyarat $\sigma_{t+1}^2 = \omega + \alpha \varepsilon_t^2 + \beta \sigma_t^2$ | Estimasi QML; *refit* berkala bulanan *expanding window* |
| LSTM *Untuned* Heuristik | *Deep Learning Default* | *Lookback*: 21, *Units*: 64, *Dropout*: 0,20, *Lr*: $10^{-3}$, *Batch*: 32 | Pelatihan Adam pada *Train Pool*; 5-seed ensemble |

## H. Protokol Evaluasi dan Inferensi Statistik

### 1. Metrik Evaluasi: QLIKE, MAE, dan RMSE

Evaluasi performa peramalan model berfokus pada fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) sebagai metrik primer, yang terbukti secara matematis konsisten dan tangguh terhadap proksi varians yang mengandung derau (Patton, 2011). Nilai QLIKE dihitung dari selisih logaritmik aktual dan prediksi ($e_t = \log RV_t - \widehat{\log RV}_t$) sebagaimana dirumuskan pada Persamaan (3.11):

$$QLIKE = \frac{1}{T} \sum_{t=1}^T \left[ \exp(e_t) - e_t - 1 \right] \tag{3.11}$$

Sebagai pelengkap analisis kuantitatif, dihitung pula metrik sekunder berupa *Mean Absolute Error* (MAE) dan *Root Mean Squared Error* (RMSE) langsung pada skala log *realized variance*, sebagaimana dirumuskan pada Persamaan (3.12) dan Persamaan (3.13) (Lim & Zohren, 2021):

$$MAE = \frac{1}{T} \sum_{t=1}^{T} \left| \log RV_t - \widehat{\log RV}_t \right| \tag{3.12}$$

$$RMSE = \sqrt{ \frac{1}{T} \sum_{t=1}^{T} \left( \log RV_t - \widehat{\log RV}_t \right)^2 } \tag{3.13}$$

### 2. Uji Asimtotik Diebold-Mariano dengan Koreksi Newey-West

Uji signifikansi komparatif antara model LSTM-Optuna dan model baseline dilakukan menggunakan uji Diebold-Mariano (Diebold & Mariano, 1995). Misalkan $d_t = QLIKE_{\text{usulan}, t} - QLIKE_{\text{baseline}, t}$ menyatakan deret selisih kerugian harian pada waktu $t$. Hipotesis statistik yang diuji dirumuskan sebagai:

$$H_0: E[d_t] \ge 0 \quad (\text{Model usulan tidak lebih baik dari baseline})$$
$$H_1: E[d_t] < 0 \quad (\text{Model usulan secara signifikan lebih akurat dari baseline})$$

Statistik uji Diebold-Mariano ($DM$) dihitung berdasarkan rasio rata-rata selisih kerugian ($\bar{d}$) terhadap estimasi simpangan baku asimtotiknya:

$$DM = \frac{\bar{d}}{\sqrt{\widehat{\text{Var}}(\bar{d})}} \tag{3.14}$$

Varians $\widehat{\text{Var}}(\bar{d})$ diestimasi menggunakan estimator *Heteroskedasticity and Autocorrelation Consistent* (HAC) Newey-West dengan panjang kelambatan (*lag*) 5 hari guna mengatasi autokorelasi serial dan heteroskedastisitas (Newey & West, 1987). Tingkat signifikansi statistik ditetapkan pada $\alpha = 0{,}05$ secara satu sisi.

### 3. Estimasi Empiris Moving-Block Bootstrap

Sebagai penopang non-parametrik yang tangguh terhadap keterbatasan ukuran sampel data uji, diterapkan metode *Moving-Block Bootstrap* (Künsch, 1989). Metode ini mempertahankan dependensi runtun waktu dengan cara meresampel blok-blok observasi berurutan sepanjang $b = 20$ hari secara berulang sebanyak 10.000 repetisi dengan penetapan benih acak *seed* 42 (Künsch, 1989; Patton, 2011).

Dari 10.000 sampel bootstrap yang terbentuk, dihitung distribusi empiris selisih rata-rata kerugian ($\Delta QLIKE$) guna menyusun interval kepercayaan persentil 95%. Keunggulan model LSTM-Optuna terbukti secara kokoh apabila batas atas dari interval kepercayaan 95% tersebut berada sepenuhnya di bawah angka nol.

### 4. Kriteria Keberhasilan Eksperimen

Kriteria keberhasilan eksperimen ditetapkan secara formal dan apriori mengacu pada protokol evaluasi:

1. **Status Positif (*Positive*):** Diberikan apabila model LSTM-Optuna menghasilkan nilai rata-rata QLIKE yang lebih rendah dibandingkan kedua baseline primer (*Persistence* dan HAR-RV), uji Diebold-Mariano satu sisi menghasilkan $p < 0{,}05$ untuk kedua perbandingan, dan batas atas interval bootstrap 95% berada di bawah nol untuk kedua perbandingan pada data uji 2026.
2. **Status Campuran (*Mixed*):** Diberikan apabila model LSTM-Optuna menghasilkan nilai QLIKE yang lebih rendah dari kedua baseline primer secara numerik (*point estimate*), namun salah satu atau lebih uji signifikansi inferensial belum mencapai ambang signifikansi $p < 0{,}05$ atau batas interval bootstrap melintasi nol.
3. **Status Negatif (*Negative*):** Diberikan apabila model LSTM-Optuna gagal menghasilkan nilai QLIKE yang lebih rendah dibandingkan salah satu atau kedua model baseline primer.

Rangkuman protokol evaluasi dan kriteria inferensi statistik disajikan pada Tabel 3.5.

**Tabel 3.5 Protokol Evaluasi dan Kriteria Inferensi Statistik**

| Komponen Evaluasi | Parameter dan Pengaturan Metodologis |
|---|---|
| Metrik Kerugian Utama | QLIKE dihitung dari log RV aktual dan prediksi: $\exp(e_t)-e_t-1$ |
| Metrik Kerugian Sekunder | Mean Absolute Error (MAE) dan Root Mean Squared Error (RMSE) pada $\log RV$ |
| Uji Signifikansi Primer | Diebold-Mariano satu sisi dengan koreksi HAC Newey-West lag 5 ($\alpha = 0{,}05$) |
| Uji Interval Non-Parametrik | Moving-Block Bootstrap (panjang blok: 20 hari, 10.000 resampel, seed: 42) |
| Pasangan Uji Primer | LSTM-Optuna vs *Random Walk Persistence*; LSTM-Optuna vs HAR-RV |
| Pasangan Uji Sekunder | LSTM-Optuna vs GARCH(1,1); LSTM-Optuna vs LSTM *Untuned* |
| Kriteria Keberhasilan | Klasifikasi status formal: *Positive*, *Mixed*, atau *Negative* secara apriori |

## I. Validitas dan Pengendalian Kebocoran Data

### 1. Pengendalian Temporal Ordering dan Look-Ahead Bias

Ancaman paling fatal terhadap validitas internal penelitian runtun waktu finansial adalah kebocoran informasi masa depan (*look-ahead bias*) (López de Prado, 2018). Pada studi yang dilakukan, urutan kronologis dijaga secara ketat pada setiap modul pemrosesan komputasi. Tidak ada satu pun proses pengacakan sampel yang diizinkan dalam pembentukan fitur masukan maupun peramalan target. Setiap vektor fitur pada hari ke-$t$ murni diekstraksi dari harga penutupan, harga ekstrem, volume, dan *realized variance* yang telah terbentuk sempurna hingga jam 23:59:59 UTC pada hari ke-$t$ tanpa pernah melampaui batas hari pengamatan yang sedang dievaluasi.

### 2. Pengendalian Information Leakage pada Standarisasi Fitur

Kebocoran data kerap menyusup melalui tahapan normalisasi atau penstandaran fitur masukan secara global terhadap seluruh dataset sebelum partisi temporal dilakukan (López de Prado, 2018). Apabila nilai rata-rata dan simpangan baku dihitung menggunakan keseluruhan rentang waktu observasi, maka karakteristik statistik dari data validasi dan data uji akan mencemari proses pembobotan pada data latih. Guna mengeliminasi risiko tersebut, parameter *StandardScaler* hanya diestimasi (*fit*) dari data pelatihan pada masing-masing lipatan validasi silang, kemudian diaplikasikan (*transform*) ke subset evaluasi tanpa pembaruan statistik.

### 3. Pengendalian Purging Gap pada Cross-Validation

Sampel sekuensial yang berdekatan berpotensi memuat sebagian observasi historis yang saling tumpang tindih. Pada skema validasi silang *rolling-origin*, diterapkan jeda pemisah (*purge gap*) sebesar $gap = lookback + 1$ hari di antara data pelatihan dan data validasi (López de Prado, 2018). Sampel yang berada di dalam zona jeda pemisah ini dieliminasi dari evaluasi lipatan tersebut guna menjamin ketiadaan irisan informasi sekuensial antar-partisi.

### 4. Isolasi Data Uji Eksternal

Data uji eksternal tahun 2026 (273 hari) diisolasi secara ketat sejak awal penelitian. Data ini tidak disentuh sama sekali selama proses penalaan hyperparameter Optuna, pelatihan model fold, pemilihan arsitektur, maupun penetapan ambang batas *early stopping*. Isolasi ketat ini menjamin bahwa evaluasi akhir mencerminkan kemampuan generalisasi model yang autentik pada data yang belum pernah dipelajari sebelumnya.

## J. Robustness, Reproduksibilitas, dan Alur Penelitian

### 1. Manajemen Provenance, Cryptographic Hashing, dan Manifest Komputasi

Ketertelusuran data dan protokol penelitian didukung oleh pencatatan *provenance* dan penguncian kode hash kriptografis SHA-256. Sebelum eksperimen skala penuh dijalankan, berkas dataset harian hasil agregasi dikunci dengan nilai hash SHA-256 `ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b` guna mencegah modifikasi data yang tidak terdokumentasi. Setiap eksekusi eksperimen akan secara otomatis mencatat manifes komputasi yang merekam commit Git, hash data, versi pustaka Python, konfigurasi parameter, dan seed acak guna menjamin keterlacakan (*traceability*) dan keterulangan (*reproducibility*) komputasional secara utuh.

### 2. Arsitektur Kode dan Unit Testing Mandiri

Perangkat lunak penelitian dibangun dengan prinsip arsitektur modular yang memisahkan tanggung jawab fungsional secara tegas (*separation of concerns*) menggunakan bahasa pemrograman Python dan kerangka kerja komputasi TensorFlow guna memudahkan audit komputasi (Lim & Zohren, 2021; TensorFlow Developers, 2024). Repositori kode dibagi menjadi sembilan modul sumber mandiri di direktori `study2_volatility/` yang mengelola konfigurasi sistem (`s2_config.py`), pemrosesan data (`s2_data.py`), kalkulasi metrik statistik (`s2_stats.py`), arsitektur model LSTM (`s2_models.py`), optimasi HPO Optuna (`s2_optuna_search.py`), pelatihan final (`s2_final_run.py`), analisis hasil (`s2_analyze.py`), pembuatan visualisasi ilmiah (`s2_figures.py`), serta pencatatan provenance dan jejak audit (`s2_runlog.py`).

Guna menjamin keandalan perangkat lunak, dibangun rangkaian pengujian unit (*unit testing*) mandiri berbasis pustaka `pytest` yang mencakup 34 skenario pengujian komprehensif. Pengujian ini memverifikasi integritas fungsi kalender temporal, isolasi penskalaan *StandardScaler*, penanganan jeda *purge gap*, kalkulasi fungsi kerugian QLIKE, hingga konsistensi uji inferensi statistik sebelum pelatihan skala penuh dieksekusi.

### 3. Tahapan Eksperimen dan Alur Komputasi

Keseluruhan alur tahapan eksperimen komputasional dirangkum secara visual pada Gambar 3.1. Alur penelitian terbagi menjadi tujuh fase utama yang saling terhubung secara berkesinambungan: (1) akuisisi dan audit kualitas data historis 2020–2026, (2) rekayasa fitur kausal dan formulasi target peramalan, (3) partisi dataset temporal kronologis, (4) optimasi hyperparameter LSTM berbasis Optuna TPE dan MedianPruner, (5) pelatihan model final multi-seed dan implementasi empat baseline pembanding, (6) evaluasi out-of-sample dan inferensi statistik Diebold-Mariano serta bootstrap, dan (7) penarikan kesimpulan ilmiah bebas bias seleksi (López de Prado, 2018).

![Gambar 3.1 Alur Tahapan Penelitian Komputasional](figures/gambar_3_1_alur_penelitian.png)

## K. Jadwal Penelitian

Matriks jadwal pelaksanaan penelitian direncanakan berlangsung selama empat bulan (16 minggu), sebagaimana dirangkum pada Tabel 3.6. Jadwal ini mencakup delapan tahapan kegiatan sistematis, mulai dari studi literatur, akuisisi data, eksperimen pemodelan, hingga penyusunan laporan naskah skripsi.

**Tabel 3.6 Matriks Jadwal Pelaksanaan Penelitian**

| No | Tahapan Kegiatan Penelitian | Bulan 1 | Bulan 2 | Bulan 3 | Bulan 4 |
|:--:|---|:---:|:---:|:---:|:---:|
| 1 | Studi literatur & perumusan celah riset (*research gap*) | ✓ | | | |
| 2 | Akuisisi data Binance Vision & verifikasi hash SHA-256 | ✓ | | | |
| 3 | Rekayasa fitur kausal & kalkulasi Realized Variance | ✓ | ✓ | | |
| 4 | Partisi data temporal & implementasi 4 model baseline | | ✓ | | |
| 5 | Eksperimen HPO Bayesian Optuna TPE & Purged CV | | ✓ | ✓ | |
| 6 | Pelatihan final 5-seed ensemble & uji eksternal 2026 | | | ✓ | |
| 7 | Inferensi statistik Diebold-Mariano & Bootstrap | | | ✓ | ✓ |
| 8 | Penyusunan laporan skripsi & ujian seminar proposal/skripsi | | | ✓ | ✓ |


---

# DAFTAR PUSTAKA

Aalborg, H. A., Molnár, P., & de Vries, J. E. (2019). What can explain the price, volatility and trading volume of Bitcoin? *Finance Research Letters, 29*, 255–265. https://doi.org/10.1016/j.frl.2018.08.010

Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2623–2631). ACM. https://doi.org/10.1145/3292500.3330701

Aldo, D., Firmansyah, M. R., & Amrustian, M. A. (2026). Comparative analysis of hyperparameter optimization methods for LSTM in cryptocurrency price prediction: An application to TRX–USD. *Jurnal Teknik Informatika (JUTIF), 7*(3), 2340–2349. https://doi.org/10.52436/1.jutif.2026.7.3.5355

Andersen, T. G., & Bollerslev, T. (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. *International Economic Review, 39*(4), 885–905. https://doi.org/10.2307/2527343

Andersen, T. G., Bollerslev, T., Diebold, F. X., & Labys, P. (2003). Modeling and forecasting realized volatility. *Econometrica, 71*(2), 579–625. https://doi.org/10.1111/1468-0262.00418

Ardia, D., Bluteau, K., & Rüede, M. (2019). Regime changes in Bitcoin GARCH volatility dynamics. *Finance Research Letters, 29*, 266–271. https://doi.org/10.1016/j.frl.2018.08.009

Aswadi, M., & Ependi, U. (2025). Predicting Bitcoin and Ethereum prices using the Long Short-Term Memory (LSTM) model. *Journal of Information Systems and Informatics, 7*(3), 3046–3061. https://doi.org/10.51519/journalisi.v7i3.1228

Barndorff-Nielsen, O. E., & Shephard, N. (2002). Econometric analysis of realized volatility and its use in estimating stochastic volatility models. *Journal of the Royal Statistical Society: Series B (Statistical Methodology), 64*(2), 253–280. https://doi.org/10.1111/1467-9868.00336

Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B. (2011). Algorithms for hyper-parameter optimization. In *Advances in Neural Information Processing Systems* (Vol. 24, pp. 2546–2554). https://papers.nips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html

Binance. (2024). *Binance Vision: Public market data archive*. https://data.binance.vision/

Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics, 31*(3), 307–327. https://doi.org/10.1016/0304-4076(86)90063-1

Bouthillier, X., Delaunay, P., Bronzi, M., Trofimov, A., Nichyporuk, B., Szeto, J., Sepah, N., Raff, E., Madan, K., Voleti, V., Kahou, S. E., Michalski, V., Serdyuk, D., Arbel, T., Pal, C., Varoquaux, G., & Vincent, P. (2021). Accounting for variance in machine learning benchmarks. *Proceedings of Machine Learning and Systems, 3*, 747–769. https://doi.org/10.48550/arXiv.2103.03098

Christensen, K., Siggaard, M., & Veliyev, B. (2023). A machine learning approach to volatility forecasting. *Journal of Financial Econometrics, 21*(5), 1680–1727. https://doi.org/10.1093/jjfinec/nbac020

Conrad, C., Custovic, A., & Ghysels, E. (2018). Long- and short-term cryptocurrency volatility components: A GARCH-MIDAS analysis. *Journal of Risk and Financial Management, 11*(2), 23. https://doi.org/10.3390/jrfm11020023

Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics, 7*(2), 174–196. https://doi.org/10.1093/jjfinec/nbp001

Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics, 13*(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599

Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica, 50*(4), 987–1007. https://doi.org/10.2307/1912773

Fawzi, M. I., Ganesha, T., Anugrah, P. R., Zhahran, M., Abimanyu, F. A., & Bimantoro, H. (2025). Forecasting Bitcoin price prediction with Long Short-Term Memory networks: Implementation and applications using Streamlit. *Jurnal Teknik Informatika (JUTIF), 6*(5), 2940–2961. https://doi.org/10.52436/1.jutif.2025.6.5.5168

Greff, K., Srivastava, R. K., Koutník, J., Steunebrink, B. R., & Schmidhuber, J. (2017). LSTM: A search space odyssey. *IEEE Transactions on Neural Networks and Learning Systems, 28*(10), 2222–2232. https://doi.org/10.1109/TNNLS.2016.2582924

Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735

Katsiampa, P. (2017). Volatility estimation for Bitcoin: A comparison of GARCH models. *Economics Letters, 158*, 3–6. https://doi.org/10.1016/j.econlet.2017.06.023

Kervancı, I. S., & Akay, M. F. (2023). LSTM hyperparameters optimization with Hparam parameters for Bitcoin price prediction. *Sakarya University Journal of Computer and Information Sciences, 6*(1), 1–9. https://doi.org/10.35377/saucis...1172027

Khumaidi, A., Kusmanto, P., & Hikmah, N. (2024). Optimizing Bitcoin price predictions using Long Short-Term Memory algorithm: A deep learning approach. *ILKOM Jurnal Ilmiah, 16*(1), 38–45. https://doi.org/10.33096/ilkom.v16i1.1831.38-45

Kim, H. Y., & Won, C. H. (2018). Forecasting the volatility of stock price index: A hybrid model integrating LSTM with multiple GARCH-type models. *Expert Systems with Applications, 103*, 25–37. https://doi.org/10.1016/j.eswa.2018.03.002

Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*. https://doi.org/10.48550/arXiv.1412.6980

Künsch, H. R. (1989). The jackknife and the bootstrap for general stationary observations. *The Annals of Statistics, 17*(3), 1217–1241. https://doi.org/10.1214/aos/1176347265

Lim, B., & Zohren, S. (2021). Time-series forecasting with deep learning: A survey. *Philosophical Transactions of the Royal Society A, 379*(2194), 20200209. https://doi.org/10.1098/rsta.2020.0209

López de Prado, M. (2018). *Advances in financial machine learning*. John Wiley & Sons.

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica, 55*(3), 703–708. https://doi.org/10.2307/1913610

Optuna Development Team. (2024). *Optuna documentation: Tree-structured Parzen Estimator and MedianPruner algorithms*. Preferred Networks. https://optuna.readthedocs.io/

Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. *Journal of Econometrics, 160*(1), 246–256. https://doi.org/10.1016/j.jeconom.2010.03.034

Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: A simple way to prevent neural networks from overfitting. *Journal of Machine Learning Research, 15*(1), 1929–1958. https://jmlr.org/papers/v15/srivastava14a.html

TensorFlow Developers. (2024). *TensorFlow: Large-scale machine learning on heterogeneous distributed systems*. Google LLC. https://www.tensorflow.org/

Ula, M., Ilhadi, V., & Sidek, Z. M. (2024). Comparing Long Short-Term Memory and Random Forest accuracy for Bitcoin price forecasting. *MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer, 23*(2), 259–272. https://doi.org/10.30812/matrik.v23i2.3267

Wahyuddin, E. P., Caraka, R. E., Kurniawan, R., Caesarendra, W., Gio, P. U., & Pardamean, B. (2025). Improved LSTM hyperparameters alongside sentiment walk-forward validation for time series prediction. *Journal of Open Innovation: Technology, Market, and Complexity, 11*(1), 100458. https://doi.org/10.1016/j.joitmc.2024.100458

Widad, M. Q., Parlika, R., & Aditiawan, F. P. (2026). Comparative analysis of LSTM and GRU models with hyperparameter optimization for Bitcoin price prediction. *Bit-Tech (Binary Digital - Technology), 9*(1), 430–440. https://doi.org/10.32877/bt.v9i1.3887


---

# LAMPIRAN

## Lampiran 1 Salinan Formulir Pengajuan Judul dan Outline Penelitian yang Disetujui

### OUTLINE PROPOSAL SKRIPSI
**PROGRAM STUDI TEKNIK INFORMATIKA — FAKULTAS SAINS DAN TEKNOLOGI**  
**UNIVERSITAS ISLAM NAHDLATUL ULAMA (UNISNU) JEPARA**

| Komponen | Pemisah | Keterangan |
|---|:---:|---|
| **Nama Lengkap** | : | Zaini Leon Musthofa Kamal |
| **Nomor Induk Mahasiswa (NIM)** | : | 231240001455 |
| **Program Studi** | : | Teknik Informatika |
| **Fakultas** | : | Sains dan Teknologi |
| **Dosen Pembimbing** | : | Teguh Tamrin, S.Kom., M.Kom. |
| **Judul Penelitian** | : | **Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin** |

#### Poin Pokok Latar Belakang Masalah
1. **Karakteristik Volatilitas Kripto:** Pasar aset kripto, khususnya Bitcoin, beroperasi secara non-stop 24/7 dan memiliki tingkat fluktuasi yang ekstrem. Peramalan harga nominal penutupan terbukti sangat sulit dilakukan secara konsisten karena deret harga mengikuti lintasan acak (*random walk*) dengan rasio sinyal terhadap derau yang rendah. Sebaliknya, varians terealisasi (*realized variance*) berbasis data intra-hari menunjukkan sifat pengelompokan (*volatility clustering*) dan persistensi temporal yang terstruktur, sehingga lebih representatif dimodelkan sebagai proksi risiko finansial.
2. **Keterbatasan Ekonometrika Klasik vs Keunggulan LSTM:** Model runtun waktu linier konvensional seperti GARCH(1,1) dan HAR-RV memiliki transparansi matematis yang tinggi, namun terbatas pada asumsi stasioneritas dan hubungan linier kaku. Algoritma jaringan saraf tiruan *Long Short-Term Memory* (LSTM) memiliki kapasitas komputasi superior dalam menangkap interaksi non-linear yang kompleks dan dependensi jangka panjang tanpa restriksi distribusi awal.
3. **Urgensi Optimasi Hyperparameter Bayesian Optuna:** Kinerja LSTM sangat rentan terhadap kombinasi *hyperparameter* (panjang *lookback*, jumlah unit neuron, *dropout*, *learning rate*, dan ukuran *batch*). Pendekatan *trial-and-error* manual maupun *random search* tidak efisien dan rentan terjebak pada konfigurasi suboptimal. Algoritma *Tree-structured Parzen Estimator* (TPE) dalam kerangka kerja Optuna menyediakan optimasi terarah berbasis probabilitas Bayesian yang dipadukan dengan *MedianPruner* untuk menghentikan evaluasi berkinerja buruk secara dini.
4. **Pengendalian Kebocoran Data dan Metrik Asimetris:** Mayoritas riset terdahulu rentan terpapar bias kebocoran data (*data leakage*) akibat pemisahan acak atau penskalaan global. Penelitian ini menerapkan protokol *Purged Cross-Validation* dengan jeda pemisah (*purge gap*) dan *fold-specific scaling*. Evaluasi performa difokuskan pada fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) yang tahan terhadap derau proksi, serta diuji signifikansinya menggunakan uji Diebold-Mariano dengan koreksi HAC Newey-West dan *Moving-Block Bootstrap*.

#### Rumusan Masalah
1. Bagaimana merancang arsitektur model *Long Short-Term Memory* (LSTM) teroptimasi Optuna dengan skema *Purged Cross-Validation* untuk mencegah kebocoran data (*data leakage*) pada peramalan *realized volatility* Bitcoin?
2. Sejauh mana peningkatan akurasi peramalan yang dihasilkan oleh model LSTM teroptimasi Optuna dibandingkan dengan *baseline persistence* berdasarkan fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) pada data uji eksternal 2026?
3. Apakah model LSTM teroptimasi Optuna mampu menyaingi performa model ekonometrika klasik *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) dan GARCH(1,1) dalam memproyeksikan volatilitas pasar kripto?

#### Lembar Pengesahan Pengajuan
Jepara, 2026

Pengusul Penelitian,  
**Zaini Leon Musthofa Kamal** (NIM: 231240001455)

Menyetujui,  
Dosen Pembimbing Proposal,  
**Teguh Tamrin, S.Kom., M.Kom.**

---

## Lampiran 2 Matriks Rencana Jadwal Pelaksanaan Penelitian (Gantt Chart 16 Minggu)

| No | Rincian Tahapan Aktivitas Penelitian | Bulan ke-1 (Minggu 1–4) | Bulan ke-2 (Minggu 5–8) | Bulan ke-3 (Minggu 9–12) | Bulan ke-4 (Minggu 13–16) |
|:--:|---|:---:|:---:|:---:|:---:|
| 1 | Studi kepustakaan, analisis gap riset, dan penyusunan proposal | [X] [X] [X] [X] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 2 | Seminar Proposal (Sempro), revisi naskah, dan pengesahan | [ ] [ ] [ ] [ ] | [X] [X] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 3 | Akuisisi 81 berkas data Binance Vision dan audit stempel waktu | [ ] [ ] [ ] [ ] | [ ] [ ] [X] [X] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 4 | Rekayasa 6 fitur kausal, partisi temporal, dan *purged CV* | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [X] [X] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 5 | Eksperimen HPO Optuna TPE (50 trial) dan pelatihan model final | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [X] [X] | [ ] [ ] [ ] [ ] |
| 6 | Evaluasi metrik QLIKE, uji Diebold-Mariano HAC, dan bootstrap | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [X] [X] [ ] [ ] |
| 7 | Penyusunan laporan skripsi lengkap dan pendaftaran munaqosyah | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [X] [X] |

---

## Lampiran 3 Spesifikasi Teknis Lingkungan Komputasi Eksperimen dan Dependensi Perangkat Lunak

### 1. Spesifikasi Perangkat Keras (Hardware Environment)
* **Unit Pemroses Sentral (CPU):** Intel® Core™ i7 / AMD Ryzen™ 7 Processor (8 Cores, 16 Threads)
* **Memori Akses Acak (RAM):** 16 GB DDR4/DDR5 Dual Channel 3200 MHz
* **Akselerator Grafis (GPU):** NVIDIA® GeForce RTX™ Series dengan dukungan VRAM dedicated dan arsitektur CUDA
* **Media Penyimpanan (Storage):** Solid State Drive (SSD) M.2 NVMe PCIe Gen 4x4 kapasitas 512 GB / 1 TB
* **Arsitektur Sistem:** 64-bit x86 Operating Environment

### 2. Spesifikasi Perangkat Lunak dan Dependensi Pustaka (Software Stack)
* **Sistem Operasi:** Microsoft Windows 11 Pro 64-Bit / Ubuntu Linux 22.04 LTS
* **Bahasa Pemrograman Utama:** Python versi 3.10+ (Lingkungan Virtual terisolasi)
* **Framework Deep Learning:** PyTorch (versi 2.2+) / TensorFlow (versi 2.15+) dengan akselerasi CUDA toolkit
* **Framework Hyperparameter Optimization:** Optuna (versi 3.6+) dilengkapi *TPESampler* dan *MedianPruner*
* **Manipulasi Data Deret Waktu:** Pandas (versi 2.2+) dan NumPy (versi 1.26+)
* **Prapemrosesan dan Pembagian Temporal:** Scikit-Learn (versi 1.4+) untuk *StandardScaler* dan *TimeSeriesSplit*
* **Pemodelan Ekonometrika dan HAC Test:** Pustaka `arch` (versi 6.3+) dan `statsmodels` (versi 0.14+)
* **Visualisasi Grafik dan Pelaporan:** Matplotlib (versi 3.8+) dan Seaborn (versi 0.13+)
* **Sistem Kendali Versi (VCS):** Git versi 2.44+ terintegrasi pada GitHub repository publik

---

## Lampiran 4 Kamus Fitur Kausal dan Integritas Kunci Kriptografis SHA-256 Dataset Binance Vision

### 1. Kamus Operasional Enam Fitur Masukan Teknikal Kausal
1. **Fitur 1 ($\log RV_t$):** Logaritma natural dari *realized variance* hari berjalan, dihitung dari 24 bar kline 1 jam UTC dengan formula $\ln(RV_t + 10^{-12})$. Berfungsi menangkap autokorelasi persistensi jangka pendek.
2. **Fitur 2 ($\log \text{range}_t$):** Logaritma natural dari selisih harga tertinggi dan terendah harian, dirumuskan sebagai $\ln(\max H_{t,h} - \min L_{t,h} + 10^{-12})$. Berfungsi menangkap rentang dispersi volatilitas ekstrem harian.
3. **Fitur 3 ($\log \text{volume}_t$):** Logaritma natural dari akumulasi volume transaksi perdagangan harian, dirumuskan sebagai $\ln(\sum V_{t,h} + 10^{-12})$. Berfungsi menangkap intensitas likuiditas dan aktivitas pasar.
4. **Fitur 4 ($\log \text{absret}_t$):** Logaritma natural dari nilai absolut imbal hasil harian, dirumuskan sebagai $\ln(|\ln(C_{t,24} / O_{t,1})| + 10^{-12})$. Berfungsi menangkap magnitudo guncangan harga harian (*price shock magnitude*).
5. **Fitur 5 ($\text{rv\_mean\_5}_t$):** Rata-rata bergerak *log realized variance* horizon mingguan (5 hari perdagangan terakhir), dirumuskan sebagai $(1/5)\sum_{i=0}^4 \log RV_{t-i}$. Berfungsi merepresentasikan ekspektasi volatilitas jangka pendek.
6. **Fitur 6 ($\text{rv\_mean\_22}_t$):** Rata-rata bergerak *log realized variance* horizon bulanan (22 hari perdagangan terakhir), dirumuskan sebagai $(1/22)\sum_{i=0}^{21} \log RV_{t-i}$. Berfungsi merepresentasikan ekspektasi volatilitas jangka menengah.

### 2. Parameter Integritas dan Partisi Data Penelitian
* **Objek Deret Waktu:** Pasangan perdagangan Bitcoin terhadap Tether (BTC/USDT) di bursa Binance.
* **Format Data Mentah:** Berkas kline per jam (*1-hour candlestick bars*) bersumber dari repositori publik Binance Vision.
* **Rentang Observasi:** 1 Januari 2020 hingga 30 September 2026 (total rentang 81 bulan kalender).
* **Standar Penanggalan Harian:** Berdasarkan waktu universal *Coordinated Universal Time* (UTC) 00:00:00 hingga 23:59:59.
* **Amandemen Integritas Data (A1):** Ambang batas toleransi kelengkapan data harian minimal 20 bar kline (83,3% kelengkapan). Hari dengan 20–23 bar dipertahankan secara utuh; hari dengan kurang dari 20 bar dieliminasi.
* **Jumlah Sampel Final:** 2.464 hari observasi terverifikasi (1.460 hari train pool 2020–2023; 731 hari validasi internal 2024–2025; 273 hari uji eksternal out-of-sample 2026).
* **Verifikasi Kunci Kriptografis:** Seluruh berkas data mentah dan data terproses diverifikasi menggunakan algoritma *Secure Hash Algorithm* (SHA-256) guna menjamin ketiadaan korupsi data dan memastikan reproduksibilitas eksperimen independen secara penuh.

---

## Lampiran 5 Format Kartu Kendali / Log Book Bimbingan Proposal Skripsi

**PROGRAM STUDI TEKNIK INFORMATIKA — FAKULTAS SAINS DAN TEKNOLOGI**  
**UNIVERSITAS ISLAM NAHDLATUL ULAMA (UNISNU) JEPARA**

| Identitas Mahasiswa | Pemisah | Keterangan |
|---|:---:|---|
| **Nama Mahasiswa** | : | Zaini Leon Musthofa Kamal |
| **Nomor Induk Mahasiswa (NIM)** | : | 231240001455 |
| **Dosen Pembimbing** | : | Teguh Tamrin, S.Kom., M.Kom. |
| **Judul Proposal Skripsi** | : | Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin |

| Pertemuan Ke- | Hari / Tanggal | Materi Konsultasi dan Pembahasan | Catatan dan Saran Arahan Pembimbing | Paraf Dosen Pembimbing |
|:---:|---|---|---|:---:|
| 1 | .................... 2026 | Pengajuan topik dan penyelarasan latar belakang masalah peramalan volatilitas Bitcoin | Identifikasi research gap diperkuat; fokuskan target pemodelan pada realized variance | .................... |
| 2 | .................... 2026 | Pembahasan rumusan masalah, batasan masalah, dan 3 tujuan penelitian | Sesuaikan rumusan masalah dengan format komparasi model baseline; batasi 6 fitur kausal | .................... |
| 3 | .................... 2026 | Penyusunan Bab II Landasan Teori dan matriks sintesis penelitian terdahulu | Lengkapi perbandingan 13 studi empiris; jabarkan formulasi matematis sel LSTM secara utuh | .................... |
| 4 | .................... 2026 | Penelaahan kerangka pemikiran konseptual dan perumusan 3 hipotesis penelitian | Gambarkan alur kerangka berpikir secara runut; susun hipotesis satu sisi terukur | .................... |
| 5 | .................... 2026 | Pembahasan Bab III Metode Penelitian, skema Purged CV, dan loss QLIKE | Perjelas mekanisme jeda pemisah (purge gap); masukkan protokol evaluasi multi-seed 5 seed | .................... |
| 6 | .................... 2026 | Review draf utuh proposal Bab I–III, uji plagiasi Turnitin, dan persetujuan Sempro | Naskah disetujui untuk diajukan ke Seminar Proposal Skripsi FST UNISNU | .................... |

Jepara, ............................................ 2026  
Mengetahui / Menyetujui,  
Dosen Pembimbing Proposal,  



**Teguh Tamrin, S.Kom., M.Kom.**  
NIP/NIY. ...................................................

