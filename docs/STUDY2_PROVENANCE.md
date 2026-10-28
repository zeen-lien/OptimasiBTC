# PROVENANCE STUDY 2 - Timeline apa yang terlihat, kapan

Tujuan: dokumen ini merekam urutan peristiwa Study 2 secara jujur, sehingga
pembaca/auditor bisa memeriksa sendiri bahwa tidak ada keputusan post-hoc
yang dibuat setelah melihat hasil test.

## Timeline (semua 2026-10-28, waktu lokal)

1. **Validasi format data (pra-protokol).**
   Permintaan HEAD/GET terhadap beberapa file bulanan Binance Vision
   (termasuk 2026-09) untuk memeriksa: status HTTP, ukuran, satuan timestamp
   (ms vs µs), kelengkapan 24 bar/jam. **Tidak ada** RV, fitur, atau statistik
   yang dihitung. Info yang didapat: 2026-10 belum tersedia → test window
   dikunci berakhir 2026-09-30 (kendala eksternal, dicatat di protokol §1).

2. **Protokol dikunci (hash pertama `20c34ee8…`).**
   `docs/STUDY2_PROTOCOL.md` + `docs/STUDY2_GAP.md` ditulis dan di-hash
   SEBELUM pipeline data dibangun.

3. **Build pertama GAGAL pada integrity check.**
   15 hari (2020-01..2023-03) punya 19-23 bar (maintenance Binance); build
   berhenti SEBELUM satu pun nilai RV dihitung.

4. **Amandemen A1 dibuat & protokol di-hash ulang (`72c75880…ba3`).**
   Aturan: drop hari <20 bar (realisasi: hanya 2020-02-19, 19 bar), pertahankan
   hari 20-23 bar, window validasi/test wajib 24 bar penuh, sampel yang
   melintasi celah kalender dikeluarkan. Konteks waktu: sebelum ada statistik
   target. Setelah ini protokol TIDAK diubah lagi.

5. **Data dibangun & dibekukan.**
   2.464 hari; CSV sha256 `ec2e3fb4…e08b`; statistik deskriptif RV (count,
   mean, std, min, max, kuartil) dicetak pada tahap ini - ini statistik
   deskriptif training pool, bukan metrik model, dan tidak menentukan
   keputusan apa pun karena semua pilihan sudah terkunci di protokol.

6. **Modul & test.** s2_stats, s2_models, s2_runlog, s2_optuna_search,
   s2_final_run, s2_analyze ditulis; smoke HPO (1 trial × 2 epoch) deterministik
   (dua run identik); 15 unit test lulus. Sanity dev-only: QLIKE persistence
   0.846 vs HAR 0.598 (informasi dev).

7. **Smoke final runner (2 seed × 2 epoch) mencetak angka placeholder LSTM
   DAN angka baseline test-window (persistence 0.80521, HAR 0.46846,
   GARCH 0.44898).** Angka baseline adalah final (tidak bergantung epoch),
   sehingga secara tidak sengaja baseline test terlihat lebih awal. Catatan
   penting: semua keputusan model (arsitektur, baselines, seeds, metrik,
   split, kriteria sukses) sudah terkunci di protokol ber-hash SEBELUM titik
   ini, sehingga angka tersebut tidak dapat dan tidak digunakan untuk
   mengubah apa pun. Fit LSTM di smoke adalah model 2-epoch yang tidak
   berarti; angka final hanya dari final run.

8. **HPO penuh (dev-only).** 50 trial, 47 complete / 3 pruned; best trial 26:
   lookback 16, units 22, layers 1, dropout 0.1, lr 5.117e-4, batch 16;
   mean CV QLIKE 0.48937. Informasi dev saja.

9. **Final run (5 seed × 2 fit × 2 model + baseline).** Prediksi 2026
   dihasilkan di sini. Analisis one-shot (`s2_analyze.py`) dijalankan
   SETELAH final run selesai; verdict mengikuti kriteria protokol §9.

## Aturan yang berlaku sejak langkah 4

- Baseline, metrik, split, seed, test window: **tidak boleh diubah**.
- Bila hasil = negative/mixed, dilaporkan apa adanya.
