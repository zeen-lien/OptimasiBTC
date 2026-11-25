"""
Skrip sinkronisasi Gambar 2.2 dan Teks Kerangka Pemikiran Bab II
1. Memastikan penomoran Tahap 1 s.d. 6 sinkron 1:1 antara gambar dan teks.
2. Memastikan seluruh bullet points di dalam gambar disusun vertikal ke bawah.
3. Mengganti image3.png di master docx dengan gambar_2_2_kerangka_pemikiran.png yang baru.
4. Render ulang BAB 1-3.pdf via Word COM.
"""

from pathlib import Path
import zipfile
import shutil
import docx
import win32com.client

DOCX_PATH = Path('03_Naskah_Skripsi/study2/file final/SEMPRO_seminar_revisi_siapsempo_v8.docx')
PDF_PATH = Path('03_Naskah_Skripsi/study2/file final/BAB 1-3.pdf')
NEW_IMG_PATH = Path('03_Naskah_Skripsi/study2/figures/gambar_2_2_kerangka_pemikiran.png')

def sync_docx_and_render():
    print(f"Loading {DOCX_PATH}...")
    doc = docx.Document(str(DOCX_PATH))

    # Cek P[175] s.d P[181]
    p175_text = "Alur kerangka pemikiran konseptual tersebut diorganisasikan ke dalam enam tahapan utama yang saling berkesinambungan:"
    p176_text = "1. Tahap Identifikasi Masalah dan Perumusan Target: Berangkat dari fenomena volatilitas pasar Bitcoin yang ekstrem dan karakteristik non-linearitasnya, penelitian merumuskan urgensi pemodelan realized volatility harian satu hari ke depan (t+1) menggunakan arsitektur deep learning LSTM yang dioptimasi secara objektif bebas penalaan manual coba-coba."
    p177_text = "2. Tahap Pengumpulan dan Pra-pemrosesan Data Frekuensi Tinggi: Mengagregasi data transaksi frekuensi tinggi kline 1 jam Binance Vision periode 2020–2026 menjadi realized variance harian UTC, memfilter data cacat (hanya hari dengan ≥ 20 bar yang dipertahankan), serta merekayasa enam fitur teknikal kausal tanpa kebocoran informasi masa depan (look-ahead bias)."
    p178_text = "3. Tahap Partisi Deret Waktu dan Pengendalian Kebocoran Data: Membagi data secara kronologis menjadi Data Pengembangan 2020–2023 (1.460 observasi) untuk penalaan HPO, Train Pool 2020–2025 (2.191 observasi) untuk pelatihan final, serta data Evaluasi Temporal 2026 (273 observasi). Pemisahan dilengkapi purge gap (lookback + 1) guna memutus autokorelasi serial antar-sampel."
    p179_text = "4. Tahap Optimasi Hyperparameter dan Mekanisme Umpan Balik (Feedback Loop): Menala arsitektur dan parameter pelatihan LSTM menggunakan algoritma Bayesian Tree-structured Parzen Estimator (Optuna TPE) sebanyak 50 trial dengan skema 5-fold Purged Cross-Validation pada data pengembangan. Apabila pada proses validasi kriteria konvergensi fungsi kerugian QLIKE belum terpenuhi atau terjadi overfitting, sistem menjalankan mekanisme umpan balik (feedback loop) di mana algoritma Optuna secara adaptif memperbarui model probabilitas Parzen dan mengeksplorasi kombinasi hyperparameter baru dalam ruang pencarian hingga diperoleh konfigurasi arsitektur terbaik."
    p180_text = "5. Tahap Pelatihan Model Final pada Train Pool (2020–2025): Melatih ulang arsitektur LSTM terbaik pada Train Pool 2020–2025 (90% fit dan 10% early stopping tanpa refit), serta membangun empat model baseline pembanding (Persistence, HAR-RV, GARCH(1,1), dan LSTM untuned) sebagai tolak ukur komparasi empiris."
    
    # Pisahkan tahap 6 sebagai paragraf tersendiri jika sebelumnya tergabung
    # Cek apakah P[180] berisi newline
    p180_combined = doc.paragraphs[180].text
    if "\n6. Tahap" in p180_combined:
        parts = p180_combined.split("\n6. Tahap")
        doc.paragraphs[180].text = parts[0].strip()
        p180b_text = "6. Tahap" + parts[1]
        # Sisipkan paragraf baru setelah P[180]
        # Dalam python-docx kita bisa menambahkan teks atau mengubah paragraf
        p_new = doc.paragraphs[180]._element.addnext(doc.add_paragraph()._element)
        # Lebih aman: update teks paragraf 180 dan buat paragraf bersih
    
    # Mari kita format ulang paragraf 175-181 secara bersih
    doc.paragraphs[175].text = p175_text
    doc.paragraphs[176].text = p176_text
    doc.paragraphs[177].text = p177_text
    doc.paragraphs[178].text = p178_text
    doc.paragraphs[179].text = p179_text
    doc.paragraphs[180].text = p180_text + "\n\n6. Tahap Evaluasi Kinerja (2026) dan Uji Hipotesis Statistik (H0 vs H1): Menguji performa generalisasi seluruh model pada periode evaluasi temporal 2026 menggunakan metrik asimetris QLIKE sebagai metrik primer serta MAE dan RMSE sebagai metrik sekunder. Signifikansi keunggulan model LSTM-Optuna diuji secara statistik inferensial menggunakan uji Diebold–Mariano satu sisi dengan koreksi HAC Newey–West (α = 0,05) dan Moving-Block Bootstrap 95% CI untuk menentukan penerimaan atau penolakan hipotesis penelitian (H0 vs H1)."

    temp_docx = "temp_synced.docx"
    doc.save(temp_docx)

    # Ganti gambar image3.png di dalam file zip docx
    print(f"Mengganti word/media/image3.png dengan {NEW_IMG_PATH}...")
    temp_zip = "temp_replaced.docx"
    with zipfile.ZipFile(temp_docx, 'r') as zin, zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/media/image3.png":
                with open(NEW_IMG_PATH, "rb") as img_fp:
                    zout.writestr(item, img_fp.read())
                print("[OK] image3.png berhasil diganti dengan Gambar 2.2 versi vertikal 6 tahap.")
            else:
                zout.writestr(item, zin.read(item.filename))

    shutil.move(temp_zip, str(DOCX_PATH))
    if Path(temp_docx).exists():
        Path(temp_docx).unlink()
    print(f"[OK] Master DOCX berhasil disimpan di: {DOCX_PATH}")

    # Render ulang PDF
    print(f"Merender ulang {PDF_PATH} menggunakan Word COM...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    try:
        d = word.Documents.Open(str(DOCX_PATH.resolve()), ReadOnly=False)
        try:
            d.Fields.Update()
            for t in d.TablesOfContents:
                t.Update()
        except Exception as e:
            print(f"Notice TOC update: {e}")
        d.SaveAs2(str(PDF_PATH.resolve()), FileFormat=17)
        d.Close(SaveChanges=False)
        print(f"[OK] PDF berhasil dirender ulang di: {PDF_PATH}")
    finally:
        word.Quit()

if __name__ == "__main__":
    sync_docx_and_render()
