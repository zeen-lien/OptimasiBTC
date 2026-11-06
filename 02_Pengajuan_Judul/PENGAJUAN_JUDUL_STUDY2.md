# OUTLINE PROPOSAL SKRIPSI
## PROGRAM STUDI TEKNIK INFORMATIKA
### FAKULTAS SAINS DAN TEKNOLOGI
### UNIVERSITAS ISLAM NAHDLATUL ULAMA (UNISNU) JEPARA

---

| Identitas | Tanda | Isi |
|---|:---:|---|
| **Nama** | : | Zaini Leon Musthofa Kamal |
| **NIM** | : | 231240001455 |
| **Judul Penelitian** | : | **Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna pada Peramalan Realized Volatility Bitcoin** |

---

### Latar Belakang (Poinnya)

Pasar aset kripto, khususnya Bitcoin, memiliki karakteristik pergerakan harga yang sangat dinamis dan berisiko tinggi. Dalam bidang Teknik Informatika, data transaksi perdagangan ini terekam secara kronologis sebagai data deret waktu (*time series*). Sejumlah penelitian terdahulu di jurnal nasional mencoba memprediksi arah atau nominal harga penutupan Bitcoin menggunakan algoritma pembelajaran mendalam (*deep learning*), seperti penelitian Khumaidi dkk. (2024), Aswadi dan Ependi (2025), serta Ula dkk. (2024). Namun, memprediksi nominal harga secara langsung terbukti memiliki tingkat kesulitan yang sangat ekstrem karena harga aset pasar efisien mendekati pergerakan acak (*random walk*). Berbeda dengan tingkat harga, besaran gejolak atau volatilitas pasar menunjukkan pola pengelompokan (*volatility clustering*), di mana periode gejolak tinggi cenderung berkelompok mengikuti periode sebelumnya, sebagaimana dibuktikan oleh Andersen dkk. (2003). Karakteristik persistensi ini membuktikan bahwa volatilitas memiliki struktur informasi yang jauh lebih teratur untuk dimodelkan. *(133 kata)*

Secara konvensional, pemodelan deret waktu volatilitas dianalisis menggunakan metode ekonometrika klasik, seperti model *Generalized Autoregressive Conditional Heteroskedasticity* atau GARCH(1,1) oleh Bollerslev (1986) serta *Heterogeneous Autoregressive of Realized Volatility* atau HAR-RV oleh Corsi (2009). Model HAR-RV membedah volatilitas menjadi komponen harian, mingguan, dan bulanan untuk mencerminkan perilaku beragam pelaku pasar yang heterogen. Walaupun model ekonometrika memiliki transparansi matematis yang tinggi, formulasinya terbatas pada asumsi kaku berupa hubungan linear. Di sisi lain, algoritma kecerdasan buatan *Long Short-Term Memory* (LSTM) yang dirintis oleh Hochreiter dan Schmidhuber (1997) memiliki keunggulan komputasi dalam menangkap hubungan non-linear yang kompleks dan dependensi temporal jangka panjang tanpa batasan asumsi distribusi. Kemampuan sel memori internal LSTM menjadikannya pendekatan yang sangat potensial untuk memodelkan dinamika volatilitas aset digital yang rumit secara adaptif. *(122 kata)*

Meskipun LSTM memiliki potensi pemodelan yang kuat, kinerja model ini sangat sensitif terhadap penentuan *hyperparameter*, yaitu parameter konfigurasi eksternal model seperti panjang jendela historis (*lookback*), jumlah neuron (*units*), tingkat regulasi *dropout*, laju pembelajaran (*learning rate*), dan ukuran *batch*. Studi optimasi LSTM pada aset kripto oleh Aldo dkk. (2026) dan Kervanci dan Akay (2023) menunjukkan bahwa penalaan parameter secara manual atau menggunakan pencarian acak (*random search*) memerlukan biaya komputasi besar dan tidak menjamin tercapainya konfigurasi optimal. Untuk mengatasi kendala tersebut, algoritma *Tree-structured Parzen Estimator* (TPE) yang diintegrasikan dalam kerangka kerja Optuna oleh Akiba dkk. (2019) menawarkan solusi optimasi terpandu Bayesian. Algoritma ini memodelkan probabilitas keberhasilan konfigurasi masa lalu secara probabilistik, sehingga proses penalaan ruang *hyperparameter* berjalan jauh lebih efisien, terarah, dan adaptif. *(121 kata)*

Kelemahan paling mendasar yang ditemukan pada riset peramalan berbasis kecerdasan buatan sebelumnya adalah masalah kebocoran data (*data leakage*) dan bias pemilihan metrik. Banyak studi membagi data latih dan uji secara acak atau melakukan normalisasi skala data pada keseluruhan dataset, yang secara tidak sadar memasukkan informasi masa depan ke masa lalu. Buku pedoman rekayasa finansial kuantitatif oleh Lopez de Prado (2018) menegaskan bahwa data deret waktu finansial wajib divalidasi menggunakan *Purged Cross-Validation* dengan menyisipkan jeda pemisah (*purge gap*) guna mencegah kebocoran informasi temporal. Selain itu, penggunaan metrik kesalahan simetris seperti *Mean Squared Error* (MSE) terbukti memberikan evaluasi yang bias. Patton (2011) membuktikan secara matematis bahwa evaluasi volatilitas memerlukan fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) yang tahan terhadap derau proksi dan memberikan penalti realistis terhadap risiko finansial. *(124 kata)*

Bertolak dari kesenjangan penelitian (*research gap*) tersebut, penelitian ini bertujuan membangun pipeline komputasi peramalan *realized volatility* harian Bitcoin yang utuh, terstandarisasi, dan bebas kebocoran data. Data mentah bersumber dari arsip kline 1 jam Binance Vision (2024) periode 2020 hingga 2026 yang diagregasi menjadi *realized variance* harian UTC. Model LSTM dioptimasi menggunakan algoritma Optuna-TPE dengan skema 5-fold *Purged Cross-Validation* pada data pengembangan 2020–2023, divalidasi pada periode 2024–2025, dan diuji secara ketat pada data uji eksternal tahun 2026. Kinerja model dievaluasi menggunakan loss function QLIKE serta diuji signifikansinya terhadap baseline pembanding *persistence*, HAR-RV, dan GARCH(1,1) melalui uji statistik Diebold dan Mariano (1995). Melalui pendekatan komputasi yang terstandarisasi ini, penelitian diharapkan memberikan kontribusi nyata dalam penerapan *machine learning* yang bebas kebocoran pada ranah volatilitas aset kripto. *(123 kata)*

---

### Rumusan Masalah

1. **Bagaimana** merancang arsitektur model *Long Short-Term Memory* (LSTM) teroptimasi Optuna dengan skema *Purged Cross-Validation* untuk mencegah kebocoran data (*data leakage*) pada peramalan *realized volatility* Bitcoin?
2. **Sejauh mana** peningkatan akurasi peramalan yang dihasilkan oleh model LSTM teroptimasi Optuna dibandingkan dengan *baseline persistence* berdasarkan fungsi kerugian asimetris *Quasi-Likelihood* (QLIKE) pada data uji eksternal 2026?
3. **Apakah** model LSTM teroptimasi Optuna mampu menyaingi performa model ekonometrika klasik *Heterogeneous Autoregressive of Realized Volatility* (HAR-RV) dan GARCH(1,1) dalam memproyeksikan volatilitas pasar kripto?

---

### Referensi / Pustaka Utama

1. Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2623–2631). https://doi.org/10.1145/3292500.3330701
2. Aldo, D., Firmansyah, M. R., & Amrustian, M. A. (2026). Comparative analysis of hyperparameter optimization methods for LSTM in cryptocurrency price prediction: An application to TRX–USD. *Jurnal Teknik Informatika (JUTIF)*, 7(3), 2340–2349. https://doi.org/10.52436/1.jutif.2026.7.3.5355
3. Andersen, T. G., Bollerslev, T., Diebold, F. X., & Labys, P. (2003). Modeling and forecasting realized volatility. *Econometrica*, 71(2), 579–625. https://doi.org/10.1111/1468-0262.00418
4. Aswadi, & Ependi, U. (2025). Predicting Bitcoin and Ethereum prices using the Long Short-Term Memory (LSTM) model. *Journal of Information Systems and Informatics*, 7(3), 1228–1243. https://doi.org/10.51519/journalisi.v7i3.1228
5. Binance. (2024). *Binance Vision: Public market data archive*. https://data.binance.vision/
6. Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327. https://doi.org/10.1016/0304-4076(86)90063-1
7. Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics*, 7(2), 174–196. https://doi.org/10.1093/jjfinec/nbp001
8. Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599
9. Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735
10. Kervancı, A., & Akay, M. F. (2023). LSTM hyperparameters optimization with Hparam parameters for Bitcoin price prediction. *Sakarya University Journal of Computer and Information Sciences*, 6(1), 1–9. https://doi.org/10.35377/saucis...1172027
11. Khumaidi, A., Kusmanto, P., & Hikmah, N. (2024). Optimizing Bitcoin price predictions using Long Short-Term Memory algorithm: A deep learning approach. *ILKOM Jurnal Ilmiah*, 16(1), 38–45. https://doi.org/10.33096/ilkom.v16i1.1831.38-45
12. López de Prado, M. (2018). *Advances in financial machine learning*. John Wiley & Sons.
13. Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. *Journal of Econometrics*, 160(1), 246–256. https://doi.org/10.1016/j.jeconom.2010.03.034
14. Ula, M., Sariah, Ilhadi, V., & Sidek, Z. M. (2024). Comparing Long Short-Term Memory and Random Forest accuracy for Bitcoin price forecasting. *MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer*, 23(2), 259–272. https://doi.org/10.30812/matrik.v23i2.3267

---

Jepara, ................................

Pengusul,



**Zaini Leon Musthofa Kamal**  
NIM. 231240001455
