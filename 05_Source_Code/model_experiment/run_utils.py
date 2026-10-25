"""
run_utils.py - Run isolation, manifests, and provenance helpers.

Every experiment run gets its own directory:

    results/runs/{run_id}/
        config.json
        env.json
        data_hash.txt
        data_hash.json
        git_commit.txt
        manifest.json
        metrics/
        predictions/
        figures/
        models/
        processed/
        logs/

Legacy artifacts under results/metrics, results/predictions_*.csv, and
models/ are never overwritten unless a script is called with --legacy.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import socket
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import config

RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MANIFEST_SCHEMA_VERSION = 1


# ---------------------------------------------------------------------------
# Run paths
# ---------------------------------------------------------------------------
@dataclass
class RunPaths:
    """Absolute paths for one isolated experiment run."""

    run_id: str
    root: Path
    run_dir: Path
    raw_dir: Path
    processed_dir: Path
    models_dir: Path
    metrics_dir: Path
    predictions_dir: Path
    figures_dir: Path
    logs_dir: Path
    legacy: bool = False

    @property
    def config_path(self) -> Path:
        return self.run_dir / "config.json"

    @property
    def manifest_path(self) -> Path:
        return self.run_dir / "manifest.json"

    @property
    def env_path(self) -> Path:
        return self.run_dir / "env.json"

    @property
    def git_commit_path(self) -> Path:
        return self.run_dir / "git_commit.txt"

    @property
    def data_hash_path(self) -> Path:
        return self.run_dir / "data_hash.txt"

    @property
    def data_hash_json_path(self) -> Path:
        return self.run_dir / "data_hash.json"

    @property
    def summary_path(self) -> Path:
        return self.run_dir / "summary.json"

    def create(self) -> "RunPaths":
        for path in (
            self.run_dir,
            self.raw_dir,
            self.processed_dir,
            self.models_dir,
            self.metrics_dir,
            self.predictions_dir,
            self.figures_dir,
            self.logs_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
        return self

    def as_dict(self) -> dict[str, str]:
        return {
            "run_id": self.run_id,
            "root": str(self.root),
            "run_dir": str(self.run_dir),
            "raw_dir": str(self.raw_dir),
            "processed_dir": str(self.processed_dir),
            "models_dir": str(self.models_dir),
            "metrics_dir": str(self.metrics_dir),
            "predictions_dir": str(self.predictions_dir),
            "figures_dir": str(self.figures_dir),
            "logs_dir": str(self.logs_dir),
            "legacy": self.legacy,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_run_id(
    stage: str = "run",
    seed: int | None = None,
    timestamp: datetime | None = None,
) -> str:
    """Create a human-readable run id, e.g. ``2026-10-25_143000_tier3_seed42``."""
    stamp = (timestamp or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
    safe_stage = re.sub(r"[^A-Za-z0-9._-]+", "-", stage).strip("-") or "run"
    parts = [stamp, safe_stage]
    if seed is not None:
        parts.append(f"seed{seed}")
    return "_".join(parts)


def _legacy_paths(root: Path) -> RunPaths:
    source = root / "05_Source_Code"
    results = source / "results"
    return RunPaths(
        run_id="legacy",
        root=root,
        run_dir=results,
        raw_dir=source / "data" / "raw",
        processed_dir=source / "data" / "processed",
        models_dir=source / "models",
        metrics_dir=results / "metrics",
        predictions_dir=results,
        figures_dir=results / "figures",
        logs_dir=results / "logs",
        legacy=True,
    )


def resolve_run_paths(
    run_id: str | None = None,
    root: Path | str | None = None,
    stage: str = "run",
    seed: int | None = None,
    legacy: bool = False,
    create: bool = True,
) -> RunPaths:
    """Resolve paths for a run.

    - ``legacy=True`` maps to the original flat artifact locations.
    - ``run_id=None`` generates a new timestamped id and guarantees uniqueness.
    - Explicit ids are validated and reused, which is how the orchestrator
      passes one id to every stage.
    """
    project_root = Path(root).resolve() if root is not None else config.PROJECT_ROOT

    if legacy:
        paths = _legacy_paths(project_root)
        return paths.create() if create else paths

    runs_root = project_root / "05_Source_Code" / "results" / "runs"
    if run_id is None:
        base = make_run_id(stage=stage, seed=seed)
        candidate = base
        counter = 2
        while (runs_root / candidate).exists():
            candidate = f"{base}_{counter:02d}"
            counter += 1
        run_id = candidate
    else:
        run_id = str(run_id).strip()
        if not RUN_ID_PATTERN.fullmatch(run_id):
            raise ValueError(
                f"run_id tidak valid: {run_id!r}. Gunakan huruf, angka, titik, "
                "garis bawah, atau tanda hubung."
            )

    run_dir = runs_root / run_id
    paths = RunPaths(
        run_id=run_id,
        root=project_root,
        run_dir=run_dir,
        raw_dir=run_dir / "raw",
        processed_dir=run_dir / "processed",
        models_dir=run_dir / "models",
        metrics_dir=run_dir / "metrics",
        predictions_dir=run_dir / "predictions",
        figures_dir=run_dir / "figures",
        logs_dir=run_dir / "logs",
    )
    return paths.create() if create else paths


# ---------------------------------------------------------------------------
# JSON / hashing / git / environment
# ---------------------------------------------------------------------------
def read_json(path: Path | str, default: Any = None) -> Any:
    path = Path(path)
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path | str, payload: Any) -> Path:
    """Write JSON atomically so interrupted runs do not leave half files."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)
        handle.write("\n")
    os.replace(tmp_path, path)
    return path


def sha256_file(path: Path | str, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_to_root(path: Path | str, root: Path) -> str:
    path = Path(path)
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def hash_inputs(
    inputs: Mapping[str, Path | str] | Iterable[Path | str],
    root: Path,
) -> dict[str, str]:
    """Hash existing input files and return ``{relative_path: sha256}``."""
    if isinstance(inputs, Mapping):
        items = [(label, Path(path)) for label, path in inputs.items()]
    else:
        items = [(relative_to_root(path, root), Path(path)) for path in inputs]

    hashes: dict[str, str] = {}
    for label, path in items:
        if path.is_file():
            hashes[label] = sha256_file(path)
        elif path.exists():
            hashes[label] = f"directory:{path}"
        else:
            hashes[label] = "missing"
    return hashes


def write_hash_manifest(paths: RunPaths, hashes: Mapping[str, str]) -> None:
    merged = read_json(paths.data_hash_json_path, default={}) or {}
    merged.update(dict(hashes))
    write_json(paths.data_hash_json_path, merged)
    lines = [f"{digest}  {label}" for label, digest in sorted(merged.items())]
    paths.data_hash_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def git_metadata(root: Path) -> dict[str, Any]:
    """Return commit id, branch, and dirty status without failing outside git."""
    def _run(*args: str) -> str:
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()

    try:
        commit = _run("rev-parse", "HEAD")
        branch = _run("rev-parse", "--abbrev-ref", "HEAD")
        status = _run("status", "--porcelain")
        return {
            "commit": commit,
            "branch": branch,
            "dirty": bool(status),
            "status_porcelain": status.splitlines(),
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "commit": "unavailable",
            "branch": "unavailable",
            "dirty": None,
            "error": str(exc),
        }


def environment_metadata() -> dict[str, Any]:
    return {
        "created_at": utc_now(),
        "python": sys.version,
        "python_version": platform.python_version(),
        "executable": sys.executable,
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
        "packages": config.package_versions(),
        "environment_variables": {
            key: os.environ.get(key)
            for key in (
                "TF_CPP_MIN_LOG_LEVEL",
                "TF_ENABLE_ONEDNN_OPTS",
                "TF_DETERMINISTIC_OPS",
                "PYTHONHASHSEED",
                "CUDA_VISIBLE_DEVICES",
            )
        },
    }


def bootstrap_run(
    paths: RunPaths,
    stage: str,
    stage_config: Mapping[str, Any] | None = None,
    inputs: Mapping[str, Path | str] | Iterable[Path | str] | None = None,
) -> dict[str, Any]:
    """Create/refresh provenance files for a run and return the manifest."""
    if paths.legacy:
        return {}

    paths.create()
    now = utc_now()

    # Environment and git are written once per run, then reused.
    if not paths.env_path.exists():
        write_json(paths.env_path, environment_metadata())

    git_info = read_json(paths.run_dir / "git.json", default=None)
    if git_info is None:
        git_info = git_metadata(paths.root)
        write_json(paths.run_dir / "git.json", git_info)
        commit_text = git_info.get("commit", "unavailable")
        dirty_text = "dirty" if git_info.get("dirty") else "clean"
        paths.git_commit_path.write_text(
            f"{commit_text}\nstatus: {dirty_text}\n", encoding="utf-8"
        )

    if inputs:
        write_hash_manifest(paths, hash_inputs(inputs, paths.root))

    # Environment/protocol files are part of the experiment provenance.
    governed_files = {
        "docs/PROTOCOL.md": paths.root / "docs" / "PROTOCOL.md",
        "requirements.txt": paths.root / "requirements.txt",
    }
    existing_governed = {
        label: path for label, path in governed_files.items() if path.is_file()
    }
    if existing_governed:
        write_hash_manifest(paths, hash_inputs(existing_governed, paths.root))

    config_payload = read_json(paths.config_path, default=None) or {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "run_id": paths.run_id,
        "created_at": now,
        "stages": {},
    }
    config_payload["run_id"] = paths.run_id
    config_payload["updated_at"] = now
    config_payload.setdefault("stages", {})
    if stage_config is not None:
        config_payload["stages"][stage] = dict(stage_config)
    write_json(paths.config_path, config_payload)

    manifest = read_json(paths.manifest_path, default=None) or {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "run_id": paths.run_id,
        "project_root": str(paths.root),
        "created_at": now,
        "stages": {},
        "stage_order": [],
    }
    manifest["updated_at"] = now
    manifest["paths"] = paths.as_dict()
    if stage not in manifest["stage_order"]:
        manifest["stage_order"].append(stage)
    write_json(paths.manifest_path, manifest)
    return manifest


def record_stage(
    paths: RunPaths,
    stage: str,
    status: str,
    started_at: str,
    finished_at: str | None = None,
    stage_config: Mapping[str, Any] | None = None,
    inputs: Mapping[str, Path | str] | Iterable[Path | str] | None = None,
    outputs: Sequence[Path | str] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Record one stage result in config.json, manifest.json, and hashes."""
    if paths.legacy:
        return {}

    finished_at = finished_at or utc_now()
    if inputs:
        write_hash_manifest(paths, hash_inputs(inputs, paths.root))
    if outputs:
        output_hashes = {
            relative_to_root(path, paths.root): sha256_file(path)
            for path in outputs
            if Path(path).is_file()
        }
        if output_hashes:
            write_hash_manifest(paths, output_hashes)

    manifest = read_json(paths.manifest_path, default=None) or bootstrap_run(
        paths, stage, stage_config, inputs
    )
    entry = {
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_seconds": _duration_seconds(started_at, finished_at),
    }
    if stage_config is not None:
        entry["config"] = dict(stage_config)
    if extra:
        entry.update(dict(extra))
    manifest.setdefault("stages", {})[stage] = entry
    manifest["updated_at"] = finished_at
    if stage not in manifest.setdefault("stage_order", []):
        manifest["stage_order"].append(stage)
    write_json(paths.manifest_path, manifest)

    config_payload = read_json(paths.config_path, default=None) or {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "run_id": paths.run_id,
        "created_at": finished_at,
        "stages": {},
    }
    config_payload["updated_at"] = finished_at
    if stage_config is not None:
        config_payload.setdefault("stages", {})[stage] = dict(stage_config)
    write_json(paths.config_path, config_payload)
    return manifest


def _duration_seconds(started_at: str, finished_at: str) -> float | None:
    try:
        start = datetime.fromisoformat(started_at)
        end = datetime.fromisoformat(finished_at)
        return round((end - start).total_seconds(), 3)
    except (TypeError, ValueError):
        return None


def add_run_arguments(parser) -> None:
    """Add common run/provenance arguments to an argparse parser."""
    parser.add_argument(
        "--project-root",
        default=None,
        help="Root repo (default: lokasi config.py)",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="ID run yang sudah ada atau baru (default: dibuat otomatis)",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Tulis ke path artefak lama (hasil lama bisa tertimpa)",
    )


def apply_project_root(project_root: str | None) -> None:
    """Honor --project-root for the duration of a script."""
    if project_root:
        root = Path(project_root).resolve()
        config.PROJECT_ROOT = root
        config.SOURCE_ROOT = root / "05_Source_Code"
        config.DATA_ROOT = config.SOURCE_ROOT / "data"
        config.RAW_DATA_DIR = config.DATA_ROOT / "raw"
        config.PROCESSED_DIR = config.DATA_ROOT / "processed"
        config.RESULTS_ROOT = config.SOURCE_ROOT / "results"
        config.RUNS_ROOT = config.RESULTS_ROOT / "runs"
        config.MODELS_ROOT = config.SOURCE_ROOT / "models"
        config.NASKAH_DIR = root / "03_Naskah_Skripsi"
        config.GENERATORS_DIR = config.SOURCE_ROOT / "generators"
        config.RAW_DATA_PATH = config.RAW_DATA_DIR / "BTCUSDT_daily_2020_2025.csv"
        config.TRAIN_PATH = config.PROCESSED_DIR / "train_insample.csv"
        config.TEST_PATH = config.PROCESSED_DIR / "test_outofsample.csv"
        config.SCALER_PATH = config.PROCESSED_DIR / "minmax_scaler.joblib"
        config.PREPROCESSING_METADATA_PATH = (
            config.PROCESSED_DIR / "preprocessing_metadata.json"
        )
        config.LEGACY_METRICS_DIR = config.RESULTS_ROOT / "metrics"
        config.LEGACY_FIGURES_DIR = config.RESULTS_ROOT / "figures"
        config.LEGACY_STUDY_DB = config.RESULTS_ROOT / "optuna_study.db"
        config.LEGACY_TRIALS_CSV = config.RESULTS_ROOT / "optuna_trials_history.csv"
        config.LEGACY_SUMMARY_JSON = config.RESULTS_ROOT / "benchmark_comparison_summary.json"
        config.LEGACY_SUMMARY_CSV = config.RESULTS_ROOT / "benchmark_comparison_table.csv"


def run_context_from_args(args, stage: str, create: bool = True) -> RunPaths:
    """Resolve paths from a parsed argparse namespace."""
    apply_project_root(getattr(args, "project_root", None))
    return resolve_run_paths(
        run_id=getattr(args, "run_id", None),
        root=config.PROJECT_ROOT,
        stage=stage,
        seed=getattr(args, "seed", None),
        legacy=getattr(args, "legacy", False),
        create=create,
    )
