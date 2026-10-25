"""
experiment_matrix.py - Controlled experiment matrix E0-E7.

The thesis comparison Tier 1 vs Tier 3 confounds three factors:

1. hyperparameter values (Optuna vs defaults),
2. loss function (MAE vs MSE),
3. learning-rate scheduler (ReduceLROnPlateau vs none).

This module defines the controlled matrix that separates them. E3-E6 hold the
frozen Tier 3 hyperparameters (``config.TIER3_CONFIG``) constant and vary only
loss and scheduler in a 2x2 factorial design:

    E3: MSE, no scheduler      (reference for E1/E4/E5)
    E4: MAE, no scheduler      (loss effect)
    E5: MSE, ReduceLROnPlateau (scheduler effect)
    E6: MAE, ReduceLROnPlateau (joint effect)

E1 (Tier 1 defaults) vs E3 isolates the tuned hyperparameters because both use
MSE and no scheduler. E7 is full HPO, so it is the proposed model, not an
ablation. E0 is the naive persistence benchmark.

Usage:
    python 05_Source_Code/model_experiment/experiment_matrix.py --list
    python 05_Source_Code/model_experiment/experiment_matrix.py --dry-run
    python 05_Source_Code/model_experiment/experiment_matrix.py \
        --run-id matrix_2026_10_25 --seeds 42,123,2024,7,99

Every experiment runs in the same isolated ``results/runs/{run_id}/`` directory
so metrics, predictions, figures, and provenance can be compared directly.
``--only E3,E4`` runs a subset. Legacy mode is rejected: the matrix must never
overwrite the frozen pre-repair artifacts.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

import config
import run_utils

SCRIPT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Experiment:
    key: str
    label: str
    script: str
    role: str
    hypothesis: str
    loss: str | None = None
    scheduler: str | None = None
    hpo: bool = False
    tag: str | None = None


EXPERIMENTS: tuple[Experiment, ...] = (
    Experiment(
        key="E0",
        label="Persistence baseline",
        script="baselines.py",
        role="baseline",
        hypothesis=(
            "One-step-ahead daily BTC prices are close to a random walk; an LSTM "
            "must beat persistence before any improvement is claimed."
        ),
    ),
    Experiment(
        key="E1",
        label="Tier 1 default LSTM",
        script="03_train_baseline_tier1.py",
        role="control",
        loss="mse",
        scheduler="none",
        hypothesis=(
            "Default lookback/units/dropout with MSE and no scheduler gives the "
            "control error level for the matrix."
        ),
    ),
    Experiment(
        key="E2",
        label="Tier 2 manual tuning",
        script="04_train_manual_tier2.py",
        role="literature_reference",
        loss="mse",
        scheduler="none",
        hypothesis=(
            "Manual replication of Khumaidi et al. (2024) is a literature "
            "reference, not evidence for or against Optuna."
        ),
    ),
    Experiment(
        key="E3",
        label="Tier 3 params, MSE, no scheduler",
        script="07_run_ablation.py",
        role="ablation_reference",
        loss="mse",
        scheduler="none",
        tag="e3_mse_none",
        hypothesis=(
            "E1 vs E3 isolates the effect of Optuna hyperparameters because "
            "loss (MSE) and scheduler (none) are identical."
        ),
    ),
    Experiment(
        key="E4",
        label="Tier 3 params, MAE, no scheduler",
        script="07_run_ablation.py",
        role="ablation_loss",
        loss="mae",
        scheduler="none",
        tag="e4_mae_none",
        hypothesis=(
            "E4 vs E3 isolates the loss function: MAE optimizes the conditional "
            "median and may reduce absolute error without any scheduler effect."
        ),
    ),
    Experiment(
        key="E5",
        label="Tier 3 params, MSE, ReduceLROnPlateau",
        script="07_run_ablation.py",
        role="ablation_scheduler",
        loss="mse",
        scheduler="plateau",
        tag="e5_mse_plateau",
        hypothesis=(
            "E5 vs E3 isolates the scheduler: ReduceLROnPlateau may improve "
            "convergence while the loss stays MSE."
        ),
    ),
    Experiment(
        key="E6",
        label="Tier 3 params, MAE, ReduceLROnPlateau",
        script="07_run_ablation.py",
        role="ablation_joint",
        loss="mae",
        scheduler="plateau",
        tag="e6_mae_plateau",
        hypothesis=(
            "E6 vs E3 is the joint loss+scheduler effect; comparing it with E4 "
            "and E5 shows whether the two factors interact."
        ),
    ),
    Experiment(
        key="E7",
        label="Tier 3 full Optuna HPO",
        script="05_optimize_optuna_tier3.py",
        role="proposed_model",
        loss="mae",
        scheduler="plateau",
        hpo=True,
        hypothesis=(
            "E7 vs E6 isolates the value of HPO itself when loss and scheduler "
            "are held identical. E7 is the proposed model; E3-E6 are ablations."
        ),
    ),
)

EXPERIMENTS_BY_KEY = {experiment.key: experiment for experiment in EXPERIMENTS}
EXPERIMENT_KEYS = tuple(EXPERIMENTS_BY_KEY)

# Artifact names written by each script. E0 has a nested baselines payload.
METRICS_FILES = {
    "E0": "metrics/metrics_baselines.json",
    "E1": "metrics/metrics_tier1.json",
    "E2": "metrics/metrics_tier2.json",
    "E3": "metrics/metrics_e3_mse_none.json",
    "E4": "metrics/metrics_e4_mae_none.json",
    "E5": "metrics/metrics_e5_mse_plateau.json",
    "E6": "metrics/metrics_e6_mae_plateau.json",
    "E7": "metrics/metrics_tier3.json",
}


def validate_matrix(experiments: Iterable[Experiment] = EXPERIMENTS) -> None:
    """Fail loudly if the factorial design is accidentally broken."""
    experiments = tuple(experiments)
    keys = [experiment.key for experiment in experiments]
    if len(keys) != len(set(keys)):
        raise ValueError("Kunci eksperimen duplikat")
    if set(keys) != set(EXPERIMENT_KEYS):
        raise ValueError(f"Matriks harus berisi tepat {EXPERIMENT_KEYS}, ditemukan {keys}")

    ablation = {
        experiment.key: experiment
        for experiment in experiments
        if experiment.key in {"E3", "E4", "E5", "E6"}
    }
    expected = {
        "E3": ("mse", "none"),
        "E4": ("mae", "none"),
        "E5": ("mse", "plateau"),
        "E6": ("mae", "plateau"),
    }
    for key, (loss, scheduler) in expected.items():
        experiment = ablation[key]
        if experiment.loss != loss or experiment.scheduler != scheduler:
            raise ValueError(
                f"{key} harus loss={loss}, scheduler={scheduler}; "
                f"ditemukan loss={experiment.loss}, scheduler={experiment.scheduler}"
            )
        if experiment.hpo:
            raise ValueError(f"{key} tidak boleh memakai HPO")
        if experiment.script != "07_run_ablation.py":
            raise ValueError(f"{key} harus memakai 07_run_ablation.py")

    e3 = ablation["E3"]
    for key in ("E4", "E5", "E6"):
        other = ablation[key]
        if other.tag == e3.tag:
            raise ValueError(f"{key} memakai tag yang sama dengan E3")
        if other.script != e3.script:
            raise ValueError(f"{key} harus memakai skrip yang sama dengan E3")

    if not EXPERIMENTS_BY_KEY["E7"].hpo:
        raise ValueError("E7 harus menjadi run HPO penuh")
    if EXPERIMENTS_BY_KEY["E7"].role != "proposed_model":
        raise ValueError("E7 adalah model usulan")


def parse_seed_list(value: str | None, primary: int = 42) -> tuple[int, ...]:
    """Parse a seed list and always include the primary seed first."""
    if primary < 0:
        raise ValueError(f"Seed utama tidak boleh negatif: {primary}")
    seeds: list[int] = [int(primary)]
    if value:
        for chunk in str(value).split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            seed = int(chunk)
            if seed < 0:
                raise ValueError(f"Seed tidak boleh negatif: {seed}")
            if seed not in seeds:
                seeds.append(seed)
    elif primary not in config.DEFAULT_SEEDS:
        seeds.extend(seed for seed in config.DEFAULT_SEEDS if seed != primary)
    else:
        seeds = [int(primary), *[seed for seed in config.DEFAULT_SEEDS if seed != primary]]
    if not seeds:
        raise ValueError("Seed set kosong")
    return tuple(seeds)


def parse_only(value: str | None) -> tuple[str, ...]:
    if not value:
        return EXPERIMENT_KEYS
    keys = tuple(part.strip().upper() for part in value.split(",") if part.strip())
    unknown = set(keys).difference(EXPERIMENT_KEYS)
    if unknown:
        raise ValueError(f"Eksperimen tidak dikenal: {sorted(unknown)}")
    return keys


def build_command(
    experiment: Experiment,
    *,
    run_id: str,
    root: Path,
    seed: int,
    seeds: tuple[int, ...],
    epochs: int,
    patience: int,
    trials: int,
    screening_epochs: int,
    cv_splits: int,
    processed_dir: str | None,
) -> list[str]:
    """Translate one matrix row into an explicit CLI command."""
    base = [
        sys.executable,
        str(SCRIPT_DIR / experiment.script),
        "--seed", str(seed),
        "--run-id", run_id,
        "--project-root", str(root),
    ]
    if processed_dir:
        base.extend(["--processed-dir", processed_dir])

    seed_args = ["--seeds", ",".join(str(seed) for seed in seeds)]
    common_training = ["--epochs", str(epochs), *seed_args, "--patience", str(patience)]

    if experiment.key == "E0":
        return base
    if experiment.key in {"E1", "E2"}:
        return [*base, *common_training]
    if experiment.key in {"E3", "E4", "E5", "E6"}:
        if not experiment.tag or not experiment.loss or not experiment.scheduler:
            raise ValueError(f"{experiment.key} tidak lengkap")
        return [
            *base,
            "--tag", experiment.tag,
            "--loss", experiment.loss,
            "--scheduler", experiment.scheduler,
            *common_training,
        ]
    if experiment.key == "E7":
        return [
            *base,
            "--trials", str(trials),
            "--epochs", str(epochs),
            "--screening-epochs", str(screening_epochs),
            "--cv-splits", str(cv_splits),
            *seed_args,
        ]
    raise ValueError(f"Tidak ada command builder untuk {experiment.key}")


def build_analysis_command(
    *,
    run_id: str,
    root: Path,
    seed: int,
    allow_partial: bool,
    publish: bool,
) -> list[str]:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "08_analyze_results.py"),
        "--seed", str(seed),
        "--run-id", run_id,
        "--project-root", str(root),
    ]
    if allow_partial:
        command.append("--allow-partial")
    if publish:
        command.append("--publish")
    return command


def matrix_plan(
    *,
    run_id: str,
    seed: int,
    seeds: tuple[int, ...],
    epochs: int,
    patience: int,
    trials: int,
    screening_epochs: int,
    cv_splits: int,
) -> dict:
    """Serializable description of the design, written before execution."""
    return {
        "schema_version": 1,
        "run_id": run_id,
        "design": "2x2 loss/scheduler factorial at fixed Tier 3 hyperparameters",
        "seed": seed,
        "seeds": list(seeds),
        "epochs_max": epochs,
        "early_stopping": {"monitor": "val_loss", "patience": patience},
        "hpo": {
            "trials": trials,
            "screening_epochs": screening_epochs,
            "cv_splits": cv_splits,
        },
        "experiments": [
            {
                **asdict(experiment),
                "role": experiment.role,
                "metrics_file": METRICS_FILES[experiment.key],
            }
            for experiment in EXPERIMENTS
        ],
        "comparisons": {
            "E1_vs_E3": "efek hyperparameter Optuna (MSE, tanpa scheduler)",
            "E4_vs_E3": "efek loss MAE (parameter tetap)",
            "E5_vs_E3": "efek ReduceLROnPlateau (parameter tetap, MSE)",
            "E6_vs_E3": "efek gabungan loss+scheduler",
            "E4_E5_interaction": "bandingkan E6 dengan E3+E4+E5",
            "E7_vs_E6": "efek HPO penuh (MAE, scheduler sama)",
            "E0_vs_semua": "apakah LSTM mengalahkan persistence",
        },
        "notes": [
            "E3-E6 memakai config.TIER3_CONFIG yang dibekukan; hanya loss/scheduler berubah.",
            "Semua run memakai split, max epoch, early stopping, dan seed set yang sama.",
            "E0 dievaluasi pada 439 hari holdout yang sama.",
            "E7 adalah model usulan; E3-E6 adalah ablation, bukan kandidat model.",
        ],
    }


def _metric_entry(key: str, payload: dict) -> tuple[dict[str, float], dict | None]:
    """Return (metrics, seed-aggregate) from either tier or baseline payload."""
    if key == "E0":
        baseline = payload["baselines"]["persistence"]
        return baseline["metrics"], None
    metrics = payload.get("metrics", {})
    aggregate = payload.get("multi_seed", {}).get("aggregate")
    return metrics, aggregate


def collect_results(
    paths: run_utils.RunPaths,
    seeds: tuple[int, ...],
    selected: tuple[str, ...] | None = None,
) -> list[dict]:
    """Read the artifact for each experiment that actually produced metrics."""
    baseline_metrics: dict[str, float] | None = None
    e3_metrics: dict[str, float] | None = None
    rows: list[dict] = []
    selected_set = set(selected) if selected is not None else set(EXPERIMENT_KEYS)

    for experiment in EXPERIMENTS:
        relative = METRICS_FILES[experiment.key]
        path = paths.run_dir / relative
        row: dict = {
            "run": experiment.key,
            "model": experiment.label,
            "role": experiment.role,
            "loss": experiment.loss or "-",
            "scheduler": experiment.scheduler or "-",
            "hpo": experiment.hpo,
            "status": "missing" if experiment.key in selected_set else "not_run",
            "metrics_file": relative,
        }
        if path.exists():
            payload = run_utils.read_json(path)
            metrics, aggregate = _metric_entry(experiment.key, payload)
            row.update(
                {
                    "status": "ok",
                    "rmse": metrics.get("RMSE"),
                    "mae": metrics.get("MAE"),
                    "mape": metrics.get("MAPE"),
                }
            )
            if aggregate:
                for metric in ("RMSE", "MAE", "MAPE"):
                    entry = aggregate.get(metric, {})
                    row[f"{metric.lower()}_mean"] = entry.get("mean")
                    row[f"{metric.lower()}_std"] = entry.get("std")
                    row[f"{metric.lower()}_n_seeds"] = entry.get("n_seeds")
            if experiment.key == "E0":
                baseline_metrics = metrics
            if experiment.key == "E3":
                e3_metrics = metrics
        row["n_seeds"] = len(seeds)
        rows.append(row)

    for row in rows:
        for reference_name, reference in (
            ("persistence", baseline_metrics),
            ("e3", e3_metrics),
        ):
            if reference and row.get("rmse") is not None:
                for metric in ("RMSE", "MAE", "MAPE"):
                    key = metric.lower()
                    value = row.get(key)
                    base = reference.get(metric)
                    if value is not None and base not in (None, 0):
                        row[f"{key}_vs_{reference_name}_percent"] = round(
                            (float(base) - float(value)) / float(base) * 100.0, 3
                        )
    return rows


def results_frame(rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def execute_command(command: list[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8", newline="\n") as log_handle:
        log_handle.write(f"$ {' '.join(command)}\n\n")
        log_handle.flush()
        process = subprocess.Popen(
            command,
            cwd=str(SCRIPT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            log_handle.write(line)
            log_handle.flush()
        return process.wait()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Matriks eksperimen terkontrol E0-E7")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--list", action="store_true", help="Tampilkan definisi matriks")
    parser.add_argument(
        "--only",
        default=None,
        help="Subset eksperimen, mis. E3,E4 (default: semua E0-E7)",
    )
    parser.add_argument("--epochs", type=int, default=config.DEFAULT_EPOCHS)
    parser.add_argument(
        "--patience",
        type=int,
        default=int(config.TIER3_CONFIG["early_stopping"]["patience"]),
        help="Patience EarlyStopping yang sama untuk semua run",
    )
    parser.add_argument("--trials", type=int, default=config.DEFAULT_OPTUNA_TRIALS)
    parser.add_argument("--screening-epochs", type=int, default=25)
    parser.add_argument("--cv-splits", type=int, default=config.DEFAULT_CV_SPLITS)
    parser.add_argument(
        "--seeds",
        default=None,
        help=(
            "Seed repetisi, mis. 42,123,2024,7,99 "
            f"(default: {','.join(map(str, config.DEFAULT_SEEDS))})"
        ),
    )
    parser.add_argument("--processed-dir", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Cetak perintah tanpa menjalankan")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Jalankan 08_analyze_results.py setelah matriks selesai",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Dengan --analyze, salin summary_final.json ke results/summary_final.json",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    validate_matrix()

    try:
        only = parse_only(args.only)
        seeds = parse_seed_list(args.seeds, args.seed)
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    selected = [EXPERIMENTS_BY_KEY[key] for key in only]

    if args.list:
        print(f"{'Run':<4} {'Role':<20} {'Loss':<5} {'Scheduler':<10} {'HPO':<5} Model")
        print("-" * 92)
        for experiment in EXPERIMENTS:
            print(
                f"{experiment.key:<4} {experiment.role:<20} "
                f"{experiment.loss or '-':<5} {experiment.scheduler or '-':<10} "
                f"{str(experiment.hpo):<5} {experiment.label}"
            )
        print("\nHipotesis:")
        for experiment in EXPERIMENTS:
            print(f"  {experiment.key}: {experiment.hypothesis}")
        return 0

    if args.legacy:
        print("[ERROR] Mode legacy ditolak: matriks harus menulis ke results/runs/{run_id}/.")
        return 2

    run_utils.apply_project_root(args.project_root)
    paths = run_utils.resolve_run_paths(
        run_id=args.run_id,
        root=config.PROJECT_ROOT,
        stage="matrix",
        seed=args.seed,
        legacy=False,
        create=not args.dry_run,
    )

    plan = matrix_plan(
        run_id=paths.run_id,
        seed=args.seed,
        seeds=seeds,
        epochs=args.epochs,
        patience=args.patience,
        trials=args.trials,
        screening_epochs=args.screening_epochs,
        cv_splits=args.cv_splits,
    )
    commands = [
        build_command(
            experiment,
            run_id=paths.run_id,
            root=paths.root,
            seed=args.seed,
            seeds=seeds,
            epochs=args.epochs,
            patience=args.patience,
            trials=args.trials,
            screening_epochs=args.screening_epochs,
            cv_splits=args.cv_splits,
            processed_dir=args.processed_dir,
        )
        for experiment in selected
    ]

    print("=" * 88)
    print("MATRIKS EKSPERIMEN TERKONTROL E0-E7")
    print(f"Run ID : {paths.run_id}")
    print(f"Output : {paths.run_dir}")
    print(f"Seeds  : {seeds}")
    print(f"Epochs : {args.epochs} | EarlyStopping patience: {args.patience}")
    print(f"Runs   : {', '.join(experiment.key for experiment in selected)}")
    print("=" * 88)
    for experiment in selected:
        print(f"  {experiment.key:<3} {experiment.label}")
        print(f"      {experiment.hypothesis}")

    if args.dry_run:
        print("\nPerintah:")
        for command in commands:
            print("  " + " ".join(command))
        if args.analyze:
            analysis_command = build_analysis_command(
                run_id=paths.run_id,
                root=paths.root,
                seed=args.seed,
                allow_partial=len(selected) < len(EXPERIMENTS),
                publish=args.publish and len(selected) == len(EXPERIMENTS),
            )
            print("  " + " ".join(analysis_command))
        return 0

    plan_path = run_utils.write_json(paths.run_dir / "experiment_matrix_plan.json", plan)
    processed_dir = Path(args.processed_dir) if args.processed_dir else config.PROCESSED_DIR
    input_paths = [
        processed_dir / "train_insample.csv",
        processed_dir / "test_outofsample.csv",
        processed_dir / "minmax_scaler.joblib",
    ]
    input_paths = [path for path in input_paths if path.exists()]
    run_utils.bootstrap_run(
        paths,
        "matrix",
        {
            "stage": "matrix",
            "plan_file": str(plan_path),
            **{key: plan[key] for key in ("seed", "seeds", "epochs_max", "early_stopping")},
        },
        inputs=input_paths,
    )

    started_at = run_utils.utc_now()
    statuses: dict[str, str] = {}
    failure: str | None = None
    for experiment, command in zip(selected, commands, strict=True):
        print(f"\n>>> {experiment.key}: {experiment.label} <<<")
        log_path = paths.logs_dir / f"matrix_{experiment.key}.log"
        started = time.time()
        return_code = execute_command(command, log_path)
        elapsed = time.time() - started
        statuses[experiment.key] = "success" if return_code == 0 else "failed"
        if return_code != 0:
            failure = (
                f"{experiment.key} gagal (exit {return_code}). Lihat log: "
                f"{log_path.resolve()}"
            )
            print(f"[FAILED] {failure}")
            break
        print(f"[OK] {experiment.key} ({elapsed:.1f}s) -> {log_path.resolve()}")

    rows = collect_results(paths, seeds, selected=only)
    frame = results_frame(rows)
    results_json_path = paths.run_dir / "experiment_matrix_results.json"
    results_csv_path = paths.run_dir / "experiment_matrix_results.csv"
    run_utils.write_json(
        results_json_path,
        {
            "run_id": paths.run_id,
            "generated_at": run_utils.utc_now(),
            "status": "failed" if failure else ("partial" if len(selected) < len(EXPERIMENTS) else "success"),
            "selected": list(only),
            "statuses": statuses,
            "seeds": list(seeds),
            "rows": rows,
            "note": (
                "Metrik pada tabel ini berasal dari seed utama (--seed). "
                "Agregat multi-seed ada di kolom *_mean/*_std dan file seed_metrics."
            ),
        },
    )
    if not frame.empty:
        frame.to_csv(results_csv_path, index=False)

    run_utils.record_stage(
        paths,
        "matrix",
        status="failed" if failure else "success",
        started_at=started_at,
        stage_config={
            "stage": "matrix",
            "selected": list(only),
            "seeds": list(seeds),
            "epochs": args.epochs,
            "patience": args.patience,
            "trials": args.trials,
            "screening_epochs": args.screening_epochs,
            "cv_splits": args.cv_splits,
        },
        inputs=input_paths,
        outputs=[plan_path, results_json_path, results_csv_path],
        extra={"statuses": statuses, "failure": failure},
    )

    if not frame.empty:
        print("\nRingkasan metrik (seed utama):")
        columns = [
            column
            for column in (
                "run", "status", "rmse", "mae", "mape",
                "rmse_vs_persistence_percent", "mae_vs_persistence_percent",
            )
            if column in frame.columns
        ]
        print(frame[columns].to_string(index=False))

    print("\n" + "=" * 88)
    print(f"MATRIKS SELESAI: {paths.run_dir}")
    print(f"Plan    -> {plan_path.resolve()}")
    print(f"Results -> {results_json_path.resolve()}")
    if not frame.empty:
        print(f"CSV     -> {results_csv_path.resolve()}")
    if failure:
        print(f"[FAILED] {failure}")
        return 1

    if args.analyze:
        analysis_command = build_analysis_command(
            run_id=paths.run_id,
            root=paths.root,
            seed=args.seed,
            allow_partial=len(selected) < len(EXPERIMENTS),
            publish=args.publish and len(selected) == len(EXPERIMENTS),
        )
        print("\n>>> ANALISIS FASE 4 <<<")
        analysis_log = paths.logs_dir / "matrix_analysis.log"
        return_code = execute_command(analysis_command, analysis_log)
        if return_code != 0:
            print(
                f"[FAILED] Analisis gagal (exit {return_code}). "
                f"Lihat log: {analysis_log.resolve()}"
            )
            return 1

    print("=" * 88)
    return 0


if __name__ == "__main__":
    sys.exit(main())
