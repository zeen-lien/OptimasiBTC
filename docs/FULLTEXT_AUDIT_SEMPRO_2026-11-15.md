# Audit full-text follow-up and SEMPRO revision log

Tanggal: 15 November 2026  
Versi yang diperiksa: `SEMPRO_seminar_revisi_siapsempo_v8.docx`

## Keputusan layout
- Halaman **PERSETUJUAN PEMBIMBING** sengaja tidak ada; halaman terpisah akan dibuat nanti.
- Entri halaman tersebut sudah dikeluarkan dari daftar isi. Hasil PDF tidak memuat entri itu atau `Bookmark not defined`.

## Verifikasi full-text sumber scan
OCR Tesseract 5.4.0 dipakai untuk halaman scan. OCR membantu membaca, tetapi hasil OCR perlu dibandingkan dengan tampilan scan jika akurasi kutipan kritis.

| Sumber | Bukti teks/halaman | Kesimpulan audit |
|---|---|---|
| Andersen & Bollerslev (1998) | PDF pp. 1–2 dan 4 menyebut fakta volatility clustering dan persistensi lintas return spekulatif; PDF pp. 13–14 menjelaskan jumlah kuadrat return intrahari untuk meningkatkan ukuran volatilitas ex-post. | Mendukung latar teori volatility clustering dan nilai data intrahari. Bukan bukti Bitcoin, dan tidak membuktikan proksi open-to-close penelitian ini sama dengan RV standar. Klaim naskah dibatasi pada sifat umum dan proksi operasional. |
| Engle (1982) | PDF p. 2 (halaman jurnal tercetak 987) memuat judul/byline/model ARCH; PDF p. 3 menampilkan bentuk model; akhir scan memuat halaman tercetak 1007. | Mendukung atribusi ARCH dan persamaan bersyarat. Metadata cover PDF menyatakan 987–1008, sedangkan halaman akhir artikel yang terbaca bernomor 1007. Daftar pustaka naskah memakai 987–1007; pagination penerbit perlu cek silang bila harus dipastikan. |
| Künsch (1989) | PDF pp. 1–5 memperkenalkan jackknife/bootstrap untuk pengamatan stasioner, mengambil blok panjang `l`, dan membahas pemilihan `l` bergantung ukuran sampel serta kekuatan dependensi. | Mendukung metode bootstrap blok untuk data bergantung. Tidak menetapkan blok 20 hari atau 10.000 repetisi sebagai pilihan universal; naskah menyajikannya sebagai parameter rancangan. Klaim dilunakkan: bootstrap blok mengurangi ketergantungan pada aproksimasi normalitas asimtotik, bukan jaminan ketangguhan umum. |
| Newey & West (1986 WP) | OCR PDF p. 1 mengidentifikasi NBER Technical Working Paper 55, April 1986; PDF p. 5 menyebut modified Bartlett weights. | PDF lokal adalah versi working paper 1986, bukan artikel *Econometrica* 1987 yang tercantum di bibliografi. Metadata dan halaman edisi jurnal tidak diverifikasi dari file lokal. |

## Klaim/entri lain yang diverifikasi
- **Katsiampa (2017), PDF p. 8, Tabel A.2:** untuk AR-GARCH, `α=0.2363` dan `β=0.7753`, sehingga jumlahnya `1.0116` (sedikit di atas satu). Naskah kini menyatakan perkiraan AR-GARCH `≈1,01` dan menghindari klaim stasioneritas kovarians untuk parameter itu. Studi membandingkan goodness-of-fit in-sample; tidak melaporkan protokol forecast out-of-sample.
- **Ardia et al. (2019), PDF pp. 1–6:** menguji regime changes memakai Markov-switching GARCH pada Bitcoin returns; memakai 1.000 return rolling estimation dan 1.355 observasi VaR out-of-sample, parameter diperbarui tiap 10 observasi (PDF p. 5). Tabel 2.1 menyebut rolling estimation dengan tepat. Studi berfokus pada GARCH/MSGARCH dan VaR, bukan deep learning.
- **Conrad et al. (2018), PDF pp. 1–4, 10:** GARCH-MIDAS untuk komponen volatilitas jangka panjang/pendek Bitcoin, dengan explanatory variables makro/keuangan; menilai hasil in-/out-of-sample dan membahas potensi forecast. Keterbatasan pada pendekatan ekonometrik parametrik/kovariat eksternal adalah peringkasan ruang lingkup, bukan klaim bahwa model tidak mampu forecasting.
- **Kim & Won (2018), PDF pp. 8–23:** objek KOSPI 200; pendekatan hybrid GARCH-type dan LSTM, ada single GARCH dan single LSTM pembanding, dengan evaluasi out-of-sample serta uji DM/WS. Deskripsi “Train-Test chronological” di Tabel 2.1 diganti menjadi “In-sample fitting dan out-of-sample forecasting”; istilah chronology tidak dipastikan eksplisit di sumber.
- **Christensen et al. (2023), PDF p. 13:** data 29 dari 30 konstituen DJIA sebelum perubahan 31 Agustus 2020. Tabel 2.1 membedakan saham individual dari indeks agregat.
- **Gambar LSTM:** teks visual “Gerbang Keluar (Output)” sudah diperbaiki; sebelumnya tertulis “Gerbang Keluar (Outputt)”. Persamaan dan panah tetap utuh.
- **Tabel 2.1:** baris Katsiampa, Ardia, Conrad, Kim–Won, Christensen dicek terhadap sumber lokal; baris lain tetap bergantung pada audit sebelumnya dan cakupan PDF yang ada.

## Perubahan pada salinan v8
- Daftar isi: menghapus entri persetujuan yang memang tidak ada, bukan memulihkan halaman.
- Katsiampa: klaim α+β diberi nilai sumber `≈1,01`.
- Künsch: ejaan nama dan tanda baca diperbaiki; klaim bootstrap dilunakkan.
- Tabel 2.1 Kim–Won: label validasi diperhalus.
- Diagram LSTM: typo label diperbaiki.
- Citation fields, isi library Mendeley, data eksperimen, kode eksperimen, dan hasil tidak diubah. Tidak ada *Refresh Citations*, model training, atau test run.

## Pemeriksaan render
- DOCX dibuka dengan Microsoft Word automation; render PDF 62 halaman.
- Pemeriksaan visual dilakukan pada daftar isi, diagram kerangka, diagram alur, diagram sel LSTM, Persamaan (3.12)–(3.13), tabel evaluasi, dan halaman jadwal. Tata letak pada halaman tersebut terbaca dan rapi; belum setiap halaman dari 62 diperiksa visual satu per satu.
- Struktur v8: 109 citation controls Mendeley, 30 objek persamaan Word, 7 tabel Word, 5 inline shapes. Tidak ada perubahan jumlah kontrol, persamaan, tabel, atau shapes pada tahap v3–v8 selain satu entri daftar isi dihapus.
- PDF hasil render disimpan di temp lokal, bukan deliverable final.

## Sisa batas / keputusan pembimbing
1. Protokol terkunci menetapkan `gap = lookback`, sementara kode memakai `gap = lookback + 1`. Naskah/diagram menyebut deviasi secara terbuka; perlu keputusan pembimbing apakah desain dipertahankan atau eksperimen dijalankan ulang. Hasil lama tidak disamakan dengan protokol.
2. Tahun evaluasi 2026 sebagian pernah ditinjau; tidak boleh disebut holdout eksternal yang sepenuhnya independen.
3. File Mendeley tidak diakses; audit memeriksa payload sitasi dalam DOCX dan bibliografi hasil render, bukan snapshot database/library.
4. Engle page range belum diselesaikan: PDF metadata menyebut 987–1008; halaman akhir scan menampilkan 1007. Verifikasi silang ke rekaman penerbit/perpustakaan masih diperlukan bila harus dipastikan final.
5. Full-text semua 33 referensi dan semua klaim seluruh bab belum dipetakan satu-per-satu di catatan ini. Baris 6+ Tabel 2.1 serta beberapa klaim Bab I masih perlu audit jika standar berarti setiap klaim tanpa pengecualian.
6. Proposal belum bisa dinyatakan siap seminar tanpa syarat sampai pembimbing menyetujui deviasi gap dan target proksi, serta semua halaman final diperiksa penulis.

## File kerja sementara
Skrip OCR, OCR text, render PDF, crop gambar, dan skrip pemeriksaan disimpan di `C:\Users\R1N0C\AppData\Local\Temp\opencode`; bukan file proyek. OCR menambah file teks sementara di folder temp itu.
