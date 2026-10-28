"""Generate the Study 2 title-submission form (DOCX) in the campus table format.

Output: 02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2.docx
Source of truth for prose: 02_Pengajuan_Judul/PENGAJUAN_JUDUL_STUDY2.md
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "02_Pengajuan_Judul" / "PENGAJUAN_JUDUL_STUDY2.docx"

JUDUL = ("Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna "
         "pada Prediksi Volatilitas Bitcoin")

LATAR = [
    "Bitcoin merupakan aset kripto dengan kapitalisasi pasar terbesar dan volatilitas tinggi. "
    "Volatilitas digunakan untuk manajemen risiko, Value-at-Risk, alokasi portofolio, dan harga derivatif.",
    "Volatilitas Bitcoin menunjukkan volatility clustering, sehingga memiliki struktur yang dapat dimodelkan "
    "dan diprediksi; berbeda dengan harga harian yang mendekati random walk.",
    "Model klasik GARCH(1,1) dan HAR-RV kuat secara interpretasi, tetapi terbatas pada hubungan linear "
    "dan bentuk fungsional yang telah ditentukan.",
    "LSTM mampu menangkap pola non-linear dan dependensi jangka panjang, namun kinerjanya sensitif terhadap "
    "hyperparameter: lookback, units, dropout, learning rate, dan batch size.",
    "Optuna dengan Tree-structured Parzen Estimator (TPE) menyediakan optimasi hyperparameter yang sistematis. "
    "Namun banyak studi melakukan tuning dan evaluasi pada periode yang sama, tanpa baseline naif, tanpa QLIKE, "
    "dan tanpa periode uji eksternal sehingga klaim peningkatan berisiko optimistic bias.",
    "Penelitian ini membangun pipeline optimasi hyperparameter LSTM berbasis Optuna yang bebas kebocoran data, "
    "menggunakan realized variance dari kline 1 jam BTC/USDT, baseline persistence/HAR-RV/GARCH(1,1)/LSTM default, "
    "metrik QLIKE, serta uji eksternal 2026 yang tidak dipakai dalam pelatihan maupun optimasi.",
]

RUMUSAN = [
    "Bagaimana merancang pipeline optimasi hyperparameter LSTM berbasis Optuna yang bebas kebocoran data "
    "untuk prediksi realized volatility Bitcoin?",
    "Sejauh mana model LSTM yang dioptimasi Optuna mampu mengungguli baseline persistence dalam memprediksi "
    "realized volatility Bitcoin pada periode uji eksternal 2026?",
    "Apakah model LSTM yang dioptimasi Optuna mampu menyaingi baseline ekonometrik HAR-RV dan GARCH(1,1) "
    "pada periode uji eksternal?",
    "Bagaimana konsistensi kinerja model LSTM yang dioptimasi Optuna antara periode validasi 2024–2025 dan "
    "periode uji eksternal 2026 yang tidak digunakan dalam pelatihan maupun optimasi?",
]

REFERENSI = [
    "Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735-1780.",
    "Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. KDD '19.",
    "Andersen, T. G., & Bollerslev, T. (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. International Economic Review, 39(4), 885-905.",
    "Corsi, F. (2009). A simple approximate long-memory model of realized volatility. Journal of Financial Econometrics, 7(2), 174-196.",
    "Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. Journal of Econometrics, 31(3), 307-327.",
    "Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility proxies. Journal of Econometrics, 160(1), 246-256.",
    "Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. Journal of Business & Economic Statistics, 13(3), 253-263.",
    "Bergmeir, C., & Benitez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. Information Sciences, 191, 192-213.",
    "Bouthillier, X., et al. (2021). Accounting for variance in machine learning benchmarks. MLSys 2021.",
]


def set_cell_text(cell, text: str, bold: bool = False) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.bold = bold


def main() -> None:
    doc = Document()
    section = doc.sections[0]
    section.page_height, section.page_width = Cm(29.7), Cm(21.0)
    for attr in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(section, attr, Cm(2.5))

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    head = doc.add_paragraph()
    head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = head.add_run("FORMULIR PENGAJUAN JUDUL SKRIPSI")
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = "Times New Roman"

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run("Program Studi Teknik Informatika - Fakultas Sains dan Teknologi\n"
                    "Universitas Islam Nahdlatul Ulama (UNISNU) Jepara")
    r.font.size = Pt(11)
    r.font.name = "Times New Roman"
    doc.add_paragraph()

    rows = [
        ("Nama", ":", "Zaini Leon Musthofa Kamal"),
        ("NIM", ":", "231240001455"),
        ("Judul Penelitian", ":", JUDUL),
        ("Latar Belakang (Poinnya)", ":", "\n".join(f"{i}. {t}" for i, t in enumerate(LATAR, 1))),
        ("Rumusan Masalah", ":", "\n".join(f"{i}. {t}" for i, t in enumerate(RUMUSAN, 1))),
        ("Referensi/Pustaka Utama", ":", "\n".join(f"[{i}] {t}" for i, t in enumerate(REFERENSI, 1))),
    ]

    table = doc.add_table(rows=len(rows), cols=4)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (label, colon, content) in enumerate(rows):
        cells = table.rows[i].cells
        set_cell_text(cells[0], label, bold=True)
        set_cell_text(cells[1], colon)
        merged = cells[2].merge(cells[3])
        set_cell_text(merged, content)
        cells[0].width = Cm(4.2)
        cells[1].width = Cm(0.6)

    doc.add_paragraph()
    ttd = doc.add_paragraph()
    ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ttd.add_run("Jepara, ................................\n\nPengusul,\n\n\n\n")
    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = name.add_run("Zaini Leon Musthofa Kamal\nNIM. 231240001455")
    r.bold = True

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"written: {OUT}")


if __name__ == "__main__":
    main()
