"""Update SIMULASI_UJIAN_SEMPRO.md safely without regex escape issues."""
from pathlib import Path

MD_PATH = Path("03_Naskah_Skripsi/study2/SIMULASI_UJIAN_SEMPRO.md")
text = MD_PATH.read_text(encoding="utf-8")

# Let's find the section
target_start = '### Pertanyaan Baru: "Bagaimana rumusan Hipotesis Penelitian kamu?'
if target_start in text:
    pos1 = text.find(target_start)
    pos2 = text.find('### ', pos1 + len(target_start))
    
    new_h = """### Pertanyaan: "Bagaimana rumusan Hipotesis Penelitian kamu? Kenapa di naskah diganti menjadi H0 dan H1, bukan H1 dan H2?"
* **🎯 Kata Kunci Hafalan:**
  **"Hipotesis dirumuskan secara baku berpasangan antara H0 (Hipotesis Nol: tidak ada keunggulan signifikan / E[dt] ≥ 0) dan H1 (Hipotesis Alternatif: model usulan unggul signifikan / E[dt] < 0) yang diuji satu sisi pada taraf α = 0,05."**
* **🗣️ Jawaban Lisan ke Penguji:**
  "Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Sesuai dengan kaidah metodologi penelitian kuantitatif yang benar dan arahan Bapak Dosen Pembimbing, penulisan hipotesis tidak boleh menggunakan label 'H1 dan H2' seolah-olah itu urutan hipotesis nomor satu dan dua. Notasi 'H' dalam statistik merujuk pada pasangan hipotesis nol dan alternatif:
  
  * **$H_0$ (Hipotesis Nol):**
    Model *deep learning* LSTM yang dioptimasi Optuna (TPE) **tidak menghasilkan** akurasi peramalan *realized volatility* Bitcoin yang lebih baik secara signifikan dibandingkan model *baseline* Random Walk Persistence dan model ekonometrika HAR-RV berdasarkan fungsi kerugian asimetris QLIKE pada data evaluasi temporal 2026 ($E[d_t] \\ge 0$).
  
  * **$H_1$ (Hipotesis Alternatif / Hipotesis Kerja):**
    Model *deep learning* LSTM yang dioptimasi Optuna (TPE) **menghasilkan** akurasi peramalan *realized volatility* Bitcoin yang lebih baik secara signifikan dibandingkan model *baseline* Random Walk Persistence dan model ekonometrika HAR-RV berdasarkan fungsi kerugian asimetris QLIKE pada data evaluasi temporal 2026 ($E[d_t] < 0$).
  
  Secara operasional, pembuktian penerimaan $H_1$ diuji terhadap dua pembanding primer:
  1. Komparasi vs **Random Walk Persistence** ($d_{1,t} = \\text{Loss}_{\\text{QLIKE}}(\\text{LSTM}) - \\text{Loss}_{\\text{QLIKE}}(\\text{Persistence})$).
  2. Komparasi vs **Model Ekonometrika HAR-RV** ($d_{2,t} = \\text{Loss}_{\\text{QLIKE}}(\\text{LSTM}) - \\text{Loss}_{\\text{QLIKE}}(\\text{HAR-RV})$).
  
  Keduanya diuji secara satu sisi (*one-sided test*) menggunakan uji Diebold–Mariano dengan estimasi HAC Newey–West pada $\\alpha = 0{,}05$ dan Moving-Block Bootstrap 95% CI. Sedangkan model GARCH(1,1) dan LSTM tanpa penalaan (*untuned*) dilaporkan secara deskriptif sebagai analisis komparasi sekunder."
\n\n"""
    if pos2 != -1:
        text = text[:pos1] + new_h + text[pos2:]
    else:
        text = text[:pos1] + new_h
    MD_PATH.write_text(text, encoding="utf-8")
    print("[OK] Replaced cleanly via string slice.")
else:
    print("Target start not found.")
