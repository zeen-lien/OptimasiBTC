"""
baselines.py - Naive forecasting baselines for the 439-day holdout.

Every baseline is causal: the prediction for day ``t`` uses only actual
closes observed before ``t`` (including the last in-sample day for the first
holdout day). No fitted parameters are estimated on the holdout.

Baselines:
- persistence: ``y_hat[t] = y[t-1]``
- drift: ``y_hat[t] = y[t-1] + mean(diff(in_sample))``
- seasonal_naive_7: ``y_hat[t] = y[t-7]``
- moving_average_7: ``y_hat[t] = mean(y[t-7:t])``

Outputs:
- ``metrics/metrics_baselines.json``
- ``predictions/predictions_baselines.csv``
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import config
import run_utils
from data_utils import load_processed_data
from experiment_utils import compute_metrics, resolve_processed_dir, rounded_metrics
from stats_utils import bootstrap_metric_ci

BASELINE_COLUMNS = {
    "persistence": "predicted_persistence",
    "drift": "predicted_drift",
    "seasonal_naive_7": "predicted_seasonal_naive_7",
    "moving_average_7": "predicted_moving_average_7",
}

BASELINE_DESCRIPTIONS = {
    "persistence": "y_hat[t] = y[t-1]; random-walk tanpa perubahan",
    "drift": "y_hat[t] = y[t-1] + rata-rata selisih harian in-sample",
    "seasonal_naive_7": "y_hat[t] = y[t-7]; pola mingguan",
    "moving_average_7": "y_hat[t] = rata-rata 7 observasi terakhir sebelum t",
}


def build_baseline_predictions(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    seasonal_period: int = 7,
) -> pd.DataFrame:
    """Construct causal baseline forecasts aligned with ``test_df``."""
    train_close = train_df["close"].to_numpy(dtype=float)
    test_close = test_df["close"].to_numpy(dtype=float)
    if len(train_close) <= seasonal_period:
        raise ValueError(
            f"In-sample ({len(train_close)}) harus lebih panjang dari seasonal period "
            f"({seasonal_period})"
        )

    full = np.concatenate([train_close, test_close])
    test_positions = np.arange(len(train_close), len(full))

    persistence = full[test_positions - 1]
    drift_per_day = float(np.mean(np.diff(train_close)))
    drift = full[test_positions - 1] + drift_per_day
    seasonal = full[test_positions - seasonal_period]
    moving_average = np.array(
        [full[position - seasonal_period : position].mean() for position in test_positions]
    )

    if not np.all(np.isfinite(drift)) or np.any(drift <= 0):
        raise ValueError("Baseline drift menghasilkan nilai tidak valid")

    return pd.DataFrame(
        {
            "date": pd.to_datetime(test_df["date"]).dt.strftime("%Y-%m-%d"),
            "actual_close": test_close,
            "predicted_persistence": persistence,
            "predicted_drift": drift,
            "predicted_seasonal_naive_7": seasonal,
            "predicted_moving_average_7": moving_average,
        }
    )


def evaluate_baselines(
    predictions: pd.DataFrame,
    run_id: str,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    bootstrap: bool = True,
) -> dict:
    actual = predictions["actual_close"].to_numpy(dtype=float)
    baselines: dict[str, dict] = {}
    for name, column in BASELINE_COLUMNS.items():
        predicted = predictions[column].to_numpy(dtype=float)
        metrics = compute_metrics(actual, predicted)
        entry = {
            "description": BASELINE_DESCRIPTIONS[name],
            "prediction_column": column,
            "metrics": rounded_metrics(metrics),
        }
        if bootstrap:
            entry["confidence_intervals"] = bootstrap_metric_ci(
                actual,
                predicted,
                n_resamples=config.BOOTSTRAP_RESAMPLES,
                confidence=config.CONFIDENCE_LEVEL,
                block_size=config.BOOTSTRAP_BLOCK_SIZE,
                seed=42,
            )
        baselines[name] = entry

    ranking = sorted(
        baselines,
        key=lambda name: baselines[name]["metrics"]["MAE"],
    )
    return {
        "run_id": run_id,
        "generated_at": run_utils.utc_now(),
        "protocol": {
            "causal": True,
            "seasonal_period_days": 7,
            "drift_estimated_on": "in_sample_only",
            "test_period": [
                str(pd.to_datetime(test_df["date"]).iloc[0])[:10],
                str(pd.to_datetime(test_df["date"]).iloc[-1])[:10],
            ],
            "n_train": int(len(train_df)),
            "n_test": int(len(test_df)),
        },
        "baselines": baselines,
        "ranking_by_mae": ranking,
        "best_baseline": ranking[0],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hitung baseline naif pada holdout")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument(
        "--no-bootstrap",
        action="store_true",
        help="Lewati bootstrap CI (lebih cepat, untuk smoke test)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="baseline")

    if paths.legacy:
        print("[WARNING] Mode legacy: artefak baseline lama dapat tertimpa.")

    processed_dir, data_source = resolve_processed_dir(
        Path(args.processed_dir) if args.processed_dir else paths.processed_dir,
        config.PROCESSED_DIR,
    )
    train_df, test_df, _ = load_processed_data(processed_dir)

    print("=" * 70)
    print("BASELINE NAIF: PERSISTENCE, DRIFT, SEASONAL NAIVE, MOVING AVERAGE")
    print("=" * 70)
    print(f"[data] {processed_dir} (source={data_source})")

    predictions = build_baseline_predictions(train_df, test_df)
    if len(predictions) != config.EXPECTED_TEST_ROWS:
        raise ValueError(
            f"Baseline menghasilkan {len(predictions)} prediksi, "
            f"diharapkan {config.EXPECTED_TEST_ROWS}"
        )
    if pd.to_datetime(predictions["date"]).iloc[0].strftime("%Y-%m-%d") != config.TEST_START_DATE:
        raise ValueError("Baseline tidak dimulai pada tanggal holdout yang benar")
    if pd.to_datetime(predictions["date"]).iloc[-1].strftime("%Y-%m-%d") != config.TEST_END_DATE:
        raise ValueError("Baseline tidak berakhir pada tanggal holdout yang benar")

    payload = evaluate_baselines(
        predictions,
        run_id=paths.run_id,
        train_df=train_df,
        test_df=test_df,
        bootstrap=not args.no_bootstrap,
    )

    print("\n[1/2] Metrik baseline pada holdout 439 hari:")
    for name in payload["ranking_by_mae"]:
        entry = payload["baselines"][name]
        metrics = entry["metrics"]
        print(
            f"      {name:<20} RMSE {metrics['RMSE']:>10,.2f} | "
            f"MAE {metrics['MAE']:>10,.2f} | MAPE {metrics['MAPE']:>6.2f}%"
        )
    print(f"\n      Baseline terbaik (MAE): {payload['best_baseline']}")

    metrics_dir = config.LEGACY_METRICS_DIR if paths.legacy else paths.metrics_dir
    predictions_dir = config.RESULTS_ROOT if paths.legacy else paths.predictions_dir
    metrics_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = metrics_dir / "metrics_baselines.json"
    predictions_path = predictions_dir / "predictions_baselines.csv"
    run_utils.write_json(metrics_path, payload)
    predictions.to_csv(predictions_path, index=False)

    print("\n[2/2] Artefak baseline:")
    print(f"      Metrik    -> {metrics_path.resolve()}")
    print(f"      Prediksi  -> {predictions_path.resolve()}")
    print("=" * 70)

    if not paths.legacy:
        stage_config = {
            "stage": "baseline",
            "seed": args.seed,
            "data_source": data_source,
            "processed_dir": str(processed_dir.resolve()),
            "baselines": list(BASELINE_COLUMNS),
            "seasonal_period_days": 7,
            "bootstrap": not args.no_bootstrap,
            "train_period": [
                str(pd.to_datetime(train_df["date"]).iloc[0])[:10],
                str(pd.to_datetime(train_df["date"]).iloc[-1])[:10],
            ],
            "test_period": payload["protocol"]["test_period"],
        }
        input_paths = [
            processed_dir / "train_insample.csv",
            processed_dir / "test_outofsample.csv",
        ]
        run_utils.bootstrap_run(paths, "baseline", stage_config, inputs=input_paths)
        run_utils.record_stage(
            paths,
            "baseline",
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=input_paths,
            outputs=[metrics_path, predictions_path],
            extra={
                "metrics": {
                    name: entry["metrics"]
                    for name, entry in payload["baselines"].items()
                },
                "best_baseline": payload["best_baseline"],
            },
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
