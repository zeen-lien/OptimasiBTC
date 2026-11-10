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
  $$d_t = L(y_t, \hat{y}_{1,t}) - L(y_t, \hat{y}_{2,t})$$
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

## RANGKUMAN CHEAT-SHEET ANGKA KUNCI SKRIPSI (HAFALKAN DI LUAR KEPALA!)

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
