"""
06_evaluate_and_compare.py — Multi-Tier Comparative Benchmark Evaluation & Visualizations
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Deskripsi:
  1. Memuat metrik performa Tier 1, Tier 2, dan Tier 3.
  2. Menghitung persentase penurunan error (Improvement %) sesuai Persamaan (3.2).
  3. Menyusun tabel komparatif 3-Tier Benchmark untuk Bab 4 Skripsi.
  4. Menghasilkan visualisasi grafik beresolusi tinggi (300 DPI):
     - Gambar 4.1: Kurva Prediksi vs Nilai Aktual pada Data Out-of-Sample (3 Tier).
     - Gambar 4.2: Diagram Batang Komparasi Metrik RMSE, MAE, dan MAPE.
     - Gambar 4.3: Kurva Konvergensi Optimasi Optuna-TPE (50 Trials).
     - Gambar 4.4: Analisis Galat Residu (Residual Error Distribution).
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set style visualisasi akademik
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 11


def calculate_improvement(base_err, opt_err):
    return ((base_err - opt_err) / base_err) * 100.0


def run_comparative_evaluation():
    print("=" * 70)
    print("PIPELINE EVALUASI 06: KOMPARASI BENCHMARK 3-TIER & VISUALISASI HASIL")
    print("=" * 70)
    
    base_dir = r"d:\OneDrive\Desktop\jurnal\05_Source_Code\results"
    metrics_dir = os.path.join(base_dir, "metrics")
    figs_dir = os.path.join(base_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)
    
    # 1. Load Metrics
    t1_file = os.path.join(metrics_dir, "metrics_tier1.json")
    t2_file = os.path.join(metrics_dir, "metrics_tier2.json")
    t3_file = os.path.join(metrics_dir, "metrics_tier3.json")
    
    for fpath in [t1_file, t2_file, t3_file]:
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"File metrik belum tersedia: {fpath}. Pastikan eksperimen Tier 1-3 telah selesai dijalankan.")
            
    with open(t1_file, "r") as f:
        t1 = json.load(f)
    with open(t2_file, "r") as f:
        t2 = json.load(f)
    with open(t3_file, "r") as f:
        t3 = json.load(f)
        
    m1 = t1["metrics"]
    m2 = t2["metrics"]
    m3 = t3["metrics"]
    
    # 2. Hitung Improvement (%)
    imp_vs_t1 = {
        "RMSE": calculate_improvement(m1["RMSE"], m3["RMSE"]),
        "MAE": calculate_improvement(m1["MAE"], m3["MAE"]),
        "MAPE": calculate_improvement(m1["MAPE"], m3["MAPE"]),
    }
    imp_vs_t2 = {
        "RMSE": calculate_improvement(m2["RMSE"], m3["RMSE"]),
        "MAE": calculate_improvement(m2["MAE"], m3["MAE"]),
        "MAPE": calculate_improvement(m2["MAPE"], m3["MAPE"]),
    }
    
    print("\n[1/4] RINGKASAN HASIL BENCHMARK 3-TIER PADA OUT-OF-SAMPLE TEST SET:")
    print("-" * 70)
    print(f"{'Metrik':<10} | {'Tier 1 (Default)':<16} | {'Tier 2 (Manual)':<16} | {'Tier 3 (Optuna)':<16}")
    print("-" * 70)
    print(f"{'RMSE':<10} | USD {m1['RMSE']:>11,.2f} | USD {m2['RMSE']:>11,.2f} | USD {m3['RMSE']:>11,.2f}")
    print(f"{'MAE':<10} | USD {m1['MAE']:>11,.2f} | USD {m2['MAE']:>11,.2f} | USD {m3['MAE']:>11,.2f}")
    print(f"{'MAPE':<10} | {m1['MAPE']:>14.2f}% | {m2['MAPE']:>14.2f}% | {m3['MAPE']:>14.2f}%")
    print("-" * 70)
    
    print("\n[2/4] PERSENTASE PENURUNAN ERROR (IMPROVEMENT TIER 3 OPTUNA):")
    print("-" * 70)
    print(f"      - vs Tier 1 (Baseline Default):")
    print(f"        * Penurunan RMSE : {imp_vs_t1['RMSE']:+.2f}%")
    print(f"        * Penurunan MAE  : {imp_vs_t1['MAE']:+.2f}%")
    print(f"        * Penurunan MAPE : {imp_vs_t1['MAPE']:+.2f}%")
    print(f"      - vs Tier 2 (Manual Tuning Khumaidi dkk.):")
    print(f"        * Penurunan RMSE : {imp_vs_t2['RMSE']:+.2f}%")
    print(f"        * Penurunan MAE  : {imp_vs_t2['MAE']:+.2f}%")
    print(f"        * Penurunan MAPE : {imp_vs_t2['MAPE']:+.2f}%")
    
    # 3. Load Predictions Data for Plotting
    p1 = pd.read_csv(os.path.join(base_dir, "predictions_tier1.csv"))
    p2 = pd.read_csv(os.path.join(base_dir, "predictions_tier2.csv"))
    p3 = pd.read_csv(os.path.join(base_dir, "predictions_tier3.csv"))
    
    p1["date"] = pd.to_datetime(p1["date"])
    
    # ── GAMBAR 4.1: Kurva Prediksi vs Nilai Aktual ──
    print("\n[3/4] Membuat Gambar Visualisasi Penelitian:")
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.plot(p1["date"], p1["actual_close"], label="Harga Aktual (Ground Truth)", color="#1F2937", linewidth=2.0)
    ax.plot(p1["date"], p1["predicted_close_tier1"], label=f"Tier 1: LSTM Default (MAPE {m1['MAPE']:.2f}%)", color="#EF4444", linestyle="--", alpha=0.8, linewidth=1.4)
    ax.plot(p1["date"], p2["predicted_close_tier2"], label=f"Tier 2: Manual Tuning (MAPE {m2['MAPE']:.2f}%)", color="#F59E0B", linestyle="-.", alpha=0.8, linewidth=1.4)
    ax.plot(p1["date"], p3["predicted_close_tier3"], label=f"Tier 3: Optuna-TPE (MAPE {m3['MAPE']:.2f}%)", color="#10B981", linestyle="-", linewidth=1.8)
    
    ax.set_title("Perbandingan Kurva Prediksi Harga Bitcoin (BTC/USDT) pada Data Out-of-Sample", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Tanggal Observasi (Oktober 2024 - Desember 2025)", fontweight="bold")
    ax.set_ylabel("Harga Penutupan (USD)", fontweight="bold")
    ax.yaxis.set_major_formatter("${x:,.0f}")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=True, loc="upper left", fontsize=10)
    fig.tight_layout()
    fig1_path = os.path.join(figs_dir, "gambar_4_1_perbandingan_prediksi_3tier.png")
    fig.savefig(fig1_path)
    plt.close(fig)
    print(f"      -> Gambar 4.1 tersimpan: {fig1_path}")
    
    # ── GAMBAR 4.2: Bar Chart Perbandingan Metrik ──
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)
    tiers = ["Tier 1\nDefault", "Tier 2\nManual", "Tier 3\nOptuna-TPE"]
    colors = ["#EF4444", "#F59E0B", "#10B981"]
    
    # Subplot 1: RMSE
    rmse_vals = [m1["RMSE"], m2["RMSE"], m3["RMSE"]]
    bars1 = axes[0].bar(tiers, rmse_vals, color=colors, width=0.55, edgecolor="#374151")
    axes[0].set_title("Root Mean Square Error (RMSE)", fontweight="bold")
    axes[0].set_ylabel("USD", fontweight="bold")
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, yval * 1.01, f"${yval:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        
    # Subplot 2: MAE
    mae_vals = [m1["MAE"], m2["MAE"], m3["MAE"]]
    bars2 = axes[1].bar(tiers, mae_vals, color=colors, width=0.55, edgecolor="#374151")
    axes[1].set_title("Mean Absolute Error (MAE)", fontweight="bold")
    axes[1].set_ylabel("USD", fontweight="bold")
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval * 1.01, f"${yval:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        
    # Subplot 3: MAPE
    mape_vals = [m1["MAPE"], m2["MAPE"], m3["MAPE"]]
    bars3 = axes[2].bar(tiers, mape_vals, color=colors, width=0.55, edgecolor="#374151")
    axes[2].set_title("Mean Absolute Percentage Error (MAPE)", fontweight="bold")
    axes[2].set_ylabel("Persentase (%)", fontweight="bold")
    for bar in bars3:
        yval = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2.0, yval * 1.01, f"{yval:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
        
    for ax in axes:
        ax.set_ylim(0, max([b.get_height() for b in ax.patches]) * 1.18)
    fig.suptitle("Perbandingan Kinerja Tiga Tingkatan Model (3-Tier Benchmark)", fontsize=14, fontweight="bold", y=1.03)
    fig.tight_layout()
    fig2_path = os.path.join(figs_dir, "gambar_4_2_bar_chart_komparasi_metrik.png")
    fig.savefig(fig2_path)
    plt.close(fig)
    print(f"      -> Gambar 4.2 tersimpan: {fig2_path}")
    
    # ── GAMBAR 4.3: Konvergensi Optuna ──
    trials_csv = os.path.join(base_dir, "optuna_trials_history.csv")
    if os.path.exists(trials_csv):
        tdf = pd.read_csv(trials_csv)
        complete_trials = tdf[tdf["state"] == "COMPLETE"].copy()
        complete_trials["best_so_far"] = complete_trials["value"].cummin()
        
        fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
        ax.scatter(complete_trials["number"], complete_trials["value"], color="#6B7280", alpha=0.6, s=35, label="Nilai Evaluasi Tiap Trial (CV Loss)")
        ax.plot(complete_trials["number"], complete_trials["best_so_far"], color="#2563EB", linewidth=2.2, label="Nilai Kerugian Terbaik (Best So Far)")
        ax.set_title("Kurva Konvergensi Optimasi Hyperparameter Optuna-TPE (50 Trials)", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Nomor Uji Coba (Trial Number)", fontweight="bold")
        ax.set_ylabel("Validation Mean Squared Error (Loss)", fontweight="bold")
        ax.legend(frameon=True, loc="upper right")
        fig.tight_layout()
        fig3_path = os.path.join(figs_dir, "gambar_4_3_konvergensi_optuna.png")
        fig.savefig(fig3_path)
        plt.close(fig)
        print(f"      -> Gambar 4.3 tersimpan: {fig3_path}")
        
    # 4. Save Final Benchmark Summary JSON & CSV
    summary_data = {
        "tier1_baseline": t1,
        "tier2_manual": t2,
        "tier3_optuna": t3,
        "improvements": {
            "tier3_vs_tier1": imp_vs_t1,
            "tier3_vs_tier2": imp_vs_t2
        }
    }
    summary_json_path = os.path.join(base_dir, "benchmark_comparison_summary.json")
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)
        
    summary_rows = [
        {"Model Tier": "Tier 1: LSTM Default (Baseline)", "Lookback": m1.get("lookback", 30), "RMSE (USD)": m1["RMSE"], "MAE (USD)": m1["MAE"], "MAPE (%)": m1["MAPE"], "Imp RMSE vs T1": "0.0%", "Imp MAE vs T1": "0.0%", "Imp MAPE vs T1": "0.0%"},
        {"Model Tier": "Tier 2: LSTM Manual (Khumaidi dkk.)", "Lookback": m2.get("lookback", 60), "RMSE (USD)": m2["RMSE"], "MAE (USD)": m2["MAE"], "MAPE (%)": m2["MAPE"], "Imp RMSE vs T1": f"{calculate_improvement(m1['RMSE'], m2['RMSE']):+.2f}%", "Imp MAE vs T1": f"{calculate_improvement(m1['MAE'], m2['MAE']):+.2f}%", "Imp MAPE vs T1": f"{calculate_improvement(m1['MAPE'], m2['MAPE']):+.2f}%"},
        {"Model Tier": "Tier 3: LSTM Optuna-TPE (Usulan)", "Lookback": t3["hyperparameters"]["lookback"], "RMSE (USD)": m3["RMSE"], "MAE (USD)": m3["MAE"], "MAPE (%)": m3["MAPE"], "Imp RMSE vs T1": f"{imp_vs_t1['RMSE']:+.2f}%", "Imp MAE vs T1": f"{imp_vs_t1['MAE']:+.2f}%", "Imp MAPE vs T1": f"{imp_vs_t1['MAPE']:+.2f}%"}
    ]
    summary_df = pd.DataFrame(summary_rows)
    summary_csv_path = os.path.join(base_dir, "benchmark_comparison_table.csv")
    summary_df.to_csv(summary_csv_path, index=False)
    
    print(f"\n[4/4] Ringkasan komparasi berhasil disimpan:")
    print(f"      -> {summary_json_path}")
    print(f"      -> {summary_csv_path}")
    print("=" * 70)


if __name__ == "__main__":
    run_comparative_evaluation()
