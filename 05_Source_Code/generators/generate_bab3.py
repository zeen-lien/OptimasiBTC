"""
generate_bab3.py — Generator BAB III: METODE PENELITIAN (REVISED & EXPANDED)
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Standar & Ketentuan Penulisan:
  - Mengikuti Panduan Penulisan Skripsi UNISNU Jepara (Format Penelitian Kuantitatif: A - F)
  - Setiap paragraf memenuhi formula SPECH (State, Problem/Premise, Evidence/Explanation, Citation, Hook/Highlight)
  - Panjang kata per paragraf: KETAT 100 - 140 kata/paragraf (bebas Turnitin & komprehensif)
  - Minimal 1 sitasi ilmiah kredibel per paragraf
  - Tipografi: Times New Roman 12pt, 1.5 spasi, first-line indent 1.0 cm, Justified
  - Margin: Top 4 cm, Left 4 cm, Bottom 3 cm, Right 3 cm
  - Notasi Matematika: Display equations menggunakan borderless table sebelum sectPr, inline math menggunakan native OMML
"""

import os
import re
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def generate_bab3():
    doc = docx.Document()

    # ── Page Setup (UNISNU A4: Top 4cm, Left 4cm, Bottom 3cm, Right 3cm) ──
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(4.0)
    section.left_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    # ── Helper: Font Setter ──
    def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic

    # ── Helper: LaTeX-to-OMML Converter (Inline Math) ──
    def latex_to_omml(token):
        token = token.strip().replace('\\\\', '\\')
        if token in [r"\hat{y}_t", "hat{y}_t"]:
            return '<m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e></m:acc>'
        elif token in [r"\tilde{C}_t", "tilde{C}_t"]:
            return '<m:acc><m:accPr><m:chr m:val="~"/></m:accPr><m:e><m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e></m:acc>'
        elif token == "O(N^3)":
            return '<m:r><m:t>O(</m:t></m:r><m:sSup><m:e><m:r><m:t>N</m:t></m:r></m:e><m:sup><m:r><m:t>3</m:t></m:r></m:sup></m:sSup><m:r><m:t>)</m:t></m:r>'
        elif token in [r"\ell(x)", "\u2113(x)"]:
            return '<m:r><m:t>\u2113(x)</m:t></m:r>'
        elif token == "g(x)":
            return '<m:r><m:t>g(x)</m:t></m:r>'
        elif token in [r"\geq", "\u2264"]:
            return '<m:r><m:t>\u2264</m:t></m:r>'
        elif token in [r"\geq", "\u2265"]:
            return '<m:r><m:t>\u2265</m:t></m:r>'
        elif token in [r"\times", "\u00d7"]:
            return '<m:r><m:t>\u00d7</m:t></m:r>'
        elif '_' in token and not ('^' in token or '\\' in token):
            base, sub = token.split('_', 1)
            sub = sub.strip('{}')
            return f'<m:sSub><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sub><m:r><m:t>{sub}</m:t></m:r></m:sub></m:sSub>'
        elif '^' in token and not ('_' in token or '\\' in token):
            base, sup = token.split('^', 1)
            sup = sup.strip('{}')
            return f'<m:sSup><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sup><m:r><m:t>{sup}</m:t></m:r></m:sup></m:sSup>'
        else:
            clean = (
                token.replace(r'\in', '\u2208')
                .replace(r'\gamma', '\u03b3').replace(r'\sigma', '\u03c3')
                .replace(r'\odot', '\u2299').replace(r'\ell', '\u2113')
                .replace(r'\leq', '\u2264').replace(r'\geq', '\u2265')
                .replace(r'\times', '\u00d7').replace('\\', '')
            )
            return f'<m:r><m:t>{clean}</m:t></m:r>'

    # ── Helper: Academic paragraph with inline OMML math ──
    def add_paragraph(text, space_after=6, line_spacing=1.5, first_line_indent=Cm(1.0), bold=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_after = Pt(space_after)
        if first_line_indent:
            p.paragraph_format.first_line_indent = first_line_indent

        if '$' in text:
            tokens = re.split(r'(\$[^\$]+\$)', text)
            for part in tokens:
                if not part:
                    continue
                if part.startswith('$') and part.endswith('$'):
                    omml_inner = latex_to_omml(part[1:-1])
                    omml_node = parse_xml(
                        f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_inner}</m:oMath>'
                    )
                    p._element.append(omml_node)
                else:
                    run = p.add_run(part)
                    set_font(run, "Times New Roman", 12, bold, False)
        else:
            run = p.add_run(text)
            set_font(run, "Times New Roman", 12, bold, False)
        return p

    # ── Helper: Primary Sub-Heading (Level A, B, C...) ──
    def add_heading(text, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, "Times New Roman", 12, True, False)
        return p

    # ── Helper: Numbered Sub-Sub Heading (Level 1, 2, 3...) ──
    def add_sub_heading(text, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, "Times New Roman", 12, True, False)
        return p

    # ── Helper: Display equation (borderless table, strictly placed before sectPr) ──
    def add_equation(math_xml, label):
        tbl_xml = (
            '<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            '<w:tblPr>'
            '<w:tblW w:w="7938" w:type="dxa"/>'
            '<w:jc w:val="center"/>'
            '<w:tblBorders>'
            '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
            '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
            '</w:tblBorders>'
            '<w:tblCellMar><w:top w:w="80"/><w:bottom w:w="80"/><w:left w:w="0"/><w:right w:w="0"/></w:tblCellMar>'
            '</w:tblPr>'
            '<w:tblGrid><w:gridCol w:w="6938"/><w:gridCol w:w="1000"/></w:tblGrid>'
            '<w:tr>'
            '<w:tc>'
            '<w:tcPr><w:tcW w:w="6938" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>'
            f'<m:oMathPara><m:oMath>{math_xml}</m:oMath></m:oMathPara></w:p>'
            '</w:tc>'
            '<w:tc>'
            '<w:tcPr><w:tcW w:w="1000" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="60"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            f'<w:sz w:val="22"/></w:rPr><w:t>{label}</w:t></w:r></w:p>'
            '</w:tc>'
            '</w:tr></w:tbl>'
        )
        sectPr = doc._body._element.xpath('./w:sectPr')[0]
        sectPr.addprevious(parse_xml(tbl_xml))

    # ── Helper: Styled Table ──
    def add_styled_table(headers, rows, col_widths, caption):
        # Table Caption
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.line_spacing = 1.0
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run(caption)
        set_font(r_cap, "Times New Roman", 11, True, False)

        all_rows = [headers] + rows
        t = doc.add_table(rows=len(all_rows), cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER

        for ri, row_data in enumerate(all_rows):
            for ci, cell_text in enumerate(row_data):
                cell = t.rows[ri].cells[ci]
                cell.width = col_widths[ci]
                cell.text = cell_text
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in [0] else WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    set_font(run, "Times New Roman", 9 if ri == 0 else 9, bold=(ri == 0))

        # Header Shading
        for cell in t.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>'))

        return t

    # ==========================================================================
    #                           BAB III CONTENT
    # ==========================================================================

    # ── JUDUL BAB ──
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_before = Pt(0)
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    r_chap = p_chap.add_run("BAB III\nMETODE PENELITIAN")
    set_font(r_chap, "Times New Roman", 14, True, False)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(12)

    # ==========================================================================
    # A. JENIS DAN PENDEKATAN PENELITIAN
    # ==========================================================================
    add_heading("A. Jenis dan Pendekatan Penelitian")

    # Paragraf 1 (SPECH: ~118 kata)
    add_paragraph(
        "Penelitian ini secara fundamental mengadopsi jenis penelitian kuantitatif dengan pendekatan "
        "eksperimental komputasi (computational experimental research) pada domain kecerdasan buatan dan "
        "rekayasa pembelajaran mesin. Pemilihan pendekatan kuantitatif didasari oleh kebutuhan untuk "
        "mengukur, menganalisis, serta membuktikan secara empiris perbedaan signifikansi kinerja peramalan "
        "harga Bitcoin sebelum dan sesudah intervensi optimasi hyperparameter dijalankan. Pendekatan ini "
        "memposisikan model Long Short-Term Memory (LSTM) sebagai subjek perlakuan komputasional terarah, "
        "di mana konfigurasi hyperparameter dimanipulasi secara adaptif melalui algoritma Optuna berbasis "
        "Tree-structured Parzen Estimator guna meminimalkan fungsi kerugian validasi (Akiba et al., 2019; "
        "Creswell & Creswell, 2018). Seluruh parameter keluaran diukur secara objektif melalui metrik "
        "evaluasi numerik terstandar, sehingga temuan yang dihasilkan memiliki landasan validitas internal "
        "yang sangat kuat serta terbebas dari bias penafsiran kualitatif subjektif (Feurer & Hutter, 2019)."
    )

    # Paragraf 2 (SPECH: ~121 kata)
    add_paragraph(
        "Rancangan eksperimen kuantitatif ini disusun secara komprehensif dalam sebuah kerangka kerja "
        "benchmark bertingkat yang mencakup tiga tingkatan pengujian (3-Tier Benchmark Evaluation) guna "
        "menghasilkan komparasi performa yang adil dan transparan. Ketiadaan skema pembanding bertingkat "
        "pada berbagai penelitian peramalan sering kali memicu klaim keunggulan model yang semu akibat "
        "pemilihan pembanding acuan yang terlalu lemah. Dalam skema ini, Tier 1 berfungsi sebagai kontrol "
        "dasar menggunakan konfigurasi default pustaka tanpa optimasi, Tier 2 mereplikasi model penalaan "
        "manual dari riset terdahulu oleh Khumaidi dkk. (2024), dan Tier 3 mengevaluasi arsitektur "
        "teroptimasi otomatis menggunakan Optuna-TPE (Bouthillier et al., 2020). Desain benchmark bertingkat "
        "ini memungkinkan penelitian membuktikan secara definitif apakah optimasi probabilistik terarah "
        "mampu melampaui keterbatasan heuristik manual manusia dalam menavigasi ruang pencarian berdimensi "
        "tinggi (Makridakis et al., 2018)."
    )

    # Paragraf 3 (SPECH: ~120 kata)
    add_paragraph(
        "Pendekatan eksperimen komputasional ini diimplementasikan sepenuhnya secara in-silico pada lingkungan "
        "perangkat lunak terisolasi tanpa melibatkan subjek manusia maupun intervensi laboratorium fisik basah. "
        "Karakteristik data deret waktu finansial yang bergerak sangat cepat dan memiliki dinamika non-linier "
        "menuntut suatu lingkungan eksperimen yang sepenuhnya deterministik, terkendali, dan dapat direplikasi "
        "secara identik oleh peneliti lain. Seluruh siklus hidup penelitian—mulai dari akuisisi data historis, "
        "rekayasa fitur sekuensial, pemisahan data temporal bebas kebocoran, pencarian hyperparameter, hingga "
        "pengujian out-of-sample—dijalankan melalui skrip program otomatis (López de Prado, 2018). Paradigma "
        "komputasi modern ini telah diakui secara luas dalam disiplin ilmu informatika dan sains data sebagai "
        "metodologi baku yang sah untuk menghasilkan penemuan ilmiah yang kredibel dan memiliki reprodusibilitas "
        "tinggi (Goodfellow et al., 2016; Lim & Zohren, 2021)."
    )

    # ==========================================================================
    # B. WAKTU DAN TEMPAT PENELITIAN
    # ==========================================================================
    add_heading("B. Waktu dan Tempat Penelitian")

    # Paragraf 4 (SPECH: ~118 kata)
    add_paragraph(
        "Penelitian skripsi ini dilaksanakan secara intensif dalam rentang waktu selama lima bulan, terhitung "
        "sejak bulan Oktober 2026 sampai dengan bulan Februari 2027. Alokasi waktu tersebut disusun secara "
        "sekuensial dan terstruktur ke dalam lima tahapan kerja utama guna mengantisipasi beban komputasi yang "
        "tinggi pada fase optimasi hyperparameter dengan validasi silang temporal. Tahapan kerja tersebut meliputi "
        "studi kepustakaan mendalam dan penyusunan proposal (Oktober–November 2026), akuisisi data serta "
        "prapemrosesan (November–Desember 2026), implementasi model dan optimasi Optuna-TPE (Desember 2026–Januari "
        "2027), evaluasi benchmark bertingkat (Januari 2027), hingga analisis komparatif serta penyusunan laporan "
        "skripsi lengkap (Januari–Februari 2027). Seluruh jadwal dirancang selaras dengan pedoman kalender "
        "akademik Fakultas Sains dan Teknologi UNISNU Jepara (UNISNU, 2023; Creswell & Creswell, 2018)."
    )

    # Paragraf 5 (SPECH: ~119 kata)
    add_paragraph(
        "Pelaksanaan operasional penelitian ini bertempat di Jepara, Jawa Tengah, dengan memanfaatkan sistem "
        "komputasi stasiun kerja mandiri yang terhubung langsung ke jaringan internet berkecepatan tinggi. "
        "Karakteristik penelitian informatika berbasis pemodelan kecerdasan buatan tidak menuntut kehadiran fisik "
        "di lokasi geografis tertentu atau laboratorium lapangan basah konvensional. Peneliti mengakses repositori "
        "data pasar keuangan global secara daring melalui antarmuka pertukaran aset kripto Binance, sementara "
        "seluruh tahapan pelatihan jaringan saraf dieksekusi secara lokal pada stasiun kerja komputasi pribadi. "
        "Fleksibilitas spasial ini memungkinkan eksperimen komputasi dijalankan secara kontinu dan terkontrol penuh "
        "tanpa terpengaruh hambatan fisik lokasi, sejalan dengan prinsip riset sains data dan rekayasa perangkat "
        "lunak modern berskala internasional (López de Prado, 2018; Tashman, 2000)."
    )

    # Tabel 3.1: Jadwal Pelaksanaan Penelitian
    jadwal_headers = ["No", "Tahapan Kegiatan Penelitian", "Okt 2026", "Nov 2026", "Des 2026", "Jan 2027", "Feb 2027"]
    jadwal_rows = [
        ["1", "Studi Literatur & Penyusunan Proposal Skripsi", "\u2713", "\u2713", "", "", ""],
        ["2", "Akuisisi Data Binance API & Prapemrosesan", "", "\u2713", "\u2713", "", ""],
        ["3", "Implementasi LSTM & Optimasi Optuna-TPE", "", "", "\u2713", "\u2713", ""],
        ["4", "Evaluasi 3-Tier Benchmark & Analisis Hasil", "", "", "", "\u2713", "\u2713"],
        ["5", "Penyusunan Naskah Lengkap & Sidang Skripsi", "", "", "", "", "\u2713"],
    ]
    jadwal_widths = [Cm(0.8), Cm(5.0), Cm(1.6), Cm(1.6), Cm(1.6), Cm(1.6), Cm(1.6)]
    add_styled_table(jadwal_headers, jadwal_rows, jadwal_widths, "Tabel 3.1 Jadwal Pelaksanaan Kegiatan Penelitian")

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(6)

    # ==========================================================================
    # C. POPULASI DAN SAMPEL PENELITIAN
    # ==========================================================================
    add_heading("C. Populasi dan Sampel Penelitian")

    # Paragraf 6 (SPECH: ~120 kata)
    add_paragraph(
        "Populasi sasaran dalam penelitian kuantitatif ini adalah seluruh catatan riwayat transaksi harga "
        "perdagangan pasar spot untuk pasangan mata uang kripto Bitcoin terhadap Tether (BTC/USDT) yang "
        "terdokumentasi pada platform bursa aset digital Binance. Berbeda dari pasar modal konvensional yang "
        "memiliki jam operasional terbatas dan libur akhir pekan, pasar mata uang kripto bergerak aktif selama "
        "24 jam tanpa henti sepanjang tahun sehingga menghasilkan struktur data deret waktu berdensitas sangat "
        "tinggi. Binance dipilih sebagai penyedia populasi data utama karena menempati peringkat teratas dunia "
        "dalam hal volume perdagangan likuid harian dan kedalaman pasar spot (Binance Developer API, 2024). "
        "Ukuran likuiditas yang sangat masif ini menjamin bahwa fluktuasi harga yang tercatat merefleksikan harga "
        "kesepakatan wajar global yang bebas dari distorsi manipulasi likuiditas bursa lokal (Gu et al., 2020)."
    )

    # Paragraf 7 (SPECH: ~124 kata)
    add_paragraph(
        "Penentuan sampel penelitian dilakukan secara sistematis menggunakan teknik purposive sampling dengan "
        "menetapkan sekumpulan kriteria inklusi berbasis kebutuhan arsitektur pemodelan pembelajaran mendalam. "
        "Pengambilan data deret waktu finansial tanpa kriteria yang ketat berisiko tinggi menyertakan celah data "
        "hilang atau gangguan instrumen yang dapat mendistorsi proses pembentukan jendela sekuensial pada model "
        "LSTM. Kriteria inklusi yang ditetapkan mencakup: data berbentuk candlestick harian (daily OHLCV) lengkap, "
        "rentang waktu historis mencakup minimal enam tahun kalender perdagangan, serta bebas dari kegagalan "
        "pencatatan sistem. Berdasarkan penerapan kriteria tersebut, sampel penelitian yang diperoleh mencakup data "
        "harian dari tanggal 1 Januari 2020 hingga 31 Desember 2025 dengan total 2.192 baris observasi berurutan "
        "(Hyndman & Athanasopoulos, 2018; Arlot & Celisse, 2010)."
    )

    # Paragraf 8 (SPECH: ~122 kata)
    add_paragraph(
        "Penetapan rentang waktu sampel selama enam tahun penuh secara sengaja dirancang untuk mencakup seluruh "
        "keragaman rezim pasar finansial utama kripto, mencakup tren naik tajam (bullish), tren penurunan tajam "
        "(bearish), serta fase konsolidasi menyamping (sideways). Kelemahan mendasar dari banyak model kecerdasan "
        "buatan terdahulu adalah runtuhnya akurasi saat diuji di luar periode latihan karena model hanya dilatih pada "
        "satu kondisi pasar tunggal. Periode pengamatan 2020–2025 merangkum momen peristiwa Bitcoin Halving ketiga "
        "pada Mei 2020, pencapaian rekor tertinggi harga historis pada November 2021, penurunan ekstrem pasar beruang "
        "pada 2022, hingga periode konsolidasi institusional 2023–2025 (BRIN & Binus, 2025). Keragaman siklus ini "
        "menjamin bahwa model LSTM teroptimasi diuji ketahanan dan daya generalisasinya secara menyeluruh (Tashman, "
        "2000; Makridakis et al., 2018)."
    )

    # ==========================================================================
    # D. INSTRUMEN PENELITIAN
    # ==========================================================================
    add_heading("D. Instrumen Penelitian")

    # Paragraf 9 (SPECH: ~119 kata)
    add_paragraph(
        "Instrumen penelitian dalam ranah eksperimen komputasi kecerdasan buatan mencakup perangkat keras, "
        "perangkat lunak pemrograman, kerangka kerja pustaka pemodelan, serta instrumen formulasi matematis yang "
        "digunakan untuk mengeksekusi dan mengukur seluruh tahapan penelitian. Standarisasi instrumen komputasi "
        "menjadi prasyarat mutlak dalam penelitian sains data agar hasil perhitungan numerik tidak mengalami "
        "penyimpangan akibat variasi spesifikasi dependensi perangkat. Instrumen ini dikelompokkan ke dalam tiga "
        "kategori utama, yaitu mesin komputasi perangkat keras untuk pemrosesan tensor, tumpukan perangkat lunak "
        "berbasis bahasa pemrograman Python, serta algoritma optimasi otomatis terstruktur (Creswell & Creswell, "
        "2018; Goodfellow et al., 2016). Keterpaduan instrumen-instrumen ini memastikan eksperimen berlangsung "
        "secara stabil, presisi, serta memiliki tingkat keterulangan empiris yang sempurna di lingkungan komputasi "
        "sejenis (Bouthillier et al., 2020)."
    )

    add_sub_heading("1. Perangkat Keras (Hardware)")

    # Paragraf 10 (SPECH: ~120 kata)
    add_paragraph(
        "Eksperimen komputasi pelatihan model dan penalaan hyperparameter dijalankan pada sebuah unit komputer "
        "stasiun kerja dengan arsitektur pemrosesan modern yang mampu menangani beban komputasi matriks berulang. "
        "Pelatihan arsitektur recurrent neural network melalui 50 siklus optimasi dengan skema validasi silang "
        "memerlukan stabilitas prosesor yang mumpuni agar tidak mengalami degradasi performa komputasi akibat panas "
        "berlebih. Komputer yang digunakan didukung oleh prosesor multi-core berbasis instruksi x86-64 dengan "
        "kecepatan frekuensi clock di atas 2.0 GHz per inti, dilengkapi memori akses acak (RAM) berkapasitas 8 GB "
        "untuk menampung struktur tensor berdimensi tiga selama pelatihan model berlangsung (Breuel, 2015). Media "
        "penyimpanan data mengandalkan Solid State Drive (SSD) bertransmisi tinggi guna mempercepat operasi baca "
        "dan tulis berkas dataset secara efisien (Goodfellow et al., 2016)."
    )

    add_sub_heading("2. Perangkat Lunak dan Pustaka Pemrograman (Software)")

    # Paragraf 11 (SPECH: ~123 kata)
    add_paragraph(
        "Seluruh rangkaian pengembangan algoritma dan analisis data dibangun menggunakan bahasa pemrograman "
        "Python versi 3.10 atau lebih tinggi yang telah terbukti sebagai standar industri utama dalam riset "
        "pembelajaran mesin dan rekayasa data. Inkonsistensi versi pustaka sering kali menjadi faktor utama kegagalan "
        "reproduksi kode komputasi kecerdasan buatan, sehingga spesifikasi modul perangkat lunak perlu didefinisikan "
        "secara presisi. Pustaka TensorFlow dan antarmuka Keras digunakan untuk membangun lapisan sel LSTM dan "
        "mengelola kompilasi graf komputasi jaringan saraf tiruan (TensorFlow Developers, 2024). Manipulasi larik "
        "matriks dan struktur data tabular dikelola menggunakan modul NumPy dan Pandas, transformasi data deret "
        "waktu dieksekusi dengan Scikit-learn, sementara visualisasi kurva evaluasi disusun menggunakan Matplotlib "
        "(Pedregosa et al., 2011; Akiba et al., 2019)."
    )

    # Tabel 3.2: Instrumen Perangkat Lunak Penelitian
    sw_headers = ["No", "Perangkat Lunak / Pustaka", "Versi Minimum", "Fungsi dan Peranan Utama"]
    sw_rows = [
        ["1", "Bahasa Python", "Versi \u2265 3.10", "Lingkungan eksekusi utama seluruh skrip pipeline eksperimen komputasi"],
        ["2", "TensorFlow / Keras", "Versi \u2265 2.12", "Konstruksi lapisan arsitektur LSTM, kompilasi loss, dan pelatihan model"],
        ["3", "Pustaka Optuna", "Versi \u2265 3.3", "Mesin optimasi hyperparameter otomatis berbasis TPE dan MedianPruner"],
        ["4", "Modul NumPy", "Versi \u2265 1.24", "Operasi matematis larik multidimensi dan kalkulasi metrik error evaluasi"],
        ["5", "Modul Pandas", "Versi \u2265 2.0", "Pengelolaan DataFrame, pembacaan berkas tabular CSV, dan manipulasi sekuens"],
        ["6", "Pustaka Scikit-learn", "Versi \u2265 1.3", "Implementasi penskalaan MinMaxScaler dan skema TimeSeriesSplit 5-fold"],
        ["7", "Modul Matplotlib", "Versi \u2265 3.7", "Visualisasi grafik prediksi deret waktu, kurva loss, dan konvergensi trial"],
        ["8", "Pustaka Requests", "Versi \u2265 2.31", "Ekstraksi data historis pasar spot melalui protokol HTTP Binance REST API"],
    ]
    sw_widths = [Cm(0.8), Cm(3.5), Cm(2.0), Cm(6.7)]
    add_styled_table(sw_headers, sw_rows, sw_widths, "Tabel 3.2 Spesifikasi Instrumen Perangkat Lunak Penelitian")

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(6)

    add_sub_heading("3. Instrumen Algoritma Optimasi (Optuna-TPE)")

    # Paragraf 12 (SPECH: ~124 kata)
    add_paragraph(
        "Instrumen algoritmik inti yang menjadi variabel perlakuan utama dalam penelitian ini adalah kerangka "
        "kerja Optuna yang mengintegrasikan algoritma pencarian probabilistik Tree-structured Parzen Estimator "
        "(TPE). Pendekatan optimasi konvensional seperti Grid Search mengalami kelemahan eksponensial terhadap "
        "jumlah parameter, sedangkan Random Search tidak memanfaatkan informasi evaluasi masa lalu untuk memandu "
        "pencarian berikutnya. Optuna memecahkan kendala ini melalui paradigma konstruksi ruang pencarian dinamis "
        "(Define-by-Run) dan pemodelan probabilistik Bayes non-parametrik yang secara adaptif memetakan wilayah "
        "konfigurasi hyperparameter yang menjanjikan (Bergstra et al., 2011; Akiba et al., 2019). Selain itu, "
        "keberadaan modul pemangkasan otomatis MedianPruner secara efisien memutus uji coba model yang berperforma "
        "buruk sebelum menyelesaikan seluruh putaran epoch, sehingga menghemat konsumsi waktu komputasi secara "
        "signifikan (Falkner et al., 2018)."
    )

    # ==========================================================================
    # E. TEKNIK PENGUMPULAN DATA
    # ==========================================================================
    add_heading("E. Teknik Pengumpulan Data")

    # Paragraf 13 (SPECH: ~121 kata)
    add_paragraph(
        "Pengumpulan data primer harga perdagangan pasangan BTC/USDT dilaksanakan secara terprogram melalui "
        "protokol antarmuka Binance Public REST API memanfaatkan endpoint Kline/Candlestick Data dengan resolusi "
        "temporal harian (1d). Pengumpulan data secara manual menggunakan peramban web memiliki risiko kesalahan "
        "manusia yang tinggi serta ketidakseragaman struktur pencatatan stempel waktu. Peneliti menyusun skrip "
        "pengunduh otomatis berbasis modul Requests yang mengeksekusi panggilan API berulang dengan mekanisme paginasi "
        "berdasarkan stempel waktu Unix guna menjaring seluruh data historis dari awal 2020 hingga akhir 2025 "
        "(Binance Developer API, 2024). Setiap rekaman candlestick memuat atribut harga pembukaan (Open), tertinggi "
        "(High), terendah (Low), penutupan (Close), serta volume perdagangan (Volume) yang disimpan ke dalam format "
        "CSV terstruktur untuk keperluan analisis lanjutan (Hyndman & Athanasopoulos, 2018)."
    )

    # Paragraf 14 (SPECH: ~123 kata)
    add_paragraph(
        "Segera setelah berkas data mentah berhasil dihimpun, peneliti menjalankan serangkaian prosedur audit "
        "kualitas data secara ketat tanpa melakukan interpolasi sintetis terhadap observasi yang hilang. Pada data "
        "finansial yang bervolatilitas tinggi, keberadaan anomali data berupa baris terduplikasi, nilai kosong "
        "(NaN), atau nilai tak terhingga (infinite) dapat merusak kestabilan gradien fungsi aktivasi pada model "
        "pembelajaran mendalam. Prosedur audit kualitas data mencakup lima pemeriksaan utama: kontinuitas stempel "
        "waktu harian tanpa celah, pengecekan ketiadaan rekaman ganda, verifikasi tipe data numerik presisi tinggi, "
        "serta validasi relasi geometris harga candlestick di mana harga High $\\geq$ Open, Close dan Low $\\leq$ "
        "Open, Close (Bouthillier et al., 2020). Hasil audit mengonfirmasi bahwa 2.192 data observasi berada dalam "
        "kondisi valid dan siap diproses ke tahap prapemrosesan (Hyndman & Athanasopoulos, 2018)."
    )

    add_sub_heading("1. Preprocessing Data (Normalisasi Min-Max)")

    # Paragraf 15 (SPECH: ~121 kata)
    add_paragraph(
        "Tahap prapemrosesan data deret waktu diawali dengan melakukan penskalaan nilai fitur harga penutupan "
        "(Close) ke dalam rentang numerik seragam antara 0 dan 1 memanfaatkan metode normalisasi Min-Max Scaling. "
        "Fluktuasi harga Bitcoin yang membentang sangat lebar dari level ribuan dolar hingga menembus puluhan ribu "
        "dolar dapat menyebabkan ketidakseimbangan pembaruan bobot serta memicu fenomena ledakan gradien pada "
        "fungsi aktivasi nonlinear LSTM. Melalui transformasi normalisasi ini, seluruh magnitudo nilai harga "
        "dikonversi ke dalam skala seragam yang kompatibel dengan karakteristik komputasi fungsi sigmoid dan "
        "tangensial hiperbolik pada gerbang internal LSTM (Goodfellow et al., 2016; Hochreiter & Schmidhuber, 1997). "
        "Formulasi matematis penskalaan Min-Max yang diterapkan dalam penelitian ini dinyatakan secara eksplisit pada "
        "Persamaan (3.1) sebagai berikut:"
    )

    # Persamaan (3.1): Normalisasi Min-Max (borderless table, before sectPr)
    eq_minmax = (
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>norm</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:f>'
        '<m:num>'
        '<m:r><m:t>x - </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>min</m:t></m:r></m:sub></m:sSub>'
        '</m:num>'
        '<m:den>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>max</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>min</m:t></m:r></m:sub></m:sSub>'
        '</m:den>'
        '</m:f>'
    )
    add_equation(eq_minmax, "(3.1)")

    # Paragraf 16 (SPECH: ~124 kata)
    add_paragraph(
        "Pada formulasi Persamaan (3.1), variabel $x$ melambangkan nilai harga penutupan asli, $x_{min}$ dan "
        "$x_{max}$ merepresentasikan nilai minimum dan maksimum historis data, serta $x_{norm}$ adalah hasil nilai "
        "ternormalisasi pada rentang interval nol hingga satu. Penerapan normalisasi ini dijalankan dengan mematuhi "
        "protokol ketat pencegahan kebocoran informasi masa depan (anti-temporal data leakage), suatu kekeliruan umum "
        "di mana statistik seluruh data dihitung sebelum pemisahan sampel dilakukan. Dalam penelitian ini, nilai batas "
        "ekstrem $x_{min}$ dan $x_{max}$ dihitung secara eksklusif hanya dari data pelatihan (fit on training partition), "
        "lalu parameter skalar tersebut diterapkan untuk mentransformasikan data pengujian (transform on testing set) "
        "(López de Prado, 2018). Protokol ini memastikan bahwa model tidak pernah terpapar informasi skala masa "
        "depan sebelum peramalan dieksekusi (Arlot & Celisse, 2010; Tashman, 2000)."
    )

    add_sub_heading("2. Pembentukan Jendela Data Sekuensial (Windowing)")

    # Paragraf 17 (SPECH: ~124 kata)
    add_paragraph(
        "Setelah proses normalisasi data selesai dilakukan, runtutan deret waktu satu dimensi ditransformasikan "
        "menjadi pasangan struktur masukan dan target keluaran sekuensial menggunakan teknik jendela geser (sliding "
        "window technique). Model jaringan syaraf berulang membutuhkan bentuk masukan berupa tensor berdimensi "
        "tiga yang memuat dimensi jumlah sampel, panjang langkah waktu, serta jumlah fitur guna mempelajari pola "
        "ketergantungan temporal. Untuk setiap langkah waktu ke-$t$, vektor masukan $X_t$ dibentuk dari $L$ observasi "
        "historis masa lalu berurutan $[x_{t-L+1}, ..., x_t]$, sementara target keluaran $y_t$ ditetapkan sebagai "
        "nilai harga pada langkah waktu tepat satu hari berikutnya $x_{t+1}$ (Sakarya University, 2023). Panjang "
        "jendela geser $L$ (lookback window) merupakan salah satu hyperparameter kritis yang turut dioptimasi "
        "menggunakan Optuna guna menemukan konteks historis paling optimal bagi model LSTM (Lim & Zohren, 2021; "
        "Greff et al., 2017)."
    )

    # ==========================================================================
    # F. TEKNIS ANALISIS DATA
    # ==========================================================================
    add_heading("F. Teknis Analisis Data")

    # Paragraf 18 (SPECH: ~123 kata)
    add_paragraph(
        "Teknis analisis data dalam penelitian ini dirancang secara sistematis melalui pipeline komputasi terpadu "
        "yang mencakup lima komponen analitis utama guna menjawab rumusan masalah secara komprehensif. Ketiadaan "
        "struktur analisis yang baku sering kali menyebabkan pengujian model berjalan tidak konsisten sehingga sulit "
        "untuk mengidentifikasi faktor utama peningkatan performa. Komponen analisis ini mencakup: perancangan ruang "
        "pencarian hyperparameter, prosedur optimasi probabilistik Optuna-TPE, skema validasi temporal bebas "
        "kebocoran (Time-Series Split 5-fold), pengujian model pada benchmark bertingkat 3-Tier, serta evaluasi "
        "kuantitatif persentase penurunan error peramalan (Creswell & Creswell, 2018; Bouthillier et al., 2020). "
        "Setiap tahapan analitis dikonstruksi secara logis untuk menjamin bahwa kesimpulan akhir didasarkan pada bukti "
        "empiris yang kuat, terukur, dan dapat dipertanggungjawabkan secara ilmiah (Feurer & Hutter, 2019)."
    )

    add_sub_heading("1. Definisi Ruang Pencarian Hyperparameter (Search Space)")

    # Paragraf 19 (SPECH: ~123 kata)
    add_paragraph(
        "Ruang pencarian (search space) hyperparameter arsitektur model LSTM dirumuskan secara terstruktur dengan "
        "mengacu pada sintesis literatur terkini mengenai faktor-faktor yang paling mempengaruhi generalisasi jaringan "
        "recurrent pada data finansial. Penentuan batas rentang pencarian yang terlalu sempit berpotensi mengabaikan "
        "konfigurasi terbaik, sedangkan batas yang terlalu luas memboroskan sumber daya komputasi pada wilayah parameter "
        "yang tidak realistis. Penelitian ini menetapkan lima hyperparameter kunci untuk dioptimasi: panjang jendela "
        "historis ($L$), jumlah unit neuron per lapisan tersembunyi, tingkat regularisasi Dropout, laju pembelajaran "
        "(Learning Rate), serta ukuran batch komputasi (Batch Size) sebagaimana dirangkum pada Tabel 3.3 (Sakarya "
        "University, 2023; Greff et al., 2017). Penentuan domain distribusi mengombinasikan tipe diskret, kontinu "
        "logaritmik, dan kategorikal sesuai karakteristik parameter (Bergstra et al., 2011)."
    )

    # Tabel 3.3: Ruang Pencarian Hyperparameter LSTM
    hp_headers = ["No", "Hyperparameter", "Tipe Distribusi Optuna", "Rentang Pencarian", "Deskripsi dan Peranan"]
    hp_rows = [
        ["1", "Lookback Window (L)", "suggest_int", "7 \u2013 30 hari", "Panjang sekuens domain-guided (siklus 1 minggu s.d. 1 bulan - Lo, 2004)"],
        ["2", "Hidden Units (per layer)", "suggest_int", "32 \u2013 128 neuron", "Kapasitas representasi fitur tersembunyi tanpa over-parametrization"],
        ["3", "Dropout Rate", "suggest_float", "0.1 \u2013 0.4", "Probabilitas eliminasi acak koneksi neuron untuk meredam overfitting"],
        ["4", "Learning Rate", "suggest_float (log)", "5\u00d710\u207b\u2074 \u2013 2\u00d710\u207b\u00b3", "Laju langkah penyesuaian gradien bobot sinapsis optimizer Adam (Kingma & Ba, 2014)"],
        ["5", "Batch Size", "suggest_categorical", "[16, 32, 64]", "Jumlah sampel observasi yang diproses per pembaruan gradien loss"],
    ]
    hp_widths = [Cm(0.7), Cm(2.8), Cm(2.8), Cm(2.8), Cm(4.2)]
    add_styled_table(hp_headers, hp_rows, hp_widths, "Tabel 3.3 Ruang Pencarian Hyperparameter LSTM pada Algoritma Optuna")

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_after = Pt(6)

    # Paragraf 20 (SPECH: ~124 kata)
    add_paragraph(
        "Di samping kelima parameter utama pada ruang pencarian tersebut, kedalaman arsitektur LSTM juga dieksplorasi "
        "secara dinamis antara rentang 1 hingga 2 lapisan berulang (stacked layers) guna menyesuaikan kapasitas abstraksi "
        "model terhadap kompleksitas volatilitas harga Bitcoin secara terukur. Algoritma optimasi Adam ditetapkan secara konstan "
        "sebagai optimizer utama karena memiliki mekanisme penyesuaian laju pembelajaran adaptif berbasis momen orde "
        "pertama dan kedua yang terbukti sangat stabil pada data deret waktu yang rentan terhadap derau acak (Kingma "
        "& Ba, 2014). Fungsi kerugian (loss function) yang diminimalkan selama pelatihan adalah Mean Absolute Error "
        "(MAE) yang secara matematis selaras langsung dengan formula evaluasi akhir MAPE, didukung oleh mekanisme penghentian "
        "dini (Early Stopping) dan scheduler penyesuaian laju pembelajaran dinamis (ReduceLROnPlateau) guna menghasilkan "
        "pendaratan konvergensi bobot yang mulus serta mencegah penghafalan derau data (Srivastava et al., 2014; Goodfellow et al., 2016)."
    )

    add_sub_heading("2. Prosedur Optimasi Algoritma Optuna-TPE")

    # Paragraf 21 (SPECH: ~124 kata)
    add_paragraph(
        "Proses penalaan hyperparameter dijalankan secara otomatis menggunakan kerangka kerja Optuna dengan total "
        "anggaran komputasi sebanyak 50 uji coba (trials) yang dipandu oleh algoritma Tree-structured Parzen Estimator "
        "(TPE). Pendekatan brute-force maupun pencarian acak mengabaikan riwayat uji coba masa lalu, sehingga kerap kali "
        "terjebak pada wilayah hyperparameter dengan performa yang buruk. Melalui pemodelan Bayes non-parametrik, TPE "
        "mengelompokkan riwayat uji coba terdahulu ke dalam dua distribusi kepadatan probabilitas, yaitu kelompok "
        "konfigurasi terbaik $\\ell(x)$ dan kelompok konfigurasi lainnya $g(x)$ berdasarkan nilai persentil kerugian "
        "validasi (Bergstra et al., 2011; Akiba et al., 2019). Kandidat titik konfigurasi baru selanjutnya diambil dari "
        "wilayah yang memaksimalkan rasio $\\ell(x)/g(x)$, sehingga proses eksplorasi bergerak secara cerdas menuju "
        "ruang pencarian yang berpotensi menghasilkan error minimum (Feurer & Hutter, 2019)."
    )

    # Paragraf 22 (SPECH: ~123 kata)
    add_paragraph(
        "Efisiensi eksekusi komputasi selama 50 uji coba optimasi ditingkatkan secara substansial melalui integrasi "
        "strategi pemangkasan cerdas berbasis modul MedianPruner bawaan Optuna. Menjalankan seluruh putaran epoch "
        "pelatihan pada konfigurasi hyperparameter yang sejak awal telah menunjukkan performa buruk hanya akan "
        "menghabiskan waktu dan sumber daya komputasi secara sia-sia. Pada setiap akhir epoch pelatihan model, "
        "MedianPruner secara otomatis membandingkan nilai kerugian validasi dari uji coba yang sedang berjalan terhadap "
        "nilai median dari riwayat seluruh uji coba sebelumnya pada titik epoch yang sama (Akiba et al., 2019). Apabila "
        "kinerja uji coba tersebut berada di bawah nilai median, Optuna seketika menghentikan proses pelatihan uji coba "
        "tersebut dan segera mengalokasikan daya komputasi untuk menguji kandidat konfigurasi baru berikutnya (Li et al., "
        "2017; Falkner et al., 2018)."
    )

    add_sub_heading("3. Skema Validasi Deret Waktu (Time-Series Split)")

    # Paragraf 23 (SPECH: ~124 kata)
    add_paragraph(
        "Evaluasi keandalan model selama proses optimasi hyperparameter dilakukan dengan menerapkan skema validasi "
        "silang deret waktu (Time-Series Split) sebanyak 5 lipatan (folds) secara ketat tanpa pengacakan data. "
        "Penggunaan metode K-Fold Cross-Validation konvensional yang lazim diterapkan pada data statis sangat dilarang "
        "dalam analisis deret waktu karena proses pengacakan observasi akan melanggar prinsip kausalitas temporal serta "
        "menimbulkan ilusi akurasi yang bias (data snooping). Pada skema Time-Series Split, data diurutkan secara kronologis "
        "di mana pada setiap lipatan ke-$k$, data pelatihan hanya menggunakan observasi masa lalu sebelum titik potong "
        "temporal ke-$k$, sedangkan data validasi dievaluasi pada jendela waktu berikutnya (Arlot & Celisse, 2010; "
        "Tashman, 2000). Rata-rata nilai kerugian validasi lintas lima lipatan tersebut dijadikan fungsi objektif yang "
        "diminimalkan oleh Optuna (BRIN & Binus, 2025)."
    )

    # Paragraf 24 (SPECH: ~123 kata)
    add_paragraph(
        "Secara keseluruhan, dataset penelitian dipartisi secara berurutan menurut garis waktu kronologis menjadi dua "
        "segmen utama dengan rasio 80:20, yaitu segmen data latih-validasi (in-sample) dan data uji akhir (out-of-sample). "
        "Pemisahan ini mutlak diperlukan untuk mencegah terjadinya bias seleksi (selection bias) di mana model dievaluasi "
        "pada data yang turut terlibat dalam pemilihan konfigurasi hyperparameter terbaik. Sebanyak 80% data awal "
        "(sekitar 1.754 hari) digunakan secara eksklusif untuk proses pelatihan dan validasi silang lima lipatan Optuna, "
        "sementara 20% data sisanya (sekitar 438 hari perdagangan terakhir) dicadangkan sebagai data uji holdout murni "
        "yang terkunci (López de Prado, 2018). Model dengan arsitektur terbaik hasil optimasi Optuna kemudian diuji "
        "kemampuannya pada segmen out-of-sample ini untuk mengukur akurasi peramalan yang objektif (Hyndman & "
        "Athanasopoulos, 2018; Makridakis et al., 2018)."
    )

    add_sub_heading("4. Desain Eksperimen Benchmark Bertingkat (3-Tier Evaluation)")

    # Paragraf 25 (SPECH: ~122 kata)
    add_paragraph(
        "Kinerja arsitektur model LSTM hasil penalaan otomatis Optuna-TPE dievaluasi melalui rancangan eksperimen "
        "benchmark bertingkat yang tersusun atas tiga tingkatan model pembanding yang diuji pada dataset pengujian yang "
        "sama persis. Struktur pembanding bertingkat ini memastikan bahwa klaim keunggulan performa model tidak sekadar "
        "berasal dari perbandingan terhadap baseline acuan yang lemah, melainkan teruji terhadap praktik standar industri "
        "maupun temuan penelitian terdahulu. Tier 1 memposisikan model LSTM dengan parameter konfigurasi default tanpa "
        "intervensi, Tier 2 mereplikasi spesifikasi penalaan manual terbaik dari publikasi Khumaidi dkk. (2024), dan Tier "
        "3 mengimplementasikan model hasil penalaan otomatis Optuna-TPE sebagaimana dirincikan pada Tabel 3.4 (Bouthillier "
        "et al., 2020). Desain benchmark ini menyediakan landasan bukti empiris yang transparan atas efektivitas optimasi "
        "probabilistik yang diusulkan (Makridakis et al., 2018)."
    )

    # Tabel 3.4: Desain 3-Tier Benchmark
    tier_headers = ["Tingkatan (Tier)", "Identitas Model", "Spesifikasi Konfigurasi Hyperparameter", "Tujuan dan Sasaran Pengujian"]
    tier_rows = [
        [
            "Tier 1",
            "LSTM Default\n(Baseline Kontrol)",
            "Lookback=30, Units=50, Dropout=0.2, LR=0.001, Batch=32, Layers=1, Epoch=100",
            "Menetapkan tolok ukur batas bawah performa arsitektur LSTM tanpa penalaan parameter"
        ],
        [
            "Tier 2",
            "LSTM Manual Tuning\n(Replikasi Khumaidi dkk., 2024)",
            "Lookback=60, Units=128, Dropout=0.2, LR=0.001, Batch=10, Layers=1, Epoch=100, Split=85%",
            "Menguji batas efektivitas metode coba-coba (trial-and-error) manual dari riset terdahulu"
        ],
        [
            "Tier 3",
            "LSTM Optuna-TPE\n(Model Usulan)",
            "Konfigurasi hyperparameter ditentukan secara otomatis adaptif oleh Optuna-TPE (50 trials)",
            "Membuktikan signifikansi keunggulan optimasi probabilistik terarah dibanding kedua baseline"
        ],
    ]
    tier_widths = [Cm(1.4), Cm(3.0), Cm(4.8), Cm(4.0)]
    add_styled_table(tier_headers, tier_rows, tier_widths, "Tabel 3.4 Desain Eksperimen Benchmark Bertingkat (3-Tier Evaluation)")

    p_sp5 = doc.add_paragraph()
    p_sp5.paragraph_format.space_after = Pt(6)

    add_sub_heading("5. Metrik Evaluasi Kinerja Model dan Persentase Penurunan Error")

    # Paragraf 26 (SPECH: ~123 kata)
    add_paragraph(
        "Kemampuan peramalan dari ketiga tingkatan model dievaluasi secara kuantitatif menggunakan tiga metrik "
        "pengukuran galat komputasi standar, yaitu Root Mean Square Error (RMSE), Mean Absolute Error (MAE), serta "
        "Mean Absolute Percentage Error (MAPE). Mengandalkan satu metrik tunggal berpotensi menghasilkan kesimpulan yang "
        "bias karena setiap formulasi matematis memiliki sensitivitas yang berlainan terhadap magnitudo dan deviasi "
        "data ekstrim. Metrik RMSE memberikan penalti berbobot kuadratik yang lebih tegas terhadap kesalahan bernilai "
        "besar, MAE mengukur deviasi rata-rata absolut linier yang intuitif, sedangkan MAPE merepresentasikan proporsi "
        "persentase kesalahan relatif terhadap nilai aktual harga (Willmott & Matsuura, 2005; Hyndman & Athanasopoulos, "
        "2018). Evaluasi multi-metrik ini dihitung secara eksklusif pada data pengujian out-of-sample untuk memastikan "
        "akurasi penilaian generalisasi model (Gu et al., 2020)."
    )

    # Persamaan (3.2): Improvement Percentage (borderless table, before sectPr)
    eq_improvement = (
        '<m:r><m:t>Improvement (%) = </m:t></m:r>'
        '<m:f>'
        '<m:num>'
        '<m:sSub><m:e><m:r><m:t>Error</m:t></m:r></m:e><m:sub><m:r><m:t>baseline</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>Error</m:t></m:r></m:e><m:sub><m:r><m:t>optimized</m:t></m:r></m:sub></m:sSub>'
        '</m:num>'
        '<m:den>'
        '<m:sSub><m:e><m:r><m:t>Error</m:t></m:r></m:e><m:sub><m:r><m:t>baseline</m:t></m:r></m:sub></m:sSub>'
        '</m:den>'
        '</m:f>'
        '<m:r><m:t> \u00d7 100</m:t></m:r>'
    )
    add_equation(eq_improvement, "(3.2)")

    # Paragraf 27 (SPECH: ~124 kata)
    add_paragraph(
        "Tingkat signifikansi keberhasilan optimasi diukur secara matematis melalui persentase perbaikan performa "
        "(Improvement Percentage) terhadap masing-masing baseline acuan sebagaimana dirumuskan pada Persamaan (3.2). "
        "Perbedaan nilai absolut error sering kali sulit diinterpretasikan antar-skenario pengujian yang berbeda, "
        "sehingga diperlukan standarisasi pengukuran penurunan error yang proporsional. Pada persamaan tersebut, "
        "variabel $Error_{baseline}$ menyatakan nilai metrik galat (RMSE, MAE, atau MAPE) dari model pembanding Tier 1 "
        "atau Tier 2, sedangkan $Error_{optimized}$ melambangkan nilai galat dari model usulan Tier 3 (Willmott & "
        "Matsuura, 2005). Nilai persentase perbaikan yang bertanda positif membuktikan keberhasilan algoritma Optuna-TPE "
        "dalam mereduksi kesalahan estimasi harga secara terukur dibandingkan model tanpa optimasi maupun model coba-coba "
        "manual (Makridakis et al., 2018; Bouthillier et al., 2020)."
    )

    add_sub_heading("6. Alur Prosedur Penelitian Secara Keseluruhan")

    # Paragraf 28 (SPECH: ~122 kata)
    add_paragraph(
        "Secara komprehensif, seluruh rangkaian pelaksanaan penelitian dari tahap inisiasi konseptual hingga "
        "penarikan kesimpulan akhir diintegrasikan ke dalam tujuh tahapan kerja sekuensial yang saling berkesinambungan. "
        "Penyusunan alur kerja yang terstandar menjamin bahwa seluruh proses manipulasi data dan eksekusi komputasi "
        "berjalan secara terkontrol tanpa distorsi metodologis. Tujuh tahapan kerja tersebut mencakup: akuisisi data "
        "historis via Binance API, audit kualitas dan normalisasi Min-Max, pemisahan partisi data in-sample dan "
        "out-of-sample, penalaan 50 trials Optuna-TPE dengan Time-Series Split 5-fold, pelatihan arsitektur model "
        "final, pengujian komparatif 3-Tier benchmark, serta analisis persentase penurunan error peramalan (Tabel 3.5) "
        "(Creswell & Creswell, 2018; Tashman, 2000). Rangkaian tahapan ini menegakkan keterulangan empiris serta keabsahan "
        "ilmiah dari model peramalan harga Bitcoin yang dikembangkan (Bouthillier et al., 2020)."
    )

    # Tabel 3.5: Ringkasan Alur Prosedur Penelitian
    proc_headers = ["Tahap", "Aktivitas Metodologis", "Keluaran (Output)", "Instrumen / Modul"]
    proc_rows = [
        ["1", "Pengumpulan Data Historis", "Dataset mentah BTC/USDT OHLCV (2.192 baris)", "Binance Public REST API, Requests"],
        ["2", "Audit & Prapemrosesan", "Data bersih ternormalisasi [0, 1] & tensor sekuen", "Pandas, NumPy, Scikit-learn"],
        ["3", "Partisi Data Bebas Bocor", "Segmen In-Sample (80%) dan Out-of-Sample (20%)", "Python, Pandas, Slicing temporal"],
        ["4", "Optimasi Hyperparameter", "Konfigurasi optimal hasil 50 trials & 5-fold CV", "Optuna, TPE Sampler, MedianPruner"],
        ["5", "Pelatihan Model Terpilih", "Bobot arsitektur model LSTM terlatih final", "TensorFlow/Keras, EarlyStopping"],
        ["6", "Evaluasi Out-of-Sample", "Nilai metrik RMSE, MAE, dan MAPE per tingkatan", "Scikit-learn, NumPy, Matplotlib"],
        ["7", "Analisis Komparatif", "Tabel benchmark 3-Tier & persentase perbaikan", "Python, Formulasi Matematis Galat"],
    ]
    proc_widths = [Cm(1.0), Cm(3.4), Cm(4.5), Cm(4.3)]
    add_styled_table(proc_headers, proc_rows, proc_widths, "Tabel 3.5 Ringkasan Alur Prosedur Pelaksanaan Penelitian")

    # ── Save Document ──
    out_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "03_Naskah_Skripsi")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BAB_3_METODE_PENELITIAN_ZAINI_LEON.docx")
    doc.save(out_path)
    print(f"[SUCCESS] BAB 3 Generated successfully: {out_path}")


if __name__ == "__main__":
    generate_bab3()
