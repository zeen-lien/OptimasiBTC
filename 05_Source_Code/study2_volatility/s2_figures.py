"""Generate figures for the Study 2 thesis (Bab 4).

Reads frozen data and saved run artifacts only; does not recompute or alter
any evaluation result. Output: 05_Source_Code/results/study2/figures/
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "05_Source_Code" / "data" / "study2" / "btc_1h_daily_rv_2020_2026.csv"
RUN = ROOT / "05_Source_Code" / "results" / "study2" / "runs" / "20261028_101839_final_ab5d93"
HPO = ROOT / "05_Source_Code" / "results" / "study2" / "runs" / "20261028_094124_optuna_hpo_5be039"
OUT = ROOT / "05_Source_Code" / "results" / "study2" / "figures"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
})


def fig_timeseries() -> None:
    df = pd.read_csv(DATA, parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    ax.plot(df["date"], df["log_rv"], color="#1f3b73", lw=0.7)
    bounds = [("Dev/HPO", "2020-01-01", "2023-12-31", "#e8eef7"),
              ("Validasi", "2024-01-01", "2025-12-31", "#fdf1dc"),
              ("Uji", "2026-01-01", "2026-09-30", "#e6f2e6")]
    for label, start, end, color in bounds:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color=color, zorder=0)
        mid = pd.Timestamp(start) + (pd.Timestamp(end) - pd.Timestamp(start)) / 2
        ax.text(mid, ax.get_ylim()[1] * 0.97 if ax.get_ylim()[1] else 0, label,
                ha="center", va="top", fontsize=8, color="#444444")
    for b in ["2024-01-01", "2026-01-01"]:
        ax.axvline(pd.Timestamp(b), color="#888888", lw=0.8, ls="--")
    ax.set_ylabel("log RV harian")
    ax.set_xlabel("Tanggal")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(OUT / "fig_4_1_log_rv_timeseries.png")
    plt.close(fig)


def fig_optuna_history() -> None:
    trials = pd.read_csv(HPO / "trials.csv")
    trials = trials.sort_values("trial")
    vals = trials["mean_cv_qlike"].to_numpy()
    best = np.minimum.accumulate(vals)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.scatter(trials["trial"], vals, s=14, color="#7a9cc6", label="Nilai trial", zorder=3)
    ax.step(trials["trial"], best, where="post", color="#c0392b", lw=1.4,
            label="Nilai terbaik kumulatif", zorder=2)
    best_row = trials.loc[trials["mean_cv_qlike"].idxmin()]
    ax.scatter([best_row["trial"]], [best_row["mean_cv_qlike"]], s=55, marker="*",
               color="#c0392b", zorder=4, label=f"Trial terbaik (#{int(best_row['trial'])})")
    ax.set_xlabel("Nomor trial")
    ax.set_ylabel("Mean CV QLIKE")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, frameon=False)
    fig.savefig(OUT / "fig_4_2_optuna_history.png")
    plt.close(fig)


def fig_predictions() -> None:
    opt = pd.read_csv(RUN / "predictions_lstm_optuna_test.csv", parse_dates=["date"])
    unt = pd.read_csv(RUN / "predictions_lstm_untuned_test.csv", parse_dates=["date"])
    base = pd.read_csv(RUN / "predictions_baselines_test.csv", parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.plot(base["date"], base["y_true"], color="#222222", lw=1.1, label="Aktual")
    ax.plot(opt["date"], opt["y_hat_mean"], color="#c0392b", lw=0.9, label="LSTM Optuna")
    ax.plot(unt["date"], unt["y_hat_mean"], color="#1e8449", lw=0.9, label="LSTM untuned")
    ax.plot(base["date"], base["har_rv"], color="#b9770e", lw=0.8, ls="--", label="HAR-RV")
    ax.set_ylabel("log RV harian")
    ax.set_xlabel("2026")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=7.5, frameon=False, ncol=2)
    fig.savefig(OUT / "fig_4_3_predictions_test.png")
    plt.close(fig)


def fig_qlike_bar() -> None:
    analysis = json.load(open(RUN / "results_analysis.json", encoding="utf-8"))
    models = analysis["test"]["models"]
    order = ["persistence", "har_rv", "garch11", "lstm_untuned", "lstm_optuna"]
    labels = {"persistence": "Persistence", "har_rv": "HAR-RV", "garch11": "GARCH(1,1)",
              "lstm_untuned": "LSTM untuned", "lstm_optuna": "LSTM Optuna"}
    colors = ["#95a5a6", "#b9770e", "#7d6608", "#1e8449", "#c0392b"]
    vals = [models[m]["qlike"] for m in order]
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    bars = ax.bar([labels[m] for m in order], vals, color=colors, width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.4f}",
                ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("QLIKE (lebih rendah lebih baik)")
    ax.set_ylim(0, max(vals) * 1.16)
    ax.grid(axis="y", alpha=0.25)
    plt.xticks(rotation=15)
    fig.savefig(OUT / "fig_4_4_qlike_test.png")
    plt.close(fig)


def fig_cumulative() -> None:
    opt = pd.read_csv(RUN / "predictions_lstm_optuna_test.csv", parse_dates=["date"])
    base = pd.read_csv(RUN / "predictions_baselines_test.csv", parse_dates=["date"])
    e_opt = base["y_true"].to_numpy() - opt["y_hat_mean"].to_numpy()
    e_per = base["y_true"].to_numpy() - base["persistence"].to_numpy()
    e_har = base["y_true"].to_numpy() - base["har_rv"].to_numpy()
    q = lambda e: np.exp(e) - e - 1
    d_opt = np.cumsum(q(e_opt) - q(e_per))
    d_har = np.cumsum(q(e_har) - q(e_per))
    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    ax.plot(base["date"], d_opt, color="#c0392b", lw=1.1, label="LSTM Optuna vs persistence")
    ax.plot(base["date"], d_har, color="#b9770e", lw=1.0, ls="--", label="HAR-RV vs persistence")
    ax.axhline(0, color="#555555", lw=0.8)
    ax.set_ylabel("ΔQLIKE kumulatif")
    ax.set_xlabel("2026")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=7.5, frameon=False)
    fig.savefig(OUT / "fig_4_5_cumulative_qlike.png")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_timeseries()
    fig_optuna_history()
    fig_predictions()
    fig_qlike_bar()
    fig_cumulative()
    for p in sorted(OUT.glob("*.png")):
        print(f"written: {p} ({p.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
