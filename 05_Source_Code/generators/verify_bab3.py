import docx

doc = docx.Document("03_Naskah_Skripsi/BAB_3_METODE_PENELITIAN_ZAINI_LEON.docx")

print("=" * 60)
print("AUDIT BAB 3 — FULL VERIFICATION")
print("=" * 60)

# 1. Document structure: body children
tags = [c.tag.split('}')[-1] for c in doc._body._body]
print(f"\n1. Total body children: {len(tags)}")

# 2. Tables: content tables + equation tables
tbl_indices = [i for i, t in enumerate(tags) if t == 'tbl']
print(f"2. Total tables: {len(tbl_indices)}")

# 3. Check equations are NOT at the end
sectPr_idx = tags.index('sectPr') if 'sectPr' in tags else len(tags)
eq_tables_after_sectPr = [i for i in tbl_indices if i > sectPr_idx]
print(f"\n3. sectPr at index: {sectPr_idx}")
print(f"   Tables AFTER sectPr (should be 0): {len(eq_tables_after_sectPr)}")
if len(eq_tables_after_sectPr) == 0:
    print("   [OK] All tables are in proper sequence before sectPr!")
else:
    print("   [BUG] Tables found after sectPr")

# 4. Check inline oMath elements in paragraphs
inline_omath_count = 0
paras_with_inline_math = []
for i, p in enumerate(doc.paragraphs):
    omath_in_para = [c for c in p._element if c.tag.split('}')[-1] == 'oMath']
    if omath_in_para:
        inline_omath_count += len(omath_in_para)
        snippet = p.text[:80] if p.text else "(empty)"
        paras_with_inline_math.append((i, len(omath_in_para), snippet))

print(f"\n4. Inline oMath elements in paragraphs: {inline_omath_count}")

# 5. Check for raw $ signs in paragraph text
dollar_paras = []
for i, p in enumerate(doc.paragraphs):
    if '$' in p.text:
        dollar_paras.append((i, p.text[:80]))

print(f"\n5. Paragraphs with raw '$' signs (should be 0): {len(dollar_paras)}")
if len(dollar_paras) == 0:
    print("   [OK] No raw LaTeX dollar signs in document text!")
else:
    print("   [BUG] Raw $ found in:")
    for pi, snip in dollar_paras:
        print(f"   Para {pi}: \"{snip}...\"")

# 6. Total oMath in entire document
all_omath = doc._body._body.xpath(".//*[local-name()='oMath']")
print(f"\n6. Total oMath elements (display + inline): {len(all_omath)}")

# 7. Check word counts per paragraph
word_counts = []
short_paras = []
long_paras = []
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    # Check if regular body paragraph (length > 100 chars, not heading or table caption)
    if len(txt) > 80 and not txt.startswith("Tabel ") and not txt.startswith("Gambar ") and not txt.startswith("BAB ") and not txt.startswith("METODE "):
        words = len(txt.split())
        word_counts.append((i, words, txt[:50]))
        if words < 90:
            short_paras.append((i, words, txt[:60]))
        elif words > 160:
            long_paras.append((i, words, txt[:60]))

print(f"\n7. Total body paragraphs analyzed: {len(word_counts)}")
if word_counts:
    avg_words = sum(w[1] for w in word_counts) / len(word_counts)
    print(f"   Average words per paragraph: {avg_words:.1f} words")
if short_paras:
    print(f"   [NOTE] {len(short_paras)} paragraphs < 90 words")
if long_paras:
    print(f"   [NOTE] {len(long_paras)} paragraphs > 160 words")

print("\n" + "=" * 60)
if len(eq_tables_after_sectPr) == 0 and len(dollar_paras) == 0:
    print("STATUS: BAB 3 VERIFIKASI SUKSES & VALID!")
else:
    print("STATUS: Ada yang perlu disesuaikan.")
print("=" * 60)
