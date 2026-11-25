# PANDUAN SIMULASI TANYA JAWAB UJIAN SEMINAR PROPOSAL (SEMPRO)
**PROGRAM STUDI TEKNIK INFORMATIKA — FAKULTAS SAINS DAN TEKNOLOGI**  
**UNIVERSITAS ISLAM NAHDLATUL ULAMA (UNISNU) JEPARA**

---

### IDENTITAS MAHASISWA & PENELITIAN
* **Nama Lengkap:** Zaini Leon Musthofa Kamal
* **NIM:** 231240001455
* **Program Studi:** Teknik Informatika (S-1)
* **Dosen Pembimbing:** Teguh Tamrin, S.Kom., M.Kom.
* **Judul Proposal:** **Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin**

---

## PETUNJUK MENTAL & TEKNIK MENJAWAB PENGUJI

> [!TIP]
> **Gunakan Formula 3 Detik Menjawab:**
> 1. **🎯 Kata Kunci Hafalan (1 Kalimat Inti):** Kalimat pendek dan tegas yang langsung kamu ucapkan di awal agar dosen tahu kamu paham betul pokok masalahnya.
> 2. **🗣️ Jawaban Lisan (Alur Natural):** Penjelasan santun, runtut, dan mengalir dengan bahasa Indonesia yang jelas tanpa gugup.
> 3. **📚 Landasan Teori & Bukti Ilmiah:** Menyebut nama pakar/tahun rujukan (misal: Andersen, Bollerslev, Patton, Corsi, Hochreiter, Bergstra, López de Prado) atau angka konkret dari proposalmu.
>
> **Pantangan Kata:** Jangan pernah mengucapkan *"Kayaknya"*, *"Mungkin"*, *"Kurang tahu"*, atau *"Coba-coba"*.  
> **Gantilah dengan:** *"Berdasarkan pengujian empiris"*, *"Merujuk pada penelitian rujukan..."*, atau *"Sesuai dengan batasan masalah yang telah ditetapkan..."*.

---

## BAGIAN 1: PERTANYAAN INTI & LATAR BELAKANG (WAJIB DIHAFAL)

### Pertanyaan 1: "Coba jelaskan dengan singkat dan padat, penelitian skripsi kamu ini sebenarnya tentang apa?"
* **🎯 Kata Kunci Hafalan:**
  **"Meramalkan risiko fluktuasi pasar (volatilitas) Bitcoin satu hari ke depan menggunakan AI Long Short-Term Memory (LSTM) yang parameternya ditala otomatis oleh Optuna."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Penelitian ini berfokus pada **perancangan sistem komputasi kecerdasan buatan untuk meramalkan tingkat risiko fluktuasi pasar atau *realized volatility* Bitcoin satu hari ke depan ($t+1$) menggunakan model *deep learning* Long Short-Term Memory (LSTM)**. Agar performa model maksimal dan efisien, seluruh parameter arsitektur LSTM ditala secara otomatis menggunakan algoritma optimasi Bayesian **Optuna (TPE)** dengan protokol **Purged Cross-Validation** guna menjamin eksperimen bebas dari kebocoran data (*data leakage*)."
* **📚 Dasar Ilmiah:**
  * Objek: Data frekuensi tinggi Bitcoin (kline 1 jam) periode 2020–2026 dari Binance Vision (2.464 hari observasi).
  * Target: Proksi operasional *Realized Variance* harian dari 24 lilin intra-hari.

---

### Pertanyaan 2: "Kenapa kamu memilih penelitian ini? Kenapa memilih Bitcoin dan kenapa yang diprediksi volatilitasnya, bukan harganya?"
* **🎯 Kata Kunci Hafalan:**
  **"Harga nominal Bitcoin terbukti acak (*random walk*), sedangkan volatilitasnya terbukti memiliki pola keteraturan statistik (*volatility clustering*)."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Ada dua alasan mendasar, Bapak/Ibu:  
  Pertama, Bitcoin adalah aset kripto dengan kapitalisasi pasar terbesar di dunia yang pasarnya beroperasi non-stop 24 jam sehari 7 hari seminggu tanpa jeda libur, sehingga memiliki dinamika risiko yang sangat kaya.  
  Kedua dan yang paling mendasar: **memprediksi harga penutupan nominal (*closing price*) secara teoretis dan empiris terbukti mendekati lintasan acak (*random walk*)** dengan rasio sinyal terhadap derau yang sangat rendah (sesuai Hipotesis Pasar Efisien Fama). Banyak peneliti komputer sebelumnya gagal mengalahkan tebakan naif saat menebak harga nominal.  
  Sebaliknya, **volatilitas atau besaran fluktuasi pasar terbukti memiliki sifat keteraturan statistik berupa pengelompokan volatilitas (*volatility clustering*)** (Bollerslev, 1986; Andersen & Bollerslev, 1998). Periode varians tinggi cenderung saling berkelompok. Oleh karena itu, memprediksi volatilitas jauh lebih rasional, ilmiah, dan sangat krusial bagi manajemen risiko portofolio digital."
* **📚 Dasar Ilmiah:**
  * Teori *Volatility Clustering* (Mandelbrot, 1963; Bollerslev, 1986).
  * Bukti empiris Andersen et al. (2003) mengenai stabilitas proksi *Realized Volatility*.

---

### Pertanyaan 3: "Apa masalah utama yang terjadi di lapangan sehingga kamu mengangkat judul ini?"
* **🎯 Kata Kunci Hafalan:**
  **"Ada 3 masalah utama: fluktuasi harga Bitcoin sangat ekstrem, model ekonometrika klasik kaku pada asumsi linier, dan riset deep learning sebelumnya marak terjebak kebocoran data (*data leakage*) serta penalaan parameter coba-coba."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Berdasarkan penelusuran latar belakang masalah di Bab I, terdapat 3 masalah krusial:
  1. **Masalah Pasar:** Tingkat volatilitas Bitcoin sangat ekstrem dan kerap memicu likuidasi massal dana investor karena ketiadaan sistem peramalan risiko yang andal.
  2. **Keterbatasan Model Ekonometrika Linier:** Model linier tradisional seperti GARCH(1,1) dan HAR-RV Corsi mengasumsikan hubungan parametrik linier statis, sehingga gagal merespons lonjakan varians non-linear mendadak (*volatility jumps*) pada pasar aset kripto.
  3. **Kelemahan Metodologi Riset Informatika Terdahulu:** Sebagian besar peneliti deep learning sebelumnya melakukan penalaan hyperparameter secara coba-coba (*manual trial-and-error*) yang boros komputasi, serta melakukan pembagian data secara acak (*random train-test split*) yang memicu bencana kebocoran data masa depan (*data leakage*)."
* **📚 Dasar Ilmiah:**
  * Ardia et al. (2019) mengenai lonjakan rezim non-linear pasar kripto.
  * López de Prado (2018) mengenai ancaman kebocoran data pada deret waktu finansial.

---

### Pertanyaan 4: "Apa urgensinya penelitian ini? Mengapa penting dan layak diteliti di tingkat skripsi Teknik Informatika?"
* **🎯 Kata Kunci Hafalan:**
  **"Urgensinya adalah standarisasi pipeline AI finansial yang bebas kebocoran data (*leakage-free*), teroptimasi secara cerdas, dan teruji secara statistik inferensial formal."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Urgensi penelitian ini mencakup dua dimensi:
  1. **Aspek Keilmuan Informatika & Sains Data:** Riset deep learning deret waktu finansial membutuhkan metodologi komputasi yang ketat. Skripsi ini menghadirkan standarisasi pipeline *machine learning* finansial yang utuh, mulai dari pra-pemrosesan berfrekuensi tinggi, optimasi Bayesian terarah dengan pemangkasan dini (*MedianPruner*), hingga validasi inferensial formal.
  2. **Aspek Praktis Industri Finansial Digital:** Informasi ramalan volatilitas satu hari ke depan berfungsi sebagai sistem peringatan dini (*early warning system*) yang sangat dibutuhkan oleh praktisi kuantitatif dan manajer risiko untuk mitigasi risiko kebangkrutan (*Value-at-Risk*) serta lindung nilai (*hedging*)."
* **📚 Dasar Ilmiah:**
  * Kim & Won (2018) mengenai integrasi AI pada estimasi risiko pasar.

---

### Pertanyaan 5: "Apa pembaruan (novelty) utama dari penelitian skripsi kamu?"
* **🎯 Kata Kunci Hafalan:**
  **"Tri-Pilar Novelty: (1) Target Realized Variance intra-hari 1 jam, (2) Optimasi Bayesian Optuna TPE + MedianPruner, dan (3) Protokol Purged CV jeda 10 hari dengan evaluasi asimetris QLIKE."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Novelty utama penelitian ini terletak pada **Tri-Pilar Sinergi Metodologis Komputasi**:
  1. **Novelty Target (Rekonseptualisasi Variabel Sasaran):** Tidak berspekulasi menebak harga nominal yang acak, melainkan memodelkan proksi *Realized Variance* (RV) berbasis agregasi kuadrat imbal hasil intra-hari 1 jam yang memiliki dasar ekonometrika kuat (Andersen et al., 2003).
  2. **Novelty Algoritmik (Optimasi Bayesian Bersyarat):** Menggantikan penalaan manual atau *grid search* yang boros dengan algoritma **Optuna TPE (Tree-structured Parzen Estimator)** yang dipadukan dengan **MedianPruner** untuk menghentikan trial buruk secara dini, sehingga menghemat daya komputasi hingga 50–70%.
  3. **Novelty Integritas Metodologis & Inferensi Asimetris:** Mengeliminasi 100% risiko kebocoran data temporal melalui **5-fold Purged Cross-Validation (jeda pemisah 10 hari)** dengan *fold-specific scaling*, serta mengevaluasi performa menggunakan loss asimetris **QLIKE** (Patton, 2011) yang tahan terhadap derau proksi dan diperkuat uji inferensi **Diebold-Mariano HAC Newey-West** serta **10.000 repetisi Bootstrap**."
* **📚 Dasar Ilmiah:**
  * Bergstra et al. (2011) untuk TPE; Patton (2011) untuk QLIKE; López de Prado (2018) untuk Purged CV.

---

### Pertanyaan 6: "Apa bedanya penelitian kamu dengan penelitian-penelitian terdahulu yang juga membahas Bitcoin?"
* **🎯 Kata Kunci Hafalan:**
  **"Perbedaannya ada 4: Pergeseran target ke RV frekuensi tinggi, eliminasi kebocoran data dengan Purged CV, optimasi otomatis Bayesian Optuna, dan pengujian inferensi formal Diebold-Mariano."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Berdasarkan sintesis terhadap 13 penelitian terdahulu pada Tabel 2.1 naskah proposal, ada 4 pembeda fundamental:
  1. **Variabel Target:** Peneliti terdahulu (seperti Khumaidi et al., 2024; Aswadi & Ependi, 2025; Fawzi et al., 2025) mayoritas memprediksi harga nominal harian. Penelitian ini memprediksi *Realized Volatility* berbasis 24 bar intra-hari.
  2. **Skema Partisi Data:** Penelitian terdahulu banyak menggunakan partisi acak (*random K-fold*) atau normalisasi skala global yang membocorkan masa depan. Penelitian ini menggunakan partisi temporal kronologis murni dengan *Purged CV* dan *fold-specific scaling*.
  3. **Metode Optimasi:** Penelitian terdahulu mengandalkan penalaan manual atau *random search*. Penelitian ini menerapkan penalaan otomatis Bayesian Optuna TPE dengan *MedianPruner*.
  4. **Metrik & Uji Statistik:** Penelitian terdahulu hanya mengandalkan metrik simetris MSE/MAE yang bias terhadap derau proksi tanpa uji signifikansi. Penelitian ini menggunakan fungsi kerugian asimetris QLIKE serta membuktikannya melalui Uji Diebold-Mariano HAC Newey-West dan *Moving-Block Bootstrap*."

---

## BAGIAN 2: DATA, REALIZED VOLATILITY (RV), & FITUR MASUKAN

### Pertanyaan 7: "Apa itu Realized Volatility / Realized Variance (RV) dan kenapa harus ditransformasi logaritma ($\log RV$)?"
* **🎯 Kata Kunci Hafalan:**
  **"RV adalah proksi varians riil harian dari penjumlahan kuadrat return 24 jam intra-hari. Transformasi logaritma dipakai untuk menormalkan data yang menceng ekstrem dan menjamin nilai prediksi selalu positif."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Volatilitas adalah variabel laten (tidak tampak pada harga harian biasa). Oleh karena itu, kita mengukurnya menggunakan **Realized Variance (RV)**, yaitu penjumlahan kuadrat imbal hasil logaritmik intra-hari 1 jam dari 24 lilin bursa sepanjang satu hari UTC:
  $$\text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2$$
  **Alasan Transformasi Logaritma ($\log RV_t$):**  
  Data empiris RV memiliki nilai yang selalu positif, tetapi memiliki kemencengan positif (*skewness*) ekstrem dan ekor tebal (*fat tails*) akibat lonjakan pasar. Dengan menerapkan transformasi:
  $$\log RV_t = \ln(\text{RV}_t + 10^{-12})$$
  sebaran data menjadi jauh lebih simetris mendekati distribusi normal (Gaussian). Ini mempermudah konvergensi optimasi gradien pada jaringan saraf LSTM dan mengeliminasi risiko prediksi bernilai negatif saat dikembalikan lewat fungsi eksponensial."
* **📚 Dasar Ilmiah:**
  * Andersen & Bollerslev (1998); Andersen, Bollerslev, Diebold, & Labys (2003).

---

### Pertanyaan 8: "Bagaimana caranya menentukan dan menghitung nilai RV dari data yang kamu gunakan?"
* **🎯 Kata Kunci Hafalan:**
  **"Dihitung melalui 3 langkah: (1) Ambil 24 bar kline 1 jam per hari UTC, (2) Hitung return logaritmik open-to-close tiap jam, (3) Jumlahkan kuadrat ke-24 return tersebut untuk menghasilkan RV harian."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Kalkulasi RV dilakukan melalui prosedur operasional matematis berikut:
  1. **Agregasi Siklus Harian UTC:** Dari data mentah Binance Vision, kita kelompokkan 24 lilin bar 1 jam dalam satu hari kalender UTC (pukul 00:00:00 hingga 23:59:59).
  2. **Hitung Return Logaritmik Intra-hari ($r_{t,h}$):** Pada setiap lilin jam ke-$h$, kita hitung selisih logaritma harga penutupan terhadap harga pembukaan:
     $$r_{t,h} = \ln(C_{t,h}) - \ln(O_{t,h})$$
  3. **Penjumlahan Kuadrat (Sum of Squared Returns):** Kuadrat dari seluruh 24 imbal hasil jam tersebut kita jumlahkan secara kumulatif:
     $$\text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2$$
  Nilai $\text{RV}_t$ inilah yang menjadi representasi besaran varians fluktuasi Bitcoin pada hari ke-$t$. Dalam naskah proposal, kami mendefinisikannya secara transparan sebagai **proksi operasional RV**."
* **📚 Dasar Ilmiah:**
  * Barndorff-Nielsen & Shephard (2002); Andersen et al. (2003).

---

### Pertanyaan 9: "Data Bitcoin yang kamu pakai itu data SPOT atau data FUTURES? Kenapa memilih jenis data tersebut?"
* **🎯 Kata Kunci Hafalan:**
  **"Data SPOT Bitcoin (BTC/USDT) di bursa Binance. Dipilih karena mencerminkan penawaran-permintaan riil murni tanpa distorsi *funding rate* atau likuidasi leverage kontrak futures."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Data yang kami gunakan adalah **data pasar SPOT pasangan BTC/USDT dari bursa Binance**, yang diunduh resmi melalui repositori **Binance Vision** (`data.binance.vision`).  
  **Alasan Memilih Pasar Spot (Bukan Futures):**
  1. **Mencerminkan Permintaan & Penawaran Riil:** Pasar spot merepresentasikan transaksi perpindahan kepemilikan aset riil (*underlying asset*), sehingga dinamika harganya murni digerakkan oleh likuiditas riil pasar.
  2. **Bebas Distorsi Mekanisme Derivatif:** Pasar futures memiliki komponen suku bunga pendanaan berkala (*funding rate*), premi/diskon basis terhadap indeks, dan fenomena rantai likuidasi utang (*leverage liquidation cascades*) yang sering menciptakan anomali lonjakan harga semu yang tidak mencerminkan volatilitas pasar yang sebenarnya.
  3. **Integritas Historis Panjang:** Data spot BTC/USDT di Binance Vision tersedia lengkap dengan likuiditas terbesar di dunia sejak awal 2020 hingga September 2026."
* **📚 Dasar Ilmiah:**
  * Dokumentasi resmi Binance Vision Archive (2026); Alexander & Heck (2020) mengenai mikrostruktur pasar kripto spot vs derivatif.

---

### Pertanyaan 10: "Mengapa kamu memilih 6 fitur teknikal masukan ini? Dari mana dasar teorinya dan kenapa tidak menggunakan indikator populer seperti RSI atau MACD?"
* **🎯 Kata Kunci Hafalan:**
  **"6 fitur dipilih berdasarkan teori ekonometrika kausal mikrostruktur pasar (autokorelasi, Parkinson range, MDH volume, absret shock, dan HAR mingguan/bulanan). Indikator RSI/MACD ditolak karena merupakan indikator tren harga yang memiliki kelambatan (*lag*) dan multikolinearitas."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Keenam fitur masukan dipilih berdasarkan **landasan teori ekonometrika mikrostruktur pasar**, bukan coba-coba:
  1. $\log RV_t$: Menangkap komponen autokorelasi langsung dan persistensi volatilitas harian.
  2. $\log range_t = \ln(H_t - L_t)$: Berbasis estimator Parkinson (1980), menangkap rentang dispersi harga ekstrem tertinggi-terendah intra-hari tanpa terdistorsi arah penutupan.
  3. $\log volume_t = \ln(V_t)$: Berdasarkan teori *Mixture of Distribution Hypothesis* (MDH; Clark, 1973), bahwa volume perdagangan berbanding lurus dengan laju kedatangan informasi dan intensitas volatilitas.
  4. $\log absret_t = \ln(|r_t| + 10^{-6})$: Mengukur magnitudo kejutan harga harian (*daily price shock*) tanpa memedulikan arah positif/negatif.
  5. $\text{rv\_mean\_5}_t$: Berbasis model HAR-RV Corsi (2009), menangkap horizon investasi mingguan (5 hari).
  6. $\text{rv\_mean\_22}_t$: Menangkap horizon investasi bulanan (22 hari kalender institusional).
  
  **Kenapa Menolak RSI, MACD, atau Bollinger Bands?**  
  Karena indikator teknikal tersebut dirancang untuk menebak **arah tren harga (*trend/momentum*)**, memiliki keterlambatan waktu (*lagging*) akibat penghalusan (*smoothing*) ganda, dan menimbulkan multikolinearitas tinggi. Target kita adalah **dispersi risiko (volatilitas)**, sehingga 6 fitur kausal bebas *look-ahead bias* jauh lebih valid secara sains data."
* **📚 Dasar Ilmiah:**
  * Corsi (2009); Parkinson (1980); Clark (1973); Andersen & Bollerslev (1998).

---

## BAGIAN 3: MODEL ARSITEKTUR LSTM & OPTIMASI OPTUNA

### Pertanyaan 11: "Kenapa memilih model LSTM? Kenapa tidak pakai RNN biasa, GRU, atau arsitektur Transformer (Informer, PatchTST)?"
* **🎯 Kata Kunci Hafalan:**
  **"LSTM memiliki bias induktif temporal alami dan sel memori bebas vanishing gradient. RNN biasa gagal karena vanishing gradient, sedangkan Transformer over-parameterized dan rentan severe overfitting pada 2.464 baris data tabular."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "1. **Kelemahan RNN Konvensional:** Mengalami masalah hilangnya gradien (*vanishing gradient*) saat memproses dependensi waktu yang panjang, sehingga mudah melupakan pola volatilitas masa lalu.  
  2. **Keunggulan LSTM Dibanding RNN & GRU:** LSTM memiliki status sel (*cell state*) dan tiga gerbang logika yang memungkinkan gradien mengalir linier tanpa hambatan (*Constant Error Carousel*). Pemisahan status sel pada LSTM lebih stabil menampung persistensi memori majemuk (harian, mingguan, bulanan) dibanding GRU.  
  3. **Mengapa Bukan Transformer / LLM?** Dataset kita berjumlah 2.464 hari observasi. Riset prestisius oleh **Zeng et al. (AAAI 2023)** berjudul *'Are Transformers Effective for Time Series?'* membuktikan bahwa model Transformer memiliki jutaan parameter bebas yang *data-hungry*, sehingga rentan mengalami *severe overfitting* pada data tabular deret waktu berukuran ribuan sampel. LSTM yang ditala secara presisi oleh Optuna jauh lebih ramping, efisien, dan andal (*Occam's Razor*)."
* **📚 Dasar Ilmiah:**
  * Hochreiter & Schmidhuber (1997); Zeng et al. (AAAI 2023); Christensen et al. (2023).

---

### Pertanyaan 12: "Bisa jelaskan cara kerja sel LSTM dan fungsi 3 gerbangnya secara intuitif tanpa rumus rumit?"
* **🎯 Kata Kunci Hafalan:**
  **"Cara kerja sel LSTM seperti memori manusia: Gerbang Lupa menghapus info usang, Gerbang Masuk mencatat info fluktuasi baru, Status Sel menyimpan memori jangka panjang, dan Gerbang Keluar memproyeksikan ramalan volatilitas."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Bisa, Bapak/Ibu. Satu sel LSTM bekerja melalui 4 tahapan sekuensial yang sangat logis:
  1. **Gerbang Lupa (*Forget Gate*, $f_t$):** Bertindak sebagai penghapus memori. Ia memeriksa masukan baru ($x_t$) dan status kemarin ($h_{t-1}$) lewat fungsi sigmoid (0 sampai 1): *'Informasi volatilitas masa lalu mana yang sudah usang dan harus dibuang (0) atau disimpan (1)?'*
  2. **Gerbang Masuk (*Input Gate*, $i_t$ & $\tilde{c}_t$):** Bertindak sebagai pencatat hal baru. Sinyal sigmoid menyeleksi kepentingannya ($i_t$), dan fungsi $\tanh$ membuat kandidat memori baru ($\tilde{c}_t$). Keduanya dikalikan.
  3. **Pembaruan Status Sel (*Cell State Update*, $c_t$):** Ini adalah 'buku catatan memori jangka panjang'. Memori lama yang disaring gerbang lupa ditambahkan dengan informasi baru dari gerbang masuk: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$.
  4. **Gerbang Keluar (*Output Gate*, $o_t$ & $h_t$):** Sinyal sigmoid memutuskan informasi mana yang dikeluarkan hari ini ($o_t$), lalu dikalikan dengan modulasi $\tanh(c_t)$ untuk menghasilkan status tersembunyi ($h_t$), yang kemudian diproyeksikan oleh lapisan linier menjadi ramalan $\log RV_{t+1}$."

---

### Pertanyaan 13: "Mengapa kamu menggunakan algoritma Optuna untuk optimasi hyperparameter? Kenapa tidak pakai Grid Search atau Random Search?"
* **🎯 Kata Kunci Hafalan:**
  **"Grid Search meledak waktu komputasinya (*curse of dimensionality*), Random Search mencari secara buta tanpa arah, sedangkan Optuna TPE menerapkan Bayesian yang belajar dari riwayat trial sebelumnya dan memiliki pemangkas dini *MedianPruner*."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "1. **Grid Search:** Mengevaluasi seluruh kombinasi secara kaku. Untuk 6 parameter dengan ribuan kombinasi, komputasi meledak secara eksponensial (*curse of dimensionality*).  
  2. **Random Search:** Memilih kombinasi secara acak tanpa belajar dari percobaan sebelumnya, membuang komputasi pada wilayah parameter yang buruk.  
  3. **Keunggulan Optuna (TPE & MedianPruner):** Optuna menerapkan algoritma probabilistik Bayesian *Tree-structured Parzen Estimator* (TPE). TPE memodelkan riwayat konfigurasi sukses ($\ell(x)$) vs konfigurasi gagal ($g(x)$), lalu secara cerdas mengarahkan *trial* berikutnya ke ruang parameter yang memaksimalkan rasio $\ell(x)/g(x)$.  
  Selain itu, Optuna dilengkapi **MedianPruner**: jika suatu arsitektur pada epoch awal menghasilkan loss yang lebih buruk dari median trial sebelumnya, pelatihan langsung dihentikan (*pruning*), sehingga menghemat waktu komputasi hingga 50–70%."
* **📚 Dasar Ilmiah:**
  * Bergstra, Bardenet, Bengio, & Kégl (2011); Akiba et al. (ACM KDD 2019).

---

### Pertanyaan 14: "Bagaimana kamu menentukan batasan ruang pencarian (search space) hyperparameter di Optuna? Apakah angkanya asal tebak?"
* **🎯 Kata Kunci Hafalan:**
  **"Tidak asal tebak, melainkan berlandaskan batasan empiris literatur terdahulu: lookback 10–30 hari siklus pasar, hidden units 16–128 kapasitas representasi, 1–2 layer efisiensi gradien, dropout 0,05–0,40, dan learning rate Adam skala log."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Batas ruang pencarian sebanyak 50 *trials* ditetapkan berdasarkan tinjauan literatur empiris:
  1. *Lookback window* [10 s.d. 30 hari]: Merujuk riset Kervancı (2023) dan siklus kalender pasar keuangan (22 hari kerja / 30 hari kalender). Di bawah 10 hari kehilangan memori mingguan, di atas 30 hari menumpuk derau usang (*fading memory*).
  2. *Hidden units* [16 s.d. 128 neuron]: Berdasarkan studi berskala besar Greff et al. (2017). Untuk 6 fitur masukan, rentang 16–128 adalah batas ideal mencegah *underfitting* (jika < 16) dan mencegah *overfitting* (jika > 128).
  3. *Layers* [1 atau 2 lapisan]: Menumpuk lebih dari 2 lapisan LSTM pada data deret waktu finansial terbukti menurunkan efisiensi gradien tanpa peningkatan akurasi berarti.
  4. *Dropout* [0,05 s.d. 0,40]: Rekomendasi Srivastava et al. (2014) untuk regularisasi jaringan rekuren.
  5. *Learning rate* Adam [$3 \times 10^{-4}$ s.d. $2 \times 10^{-3}$, skala log]: Skala standar optimizer Adam (Kingma & Ba, 2014) untuk stabilitas penurunan gradien.
  6. *Batch size* [16, 32, 64 sampel]: Mengendalikan variabilitas stokastik pembaruan bobot."
* **📚 Dasar Ilmiah:**
  * Greff et al. (2017); Srivastava et al. (2014); Kingma & Ba (2014); Kervancı & Akay (2023).

---

## BAGIAN 4: METODOLOGI VALIDASI, ANTI-LEAKAGE, & EVALUASI STATISTIK

### Pertanyaan 15: "Apa jenis dan pendekatan penelitian yang kamu gunakan dalam skripsi ini? Kenapa bukan Research and Development (R&D) atau kualitatif?"
* **🎯 Kata Kunci Hafalan:**
  **"Pendekatan Kuantitatif dengan Desain Eksperimental Komputasional. Bukan R&D karena ini adalah eksperimen sains data terkontrol untuk menguji hipotesis statistik, bukan merancang aplikasi antarmuka software."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Sebagaimana tercantum pada **Bab III Sub-bab A.1 proposal**, penelitian ini menggunakan **pendekatan kuantitatif dengan desain eksperimental komputasional (*computational experimental research*)**.  
  **Alasan Ilmiahnya:**
  1. **Kuantitatif:** Karena objek penelitian adalah data deret waktu finansial numerik terukur guna menguji 3 hipotesis penelitian ($H_1, H_2, H_3$) secara matematis.
  2. **Eksperimental Komputasional (Bukan R&D):** Penelitian ini bukan merancang produk perangkat lunak antarmuka seperti website atau aplikasi mobile (*software engineering / R&D prototyping*), melainkan melakukan **eksperimen sains data terkontrol**. Kami menguji efek variabel perlakuan (*treatment*, model LSTM-Optuna) terhadap 4 model pembanding kontrol (*baseline*: Persistence, HAR-RV, GARCH, LSTM Untuned) di bawah protokol yang sama persis bebas kebocoran data.
  3. **Kesesuaian Pedoman UNISNU:** Sesuai Buku Pedoman Skripsi UNISNU Bab III (bagian Penelitian Kuantitatif), desain eksperimental komputasional adalah bentuk metodologi standar tertinggi untuk bidang Kecerdasan Buatan dan Sains Data."

---

### Pertanyaan 16: "Apa yang dimaksud dengan kebocoran data (*data leakage*) pada deret waktu dan bagaimana kamu membuktikan penelitian kamu bebas kebocoran data?"
* **🎯 Kata Kunci Hafalan:**
  **"Data leakage adalah masuknya informasi masa depan ke dalam pelatihan masa lalu (*look-ahead bias*). Kami cegah dengan 4 benteng: partisi kronologis murni, Purged CV jeda 10 hari, scaler fold-specific, dan isolasi data evaluasi 2026."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Kebocoran data (*data leakage*) adalah cacat metodologis fatal di mana informasi masa depan menyusup ke proses pelatihan masa lalu (*look-ahead bias*), menghasilkan akurasi semu di atas kertas yang langsung hancur saat diuji di dunia nyata.  
  Kami menerapkan **4 lapis benteng pencegahan**:
  1. **Partisi Temporal Kronologis Murni:** Data dibagi menurut kalender: Development 2020–2023 (1.460 hari), Validation 2024–2025 (731 hari), dan Evaluasi Temporal 2026 (273 hari). Tidak ada pengacakan urutan waktu.
  2. **Skema Purged Cross-Validation:** Pada setiap lipatan (*fold*), disisipkan jeda pemisah (*purge gap*) selama 10 hari antara data latih dan validasi untuk memutus autokorelasi serial jendela geser.
  3. **Fold-Specific Scaling:** Normalisasi `StandardScaler` dihitung murni dari nilai mean dan varians data latih di masing-masing fold, tanpa pernah menyentuh data validasi.
  4. **Isolasi Evaluasi Temporal 2026:** Periode 2026 dikunci total dan tidak pernah digunakan dalam proses pencarian hyperparameter Optuna."
* **📚 Dasar Ilmiah:**
  * Marcos López de Prado (2018) — *Advances in Financial Machine Learning*.

---

### Pertanyaan 17: "Kenapa evaluasi utamanya memakai fungsi kerugian QLIKE, bukan MSE atau MAE? Bagaimana bukti matematis keunggulan penalti asimetrisnya?"
* **🎯 Kata Kunci Hafalan:**
  **"QLIKE terbukti matematis tahan terhadap derau proksi (Patton, 2011) dan bersifat asimetris: menghukum kesalahan meremehkan risiko (*under-forecasting*) 4 kali lipat lebih berat dibanding *over-forecasting*."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Karena volatilitas aktual adalah variabel laten yang diestimasi menggunakan proksi (*realized variance*) yang berderau (*noisy proxy*).  
  Riset ekonometrika terkemuka oleh **Patton (2011)** membuktikan secara analitik bahwa metrik simetris seperti MSE menghasilkan perankingan model yang bias jika proksinya berderau. Sebaliknya, **QLIKE terbukti robust**: perankingan model di bawah QLIKE konsisten sama apakah dihitung terhadap volatilitas laten murni maupun terhadap proksi berderau.
  
  **Bukti Keunggulan Penalti Asimetris:**  
  Rumus QLIKE: $\text{QLIKE}(RV, \widehat{RV}) = \frac{RV}{\widehat{RV}} - \ln\left(\frac{RV}{\widehat{RV}}\right) - 1$.  
  Jika volatilitas aktual $RV = 0{,}10$:
  * **Model A (*Under-forecast* 0,05; $\widehat{RV} = 0{,}05$):** Galat $\text{QLIKE} = \mathbf{0{,}307}$.
  * **Model B (*Over-forecast* 0,05; $\widehat{RV} = 0{,}15$):** Galat $\text{QLIKE} = \mathbf{0{,}072}$.
  
  Pada metrik MSE, kedua model dianggap sama persis ($0{,}0025$). Namun pada QLIKE, meremehkan risiko dihukum **lebih dari 4 kali lipat lebih berat** ($0{,}307$ vs $0{,}072$)! Dalam dunia finansial, meremehkan risiko (*under-forecast*) berakibat fatal karena memicu kebangkrutan modal dan likuidasi margin call."
* **📚 Dasar Ilmiah:**
  * Patton, A. J. (2011). *Data-based ranking of volatility models*. Journal of Econometrics.

---

### Pertanyaan 18: "Apa saja 4 model baseline pembanding yang kamu gunakan dan apa fungsinya masing-masing?"
* **🎯 Kata Kunci Hafalan:**
  **"4 Baseline bertingkat: Persistence (sanity check naif), HAR-RV Corsi (standar industri frekuensi tinggi), GARCH(1,1) (ekonometrika klasik), dan LSTM Untuned (membuktikan efek Optuna)."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Kami menguji model usulan terhadap 4 model pembanding bertingkat:
  1. **Random Walk Persistence (Baseline Naif):** Asumsi besok sama dengan hari ini. Ini adalah *sanity check*: jika model AI gagal mengalahkan model naif ini, maka model AI tersebut secara ilmiah tidak layak dipakai.
  2. **HAR-RV Corsi (2009) (Baseline Ekonometrika Frekuensi Tinggi):** Model regresi linier standar industri yang memanfaatkan komponen harian, mingguan, dan bulanan.
  3. **GARCH(1,1) (Baseline Ekonometrika Klasik):** Model varians bersyarat konvensional berbasis imbal hasil harian dengan skema *expanding window*.
  4. **LSTM Untuned (Baseline Deep Learning Heuristik):** Arsitektur LSTM default tanpa bantuan Optuna. Fungsinya membuktikan bahwa peningkatan akurasi benar-benar dihasilkan oleh optimasi Bayesian Optuna, bukan semata-mata karena algoritma LSTM-nya."

---

### Pertanyaan 19: "Bagaimana kamu membuktikan bahwa keunggulan model LSTM-Optuna bukan faktor kebetulan (stochastic fluke)?"
* **🎯 Kata Kunci Hafalan:**
  **"Dibuktikan melalui tiga lapis pengujian formal: Uji Diebold-Mariano berkoreksi HAC Newey-West ($p < 0{,}05$), Moving-Block Bootstrap 10.000 repetisi (CI 95%), dan protokol 5 seed acak tetap."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Keunggulan model tidak hanya dinilai dari selisih rata-rata angka, melainkan diuji secara inferensial formal:
  1. **Uji Diebold-Mariano (1995) dengan Koreksi HAC Newey-West:** Menguji secara asimtotik apakah selisih kerugian peramalan ($d_t = L_{\text{baseline}} - L_{\text{LSTM}}$) bernilai positif secara signifikan dengan nilai-$p < 0{,}05$. Estimator HAC Newey-West dengan lag 5 digunakan untuk mengoreksi autokorelasi serial dan heteroskedastisitas pada deret galat.
  2. **Moving-Block Bootstrap (10.000 Repetisi):** Mengonstruksi selang kepercayaan empiris 95% yang mempertahankan struktur dependensi deret waktu (Künsch, 1989). Keunggulan terbukti kokoh jika batas atas interval bootstrap 95% berada di bawah nol.
  3. **Protokol Multi-Seed (5 Seed):** Mengendalikan variabilitas inisialisasi bobot jaringan saraf dengan melatih model menggunakan lima seed deterministik tetap: `(42, 123, 2024, 7, 99)`."
* **📚 Dasar Ilmiah:**
  * Diebold & Mariano (1995); Newey & West (1987); Künsch (1989); Bouthillier et al. (2021).

---

### Pertanyaan 20: "Apa maksud notasi $z_t \sim N(0,1)$ dan parameter $(1,1)$ pada model pembanding GARCH(1,1)?"
* **🎯 Kata Kunci Hafalan:**
  **"$N(0,1)$ adalah notasi statistik bahwa inovasi derau berdistribusi Normal Baku (rata-rata 0, varians 1). Angka $(1,1)$ adalah ordo lag: melihat 1 hari residual kuadrat (ARCH) dan 1 hari varians masa lalu (GARCH)."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Notasi $z_t \sim N(0,1)$ pada Persamaan (2.3) merupakan **asumsi distribusi probabilitas dari variabel derau acak (*random innovation / white noise*)**. Huruf $N$ melambangkan distribusi Normal, angka 0 adalah nilai rata-rata (*mean*), dan angka 1 adalah variansnya. Komponen ini wajib ada secara matematis sebagai pemicu fluktuasi acak pada residual $\varepsilon_t = \sigma_t z_t$ agar model GARCH dapat diestimasi parameternya lewat metode *Maximum Likelihood*.  
  Sedangkan angka $(1,1)$ pada nama GARCH(1,1) menunjukkan **ordo lag**:
  * Angka 1 pertama: melihat kuadrat residual **1 periode ke belakang** ($\varepsilon_{t-1}^2$).
  * Angka 1 kedua: melihat varians **1 periode ke belakang** ($\sigma_{t-1}^2$)."
* **📚 Dasar Ilmiah:**
  * Bollerslev, T. (1986). *Generalized autoregressive conditional heteroskedasticity*. Journal of Econometrics.

---


### Pertanyaan Baru: "Bagaimana rumusan Hipotesis Penelitian kamu? Kenapa menggunakan format $H_0$ dan $H_1$ serta pengujian satu sisi?"
* **🎯 Kata Kunci Hafalan:**
  **"Hipotesis dirumuskan formal berpasangan H0 (tidak ada keunggulan signifikan / selisih loss ≥ 0) dan H1 (LSTM-Optuna unggul signifikan / selisih loss < 0) yang diuji satu sisi pada taraf α = 0,05."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Sesuai kaidah metode penelitian kuantitatif, hipotesis penelitian dirumuskan secara berpasangan antara Hipotesis Nol ($H_0$) dan Hipotesis Alternatif ($H_1$) untuk dua komparasi primer:
  1. **Hipotesis 1 (vs Baseline Random Walk Persistence):**
     * **$H_0$:** Model LSTM-Optuna tidak menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan baseline Persistence pada evaluasi temporal 2026 ($\mu_{d_1} \ge 0$).
     * **$H_1$:** Model LSTM-Optuna menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan baseline Persistence pada evaluasi temporal 2026 ($\mu_{d_1} < 0$).
  2. **Hipotesis 2 (vs Model Ekonometrika HAR-RV):**
     * **$H_0$:** Model LSTM-Optuna tidak menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan model HAR-RV pada evaluasi temporal 2026 ($\mu_{d_2} \ge 0$).
     * **$H_1$:** Model LSTM-Optuna menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan model HAR-RV pada evaluasi temporal 2026 ($\mu_{d_2} < 0$).
  
  **Alasan Pengujian Satu Sisi (One-Sided):** Karena tujuan penelitian adalah membuktikan keunggulan (*superiority*) model usulan, bukan sekadar melihat apakah ada perbedaan dua arah. Uji statistiknya menggunakan Diebold–Mariano dengan estimasi HAC Newey–West pada $\alpha = 0{,}05$.
  Sedangkan GARCH(1,1) dan LSTM untuned dilaporkan secara deskriptif sebagai pembanding sekunder tanpa uji hipotesis formal primer."



### Pertanyaan Baru: "Pada Bab III tertulis pengujian unit (unit testing) mandiri, apakah berkas tes fisiknya benar-benar ada di repositori dan apa saja yang diuji?"
* **🎯 Kata Kunci Hafalan:**
  **"Ada 34 skenario unit test terotomatisasi yang terbagi dalam 4 file skrip fisik di folder tests/ dan seluruhnya lulus 100% menggunakan pytest."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Benar sekali, Bapak/Ibu Penguji. Repositori penelitian kami dilengkapi dengan pengujian unit terotomatisasi (*automated unit testing*) yang dibangun menggunakan framework `pytest`. Seluruh skrip tersimpan secara fisik di direktori `tests/` yang terdiri dari 4 berkas mandiri dengan total 34 skenario tes:
  1. **`tests/test_study2.py` (15 skenario tes):** Menguji validasi cryptographic hash SHA-256 pada dataset beku, kelengkapan 24 bar lilin per hari kalender, kepositifan nilai RV, ketiadaan kebocoran fitur masa depan (*no future leakage*), sifat matematis penalti asimetris fungsi QLIKE, serta konsistensi uji Diebold-Mariano dan Bootstrap.
  2. **`tests/test_s2_calendar.py` (7 skenario tes):** Menguji penanganan celah kalender (*gap handling*) pada model baseline agar tidak melompati hari yang hilang secara kausal.
  3. **`tests/test_s2_split_scaler.py` (6 skenario tes):** Memverifikasi isolasi *scaler fitting* hanya pada subset pelatihan tiap fold dan penegakan *purge gap* antar-partisi deret waktu.
  4. **`tests/test_s2_analyze.py` (6 skenario tes):** Menguji keselarasan baris tanggal prediksi (*alignment validation*) sebelum uji statistik dijalankan.
  
  Seluruh 34 skenario tes ini dieksekusi secara berkala dan berhasil lulus 100% (*passed*) tanpa kegagalan, membuktikan bahwa pipeline komputasi kami solid, bebas kebocoran data, dan dapat dipertanggungjawabkan secara ilmiah."


## BAGIAN 5: MENGHADAPI PERTANYAAN JEBAKAN DOSEN (*TRICKY QUESTIONS*)

### Pertanyaan 21 (Jebakan 1): "Kenapa kamu tidak membuat aplikasi Android/Web-nya saja agar bisa dipakai langsung oleh masyarakat?"
* **🎯 Kata Kunci Hafalan:**
  **"Fokus skripsi ini adalah kontribusi saintifik pada keandalan engine komputasi peramalan. Membuat antarmuka aplikasi tanpa memastikan modelnya akurat dan bebas bias justru berbahaya bagi pengguna finansial."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Sesuai dengan **Batasan Masalah butir 7 di Bab I**, fokus penelitian skripsi ini murni diletakkan pada **kontribusi komputasional dan saintifik deret waktu**, yaitu memecahkan masalah keandalan peramalan non-linear, optimasi parameter Bayesian, dan integritas validasi bebas kebocoran data.  
  Membangun aplikasi antarmuka tanpa memastikan model peramalannya akurat dan bebas bias secara statistik justru akan menghasilkan sistem yang berbahaya bagi pengguna. Oleh karena itu, penelitian ini fokus menuntaskan modul peramalan inti (*core computation engine*)-nya terlebih dahulu. Pembuatan aplikasi antarmuka pengguna (*user interface*) telah kami rencanakan sebagai rekomendasi saran untuk penelitian lanjutan di Bab V."*

---

### Pertanyaan 22 (Jebakan 2): "Dari mana kamu mendapatkan data kline 1 jam Bitcoin? Apakah datanya resmi dan valid?"
* **🎯 Kata Kunci Hafalan:**
  **"Data resmi publik dari bursa Binance Vision, diverifikasi dengan checksum kriptografis SHA-256 pada seluruh 81 berkas bulanan, dan diaudit integritasnya melalui Amandemen A1."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Data diunduh langsung dari arsip publik resmi bursa Binance melalui repositori **Binance Vision** (`data.binance.vision`), yang merupakan standar data institusional bagi peneliti komputasi finansial global.  
  Sebanyak 81 berkas arsip bulanan (Januari 2020 s.d. September 2026) telah diverifikasi integritasnya menggunakan **kunci kriptografis SHA-256** (tercatat pada Lampiran 4 proposal). Selain itu, kami menerapkan Amandemen A1: seluruh hari observasi memiliki kelengkapan minimal 20 kline (83,3% kelengkapan), di mana hanya ada 1 hari cacat server bursa pada 19 Februari 2020 yang dieliminasi secara objektif sehingga didapatkan tepat 2.464 hari observasi bersih."*

---

### Pertanyaan 23 (Jebakan 3): "Kalau hasil pengujian nanti ternyata model LSTM kamu kalah dari HAR-RV, apakah skripsi kamu dianggap gagal?"
* **🎯 Kata Kunci Hafalan:**
  **"Tidak gagal. Nilai ilmiah skripsi terletak pada objektivitas metodologi yang sahih untuk menemukan kebenaran empiris, bukan memaksakan model harus menang."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Tidak, Bapak/Ibu. Dalam penelitian sains komputasi yang berintegritas tinggi, **tujuan utama penelitian adalah menemukan kebenaran empiris melalui metodologi yang sahih, bukan memaksakan model harus menang**.  
  Pada Tabel 3.5 naskah Bab III, kami telah mendefinisikan secara jujur kriteria keberhasilan eksperimen:
  * **Hasil Positif:** LSTM mengungguli seluruh model baseline secara signifikan ($p < 0{,}05$).
  * **Hasil Campuran:** LSTM mengalahkan model naif Persistence, namun setara atau bersaing ketat dengan HAR-RV. Ini tetap merupakan temuan ilmiah bernilai karena membuktikan kapasitas model deep learning non-linear dalam menyamai model ekonometrika frekuensi tinggi tanpa restriksi asumsi linier.
  * **Hasil Negatif:** Jika LSTM tidak mampu mengalahkan baseline, penelitian ini tetap memberikan kontribusi metodologis penting: membuktikan bahwa pada volatilitas kripto, kompleksitas deep learning rentan over-fitting dibandingkan formulasi autoregresif linier sederhana apabila data leakage dikendalikan secara ketat."*

---

### Pertanyaan 24 (Jebakan 4): "Apa jaminan bahwa eksperimen kamu bisa direproduksi ulang (*reproducible*) secara identik oleh orang lain atau penguji?"
* **🎯 Kata Kunci Hafalan:**
  **"Dijamin melalui 4 pilar: 5 random seed deterministik tetap, audit checksum SHA-256 data, penyimpanan jejak manifes log JSON/CSV, dan 34 automated unit test pytest yang lulus 100%."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Kami menjamin reproduktibilitas eksperimen melalui 4 pilar transparansi komputasi:
  1. **Determinisme Komputasi Penuh:** Seluruh inisialisasi benih acak (*random seeds*) pada level Python, NumPy, PyTorch/TensorFlow, dan Optuna dikunci deterministik menggunakan lima seed tetap: `(42, 123, 2024, 7, 99)`.
  2. **Audit Hash Data Kriptografis:** Seluruh berkas data mentah diverifikasi menggunakan ringkasan SHA-256 sehingga bit data identik 100%.
  3. **Penyimpanan Manifes Eksperimen:** Seluruh riwayat penalaan 50 trials Optuna, kurva kerugian per epoch, dan bobot akhir model disimpan dalam format standar terbuka (`.json`, `.csv`, `.pt`).
  4. **Uji Otomatis (*Automated Unit Testing*):** Repositori dilengkapi **34 pengujian unit terotomasi** menggunakan pustaka `pytest` yang telah berstatus lulus 100% (*all green tests*) untuk memvalidasi fungsi kalkulasi RV, scaling, dan loss QLIKE."*

---

### Pertanyaan 25 (Jebakan 5): "Apa batasan (limitasi) penelitian ini jika diterapkan di dunia nyata atau industri finansial?"
* **🎯 Kata Kunci Hafalan:**
  **"3 Batasan: Fokus pada point forecasting bukan sistem eksekusi perdagangan (*no slippage/fee*), data bursa tunggal Binance Spot, dan tidak memasukkan data sentimen berita atau on-chain."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Secara transparan kami mengakui 3 batasan masalah sebagaimana tercantum di Bab I:
  1. **Fokus pada Point Forecasting, Bukan Sistem Eksekusi:** Model ini dirancang khusus untuk meramalkan angka estimasi varians satu hari ke depan (*statistical point forecast*). Model ini belum mencakup simulasi eksekusi perdagangan riil (*backtesting*), biaya transaksi (*trading fee*), *slippage*, atau kedalaman order book.
  2. **Cakupan Bursa Tunggal (Single-Exchange):** Data diambil murni dari bursa Binance pasangan spot BTC/USDT. Meskipun Binance mewakili >50% likuiditas pasar kripto global, dinamika harga pada bursa terdesentralisasi (DEX) atau derivatif bisa memiliki sedikit disparitas harga.
  3. **Eksklusi Fitur Sentimen dan On-Chain:** Masukan dibatasi murni pada data pasar kausal mikrostruktur. Data sentimen berita atau *on-chain* tidak dimasukkan untuk menjaga objektivitas stempel waktu resolusi jam dan mencegah kebocoran temporal."*

---

### Pertanyaan 26 (Jebakan 6): "Di naskah tertulis deviasi gap = lookback + 1, kenapa ada tambahan plus 1?"
* **🎯 Kata Kunci Hafalan:**
  **"Tambahan +1 adalah buffer pengaman ekstra (*conservative design*) untuk memutus ketergantungan autokorelasi lag pertama antara sampel jendela geser terakhir data latih dan sampel pertama data validasi."**
* **🗣️ Jawaban Lisan ke Penguji:**
  *"Penambahan satu observasi (`+1`) pada purge gap sengaja kami tetapkan sebagai batas pengaman ekstra (*conservative buffer*) untuk memutus autokorelasi lag pertama antara sampel jendela geser terakhir data latih dan sampel pertama data validasi. Dengan menambahkan satu hari ekstra, kami menjamin secara ketat bahwa tidak ada irisan observasi masa depan yang menyusup ke masa lalu. Kami mencantumkan perbedaan ini secara transparan di Bab III sebagai bentuk kejujuran dokumentasi kode terhadap protokol teoretis."*

---

## BAGIAN 6: BEDAH TUNTAS RUMUS MATEMATIS & CARA BACA SIMBOL SECARA LISAN

### 1. Rumus Realized Variance (RV) & Imbal Hasil Intra-hari
$$r_{t,h} = \ln(C_{t,h}) - \ln(O_{t,h}), \quad \text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2, \quad \log RV_t = \ln(\text{RV}_t + 10^{-12})$$
* **Cara Membaca Simbolnya di Depan Dosen:**
  * $r_{t,h}$: *"r sub t koma h"* $\rightarrow$ Imbal hasil logaritmik hari ke-$t$ jam ke-$h$.
  * $\ln$: *"logaritma natural"* $\rightarrow$ Logaritma berbasis bilangan Euler $e$.
  * $C_{t,h}$: *"C sub t koma h"* $\rightarrow$ Harga penutupan (*closing price*) jam ke-$h$.
  * $O_{t,h}$: *"O sub t koma h"* $\rightarrow$ Harga pembukaan (*opening price*) jam ke-$h$.
  * $\text{RV}_t$: *"Realized Variance hari ke-t"*.
  * $\sum_{h=1}^{24}$: *"sigma penjumlahan dari h sama dengan 1 sampai 24 lilin satu jam"*.
  * $10^{-12}$: *"sepuluh pangkat minus dua belas"* $\rightarrow$ Konstanta stabilitas numerik (*machine epsilon*) agar fungsi $\ln$ tidak bernilai minus tak hingga jika RV bernilai nol.

---

### 2. Rumus Arsitektur Sel dan 3 Gerbang LSTM
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f), \quad i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i), \quad \tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$
$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t, \quad o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o), \quad h_t = o_t \odot \tanh(c_t)$$
* **Cara Membaca Simbolnya di Depan Dosen:**
  * $f_t$: *"f sub t"* $\rightarrow$ Gerbang lupa (*forget gate*).
  * $\sigma$: *"sigma"* $\rightarrow$ Fungsi aktivasi sigmoid logistik (rentang 0 s.d. 1; 0 = buang, 1 = simpan).
  * $W_f$: *"W sub f"* $\rightarrow$ Matriks bobot gerbang lupa.
  * $[h_{t-1}, x_t]$: *"konkatenasi vektor hidden state kemarin h sub t minus 1 dengan masukan baru x sub t hari ini"*.
  * $b_f$: *"b sub f"* $\rightarrow$ Vektor bias gerbang lupa.
  * $i_t$: *"i sub t"* $\rightarrow$ Gerbang masuk (*input gate*).
  * $\tilde{c}_t$: *"c-tilde sub t"* $\rightarrow$ Kandidat status sel baru hari ini.
  * $\tanh$: *"tangens hiperbolik"* $\rightarrow$ Fungsi modulasi non-linear rentang $[-1, +1]$.
  * $c_t$: *"c sub t"* $\rightarrow$ Status sel (*cell state*) hari ini (jalan tol memori jangka panjang).
  * $\odot$: *"Hadamard product atau perkalian elemen-per-elemen"* (bukan perkalian matriks biasa!).
  * $o_t$: *"o sub t"* $\rightarrow$ Gerbang keluar (*output gate*).
  * $h_t$: *"h sub t"* $\rightarrow$ Status tersembunyi (*hidden state*) hari ini yang diteruskan ke langkah berikutnya.

---

### 3. Rumus Fungsi Kerugian Asimetris QLIKE (Patton, 2011)
$$\text{QLIKE}(RV_t, \widehat{RV}_t) = \frac{RV_t}{\widehat{RV}_t} - \ln\left(\frac{RV_t}{\widehat{RV}_t}\right) - 1$$
* **Cara Membaca Simbolnya di Depan Dosen:**
  * $\text{QLIKE}(RV_t, \widehat{RV}_t)$: *"nilai kerugian QLIKE antara RV aktual RV sub t dengan ramalan RV-topi sub t"*.
  * $\frac{RV_t}{\widehat{RV}_t}$: *"rasio RV aktual dibagi RV prediksi"*.
  * $\ln\left(\frac{RV_t}{\widehat{RV}_t}\right)$: *"logaritma natural dari rasio RV aktual terhadap prediksi"*.
  * $- 1$: *"dikurangi satu (konstanta agar kerugian bernilai tepat 0 jika prediksi sempurna sama dengan aktual)"*.

---

### 4. Rumus Uji Diebold-Mariano & Koreksi HAC Newey-West
$$\text{DM} = \frac{\bar{d}}{\sqrt{\hat{V}(\bar{d}) / T}} \xrightarrow{d} \mathcal{N}(0, 1), \quad \hat{V}(\bar{d}) = \hat{\gamma}_0 + 2 \sum_{j=1}^{h-1} \left(1 - \frac{j}{h}\right) \hat{\gamma}_j$$
* **Cara Membaca Simbolnya di Depan Dosen:**
  * $\bar{d}$: *"d-bar"* $\rightarrow$ Rata-rata selisih kerugian peramalan antara baseline dan LSTM.
  * $\text{DM}$: *"statistik uji Diebold-Mariano"*.
  * $\hat{V}(\bar{d})$: *"V-topi dari d-bar"* $\rightarrow$ Taksiran varians jangka panjang Newey-West.
  * $\hat{\gamma}_j$: *"gamma-topi sub j"* $\rightarrow$ Autokovarians sampel pada lag ke-$j$.
  * $1 - \frac{j}{h}$: *"bobot kernel segitiga Bartlett pada lag j dengan horizon pemotongan h sama dengan 5"*.
  * $\xrightarrow{d} \mathcal{N}(0, 1)$: *"berkonvergensi dalam distribusi menuju normal baku standar rata-rata 0 varians 1"*.

---

## BAGIAN 7: PANDUAN LISAN MENJELASKAN DIAGRAM DI DEPAN PENGUJI

### 1. Cara Menjelaskan GAMBAR 2.1 (Arsitektur Sel & Aliran Informasi LSTM)
*(Tunjukkan gambar anatomi satu sel LSTM dengan jalur horizontal atas dan 4 kotak di tengah)*

> **Skrip Lisan:**  
> *"Bapak dan Ibu Dosen Penguji yang saya hormati, izin saya menguraikan Gambar 2.1 mengenai arsitektur sel LSTM dan dinamika aliran informasinya:*
> 
> *Di dalam satu sel LSTM pada langkah waktu $t$ terdapat dua jalur utama dan tiga gerbang logika penyaring:*
> 1. **Dua Masukan di Kiri Bawah ($x_t$ dan $h_{t-1}$):** Vektor fitur hari ini ($x_t$, berupa 6 fitur kausal kita) dan rekaman memori kemarin ($h_{t-1}$) digabungkan secara konkatenasi untuk disalurkan serentak ke gerbang-gerbang logika.
> 2. **Jalan Tol Memori di Atas (Cell State, $c_{t-1} \to c_t$):** Garis horizontal paling atas adalah *cell state* (jalan tol memori jangka panjang). Di sini gradien mengalir secara linier tanpa perkalian matriks berulang, sehingga LSTM bebas dari masalah *vanishing gradient*.
> 3. **Gerbang Lupa di Kiri ($f_t$):** Fungsi sigmoid ($\sigma$) menghasilkan nilai 0 sampai 1 yang dikalikan secara Hadamard ($\odot$) ke status sel lama ($c_{t-1}$) untuk memutuskan informasi usang mana yang harus dibuang.
> 4. **Gerbang Masuk & Kandidat di Tengah ($i_t$ dan $\tilde{c}_t$):** Sigmoid menyaring kepentingannya ($i_t$), fungsi $\tanh$ membuat kandidat informasi baru ($\tilde{c}_t$). Keduanya dikalikan lalu ditambahkan ($+$) ke jalan tol status sel untuk memperbarui memori menjadi $c_t$.
> 5. **Gerbang Keluar di Kanan ($o_t$ dan $h_t$):** Sigmoid menyaring informasi luaran ($o_t$), status sel $c_t$ dimodulasi lewat $\tanh$. Keduanya dikalikan untuk menghasilkan $h_t$ (status tersembunyi), yang dikeluarkan ke atas untuk menghasilkan prediksi $\log RV_{t+1}$ melalui lapisan Dense linier sekaligus diteruskan ke sel langkah berikutnya."*

---

### 2. Cara Menjelaskan GAMBAR 2.2 (Kerangka Pemikiran Konseptual Penelitian dengan Decision Loop)
*(Tunjukkan alur tahapan, belah ketupat keputusan/decision diamond, dan arah putaran feedback loop saat ditanya penguji)*

* **🎯 Kata Kunci Hafalan:**
  **"Alur kerangka pemikiran terdiri dari 6 tahap berurutan: dari perumusan masalah, pra-pemrosesan data frekuensi tinggi, partisi kronologis anti-leakage, penalaan Optuna dengan mekanisme umpan balik (feedback loop) jika validasi belum konvergen, pelatihan final, hingga uji hipotesis formal H0 vs H1."**

* **🗣️ Skrip Lisan Lengkap ke Penguji:**
  "Terima kasih Bapak/Ibu Penguji. Gambar 2.2 ini merangkum logika penelitian saya dari hulu ke hilir:
  1. **Kotak 1 (Masalah & Target):** Berangkat dari fenomena volatilitas Bitcoin yang sangat liar dan kegagalan model linier. Target ramalannya adalah $\log RV_{t+1}$ satu hari ke depan.
  2. **Kotak 2 (Data & Fitur):** Menggunakan data SPOT Binance Vision kline 1 jam periode 2020–2026 yang direkayasa menjadi 6 fitur teknikal kausal.
  3. **Kotak 3 (Partisi Temporal):** Data dibagi kronologis: Development 2020–2023 untuk penalaan HPO, Train Pool 2020–2025 untuk pelatihan final, dan Evaluasi Temporal 2026. Pemisahan dilindungi oleh *purge gap* ($lookback + 1$) agar tidak ada kebocoran autokorelasi serial.
  4. **Kotak 4 & Belah Ketupat Keputusan (Decision Diamond + Feedback Loop):**
     * Model usulan LSTM ditala menggunakan algoritma Bayesian Optuna (TPE) berbasis 5-fold Purged Cross-Validation.
     * **Jika ditanya loop-nya ke mana:** Pada belah ketupat keputusan, sistem mengevaluasi: *Apakah kriteria validasi dan konvergensi loss QLIKE sudah terpenuhi?*
     * **Jika TIDAK (Terjadi Overfit / Loss Belum Minimum):** Alur masuk ke panah merah **Feedback Loop (Umpan Balik)**, di mana Optuna TPE secara adaptif memperbarui model probabilitas Parzen dan mengeksplorasi kombinasi hyperparameter baru.
     * **Jika YA (Konvergen & Optimal):** Model melangkah ke **Pelatihan Model Final** pada Train Pool (90% fit, 10% early stopping).
  5. **Kotak 5 (Pengujian Evaluasi Temporal 2026):** Seluruh model (LSTM-Optuna vs 4 baseline pembanding) diuji pada 273 hari data 2026 menggunakan fungsi kerugian asimetris QLIKE (primer) serta MAE/RMSE (sekunder).
  6. **Kotak 6 (Uji Inferensial & Keputusan Hipotesis):** Menguji signifikansi komparatif menggunakan Uji Diebold–Mariano satu sisi berkoreksi HAC Newey–West dan Moving-Block Bootstrap untuk memutuskan penolakan $H_0$ dan penerimaan $H_1$."*

---

### 3. Cara Menjelaskan GAMBAR 3.1 (Alur Tahapan Penelitian Komputasional 8 Tahap)
*(Tunjukkan 8 kotak vertikal berurutan dari hulu ke hilir)*

> **Skrip Lisan:**  
> *"Gambar 3.1 menguraikan 8 tahapan metodologi komputasional eksperimen kami:
> 1. **Tahap 1 (Akuisisi Data):** Mengunduh 81 berkas bulanan kline 1 jam spot BTC/USDT dari Binance Vision (2020–2026).
> 2. **Tahap 2 (Audit & Prapemrosesan):** Audit integritas bar UTC dan menerapkan Amandemen A1 (eliminasi 1 hari cacat server 19 Feb 2020) menghasilkan 2.464 hari observasi terverifikasi dengan hash SHA-256.
> 3. **Tahap 3 (Target & Fitur Kausal):** Menghitung variabel target $\log RV_{t+1}$ dan 6 fitur kausal mikrostruktur tanpa *look-ahead bias*.
> 4. **Tahap 4 (Partisi Waktu):** Membagi dataset secara tegas: Development 2020–2023 (1.460 hari), Validation 2024–2025 (731 hari), dan Evaluasi Temporal 2026 (273 hari).
> 5. **Tahap 5 (Optimasi LSTM):** Menjalankan 50 trials penalaan Optuna TPE dan *MedianPruner* pada 5-fold Purged CV ber-jeda 10 hari dan scaler fold-specific.
> 6. **Tahap 6 (Pelatihan Final & Baseline):** Melatih arsitektur LSTM optimal dengan pemisahan 90% fit dan 10% early stopping pada Train Pool, serta mengimplementasikan 4 baseline pembanding.
> 7. **Tahap 7 (Evaluasi & Inferensi):** Menghitung loss QLIKE, menguji signifikansi selisih galat dengan Uji Diebold-Mariano HAC Newey-West lag 5, dan selang kepercayaan Bootstrap 10.000 repetisi.
> 8. **Tahap 8 (Pelaporan):** Melaporkan seluruh metrik performa, selisih kerugian, nilai-$p$, selang kepercayaan, serta keterbatasan penelitian secara transparan."*

---

## BAGIAN 8: CHEAT-SHEET ANGKA KUNCI SKRIPSI (HAFALKAN DI LUAR KEPALA!)

* **Rentang Waktu Data:** 1 Januari 2020 s.d. 30 September 2026 (81 bulan kalender).
* **Total Sampel Hari:** **2.464 hari observasi valid** (setelah eliminasi 1 hari cacat server 19 Feb 2020 via Amandemen A1).
* **Partisi Temporal:**
  * *Development Set* (Pelatihan CV): 2020–2023 (**1.460 hari / ~59,2%**).
  * *Validation Set* (Penalaan Optuna): 2024–2025 (**731 hari / ~29,7%**).
  * *Train Pool Gabungan:* 2020–2025 (**2.191 hari / ~88,9%**).
  * *Evaluasi Temporal Out-of-Sample:* 1 Jan – 30 Sep 2026 (**273 hari / ~11,1%**).
* **Fitur Masukan (6 Fitur Kausal):** $\log RV_t$, $\log range_t$, $\log volume_t$, $\log absret_t$, $\text{rv\_mean\_5}_t$, $\text{rv\_mean\_22}_t$.
* **Target Ramalan:** Nilai satu hari ke depan $\log RV_{t+1} = \ln(\text{RV}_{t+1} + 10^{-12})$.
* **Optimasi Optuna:** 50 *trials*, algoritma Bayesian TPE, pemangkas dini *MedianPruner* (`startup = 10`, `warmup = 2`).
* **Search Space Hyperparameter (6 Parameter):**
  * *Lookback window:* 10 s.d. 30 hari.
  * *Hidden units:* 16 s.d. 128 neuron.
  * *Layers:* 1 atau 2 lapisan LSTM.
  * *Dropout:* 0,05 s.d. 0,40 (langkah 0,05).
  * *Learning rate:* $3 \times 10^{-4}$ s.d. $2 \times 10^{-3}$ (skala logaritmik).
  * *Batch size:* 16, 32, atau 64 sampel.
* **Protokol Validasi:** 5-fold *Purged Rolling-Origin Cross-Validation* dengan *purge gap* 10 hari (`gap = lookback + 1`) dan scaler lokal fold-specific.
* **Model Pembanding (4 Baseline):** *Random Walk Persistence*, HAR-RV Corsi (2009), GARCH(1,1), LSTM *Untuned* (1 layer).
* **Evaluasi & Inferensi:**
  * Loss Primer: QLIKE (Patton, 2011) asimetris tahan derau.
  * Loss Sekunder: RMSE dan MAE.
  * Uji Asimtotik: Diebold-Mariano berkoreksi HAC Newey-West lag 5 ($p < 0{,}05$).
  * Uji Empiris: *Moving-Block Bootstrap* 10.000 repetisi (panjang blok 20 hari, interval 95%).
  * Pengendalian Stokastik: 5 seed acak deterministik `(42, 123, 2024, 7, 99)`.
* **Kualitas Kode & Integritas:** 34 pengujian unit otomatis (`pytest`) lulus 100%, verifikasi hash kriptografis SHA-256 dataset.
