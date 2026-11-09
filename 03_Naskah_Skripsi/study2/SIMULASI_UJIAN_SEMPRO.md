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
> 2. **Landasan Teori & Bukti Komputasi (*Scientific Evidence*):** Berikan argumentasi ilmiah, sitasi peneliti rujukan (misal: Patton, Corsi, Hochreiter, Bergstra), atau fakta komputasi/angka riil.
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

## BAGIAN 2: LANDASAN TEORI & ARSITEKTUR MODEL

### Pertanyaan 6: "Kenapa kamu memilih model LSTM? Kenapa tidak pakai RNN biasa, GRU, atau algoritma Machine Learning sederhana seperti Random Forest atau SVR?"
* **Jawaban Langsung:**
  "1. **Kelemahan RNN Standar:** RNN konvensional mengalami masalah hilangnya gradien (*vanishing gradient*) ketika memproses dependensi waktu yang panjang, sehingga mudah 'lupa' pola masa lalu yang berjarak belasan langkah ke belakang.  
  2. **Keunggulan LSTM:** LSTM dilengkapi sel memori internal (*cell state*) dan tiga gerbang logika (*forget*, *input*, *output gate*) yang memungkinkan gradien mengalir tanpa hambatan, sehingga sangat efektif menangkap memori temporal jangka panjang.  
  3. **Dibandingkan GRU:** GRU menggabungkan gerbang sel dan status tersembunyi; namun untuk dinamika volatilitas yang memiliki komponen persistensi majemuk (harian, mingguan, bulanan), pemisahan *cell state* pada LSTM terbukti lebih stabil menampung memori volatilitas masa lalu.  
  4. **Dibandingkan Model Linier (GARCH & HAR-RV):** Model linier kaku mengasumsikan hubungan parametrik simetris, sedangkan LSTM mampu memodelkan relasi non-linear kompleks dan lonjakan ekstrem (*volatility jumps*) pasar kripto tanpa asumsi distribusi awal yang kaku."
* **Sitasi Kunci:** Hochreiter & Schmidhuber (1997); Christensen et al. (2023).

---

### Pertanyaan 7: "Bisa jelaskan cara kerja sel LSTM dan fungsi masing-masing gerbangnya secara sederhana tanpa rumus yang rumit?"
* **Jawaban Langsung:**
  "Bisa, Bapak/Ibu. Arsitektur sel LSTM bekerja persis seperti mekanisme kerja memori manusia yang memiliki filter penyaring informasi melalui 4 tahapan berurutan:
  1. **Gerbang Lupa (*Forget Gate*, $f_t$):** Bertindak sebagai penghapus memori. Ia memeriksa masukan baru ($x_t$) dan status sebelumnya ($h_{t-1}$), lalu memutuskan: *'Informasi volatilitas masa lalu mana yang sudah usang dan harus dibuang?'* (Output 0 berarti buang total, 1 berarti pertahankan penuh).
  2. **Gerbang Masuk (*Input Gate*, $i_t$):** Bertindak sebagai penyeleksi informasi baru. Ia memutuskan informasi fluktuasi hari ini mana yang cukup penting untuk dicatat. Bersamaan dengan itu dibuat kandidat memori baru ($\tilde{c}_t$).
  3. **Pembaruan Status Sel (*Cell State Update*, $c_t$):** Ini adalah 'buku catatan memori jangka panjang'. Memori lama yang sudah disaring dikalikan dengan gerbang lupa, lalu ditambahkan informasi baru dari gerbang masuk.
  4. **Gerbang Keluar (*Output Gate*, $o_t$):** Memutuskan informasi apa yang akan dikeluarkan sebagai proyeksi *hidden state* ($h_t$), yang kemudian dipetakan oleh lapisan linear menjadi ramalan volatilitas satu langkah ke depan ($\log RV_{t+1}$)."

---

### Pertanyaan 8: "Apa itu Realized Variance (RV) dan kenapa harus ditransformasi ke bentuk logaritma ($\log RV$)?"
* **Jawaban Langsung:**
  * **Realized Variance (RV):** Volatilitas pasar adalah variabel laten (tidak tampak langsung pada data harian). Oleh karena itu, kita mengukurnya menggunakan *Realized Variance*, yaitu penjumlahan kuadrat return harga intra-hari 1 jam dari 24 lilin (*candlestick bars*) sepanjang satu hari UTC:
    $$\text{RV}_t = \sum_{h=1}^{24} r_{t,h}^2$$
  * **Alasan Transformasi Logaritma:**
    Data empiris RV memiliki nilai yang selalu positif, tetapi memiliki kemencengan (*skewness*) ekstrem dan ekor tebal (*heavy tails*) akibat lonjakan pasar. Dengan menerapkan transformasi logaritmik $\log RV_t = \ln(RV_t + 10^{-12})$, sebaran data menjadi jauh lebih stabil mendekati distribusi normal (Gaussian), mengeliminasi risiko prediksi bernilai negatif, dan mempermudah konvergensi proses optimasi gradien pada jaringan saraf tiruan.

---

## BAGIAN 3: OPTIMASI HYPERPARAMETER DENGAN OPTUNA

### Pertanyaan 9: "Mengapa kamu menggunakan algoritma Optuna untuk optimasi hyperparameter? Kenapa tidak pakai Grid Search atau Random Search yang lebih lazim?"
* **Jawaban Langsung:**
  "1. **Kelemahan Grid Search:** Grid Search melakukan evaluasi pada semua titik kombinasi secara kaku. Jika kita punya 6 parameter dengan kombinasi ribuan titik, waktu komputasi akan meledak secara eksponensial (*curse of dimensionality*).  
  2. **Kelemahan Random Search:** Random Search memilih kombinasi secara acak tanpa belajar dari hasil uji coba sebelumnya, sehingga membuang-buang daya komputasi pada wilayah parameter yang buruk.  
  3. **Keunggulan Optuna (TPE):** Optuna menerapkan algoritma *Tree-structured Parzen Estimator* (TPE) berbasis optimasi Bayesian. TPE memodelkan probabilitas konfigurasi masa lalu yang menghasilkan skor baik vs skor buruk. Dari riwayat tersebut, Optuna secara cerdas dan adaptif mengarahkan *trial* berikutnya ke ruang parameter yang paling menjanjikan. Hasil riset Bergstra et al. membuktikan TPE menemukan kombinasi optimal jauh lebih cepat dibandingkan random search."
* **Sitasi Kunci:** Bergstra et al. (2011); Akiba et al. (2019).

---

### Pertanyaan 10: "Apa itu MedianPruner dalam Optuna dan bagaimana mekanisme kerjanya?"
* **Jawaban Langsung:**
  "**MedianPruner adalah algoritma pemangkasan dini (*early stopping / pruning*) pada Optuna.**  
  Cara kerjanya: Saat sebuah *trial* arsitektur LSTM sedang dilatih pada suatu epoch awal, Optuna memeriksa nilai kerugian validasinya. Jika nilai kerugian tersebut ternyata lebih buruk daripada nilai median dari *trial-trial* sebelumnya pada epoch yang sama, Optuna akan langsung menghentikan (*pruning*) pelatihan model tersebut tanpa harus menunggu sampai epoch ke-100 selesai.  
  Fungsinya adalah menghemat waktu dan sumber daya komputasi secara drastis, sehingga waktu eksperimen dapat dialokasikan untuk mengeksplorasi kandidat arsitektur lain yang lebih potensial."
* **Catatan Parameter:** Eksperimen kita menggunakan `n_startup_trials = 10` (10 trial pertama dibiarkan selesai tanpa dipangkas untuk membentuk baseline median yang stabil) dan `n_warmup_steps = 2`.

---

### Pertanyaan 11: "Hyperparameter apa saja yang ditala oleh Optuna dalam model LSTM kamu?"
* **Jawaban Langsung:**
  "Terdapat **6 hyperparameter arsitektural dan pelatihan** yang dioptimasi dalam ruang pencarian (*search space*) sebanyak 50 *trials*:
  1. *Lookback window* (panjang jendela memori historis): 10 s.d. 30 hari.
  2. Jumlah neuron (*hidden units*): 16 s.d. 128 neuron.
  3. Jumlah lapisan LSTM (*layers*): 1 atau 2 lapisan bertumpuk (*stacked*).
  4. Tingkat regulasi *Dropout*: 0,05 s.d. 0,40 (langkah 0,05) untuk mencegah overfitting.
  5. *Learning rate* Adam: $3 \times 10^{-4}$ s.d. $2 \times 10^{-3}$ (pada skala logaritmik).
  6. Ukuran *batch* (*batch size*): 16, 32, atau 64 sampel."

---

## BAGIAN 4: METODOLOGI, ANTI-LEAKAGE, & STATISTIK INFERENSIAL

### Pertanyaan 12: "Apa yang dimaksud dengan kebocoran data (*data leakage*) pada data time series dan bagaimana kamu membuktikan bahwa penelitian kamu bebas dari kebocoran data?"
* **Jawaban Langsung:**
  "**Kebocoran data (*data leakage*) adalah kondisi cacat metodologis fatal di mana informasi masa depan (*future information*) secara sengaja atau tidak sengaja menyusup ke dalam proses pelatihan masa lalu (*look-ahead bias*), sehingga menghasilkan performa semu yang tampak hebat di atas kertas tetapi langsung gagal saat diuji di dunia nyata.**  
  Penelitian ini menerapkan **4 lapis benteng pencegahan kebocoran data**:
  1. **Partisi Temporal Kronologis Murni:** Data dipecah berdasarkan urutan waktu kalender, bukan diacak: Development (2020–2023), Validation (2024–2025), dan Test Out-of-Sample (1 Januari – 30 September 2026).
  2. **Skema Purged Cross-Validation:** Pada setiap lipatan (*fold*), disisipkan jeda pemisah (*purge gap*) selama 10 hari antara data latih dan data validasi untuk memutus ketergantungan serial antar-sampel jendela geser (*sliding window*).
  3. **Fold-Specific Scaling:** Normalisasi `StandardScaler` dihitung murni dari nilai mean dan deviasi standar data latih pada masing-masing fold. Nilai skala tersebut baru diaplikasikan ke data validasi tanpa pernah menghitung scaler global di awal.
  4. **Isolasi Penuh Data Uji 2026:** Data uji eksternal 2026 dikunci total dan tidak pernah disentuh dalam proses optimasi hyperparameter Optuna maupun pemilihan model."
* **Sitasi Kunci:** Marcos López de Prado (2018) — *Advances in Financial Machine Learning*.

---

### Pertanyaan 13: "Kenapa evaluasi utamanya memakai fungsi kerugian QLIKE, bukan MSE (Mean Squared Error) atau MAE?"
* **Jawaban Langsung:**
  "Karena **volatilitas aktual adalah variabel laten yang diestimasi menggunakan proksi (*realized variance*) yang berderau (*noisy proxy*)**.  
  Penelitian ekonometrika terkemuka oleh **Patton (2011)** membuktikan secara matematis bahwa fungsi kerugian simetris konvensional seperti MSE tidak tahan terhadap derau proksi dan dapat menghasilkan perankingan model yang bias/salah.  
  Sebaliknya, **QLIKE (*Quasi-Likelihood*) terbukti mathematically robust**: perankingan model di bawah QLIKE konsisten sama apakah dihitung terhadap volatilitas laten murni maupun terhadap proksi berderau. Selain itu, QLIKE bersifat asimetris: ia memberikan penalti kerugian yang jauh lebih berat pada kesalahan *under-forecasting* (meramal risiko terlalu rendah dari kenyataan), yang sangat penting dalam manajemen risiko finansial."
* **Formula Singkat:** $\text{QLIKE}(RV, \widehat{RV}) = \frac{RV}{\widehat{RV}} - \ln\left(\frac{RV}{\widehat{RV}}\right) - 1$.

---

### Pertanyaan 14: "Apa saja model pembanding (*baseline*) yang kamu gunakan dan apa fungsinya masing-masing?"
* **Jawaban Langsung:**
  "Penelitian ini membandingkan model usulan (LSTM-Optuna) terhadap **4 model baseline bertingkat**:
  1. **Random Walk Persistence (Baseline Naif):** Asumsi sederhana bahwa volatilitas besok sama persis dengan volatilitas hari ini. Ini adalah *sanity check* paling mendasar: jika model deep learning gagal mengalahkan model naif ini, maka model tersebut secara ilmiah tidak layak dipakai.
  2. **HAR-RV Corsi (2009) (Baseline Ekonometrika Frekuensi Tinggi):** Model regresi linier standar industri yang memanfaatkan rata-rata volatilitas harian, mingguan (5 hari), dan bulanan (22 hari).
  3. **GARCH(1,1) (Baseline Ekonometrika Klasik):** Model varians bersyarat konvensional berbasis imbal hasil harian yang diestimasi dengan skema *expanding window*.
  4. **LSTM Untuned (Baseline Deep Learning Heuristik):** Arsitektur LSTM dengan konfigurasi default umum tanpa bantuan Optuna. Fungsinya adalah untuk membuktikan secara empiris bahwa peningkatan akurasi benar-benar dihasilkan oleh optimasi Bayesian Optuna, bukan semata-mata karena algoritma LSTM-nya."

---

### Pertanyaan 15: "Bagaimana kamu membuktikan bahwa model usulan kamu benar-benar lebih unggul dan bukan karena faktor kebetulan (*stochastic fluke*)?"
* **Jawaban Langsung:**
  "Keunggulan model tidak hanya dinilai dari selisih angka rata-rata metrik, melainkan dibuktikan melalui **tiga lapisan uji statistik inferensial formal**:
  1. **Uji Diebold-Mariano (1995) dengan Koreksi HAC Newey-West:** Menguji secara asimtotik apakah selisih kerugian peramalan ($d_t = L_{\text{baseline}} - L_{\text{LSTM}}$) bernilai positif secara signifikan dengan nilai-$p < 0{,}05$. Estimator HAC Newey-West dengan lag 5 digunakan untuk mengoreksi autokorelasi dan heteroskedastisitas pada deret galat.
  2. **Moving-Block Bootstrap (10.000 Repetisi):** Mengonstruksi selang kepercayaan empiris 95% untuk selisih kerugian yang mempertahankan struktur ketergantungan temporal runtun waktu (Künsch, 1989). Model LSTM-Optuna terbukti unggul kokoh jika batas atas interval bootstrap 95% berada di bawah nol.
  3. **Protokol Multi-Seed (5 Seed):** Mengendalikan variabilitas acak akibat inisialisasi bobot jaringan saraf dengan melatih model menggunakan lima benih acak yang ditetapkan apriori: `(42, 123, 2024, 7, 99)`, lalu melaporkan rata-rata dan deviasi standarnya."

---

## BAGIAN 5: CARA MENGHADAPI PERTANYAAN JEBAKAN (*TRICKY QUESTIONS*)

### Jebakan 1: "Kenapa kamu tidak membuat aplikasi Android/Web-nya saja agar bisa dipakai langsung oleh masyarakat?"
* **Cara Menjawab:**
  *"Terima kasih atas sarannya, Bapak/Ibu Penguji. Sesuai dengan **Batasan Masalah butir 7 di Bab I**, fokus penelitian skripsi ini murni diletakkan pada **kontribusi komputasional dan saintifik deret waktu**, yaitu memecahkan masalah keandalan peramalan non-linear, optimasi parameter Bayesian, dan integritas validasi bebas kebocoran data.  
  Membangun aplikasi antarmuka tanpa memastikan model peramalannya akurat dan bebas bias secara statistik justru akan menghasilkan sistem yang berbahaya bagi pengguna. Oleh karena itu, penelitian ini fokus menuntaskan modul peramalan inti (*core computation engine*)-nya terlebih dahulu. Pembuatan aplikasi antarmuka pengguna (*user interface*) dan integrasi sistem perdagangan otomatis telah kami rencanakan sebagai rekomendasi saran untuk penelitian lanjutan di Bab V."*

---

### Jebakan 2: "Dari mana kamu mendapatkan data kline 1 jam Bitcoin? Apakah datanya resmi dan valid?"
* **Cara Menjawab:**
  *"Data diunduh langsung dari arsip publik resmi bursa Binance melalui repositori **Binance Vision** (`data.binance.vision`), yang merupakan repositori data historis terstandarisasi institusional yang digunakan oleh peneliti komputasi finansial global.  
  Sebanyak 81 berkas arsip bulanan (Januari 2020 s.d. September 2026) telah diverifikasi integritasnya menggunakan **kunci kriptografis SHA-256** (tercatat pada Lampiran 4 proposal). Selain itu, kami melakukan audit stempel waktu UTC dan menerapkan Amandemen A1: seluruh hari observasi memiliki kelengkapan minimal 20 kline (83,3% kelengkapan), di mana hanya ada 1 hari cacat server bursa pada 19 Februari 2020 yang memiliki 1 kline sehingga dieliminasi secara objektif."*

---

### Jebakan 3: "Kalau hasil pengujian nanti ternyata model LSTM kamu kalah dari HAR-RV, apakah skripsi kamu dianggap gagal?"
* **Cara Menjawab:**
  *"Tidak, Bapak/Ibu. Dalam penelitian sains komputasi yang berintegritas tinggi, **tujuan utama penelitian adalah menemukan kebenaran empiris melalui metodologi yang sahih, bukan memaksakan model harus menang dengan cara memanipulasi data**.  
  Pada Tabel 3.5 naskah Bab III, kami telah mendefinisikan secara jujur kriteria keberhasilan eksperimen:
  * **Hasil Positif:** LSTM mengungguli seluruh model baseline secara signifikan ($p < 0{,}05$).
  * **Hasil Campuran:** LSTM mengalahkan model naif Persistence, namun setara atau bersaing ketat dengan HAR-RV. Ini tetap merupakan temuan ilmiah yang sangat bernilai karena membuktikan kapasitas model deep learning non-linear dalam menyamai model ekonometrika frekuensi tinggi tanpa restriksi asumsi linier.
  * **Hasil Negatif:** Jika LSTM tidak mampu mengalahkan baseline, penelitian ini tetap memberikan kontribusi metodologis penting: membuktikan bahwa pada volatilitas kripto, kompleksitas deep learning rentan over-fitting dibandingkan formulasi autoregresif linier sederhana apabila data leakage dikendalikan secara ketat. Jadi, nilai ilmiah skripsi terletak pada objektivitas dan kekuatan metodologinya."*

---

### RANGKUMAN CHEAT-SHEET ANGKA KUNCI SKRIPSI (HAFALKAN DI LUAR KEPALA!)
* **Rentang Data:** 1 Januari 2020 s.d. 30 September 2026 (81 bulan kalender).
* **Total Sampel Hari:** **2.464 hari observasi** (1.460 hari Dev 2020–2023; 731 hari Val 2024–2025; 273 hari Test Out-of-Sample 2026).
* **Fitur Masukan (6 Fitur):** $\log RV_t$, $\log range_t$, $\log volume_t$, $\log absret_t$, $\text{rv\_mean\_5}_t$, $\text{rv\_mean\_22}_t$.
* **Target Ramalan:** Nilai satu hari ke depan $\log RV_{t+1} = \ln(RV_{t+1} + 10^{-12})$.
* **Optimasi Optuna:** 50 *trials*, algoritma TPE, pemangkas *MedianPruner* (`startup = 10`, `warmup = 2`).
* **Cross-Validation:** 5-fold *Purged Rolling-Origin* dengan *purge gap* 10 hari dan scaler spesifik per fold.
* **Model Baseline (4 Model):** *Random Walk Persistence*, HAR-RV Corsi, GARCH(1,1), LSTM *Untuned*.
* **Evaluasi & Uji:** Loss primer QLIKE, Diebold-Mariano HAC Newey-West lag 5 ($p < 0{,}05$), *Moving-Block Bootstrap* 10.000 sampel (selang 95%), 5 seed `(42, 123, 2024, 7, 99)`.
