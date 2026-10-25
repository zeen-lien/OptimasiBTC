"""
verify_bab4.py — Audit & Verification Script for BAB IV
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara
"""

import docx

doc = docx.Document("03_Naskah_Skripsi/BAB_4_HASIL_DAN_PEMBAHASAN_ZAINI_LEON.docx")

print("=" * 65)
print("AUDIT BAB 4: HASIL PENELITIAN DAN PEMBAHASAN — FULL VERIFICATION")
print("=" * 65)

# 1. Total Elements
tags = [c.tag.split('}')[-1] for c in doc._body._body]
tbl_indices = [i for i, t in enumerate(tags) if t == 'tbl']
print(f"\n1. Total elemen body: {len(tags)}")
print(f"   Total tabel tersemat: {len(tbl_indices)} tabel (Tabel 4.1 s.d. 4.5)")

# 2. Check Images (drawing elements)
drawings = doc._body._body.xpath(".//*[local-name()='drawing']")
print(f"\n2. Total gambar grafik akademik tersemat: {len(drawings)} gambar (Gambar 4.1 s.d. 4.3)")

# 3. Check Raw LaTeX dollar signs
dollar_paras = []
for i, p in enumerate(doc.paragraphs):
    if '$' in p.text:
        dollar_paras.append((i, p.text[:80]))

print(f"\n3. Paragraf dengan raw '$' LaTeX (harus 0): {len(dollar_paras)}")
if len(dollar_paras) == 0:
    print("   [OK] LULUS: Tidak ada simbol dollar mentah ($), seluruh math menggunakan OMML!")
else:
    print(f"   [BUG] Ditemukan raw $ pada: {dollar_paras}")

# 4. Check Inline OMML Elements
omath_count = len(doc._body._body.xpath(".//*[local-name()='oMath']"))
print(f"\n4. Total elemen notasi matematika OMML native: {omath_count}")

# 5. Check Paragraph Word Counts (Range 100 - 140 kata)
print(f"\n5. Analisis Panjang Kata per Paragraf (Syarat: 100 - 140 kata):")
body_paras = []
out_of_bounds = []

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    # Saring hanya paragraf narasi body (bukan judul, sub-heading, caption tabel, atau caption gambar)
    if (len(t) > 60 and not t.startswith("Tabel ") and not t.startswith("Gambar ") 
        and not t.startswith("BAB ") and not t.startswith("HASIL ") and not t.startswith("A. ") and not t.startswith("B. ")
        and not any(t.startswith(f"{d}. ") for d in range(1, 10))):
        words = len(t.split())
        body_paras.append((i, words, t))
        if words < 100 or words > 140:
            out_of_bounds.append((len(body_paras), words, t[:60]))
        status = "OK" if 100 <= words <= 140 else "OUT_OF_BOUNDS"
        print(f"   P{len(body_paras):02d} (p_idx {i:02d}): {words:3d} kata -> [{status}] | {t[:65]}...")

print(f"\n   Total Paragraf Narasi Body : {len(body_paras)} paragraf")
avg_words = sum(w[1] for w in body_paras) / len(body_paras) if body_paras else 0
print(f"   Rata-rata Panjang Paragraf : {avg_words:.1f} kata/paragraf")
print(f"   Paragraf di luar 100-140   : {len(out_of_bounds)}")

print("\n" + "=" * 65)
if len(dollar_paras) == 0 and len(out_of_bounds) == 0 and len(drawings) >= 3 and len(tbl_indices) >= 5:
    print("[SUCCESS] STATUS: VERIFIKASI BAB 4 SUKSES 100% SESUAI SEMUA STANDAR!")
else:
    print("[WARNING] STATUS: Masih ada aspek yang perlu disesuaikan.")
print("=" * 65)
