"""
06_evaluate_and_compare.py - Comparative benchmark and thesis figures.

Fase 1 keeps the legacy 3-tier comparison but makes provenance explicit:
the script selects a complete run (or legacy artifacts), verifies that the
metrics JSON matches the prediction CSVs, and labels the Tier 3 loss
correctly (MAE, not MSE).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Mapping

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
import run_utils
import stats_utils

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 11

TIER_FILES = {
    1: "metrics_tier1.json",
    2: "metrics_tier2.json",
    3: "metrics_tier3.json",
}
PREDICTION_FILES = {
    1: "predictions_tier1.csv",
    2: "predictions_tier2.csv",
    3: "predictions_tier3.csv",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Komparasi benchmark 3-tier dan visualisasi")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--metrics-dir", default=None, help="Direktori metrik eksplisit")
    parser.add_argument("--predictions-dir", default=None, help="Direktori prediksi eksplisit")
    parser.add_argument("--figures-dir", default=None, help="Direktori figure eksplisit")
    return parser.parse_args(argv)


def calculate_improvement(base_err: float, opt_err: float) -> float:
    return ((base_err - opt_err) / base_err) * 100.0


def find_complete_run(root: Path) -> str | None:
    runs_root = root / "05_Source_Code" / "results" / "runs"
    if not runs_root.exists():
        return None
    candidates = []
    for run_dir in runs_root.iterdir():
        if not run_dir.is_dir():
            continue
        if all((run_dir / "metrics" / name).exists() for name in TIER_FILES.values()):
            candidates.append(run_dir)
    if not candidates:
        return None
    latest = max(candidates, key=lambda path: (path.stat().st_mtime, path.name))
    return latest.name


def resolve_eval_paths(args) -> run_utils.RunPaths:
    run_utils.apply_project_root(args.project_root)
    if args.legacy:
        return run_utils.resolve_run_paths(legacy=True, root=config.PROJECT_ROOT)

    run_id = args.run_id
    if run_id is None and args.metrics_dir is None:
        run_id = find_complete_run(config.PROJECT_ROOT)
        if run_id is None:
            print("[INFO] Tidak ada run lengkap; memakai artefak legacy.")
            return run_utils.resolve_run_paths(legacy=True, root=config.PROJECT_ROOT)
        print(f"[INFO] Memakai run lengkap terbaru: {run_id}")

    return run_utils.resolve_run_paths(
        run_id=run_id,
        root=config.PROJECT_ROOT,
        stage="eval",
        seed=args.seed,
        legacy=False,
    )


def load_inputs(paths: run_utils.RunPaths, args) -> tuple[dict, dict, dict]:
    metrics_dir = Path(args.metrics_dir) if args.metrics_dir else paths.metrics_dir
    predictions_dir = Path(args.predictions_dir) if args.predictions_dir else paths.predictions_dir

    metrics = {}
    predictions = {}
    missing = []
    for tier, filename in TIER_FILES.items():
        path = metrics_dir / filename
        if not path.exists():
            missing.append(str(path))
            continue
        with path.open("r", encoding="utf-8") as handle:
            metrics[tier] = json.load(handle)

    for tier, filename in PREDICTION_FILES.items():
        path = predictions_dir / filename
        if not path.exists():
            missing.append(str(path))
            continue
        predictions[tier] = pd.read_csv(path)

    if missing:
        raise FileNotFoundError(
            "Artefak evaluasi belum lengkap:\n  - " + "\n  - ".join(missing)
        )
    return metrics, predictions, {"metrics_dir": metrics_dir, "predictions_dir": predictions_dir}


def verify_predictions(predictions: dict[int, pd.DataFrame]) -> None:
    dates = {tier: pd.to_datetime(frame["date"]) for tier, frame in predictions.items()}
    base = dates[1]
    for tier, series in dates.items():
        if len(series) != config.EXPECTED_TEST_ROWS:
            raise ValueError(
                f"Tier {tier} memiliki {len(series)} prediksi, "
                f"diharapkan {config.EXPECTED_TEST_ROWS}"
            )
        if not series.equals(base):
            raise ValueError(f"Tanggal prediksi Tier {tier} tidak identik dengan Tier 1")
        if series.iloc[0].strftime("%Y-%m-%d") != config.TEST_START_DATE:
            raise ValueError(f"Tier {tier} tidak dimulai pada {config.TEST_START_DATE}")
        if series.iloc[-1].strftime("%Y-%m-%d") != config.TEST_END_DATE:
            raise ValueError(f"Tier {tier} tidak berakhir pada {config.TEST_END_DATE}")

    actual = predictions[1]["actual_close"].to_numpy()
    for tier, frame in predictions.items():
        if not np.allclose(frame["actual_close"].to_numpy(), actual, rtol=1e-9, atol=1e-6):
            raise ValueError(f"Nilai aktual Tier {tier} berbeda dari Tier 1")


def recompute_metrics(frame: pd.DataFrame, column: str) -> dict[str, float]:
    y_true = frame["actual_close"].to_numpy(dtype=float)
    y_pred = frame[column].to_numpy(dtype=float)
    return {
        "RMSE": float(np.sqrt(np.mean((y_true - y_pred) ** 2))),
        "MAE": float(np.mean(np.abs(y_true - y_pred))),
        "MAPE": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100.0),
    }


def verify_metric_consistency(metrics: dict, predictions: dict[int, pd.DataFrame]) -> None:
    for tier, frame in predictions.items():
        column = f"predicted_close_tier{tier}"
        recomputed = recompute_metrics(frame, column)
        recorded = metrics[tier]["metrics"]
        for key in ("RMSE", "MAE", "MAPE"):
            if abs(float(recorded[key]) - recomputed[key]) > 0.05:
                raise ValueError(
                    f"Metrik {key} Tier {tier} tidak cocok dengan prediksi: "
                    f"JSON={recorded[key]}, recomputed={recomputed[key]:.4f}"
                )


def verify_baselines(
    baseline_frame: pd.DataFrame,
    predictions: dict[int, pd.DataFrame],
) -> None:
    dates = pd.to_datetime(baseline_frame["date"])
    if not dates.equals(pd.to_datetime(predictions[1]["date"])):
        raise ValueError("Tanggal baseline tidak identik dengan tanggal prediksi tier")
    if len(baseline_frame) != config.EXPECTED_TEST_ROWS:
        raise ValueError("Jumlah baris baseline tidak sesuai kontrak holdout")
    np.testing.assert_allclose(
        baseline_frame["actual_close"].to_numpy(dtype=float),
        predictions[1]["actual_close"].to_numpy(dtype=float),
        rtol=0,
        atol=0.02,
    )


def loss_label(metrics_payload: dict) -> str:
    loss = str(metrics_payload.get("loss", "mean_absolute_error")).lower()
    if "absolute" in loss or loss in {"mae", "l1"}:
        return "Validation Mean Absolute Error (MAE Loss)"
    if "squared" in loss or loss in {"mse", "l2"}:
        return "Validation Mean Squared Error (MSE Loss)"
    return f"Validation Loss ({loss})"


def load_seed_studies(predictions_dir: Path) -> dict[int, dict]:
    """Load optional multi-seed aggregates produced by the training scripts."""
    studies: dict[int, dict] = {}
    for tier in (1, 2, 3):
        path = predictions_dir / f"seed_metrics_tier{tier}.json"
        if path.exists():
            with path.open("r", encoding="utf-8") as handle:
                studies[tier] = json.load(handle)
    return studies


def load_baselines(
    metrics_dir: Path, predictions_dir: Path
) -> tuple[dict | None, pd.DataFrame | None]:
    """Load naive baselines if the baseline stage has been run for this run."""
    metrics_path = metrics_dir / "metrics_baselines.json"
    predictions_path = predictions_dir / "predictions_baselines.csv"
    if not metrics_path.exists() or not predictions_path.exists():
        return None, None
    with metrics_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload, pd.read_csv(predictions_path)


def compute_bootstrap_intervals(
    predictions: dict[int, pd.DataFrame],
) -> dict[int, dict[str, dict[str, float]]]:
    intervals: dict[int, dict[str, dict[str, float]]] = {}
    for tier, frame in predictions.items():
        intervals[tier] = stats_utils.bootstrap_metric_ci(
            frame["actual_close"].to_numpy(dtype=float),
            frame[f"predicted_close_tier{tier}"].to_numpy(dtype=float),
            n_resamples=config.BOOTSTRAP_RESAMPLES,
            confidence=config.CONFIDENCE_LEVEL,
            block_size=config.BOOTSTRAP_BLOCK_SIZE,
            seed=42,
        )
    return intervals


def format_interval(entry: Mapping[str, float]) -> str:
    low, high = entry["ci_low"], entry["ci_high"]
    if entry["estimate"] > 500:
        return f"{low:,.0f} - {high:,.0f}"
    return f"{low:.2f} - {high:.2f}"


def format_seed_summary(seed_study: Mapping[str, object] | None, metric: str) -> str:
    if not seed_study:
        return "-"
    aggregate = seed_study.get("aggregate", {}).get(metric)
    if not aggregate:
        return "-"
    return f"{aggregate['mean']:.2f} +/- {aggregate['std']:.2f} (n={aggregate['n_seeds']})"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = resolve_eval_paths(args)

    if paths.legacy:
        print("[WARNING] Mode legacy: summary/figure lama dapat tertimpa.")

    metrics, predictions, input_dirs = load_inputs(paths, args)
    verify_predictions(predictions)
    verify_metric_consistency(metrics, predictions)
    seed_studies = load_seed_studies(input_dirs["predictions_dir"])
    baseline_payload, baseline_frame = load_baselines(
        input_dirs["metrics_dir"], input_dirs["predictions_dir"]
    )
    if baseline_payload is not None and baseline_frame is not None:
        verify_baselines(baseline_frame, predictions)
        persistence_metrics = baseline_payload["baselines"]["persistence"]["metrics"]
        persistence_column = baseline_payload["baselines"]["persistence"]["prediction_column"]
        persistence_ci = baseline_payload["baselines"]["persistence"].get(
            "confidence_intervals"
        )
    else:
        persistence_metrics = None
        persistence_column = None
        persistence_ci = None

    intervals = compute_bootstrap_intervals(predictions)
    paired_differences = {
        "tier3_vs_tier1": {
            metric: stats_utils.paired_bootstrap_difference(
                predictions[1]["actual_close"].to_numpy(dtype=float),
                predictions[1]["predicted_close_tier1"].to_numpy(dtype=float),
                predictions[3]["predicted_close_tier3"].to_numpy(dtype=float),
                metric=metric,
                n_resamples=config.BOOTSTRAP_RESAMPLES,
                confidence=config.CONFIDENCE_LEVEL,
                block_size=config.BOOTSTRAP_BLOCK_SIZE,
                seed=42,
            )
            for metric in ("RMSE", "MAE", "MAPE")
        },
        "tier3_vs_tier2": {
            metric: stats_utils.paired_bootstrap_difference(
                predictions[2]["actual_close"].to_numpy(dtype=float),
                predictions[2]["predicted_close_tier2"].to_numpy(dtype=float),
                predictions[3]["predicted_close_tier3"].to_numpy(dtype=float),
                metric=metric,
                n_resamples=config.BOOTSTRAP_RESAMPLES,
                confidence=config.CONFIDENCE_LEVEL,
                block_size=config.BOOTSTRAP_BLOCK_SIZE,
                seed=42,
            )
            for metric in ("RMSE", "MAE", "MAPE")
        },
    }
    if baseline_frame is not None and persistence_column is not None:
        paired_differences["tier3_vs_persistence"] = {
            metric: stats_utils.paired_bootstrap_difference(
                predictions[1]["actual_close"].to_numpy(dtype=float),
                baseline_frame[persistence_column].to_numpy(dtype=float),
                predictions[3]["predicted_close_tier3"].to_numpy(dtype=float),
                metric=metric,
                n_resamples=config.BOOTSTRAP_RESAMPLES,
                confidence=config.CONFIDENCE_LEVEL,
                block_size=config.BOOTSTRAP_BLOCK_SIZE,
                seed=42,
            )
            for metric in ("RMSE", "MAE", "MAPE")
        }

    t1, t2, t3 = metrics[1], metrics[2], metrics[3]
    m1, m2, m3 = t1["metrics"], t2["metrics"], t3["metrics"]

    imp_vs_t1 = {
        key: calculate_improvement(m1[key], m3[key]) for key in ("RMSE", "MAE", "MAPE")
    }
    imp_vs_t2 = {
        key: calculate_improvement(m2[key], m3[key]) for key in ("RMSE", "MAE", "MAPE")
    }
    imp_vs_persistence = (
        {
            key: calculate_improvement(persistence_metrics[key], m3[key])
            for key in ("RMSE", "MAE", "MAPE")
        }
        if persistence_metrics
        else None
    )

    print("=" * 70)
    print("PIPELINE EVALUASI 06: KOMPARASI BENCHMARK 3-TIER & VISUALISASI")
    print("=" * 70)
    print(f"[1/4] Metrik out-of-sample ({paths.run_id}):")
    print("-" * 70)
    print(f"{'Metrik':<8} | {'Tier 1':>14} | {'Tier 2':>14} | {'Tier 3':>14}")
    print("-" * 70)
    print(f"{'RMSE':<8} | {m1['RMSE']:>14,.2f} | {m2['RMSE']:>14,.2f} | {m3['RMSE']:>14,.2f}")
    print(f"{'MAE':<8} | {m1['MAE']:>14,.2f} | {m2['MAE']:>14,.2f} | {m3['MAE']:>14,.2f}")
    print(f"{'MAPE':<8} | {m1['MAPE']:>13.2f}% | {m2['MAPE']:>13.2f}% | {m3['MAPE']:>13.2f}%")
    print("-" * 70)

    print(f"\n[1b] Interval kepercayaan {int(config.CONFIDENCE_LEVEL * 100)}% "
          f"(moving-block bootstrap, blok {config.BOOTSTRAP_BLOCK_SIZE} hari, "
          f"{config.BOOTSTRAP_RESAMPLES} resample):")
    for tier, tier_intervals in intervals.items():
        parts = [
            f"{metric} {format_interval(tier_intervals[metric])}"
            for metric in ("RMSE", "MAE", "MAPE")
        ]
        print(f"      Tier {tier}: " + " | ".join(parts))

    if seed_studies:
        print("\n[1c] Ringkasan multi-seed (mean +/- std):")
        for tier, seed_study in seed_studies.items():
            seeds = seed_study.get("seeds", [])
            parts = [
                f"{metric} {format_seed_summary(seed_study, metric)}"
                for metric in ("RMSE", "MAE", "MAPE")
            ]
            print(f"      Tier {tier} (seed {seeds}): " + " | ".join(parts))
    else:
        print("\n[1c] Multi-seed: belum ada seed_metrics_tier*.json untuk run ini.")

    if baseline_payload is not None:
        print("\n[1d] Baseline naif pada holdout yang sama:")
        for name in baseline_payload.get("ranking_by_mae", []):
            entry = baseline_payload["baselines"][name]
            metrics = entry["metrics"]
            print(
                f"      {name:<20} RMSE {metrics['RMSE']:>10,.2f} | "
                f"MAE {metrics['MAE']:>10,.2f} | MAPE {metrics['MAPE']:>6.2f}%"
            )
        print(f"      Baseline terbaik (MAE): {baseline_payload['best_baseline']}")

    print("\n[2/4] Penurunan error Tier 3:")
    for label, values in (("vs Tier 1", imp_vs_t1), ("vs Tier 2", imp_vs_t2)):
        print(f"      {label}: RMSE {values['RMSE']:+.2f}% | "
              f"MAE {values['MAE']:+.2f}% | MAPE {values['MAPE']:+.2f}%")
    if imp_vs_persistence is not None:
        print(f"      vs Persistence: RMSE {imp_vs_persistence['RMSE']:+.2f}% | "
              f"MAE {imp_vs_persistence['MAE']:+.2f}% | "
              f"MAPE {imp_vs_persistence['MAPE']:+.2f}%")
        print("      (positif = Tier 3 lebih rendah error-nya daripada baseline)")

    figures_dir = Path(args.figures_dir) if args.figures_dir else (
        config.LEGACY_FIGURES_DIR if paths.legacy else paths.figures_dir
    )
    figures_dir.mkdir(parents=True, exist_ok=True)

    p1, p2, p3 = predictions[1], predictions[2], predictions[3]
    p1["date"] = pd.to_datetime(p1["date"])

    print("\n[3/4] Membuat figure:")
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.plot(p1["date"], p1["actual_close"], label="Harga Aktual (Ground Truth)",
            color="#1F2937", linewidth=2.0)
    ax.plot(p1["date"], p1["predicted_close_tier1"],
            label=f"Tier 1: LSTM Default (MAPE {m1['MAPE']:.2f}%)",
            color="#EF4444", linestyle="--", alpha=0.8, linewidth=1.4)
    ax.plot(p1["date"], p2["predicted_close_tier2"],
            label=f"Tier 2: Manual Tuning (MAPE {m2['MAPE']:.2f}%)",
            color="#F59E0B", linestyle="-.", alpha=0.8, linewidth=1.4)
    ax.plot(p1["date"], p3["predicted_close_tier3"],
            label=f"Tier 3: Optuna-TPE (MAPE {m3['MAPE']:.2f}%)",
            color="#10B981", linestyle="-", linewidth=1.8)
    if baseline_frame is not None and persistence_column is not None:
        ax.plot(
            pd.to_datetime(baseline_frame["date"]),
            baseline_frame[persistence_column],
            label=(
                "Baseline Persistence "
                f"(MAPE {persistence_metrics['MAPE']:.2f}%)"
            ),
            color="#6B7280",
            linestyle=":",
            linewidth=1.8,
            alpha=0.9,
        )
    ax.set_title(
        "Perbandingan Kurva Prediksi Harga Bitcoin (BTC/USDT) pada Data Out-of-Sample"
        + (" dengan Baseline Persistence" if baseline_frame is not None else ""),
        fontsize=13, fontweight="bold", pad=12,
    )
    ax.set_xlabel("Tanggal Observasi (Oktober 2024 - Desember 2025)", fontweight="bold")
    ax.set_ylabel("Harga Penutupan (USD)", fontweight="bold")
    ax.yaxis.set_major_formatter("${x:,.0f}")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(frameon=True, loc="upper left", fontsize=10)
    fig.tight_layout()
    fig1_path = figures_dir / "gambar_4_1_perbandingan_prediksi_3tier.png"
    fig.savefig(fig1_path)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)
    tiers = ["Tier 1\nDefault", "Tier 2\nManual", "Tier 3\nOptuna-TPE"]
    colors = ["#EF4444", "#F59E0B", "#10B981"]
    for axis, key, title, suffix in (
        (axes[0], "RMSE", "Root Mean Square Error (RMSE)", ""),
        (axes[1], "MAE", "Mean Absolute Error (MAE)", ""),
        (axes[2], "MAPE", "Mean Absolute Percentage Error (MAPE)", "%"),
    ):
        values = [m1[key], m2[key], m3[key]]
        errors = np.array(
            [
                [
                    intervals[tier][key]["estimate"] - intervals[tier][key]["ci_low"]
                    for tier in (1, 2, 3)
                ],
                [
                    intervals[tier][key]["ci_high"] - intervals[tier][key]["estimate"]
                    for tier in (1, 2, 3)
                ],
            ]
        )
        bars = axis.bar(
            tiers,
            values,
            color=colors,
            width=0.55,
            edgecolor="#374151",
            yerr=errors,
            capsize=5,
            error_kw={"elinewidth": 1.2, "ecolor": "#374151"},
        )
        axis.set_title(title, fontweight="bold")
        axis.set_ylabel("Persentase (%)" if suffix else "USD", fontweight="bold")
        for bar in bars:
            height = bar.get_height()
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                height * 1.01,
                f"{height:.2f}%" if suffix else f"${height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )
        axis.set_ylim(0, max(values) * 1.18)
    fig.suptitle("Perbandingan Kinerja Tiga Tingkatan Model (3-Tier Benchmark)",
                 fontsize=14, fontweight="bold", y=1.03)
    fig.tight_layout()
    fig2_path = figures_dir / "gambar_4_2_bar_chart_komparasi_metrik.png"
    fig.savefig(fig2_path)
    plt.close(fig)

    trials_csv = (config.LEGACY_TRIALS_CSV if paths.legacy else paths.run_dir / "optuna_trials_history.csv")
    fig3_path = None
    if trials_csv.exists():
        tdf = pd.read_csv(trials_csv)
        complete_trials = tdf[tdf["state"] == "COMPLETE"].copy()
        if not complete_trials.empty:
            complete_trials["best_so_far"] = complete_trials["value"].cummin()
            fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
            ax.scatter(complete_trials["number"], complete_trials["value"],
                       color="#6B7280", alpha=0.6, s=35,
                       label="Nilai Evaluasi Tiap Trial (CV Loss)")
            ax.plot(complete_trials["number"], complete_trials["best_so_far"],
                    color="#2563EB", linewidth=2.2, label="Nilai Kerugian Terbaik (Best So Far)")
            ax.set_title(
                f"Kurva Konvergensi Optimasi Hyperparameter Optuna-TPE "
                f"({len(tdf)} Trials)",
                fontsize=13,
                fontweight="bold",
                pad=12,
            )
            ax.set_xlabel("Nomor Uji Coba (Trial Number)", fontweight="bold")
            ax.set_ylabel(loss_label(t3), fontweight="bold")
            ax.legend(frameon=True, loc="upper right")
            fig.tight_layout()
            fig3_path = figures_dir / "gambar_4_3_konvergensi_optuna.png"
            fig.savefig(fig3_path)
            plt.close(fig)
    if fig3_path:
        print(f"      -> {fig1_path.name}, {fig2_path.name}, {fig3_path.name}")
    else:
        print(f"      -> {fig1_path.name}, {fig2_path.name} (trials CSV tidak tersedia)")

    summary_data = {
        "run_id": paths.run_id,
        "generated_at": run_utils.utc_now(),
        "protocol": {
            "tier1_loss": t1.get("loss", "mean_squared_error"),
            "tier2_loss": t2.get("loss", "mean_squared_error"),
            "tier3_loss": t3.get("loss", "mean_absolute_error"),
            "tier3_cv_protocol": t3.get("cv_protocol"),
            "note": (
                "Perbandingan 3-tier pada skrip ini bersifat deskriptif. Klaim "
                "terkontrol memakai matriks E0-E7 dan summary_final.json."
            ),
        },
        "tier1_baseline": t1,
        "tier2_manual": t2,
        "tier3_optuna": t3,
        "uncertainty": {
            "method": "moving_block_bootstrap_percentile",
            "confidence": config.CONFIDENCE_LEVEL,
            "n_resamples": config.BOOTSTRAP_RESAMPLES,
            "block_size_days": config.BOOTSTRAP_BLOCK_SIZE,
            "note": (
                "CI menggambarkan ketidakpastian sampling pada 439 hari holdout; "
                "bukan variasi antar-seed maupun antar-inisialisasi model."
            ),
        },
        "confidence_intervals": intervals,
        "paired_differences": paired_differences,
        "multi_seed": seed_studies,
        "baselines": baseline_payload,
        "persistence_comparison": (
            {
                "persistence_metrics": persistence_metrics,
                "tier3_improvement_percent": imp_vs_persistence,
                "note": (
                    "Positif berarti Tier 3 memiliki error lebih rendah daripada "
                    "persistence; negatif berarti Tier 3 kalah."
                ),
            }
            if persistence_metrics
            else None
        ),
        "improvements": {
            "tier3_vs_tier1": imp_vs_t1,
            "tier3_vs_tier2": imp_vs_t2,
        },
    }
    summary_json_path = config.RESULTS_ROOT / "benchmark_comparison_summary.json" if paths.legacy else paths.summary_path
    run_utils.write_json(summary_json_path, summary_data)

    def lookback_of(payload: dict, default: int) -> int:
        return int(payload.get("hyperparameters", {}).get("lookback", default))

    def uncertainty_columns(tier: int) -> dict[str, str]:
        columns = {
            f"{metric} {int(config.CONFIDENCE_LEVEL * 100)}% CI": format_interval(
                intervals[tier][metric]
            )
            for metric in ("RMSE", "MAE", "MAPE")
        }
        for metric in ("RMSE", "MAE", "MAPE"):
            columns[f"{metric} multi-seed"] = format_seed_summary(
                seed_studies.get(tier), metric
            )
        return columns

    def persistence_improvement(metrics_payload: dict) -> dict[str, str]:
        if not persistence_metrics:
            return {
                "Imp RMSE vs Persistence": "-",
                "Imp MAE vs Persistence": "-",
                "Imp MAPE vs Persistence": "-",
            }
        return {
            f"Imp {key} vs Persistence": (
                f"{calculate_improvement(persistence_metrics[key], metrics_payload[key]):+.2f}%"
            )
            for key in ("RMSE", "MAE", "MAPE")
        }

    summary_rows = [
        {
            "Model Tier": "Tier 1: LSTM Default (Baseline)",
            "Lookback": lookback_of(t1, config.TIER1_CONFIG["lookback"]),
            "Loss": t1.get("loss", "mean_squared_error"),
            "RMSE (USD)": m1["RMSE"],
            "MAE (USD)": m1["MAE"],
            "MAPE (%)": m1["MAPE"],
            "Imp RMSE vs T1": "0.0%",
            "Imp MAE vs T1": "0.0%",
            "Imp MAPE vs T1": "0.0%",
            **persistence_improvement(m1),
            **uncertainty_columns(1),
        },
        {
            "Model Tier": "Tier 2: LSTM Manual (Khumaidi dkk.)",
            "Lookback": lookback_of(t2, config.TIER2_CONFIG["lookback"]),
            "Loss": t2.get("loss", "mean_squared_error"),
            "RMSE (USD)": m2["RMSE"],
            "MAE (USD)": m2["MAE"],
            "MAPE (%)": m2["MAPE"],
            "Imp RMSE vs T1": f"{calculate_improvement(m1['RMSE'], m2['RMSE']):+.2f}%",
            "Imp MAE vs T1": f"{calculate_improvement(m1['MAE'], m2['MAE']):+.2f}%",
            "Imp MAPE vs T1": f"{calculate_improvement(m1['MAPE'], m2['MAPE']):+.2f}%",
            **persistence_improvement(m2),
            **uncertainty_columns(2),
        },
        {
            "Model Tier": "Tier 3: LSTM Optuna-TPE (Usulan)",
            "Lookback": lookback_of(t3, config.TIER3_CONFIG["lookback"]),
            "Loss": t3.get("loss", "mean_absolute_error"),
            "RMSE (USD)": m3["RMSE"],
            "MAE (USD)": m3["MAE"],
            "MAPE (%)": m3["MAPE"],
            "Imp RMSE vs T1": f"{imp_vs_t1['RMSE']:+.2f}%",
            "Imp MAE vs T1": f"{imp_vs_t1['MAE']:+.2f}%",
            "Imp MAPE vs T1": f"{imp_vs_t1['MAPE']:+.2f}%",
            **persistence_improvement(m3),
            **uncertainty_columns(3),
        },
    ]
    if persistence_metrics:
        baseline_row = {
            "Model Tier": "Baseline: Persistence (naif)",
            "Lookback": "-",
            "Loss": "-",
            "RMSE (USD)": persistence_metrics["RMSE"],
            "MAE (USD)": persistence_metrics["MAE"],
            "MAPE (%)": persistence_metrics["MAPE"],
            "Imp RMSE vs T1": "-",
            "Imp MAE vs T1": "-",
            "Imp MAPE vs T1": "-",
            "Imp RMSE vs Persistence": "0.0%",
            "Imp MAE vs Persistence": "0.0%",
            "Imp MAPE vs Persistence": "0.0%",
        }
        for metric in ("RMSE", "MAE", "MAPE"):
            entry = (persistence_ci or {}).get(metric)
            baseline_row[f"{metric} {int(config.CONFIDENCE_LEVEL * 100)}% CI"] = (
                format_interval(entry) if entry else "-"
            )
            baseline_row[f"{metric} multi-seed"] = "-"
        summary_rows.append(baseline_row)
    summary_csv_path = config.LEGACY_SUMMARY_CSV if paths.legacy else paths.run_dir / "benchmark_comparison_table.csv"
    pd.DataFrame(summary_rows).to_csv(summary_csv_path, index=False)

    print("\n[4/4] Ringkasan komparasi:")
    print(f"      -> {summary_json_path.resolve()}")
    print(f"      -> {summary_csv_path.resolve()}")
    print("=" * 70)

    if not paths.legacy:
        stage_config = {
            "stage": "eval",
            "run_id": paths.run_id,
            "metrics_dir": str(input_dirs["metrics_dir"].resolve()),
            "predictions_dir": str(input_dirs["predictions_dir"].resolve()),
            "figures_dir": str(figures_dir.resolve()),
            "tier1_loss": t1.get("loss", "mean_squared_error"),
            "tier2_loss": t2.get("loss", "mean_squared_error"),
            "tier3_loss": t3.get("loss", "mean_absolute_error"),
            "tier3_cv_protocol": t3.get("cv_protocol"),
            "bootstrap": {
                "confidence": config.CONFIDENCE_LEVEL,
                "n_resamples": config.BOOTSTRAP_RESAMPLES,
                "block_size_days": config.BOOTSTRAP_BLOCK_SIZE,
            },
            "seed_studies_available": sorted(seed_studies),
            "baseline_available": baseline_payload is not None,
            "seed": args.seed,
        }
        input_paths = [
            input_dirs["metrics_dir"] / name for name in TIER_FILES.values()
        ] + [input_dirs["predictions_dir"] / name for name in PREDICTION_FILES.values()]
        input_paths.extend(
            input_dirs["predictions_dir"] / f"seed_metrics_tier{tier}.json"
            for tier in seed_studies
        )
        if baseline_payload is not None:
            input_paths.extend(
                [
                    input_dirs["metrics_dir"] / "metrics_baselines.json",
                    input_dirs["predictions_dir"] / "predictions_baselines.csv",
                ]
            )
        outputs = [summary_json_path, summary_csv_path, fig1_path, fig2_path]
        if fig3_path:
            outputs.append(fig3_path)
        run_utils.bootstrap_run(paths, "eval", stage_config, inputs=input_paths)
        run_utils.record_stage(
            paths,
            "eval",
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=input_paths,
            outputs=outputs,
            extra={"improvements": summary_data["improvements"]},
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
