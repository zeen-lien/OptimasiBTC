"""
Perbarui Sub-bab I (Hipotesis Penelitian) di SEMPRO_seminar_revisi_siapsempo_v8.docx
menjadi murni H0 dan H1 (tanpa sebutan Hipotesis 1 / Hipotesis 2 atau H1 / H2),
lalu render ulang ke D:\OneDrive\Desktop\jurnal\03_Naskah_Skripsi\study2\file final\BAB 1-3.pdf.
"""

from pathlib import Path
import docx
import win32com.client

DOCX_PATH = Path('03_Naskah_Skripsi/study2/file final/SEMPRO_seminar_revisi_siapsempo_v8.docx')
PDF_PATH = Path('03_Naskah_Skripsi/study2/file final/BAB 1-3.pdf')

doc = docx.Document(str(DOCX_PATH))

# Cek paragraf 181 - 186
print(f"P[181]: {doc.paragraphs[181].text}")
print(f"P[182]: {doc.paragraphs[182].text}")

# Update Sub-bab I
doc.paragraphs[181].text = "I. Hipotesis Penelitian"

p182 = "Berdasarkan landasan teori, tinjauan penelitian terdahulu, dan kerangka pemikiran konseptual yang telah dipaparkan, hipotesis yang diajukan dalam penelitian ini dirumuskan sebagai pasangan Hipotesis Nol (H0) dan Hipotesis Alternatif (H1) sebagai berikut:"

p183 = "H0 (Hipotesis Nol):\n" \
       "Model peramalan deep learning Long Short-Term Memory (LSTM) dengan optimasi hyperparameter Optuna (TPE) tidak menghasilkan akurasi peramalan realized volatility Bitcoin yang lebih baik secara signifikan dibandingkan model baseline Random Walk Persistence dan model ekonometrika HAR-RV berdasarkan fungsi kerugian asimetris Quasi-Likelihood (QLIKE) pada data evaluasi temporal 2026 (E[dt] ≥ 0)."

p184 = "H1 (Hipotesis Alternatif):\n" \
       "Model peramalan deep learning Long Short-Term Memory (LSTM) dengan optimasi hyperparameter Optuna (TPE) menghasilkan akurasi peramalan realized volatility Bitcoin yang lebih baik secara signifikan dibandingkan model baseline Random Walk Persistence dan model ekonometrika HAR-RV berdasarkan fungsi kerugian asimetris Quasi-Likelihood (QLIKE) pada data evaluasi temporal 2026 (E[dt] < 0)."

p185 = "Secara operasional, pembuktian hipotesis di atas diuji melalui dua kriteria inferensial primer:\n" \
       "1. Komparasi terhadap baseline Random Walk Persistence menggunakan uji Diebold–Mariano satu sisi berkoreksi HAC Newey–West pada taraf signifikansi α = 0,05 (d1,t = Loss_QLIKE(LSTM-Optuna)t − Loss_QLIKE(Persistence)t).\n" \
       "2. Komparasi terhadap model ekonometrika HAR-RV menggunakan uji Diebold–Mariano satu sisi berkoreksi HAC Newey–West pada taraf signifikansi α = 0,05 (d2,t = Loss_QLIKE(LSTM-Optuna)t − Loss_QLIKE(HAR-RV)t).\n" \
       "Kriteria keberhasilan (positive outcome) mensyaratkan kedua pengujian H1 terbukti signifikan secara statistik (p < 0,05) dan batas atas selang kepercayaan 95% Moving-Block Bootstrap bernilai di bawah nol. Adapun kinerja model pembanding GARCH(1,1) dan LSTM tanpa penalaan (untuned) dilaporkan dan dievaluasi secara deskriptif sebagai analisis komparasi sekunder untuk mengamati dinamika varians bersyarat linier dan mengukur dampak penalaan hyperparameter, sehingga tidak dirumuskan hipotesis inferensial primer tersendiri."

doc.paragraphs[182].text = p182
doc.paragraphs[183].text = p183
doc.paragraphs[184].text = p184
doc.paragraphs[185].text = p185

doc.save(str(DOCX_PATH))
print(f"[OK] Master DOCX berhasil diperbarui: {DOCX_PATH}")

# Render ulang PDF lewat Word COM
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = False
try:
    d = word.Documents.Open(str(DOCX_PATH.resolve()), ReadOnly=False)
    try:
        d.Fields.Update()
        for t in d.TablesOfContents:
            t.Update()
    except Exception as e:
        print(f"Notice TOC: {e}")
    d.SaveAs2(str(PDF_PATH.resolve()), FileFormat=17)
    d.Close(SaveChanges=False)
    print(f"[OK] Re-rendered PDF at: {PDF_PATH}")
finally:
    word.Quit()
