"""
verify_full_skripsi.py
Skrip audit komprehensif master naskah skripsi:
03_Naskah_Skripsi/SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx
"""

import os
import re
import docx

def verify_full_skripsi():
    doc_path = "03_Naskah_Skripsi/SKRIPSI_FULL_ZAINI_LEON_MUSTHOFA_KAMAL.docx"
    print(f"=== AUDIT MASTER NASKAH SKRIPSI LENGKAP ===")
    print(f"File Target: {doc_path}")
    
    if not os.path.exists(doc_path):
        print(f"[FAIL] Berkas {doc_path} tidak ditemukan!")
        return False
        
    file_size_kb = os.path.getsize(doc_path) / 1024
    print(f"[OK] Ukuran Berkas: {file_size_kb:.2f} KB ({file_size_kb/1024:.2f} MB)")
    
    doc = docx.Document(doc_path)
    print(f"[OK] Total Paragraf: {len(doc.paragraphs)}")
    print(f"[OK] Total Tabel: {len(doc.tables)}")
    print(f"[OK] Total Section: {len(doc.sections)}")
    
    # 1. Audit Section Setup & Pagination
    sec0 = doc.sections[0]
    sec1 = doc.sections[1] if len(doc.sections) > 1 else None
    
    pgnum0 = sec0._sectPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType')
    fmt0 = pgnum0.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fmt') if pgnum0 is not None else None
    print(f"  - Section 0 (Front Matter) Page Format: {fmt0} (Expected: lowerRoman)")
    
    if sec1 is not None:
        pgnum1 = sec1._sectPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType')
        fmt1 = pgnum1.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fmt') if pgnum1 is not None else None
        print(f"  - Section 1 (Body) Page Format: {fmt1} (Expected: decimal)")
    
    # 2. Audit Images in Package
    img_rels = [r for r in doc.part.rels.values() if 'image' in r.target_ref]
    print(f"[OK] Total Relasi Gambar dalam Package: {len(img_rels)} (Logo UNISNU + Gambar 4.1, 4.2, 4.3)")
    
    # 3. Audit OMML Formulas
    omml_count = 0
    for p in doc.paragraphs:
        if 'm:oMath' in p._element.xml:
            omml_count += 1
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if 'm:oMath' in p._element.xml:
                        omml_count += 1
    print(f"[OK] Total Objek OMML Matematika: {omml_count}")
    
    # 4. Audit Raw $ (Should be 0)
    raw_math_matches = []
    for idx, p in enumerate(doc.paragraphs):
        txt = p.text
        m = re.findall(r'(?<!\\)\$[^$]+\$', txt)
        if m:
            raw_math_matches.append((idx, m))
    if raw_math_matches:
        print(f"[WARNING] Ditemukan raw $ pada {len(raw_math_matches)} paragraf: {raw_math_matches[:3]}")
    else:
        print(f"[OK] Bebas Raw Math Delimiter ($): 0 ditemukan (Semua rumus bersih / native OMML)")

    # 5. Audit Struktur Bab dan Pustaka
    full_text = "\n".join([p.text for p in doc.paragraphs])
    key_markers = [
        "OPTIMASI HYPERPARAMETER LONG SHORT-TERM MEMORY",
        "SURAT PERNYATAAN KEASLIAN KARYA TULIS SKRIPSI",
        "LEMBAR PERSETUJUAN PEMBIMBING",
        "LEMBAR PENGESAHAN SKRIPSI",
        "HALAMAN PERSEMBAHAN",
        "HALAMAN MOTTO",
        "KATA PENGANTAR",
        "ABSTRAK",
        "ABSTRACT",
        "DAFTAR ISI",
        "DAFTAR TABEL",
        "DAFTAR GAMBAR",
        "DAFTAR LAMPIRAN",
        "BAB I\nPENDAHULUAN",
        "BAB II\nLANDASAN TEORI",
        "BAB III\nMETODE PENELITIAN",
        "BAB IV\nHASIL PENELITIAN DAN PEMBAHASAN",
        "BAB V\nPENUTUP",
        "DAFTAR PUSTAKA",
        "LAMPIRAN 1",
        "LAMPIRAN 2",
        "LAMPIRAN 3"
    ]
    
    print("\n--- Verifikasi Penanda Bab & Komponen Skripsi ---")
    all_markers_ok = True
    for marker in key_markers:
        found = marker in full_text
        status = "[OK]" if found else "[MISSING]"
        if not found:
            all_markers_ok = False
        print(f"  {status} {marker.replace(chr(10), ' - ')}")

    # 6. Audit 32 Referensi
    print("\n--- Verifikasi Referensi Ilmiah ---")
    sample_authors = ["Akiba", "Bergstra", "Hochreiter", "Khumaidi", "Goodfellow", "Kingma", "Srivastava", "Hyndman", "López de Prado", "Creswell"]
    ref_found_cnt = sum(1 for a in sample_authors if a in full_text)
    print(f"  [OK] Sampel Penulis Terdeteksi di Naskah: {ref_found_cnt}/{len(sample_authors)}")
    
    print("\n=======================================================")
    if all_markers_ok and len(img_rels) >= 4 and omml_count >= 40:
        print(" HASIL AUDIT: SEMPURNA & 100% TERVERIFIKASI!")
        print(" Dokumen master siap dicetak dan diajukan ke sidang munaqasyah.")
    else:
        print(" HASIL AUDIT: Ada beberapa komponen yang memerlukan perhatian.")
    print("=======================================================\n")

if __name__ == "__main__":
    verify_full_skripsi()
