"""
04_train_manual_tier2.py - Tier 2: manual-tuning replication.

Legacy configuration from Khumaidi et al. (2024): lookback 60, 128 units,
dropout 0.2, Adam 1e-3, batch 10, MSE. Overrides are exposed for controlled
experiments and all values are recorded in the run manifest.

``--seeds`` repeats final training with several initializations; the primary
seed still produces ``metrics_tier2.json`` and ``predictions_tier2.csv``.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

import config
import run_utils
import stats_utils
from data_utils import create_sequences, load_processed_data, transform_data
from experiment_utils import (
    build_lstm_model,
    build_predictions_frame,
    compute_metrics,
    make_test_sequences,
    parse_seeds,
    resolve_processed_dir,
    rounded_metrics,
    set_global_seed,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    defaults = config.TIER2_CONFIG
    parser = argparse.ArgumentParser(description="Latih dan evaluasi Tier 2")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument("--lookback", type=int, default=defaults["lookback"])
    parser.add_argument("--units", type=int, default=defaults["units"])
    parser.add_argument("--dropout", type=float, default=defaults["dropout"])
    parser.add_argument("--learning-rate", type=float, default=defaults["learning_rate"])
    parser.add_argument("--batch-size", type=int, default=defaults["batch_size"])
    parser.add_argument("--layers", type=int, default=defaults["layers"])
    parser.add_argument("--epochs", type=int, default=defaults["epochs"])
    parser.add_argument(
        "--patience",
        type=int,
        default=10,
        help="Patience EarlyStopping (default 10; matriks memakai 12 agar setara)",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Daftar seed repetisi, mis. 42,123,2024 (seed utama selalu ikut)",
    )
    return parser.parse_args(argv)


def train_one_seed(
    seed: int,
    args: argparse.Namespace,
    train_scaled: np.ndarray,
    test_scaled: np.ndarray,
    test_df,
    scaler,
    weights_path: Path,
) -> dict:
    """Train one model with a fixed seed and score the shared holdout."""
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

    set_global_seed(seed)
    X_train, y_train = create_sequences(train_scaled, args.lookback)
    X_test, y_test = make_test_sequences(train_scaled, test_scaled, args.lookback)

    model = build_lstm_model(
        lookback=args.lookback,
        units=args.units,
        dropout=args.dropout,
        learning_rate=args.learning_rate,
        layers=args.layers,
        loss="mean_squared_error",
    )

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=args.patience, restore_best_weights=True, verbose=0),
        ModelCheckpoint(str(weights_path), monitor="val_loss", save_best_only=True, verbose=0),
    ]

    fit_start = time.time()
    history = model.fit(
        X_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1,
    )
    training_time = time.time() - fit_start
    actual_epochs = len(history.history["loss"])

    y_pred_scaled = model.predict(X_test, verbose=0)
    y_test_usd = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    y_pred_usd = scaler.inverse_transform(y_pred_scaled).flatten()
    metrics = compute_metrics(y_test_usd, y_pred_usd)

    return {
        "seed": seed,
        "model": model,
        "metrics": metrics,
        "y_test_usd": y_test_usd,
        "y_pred_usd": y_pred_usd,
        "training_time_seconds": training_time,
        "epochs_run": actual_epochs,
        "weights_path": weights_path,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="tier2")

    if paths.legacy:
        print("[WARNING] Mode legacy: metrik/prediksi/model Tier 2 lama dapat tertimpa.")

    processed_dir, data_source = resolve_processed_dir(
        Path(args.processed_dir) if args.processed_dir else paths.processed_dir,
        config.PROCESSED_DIR,
    )
    train_df, test_df, scaler = load_processed_data(processed_dir)
    train_scaled = transform_data(scaler, train_df)
    test_scaled = transform_data(scaler, test_df)

    print("=" * 70)
    print("EKSPERIMEN TIER 2: LSTM MANUAL TUNING (REPLIKASI KHUMAIDI DKK., 2024)")
    print("=" * 70)
    print(f"[data] {processed_dir} (source={data_source})")

    seeds = parse_seeds(args.seeds, args.seed)
    print(f"[seed] utama={args.seed}, repetisi={seeds}")

    X_preview, _ = create_sequences(train_scaled, args.lookback)
    X_test_preview, _ = make_test_sequences(train_scaled, test_scaled, args.lookback)
    print(f"[1/5] Sekuen (lookback={args.lookback}):")
    print(f"      X_train {X_preview.shape}, X_test {X_test_preview.shape}")

    model_dir = config.MODELS_ROOT / "tier2_manual" if paths.legacy else paths.models_dir / "tier2_manual"
    model_dir.mkdir(parents=True, exist_ok=True)

    metrics_dir = config.LEGACY_METRICS_DIR if paths.legacy else paths.metrics_dir
    predictions_dir = config.RESULTS_ROOT if paths.legacy else paths.predictions_dir
    metrics_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)

    runs: dict[int, dict] = {}
    output_paths: list[Path] = []
    for seed in seeds:
        weights_path = (
            model_dir / "tier2_best_weights.keras"
            if seed == args.seed
            else model_dir / f"tier2_seed{seed}_best_weights.keras"
        )
        print(f"\n[2/5] Pelatihan seed {seed} "
              f"(maks {args.epochs} epoch, validation_split=0.1)...")
        result = train_one_seed(
            seed, args, train_scaled, test_scaled, test_df, scaler, weights_path
        )
        runs[seed] = result

        prediction_name = (
            "predictions_tier2.csv" if seed == args.seed else f"predictions_tier2_seed{seed}.csv"
        )
        predictions_path = predictions_dir / prediction_name
        predictions_df = build_predictions_frame(
            test_df["date"], result["y_test_usd"], result["y_pred_usd"], "predicted_close_tier2"
        )
        predictions_df.to_csv(predictions_path, index=False)
        output_paths.extend([predictions_path, weights_path])

        print(f"      Selesai: {result['training_time_seconds']:.2f}s, "
              f"{result['epochs_run']} epoch")
        print("      Metrik: " + " | ".join(
            f"{key} {value:,.2f}{'%' if key == 'MAPE' else ''}"
            for key, value in result["metrics"].items()
        ))

    primary = runs[args.seed]
    metrics = primary["metrics"]
    metrics_payload = {
        "tier": "Tier 2 (LSTM Manual Tuning Khumaidi dkk.)",
        "seed": args.seed,
        "loss": "mean_squared_error",
        "optimizer": "adam",
        "scheduler": None,
        "early_stopping": {"monitor": "val_loss", "patience": args.patience},
        "hyperparameters": {
            "lookback": args.lookback,
            "units": args.units,
            "dropout": args.dropout,
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "layers": args.layers,
            "epochs_max": args.epochs,
            "epochs_run": primary["epochs_run"],
        },
        "training_time_seconds": round(primary["training_time_seconds"], 2),
        "data": {
            "processed_dir": str(processed_dir.resolve()),
            "source": data_source,
            "n_train": int(len(train_df)),
            "n_test": int(len(test_df)),
        },
        "metrics": rounded_metrics(metrics),
    }

    per_seed = {
        str(seed): {
            **rounded_metrics(run["metrics"]),
            "epochs_run": int(run["epochs_run"]),
            "training_time_seconds": round(float(run["training_time_seconds"]), 2),
        }
        for seed, run in runs.items()
    }
    metrics_payload["multi_seed"] = {
        "seeds": seeds,
        "per_seed": per_seed,
        "aggregate": stats_utils.aggregate_seed_metrics(per_seed),
    }

    metrics_path = metrics_dir / "metrics_tier2.json"
    run_utils.write_json(metrics_path, metrics_payload)
    output_paths.append(metrics_path)

    seed_metrics_path = None
    if len(seeds) > 1:
        seed_metrics_path = predictions_dir / "seed_metrics_tier2.json"
        run_utils.write_json(
            seed_metrics_path,
            {
                "tier": "Tier 2 (LSTM Manual Tuning Khumaidi dkk.)",
                "primary_seed": args.seed,
                "seeds": seeds,
                "per_seed": per_seed,
                "aggregate": stats_utils.aggregate_seed_metrics(per_seed),
            },
        )
        output_paths.append(seed_metrics_path)

    print("\n[5/5] Artefak Tier 2:")
    print(f"      Metrik    -> {metrics_path.resolve()}")
    if seed_metrics_path:
        print(f"      Multi-seed-> {seed_metrics_path.resolve()}")
    for seed, run in runs.items():
        print(f"      Seed {seed:<6} -> {run['weights_path'].resolve()}")
    print("=" * 70)

    if not paths.legacy:
        stage_config = {
            "stage": "tier2",
            "model": "LSTM manual tuning",
            "seed": args.seed,
            "seeds": seeds,
            "data_source": data_source,
            "processed_dir": str(processed_dir.resolve()),
            "lookback": args.lookback,
            "units": args.units,
            "dropout": args.dropout,
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "layers": args.layers,
            "loss": "mean_squared_error",
            "optimizer": "adam",
            "scheduler": None,
            "epochs_max": args.epochs,
            "epochs_run": primary["epochs_run"],
            "validation_split": 0.1,
            "early_stopping": {"monitor": "val_loss", "patience": args.patience},
            "train_period": [
                str(train_df["date"].iloc[0])[:10],
                str(train_df["date"].iloc[-1])[:10],
            ],
            "test_period": [
                str(test_df["date"].iloc[0])[:10],
                str(test_df["date"].iloc[-1])[:10],
            ],
        }
        input_paths = [
            processed_dir / "train_insample.csv",
            processed_dir / "test_outofsample.csv",
            processed_dir / "minmax_scaler.joblib",
        ]
        run_utils.bootstrap_run(paths, "tier2", stage_config, inputs=input_paths)
        run_utils.record_stage(
            paths,
            "tier2",
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=input_paths,
            outputs=output_paths,
            extra={
                "metrics": rounded_metrics(metrics),
                "multi_seed": metrics_payload["multi_seed"] if len(seeds) > 1 else None,
            },
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
