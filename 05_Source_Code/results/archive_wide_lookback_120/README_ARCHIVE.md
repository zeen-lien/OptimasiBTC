# Arsip Eksperimen Pra-Optimasi (Wide Lookback 7–120 Hari)

## Keterangan
Eksperimen ini dijalankan dengan ruang pencarian (search space) lookback yang sangat lebar (7 sampai 120 hari).

## Temuan Ilmiah
1. Algoritma Optuna TPE memilih **Lookback 114 hari (Trial #33)** karena pada tahap cross-validation data latih (2020-2023 sideways), window panjang memberikan loss in-sample paling kecil (0.000684).
2. Namun, saat diuji pada data uji out-of-sample (Holdout Test 2024 Bull Run), model mengalami **memory lag** berat akibat akumulasi beban memori 4 bulan ke belakang, menghasilkan **MAPE 3,92% (RMSE USD 4.667,03)**.
3. Hasil ini menjadi dasar ilmiah (berdasarkan *Adaptive Market Hypothesis* - Lo, 2004 dan dinamika Cell State LSTM - Fischer & Krauss, 2018) untuk membatasi search space lookback pada domain jangka pendek (7–30 hari) pada eksperimen utama.
