"""
[BAB 3 §3.1 & §3.7 | MANIFEST PROVENANCE & JEJAK AUDIT RUN]
Modul ini bertugas mencatat manifest minimal untuk setiap proses komputasi Study 2,
mencakup hash Git commit, lingkungan dependensi Python, stempel waktu UTC,
dan hash data agar setiap hasil eksperimen dapat diaudit secara independen.

Setiap eksekusi membuat subdirektori di: `05_Source_Code/results/study2/runs/{run_id}/`
yang memuat: `manifest.json`, `env.json`, `git_commit.txt`, dan `log.txt`.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import s2_config as cfg


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def python_env() -> dict:
    import importlib.metadata as md

    pkgs = ["tensorflow", "optuna", "scikit-learn", "numpy", "pandas", "arch", "statsmodels"]
    return {"python": sys.version.split()[0],
            "packages": {p: md.version(p) for p in pkgs if _has(p)}}


def _has(name: str) -> bool:
    try:
        import importlib.metadata as md
        md.version(name)
        return True
    except Exception:
        return False


def new_run(label: str, extra: dict | None = None) -> tuple[str, Path]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"{stamp}_{label}_{uuid.uuid4().hex[:6]}"
    run_dir = cfg.S2_RUNS_ROOT / run_id
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)

    payload = {
        "run_id": run_id,
        "label": label,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "protocol_sha256": cfg.protocol_hash(),
        "protocol_sha256_recorded": cfg.PROTOCOL_HASH_PATH.read_text().strip(),
        "data": {
            "daily_csv_sha256": cfg.sha256_file(cfg.S2_DAILY_CSV),
            "freeze": (cfg.S2_DATA_FREEZE_HASH.read_text(encoding="utf-8")
                       if cfg.S2_DATA_FREEZE_HASH.exists() else None),
        },
        "env": python_env(),
        "extra": extra or {},
    }
    (run_dir / "manifest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (run_dir / "git_commit.txt").write_text(payload["git_commit"] + "\n", encoding="utf-8")
    (run_dir / "env.json").write_text(json.dumps(payload["env"], indent=2), encoding="utf-8")
    print(f"[run] {run_id} -> {run_dir}")
    return run_id, run_dir
