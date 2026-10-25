"""
generate_back_matter.py
Membuat Bagian Akhir (Back Matter) Skripsi UNISNU Jepara:
- DAFTAR PUSTAKA (32 Referensi Ilmiah Lengkap Format APA 7th Edition, Urut Abjad A-Z)
- LAMPIRAN:
  - Lampiran 1: Ringkasan Kode Program Pipeline Komputasi Python (01 s.d. 08)
  - Lampiran 2: Sampel Data Historis Transaksi Harian Binance BTC/USDT Periode 2020–2025
  - Lampiran 3: Log Riwayat 50 Trial Optimasi Bayesian Optuna-TPE
"""

import os
import pandas as pd
import docx
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from doc_paths import SOURCE_ROOT
from reference_data import REFERENCES, apa_reference
from results_context import FinalResults

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic

def format_cell(cell, top_border=True, bottom_border=True, left_border=False, right_border=False):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = 'single' if top_border else 'none'
    bb = 'single' if bottom_border else 'none'
    lb = 'single' if left_border else 'none'
    rb = 'single' if right_border else 'none'
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{tb}" w:sz="4" w:space="0" w:color="000000"/>
            <w:bottom w:val="{bb}" w:sz="4" w:space="0" w:color="000000"/>
            <w:left w:val="{lb}" w:sz="4" w:space="0" w:color="000000"/>
            <w:right w:val="{rb}" w:sz="4" w:space="0" w:color="000000"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def generate_back_matter(output_path=None):
    if output_path is None:
        output_path = str(SOURCE_ROOT / "back_matter.docx")
    results = FinalResults.load()
    config = results.final_configuration()
    best_trial_number = int(config.get("best_trial_number", -1))
    doc = docx.Document()
    
    # Page Setup UNISNU
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(4.0)
    sec.left_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # =========================================================================
    # DAFTAR PUSTAKA
    # =========================================================================
    p_dp = doc.add_paragraph()
    p_dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dp.paragraph_format.space_before = Pt(0)
    p_dp.paragraph_format.space_after = Pt(24)
    r_dp = p_dp.add_run("DAFTAR PUSTAKA")
    set_font(r_dp, "Times New Roman", 14, bold=True)

    # 32 Referensi Lengkap Format APA 7th Edition (Urut Abjad A - Z)
    references = [
        apa_reference(ref)
        for ref in sorted(REFERENCES, key=lambda item: (item["first_author"].lower(), item["year"]))
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Cm(1.0)
        p_ref.paragraph_format.first_line_indent = Cm(-1.0)
        r = p_ref.add_run(ref)
        set_font(r, "Times New Roman", 12)

    doc.add_page_break()

    # =========================================================================
    # LAMPIRAN 1: RINGKASAN KODE PIPELINE KOMPUTASI PYTHON
    # =========================================================================
    p_lp1 = doc.add_paragraph()
    p_lp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lp1.paragraph_format.space_before = Pt(0)
    p_lp1.paragraph_format.space_after = Pt(6)
    r = p_lp1.add_run("LAMPIRAN 1\nRINGKASAN KODE PROGRAM PIPELINE KOMPUTASI PYTHON")
    set_font(r, "Times New Roman", 12, bold=True)

    p_desc1 = doc.add_paragraph()
    p_desc1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc1.paragraph_format.line_spacing = 1.5
    p_desc1.paragraph_format.first_line_indent = Cm(1.0)
    p_desc1.paragraph_format.space_after = Pt(12)
    r = p_desc1.add_run(
        "Berikut merupakan ringkasan modul-modul skrip Python yang dirancang dan dieksekusi dalam lingkungan eksperimen "
        "komputasi penelitian, mencakup penarikan data Binance API, pra-pemrosesan bebas kebocoran, pelatihan Tier 1, "
        "replikasi manual Tier 2, optimasi Optuna-TPE, matriks eksperimen E0–E7, evaluasi komparatif, dan analisis "
        "akhir. Potongan kode bersifat representatif; implementasi lengkap berada pada folder "
        "05_Source_Code/model_experiment."
    )
    set_font(r, "Times New Roman", 12)

    code_modules = [
        ("Modul 01: Penarikan Data Historis Binance API (01_fetch_binance_data.py)",
         "import requests, pandas as pd\n"
         "BASE_URL = 'https://api.binance.com/api/v3/klines'\n"
         "params = {'symbol': 'BTCUSDT', 'interval': '1d', 'limit': 1000}\n"
         "# Pagination iteratif: 2.192 observasi harian (2020-01-01 s.d. 2025-12-31)\n"
         "df = pd.DataFrame(raw_klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', ...])\n"
         "df['close'] = df['close'].astype(float)\n"
         "df.to_csv('BTCUSDT_daily_2020_2025.csv', index=False)"),

        ("Modul 02: Pra-Pemrosesan & Partisi Data Kronologis (02_preprocessing.py)",
         "from sklearn.preprocessing import MinMaxScaler\n"
         "# Partisi kronologis 80:20 (1.753 in-sample vs 439 holdout)\n"
         "train_raw = df['close'].iloc[:1753].values.reshape(-1, 1)\n"
         "test_raw = df['close'].iloc[1753:].values.reshape(-1, 1)\n"
         "scaler = MinMaxScaler(feature_range=(0, 1))\n"
         "train_scaled = scaler.fit_transform(train_raw)  # fit hanya pada data latih\n"
         "test_scaled = scaler.transform(test_raw)\n"
         "# Pada CV, scaler di-fit ulang pada setiap fold training"),

        ("Modul 03: Pelatihan Model Baseline Default Tier 1 (03_train_baseline_tier1.py)",
         "import tensorflow as tf\n"
         "model = tf.keras.Sequential([\n"
         "    tf.keras.layers.LSTM(units=50, input_shape=(30, 1)),\n"
         "    tf.keras.layers.Dropout(0.2),\n"
         "    tf.keras.layers.Dense(1)\n"
         "])\n"
         "model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')\n"
         "model.fit(X_train, y_train, epochs=100, batch_size=32,\n"
         "          validation_split=0.1, callbacks=[EarlyStopping(patience=12)])"),

        ("Modul 04: Pelatihan Model Replikasi Manual Tuning Tier 2 (04_train_manual_tier2.py)",
         "# Parameter Khumaidi dkk. (2024): lookback=60, units=128, dropout=0.20, lr=0.001, batch=10\n"
         "model = tf.keras.Sequential([\n"
         "    tf.keras.layers.LSTM(units=128, input_shape=(60, 1)),\n"
         "    tf.keras.layers.Dropout(0.20),\n"
         "    tf.keras.layers.Dense(1)\n"
         "])\n"
         "model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')\n"
         "model.fit(X_train, y_train, epochs=100, batch_size=10, validation_split=0.1)"),

        ("Modul 05: Optimasi Bayesian Tree-structured Parzen Estimator Tier 3 (05_optimize_optuna_tier3.py)",
         "import optuna\n"
         "def objective(trial):\n"
         "    lookback = trial.suggest_int('lookback', 7, 30)\n"
         "    units = trial.suggest_int('units', 32, 128)\n"
         "    dropout = trial.suggest_float('dropout', 0.10, 0.40, step=0.05)\n"
         "    lr = trial.suggest_float('learning_rate', 5e-4, 2e-3, log=True)\n"
         "    batch_size = trial.suggest_categorical('batch_size', [16, 32, 64])\n"
         "    layers = trial.suggest_int('layers', 1, 2)\n"
         "    # Purged TimeSeriesSplit 5 fold; scaler fit per fold; validasi USD (MAE)\n"
         "    return cv_mae\n"
         "study = optuna.create_study(\n"
         "    direction='minimize',\n"
         "    sampler=optuna.samplers.TPESampler(seed=42),\n"
         "    pruner=optuna.pruners.MedianPruner(n_startup_trials=3, n_warmup_steps=1),\n"
         ")\n"
         "study.optimize(objective, n_trials=50)"),

        ("Modul 06: Evaluasi Komparatif dan Figur (06_evaluate_and_compare.py)",
         "import numpy as np\n"
         "def compute_metrics(y_true, y_pred):\n"
         "    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))\n"
         "    mae = np.mean(np.abs(y_true - y_pred))\n"
         "    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100\n"
         "    return {'RMSE': rmse, 'MAE': mae, 'MAPE': mape}"),

        ("Modul 07: Matriks Eksperimen Terkontrol E0–E7 (experiment_matrix.py)",
         "EXPERIMENTS = ('E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7')\n"
         "# E0 persistence; E1/E2 kontrol; E3-E6 ablasi loss x scheduler;\n"
         "# E7 HPO penuh. Setiap model dijalankan pada seed 42, 123, 2024, 7, 99.\n"
         "for seed in (42, 123, 2024, 7, 99):\n"
         "    run_matrix(experiments=EXPERIMENTS, seed=seed, trials=50)"),

        ("Modul 08: Analisis Akhir dan Publikasi Angka (08_analyze_results.py)",
         "summary = build_summary(run_dir)\n"
         "# Metrik holdout, CI moving-block bootstrap, variabilitas antar-seed,\n"
         "# analisis residual/rezim, dan verdict ilmiah ditulis ke satu berkas.\n"
         "write_json(run_dir / 'summary_final.json', summary)\n"
         "if publish:\n"
         "    write_json(RESULTS_ROOT / 'summary_final.json', summary)"),
    ]

    for mod_title, mod_code in code_modules:
        p_mod = doc.add_paragraph()
        p_mod.paragraph_format.space_before = Pt(8)
        p_mod.paragraph_format.space_after = Pt(2)
        r = p_mod.add_run(mod_title)
        set_font(r, "Times New Roman", 11, bold=True)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        c.width = Cm(14.0)
        tcPr = c._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F6F9"/>'))
        format_cell(c, True, True, True, True)
        p_c = c.paragraphs[0]
        p_c.paragraph_format.line_spacing = 1.05
        p_c.paragraph_format.space_before = Pt(4)
        p_c.paragraph_format.space_after = Pt(4)
        r_c = p_c.add_run(mod_code)
        set_font(r_c, "Consolas", 8.5)

    doc.add_page_break()

    # =========================================================================
    # LAMPIRAN 2: SAMPEL DATA HISTORIS BINANCE BTC/USDT (2020-2025)
    # =========================================================================
    p_lp2 = doc.add_paragraph()
    p_lp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lp2.paragraph_format.space_before = Pt(0)
    p_lp2.paragraph_format.space_after = Pt(6)
    r = p_lp2.add_run("LAMPIRAN 2\nSAMPEL DATA HISTORIS TRANSAKSI HARIAN BINANCE BTC/USDT (2020–2025)")
    set_font(r, "Times New Roman", 12, bold=True)

    p_desc2 = doc.add_paragraph()
    p_desc2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc2.paragraph_format.line_spacing = 1.5
    p_desc2.paragraph_format.first_line_indent = Cm(1.0)
    p_desc2.paragraph_format.space_after = Pt(10)
    r = p_desc2.add_run(
        "Berikut merupakan cuplikan sampel data historis transaksi harian pasangan BTC/USDT yang dihimpun dari Binance Public "
        "Market Data API sebanyak 2.192 hari. Tabel di bawah menampilkan 15 observasi awal periode Januari 2020 dan 15 observasi akhir "
        "periode Desember 2025 dengan atribut Open, High, Low, Close (USD), serta Volume perdagangan harian (BTC)."
    )
    set_font(r, "Times New Roman", 12)

    df_raw = pd.read_csv("05_Source_Code/data/raw/BTCUSDT_daily_2020_2025.csv")
    sample_head = df_raw.head(12)
    sample_tail = df_raw.tail(12)

    tbl_s = doc.add_table(rows=1 + len(sample_head) + 1 + len(sample_tail), cols=6)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["No.", "Tanggal", "Open (USD)", "High (USD)", "Low (USD)", "Close (USD)"]
    for j, h in enumerate(headers):
        cell = tbl_s.rows[0].cells[j]
        set_font(cell.paragraphs[0].add_run(h), "Times New Roman", 9, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_cell(cell, top_border=True, bottom_border=True)
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>'))

    row_idx = 1
    # Head rows
    for i, (_, r_data) in enumerate(sample_head.iterrows()):
        row = tbl_s.rows[row_idx]
        vals = [str(i + 1), str(r_data["date"]), f"{r_data['open']:,.2f}", f"{r_data['high']:,.2f}", f"{r_data['low']:,.2f}", f"{r_data['close']:,.2f}"]
        for j, v in enumerate(vals):
            cell = row.cells[j]
            set_font(cell.paragraphs[0].add_run(v), "Times New Roman", 8.5)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT
            format_cell(cell, False, False)
        row_idx += 1

    # Separator row
    row_sep = tbl_s.rows[row_idx]
    for j in range(6):
        cell = row_sep.cells[j]
        set_font(cell.paragraphs[0].add_run("..." if j in [1, 5] else ""), "Times New Roman", 8.5, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_cell(cell, False, False)
    row_idx += 1

    # Tail rows
    for i, (_, r_data) in enumerate(sample_tail.iterrows()):
        row = tbl_s.rows[row_idx]
        curr_no = 2192 - len(sample_tail) + i + 1
        vals = [str(curr_no), str(r_data["date"]), f"{r_data['open']:,.2f}", f"{r_data['high']:,.2f}", f"{r_data['low']:,.2f}", f"{r_data['close']:,.2f}"]
        for j, v in enumerate(vals):
            cell = row.cells[j]
            set_font(cell.paragraphs[0].add_run(v), "Times New Roman", 8.5)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT
            format_cell(cell, False, (row_idx == len(tbl_s.rows) - 1))
        row_idx += 1

    doc.add_page_break()

    # =========================================================================
    # LAMPIRAN 3: LOG RIWAYAT 50 TRIAL OPTUNA-TPE
    # =========================================================================
    p_lp3 = doc.add_paragraph()
    p_lp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lp3.paragraph_format.space_before = Pt(0)
    p_lp3.paragraph_format.space_after = Pt(6)
    total_trials = int(config.get("total_trials", 50))
    r = p_lp3.add_run(
        f"LAMPIRAN 3\nLOG RIWAYAT {total_trials} PERCOBAAN OPTIMASI BAYESIAN OPTUNA-TPE"
    )
    set_font(r, "Times New Roman", 12, bold=True)

    p_desc3 = doc.add_paragraph()
    p_desc3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc3.paragraph_format.line_spacing = 1.5
    p_desc3.paragraph_format.first_line_indent = Cm(1.0)
    p_desc3.paragraph_format.space_after = Pt(10)
    r = p_desc3.add_run(
        f"Tabel berikut merangkum seluruh riwayat {total_trials} percobaan (trials) yang dieksekusi oleh algoritma "
        "Optuna berbasis Tree-structured Parzen Estimator (TPE) dan mekanisme pemangkasan MedianPruner. Parameter "
        "yang dicatat meliputi nomor trial, lookback window, units, dropout rate, learning rate, batch size, jumlah "
        "layer, nilai objektif validasi silang berpurge dalam USD, serta status akhir trial. Baris yang disorot "
        "adalah trial terbaik yang dipilih berdasarkan nilai objektif terkecil pada data in-sample."
    )
    set_font(r, "Times New Roman", 12)

    trials_path = results.run_dir / "optuna_trials_history.csv"
    if not trials_path.exists():
        raise FileNotFoundError(
            f"Riwayat trial tidak ditemukan: {trials_path}. "
            "Jalankan 05_optimize_optuna_tier3.py terlebih dahulu."
        )
    df_trials = pd.read_csv(trials_path).sort_values("number").reset_index(drop=True)
    t_opt = doc.add_table(rows=1 + len(df_trials), cols=8)
    t_opt.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_opt = ["Trial", "Lookback", "Units", "Dropout", "Learning Rate", "Batch / Layer", "Nilai Objektif (USD)", "Status"]
    for j, h in enumerate(headers_opt):
        cell = t_opt.rows[0].cells[j]
        set_font(cell.paragraphs[0].add_run(h), "Times New Roman", 8.5, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_cell(cell, top_border=True, bottom_border=True)
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>'))

    for i, (_, tr) in enumerate(df_trials.iterrows()):
        row = t_opt.rows[i + 1]
        t_no = str(int(tr["number"]))
        t_lb = str(int(tr["params_lookback"]))
        t_un = str(int(tr["params_units"]))
        t_dr = f"{tr['params_dropout']:.2f}"
        t_lr = f"{tr['params_learning_rate']:.4f}"
        t_bs = f"{int(tr['params_batch_size'])} / {int(tr['params_layers'])}"
        t_vl = f"{tr['value']:.6f}" if pd.notnull(tr['value']) else "-"
        t_st = str(tr["state"])
        vals = [t_no, t_lb, t_un, t_dr, t_lr, t_bs, t_vl, t_st]
        
        is_best = int(tr["number"]) == best_trial_number
        
        for j, v in enumerate(vals):
            cell = row.cells[j]
            r_v = cell.paragraphs[0].add_run(v)
            set_font(r_v, "Times New Roman", 8, bold=is_best)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [0, 1, 5, 7] else WD_ALIGN_PARAGRAPH.RIGHT
            format_cell(cell, False, (i == len(df_trials) - 1))
            if is_best:
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="D4EDDA"/>'))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Back matter generated successfully: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_back_matter()
