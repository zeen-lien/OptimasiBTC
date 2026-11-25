"""
Skrip untuk memperbarui SEMPRO_seminar_revisi_siapsempo_v8.docx dan render BAB 1-3.pdf
sesuai dengan seluruh catatan bimbingan Pak Teguh Tamrin.
"""

import os
import shutil
import zipfile
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOCX_PATH = Path('03_Naskah_Skripsi/study2/file final/SEMPRO_seminar_revisi_siapsempo_v8.docx')
PDF_PATH = Path('03_Naskah_Skripsi/study2/file final/BAB 1-3.pdf')
NEW_IMG_PATH = Path('03_Naskah_Skripsi/study2/figures/gambar_2_2_kerangka_pemikiran.png')

def update_docx_content():
    print(f"Loading {DOCX_PATH}...")
    doc = docx.Document(str(DOCX_PATH))

    # 1. Update Kerangka Pemikiran P[175] - P[180]
    p175_text = "Alur kerangka pemikiran konseptual tersebut diorganisasikan ke dalam enam tahapan utama yang saling berkesinambungan:"
    p176_text = "1. Tahap Identifikasi Masalah dan Perumusan Target: Berangkat dari fenomena volatilitas pasar Bitcoin yang ekstrem dan karakteristik non-linearitasnya, penelitian merumuskan urgensi pemodelan realized volatility harian satu hari ke depan (t+1) menggunakan arsitektur deep learning LSTM yang dioptimasi secara objektif bebas penalaan manual coba-coba."
    p177_text = "2. Tahap Akuisisi dan Rekayasa Fitur: Mengagregasi data transaksi frekuensi tinggi kline 1 jam Binance Vision periode 2020–2026 menjadi realized variance harian UTC, mengeliminasi sampel cacat, serta mengekstraksi enam fitur teknikal kausal tanpa kebocoran informasi masa depan (look-ahead bias)."
    p178_text = "3. Tahap Partisi Deret Waktu dan Pembatasan Kebocoran Data: Membagi data secara kronologis menjadi Data Pengembangan 2020–2023 (1.460 observasi) untuk penalaan HPO, Train Pool 2020–2025 (2.191 observasi) untuk pelatihan final, serta data Evaluasi Temporal 2026 (273 observasi). Pemisahan dilengkapi purge gap (lookback + 1) guna memutus autokorelasi serial antar-sampel."
    p179_text = "4. Tahap Optimasi Hyperparameter dan Mekanisme Umpan Balik (Feedback Loop): Menala arsitektur dan parameter pelatihan LSTM menggunakan algoritma Bayesian Tree-structured Parzen Estimator (Optuna TPE) sebanyak 50 trial dengan skema 5-fold Purged Cross-Validation pada data pengembangan. Apabila pada proses validasi kriteria konvergensi fungsi kerugian QLIKE belum terpenuhi atau terjadi overfitting, sistem menjalankan mekanisme umpan balik (feedback loop) di mana algoritma Optuna secara adaptif memperbarui model probabilitas Parzen dan mengeksplorasi kombinasi hyperparameter baru dalam ruang pencarian hingga diperoleh konfigurasi arsitektur terbaik."
    p180_text = "5. Tahap Pelatihan Model Final dan Implementasi Baseline: Melatih ulang arsitektur LSTM terbaik pada Train Pool 2020–2025 (90% fit dan 10% early stopping tanpa refit), serta membangun empat model baseline pembanding (Persistence, HAR-RV, GARCH(1,1), dan LSTM untuned) sebagai tolak ukur komparasi empiris."
    
    # We also have stage 6
    p180b_text = "6. Tahap Evaluasi Kinerja dan Uji Hipotesis Statistik: Menguji performa generalisasi seluruh model pada periode evaluasi temporal 2026 menggunakan metrik asimetris QLIKE sebagai metrik primer serta MAE dan RMSE sebagai metrik sekunder. Signifikansi keunggulan model LSTM-Optuna diuji secara statistik inferensial menggunakan uji Diebold–Mariano satu sisi dengan koreksi HAC Newey–West (α = 0,05) dan Moving-Block Bootstrap 95% CI untuk menentukan penerimaan atau penolakan hipotesis penelitian (H0 vs H1)."

    doc.paragraphs[175].text = p175_text
    doc.paragraphs[176].text = p176_text
    doc.paragraphs[177].text = p177_text
    doc.paragraphs[178].text = p178_text
    doc.paragraphs[179].text = p179_text
    doc.paragraphs[180].text = p180_text

    # Check if we should append stage 6 to paragraph 180 or insert it
    doc.paragraphs[180].text = p180_text + "\n" + p180b_text

    # 2. Update Hipotesis Penelitian Sub-bab I (P[182] - P[185])
    p182_text = "Berdasarkan landasan teori, tinjauan penelitian terdahulu, dan kerangka pemikiran konseptual yang telah dipaparkan, dirumuskan hipotesis statistik formal yang terdiri dari pasangan Hipotesis Nol (H0) dan Hipotesis Alternatif (H1) untuk menguji signifikansi komparatif performa model pada data evaluasi temporal 2026:"
    
    p183_text = "1. Hipotesis 1: Komparasi Terhadap Baseline Random Walk Persistence\n" \
                "   • H0 (Hipotesis Nol): Model LSTM yang dioptimasi dengan algoritma Optuna tidak menghasilkan rata-rata fungsi kerugian QLIKE yang lebih rendah secara signifikan dibandingkan baseline Random Walk Persistence pada data evaluasi temporal 2026 (μ_d1 ≥ 0).\n" \
                "   • H1 (Hipotesis Alternatif): Model LSTM yang dioptimasi dengan algoritma Optuna menghasilkan rata-rata fungsi kerugian QLIKE yang lebih rendah secara signifikan dibandingkan baseline Random Walk Persistence pada data evaluasi temporal 2026 (μ_d1 < 0).\n" \
                "   (Diferensial kerugian didefinisikan sebagai d_1,t = Loss_QLIKE(LSTM-Optuna)_t - Loss_QLIKE(Persistence)_t, diuji satu sisi menggunakan uji Diebold–Mariano berkoreksi HAC Newey–West pada taraf signifikansi α = 0,05)."

    p184_text = "2. Hipotesis 2: Komparasi Terhadap Model Ekonometrika HAR-RV\n" \
                "   • H0 (Hipotesis Nol): Model LSTM yang dioptimasi dengan algoritma Optuna tidak menghasilkan rata-rata fungsi kerugian QLIKE yang lebih rendah secara signifikan dibandingkan model ekonometrika HAR-RV pada data evaluasi temporal 2026 (μ_d2 ≥ 0).\n" \
                "   • H1 (Hipotesis Alternatif): Model LSTM yang dioptimasi dengan algoritma Optuna menghasilkan rata-rata fungsi kerugian QLIKE yang lebih rendah secara signifikan dibandingkan model ekonometrika HAR-RV pada data evaluasi temporal 2026 (μ_d2 < 0).\n" \
                "   (Diferensial kerugian didefinisikan sebagai d_2,t = Loss_QLIKE(LSTM-Optuna)_t - Loss_QLIKE(HAR-RV)_t, diuji satu sisi menggunakan uji Diebold–Mariano berkoreksi HAC Newey–West pada taraf signifikansi α = 0,05)."

    p185_text = "Adapun kinerja model pembanding GARCH(1,1) dan LSTM tanpa penalaan (untuned) dilaporkan dan dievaluasi secara deskriptif sebagai analisis komparasi sekunder untuk mengamati dinamika varians bersyarat linier dan mengukur kontribusi penalaan hyperparameter, sehingga tidak dirumuskan hipotesis inferensial primer tersendiri."

    doc.paragraphs[182].text = p182_text
    doc.paragraphs[183].text = p183_text
    doc.paragraphs[184].text = p184_text
    doc.paragraphs[185].text = p185_text

    # 3. Update Unit Testing Mandiri P[316]
    p316_text = "Untuk menjamin keandalan perangkat lunak, integritas data, dan ketiadaan kebocoran data (data leakage) secara berulang, repositori penelitian dilengkapi rangkaian pengujian unit terotomatisasi (automated unit testing) berbasis pustaka pytest. Rangkaian ini terdiri atas 34 skenario pengujian mandiri yang terdistribusi ke dalam empat berkas skrip tes fisik di direktori tests/, yaitu:\n" \
                "1) tests/test_study2.py (15 skenario tes): Menguji verifikasi hash integritas dataset (SHA-256), kelengkapan 24 bar intrahari per tanggal kalender UTC, kepositifan RV dan keterhinggaan nilai log(RV), ketiadaan kebocoran fitur masa depan (no future leakage), keselarasan jendela sekuens masukan, sifat penalti asimetris fungsi QLIKE, komputasi uji statistik Diebold–Mariano berkoreksi Newey–West, serta selang kepercayaan Moving-Block Bootstrap.\n" \
                "2) tests/test_s2_calendar.py (7 skenario tes): Menguji penanganan diskontinuitas kalender (gap handling) pada seluruh model baseline (Persistence, HAR-RV, dan GARCH(1,1)) agar perhitungan imbal hasil dan jendela lookback tidak melompati hari yang hilang secara kausal.\n" \
                "3) tests/test_s2_split_scaler.py (6 skenario tes): Menguji penegakan isolasi penyesuaian skala (scaler fitting) hanya pada subset pelatihan tiap lipatan, penegakan purge gap antar-partisi deret waktu guna memutus autokorelasi serial, serta pemisahan internal validation set.\n" \
                "4) tests/test_s2_analyze.py (6 skenario tes): Menguji keselarasan baris tanggal prediksi (alignment validation) dan penolakan otomatis terhadap luaran prediksi yang cacat atau tidak sinkron sebelum inferensi statistik dieksekusi.\n" \
                "Seluruh 34 skenario pengujian unit ini telah diverifikasi dan berhasil lulus 100% (passed) secara otomatis pada repositori lokal maupun repositori GitHub."

    doc.paragraphs[316].text = p316_text

    # Save modified DOCX
    temp_docx = "temp_updated.docx"
    doc.save(temp_docx)
    print("[OK] Saved text updates to temp docx.")

    # 4. Replace image3.png in docx zip with NEW_IMG_PATH
    print(f"Replacing word/media/image3.png with {NEW_IMG_PATH}...")
    temp_zip = "temp_replaced.docx"
    with zipfile.ZipFile(temp_docx, 'r') as zin, zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/media/image3.png":
                with open(NEW_IMG_PATH, "rb") as img_fp:
                    zout.writestr(item, img_fp.read())
                print("[OK] image3.png replaced with new Gambar 2.2 PNG.")
            else:
                zout.writestr(item, zin.read(item.filename))

    # Overwrite destination
    shutil.move(temp_zip, str(DOCX_PATH))
    if os.path.exists(temp_docx):
        os.remove(temp_docx)
    print(f"[OK] Master DOCX successfully updated at: {DOCX_PATH}")

def render_pdf_with_word():
    print("Rendering updated DOCX to PDF using Word COM...")
    import win32com.client
    import time
    
    abs_docx = str(DOCX_PATH.resolve())
    abs_pdf = str(PDF_PATH.resolve())

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False

    try:
        doc = word.Documents.Open(abs_docx, ReadOnly=False)
        # Update fields (e.g. TOC, cross references)
        try:
            doc.Fields.Update()
            for t in doc.TablesOfContents:
                t.Update()
        except Exception as e:
            print(f"Notice on updating TOC: {e}")

        # Save as PDF (Format 17 = wdFormatPDF)
        doc.SaveAs2(abs_pdf, FileFormat=17)
        doc.Close(SaveChanges=False)
        print(f"[OK] PDF successfully generated at: {abs_pdf}")
    finally:
        word.Quit()

if __name__ == "__main__":
    update_docx_content()
    render_pdf_with_word()
