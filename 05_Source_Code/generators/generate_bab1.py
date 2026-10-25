import docx
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_bab1_document():
    doc = docx.Document()

    # 1. Page Setup according to UNISNU Guidelines
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(4.0)
    section.left_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    # Helper function for setting run font
    def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic

    # Helper function for adding paragraphs with UNISNU style
    def add_academic_paragraph(text, space_after=6, line_spacing=1.5, first_line_indent=Cm(1.0)):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_after = Pt(space_after)
        if first_line_indent:
            p.paragraph_format.first_line_indent = first_line_indent
        run = p.add_run(text)
        set_font(run, "Times New Roman", 12, False, False)
        return p

    # --- JUDUL BAB ---
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_before = Pt(0)
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    r_chap = p_chap.add_run("BAB I\nPENDAHULUAN")
    set_font(r_chap, "Times New Roman", 14, True, False)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(12)

    # ==========================================
    # A. LATAR BELAKANG MASALAH
    # ==========================================
    p_subA = doc.add_paragraph()
    p_subA.paragraph_format.space_before = Pt(12)
    p_subA.paragraph_format.space_after = Pt(6)
    p_subA.paragraph_format.line_spacing = 1.5
    r_subA = p_subA.add_run("A. Latar Belakang Masalah")
    set_font(r_subA, "Times New Roman", 12, True, False)

    # Paragraf 1: Konteks Time Series & Fluktuasi Bitcoin (SPECH)
    p1 = (
        "Perkembangan teknologi finansial berbasis komputasi terdesentralisasi telah menempatkan Bitcoin "
        "sebagai aset digital dengan volume transaksi dan kapitalisasi pasar terbesar di dunia. Karakteristik "
        "data deret waktu (time series) Bitcoin memperlihatkan tingkat volatilitas ekstrem serta non-stasioneritas "
        "yang sangat dinamis akibat dipengaruhi oleh likuiditas global dan sentimen pasar (Lim & Zohren, 2021; "
        "Aswadi & Ependi, 2022). Fluktuasi nilai tukar yang bergerak secara cepat dan tidak berpola linier "
        "tersebut menimbulkan tantangan komputasi yang rumit dalam bidang rekayasa kecerdasan buatan. "
        "Metode analisis statistik parametrik klasik seperti Autoregressive Integrated Moving Average (ARIMA) "
        "kerap mengalami degradasi performa karena ketidakmampuannya menangkap interaksi ketergantungan temporal "
        "jangka panjang yang kompleks. Keterbatasan pemodelan linier konvensional tersebut mendorong urgensi "
        "pemanfaatan paradigma pembelajaran mendalam (deep learning) yang adaptif terhadap dependensi sekuensial data."
    )
    add_academic_paragraph(p1)

    # Paragraf 2: Arsitektur LSTM & Keunggulannya (SPECH)
    p2 = (
        "Dalam domain pembelajaran mendalam untuk peramalan deret waktu, arsitektur Recurrent Neural Network (RNN) "
        "varian Long Short-Term Memory (LSTM) telah menjadi metode rujukan utama dalam memodelkan data sekuensial. "
        "Arsitektur LSTM yang diperkenalkan oleh Hochreiter & Schmidhuber (1997) dan dikaji lebih lanjut oleh "
        "Greff et al. (2017) dirancang secara spesifik untuk memecahkan permasalahan hilangnya gradien "
        "(vanishing gradient) yang melekat pada jaringan saraf berulang tradisional. Melalui integrasi tiga "
        "gerbang logika utama—input gate, forget gate, dan output gate—serta cell state internal, LSTM mampu "
        "mengatur retensi dan pembaruan informasi temporal secara selektif. Keunggulan struktural ini memungkinkan "
        "model mempertahankan memori historis penting melintasi rentang waktu yang panjang jauh melampaui algoritma "
        "machine learning standar (Ula et al., 2024). Kendati demikian, efektivitas representasi fitur dan akurasi "
        "prediksi LSTM sangat bergantung pada ketepatan konfigurasi hyperparameter yang diterapkan."
    )
    add_academic_paragraph(p2)

    # Paragraf 3: Masalah Search Space & Kelemahan Manual Tuning (SPECH)
    p3 = (
        "Penentuan konfigurasi parameter optimal pada model jaringan saraf tiruan mendalam melibatkan ruang "
        "pencarian (search space) multidimensi yang bersifat non-konveks dan saling berinteraksi secara rumit. "
        "Parameter arsitektur seperti panjang jendela historis (lookback window), jumlah neuron tersembunyi, "
        "dropout rate, serta parameter pelatihan seperti learning rate dan batch size memiliki sensitivitas "
        "sangat tinggi terhadap performa konvergensi model (Goodfellow et al., 2016; Sakarya University, 2023). "
        "Pada praktiknya, sejumlah kajian peramalan Bitcoin, seperti riset yang dipublikasikan oleh Khumaidi dkk. "
        "(2024) pada jurnal terakreditasi SINTA 2, masih mengandalkan penyesuaian parameter secara manual "
        "(trial-and-error) dengan kombinasi nilai yang sangat terbatas. Pendekatan manual ini terbukti tidak efisien, "
        "memerlukan intervensi subjektif, serta memiliki probabilitas tinggi terjebak pada titik optimum lokal "
        "(local minima) yang suboptimal. Kelemahan proses manual tersebut menuntut diterapkannya metode pencarian "
        "parameter otomatis yang terstruktur secara algoritmik."
    )
    add_academic_paragraph(p3)

    # Paragraf 4: Kelemahan Grid Search & Random Search (SPECH)
    p4 = (
        "Metode pencarian hyperparameter otomatis konvensional yang kerap digunakan pada penelitian informatika "
        "meliputi Grid Search dan Random Search. Studi komprehensif oleh Feurer & Hutter (2019) serta evaluasi empiris "
        "terkini pada instrumen aset kripto (JUTIF, 2026) mengungkapkan bahwa Grid Search menuntut biaya komputasi "
        "yang sangat mahal secara eksponensial seiring bertambahnya dimensi parameter yang diuji. Di sisi lain, "
        "meskipun Random Search menawarkan efisiensi waktu yang lebih baik, algoritma ini mengevaluasi parameter "
        "secara acak tanpa memanfaatkan riwayat informasi keberhasilan iterasi sebelumnya. Akibatnya, pada data deret "
        "waktu dengan tingkat derau (noise) tinggi, Random Search menghasilkan variansi performa yang tidak konsisten "
        "dan kerap berkinerja buruk (JUTIF, 2026). Oleh sebab itu, diperlukan algoritma optimasi cerdas berbasis "
        "probabilistik yang mampu memandu arah pencarian parameter secara terarah dan hemat sumber daya komputasi."
    )
    add_academic_paragraph(p4)

    # Paragraf 5: Keunggulan Algoritma Optuna TPE (SPECH)
    p5 = (
        "Kerangka kerja optimasi modern Optuna hadir memberikan solusi mutakhir terhadap inefisiensi eksplorasi "
        "ruang parameter pada model pembelajaran mendalam. Dikembangkan oleh Akiba et al. (2019), Optuna "
        "mengimplementasikan algoritma Bayesian Optimization berbasis Tree-structured Parzen Estimator (TPE) "
        "yang memodelkan fungsi objektif secara probabilistik (Bergstra et al., 2011). Pendekatan TPE mengelompokkan "
        "riwayat evaluasi konfigurasi parameter menjadi dua distribusi probabilitas kontinu guna menghitung kriteria "
        "Expected Improvement secara adaptif pada setiap langkah uji. Selain itu, fitur pemangkasan otomatis "
        "(Asynchronous MedianPruner) pada Optuna mampu menghentikan uji coba kandidat parameter yang berkinerja "
        "buruk secara dini sebelum proses pelatihan selesai (Falkner et al., 2018; Li et al., 2017). Namun demikian, "
        "keandalan konfigurasi parameter yang ditemukan oleh Optuna sangat dipengaruhi oleh integritas skema validasi data."
    )
    add_academic_paragraph(p5)

    # Paragraf 6: Masalah Validasi Statis & Solusi Walk-Forward (SPECH)
    p6 = (
        "Prosedur pembagian data statis (static train-test split) yang umum diterapkan pada penelitian deret waktu "
        "memiliki kelemahan metodologis yang berpotensi menghasilkan kesimpulan semu. Riset mutakhir oleh BRIN "
        "(Journal of Open Innovation, 2025) menegaskan bahwa optimasi parameter deret waktu finansial yang hanya "
        "bertumpu pada potongan data statis menimbulkan bias estimasi serta kebocoran informasi masa depan "
        "(temporal data leakage). Pada instrumen Bitcoin yang kerap mengalami pergeseran rezim tren (regime shift), "
        "parameter yang tampak prima pada data latih statis sering kali mengalami degradasi drastis saat diuji pada "
        "fase pasar berikutnya (López de Prado, 2018). Untuk menjamin ketahanan model, penerapan skema validasi deret "
        "waktu berurutan (Time-Series Split / Walk-Forward) menjadi esensial guna mengevaluasi generalisasi model secara "
        "murni pada data out-of-sample (Tashman, 2000; Arlot & Celisse, 2010). Penggabungan algoritma Optuna-TPE dengan "
        "protokol validasi deret waktu menjadi celah riset utama yang sangat mendesak untuk dituntaskan."
    )
    add_academic_paragraph(p6)

    # Paragraf 7: Research Gap & 3-Tier Benchmark (SPECH)
    p7 = (
        "Kesenjangan penelitian (research gap) ini ditempatkan pada rekayasa optimasi hyperparameter otomatis "
        "multi-dimensi model LSTM dengan menerapkan protokol validasi deret waktu yang ketat bebas kebocoran data. "
        "Kajian terdahulu telah meneliti optimasi LSTM pada aset digital alternatif (JUTIF, 2026) dan penyetelan manual "
        "pada Bitcoin (Khumaidi dkk., 2024), namun belum mengintegrasikan pencarian parameter terarah Optuna-TPE "
        "berbasis time-series split. Penelitian ini merancang ruang pencarian gabungan yang mencakup parameter arsitektur "
        "(lookback window, unit LSTM layer, dropout) dan pelatihan (learning rate, optimizer, batch size) secara terpadu. "
        "Guna menjamin kontribusi positif yang objektif, pengujian empiris dirancang secara bertingkat (3-Tier Benchmark) "
        "membandingkan model LSTM default, model replikasi manual, dan model teroptimasi Optuna-TPE. Evaluasi akurasi "
        "diukur melalui tiga metrik standar informatika: RMSE, MAE, dan MAPE (Hyndman & Athanasopoulos, 2018; Willmott & Matsuura, 2005)."
    )
    add_academic_paragraph(p7)

    # Paragraf 8: Urgensi & Pernyataan Judul (SPECH)
    p8 = (
        "Implementasi kerangka kerja optimasi ini memberikan kontribusi nyata dalam memajukan metodologi "
        "rekayasa kecerdasan buatan pada peramalan deret waktu bervolatilitas tinggi. Pemanfaatan data historis "
        "harga penutupan Bitcoin (BTC/USDT) yang bersumber langsung dari bursa resmi Binance API (2024) menyediakan "
        "dasar empiris yang objektif dan transparan. Melalui optimasi terarah berbasis Optuna-TPE, proses penentuan "
        "arsitektur jaringan saraf tidak lagi didasarkan pada intuisi coba-coba manusia yang memakan waktu, melainkan "
        "berpijak pada pemodelan matematis probabilistik yang dapat dipertanggungjawabkan. Hasil pengujian ini diharapkan "
        "membuktikan adanya penurunan nilai error yang signifikan dan konsisten melintasi berbagai periode pasar out-of-sample. "
        "Berdasarkan seluruh latar belakang dan urgensi ilmiah tersebut, penelitian ini dilaksanakan dengan judul "
        "\"Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin\"."
    )
    add_academic_paragraph(p8)

    # ==========================================
    # B. RUMUSAN MASALAH
    # ==========================================
    p_subB = doc.add_paragraph()
    p_subB.paragraph_format.space_before = Pt(14)
    p_subB.paragraph_format.space_after = Pt(6)
    p_subB.paragraph_format.line_spacing = 1.5
    r_subB = p_subB.add_run("B. Rumusan Masalah")
    set_font(r_subB, "Times New Roman", 12, True, False)

    p_rm_intro = (
        "Berdasarkan latar belakang masalah yang telah diuraikan, rumusan masalah dalam penelitian ini "
        "disusun secara berjenjang tanpa adanya duplikasi kata tanya sebagai berikut:"
    )
    add_academic_paragraph(p_rm_intro, space_after=4)

    rumusan_masalah_items = [
        "Bagaimana proses penentuan arsitektur dan konfigurasi hyperparameter optimal pada model Long Short-Term Memory (LSTM) menggunakan algoritma Optuna berbasis Tree-structured Parzen Estimator (TPE)?",
        "Berapa persentase penurunan nilai error (RMSE, MAE, dan MAPE) yang berhasil dicapai oleh model LSTM teroptimasi Optuna dibandingkan dengan model baseline berkonfigurasi default maupun manual tuning?",
        "Apakah konfigurasi hyperparameter hasil optimasi algoritma Optuna mampu mempertahankan stabilitas akurasi prediksi secara konsisten ketika dievaluasi pada berbagai pengujian data deret waktu out-of-sample?"
    ]

    for idx, item in enumerate(rumusan_masalah_items, 1):
        p_item = doc.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_item.paragraph_format.line_spacing = 1.5
        p_item.paragraph_format.space_after = Pt(4)
        p_item.paragraph_format.left_indent = Cm(1.0)
        p_item.paragraph_format.first_line_indent = Cm(-0.6)
        r_num = p_item.add_run(f"{idx}. ")
        set_font(r_num, "Times New Roman", 12, True, False)
        r_txt = p_item.add_run(item)
        set_font(r_txt, "Times New Roman", 12, False, False)

    # ==========================================
    # C. TUJUAN PENELITIAN
    # ==========================================
    p_subC = doc.add_paragraph()
    p_subC.paragraph_format.space_before = Pt(14)
    p_subC.paragraph_format.space_after = Pt(6)
    p_subC.paragraph_format.line_spacing = 1.5
    r_subC = p_subC.add_run("C. Tujuan Penelitian")
    set_font(r_subC, "Times New Roman", 12, True, False)

    p_tp_intro = (
        "Mengacu secara selaras kepada rumusan masalah yang diajukan, tujuan yang hendak dicapai "
        "melalui pelaksanaan penelitian ini adalah:"
    )
    add_academic_paragraph(p_tp_intro, space_after=4)

    tujuan_items = [
        "Menganalisis dan mengimplementasikan proses pencarian konfigurasi hyperparameter optimal pada model Long Short-Term Memory (LSTM) secara otomatis menggunakan kerangka kerja Optuna berbasis Tree-structured Parzen Estimator (TPE).",
        "Mengukur dan membandingkan secara kuantitatif besaran penurunan nilai error (Root Mean Square Error, Mean Absolute Error, dan Mean Absolute Percentage Error) yang dihasilkan oleh model LSTM teroptimasi Optuna terhadap model baseline default dan manual tuning.",
        "Mengevaluasi dan membuktikan tingkat ketahanan generalisasi model LSTM hasil optimasi Optuna ketika diuji melintasi berbagai periode data deret waktu finansial out-of-sample menggunakan skema Time-Series Split."
    ]

    for idx, item in enumerate(tujuan_items, 1):
        p_item = doc.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_item.paragraph_format.line_spacing = 1.5
        p_item.paragraph_format.space_after = Pt(4)
        p_item.paragraph_format.left_indent = Cm(1.0)
        p_item.paragraph_format.first_line_indent = Cm(-0.6)
        r_num = p_item.add_run(f"{idx}. ")
        set_font(r_num, "Times New Roman", 12, True, False)
        r_txt = p_item.add_run(item)
        set_font(r_txt, "Times New Roman", 12, False, False)

    # ==========================================
    # D. MANFAAT PENELITIAN
    # ==========================================
    p_subD = doc.add_paragraph()
    p_subD.paragraph_format.space_before = Pt(14)
    p_subD.paragraph_format.space_after = Pt(6)
    p_subD.paragraph_format.line_spacing = 1.5
    r_subD = p_subD.add_run("D. Manfaat Penelitian")
    set_font(r_subD, "Times New Roman", 12, True, False)

    p_manfaat_intro = (
        "Hasil dari penelitian ini diharapkan dapat memberikan kontribusi nyata yang bermanfaat "
        "baik secara teoretis bagi perkembangan keilmuan informatika maupun secara praktis bagi para praktisi:"
    )
    add_academic_paragraph(p_manfaat_intro, space_after=4)

    # 1. Manfaat Teoretis
    p_mt_title = doc.add_paragraph()
    p_mt_title.paragraph_format.left_indent = Cm(0.6)
    p_mt_title.paragraph_format.space_after = Pt(2)
    p_mt_title.paragraph_format.line_spacing = 1.5
    r_mt_num = p_mt_title.add_run("1. Manfaat Teoretis")
    set_font(r_mt_num, "Times New Roman", 12, True, False)

    p_mt_desc = (
        "Secara teoretis, penelitian ini memberikan sumbangan literatur ilmiah dalam domain rekayasa kecerdasan "
        "buatan (artificial intelligence) dan pembelajaran mendalam (deep learning), khususnya mengenai integrasi "
        "algoritma optimasi Bayesian berbasis Tree-structured Parzen Estimator (TPE) pada arsitektur Long Short-Term "
        "Memory (LSTM). Penelitian ini memperkaya khazanah metodologi peramalan data deret waktu bervolatilitas tinggi "
        "melalui pembuktian empiris bahwa proses optimasi otomatis dengan protokol validasi terstruktur mampu "
        "menghilangkan bias estimasi parameter model."
    )
    p_mt_p = doc.add_paragraph()
    p_mt_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_mt_p.paragraph_format.left_indent = Cm(0.6)
    p_mt_p.paragraph_format.first_line_indent = Cm(0.6)
    p_mt_p.paragraph_format.line_spacing = 1.5
    p_mt_p.paragraph_format.space_after = Pt(6)
    r_mt_txt = p_mt_p.add_run(p_mt_desc)
    set_font(r_mt_txt, "Times New Roman", 12, False, False)

    # 2. Manfaat Praktis
    p_mp_title = doc.add_paragraph()
    p_mp_title.paragraph_format.left_indent = Cm(0.6)
    p_mp_title.paragraph_format.space_after = Pt(2)
    p_mp_title.paragraph_format.line_spacing = 1.5
    r_mp_num = p_mp_title.add_run("2. Manfaat Praktis")
    set_font(r_mp_num, "Times New Roman", 12, True, False)

    manfaat_praktis_items = [
        ("Bagi Peneliti dan Akademisi", "Memberikan panduan kerangka kerja eksperimental yang teruji dalam menerapkan kerangka kerja Optuna untuk tuning model jaringan saraf berulang pada data deret waktu yang kompleks."),
        ("Bagi Praktisi Teknologi dan Analis Komputasi", "Menyediakan rujukan arsitektur model peramalan otomatis yang efisien dalam penggunaan sumber daya komputasi melalui fitur early pruning, sehingga dapat diterapkan pada sistem analitik data skala besar."),
        ("Bagi Program Studi Teknik Informatika UNISNU Jepara", "Menambah koleksi karya ilmiah tugas akhir yang berbobot, bereputasi tinggi, dan menerapkan metode kecerdasan buatan mutakhir yang relevan dengan perkembangan industri teknologi informasi global.")
    ]

    for label, desc in manfaat_praktis_items:
        p_mp_item = doc.add_paragraph()
        p_mp_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_mp_item.paragraph_format.left_indent = Cm(1.2)
        p_mp_item.paragraph_format.first_line_indent = Cm(-0.6)
        p_mp_item.paragraph_format.line_spacing = 1.5
        p_mp_item.paragraph_format.space_after = Pt(3)
        r_lbl = p_mp_item.add_run(f"a. {label}: ") if label.startswith("Bagi Peneliti") else (
            p_mp_item.add_run(f"b. {label}: ") if label.startswith("Bagi Praktisi") else p_mp_item.add_run(f"c. {label}: ")
        )
        set_font(r_lbl, "Times New Roman", 12, True, False)
        r_dsc = p_mp_item.add_run(desc)
        set_font(r_dsc, "Times New Roman", 12, False, False)

    # ==========================================
    # E. BATASAN MASALAH
    # ==========================================
    p_subE = doc.add_paragraph()
    p_subE.paragraph_format.space_before = Pt(14)
    p_subE.paragraph_format.space_after = Pt(6)
    p_subE.paragraph_format.line_spacing = 1.5
    r_subE = p_subE.add_run("E. Batasan Masalah")
    set_font(r_subE, "Times New Roman", 12, True, False)

    p_bm_intro = (
        "Agar pelaksanaan penelitian ini berjalan secara terarah, terukur, dan fokus pada ruang lingkup "
        "keilmuan Teknik Informatika, maka batasan masalah ditetapkan sebagai berikut:"
    )
    add_academic_paragraph(p_bm_intro, space_after=4)

    batasan_items = [
        "Data penelitian yang digunakan adalah data historis harga penutupan harian (daily closing price) cryptocurrency pasangan Bitcoin terhadap Tether (BTC/USDT) yang dihimpun dari platform Binance Public API.",
        "Periode rentang waktu dataset mencakup rentang multi-tahun (2020 hingga 2024) guna merepresentasikan variasi kondisi pasar yang komprehensif, meliputi fase tren bullish, bearish, dan konsolidasi pasar.",
        "Model pembelajaran mendalam (deep learning) yang diuji dan dioptimasi dibatasi secara khusus pada arsitektur Long Short-Term Memory (LSTM) berbasis input deret waktu univariat harga penutupan.",
        "Algoritma optimasi hyperparameter yang diterapkan adalah Tree-structured Parzen Estimator (TPE) yang dijalankan melalui kerangka kerja Optuna dengan mekanisme pemangkasan otomatis Asynchronous MedianPruner.",
        "Ruang pencarian (search space) hyperparameter yang dioptimasi difokuskan pada lima variabel komputasi utama, yaitu: panjang jendela historis (lookback window), jumlah unit neuron tersembunyi (hidden units), tingkat regulerisasi (dropout rate), laju pembelajaran (learning rate), dan ukuran batch pelatihan (batch size).",
        "Skema evaluasi dan validasi data menggunakan metode Time-Series Split (Walk-Forward Validation) berurutan untuk menjamin pengujian bebas dari kebocoran data masa depan (temporal data leakage).",
        "Metrik evaluasi performa akurasi dan kesalahan komputasi model dibatasi pada tiga indikator standar peramalan, yaitu Root Mean Square Error (RMSE), Mean Absolute Error (MAE), dan Mean Absolute Percentage Error (MAPE)."
    ]

    for idx, item in enumerate(batasan_items, 1):
        p_item = doc.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_item.paragraph_format.line_spacing = 1.5
        p_item.paragraph_format.space_after = Pt(4)
        p_item.paragraph_format.left_indent = Cm(1.0)
        p_item.paragraph_format.first_line_indent = Cm(-0.6)
        r_num = p_item.add_run(f"{idx}. ")
        set_font(r_num, "Times New Roman", 12, True, False)
        r_txt = p_item.add_run(item)
        set_font(r_txt, "Times New Roman", 12, False, False)

    # Save document
    filename = "BAB_1_PENDAHULUAN_ZAINI_LEON.docx"
    doc.save(filename)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    create_bab1_document()
