"""Generate BAB V from the published final results, including negative findings."""

from __future__ import annotations

import re

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.shared import Cm, Pt

from doc_paths import ensure_naskah_dir
from results_context import (
    FinalResults,
    format_number,
    format_pct,
    format_usd,
)


def generate_bab5():
    results = FinalResults.load()
    e0 = results.metrics("E0")
    e7 = results.metrics("E7")
    best_lstm = results.best_lstm
    config = results.final_configuration()
    hyper = config.get("hyperparameters") or {}
    verdict = results.verdict
    status = verdict.get("status")

    doc = docx.Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(4.0)
    section.left_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic

    def latex_to_omml(token):
        token = token.strip().replace("\\\\", "\\")
        if token in [r"\hat{y}_t", "hat{y}_t"]:
            return (
                '<m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:sSub>'
                "<m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t>"
                "</m:r></m:sub></m:sSub></m:e></m:acc>"
            )
        if token in [r"\geq", "\u2265"]:
            return '<m:r><m:t>\u2265</m:t></m:r>'
        if token in [r"\leq", "\u2264"]:
            return '<m:r><m:t>\u2264</m:t></m:r>'
        if "_" in token and not ("^" in token or "\\" in token):
            base, sub = token.split("_", 1)
            sub = sub.strip("{}")
            return (
                f"<m:sSub><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sub>"
                f"<m:r><m:t>{sub}</m:t></m:r></m:sub></m:sSub>"
            )
        clean = token.replace("\\", "")
        return f"<m:r><m:t>{clean}</m:t></m:r>"

    def add_paragraph(
        text, space_after=6, line_spacing=1.5, first_line_indent=Cm(1.0)
    ):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_after = Pt(space_after)
        if first_line_indent:
            p.paragraph_format.first_line_indent = first_line_indent
        if "$" in text:
            for part in re.split(r"(\$[^\$]+\$)", text):
                if not part:
                    continue
                if part.startswith("$") and part.endswith("$"):
                    inner = latex_to_omml(part[1:-1])
                    p._element.append(
                        parse_xml(
                            '<m:oMath xmlns:m="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/math">{inner}</m:oMath>'
                        )
                    )
                else:
                    set_font(p.add_run(part), size=12)
        else:
            set_font(p.add_run(text), size=12)
        return p

    def add_heading(text, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        set_font(p.add_run(text), size=12, bold=True)
        return p

    def add_sub_heading(text, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        set_font(p.add_run(text), size=12, bold=True)
        return p

    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    set_font(p_chap.add_run("BAB V\nPENUTUP"), size=14, bold=True)

    add_heading("A. Simpulan")

    data = results.data
    add_paragraph(
        "Penelitian ini merancang dan mengevaluasi pipeline optimasi "
        "hyperparameter LSTM berbasis Optuna-TPE untuk peramalan harga penutupan "
        "Bitcoin satu langkah ke depan. Evaluasi dilakukan dengan matriks "
        f"terkontrol E0 sampai E7, holdout {format_number(data.get('n_test', 0), 0)} "
        "hari yang tidak dipakai untuk tuning, scaler per fold, purge sebesar "
        f"lookback, {results.expected_seeds} seed, dan "
        "moving-block bootstrap. Pertanyaan penelitian dijawab melalui bukti "
        "kuantitatif yang dapat ditelusuri ke berkas hasil, bukan melalui klaim "
        "bahwa model usulan pasti unggul. Pendekatan ini penting karena "
        "peramalan aset kripto rentan menghasilkan kesimpulan yang terlalu "
        "optimistis bila baseline naif dan ketidakpastian tidak dilaporkan "
        "(Bouthillier et al., 2021; Makridakis et al., 2018)."
    )

    if verdict.get("ci_direction") == "persistence_better":
        verdict_sentence = (
            "Verdict ilmiah menyatakan bahwa E7 memiliki MAE lebih tinggi "
            "daripada persistence dan CI selisih berpasangan seluruhnya di atas "
            "nol, sehingga hasil ini secara statistik lebih buruk."
        )
    elif status == "proposed_lower_mae_ci_excludes_zero":
        verdict_sentence = (
            "Verdict ilmiah menyatakan bahwa E7 memiliki MAE lebih rendah "
            "daripada persistence dengan CI selisih berpasangan yang tidak "
            "melewati nol."
        )
    elif status == "proposed_lower_mae_ci_includes_zero":
        verdict_sentence = (
            "Verdict ilmiah menyatakan bahwa MAE titik E7 lebih rendah, tetapi "
            "CI selisih berpasangan masih melewati nol sehingga belum dapat "
            "disebut signifikan."
        )
    else:
        verdict_sentence = (
            "Verdict ilmiah menyatakan bahwa E7 tidak lebih baik daripada "
            "persistence pada MAE titik."
        )

    add_paragraph(
        "Simpulan pertama berkaitan dengan kinerja relatif terhadap persistence. "
        f"Baseline persistence menghasilkan MAE {format_usd(e0['MAE'])} pada "
        f"holdout, sedangkan model usulan E7 menghasilkan MAE {format_usd(e7['MAE'])}. "
        f"Model LSTM terbaik adalah {best_lstm['run']} dengan MAE "
        f"{format_usd(best_lstm['MAE'])}. {verdict_sentence} Apabila E7 tidak lebih "
        "rendah daripada persistence, maka hasil negatif ini menjadi simpulan "
        "utama: pada data dan horizon yang diuji, optimasi hyperparameter belum "
        "cukup untuk mengalahkan prediksi naif. Klaim keunggulan tidak boleh "
        "dipaksakan hanya karena model lebih kompleks atau proses optimasinya "
        "lebih mahal (Willmott & Matsuura, 2005; Lim & Zohren, 2021)."
    )

    add_paragraph(
        "Simpulan kedua berkaitan dengan konfigurasi hasil HPO. E7 memilih "
        f"lookback {hyper.get('lookback', '-')} hari, {hyper.get('units', '-')} "
        f"unit LSTM, dropout {format_number(hyper.get('dropout', 0), 2)}, "
        f"learning rate {format_number(hyper.get('learning_rate', 0), 5)}, "
        f"batch size {hyper.get('batch_size', '-')}, dan "
        f"{hyper.get('layers', '-')} layer. Studi menyelesaikan "
        f"{config.get('total_trials', '-')} trial dan memilih trial nomor "
        f"{config.get('best_trial_number', '-')}. Konfigurasi ini adalah hasil "
        "pencarian pada data in-sample, bukan bukti bahwa kombinasi tersebut "
        "akan optimal pada aset atau periode lain. Nilai tambah HPO harus "
        "dinilai dari perbandingan E7 terhadap E6 yang memakai loss dan "
        "scheduler sama, bukan dari besarnya ruang pencarian semata (Akiba et "
        "al., 2019; Feurer & Hutter, 2019)."
    )

    add_paragraph(
        "Simpulan ketiga berkaitan dengan ablasi loss dan scheduler. E3 sampai E6 "
        "menunjukkan bahwa perubahan fungsi kerugian dan scheduler dapat "
        "mengubah MAE, tetapi arah dan besarnya tidak selalu konsisten dengan "
        "klaim teoretis. Pada konfigurasi yang diuji, loss MAE dan "
        "ReduceLROnPlateau bukan jaminan perbaikan otomatis; keduanya harus "
        "dievaluasi bersama variabilitas antar-seed dan interval kepercayaan. "
        "Dengan demikian, kontribusi metodologis penelitian ini adalah "
        "pemisahan faktor yang jelas dan pelaporan efek yang dapat diaudit, "
        "bukan resep hyperparameter yang berlaku umum (Bouthillier et al., "
        "2021; Greff et al., 2017)."
    )

    if status == "proposed_lower_mae_ci_excludes_zero":
        empirical_reading = (
            "Temuan bahwa E7 mengalahkan persistence dengan interval kepercayaan "
            "berpasangan yang tidak melewati nol memberi bukti awal bahwa HPO "
            "dapat menambah nilai pada data dan horizon yang diuji. Klaim tetap "
            "dibatasi pada satu aset, satu horizon, dan satu periode holdout."
        )
    elif status == "proposed_lower_mae_ci_includes_zero":
        empirical_reading = (
            "Temuan bahwa MAE titik E7 lebih rendah tetapi interval kepercayaan "
            "masih melewati nol menunjukkan bahwa perbaikan belum stabil secara "
            "statistik. Kompleksitas model belum dapat dijadikan pengganti bukti "
            "empiris yang meyakinkan."
        )
    else:
        if verdict.get("ci_direction") == "persistence_better":
            empirical_reading = (
                "Temuan bahwa MAE E7 lebih tinggi daripada persistence dengan "
                "interval kepercayaan berpasangan yang seluruhnya di atas nol "
                "memberi informasi yang jujur bagi praktisi: pada data dan horizon "
                "yang diuji, kompleksitas model serta HPO bukan pengganti bukti "
                "empiris dan justru menambah galat."
            )
        else:
            empirical_reading = (
                "Temuan bahwa LSTM belum mengalahkan persistence memberi informasi "
                "yang jujur bagi praktisi: kompleksitas model bukan pengganti bukti "
                "empiris."
            )

    add_paragraph(
        "Simpulan keempat berkaitan dengan kontribusi metodologis penelitian. "
        "Pipeline yang dibangun tetap bernilai karena menyediakan cara "
        "mereproduksi eksperimen, memisahkan data tuning dan holdout, menghitung "
        "ketidakpastian, dan membandingkan model dengan baseline naif. "
        f"{empirical_reading} Kontribusi tersebut lebih defensible daripada "
        "mengklaim keunggulan yang tidak didukung data (Makridakis et al., 2018; "
        "López de Prado, 2018)."
    )

    add_heading("B. Saran")

    add_paragraph(
        "Penelitian lanjutan disarankan memperluas cakupan data ke beberapa aset "
        "kripto dan beberapa periode holdout yang mewakili rezim bull, bear, dan "
        "sideways. Evaluasi multi-aset memungkinkan pengujian apakah kegagalan "
        "mengalahkan persistence bersifat umum atau hanya terjadi pada BTC/USDT "
        "dan periode tertentu. Selain itu, protokol yang sama sebaiknya "
        "diterapkan pada data pasar tradisional sebagai pembanding eksternal. "
        "Dengan desain seperti ini, klaim generalisasi dapat diuji secara "
        "empiris, bukan diasumsikan dari satu run (Lim & Zohren, 2021; "
        "Makridakis et al., 2018)."
    )

    add_paragraph(
        "Dari sisi fitur dan arsitektur, penelitian berikutnya dapat menguji "
        "model multivariat yang memasukkan volume, indikator on-chain, sentimen "
        "berita, dan faktor makroekonomi. Eksperimen juga dapat memperluas "
        "horizon dari satu langkah menjadi multi-langkah, serta membandingkan "
        "LSTM dengan GRU, Temporal Convolutional Network, atau Transformer "
        "dalam protokol tuning yang identik. Perluasan ini harus tetap "
        "mempertahankan pemisahan in-sample dan holdout serta scaler per fold "
        "agar perbandingan tidak terkontaminasi kebocoran data (Lim & Zohren, 2021; "
        "Greff et al., 2017)."
    )

    add_paragraph(
        "Dari sisi evaluasi, penelitian lanjutan perlu menambahkan uji formal "
        "seperti Diebold-Mariano, analisis biaya transaksi, bid-ask spread, dan "
        "slippage, serta simulasi strategi perdagangan yang realistis. "
        "Pelaporan sebaiknya mencakup lebih banyak seed, interval kepercayaan "
        "antar-seed, dan analisis sensitivitas terhadap panjang holdout. "
        "Dengan demikian, pembaca dapat membedakan peningkatan akurasi statistik "
        "dari nilai ekonomi yang nyata. Langkah ini penting agar hasil "
        "penelitian tidak berhenti pada angka galat, tetapi memberi panduan "
        "yang dapat diuji bagi pengembangan sistem peramalan dan manajemen "
        "risiko aset digital (Gu et al., 2020; Tashman, 2000)."
    )

    out_dir = ensure_naskah_dir()
    out_path = out_dir / "BAB_5_PENUTUP_ZAINI_LEON.docx"
    doc.save(out_path)
    print(f"[SUCCESS] BAB 5 Generated successfully: {out_path}")


if __name__ == "__main__":
    generate_bab5()
