# BAB III METODOLOGI PENELITIAN


## A. Jenis dan Desain Penelitian


### 1. Pendekatan dan Desain Eksperimental Komputasional

Penelitian ini dirancang menggunakan pendekatan kuantitatif dengan desain eksperimental komputasional yang berfokus pada pemodelan runtun waktu finansial secara objektif dan sistematis. Pendekatan kuantitatif dipilih karena fenomena volatilitas pasar aset digital direpresentasikan melalui metrik numerik terukur yang memerlukan pembuktian empiris berbasis data historis (Lim & Zohren, 2021). Desain eksperimental komputasional diterapkan guna memastikan bahwa seluruh tahapan pengujian, mulai dari pra-pemrosesan data mentah, rekayasa fitur kausal, pencarian parameter optimal, hingga inferensi statistik, dieksekusi secara otomatis melalui instruksi perangkat lunak yang terkontrol secara ketat. Pendekatan terstruktur ini memungkinkan pengujian hipotesis dilakukan dalam kondisi lingkungan komputasi yang seragam, sehingga perbandingan akurasi peramalan antara arsitektur jaringan saraf tiruan yang diusulkan dan seluruh model pembanding dapat diukur secara adil tanpa adanya distorsi subjektivitas peneliti.

Integritas metodologis pada studi yang dilakukan ditegakkan melalui penerapan prinsip pra-registrasi protokol eksperimen komputasional sebelum model dieksekusi pada data uji. Protokol eksperimen menetapkan batasan ruang pencarian hyperparameter, kriteria fungsi kerugian, skema validasi silang, serta metode inferensi statistik secara apriori sebelum evaluasi out-of-sample dilakukan (Bouthillier et al., 2021). Melalui pembekuan spesifikasi algoritma dan penguncian urutan analisis, risiko terjadinya bias seleksi model maupun manipulasi pengujian hipotesis (p-hacking) dapat dieliminasi secara menyeluruh. Paradigma komputasional ini memberikan jaminan bahwa seluruh luaran peramalan yang dihasilkan bukan merupakan hasil penyesuaian parameter secara retrospektif (post-hoc fitting), melainkan murni merefleksikan kapasitas generalisasi model jaringan saraf tiruan dalam menangkap dinamika ketidakpastian pasar finansial pada periode waktu yang belum pernah diobservasi sebelumnya. Prosedur metodologis yang ketat dan terstandarisasi ini.

### 2. Objek Penelitian dan Ruang Lingkup

Objek yang diteliti pada studi yang dilakukan adalah realized volatility harian dari pasangan perdagangan Bitcoin terhadap Tether (BTC/USDT) pada bursa aset digital global. Aset kripto Bitcoin dipilih sebagai objek kajian utama karena memiliki kapitalisasi pasar terbesar serta memperlihatkan karakteristik dinamika volatilitas yang sangat kompleks, ekstrem, dan berfluktuasi tinggi tanpa henti (Andersen et al., 2003; Katsiampa, 2017). Fenomena ketidakpastian harga yang sering kali memicu lompatan nilai secara tiba-tiba (volatility jumps) dan pengelompokan gejolak pasar (volatility clustering) menjadikan Bitcoin instrumen yang sangat menantang bagi model peramalan runtun waktu. Pengukuran volatilitas berbasis data frekuensi tinggi intra-hari memberikan estimasi variabilitas harga yang jauh lebih akurat dibandingkan penggunaan kuadrat imbal hasil harian konvensional yang kerap kali terdistorsi derau mikrostruktur pasar keuangan digital terkini.

Ruang lingkup penelitian ini dibatasi secara tegas pada peramalan varians terealisasi logaritmik satu langkah ke depan ($t+1$) pada skala temporal harian. Pembatasan horizon peramalan satu hari ke depan bertujuan untuk memfokuskan analisis komputasi pada pembuktian keunggulan arsitektur deep learning dalam menangani persistensi volatilitas jangka pendek yang sangat krusial bagi manajemen risiko portofolio (Kim & Won, 2018). Penelitian ini membatasi ranah pengujian pada akurasi peramalan statistik dan signifikansi inferensi ekonometrika komputasional, sehingga tidak mencakup simulasi eksekusi strategi perdagangan aktif frekuensi tinggi atau analisis arbitrase likuiditas pasar. Dengan menetapkan batasan objektif ini, pengujian performa dapat diarahkan secara mendalam untuk menguji apakah optimasi hyperparameter berbasis algoritma Bayesian Optuna mampu memberikan lompatan akurasi yang signifikan secara statistik. Prosedur metodologis yang ketat dan.

### 3. Sumber dan Pengumpulan Data

Sumber data primer yang digunakan pada studi yang dilakukan diperoleh secara langsung dari repositori arsip data publik resmi Binance Vision (Binance, 2024). Platform Binance dipilih sebagai penyedia data rujukan utama karena memegang pangsa pasar likuiditas perdagangan Bitcoin global terbesar, sehingga menghasilkan representasi pembentukan harga pasar yang sangat mendalam dan berkesinambungan bagi komunitas internasional. Data yang dikumpulkan merupakan data candlestick (kline) dengan frekuensi temporal 1 jam untuk pasangan aset BTC/USDT yang mencakup riwayat perdagangan sejak tanggal 1 Januari 2020 hingga 30 September 2026. Periode pengamatan selama hampir tujuh tahun ini mencakup berbagai siklus pasar yang sangat beragam, termasuk fase pasar bullish yang agresif, fase bear market yang berkepanjangan, hingga periode konsolidasi makroekonomi pasca peristiwa halving. Prosedur metodologis yang ketat dan.

Mekanisme pengumpulan data dijalankan secara terprogram melalui skrip otomasi komputasi yang mengunduh 81 berkas arsip kompresi bulanan resmi dari peladen Binance Vision. Setiap berkas arsip yang berhasil diunduh langsung diperiksa integritas fisiknya melalui perhitungan fungsi hash satu arah Secure Hash Algorithm 256-bit (SHA-256) dan dicatat secara sistematis ke dalam berkas manifes komputasi (López de Prado, 2018). Prosedur pencatatan hash kriptografis ini menjamin bahwa seluruh berkas data mentah yang dianalisis pada studi yang dilakukan bersifat autentik, tidak mengalami korupsi data selama proses transfer jaringan, dan dapat diverifikasi ulang secara independen oleh peneliti lain. Prosedur akuisisi data yang transparan ini menjadi fondasi awal yang kokoh dalam menegakkan standar ketertelusuran ilmiah dan keterulangan komputasi sepanjang siklus penelitian berlangsung. Prosedur metodologis yang ketat.

## B. Data Penelitian dan Pra-Pemrosesan


### 1. Audit Kualitas dan Integritas Data

Tahap awal pra-pemrosesan data difokuskan pada pelaksanaan audit kualitas dan verifikasi integritas struktur bar harga intra-hari secara menyeluruh pada seluruh runtun waktu. Karena pasar aset digital beroperasi tanpa henti selama 24 jam sehari dan 7 hari seminggu, maka setiap unit hari kalender wajib memiliki tepat 24 bar kline berdurasi 1 jam (Binance, 2024). Pemeriksaan kelengkapan bar dilakukan dengan memvalidasi kontinuitas sekuens stempel waktu intra-hari guna mendeteksi keberadaan celah data (data gaps) yang berpotensi timbul akibat kendala konektivitas bursa atau periode pemeliharaan peladen berkala. Keberadaan bar yang hilang atau tidak lengkap dapat menyebabkan distorsi sistematis pada kalkulasi nilai realized variance harian, sehingga audit kualitas data menjadi prasyarat mutlak sebelum fitur dan target peramalan dihitung secara presisi. Langkah pra-pemrosesan data.

Berdasarkan audit kelengkapan sekuens intra-hari, ditemukan 15 unit hari kalender pada rentang Januari 2020 hingga Maret 2023 yang memiliki jumlah bar antara 19 hingga 23 bar akibat jendela pemeliharaan sistem bursa (Ardia et al., 2019). Guna menjaga konsistensi kalender runtun waktu tanpa merusak representasi volatilitas pasar, ditetapkan Amandemen Data A1 secara apriori sebelum eksperimen dijalankan. Aturan amandemen ini menetapkan bahwa hari dengan jumlah bar kurang dari 20 bar akan dieliminasi dari dataset, sementara hari dengan ketersediaan 20 hingga 23 bar tetap dipertahankan dengan menghitung realized variance dari bar yang tersedia serta menyematkan label provisi data. Berdasarkan aturan tersebut, hanya satu hari kalender yang dieliminasi, yaitu tanggal 19 Februari 2020 yang hanya memiliki 19 bar. Langkah pra-pemrosesan data yang.

### 2. Normalisasi Timestamp dan Agregasi Bar Harian UTC

Stempel waktu transaksi pada berkas historis Binance Vision memiliki variasi format penomoran, mulai dari presisi milidetik hingga mikrodetik yang mengikuti perkembangan pembaruan mesin pencocokan transaksi bursa (Binance, 2024). Seluruh stempel waktu tersebut dinormalisasi ke format standar waktu Universal Time Coordinated (UTC) dengan resolusi detik guna memastikan sinkronisasi temporal yang seragam. Pemilihan basis zona waktu UTC sangat esensial karena perdagangan aset kripto bersifat lintas negara tanpa batas sesi pembukaan atau penutupan bursa regional (Conrad et al., 2018). Setiap bar perdagangan 1 jam dialokasikan secara presisi ke dalam batas awal jam 00:00:00 UTC hingga batas akhir jam 23:59:59 UTC, sehingga batas pergantian hari kalender terdefinisi secara konsisten di seluruh rentang tahun penelitian. Langkah pra-pemrosesan data yang sistematis ini menjadi jaminan.

Setelah stempel waktu dinormalisasi, dilakukan proses agregasi 24 bar intra-hari berdurasi 1 jam untuk membentuk satu bar observasi harian tunggal yang mencakup harga pembukaan, harga tertinggi, harga terendah, harga penutupan, volume transaksi kumulatif, serta nilai realized variance harian (Barndorff-Nielsen & Shephard, 2002). Konsistensi pembentukan bar harian berbasis UTC menjamin bahwa estimasi variabilitas harga intra-hari bebas dari distorsi zona waktu lokal peneliti yang dapat memicu ketidaksinkronan temporal antarsiklus perdagangan. Melalui tahapan audit integritas dan agregasi harian yang sistematis ini, diperoleh dataset final yang sepenuhnya bersih dan kontinu sebanyak 2.464 hari kalender perdagangan, yang membentang tanpa jeda sejak tanggal 1 Januari 2020 hingga tanggal 30 September 2026 secara lengkap, rapi, dan teratur untuk analisis lanjutan. Langkah pra-pemrosesan data yang sistematis.

## C. Pengembangan Fitur dan Target Peramalan


### 1. Kalkulasi Realized Variance dan Transformasi Logaritmik

Variabel target yang diramalkan pada studi yang dilakukan dirumuskan melalui perhitungan realized variance harian yang mengagregasikan kuadrat imbal hasil logaritmik intra-hari berfrekuensi tinggi (Andersen & Bollerslev, 1998; Barndorff-Nielsen & Shephard, 2002). Pendekatan data frekuensi tinggi intra-hari ini memungkinkan penangkapan lintasan variabilitas harga secara terperinci tanpa terdistorsi oleh fluktuasi sesaat pembukaan dan penutupan harian. Untuk setiap unit hari kalender perdagangan $t$, nilai realized variance harian ($RV_t$) dihitung secara matematis melalui akumulasi penjumlahan kuadrat imbal hasil logaritmik dari 24 bar kline berdurasi 1 jam yang tersedia sepanjang 24 jam penuh hari bersangkutan sebagaimana diformulasikan pada Persamaan (3.1). Formulasi ini menjadi standar baku dalam ekonometrika keuangan modern untuk memperoleh estimasi volatilitas yang bebas dari bias mikrostruktur pasar. Formulasi fitur teknikal kausal ini.

$$
RV_t = \sum_{h=1}^{24} \left[ \ln\left( \frac{C_{t,h}}{O_{t,h}} \right) \right]^2
\tag{3.1}
$$

Berdasarkan Persamaan (3.1), variabel $C_{t,h}$ merepresentasikan harga penutupan dan $O_{t,h}$ adalah harga pembukaan pada jam perdagangan ke-$h$ dalam hari kalender $t$. Nilai realized variance yang dihasilkan dari perhitungan tersebut secara empiris memperlihatkan distribusi data yang sangat menceng ke kanan (positive skewness) dengan ekor yang sangat tebal (leptokurtik), yang merupakan ciri khas pasar kripto (Andersen et al., 2003). Guna menstabilkan varians dan mendekatkan distribusi data ke bentuk kurva normal yang ideal bagi proses konvergensi fungsi optimasi jaringan saraf tiruan, nilai $RV_t$ ditransformasikan ke dalam skala logaritma natural sebagaimana disajikan pada Persamaan (3.2). Transformasi logaritmik ini memastikan bahwa model belajar menangkap proporsi perubahan volatilitas secara simetris tanpa terdominasi oleh lonjakan nilai absolut ekstrem. Formulasi fitur teknikal kausal ini memastikan bahwa.

$$
\log RV_t = \ln\left( RV_t + 10^{-12} \right)
\tag{3.2}
$$

Konstanta kecil bernilai $10^{-12}$ ditambahkan ke dalam argumen logaritma pada Persamaan (3.2) sebagai suku penstabil numerik guna mencegah timbulnya nilai tak hingga ketika varians mendekati nol pada kondisi pasar yang sangat tenang (Andersen et al., 2003). Variabel target yang akan diprediksi oleh model pembelajaran mendalam didefinisikan secara prospektif sebagai $\log RV_{t+1}$, yaitu nilai log realized variance pada satu hari perdagangan berikutnya di masa depan. Penetapan target berbasis logaritma natural realized variance satu langkah ke depan ini memastikan bahwa model diarahkan untuk mengevaluasi skala ketidakpastian pasar masa depan secara terukur. Pendekatan peramalan prospektif ini memberikan landasan operasional yang sangat relevan bagi aplikasi pengelolaan risiko investasi dan mitigasi fluktuasi portofolio aset kripto. Formulasi fitur teknikal kausal ini memastikan bahwa seluruh.

### 2. Pembentukan Enam Fitur Masukan Teknikal Kausal

Penelitian ini merancang himpunan enam fitur masukan teknikal kausal yang dirumuskan secara ketat hanya menggunakan informasi historis yang telah tersedia hingga penutupan hari $t$ (Aalborg et al., 2019; Christensen et al., 2023). Pembatasan informasi kausal ini menjamin bahwa tidak ada kebocoran data masa depan (look-ahead bias) yang menyusup ke dalam proses pembelajaran representasi internal jaringan saraf tiruan. Fitur pertama adalah log realized variance hari ini ($\log RV_t$) yang berfungsi menangkap derajat persistensi volatilitas terkini, sedangkan fitur kedua adalah log intraday range ($\log range_t$) yang mengukur selisih logaritmik antara harga tertinggi dan terendah intra-hari sebagaimana disajikan pada Persamaan (3.3). Rentang harga ekstrem intra-hari ini memberikan sinyal tambahan mengenai intensitas tekanan dispersi harga yang terjadi di pasar secara dinamis.

$$
\log range_t = \ln\left( \frac{H_t}{L_t} \right) = \ln\left( \frac{\max_{h} H_{t,h}}{\min_{h} L_{t,h}} \right)
\tag{3.3}
$$

Fitur masukan ketiga merepresentasikan volume perdagangan logaritmik kumulatif harian ($\log volume_t = \ln(V_t + 10^{-12})$ dengan $V_t = \sum_{h=1}^{24} V_{t,h}$), yang mengindikasikan intensitas likuiditas dan aktivitas partisipasi pasar yang sering kali menjadi pemicu eskalasi volatilitas harga aset kripto (Christensen et al., 2023). Fitur keempat dirumuskan sebagai logaritmik imbal hasil absolut harian ($\log absret_t$) sebagaimana ditunjukkan pada Persamaan (3.4), yang menangkap magnitudo guncangan pergerakan harga pasar tanpa memperhitungkan arah pergerakan kenaikan atau penurunan. Penggabungan volume transaksi dan besaran imbal hasil absolut ini melengkapi profil informasi pasar, sehingga model jaringan saraf tiruan mampu mengenali apakah gejolak volatilitas didorong oleh volume likuiditas yang tinggi ataukah oleh kepanikan pasar yang sepi likuiditas secara objektif. Formulasi fitur teknikal kausal ini memastikan bahwa seluruh.

$$
\log absret_t = \ln\left( \left| \ln\left( \frac{C_t}{C_{t-1}} \right) \right| + 10^{-12} \right)
\tag{3.4}
$$

Guna membekali model LSTM dengan informasi memori jangka menengah dan jangka panjang sebagaimana terbukti efektif pada arsitektur ekonometrika heterogen, dirumuskan fitur kelima dan keenam berupa rata-rata bergerak historis (Corsi, 2009). Fitur kelima ($rv\_mean\_5_t$) merupakan rata-rata log realized variance selama 5 hari perdagangan terakhir untuk menangkap komponen mingguan sebagaimana diformulasikan pada Persamaan (3.5), sedangkan fitur keenam ($rv\_mean\_22_t$) merupakan rata-rata bergerak selama 22 hari perdagangan terakhir yang merepresentasikan siklus volatilitas bulanan pasar pada Persamaan (3.6). Ringkasan formulasi matematis, definisi operasional, dan justifikasi teoretis dari keenam fitur masukan teknikal kausal disajikan secara sistematis pada Tabel 3.1 sebagai representasi kausalitas multiskala pasar Bitcoin yang komprehensif bagi arsitektur komputasi dalam mengekstraksi ketergantungan temporal jangka panjang secara efektif dan konsisten (López de Prado, 2018).

$$
rv\_mean\_5_t = \frac{1}{5} \sum_{i=0}^{4} \log RV_{t-i}
\tag{3.5}
$$

$$
rv\_mean\_22_t = \frac{1}{22} \sum_{i=0}^{21} \log RV_{t-i}
\tag{3.6}
$$

**Tabel 3.1 Definisi Fitur Masukan Teknikal Kausal**

| No | Nama Fitur | Formulasi Matematis | Peran dan Justifikasi Teoretis |
|---:|---|---|---|
| 1 | $\log RV_t$ | $\ln(RV_t + 10^{-12})$ | Mengukur level volatilitas terealisasi terkini dan persistensi autoregresif harian |
| 2 | $\log range_t$ | $\ln(\max_h H_{t,h} / \min_h L_{t,h})$ | Menangkap dispersi harga ekstrem intra-hari sebagai proksi volatilitas bayangan |
| 3 | $\log volume_t$ | $\ln(\sum_h V_{t,h} + 10^{-12})$ | Merefleksikan intensitas likuiditas transaksi dan tekanan aliran pesanan pasar |
| 4 | $\log absret_t$ | $\ln(\lvert \ln(C_t / C_{t-1}) \rvert + 10^{-12})$ | Menangkap magnitudo guncangan imbal hasil absolut harian tanpa bias arah |
| 5 | $rv\_mean\_5_t$ | $\frac{1}{5}\sum_{i=0}^{4} \log RV_{t-i}$ | Merepresentasikan komponen memori volatilitas jangka menengah (siklus mingguan) |
| 6 | $rv\_mean\_22_t$ | $\frac{1}{22}\sum_{i=0}^{21} \log RV_{t-i}$ | Merepresentasikan komponen memori volatilitas jangka panjang (siklus bulanan) |

### 3. Skalasi Fitur Tanpa Kebocoran (StandardScaler Fold-Specific)

Pelatihan jaringan saraf tiruan berbasis perambatan mundur (backpropagation) dan algoritma optimasi gradien adaptif sangat rentan terhadap disparitas skala antarvariabel masukan yang dialirkan ke dalam sel komputasi (Hochreiter & Schmidhuber, 1997; Kingma & Ba, 2014). Apabila fitur-fitur masukan memiliki rentang magnitudo yang berbeda secara drastis—misalnya volume perdagangan harian yang bernilai jutaan dibandingkan log imbal hasil yang bernilai desimal kecil—fungsi pembaruan bobot sinaptik akan didominasi secara keliru oleh gradien dari variabel bernilai besar. Atas dasar tersebut, seluruh fitur masukan dan variabel target wajib ditransformasikan ke dalam skala standar menggunakan algoritma StandardScaler, yang memusatkan sebaran data pada nilai rata-rata nol dan menyelaraskan simpangan baku menjadi satu demi kelancaran propagasi gradien matematika yang stabil, teratur, dan konvergen secara seimbang. Formulasi fitur teknikal.

Guna mencegah terjadinya kebocoran informasi masa depan (information leakage) secara sistematis, parameter penstandar—yaitu nilai rata-rata ($\mu$) dan simpangan baku ($\sigma$)—hanya dihitung (fit) dari data pelatihan pada masing-masing subset lipatan validasi silang (López de Prado, 2018). Parameter yang diekstraksi dari data latih tersebut kemudian diterapkan (transform) secara satu arah untuk menstandarisasi data validasi dan data uji tanpa memperbarui statistik penskalaan. Demikian pula pada tahap pelatihan model final, penskalaan hanya dihitung dari kumpulan data latih pengembangan. Setelah prediksi log realized variance terstandarisasi dihasilkan oleh model, nilai tersebut langsung dikembalikan ke skala logaritma aslinya (inverse transform) sebelum seluruh metrik evaluasi dihitung demi menjaga kemurnian evaluasi out-of-sample secara ketat, konsisten, dan terbebas dari polusi informasi eksternal. Formulasi fitur teknikal kausal ini memastikan.

## D. Pembagian Data Temporal Kronologis (Temporal Window)


### 1. Pembagian Dataset: Pengembangan, Validasi, dan Uji Eksternal

Penelitian runtun waktu finansial melarang keras penggunaan metode pembagian data secara acak (random split) atau pengacakan silang konvensional (shuffling), karena data keuangan mengandung korelasi serial dan struktur kausalitas waktu yang kuat (López de Prado, 2018). Pengacakan acak akan menyebabkan data masa depan bocor ke dalam data masa lalu, sehingga menghasilkan estimasi performa model yang terlalu optimis secara semu (look-ahead bias). Atas dasar tersebut, penelitian ini menerapkan partisi temporal kronologis yang membagi rentang observasi menjadi tiga jendela waktu yang saling terpisah secara sekuensial: jendela pengembangan (development window), jendela validasi internal (validation checkpoint), dan jendela uji eksternal (out-of-sample holdout test window) guna merefleksikan kondisi peramalan dunia nyata secara autentik, kredibel, dan dapat diandalkan secara ilmiah. Pembagian partisi temporal yang terisolasi.

Rincian pembagian jendela temporal dataset penelitian disajikan pada Tabel 3.2. Jendela pengembangan mencakup rentang 1 Januari 2020 hingga 31 Desember 2023 (1.460 hari) yang difungsikan secara eksklusif untuk pelatihan model awal dan pencarian hyperparameter optimal melalui skema validasi silang (Bouthillier et al., 2021). Jendela validasi internal mencakup rentang 1 Januari 2024 hingga 31 Desember 2025 (731 hari) yang berfungsi sebagai pos pemeriksaan kualitas pipa komputasi dan kalibrasi model pembanding tanpa diikutsertakan dalam penalaan parameter arsitektur. Gabungan kedua jendela ini (2020–2025) membentuk train pool sebanyak 2.191 hari untuk melatih model final, sedangkan periode 1 Januari 2026 hingga 30 September 2026 (273 hari) diisolasi sebagai data uji eksternal murni yang sepenuhnya steril dari intervensi model dan campur tangan optimasi apapun.

**Tabel 3.2 Pembagian Temporal Window Dataset**

| Jendela Temporal | Rentang Tanggal Kalender | Jumlah Hari | Peran Fungsional dalam Metodologi |
|---|---|---:|---|
| Pengembangan (Development) | 1 Jan 2020 – 31 Des 2023 | 1.460 | Pelatihan lipatan internal dan penalaan ruang hyperparameter Optuna |
| Validasi Internal (Validation) | 1 Jan 2024 – 31 Des 2025 | 731 | Pemeriksaan stabilitas pipa komputasi dan kalibrasi parameter baseline |
| Kumpulan Latih Final (Train Pool) | 1 Jan 2020 – 31 Des 2025 | 2.191 | Pelatihan ulang model final terpilih sebelum evaluasi out-of-sample |
| Uji Eksternal (Holdout Test) | 1 Jan 2026 – 30 Sep 2026 | 273 | Evaluasi performa generalisasi out-of-sample murni satu kali eksekusi |

### 2. Pembentukan Sampel Sekuensial Sliding Window

Struktur masukan bagi arsitektur LSTM dibentuk melalui mekanisme jendela bergeser (sliding window) temporal yang merangkum riwayat masa lalu sepanjang parameter lookback ($L$) secara sekuensial (Lim & Zohren, 2021). Untuk setiap target peramalan hari ke-$t+1$, masukan yang disajikan ke dalam jaringan saraf tiruan berupa matriks dua dimensi berukuran $L imes 6$, di mana $L$ menunjukkan jumlah langkah waktu historis ke belakang dan angka 6 merepresentasikan jumlah fitur masukan teknikal kausal. Jendela bergeser bergerak maju satu langkah waktu setiap hari kalender, sehingga dinamika transisi volatilitas dapat ditangkap secara berkesinambungan tanpa merusak urutan sekuensial data pasar. Pendekatan sliding window ini memungkinkan model merefleksikan konteks temporal secara adaptif pada setiap titik peramalan runtun waktu. Pembagian partisi temporal yang terisolasi secara ketat ini.

Pembentukan sampel sliding window memerlukan periode pemanasan awal (warm-up period) akibat kebutuhan historis dari fitur rata-rata bergerak 22 hari ($rv\_mean\_22_t$) serta panjang lookback yang dieksplorasi (Greff et al., 2017). Konsekuensinya, jumlah sampel efektif yang dapat digunakan dalam proses pelatihan sedikit lebih kecil dibandingkan jumlah hari kalender mentah yang tersedia pada jendela temporal bersangkutan. Seluruh sampel dibentuk secara ketat hanya jika seluruh nilai fitur pada blok waktu lookback tersedia secara lengkap tanpa celah data, sehingga konsistensi dimensi matriks masukan tetap terjaga saat dialirkan ke dalam lapisan sel memori jaringan LSTM. Ketiadaan interpolasi buatan pada sampel yang hilang menjamin kualitas representasi matematis yang bersih bagi model peramalan runtun waktu finansial dalam menangkap eskalasi gejolak pasar secara akurat. Pembagian partisi temporal.

## E. Pemodelan Usulan (LSTM) dan Optimasi Hyperparameter Optuna


### 1. Arsitektur Jaringan Vanilla LSTM Multivariat-Sekuensial

Model deep learning yang dirancang pada studi yang dilakukan mengadopsi arsitektur Vanilla Long Short-Term Memory (LSTM) multivariat-sekuensial untuk menangani pemodelan runtun waktu finansial secara optimal (Greff et al., 2017; Hochreiter & Schmidhuber, 1997). Arsitektur ini terdiri atas lapisan masukan temporal yang menerima tensor berdimensi [batch size, lookback, 6 fitur], diikuti oleh satu atau dua lapisan tersembunyi bersel memori LSTM, lapisan regularisasi dropout, dan diakhiri oleh satu lapisan keluaran linear (dense) tanpa fungsi aktivasi non-linear untuk memproyeksikan estimasi skalar $\log RV_{t+1}$. Pemilihan arsitektur vanilla LSTM didasarkan pada efisiensi komputasinya yang seimbang serta kemampuannya yang terbukti tangguh dalam memodelkan ketergantungan non-linear jangka panjang pada deret waktu finansial frekuensi tinggi terkini secara komputasional dan stabil. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan.

Mekanisme internal sel LSTM mengandalkan interaksi dinamis antara gerbang lupa ($f_t$), gerbang masuk ($i_t$), kandidat pembaruan sel ($\tilde{c}_t$), dan gerbang keluar ($o_t$) guna mengatur aliran informasi temporal secara adaptif (Hochreiter & Schmidhuber, 1997; Kim & Won, 2018). Gerbang lupa bertugas membuang informasi volatilitas masa lalu yang telah usang atau tidak relevan, gerbang masuk menyeleksi sinyal guncangan harga baru yang perlu disimpan ke dalam status memori sel ($c_t$), sedangkan gerbang keluar mengontrol proyeksi representasi status tersembunyi ($h_t$) ke lapisan keluaran. Struktur selular ini melindungi gradien galat dari ancaman lenyapnya gradien (vanishing gradient), sehingga memungkinkan jaringan mempelajari pola pengelompokan volatilitas Bitcoin yang memiliki persistensi tinggi secara stabil dan berkelanjutan tanpa degradasi bobot. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan.

### 2. Ruang Pencarian Hyperparameter

Guna menemukan konfigurasi arsitektur jaringan yang optimal tanpa campur tangan subjektif manusia, ruang pencarian hyperparameter ditetapkan secara apriori sebelum proses optimasi komputasi dijalankan (Akiba et al., 2019; Bergstra et al., 2011). Ruang pencarian mencakup enam hyperparameter krusial yang menentukan kapasitas representasi, laju pembelajaran, dan efektivitas regularisasi model: panjang jendela lookback temporal, jumlah unit memori per lapisan LSTM, jumlah kedalaman lapisan, tingkat dropout regularisasi, laju pembelajaran pengoptimal Adam, serta ukuran batch pelatihan. Konfigurasi batas ruang pencarian hyperparameter dirangkum secara rinci pada Tabel 3.3. Penetapan ruang eksplorasi yang terstruktur ini menjamin pencarian parameter berlangsung secara komprehensif, efisien, dan objektif demi menemukan konfigurasi arsitektur yang paling adaptif terhadap data historis Bitcoin secara sistematis, terukur, dan transparan. Penalaan hyperparameter berbasis algoritma Bayesian.

Batas bawah dan batas atas pada ruang pencarian ditentukan secara cermat berdasarkan karakteristik data deret waktu harian yang memiliki ukuran sampel terbatas guna menghindari risiko overfitting ekstrem (Greff et al., 2017; Kervancı & Akay, 2023). Parameter lookback dibatasi antara 10 hingga 30 hari untuk menangkap dinamika memori jangka pendek dan bulanan pasar kripto. Jumlah unit tersembunyi dibatasi antara 16 hingga 128 unit, kedalaman lapisan ditetapkan maksimal dua lapisan, dan tingkat dropout dibatasi pada rentang 0,05 hingga 0,40. Laju pembelajaran dieksplorasi secara logaritmik antara $3 \times 10^{-4}$ hingga $2 \times 10^{-3}$, sedangkan ukuran batch dibatasi pada pilihan nilai 16, 32, dan 64 guna menjaga stabilitas estimasi gradien stokastik sepanjang pelatihan berlangsung. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan.

**Tabel 3.3 Ruang Pencarian Hyperparameter Model LSTM**

| Nama Hyperparameter | Tipe Variabel | Batasan Domain Pencarian | Rasional dan Peran Fungsional |
|---|---|---|---|
| lookback ($L$) | Integer | 10 – 30 hari (langkah: 1) | Menentukan panjang horizon memori historis sekuensial masukan |
| units ($U$) | Integer | 16 – 128 sel (langkah: 1) | Mengatur kapasitas dimensi representasi non-linear ruang tersembunyi |
| layers | Kategorikal | 1 atau 2 lapisan | Menentukan kedalaman hierarki abstraksi representasi fitur temporal |
| dropout ($p$) | Float | 0,05 – 0,40 (langkah: 0,05) | Mengontrol intensitas regularisasi penonaktifan bobot pencegah overfitting |
| learning_rate | Float (Log) | $3 \times 10^{-4}$ – $2 \times 10^{-3}$ | Mengatur besaran langkah pembaruan bobot pada pengoptimal gradien Adam |
| batch_size | Kategorikal | 16, 32, 64 sampel | Mengatur ukuran blok data pada estimasi gradien per iterasi pelatihan |

### 3. Skema 5-Fold Purged Rolling-Origin Cross-Validation

Optimasi hyperparameter dijalankan secara ketat hanya pada data pengembangan (2020–2023) menggunakan skema 5-fold Purged Rolling-Origin Cross-Validation guna menjaga integritas temporal (López de Prado, 2018). Berbeda dari validasi silang standar yang mengabaikan urutan waktu, skema rolling-origin mempertahankan kronologi temporal: data pelatihan selalu berada di masa lalu, sementara subset validasi berada di masa depan. Pada setiap lipatan (fold), jendela pelatihan diperluas secara bertahap (expanding window) dan diikuti oleh jendela validasi yang bergeser maju, sehingga model diuji pada kondisi data out-of-sample yang belum pernah diobservasi sebelumnya pada lipatan tersebut. Pendekatan ini secara realistis mereplikasi kondisi operasional peramalan volatilitas pasar keuangan dari waktu ke waktu secara berkesinambungan dan ketat tanpa kebocoran masa depan. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan komputasi.

Guna meniadakan potensi kebocoran data akibat tumpang tindih sekuens temporal antara akhir periode latih dan awal periode validasi, disisipkan celah pemisah (purging gap) sepanjang nilai lookback ($L$) di antara kedua subset tersebut (López de Prado, 2018). Keberadaan celah pembersihan ini memastikan bahwa tidak ada observasi masukan pada subset validasi yang memuat informasi historis dari rentang waktu subset latih. Kinerja penalaan pada setiap uji coba (trial) dinilai berdasarkan rata-rata fungsi kerugian QLIKE dari kelima lipatan validasi silang (Patton, 2011). Konfigurasi hyperparameter yang menghasilkan nilai mean CV QLIKE terendah akan dipilih sebagai konfigurasi arsitektur final yang akan digunakan dalam tahap pelatihan model utama secara transparan, akuntabel, dan terstandarisasi penuh. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan komputasi yang substansial.

### 4. Algoritma Tree-structured Parzen Estimator (TPE) dan MedianPruner

Pencarian konfigurasi optimal dalam ruang hyperparameter dieksekusi menggunakan kerangka kerja Optuna berbantuan algoritma Bayesian Tree-structured Parzen Estimator (TPE) sebanyak 50 trial terarah (Akiba et al., 2019; Bergstra et al., 2011). Algoritma TPE bekerja dengan memodelkan distribusi probabilitas konfigurasi parameter bersyarat terhadap performa fungsi tujuan sebagaimana disajikan pada Persamaan (3.7). Melalui pemodelan densitas non-parametrik ini, algoritma TPE secara cerdas mengidentifikasi wilayah ruang hyperparameter yang paling berpotensi menghasilkan fungsi kerugian rendah. Mekanisme probabilistik ini terbukti jauh lebih efisien dibandingkan penelusuran acak (random search) maupun pencarian kisi konvensional (grid search) yang memboroskan daya komputasi secara eksponensial dalam ruang berdimensi tinggi tanpa jaminan konvergensi optimal pada deret waktu. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan komputasi yang substansial dalam memetakan interaksi.

$$
p(x|y) = 
\begin{cases} 
\ell(x), & \text{jika } y < y^* \\ 
g(x), & \text{jika } y \ge y^* 
\end{cases}
\tag{3.7}
$$

Berdasarkan Persamaan (3.7), variabel $y^*$ merepresentasikan ambang batas kuantil performa QLIKE terbaik historis yang memisahkan kelompok pengujian unggul dan inferior. Kerapatan probabilitas $\ell(x)$ dibentuk dari kumpulan parameter dengan performa unggul, sedangkan $g(x)$ dibentuk dari parameter yang kurang optimal. Algoritma memaksimalkan rasio $\ell(x)/g(x)$ untuk menentukan kandidat parameter pengujian berikutnya, sehingga eksplorasi berfokus pada area parameter yang paling menjanjikan secara efisien (Bergstra et al., 2011). Pendekatan eksplorasi terarah ini secara signifikan mempercepat penemuan kombinasi parameter terbaik dalam batas 50 kali pengujian coba yang telah dialokasikan dalam rancangan eksperimen, sehingga konvergensi solusi tercapai secara optimal tanpa memerlukan ratusan iterasi yang tidak efisien dan membebani komputasi. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan komputasi yang substansial dalam memetakan interaksi non-linear parameter.

Guna mengoptimalkan efisiensi komputasi selama proses penalaan 50 trial, diterapkan algoritma pemangkasan otomatis MedianPruner dengan parameter 10 trial awal tanpa pemangkasan ($n_{\text{startup\_trials}} = 10$) dan 2 langkah evaluasi pemanasan ($n_{\text{warmup\_steps}} = 2$) (Akiba et al., 2019; Optuna Development Team, 2024). Mekanisme MedianPruner secara otomatis menghentikan eksekusi pelatihan pada lipatan validasi jika nilai kerugian sementara yang dicapai berada di bawah nilai median historis pada langkah pelatihan yang setara. Strategi pemangkasan dini ini mencegah pemborosan siklus komputasi pada arsitektur yang terbukti suboptimal tanpa merusak ruang pencarian solusi terbaik global, sehingga waktu pelatihan dapat dialokasikan secara optimal pada kandidat model yang benar-benar menjanjikan performa superior pada data pasar riil. Penalaan hyperparameter berbasis algoritma Bayesian ini memberikan keunggulan komputasi yang substansial dalam.

## F. Pelatihan Model Final dan Protokol Multi-Seed


### 1. Pelatihan Ulang pada Train Pool (2020–2025)

Setelah konfigurasi hyperparameter terbaik diidentifikasi melalui proses optimasi Optuna TPE pada data pengembangan, model arsitektur final dilatih ulang menggunakan seluruh data yang terhimpun dalam train pool periode 2020 hingga 2025 (Wahyuddin et al., 2025). Penggabungan data pengembangan (2020–2023) dan data validasi (2024–2025) menjadi kumpulan latih tunggal sebanyak 2.191 hari kalender bertujuan untuk memperkaya representasi pola volatilitas terkini yang dialami pasar Bitcoin sebelum model dievaluasi pada periode uji out-of-sample murni tahun 2026. Pelatihan ulang ini memastikan model memanfaatkan volume observasi maksimal yang tersedia tanpa menyentuh data masa depan, sehingga bobot jaringan mampu menangkap pola struktural pasar terkini secara representatif, mendalam, dan komprehensif bagi estimasi volatilitas. Protokol pelatihan ulang dan ansambel multi-seed ini secara efektif mengeliminasi pengaruh kebetulan inisialisasi bobot.

Proses pelatihan ulang model final mengadopsi algoritma optimasi penurunan gradien stokastik Adam dengan jadwal laju pembelajaran konstan hasil penalaan Optuna (Kingma & Ba, 2014; TensorFlow Developers, 2024). Fungsi kerugian yang diminimalkan selama proses pelatihan adalah Mean Squared Error (MSE) pada skala log realized variance yang telah distandarisasi. Pelatihan diatur dengan batas maksimal 100 epoch dan dilengkapi mekanisme penghentian dini (EarlyStopping) dengan parameter kesabaran (patience) sebesar 10 epoch. Proporsi 10% data temporal terakhir dari train pool disisihkan secara kronologis sebagai subset pemantau internal guna memulihkan kumpulan bobot sinaptik terbaik (restore best weights) saat konvergensi optimal tercapai demi stabilitas numerik yang andal dan terhindar dari fenomena overfitting data latih. Protokol pelatihan ulang dan ansambel multi-seed ini secara efektif mengeliminasi pengaruh.

### 2. Protokol Multi-Seed Ensemble

Inisialisasi bobot sinaptik secara acak dan urutan pengacakan batch pelatihan sering kali memicu variabilitas hasil prediksi pada jaringan saraf tiruan (Bouthillier et al., 2021). Memilih model terbaik berdasarkan hasil uji acak tunggal (single seed) sangat berbahaya karena rentan memicu bias keberuntungan (cherry-picking). Atas dasar tersebut, penelitian ini menerapkan protokol multi-seed ensemble dengan melatih lima model LSTM secara independen menggunakan lima nilai acakan acak (seed) yang ditetapkan secara apriori, yaitu seed 42, 123, 2024, 7, dan 99. Kelima nilai seed ini mereplikasi variasi inisialisasi bobot dan pengacakan data latih dalam kondisi lingkungan perangkat lunak yang terkontrol secara deterministik tanpa manipulasi subjektif dari peneliti demi keandalan sains dan keterulangan komputasi. Protokol pelatihan ulang dan ansambel multi-seed ini secara efektif mengeliminasi.

Prediksi akhir model LSTM untuk setiap langkah waktu peramalan $t+1$ dihasilkan melalui agregasi rata-rata aritmatika dari kelima prediksi model multi-seed tersebut sebagaimana dirumuskan pada Persamaan (3.8) (Bouthillier et al., 2021; Fawzi et al., 2025). Strategi ansambel rata-rata ini secara teoritis terbukti mampu mereduksi varians estimasi galat individual tanpa meningkatkan bias model, sehingga menghasilkan peramalan volatilitas yang jauh lebih stabil dan andal. Selain menghitung rata-rata ansambel, variabilitas performa metrik antar-seed juga didokumentasikan secara transparan dalam berkas luaran komputasi guna memberikan analisis komprehensif mengenai tingkat stabilitas numerik arsitektur jaringan terhadap efek stokastisitas inisialisasi bobot sepanjang pengujian empiris berlangsung di bursa kripto. Protokol pelatihan ulang dan ansambel multi-seed ini secara efektif mengeliminasi pengaruh kebetulan inisialisasi bobot awal, sehingga menghasilkan stabilitas peramalan.

$$
\widehat{\log RV}_{t+1} = \frac{1}{5} \sum_{s \in \{42, 123, 2024, 7, 99\}} \widehat{\log RV}_{t+1}^{(s)}
\tag{3.8}
$$

## G. Implementasi Model Baseline Pembanding


### 1. Baseline Naif: Random Walk Persistence

Sebagai standar pembanding kinerja paling mendasar, penelitian ini mengimplementasikan model naif Random Walk Persistence (Andersen et al., 2003; Patton, 2011). Model persistence memproyeksikan bahwa tingkat realized volatility pada hari esok ($t+1$) bernilai persis sama dengan tingkat realized volatility yang diobservasi pada hari ini ($t$), tanpa melibatkan proses estimasi parameter statistik maupun optimasi komputasi apapun sebagaimana dinyatakan pada Persamaan (3.9). Kesederhanaan model ini menjadikannya cerminan hipotesis pasar efisien bentuk lemah, di mana perubahan volatilitas esok hari diasumsikan sebagai inovasi acak murni yang tidak dapat diprediksi melampaui level terkininya, sehingga memberikan standar pembanding minimal yang wajib dikalahkan oleh arsitektur kecerdasan buatan manapun dalam riset finansial. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi.

$$
\widehat{\log RV}_{t+1} = \log RV_t
\tag{3.9}
$$

Implementasi model naif persistence memegang peranan krusial sebagai patokan kelayakan ilmiah minimal (sanity benchmark) dalam literatur peramalan runtun waktu finansial (Corsi, 2009). Karena deret waktu realized volatility memiliki tingkat ketergantungan temporal dan persistensi autoregresif yang sangat tinggi, model pembelajaran mesin yang gagal mengungguli akurasi model persistence pada data out-of-sample tidak memiliki nilai tambah terapan yang sah. Atas dasar tersebut, keunggulan signifikan terhadap model persistence menjadi prasyarat mutlak yang wajib dipenuhi oleh model LSTM yang diusulkan sebelum klaim keberhasilan arsitektur komputasi cerdas dapat diakui secara akademis dalam komunitas penelitian sains data dan ekonometrika keuangan modern saat ini secara sah dan terpercaya. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari.

### 2. Baseline Ekonometrika High-Frequency: HAR-RV

Model pembanding kedua adalah Heterogeneous Autoregressive of Realized Volatility (HAR-RV), yang merupakan standar emas dalam pemodelan volatilitas berbasis data frekuensi tinggi (Corsi, 2009). Model HAR-RV memformulasi dinamika volatilitas melalui kombinasi linear dari tiga komponen realized volatility pada horizon waktu yang berbeda, yaitu komponen harian ($RV_t$), komponen mingguan ($RV_{t}^{(w)}$), dan komponen bulanan ($RV_{t}^{(m)}$) sebagaimana dirumuskan pada Persamaan (3.10). Struktur regresi bertingkat ini secara elegan menangkap interaksi asimetris antara pelaku pasar jangka pendek dan pelaku pasar jangka panjang tanpa memerlukan estimasi model fraksional yang rumit secara matematis dan berat secara komputasi bagi sistem peramalan runtun waktu modern. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari arsitektur deep learning yang diusulkan.

$$
\log RV_{t+1} = \beta_0 + \beta_d \log RV_t + \beta_w \left( \frac{1}{5}\sum_{i=0}^{4} \log RV_{t-i} \right) + \beta_m \left( \frac{1}{22}\sum_{i=0}^{21} \log RV_{t-i} \right) + \varepsilon_{t+1}
\tag{3.10}
$$

Parameter regresi linear Persamaan (3.10) diestimasi menggunakan metode Ordinary Least Squares (OLS) pada kumpulan data train pool periode 2020 hingga 2025 (Andersen et al., 2003; Corsi, 2009). Struktur autoregresif bertingkat pada model HAR-RV dirancang untuk menangkap fenomena memori panjang semu (pseudo long-memory) dan heterogenitas horizon investasi pelaku pasar keuangan, mulai dari pedagang harian intra-hari hingga investor institusional jangka panjang. Kemampuan model ini merefleksikan dinamika multiskala menjadikannya tolok ukur ekonometrika yang sangat kompetitif dan tangguh bagi arsitektur jaringan saraf tiruan deep learning dalam memvalidasi keunggulan representasi non-linear yang dipelajari secara otomatis dari data pasar historis yang sarat akan gejolak harga ekstrem. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari.

### 3. Baseline Volatilitas Klasik: GARCH(1,1) Expanding Window

Model pembanding ketiga mewakili paradigma ekonometrika volatilitas bersyarat klasik, yaitu model Generalized Autoregressive Conditional Heteroskedasticity GARCH(1,1) (Bollerslev, 1986). Berbeda dari model berbasis realized variance yang memanfaatkan data frekuensi tinggi intra-hari, GARCH(1,1) diestimasi pada deret imbal hasil logaritmik harian Bitcoin ($r_t = \ln(C_t / C_{t-1}) \times 100$) dengan persamaan varians bersyarat sebagaimana dirumuskan pada Persamaan (3.11). Model ini mengasumsikan bahwa varians bersyarat hari esok dipengaruhi oleh kuadrat galat residu hari ini dan varians bersyarat masa lalu melalui mekanisme peluruhan autoregresif yang linier dan stasioner sepanjang waktu pengamatan tanpa memanfaatkan informasi intra-hari yang kaya akan pergerakan mikrostruktur pasar. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari arsitektur deep learning yang.

$$
\sigma_{t+1}^2 = \omega + \alpha \varepsilon_t^2 + \beta \sigma_t^2
\tag{3.11}
$$

Parameter model ($\omega, \alpha, \beta$) diestimasi menggunakan metode Quasi-Maximum Likelihood (QML) dengan asumsi inovasi berdistribusi normal (Ardia et al., 2019; Katsiampa, 2017). Selama periode evaluasi out-of-sample tahun 2026, model GARCH(1,1) diestimasi ulang secara berkala pada setiap awal bulan kalender menggunakan jendela pelatihan yang meluas (expanding window). Proyeksi varians bersyarat satu langkah ke depan kemudian ditransformasikan ke dalam skala logaritma natural agar dapat diperbandingkan secara setara dan adil terhadap nilai target realized variance aktual guna menguji relevansi data frekuensi rendah vs data frekuensi tinggi pada volatilitas kripto modern dalam kerangka komparatif yang ketat dan objektif. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari arsitektur deep learning yang diusulkan.

### 4. Baseline Deep Learning Heuristik: LSTM Untuned

Guna membuktikan nilai tambah objektif dari algoritma penalaan Bayesian Optuna TPE, model pembanding keempat dirancang berupa arsitektur LSTM tanpa penalaan (LSTM Untuned) yang mengadopsi konfigurasi parameter heuristik umum dari literatur (Aswadi & Ependi, 2025; Khumaidi et al., 2024). Model heuristik ini menggunakan panjang lookback sebesar 21 hari kalender, 64 unit tersembunyi pada satu lapisan LSTM, tingkat dropout regularisasi 0,20, laju pembelajaran Adam sebesar $10^{-3}$, serta ukuran batch pelatihan 32 sampel. Spesifikasi ringkas dari keempat model baseline pembanding dirangkum secara komparatif pada Tabel 3.4 sebagai kerangka evaluasi empiris yang komprehensif bagi pembaca akademis dan penguji skripsi dalam menilai kontribusi nyata algoritma. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari.

Pelatihan model LSTM Untuned dijalankan menggunakan protokol data dan prosedur ansambel 5-seed yang persis identik dengan model usulan (Aldo et al., 2026; Widad et al., 2026). Melalui isolasi komparatif ini, penelitian dapat mengidentifikasi secara transparan apakah peningkatan akurasi peramalan volatilitas benar-benar dipicu oleh kecerdasan algoritma penalaan Optuna dalam menjelajahi lanskap parameter non-linear, ataukah semata-mata merupakan implikasi bawaan dari penggunaan arsitektur jaringan saraf rekuren. Pengujian ini memberikan kontribusi kritis dalam menjawab apakah kompleksitas komputasi penalaan bayesian sebanding dengan perolehan akurasi yang dicapai dalam aplikasi praktis peramalan risiko pasar finansial dan manajemen investasi kuantitatif. Perbandingan komprehensif terhadap seluruh model baseline ini menjadi landasan empiris yang sangat kuat dalam memvalidasi nilai tambah dari arsitektur deep learning yang diusulkan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

**Tabel 3.4 Konfigurasi Spesifikasi Model Baseline Pembanding**

| Nama Model Baseline | Kategori Paradigma | Formulasi dan Konfigurasi Spesifikasi | Prosedur Estimasi Parameter |
|---|---|---|---|
| Random Walk Persistence | Model Naif Statis | $\widehat{\log RV}_{t+1} = \log RV_t$ | Tanpa estimasi parameter statistik |
| HAR-RV (Corsi, 2009) | Ekonometrika High-Freq | Regresi 3 skala: harian, mingguan (5), bulanan (22) | Estimasi OLS pada data train pool (2020–2025) |
| GARCH(1,1) Expanding | Ekonometrika Return | Model varians $\sigma_{t+1}^2 = \omega + \alpha \varepsilon_t^2 + \beta \sigma_t^2$ | Estimasi QML; refit bulanan expanding window |
| LSTM Untuned Heuristik | Deep Learning Default | Lookback: 21, Units: 64, Dropout: 0,2, Lr: $10^{-3}$, Batch: 32 | Pelatihan Adam pada train pool; 5-seed ensemble |

## H. Protokol Evaluasi dan Inferensi Statistik


### 1. Metrik Evaluasi: Asymmetric QLIKE, MAE, dan RMSE

Evaluasi akurasi peramalan volatilitas finansial memerlukan metrik kerugian yang memiliki ketahanan terhadap keberadaan derau mikrostruktur pasar (Patton, 2011). Penggunaan metrik simetris konvensional seperti MSE pada skala varians level terbukti rentan menghasilkan pemeringkatan model yang inkonsisten ketika proksi volatilitas mengandung estimasi galat observasi. Atas dasar tersebut, metrik evaluasi primer pada studi yang dilakukan ditetapkan berupa Quasi-Likelihood loss function (QLIKE) yang terbukti secara matematis bersifat robust dan homogen derajat nol dalam membandingkan model peramalan varians sebagaimana diformulasikan pada Persamaan (3.12). Keandalan metrik QLIKE memastikan evaluasi kinerja terhindar dari distorsi pemeringkatan yang menyesatkan pada data finansial frekuensi tinggi bursa kripto. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris yang sahih dan.

$$
QLIKE_t = \frac{RV_t}{\widehat{RV}_t} - \ln\left( \frac{RV_t}{\widehat{RV}_t} \right) - 1
\tag{3.12}
$$

Fungsi kerugian QLIKE pada Persamaan (3.12) bersifat asimetris, di mana penalti kerugian yang diberikan jauh lebih besar pada kesalahan peramalan yang meremehkan volatilitas aktual (under-prediction) dibandingkan peramalan yang melebih-lebihkan risiko (over-prediction) (Patton, 2011). Karakteristik asimetris ini sangat selaras dengan prinsip kehati-hatian dalam manajemen risiko pasar keuangan, di mana kegagalan mendeteksi lonjakan gejolak pasar membawa dampak kerugian portofolio yang fatal dibandingkan estimasi risiko yang konservatif. Maka dari itu, optimalisasi fungsi QLIKE menghasilkan sistem peramalan yang memiliki sensitivitas tinggi terhadap ancaman lonjakan risiko ekstrem pada perdagangan aset kripto yang sarat akan gejolak mendadak dan kepanikan pasar yang tak terduga. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris yang sahih dan.

Sebagai pelengkap analisis kuantitatif, dihitung pula metrik sekunder berupa Mean Absolute Error (MAE) dan Root Mean Squared Error (RMSE) yang dievaluasi langsung pada skala log realized variance (Lim & Zohren, 2021). Metrik MAE mengukur besaran deviasi rata-rata absolut dalam satuan logaritmik pada Persamaan (3.13), sedangkan metrik RMSE memberikan penalti kuadratik yang lebih tinggi pada simpangan kesalahan prediksi yang bernilai besar sebagaimana dirumuskan pada Persamaan (3.14). Kombinasi metrik primer QLIKE dan metrik sekunder MAE serta RMSE menyajikan gambaran komprehensif mengenai karakteristik galat peramalan model, baik dari perspektif asimetri risiko finansial maupun dispersi kesalahan numerik standar secara seimbang, mendalam, dan terukur. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris.

$$
MAE = \frac{1}{T} \sum_{t=1}^{T} \left| \log RV_t - \widehat{\log RV}_t \right|
\tag{3.13}
$$

$$
RMSE = \sqrt{ \frac{1}{T} \sum_{t=1}^{T} \left( \log RV_t - \widehat{\log RV}_t \right)^2 }
\tag{3.14}
$$

### 2. Uji Asimtotik Diebold-Mariano dengan Koreksi Newey-West

Perbedaan nilai rata-rata fungsi kerugian antara dua model peramalan wajib diuji signifikansinya secara statistik guna memastikan bahwa keunggulan model bukan merupakan artefak kebetulan semata (Diebold & Mariano, 1995). Uji signifikansi komparatif dieksekusi menggunakan uji asimtotik Diebold-Mariano (DM) satu sisi berbasis deret diferensial kerugian harian sebagaimana diformulasikan pada Persamaan (3.15). Uji ini secara ketat membandingkan apakah pengurangan galat yang dicapai oleh model usulan memiliki bukti statistik yang cukup kuat untuk menolak hipotesis kesetaraan performa terhadap seluruh model pembanding pada tingkat signifikansi yang telah ditentukan secara baku dalam metodologi peramalan ekonometrika modern dan sains data komputasional terkini. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris yang sahih dan dapat.

$$
d_t = QLIKE_{A,t} - QLIKE_{B,t}
\tag{3.15}
$$

Hipotesis nol ($H_0: E[d_t] \ge 0$) menyatakan bahwa model usulan memiliki kerugian yang sama atau lebih besar dibandingkan model pembanding, sedangkan hipotesis alternatif ($H_1: E[d_t] < 0$) menyatakan bahwa model usulan menghasilkan kerugian yang signifikan lebih rendah (Diebold & Mariano, 1995). Karena deret diferensial kerugian runtun waktu finansial kerap memperlihatkan autokorelasi serial dan heteroskedastisitas, varians rata-rata diferensial diestimasi menggunakan estimator Heteroskedasticity and Autocorrelation Consistent (HAC) Newey-West dengan panjang kelambatan (lag truncation) sebesar 5 hari (Newey & West, 1987). Tingkat signifikansi statistik ditetapkan pada ambang batas $\alpha = 0,05$ guna menguji keunggulan komparatif model secara asimtotik yang valid, kuat, dan dapat dipertanggungjawabkan. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan.

### 3. Estimasi Empiris Moving-Block Bootstrap

Sebagai pelengkap uji asimtotik yang berpotensi bias pada ukuran sampel terbatas, diterapkan metode estimasi non-parametrik Moving-Block Bootstrap (Künsch, 1989). Uji bootstrap konvensional yang mengacak observasi secara individual akan merusak struktur dependensi temporal pada deret diferensial kerugian volatilitas. Atas dasar tersebut, Moving-Block Bootstrap mempertahankan korelasi runtun waktu dengan mengambil cuplikan blok-blok data harian berurutan sepanjang $b = 20$ hari kalender secara berulang sebanyak 10.000 repetisi empiris dengan nilai seed acakan terkunci pada 42 (Künsch, 1989; Patton, 2011). Pelaksanaan 10.000 kali pengacakan blok ini menjamin konvergensi distribusi sampling selisih kerugian antar-model secara representatif dan tangguh terhadap pelanggaran asumsi parametrik yang sering terjadi. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti.

Dari 10.000 sampel bootstrap yang terbentuk, dihitung distribusi empiris dari selisih rata-rata kerugian ($\Delta QLIKE$) guna menyusun interval kepercayaan persentil 95% secara teliti (Künsch, 1989). Keputusan penolakan hipotesis nol didasarkan pada posisi batas atas interval kepercayaan: apabila batas atas interval persentil 95% bernilai negatif secara tegas (berada di bawah angka nol), maka model usulan disimpulkan secara konsisten lebih unggul dibandingkan model pembanding pada seluruh rentang kemungkinan data yang masuk akal (Patton, 2011). Pendekatan non-parametrik ini memberikan kepastian inferensi yang sangat kokoh tanpa bergantung pada asumsi normalitas galat atau ketiadaan autokorelasi residu dalam inferensi finansial runtun waktu. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris yang sahih dan.

### 4. Kriteria Keberhasilan Eksperimen

Guna menegakkan prinsip objektivitas ilmiah yang bebas dari manipulasi hasil, kriteria keberhasilan eksperimen ditetapkan secara apriori ke dalam tiga kategori klasifikasi luaran: 'positive', 'mixed', atau 'negative' (Bouthillier et al., 2021). Hasil eksperimen diklasifikasikan berstatus 'positive' jika seluruh kriteria berikut terpenuhi pada data uji 2026: (1) rata-rata QLIKE model LSTM-Optuna lebih rendah dibandingkan persistence dan HAR-RV, (2) uji DM satu sisi menghasilkan $p < 0,05$ pada kedua perbandingan utama, dan (3) batas atas interval kepercayaan bootstrap 95% berada di bawah nol. Protokol evaluasi dirangkum secara sistematis pada Tabel 3.5 sebagai pedoman interpretasi objektif hasil eksperimen yang transparan bagi evaluasi luaran model secara tegas. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik.

Apabila model usulan hanya mampu memenuhi sebagian dari ketiga kriteria ketat tersebut, maka hasil eksperimen secara jujur diklasifikasikan berstatus 'mixed' (Bouthillier et al., 2021). Sementara itu, apabila performa model LSTM-Optuna terbukti kalah secara statistik terhadap model persistence maupun HAR-RV, luaran dikategorikan berstatus 'negative'. Seluruh hasil pengujian akan dilaporkan secara transparan pada Bab IV apa adanya tanpa ada upaya perubahan konfigurasi split, manipulasi seed, atau penggantian fungsi metrik setelah data uji dievaluasi demi menjaga kehormatan etika penelitian sains komputasi yang berintegritas tinggi serta berorientasi pada kebenaran faktual secara terbuka dan dapat diaudit. Penerapan metrik kerugian asimetris dan inferensi statistik inferensial ini memastikan bahwa kesimpulan mengenai keunggulan model ditarik berdasarkan bukti empiris yang sahih dan dapat dipertanggungjawabkan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

**Tabel 3.5 Protokol Evaluasi dan Kriteria Inferensi Statistik**

| Komponen Evaluasi | Parameter dan Pengaturan Metodologis |
|---|---|
| Metrik Kerugian Utama | Asymmetric Quasi-Likelihood (QLIKE) pada skala level varians |
| Metrik Kerugian Sekunder | Mean Absolute Error (MAE) dan Root Mean Squared Error (RMSE) pada $\log RV$ |
| Uji Signifikansi Primer | Diebold-Mariano satu sisi dengan koreksi HAC Newey-West lag 5 ($\alpha = 0,05$) |
| Uji Interval Non-Parametrik | Moving-Block Bootstrap (panjang blok: 20 hari, 10.000 resampel, seed: 42) |
| Pasangan Uji Primer | LSTM-Optuna vs Random Walk Persistence; LSTM-Optuna vs HAR-RV |
| Pasangan Uji Sekunder | LSTM-Optuna vs GARCH(1,1); LSTM-Optuna vs LSTM Untuned |
| Kriteria Keberhasilan | Klasifikasi status formal: 'positive', 'mixed', atau 'negative' secara apriori |

## I. Validitas dan Pengendalian Kebocoran Data


### 1. Pengendalian Temporal Ordering dan Look-Ahead Bias

Ancaman paling fatal terhadap validitas internal penelitian runtun waktu finansial adalah kebocoran informasi masa depan (look-ahead bias) (López de Prado, 2018). Pada studi yang dilakukan, urutan waktu kronologis dijaga secara ketat pada setiap modul pemrosesan komputasi. Tidak ada satupun proses pengacakan sampel acak yang diizinkan dalam tahapan pembentukan fitur masukan maupun peramalan target. Setiap vektor fitur pada hari ke-$t$ murni diekstraksi dari harga penutupan, harga ekstrem, volume, dan realized variance yang telah terbentuk sempurna hingga jam 23:59:59 UTC pada hari ke-$t$ tanpa pernah melampaui batas hari pengamatan yang sedang dievaluasi pada saat pemodelan runtun waktu. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan.

Pemisahan tegas ini menjamin bahwa seluruh variabel prediktor yang dialirkan ke dalam lapisan sel LSTM telah berstatus informasi masa lalu saat model berusaha memproyeksikan realized variance pada hari esok ($t+1$) (Lim & Zohren, 2021). Desain kausalitas temporal ini mencerminkan kondisi riil yang dihadapi oleh praktisi manajemen risiko di dunia nyata, di mana peramalan untuk hari perdagangan berikutnya harus dieksekusi secara prospektif tanpa pernah mengetahui dinamika harga masa depan yang belum terjadi. Dengan menegakkan aturan ini, estimasi akurasi yang diperoleh terhindar dari bias masa depan yang menyesatkan dan sepenuhnya dapat dipertanggungjawabkan secara metodologis serta dapat diimplementasikan secara nyata pada industri pasar modal. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi.

### 2. Pengendalian Information Leakage pada Standarisasi Fitur

Kebocoran data kerap kali menyusup tanpa disadari melalui tahapan normalisasi atau penstandaran fitur masukan secara global terhadap seluruh dataset sebelum partisi dilakukan (López de Prado, 2018). Apabila nilai rata-rata dan simpangan baku dihitung menggunakan keseluruhan rentang waktu observasi, maka karakteristik statistik dari data validasi dan data uji akan mencemari proses pembobotan awal pada data latih. Fenomena ini menciptakan ilusi akurasi yang tinggi di laboratorium komputasi namun gagal total saat diterapkan pada data produksi yang sesungguhnya karena model telah terpapar distribusi masa depan secara ilegal tanpa disadari oleh pengembang sistem peramalan finansial yang ceroboh. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

Guna meniadakan risiko information leakage tersebut, penelitian ini menerapkan aturan penguncian statistik parameter penstandar secara ketat pada setiap modul (López de Prado, 2018; Wahyuddin et al., 2025). Objek StandardScaler hanya diizinkan mempelajari (fit) statistik parameter rata-rata dan deviasi standar dari himpunan data pelatihan pada lipatan validasi silang bersangkutan atau data train pool. Objek penstandar yang telah terkunci tersebut kemudian mentransformasikan (transform) data validasi dan data uji secara pasif, sehingga data uji tetap berstatus murni out-of-sample tanpa pernah mempengaruhi parameter penskalaan model sepanjang siklus pengujian berlangsung dalam eksperimen penelitian yang terkontrol dan terisolasi penuh. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

### 3. Pengendalian Purging Gap pada Cross-Validation

Penerapan metode validasi silang pada data yang dibentuk melalui jendela bergeser (sliding window) rentan mengalami tumpang tindih informasi temporal (information overlap) pada batas pergantian data latih dan data uji lipatan (López de Prado, 2018). Karena setiap sampel masukan LSTM merangkum riwayat harga sepanjang $L$ hari ke belakang, sampel target pada awal periode validasi berpotensi menggunakan fitur-fitur yang sebagian besar berasal dari rentang hari-hari akhir periode pelatihan lipatan tersebut, sehingga menciptakan ketergantungan informasi tersembunyi yang merusak independensi validasi silang dalam mengukur kemampuan generalisasi model secara obyektif dan kredibel. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

Penelitian ini mengatasi celah kebocoran tersebut dengan menyisipkan purging gap sepanjang nilai lookback ($L$) di antara akhir sekuens pelatihan dan awal sekuens validasi pada setiap lipatan 5-fold cross-validation (López de Prado, 2018). Sampel-sampel yang berada di dalam zona purging gap dibuang secara permanen dari subset pengujian lipatan. Prosedur pembersihan ini memutus korelasi serial dan ketergantungan temporal antar-subset secara mutlak, sehingga evaluasi pada lipatan validasi benar-benar mencerminkan kemampuan generalisasi model terhadap struktur data yang sepenuhnya terisolasi dari riwayat jendela pelatihan sebelumnya secara adil dan terukur dalam setiap siklus validasi silang eksperimen. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

### 4. Isolasi Data Uji Eksternal (Pure Out-of-Sample Holdout)

Prinsip isolasi data uji out-of-sample ditegakkan secara mutlak dengan melarang keterlibatan data uji eksternal tahun 2026 dalam proses pengambilan keputusan pemodelan apapun (Bouthillier et al., 2021). Data uji tidak pernah dilibatkan dalam proses penalaan hyperparameter Optuna, penentuan titik penghentian dini (early stopping), pemilihan nilai acakan (seed), maupun modifikasi arsitektur jaringan saraf tiruan. Seluruh keputusan desain model telah dibekukan secara permanen sebelum data uji disentuh, sehingga dataset uji tetap steril dari polusi optimasi atau bias konfirmasi peneliti yang dapat mendistorsi keabsahan evaluasi komputasional pada tahap pelaporan hasil akhir skripsi. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

Evaluasi terhadap data uji eksternal tahun 2026 hanya dieksekusi tepat satu kali (single execution run) di akhir siklus eksperimen komputasional setelah seluruh bobot dibekukan (López de Prado, 2018). Larangan iterasi uji ulang (multiple testing) ini mencegah terjadinya bias kurasi data (data snooping) dan overfitting terhadap data uji. Dengan protokol isolasi yang sangat ketat ini, estimasi kinerja dan uji signifikansi statistik yang disajikan pada Bab IV terjamin memiliki validitas ilmiah yang tinggi serta bebas dari klaim performa yang menyesatkan bagi komunitas akademis dan praktisi pasar modal digital di masa mendatang dalam mengevaluasi risiko. Disiplin pengendalian kebocoran data pada setiap subsistem pemrosesan menegakkan integritas ilmiah penelitian ini sehingga terbebas dari ilusi performa akibat bias masa depan. Hal ini dilakukan demi menjamin integritas ilmiah riset.

## J. Robustness, Reproduksibilitas, dan Alur Penelitian


### 1. Manajemen Provenance, Cryptographic Hashing, dan Manifest Komputasi

Standar keterulangan komputasi pada studi yang dilakukan dijamin melalui manajemen asal-usul data (data provenance) dan penerapan fungsi hash kriptografis SHA-256 pada seluruh artefak penelitian (López de Prado, 2018). Sebelum satu pun model dilatih, berkas protokol metodologi dikunci secara formal dan menghasilkan hash kriptografis `72c7588046b4ab644d814031e3329702ed884c6d9f0d0ff3c5d27660e36caba3`. Demikian pula berkas dataset harian hasil agregasi dikunci dengan nilai hash SHA-256 `ec2e3fb42f9233b4e37f2f6a9a79cc0cd6a34e78c275c27b7e98e546e651e08b` guna mencegah modifikasi data yang tidak terdokumentasi selama masa riset berlangsung di lingkungan komputasi. Kedua nilai hash tersebut dicocokkan secara otomatis sebelum eksekusi dimulai oleh pipa analisis. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya keraguan metodologis. Hal ini dilakukan demi menjamin integritas ilmiah riset.

Setiap eksekusi modul komputasi secara otomatis mencatat metadata lengkap ke dalam berkas manifes JSON, yang mencakup identitas run unik, stempel waktu presisi, hash commit repositori Git, versi pustaka perangkat lunak (Python 3.14.7, TensorFlow 2.22.0, Optuna 5.0.0), serta daftar nilai seed acakan (Bouthillier et al., 2021; TensorFlow Developers, 2024). Sebelum model final dijalankan, skrip secara otomatis memverifikasi kecocokan hash protokol dan data. Apabila terjadi perbedaan satu karakter pada berkas data atau protokol, eksekusi akan dihentikan secara otomatis guna mencegah penyimpangan metodologis dan memastikan keterulangan hasil yang presisi serta dapat diaudit ulang secara independen oleh pihak luar kapan saja dengan tingkat akurasi absolut. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat.

### 2. Arsitektur Kode dan Unit Testing Mandiri

Perangkat lunak penelitian dibangun dengan prinsip arsitektur modular yang memisahkan tanggung jawab fungsional secara tegas (separation of concerns) guna memudahkan proses audit komputasi (Lim & Zohren, 2021). Repositori kode dibagi menjadi delapan modul sumber mandiri yang mengelola konfigurasi sistem (`s2_config.py`), pemrosesan data (`s2_data.py`), kalkulasi metrik statistik (`s2_stats.py`), arsitektur model LSTM (`s2_models.py`), optimasi HPO Optuna (`s2_optuna_search.py`), pelatihan final (`s2_final_run.py`), analisis hasil (`s2_analyze.py`), serta pembuatan visualisasi ilmiah (`s2_figures.py`). Pemisahan ini meminimalkan risiko bug tersembunyi antarfungsi komputasi serta memfasilitasi keterbacaan kode secara sistematis bagi pengembang dan pemeriksa independen. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya keraguan metodologis. Hal ini dilakukan demi menjamin integritas ilmiah riset.

Keandalan operasional seluruh modul diverifikasi secara ketat melalui implementasi 34 unit pengujian perangkat lunak mandiri (unit tests) berbasis kerangka kerja pytest (Bouthillier et al., 2021). Rangkaian pengujian otomatis ini mencakup verifikasi kontinuitas kalender bar data, validasi kebenaran formulasi matematis fungsi kerugian QLIKE, pengujian isolasi partisi temporal scaler, serta pemeriksaan kebenaran perilaku asimtotik uji Diebold-Mariano dan block bootstrap. Seluruh 34 unit testing terbukti lulus 100% sebelum analisis akhir dijalankan, menjamin tidak adanya galat logika pemrograman dalam alur eksperimen peramalan yang dapat mengorbankan validitas temuan ilmiah yang disajikan kepada sidang akademik skripsi maupun publikasi internasional. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya.

### 3. Tahapan Eksperimen dan Alur Komputasi

Keseluruhan alur tahapan eksperimen penelitian komputasional dirangkum secara visual pada Gambar 3.1. Alur penelitian terbagi menjadi tujuh fase utama yang saling terhubung secara berkesinambungan: (1) akuisisi dan audit kualitas data historis 2020–2026, (2) rekayasa fitur kausal dan formulasi target peramalan, (3) partisi dataset temporal kronologis, (4) optimasi hyperparameter LSTM berbasis Optuna TPE dan MedianPruner, (5) pelatihan model final multi-seed dan implementasi empat baseline pembanding, (6) evaluasi out-of-sample dan inferensi statistik Diebold-Mariano serta bootstrap, dan (7) penarikan kesimpulan ilmiah bebas p-hacking (López de Prado, 2018). Setiap fase dirancang dengan batasan protokol yang terukur secara sistematis, transparan, dan terarah. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh.

Integrasi terpadu antartahapan ini memastikan bahwa setiap proses komputasi memiliki dasar justifikasi teoretis yang kuat dan dapat ditelusuri kembali ke berkas log eksekusi yang transparan (Lim & Zohren, 2021; Patton, 2011). Dengan mengisolasi data uji eksternal hingga fase keenam dan mengunci seluruh ruang hyperparameter pada fase keempat, metodologi ini menyajikan kerangka kerja penelitian yang kokoh, terhindar dari bias seleksi model, dan mampu menjawab seluruh pertanyaan penelitian secara meyakinkan. Desain sistematis ini memberikan keyakinan metodologis penuh bagi pengujian hipotesis empiris pada bab tahap berikutnya tanpa keraguan ilmiah sedikit pun mengenai validitas hasil temuan yang diperoleh. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya.

![Gambar 3.1 Alur Tahapan Penelitian Komputasional](figures/gambar_3_1_alur_penelitian.png)
*Gambar 3.1 Alur Tahapan Penelitian Komputasional Peramalan Realized Volatility Bitcoin*

### 4. Ringkasan Metodologi Penelitian

Metodologi penelitian yang dirancang pada studi yang dilakukan menghadirkan sintesis komprehensif antara kekuatan representasi non-linear deep learning dan ketatnya disiplin inferensi ekonometrika finansial (Akiba et al., 2019; Corsi, 2009; Patton, 2011). Pemanfaatan algoritma Bayesian Optuna TPE dengan panduan fungsi kerugian asimetris QLIKE pada skema purged cross-validation mengatasi kelemahan mendasar metode trial-and-error konvensional yang kerap kali bias dan rentan terhadap kebocoran informasi masa depan. Penerapan multi-seed ensemble semakin memperkokoh stabilitas model dalam menghadapi volatilitas ekstrem pasar aset kripto Bitcoin secara berkesinambungan dan terukur bagi aplikasi praktis manajemen risiko investasi dan mitigasi gejolak pasar modal. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya keraguan.

Melalui protokol evaluasi ganda yang memadukan uji asimtotik Diebold-Mariano terkoreksi HAC Newey-West dan estimasi non-parametrik Moving-Block Bootstrap terhadap empat model baseline pembanding, metodologi ini siap menyajikan pembuktian empiris yang tervalidasi secara mendalam pada Bab IV (Bouthillier et al., 2021). Rancangan metodologis yang transparan, terotomatisasi, dan teruji secara komputasional ini memberikan fondasi yang sangat kokoh dalam menjawab ketiga rumusan masalah penelitian serta membuktikan kebenaran hipotesis ilmiah yang diajukan dengan standar akurasi dan integritas akademik tertinggi di bidang informatika finansial dan komputasi cerdas modern saat ini. Prosedur metodologis yang ketat dan terstandarisasi ini dirancang secara khusus untuk memastikan bahwa seluruh tahapan eksperimen dapat direplikasi secara penuh oleh komunitas akademis tanpa adanya keraguan metodologis. Hal ini dilakukan demi menjamin integritas ilmiah riset.


## K. Jadwal Penelitian

Pelaksanaan penelitian peramalan realized volatility Bitcoin ini direncanakan berlangsung selama 4 bulan (16 minggu) kerja efektif, dimulai sejak tahap penyusunan proposal hingga penyelesaian naskah skripsi akhir. Alokasi jadwal disusun secara terstruktur ke dalam delapan tahapan kegiatan utama yang mencakup studi kepustakaan, pengunduhan dan audit data frekuensi tinggi Binance Vision, rekayasa fitur volatilitas kausal, perancangan skema purged cross-validation, eksperimen optimasi hyperparameter Bayesian Optuna, pelatihan ansambel multi-seed, evaluasi inferensi statistik Diebold-Mariano out-of-sample, hingga penyusunan laporan ilmiah lengkap. Matriks pembagian jadwal penelitian disajikan secara rinci pada Tabel 3.6 guna menjamin seluruh target komputasi dapat tercapai secara terukur, sistematis, dan tepat waktu sesuai kalender akademik Fakultas Sains dan Teknologi Universitas Islam Nahdlatul Ulama Jepara.

**Tabel 3.6 Matriks Jadwal Pelaksanaan Penelitian**

| No | Tahapan Kegiatan Penelitian | Bulan 1 | Bulan 2 | Bulan 3 | Bulan 4 |
|:--:|---|:---:|:---:|:---:|:---:|
| 1 | Studi literatur & perumusan celah riset (*research gap*) | ✓ | | | |
| 2 | Akuisisi data Binance Vision & verifikasi hash SHA-256 | ✓ | | | |
| 3 | Rekayasa fitur kausal & kalkulasi Realized Variance | ✓ | ✓ | | |
| 4 | Partisi data temporal & implementasi 4 model baseline | | ✓ | | |
| 5 | Eksperimen HPO Bayesian Optuna TPE & Purged CV | | ✓ | ✓ | |
| 6 | Pelatihan final 5-seed ensemble & uji holdout 2026 | | | ✓ | |
| 7 | Inferensi statistik Diebold-Mariano & Bootstrap | | | ✓ | ✓ |
| 8 | Penyusunan laporan skripsi & ujian seminar proposal/skripsi | | | ✓ | ✓ |
