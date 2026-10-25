# Arsip Eksperimen Tahap 2 (Low-Fidelity Screening Bias)

## Keterangan
Eksperimen ini dijalankan dengan search space learning rate lebar (1e-4 s.d. 1e-2) dan budget skrining rendah (10 epoch).

## Temuan Ilmiah
1. Algoritma Optuna TPE memilih **Learning Rate tinggi (0.00817, Trial #15)** karena pada skrining 10 epoch, laju langkah besar melompat lebih cepat sehingga loss 10 epoch tampak lebih kecil. Ini adalah bukti nyata fenomena **Low-Fidelity Bias** (Falkner et al., 2018).
2. Namun pada pelatihan akhir 100 epoch, LR 0.00817 mengalami osilasi gradien dan menghasilkan MAPE 2,61%.
3. Bukti empiris ini menjadi landasan untuk membatasi ruang pencarian learning rate pada rentang kestabilan teoritis Adam (5e-4 s.d. 2e-3, Kingma & Ba 2014) serta menaikkan budget skrining menjadi 25 epoch dengan Early Stopping.
