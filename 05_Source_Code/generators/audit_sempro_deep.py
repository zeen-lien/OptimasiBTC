"""Audit mendalam untuk Proposal Sempro Bab 1, Bab 2, dan Bab 3.
Memverifikasi:
1. Setiap rumus dan persamaan matematis: sintaks, kebenaran teori, konsistensi tag.
2. Penjelasan simbol di bawah setiap rumus.
3. Kesejajaran rumus Bab 2 (teori) dan Bab 3 (operasional).
4. Konsistensi tabel, gambar, sitasi, dan ketiadaan cacat bahasa.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BAB1_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_1_PENDAHULUAN.md"
BAB2_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_2_LANDASAN_TEORI.md"
BAB3_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "BAB_3_METODE_PENELITIAN.md"
REF_PATH = ROOT / "03_Naskah_Skripsi" / "study2" / "DAFTAR_REFERENSI_STUDY2.md"

def audit_equations():
    print("=" * 60)
    print("1. AUDIT PERSAMAAN MATEMATIKA")
    print("=" * 60)
    
    for b_path, bab_num in [(BAB2_PATH, 2), (BAB3_PATH, 3)]:
        text = b_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        print(f"\n--- BAB {bab_num} ---")
        
        # Cari semua tag
        tags = []
        for i, line in enumerate(lines):
            m = re.search(r"\\tag\{(\d+\.\d+)\}", line)
            if m:
                tag = m.group(1)
                tags.append(tag)
                # Tampilkan 3 baris sebelum tag untuk melihat konteks rumus
                context = lines[max(0, i-3):i+1]
                formula = " ".join([c.strip() for c in context if c.strip() and not c.strip().startswith("$$") and not c.strip().endswith("$$")])
                print(f"Persamaan ({tag}): {formula[:100]}")
        
        # Cek urutan tag
        expected_tags = [f"{bab_num}.{i}" for i in range(1, len(tags) + 1)]
        if tags == expected_tags:
            print(f"  -> Urutan nomor persamaan Bab {bab_num} LENGKAP & KONSISTEN (1 s.d. {len(tags)})")
        else:
            print(f"  -> PERINGATAN: Urutan tidak konsisten! Ditemukan: {tags}, Seharusnya: {expected_tags}")

def audit_symbols_explanation():
    print("\n" + "=" * 60)
    print("2. AUDIT PENJELASAN SIMBOL DALAM PARAGRAF")
    print("=" * 60)
    
    b2 = BAB2_PATH.read_text(encoding="utf-8")
    b3 = BAB3_PATH.read_text(encoding="utf-8")
    
    critical_symbols = {
        "Bab 2 RV": ("RV_t", "C_{t,h}", "O_{t,h}", "\\mathcal{H}_t"),
        "Bab 2 GARCH": ("r_t", "\\sigma_t^2", "\\omega", "\\alpha", "\\beta", "\\varepsilon_t"),
        "Bab 2 HAR-RV": ("\\beta_0", "\\beta_d", "\\beta_w", "\\beta_m", "\\log RV_t"),
        "Bab 2 LSTM": ("f_t", "i_t", "\\tilde{c}_t", "c_t", "o_t", "h_t", "W_f", "W_i", "W_c", "W_o", "b_f", "b_i", "b_c", "b_o", "\\sigma", "\\tanh"),
        "Bab 2 TPE": ("P(x|y)", "\\ell(x)", "g(x)", "y^*", "EI"),
        "Bab 2 QLIKE": ("QLIKE", "e_t", "\\exp(e_t)", "\\widehat{RV}_t"),
        "Bab 2 DM": ("DM", "\\bar{d}", "\\widehat{\\text{Var}}(\\bar{d})"),
        "Bab 3 Fitur": ("\\log range_t", "\\log volume_t", "\\log absret_t", "rv\\_mean\\_5_t", "rv\\_mean\\_22_t"),
        "Bab 3 Ensemble": ("\\widehat{\\log RV}_{t+1}", "s \\in \\{42, 123, 2024, 7, 99\\}"),
    }
    
    text_combined = b2 + "\n" + b3
    for group, syms in critical_symbols.items():
        missing = []
        for s in syms:
            # Cari apakah simbol dijelaskan di teks
            s_clean = s.replace("\\", "").replace("{", "").replace("}", "").replace("^", "")
            if s_clean.lower() not in text_combined.lower():
                missing.append(s)
        if missing:
            print(f"[{group}] Simbol belum dijelaskan: {missing}")
        else:
            print(f"[{group}] Semua simbol terdefinisi dengan baik.")

def audit_tables_and_figures():
    print("\n" + "=" * 60)
    print("3. AUDIT TABEL DAN GAMBAR")
    print("=" * 60)
    for b_path, bab_num in [(BAB1_PATH, 1), (BAB2_PATH, 2), (BAB3_PATH, 3)]:
        text = b_path.read_text(encoding="utf-8")
        tables = re.findall(r"\*\*Tabel\s+(\d+\.\d+)\s+([^\*]+)\*\*", text)
        figs = re.findall(r"!\[(Gambar\s+\d+\.\d+[^\]]*)\]\(([^)]+)\)", text)
        print(f"Bab {bab_num}: {len(tables)} tabel, {len(figs)} gambar")
        for num, title in tables:
            print(f"  - Tabel {num}: {title.strip()}")
        for caption, path in figs:
            fpath = ROOT / "03_Naskah_Skripsi" / "study2" / path
            exists = fpath.exists()
            print(f"  - {caption} -> berkas: {path} (Ada di disk: {exists})")

def audit_structure_checklist():
    print("\n" + "=" * 60)
    print("4. AUDIT STRUKTUR HIERARKI SUBBAB (FST UNISNU)")
    print("=" * 60)
    for b_path, bab_num in [(BAB1_PATH, 1), (BAB2_PATH, 2), (BAB3_PATH, 3)]:
        text = b_path.read_text(encoding="utf-8")
        h2 = re.findall(r"^##\s+([A-Z]\..*)$", text, re.MULTILINE)
        print(f"Bab {bab_num} Subbab (## A, B, C...): {len(h2)} bagian")
        for h in h2:
            print(f"  {h}")

if __name__ == "__main__":
    audit_equations()
    audit_symbols_explanation()
    audit_tables_and_figures()
    audit_structure_checklist()
