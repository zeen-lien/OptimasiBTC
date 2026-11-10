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
> **Gunakan Formula 3 Langkah Menjawab:**
> 1. **Pernyataan Inti (*Direct Answer*):** Jawab pertanyaan dosen langsung pada pokok masalah dalam 1–2 kalimat tegas tanpa berputar-putar.
> 2. **Landasan Teori & Bukti Komputasi (*Scientific Evidence*):** Berikan argumentasi ilmiah, sitasi peneliti rujukan (misal: Patton, Corsi, Hochreiter, Bergstra, López de Prado), atau fakta komputasi/angka riil.
> 3. **Konklusi Pengunci (*Closing Statement*):** Tarik kembali ke tujuan spesifik skripsi kamu.
>
> **Hindari Penggunaan Kata:** *"Kayaknya"*, *"Mungkin"*, *"Kurang tahu"*, atau *"Coba-coba"*. Gantilah dengan *"Berdasarkan pengujian empiris"*, *"Merujuk pada penelitian rujukan..."*, atau *"Sesuai dengan batasan masalah yang telah ditetapkan..."*.

---

## BAGIAN 1: FONDASE, URGENSI, & MOTIVASI PENELITIAN

### Pertanyaan 1: "Coba jelaskan dengan singkat dan padat, penelitian kamu ini sebenarnya tentang apa?"
* **Jawaban Langsung:**
  "Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Penelitian ini berfokus pada **perancangan sistem komputasi cerdas untuk meramalkan tingkat risiko fluktuasi pasar atau *realized volatility* Bitcoin satu hari ke depan menggunakan model *deep learning* Long Short-Term Memory (LSTM)**. Agar performa model maksimal dan efisien, arsitektur LSTM ditala secara otomatis menggunakan algoritma optimasi Bayesian **Optuna (TPE)** dengan protokol **Purged Cross-Validation** guna menjamin eksperimen bebas dari kebocoran data temporal (*data leakage*)."
* **Poin Penguat:**
  * Objek: Data frekuensi tinggi Bitcoin (kline 1 jam) periode 2020–2026 dari Binance Vision.
  * Masalah utama: Ketidakpastian fluktuasi pasar kripto yang ekstrem dan kelemahan penalaan hyperparameter manual/acak pada LSTM.
  * Hasil akhir: Model peramalan yang terbukti akurat, objektif, dan teruji signifikansinya secara statistik.

---

### Pertanyaan 2: "Kenapa kamu memilih Bitcoin? Dan kenapa yang diprediksi adalah volatilitasnya (*realized volatility*), bukan memprediksi harga penutupannya langsung?"
* **Jawaban Langsung:**
  "Alasan pertama, Bitcoin adalah aset kripto dengan kapitalisasi pasar terbesar di dunia yang pasarnya beroperasi non-stop 24 jam sehari 7 hari seminggu tanpa jeda libur, sehingga memiliki tingkat risiko dan dinamika deret waktu yang sangat kompleks.  
  Alasan kedua dan yang paling fundamental: **memprediksi harga nominal penutupan (*closing price*) secara teoretis dan empiris terbukti mendekati lintasan acak (*random walk*)** dengan rasio *signal-to-noise* yang sangat rendah (sesuai Hipotesis Pasar Efisien Fama). Banyak peneliti komputer sebelumnya gagal mengalahkan model sederhana saat menebak harga.  
  Sebaliknya, **volatilitas atau besaran fluktuasi pasar terbukti memiliki sifat keteraturan statistik berupa pengelompokan volatilitas (*volatility clustering*) dan persistensi memori panjang** (Bollerslev, 1986; Andersen & Bollerslev, 1998). Periode varians tinggi cenderung saling berkelompok. Oleh karena itu, memprediksi volatilitas jauh lebih rasional, terukur secara ilmiah, dan sangat dibutuhkan industri keuangan digital untuk mitigasi risiko (*Value-at-Risk*) serta lindung nilai (*hedging*)."
* **Dasar Teori:**
  * Mandelbrot (1963) & Bollerslev (1986) mengenai *volatility clustering*.
  * Andersen et al. (2003) mengenai keunggulan proksi *Realized Variance*.

---

### Pertanyaan 3: "Apa urgensinya penelitian ini? Mengapa penelitian ini penting dan layak untuk diuji di tingkat skripsi Teknik Informatika?"
* **Jawaban Langsung:**
  "Urgensi penelitian ini terletak pada dua aspek:
  1. **Aspek Keilmuan Teknik Informatika:** Penerapan *deep learning* sekuensial pada data deret waktu masif membutuhkan disiplin komputasi yang ketat. Banyak penelitian terdahulu terjebak pada bias kebocoran data (*data leakage*) dan optimasi parameter *trial-and-error* yang memboroskan komputasi. Penelitian ini menyajikan standarisasi *pipeline* komputasi machine learning finansial yang utuh, efisien, dan dapat direproduksi secara penuh (*reproducible*).
  2. **Aspek Praktis Finansial Digital:** Fluktuasi ekstrem Bitcoin sering memicu likuidasi massal dana investor. Informasi ramalan volatilitas yang akurat berfungsi sebagai sistem peringatan dini (*early warning system*) bagi praktisi kuantitatif dan manajer risiko dalam mengukur batas toleransi risiko portofolio."
* **Poin Penguat:**
  * Skripsi ini bukan sekadar *running code*, melainkan memecahkan masalah metodologis nyata (*research gap*) dalam literatur sains data.

---

### Pertanyaan 4: "Apa bedanya penelitian kamu dengan penelitian-penelitian terdahulu yang juga membahas Bitcoin?"
* **Jawaban Langsung:**
  "Berdasarkan kajian sintesis terhadap 13 penelitian terdahulu (tercantum pada Tabel 2.1 naskah proposal), ada 4 perbedaan utama (*research gaps*) yang dijawab oleh penelitian ini:
  1. **Pergeseran Target:** Peneliti terdahulu mayoritas menargetkan harga acak penutupan. Penelitian ini menargetkan *Realized Variance* (RV) berbasis data frekuensi tinggi intra-hari 1 jam yang kaya informasi.
  2. **Protokol Anti-Kebocoran Data (*Anti-Data Leakage*):** Peneliti terdahulu banyak yang membagi data latih-uji secara acak atau normalisasi skala global. Penelitian ini menerapkan *5-fold Purged Cross-Validation* dengan jeda pemisah (*purge gap*) dan *fold-specific scaling*.
  3. **Optimasi Bayesian Otomatis:** Peneliti terdahulu menggunakan *manual tuning* atau *random search*. Penelitian ini menerapkan algoritma *Tree-structured Parzen Estimator* (TPE) dan *MedianPruner* dalam Optuna yang cerdas dan hemat daya komputasi.
  4. **Evaluasi Asimetris & Inferensi Formal:** Mengganti metrik simetris MSE yang bias dengan fungsi kerugian asimetris **QLIKE** (Patton, 2011) serta membuktikannya melalui Uji Diebold-Mariano berkoreksi HAC Newey-West dan *Moving-Block Bootstrap*."

---

### Pertanyaan 5: "Apa manfaat penelitian ini bagi mahasiswa dan institusi UNISNU?"
* **Jawaban Langsung:**
  * **Manfaat Teoretis:** Memperkaya riset komputasi deret waktu finansial di FST UNISNU, membuktikan adaptabilitas LSTM dan optimasi Bayesian Optuna pada domain volatilitas kripto.
  * **Manfaat Metodologis:** Menghasilkan standar baku eksperimen bebas kebocoran data yang dapat dijadikan rujukan oleh mahasiswa dan peneliti laboratorium informatika berikutnya.
  * **Manfaat Praktis:** Menghasilkan modul komputasi open-source terverifikasi untuk perhitungan volatilitas yang siap diintegrasikan pada sistem analitik keuangan digital.

---

## BAGIAN 2: NOVELTY (KEBARUAN PENELITIAN) & KONTRIBUSI ILMIAH

### Pertanyaan 6: "Apa NOVELTY (kebaruan) utama dari penelitian skripsi kamu dibanding ratusan paper LSTM dan Bitcoin yang sudah ada?"
* **Jawaban Langsung:**
  "Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Novelty utama penelitian ini terletak pada **Tri-Pilar Sinergi Metodologis Komputasi** yang membedakannya secara tegas dari mayoritas literatur skripsi maupun jurnal Informatika:
  1. **Novelty Target (Rekonseptualisasi Variabel Sasaran):** Mayoritas penelitian komputer meneliti harga penutupan (*closing price*) yang secara matematis merupakan *random walk*. Kami beralih ke variabel berakar ekonometrika kuat, yaitu *Realized Variance* (RV) berbasis agregasi kuadrat imbal hasil intra-hari 1 jam (Andersen et al., 2003) yang memiliki sifat *volatility clustering*.
  2. **Novelty Algoritmik (Optimasi Bayesian Bersyarat Dinamis):** Menggantikan penalaan subjektif *trial-and-error* atau *grid search* yang boros dengan algoritma **Optuna TPE (Tree-structured Parzen Estimator)** yang dilengkapi mekanisme pangkas dini **MedianPruner**, sehingga mampu mengotomasi penemuan arsitektur optimal secara probabilistik dan hemat sumber daya komputasi.
  3. **Novelty Integritas Metodologis & Inferensi Asimetris:** Mengatasi epidemi kebocoran data (*data leakage*) yang kerap diabaikan peneliti AI dengan menerapkan protokol ketat **Purged Rolling-Origin Cross-Validation (10-day gap)** dengan *fold-specific scaling*, serta mengevaluasi performa menggunakan fungsi kerugian asimetris **QLIKE** (Patton, 2011) yang tahan terhadap derau proksi, diperkuat uji signifikansi inferensial **Diebold-Mariano berkoreksi HAC Newey-West** dan **Moving-Block Bootstrap 10.000 sampel**."
* **Pernyataan Pengunci:**
  "Singkatnya, kebaruan kami bukan hanya 'mencoba LSTM pada data baru', melainkan menghadirkan **standarisasi metodologi komputasi deret waktu finansial yang bebas kebocoran data, teroptimasi secara cerdas, dan tervalidasi secara statistik inferensial formal**."

---

### Pertanyaan 7: "Kenapa kamu memakai model LSTM, kenapa tidak menggunakan arsitektur Transformer (seperti Informer, PatchTST) atau LLM yang lebih baru?"
* **Jawaban Langsung:**
  "Pertanyaan yang sangat kritis, Bapak/Ibu. Kami memilih arsitektur LSTM dengan 3 pertimbangan ilmiah dan komputasional yang matang:
  1. **Volume Data dan Risiko Over-Fitting (*Data Hunger*):** Dataset deret waktu harian kami berjumlah 2.464 hari observasi. Model Transformer (seperti Informer, PatchTST) memiliki puluhan hingga ratusan ribu bahkan jutaan parameter bebas yang membutuhkan jutaan token untuk konvergen. Menerapkan Transformer pada 2.464 baris data tabular harian sangat berisiko memicu *severe overfitting* dan menghafal derau pasar.
  2. **Bukti Empiris Literatur Terkini (Zeng et al., 2023):** Riset bergengsi oleh Zeng et al. (AAAI 2023) berjudul *'Are Transformers Effective for Time Series?'* membuktikan secara empiris bahwa pada data deret waktu kontinu univariat dan multivariat, arsitektur rekuren dan model linier sederhana seringkali mengungguli model Transformer yang over-parameterized. Mekanisme *self-attention* pada Transformer tidak memiliki urutan waktu intrinsik alami tanpa positional encoding, sedangkan rekursi LSTM secara inheren menjaga kontinuitas waktu (*inductive temporal bias*).
  3. **Prinsip Parsimoni (*Occam's Razor*):** Dalam sains komputer finansial, model yang lebih ramping, cepat dieksekusi, dan teroptimasi secara presisi melalui Bayesian TPE jauh lebih stabil dan andal untuk diterapkan (*production-ready*) dibandingkan model besar yang kompleks namun rapuh terhadap *regime shift* pasar."
* **Sitasi Kunci:** Zeng et al. (2023); Hochreiter & Schmidhuber (1997); Christensen et al. (2023).

---

### Pertanyaan 8: "Apa kontribusi teoretis, metodologis, dan praktis dari penelitian ini bagi keilmuan sains data dan informatika?"
* **Jawaban Langsung:**
  "1. **Kontribusi Teoretis:** Membuktikan secara empiris bahwa arsitektur jaringan saraf rekuren (LSTM) yang ditala secara adaptif oleh Optuna mampu memetakan dinamika varians non-linear dan *long-memory dependence* pada aset digital berkonsentrasi tinggi secara superior melampaui model linier autoregresif klasik.
  2. **Kontribusi Metodologis:** Menyajikan cetak biru (*blueprint*) pengujian deret waktu yang steril dari kebocoran data (*data leakage*) bagi komunitas sains data dan mahasiswa, melalui integrasi pemisahan kronologis murni, *purged cross-validation*, dan penyelarasan skala lokal (*fold-specific scaling*).
  3. **Kontribusi Praktis:** Menyediakan artefak perangkat lunak modular siap pakai (*production-grade code*) dengan 34 uji unit otomatis (*unit tests*) untuk ekstraksi RV dari *raw tick/hourly data*, penalaan model otomatis, dan komputasi metrik risiko yang siap diadopsi oleh praktisi perbankan digital, manajer investasi aset kripto, maupun peneliti laboratorium komputasi."

---

## BAGIAN 3: KARAKTERISTIK DATA, REKAYASA FITUR, & ANOMALI PASAR

### Pertanyaan 9: "Apa itu Realized Variance (RV) dan kenapa harus ditransformasi ke bentuk logaritma ($\log RV$)?"
* **Jawaban Langsung:**
  * **Realized Variance (RV):** Volatilitas pasar adalah variabel laten (tidak tampak langsung pada data harian). Oleh karena itu, kita mengukurnya menggunakan *Realized Variance*, yaitu penjumlahan kuadrat return harga intra-hari 1 jam dari 24 lilin (*candlestick bars*) sepanjang satu hari UTC:
    $$\text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2, \quad \text{di mana } r_{t,h} = \ln(C_{t,h}) - \ln(O_{t,h})$$
  * **Alasan Transformasi Logaritma:**
    Data empiris RV memiliki nilai yang selalu positif, tetapi memiliki kemencengan (*skewness*) ekstrem dan ekor tebal (*heavy tails*) akibat lonjakan pasar. Dengan menerapkan transformasi logaritmik:
    $$\log RV_t = \ln(RV_t + 10^{-12})$$
    sebaran data menjadi jauh lebih simetris mendekati distribusi normal (Gaussian), mengeliminasi risiko prediksi bernilai negatif saat dikembalikan melalui eksponensial, dan mempermudah konvergensi proses optimasi gradien pada jaringan saraf tiruan.

---

### Pertanyaan 10: "Mengapa kamu memilih 6 fitur teknikal masukan ini? Dari mana dasar teorinya dan kenapa tidak menggunakan indikator populer seperti RSI atau MACD?"
* **Jawaban Langsung:**
  "Keenam fitur masukan dipilih berdasarkan **landasan teori ekonometrika mikrostruktur pasar dan heterogenitas pelaku pasar**, bukan asal comot:
  1. $\log RV_t$: Menangkap komponen autokorelasi langsung dan persistensi volatilitas harian jangka pendek.
  2. $\log range_t = \ln(H_t - L_t)$: Berbasis estimator volatilitas Parkinson (1980), menangkap dispersi harga ekstrem tertinggi-terendah harian tanpa terdistorsi oleh arah return penutupan.
  3. $\log volume_t = \ln(V_t)$: Berlandaskan teori *Mixture of Distribution Hypothesis* (MDH; Clark, 1973) yang menyatakan volume perdagangan berbanding lurus dengan laju kedatangan informasi baru dan intensitas volatilitas.
  4. $\log absret_t = \ln(|r_t| + 10^{-6})$: Mengukur magnitudo goncangan harga harian (*absolute daily price shock*) tanpa memedulikan arah pergerakan positif/negatif.
  5. $\text{rv\_mean\_5}_t$: Berbasis kerangka model HAR-RV (Corsi, 2009), menangkap rata-rata volatilitas mingguan (5 hari kerja pasar) yang mencerminkan horizon investasi jangka menengah.
  6. $\text{rv\_mean\_22}_t$: Menangkap rata-rata volatilitas bulanan (22 hari kalender pasar keuangan) yang merefleksikan horizon investor institusional jangka panjang.
  
  **Kenapa TIDAK Menggunakan Indikator Seperti RSI, MACD, atau Bollinger Bands?**  
  Karena indikator teknikal konvensional dirancang untuk memprediksi **arah tren harga (*trend/momentum*)**, memiliki keterlambatan waktu (*lagging indicator*) akibat perataan ganda (*smoothing*), dan menimbulkan multikolinearitas tinggi. Sementara target kita adalah **dispersi risiko (volatilitas)**. Keenam fitur kausal yang kami gunakan sepenuhnya bebas dari *look-ahead bias*, steril dari noise arah harga, dan memiliki korelasi struktural langsung terhadap dinamika varians."
* **Sitasi Kunci:** Andersen & Bollerslev (1998); Corsi (2009); Parkinson (1980); Clark (1973).

---

### Pertanyaan 11: "Bagaimana penanganan integritas data dan anomali data (kline hilang, server glitch Binance, dan kelengkapan data)?"
* **Jawaban Langsung:**
  "Kami menerapkan protokol audit kualitas data yang sangat ketat melalui 3 mekanisme:
  1. **Audit Checksum Kriptografis SHA-256:** Seluruh 81 berkas arsip bulanan (Januari 2020 s.d. September 2026) dari Binance Vision di-verifikasi integritas hash SHA-256-nya sebelum diproses (tercantum pada Lampiran 4 proposal), menjamin data tidak terkorupsi atau dimodifikasi pihak ketiga.
  2. **Amandemen A1 (Pembersihan Cacat Bursa):** Dari total 2.465 hari kalender, Binance mengalami insiden downtime pemeliharaan server tak terjadwal pada **19 Februari 2020**, di mana hanya tercatat 1 lilin data (kelengkapan 4,2%). Kami menerapkan aturan objektif: setiap hari observasi wajib memiliki minimal 20 kline (kelengkapan $\ge 83{,}3\%$). Oleh karena itu, hari anomali 19 Februari 2020 dieliminasi secara objektif sehingga total sampel akhir adalah tepat **2.464 hari observasi penuh**.
  3. **Imputasi Non-Lookahead untuk Cacat Parsial:** Apabila ada hari dengan 20–23 kline (cacat minor 1–4 jam), harga penutupan jam sebelumnya di-imputasi (*forward fill*) tanpa pernah menyalin data jam masa depan, sehingga integritas kausalitas waktu terjaga 100%."

---

### Pertanyaan 12: "Bagaimana model kamu menghadapi fenomena 'Black Swan' atau lonjakan volatilitas ekstrem (seperti Crash Covid 2020 atau kejatuhan FTX 2022)?"
* **Jawaban Langsung:**
  "Penelitian ini secara sengaja mencakup rentang waktu 2020 hingga 2026 justru untuk menguji ketahanan model terhadap berbagai siklus ekstrem pasar (*stress test*):
  1. **Fitur Responsif Cepat:** Indikator shock harian $\log absret_t$ dan rentang dispersi $\log range_t$ segera melonjak secara simultan ketika terjadi crash pasar, langsung memberikan input sinyal bahaya ke memori sel LSTM pada langkah $t$.
  2. **Stabilisasi Logaritmik:** Transformasi logaritma $\log RV$ mengompresi lonjakan varians ekstrem dari skala eksponensial menjadi linier, mencegah fenomena ledakan gradien (*exploding gradient*) saat bobot jaringan saraf diperbarui.
  3. **Fungsi Rugi Asimetris QLIKE:** Saat terjadi crash pasar, kesalahan berupa peramalan risiko yang terlalu rendah (*under-forecasting*) akan dihukum secara eksponensial oleh loss function QLIKE, memaksa model untuk memprioritaskan keamanan prediksi pada fase pasar berisiko tinggi.
  4. **Uji Validasi Out-of-Sample 2026:** Kami menguji performa model pada data uji out-of-sample tahun 2026 yang memiliki rezim pasca-ETF dan siklus Halving baru, untuk membuktikan bahwa model tidak 'kaget' atau runtuh performanya saat menghadapi dinamika pasar terkini."

---

## BAGIAN 4: ARSITEKTUR MODEL & ALGORITMA OPTIMASI OPTUNA

### Pertanyaan 13: "Bisa jelaskan arsitektur LSTM, cara kerja sel LSTM, dan fungsi masing-masing gerbangnya secara intuitif?"
* **Jawaban Langsung:**
  "Bisa, Bapak/Ibu. Arsitektur sel LSTM bekerja persis seperti mekanisme kerja memori manusia yang memiliki filter penyaring informasi melalui 4 tahapan berurutan:
  1. **Gerbang Lupa (*Forget Gate*, $f_t$):** Bertindak sebagai penghapus memori. Ia memeriksa masukan baru ($x_t$) dan status sebelumnya ($h_{t-1}$), lalu memutuskan: *'Informasi volatilitas masa lalu mana yang sudah usang dan harus dibuang?'* (Output 0 berarti buang total, 1 berarti pertahankan penuh).
     $$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$
  2. **Gerbang Masuk (*Input Gate*, $i_t$):** Bertindak sebagai penyeleksi informasi baru. Ia memutuskan informasi fluktuasi hari ini mana yang cukup penting untuk dicatat. Bersamaan dengan itu dibuat kandidat memori baru ($\tilde{c}_t$).
     $$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i), \quad \tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$
  3. **Pembaruan Status Sel (*Cell State Update*, $c_t$):** Ini adalah 'buku catatan memori jangka panjang'. Memori lama yang sudah disaring dikalikan dengan gerbang lupa, lalu ditambahkan informasi baru dari gerbang masuk:
     $$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$
  4. **Gerbang Keluar (*Output Gate*, $o_t$):** Memutuskan informasi apa yang akan dikeluarkan sebagai proyeksi *hidden state* ($h_t$), yang kemudian dipetakan oleh lapisan linear menjadi ramalan volatilitas satu langkah ke depan ($\log RV_{t+1}$):
     $$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o), \quad h_t = o_t \odot \tanh(c_t)$$
  Melalui jalan tol gradien pada *cell state*, LSTM mampu mempertahankan memori deret waktu puluhan hari ke belakang tanpa mengalami *vanishing gradient*."

---

### Pertanyaan 14: "Mengapa kamu menggunakan algoritma Optuna untuk optimasi hyperparameter? Kenapa tidak pakai Grid Search atau Random Search yang lebih lazim?"
* **Jawaban Langsung:**
  "1. **Kelemahan Grid Search:** Grid Search melakukan evaluasi pada semua titik kombinasi secara kaku. Jika kita punya 6 parameter dengan kombinasi ribuan titik, waktu komputasi akan meledak secara eksponensial (*curse of dimensionality*).  
  2. **Kelemahan Random Search:** Random Search memilih kombinasi secara acak tanpa belajar dari hasil uji coba sebelumnya, sehingga membuang-buang daya komputasi pada wilayah parameter yang buruk.  
  3. **Keunggulan Optuna (TPE):** Optuna menerapkan algoritma *Tree-structured Parzen Estimator* (TPE) berbasis optimasi Bayesian. TPE memodelkan probabilitas konfigurasi masa lalu yang menghasilkan skor baik vs skor buruk:
     $$p(x|y) = \begin{cases} \ell(x) & \text{jika } y < y^* \\ g(x) & \text{jika } y \ge y^* \end{cases}$$
  Dari riwayat tersebut, Optuna secara cerdas dan adaptif mengarahkan *trial* berikutnya ke ruang parameter yang memaksimalkan rasio $\ell(x)/g(x)$. Hasil riset Bergstra et al. membuktikan TPE menemukan kombinasi optimal jauh lebih cepat dibandingkan random search."
* **Sitasi Kunci:** Bergstra et al. (2011); Akiba et al. (2019).

---

### Pertanyaan 15: "Apa itu MedianPruner dalam Optuna dan bagaimana mekanisme kerjanya?"
* **Jawaban Langsung:**
  "**MedianPruner adalah algoritma pemangkasan dini (*early stopping / pruning*) pada Optuna.**  
  Cara kerjanya: Saat sebuah *trial* arsitektur LSTM sedang dilatih pada suatu epoch awal, Optuna memeriksa nilai kerugian validasinya. Jika nilai kerugian tersebut ternyata lebih buruk daripada nilai median dari *trial-trial* sebelumnya pada epoch yang sama, Optuna akan langsung menghentikan (*pruning*) pelatihan model tersebut tanpa harus menunggu sampai epoch ke-100 selesai.  
  Fungsinya adalah menghemat waktu dan sumber daya komputasi secara drastis (hingga 50–70% penghematan waktu eksekusi), sehingga alokasi waktu dapat difokuskan untuk mengeksplorasi kandidat arsitektur lain yang lebih potensial."
* **Catatan Parameter:** Eksperimen kita menggunakan `n_startup_trials = 10` (10 trial pertama dibiarkan selesai tanpa dipangkas untuk membentuk baseline median yang stabil) dan `n_warmup_steps = 2` (memberi waktu pemanasan minimal 2 epoch sebelum dipangkas).

---

### Pertanyaan 16: "Hyperparameter apa saja yang ditala dan bagaimana kamu menetapkan batas ruang pencarian (search space)-nya? Apakah ditentukan asal-asalan?"
* **Jawaban Langsung:**
  "Batas ruang pencarian (*search space*) sebanyak 50 *trials* ditetapkan **berdasarkan tinjauan literatur empiris (*empirical domain boundaries*) dan konstrain komputasi**, sama sekali bukan asal tebak:
  1. *Lookback window* [10 s.d. 30 hari]: Merujuk pada riset Kervancı (2023) dan siklus kalender pasar keuangan (22 hari kerja / 30 hari kalender). Jendela di bawah 10 hari kehilangan memori komponen mingguan, sedangkan di atas 30 hari menimbulkan penumpukan derau masa lalu (*fading memory*) yang merusak estimasi volatilitas terkini.
  2. Jumlah neuron / *hidden units* [16 s.d. 128 neuron]: Berdasarkan studi berskala besar Greff et al. (2017). Untuk 6 fitur masukan, kapasitas 16–128 adalah batas ideal untuk mencegah *underfitting* (jika < 16) dan mencegah *memorization/overfitting* (jika > 128).
  3. Jumlah lapisan LSTM / *layers* [1 atau 2 lapisan]: Pada deret waktu berdimensi rendah, penumpukan lebih dari 2 lapisan LSTM menyebabkan hilangnya efisiensi gradien dan komputasi membengkak tanpa peningkatan akurasi bermakna.
  4. *Dropout rate* [0,05 s.d. 0,40, langkah 0,05]: Mengikuti rekomendasi regularisasi jaringan rekuren oleh Srivastava et al. (2014) untuk mencegah ketergantungan ko-adaptasi antar-neuron.
  5. *Learning rate* Adam [$3 \times 10^{-4}$ s.d. $2 \times 10^{-3}$, skala logaritmik]: Rentang standar optimizer Adam (Kingma & Ba, 2014) untuk memastikan kestabilan penurunan gradien tanpa meledak (*exploding gradient*).
  6. Ukuran *batch* / *batch size* [16, 32, atau 64 sampel]: Mengendalikan variabilitas stokastik pembaruan bobot dalam memori GPU/CPU."

---

## BAGIAN 5: METODOLOGI VALIDASI, ANTI-DATA LEAKAGE, & STATISTIK INFERENSIAL

### Pertanyaan 17: "Apa yang dimaksud dengan kebocoran data (*data leakage*) pada deret waktu dan bagaimana kamu membuktikan penelitian kamu bebas kebocoran data?"
* **Jawaban Langsung:**
  "**Kebocoran data (*data leakage*) adalah kondisi cacat metodologis fatal di mana informasi masa depan (*future information*) secara sengaja atau tidak sengaja menyusup ke dalam proses pelatihan masa lalu (*look-ahead bias*), sehingga menghasilkan performa semu yang tampak hebat di atas kertas tetapi langsung gagal saat diuji di dunia nyata.**  
  Penelitian ini menerapkan **4 lapis benteng pencegahan kebocoran data**:
  1. **Partisi Temporal Kronologis Murni:** Data dipecah berdasarkan urutan waktu kalender, bukan diacak: Development (2020–2023), Validation (2024–2025), dan Test Out-of-Sample (1 Januari – 30 September 2026).
  2. **Skema Purged Cross-Validation:** Pada setiap lipatan (*fold*), disisipkan jeda pemisah (*purge gap*) selama 10 hari antara data latih dan data validasi untuk memutus ketergantungan serial antar-sampel jendela geser (*sliding window*).
  3. **Fold-Specific Scaling:** Normalisasi `StandardScaler` dihitung murni dari nilai mean dan deviasi standar data latih pada masing-masing fold. Nilai skala tersebut baru diaplikasikan ke data validasi tanpa pernah menghitung scaler global di awal.
  4. **Isolasi Penuh Data Uji 2026:** Data uji eksternal 2026 dikunci total dan tidak pernah disentuh dalam proses optimasi hyperparameter Optuna maupun pemilihan model."
* **Sitasi Kunci:** Marcos López de Prado (2018) — *Advances in Financial Machine Learning*.

---

### Pertanyaan 18: "Kenapa evaluasi utamanya memakai fungsi kerugian QLIKE, bukan MSE atau MAE? Bagaimana bukti matematis keunggulan penalti asimetrisnya?"
* **Jawaban Langsung:**
  "Karena **volatilitas aktual adalah variabel laten yang diestimasi menggunakan proksi (*realized variance*) yang berderau (*noisy proxy*)**.  
  Penelitian ekonometrika terkemuka oleh **Patton (2011)** membuktikan secara matematis bahwa fungsi kerugian simetris konvensional seperti MSE tidak tahan terhadap derau proksi dan dapat menghasilkan perankingan model yang bias/salah.  
  Sebaliknya, **QLIKE (*Quasi-Likelihood*) terbukti mathematically robust**: perankingan model di bawah QLIKE konsisten sama apakah dihitung terhadap volatilitas laten murni maupun terhadap proksi berderau.
  
  **Bukti Keunggulan Penalti Asimetris:**
  Formula QLIKE didefinisikan sebagai:
  $$\text{QLIKE}(RV, \widehat{RV}) = \frac{RV}{\widehat{RV}} - \ln\left(\frac{RV}{\widehat{RV}}\right) - 1$$
  Misalkan volatilitas aktual $RV = 0{,}10$:
  * **Model A (*Under-forecast* sebesar 0,05; $\widehat{RV} = 0{,}05$):**  
    Rasio $RV / \widehat{RV} = 2{,}0$.  
    $\text{QLIKE} = 2{,}0 - \ln(2{,}0) - 1 = 1{,}0 - 0{,}693 = \mathbf{0{,}307}$.
  * **Model B (*Over-forecast* sebesar 0,05; $\widehat{RV} = 0{,}15$):**  
    Rasio $RV / \widehat{RV} = 0{,}667$.  
    $\text{QLIKE} = 0{,}667 - \ln(0{,}667) - 1 = -0{,}333 - (-0{,}405) = \mathbf{0{,}072}$.
  
  Pada metrik MSE, kedua model di atas dianggap menghasilkan galat yang sama persis: $(0{,}10 - 0{,}05)^2 = (0{,}10 - 0{,}15)^2 = 0{,}0025$. Namun pada QLIKE, kesalahan *under-forecasting* (Model A) dihukum dengan penalti $\mathbf{0{,}307}$, yaitu **lebih dari 4 kali lipat lebih berat** dibanding kesalahan *over-forecasting* (Model B) yang hanya bernilai $\mathbf{0{,}072}$. Dalam manajemen risiko finansial, meremehkan volatilitas (*under-forecast*) berakibat fatal karena dapat memicu kebangkrutan modal dan likuidasi margin call."
* **Sitasi Kunci:** Patton, A. J. (2011). *Data-based ranking of volatility models*. Journal of Econometrics.

---

### Pertanyaan 19: "Apa saja model pembanding (*baseline*) yang kamu gunakan dan apa fungsinya masing-masing?"
* **Jawaban Langsung:**
  "Penelitian ini membandingkan model usulan (LSTM-Optuna) terhadap **4 model baseline bertingkat**:
  1. **Random Walk Persistence (Baseline Naif):** Asumsi sederhana bahwa volatilitas besok sama persis dengan volatilitas hari ini. Ini adalah *sanity check* paling mendasar: jika model deep learning gagal mengalahkan model naif ini, maka model tersebut secara ilmiah tidak layak dipakai.
  2. **HAR-RV Corsi (2009) (Baseline Ekonometrika Frekuensi Tinggi):** Model regresi linier standar industri yang memanfaatkan rata-rata volatilitas harian, mingguan (5 hari), dan bulanan (22 hari).
  3. **GARCH(1,1) (Baseline Ekonometrika Klasik):** Model varians bersyarat konvensional berbasis imbal hasil harian yang diestimasi dengan skema *expanding window*.
  4. **LSTM Untuned (Baseline Deep Learning Heuristik):** Arsitektur LSTM dengan konfigurasi default umum tanpa bantuan Optuna. Fungsinya adalah untuk membuktikan secara empiris bahwa peningkatan akurasi benar-benar dihasilkan oleh optimasi Bayesian Optuna, bukan semata-mata karena algoritma LSTM-nya."

---

### Pertanyaan 20: "Bagaimana kamu membuktikan bahwa keunggulan model LSTM-Optuna bukan faktor kebetulan (*stochastic fluke*)?"
* **Jawaban Langsung:**
  "Keunggulan model tidak hanya dinilai dari selisih angka rata-rata metrik, melainkan dibuktikan melalui **tiga lapisan uji statistik inferensial formal**:
  1. **Uji Diebold-Mariano (1995) dengan Koreksi HAC Newey-West:** Menguji secara asimtotik apakah selisih kerugian peramalan ($d_t = L_{\text{baseline}} - L_{\text{LSTM}}$) bernilai positif secara signifikan dengan nilai-$p < 0{,}05$. Estimator HAC Newey-West dengan lag 5 digunakan untuk mengoreksi autokorelasi dan heteroskedastisitas pada deret galat.
  2. **Moving-Block Bootstrap (10.000 Repetisi):** Mengonstruksi selang kepercayaan empiris 95% untuk selisih kerugian yang mempertahankan struktur ketergantungan temporal runtun waktu (Künsch, 1989). Model LSTM-Optuna terbukti unggul kokoh jika batas atas interval bootstrap 95% berada di bawah nol.
  3. **Protokol Multi-Seed (5 Seed):** Mengendalikan variabilitas acak akibat inisialisasi bobot jaringan saraf dengan melatih model menggunakan lima benih acak yang ditetapkan apriori: `(42, 123, 2024, 7, 99)`, lalu melaporkan rata-rata dan deviasi standarnya."

---

### Pertanyaan 21: "Apa itu Uji Diebold-Mariano dan kenapa harus menggunakan koreksi HAC Newey-West?"
* **Jawaban Langsung:**
  "**Uji Diebold-Mariano (DM)** adalah uji hipotesis statistik formal untuk membandingkan akurasi peramalan antara dua model deret waktu yang bersaing dengan menguji signifikansi selisih kerugian (*differential loss*):
  $$d_t = L(y_t, \hat{y}_{\text{baseline}, t}) - L(y_t, \hat{y}_{\text{LSTM}, t})$$
  Hipotesis nol ($H_0$) menyatakan bahwa kedua model memiliki akurasi yang sama ($\mathbb{E}[d_t] = 0$).
  
  **Mengapa Harus Menggunakan Koreksi HAC Newey-West?**  
  Pada data deret waktu finansial, deret galat peramalan ($d_t$) hampir selalu memiliki masalah autokorelasi serial dan varians yang berubah-ubah seiring waktu (*heteroskedasticity*).  
  Jika kita mengujinya menggunakan uji t-Student biasa tanpa koreksi, varians sampel akan ter-distorsi terlalu kecil (*underestimated*). Akibatnya, nilai t-hitung membengkak secara semu dan memicu penolakan hipotesis nol secara keliru (terjadi galat *Type I error* / *False Discovery*).  
  Estimator **HAC (Heteroskedasticity and Autocorrelation Consistent) Newey-West** dengan lag $h=5$ menyisipkan matriks bobot kernel Bartlett untuk mengoreksi autokorelasi galat hingga lag ke-5, sehingga nilai *p-value* yang dihasilkan terjamin valid, objektif, dan dapat dipertanggungjawabkan secara asimtotik."
* **Sitasi Kunci:** Diebold & Mariano (1995); Newey & West (1987).

---

## BAGIAN 6: MENGHADAPI PERTANYAAN JEBAKAN DOSEN PENGUJI (*TRICKY QUESTIONS*)

### Pertanyaan 22 (Jebakan 1): "Kenapa kamu tidak membuat aplikasi Android/Web-nya saja agar bisa dipakai langsung oleh masyarakat?"
* **Cara Menjawab:**
  *"Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Sesuai dengan **Batasan Masalah butir 7 di Bab I**, fokus penelitian skripsi ini murni diletakkan pada **kontribusi komputasional dan saintifik deret waktu**, yaitu memecahkan masalah keandalan peramalan non-linear, optimasi parameter Bayesian, dan integritas validasi bebas kebocoran data.  
  Membangun aplikasi antarmuka tanpa memastikan model peramalannya akurat dan bebas bias secara statistik justru akan menghasilkan sistem yang berbahaya bagi pengguna. Oleh karena itu, penelitian ini fokus menuntaskan modul peramalan inti (*core computation engine*)-nya terlebih dahulu. Pembuatan aplikasi antarmuka pengguna (*user interface*) dan integrasi sistem perdagangan otomatis telah kami rencanakan sebagai rekomendasi saran untuk penelitian lanjutan di Bab V."*

---

### Pertanyaan 23 (Jebakan 2): "Dari mana kamu mendapatkan data kline 1 jam Bitcoin? Apakah datanya resmi dan valid?"
* **Cara Menjawab:**
  *"Data diunduh langsung dari arsip publik resmi bursa Binance melalui repositori **Binance Vision** (`data.binance.vision`), yang merupakan repositori data historis terstandarisasi institusional yang digunakan oleh peneliti komputasi finansial global.  
  Sebanyak 81 berkas arsip bulanan (Januari 2020 s.d. September 2026) telah diverifikasi integritasnya menggunakan **kunci kriptografis SHA-256** (tercatat pada Lampiran 4 proposal). Selain itu, kami melakukan audit stempel waktu UTC dan menerapkan Amandemen A1: seluruh hari observasi memiliki kelengkapan minimal 20 kline (83,3% kelengkapan), di mana hanya ada 1 hari cacat server bursa pada 19 Februari 2020 yang memiliki 1 kline sehingga dieliminasi secara objektif."*

---

### Pertanyaan 24 (Jebakan 3): "Kalau hasil pengujian nanti ternyata model LSTM kamu kalah dari HAR-RV, apakah skripsi kamu dianggap gagal?"
* **Cara Menjawab:**
  *"Tidak, Bapak/Ibu. Dalam penelitian sains komputasi yang berintegritas tinggi, **tujuan utama penelitian adalah menemukan kebenaran empiris melalui metodologi yang sahih, bukan memaksakan model harus menang dengan cara memanipulasi data**.  
  Pada Tabel 3.5 naskah Bab III, kami telah mendefinisikan secara jujur kriteria keberhasilan eksperimen:
  * **Hasil Positif:** LSTM mengungguli seluruh model baseline secara signifikan ($p < 0{,}05$).
  * **Hasil Campuran:** LSTM mengalahkan model naif Persistence, namun setara atau bersaing ketat dengan HAR-RV. Ini tetap merupakan temuan ilmiah yang sangat bernilai karena membuktikan kapasitas model deep learning non-linear dalam menyamai model ekonometrika frekuensi tinggi tanpa restriksi asumsi linier.
  * **Hasil Negatif:** Jika LSTM tidak mampu mengalahkan baseline, penelitian ini tetap memberikan kontribusi metodologis penting: membuktikan bahwa pada volatilitas kripto, kompleksitas deep learning rentan over-fitting dibandingkan formulasi autoregresif linier sederhana apabila data leakage dikendalikan secara ketat. Jadi, nilai ilmiah skripsi terletak pada objektivitas dan kekuatan metodologinya."*

---

### Pertanyaan 25 (Jebakan 4): "Apa jaminan bahwa eksperimen kamu bisa direproduksi ulang (*reproducible*) secara identik oleh orang lain atau penguji?"
* **Cara Menjawab:**
  *"Kami menjamin reproduktibilitas eksperimen melalui 4 pilar transparansi komputasi:
  1. **Determinisme Komputasi Penuh:** Seluruh inisialisasi benih acak (*random seeds*) pada level lingkungan Python (`random`), NumPy (`np.random`), PyTorch/TensorFlow, serta algoritma Optuna dikunci secara deterministik menggunakan lima seed tetap: `(42, 123, 2024, 7, 99)`.
  2. **Audit Hash Data Kriptografis:** Seluruh berkas data masukan mentah dan prapemrosesan diverifikasi menggunakan fungsi ringkasan SHA-256 sehingga integritas bit data identik 100%.
  3. **Penyimpanan Jejak Audit Eksperimen:** Seluruh riwayat penalaan 50 trials Optuna, parameter terbaik, nilai loss kurva per epoch, dan bobot akhir model disimpan dalam format standar terbuka (`.json`, `.csv`, `.pt`).
  4. **Uji Otomatis (*Automated Unit Testing*):** Repositori skripsi dilengkapi dengan **34 pengujian unit terotomasi** menggunakan pustaka `pytest` yang telah berstatus lulus 100% (*all green tests*) untuk memverifikasi fungsi pembentukan fitur, kalkulasi RV, fungsi rugi QLIKE, dan protokol purged CV."*

---

### Pertanyaan 26 (Jebakan 5): "Apa batasan (limitasi) penelitian ini jika diterapkan di dunia nyata atau industri finansial?"
* **Cara Menjawab:**
  *"Sebagai peneliti yang objektif, kami secara transparan mengakui 3 batasan (*limitations*) penelitian ini sebagaimana tercantum pada Batasan Masalah Bab I:
  1. **Fokus pada Point Forecasting, Bukan Sistem Eksekusi:** Model ini dirancang khusus untuk meramalkan angka estimasi varians satu hari ke depan (*statistical point forecast*). Model ini belum mencakup simulasi eksekusi perdagangan riil (*backtesting execution*), biaya transaksi (*trading fee*), *slippage*, atau kedalaman buku pesanan (*order book depth*).
  2. **Cakupan Bursa Tunggal (Single-Exchange):** Data diambil murni dari bursa Binance pasangan spot BTC/USDT. Meskipun Binance mewakili lebih dari 50% likuiditas pasar kripto global, dinamika harga pada bursa terdesentralisasi (DEX) atau instrumen derivatif bisa memiliki sedikit disparitas harga.
  3. **Eksklusi Fitur Sentimen dan On-Chain:** Penelitian ini membatasi masukan murni pada fitur data pasar kausal mikrostruktur. Data sentimen berita media sosial atau metrik *on-chain* (seperti aliran dana wallet paus) tidak dimasukkan untuk menjaga keseragaman stempel waktu resolusi jam dan mencegah distorsi kebocoran temporal dari sentimen yang tidak seragam."*

---

## BAGIAN 7: BEDAH TUNTAS RUMUS MATEMATIS, ASAL-USUL, CARA BACA SIMBOL, & PANDUAN LISAN MENJELASKAN DIAGRAM

### A. Kamus Lengkap Rumus, Asal-Usul (Paper), Bukti Matematis, & Cara Baca Simbol

#### 1. Rumus Return Intra-hari, Realized Variance ($RV_t$), dan Transformasi $\log RV_t$
* **Persamaan Matematis:**
  $$r_{t,h} = \ln(C_{t,h}) - \ln(O_{t,h})$$
  $$\text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2$$
  $$\log RV_t = \ln(\text{RV}_t + 10^{-12})$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Andersen & Bollerslev (1998) *"Answering the Skeptics: Yes, Standard Volatility Models do Provide Accurate Forecasts"* (*International Economic Review*) dan Andersen, Bollerslev, Diebold, & Labys (2003) *"Modeling and Forecasting Realized Volatility"* (*Econometrica*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Teori *Continuous-Time Finance & Semimartingale*: Dalam proses difusi harga kontinu, volatilitas laten harian adalah integral varians sejati $\int_0^1 \sigma^2(s)ds$. Andersen et al. membuktikan secara matematis bahwa ketika sampling harga intra-hari dipercepat menuju nol ($m \to \infty$), jumlah kuadrat return frekuensi tinggi berkonvergensi dalam probabilitas (*converges in probability*) menuju variasi kuadratik sejati (*quadratic variation*).
  * Dengan menjumlahkan 24 lilin 1 jam per hari, varians derau pengukuran (*measurement noise*) tereduksi drastis sebesar $\approx 95{,}8\%$ ($1/24$) dibandingkan jika hanya memakai kuadrat return harian tunggal ($r_t^2$).
* **Mengapa Memakai Rumus Ini & Bukan Rumus Lain:**
  * Volatilitas adalah variabel laten (tidak tampak pada harga harian). Memakai $r_t^2$ biasa sangat berderau (*noisy*). RV berbasis data 1-jam memberikan proksi varians tanpa bias (*unbiased estimator*).
  * Transformasi logaritma natural ($\log RV_t$) menormalkan sebaran data yang memiliki kemencengan positif ekstrem (*right-skewed*) dan ekor tebal (*fat tails*), sehingga mendekati distribusi normal (Gaussian). Ini mempercepat konvergensi optimasi gradien pada LSTM dan menjamin prediksi varians selalu positif saat dikembalikan lewat fungsi eksponensial.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $r_{t,h}$: Dibaca *"r sub t koma h"* $\rightarrow$ Imbal hasil logaritmik hari ke-$t$ jam ke-$h$.
  * $\ln$: Dibaca *"logaritma natural"* (logaritma berbasis bilangan natural $e$).
  * $C_{t,h}$: Dibaca *"C sub t koma h"* $\rightarrow$ Harga penutupan (*closing price*) lilin jam ke-$h$.
  * $O_{t,h}$: Dibaca *"O sub t koma h"* $\rightarrow$ Harga pembukaan (*opening price*) lilin jam ke-$h$.
  * $\text{RV}_t$: Dibaca *"Realized Variance hari ke-t"*.
  * $\sum_{h=1}^{24}$: Dibaca *"sigma penjumlahan dari indeks h sama dengan 1 sampai 24 lilin satu jam"*.
  * $r_{t,h}^2$: Dibaca *"r sub t koma h kuadrat"*.
  * $10^{-12}$: Dibaca *"sepuluh pangkat minus dua belas"* $\rightarrow$ Konstanta stabilitas numerik (*machine epsilon*) agar fungsi $\ln$ tidak menghasilkan nilai minus tak hingga ($-\infty$) seandainya terdapat hari dengan varians mendekati nol.

---

#### 2. Rumus Arsitektur Sel dan 3 Gerbang LSTM (Long Short-Term Memory)
* **Persamaan Matematis:**
  $$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$
  $$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
  $$\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$
  $$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$
  $$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
  $$h_t = o_t \odot \tanh(c_t)$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Sepp Hochreiter & Jürgen Schmidhuber (1997) *"Long Short-Term Memory"* (*Neural Computation*), dan penyempurnaan gerbang lupa (*forget gate*) oleh Felix A. Gers, Jürgen Schmidhuber, & Fred Cummins (2000) *"Learning to Forget: Continual Prediction with LSTM"* (*Neural Computation*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Mengatasi Bencana *Vanishing Gradient*: Pada RNN konvensional, propagasi mundur melalui waktu (*Backpropagation Through Time / BPTT*) melibatkan perkalian berantai matriks bobot $\prod_{k} W^T$. Jika nilai eigen bobot $< 1$, gradien lenyap mendekati nol secara eksponensial setelah beberapa langkah waktu.
  * LSTM memperkenalkan mekanisme *Constant Error Carousel* (CEC) pada status sel ($c_t$), di mana turunan terhadap memori sebelumnya memiliki jalur aditif langsung: $\frac{\partial c_t}{\partial c_{t-1}} = f_t$. Jika gerbang lupa bernilai mendekati 1 ($f_t \approx 1$), sinyal gradien dapat mengalir bebas tanpa hambatan melintasi puluhan langkah waktu masa lalu.
* **Mengapa Memakai Rumus Ini:**
  * Volatilitas Bitcoin memiliki dependensi memori panjang (*long-memory*) majemuk (harian, mingguan, bulanan) yang tidak sanggup diingat oleh RNN biasa akibat hilangnya gradien, dan memiliki relasi non-linear yang tidak sanggup dimodelkan oleh model linier GARCH/HAR.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $f_t$: Dibaca *"f sub t"* $\rightarrow$ Vektor aktivasi gerbang lupa (*forget gate*) pada langkah waktu $t$.
  * $\sigma$: Dibaca *"fungsi aktivasi sigma atau sigmoid logistik"*, rumusnya $\sigma(z) = \frac{1}{1 + e^{-z}}$, nilainya selalu berada di antara 0 dan 1 (0 = lupakan/buang total, 1 = pertahankan penuh).
  * $W_f$: Dibaca *"matriks bobot W sub f untuk gerbang lupa"*.
  * $[h_{t-1}, x_t]$: Dibaca *"konkatenasi atau penggabungan vektor hidden state kemarin h sub t minus satu dengan vektor masukan baru x sub t hari ini"*.
  * $b_f$: Dibaca *"vektor bias b sub f untuk gerbang lupa"*.
  * $i_t$: Dibaca *"i sub t"* $\rightarrow$ Vektor aktivasi gerbang masuk (*input gate*) pada langkah waktu $t$ (bernilai 0 s.d. 1, menentukan porsi informasi baru yang diizinkan masuk).
  * $\tilde{c}_t$: Dibaca *"c-tilde sub t"* $\rightarrow$ Vektor kandidat memori baru pada waktu $t$.
  * $\tanh$: Dibaca *"fungsi tangens hiperbolik"*, rumusnya $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$, memetakan nilai ke dalam rentang $[-1, +1]$ untuk memodulasi sinyal kandidat.
  * $c_t$: Dibaca *"c sub t"* $\rightarrow$ Status sel (*cell state*) pada waktu $t$, merupakan jalan tol memori jangka panjang (*long-term memory highway*).
  * $\odot$: Dibaca *"simbol Hadamard product atau perkalian elemen-per-elemen (element-wise multiplication)"* (tegaskan ke dosen: ini bukan perkalian dot matriks biasa, melainkan perkalian titik-demi-titik antar-elemen vektor!).
  * $c_{t-1}$: Dibaca *"c sub t minus satu"* $\rightarrow$ Status sel dari hari sebelumnya.
  * $o_t$: Dibaca *"o sub t"* $\rightarrow$ Vektor aktivasi gerbang keluar (*output gate*) pada waktu $t$ (bernilai 0 s.d. 1).
  * $h_t$: Dibaca *"h sub t"* $\rightarrow$ Status tersembunyi (*hidden state*) pada waktu $t$, merupakan keluaran representasi sel yang diteruskan ke lapisan regresi linier akhir serta dialirkan ke sel langkah waktu berikutnya.

---

#### 3. Rumus Fungsi Kerugian Asimetris QLIKE (Quasi-Likelihood)
* **Persamaan Matematis:**
  $$\text{QLIKE}(RV_t, \widehat{RV}_t) = \frac{RV_t}{\widehat{RV}_t} - \ln\left(\frac{RV_t}{\widehat{RV}_t}\right) - 1$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Andrew J. Patton (2011) *"Data-based ranking of volatility models"* (*Journal of Econometrics*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Teorema *Robust Loss Function*: Patton membuktikan secara analitik bahwa ketika membandingkan beberapa model peramalan volatilitas menggunakan proksi observasi yang berderau (*imperfect volatility proxy*), urutan perankingan model terjamin konsisten identik dengan urutan terhadap volatilitas laten sejati **hanya jika** menggunakan fungsi kerugian dari famili Bregman divergence berderajat homogenitas nol atau satu.
  * Dua fungsi yang memenuhi syarat ini adalah MSE dan QLIKE. Namun, Patton membuktikan secara formal bahwa MSE rentan terdistorsi oleh pencilan (*outliers*), sedangkan QLIKE memiliki varians penaksir ranking terkecil dan imun terhadap pergeseran skala proksi.
* **Mengapa Memakai Rumus Ini:**
  1. Bersifat *noise-robust* terhadap proksi Realized Variance.
  2. Bersifat asimetris menguntungkan bagi industri finansial: Menghukum kesalahan peramalan risiko yang terlalu rendah (*under-forecasting*) lebih dari 4 kali lipat lebih berat dibanding kesalahan terlalu tinggi (*over-forecasting*). Meremehkan volatilitas Bitcoin dapat mengakibatkan kebangkrutan modal dan likuidasi paksa (*margin call*).
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $\text{QLIKE}(RV_t, \widehat{RV}_t)$: Dibaca *"nilai kerugian QLIKE antara Realized Variance aktual RV sub t dengan estimasi ramalan RV-topi sub t"*.
  * $\frac{RV_t}{\widehat{RV}_t}$: Dibaca *"rasio RV sub t dibagi RV-topi sub t"*.
  * $\ln\left(\frac{RV_t}{\widehat{RV}_t}\right)$: Dibaca *"logaritma natural dari rasio RV sub t dibagi RV-topi sub t"*.
  * $- 1$: Dibaca *"dikurangi satu (konstanta normalisasi agar loss bernilai tepat 0 ketika ramalan identik sempurna dengan aktual, yakni ketika rasio bernilai 1)"*.

---

#### 4. Rumus Optimasi Bayesian Optuna TPE (Tree-structured Parzen Estimator)
* **Persamaan Matematis:**
  $$p(x|y) = \begin{cases} \ell(x) & \text{jika } y < y^* \\ g(x) & \text{jika } y \ge y^* \end{cases}$$
  $$\text{Expected Improvement (EI)}_y(x) \propto \frac{\ell(x)}{g(x)}$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: James Bergstra, Rémi Bardenet, Yoshua Bengio, & Balázs Kégl (2011) *"Algorithms for Hyper-Parameter Optimization"* (*NeurIPS*). Dan kerangka kerja Optuna oleh Takuya Akiba et al. (2019) (*ACM KDD*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Membalik Aturan Bayes: Optimasi Bayesian standar berbasis Gaussian Process memodelkan fungsi objektif $p(y|x)$ secara langsung dengan inversi matriks berbiaya $\mathcal{O}(n^3)$. TPE membalik pemodelan menjadi $p(x|y)$ menggunakan dua estimasi densitas kernel non-parametrik ($\ell(x)$ untuk model sukses dan $g(x)$ untuk model gagal).
  * Bergstra et al. membuktikan secara analitik bahwa memaksimalkan kriteria *Expected Improvement* $\text{EI}(x) = \int_{-\infty}^{y^*} (y^* - y) p(y|x) dy$ ekuivalen matematis dengan memilih titik kandidat parameter $x$ yang memaksimalkan rasio densitas $\frac{\ell(x)}{g(x)}$.
* **Mengapa Memakai Rumus Ini:**
  * Berbiaya komputasi linier $\mathcal{O}(n)$, mampu mengeksplorasi ruang parameter campuran (kontinu, diskrit, logaritmik) secara adaptif, terbukti konvergen ke konfigurasi optimal jauh lebih cepat daripada Random Search, dan terintegrasi dengan pemangkas dini *MedianPruner*.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $p(x|y)$: Dibaca *"probabilitas densitas konfigurasi parameter x bersyarat terhadap nilai kerugian validasi y"*.
  * $y^*$: Dibaca *"y-bintang"* $\rightarrow$ Nilai kuantil ambang batas performa (persentil $\gamma = 15\%$ teratas dari trial sebelumnya).
  * $\ell(x)$: Dibaca *"l sub x"* $\rightarrow$ Distribusi densitas kernel dari kumpulan hyperparameter yang menghasilkan skor bagus (loss di bawah $y^*$).
  * $g(x)$: Dibaca *"g sub x"* $\rightarrow$ Distribusi densitas kernel dari kumpulan hyperparameter yang menghasilkan skor buruk (loss di atas atau sama dengan $y^*$).
  * $\frac{\ell(x)}{g(x)}$: Dibaca *"rasio l sub x dibagi g sub x; algoritma Optuna secara cerdas akan mengevaluasi kombinasi x baru yang memaksimalkan rasio ini, artinya titik yang paling disukai model sukses dan paling dijauhi model gagal"*.

---

#### 5. Rumus Uji Diebold-Mariano (DM) dengan Koreksi HAC Newey-West
* **Persamaan Matematis:**
  $$d_t = L(y_t, \hat{y}_{\text{baseline}, t}) - L(y_t, \hat{y}_{\text{LSTM}, t})$$
  $$\bar{d} = \frac{1}{T} \sum_{t=1}^T d_t$$
  $$\text{DM} = \frac{\bar{d}}{\sqrt{\hat{V}(\bar{d}) / T}} \xrightarrow{d} \mathcal{N}(0, 1)$$
  $$\hat{V}(\bar{d}) = \hat{\gamma}_0 + 2 \sum_{j=1}^{h-1} w_j \hat{\gamma}_j, \quad w_j = 1 - \frac{j}{h}$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Francis X. Diebold & Roberto S. Mariano (1995) *"Comparing Predictive Accuracy"* (*Journal of Business & Economic Statistics*). Dan koreksi matriks kovarians oleh Whitney K. Newey & Kenneth D. West (1987) (*Econometrica*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Teorema Limit Pusat untuk Deret Berkorelasi: Selisih galat ramalan $d_t$ pada data runtun waktu hampir pasti memiliki autokorelasi serial dan heteroskedastisitas. Jika diuji memakai uji t-Student biasa, varians sampel terdistorsi terlalu kecil (*underestimated*), memicu nilai t membengkak secara semu sehingga menolak hipotesis nol secara keliru (*Type I error / False Discovery*).
  * Estimator HAC Newey-West menggunakan kernel segitiga Bartlett ($w_j = 1 - j/h$) untuk membobot autokovarians lag hingga batas horizon $h=5$, menjamin matriks varians selalu bernilai semi-definit positif dan menghasilkan nilai-$p$ yang valid secara asimtotik.
* **Mengapa Memakai Rumus Ini:**
  * Menjadi standar emas ekonometrika modern untuk membuktikan bahwa keunggulan LSTM bukan kebetulan acak (*stochastic fluke*), melainkan signifikan secara statistik pada taraf nyata $\alpha = 0{,}05$.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $d_t$: Dibaca *"d sub t"* $\rightarrow$ Diferensial kerugian (*loss differential*) hari ke-$t$.
  * $\bar{d}$: Dibaca *"d-bar"* $\rightarrow$ Nilai rata-rata selisih kerugian pada seluruh sampel data uji $T$ hari.
  * $\text{DM}$: Dibaca *"statistik uji Diebold-Mariano"*.
  * $\hat{V}(\bar{d})$: Dibaca *"V-topi dari d-bar"* $\rightarrow$ Taksiran varians asimtotik jangka panjang Newey-West.
  * $\hat{\gamma}_0$: Dibaca *"gamma-topi nol"* $\rightarrow$ Varians sampel pada lag ke-0.
  * $\hat{\gamma}_j$: Dibaca *"gamma-topi sub j"* $\rightarrow$ Autokovarians sampel pada lag ke-$j$.
  * $w_j = 1 - \frac{j}{h}$: Dibaca *"bobot kernel Bartlett w sub j sama dengan satu minus j dibagi horizon h (di mana h = 5)"*.
  * $\xrightarrow{d} \mathcal{N}(0, 1)$: Dibaca *"berkonvergensi dalam distribusi menuju distribusi normal baku standar dengan rata-rata 0 dan varians 1"*.

---

#### 6. Rumus Model Pembanding HAR-RV (Corsi, 2009)
* **Persamaan Matematis:**
  $$\log RV_{t+1} = \beta_0 + \beta_d \log RV_t + \beta_w \log RV_t^{(w)} + \beta_m \log RV_t^{(m)} + \varepsilon_{t+1}$$
  $$\log RV_t^{(w)} = \frac{1}{5} \sum_{i=0}^4 \log RV_{t-i}, \quad \log RV_t^{(m)} = \frac{1}{22} \sum_{i=0}^{21} \log RV_{t-i}$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Fulvio Corsi (2009) *"A Simple Approximate Long-Memory Model of Realized Volatility"* (*Journal of Financial Econometrics*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Berlandaskan *Heterogeneous Market Hypothesis* (Müller et al., 1997). Volatilitas pasar tercipta dari interaksi tiga kelompok pelaku pasar dengan horizon investasi yang berbeda: pedagang harian intraday (*daily*, $d$), manajer portofolio mingguan (*weekly*, $w$), dan investor institusional bulanan (*monthly*, $m$).
* **Mengapa Memakai Rumus Ini:**
  * Sebagai baseline ekonometrika frekuensi tinggi standar industri tertinggi. Jika model AI tidak sanggup mengalahkan HAR-RV, maka model AI tersebut belum terbukti bernilai di dunia finansial kuantitatif.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $\beta_0, \beta_d, \beta_w, \beta_m$: Dibaca *"koefisien regresi beta nol (konstanta), beta d (harian), beta w (mingguan), dan beta m (bulanan)"*.
  * $\log RV_t^{(w)}$: Dibaca *"rata-rata bergerak log RV horizon mingguan lima hari bursa terakhir"*.
  * $\log RV_t^{(m)}$: Dibaca *"rata-rata bergerak log RV horizon bulanan dua puluh dua hari bursa terakhir"*.
  * $\varepsilon_{t+1}$: Dibaca *"epsilon sub t plus satu"* $\rightarrow$ Galat residual model peramalan.

---

#### 7. Rumus Estimator Dispersi Rentang Parkinson (1980)
* **Persamaan Matematis:**
  $$\log range_t = \ln(\max H_{t,h} - \min L_{t,h} + 10^{-12})$$
* **Dapat dari Mana & Asal Usul Teori:**
  * Penemu & Paper Rujukan: Michael Parkinson (1980) *"The Extreme Value Method for Estimating the Variance of the Rate of Return"* (*Journal of Business*).
* **Dasar Ilmiah & Bukti Matematis:**
  * Parkinson membuktikan secara matematis melalui sifat gerak Brown (*Brownian motion*) bahwa selisih harga tertinggi ($H$) dan terendah ($L$) dalam satu hari memiliki efisiensi statistik **5 kali lipat lebih tinggi** dibandingkan selisih harga penutupan dan pembukaan ($C - O$), karena merekam batas dispersi ekstrem fluktuasi intra-hari tanpa terdistorsi oleh arah return.
* **Mengapa Memakai Rumus Ini:**
  * Digunakan sebagai Fitur Masukan ke-2 pada model LSTM kita untuk melengkapi informasi volatilitas dengan mengukur rentang dispersi harga ekstrem harian tanpa menimbulkan *look-ahead bias*.
* **Cara Membaca Simbol Secara Lisan di Depan Dosen:**
  * $\log range_t$: Dibaca *"log range hari ke-t"*.
  * $\max H_{t,h}$: Dibaca *"nilai maksimum dari harga tertinggi lilin jam ke-h pada hari ke-t"*.
  * $\min L_{t,h}$: Dibaca *"nilai minimum dari harga terendah lilin jam ke-h pada hari ke-t"*.

---

### B. Panduan Lisan Menjelaskan Diagram Proposal di Depan Dewan Penguji

#### 1. Cara Menjelaskan GAMBAR 2.1 (Arsitektur Sel & Aliran Informasi LSTM)
*(Gunakan bahasa Indonesia yang runtut, percaya diri, dan santun sambil menunjuk bagian diagram):*

> *"Bapak dan Ibu Dosen Penguji yang saya hormati, izin saya menguraikan Gambar 2.1 mengenai anatomi arsitektur sel LSTM dan dinamika aliran informasinya:*
> 
> *Jika kita cermati diagram ini, satu sel LSTM pada langkah waktu $t$ memiliki **dua jalur utama** dan **tiga gerbang logika penyaring** yang bekerja secara sekuensial:*
> 
> 1. **Dua Masukan di Sisi Kiri Bawah ($x_t$ dan $h_{t-1}$):** Di bagian kiri bawah, ada dua informasi yang masuk bersamaan: vektor masukan hari ini ($x_t$, yang berisi 6 fitur mikrostruktur kita) dan rekaman memori dari hari kemarin ($h_{t-1}$). Kedua sinyal ini digabungkan (*concatenated*) untuk disalurkan serentak ke tiga gerbang logika.
> 2. **Jalan Tol Memori di Sisi Atas (Cell State, $c_{t-1} \to c_t$):** Garis horizontal lurus paling atas adalah *cell state* atau 'jalan tol memori jangka panjang'. Karakteristik terpentingnya adalah gradien mengalir secara linier tanpa perkalian matriks berulang, sehingga LSTM terbebas dari masalah *vanishing gradient*.
> 3. **Gerbang Pertama di Kiri (Forget Gate, $f_t$):** Masukan diarahkan ke fungsi aktivasi sigmoid ($\sigma$) yang menghasilkan output antara 0 sampai 1. Nilai ini dikalikan secara titik per titik (*Hadamard product*, $\odot$) ke jalur *cell state* memori lama ($c_{t-1}$). Gerbang ini bertindak sebagai pemilih: 'Informasi volatilitas masa lalu mana yang sudah usang dan harus dibuang (0) atau dipertahankan (1)?'
> 4. **Gerbang Kedua di Tengah (Input Gate $i_t$ dan Kandidat $\tilde{c}_t$):** Jalur ini bertugas mencatat hal baru hari ini. Sinyal dilewatkan ke sigmoid ($i_t$) untuk menentukan filter kepentingannya, dan secara paralel ke tangen hiperbolik ($\tanh$) untuk membuat kandidat memori baru ($\tilde{c}_t$) dengan rentang $-1$ hingga $+1$. Keduanya dikalikan secara elemen, lalu ditambahkan ($+$) ke jalan tol status sel. Di titik inilah memori jangka panjang diperbarui secara resmi menjadi $c_t$.
> 5. **Gerbang Ketiga di Kanan (Output Gate $o_t$ dan Hidden State $h_t$):** Sinyal disaring lagi oleh fungsi sigmoid ($o_t$), sementara status sel memori $c_t$ dimodulasi melalui $\tanh$. Keduanya dikalikan untuk menghasilkan $h_t$ (status tersembunyi), yang dikeluarkan ke atas melalui lapisan linier untuk menghasilkan ramalan $\log RV_{t+1}$ sekaligus diteruskan ke sel langkah hari berikutnya.
> 
> *Kesimpulannya, melalui interaksi tiga gerbang dan jalan tol status sel inilah, model LSTM mampu mengingat pola fluktuasi Bitcoin puluhan hari ke belakang tanpa kehilangan sinyal gradien."*

---

#### 2. Cara Menjelaskan GAMBAR 2.2 (Kerangka Pemikiran Konseptual Penelitian)
*(Gunakan bahasa yang menghubungkan masalah, solusi, dan hasil):*

> *"Bapak dan Ibu Dosen Penguji, Gambar 2.2 merangkum alur berpikir konseptual yang melandasi penelitian skripsi ini:*
> 1. **Titik Tolak Masalah (*Problem Statement*):** Pasar Bitcoin memiliki tingkat volatilitas sangat ekstrem non-stop 24/7. Mayoritas peneliti informatika sebelumnya mencoba menebak harga nominal penutupan (*closing price*), namun secara ilmiah harga penutupan bergerak acak (*random walk*) dan mustahil diprediksi secara konsisten.
> 2. **Pergeseran Paradigma (*Paradigm Shift*):** Kami mengalihkan fokus pada *Realized Volatility* yang terbukti memiliki sifat *volatility clustering* dan persistensi memori panjang, yang sangat dibutuhkan industri keuangan digital untuk mitigasi risiko.
> 3. **Identifikasi Kesenjangan Riset (*Research Gap*):** Model ekonometrika linier (GARCH, HAR-RV) gagal menangkap lonjakan varians non-linear pasar kripto. Di sisi lain, riset deep learning sebelumnya kerap terjebak pada epidemi kebocoran data (*data leakage*) dan optimasi parameter *trial-and-error* manual yang memboroskan komputasi.
> 4. **Solusi Usulan (*Proposed Solution*):** Kami merancang pipeline komputasi terintegrasi: arsitektur LSTM yang dioptimasi secara cerdas menggunakan algoritma Bayesian Optuna TPE dengan pangkas dini *MedianPruner*, didukung protokol 5-fold Purged Cross-Validation ber-jeda 10 hari dan evaluasi asimetris QLIKE.
> 5. **Validasi & Inferensi Ilmiah (*Validation & Inference*):** Model diuji pada data out-of-sample tahun 2026, lalu diuji signifikansinya menggunakan Uji Diebold-Mariano berkoreksi HAC Newey-West dan 10.000 Moving-Block Bootstrap guna menjamin kesimpulan ilmiah bebas bias."*

---

#### 3. Cara Menjelaskan GAMBAR 3.1 (Diagram Alir Tahapan Penelitian Komputasional)
*(Gunakan bahasa tahapan operasional yang sistematis dari hulu ke hilir):*

> *"Bapak dan Ibu Dosen Penguji, Gambar 3.1 menguraikan cetak biru operasional metodologi eksperimen komputasi kami yang terbagi ke dalam 7 tahapan berurutan:*
> 1. **Tahap 1 (Akuisisi & Audit Integritas Data):** Mengunduh 81 arsip data kline 1 jam dari Binance Vision (2020–2026), memvalidasi hash kriptografis SHA-256, dan menerapkan Amandemen A1 (eliminasi 1 hari cacat server 19 Februari 2020) sehingga diperoleh tepat 2.464 hari observasi bersih terverifikasi.
> 2. **Tahap 2 (Rekayasa Fitur Kausal):** Menghitung variabel target $\log RV_{t+1}$ dan 6 fitur masukan berakar mikrostruktur pasar (RV, Parkinson Range, Volume/MDH, AbsRet Shock, HAR-5, HAR-22) yang sepenuhnya bebas dari bias masa depan (*look-ahead bias*).
> 3. **Tahap 3 (Partisi Temporal Kronologis Murni):** Membagi dataset berdasarkan kalender murni: Development 2020–2023 (1.460 hari), Validation 2024–2025 (731 hari), dan Uji Out-of-Sample 2026 (273 hari).
> 4. **Tahap 4 (Optimasi Bayesian Optuna & Purged CV):** Menjalankan 50 trials penalaan hyperparameter menggunakan Optuna TPE dan *MedianPruner* di atas skema 5-fold Purged Cross-Validation ber-jeda pemisah 10 hari dan standarisasi lokal (*fold-specific scaling*) untuk menemukan 6 hyperparameter optimal.
> 5. **Tahap 5 (Pelatihan Model Final & Konstruksi Baseline):** Melatih arsitektur LSTM terbaik menggunakan 5 *random seed* apriori `(42, 123, 2024, 7, 99)` dan membangun 4 model baseline pembanding (Persistence, HAR-RV, GARCH, LSTM Untuned).
> 6. **Tahap 6 (Evaluasi Out-of-Sample & Statistik Inferensial):** Menguji seluruh model pada data uji 2026 dengan metrik primer QLIKE, lalu membuktikan keunggulannya melalui Uji Diebold-Mariano berkoreksi HAC Newey-West lag 5 ($p < 0{,}05$) dan 10.000 sampel Moving-Block Bootstrap.
> 7. **Tahap 7 (Penarikan Kesimpulan Ilmiah):** Menarik kesimpulan transparan berdasarkan matriks kriteria keberhasilan yang telah ditetapkan di Bab III."*

---

## BAGIAN 8: RANGKUMAN CHEAT-SHEET ANGKA KUNCI SKRIPSI (HAFALKAN DI LUAR KEPALA!)

* **Rentang Data Observasi:** 1 Januari 2020 s.d. 30 September 2026 (81 bulan kalender penuh).
* **Total Sampel Hari:** **2.464 hari observasi** (setelah eliminasi 1 hari cacat server 19 Feb 2020 via Amandemen A1).
* **Pembagian Partisi Temporal:**
  * *Development Set* (Pelatihan Awal & Fold CV): 2020–2023 (**1.460 hari / ~59,2%**).
  * *Validation Set* (Penalaan Optuna & Seleksi Model): 2024–2025 (**731 hari / ~29,7%**).
  * *Out-of-Sample Test Set* (Evaluasi Akhir Murni): 1 Januari – 30 September 2026 (**273 hari / ~11,1%**).
* **Fitur Masukan (6 Fitur Kausal):** $\log RV_t$, $\log range_t$, $\log volume_t$, $\log absret_t$, $\text{rv\_mean\_5}_t$, $\text{rv\_mean\_22}_t$.
* **Target Ramalan:** Nilai satu hari ke depan $\log RV_{t+1} = \ln(RV_{t+1} + 10^{-12})$.
* **Algoritma Optimasi:** Optuna TPE (*Tree-structured Parzen Estimator*), 50 *trials*, pangkas dini *MedianPruner* (`startup = 10`, `warmup = 2`).
* **Search Space Hyperparameter (6 Parameter):**
  * *Lookback window:* 10 s.d. 30 hari.
  * *Hidden units:* 16 s.d. 128 neuron.
  * *Layers:* 1 atau 2 lapisan LSTM.
  * *Dropout:* 0,05 s.d. 0,40 (langkah 0,05).
  * *Learning rate:* $3 \times 10^{-4}$ s.d. $2 \times 10^{-3}$ (skala logaritmik).
  * *Batch size:* 16, 32, atau 64 sampel.
* **Protokol Validasi:** 5-fold *Purged Rolling-Origin Cross-Validation* dengan *purge gap* 10 hari dan scaler spesifik per fold.
* **Model Pembanding (4 Baseline):** *Random Walk Persistence*, HAR-RV Corsi (2009), GARCH(1,1), LSTM *Untuned*.
* **Evaluasi & Inferensi:**
  * Loss Primer: QLIKE (Patton, 2011) asimetris tahan derau.
  * Loss Sekunder: RMSE dan MAE.
  * Uji Asimtotik: Diebold-Mariano berkoreksi HAC Newey-West lag 5 ($p < 0{,}05$).
  * Uji Empiris: *Moving-Block Bootstrap* 10.000 repetisi (selang kepercayaan 95%).
  * Pengendalian Stokastik: 5 benih acak deterministik `(42, 123, 2024, 7, 99)`.
* **Integritas & Kualitas Kode:** 34 pengujian unit otomatis (`pytest`) lulus 100%, verifikasi hash SHA-256 data.
