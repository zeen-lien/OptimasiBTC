"""
07_run_ablation.py - Controlled loss/scheduler ablation at fixed Tier 3 params.

The thesis comparison Tier 1 vs Tier 3 mixes three factors: hyperparameter
values, loss function, and learning-rate scheduler. This script holds the
hyperparameters fixed at ``config.TIER3_CONFIG`` (the frozen Optuna best trial)
and varies only:

- loss: ``mse`` or ``mae``
- scheduler: ``none`` or ``plateau`` (ReduceLROnPlateau)

It is used by ``experiment_matrix.py`` for E3-E6. Holdout evaluation is
identical to the other tiers: final scaler fit on 1.753 in-sample rows, 439
holdout rows scored once, optional multi-seed repetition.
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

LOSS_MAP = {
    "mse": "mean_squared_error",
    "mae": "mean_absolute_error",
}
SCHEDULER_CHOICES = ("none", "plateau")


def default_tag(loss: str, scheduler: str) -> str:
    return f"tier3params_{loss}_{scheduler}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    defaults = config.TIER3_CONFIG
    parser = argparse.ArgumentParser(description="Ablation loss/scheduler pada parameter Tier 3")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument("--tag", default=None, help="Nama artefak, mis. e3_mse_none")
    parser.add_argument("--loss", choices=sorted(LOSS_MAP), default="mse")
    parser.add_argument("--scheduler", choices=SCHEDULER_CHOICES, default="none")
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
        default=12,
        help="Patience EarlyStopping (default 12, sama dengan retrain Tier 3)",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Daftar seed repetisi, mis. 42,123,2024 (seed utama selalu ikut)",
    )
    return parser.parse_args(argv)


def build_callbacks(scheduler: str, weights_path: Path, patience: int) -> list:
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=patience, restore_best_weights=True, verbose=0),
        ModelCheckpoint(str(weights_path), monitor="val_loss", save_best_only=True, verbose=0),
    ]
    if scheduler == "plateau":
        callbacks.insert(
            1,
            ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=4, min_lr=1e-5, verbose=0
            ),
        )
    return callbacks


def train_one_seed(
    seed: int,
    args: argparse.Namespace,
    train_scaled: np.ndarray,
    test_scaled: np.ndarray,
    scaler,
    weights_path: Path,
) -> dict:
    set_global_seed(seed)
    X_train, y_train = create_sequences(train_scaled, args.lookback)
    X_test, y_test = make_test_sequences(train_scaled, test_scaled, args.lookback)

    model = build_lstm_model(
        lookback=args.lookback,
        units=args.units,
        dropout=args.dropout,
        learning_rate=args.learning_rate,
        layers=args.layers,
        loss=LOSS_MAP[args.loss],
    )

    fit_start = time.time()
    history = model.fit(
        X_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=0.1,
        callbacks=build_callbacks(args.scheduler, weights_path, args.patience),
        verbose=1,
    )
    training_time = time.time() - fit_start

    y_pred_scaled = model.predict(X_test, verbose=0)
    y_test_usd = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    y_pred_usd = scaler.inverse_transform(y_pred_scaled).flatten()
    return {
        "seed": seed,
        "metrics": compute_metrics(y_test_usd, y_pred_usd),
        "y_test_usd": y_test_usd,
        "y_pred_usd": y_pred_usd,
        "training_time_seconds": training_time,
        "epochs_run": len(history.history["loss"]),
        "weights_path": weights_path,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    tag = args.tag or default_tag(args.loss, args.scheduler)
    stage_name = f"ablation_{tag}"
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage=stage_name)

    if paths.legacy:
        print("[WARNING] Mode legacy: artefak ablation dapat tertimpa.")

    processed_dir, data_source = resolve_processed_dir(
        Path(args.processed_dir) if args.processed_dir else paths.processed_dir,
        config.PROCESSED_DIR,
    )
    train_df, test_df, scaler = load_processed_data(processed_dir)
    train_scaled = transform_data(scaler, train_df)
    test_scaled = transform_data(scaler, test_df)

    seeds = parse_seeds(args.seeds, args.seed)

    print("=" * 70)
    print(f"ABLATION {tag}: loss={args.loss}, scheduler={args.scheduler}")
    print("=" * 70)
    print(f"[data] {processed_dir} (source={data_source})")
    print(f"[seed] utama={args.seed}, repetisi={seeds}")
    print(
        f"[params] L={args.lookback} U={args.units} Drop={args.dropout} "
        f"LR={args.learning_rate:.6g} B={args.batch_size} Ly={args.layers}"
    )

    model_dir = (
        config.MODELS_ROOT / "ablation" if paths.legacy else paths.models_dir / "ablation"
    )
    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir = config.LEGACY_METRICS_DIR if paths.legacy else paths.metrics_dir
    predictions_dir = config.RESULTS_ROOT if paths.legacy else paths.predictions_dir
    metrics_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)

    runs: dict[int, dict] = {}
    outputs: list[Path] = []
    for seed in seeds:
        weights_path = (
            model_dir / f"{tag}_best_weights.keras"
            if seed == args.seed
            else model_dir / f"{tag}_seed{seed}_best_weights.keras"
        )
        print(f"\nPelatihan seed {seed} (maks {args.epochs} epoch)...", flush=True)
        result = train_one_seed(
            seed, args, train_scaled, test_scaled, scaler, weights_path
        )
        runs[seed] = result

        prediction_name = (
            f"predictions_{tag}.csv"
            if seed == args.seed
            else f"predictions_{tag}_seed{seed}.csv"
        )
        predictions_path = predictions_dir / prediction_name
        prediction_column = f"predicted_close_{tag}"
        build_predictions_frame(
            test_df["date"], result["y_test_usd"], result["y_pred_usd"], prediction_column
        ).to_csv(predictions_path, index=False)
        outputs.extend([predictions_path, weights_path])

        print(f"      Selesai: {result['training_time_seconds']:.2f}s, "
              f"{result['epochs_run']} epoch")
        print("      Metrik: " + " | ".join(
            f"{key} {value:,.2f}{'%' if key == 'MAPE' else ''}"
            for key, value in result["metrics"].items()
        ))

    primary = runs[args.seed]
    per_seed = {
        str(seed): {
            **rounded_metrics(run["metrics"]),
            "epochs_run": int(run["epochs_run"]),
            "training_time_seconds": round(float(run["training_time_seconds"]), 2),
        }
        for seed, run in runs.items()
    }
    payload = {
        "experiment": {
            "tag": tag,
            "loss": LOSS_MAP[args.loss],
            "loss_short": args.loss,
            "scheduler": args.scheduler,
            "hpo": False,
            "parameters_source": "config.TIER3_CONFIG",
            "early_stopping": {"monitor": "val_loss", "patience": args.patience},
        },
        "tier": f"Ablation {tag}",
        "seed": args.seed,
        "seeds": seeds,
        "hyperparameters": {
            "lookback": args.lookback,
            "units": args.units,
            "dropout": args.dropout,
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "layers": args.layers,
            "epochs_max": args.epochs,
            "epochs_run": primary["epochs_run"],
            "validation_split": 0.1,
        },
        "training_time_seconds": round(primary["training_time_seconds"], 2),
        "data": {
            "processed_dir": str(processed_dir.resolve()),
            "source": data_source,
            "n_train": int(len(train_df)),
            "n_test": int(len(test_df)),
        },
        "metrics": rounded_metrics(primary["metrics"]),
        "multi_seed": {
            "seeds": seeds,
            "per_seed": per_seed,
            "aggregate": stats_utils.aggregate_seed_metrics(per_seed),
        },
    }
    if len(seeds) > 1:
        payload["experiment"]["seed_set"] = seeds

    metrics_path = metrics_dir / f"metrics_{tag}.json"
    run_utils.write_json(metrics_path, payload)
    outputs.append(metrics_path)

    seed_metrics_path = None
    if len(seeds) > 1:
        seed_metrics_path = predictions_dir / f"seed_metrics_{tag}.json"
        run_utils.write_json(
            seed_metrics_path,
            {
                "tier": f"Ablation {tag}",
                "primary_seed": args.seed,
                "seeds": seeds,
                "per_seed": per_seed,
                "aggregate": payload["multi_seed"]["aggregate"],
            },
        )
        outputs.append(seed_metrics_path)

    print(f"\n      Metrik -> {metrics_path.resolve()}")
    for seed, run in runs.items():
        print(f"      Seed {seed:<6} -> {run['weights_path'].resolve()}")
    print("=" * 70)

    if not paths.legacy:
        stage_config = {
            "stage": stage_name,
            "tag": tag,
            "seed": args.seed,
            "seeds": seeds,
            "loss": LOSS_MAP[args.loss],
            "scheduler": args.scheduler,
            "hpo": False,
            "parameters_source": "config.TIER3_CONFIG",
            "early_stopping": {"monitor": "val_loss", "patience": args.patience},
            "lookback": args.lookback,
            "units": args.units,
            "dropout": args.dropout,
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "layers": args.layers,
            "epochs_max": args.epochs,
            "validation_split": 0.1,
            "data_source": data_source,
            "processed_dir": str(processed_dir.resolve()),
        }
        input_paths = [
            processed_dir / "train_insample.csv",
            processed_dir / "test_outofsample.csv",
            processed_dir / "minmax_scaler.joblib",
        ]
        run_utils.bootstrap_run(paths, stage_name, stage_config, inputs=input_paths)
        run_utils.record_stage(
            paths,
            stage_name,
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=input_paths,
            outputs=outputs,
            extra={"metrics": rounded_metrics(primary["metrics"])},
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
