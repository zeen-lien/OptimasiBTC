import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_proposal():
    doc = docx.Document('file contoh pengajuan judul.docx')
    t1 = doc.tables[0]

    # Ensure row 5 has 3 cells
    r5 = t1.rows[5]
    if len(r5.cells) < 3:
        new_tc = parse_xml(f'<w:tc {nsdecls("w")}><w:tcPr><w:tcW w:w="5255" w:type="dxa"/></w:tcPr><w:p/></w:tc>')
        r5._tr.append(new_tc)

    # 1. Judul Penelitian (Row 2, Cell 2)
    judul = "Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin"
    cell_judul = t1.rows[2].cells[2]
    cell_judul.text = ""
    p_judul = cell_judul.paragraphs[0]
    p_judul.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_j = p_judul.add_run(judul)
    r_j.font.name = "Times New Roman"
    r_j.font.size = Pt(12)
    r_j.font.bold = True

    # 2. Latar Belakang (Row 3, Cell 2)
    latar_belakang_paragraphs = [
        "Bitcoin merupakan aset kripto dengan tingkat kapitalisasi pasar terbesar di dunia yang menghasilkan data deret waktu (time series) dengan fluktuasi dan non-stasioneritas sangat tinggi. Karakteristik pergerakan harga Bitcoin dipengaruhi oleh dinamika pasar yang kompleks dan pergeseran tren temporal (regime shift), sehingga metode peramalan statistik linier konvensional kerap mengalami keterbatasan dalam menangkap keterkaitan non-linier data. Dalam bidang keilmuan Teknik Informatika dan Machine Learning, pemodelan Deep Learning khususnya arsitektur Recurrent Neural Network (RNN) varian Long Short-Term Memory (LSTM) menjadi pendekatan yang dominan. LSTM dirancang secara khusus untuk mengatasi permasalahan vanishing gradient melalui mekanisme gerbang logika (input, forget, dan output gate), memungkinkannya mempertahankan memori jangka panjang atas pola historis deret waktu.",

        "Meskipun model LSTM memiliki kapasitas representasi fitur deret waktu yang kuat, akurasi peramalannya sangat sensitif dan bergantung pada pemilihan konfigurasi hyperparameter. Parameter arsitektur dan proses pelatihan seperti lookback window (panjang jendela historis), jumlah neuron pada hidden layer, dropout rate (regulerisasi pencegah overfitting), learning rate (kecepatan konvergensi optimasi), dan batch size membentuk ruang pencarian (search space) multidimensi yang saling berinteraksi secara kompleks. Penelitian terdahulu oleh Khumaidi dkk. (2024) yang diterbitkan pada ILKOM Jurnal Ilmiah (Sinta 2) membuktikan bahwa penyesuaian hyperparameter mampu menekan tingkat error prediksi Bitcoin hingga rata-rata 6,31%. Namun, penelitian tersebut masih mengandalkan penyesuaian parameter secara manual (trial-and-error) pada skenario yang sangat terbatas. Pendekatan manual ini tidak efisien, memerlukan waktu komputasi yang tidak terukur, serta berisiko tinggi terjebak pada local minima suboptimal.",

        "Di sisi lain, teknik pencarian hyperparameter konvensional seperti Grid Search membutuhkan biaya komputasi yang sangat masif (computationally prohibitive) seiring bertambahnya dimensi parameter, sebagaimana diuraikan dalam studi Bit-Tech (2026). Sementara itu, metode Random Search terbukti menghasilkan performa yang tidak konsisten dan tidak menjamin tercapainya konvergensi optimal pada aset kripto (Jurnal Teknik Informatika - JUTIF, 2026). Untuk menjawab kelemahan tersebut, metode optimasi berbasis Bayesian Optimization dengan algoritma Tree-structured Parzen Estimator (TPE) yang diintegrasikan melalui kerangka kerja Optuna menawarkan efisiensi komputasi yang unggul. Algoritma Optuna-TPE membangun model probabilistik surrogate P(x|y) dari riwayat evaluasi objektif sebelumnya, sehingga pencarian ruang parameter berikutnya difokuskan secara cerdas pada area yang paling berpotensi meminimalkan nilai error fungsi loss.",

        "Kelemahan lain yang sering dijumpai pada riset optimasi deret waktu adalah penggunaan pembagian data statis (static train-test split) yang rentan menimbulkan bias estimasi dan kebocoran informasi (information leakage). Berdasarkan studi mutakhir oleh peneliti BRIN (Journal of Open Innovation, 2025), proses optimasi hyperparameter harus dipadukan dengan skema evaluasi deret waktu yang ketat (Time-Series Split / Walk-Forward Out-of-Sample) agar parameter yang terpilih benar-benar tangguh terhadap pergeseran volatilitas masa depan. Mengacu pada telaah pustaka tersebut, research gap penelitian ini ditempatkan pada rekayasa optimasi otomatis: menguji secara sistematis bagaimana penerapan algoritma Optuna berbasis TPE mampu menemukan konfigurasi hyperparameter optimal pada model LSTM, serta membuktikan bahwa model teroptimasi menghasilkan penurunan error (positive improvement) yang signifikan dibanding konfigurasi baseline (default dan manual tuning).",

        "Penelitian ini memanfaatkan data historis harga penutupan (closing price) Bitcoin (BTC/USDT) yang dihimpun dari bursa Binance. Kinerja model dievaluasi secara kuantitatif melalui tiga metrik standar evaluasi peramalan informatika, yaitu Root Mean Square Error (RMSE), Mean Absolute Error (MAE), dan Mean Absolute Percentage Error (MAPE). Kontribusi nyata yang diharapkan dari penelitian ini adalah tersusunnya kerangka kerja optimasi hyperparameter LSTM yang terstruktur, otomatis, dan terbukti menghasilkan akurasi prediksi yang superior serta tahan terhadap dinamika volatilitas data deret waktu finansial."
    ]

    cell_lb = t1.rows[3].cells[2]
    cell_lb.text = ""
    for idx, p_text in enumerate(latar_belakang_paragraphs):
        p = cell_lb.paragraphs[0] if idx == 0 else cell_lb.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(p_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    # 3. Rumusan Masalah (Row 4, Cell 2) - KATA TANYA TIDAK BOLEH DUPLIKAT!
    # 1. Bagaimana...
    # 2. Berapa...
    # 3. Apakah...
    rumusan_masalah_list = [
        "Bagaimana proses penentuan arsitektur dan konfigurasi hyperparameter optimal pada model Long Short-Term Memory (LSTM) menggunakan algoritma Optuna berbasis Tree-structured Parzen Estimator (TPE)?",
        "Berapa persentase penurunan nilai error (RMSE, MAE, dan MAPE) yang berhasil dicapai oleh model LSTM teroptimasi Optuna dibandingkan dengan model baseline berkonfigurasi default maupun manual tuning?",
        "Apakah konfigurasi hyperparameter hasil optimasi algoritma Optuna mampu mempertahankan stabilitas akurasi prediksi secara konsisten ketika dievaluasi pada berbagai pengujian data deret waktu out-of-sample?"
    ]

    cell_rm = t1.rows[4].cells[2]
    cell_rm.text = ""
    for idx, rm_text in enumerate(rumusan_masalah_list):
        p = cell_rm.paragraphs[0] if idx == 0 else cell_rm.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run_num = p.add_run(f"{idx+1}. ")
        run_num.font.name = "Times New Roman"
        run_num.font.size = Pt(11)
        run_num.font.bold = True
        run = p.add_run(rm_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    # 4. Referensi / Pustaka Utama (Row 5, Cell 2) - Minimal > 7 paper (Kita siapkan 10 paper kredibel SINTA & Internasional)
    referensi_list = [
        "JUTIF (2026). Comparative Analysis of Hyperparameter Optimization Methods for LSTM in Cryptocurrency Price Prediction: An Application to TRX–USD. Jurnal Teknik Informatika (JUTIF), Vol. 7, No. 3, hlm. 2340–2349. (Terakreditasi SINTA 2).",
        "Khumaidi, A., Kusmanto, P., & Hikmah, N. (2024). Optimizing Bitcoin Price Predictions Using Long Short-Term Memory Algorithm: A Deep Learning Approach. ILKOM Jurnal Ilmiah, Vol. 16, No. 1, hlm. 38–45. (Terakreditasi SINTA 2).",
        "Ganesha, P. R., Ratmadani, A. P., dkk. (2025). Forecasting Bitcoin Price Prediction with Long Short-Term Memory Networks Implementation and Applications Using Streamlit. Jurnal Teknik Informatika (JUTIF), Vol. 6, No. 5, hlm. 2940–2961. (Terakreditasi SINTA 2).",
        "Bit-Tech (2026). Comparative Analysis of LSTM and GRU Models with Hyperparameter Optimization for Bitcoin Price Prediction. Bit-Tech (Binary Digital - Technology), Vol. 9, No. 1, hlm. 1–11. (Jurnal Nasional Informatika).",
        "BRIN & Bina Nusantara University (2025). Improved LSTM Hyperparameters Alongside Sentiment Walk-Forward. Journal of Open Innovation: Technology, Market, and Complexity, Vol. 11, No. 1, 100458. (Terindeks Scopus Q1).",
        "Sakarya University (2023). LSTM Hyperparameters Optimization with Hparam Parameters for Bitcoin Price Prediction. Sakarya University Journal of Computer and Information Sciences, Vol. 6, No. 1, hlm. 45–53.",
        "Gaona, A., Rangel-Madariaga, J., & Uribe, L. (2026). Intraday Trading Strategy Selection Under Transaction Costs with Machine Learning. Frontiers in Applied Mathematics and Statistics, Vol. 10, hlm. 1–29. (Terindeks Scopus Q1).",
        "IJEECS (2023). Cryptocurrency Price Forecasting Method Using Long Short-Term Memory with Time-Varying Parameters. Indonesian Journal of Electrical Engineering and Computer Science, Vol. 30, No. 1, hlm. 435–443. (Terindeks Scopus).",
        "University of Warsaw (2026). Machine Learning-Based Bitcoin Trading Under Transaction Costs: Evidence From Walk-Forward Forecasting. Faculty of Economic Sciences & Machine Learning Research Group, hlm. 1–42.",
        "Jurnal RESTI (2024). Rekayasa Sistem dan Teknologi Informasi: Penerapan Algoritma Optimasi Metaheuristik pada Hyperparameter Arsitektur Deep Learning untuk Data Deret Waktu. Jurnal RESTI, Vol. 8, No. 2. (Terakreditasi SINTA 2)."
    ]

    cell_ref = t1.rows[5].cells[2]
    cell_ref.text = ""
    for idx, ref_text in enumerate(referensi_list):
        p = cell_ref.paragraphs[0] if idx == 0 else cell_ref.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run_num = p.add_run(f"[{idx+1}] ")
        run_num.font.name = "Times New Roman"
        run_num.font.size = Pt(10)
        run_num.font.bold = True
        run = p.add_run(ref_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

    # Output file
    output_filename = "Proposal_Skripsi_Optimasi_LSTM_Optuna_Zaini.docx"
    doc.save(output_filename)
    print(f"Successfully generated proposal document: {output_filename}")

if __name__ == "__main__":
    generate_proposal()
