import os
import re
import docx
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_enhanced_bab2():
    doc = docx.Document()

    # 1. Page Setup according to UNISNU Guidelines (A4, 4-4-3-3 cm)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(4.0)
    section.left_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    # Helper function for setting font properties
    def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic

    # Helper function to convert inline math expressions to native Word OMML
    def latex_to_omml(token):
        token = token.strip()
        # Normalize double-escaped backslashes from Python string literals
        token = token.replace('\\\\', '\\')
        if token in [r"\hat{y}_t", "hat{y}_t"]:
            return '<m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e></m:acc>'
        elif token in [r"\tilde{C}_t", "tilde{C}_t"]:
            return '<m:acc><m:accPr><m:chr m:val="~"/></m:accPr><m:e><m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e></m:acc>'
        elif token == "O(N^3)":
            return '<m:r><m:t>O(</m:t></m:r><m:sSup><m:e><m:r><m:t>N</m:t></m:r></m:e><m:sup><m:r><m:t>3</m:t></m:r></m:sup></m:sSup><m:r><m:t>)</m:t></m:r>'
        elif token == "y^*":
            return '<m:sSup><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sup><m:r><m:t>*</m:t></m:r></m:sup></m:sSup>'
        elif r"t \in" in token:
            clean_range = token.replace(r'\in', '\u2208')
            return f'<m:r><m:t>{clean_range}</m:t></m:r>'
        elif token in [r"\ell(x)/g(x)", "\u2113(x)/g(x)"]:
            return '<m:r><m:t>\u2113(x)/g(x)</m:t></m:r>'
        elif token in [r"\ell(x)", "\u2113(x)"]:
            return '<m:r><m:t>\u2113(x)</m:t></m:r>'
        elif token == "g(x)":
            return '<m:r><m:t>g(x)</m:t></m:r>'
        elif token == "P(y|x)":
            return '<m:r><m:t>P(y|x)</m:t></m:r>'
        elif token == "P(x|y)":
            return '<m:r><m:t>P(x|y)</m:t></m:r>'
        elif token in [r"\gamma", "\u03b3"]:
            return '<m:r><m:t>\u03b3</m:t></m:r>'
        elif token in [r"\sigma", "\u03c3"]:
            return '<m:r><m:t>\u03c3</m:t></m:r>'
        elif token in [r"\odot", "\u2299"]:
            return '<m:r><m:t>\u2299</m:t></m:r>'
        elif '_' in token and not ('^' in token or '\\' in token):
            base, sub = token.split('_', 1)
            sub = sub.strip('{}')
            return f'<m:sSub><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sub><m:r><m:t>{sub}</m:t></m:r></m:sub></m:sSub>'
        else:
            clean = (
                token.replace(r'\in', '\u2208')
                .replace(r'\gamma', '\u03b3')
                .replace(r'\sigma', '\u03c3')
                .replace(r'\odot', '\u2299')
                .replace(r'\ell', '\u2113')
                .replace('\\', '')
            )
            return f'<m:r><m:t>{clean}</m:t></m:r>'

    # Helper function for academic body paragraphs (SPECH formula) with native inline math support
    def add_academic_paragraph(text, space_after=6, line_spacing=1.5, first_line_indent=Cm(1.0)):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_after = Pt(space_after)
        if first_line_indent:
            p.paragraph_format.first_line_indent = first_line_indent
        
        # Check if text contains inline math notation $...$
        if '$' in text:
            tokens = re.split(r'(\$[^\$]+\$)', text)
            for part in tokens:
                if not part:
                    continue
                if part.startswith('$') and part.endswith('$'):
                    math_content = part[1:-1]
                    omml_inner = latex_to_omml(math_content)
                    omml_node = parse_xml(f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_inner}</m:oMath>')
                    p._element.append(omml_node)
                else:
                    run = p.add_run(part)
                    set_font(run, "Times New Roman", 12, False, False)
        else:
            run = p.add_run(text)
            set_font(run, "Times New Roman", 12, False, False)
        return p

    # Helper function for native Word OMML equation with right-aligned numbering inserted strictly in-sequence
    def add_omml_equation(math_content_xml, label_text):
        tbl_xml = (
            f'<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            f'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f'<w:tblPr>'
            f'<w:tblW w:w="7938" w:type="dxa"/>'
            f'<w:jc w:val="center"/>'
            f'<w:tblBorders>'
            f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
            f'<w:insideH w:val="none"/><w:insideV w:val="none"/>'
            f'</w:tblBorders>'
            f'<w:tblCellMar><w:top w:w="80"/><w:bottom w:w="80"/><w:left w:w="0"/><w:right w:w="0"/></w:tblCellMar>'
            f'</w:tblPr>'
            f'<w:tblGrid>'
            f'<w:gridCol w:w="6938"/>'
            f'<w:gridCol w:w="1000"/>'
            f'</w:tblGrid>'
            f'<w:tr>'
            f'<w:tc>'
            f'<w:tcPr><w:tcW w:w="6938" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>'
            f'<m:oMathPara><m:oMath>{math_content_xml}</m:oMath></m:oMathPara>'
            f'</w:p>'
            f'</w:tc>'
            f'<w:tc>'
            f'<w:tcPr><w:tcW w:w="1000" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="60"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr><w:t>{label_text}</w:t></w:r>'
            f'</w:p>'
            f'</w:tc>'
            f'</w:tr>'
            f'</w:tbl>'
        )
        # CRITICAL FIX: Insert table immediately before sectPr to preserve strict chronological document sequence!
        sectPr = doc._body._element.xpath('./w:sectPr')[0]
        sectPr.addprevious(parse_xml(tbl_xml))

    # --- JUDUL BAB ---
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_before = Pt(0)
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    r_chap = p_chap.add_run("BAB II\nLANDASAN TEORI")
    set_font(r_chap, "Times New Roman", 14, True, False)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(12)

    # =========================================================================
    # A. PENELITIAN TERDAHULU (KAJIAN PUSTAKA RELEVAN)
    # =========================================================================
    p_subA = doc.add_paragraph()
    p_subA.paragraph_format.space_before = Pt(12)
    p_subA.paragraph_format.space_after = Pt(6)
    p_subA.paragraph_format.line_spacing = 1.5
    r_subA = p_subA.add_run("A. Penelitian Terdahulu yang Relevan")
    set_font(r_subA, "Times New Roman", 12, True, False)

    p_a_intro = (
        "Penelitian mengenai peramalan deret waktu dan optimasi arsitektur deep learning telah berkembang pesat "
        "seiring dengan meningkatnya kebutuhan model prediktif pada instrumen bervolatilitas tinggi seperti cryptocurrency. "
        "Kajian terhadap literatur terdahulu memiliki peranan mendasar guna membedah kelebihan serta keterbatasan metodologi "
        "yang telah ada, sehingga posisi kebaruan (novelty) dan kontribusi penelitian ini dapat ditempatkan secara tegas "
        "dan dapat dipertanggungjawabkan (Creswell & Creswell, 2018). Penelitian ini berakar pada delapan kajian ilmiah "
        "utama yang menginvestigasi model Long Short-Term Memory (LSTM), teknik hyperparameter optimization (HPO), serta skema "
        "validasi deret waktu finansial. Rincian ulasan kritis terhadap masing-masing paper tersebut dijabarkan sebagai berikut:"
    )
    add_academic_paragraph(p_a_intro)

    # --- 8 PAPER BREAKDOWN (SEPERTI CONTOH TEMAN / KAMPUS) ---
    paper_reviews = [
        (
            "1. JUTIF (2026): Comparative Analysis of HPO Methods for LSTM",
            "Kajian yang diterbitkan dalam Jurnal Teknik Informatika (JUTIF, 2026) berjudul \"Comparative Analysis of Hyperparameter Optimization Methods for LSTM in Cryptocurrency Price Prediction: An Application to TRX–USD\" mengevaluasi enam teknik optimasi parameter (Grid Search, Random Search, Hyperopt, Optuna, Particle Swarm Optimization/PSO, dan Genetic Algorithm/GA) pada arsitektur LSTM menggunakan 2.096 data historis harian dari Binance. Hasil evaluasi empiris membuktikan bahwa metode metaheuristik dan Bayesian Optimization menghasilkan akurasi tertinggi, di mana GA dan Optuna mencapai nilai koefisien determinasi (R-squared) sebesar 0,8088 dengan error terendah, sementara Random Search terpuruk dengan R-squared hanya 0,28.",
            "Kaitan dengan penelitian ini terletak pada pemilihan kerangka kerja Optuna sebagai algoritma pencarian hyperparameter utama yang telah terbukti secara empiris jauh lebih unggul dan efisien dibanding teknik acak maupun grid. Namun, keterbatasan kajian JUTIF (2026) terletak pada pengujian yang hanya berfokus pada aset kripto alternatif (TRX/USD) dan hanya mengandalkan satu pembagian data statis (static train-test split). Penelitian ini mengatasi celah tersebut dengan memfokuskan pengujian pada aset utama Bitcoin (BTC/USDT) serta mengintegrasikan skema Time-Series Split untuk menguji ketahanan model terhadap pergeseran rezim tren pasar."
        ),
        (
            "2. Khumaidi, Kusmanto, dan Hikmah (ILKOM Jurnal Ilmiah, 2024)",
            "Penelitian oleh Khumaidi dkk. (2024) yang dipublikasikan pada ILKOM Jurnal Ilmiah (SINTA 2) berjudul \"Optimizing Bitcoin Price Predictions Using Long Short-Term Memory Algorithm: A Deep Learning Approach\" menguji akurasi algoritma LSTM untuk memprediksi harga penutupan Bitcoin selama rentang waktu 3 tahun. Penyetelan hyperparameter dilakukan secara manual melalui tiga skenario variasi data latih (80%, 85%, 90%), ukuran batch (10 dan 20), serta 100 epoch. Hasil penelitian menyimpulkan bahwa konfigurasi data latih 85%, batch size 10, dan 100 epoch menghasilkan performa terbaik dengan tingkat akurasi rata-rata 93,69% dan tingkat kesalahan (error rate) terendah sebesar 6,31%.",
            "Kajian Khumaidi dkk. (2024) menjadi rujukan krusial sekaligus berperan sebagai model pembanding Tier-2 Baseline (manual tuning) dalam penelitian ini. Kendati menunjukkan hasil yang baik, kelemahan mendasar penelitian tersebut adalah proses optimasi yang masih dilakukan secara coba-coba manual (trial-and-error) pada ruang parameter diskret yang sangat sempit. Penelitian ini menyempurnakan kelemahan tersebut dengan menggantikan proses coba-coba manual menggunakan optimasi cerdas berbasis algoritma Tree-structured Parzen Estimator (TPE) pada ruang pencarian kontinu berdimensi jamak."
        ),
        (
            "3. BRIN dan Bina Nusantara University (Journal of Open Innovation, 2025)",
            "Studi komprehensif oleh peneliti Badan Riset dan Inovasi Nasional (BRIN) bersama Binus University (2025) berjudul \"Improved LSTM Hyperparameters Alongside Sentiment Walk-Forward\" dalam jurnal bereputasi internasional (Scopus Q1) mengungkap fenomena kritis mengenai bias estimasi pada pemodelan deret waktu finansial. Penelitian tersebut membuktikan bahwa optimasi hyperparameter yang dijalankan pada potongan data statis menghasilkan kesimpulan semu akibat overfitting temporal. Dengan mengintegrasikan Bayesian Optimization bersama protokol validasi jendela bergerak (Walk-Forward Validation) melintasi 10 iterasi, studi tersebut berhasil memangkas nilai RMSE rata-rata sebesar 24,3% dan meningkatkan stabilitas prediksi secara konsisten.",
            "Penelitian BRIN (2025) menjadi pijakan metodologis terpenting bagi penelitian ini dalam menerapkan skema validasi deret waktu yang ketat bebas kebocoran informasi masa depan (temporal data leakage). Celah penelitian yang disasar adalah bahwa studi BRIN berfokus pada instrumen saham perbankan (BBRI) dengan volatilitas terkontrol. Penelitian ini membawa kebaruan metodologis tersebut ke dalam pasar Bitcoin yang memiliki volatilitas dan dinamika non-stasioneritas yang jauh lebih ekstrem, serta memperluas ruang pencarian ke arsitektur multi-layer LSTM."
        ),
        (
            "4. Bit-Tech (2026): Comparative Analysis of LSTM and GRU Models with HPO",
            "Artikel ilmiah pada jurnal Bit-Tech (2026) berjudul \"Comparative Analysis of LSTM and GRU Models with Hyperparameter Optimization for Bitcoin Price Prediction\" membandingkan efisiensi dan akurasi antara arsitektur Long Short-Term Memory (LSTM) dan Gated Recurrent Unit (GRU) pada data harga penutupan Bitcoin dari Yahoo Finance. Proses optimasi parameter dilakukan menggunakan metode Grid Search terstandardisasi. Temuan studi memperlihatkan adanya kompromi komputasi (accuracy-efficiency trade-off), di mana GRU unggul dalam kecepatan waktu pelatihan karena arsitekturnya yang lebih ringkas, sedangkan LSTM menunjukkan stabilitas metrik MAPE yang lebih baik pada peramalan rentang waktu panjang.",
            "Kaitan kajian tersebut dengan penelitian ini adalah penegasan posisi LSTM sebagai model yang tangguh dalam mempertahankan dependensi temporal panjang. Celah riset yang ditinggalkan oleh Bit-Tech (2026) adalah penggunaan Grid Search yang menuntut biaya komputasi sangat mahal dan tidak realistis saat jumlah kombinasi parameter meningkat. Penelitian ini menjawab limitasi tersebut dengan menerapkan algoritma Optuna-TPE yang secara probabilistik memfokuskan pencarian pada area hyperparameter yang paling menjanjikan, sehingga memangkas waktu komputasi secara signifikan."
        ),
        (
            "5. Ganesha, Ratmadani, dkk. (JUTIF, 2025): Streamlit Implementation",
            "Kajian terapan oleh Ganesha dkk. (2025) dalam Jurnal Teknik Informatika (JUTIF, SINTA 2) berjudul \"Forecasting Bitcoin Price Prediction with Long Short-Term Memory Networks Implementation and Applications Using Streamlit\" mengembangkan pipeline peramalan harga Bitcoin dari Yahoo Finance dan mengintegrasikannya ke dalam aplikasi web interaktif berbasis Streamlit. Model LSTM dievaluasi menggunakan metrik Mean Absolute Error (MAE sebesar 150,57) dan Root Mean Square Error (RMSE sebesar 231,90) untuk memvisualisasikan pergerakan harga historis dan masa depan secara langsung.",
            "Kaitan penelitian Ganesha dkk. (2025) terhadap penelitian ini terletak pada standardisasi pipeline pemrosesan data deret waktu Bitcoin dan penggunaan metrik evaluasi formal. Namun, kelemahan utama dari penelitian tersebut adalah arsitektur LSTM yang digunakan masih berkonfigurasi bawaan (default/statis) tanpa adanya tahapan hyperparameter tuning sistematis. Penelitian ini mengisi celah tersebut dengan merekayasa proses optimasi hyperparameter otomatis multi-variabel untuk menjamin bahwa model yang dihasilkan memiliki akurasi yang teroptimasi secara maksimal."
        ),
        (
            "6. Sakarya University (2023): LSTM Hparam Optimization for Bitcoin",
            "Penelitian oleh Sakarya University Journal of Computer and Information Sciences (2023) berjudul \"LSTM Hyperparameters Optimization with Hparam Parameters for Bitcoin Price Prediction\" menginvestigasi pengaruh delapan hyperparameter arsitektur LSTM (go-backward, epoch, batch size, dropout rate, fungsi aktivasi, jenis optimizer, learning rate, dan jumlah neuron) terhadap error prediksi Bitcoin. Dengan memanfaatkan modul visualisasi koordinat paralel TensorBoard Hparam, studi tersebut menemukan bahwa optimizer Adam memberikan konvergensi Mean Square Error (MSE) terendah dan paling stabil dibandingkan SGD dan RMSprop pada data deret waktu.",
            "Kajian Sakarya University (2023) memberikan rujukan berharga bagi penelitian ini dalam menyusun batasan ruang pencarian (search space) hyperparameter yang relevan pada model LSTM. Keterbatasan dari penelitian tersebut adalah modul Hparam hanya bertindak sebagai alat pemetaan kombinasi diskret pasif tanpa memiliki mekanisme pembelajaran konvergensi adaptif. Penelitian ini melangkah lebih maju dengan menggunakan algoritma Optuna-TPE yang memiliki fungsi akuisisi Expected Improvement untuk memandu pencarian parameter secara cerdas."
        ),
        (
            "7. Ula, Ilhadi, dan Sidek (MATRIK, 2024): LSTM vs Random Forest",
            "Artikel ilmiah pada jurnal terakreditasi SINTA 2 MATRIK (2024) berjudul \"Comparing Long Short-Term Memory and Random Forest Accuracy for Bitcoin Price Forecasting\" menguji perbandingan kinerja antara model deep learning LSTM dan algoritma ensemble machine learning Random Forest pada data historis penutupan Bitcoin. Hasil eksperimen empiris membuktikan bahwa arsitektur LSTM secara konsisten mengungguli Random Forest dengan menghasilkan nilai Mean Absolute Percentage Error (MAPE) yang jauh lebih kecil, membuktikan keandalan mekanisme gerbang berulang dalam menangkap pola autokorelasi deret waktu.",
            "Kajian Ula dkk. (2024) memperkuat landasan teoretis penelitian ini bahwa LSTM merupakan algoritma yang paling tepat untuk menangani data deret waktu finansial yang sarat fluktuasi. Celah riset yang belum diselesaikan adalah bahwa model LSTM dalam studi tersebut masih menggunakan konfigurasi standar tanpa optimasi hyperparameter. Penelitian ini melengkapi temuan tersebut dengan membuktikan bahwa akurasi LSTM dapat ditingkatkan lebih jauh melalui optimasi terarah berbasis algoritma Optuna."
        ),
        (
            "8. Akiba et al. (2019) dan Bergstra et al. (2011): Optuna & TPE",
            "Kajian seminal oleh Akiba et al. (2019) pada ACM SIGKDD berjudul \"Optuna: A Next-Generation Hyperparameter Optimization Framework\" memperkenalkan arsitektur Define-by-Run dan strategi pemangkasan otomatis (Asynchronous Successive Halving / MedianPruner). Algoritma pencarian probabilistik yang digunakan berpijak pada fondasi matematis Tree-structured Parzen Estimator (TPE) yang dikembangkan oleh Bergstra et al. (2011) pada konferensi NIPS, yang memodelkan distribusi probabilitas konfigurasi hyperparameter berdasarkan riwayat evaluasi fungsi loss melalui aturan Bayes.",
            "Paper Akiba et al. (2019) dan Bergstra et al. (2011) menjadi landasan teoretis dan algoritmik utama bagi instrumen optimasi dalam penelitian ini. Kontribusi kebaruan penelitian ini adalah mengimplementasikan algoritma Optuna-TPE pada model LSTM untuk data deret waktu Bitcoin dengan mengintegrasikan mekanisme pemangkasan dini (early pruning) dan skema validasi deret waktu (Time-Series Split) guna menghasilkan model peramalan yang akurat dan efisien secara komputasi."
        )
    ]

    for title, p1, p2 in paper_reviews:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.5
        r_t = p_t.add_run(title)
        set_font(r_t, "Times New Roman", 12, True, False)
        add_academic_paragraph(p1, space_after=3)
        add_academic_paragraph(p2, space_after=6)

    # --- TABEL 2.1: MATRIKS PENELITIAN TERDAHULU ---
    p_tab_label = doc.add_paragraph()
    p_tab_label.paragraph_format.space_before = Pt(10)
    p_tab_label.paragraph_format.space_after = Pt(3)
    p_tab_label.paragraph_format.line_spacing = 1.0
    r_tl = p_tab_label.add_run("Tabel 2.1 Matriks Sintesis Penelitian Terdahulu dan Posisi Penelitian Ini")
    set_font(r_tl, "Times New Roman", 11, True, False)

    table_data = [
        ["No", "Peneliti & Tahun", "Metode & Model", "Dataset & Objek", "Temuan Utama", "Celah Riset & Posisi Penelitian Ini"],
        [
            "1",
            "JUTIF\n(2026)",
            "LSTM + 6 HPO (Grid, Random, Optuna, Hyperopt, PSO, GA)",
            "TRX/USD Binance (2.096 data harian)",
            "Optuna & GA mencapai akurasi tertinggi (R2 = 0,8088); Random Search terburuk.",
            "Celah: Hanya uji koin alternatif dan static split.\nPosisi: Menguji Bitcoin dengan Time-Series Split."
        ],
        [
            "2",
            "Khumaidi dkk.\n(ILKOM, 2024)",
            "LSTM + Penyetelan Manual (Trial-and-Error)",
            "Bitcoin Closing Price (3 tahun data)",
            "Kombinasi batch 10, split 85%, epoch 100 hasilkan akurasi 93,69% dan error 6,31%.",
            "Celah: Pencarian manual diskret rawan local minima.\nPosisi: Dijadikan Tier-2 Baseline pembanding."
        ],
        [
            "3",
            "BRIN & Binus\n(JOItmC, 2025)",
            "LSTM + Bayesian Optimization + Walk-Forward",
            "Data Saham & Indikator Finansial",
            "Static split picu biased estimation error; walk-forward pangkas RMSE 24,3%.",
            "Celah: Terbatas pada saham perbankan.\nPosisi: Menerapkan walk-forward pada Bitcoin."
        ],
        [
            "4",
            "Bit-Tech\n(2026)",
            "Komparasi LSTM vs GRU + Grid Search",
            "Bitcoin Closing Price (Yahoo Finance)",
            "GRU lebih cepat dalam komputasi, namun LSTM lebih stabil dalam MAPE.",
            "Celah: Grid Search boros komputasi eksponensial.\nPosisi: Mengganti Grid Search dengan Optuna-TPE."
        ],
        [
            "5",
            "Ganesha dkk.\n(JUTIF, 2025)",
            "LSTM Default + Web App Streamlit",
            "Bitcoin Closing Price (Yahoo Finance)",
            "Berhasil visualisasi prediksi interaktif dengan MAE 150,57 dan RMSE 231,90.",
            "Celah: Parameter model statis tanpa optimasi.\nPosisi: Melakukan optimasi otomatis multi-variabel."
        ],
        [
            "6",
            "Sakarya Univ.\n(2023)",
            "LSTM + TensorBoard HParam",
            "Data Bitcoin (8 parameter uji)",
            "Optimizer Adam paling stabil dan menghasilkan MSE terendah.",
            "Celah: Hparam hanya pemetaan pasif tanpa konvergensi.\nPosisi: Optimasi probabilistik terarah via TPE."
        ],
        [
            "7",
            "Ula dkk.\n(MATRIK, 2024)",
            "Komparasi LSTM vs Random Forest",
            "Data Deret Waktu Bitcoin",
            "LSTM terbukti lebih unggul dibanding Random Forest pada data temporal.",
            "Celah: Model LSTM tidak dioptimasi (default).\nPosisi: Mengoptimalkan parameter LSTM secara penuh."
        ],
        [
            "8",
            "Akiba et al. (2019) & Bergstra (2011)",
            "Framework Optuna & Algoritma TPE",
            "Algoritma HPO & Benchmark ML",
            "Define-by-Run dan TPE memangkas waktu komputasi via Asynchronous MedianPruner.",
            "Celah: Paper fondasi algoritma umum.\nPosisi: Instrumen optimasi utama model LSTM Bitcoin."
        ],
        [
            "9",
            "Penelitian Ini\n(Zaini, 2026)",
            "LSTM Teroptimasi Optuna-TPE + Time-Series Split",
            "Data Deret Waktu Harian BTC/USDT (Binance API)",
            "Membuktikan penurunan error bertingkat (positive improvement) secara terukur.",
            "Menjawab tuntas seluruh celah: Optimasi TPE terarah, validasi anti-leakage, dan benchmark 3-tier adil."
        ]
    ]

    t2 = doc.add_table(rows=len(table_data), cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Cm(0.8), Cm(2.2), Cm(3.2), Cm(2.8), Cm(4.0), Cm(4.2)]

    for row_idx, row in enumerate(t2.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            cell.text = table_data[row_idx][col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1] else WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for run in p.runs:
                is_head = (row_idx == 0)
                is_last_row = (row_idx == len(table_data) - 1)
                set_font(run, "Times New Roman", 9 if is_head else 8.5, bold=(is_head or is_last_row))

    for cell in t2.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>'))
    for cell in t2.rows[-1].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F5FA"/>'))

    # Spacer
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # B. LANDASAN TEORI
    # =========================================================================
    p_subB = doc.add_paragraph()
    p_subB.paragraph_format.space_before = Pt(14)
    p_subB.paragraph_format.space_after = Pt(6)
    p_subB.paragraph_format.line_spacing = 1.5
    r_subB = p_subB.add_run("B. Landasan Teori")
    set_font(r_subB, "Times New Roman", 12, True, False)

    # 1. Karakteristik Data Deret Waktu & Bitcoin
    p_b1_title = doc.add_paragraph()
    p_b1_title.paragraph_format.space_before = Pt(6)
    p_b1_title.paragraph_format.space_after = Pt(3)
    p_b1_title.paragraph_format.line_spacing = 1.5
    r_b1_t = p_b1_title.add_run("1. Karakteristik Data Deret Waktu dan Volatilitas Pasar Bitcoin")
    set_font(r_b1_t, "Times New Roman", 12, True, False)

    p_b1_1 = (
        "Data deret waktu (time series) didefinisikan sebagai sekumpulan observasi terindeks waktu yang "
        "dihasilkan melalui proses pengukuran berulang pada interval waktu diskret yang teratur (Hyndman & Athanasopoulos, 2018). "
        "Dalam ekosistem aset digital, data harga historis Bitcoin (BTC/USDT) membentuk struktur deret waktu dengan derajat "
        "non-stasioneritas yang sangat tinggi, di mana parameter statistik seperti rata-rata (mean) dan variansi tidak konstan "
        "sepanjang waktu (Lim & Zohren, 2021). Pasar mata uang kripto beroperasi tanpa jeda selama 24 jam sehari secara global, "
        "menjadikan pergerakan harga penutupan harian sangat sensitif terhadap perubahan likuiditas, sentimen publik, serta "
        "pergeseran tren pasar (regime shift) yang tidak berpola linier (Aswadi & Ependi, 2022)."
    )
    add_academic_paragraph(p_b1_1)

    # 2. Arsitektur Jaringan Saraf Tiruan LSTM
    p_b2_title = doc.add_paragraph()
    p_b2_title.paragraph_format.space_before = Pt(8)
    p_b2_title.paragraph_format.space_after = Pt(3)
    p_b2_title.paragraph_format.line_spacing = 1.5
    r_b2_t = p_b2_title.add_run("2. Arsitektur Jaringan Saraf Tiruan Long Short-Term Memory (LSTM)")
    set_font(r_b2_t, "Times New Roman", 12, True, False)

    p_b2_1 = (
        "Long Short-Term Memory (LSTM) merupakan arsitektur mutakhir dari Recurrent Neural Network (RNN) yang "
        "dirancang secara khusus oleh Hochreiter & Schmidhuber (1997) guna memecahkan masalah hilangnya gradien "
        "(vanishing gradient) dan ledakan gradien (exploding gradient) pada data sekuensial panjang. Pada RNN konvensional, "
        "perkalian matriks bobot berulang melintasi langkah waktu menyebabkan sinyal kesalahan melemah secara eksponensial "
        "saat ditransmisikan kembali melalui waktu (backpropagation through time). LSTM mengatasi kendala tersebut dengan "
        "memperkenalkan cell state internal ($C_t$) sebagai jalur transmisi memori linear yang diregulasi oleh tiga gerbang "
        "logika utama: forget gate ($f_t$), input gate ($i_t$), dan output gate ($o_t$) (Greff et al., 2017; Lipton et al., 2015)."
    )
    add_academic_paragraph(p_b2_1)

    p_b2_intro_eq = (
        "Mekanisme transmisi data dan pembaruan keadaan memori internal sel LSTM pada langkah waktu $t$ dengan vektor "
        "masukan $x_t$ dan vektor keadaan tersembunyi sebelumnya $h_{t-1}$ diformulasikan secara matematis melalui "
        "Persamaan (2.1) sampai dengan Persamaan (2.6) sebagai berikut (Hochreiter & Schmidhuber, 1997; Goodfellow et al., 2016):"
    )
    add_academic_paragraph(p_b2_intro_eq, space_after=3)

    # --- EQUATIONS 2.1 - 2.6 (NATIVE OMML WORD MATH) ---
    eq_f_xml = (
        '<m:sSub><m:e><m:r><m:t>f</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = σ(</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>W</m:t></m:r></m:e><m:sub><m:r><m:t>f</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> · [</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>, </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>] + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>f</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>)</m:t></m:r>'
    )
    add_omml_equation(eq_f_xml, "(2.1)")

    eq_i_xml = (
        '<m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = σ(</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>W</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> · [</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>, </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>] + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>)</m:t></m:r>'
    )
    add_omml_equation(eq_i_xml, "(2.2)")

    eq_c_tilde_xml = (
        '<m:acc><m:accPr><m:chr m:val="~"/></m:accPr><m:e>'
        '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:acc>'
        '<m:r><m:t> = tanh(</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>W</m:t></m:r></m:e><m:sub><m:r><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> · [</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>, </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>] + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>)</m:t></m:r>'
    )
    add_omml_equation(eq_c_tilde_xml, "(2.3)")

    eq_c_xml = (
        '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>f</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> ⊙ </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> ⊙ </m:t></m:r>'
        '<m:acc><m:accPr><m:chr m:val="~"/></m:accPr><m:e>'
        '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:acc>'
    )
    add_omml_equation(eq_c_xml, "(2.4)")

    eq_o_xml = (
        '<m:sSub><m:e><m:r><m:t>o</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = σ(</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>W</m:t></m:r></m:e><m:sub><m:r><m:t>o</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> · [</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>, </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>] + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>o</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>)</m:t></m:r>'
    )
    add_omml_equation(eq_o_xml, "(2.5)")

    eq_h_xml = (
        '<m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>o</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> ⊙ tanh(</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>)</m:t></m:r>'
    )
    add_omml_equation(eq_h_xml, "(2.6)")

    p_b2_desc = (
        "Pada rangkaian persamaan di atas, simbol $W$ dan $b$ masing-masing menyatakan matriks bobot dan "
        "vektor bias yang dipelajari selama pelatihan, $\\sigma$ menyatakan fungsi aktivasi non-linier sigmoid, "
        "dan simbol $\\odot$ menyatakan operasi perkalian elemen-per-elemen (Hadamard product). Forget gate ($f_t$) "
        "menentukan fraksi memori lama $C_{t-1}$ yang harus dilupakan, input gate ($i_t$) bersama kandidat pembaruan "
        "$\\tilde{C}_t$ mengatur informasi baru yang diserap ke dalam keadaan sel $C_t$, dan output gate ($o_t$) mengontrol "
        "pembentukan vektor keadaan tersembunyi $h_t$ yang diteruskan sebagai keluaran prediksi pada langkah waktu $t$ "
        "(Greff et al., 2017; Goodfellow et al., 2016)."
    )
    add_academic_paragraph(p_b2_desc)

    # 3. Hyperparameter dan Search Space
    p_b3_title = doc.add_paragraph()
    p_b3_title.paragraph_format.space_before = Pt(8)
    p_b3_title.paragraph_format.space_after = Pt(3)
    p_b3_title.paragraph_format.line_spacing = 1.5
    r_b3_t = p_b3_title.add_run("3. Ruang Pencarian Hyperparameter pada Arsitektur LSTM")
    set_font(r_b3_t, "Times New Roman", 12, True, False)

    p_b3_1 = (
        "Hyperparameter merupakan parameter konfigurasi arsitektur dan algoritma yang nilainya ditetapkan secara "
        "eksternal sebelum proses pembelajaran model dimulai, berbeda dengan parameter bobot yang dipelajari secara "
        "internal dari data latih (Goodfellow et al., 2016). Kinerja generalisasi model LSTM sangat sensitif terhadap "
        "kombinasi lima hyperparameter utama: panjang jendela historis (lookback window), jumlah unit neuron tersembunyi "
        "(hidden units), tingkat regulerisasi (dropout rate), laju pembelajaran (learning rate), dan ukuran batch pelatihan "
        "(batch size) (Feurer & Hutter, 2019; Sakarya University, 2023). Panjang lookback window menentukan seberapa jauh horizon "
        "data masa lalu yang dianalisis oleh sel memori untuk menghasilkan proyeksi harga satu langkah ke depan (IJEECS, 2023)."
    )
    add_academic_paragraph(p_b3_1)

    p_b3_2 = (
        "Sementara itu, jumlah unit neuron pada hidden layer mengatur kapasitas representasi fitur jaringan, di mana kapasitas "
        "yang terlalu kecil memicu underfitting sedangkan unit yang berlebih menyebabkan overfitting dan pemborosan komputasi. "
        "Guna mencegah terjadinya fenomena overfitting pada data deret waktu, teknik regularisasi Dropout diterapkan dengan "
        "mematikan sebagian koneksi neuron secara acak dengan probabilitas $p$ selama proses iterasi pelatihan (Srivastava et al., 2014). "
        "Adapun laju pembelajaran (learning rate) dan ukuran batch (batch size) mengendalikan kestabilan serta kecepatan konvergensi "
        "algoritma optimizer Adam dalam memperbarui bobot gradien (Kingma & Ba, 2014). Interaksi non-linier antara variabel-variabel ini "
        "membentuk ruang pencarian (search space) multidimensi yang menuntut metode optimasi cerdas otomatis."
    )
    add_academic_paragraph(p_b3_2)

    # 4. Optuna & TPE
    p_b4_title = doc.add_paragraph()
    p_b4_title.paragraph_format.space_before = Pt(8)
    p_b4_title.paragraph_format.space_after = Pt(3)
    p_b4_title.paragraph_format.line_spacing = 1.5
    r_b4_t = p_b4_title.add_run("4. Kerangka Kerja Optuna dan Algoritma Tree-structured Parzen Estimator (TPE)")
    set_font(r_b4_t, "Times New Roman", 12, True, False)

    p_b4_1 = (
        "Optuna merupakan kerangka kerja optimasi hyperparameter generasi baru berbasis paradigma Define-by-Run yang dirancang "
        "oleh Akiba et al. (2019) guna mengatasi inefisiensi ruang pencarian pada model deep learning. Berbeda dari kerangka kerja lama "
        "yang mengharuskan definisi ruang parameter statis secara kaku, Optuna memungkinkan pembentukan ruang parameter secara dinamis "
        "menggunakan struktur kontrol Python standar. Algoritma pencarian probabilistik utama yang diimplementasikan Optuna adalah "
        "Tree-structured Parzen Estimator (TPE), yang tergolong dalam kelas Sequential Model-Based Optimization (SMBO) berbasis "
        "inferensi Bayesian (Bergstra et al., 2011)."
    )
    add_academic_paragraph(p_b4_1)

    p_b4_2 = (
        "Alih-alih memodelkan probabilitas $P(y|x)$ secara langsung menggunakan Gaussian Process yang membutuhkan komputasi kubik "
        "$O(N^3)$, algoritma TPE memodelkan probabilitas kondisional parameter $P(x|y)$ dengan memisahkan riwayat evaluasi konfigurasi "
        "menjadi dua fungsi densitas probabilitas terpisah berdasarkan batas kuantil $\\gamma$ (Bergstra et al., 2011; Falkner et al., 2018):"
    )
    add_academic_paragraph(p_b4_2, space_after=3)

    # Eq 2.7: TPE Conditional Density Model
    eq_tpe_xml = (
        '<m:r><m:t>P(x|y) = </m:t></m:r>'
        '<m:d>'
        '<m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/><m:grow m:val="1"/></m:dPr>'
        '<m:e>'
        '<m:eqArr>'
        '<m:e>'
        '<m:r><m:t>ℓ(x)     apabila  y &lt; y*</m:t></m:r>'
        '</m:e>'
        '<m:e>'
        '<m:r><m:t>g(x)     apabila  y ≥ y*</m:t></m:r>'
        '</m:e>'
        '</m:eqArr>'
        '</m:e>'
        '</m:d>'
    )
    add_omml_equation(eq_tpe_xml, "(2.7)")

    p_b4_3 = (
        "Pada Persamaan (2.7), $\\ell(x)$ merepresentasikan densitas probabilitas dari konfigurasi parameter yang menghasilkan "
        "nilai loss unggul (di bawah ambang $y^*$), sedangkan $g(x)$ merepresentasikan densitas dari konfigurasi berkinerja buruk. "
        "Kandidat konfigurasi hyperparameter berikutnya dipilih dengan memaksimalkan kriteria Expected Improvement (EI), yang "
        "secara matematis setara dengan memaksimalkan rasio densitas $\\ell(x)/g(x)$ melalui Persamaan (2.8) (Bergstra et al., 2011):"
    )
    add_academic_paragraph(p_b4_3, space_after=3)

    # Eq 2.8: Expected Improvement Ratio
    eq_ei_xml = (
        '<m:sSub><m:e><m:r><m:t>EI</m:t></m:r></m:e><m:sub><m:sSup><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sup><m:r><m:t>*</m:t></m:r></m:sup></m:sSup></m:sub></m:sSub>'
        '<m:r><m:t>(x) = </m:t></m:r>'
        '<m:f>'
        '<m:num><m:r><m:t>γ · y* · ℓ(x) - ℓ(x) · ∫ P(y)dy</m:t></m:r></m:num>'
        '<m:den><m:r><m:t>γ · ℓ(x) + (1 - γ) · g(x)</m:t></m:r></m:den>'
        '</m:f>'
        '<m:r><m:t> ∝ </m:t></m:r>'
        '<m:sSup>'
        '<m:e>'
        '<m:d>'
        '<m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>'
        '<m:e>'
        '<m:r><m:t>γ + </m:t></m:r>'
        '<m:f><m:num><m:r><m:t>g(x)</m:t></m:r></m:num><m:den><m:r><m:t>ℓ(x)</m:t></m:r></m:den></m:f>'
        '<m:r><m:t> · (1 - γ)</m:t></m:r>'
        '</m:e>'
        '</m:d>'
        '</m:e>'
        '<m:sup><m:r><m:t>-1</m:t></m:r></m:sup>'
        '</m:sSup>'
    )
    add_omml_equation(eq_ei_xml, "(2.8)")

    p_b4_4 = (
        "Mekanisme rasio densitas ini menjamin bahwa Optuna secara aktif mengeksplorasi kandidat parameter yang memiliki "
        "probabilitas tinggi menghasilkan error rendah (meningkatkan $\\ell(x)$) sekaligus menjauhi kandidat yang berulang kali "
        "gagal (menekan $g(x)$). Di samping itu, keunggulan komputasi Optuna diperkuat oleh algoritma pemangkasan Asynchronous MedianPruner, "
        "yang membandingkan nilai loss parsial model pada langkah epoch berjalan terhadap nilai median riwayat uji coba terdahulu "
        "dan secara otomatis memutus uji coba yang tidak menjanjikan sebelum mencapai epoch maksimum (Akiba et al., 2019; Li et al., 2017)."
    )
    add_academic_paragraph(p_b4_4)

    # 5. Validasi Deret Waktu Anti-Leakage
    p_b5_title = doc.add_paragraph()
    p_b5_title.paragraph_format.space_before = Pt(8)
    p_b5_title.paragraph_format.space_after = Pt(3)
    p_b5_title.paragraph_format.line_spacing = 1.5
    r_b5_t = p_b5_title.add_run("5. Skema Validasi Deret Waktu (Time-Series Split / Walk-Forward)")
    set_font(r_b5_t, "Times New Roman", 12, True, False)

    p_b5_1 = (
        "Penerapan validasi silang konvensional seperti k-Fold Cross-Validation yang mengacak urutan observasi merupakan "
        "kesalahan fatal pada data deret waktu karena merusak struktur dependensi autokorelasi temporal dan memicu kebocoran "
        "informasi masa depan ke masa lalu (temporal data leakage) (Arlot & Celisse, 2010; López de Prado, 2018). Untuk mencegah "
        "kebocoran data tersebut, prosedur validasi baku yang wajib digunakan adalah Time-Series Split (dikenal pula sebagai "
        "Walk-Forward Validation atau Expanding Window) (Tashman, 2000; BRIN & Binus, 2025). Pada skema ini, pelatihan model "
        "dibatasi hanya pada jendela historis $t \\in [1, T]$, sedangkan evaluasi performa dilakukan secara murni pada jendela waktu "
        "sesudahnya $t \\in [T+1, T+k]$ tanpa pernah menyentuh data masa depan dalam proses pelatihan."
    )
    add_academic_paragraph(p_b5_1)

    # 6. Metrik Evaluasi
    p_b6_title = doc.add_paragraph()
    p_b6_title.paragraph_format.space_before = Pt(8)
    p_b6_title.paragraph_format.space_after = Pt(3)
    p_b6_title.paragraph_format.line_spacing = 1.5
    r_b6_t = p_b6_title.add_run("6. Metrik Evaluasi Kinerja Peramalan Komputasi")
    set_font(r_b6_t, "Times New Roman", 12, True, False)

    p_b6_1 = (
        "Evaluasi kinerja model peramalan deret waktu dilakukan secara kuantitatif melalui pengukuran selisih deviasi antara "
        "nilai aktual penutupan Bitcoin ($y_t$) dan nilai hasil prediksi model ($\\hat{y}_t$) untuk total $n$ observasi pada periode "
        "pengujian out-of-sample. Tiga metrik standar peramalan komputasi yang digunakan dalam penelitian ini adalah Root Mean "
        "Square Error (RMSE), Mean Absolute Error (MAE), dan Mean Absolute Percentage Error (MAPE), yang diformulasikan secara formal "
        "melalui Persamaan (2.9) hingga Persamaan (2.11) sebagai berikut (Hyndman & Athanasopoulos, 2018; Willmott & Matsuura, 2005):"
    )
    add_academic_paragraph(p_b6_1, space_after=3)

    # Eq 2.9: RMSE (Native OMML)
    eq_rmse_xml = (
        '<m:r><m:t>RMSE = </m:t></m:r>'
        '<m:rad>'
        '<m:radPr><m:degHide m:val="1"/></m:radPr>'
        '<m:deg/>'
        '<m:e>'
        '<m:f>'
        '<m:num><m:r><m:t>1</m:t></m:r></m:num>'
        '<m:den><m:r><m:t>n</m:t></m:r></m:den>'
        '</m:f>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:grow m:val="1"/></m:naryPr>'
        '<m:sub><m:r><m:t>t=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>n</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:sSup>'
        '<m:e>'
        '<m:d>'
        '<m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>'
        '<m:e>'
        '<m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:acc>'
        '<m:accPr><m:chr m:val="^"/></m:accPr>'
        '<m:e><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e>'
        '</m:acc>'
        '</m:e>'
        '</m:d>'
        '</m:e>'
        '<m:sup><m:r><m:t>2</m:t></m:r></m:sup>'
        '</m:sSup>'
        '</m:e>'
        '</m:nary>'
        '</m:e>'
        '</m:rad>'
    )
    add_omml_equation(eq_rmse_xml, "(2.9)")

    # Eq 2.10: MAE (Native OMML)
    eq_mae_xml = (
        '<m:r><m:t>MAE = </m:t></m:r>'
        '<m:f>'
        '<m:num><m:r><m:t>1</m:t></m:r></m:num>'
        '<m:den><m:r><m:t>n</m:t></m:r></m:den>'
        '</m:f>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:grow m:val="1"/></m:naryPr>'
        '<m:sub><m:r><m:t>t=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>n</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:d>'
        '<m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr>'
        '<m:e>'
        '<m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:acc>'
        '<m:accPr><m:chr m:val="^"/></m:accPr>'
        '<m:e><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e>'
        '</m:acc>'
        '</m:e>'
        '</m:d>'
        '</m:e>'
        '</m:nary>'
    )
    add_omml_equation(eq_mae_xml, "(2.10)")

    # Eq 2.11: MAPE (Native OMML)
    eq_mape_xml = (
        '<m:r><m:t>MAPE = </m:t></m:r>'
        '<m:f>'
        '<m:num><m:r><m:t>100%</m:t></m:r></m:num>'
        '<m:den><m:r><m:t>n</m:t></m:r></m:den>'
        '</m:f>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:grow m:val="1"/></m:naryPr>'
        '<m:sub><m:r><m:t>t=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>n</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:d>'
        '<m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr>'
        '<m:e>'
        '<m:f>'
        '<m:num>'
        '<m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:acc>'
        '<m:accPr><m:chr m:val="^"/></m:accPr>'
        '<m:e><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:e>'
        '</m:acc>'
        '</m:num>'
        '<m:den>'
        '<m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>'
        '</m:den>'
        '</m:f>'
        '</m:e>'
        '</m:d>'
        '</m:e>'
        '</m:nary>'
    )
    add_omml_equation(eq_mape_xml, "(2.11)")

    p_b6_desc = (
        "Metrik RMSE memberikan penalti kuadratik yang lebih berat terhadap deviasi kesalahan bernilai besar, "
        "sehingga sangat sensitif dalam mendeteksi adanya kegagalan peramalan ekstrem (outlier errors). Sebaliknya, "
        "metrik MAE mengukur nilai absolut kesalahan secara proporsional dan tidak memperbesar bobot outlier, mencerminkan "
        "deviasi magnitudo harga riil secara stabil (Willmott & Matsuura, 2005). Sementara itu, metrik MAPE menormalisasi "
        "kesalahan ke dalam skala persentase relatif terhadap harga aktual, memberikan kemudahan interpretasi akurasi "
        "ketika diuji pada periode harga Bitcoin yang mengalami eskalasi nilai yang sangat masif (Hyndman & Athanasopoulos, 2018)."
    )
    add_academic_paragraph(p_b6_desc)

    # =========================================================================
    # C. KERANGKA BERPIKIR PENELITIAN
    # =========================================================================
    p_subC = doc.add_paragraph()
    p_subC.paragraph_format.space_before = Pt(14)
    p_subC.paragraph_format.space_after = Pt(6)
    p_subC.paragraph_format.line_spacing = 1.5
    r_subC = p_subC.add_run("C. Kerangka Berpikir Penelitian")
    set_font(r_subC, "Times New Roman", 12, True, False)

    p_c1 = (
        "Kerangka berpikir penelitian ini dibangun berdasarkan penalaran komputasi terstruktur guna memecahkan kesenjangan "
        "antara karakteristik non-stasioneritas data Bitcoin dengan keterbatasan metode peramalan yang telah ada sebelumnya. "
        "Alur logis keterkaitan antarvariabel dan tahapan metodologis penyelesaian masalah dirumuskan secara sistematis "
        "sebagai berikut:"
    )
    add_academic_paragraph(p_c1)

    framework_steps = [
        ("1. Identifikasi Masalah (Problem Identification)", "Data deret waktu harga Bitcoin memiliki non-stasioneritas ekstrem dan pergeseran rezim tren pasar. Penyetelan parameter model deep learning LSTM selama ini masih mengandalkan penyesuaian manual (trial-and-error) yang terbatas dan rawan local minima (Khumaidi dkk., 2024), sedangkan Grid Search menuntut komputasi eksponensial yang tidak terukur (Bit-Tech, 2026). Selain itu, evaluasi berbasis static split menimbulkan biased estimation error (BRIN, 2025)."),
        ("2. Intervensi Metodologis (Methodological Intervention)", "Menerapkan kerangka kerja optimasi otomatis Optuna berbasis algoritma probabilistik Tree-structured Parzen Estimator (TPE) untuk mengeksplorasi ruang pencarian hyperparameter arsitektur dan pelatihan LSTM secara efisien, dipadukan dengan mekanisme pemangkasan Asynchronous MedianPruner."),
        ("3. Protokol Validasi Bebas Kebocoran (Data Validation Scheme)", "Mengintegrasikan proses optimasi dan evaluasi model dengan skema Time-Series Split (Walk-Forward Validation) untuk menjamin parameter yang ditemukan teruji secara murni pada data out-of-sample lintas periode pasar tanpa kebocoran data masa depan (temporal data leakage)."),
        ("4. Pengujian Empiris Bertingkat (3-Tier Benchmark Evaluation)", "Membandingkan performa model dalam tiga tingkat: Tier 1 (LSTM Default), Tier 2 (LSTM Replikasi Manual Khumaidi dkk., 2024), dan Tier 3 (LSTM Teroptimasi Optuna-TPE) menggunakan metrik kuantitatif standar informatika: RMSE, MAE, dan MAPE."),
        ("5. Kontribusi Ilmiah (Expected Scientific Contribution)", "Terbuktinya penurunan nilai error (positive improvement) yang signifikan dan stabil, tersusunnya konfigurasi hyperparameter optimal model LSTM, serta tersedianya kerangka kerja optimasi yang efisien bagi peramalan deret waktu bervolatilitas tinggi.")
    ]

    for title, desc in framework_steps:
        p_f = doc.add_paragraph()
        p_f.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_f.paragraph_format.line_spacing = 1.5
        p_f.paragraph_format.space_after = Pt(4)
        p_f.paragraph_format.left_indent = Cm(0.8)
        p_f.paragraph_format.first_line_indent = Cm(-0.8)
        r_ft = p_f.add_run(f"{title}: ")
        set_font(r_ft, "Times New Roman", 12, True, False)
        r_fd = p_f.add_run(desc)
        set_font(r_fd, "Times New Roman", 12, False, False)

    # =========================================================================
    # D. HIPOTESIS PENELITIAN
    # =========================================================================
    p_subD = doc.add_paragraph()
    p_subD.paragraph_format.space_before = Pt(14)
    p_subD.paragraph_format.space_after = Pt(6)
    p_subD.paragraph_format.line_spacing = 1.5
    r_subD = p_subD.add_run("D. Hipotesis Penelitian")
    set_font(r_subD, "Times New Roman", 12, True, False)

    p_hipo_intro = (
        "Berdasarkan landasan teori, kajian penelitian terdahulu yang komprehensif, serta kerangka berpikir penelitian, "
        "maka hipotesis penelitian dirumuskan secara terarah guna menjawab rumusan masalah sebagai berikut:"
    )
    add_academic_paragraph(p_hipo_intro, space_after=4)

    hipotesis_items = [
        ("H1", "Algoritma Optuna berbasis Tree-structured Parzen Estimator (TPE) mampu mengidentifikasi konfigurasi hyperparameter optimal model Long Short-Term Memory (LSTM) secara konvergen dan terarah pada ruang pencarian multidimensi."),
        ("H2", "Model Long Short-Term Memory (LSTM) yang dioptimasi menggunakan algoritma Optuna-TPE menghasilkan penurunan nilai error (positive improvement) yang signifikan pada metrik Root Mean Square Error (RMSE), Mean Absolute Error (MAE), dan Mean Absolute Percentage Error (MAPE) dibandingkan dengan model baseline berkonfigurasi default maupun manual tuning."),
        ("H3", "Konfigurasi hyperparameter model LSTM hasil optimasi algoritma Optuna mampu mempertahankan stabilitas akurasi prediksi secara konsisten ketika dievaluasi pada berbagai pengujian data deret waktu out-of-sample melintasi berbagai fase volatilitas pasar.")
    ]

    for code, item in hipotesis_items:
        p_h = doc.add_paragraph()
        p_h.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_h.paragraph_format.line_spacing = 1.5
        p_h.paragraph_format.space_after = Pt(4)
        p_h.paragraph_format.left_indent = Cm(1.0)
        p_h.paragraph_format.first_line_indent = Cm(-0.6)
        r_hc = p_h.add_run(f"{code}: ")
        set_font(r_hc, "Times New Roman", 12, True, False)
        r_ht = p_h.add_run(item)
        set_font(r_ht, "Times New Roman", 12, False, False)

    # Save to 03_Naskah_Skripsi
    out_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "03_Naskah_Skripsi")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BAB_2_LANDASAN_TEORI_ZAINI_LEON.docx")
    doc.save(out_path)
    print(f"Successfully generated enhanced Bab 2: {out_path}")

if __name__ == "__main__":
    generate_enhanced_bab2()
