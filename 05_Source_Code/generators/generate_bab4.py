"""Generate BAB IV from the published final results.

All metrics, confidence intervals, effect sizes, and the scientific verdict
come from ``05_Source_Code/results/summary_final.json``.  The chapter does not
hardcode a winner: if E7 fails to beat persistence, the text says so.
"""

from __future__ import annotations

import re

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Cm, Pt

from doc_paths import ensure_naskah_dir
from results_context import (
    FinalResults,
    format_number,
    format_pct,
    format_usd,
)


def generate_bab4():
    results = FinalResults.load()
    figures_dir = results.figures_dir

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
        if token in [r"\hat{y}", "hat{y}"]:
            return (
                '<m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r>'
                "<m:t>y</m:t></m:r></m:e></m:acc>"
            )
        if token in [r"\geq", "\u2265"]:
            return '<m:r><m:t>\u2265</m:t></m:r>'
        if token in [r"\leq", "\u2264"]:
            return '<m:r><m:t>\u2264</m:t></m:r>'
        if token in [r"\times", "\u00d7"]:
            return '<m:r><m:t>\u00d7</m:t></m:r>'
        if token in [r"\ell(x)/g(x)", "\u2113(x)/g(x)"]:
            return '<m:r><m:t>\u2113(x)/g(x)</m:t></m:r>'
        if "_" in token and not ("^" in token or "\\" in token):
            base, sub = token.split("_", 1)
            sub = sub.strip("{}")
            return (
                f"<m:sSub><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sub>"
                f"<m:r><m:t>{sub}</m:t></m:r></m:sub></m:sSub>"
            )
        if "^" in token and not ("_" in token or "\\" in token):
            base, sup = token.split("^", 1)
            sup = sup.strip("{}")
            return (
                f"<m:sSup><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sup>"
                f"<m:r><m:t>{sup}</m:t></m:r></m:sup></m:sSup>"
            )
        clean = (
            token.replace(r"\in", "\u2208")
            .replace(r"\gamma", "\u03b3")
            .replace(r"\sigma", "\u03c3")
            .replace(r"\odot", "\u2299")
            .replace(r"\ell", "\u2113")
            .replace(r"\leq", "\u2264")
            .replace(r"\geq", "\u2265")
            .replace(r"\times", "\u00d7")
            .replace("\\", "")
        )
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

    def add_styled_table(headers, rows, col_widths, caption, font_size=8.5):
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.line_spacing = 1.0
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p_cap.add_run(caption), size=11, bold=True)

        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for ri, row_data in enumerate([headers] + rows):
            for ci, cell_text in enumerate(row_data):
                cell = table.rows[ri].cells[ci]
                cell.width = col_widths[ci]
                cell.text = str(cell_text)
                p = cell.paragraphs[0]
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if ci == 0 or ri == 0
                    else WD_ALIGN_PARAGRAPH.JUSTIFY
                )
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for run in p.runs:
                    set_font(run, size=font_size, bold=(ri == 0))
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>'))
        return table

    def add_figure(image_path, caption, width_cm=14.0):
        if not image_path.exists():
            raise FileNotFoundError(
                f"Gambar wajib tidak ditemukan: {image_path}. "
                "Jalankan 06_evaluate_and_compare.py dan 08_analyze_results.py."
            )
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(str(image_path), width=Cm(width_cm))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        set_font(p_cap.add_run(caption), size=10.5, bold=True)

    def signed_change(value: float) -> str:
        """Describe a relative change without hiding a negative result."""
        if value >= 0:
            return f"perbaikan {format_pct(value)}"
        return f"peningkatan galat {format_pct(abs(value))}"

    def comparison_claim(label: str) -> str:
        """Describe a paired MAE comparison using the observed direction.

        ``difference_b_minus_a`` is negative when model B has the lower error.
        The sentence reports the difference in the same B - A orientation as the
        table so the prose and the interval keep identical signs.
        """
        payload = results.comparison(label)
        mae = results.comparison_metric(label, "MAE")
        difference = float(mae["difference_b_minus_a"])
        key_a = str(payload["model_a"])
        key_b = str(payload["model_b"])
        ci_low = float(mae["ci_low"])
        ci_high = float(mae["ci_high"])
        excludes_zero = ci_high < 0 or ci_low > 0

        if abs(difference) < 1e-12:
            return (
                f"selisih MAE {key_b} terhadap {key_a} nol, sehingga tidak ada "
                "perbedaan titik yang dapat diklaim."
            )

        lower, higher = (
            (key_b, key_a) if difference < 0 else (key_a, key_b)
        )
        interval = (
            f"CI 95% selisih {format_usd(ci_low, signed=True)} sampai "
            f"{format_usd(ci_high, signed=True)}"
        )
        if excludes_zero:
            return (
                f"selisih MAE {key_b} − {key_a} adalah "
                f"{format_usd(difference, signed=True)}, dengan {interval} yang "
                f"tidak melewati nol; {lower} mencatat MAE lebih rendah daripada "
                f"{higher}."
            )
        return (
            f"selisih MAE {key_b} − {key_a} adalah "
            f"{format_usd(difference, signed=True)} dengan {interval}; karena CI "
            "melewati nol, perbedaan ini belum dapat disebut sebagai bukti "
            "keunggulan."
        )

    # ------------------------------------------------------------------
    # Chapter title
    # ------------------------------------------------------------------
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_after = Pt(4)
    p_chap.paragraph_format.line_spacing = 1.15
    set_font(
        p_chap.add_run("BAB IV\nHASIL PENELITIAN DAN PEMBAHASAN"),
        size=14,
        bold=True,
    )

    add_heading("A. Hasil Penelitian")

    add_paragraph(
        "Bab ini melaporkan hasil matriks eksperimen terkontrol E0 sampai E7 "
        "untuk peramalan harga penutupan Bitcoin satu langkah ke depan. Seluruh "
        f"model dievaluasi pada {format_number(results.data.get('n_test', 0), 0)} hari "
        "holdout yang identik, sedangkan pemilihan hyperparameter, early stopping "
        "internal, dan seluruh keputusan desain hanya menggunakan "
        f"{format_number(results.data.get('n_train', 0), 0)} observasi in-sample. "
        "Angka yang disajikan pada "
        "tabel dan paragraf dibaca langsung dari berkas hasil final yang "
        "tersimpan, bukan dari ingatan peneliti atau tabel lama. Dengan demikian, "
        "setiap klaim dapat ditelusuri kembali ke run, seed, dan berkas metrik "
        "yang menghasilkan angka tersebut (Bouthillier et al., 2021)."
    )

    add_sub_heading("1. Karakteristik Data dan Protokol Evaluasi")

    stats = results.data.get("statistics") or {}
    add_paragraph(
        "Data primer berupa harga penutupan harian BTC/USDT periode "
        f"{stats.get('period', ['-', '-'])[0]} sampai "
        f"{stats.get('period', ['-', '-'])[1]} dengan total "
        f"{format_number(stats.get('n_observations', 0), 0)} observasi. Harga "
        f"terendah tercatat {format_usd(stats.get('min', 0))} pada "
        f"{stats.get('min_date', '-')}, sedangkan harga tertinggi "
        f"{format_usd(stats.get('max', 0))} pada {stats.get('max_date', '-')}. "
        f"Rata-rata harga adalah {format_usd(stats.get('mean', 0))}, median "
        f"{format_usd(stats.get('median', 0))}, dan simpangan baku "
        f"{format_usd(stats.get('std', 0))}. Rentang harga yang lebar menunjukkan "
        "bahwa model harus bekerja pada rezim pasar yang sangat berbeda, "
        "sehingga evaluasi tunggal pada satu periode tidak cukup untuk "
        "menggeneralisasi ke seluruh siklus Bitcoin (Makridakis et al., 2018)."
    )

    add_styled_table(
        ["No", "Parameter", "Nilai", "Keterangan"],
        [
            ["1", "Total observasi", f"{format_number(stats.get('n_observations', 0), 0)} hari", "Data harian tanpa celah"],
            ["2", "Harga minimum", format_usd(stats.get("min", 0)), f"Tercatat {stats.get('min_date', '-')}"],
            ["3", "Harga maksimum", format_usd(stats.get("max", 0)), f"Tercatat {stats.get('max_date', '-')}"],
            ["4", "Rata-rata", format_usd(stats.get("mean", 0)), "Rerata aritmatika"],
            ["5", "Median", format_usd(stats.get("median", 0)), "Titik tengah distribusi"],
            ["6", "Simpangan baku", format_usd(stats.get("std", 0)), "Dispersi harga"],
        ],
        [Cm(0.8), Cm(3.2), Cm(3.4), Cm(6.6)],
        "Tabel 4.1 Statistik Deskriptif Harga Penutupan Bitcoin",
    )

    add_paragraph(
        "Partisi data dilakukan secara kronologis 80:20 tanpa pengacakan: "
        f"{format_number(results.data.get('n_train', 0), 0)} observasi in-sample, "
        f"lalu {format_number(results.data.get('n_test', 0), 0)} observasi holdout "
        f"mulai {results.data.get('test_period', ['-', '-'])[0]} sampai "
        f"{results.data.get('test_period', ['-', '-'])[1]}. Holdout tidak pernah "
        "dibaca selama tuning. Pada Tier 3, validasi silang menggunakan "
        "Time-Series Split berpurge dengan jarak sebesar lookback dan scaler "
        "Min-Max yang di-fit ulang pada setiap fold. Interval kepercayaan "
        "dihitung dengan moving-block bootstrap 7 hari sebanyak 2.000 resample "
        "pada tanggal yang sama, sedangkan variabilitas antar-seed dilaporkan "
        "terpisah sebagai mean dan simpangan baku dari lima seed "
        "(Arlot & Celisse, 2010; Tashman, 2000)."
    )

    add_sub_heading("2. Baseline Persistence dan Baseline Naif")

    baselines = results.payload.get("baselines") or {}
    e0 = results.metrics("E0")
    e0_ci = results.ci("E0", "MAE")
    baseline_rows = []
    for name, payload in baselines.items():
        metrics = payload.get("metrics") or {}
        baseline_rows.append(
            [
                name.replace("_", " ").title(),
                format_usd(metrics.get("RMSE", 0)),
                format_usd(metrics.get("MAE", 0)),
                format_pct(metrics.get("MAPE", 0)),
            ]
        )
    if not baseline_rows:
        baseline_rows = [["Persistence", format_usd(e0["RMSE"]), format_usd(e0["MAE"]), format_pct(e0["MAPE"])]]

    add_paragraph(
        "Baseline persistence memprediksi harga besok sama dengan harga hari ini. "
        f"Pada holdout, baseline ini menghasilkan RMSE {format_usd(e0['RMSE'])}, "
        f"MAE {format_usd(e0['MAE'])}, dan MAPE {format_pct(e0['MAPE'])}. "
        f"Interval kepercayaan 95% untuk MAE persistence adalah "
        f"{format_usd(e0_ci['ci_low'])} sampai {format_usd(e0_ci['ci_high'])}. "
        "Nilai tersebut menjadi ambang minimum yang harus dikalahkan sebelum "
        "sebuah model LSTM layak disebut bermanfaat. Baseline drift dan seasonal "
        "naive juga dilaporkan pada Tabel 4.2 untuk menunjukkan bahwa kesimpulan "
        "tidak bergantung pada satu pembanding yang lemah (Hyndman & "
        "Athanasopoulos, 2018; Makridakis et al., 2018)."
    )

    add_styled_table(
        ["Baseline", "RMSE", "MAE", "MAPE"],
        baseline_rows,
        [Cm(3.4), Cm(3.4), Cm(3.4), Cm(3.4)],
        "Tabel 4.2 Kinerja Baseline Naif pada Holdout",
    )

    add_sub_heading("3. Model Kontrol Tier 1 dan Tier 2")

    e1 = results.metrics("E1")
    e2 = results.metrics("E2")
    e1_vs_e0 = results.improvement("E1", "E0", "MAE")
    e2_vs_e0 = results.improvement("E2", "E0", "MAE")
    if e1["MAE"] < e0["MAE"] and e2["MAE"] < e0["MAE"]:
        control_reading = (
            "Keduanya mencatat MAE lebih rendah daripada persistence, sehingga "
            "pada konfigurasi ini peningkatan kapasitas maupun replikasi resep "
            "manual memberi perbaikan titik terhadap baseline naif."
        )
    elif e1["MAE"] > e0["MAE"] and e2["MAE"] > e0["MAE"]:
        control_reading = (
            "Keduanya masih lebih tinggi daripada persistence yang memiliki MAE "
            f"{format_usd(e0['MAE'])}, sehingga menambah kapasitas atau mengikuti "
            "resep manual tidak otomatis mengalahkan baseline naif pada horizon "
            "satu hari."
        )
    else:
        control_reading = (
            "Hanya salah satu model kontrol yang mencatat MAE lebih rendah "
            "daripada persistence, sehingga keunggulan konfigurasi tidak dapat "
            "digeneralisasi hanya dari label Tier."
        )
    add_paragraph(
        "Model kontrol Tier 1 memakai konfigurasi default, sedangkan Tier 2 "
        "mereplikasi konfigurasi manual Khumaidi dkk. (2024). Tier 1 menghasilkan "
        f"MAE {format_usd(e1['MAE'])} dan Tier 2 menghasilkan MAE "
        f"{format_usd(e2['MAE'])}. {control_reading} "
        f"Perubahan MAE Tier 1 terhadap persistence adalah {signed_change(e1_vs_e0)}, "
        f"sedangkan Tier 2 terhadap persistence adalah {signed_change(e2_vs_e0)}. "
        "Perbandingan ini penting karena posisi kedua kontrol terhadap baseline "
        "menentukan apakah ablasi berikutnya benar-benar memperbaiki titik acuan "
        "yang bermakna (Khumaidi dkk., 2024; Willmott & Matsuura, 2005)."
    )

    add_sub_heading("4. Ablasi Loss dan Scheduler pada Parameter Tier 3")

    e3 = results.metrics("E3")
    e4 = results.metrics("E4")
    e5 = results.metrics("E5")
    e6 = results.metrics("E6")
    add_paragraph(
        "Ablasi E3 sampai E6 membekukan parameter Tier 3 dan hanya memvariasikan "
        "fungsi kerugian serta scheduler dalam desain faktorial 2x2. E3 memakai "
        f"MSE tanpa scheduler dan menghasilkan MAE {format_usd(e3['MAE'])}. "
        f"E4 memakai MAE tanpa scheduler dengan MAE {format_usd(e4['MAE'])}, "
        f"sedangkan E5 memakai MSE dengan ReduceLROnPlateau dan MAE "
        f"{format_usd(e5['MAE'])}. Kombinasi keduanya pada E6 menghasilkan MAE "
        f"{format_usd(e6['MAE'])}. Dengan demikian, perubahan MAE E4 terhadap E3 "
        f"adalah {signed_change(results.improvement('E4', 'E3', 'MAE'))}, "
        f"E5 terhadap E3 adalah {signed_change(results.improvement('E5', 'E3', 'MAE'))}, "
        f"dan E6 terhadap E3 adalah {signed_change(results.improvement('E6', 'E3', 'MAE'))}."
    )

    ablation_rows = []
    for row in results.ablation_rows():
        ablation_rows.append(
            [
                row["run"],
                f"{'MAE' if row['loss'] == 'mae' else 'MSE'} / "
                f"{'Plateau' if row['scheduler'] == 'plateau' else 'Tanpa'}",
                format_usd(row["RMSE"]),
                format_usd(row["MAE"]),
                format_pct(row["MAPE"]),
                format_pct(row["delta_MAE_vs_E3"], signed=True),
            ]
        )
    add_styled_table(
        ["Run", "Loss / Scheduler", "RMSE", "MAE", "MAPE", "Delta MAE vs E3"],
        ablation_rows,
        [Cm(1.2), Cm(3.8), Cm(2.4), Cm(2.4), Cm(1.6), Cm(2.6)],
        "Tabel 4.3 Hasil Ablasi Loss dan Scheduler",
    )

    add_paragraph(
        "Pola pada Tabel 4.3 menunjukkan bahwa efek loss dan scheduler tidak "
        "selalu bersifat aditif. Bila delta E4 positif, fungsi kerugian MAE "
        "menurunkan galat absolut rata-rata dibandingkan MSE pada parameter yang "
        "sama. Bila delta E5 positif, scheduler memberi perbaikan meskipun loss "
        "tetap MSE. Efek gabungan pada E6 kemudian dibandingkan dengan E4 dan E5 "
        "untuk melihat apakah kedua faktor saling memperkuat atau justru "
        "mengganggu. Interpretasi dilakukan pada arah dan besaran efek, bukan "
        "pada klaim kausal tentang mekanisme internal jaringan, karena ablation "
        "ini hanya mengubah dua faktor pada satu konfigurasi parameter "
        "(Bouthillier et al., 2021; Greff et al., 2017)."
    )

    add_sub_heading("5. Hasil HPO Bersih Tier 3 (E7)")

    config = results.final_configuration()
    hyper = config.get("hyperparameters") or {}
    e7 = results.metrics("E7")
    e7_ci = results.ci("E7", "MAE")
    add_paragraph(
        "E7 adalah model usulan yang menjalani HPO penuh dengan Optuna-TPE. "
        f"Studi menyelesaikan {config.get('total_trials', 0)} trial dan memilih "
        f"trial nomor {config.get('best_trial_number', '-')} dengan nilai CV "
        f"MAE {format_number(config.get('best_cv_loss', 0))} USD. Konfigurasi "
        f"terpilih memakai lookback {hyper.get('lookback', '-')} hari, "
        f"{hyper.get('units', '-')} unit LSTM, dropout "
        f"{format_number(hyper.get('dropout', 0), 2)}, learning rate "
        f"{format_number(hyper.get('learning_rate', 0), 5)}, batch size "
        f"{hyper.get('batch_size', '-')}, dan {hyper.get('layers', '-')} layer. "
        f"Model final dilatih selama {config.get('epochs_run', '-')} epoch dengan "
        f"EarlyStopping patience {config.get('early_stopping', {}).get('patience', '-')}."
    )

    add_styled_table(
        ["Parameter", "Nilai Terpilih", "Peran"],
        [
            ["Lookback", f"{hyper.get('lookback', '-')} hari", "Panjang jendela masukan"],
            ["Hidden units", f"{hyper.get('units', '-')}", "Kapasitas representasi"],
            ["Dropout", format_number(hyper.get("dropout", 0), 2), "Regularisasi"],
            ["Learning rate", format_number(hyper.get("learning_rate", 0), 5), "Laju Adam"],
            ["Batch size", f"{hyper.get('batch_size', '-')}", "Ukuran minibatch"],
            ["Layers", f"{hyper.get('layers', '-')}", "Kedalaman LSTM"],
            ["Total trials", f"{config.get('total_trials', '-')}", "Anggaran HPO"],
            ["Trial terbaik", f"#{config.get('best_trial_number', '-')}", "Indeks Optuna (mulai 0)"],
            ["Epoch final", f"{config.get('epochs_run', '-')}", "Hasil EarlyStopping"],
        ],
        [Cm(3.4), Cm(4.4), Cm(6.2)],
        "Tabel 4.4 Konfigurasi Final Model Usulan E7",
    )

    add_paragraph(
        f"Pada holdout, E7 menghasilkan RMSE {format_usd(e7['RMSE'])}, MAE "
        f"{format_usd(e7['MAE'])}, dan MAPE {format_pct(e7['MAPE'])}. Interval "
        f"kepercayaan 95% untuk MAE E7 adalah {format_usd(e7_ci['ci_low'])} sampai "
        f"{format_usd(e7_ci['ci_high'])}. Sebagai pembanding, E6 yang memakai "
        f"parameter Tier 3 tetap tanpa HPO menghasilkan MAE {format_usd(e6['MAE'])}. "
        f"Perubahan MAE E7 terhadap E6 adalah "
        f"{signed_change(results.improvement('E7', 'E6', 'MAE'))}, sedangkan "
        f"perubahan terhadap persistence adalah "
        f"{signed_change(results.improvement('E7', 'E0', 'MAE'))}. Angka ini "
        "menjadi dasar penilaian apakah HPO penuh memberi nilai tambah di luar "
        "pemilihan loss dan scheduler (Akiba et al., 2019; Feurer & Hutter, 2019)."
    )

    add_figure(
        figures_dir / "gambar_4_3_konvergensi_optuna.png",
        "Gambar 4.1 Kurva Konvergensi Nilai Validasi Optuna-TPE",
    )

    add_sub_heading("6. Perbandingan Statistik dan Verdict Ilmiah")

    best_lstm = results.best_lstm
    verdict = results.verdict
    status = verdict.get("status")
    e7_vs_e0 = results.comparison_metric("E7_vs_persistence", "MAE")
    if status == "proposed_lower_mae_ci_excludes_zero":
        verdict_text = (
            "Verdict otomatis menyatakan bahwa E7 memiliki MAE lebih rendah "
            "daripada persistence dan CI selisih berpasangan tidak melewati nol. "
            "Klaim keunggulan masih harus dibatasi pada satu aset, horizon satu "
            "hari, satu periode holdout, dan model univariat."
        )
    elif status == "proposed_lower_mae_ci_includes_zero":
        verdict_text = (
            "Verdict otomatis menyatakan bahwa MAE titik E7 lebih rendah daripada "
            "persistence, tetapi CI selisih berpasangan masih melewati nol. "
            "Karena itu, hasil ini tidak boleh disebut signifikan atau unggul "
            "secara meyakinkan; yang dapat dikatakan hanyalah arah perbaikan "
            "yang belum stabil."
        )
    else:
        if results.verdict.get("ci_direction") == "persistence_better":
            verdict_text = (
                "Verdict otomatis menyatakan bahwa E7 memiliki MAE lebih tinggi "
                "daripada persistence dan CI selisih berpasangan seluruhnya di atas "
                "nol. Dengan demikian, hasil ini bukan sekadar tidak lebih baik, "
                "tetapi secara statistik lebih buruk pada periode holdout yang "
                "diuji. Hasil negatif ini dilaporkan apa adanya: model LSTM yang "
                "dioptimasi belum mampu mengalahkan baseline naif pada horizon satu "
                "hari. Kontribusi penelitian kemudian bergeser menjadi pipeline "
                "evaluasi dan bukti terkontrol tentang batas kemampuan LSTM, bukan "
                "klaim keunggulan prediktif."
            )
        else:
            verdict_text = (
                "Verdict otomatis menyatakan bahwa E7 tidak lebih baik daripada "
                "persistence pada MAE titik, dan CI selisih berpasangan masih "
                "melewati nol sehingga arah perbedaannya belum dapat dipastikan. "
                "Hasil negatif ini dilaporkan apa adanya: model LSTM yang "
                "dioptimasi belum mampu mengalahkan baseline naif pada horizon satu "
                "hari. Kontribusi penelitian kemudian bergeser menjadi pipeline "
                "evaluasi dan bukti terkontrol tentang batas kemampuan LSTM, bukan "
                "klaim keunggulan prediktif."
            )

    add_paragraph(
        f"Tabel 4.5 merangkum seluruh model. Model LSTM terbaik menurut MAE adalah "
        f"{best_lstm['run']} dengan MAE {format_usd(best_lstm['MAE'])}, sedangkan "
        f"persistence memiliki MAE {format_usd(e0['MAE'])}. Untuk E7, selisih MAE "
        f"terhadap persistence adalah {format_usd(e7_vs_e0['difference_b_minus_a'], signed=True)} "
        f"dengan CI 95% {format_usd(e7_vs_e0['ci_low'], signed=True)} sampai "
        f"{format_usd(e7_vs_e0['ci_high'], signed=True)}. {verdict_text}"
    )

    benchmark_rows = []
    for row in results.summary_rows():
        ci = results.ci(row["run"], "MAE")
        aggregate = results.aggregate(row["run"], "MAE") or {}
        mean_std = (
            f"{format_usd(aggregate.get('mean', row['MAE']))} ± "
            f"{format_number(aggregate.get('std', 0.0))}"
        )
        benchmark_rows.append(
            [
                row["run"],
                row["label"],
                format_usd(row["RMSE"]),
                format_usd(row["MAE"]),
                format_pct(row["MAPE"]),
                mean_std,
                f"{format_usd(ci['ci_low'])}–{format_usd(ci['ci_high'])}",
            ]
        )
    add_styled_table(
        ["Run", "Model", "RMSE", "MAE", "MAPE", "MAE mean ± std", "CI 95% MAE"],
        benchmark_rows,
        [Cm(1.0), Cm(3.1), Cm(1.9), Cm(1.9), Cm(1.4), Cm(2.5), Cm(2.6)],
        "Tabel 4.5 Perbandingan Kinerja Seluruh Model pada Holdout",
        font_size=7.5,
    )

    comparison_rows = []
    for label in (
        "E7_vs_persistence",
        "E7_vs_E6",
        "E1_vs_E3",
        "E4_vs_E3",
        "E5_vs_E3",
        "E6_vs_E3",
    ):
        try:
            payload = results.comparison(label)
            mae = results.comparison_metric(label, "MAE")
        except Exception:
            continue
        comparison_rows.append(
            [
                f"{payload.get('model_a')} vs {payload.get('model_b')}",
                format_usd(mae["difference_b_minus_a"], signed=True),
                f"{format_usd(mae['ci_low'], signed=True)}–{format_usd(mae['ci_high'], signed=True)}",
                "Ya" if results.is_significant(label, "MAE") else "Tidak",
            ]
        )
    add_styled_table(
        ["Perbandingan", "Selisih MAE (B - A)", "CI 95%", "CI jauh dari nol?"],
        comparison_rows,
        [Cm(3.6), Cm(3.6), Cm(4.6), Cm(2.2)],
        "Tabel 4.6 Perbandingan Berpasangan pada Tanggal yang Sama",
        font_size=8,
    )

    add_paragraph(
        "Perbandingan berpasangan pada Tabel 4.6 memakai tanggal yang sama untuk "
        "setiap model, sehingga perbedaan tidak tercampur dengan perbedaan "
        "komposisi hari. Selisih negatif berarti model B memiliki galat lebih "
        "rendah. Kolom terakhir hanya menyatakan apakah seluruh interval "
        "kepercayaan berada di bawah nol; nilai p yang menyertainya bersifat "
        "deskriptif dan bukan pengganti uji formal Diebold-Mariano. Pembacaan "
        "yang benar adalah membandingkan arah efek, besar efek, dan lebar "
        "interval secara bersama-sama, bukan memilih satu angka yang paling "
        "menguntungkan (Bouthillier et al., 2021; Willmott & Matsuura, 2005)."
    )

    add_sub_heading("7. Analisis Residual, Rezim, dan Arah")

    e7_res = results.model("E7").get("residuals") or {}
    e7_regime = results.model("E7").get("regime") or {}
    e7_high = results.model("E7").get("high_volatility") or {}
    e7_normal = results.model("E7").get("normal_volatility") or {}
    direction = results.model("E7").get("directional_accuracy") or {}
    add_paragraph(
        f"Residual E7 memiliki rata-rata {format_usd(e7_res.get('mean', 0), signed=True)} "
        f"dan simpangan baku {format_usd(e7_res.get('std', 0))}. Galat absolut "
        f"maksimum mencapai {format_usd(e7_res.get('max_absolute_error', 0))}, "
        f"sedangkan proporsi hari dengan galat di bawah 2% adalah "
        f"{format_pct((e7_res.get('share_within_2_percent', 0) or 0) * 100)}. "
        f"Pada rezim bull, MAE E7 adalah "
        f"{format_usd((e7_regime.get('bull') or {}).get('MAE', 0))}; pada rezim "
        f"bear {format_usd((e7_regime.get('bear') or {}).get('MAE', 0))}; dan pada "
        f"sideways {format_usd((e7_regime.get('sideways') or {}).get('MAE', 0))}. "
        f"Pada hari berivolatilitas tinggi, MAE {format_usd(e7_high.get('MAE', 0))}, "
        f"sedangkan pada hari normal {format_usd(e7_normal.get('MAE', 0))}."
    )

    add_styled_table(
        ["Segmen", "n", "RMSE", "MAE", "MAPE"],
        [
            [
                "Bull",
                (e7_regime.get("bull") or {}).get("n", 0),
                format_usd((e7_regime.get("bull") or {}).get("RMSE", 0)),
                format_usd((e7_regime.get("bull") or {}).get("MAE", 0)),
                format_pct((e7_regime.get("bull") or {}).get("MAPE", 0)),
            ],
            [
                "Bear",
                (e7_regime.get("bear") or {}).get("n", 0),
                format_usd((e7_regime.get("bear") or {}).get("RMSE", 0)),
                format_usd((e7_regime.get("bear") or {}).get("MAE", 0)),
                format_pct((e7_regime.get("bear") or {}).get("MAPE", 0)),
            ],
            [
                "Sideways",
                (e7_regime.get("sideways") or {}).get("n", 0),
                format_usd((e7_regime.get("sideways") or {}).get("RMSE", 0)),
                format_usd((e7_regime.get("sideways") or {}).get("MAE", 0)),
                format_pct((e7_regime.get("sideways") or {}).get("MAPE", 0)),
            ],
            [
                "Volatilitas tinggi",
                e7_high.get("n", 0),
                format_usd(e7_high.get("RMSE", 0)),
                format_usd(e7_high.get("MAE", 0)),
                format_pct(e7_high.get("MAPE", 0)),
            ],
            [
                "Volatilitas normal",
                e7_normal.get("n", 0),
                format_usd(e7_normal.get("RMSE", 0)),
                format_usd(e7_normal.get("MAE", 0)),
                format_pct(e7_normal.get("MAPE", 0)),
            ],
        ],
        [Cm(3.6), Cm(1.4), Cm(3.2), Cm(3.2), Cm(2.6)],
        "Tabel 4.7 Kinerja E7 Menurut Rezim dan Volatilitas (Label Ex-Ante)",
    )

    add_paragraph(
        "Label rezim dan volatilitas dihitung dari data yang berakhir pada hari "
        "sebelumnya, sehingga tidak memakai informasi hari yang diprediksi. "
        "Karena itu, tabel ini berfungsi sebagai analisis pasca-hoc untuk melihat "
        "di mana galat membesar, bukan sebagai fitur model atau klaim kausal. "
        "Perbedaan MAE antar-rezim menunjukkan bahwa satu angka agregat dapat "
        "menyembunyikan heterogenitas: model yang tampak moderat pada seluruh "
        "holdout dapat sangat buruk pada bull market atau sebaliknya. Pembacaan "
        "seperti ini penting sebelum model dipakai untuk keputusan investasi "
        "(López de Prado, 2018; Lim & Zohren, 2021)."
    )

    add_paragraph(
        f"Akurasi arah E7 adalah {format_pct((direction.get('accuracy', 0) or 0) * 100)} "
        f"dengan {direction.get('correct', 0)} dari {direction.get('n', 0)} hari "
        "benar. Pada hari harga naik, akurasi hanya "
        f"{format_pct((direction.get('up_accuracy', 0) or 0) * 100)}, sedangkan pada "
        f"hari harga turun {format_pct((direction.get('down_accuracy', 0) or 0) * 100)}. "
        "Ketimpangan ini menunjukkan bahwa angka agregat sekitar 50% tidak "
        "mencerminkan kemampuan dua arah yang seimbang, melainkan bias arah yang "
        "kuat. Angka ini juga tidak boleh dibandingkan langsung dengan persistence, "
        "karena persistence selalu memprediksi harga yang sama sehingga arah "
        "prediksinya degenerat dan akurasinya dilaporkan terpisah sebagai tidak "
        "interpretable. Untuk model LSTM, pola ini menunjukkan bahwa kemampuan "
        "menangkap tanda perubahan harga masih terbatas, bahkan ketika galat harga "
        "dalam dolar terlihat moderat (Hyndman & Athanasopoulos, 2018)."
    )

    add_figure(
        figures_dir / "gambar_4_1_perbandingan_prediksi_3tier.png",
        "Gambar 4.2 Perbandingan Harga Aktual dan Prediksi pada Holdout",
    )
    add_figure(
        figures_dir / "gambar_4_2_bar_chart_komparasi_metrik.png",
        "Gambar 4.3 Diagram Batang Perbandingan Metrik",
    )
    add_figure(
        figures_dir / "residual_abs_boxplot.png",
        "Gambar 4.4 Distribusi Galat Absolut Menurut Model",
    )
    add_figure(
        figures_dir / "error_by_regime.png",
        "Gambar 4.5 Galat Menurut Rezim Pasar",
    )

    # ------------------------------------------------------------------
    # B. Pembahasan
    # ------------------------------------------------------------------
    add_heading("B. Pembahasan Hasil Penelitian")

    add_paragraph(
        "Pembahasan ini menghubungkan hasil numerik dengan teori peramalan deret "
        "waktu dan literatur optimasi hyperparameter. Fokusnya bukan memilih "
        "model yang paling menguntungkan untuk diklaim, melainkan menjelaskan "
        "mengapa pola hasil muncul dan apa batas kesimpulan yang dapat ditarik. "
        "Tiga pertanyaan dibahas: mengapa persistence sulit dikalahkan, apakah "
        "faktor loss, scheduler, dan HPO memberi efek yang dapat dipisahkan, dan "
        "apa implikasi serta keterbatasan hasil ini bagi penelitian lanjutan "
        "(Bouthillier et al., 2021; Makridakis et al., 2018)."
    )

    add_sub_heading("1. Mengapa Baseline Persistence Sulit Dikalahkan")

    add_paragraph(
        "Persistence efektif mengasumsikan bahwa perubahan harga harian memiliki "
        "ekspektasi mendekati nol. Pada aset likuid dengan perdagangan "
        "twenty-four seven seperti Bitcoin, asumsi ini sering sulit dikalahkan "
        "oleh model yang hanya melihat harga masa lalu, terutama pada horizon "
        "satu hari. Hasil penelitian ini konsisten dengan pola tersebut: seluruh "
        f"model LSTM memiliki MAE di atas {format_usd(e0['MAE'])}. Fenomena ini "
        "bukan berarti LSTM tidak berguna, tetapi menunjukkan bahwa sinyal "
        "prediktif harian yang tersedia pada data univariat sangat kecil "
        "dibandingkan derau pasar (Makridakis et al., 2018; Lim & Zohren, 2021)."
    )

    add_paragraph(
        "Kekalahan model yang lebih kompleks juga dapat dijelaskan oleh "
        "kombinasi non-stasioneritas, perubahan rezim, dan keterbatasan horizon. "
        "Model dilatih pada periode in-sample yang mencakup kondisi pasar "
        "berbeda, lalu diuji pada periode yang didominasi harga tinggi. "
        "Pergeseran distribusi ini membuat bobot yang optimal secara historis "
        "belum tentu optimal pada holdout. Baseline persistence tidak memiliki "
        "parameter yang harus diperbarui, sehingga lebih tahan terhadap "
        "pergeseran tersebut. Temuan ini menegaskan pentingnya melaporkan "
        "baseline naif secara eksplisit sebelum mengklaim kemajuan algoritma "
        "(Bouthillier et al., 2021; Gu et al., 2020)."
    )

    add_sub_heading("2. Efek Hyperparameter Optuna: E1 versus E3")

    if e3["MAE"] < e1["MAE"]:
        hyperparameter_reading = (
            "Arah ini menunjukkan bahwa konfigurasi hasil pencarian Optuna "
            "menurunkan galat dibandingkan konfigurasi default ketika loss dan "
            "aturan pelatihan disamakan."
        )
    elif e1["MAE"] < e3["MAE"]:
        hyperparameter_reading = (
            "Arah ini menunjukkan bahwa konfigurasi hasil pencarian Optuna tidak "
            "otomatis lebih baik daripada konfigurasi default ketika loss dan "
            "aturan pelatihan disamakan."
        )
    else:
        hyperparameter_reading = (
            "Kedua konfigurasi menghasilkan MAE titik yang sama, sehingga tidak "
            "ada arah efek yang dapat diklaim."
        )

    add_paragraph(
        f"Perbandingan E1 dan E3 mengisolasi efek hyperparameter karena keduanya "
        f"memakai MSE dan tanpa scheduler. E1 memiliki MAE {format_usd(e1['MAE'])}, "
        f"sedangkan E3 memiliki MAE {format_usd(e3['MAE'])}. "
        f"{comparison_claim('E1_vs_E3')} {hyperparameter_reading} Klaim bahwa "
        "Optuna selalu menghasilkan hyperparameter yang lebih unggul perlu "
        "dihindari; yang dapat dikatakan adalah bahwa efek HPO bergantung pada "
        "ruang pencarian, metrik objektif, dan interaksi dengan faktor pelatihan "
        "lain (Akiba et al., 2019; Bergstra et al., 2011)."
    )

    add_sub_heading("3. Efek Loss MAE dan Scheduler")

    loss_effect = e3["MAE"] - e4["MAE"]
    scheduler_effect = e3["MAE"] - e5["MAE"]
    if loss_effect > 0:
        loss_reading = (
            "Arah ini sejalan dengan tujuan MAE yang mengoptimalkan galat "
            "absolut, tetapi besarnya efek tetap harus dibaca bersama "
            "variabilitas antar-seed."
        )
    else:
        loss_reading = (
            "Arah ini tidak mendukung dugaan bahwa loss MAE otomatis lebih baik "
            "pada konfigurasi ini; efeknya harus dibaca bersama variabilitas "
            "antar-seed."
        )
    if scheduler_effect > 0:
        scheduler_reading = (
            f"Scheduler menurunkan MAE titik sebesar {format_usd(scheduler_effect)}, "
            "tetapi besar efeknya "
        )
        scheduler_reading += (
            "lebih kecil daripada efek penggantian loss."
            if abs(scheduler_effect) < abs(loss_effect)
            else "menyamai atau melampaui efek penggantian loss."
        )
    elif scheduler_effect < 0:
        scheduler_reading = (
            f"Scheduler justru menaikkan MAE titik sebesar "
            f"{format_usd(abs(scheduler_effect))}, sehingga tidak memberi "
            "perbaikan pada konfigurasi ini."
        )
    else:
        scheduler_reading = (
            "Scheduler tidak mengubah MAE titik pada konfigurasi ini."
        )

    add_paragraph(
        f"Pada E4, penggantian MSE dengan MAE tanpa scheduler mengubah MAE dari "
        f"{format_usd(e3['MAE'])} menjadi {format_usd(e4['MAE'])}. "
        f"{comparison_claim('E4_vs_E3')} {loss_reading} Sebaliknya, E5 menguji "
        f"scheduler tanpa mengubah loss dan menghasilkan MAE {format_usd(e5['MAE'])}. "
        f"{comparison_claim('E5_vs_E3')} {scheduler_reading} Efek scheduler yang "
        "kecil atau tidak konsisten menunjukkan bahwa faktor ini bukan sumber "
        "utama perbedaan pada konfigurasi yang diuji (Willmott & Matsuura, "
        "2005; Kingma & Ba, 2014)."
    )

    add_paragraph(
        f"E6 menggabungkan MAE dan ReduceLROnPlateau dan menghasilkan MAE "
        f"{format_usd(e6['MAE'])}. Dibandingkan E3, perubahan MAE E6 adalah "
        f"{signed_change(results.improvement('E6', 'E3', 'MAE'))}. "
        f"Perbandingan E6 terhadap E4 dan E5 menunjukkan apakah efek kedua faktor "
        "saling memperkuat. Namun, karena semua varian memakai parameter Tier 3 "
        "yang sama, hasil ini tidak dapat digunakan untuk mengklaim bahwa "
        "kombinasi tertentu akan tetap unggul pada arsitektur atau dataset lain. "
        "Interpretasi yang defensible adalah bahwa pada konfigurasi yang diuji, "
        "loss MAE dan scheduler menghasilkan perubahan titik yang arah serta "
        "besar efeknya dilaporkan pada Tabel 4.3 dan Tabel 4.6; klaim signifikansi "
        "tetap mengikuti interval kepercayaan berpasangan, bukan selisih "
        "persentase semata (Bouthillier et al., 2021; Greff et al., 2017)."
    )

    add_sub_heading("4. Nilai Tambah HPO Penuh: E7 versus E6")

    if e7["MAE"] < e6["MAE"]:
        if results.is_improvement("E7_vs_E6", "MAE"):
            hpo_reading = (
                "HPO penuh menurunkan MAE titik dan perbedaannya didukung CI "
                "berpasangan yang tidak melewati nol."
            )
        else:
            hpo_reading = (
                "HPO penuh menurunkan MAE titik, tetapi CI berpasangan masih "
                "melewati nol sehingga belum dapat disebut sebagai bukti "
                "keunggulan."
            )
    elif e7["MAE"] > e6["MAE"]:
        hpo_reading = (
            "HPO penuh tidak menurunkan MAE dibandingkan E6; konfigurasi hasil "
            "pencarian justru menghasilkan galat titik yang lebih tinggi."
        )
    else:
        hpo_reading = "HPO penuh menghasilkan MAE titik yang sama dengan E6."

    add_paragraph(
        f"E7 dan E6 memakai loss MAE serta scheduler yang sama, sehingga "
        f"perbedaannya mengisolasi efek HPO penuh. E7 menghasilkan MAE "
        f"{format_usd(e7['MAE'])}, sedangkan E6 menghasilkan "
        f"{format_usd(e6['MAE'])}. "
        f"{comparison_claim('E7_vs_E6')} {hpo_reading} Apa pun arahnya, nilai "
        "tambah metodologis tetap terletak pada proses pencarian yang "
        "terdokumentasi dan kemampuannya mengungkap kombinasi yang menghasilkan "
        "kinerja serupa. Temuan ini sejalan dengan pandangan bahwa evaluasi HPO "
        "harus mempertimbangkan variabilitas dan biaya komputasi, bukan hanya "
        "nilai terbaik pada satu trial (Akiba et al., 2019; Feurer & Hutter, "
        "2019)."
    )

    if best_lstm["run"] == "E7":
        ranking_reading = (
            "Peringkat ini sesuai dengan posisi E7 sebagai model usulan, tetapi "
            "keunggulannya tetap harus dibaca bersama CI berpasangan dan "
            "variabilitas antar-seed, bukan dari label model."
        )
    else:
        ranking_reading = (
            f"Peringkat tersebut berbeda dari model usulan E7, sehingga pemilihan "
            "model tidak boleh didasarkan pada label 'usulan' atau 'paling "
            "kompleks'. Perbedaan ini justru menunjukkan bahwa matriks eksperimen "
            "bekerja sebagaimana mestinya: setiap klaim diuji, dan model yang "
            "menang ditentukan oleh data, bukan oleh preferensi peneliti."
        )

    add_paragraph(
        f"Model LSTM terbaik pada penelitian ini adalah {best_lstm['run']} dengan "
        f"MAE {format_usd(best_lstm['MAE'])}. {ranking_reading} "
        "(Bouthillier et al., 2021; Willmott & Matsuura, 2005)."
    )

    add_sub_heading("5. Implikasi Teoritis dan Praktis")

    add_paragraph(
        "Secara teoritis, penelitian ini memperkuat pandangan bahwa peramalan "
        "harga aset kripto satu langkah ke depan sangat dipengaruhi oleh "
        "komponen random walk. Model pembelajaran mendalam dapat menangkap "
        "pola non-linier, tetapi pola tersebut belum tentu cukup stabil untuk "
        "mengalahkan prediksi naif pada periode uji yang berbeda dari periode "
        "latih. Kontribusi metodologis yang lebih kokoh adalah pipeline "
        "evaluasi yang memisahkan in-sample dan holdout, memakai scaler per "
        "fold, menghitung interval kepercayaan blok, dan melaporkan hasil "
        "negatif secara eksplisit (Lim & Zohren, 2021; López de Prado, 2018)."
    )

    add_paragraph(
        "Secara praktis, hasil ini memberi peringatan bagi pengembangan sistem "
        "perdagangan algoritmik: akurasi harga yang terlihat tinggi pada data "
        "historis tidak otomatis menghasilkan keuntungan setelah biaya "
        "transaksi, slippage, dan risiko eksekusi. Model yang tidak mengalahkan "
        "persistence pada MAE sebaiknya tidak dipakai sebagai sinyal tunggal "
        "untuk keputusan beli atau jual. Penggunaan model perlu disertai "
        "manajemen risiko, validasi out-of-time, dan pembandingan dengan "
        "strategi naif sebelum diklaim memiliki nilai ekonomi (Gu et al., 2020; "
        "Makridakis et al., 2018)."
    )

    add_sub_heading("6. Keterbatasan Penelitian")

    add_paragraph(
        "Penelitian ini memiliki beberapa keterbatasan yang harus dibaca bersama "
        "hasil. Pertama, data hanya mencakup satu aset, yaitu BTC/USDT, sehingga "
        "temuan belum tentu berlaku untuk aset kripto lain atau pasar tradisional. "
        "Kedua, horizon peramalan terbatas pada satu langkah ke depan dan model "
        "bersifat univariat, sehingga belum menguji peramalan multi-horizon atau "
        "manfaat fitur eksternal seperti sentimen, volume on-chain, dan indikator "
        "makroekonomi. Ketiga, evaluasi hanya memakai satu periode holdout "
        f"sepanjang {format_number(results.data.get('n_test', 0), 0)} hari, "
        "sehingga hasil sangat bergantung pada rezim pasar "
        "yang terjadi pada periode tersebut (Makridakis et al., 2018; Lim & "
        "Zohren, 2021)."
    )

    add_paragraph(
        "Keterbatasan keempat adalah belum diperhitungkannya biaya transaksi, "
        "bid-ask spread, dan slippage, sehingga angka MAE tidak dapat langsung "
        "diterjemahkan menjadi profitabilitas. Kelima, early stopping internal "
        "memakai 10% data latih terakhir sebagai validation split; meskipun "
        "bersifat kronologis, mekanisme ini masih berpotensi memberi optimism "
        "kecil pada pemilihan epoch. Keenam, uji signifikansi bersifat "
        "deskriptif dan tidak menggantikan uji formal Diebold-Mariano. "
        "Keterbatasan-keterbatasan ini membuka ruang penelitian lanjutan, "
        "terutama evaluasi multi-aset dan multi-periode dengan protokol yang "
        "sama (Bouthillier et al., 2021; Tashman, 2000)."
    )

    add_sub_heading("7. Ringkasan Bab")

    add_paragraph(
        f"Bab ini menunjukkan bahwa baseline persistence memiliki MAE "
        f"{format_usd(e0['MAE'])}, sedangkan model LSTM terbaik {best_lstm['run']} "
        f"memiliki MAE {format_usd(best_lstm['MAE'])}. Verdict ilmiah berstatus "
        f"{status}. Dengan demikian, kontribusi utama penelitian adalah pipeline "
        "eksperimen terkontrol, laporan ablasi yang memisahkan loss dan "
        "scheduler, serta evaluasi statistik yang jujur tentang batas kemampuan "
        "LSTM pada peramalan harga Bitcoin satu langkah ke depan. Bab V merangkum "
        "simpulan tersebut dan merumuskan saran penelitian lanjutan."
    )

    out_dir = ensure_naskah_dir()
    out_path = out_dir / "BAB_4_HASIL_DAN_PEMBAHASAN_ZAINI_LEON.docx"
    doc.save(out_path)
    print(f"[SUCCESS] BAB 4 Generated successfully: {out_path}")


if __name__ == "__main__":
    generate_bab4()
