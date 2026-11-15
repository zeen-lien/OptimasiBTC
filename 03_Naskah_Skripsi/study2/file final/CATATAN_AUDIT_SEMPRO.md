# Catatan Revisi dan Audit SEMPRO

Dokumen kerja utama: `SEMPRO_seminar_revisi.docx`  
Riwayat: versi ini sebelumnya disusun dari `SEMPRO_revisi.docx`; `SEMPRO.docx` adalah dokumen asli. Atas persetujuan eksplisit peneliti pada 2026-11-15, kedua DOCX lama tersebut dihapus dari folder final. Hanya dokumen seminar dan catatan audit dipertahankan di folder itu.

## Perubahan yang diterapkan

- Menyelaraskan deskripsi implementasi CV: `gap = lookback + 1`; scaler dan model final fit pada 90% sampel kronologis awal Train Pool; 10% terakhir dipakai untuk early stopping; tidak ada refit setelah pemilihan epoch.
- Revisi 2026-11-15: memperbaiki kriteria Positive agar mencakup CI bootstrap sesuai protokol; menambahkan catatan deviasi CV gap pada uraian; menambah satu tahap agar teks metode cocok dengan delapan tahap diagram; memperjelas 2.191 sebagai jumlah baris Train Pool, bukan sekuens; mencantumkan `layers=1` untuk LSTM untuned; mengganti dua diagram metodologis dengan versi yang menyebut target proksi, paparan test, prosedur 90/10, dan deviasi gap.
- Menjelaskan periode 2024–2025 sebagai bagian Train Pool yang memengaruhi early stopping, bukan evaluasi independen.
- Mengganti “uji eksternal” dengan “evaluasi temporal 2026” dan mempertahankan batas paparan sebelumnya.
- Memperbaiki interpretasi jumlah: total 2.464 observasi valid dari rentang 2.465 tanggal kalender; pembagian valid 1.460 + 731 + 273. Jumlah tersebut bukan jumlah semua tanggal kalender tiap periode.
- Menjelaskan target RV aktual sebagai proksi operasional jumlah kuadrat return open-to-close per bar 1 jam; ukuran tidak memasukkan return antarbar dan bukan seluruh perubahan harga harian.
- Membatasi klaim presisi RV, kelemahan model parametrik, purged CV, robust QLIKE, serta asimetri penalti QLIKE agar tidak terlalu mutlak.
- Mendefinisikan Δ QLIKE sebagai loss LSTM dikurangi baseline; bootstrap menjadi dukungan deskriptif, DM menjadi inferensi utama.
- Menjelaskan horizon HAR tujuh/22 observasi sebagai spesifikasi model pada pasar 24/7, bukan hari kerja bursa; memperbaiki horizon fitur rolling sebagai observasi kalender.
- Menjelaskan bahwa perbandingan LSTM untuned dan Optuna tidak otomatis mengisolasi efek Optuna dari semua pilihan konfigurasi.
- Mempertahankan payload sitasi Mendeley dan objek persamaan; tabel temporal diset tanpa split baris dan dengan header berulang.

## Pemeriksaan struktur dan render

- Metadata teks bibliografi lama pernah dikoreksi, tetapi Mendeley telah dikonfirmasi pengguna sebagai sumber manual dan ekspor RIS/BibTeX telah dihapus; jangan perlakukan ekspor tersebut sebagai workflow atau syarat audit.
- DOCX ZIP/XML setelah revisi 2026-11-15 lolos validasi; 108 citation controls, 110 content controls, 30 objek persamaan, 9 tabel. Citation payload tidak diubah. Hash DOCX terkini: `dd18993108dc16a9b5b8cb1862f595202c90b4487195013b06d57c2eb96eb66f`.
- Diagram Gambar 2.2 dan 3.1 diganti di DOCX. PNG sumber diperiksa langsung; PDF terbaru belum berhasil dirender karena Word COM tidak dapat dijalankan tanpa membuka GUI/foreground. Jadi paginasi, keterbacaan dalam ukuran halaman, tabel/persamaan, dan daftar pustaka setelah perubahan belum tervalidasi.
- Daftar isi/field diperbarui pada versi sebelumnya. Belum dibuktikan apakah pagination tetap sama setelah dua diagram diganti; PDF sebelumnya mendahului revisi terakhir dan tidak boleh disebut render final.
- Tidak menjalankan ulang HPO, model, analyzer, atau test 2026; hasil historis tetap tidak disentuh.

## Batas tujuan dan audit lintas artefak (2026-11-15)

- Ekspor `D:\OneDrive\Desktop\jurnal\references\study2_references.ris` dan `study2_references.bib` bukan sumber kerja pengguna dan telah dihapus atas permintaan pengguna. Metadata Mendeley telah dikonfirmasi manual oleh pengguna; jangan memakai RIS/BibTeX atau meminta sinkronisasi Mendeley sebagai langkah audit berikutnya.
- Fokus audit aktif: kesesuaian paper dengan klaim/sitasi, kesesuaian protokol dan kode dengan eksperimen historis, serta ketepatan angka, diagram, tabel, dan persamaan proposal terhadap artefak eksperimen. Jangan jalankan ulang model, HPO, analyzer, atau evaluasi test.
- Pemeriksaan kode/config dan artefak TEST historis: Optuna-LSTM QLIKE 0.40333, untuned 0.34422, persistence 0.80521, HAR-RV 0.46846, GARCH 0.44898; DM vs persistence p<0.0001 dan vs HAR p=0.0534. Dibaca dari `results_analysis.md`, bukan dihitung ulang. Kriteria Positive di naskah telah diselaraskan dengan protokol; hasil tetap mixed.
- Perbedaan kode–protokol: CV memakai `gap=lookback+1` alih-alih `lookback`; final LSTM memakai 90% fit/10% early stopping tanpa refit seluruh Train Pool; test 2026 sempat terlihat saat smoke. Deviasi gap kini disebut eksplisit di uraian dan dua diagram; prosedur final dan keterbatasan test dicantumkan di Gambar 2.2/3.1. Belum seluruh teks Bab I–III dicek untuk sisa istilah lama.
- Struktur DOCX terakhir: 9 tabel, 30 objek persamaan, 108 citation controls, 110 content controls. DOCX XML/ZIP valid. PDF dari revisi terbaru belum dibuat.

## Audit lanjutan dan batas yang belum tuntas

- Matriks klaim–sumber–halaman Bab I–III tersedia di `D:\OneDrive\Desktop\jurnal\docs\CLAIM_SOURCE_AUDIT_SEMPRO_2026-11-15.md`.
- Audit sumber–klaim Bab I–III tersedia di `D:\OneDrive\Desktop\jurnal\docs\CLAIM_SOURCE_AUDIT_SEMPRO_2026-11-15.md`, namun masih parsial; tidak semua klaim atau Bab IV–V dicek full-text. Temuan yang masih perlu dibersihkan: klaim random-walk/“hampir mustahil”, klaim universal QLIKE, kelemahan studi terdahulu, novelty, dan manfaat risiko yang belum merata dukungan sumbernya.
- Mendeley sudah dicek dan disetel manual oleh pengguna. Audit ini tidak memeriksa ulang library dan tidak meminta Refresh Citations.
- Kecocokan seluruh sitasi dan klaim belum diaudit full-text dua arah. Beberapa sumber scan/preview belum diverifikasi per halaman. Jangan klaim audit referensi selesai.
- Pemeriksaan visual gambar hanya mengonfirmasi bahwa PNG pengganti terbaca dan memuat keterangan metode yang dibutuhkan; ukuran cetak dan pagination belum dicek melalui render PDF terbaru.
- Folder `file final` kini hanya memuat `SEMPRO_seminar_revisi.docx` dan catatan ini. `SEMPRO.docx` dan `SEMPRO_revisi.docx` dihapus pada 2026-11-15 atas persetujuan eksplisit peneliti. Keduanya bukan lagi salinan cadangan yang tersedia.

## Konfirmasi peneliti/pembimbing

- Dokumentasikan sebagai amendemen bertanggal perbedaan protokol terkunci dengan kode: CV gap `lookback` vs `lookback + 1`; final fit seluruh Train Pool menurut protokol vs implementasi 90%/10% early stopping. Jangan ubah hasil historis secara diam-diam.
- Pertahankan label target sebagai “proksi operasional berbasis return open-to-close per bar 1 jam”; jangan hitung ulang hasil untuk memilih definisi setelah paparan hasil test.
- Tutup audit klaim dan metadata per sumber, termasuk DOI/byline dan kecocokan semua halaman yang dirujuk. Pastikan metadata Mendeley benar sebelum Refresh Citations.
- Pembimbing perlu menyetujui pencatatan pasca-eksekusi tentang deviasi protokol: CV gap `lookback` vs `lookback + 1`, dan final fit seluruh Train Pool pada protokol vs 90/10 early stopping pada implementasi. Hasil historis tidak diubah.
- Setelah keputusan metode, render DOCX di Microsoft Word dan audit seluruh halaman, khususnya Gambar 2.2/3.1, persamaan (3.12)–(3.13), tabel 3.1–3.6, daftar isi, dan daftar pustaka.
