"""
Perbaiki double '1. 1.' di p183 dan render ulang PDF.
"""
import docx
from pathlib import Path
import win32com.client

DOCX_PATH = Path('03_Naskah_Skripsi/study2/file final/SEMPRO_seminar_revisi_siapsempo_v8.docx')
PDF_PATH = Path('03_Naskah_Skripsi/study2/file final/BAB 1-3.pdf')

doc = docx.Document(str(DOCX_PATH))
for i, p in enumerate(doc.paragraphs):
    if '1. 1. Hipotesis 1' in p.text:
        p.text = p.text.replace('1. 1. Hipotesis 1', '1. Hipotesis 1')
        print(f"Fixed typo in P[{i}]")

doc.save(str(DOCX_PATH))
print("[OK] Saved docx with fixed typo.")

# Render to PDF
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
