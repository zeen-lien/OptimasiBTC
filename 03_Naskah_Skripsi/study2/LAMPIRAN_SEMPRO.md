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
