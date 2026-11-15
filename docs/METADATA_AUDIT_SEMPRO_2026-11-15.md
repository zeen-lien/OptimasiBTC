# Audit metadata bibliografi SEMPRO Study 2

> Arsip audit historis. Pengguna mengonfirmasi Mendeley diperiksa dan disetel manual; RIS/BibTeX bukan sumber kerja dan telah dihapus pada 2026-11-15 atas permintaan pengguna. Jangan gunakan laporan ini untuk menyarankan sinkronisasi/Refresh Citations. Audit isi harus berfokus pada sumber yang benar-benar dikutip di DOCX, klaim, dan konsistensi dengan eksperimen.

**Tanggal:** 2026-11-15  
**Mode:** read-only; tidak ada perubahan pada DOCX, PDF, RIS, BibTeX, ataupun Mendeley.  
**Draf utama:** `D:\OneDrive\Desktop\jurnal\03_Naskah_Skripsi\study2\file final\SEMPRO_seminar_revisi.docx`  
**RIS pembanding:** `D:\OneDrive\Desktop\jurnal\references\study2_references.ris`  
**Batas:** `DAFTAR_REFERENSI_STUDY2.md` tidak ditemukan pada path yang diminta audit, maka RIS dan bibliography DOCX digunakan untuk cek silang. Temuan subagent didasarkan pada laman penerbit/rekaman primer; bukan verifikasi duplikasi record lengkap di Mendeley.

## Ringkasan hasil

- 36 entri RIS dicek terhadap sumber primer/penerbit dan bibliografi DOCX.
- Tidak ditemukan DOI identik berulang dalam 36 entri RIS.
- 27 entri lulus cek metadata; 6 butuh penetapan versi/tanggal; 2 berbeda antara RIS dan DOCX; pagination Engle salah satu halaman pada DOCX awal dan kini sudah dikoreksi menjadi 987–1007.
- Database lokal Mendeley hanya memberikan indeks FTS, bukan tabel library penuh. Audit mendapati 36/36 ID sitasi DOCX ada pada indeks FTS, tetapi ini **tidak** membuktikan metadata library benar, daftar pustaka dua arah lengkap, atau tidak ada record duplikat.
- Status lulus metadata tidak berarti klaim substantif sumber sudah diverifikasi per halaman. Matriks klaim ada di `CLAIM_SOURCE_AUDIT_SEMPRO_2026-11-15.md` dan menyatakan audit full-text masih parsial.

## Temuan yang perlu dikoreksi atau diputuskan

| Referensi/record | Bukti sumber primer | Temuan | Langkah koreksi yang disarankan |
|---|---|---|---|
| Engle (1982) | [JSTOR](https://doi.org/10.2307/1912773) | DOCX awal mencantumkan halaman 987–1008; artikel *Econometrica* 50(4) berakhir di 1007. RIS benar: 987–1007. | **Dikoreksi dalam DOCX** ke 987–1007. Record Mendeley tidak diubah; cocokkan record library sebelum refresh field. |
| Diebold & Mariano | [Artikel asli 1995](https://doi.org/10.1080/07350015.1995.10524599) | RIS memakai asli 1995, *JBES* 13(3), 253–263. DOCX memakai reprint 2002, *JBES* 20(1), 134–144. Edisi terkait merupakan karya sama, bukan dua sumber independen. | Pilih edisi yang memang menjadi rujukan; samakan author-year, jurnal, volume, halaman, dan URL di library, sitasi, dan daftar pustaka. Naskah saat ini secara eksplisit menyebut DM (2002). |
| Kingma & Ba | [arXiv 2014](https://arxiv.org/abs/1412.6980) | RIS memakai arXiv 2014; DOCX menyebut ICLR 2015. Dua versi/record publikasi berbeda. | Pilih versi yang dipakai dan samakan tahun serta tipe publikasi. Jangan refresh sebelum metadata library diperbaiki. |
| TensorFlow / Abadi et al. | [Paper Abadi et al.](https://arxiv.org/abs/1603.04467); [TensorFlow docs](https://www.tensorflow.org/) | RIS memakai TensorFlow Developers (2024), homepage; DOCX bibliography memakai Abadi et al. (2016), paper *TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems*. Bukan metadata ekuivalen. | Pilih sumber berdasarkan klaim: kutip paper untuk arsitektur/sistem TensorFlow atau dokumentasi/rilis versi untuk software yang dipakai. Cantumkan versi software eksperimen. |
| Binance | [Binance Vision](https://data.binance.vision/) | RIS menyebut 2024, DOCX mengutip Binance (2026). Homepage live tidak menetapkan tahun publikasi atau file dataset tertentu. | Sitasi arsip spesifik (pasangan, interval, cakupan tanggal/file), versi/tanggal unduh dan tanggal akses yang tercatat; samakan entri dengan bukti data yang benar-benar digunakan. |
| Ula et al. (2024) | [Halaman penerbit MATRIK](https://doi.org/10.30812/matrik.v23i2.3267) | Byline sumber primer/RIS tidak cocok dengan author “Sariah” tambahan pada bibliography DOCX. | Cocokkan langsung byline PDF/laman penerbit; perbaiki author list record dan bibliography sesuai byline. |
| Kervancı & Akay (2023) | [Laman penerbit](https://dergipark.org.tr/en/pub/saucis/article/1172027) | Publisher menampilkan DOI `10.35377/saucis...1172027`; elipsis membuatnya cacat/tidak dapat diperlakukan sebagai DOI terverifikasi. Metadata artikel: *SAUCIS* 6(1), 1–9, terbit 2023-04-30. | Minta DOI benar dari jurnal. Jangan menebak atau mengganti DOI; jika tak tersedia, hapus identifier yang cacat setelah keputusan penulis. |
| López de Prado (2018) | [Rekaman buku Wiley](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086) | DOCX memakai tautan preview SSRN; file lokal hanya preview 61 halaman, bukan buku penuh. | Gunakan metadata buku penerbit sebagai bibliografi jika buku yang dikutip; tandai keterbatasan akses isi, terutama Bab 7. |
| Optuna Development Team (2024) | [Dokumentasi Optuna](https://optuna.readthedocs.io/) | Homepage dokumentasi generik tidak menetapkan versi/tahun tertentu atau API yang digunakan. | Kutip docs versi terkait dan dokumentasikan versi Optuna eksperimen; verifikasi deskripsi `MedianPruner` terhadap API versi itu. |
| Newey & West (1987) | [Artikel jurnal JSTOR](https://doi.org/10.2307/1913610) | Metadata jurnal *Econometrica* 55(3), 703–708, 1987 benar untuk sitasi DOCX. PDF lokal adalah NBER WP 1986, versi awal, bukan edisi jurnal. | Pertahankan metadata jurnal bila itu edisi yang dikutip; nyatakan PDF lokal versi working paper dan jangan gunakan paginasi WP untuk mengklaim paginasi jurnal. |

## Pemeriksaan metadata lainnya

Hasil subagent menyatakan metadata penerbit cocok untuk entri berikut: Aalborg et al. (2019), Akiba et al. (2019), Aldo et al. (2026), Andersen & Bollerslev (1998), Andersen et al. (2003), Ardia et al. (2019), Aswadi & Ependi (2025), Barndorff-Nielsen & Shephard (2002), Bergstra et al. (2011), Bollerslev (1986), Bouthillier et al. (2021), Christensen et al. (2023), Conrad et al. (2018), Corsi (2009), Fawzi et al. (2025), Greff et al. (2017), Hochreiter & Schmidhuber (1997), Katsiampa (2017), Khumaidi et al. (2024), Kim & Won (2018), Künsch (1989), Lim & Zohren (2021), Patton (2011), Srivastava et al. (2014), Wahyuddin et al. (2025), dan Widad et al. (2026). Tautan DOI atau laman penerbit untuk item-item ini tersedia pada metadata setiap sumber dan tidak semuanya dicantumkan ulang di tabel.

## Perubahan yang telah diterapkan

- Bibliografi statis DOCX: Engle pp. 987–1007; Ula et al. tanpa nama tambahan “Sariah”; Kervancı & Akay tanpa DOI cacat, memakai URL laman penerbit dan author detail yang tersedia; Diebold–Mariano diselaraskan ke reprint 2002 yang dikutip naskah; Kingma–Ba diselaraskan dengan ICLR 2015; Abadi et al. (2016) dipakai untuk paper TensorFlow; Binance diberi keterangan dataset BTC/USDT spot klines 1 jam dan retrieval date yang terdokumentasi; Optuna diselaraskan ke versi 5.0.0 di manifest eksperimen.
- RIS/BibTeX diselaraskan untuk Diebold–Mariano, Binance, Kingma–Ba, Optuna, TensorFlow, dan Kervancı & Akay. Tidak ada DOI pengganti yang ditebak.
- Mendeley citation payload di dalam DOCX tidak diubah. Database/library Mendeley tidak diubah, karena struktur lokal hanya FTS dan tak cukup untuk koreksi record yang aman.
- Verifikasi struktur DOCX setelah perubahan: ZIP/XML valid; 108 citation controls, 110 content controls, 30 objek persamaan, 9 tabel. Hash DOCX: `0f386b403e3145c7913b119984f09e2b36af268a438961463f9826da2ea9085`.

## Yang masih butuh konfirmasi / penyelesaian

1. Buka Mendeley dan koreksi record library yang sepadan sebelum refresh fields; perubahan RIS/BibTeX tidak otomatis memperbaiki library.
2. Konfirmasi DOI Kervancı & Akay dengan penerbit; bibliografi memakai URL laman artikel tanpa DOI sementara.
3. Konfirmasi bahwa citation fields Diebold–Mariano, Kingma–Ba, dan Abadi et al. mengacu ke ID record yang sama dengan bibliography yang diperbarui. Jangan refresh sebelum ini dicek.
4. Binance retrieval date 2026-10-28 bersumber dari timeline data akuisisi, tetapi file unduhan individual yang membentuk hash belum dipetakan kembali satu per satu pada sesi ini.
5. Render ulang DOCX di Word dan cek halaman daftar pustaka/flow karena bibliography berubah. Render final baru belum dibuat.
6. Audit klaim full-text Bab I–III masih parsial; Bab IV–V dan metadata duplikasi record library belum diverifikasi.

## Putusan

**Metadata bibliography DOCX dan ekspor RIS/BibTeX telah dikoreksi pada ketidaksesuaian yang dapat dipastikan; library Mendeley belum disinkronkan dan render belum diperbarui.** Jangan Refresh Citations sebelum record library dan citation IDs dikonfirmasi. File berubah: DOCX utama, `study2_references.ris`, `study2_references.bib`, dan catatan audit; hasil eksperimen tidak disentuh.
