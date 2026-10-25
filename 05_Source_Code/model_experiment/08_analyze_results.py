"""
08_analyze_results.py - Final analysis for the controlled matrix E0-E7.

Consumes the artifacts produced by ``experiment_matrix.py`` (and the tier
scripts) and writes:

- ``summary_final.json`` - the single source of truth for thesis numbers;
- ``residual_analysis.json`` - residual distribution, worst cases, ex-ante
  regime/volatility breakdown, and directional accuracy;
- ``benchmark_matrix_table.csv`` / ``.md`` - complete comparison table;
- ``figures/matrix_metrics.png``, ``figures/residual_abs_boxplot.png``,
  ``figures/error_by_regime.png``.

Bootstrap CIs describe holdout sampling uncertainty (moving-block, 7 days,
2.000 resamples). Multi-seed mean +/- std describes initialization/training
variability. The two are reported separately and must not be conflated.

Usage:
    python 05_Source_Code/model_experiment/08_analyze_results.py \
        --run-id final_matrix_20261025 --publish
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import analysis_utils
import config
import run_utils
import stats_utils
from data_utils import load_processed_data
from experiment_matrix import EXPERIMENTS, EXPERIMENTS_BY_KEY, METRICS_FILES
from experiment_utils import compute_metrics, resolve_processed_dir

PREDICTION_FILES: dict[str, tuple[str, str]] = {
    "E0": ("predictions_baselines.csv", "predicted_persistence"),
    "E1": ("predictions_tier1.csv", "predicted_close_tier1"),
    "E2": ("predictions_tier2.csv", "predicted_close_tier2"),
    "E3": ("predictions_e3_mse_none.csv", "predicted_close_e3_mse_none"),
    "E4": ("predictions_e4_mae_none.csv", "predicted_close_e4_mae_none"),
    "E5": ("predictions_e5_mse_plateau.csv", "predicted_close_e5_mse_plateau"),
    "E6": ("predictions_e6_mae_plateau.csv", "predicted_close_e6_mae_plateau"),
    "E7": ("predictions_tier3.csv", "predicted_close_tier3"),
}

REFERENCE_ORDER = ("E1", "E7", "E2", "E3", "E4", "E5", "E6", "E0")

PAIRED_COMPARISONS = (
    ("E0", "E7", "E7_vs_persistence", "negatif = E7 lebih baik"),
    ("E1", "E7", "E7_vs_tier1", "negatif = E7 lebih baik"),
    ("E2", "E7", "E7_vs_tier2", "negatif = E7 lebih baik"),
    ("E6", "E7", "E7_vs_E6", "negatif = HPO penuh lebih baik"),
    ("E1", "E3", "E1_vs_E3", "negatif = parameter Tier 3 lebih baik"),
    ("E3", "E4", "E4_vs_E3", "negatif = MAE lebih baik"),
    ("E3", "E5", "E5_vs_E3", "negatif = scheduler lebih baik"),
    ("E3", "E6", "E6_vs_E3", "negatif = gabungan lebih baik"),
    ("E4", "E6", "E6_vs_E4", "negatif = tambahan scheduler lebih baik"),
    ("E5", "E6", "E6_vs_E5", "negatif = tambahan MAE lebih baik"),
)

METRICS = ("RMSE", "MAE", "MAPE")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protocol_hash_issues(root: Path, run_dir: Path) -> dict[str, dict]:
    """Compare recorded protocol/environment hashes with the current files."""
    recorded = run_utils.read_json(run_dir / "data_hash.json", default={})
    issues: dict[str, dict] = {}
    for relative in ("docs/PROTOCOL.md", "requirements.txt"):
        path = root / relative
        if not path.exists():
            issues[relative] = {"recorded": recorded.get(relative), "actual": "missing"}
            continue
        actual = file_sha256(path)
        if recorded.get(relative) != actual:
            issues[relative] = {"recorded": recorded.get(relative), "actual": actual}
    return issues


def normalize_dates(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"]).dt.strftime("%Y-%m-%d")
    if frame["date"].duplicated().any():
        raise ValueError("Kolom date berisi duplikat")
    return frame


def load_predictions(paths: run_utils.RunPaths) -> tuple[dict[str, pd.DataFrame], list[str]]:
    frames: dict[str, pd.DataFrame] = {}
    missing: list[str] = []
    for experiment in EXPERIMENTS:
        filename, column = PREDICTION_FILES[experiment.key]
        path = paths.predictions_dir / filename
        if not path.exists():
            missing.append(experiment.key)
            continue
        frame = normalize_dates(pd.read_csv(path))
        required = {"date", "actual_close", column}
        if not required.issubset(frame.columns):
            raise ValueError(
                f"{path.name} tidak memuat kolom {sorted(required)}; "
                f"ditemukan {list(frame.columns)}"
            )
        frames[experiment.key] = frame
    return frames, missing


def choose_reference(frames: dict[str, pd.DataFrame]) -> str:
    for key in REFERENCE_ORDER:
        if key in frames:
            return key
    raise ValueError("Tidak ada prediksi model yang bisa dipakai sebagai referensi")


def align_frames(
    frames: dict[str, pd.DataFrame], reference_key: str
) -> tuple[pd.Series, pd.DataFrame, dict[str, np.ndarray]]:
    reference = frames[reference_key].set_index("date").sort_index()
    dates = reference.index
    reference_actual = reference["actual_close"].to_numpy(dtype=float)
    aligned: dict[str, np.ndarray] = {}
    for key, frame in frames.items():
        indexed = frame.set_index("date").sort_index()
        if not indexed.index.equals(dates):
            raise ValueError(f"Tanggal prediksi {key} tidak identik dengan {reference_key}")
        _, column = PREDICTION_FILES[key]
        predicted = indexed[column].to_numpy(dtype=float)
        if not np.isfinite(predicted).all():
            raise ValueError(f"Prediksi {key} mengandung NaN/inf")
        np.testing.assert_allclose(
            indexed["actual_close"].to_numpy(dtype=float),
            reference_actual,
            rtol=0,
            atol=0.02,
            err_msg=f"actual_close {key} berbeda dari referensi {reference_key}",
        )
        aligned[key] = predicted
    return dates, pd.Series(reference_actual, index=dates), aligned


def load_metrics_payload(paths: run_utils.RunPaths, key: str) -> dict:
    path = paths.run_dir / METRICS_FILES[key]
    if not path.exists():
        return {}
    payload = run_utils.read_json(path)
    if key == "E0":
        return payload.get("baselines", {}).get("persistence", {})
    return payload


def recorded_metrics(payload: dict, key: str) -> dict[str, float] | None:
    if key == "E0":
        return payload.get("metrics")
    return payload.get("metrics")


def multi_seed_payload(payload: dict, key: str) -> dict | None:
    if key == "E0":
        return None
    return payload.get("multi_seed")


def seed_coverage(models: dict[str, dict], expected_seeds: int) -> dict[str, int | None]:
    """Report models whose multi-seed aggregate does not match the plan."""
    if expected_seeds <= 1:
        return {}
    issues: dict[str, int | None] = {}
    for key, entry in models.items():
        if key == "E0":
            continue
        aggregate = (entry.get("multi_seed") or {}).get("aggregate") or {}
        n_seeds = (aggregate.get("MAE") or {}).get("n_seeds")
        if n_seeds != expected_seeds:
            issues[key] = n_seeds
    return issues


def dataset_statistics(train_df: pd.DataFrame, test_df: pd.DataFrame) -> dict:
    """Descriptive statistics used by the thesis data table."""
    combined = pd.concat([train_df, test_df], ignore_index=True)
    close = combined["close"].astype(float)
    dates = pd.to_datetime(combined["date"])
    return {
        "n_observations": int(len(combined)),
        "period": [str(dates.iloc[0].date()), str(dates.iloc[-1].date())],
        "min": float(close.min()),
        "min_date": str(dates.loc[close.idxmin()].date()),
        "max": float(close.max()),
        "max_date": str(dates.loc[close.idxmax()].date()),
        "mean": float(close.mean()),
        "median": float(close.median()),
        "std": float(close.std(ddof=1)),
    }


def training_summary(payload: dict, key: str) -> dict:
    """Configuration and cost fields used by the thesis tables."""
    if key == "E0":
        return {"model": "persistence"}
    hyperparameters = payload.get("hyperparameters") or {}
    summary = {
        "loss": payload.get("loss"),
        "scheduler": payload.get("scheduler"),
        "early_stopping": payload.get("early_stopping"),
        "hyperparameters": hyperparameters,
        "epochs_run": hyperparameters.get("epochs_run"),
        "training_time_seconds": payload.get(
            "final_training_time_seconds", payload.get("training_time_seconds")
        ),
    }
    for field in (
        "total_trials",
        "complete_trials",
        "pruned_trials",
        "best_trial_number",
        "best_cv_loss",
        "sampler",
        "sampler_seed",
        "pruner",
        "optimization_time_seconds",
        "cv_protocol",
    ):
        if field in payload:
            summary[field] = payload[field]
    return summary


def check_metric_consistency(
    key: str,
    recorded: dict[str, float] | None,
    recomputed: dict[str, float],
) -> None:
    if not recorded:
        return
    for metric in METRICS:
        if metric not in recorded:
            continue
        if abs(float(recorded[metric]) - float(recomputed[metric])) > 0.05:
            raise ValueError(
                f"Metrik {metric} {key} tidak cocok: JSON={recorded[metric]}, "
                f"recomputed={recomputed[metric]:.4f}"
            )


def build_entry(
    experiment_key: str,
    *,
    payload: dict,
    actual: np.ndarray,
    predicted: np.ndarray,
    dates: pd.Series,
    previous_close: np.ndarray,
    context: pd.DataFrame,
    n_worst: int,
) -> dict:
    experiment = EXPERIMENTS_BY_KEY[experiment_key]
    metrics = compute_metrics(actual, predicted)
    recorded = recorded_metrics(payload, experiment_key)
    check_metric_consistency(experiment_key, recorded, metrics)

    intervals = stats_utils.bootstrap_metric_ci(
        actual,
        predicted,
        n_resamples=config.BOOTSTRAP_RESAMPLES,
        confidence=config.CONFIDENCE_LEVEL,
        block_size=config.BOOTSTRAP_BLOCK_SIZE,
        seed=42,
    )
    residuals = analysis_utils.residual_statistics(actual, predicted)
    direction = analysis_utils.directional_accuracy(actual, predicted, previous_close)
    if experiment_key == "E0":
        direction = {
            **direction,
            "interpretable": False,
            "note": (
                "Persistence selalu memprediksi sama dengan close sebelumnya, "
                "sehingga arah prediksi selalu flat dan accuracy 0% tidak "
                "informatif. Jangan bandingkan angka ini dengan model LSTM."
            ),
        }
    else:
        direction = {**direction, "interpretable": True}
    regime = analysis_utils.regime_summary(context, actual, predicted)
    high_volatility = analysis_utils.metrics_for_mask(
        actual, predicted, context["high_volatility"].to_numpy()
    )
    normal_volatility = analysis_utils.metrics_for_mask(
        actual, predicted, ~context["high_volatility"].to_numpy()
    )
    seed_payload = multi_seed_payload(payload, experiment_key)

    return {
        "run": experiment.key,
        "model": experiment.label,
        "role": experiment.role,
        "loss": experiment.loss or "-",
        "scheduler": experiment.scheduler or "-",
        "hpo": experiment.hpo,
        "metrics": {metric: float(metrics[metric]) for metric in METRICS},
        "recorded_metrics": recorded,
        "confidence_intervals": intervals,
        "multi_seed": seed_payload,
        "residuals": residuals,
        "directional_accuracy": direction,
        "regime": regime,
        "high_volatility": high_volatility,
        "normal_volatility": normal_volatility,
        "worst_cases": analysis_utils.worst_cases(
            dates.to_numpy(), actual, predicted, n=n_worst
        ),
        "metrics_file": METRICS_FILES[experiment_key],
        "prediction_file": PREDICTION_FILES[experiment_key][0],
        "prediction_column": PREDICTION_FILES[experiment_key][1],
        "n_predictions": int(len(actual)),
    }


def add_improvements(models: dict[str, dict]) -> None:
    references = {"persistence": "E0", "tier1": "E1", "tier2": "E2", "e3": "E3"}
    for entry in models.values():
        entry["improvement_vs"] = {}
        for label, reference_key in references.items():
            reference = models.get(reference_key)
            if not reference:
                continue
            entry["improvement_vs"][label] = {
                metric: analysis_utils.improvement_percent(
                    reference["metrics"][metric], entry["metrics"][metric]
                )
                for metric in METRICS
            }


def build_paired_comparisons(
    aligned: dict[str, np.ndarray], actual: np.ndarray
) -> dict:
    comparisons: dict[str, dict] = {}
    for key_a, key_b, label, direction in PAIRED_COMPARISONS:
        if key_a not in aligned or key_b not in aligned:
            continue
        comparisons[label] = {
            "model_a": key_a,
            "model_b": key_b,
            "direction": direction,
            "metrics": {
                metric: stats_utils.paired_bootstrap_difference(
                    actual,
                    aligned[key_a],
                    aligned[key_b],
                    metric=metric,
                    n_resamples=config.BOOTSTRAP_RESAMPLES,
                    confidence=config.CONFIDENCE_LEVEL,
                    block_size=config.BOOTSTRAP_BLOCK_SIZE,
                    seed=42,
                )
                for metric in METRICS
            },
        }
    return comparisons


def build_verdict(models: dict[str, dict], comparisons: dict) -> dict:
    if "E7" not in models or "E0" not in models:
        return {
            "status": "incomplete",
            "claim": "E7 atau E0 belum tersedia; verdict belum bisa dihitung.",
        }
    proposed = models["E7"]["metrics"]
    persistence = models["E0"]["metrics"]
    mae_comparison = comparisons.get("E7_vs_persistence", {}).get("metrics", {}).get("MAE")
    point_better = proposed["MAE"] < persistence["MAE"]
    ci_low = mae_comparison["ci_low"] if mae_comparison else None
    ci_high = mae_comparison["ci_high"] if mae_comparison else None
    ci_excludes_zero = bool(
        ci_low is not None and ci_high is not None and (ci_low > 0 or ci_high < 0)
    )
    ci_favors_proposed = bool(ci_high is not None and ci_high < 0)
    if point_better and ci_favors_proposed:
        status = "proposed_lower_mae_ci_excludes_zero"
        ci_direction = "proposed_better"
        claim = (
            "E7 memiliki MAE lebih rendah daripada persistence dan CI selisih "
            "berpasangan tidak melewati nol. Tetap sebutkan keterbatasan "
            "one-step-ahead, satu aset, dan satu periode uji."
        )
    elif point_better:
        status = "proposed_lower_mae_ci_includes_zero"
        ci_direction = "inconclusive"
        claim = (
            "E7 memiliki MAE titik lebih rendah daripada persistence, tetapi CI "
            "selisih berpasangan masih melewati nol. Jangan sebut signifikan."
        )
    else:
        status = "proposed_not_better_than_persistence"
        if ci_low is not None and ci_low > 0:
            ci_direction = "persistence_better"
            claim = (
                "E7 memiliki MAE lebih tinggi daripada persistence dan CI selisih "
                "berpasangan seluruhnya di atas nol, sehingga hasil ini secara "
                "statistik lebih buruk. Laporkan hasil negatif ini secara eksplisit "
                "dan jangan memilih baseline yang menguntungkan."
            )
        else:
            ci_direction = "inconclusive"
            claim = (
                "E7 tidak lebih baik daripada persistence pada MAE titik. Laporkan "
                "hasil negatif ini secara eksplisit; jangan memilih baseline yang "
                "menguntungkan."
            )
    return {
        "status": status,
        "claim": claim,
        "proposed_mae": float(proposed["MAE"]),
        "persistence_mae": float(persistence["MAE"]),
        "relative_improvement_percent": float(
            analysis_utils.improvement_percent(persistence["MAE"], proposed["MAE"])
        ),
        "paired_mae_ci_low": mae_comparison["ci_low"] if mae_comparison else None,
        "paired_mae_ci_high": mae_comparison["ci_high"] if mae_comparison else None,
        "paired_mae_p_value": mae_comparison["p_value"] if mae_comparison else None,
        "ci_excludes_zero": ci_excludes_zero,
        "ci_favors_proposed": ci_favors_proposed,
        "ci_direction": ci_direction,
    }


def build_table(models: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for key, entry in models.items():
        metrics = entry["metrics"]
        intervals = entry["confidence_intervals"]
        aggregate = (entry["multi_seed"] or {}).get("aggregate", {})
        row = {
            "Run": key,
            "Model": entry["model"],
            "Role": entry["role"],
            "Loss": entry["loss"],
            "Scheduler": entry["scheduler"],
            "HPO": entry["hpo"],
            "RMSE (USD)": metrics["RMSE"],
            "MAE (USD)": metrics["MAE"],
            "MAPE (%)": metrics["MAPE"],
            "RMSE CI low": intervals["RMSE"]["ci_low"],
            "RMSE CI high": intervals["RMSE"]["ci_high"],
            "MAE CI low": intervals["MAE"]["ci_low"],
            "MAE CI high": intervals["MAE"]["ci_high"],
            "MAPE CI low": intervals["MAPE"]["ci_low"],
            "MAPE CI high": intervals["MAPE"]["ci_high"],
            "Directional accuracy": (
                entry["directional_accuracy"]["accuracy"]
                if entry["directional_accuracy"].get("interpretable", True)
                else None
            ),
            "Worst abs error": entry["residuals"]["max_absolute_error"],
            "High-vol MAE": (entry["high_volatility"] or {}).get("MAE"),
            "n": entry["n_predictions"],
        }
        for metric in METRICS:
            metric_key = metric.lower()
            row[f"{metric} mean"] = aggregate.get(metric, {}).get("mean")
            row[f"{metric} std"] = aggregate.get(metric, {}).get("std")
            row[f"{metric} n seeds"] = aggregate.get(metric, {}).get("n_seeds")
        for reference in ("persistence", "tier1", "tier2", "e3"):
            improvement = entry["improvement_vs"].get(reference, {})
            for metric in METRICS:
                row[f"Imp {metric} vs {reference}"] = improvement.get(metric)
        rows.append(row)
    return pd.DataFrame(rows)


def format_markdown_table(frame: pd.DataFrame) -> str:
    def fmt(value) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return "-"
        if isinstance(value, (bool, np.bool_)):
            return "Ya" if value else "Tidak"
        if isinstance(value, (int, np.integer)):
            return str(value)
        if isinstance(value, (float, np.floating)):
            return f"{value:,.2f}"
        return str(value)

    headers = list(frame.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(fmt(row[column]) for column in headers) + " |")
    return "\n".join(lines) + "\n"


def plot_metric_bars(models: dict[str, dict], output_path: Path) -> None:
    keys = list(models)
    rmse = [models[key]["metrics"]["RMSE"] for key in keys]
    mae = [models[key]["metrics"]["MAE"] for key in keys]
    rmse_errors = np.array(
        [
            [
                models[key]["metrics"]["RMSE"] - models[key]["confidence_intervals"]["RMSE"]["ci_low"]
                for key in keys
            ],
            [
                models[key]["confidence_intervals"]["RMSE"]["ci_high"] - models[key]["metrics"]["RMSE"]
                for key in keys
            ],
        ]
    )
    mae_errors = np.array(
        [
            [
                models[key]["metrics"]["MAE"] - models[key]["confidence_intervals"]["MAE"]["ci_low"]
                for key in keys
            ],
            [
                models[key]["confidence_intervals"]["MAE"]["ci_high"] - models[key]["metrics"]["MAE"]
                for key in keys
            ],
        ]
    )
    x = np.arange(len(keys))
    width = 0.38
    fig, axis = plt.subplots(figsize=(12, 6))
    axis.bar(
        x - width / 2,
        rmse,
        width,
        label="RMSE",
        color="#2563EB",
        yerr=rmse_errors,
        capsize=4,
        error_kw={"elinewidth": 1, "ecolor": "#111827"},
    )
    axis.bar(
        x + width / 2,
        mae,
        width,
        label="MAE",
        color="#F59E0B",
        yerr=mae_errors,
        capsize=4,
        error_kw={"elinewidth": 1, "ecolor": "#111827"},
    )
    axis.set_xticks(x, keys)
    axis.set_ylabel("Error (USD)")
    axis.set_title("Perbandingan RMSE dan MAE Matriks E0-E7 (95% bootstrap CI)")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_residual_boxplot(models: dict[str, dict], actual, aligned, output_path: Path) -> None:
    keys = list(models)
    data = [np.abs(actual - aligned[key]) for key in keys]
    fig, axis = plt.subplots(figsize=(12, 6))
    axis.boxplot(data, tick_labels=keys, showfliers=False)
    axis.set_yscale("log")
    axis.set_ylabel("Absolute error (USD, log scale)")
    axis.set_title("Distribusi Absolute Error per Run (tanpa outlier ekstrem)")
    axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_regime_bars(models: dict[str, dict], output_path: Path) -> None:
    keys = [key for key in ("E0", "E1", "E3", "E6", "E7") if key in models]
    regimes = ("bull", "bear", "sideways")
    x = np.arange(len(regimes))
    width = 0.8 / max(len(keys), 1)
    fig, axis = plt.subplots(figsize=(10, 6))
    for index, key in enumerate(keys):
        values = [
            (models[key]["regime"].get(regime) or {}).get("MAE", np.nan)
            for regime in regimes
        ]
        axis.bar(x + (index - (len(keys) - 1) / 2) * width, values, width, label=key)
    axis.set_xticks(x, regimes)
    axis.set_ylabel("MAE (USD)")
    axis.set_title("MAE per Rezim Pasar Ex-Ante (label 30 hari sebelumnya)")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analisis final matriks E0-E7")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Izinkan run tanpa semua E0-E7 (untuk smoke test)",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Salin summary_final.json ke results/summary_final.json",
    )
    parser.add_argument("--n-worst", type=int, default=5)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="analysis")
    if paths.legacy:
        print("[ERROR] Analisis hanya untuk run baru di results/runs/{run_id}.")
        return 2

    frames, missing = load_predictions(paths)
    if not frames:
        print("[ERROR] Tidak ada file prediksi yang ditemukan.")
        return 2
    if missing and not args.allow_partial:
        print(f"[ERROR] Run belum lengkap. Model hilang: {', '.join(missing)}")
        print("        Gunakan --allow-partial hanya untuk smoke test.")
        return 2

    processed_dir, data_source = resolve_processed_dir(
        Path(args.processed_dir) if args.processed_dir else paths.processed_dir,
        config.PROCESSED_DIR,
    )
    train_df, test_df, _ = load_processed_data(processed_dir)

    reference_key = choose_reference(frames)
    dates, actual_series, aligned = align_frames(frames, reference_key)
    actual = actual_series.to_numpy(dtype=float)
    combined_close = np.concatenate(
        [train_df["close"].to_numpy(dtype=float), test_df["close"].to_numpy(dtype=float)]
    )
    previous_close = combined_close[len(train_df) - 1 : -1]
    if len(previous_close) != len(actual):
        raise ValueError("previous_close tidak sejajar dengan holdout")

    processed_dates = (
        pd.to_datetime(test_df["date"]).dt.strftime("%Y-%m-%d").to_numpy()
    )
    if list(processed_dates) != list(dates):
        raise ValueError("Tanggal prediksi tidak identik dengan tanggal holdout processed")
    np.testing.assert_allclose(
        actual,
        test_df["close"].to_numpy(dtype=float),
        rtol=0,
        atol=0.02,
        err_msg="actual_close prediksi tidak cocok dengan close holdout processed",
    )

    context = analysis_utils.market_context(
        train_df["close"].to_numpy(dtype=float),
        test_df["close"].to_numpy(dtype=float),
        test_df["date"],
    )

    models: dict[str, dict] = {}
    for experiment in EXPERIMENTS:
        if experiment.key not in frames:
            continue
        payload = load_metrics_payload(paths, experiment.key)
        models[experiment.key] = build_entry(
            experiment.key,
            payload=payload,
            actual=actual,
            predicted=aligned[experiment.key],
            dates=dates,
            previous_close=previous_close,
            context=context,
            n_worst=args.n_worst,
        )
        models[experiment.key]["training"] = training_summary(
            payload, experiment.key
        )

    add_improvements(models)
    plan_payload = run_utils.read_json(
        paths.run_dir / "experiment_matrix_plan.json", default={}
    )
    expected_seeds = len(plan_payload.get("seeds") or []) or len(config.DEFAULT_SEEDS)
    seed_issues = seed_coverage(models, expected_seeds)
    if seed_issues and not args.allow_partial:
        print(
            "[ERROR] Cakupan seed tidak sesuai plan: "
            f"diharapkan {expected_seeds}, ditemukan {seed_issues}."
        )
        return 2
    hash_issues = protocol_hash_issues(paths.root, paths.run_dir)
    comparisons = build_paired_comparisons(aligned, actual)
    verdict = build_verdict(models, comparisons)
    ranking = sorted(
        (
            {"run": key, "model": entry["model"], "MAE": entry["metrics"]["MAE"]}
            for key, entry in models.items()
        ),
        key=lambda row: row["MAE"],
    )
    lstm_ranking = [row for row in ranking if row["run"] != "E0"]

    frame = build_table(models)
    table_csv_path = paths.run_dir / "benchmark_matrix_table.csv"
    frame.to_csv(table_csv_path, index=False)
    table_md_path = paths.run_dir / "benchmark_matrix_table.md"
    table_md_path.write_text(format_markdown_table(frame), encoding="utf-8")

    residual_payload = {
        "run_id": paths.run_id,
        "generated_at": run_utils.utc_now(),
        "regime_definition": {
            "type": "ex_ante_trailing_30d_return",
            "bull_threshold": context.attrs["bull_threshold"],
            "bear_threshold": context.attrs["bear_threshold"],
            "volatility_window_days": 7,
            "high_volatility_threshold": context.attrs["volatility_threshold"],
            "note": (
                "Label hari t memakai data sampai t-1; bukan input model dan "
                "bukan klaim kausal."
            ),
        },
        "regime_counts": context["regime"].value_counts().to_dict(),
        "high_volatility_days": int(context["high_volatility"].sum()),
        "models": {
            key: {
                "residuals": entry["residuals"],
                "directional_accuracy": entry["directional_accuracy"],
                "regime": entry["regime"],
                "high_volatility": entry["high_volatility"],
                "normal_volatility": entry["normal_volatility"],
                "worst_cases": entry["worst_cases"],
            }
            for key, entry in models.items()
        },
    }
    residual_path = paths.run_dir / "residual_analysis.json"
    run_utils.write_json(residual_path, residual_payload)

    figures = {
        "matrix_metrics": paths.figures_dir / "matrix_metrics.png",
        "residual_abs_boxplot": paths.figures_dir / "residual_abs_boxplot.png",
        "error_by_regime": paths.figures_dir / "error_by_regime.png",
    }
    plot_metric_bars(models, figures["matrix_metrics"])
    plot_residual_boxplot(models, actual, aligned, figures["residual_abs_boxplot"])
    plot_regime_bars(models, figures["error_by_regime"])

    summary = {
        "schema_version": 1,
        "run_id": paths.run_id,
        "generated_at": run_utils.utc_now(),
        "status": "partial" if missing else "complete",
        "missing_models": missing,
        "data": {
            "processed_dir": str(processed_dir.resolve()),
            "source": data_source,
            "source_note": (
                "'legacy' berarti folder processed bersama yang dibekukan, "
                "bukan hasil eksperimen lama."
            ),
            "n_train": int(len(train_df)),
            "n_test": int(len(test_df)),
            "test_period": [str(processed_dates[0]), str(processed_dates[-1])],
            "statistics": dataset_statistics(train_df, test_df),
        },
        "baselines": (
            run_utils.read_json(paths.metrics_dir / "metrics_baselines.json", default={})
            .get("baselines", {})
        ),
        "protocol": {
            "reference_actual": f"prediction CSV {reference_key} (inverse-transformed USD)",
            "metrics": "RMSE/MAE/MAPE on 439 holdout days",
            "bootstrap": {
                "method": "moving_block_percentile",
                "n_resamples": config.BOOTSTRAP_RESAMPLES,
                "block_size_days": config.BOOTSTRAP_BLOCK_SIZE,
                "confidence": config.CONFIDENCE_LEVEL,
                "seed": 42,
            },
            "multi_seed": "mean +/- std from seed_metrics/multi_seed aggregate",
            "paired_comparison": (
                "difference = model_b - model_a on identical dates; "
                "p_value is descriptive, not a formal significance test"
            ),
        },
        "data_hash": run_utils.read_json(paths.run_dir / "data_hash.json", default={}),
        "environment": run_utils.read_json(paths.run_dir / "env.json", default={}),
        "primary_metric": "MAE",
        "expected_seeds": expected_seeds,
        "seed_coverage_issues": seed_issues,
        "protocol_hash_issues": hash_issues,
        "claim_rule": {
            "metric": "MAE",
            "rule": (
                "Klaim keunggulan hanya bila MAE titik E7 lebih rendah dan CI "
                "selisih berpasangan E7-persistence tidak melewati nol."
            ),
            "comparison": "E7_vs_persistence",
        },
        "groups": {
            "baseline": ["E0"],
            "control": ["E1"],
            "literature_reference": ["E2"],
            "ablation": ["E3", "E4", "E5", "E6"],
            "proposed_model": ["E7"],
        },
        "final_configuration": models.get("E7", {}).get("training"),
        "training": {
            key: entry.get("training", {}) for key, entry in models.items()
        },
        "ranking_by_mae": ranking,
        "best_by_mae": ranking[0] if ranking else None,
        "lstm_ranking_by_mae": lstm_ranking,
        "best_lstm_by_mae": lstm_ranking[0] if lstm_ranking else None,
        "proposed_model": "E7",
        "headline": verdict,
        "models": models,
        "paired_comparisons": comparisons,
        "artifacts": {
            "run_dir": str(paths.run_dir.resolve()),
            "figures_dir": str(paths.figures_dir.resolve()),
            "predictions_dir": str(paths.predictions_dir.resolve()),
            "figures": {
                name: str(path.resolve()) for name, path in figures.items()
            },
        },
        "warnings": [
            "E0 actual_close berasal dari CSV baseline; model LSTM memakai actual_close hasil inverse transform. Selisih maksimum yang ditoleransi 0.02 USD.",
            "Bootstrap CI mengukur ketidakpastian sampling 439 hari holdout, bukan variasi antar-seed.",
            "p_value pada paired bootstrap adalah ukuran stabilitas deskriptif, bukan uji formal.",
            "Regime dan high-volatility adalah label ex-ante untuk analisis, bukan input model.",
            "Directional accuracy E0 (persistence) bersifat degenerat dan dilaporkan sebagai kosong.",
            "Angka pada tabel memakai seed utama; agregat multi-seed dilaporkan terpisah.",
        ]
        + (["Run ini parsial; jangan dipakai untuk klaim final."] if missing else [])
        + (
            [f"Cakupan seed tidak lengkap: {seed_issues}; diharapkan {expected_seeds}."]
            if seed_issues
            else []
        )
        + (
            [f"Hash protokol/requirements berubah sejak run dimulai: {hash_issues}."]
            if hash_issues
            else []
        ),
    }

    summary_path = paths.run_dir / "summary_final.json"
    run_utils.write_json(summary_path, summary)
    published_path = None
    if args.publish:
        if missing:
            print("[ERROR] --publish ditolak karena run parsial.")
            return 2
        if seed_issues:
            print(
                "[ERROR] --publish ditolak karena cakupan seed tidak lengkap: "
                f"{seed_issues} (diharapkan {expected_seeds})."
            )
            return 2
        if hash_issues:
            print(
                "[ERROR] --publish ditolak karena hash protokol/requirements "
                f"berubah sejak run dimulai: {hash_issues}."
            )
            return 2
        matrix_results = run_utils.read_json(
            paths.run_dir / "experiment_matrix_results.json", default={}
        )
        if matrix_results.get("status") != "success":
            print(
                "[ERROR] --publish ditolak: experiment_matrix_results.json "
                f"berstatus {matrix_results.get('status')!r}."
            )
            return 2
        failed = {
            key: status
            for key, status in matrix_results.get("statuses", {}).items()
            if status != "success"
        }
        if failed:
            print(f"[ERROR] --publish ditolak: eksperimen gagal {failed}.")
            return 2
        published_path = config.RESULTS_ROOT / "summary_final.json"
        run_utils.write_json(published_path, summary)

    print("=" * 78)
    print(f"ANALISIS FINAL: {paths.run_id}")
    print("=" * 78)
    print(f"Referensi actual : {reference_key}")
    print(f"Model tersedia   : {', '.join(models)}")
    if missing:
        print(f"Model hilang     : {', '.join(missing)} (parsial)")
    print("\nPeringkat MAE:")
    for position, row in enumerate(ranking, start=1):
        print(f"  {position}. {row['run']:<3} {row['MAE']:>12,.2f} USD  {row['model']}")
    if lstm_ranking:
        best_lstm = lstm_ranking[0]
        print(
            f"\nLSTM terbaik (MAE): {best_lstm['run']} "
            f"{best_lstm['MAE']:,.2f} USD  {best_lstm['model']}"
        )
    print("\nHeadline:")
    print(f"  {verdict['claim']}")
    if "relative_improvement_percent" in verdict:
        print(
            f"  E7 vs persistence (MAE): "
            f"{verdict['relative_improvement_percent']:+.2f}% "
            f"(CI selisih {verdict['paired_mae_ci_low']:,.2f} s.d. "
            f"{verdict['paired_mae_ci_high']:,.2f})"
        )
    print("\nArtefak:")
    print(f"  Summary    -> {summary_path.resolve()}")
    print(f"  Residual   -> {residual_path.resolve()}")
    print(f"  Tabel CSV  -> {table_csv_path.resolve()}")
    print(f"  Tabel MD   -> {table_md_path.resolve()}")
    for label, path in figures.items():
        print(f"  Figure {label:<20} -> {path.resolve()}")
    if published_path:
        print(f"  Published  -> {published_path.resolve()}")
    print("=" * 78)

    inputs = [
        paths.run_dir / METRICS_FILES[key]
        for key in models
        if (paths.run_dir / METRICS_FILES[key]).exists()
    ]
    inputs.extend(
        paths.predictions_dir / PREDICTION_FILES[key][0]
        for key in models
        if (paths.predictions_dir / PREDICTION_FILES[key][0]).exists()
    )
    inputs.extend(
        [
            processed_dir / "train_insample.csv",
            processed_dir / "test_outofsample.csv",
        ]
    )
    run_utils.bootstrap_run(
        paths,
        "analysis",
        {
            "stage": "analysis",
            "reference_model": reference_key,
            "models": list(models),
            "missing_models": missing,
            "bootstrap_resamples": config.BOOTSTRAP_RESAMPLES,
            "bootstrap_block_size": config.BOOTSTRAP_BLOCK_SIZE,
            "publish": args.publish,
        },
        inputs=inputs,
    )
    run_utils.record_stage(
        paths,
        "analysis",
        status="success",
        started_at=started_at,
        stage_config={
            "stage": "analysis",
            "reference_model": reference_key,
            "models": list(models),
            "missing_models": missing,
            "publish": args.publish,
        },
        inputs=inputs,
        outputs=[
            summary_path,
            residual_path,
            table_csv_path,
            table_md_path,
            *figures.values(),
            *([published_path] if published_path else []),
        ],
        extra={"headline": verdict, "best_by_mae": ranking[0] if ranking else None},
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
