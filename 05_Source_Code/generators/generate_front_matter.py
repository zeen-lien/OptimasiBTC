"""
generate_front_matter.py
Membuat seluruh bagian awal (Front Matter) Skripsi UNISNU Jepara:
- Sampul Luar & Sampul Dalam
- Pernyataan Keaslian (Bebas Plagiasi)
- Persetujuan Pembimbing
- Pengesahan Tim Penguji
- Halaman Persembahan
- Halaman Motto
- Kata Pengantar
- Abstrak (Bahasa Indonesia) & Abstract (Bahasa Inggris)
- Daftar Isi
- Daftar Tabel
- Daftar Gambar
- Daftar Lampiran
"""

import os
import docx
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from doc_paths import SOURCE_ROOT
from results_context import (
    FinalResults,
    format_number,
    format_pct,
    format_usd,
)

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic

def generate_front_matter(output_path=None):
    if output_path is None:
        output_path = str(SOURCE_ROOT / "front_matter.docx")
    results = FinalResults.load()
    doc = docx.Document()
    
    # Page Setup UNISNU: Top 4cm, Left 4cm, Bottom 3cm, Right 3cm
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(4.0)
    sec.left_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # Footer Roman Numeral
    sectPr = sec._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
    sectPr.append(pgNumType)

    footer = sec.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = f_p.add_run()
    set_font(f_run, "Times New Roman", 10)
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    f_p._p.append(fld)

    logo_path = os.path.abspath("05_Source_Code/extracted_logo/img_3.png")

    # =========================================================================
    # 1. SAMPUL LUAR (HARD COVER)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run("OPTIMASI HYPERPARAMETER LONG SHORT-TERM MEMORY MENGGUNAKAN ALGORITMA OPTUNA PADA PREDIKSI HARGA BITCOIN")
    set_font(r, "Times New Roman", 14, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(18)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("SKRIPSI")
    set_font(r_sub, "Times New Roman", 14, bold=True)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(6)
    p_req.paragraph_format.space_after = Pt(24)
    p_req.paragraph_format.line_spacing = 1.15
    r_req = p_req.add_run("Diajukan sebagai salah satu syarat untuk memperoleh gelar Sarjana Komputer (S.Kom.) pada Program Studi Teknik Informatika")
    set_font(r_req, "Times New Roman", 11, italic=False)

    # Logo
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(24)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Cm(5.0))

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(12)
    p_auth.paragraph_format.space_after = Pt(4)
    p_auth.paragraph_format.line_spacing = 1.15
    r_auth = p_auth.add_run("Disusun Oleh:\nZAINI LEON MUSTHOFA KAMAL\nNIM: 231240001455")
    set_font(r_auth, "Times New Roman", 12, bold=True)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS ISLAM NAHDLATUL ULAMA JEPARA\n2026")
    set_font(r_inst, "Times New Roman", 13, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 2. SAMPUL DALAM
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run("OPTIMASI HYPERPARAMETER LONG SHORT-TERM MEMORY MENGGUNAKAN ALGORITMA OPTUNA PADA PREDIKSI HARGA BITCOIN")
    set_font(r, "Times New Roman", 14, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(18)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("SKRIPSI")
    set_font(r_sub, "Times New Roman", 14, bold=True)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(6)
    p_req.paragraph_format.space_after = Pt(24)
    p_req.paragraph_format.line_spacing = 1.15
    r_req = p_req.add_run("Diajukan sebagai salah satu syarat untuk memperoleh gelar Sarjana Komputer (S.Kom.) pada Program Studi Teknik Informatika")
    set_font(r_req, "Times New Roman", 11, italic=False)

    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(24)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Cm(5.0))

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(12)
    p_auth.paragraph_format.space_after = Pt(4)
    p_auth.paragraph_format.line_spacing = 1.15
    r_auth = p_auth.add_run("Disusun Oleh:\nZAINI LEON MUSTHOFA KAMAL\nNIM: 231240001455")
    set_font(r_auth, "Times New Roman", 12, bold=True)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS ISLAM NAHDLATUL ULAMA JEPARA\n2026")
    set_font(r_inst, "Times New Roman", 13, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 3. SURAT PERNYATAAN KEASLIAN
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("SURAT PERNYATAAN KEASLIAN KARYA TULIS SKRIPSI")
    set_font(r, "Times New Roman", 12, bold=True)

    p_stmt_intro = doc.add_paragraph()
    p_stmt_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_stmt_intro.paragraph_format.line_spacing = 1.5
    p_stmt_intro.paragraph_format.space_after = Pt(8)
    r = p_stmt_intro.add_run("Yang bertanda tangan di bawah ini:")
    set_font(r, "Times New Roman", 12)

    bio_tbl = doc.add_table(rows=4, cols=3)
    bio_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    bio_data = [
        ("Nama", ":", "Zaini Leon Musthofa Kamal"),
        ("NIM", ":", "231240001455"),
        ("Program Studi", ":", "Teknik Informatika"),
        ("Fakultas", ":", "Sains dan Teknologi, UNISNU Jepara")
    ]
    for idx, (lbl, col, val) in enumerate(bio_data):
        row = bio_tbl.rows[idx]
        cell_lbl, cell_col, cell_val = row.cells[0], row.cells[1], row.cells[2]
        cell_lbl.width = Cm(4.0)
        cell_col.width = Cm(0.5)
        cell_val.width = Cm(10.5)
        set_font(cell_lbl.paragraphs[0].add_run(lbl), "Times New Roman", 12)
        set_font(cell_col.paragraphs[0].add_run(col), "Times New Roman", 12)
        set_font(cell_val.paragraphs[0].add_run(val), "Times New Roman", 12, bold=(idx < 2))
        for c in (cell_lbl, cell_col, cell_val):
            c.paragraphs[0].paragraph_format.space_after = Pt(4)
            c.paragraphs[0].paragraph_format.line_spacing = 1.15

    p_stmt_body1 = doc.add_paragraph()
    p_stmt_body1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_stmt_body1.paragraph_format.line_spacing = 1.5
    p_stmt_body1.paragraph_format.first_line_indent = Cm(1.0)
    p_stmt_body1.paragraph_format.space_before = Pt(12)
    p_stmt_body1.paragraph_format.space_after = Pt(6)
    r = p_stmt_body1.add_run(
        "Menyatakan dengan sesungguhnya bahwa naskah Skripsi yang berjudul: \"Optimasi Hyperparameter Long Short-Term "
        "Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin\" adalah benar-benar hasil karya ilmiah mandiri "
        "saya sendiri, bukan merupakan karya tiruan, saduran, atau plagiasi dari karya orang lain, baik sebagian maupun seluruhnya. "
        "Sepanjang pengetahuan saya, tidak terdapat karya atau pendapat yang pernah ditulis atau diterbitkan oleh orang lain, "
        "kecuali yang secara tertulis dan formal disitasi dalam naskah ini serta dicantumkan dalam daftar pustaka sesuai dengan kaidah ilmiah."
    )
    set_font(r, "Times New Roman", 12)

    p_stmt_body2 = doc.add_paragraph()
    p_stmt_body2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_stmt_body2.paragraph_format.line_spacing = 1.5
    p_stmt_body2.paragraph_format.first_line_indent = Cm(1.0)
    p_stmt_body2.paragraph_format.space_after = Pt(18)
    r = p_stmt_body2.add_run(
        "Apabila di kemudian hari terbukti atau dapat dibuktikan bahwa skripsi ini merupakan hasil plagiasi, penjiplakan, atau rekayasa data "
        "yang melanggar kode etik akademik, maka saya bersedia menerima sanksi akademik yang seberat-beratnya sesuai dengan peraturan "
        "perundang-undangan yang berlaku dan Peraturan Rektor UNISNU Jepara, termasuk pencabutan gelar kesarjanaan yang telah saya peroleh."
    )
    set_font(r, "Times New Roman", 12)

    p_ttd = doc.add_paragraph()
    p_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ttd.paragraph_format.line_spacing = 1.15
    p_ttd.paragraph_format.space_before = Pt(18)
    r = p_ttd.add_run("Jepara, 20 Oktober 2026\nYang membuat pernyataan,\n\n\n\nMeterai Rp10.000\n\n\n")
    set_font(r, "Times New Roman", 12)
    r_nm = p_ttd.add_run("Zaini Leon Musthofa Kamal\nNIM: 231240001455")
    set_font(r_nm, "Times New Roman", 12, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 4. LEMBAR PERSETUJUAN PEMBIMBING
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("LEMBAR PERSETUJUAN PEMBIMBING")
    set_font(r, "Times New Roman", 12, bold=True)

    p_app_intro = doc.add_paragraph()
    p_app_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_app_intro.paragraph_format.line_spacing = 1.5
    p_app_intro.paragraph_format.space_after = Pt(8)
    r = p_app_intro.add_run("Naskah Skripsi dengan identitas sebagai berikut:")
    set_font(r, "Times New Roman", 12)

    app_tbl = doc.add_table(rows=4, cols=3)
    app_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    app_data = [
        ("Nama Mahasiswa", ":", "Zaini Leon Musthofa Kamal"),
        ("Nomor Induk Mahasiswa", ":", "231240001455"),
        ("Program Studi", ":", "Teknik Informatika"),
        ("Judul Skripsi", ":", "Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin")
    ]
    for idx, (lbl, col, val) in enumerate(app_data):
        row = app_tbl.rows[idx]
        cell_lbl, cell_col, cell_val = row.cells[0], row.cells[1], row.cells[2]
        cell_lbl.width = Cm(4.5)
        cell_col.width = Cm(0.5)
        cell_val.width = Cm(10.0)
        set_font(cell_lbl.paragraphs[0].add_run(lbl), "Times New Roman", 12)
        set_font(cell_col.paragraphs[0].add_run(col), "Times New Roman", 12)
        set_font(cell_val.paragraphs[0].add_run(val), "Times New Roman", 12, bold=(idx < 2))
        for c in (cell_lbl, cell_col, cell_val):
            c.paragraphs[0].paragraph_format.space_after = Pt(4)
            c.paragraphs[0].paragraph_format.line_spacing = 1.15

    p_app_body = doc.add_paragraph()
    p_app_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_app_body.paragraph_format.line_spacing = 1.5
    p_app_body.paragraph_format.first_line_indent = Cm(1.0)
    p_app_body.paragraph_format.space_before = Pt(14)
    p_app_body.paragraph_format.space_after = Pt(18)
    r = p_app_body.add_run(
        "Telah diperiksa dan disetujui oleh Dosen Pembimbing untuk diajukan dalam Ujian Sidang Skripsi (Munaqasyah) "
        "Program Studi Teknik Informatika Fakultas Sains dan Teknologi Universitas Islam Nahdlatul Ulama Jepara."
    )
    set_font(r, "Times New Roman", 12)

    p_app_ttd = doc.add_paragraph()
    p_app_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_app_ttd.paragraph_format.line_spacing = 1.15
    p_app_ttd.paragraph_format.space_before = Pt(24)
    r = p_app_ttd.add_run("Jepara, 20 Oktober 2026\nMenyetujui,\nDosen Pembimbing,\n\n\n\n\n\n")
    set_font(r, "Times New Roman", 12)
    r_dos = p_app_ttd.add_run("Teguh Tamrin, S.Kom., M.Kom.\nNIDN. 0620127603 / NIY. 4 761220 17 235")
    set_font(r_dos, "Times New Roman", 12, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 5. LEMBAR PENGESAHAN TIM PENGUJI
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("LEMBAR PENGESAHAN SKRIPSI")
    set_font(r, "Times New Roman", 12, bold=True)

    p_peng = doc.add_paragraph()
    p_peng.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_peng.paragraph_format.line_spacing = 1.5
    p_peng.paragraph_format.space_after = Pt(10)
    r = p_peng.add_run(
        "Skripsi dengan judul \"Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin\" "
        "yang disusun oleh Zaini Leon Musthofa Kamal (NIM: 231240001455) telah dipertahankan di hadapan Dewan Penguji Ujian Sidang Skripsi "
        "Program Studi Teknik Informatika Fakultas Sains dan Teknologi Universitas Islam Nahdlatul Ulama Jepara pada tanggal 20 Oktober 2026 "
        "dan dinyatakan LULUS serta diterima sebagai salah satu syarat untuk memperoleh gelar Sarjana Komputer (S.Kom.)."
    )
    set_font(r, "Times New Roman", 12)

    p_dewan = doc.add_paragraph()
    p_dewan.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dewan.paragraph_format.space_before = Pt(10)
    p_dewan.paragraph_format.space_after = Pt(8)
    r = p_dewan.add_run("DEWAN PENGUJI:")
    set_font(r, "Times New Roman", 12, bold=True)

    t_peng = doc.add_table(rows=3, cols=3)
    t_peng.alignment = WD_TABLE_ALIGNMENT.CENTER
    peng_data = [
        ("Ketua Penguji", ":", "Teguh Tamrin, S.Kom., M.Kom."),
        ("Sekretaris Penguji", ":", "Gentur Wahyu Nyipto Wibowo, S.Kom., M.Kom."),
        ("Anggota Penguji", ":", "Danang Mahendra, S.Kom., M.Kom.")
    ]
    for idx, (lbl, col, val) in enumerate(peng_data):
        row = t_peng.rows[idx]
        row.cells[0].width = Cm(4.5)
        row.cells[1].width = Cm(0.5)
        row.cells[2].width = Cm(10.0)
        set_font(row.cells[0].paragraphs[0].add_run(lbl), "Times New Roman", 12)
        set_font(row.cells[1].paragraphs[0].add_run(col), "Times New Roman", 12)
        set_font(row.cells[2].paragraphs[0].add_run(val + "  ( ..................................... )"), "Times New Roman", 12)
        for c in row.cells:
            c.paragraphs[0].paragraph_format.space_after = Pt(8)
            c.paragraphs[0].paragraph_format.line_spacing = 1.15

    p_mengk = doc.add_paragraph()
    p_mengk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mengk.paragraph_format.line_spacing = 1.15
    p_mengk.paragraph_format.space_before = Pt(20)
    r = p_mengk.add_run("Mengesahkan,\nDekan Fakultas Sains dan Teknologi\nUniversitas Islam Nahdlatul Ulama Jepara\n\n\n\n\n")
    set_font(r, "Times New Roman", 12)
    r_dek = p_mengk.add_run("Dr. Arif Mustofa, S.T., M.Si.\nNIY. 3 730617 13 124 / NIDN. 0617067302")
    set_font(r_dek, "Times New Roman", 12, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 6. HALAMAN PERSEMBAHAN
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("HALAMAN PERSEMBAHAN")
    set_font(r, "Times New Roman", 12, bold=True)

    p_persembahan = doc.add_paragraph()
    p_persembahan.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_persembahan.paragraph_format.line_spacing = 1.5
    p_persembahan.paragraph_format.space_after = Pt(12)
    r = p_persembahan.add_run(
        "Alhamdulillahirabbil'alamin, dengan penuh rasa syukur ke hadirat Allah SWT atas segala limpahan rahmat, hidayah, "
        "dan kemudahan yang dianugerahkan-Nya, karya tulis skripsi yang sederhana ini saya persembahkan dengan segenap cinta, "
        "penghargaan, dan rasa hormat yang mendalam kepada:"
    )
    set_font(r, "Times New Roman", 12)

    persembahan_items = [
        "Kedua orang tua tercinta yang tiada henti memanjatkan doa tulus di setiap sujudnya, memberikan dukungan moril dan materil tanpa pamrih, serta menanamkan nilai-nilai kegigihan dan ketulusan dalam menuntut ilmu.",
        "Keluarga besar yang senantiasa menjadi sumber inspirasi, motivasi, dan kehangatan dalam setiap langkah perjuangan menempuh studi pendidikan sarjana.",
        "Dosen Pembimbing dan seluruh Bapak/Ibu Dosen Program Studi Teknik Informatika FST UNISNU Jepara yang telah ikhlas mentransfer ilmu pengetahuan, bimbingan, arahan metodologis, dan teladan integritas akademik yang tak ternilai.",
        "Rekan-rekan seperjuangan mahasiswa Program Studi Teknik Informatika FST UNISNU Jepara Angkatan 2023 atas kebersamaan, sinergi, diskusi intelektual, dan persahabatan yang senantiasa saling menguatkan.",
        "Almamater tercinta, Universitas Islam Nahdlatul Ulama (UNISNU) Jepara, sebagai kawah candradimuka yang menempa keilmuan teknologi informasi berlandaskan nilai-nilai Ahlussunnah wal Jama'ah."
    ]
    for item in persembahan_items:
        p_item = doc.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_item.paragraph_format.line_spacing = 1.5
        p_item.paragraph_format.first_line_indent = Cm(1.0)
        p_item.paragraph_format.space_after = Pt(6)
        r = p_item.add_run("•  " + item)
        set_font(r, "Times New Roman", 12)

    doc.add_page_break()

    # =========================================================================
    # 7. HALAMAN MOTTO
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("HALAMAN MOTTO")
    set_font(r, "Times New Roman", 12, bold=True)

    mottos = [
        ("“Barangsiapa bertakwa kepada Allah niscaya Dia akan mengadakan baginya jalan keluar, dan memberinya rezeki dari arah yang tiada disangka-sangkanya. Dan barangsiapa yang bertawakkal kepada Allah niscaya Allah akan mencukupkan (keperluan)nya.”", "(QS. At-Talaq: 2-3)"),
        ("“Sesungguhnya Allah mencintai seorang hamba yang apabila mengerjakan suatu pekerjaan, ia melakukannya dengan itqan (profesional, tekun, dan tuntas).”", "(HR. At-Thabrani dan Al-Baihaqi)"),
        ("“Bukan kecerdasan semata yang menentukan keberhasilan penyelesaian suatu riset, melainkan ketekunan dalam menghadapi anomali data, kedisiplinan metode ilmiah, dan kerendahan hati untuk terus belajar memperbarui pemahaman.”", "(Zaini Leon Musthofa Kamal)")
    ]

    for quote, src in mottos:
        p_q = doc.add_paragraph()
        p_q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_q.paragraph_format.line_spacing = 1.5
        p_q.paragraph_format.space_before = Pt(18)
        p_q.paragraph_format.space_after = Pt(4)
        r_q = p_q.add_run(quote)
        set_font(r_q, "Times New Roman", 12, italic=True)

        p_s = doc.add_paragraph()
        p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_s.paragraph_format.space_after = Pt(24)
        r_s = p_s.add_run(src)
        set_font(r_s, "Times New Roman", 11, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 8. KATA PENGANTAR
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("KATA PENGANTAR")
    set_font(r, "Times New Roman", 12, bold=True)

    kata_pengantar_paras = [
        "Puji dan syukur senantiasa penulis panjatkan ke hadirat Allah SWT atas limpahan rahmat, taufiq, karunia, dan inayah-Nya, sehingga penulis dapat menyelesaikan penyusunan skripsi yang berjudul \"Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin\" dengan baik dan lancar. Shalawat serta salam semoga senantiasa tercurahkan kepada junjungan kita Nabi Agung Muhammad SAW, keluarga, para sahabat, dan pengikutnya hingga akhir zaman.",
        "Skripsi ini disusun sebagai salah satu syarat akademik guna menyelesaikan studi jenjang Strata 1 (S1) dan memperoleh gelar Sarjana Komputer (S.Kom.) pada Program Studi Teknik Informatika, Fakultas Sains dan Teknologi, Universitas Islam Nahdlatul Ulama (UNISNU) Jepara. Penulis menyadari sepenuhnya bahwa selesainya penulisan skripsi ini tidak terlepas dari bantuan, bimbingan, doa, dan motivasi dari berbagai pihak.",
        "Oleh karena itu, dengan penuh kerendahan hati dan rasa hormat yang mendalam, penulis ingin menyampaikan ucapan terima kasih yang sebesar-besarnya kepada:",
        "1. Prof. Dr. H. Abdul Djamil, M.A., selaku Rektor Universitas Islam Nahdlatul Ulama (UNISNU) Jepara, atas segala fasilitas dan kebijakan akademik yang mendukung kelancaran studi mahasiswa.\n"
        "2. Dr. Arif Mustofa, S.T., M.Si., selaku Dekan Fakultas Sains dan Teknologi UNISNU Jepara, atas kepemimpinan, dedikasi, dan sarana prasarana yang disediakan selama masa perkuliahan.\n"
        "3. Gentur Wahyu Nyipto Wibowo, S.Kom., M.Kom., selaku Ketua Program Studi Teknik Informatika FST UNISNU Jepara, atas pengarahan kurikulum, dorongan akademis, dan kemudahan proses administrasi tugas akhir.\n"
        "4. Teguh Tamrin, S.Kom., M.Kom., selaku Dosen Pembimbing Skripsi, yang telah dengan penuh kesabaran, ketelitian, dan keikhlasan meluangkan waktu serta mencurahkan pemikiran dalam membimbing, mengarahkan, dan memberikan telaah kritis sejak awal pengajuan proposal hingga naskah skripsi ini terselesaikan secara utuh dan teruji.\n"
        "5. Seluruh Dewan Penguji Ujian Sidang Skripsi yang telah memberikan koreksi, evaluasi metodologis, dan masukan berharga demi penyempurnaan kualitas ilmiah naskah ini.\n"
        "6. Seluruh Bapak dan Ibu Dosen serta staf akademik di lingkungan Program Studi Teknik Informatika dan Fakultas Sains dan Teknologi UNISNU Jepara yang telah membekali penulis dengan berbagai khazanah ilmu pengetahuan dan keteladanan budi pekerti luhur.\n"
        "7. Kedua orang tua tercinta dan segenap keluarga besar yang senantiasa mengiringi setiap perjuangan penulis dengan doa yang tulus, limpahan kasih sayang yang tak bertepi, serta pengorbanan moril dan materiil yang tak terhingga nilainya.\n"
        "8. Sahabat-sahabat dan rekan mahasiswa Program Studi Teknik Informatika UNISNU Jepara Angkatan 2023 atas kebersamaan, kekompakan, serta diskusi saintifik yang selalu membangun.",
        "Penulis menyadari bahwa skripsi ini masih jauh dari kesempurnaan akibat keterbatasan pengalaman dan wawasan penulis. Meskipun demikian, penulis telah berusaha semaksimal mungkin mencurahkan kemampuan terbaik dalam menyelesaikan karya ini. Akhir kata, penulis berharap semoga skripsi ini dapat memberikan kontribusi nyata serta kemaslahatan bagi pengembangan ilmu pengetahuan dan teknologi, khususnya di bidang Artificial Intelligence, Deep Learning, dan rekayasa optimasi peramalan finansial."
    ]

    for idx, text in enumerate(kata_pengantar_paras):
        p_kp = doc.add_paragraph()
        p_kp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_kp.paragraph_format.line_spacing = 1.5
        p_kp.paragraph_format.space_after = Pt(6)
        if idx not in [0, 2]:
            p_kp.paragraph_format.first_line_indent = Cm(1.0)
        r = p_kp.add_run(text)
        set_font(r, "Times New Roman", 12)

    p_kp_ttd = doc.add_paragraph()
    p_kp_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_kp_ttd.paragraph_format.line_spacing = 1.15
    p_kp_ttd.paragraph_format.space_before = Pt(16)
    r = p_kp_ttd.add_run("Jepara, 20 Oktober 2026\nPenulis,\n\n\n\n")
    set_font(r, "Times New Roman", 12)
    r_nm = p_kp_ttd.add_run("Zaini Leon Musthofa Kamal\nNIM: 231240001455")
    set_font(r_nm, "Times New Roman", 12, bold=True)

    doc.add_page_break()

    # =========================================================================
    # 9. ABSTRAK (BAHASA INDONESIA)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("ABSTRAK")
    set_font(r, "Times New Roman", 12, bold=True)

    p_id = doc.add_paragraph()
    p_id.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_id.paragraph_format.space_after = Pt(10)
    p_id.paragraph_format.line_spacing = 1.0
    r_id = p_id.add_run("Zaini Leon Musthofa Kamal, 231240001455, Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin, 2026.")
    set_font(r_id, "Times New Roman", 11, bold=True)

    # Abstract numbers follow the same published summary as the thesis tables.
    e0 = results.metrics("E0")
    e7 = results.metrics("E7")
    best_lstm = results.best_lstm
    status = results.verdict.get("status")
    config = results.final_configuration()
    hyper = config.get("hyperparameters") or {}
    if status == "proposed_lower_mae_ci_excludes_zero":
        result_id = (
            f"E7 mencatat MAE {format_usd(e7['MAE'])}, lebih rendah daripada "
            f"persistence ({format_usd(e0['MAE'])}), dan CI selisih berpasangan "
            "tidak melewati nol. Klaim keunggulan tetap dibatasi pada satu aset, "
            "satu horizon, dan satu periode uji."
        )
        result_en = (
            f"E7 achieved an MAE of {format_usd(e7['MAE'])}, lower than persistence "
            f"({format_usd(e0['MAE'])}), with a paired confidence interval that "
            "excluded zero. The claim remains limited to one asset, one horizon, "
            "and one test period."
        )
    elif status == "proposed_lower_mae_ci_includes_zero":
        result_id = (
            f"E7 mencatat MAE {format_usd(e7['MAE'])}, lebih rendah daripada "
            f"persistence ({format_usd(e0['MAE'])}), tetapi CI selisih "
            "berpasangan masih melewati nol sehingga perbedaan tersebut belum "
            "dapat disebut signifikan."
        )
        result_en = (
            f"E7 achieved an MAE of {format_usd(e7['MAE'])}, lower than persistence "
            f"({format_usd(e0['MAE'])}), but the paired confidence interval still "
            "included zero, so the difference cannot be called significant."
        )
    else:
        if results.verdict.get("ci_direction") == "persistence_better":
            result_id = (
                f"E7 mencatat MAE {format_usd(e7['MAE'])}, lebih tinggi daripada "
                f"persistence ({format_usd(e0['MAE'])}), dengan CI selisih "
                "berpasangan yang seluruhnya di atas nol. Hasil ini secara "
                "statistik lebih buruk dan dilaporkan apa adanya; kontribusi "
                "penelitian diarahkan pada pipeline evaluasi serta bukti "
                "terkontrol tentang batas kemampuan LSTM."
            )
            result_en = (
                f"E7 achieved an MAE of {format_usd(e7['MAE'])}, higher than "
                f"persistence ({format_usd(e0['MAE'])}), with a paired confidence "
                "interval entirely above zero. This result is statistically worse "
                "and is reported as such; the contribution is reframed as a "
                "controlled evaluation pipeline and evidence about the limits of "
                "LSTM."
            )
        else:
            result_id = (
                f"E7 mencatat MAE {format_usd(e7['MAE'])}, tidak lebih baik daripada "
                f"persistence ({format_usd(e0['MAE'])}). Hasil negatif ini dilaporkan "
                "secara eksplisit dan kontribusi penelitian diarahkan pada pipeline "
                "evaluasi serta bukti terkontrol tentang batas kemampuan LSTM."
            )
            result_en = (
                f"E7 achieved an MAE of {format_usd(e7['MAE'])}, which did not beat "
                f"persistence ({format_usd(e0['MAE'])}). This negative result is "
                "reported explicitly, and the contribution is reframed as a "
                "controlled evaluation pipeline and evidence about the limits of LSTM."
            )

    # 1 Single Paragraph, 250 - 500 words
    abstrak_id_text = (
        "Volatilitas ekstrem dan sifat non-stasioner pada harga penutupan Bitcoin "
        "menimbulkan tantangan dalam pemodelan deret waktu finansial. Arsitektur "
        "Long Short-Term Memory (LSTM) mampu menangkap ketergantungan temporal, "
        "tetapi kinerjanya sensitif terhadap hyperparameter dan aturan pelatihan. "
        "Penelitian ini merancang pipeline optimasi berbasis Tree-structured Parzen "
        "Estimator (TPE) melalui Optuna, lalu mengevaluasinya dengan matriks "
        "terkontrol E0 sampai E7. Data mencakup "
        f"{format_number(results.data.get('n_train', 0) + results.data.get('n_test', 0), 0)} "
        "harga penutupan harian BTC/USDT; "
        f"{format_number(results.data.get('n_train', 0), 0)} observasi in-sample "
        "dipakai untuk tuning dan "
        f"{format_number(results.data.get('n_test', 0), 0)} observasi holdout hanya "
        "untuk evaluasi akhir. Validasi memakai Time-Series Split berpurge, scaler "
        "per fold, lima seed, moving-block bootstrap, dan pembanding persistence. "
        f"E7 menjalani {config.get('total_trials', 0)} trial dan memilih lookback "
        f"{hyper.get('lookback', '-')} hari, {hyper.get('units', '-')} unit, dropout "
        f"{format_number(hyper.get('dropout', 0), 2)}, learning rate "
        f"{format_number(hyper.get('learning_rate', 0), 5)}, serta batch size "
        f"{hyper.get('batch_size', '-')}. Evaluasi holdout menghasilkan RMSE "
        f"{format_usd(e7['RMSE'])}, MAE {format_usd(e7['MAE'])}, dan MAPE "
        f"{format_pct(e7['MAPE'])}. {result_id} Model LSTM terbaik adalah "
        f"{best_lstm['run']} dengan MAE {format_usd(best_lstm['MAE'])}. Temuan ini "
        "menegaskan pentingnya baseline naif, pemisahan data tuning, dan pelaporan "
        "hasil negatif dalam riset peramalan aset kripto."
    )
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.first_line_indent = Cm(1.0)
    p_abs.paragraph_format.line_spacing = 1.0
    p_abs.paragraph_format.space_after = Pt(12)
    r = p_abs.add_run(abstrak_id_text)
    set_font(r, "Times New Roman", 11)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.line_spacing = 1.0
    p_kw.paragraph_format.space_after = Pt(12)
    r_kw_lbl = p_kw.add_run("Kata Kunci: ")
    set_font(r_kw_lbl, "Times New Roman", 11, bold=True)
    r_kw_val = p_kw.add_run("Long Short-Term Memory, Optuna-TPE, Prediksi Harga Bitcoin, Optimasi Hyperparameter, Deret Waktu Finansial.")
    set_font(r_kw_val, "Times New Roman", 11, italic=True)

    doc.add_page_break()

    # =========================================================================
    # 10. ABSTRACT (BAHASA INGGRIS)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("ABSTRACT")
    set_font(r, "Times New Roman", 12, bold=True)

    p_en_id = doc.add_paragraph()
    p_en_id.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_en_id.paragraph_format.space_after = Pt(10)
    p_en_id.paragraph_format.line_spacing = 1.0
    r_en_id = p_en_id.add_run("Zaini Leon Musthofa Kamal, 231240001455, Hyperparameter Optimization of Long Short-Term Memory Using Optuna Algorithm in Bitcoin Price Prediction, 2026.")
    set_font(r_en_id, "Times New Roman", 11, bold=True)

    abstrak_en_text = (
        "Extreme volatility and non-stationarity in Bitcoin closing prices pose "
        "substantial challenges for financial time-series modeling. Long Short-Term "
        "Memory (LSTM) networks can capture temporal dependencies, but their "
        "performance is sensitive to hyperparameters and training rules. This study "
        "builds a Tree-structured Parzen Estimator (TPE) pipeline in Optuna and "
        "evaluates it with a controlled E0-E7 matrix. The dataset contains "
        f"{format_number(results.data.get('n_train', 0) + results.data.get('n_test', 0), 0)} "
        "daily BTC/USDT closing prices; "
        f"{format_number(results.data.get('n_train', 0), 0)} in-sample observations "
        "were used for tuning and "
        f"{format_number(results.data.get('n_test', 0), 0)} holdout observations only "
        "for final evaluation. Validation used a purged Time-Series Split, per-fold "
        "scaling, five seeds, moving-block bootstrap, and a persistence benchmark. "
        f"E7 ran {config.get('total_trials', 0)} trials and selected a "
        f"{hyper.get('lookback', '-')}-day lookback, {hyper.get('units', '-')} units, "
        f"dropout {format_number(hyper.get('dropout', 0), 2)}, learning rate "
        f"{format_number(hyper.get('learning_rate', 0), 5)}, and batch size "
        f"{hyper.get('batch_size', '-')}. Holdout evaluation produced an RMSE of "
        f"{format_usd(e7['RMSE'])}, MAE of {format_usd(e7['MAE'])}, and MAPE of "
        f"{format_pct(e7['MAPE'])}. {result_en} The best LSTM was "
        f"{best_lstm['run']} with an MAE of {format_usd(best_lstm['MAE'])}. These "
        "findings underline the importance of naive baselines, tuning-holdout "
        "separation, and transparent reporting of negative results in "
        "cryptocurrency forecasting research."
    )
    p_abs_en = doc.add_paragraph()
    p_abs_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_en.paragraph_format.first_line_indent = Cm(1.0)
    p_abs_en.paragraph_format.line_spacing = 1.0
    p_abs_en.paragraph_format.space_after = Pt(12)
    r = p_abs_en.add_run(abstrak_en_text)
    set_font(r, "Times New Roman", 11, italic=True)

    p_kw_en = doc.add_paragraph()
    p_kw_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw_en.paragraph_format.line_spacing = 1.0
    p_kw_en.paragraph_format.space_after = Pt(12)
    r_kw_lbl_en = p_kw_en.add_run("Keywords: ")
    set_font(r_kw_lbl_en, "Times New Roman", 11, bold=True)
    r_kw_val_en = p_kw_en.add_run("Long Short-Term Memory, Optuna-TPE, Bitcoin Price Forecasting, Hyperparameter Optimization, Financial Time-Series.")
    set_font(r_kw_val_en, "Times New Roman", 11, italic=True)

    doc.add_page_break()

    # =========================================================================
    # 11. DAFTAR ISI
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("DAFTAR ISI")
    set_font(r, "Times New Roman", 12, bold=True)

    toc_entries = [
        ("HALAMAN SAMPUL LUAR", "i", False),
        ("HALAMAN SAMPUL DALAM", "ii", False),
        ("SURAT PERNYATAAN KEASLIAN", "iii", False),
        ("LEMBAR PERSETUJUAN PEMBIMBING", "v", False),
        ("LEMBAR PENGESAHAN SKRIPSI", "vi", False),
        ("HALAMAN PERSEMBAHAN", "vii", False),
        ("HALAMAN MOTTO", "viii", False),
        ("KATA PENGANTAR", "ix", False),
        ("ABSTRAK", "xi", False),
        ("ABSTRACT", "xii", False),
        ("DAFTAR ISI", "xiii", False),
        ("DAFTAR TABEL", "xv", False),
        ("DAFTAR GAMBAR", "xvi", False),
        ("DAFTAR LAMPIRAN", "xvii", False),
        ("BAB I   PENDAHULUAN", "1", True),
        ("   A. Latar Belakang Masalah", "1", False),
        ("   B. Rumusan Masalah", "4", False),
        ("   C. Tujuan Penelitian", "5", False),
        ("   D. Manfaat Penelitian", "5", False),
        ("   E. Batasan Masalah", "6", False),
        ("BAB II  LANDASAN TEORI", "7", True),
        ("   A. Penelitian Terdahulu yang Relevan", "7", False),
        ("   B. Landasan Teori", "14", False),
        ("      1. Karakteristik Data Deret Waktu dan Volatilitas Pasar Bitcoin", "14", False),
        ("      2. Arsitektur Jaringan Saraf Tiruan Long Short-Term Memory (LSTM)", "14", False),
        ("      3. Ruang Pencarian Hyperparameter pada Arsitektur LSTM", "15", False),
        ("      4. Kerangka Kerja Optuna dan Algoritma Tree-structured Parzen Estimator (TPE)", "16", False),
        ("      5. Skema Validasi Deret Waktu (Time-Series Split / Walk-Forward)", "17", False),
        ("      6. Metrik Evaluasi Kinerja Peramalan Komputasi", "18", False),
        ("   C. Kerangka Berpikir Penelitian", "19", False),
        ("   D. Hipotesis Penelitian", "20", False),
        ("BAB III METODE PENELITIAN", "20", True),
        ("   A. Jenis dan Pendekatan Penelitian", "21", False),
        ("   B. Waktu dan Tempat Penelitian", "22", False),
        ("   C. Populasi dan Sampel Penelitian", "23", False),
        ("   D. Instrumen Penelitian", "24", False),
        ("   E. Teknik Pengumpulan Data", "27", False),
        ("   F. Teknis Analisis Data", "29", False),
        ("BAB IV  HASIL PENELITIAN DAN PEMBAHASAN", "36", True),
        ("   A. Hasil Penelitian", "36", False),
        ("      1. Karakteristik Data dan Protokol Evaluasi", "36", False),
        ("      2. Baseline Persistence dan Baseline Naif", "37", False),
        ("      3. Model Kontrol Tier 1 dan Tier 2", "37", False),
        ("      4. Ablasi Loss dan Scheduler pada Parameter Tier 3", "38", False),
        ("      5. Hasil HPO Bersih Tier 3 (E7)", "38", False),
        ("      6. Perbandingan Statistik dan Verdict Ilmiah", "39", False),
        ("      7. Analisis Residual, Rezim, dan Arah", "40", False),
        ("   B. Pembahasan Hasil Penelitian", "43", False),
        ("      1. Mengapa Baseline Persistence Sulit Dikalahkan", "43", False),
        ("      2. Efek Hyperparameter Optuna: E1 versus E3", "44", False),
        ("      3. Efek Loss MAE dan Scheduler", "44", False),
        ("      4. Nilai Tambah HPO Penuh: E7 versus E6", "45", False),
        ("      5. Implikasi Teoritis dan Praktis", "46", False),
        ("      6. Keterbatasan Penelitian", "46", False),
        ("      7. Ringkasan Bab", "47", False),
        ("BAB V   PENUTUP", "47", True),
        ("   A. Simpulan", "47", False),
        ("   B. Saran", "49", False),
        ("DAFTAR PUSTAKA", "50", True),
        ("LAMPIRAN", "54", True),
        ("   Lampiran 1: Ringkasan Kode Program Pipeline Komputasi Python", "54", False),
        ("   Lampiran 2: Sampel Data Historis Transaksi Binance BTC/USDT", "56", False),
        ("   Lampiran 3: Log Riwayat Percobaan 50 Trial Optuna-TPE", "58", False),
    ]

    for title, page_no, is_bold in toc_entries:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.tab_stops.add_tab_stop(Cm(13.8), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_t = p_t.add_run(title)
        set_font(r_t, "Times New Roman", 11, bold=is_bold)
        r_tab = p_t.add_run(f"\t{page_no}")
        set_font(r_tab, "Times New Roman", 11, bold=is_bold)

    doc.add_page_break()

    # =========================================================================
    # 12. DAFTAR TABEL
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("DAFTAR TABEL")
    set_font(r, "Times New Roman", 12, bold=True)

    table_entries = [
        ("Tabel 2.1", "Matriks Sintesis Penelitian Terdahulu dan Posisi Penelitian Ini", "13"),
        ("Tabel 3.1", "Jadwal Pelaksanaan Kegiatan Penelitian", "23"),
        ("Tabel 3.2", "Spesifikasi Instrumen Perangkat Lunak Penelitian", "26"),
        ("Tabel 3.3", "Ruang Pencarian Hyperparameter LSTM pada Algoritma Optuna", "30"),
        ("Tabel 3.4", "Matriks Eksperimen Terkontrol E0–E7", "33"),
        ("Tabel 3.5", "Ringkasan Alur Prosedur Pelaksanaan Penelitian", "35"),
        ("Tabel 4.1", "Statistik Deskriptif Harga Penutupan Bitcoin", "36"),
        ("Tabel 4.2", "Kinerja Baseline Naif pada Holdout", "37"),
        ("Tabel 4.3", "Hasil Ablasi Loss dan Scheduler", "38"),
        ("Tabel 4.4", "Konfigurasi Final Model Usulan E7", "38"),
        ("Tabel 4.5", "Perbandingan Kinerja Seluruh Model pada Holdout", "40"),
        ("Tabel 4.6", "Perbandingan Berpasangan pada Tanggal yang Sama", "40"),
        ("Tabel 4.7", "Kinerja E7 Menurut Rezim dan Volatilitas (Label Ex-Ante)", "41"),
    ]

    for tbl_num, tbl_title, page_no in table_entries:
        p_tb = doc.add_paragraph()
        p_tb.paragraph_format.line_spacing = 1.15
        p_tb.paragraph_format.space_after = Pt(3)
        p_tb.paragraph_format.tab_stops.add_tab_stop(Cm(13.8), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_num = p_tb.add_run(f"{tbl_num}  {tbl_title}")
        set_font(r_num, "Times New Roman", 11, bold=False)
        r_p = p_tb.add_run(f"\t{page_no}")
        set_font(r_p, "Times New Roman", 11, bold=False)

    doc.add_page_break()

    # =========================================================================
    # 13. DAFTAR GAMBAR
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("DAFTAR GAMBAR")
    set_font(r, "Times New Roman", 12, bold=True)

    figure_entries = [
        ("Gambar 4.1", "Kurva Konvergensi Nilai Validasi Optuna-TPE", "39"),
        ("Gambar 4.2", "Perbandingan Harga Aktual dan Prediksi pada Holdout", "42"),
        ("Gambar 4.3", "Diagram Batang Perbandingan Metrik", "42"),
        ("Gambar 4.4", "Distribusi Galat Absolut Menurut Model", "42"),
        ("Gambar 4.5", "Galat Menurut Rezim Pasar", "43"),
    ]

    for fig_num, fig_title, page_no in figure_entries:
        p_fg = doc.add_paragraph()
        p_fg.paragraph_format.line_spacing = 1.15
        p_fg.paragraph_format.space_after = Pt(3)
        p_fg.paragraph_format.tab_stops.add_tab_stop(Cm(13.8), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_num = p_fg.add_run(f"{fig_num}  {fig_title}")
        set_font(r_num, "Times New Roman", 11, bold=False)
        r_p = p_fg.add_run(f"\t{page_no}")
        set_font(r_p, "Times New Roman", 11, bold=False)

    doc.add_page_break()

    # =========================================================================
    # 14. DAFTAR LAMPIRAN
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("DAFTAR LAMPIRAN")
    set_font(r, "Times New Roman", 12, bold=True)

    appendix_entries = [
        ("Lampiran 1", "Ringkasan Kode Program Pipeline Komputasi Python (01 s.d. 08)", "54"),
        ("Lampiran 2", "Sampel Data Historis Transaksi Binance BTC/USDT Periode 2020–2025", "56"),
        ("Lampiran 3", "Log Riwayat Percobaan 50 Trial Optimasi Bayesian Optuna-TPE", "58"),
    ]

    for app_num, app_title, page_no in appendix_entries:
        p_ap = doc.add_paragraph()
        p_ap.paragraph_format.line_spacing = 1.15
        p_ap.paragraph_format.space_after = Pt(3)
        p_ap.paragraph_format.tab_stops.add_tab_stop(Cm(13.8), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_num = p_ap.add_run(f"{app_num}: {app_title}")
        set_font(r_num, "Times New Roman", 11, bold=False)
        r_p = p_ap.add_run(f"\t{page_no}")
        set_font(r_p, "Times New Roman", 11, bold=False)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Front matter generated successfully: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_front_matter()
