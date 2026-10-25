"""
05_optimize_optuna_tier3.py - Tier 3: Optuna-TPE hyperparameter optimization.

The search space is read from config.SEARCH_SPACE so the thesis tables, the
generators, and this script cannot silently drift apart.

CV protocol (Fase 2): expanding-window TimeSeriesSplit over raw in-sample
close prices, purge gap equal to the trial lookback, and a MinMaxScaler fit
per fold on the training window only. Validation predictions are scored in
USD (MAE). The 439-day holdout test is touched only by the final retrain.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import optuna
import pandas as pd

import config
import run_utils
import stats_utils
from data_utils import create_sequences, load_processed_data, transform_data
from cv_utils import build_fold_sequences, purged_time_folds, scaler_bounds
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

optuna.logging.set_verbosity(optuna.logging.WARNING)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Optimasi hyperparameter Tier 3")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument("--trials", type=int, default=config.DEFAULT_OPTUNA_TRIALS)
    parser.add_argument("--cv-splits", type=int, default=config.DEFAULT_CV_SPLITS)
    parser.add_argument("--screening-epochs", type=int, default=25)
    parser.add_argument("--epochs", type=int, default=config.DEFAULT_EPOCHS)
    parser.add_argument("--study-name", default=config.TIER3_STUDY_NAME)
    parser.add_argument("--retrain", action="store_true", help="Latih ulang best trial yang tersimpan")
    parser.add_argument("--resume", action="store_true", help="Lanjutkan study yang sudah ada")
    parser.add_argument("--overwrite", action="store_true", help="Backup lalu buat study baru")
    parser.add_argument(
        "--seeds",
        default=None,
        help="Daftar seed retrain final, mis. 42,123,2024 (seed utama selalu ikut)",
    )
    return parser.parse_args(argv)


def suggest_params(trial: optuna.Trial) -> dict:
    space = config.SEARCH_SPACE
    return {
        "lookback": trial.suggest_int("lookback", space["lookback"]["low"], space["lookback"]["high"]),
        "units": trial.suggest_int("units", space["units"]["low"], space["units"]["high"]),
        "dropout": trial.suggest_float(
            "dropout",
            space["dropout"]["low"],
            space["dropout"]["high"],
            step=space["dropout"]["step"],
        ),
        "learning_rate": trial.suggest_float(
            "learning_rate",
            space["learning_rate"]["low"],
            space["learning_rate"]["high"],
            log=space["learning_rate"]["log"],
        ),
        "batch_size": trial.suggest_categorical("batch_size", space["batch_size"]["choices"]),
        "layers": trial.suggest_int("layers", space["layers"]["low"], space["layers"]["high"]),
    }


def objective(
    trial: optuna.Trial,
    train_raw: np.ndarray,
    cv_splits: int,
    screening_epochs: int,
) -> float:
    """
    Purged, per-fold-scaled CV objective.

    The scaler for each fold is fit on that fold's training raw prices only.
    Validation predictions are inverse-transformed and scored in USD (MAE).
    """
    from tensorflow.keras.callbacks import EarlyStopping

    params = suggest_params(trial)
    lookback = int(params["lookback"])
    gap = lookback  # no shared raw observation between train and validation windows

    try:
        folds = list(purged_time_folds(len(train_raw), n_splits=cv_splits, gap=gap))
    except ValueError:
        return float("inf")

    fold_losses: list[float] = []
    fold_details: list[dict] = []

    for fold, train_idx, val_idx in folds:
        bundle = build_fold_sequences(train_raw, train_idx, val_idx, lookback, fold)
        if len(bundle.X_train) < 25 or len(bundle.X_val) < 1:
            return float("inf")

        model = build_lstm_model(
            lookback=lookback,
            units=params["units"],
            dropout=params["dropout"],
            learning_rate=params["learning_rate"],
            layers=params["layers"],
            loss="mean_absolute_error",
        )
        early_stop = EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True, verbose=0
        )
        history = model.fit(
            bundle.X_train,
            bundle.y_train,
            validation_data=(bundle.X_val, bundle.y_val),
            epochs=screening_epochs,
            batch_size=params["batch_size"],
            callbacks=[early_stop],
            verbose=0,
        )

        y_pred_scaled = model.predict(bundle.X_val, verbose=0)
        y_pred_usd = bundle.scaler.inverse_transform(y_pred_scaled).reshape(-1)
        fold_metric = compute_metrics(bundle.y_val_usd, y_pred_usd)
        val_mae_usd = float(fold_metric["MAE"])
        fold_losses.append(val_mae_usd)
        low, high = scaler_bounds(bundle.scaler)
        fold_details.append(
            {
                "fold": fold,
                "n_train_windows": int(len(bundle.X_train)),
                "n_val_windows": int(len(bundle.X_val)),
                "gap": gap,
                "scaler_min": low,
                "scaler_max": high,
                "val_mae_usd": val_mae_usd,
                "val_rmse_usd": float(fold_metric["RMSE"]),
            }
        )

        trial.report(val_mae_usd, step=fold)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    trial.set_user_attr("fold_metrics_usd", fold_details)
    trial.set_user_attr("cv_protocol", "per_fold_scaler_purged")
    trial.set_user_attr("cv_gap", gap)
    return float(np.mean(fold_losses))


def study_duration_seconds(study: optuna.Study) -> float:
    durations = []
    for trial in study.trials:
        if trial.datetime_start and trial.datetime_complete:
            durations.append((trial.datetime_complete - trial.datetime_start).total_seconds())
    return round(float(sum(durations)), 2)


def safe_best_value(study: optuna.Study) -> float | None:
    try:
        return float(study.best_value)
    except ValueError:
        return None


def create_or_load_study(
    db_path: Path,
    study_name: str,
    args: argparse.Namespace,
) -> tuple[optuna.Study, bool]:
    """Return (study, loaded_existing). Never silently destroys a study."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    storage = f"sqlite:///{db_path.as_posix()}"

    if args.retrain:
        if not db_path.exists():
            raise FileNotFoundError(
                f"Mode --retrain membutuhkan study yang ada: {db_path}. "
                "Gunakan --run-id run yang sudah berisi optuna_study.db."
            )
        return (
            optuna.load_study(study_name=study_name, storage=storage),
            True,
        )

    if db_path.exists():
        if args.resume:
            return (
                optuna.load_study(study_name=study_name, storage=storage),
                True,
            )
        if not args.overwrite:
            raise FileExistsError(
                f"Study sudah ada: {db_path}. Pilih --resume, --overwrite, "
                "atau gunakan --run-id baru. File lama tidak dihapus otomatis."
            )
        backup = db_path.with_name(
            f"{db_path.stem}_backup_{datetime.now():%Y%m%d_%H%M%S}{db_path.suffix}"
        )
        shutil.copy2(db_path, backup)
        db_path.unlink()
        print(f"      Study lama dibackup ke {backup}")

    study = optuna.create_study(
        study_name=study_name,
        storage=storage,
        load_if_exists=False,
        direction="minimize",
        sampler=optuna.samplers.TPESampler(seed=args.seed),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=3, n_warmup_steps=1),
    )
    return study, False


def train_final_one_seed(
    seed: int,
    args: argparse.Namespace,
    best_params: dict,
    train_scaled: np.ndarray,
    test_scaled: np.ndarray,
    scaler,
    weights_path: Path,
) -> dict:
    """Retrain the best configuration on all in-sample data for one seed."""
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

    lookback = int(best_params["lookback"])
    set_global_seed(seed)
    X_train_full, y_train_full = create_sequences(train_scaled, lookback)
    X_test_full, y_test_full = make_test_sequences(train_scaled, test_scaled, lookback)

    model = build_lstm_model(
        lookback=lookback,
        units=int(best_params["units"]),
        dropout=float(best_params["dropout"]),
        learning_rate=float(best_params["learning_rate"]),
        layers=int(best_params["layers"]),
        loss="mean_absolute_error",
    )

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=12, restore_best_weights=True, verbose=0),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-5, verbose=0),
        ModelCheckpoint(str(weights_path), monitor="val_loss", save_best_only=True, verbose=0),
    ]

    fit_start = time.time()
    history = model.fit(
        X_train_full,
        y_train_full,
        epochs=args.epochs,
        batch_size=int(best_params["batch_size"]),
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1,
    )
    final_training_time = time.time() - fit_start

    y_pred_scaled = model.predict(X_test_full, verbose=0)
    y_test_usd = scaler.inverse_transform(y_test_full.reshape(-1, 1)).flatten()
    y_pred_usd = scaler.inverse_transform(y_pred_scaled).flatten()
    return {
        "seed": seed,
        "metrics": compute_metrics(y_test_usd, y_pred_usd),
        "y_test_usd": y_test_usd,
        "y_pred_usd": y_pred_usd,
        "training_time_seconds": final_training_time,
        "epochs_run": len(history.history["loss"]),
        "weights_path": weights_path,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="tier3")

    if paths.legacy:
        print("[WARNING] Mode legacy: study/metrik/prediksi/model Tier 3 lama dapat tertimpa.")

    processed_dir, data_source = resolve_processed_dir(
        Path(args.processed_dir) if args.processed_dir else paths.processed_dir,
        config.PROCESSED_DIR,
    )
    train_df, test_df, scaler = load_processed_data(processed_dir)
    train_scaled = transform_data(scaler, train_df)
    test_scaled = transform_data(scaler, test_df)

    print("=" * 70)
    print("EKSPERIMEN TIER 3: OPTIMASI HYPERPARAMETER LSTM MENGGUNAKAN OPTUNA-TPE")
    print("=" * 70)
    print(f"[data] {processed_dir} (source={data_source})")
    set_global_seed(args.seed)

    db_path = config.LEGACY_STUDY_DB if paths.legacy else paths.run_dir / "optuna_study.db"
    trials_csv_path = (
        config.LEGACY_TRIALS_CSV if paths.legacy else paths.run_dir / "optuna_trials_history.csv"
    )

    study, loaded_existing = create_or_load_study(db_path, args.study_name, args)

    if not args.retrain:
        optimize_start = time.time()
        print(f"\n[1/4] Optimasi TPE: {args.trials} trial baru, CV {args.cv_splits} fold, "
              f"screening {args.screening_epochs} epoch", flush=True)

        def print_callback(study: optuna.Study, trial: optuna.Trial) -> None:
            status = "PRUNED" if trial.state == optuna.trial.TrialState.PRUNED else "COMPLETE"
            value = f"{trial.value:.6f}" if trial.value is not None else "N/A"
            current_best = safe_best_value(study)
            best = f"{current_best:.6f}" if current_best is not None else "N/A"
            params = trial.params
            print(
                f"  [Trial {trial.number:02d}] {status:<8} | Loss {value:<10} | "
                f"Best {best:<10} | L={params.get('lookback', 0)} "
                f"U={params.get('units', 0)} Ly={params.get('layers', 1)} "
                f"B={params.get('batch_size', 0)} LR={params.get('learning_rate', 0):.5f} "
                f"Drop={params.get('dropout', 0):.2f}",
                flush=True,
            )

        train_raw_close = train_df["close"].to_numpy(dtype=float)
        study.optimize(
            lambda trial: objective(
                trial, train_raw_close, args.cv_splits, args.screening_epochs
            ),
            n_trials=args.trials,
            callbacks=[print_callback],
        )
        optimization_time = time.time() - optimize_start
    else:
        optimization_time = study_duration_seconds(study)
        print(f"[1/4] Mode retrain: memuat study {db_path}")

    best_value = safe_best_value(study)
    if best_value is None:
        raise RuntimeError("Study tidak memiliki trial COMPLETE; tidak ada model yang bisa dilatih.")

    best = study.best_trial
    best_params = best.params
    print(f"\n      Total trial: {len(study.trials)} | best trial #{best.number} | "
          f"CV loss {best_value:.6f}")
    print("[2/4] Hyperparameter terbaik:")
    for key, value in best_params.items():
        print(f"      - {key:<14}: {value}")

    lookback = int(best_params["lookback"])
    units = int(best_params["units"])
    dropout = float(best_params["dropout"])
    learning_rate = float(best_params["learning_rate"])
    batch_size = int(best_params["batch_size"])
    layers = int(best_params["layers"])

    seeds = parse_seeds(args.seeds, args.seed)
    print(f"\n[3/4] Retrain model final pada seluruh in-sample "
          f"(maks {args.epochs} epoch, MAE loss, ReduceLROnPlateau; seed {seeds})...",
          flush=True)

    model_dir = (
        config.MODELS_ROOT / "tier3_optuna"
        if paths.legacy
        else paths.models_dir / "tier3_optuna"
    )
    model_dir.mkdir(parents=True, exist_ok=True)

    metrics_dir = config.LEGACY_METRICS_DIR if paths.legacy else paths.metrics_dir
    predictions_dir = config.RESULTS_ROOT if paths.legacy else paths.predictions_dir
    metrics_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)

    runs: dict[int, dict] = {}
    output_paths: list[Path] = []
    for seed in seeds:
        weights_path = (
            model_dir / "tier3_best_weights.keras"
            if seed == args.seed
            else model_dir / f"tier3_seed{seed}_best_weights.keras"
        )
        print(f"\n      Seed {seed} (maks {args.epochs} epoch)...", flush=True)
        result = train_final_one_seed(
            seed, args, best_params, train_scaled, test_scaled, scaler, weights_path
        )
        runs[seed] = result

        prediction_name = (
            "predictions_tier3.csv" if seed == args.seed else f"predictions_tier3_seed{seed}.csv"
        )
        predictions_path = predictions_dir / prediction_name
        predictions_df = build_predictions_frame(
            test_df["date"], result["y_test_usd"], result["y_pred_usd"], "predicted_close_tier3"
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
    final_training_time = primary["training_time_seconds"]
    final_epochs = primary["epochs_run"]

    metrics_payload = {
        "tier": "Tier 3 (LSTM Optuna-TPE)",
        "seed": args.seed,
        "loss": "mean_absolute_error",
        "optimizer": "adam",
        "scheduler": "reduce_lr_on_plateau",
        "early_stopping": {"monitor": "val_loss", "patience": 12},
        "hyperparameters": {
            "lookback": lookback,
            "units": units,
            "dropout": dropout,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "layers": layers,
            "epochs_max": args.epochs,
            "epochs_run": final_epochs,
        },
        "optimization_time_seconds": round(optimization_time, 2),
        "final_training_time_seconds": round(final_training_time, 2),
        "total_trials": len(study.trials),
        "complete_trials": sum(
            1 for trial in study.trials if trial.state == optuna.trial.TrialState.COMPLETE
        ),
        "pruned_trials": sum(
            1 for trial in study.trials if trial.state == optuna.trial.TrialState.PRUNED
        ),
        "best_trial_number": best.number,
        "best_cv_loss": round(float(best_value), 6),
        "sampler": "TPESampler",
        "sampler_seed": args.seed,
        "pruner": "MedianPruner(n_startup_trials=3, n_warmup_steps=1)",
        "cv_protocol": (
            f"purged TimeSeriesSplit(n_splits={args.cv_splits}, gap=lookback) on raw "
            "in-sample close; MinMaxScaler fit per fold on training window only; "
            "validation scored in USD (MAE)"
        ),
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

    metrics_path = metrics_dir / "metrics_tier3.json"
    run_utils.write_json(metrics_path, metrics_payload)
    output_paths.append(metrics_path)

    seed_metrics_path = None
    if len(seeds) > 1:
        seed_metrics_path = predictions_dir / "seed_metrics_tier3.json"
        run_utils.write_json(
            seed_metrics_path,
            {
                "tier": "Tier 3 (LSTM Optuna-TPE)",
                "primary_seed": args.seed,
                "seeds": seeds,
                "per_seed": per_seed,
                "aggregate": stats_utils.aggregate_seed_metrics(per_seed),
            },
        )
        output_paths.append(seed_metrics_path)

    trials_df = study.trials_dataframe()
    trials_df.to_csv(trials_csv_path, index=False)

    print(f"\n      Metrik    -> {metrics_path.resolve()}")
    if seed_metrics_path:
        print(f"      Multi-seed-> {seed_metrics_path.resolve()}")
    print(f"      Trial CSV -> {trials_csv_path.resolve()}")
    for seed, run in runs.items():
        print(f"      Seed {seed:<6} -> {run['weights_path'].resolve()}")
    print("=" * 70, flush=True)

    if not paths.legacy:
        stage_config = {
            "stage": "tier3",
            "model": "LSTM Optuna-TPE",
            "seed": args.seed,
            "seeds": seeds,
            "study_name": args.study_name,
            "study_db": str(db_path.resolve()),
            "loaded_existing_study": loaded_existing,
            "trials_requested": args.trials,
            "total_trials": len(study.trials),
            "best_trial_number": best.number,
            "best_cv_loss": round(float(best_value), 6),
            "best_params": best_params,
            "search_space": config.SEARCH_SPACE,
            "cv_splits": args.cv_splits,
            "screening_epochs": args.screening_epochs,
            "cv_protocol": metrics_payload["cv_protocol"],
            "loss": "mean_absolute_error",
            "optimizer": "adam",
            "scheduler": "reduce_lr_on_plateau",
            "epochs_max": args.epochs,
            "epochs_run": final_epochs,
            "validation_split": 0.1,
            "early_stopping": {"monitor": "val_loss", "patience": 12},
            "data_source": data_source,
            "processed_dir": str(processed_dir.resolve()),
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
        run_utils.bootstrap_run(paths, "tier3", stage_config, inputs=input_paths)
        run_utils.record_stage(
            paths,
            "tier3",
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=input_paths,
            outputs=[*output_paths, trials_csv_path, db_path],
            extra={
                "metrics": rounded_metrics(metrics),
                "multi_seed": metrics_payload["multi_seed"] if len(seeds) > 1 else None,
            },
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
