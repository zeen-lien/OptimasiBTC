"""
generate_bab5.py — Generator BAB V: PENUTUP (SIMPULAN DAN SARAN)
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Standar & Ketentuan Penulisan:
  - Mengikuti Panduan Penulisan Skripsi UNISNU Jepara (Format Penelitian Kuantitatif: A. Simpulan, B. Saran)
  - Setiap paragraf memenuhi formula SPECH (State, Premise/Problem, Evidence/Explanation, Citation, Hook/Highlight)
  - Panjang kata per paragraf: KETAT 100 - 140 kata/paragraf (bebas Turnitin & komprehensif)
  - Minimal 1 sitasi ilmiah kredibel per paragraf
  - Tipografi: Times New Roman 12pt, 1.5 spasi, first-line indent 1.0 cm, Justified
  - Margin: Top 4 cm, Left 4 cm, Bottom 3 cm, Right 3 cm
  - Notasi Matematika: Inline math menggunakan native OMML
"""

import os
import re
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml


def generate_bab5():
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
        elif token in [r"\geq", "\u2265"]:
            return '<m:r><m:t>\u2265</m:t></m:r>'
        elif token in [r"\leq", "\u2264"]:
            return '<m:r><m:t>\u2264</m:t></m:r>'
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
            clean = token.replace('\\', '')
            return f'<m:r><m:t>{clean}</m:t></m:r>'

    # ── Helper: Academic Paragraph with Inline OMML Math ──
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

    # ── Helper: Primary Sub-Heading (Level A, B...) ──
    def add_heading(text, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, "Times New Roman", 12, True, False)
        return p

    # ── Helper: Numbered Sub-Sub Heading (Level 1, 2...) ──
    def add_sub_heading(text, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, "Times New Roman", 12, True, False)
        return p

    # ==========================================================================
    #                           BAB V CONTENT
    # ==========================================================================

    # ── JUDUL BAB ──
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_before = Pt(0)
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    r_chap = p_chap.add_run("BAB V\nPENUTUP")
    set_font(r_chap, "Times New Roman", 14, True, False)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(12)

    # ==========================================================================
    # A. SIMPULAN
    # ==========================================================================
    add_heading("A. Simpulan")

    # Paragraf 1 (SPECH: ~118 kata)
    add_paragraph(
        "Berdasarkan keseluruhan rangkaian eksperimen komputasi, analisis numerik, dan pembahasan "
        "kritis yang telah diuraikan pada bab-bab sebelumnya, penelitian ini berhasil menjawab seluruh "
        "rumusan masalah dan memvalidasi hipotesis yang diajukan secara ilmiah. Peramalan harga penutupan "
        "aset kripto Bitcoin pada data deret waktu bervolatilitas tinggi menuntut suatu mekanisme penalaan "
        "parameter arsitektur jaringan saraf tiruan yang adaptif, terarah, serta bebas dari bias subjektif "
        "manusia. Integrasi algoritma Tree-structured Parzen Estimator (TPE) pada kerangka kerja Optuna "
        "terbukti mampu mengotomatisasi proses eksplorasi ruang pencarian hyperparameter LSTM secara efisien "
        "(Akiba et al., 2019; Bergstra et al., 2011). Sebagai intisari dari hasil penelitian kuantitatif ini, "
        "ditarik tiga poin simpulan esensial sebagai berikut (Creswell & Creswell, 2018)."
    )

    # Paragraf 2 (SPECH: ~124 kata)
    add_paragraph(
        "Pertama, penerapan algoritma Optuna berbasis Tree-structured Parzen Estimator (TPE) terbukti "
        "sangat efektif dalam memecahkan permasalahan penalaan hyperparameter arsitektur Long Short-Term "
        "Memory (LSTM) pada peramalan harga Bitcoin. Melalui alokasi komputasi sebanyak 50 uji coba terarah "
        "yang dipadukan dengan skema validasi silang temporal Time-Series Split 5-fold, fungsi kerugian linier MAE, "
        "dan scheduler ReduceLROnPlateau, Optuna berhasil mengidentifikasi konfigurasi parameter optimal yang paling tangguh "
        "menghadapi dinamika pasar (Feurer & Hutter, 2019). Konfigurasi optimal yang ditemukan menetapkan panjang jendela lookback "
        "$L=22$ hari, kapasitas hidden layer 100 unit neuron tunggal, tingkat Dropout 0.10, optimizer Adam "
        "dengan laju pembelajaran awal 0.00197, serta ukuran batch 16 sampel (Sakarya University, 2023). Mekanisme "
        "pemangkasan cerdas MedianPruner secara terukur mampu menghemat waktu komputasi tanpa mengorbankan "
        "kualitas penjelajahan ruang pencarian (Falkner et al., 2018)."
    )

    # Paragraf 3 (SPECH: ~124 kata)
    add_paragraph(
        "Kedua, model usulan Tier 3 (LSTM Optuna-TPE dengan MAE Loss dan ReduceLROnPlateau) secara konsisten membuktikan keunggulan performa "
        "yang superior dibandingkan model rujukan utama Tier 2 (Replikasi Manual Khumaidi dkk., 2024) serta model "
        "baseline default Tier 1 pada data out-of-sample holdout. Evaluasi pada 439 hari pengujian murni menghasilkan "
        "nilai Root Mean Square Error (RMSE) sebesar USD 2.338,22, Mean Absolute Error (MAE) sebesar USD 1.784,27, "
        "serta Mean Absolute Percentage Error (MAPE) sebesar 1,81% (Bouthillier et al., 2020). Capaian ini "
        "mencatatkan persentase penurunan error (*positive improvement*) yang sangat signifikan sebesar +40,11% "
        "(RMSE), +43,94% (MAE), dan +42,72% (MAPE) terhadap model manual Khumaidi dkk., serta penurunan galat +20,67% "
        "(RMSE) dan +23,31% (MAPE) terhadap model baseline kontrol (Makridakis et al., 2018; Willmott & Matsuura, 2005)."
    )

    # Paragraf 4 (SPECH: ~124 kata)
    add_paragraph(
        "Ketiga, penelitian ini menghasilkan temuan metodologis baru yang sangat esensial bahwa penentuan ruang pencarian "
        "hyperparameter harus dibimbing oleh teori finansial (Domain-Guided HPO) dan diselaraskan dengan objektif evaluasi. Berdasarkan Adaptive Market Hypothesis "
        "(Lo, 2004) dan dinamika Cell State LSTM (Fischer & Krauss, 2018), pemilihan jendela temporal teroptimasi 22 hari ($L=22$) "
        "terbukti jauh lebih adaptif dalam menangkap momentum harga Bitcoin dibandingkan jendela panjang 60 hari pada penelitian terdahulu "
        "maupun jendela 114 hari pada uji pra-eksperimen yang menderita fenomena kelambatan momentum (*momentum drag*). Di samping itu, "
        "harmonisasi fungsi kerugian MAE dan dynamic decay scheduler terbukti efektif menembus presisi tingkat tinggi di bawah 2% (MAPE 1,81%) "
        "pada fase pasar terbuka tanpa mengalami distorsi bobot masa lalu yang usang (Gu et al., 2020; Tashman, 2000)."
    )

    # ==========================================================================
    # B. SARAN
    # ==========================================================================
    add_heading("B. Saran")

    # Paragraf 5 (SPECH: ~120 kata)
    add_paragraph(
        "Berdasarkan temuan empiris yang diperoleh, pembahasan kritis yang mendalam, serta sejumlah keterbatasan "
        "metodologis yang telah diidentifikasi sepanjang pelaksanaan eksperimen komputasi ini, dirumuskan sejumlah rekomendasi "
        "saran operasional yang ditujukan bagi akademisi, praktisi rekayasa kecerdasan buatan, maupun pelaku industri keuangan "
        "digital. Penelitian di bidang peramalan deret waktu finansial merupakan ranah keilmuan yang terus bertransformasi "
        "secara dinamis seiring dengan pesatnya perkembangan arsitektur pembelajaran mendalam mutakhir serta perubahan likuiditas "
        "pasar global yang kian kompleks (Lim & Zohren, 2021; Goodfellow et al., 2016). Guna menyempurnakan ketahanan prediksi, "
        "memitigasi risiko overfitting, dan memperluas daya guna model peramalan prediktif pada masa mendatang, sejumlah saran "
        "strategis dan aplikatif dikemukakan sebagai berikut (Creswell & Creswell, 2018; Bouthillier et al., 2020)."
    )

    # Paragraf 6 (SPECH: ~124 kata)
    add_paragraph(
        "Pertama, penelitian lanjutan sangat disarankan untuk memperluas ruang lingkup fitur masukan dari "
        "pemodelan univariat menuju pemodelan multivariat terpadu dengan mengintegrasikan variabel sentimen pasar publik dan "
        "data fundamental on-chain jaringan Bitcoin. Mengingat laju volatilitas harga mata uang digital sangat rentan "
        "terhadap dinamika opini massa dan arus berita makroekonomi global, penggabungan metrik sentimen media sosial, indeks "
        "ketakutan dan keserakahan (Crypto Fear and Greed Index), aliran likuiditas exchange, serta volume transaksi aktif "
        "dompet digital berpotensi memperkuat kepekaan model terhadap anomali fluktuasi mendadak (BRIN & Binus, 2025; Gu et al., "
        "2020). Eksplorasi rekayasa fitur multi-sumber ini diyakini mampu menyediakan sinyal komplementer yang memperkaya "
        "kapasitas representasi jaringan saraf rekuren melampaui pola harga historis semata (Sakarya University, 2023)."
    )

    # Paragraf 7 (SPECH: ~124 kata)
    add_paragraph(
        "Kedua, peneliti berikutnya dianjurkan untuk mengeksplorasi penggabungan arsitektur pembelajaran "
        "mendalam hybrid mutakhir, seperti pengintegrasian mekanisme atensi (*Self-Attention Mechanism*), model Transformer "
        "temporal, maupun komparasi performa arsitektur Gated Recurrent Unit (GRU) dalam ruang pencarian Optuna yang sama. Penggunaan "
        "mekanisme atensi dapat membantu model memusatkan alokasi bobot pentingnya pada titik-titik waktu tertentu yang "
        "memiliki dampak volatilitas paling signifikan di dalam jendela historis masukan (Vaswani et al., 2017). Di samping "
        "itu, perluasan cakupan horizon peramalan dari estimasi satu langkah ke depan (*one-step-ahead*) menjadi multi-langkah "
        "(*multi-horizon forecasting*) sangat bernilai untuk menguji stabilitas performa model dalam jangka menengah, sehingga "
        "memberikan wawasan prediktif yang lebih komprehensif bagi perencana investasi (Lim & Zohren, 2021; Makridakis et al., 2018)."
    )

    # Paragraf 8 (SPECH: ~123 kata)
    add_paragraph(
        "Ketiga, dari aspek implementasi terapan pada ekosistem industri, kerangka kerja optimasi hyperparameter Optuna-TPE "
        "yang dikembangkan dalam skripsi ini sangat potensial untuk diintegrasikan secara langsung ke dalam sistem "
        "perdagangan algoritmik (*algorithmic trading*) atau bot transaksi berbasis eksekusi API otomatis. Implementasi "
        "dunia nyata tersebut perlu dilengkapi dengan modul kalibrasi ulang berkala (*continuous re-training pipeline*) serta "
        "wajib memperhitungkan friksi pasar riil berupa biaya komisi transaksi (transaction fee), selisih harga jual-beli "
        "(bid-ask spread), dan slippage eksekusi agar tidak menghasilkan estimasi keuntungan semu (Binance Developer API, "
        "2024; López de Prado, 2018). Integrasi praktis yang komprehensif ini akan menjembatani temuan akurasi numerik "
        "laboratorium komputasi dengan profitabilitas portofolio yang aman dan berkelanjutan (Tashman, 2000; Willmott & Matsuura, 2005)."
    )

    # ── Save Document ──
    out_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "03_Naskah_Skripsi")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BAB_5_PENUTUP_ZAINI_LEON.docx")
    doc.save(out_path)
    print(f"[SUCCESS] BAB 5 Generated successfully: {out_path}")


if __name__ == "__main__":
    generate_bab5()
