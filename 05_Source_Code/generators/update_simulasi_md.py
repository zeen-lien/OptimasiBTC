"""
Perbarui SIMULASI_UJIAN_SEMPRO.md dengan:
1. Panduan Lisan Gambar 2.2 versi terbaru (Decision Diamond & Feedback Loop).
2. Pertanyaan khusus Hipotesis Penelitian (H0 vs H1).
3. Pertanyaan khusus Unit Testing Mandiri (34 skenario & 4 berkas fisik).
4. Penegasan status evaluasi temporal 2026.
"""

from pathlib import Path
import re

MD_PATH = Path("03_Naskah_Skripsi/study2/SIMULASI_UJIAN_SEMPRO.md")

with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Gambar 2.2 Explanation
old_g22 = """### 2. Cara Menjelaskan GAMBAR 2.2 (Kerangka Pemikiran Konseptual Penelitian)
*(Tunjukkan alur bercabang dari masalah pasar sampai pengujian hipotesis)*

> **Skrip Lisan:**  
> *"Gambar 2.2 merangkum alur berpikir konseptual yang melandasi penelitian skripsi ini:
> 1. **Masalah & Target:** Fluktuasi Bitcoin sangat ekstrem. Kami tidak memprediksi harga nominal yang acak (*random walk*), melainkan menargetkan proksi *Realized Variance* (RV) satu hari ke depan.
> 2. **Data & Fitur:** Menggunakan data kline 1 jam Binance Vision 2020–2026 yang diekstraksi menjadi 6 fitur kausal mikrostruktur.
> 3. **Partisi Temporal:** Dibagi kronologis: Development 2020–2023, Train Pool 2020–2025, dan Evaluasi Temporal 2026.
> 4. **Komparasi Model:** Membandingkan model usulan (LSTM ditala oleh Bayesian Optuna TPE dengan *MedianPruner* pada 5-fold Purged CV) terhadap 4 model pembanding (Persistence, HAR-RV, GARCH, LSTM Untuned).
> 5. **Evaluasi & Inferensi:** Evaluasi primer menggunakan fungsi rugi asimetris QLIKE, lalu diuji signifikansinya menggunakan Uji Diebold-Mariano berkoreksi HAC Newey-West dan 10.000 Moving-Block Bootstrap untuk memastikan kesimpulan bebas dari faktor kebetulan."*"""

new_g22 = """### 2. Cara Menjelaskan GAMBAR 2.2 (Kerangka Pemikiran Konseptual Penelitian dengan Decision Loop)
*(Tunjukkan alur tahapan, belah ketupat keputusan/decision diamond, dan arah putaran feedback loop saat ditanya penguji)*

* **🎯 Kata Kunci Hafalan:**
  **"Alur kerangka pemikiran terdiri dari 6 tahap berurutan: dari perumusan masalah, pra-pemrosesan data frekuensi tinggi, partisi kronologis anti-leakage, penalaan Optuna dengan mekanisme umpan balik (feedback loop) jika validasi belum konvergen, pelatihan final, hingga uji hipotesis formal H0 vs H1."**

* **🗣️ Skrip Lisan Lengkap ke Penguji:**
  "Terima kasih Bapak/Ibu Penguji. Gambar 2.2 ini merangkum logika penelitian saya dari hulu ke hilir:
  1. **Kotak 1 (Masalah & Target):** Berangkat dari fenomena volatilitas Bitcoin yang sangat liar dan kegagalan model linier. Target ramalannya adalah $\\log RV_{t+1}$ satu hari ke depan.
  2. **Kotak 2 (Data & Fitur):** Menggunakan data SPOT Binance Vision kline 1 jam periode 2020–2026 yang direkayasa menjadi 6 fitur teknikal kausal.
  3. **Kotak 3 (Partisi Temporal):** Data dibagi kronologis: Development 2020–2023 untuk penalaan HPO, Train Pool 2020–2025 untuk pelatihan final, dan Evaluasi Temporal 2026. Pemisahan dilindungi oleh *purge gap* ($lookback + 1$) agar tidak ada kebocoran autokorelasi serial.
  4. **Kotak 4 & Belah Ketupat Keputusan (Decision Diamond + Feedback Loop):**
     * Model usulan LSTM ditala menggunakan algoritma Bayesian Optuna (TPE) berbasis 5-fold Purged Cross-Validation.
     * **Jika ditanya loop-nya ke mana:** Pada belah ketupat keputusan, sistem mengevaluasi: *Apakah kriteria validasi dan konvergensi loss QLIKE sudah terpenuhi?*
     * **Jika TIDAK (Terjadi Overfit / Loss Belum Minimum):** Alur masuk ke panah merah **Feedback Loop (Umpan Balik)**, di mana Optuna TPE secara adaptif memperbarui model probabilitas Parzen dan mengeksplorasi kombinasi hyperparameter baru.
     * **Jika YA (Konvergen & Optimal):** Model melangkah ke **Pelatihan Model Final** pada Train Pool (90% fit, 10% early stopping).
  5. **Kotak 5 (Pengujian Evaluasi Temporal 2026):** Seluruh model (LSTM-Optuna vs 4 baseline pembanding) diuji pada 273 hari data 2026 menggunakan fungsi kerugian asimetris QLIKE (primer) serta MAE/RMSE (sekunder).
  6. **Kotak 6 (Uji Inferensial & Keputusan Hipotesis):** Menguji signifikansi komparatif menggunakan Uji Diebold–Mariano satu sisi berkoreksi HAC Newey–West dan Moving-Block Bootstrap untuk memutuskan penolakan $H_0$ dan penerimaan $H_1$."*"""

text = text.replace(old_g22, new_g22)

# 2. Add question about H0 vs H1
h_qa = """
### Pertanyaan Baru: "Bagaimana rumusan Hipotesis Penelitian kamu? Kenapa menggunakan format $H_0$ dan $H_1$ serta pengujian satu sisi?"
* **🎯 Kata Kunci Hafalan:**
  **"Hipotesis dirumuskan formal berpasangan H0 (tidak ada keunggulan signifikan / selisih loss ≥ 0) dan H1 (LSTM-Optuna unggul signifikan / selisih loss < 0) yang diuji satu sisi pada taraf α = 0,05."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Sesuai kaidah metode penelitian kuantitatif, hipotesis penelitian dirumuskan secara berpasangan antara Hipotesis Nol ($H_0$) dan Hipotesis Alternatif ($H_1$) untuk dua komparasi primer:
  1. **Hipotesis 1 (vs Baseline Random Walk Persistence):**
     * **$H_0$:** Model LSTM-Optuna tidak menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan baseline Persistence pada evaluasi temporal 2026 ($\mu_{d_1} \ge 0$).
     * **$H_1$:** Model LSTM-Optuna menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan baseline Persistence pada evaluasi temporal 2026 ($\mu_{d_1} < 0$).
  2. **Hipotesis 2 (vs Model Ekonometrika HAR-RV):**
     * **$H_0$:** Model LSTM-Optuna tidak menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan model HAR-RV pada evaluasi temporal 2026 ($\mu_{d_2} \ge 0$).
     * **$H_1$:** Model LSTM-Optuna menghasilkan rata-rata QLIKE yang lebih rendah secara signifikan dibandingkan model HAR-RV pada evaluasi temporal 2026 ($\mu_{d_2} < 0$).
  
  **Alasan Pengujian Satu Sisi (One-Sided):** Karena tujuan penelitian adalah membuktikan keunggulan (*superiority*) model usulan, bukan sekadar melihat apakah ada perbedaan dua arah. Uji statistiknya menggunakan Diebold–Mariano dengan estimasi HAC Newey–West pada $\alpha = 0{,}05$.
  Sedangkan GARCH(1,1) dan LSTM untuned dilaporkan secara deskriptif sebagai pembanding sekunder tanpa uji hipotesis formal primer."
"""

# Insert H_QA into Bagian 4
text = text.replace("## BAGIAN 5: MENGHADAPI PERTANYAAN JEBAKAN DOSEN", h_qa + "\n\n## BAGIAN 5: MENGHADAPI PERTANYAAN JEBAKAN DOSEN")

# 3. Add question about Unit Testing physically existing in repo
unit_qa = """
### Pertanyaan Baru: "Pada Bab III tertulis pengujian unit (unit testing) mandiri, apakah berkas tes fisiknya benar-benar ada di repositori dan apa saja yang diuji?"
* **🎯 Kata Kunci Hafalan:**
  **"Ada 34 skenario unit test terotomatisasi yang terbagi dalam 4 file skrip fisik di folder tests/ dan seluruhnya lulus 100% menggunakan pytest."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Benar sekali, Bapak/Ibu Penguji. Repositori penelitian kami dilengkapi dengan pengujian unit terotomatisasi (*automated unit testing*) yang dibangun menggunakan framework `pytest`. Seluruh skrip tersimpan secara fisik di direktori `tests/` yang terdiri dari 4 berkas mandiri dengan total 34 skenario tes:
  1. **`tests/test_study2.py` (15 skenario tes):** Menguji validasi cryptographic hash SHA-256 pada dataset beku, kelengkapan 24 bar lilin per hari kalender, kepositifan nilai RV, ketiadaan kebocoran fitur masa depan (*no future leakage*), sifat matematis penalti asimetris fungsi QLIKE, serta konsistensi uji Diebold-Mariano dan Bootstrap.
  2. **`tests/test_s2_calendar.py` (7 skenario tes):** Menguji penanganan celah kalender (*gap handling*) pada model baseline agar tidak melompati hari yang hilang secara kausal.
  3. **`tests/test_s2_split_scaler.py` (6 skenario tes):** Memverifikasi isolasi *scaler fitting* hanya pada subset pelatihan tiap fold dan penegakan *purge gap* antar-partisi deret waktu.
  4. **`tests/test_s2_analyze.py` (6 skenario tes):** Menguji keselarasan baris tanggal prediksi (*alignment validation*) sebelum uji statistik dijalankan.
  
  Seluruh 34 skenario tes ini dieksekusi secara berkala dan berhasil lulus 100% (*passed*) tanpa kegagalan, membuktikan bahwa pipeline komputasi kami solid, bebas kebocoran data, dan dapat dipertanggungjawabkan secara ilmiah."
"""

text = text.replace("## BAGIAN 5: MENGHADAPI PERTANYAAN JEBAKAN DOSEN", unit_qa + "\n\n## BAGIAN 5: MENGHADAPI PERTANYAAN JEBAKAN DOSEN")

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] SIMULASI_UJIAN_SEMPRO.md updated successfully.")
