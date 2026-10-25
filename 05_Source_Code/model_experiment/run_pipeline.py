"""
run_pipeline.py - Master orchestration for the Bitcoin LSTM experiment.

Examples:
    python 05_Source_Code/model_experiment/run_pipeline.py --all --trials 50
    python 05_Source_Code/model_experiment/run_pipeline.py --all --run-id 2026-10-25_tier3_seed42
    python 05_Source_Code/model_experiment/run_pipeline.py --stage data --reuse-data
    python 05_Source_Code/model_experiment/run_pipeline.py --all --dry-run
    python 05_Source_Code/model_experiment/experiment_matrix.py --run-id matrix_final

Every stage receives the same run id, so metrics, figures, model weights, and
provenance land in one isolated directory under results/runs/{run_id}/.
The full controlled matrix E0-E7 is orchestrated by experiment_matrix.py, not
by --all, because E7 performs a complete Optuna study.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import config
import run_utils

SCRIPT_DIR = Path(__file__).resolve().parent


class PipelineError(RuntimeError):
    pass


STAGE_SCRIPTS = {
    "data": ["01_fetch_binance_data.py", "02_preprocessing.py"],
    "baseline": ["baselines.py"],
    "tier1": ["03_train_baseline_tier1.py"],
    "tier2": ["04_train_manual_tier2.py"],
    "tier3": ["05_optimize_optuna_tier3.py"],
    "eval": ["06_evaluate_and_compare.py"],
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Master pipeline skripsi Bitcoin LSTM Optuna")
    parser.add_argument("--all", action="store_true", help="Jalankan seluruh pipeline")
    parser.add_argument(
        "--stage",
        choices=list(STAGE_SCRIPTS),
        help="Jalankan satu stage tertentu",
    )
    run_utils.add_run_arguments(parser)
    parser.add_argument("--trials", type=int, default=config.DEFAULT_OPTUNA_TRIALS)
    parser.add_argument("--epochs", type=int, default=config.DEFAULT_EPOCHS)
    parser.add_argument("--screening-epochs", type=int, default=25)
    parser.add_argument("--cv-splits", type=int, default=config.DEFAULT_CV_SPLITS)
    parser.add_argument(
        "--seeds",
        default=None,
        help="Seed repetisi untuk Tier 1/2/3, mis. 42,123,2024",
    )
    parser.add_argument(
        "--reuse-data",
        action="store_true",
        help="Salin data mentah yang sudah ada (offline) alih-alih mengunduh ulang",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Teruskan study Optuna yang sudah ada di run ini",
    )
    parser.add_argument("--dry-run", action="store_true", help="Cetak perintah tanpa menjalankannya")
    return parser.parse_args(argv)


def common_args(args: argparse.Namespace, paths: run_utils.RunPaths) -> list[str]:
    result = [
        "--seed", str(args.seed),
        "--project-root", str(paths.root),
    ]
    if args.legacy:
        result.append("--legacy")
    else:
        result.extend(["--run-id", paths.run_id])
    return result


def stage_commands(
    stage: str,
    args: argparse.Namespace,
    paths: run_utils.RunPaths,
) -> list[list[str]]:
    base = common_args(args, paths)
    commands: list[list[str]] = []

    if stage == "data":
        fetch = [sys.executable, str(SCRIPT_DIR / "01_fetch_binance_data.py"), *base]
        if args.reuse_data:
            fetch.append("--reuse-local")
        commands.append(fetch)
        commands.append([sys.executable, str(SCRIPT_DIR / "02_preprocessing.py"), *base])
    elif stage == "baseline":
        commands.append([sys.executable, str(SCRIPT_DIR / "baselines.py"), *base])
    elif stage == "tier1":
        commands.append([
            sys.executable,
            str(SCRIPT_DIR / "03_train_baseline_tier1.py"),
            *base,
            "--epochs", str(args.epochs),
            *(["--seeds", args.seeds] if args.seeds else []),
        ])
    elif stage == "tier2":
        commands.append([
            sys.executable,
            str(SCRIPT_DIR / "04_train_manual_tier2.py"),
            *base,
            "--epochs", str(args.epochs),
            *(["--seeds", args.seeds] if args.seeds else []),
        ])
    elif stage == "tier3":
        tier3 = [
            sys.executable,
            str(SCRIPT_DIR / "05_optimize_optuna_tier3.py"),
            *base,
            "--trials", str(args.trials),
            "--epochs", str(args.epochs),
            "--screening-epochs", str(args.screening_epochs),
            "--cv-splits", str(args.cv_splits),
            *(["--seeds", args.seeds] if args.seeds else []),
        ]
        if args.resume:
            tier3.append("--resume")
        commands.append(tier3)
    elif stage == "eval":
        commands.append([sys.executable, str(SCRIPT_DIR / "06_evaluate_and_compare.py"), *base])
    else:
        raise ValueError(f"Stage tidak dikenal: {stage}")
    return commands


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


def run_stage(stage: str, args: argparse.Namespace, paths: run_utils.RunPaths) -> None:
    stage_started = run_utils.utc_now()
    commands = stage_commands(stage, args, paths)
    print(f"\n>>> STAGE {stage.upper()} ({paths.run_id}) <<<")

    if args.dry_run:
        for command in commands:
            print("    " + " ".join(command))
        return

    stage_run_started = time.time()
    for command in commands:
        script_name = Path(command[1]).stem
        log_path = paths.logs_dir / f"{script_name}.log"
        started = time.time()
        return_code = execute_command(command, log_path)
        elapsed = time.time() - started
        if return_code != 0:
            run_utils.record_stage(
                paths,
                stage,
                status="failed",
                started_at=stage_started,
                stage_config={"stage": stage, "commands": commands},
                extra={"return_code": return_code, "failed_script": script_name},
            )
            raise PipelineError(
                f"Stage '{stage}' gagal pada {script_name} (exit {return_code}). "
                f"Lihat log: {log_path.resolve()}"
            )
        print(f"    [OK] {script_name} ({elapsed:.1f}s) -> {log_path.resolve()}")

    run_utils.record_stage(
        paths,
        stage,
        status="success",
        started_at=stage_started,
        stage_config={"stage": stage, "commands": commands},
        extra={"elapsed_seconds": round(time.time() - stage_run_started, 3)},
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.all and not args.stage:
        print("Gunakan --all atau --stage {data,baseline,tier1,tier2,tier3,eval}.")
        return 2

    run_utils.apply_project_root(args.project_root)
    paths = run_utils.resolve_run_paths(
        run_id=args.run_id,
        root=config.PROJECT_ROOT,
        stage="pipeline",
        seed=args.seed,
        legacy=args.legacy,
    )

    if paths.legacy:
        log_dir = config.RESULTS_ROOT / "logs" / f"legacy_{run_utils.make_run_id('pipeline', args.seed)}"
        paths.logs_dir = log_dir  # type: ignore[misc]
        log_dir.mkdir(parents=True, exist_ok=True)
        print("[WARNING] Mode legacy: hasil lama dapat tertimpa.")
    else:
        run_utils.bootstrap_run(
            paths,
            "pipeline",
            {
                "stage": "pipeline",
                "seed": args.seed,
                "trials": args.trials,
                "epochs": args.epochs,
                "screening_epochs": args.screening_epochs,
                "cv_splits": args.cv_splits,
                "seeds": args.seeds,
                "reuse_data": args.reuse_data,
                "stages": list(STAGE_SCRIPTS) if args.all else [args.stage],
            },
        )

    print("=" * 70)
    print("MASTER PIPELINE SKRIPSI: LSTM + OPTUNA BITCOIN")
    print(f"Run ID : {paths.run_id}")
    print(f"Root   : {paths.root}")
    print(f"Output : {paths.run_dir}")
    print(f"Mode   : {'dry-run' if args.dry_run else 'execute'}")
    print("=" * 70)

    stages = list(STAGE_SCRIPTS) if args.all else [args.stage]
    pipeline_started = run_utils.utc_now()
    try:
        for stage in stages:
            run_stage(stage, args, paths)
    except PipelineError as exc:
        print(f"\n[FAILED] {exc}")
        return 1

    if not args.dry_run:
        run_utils.record_stage(
            paths,
            "pipeline",
            status="success",
            started_at=pipeline_started,
            stage_config={
                "stage": "pipeline",
                "seed": args.seed,
                "trials": args.trials,
                "epochs": args.epochs,
                "screening_epochs": args.screening_epochs,
                "cv_splits": args.cv_splits,
                "seeds": args.seeds,
                "reuse_data": args.reuse_data,
                "stages": stages,
            },
        )
        summary_path = paths.run_dir / "pipeline_summary.json"
        run_utils.write_json(
            summary_path,
            {
                "run_id": paths.run_id,
                "status": "success",
                "stages": stages,
                "finished_at": run_utils.utc_now(),
                "output_dir": str(paths.run_dir),
            },
        )
        print("\n" + "=" * 70)
        print(f"PIPELINE SELESAI: {paths.run_dir}")
        print(f"Manifest: {paths.manifest_path}")
        print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
