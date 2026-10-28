"""
s2_config.py - Constants, paths, and pre-registered settings for Study 2.

Study 2: LSTM + Optuna for daily Bitcoin realized-volatility forecasting.
All values here mirror docs/STUDY2_PROTOCOL.md (frozen before any 2026 test).
Study 1 lives in 05_Source_Code/model_experiment/ and must not be modified.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "05_Source_Code"

S2_PACKAGE_DIR = SOURCE_ROOT / "study2_volatility"
S2_DATA_DIR = SOURCE_ROOT / "data" / "study2"
S2_RAW_ZIP_DIR = S2_DATA_DIR / "raw_1h_monthly"
S2_DAILY_CSV = S2_DATA_DIR / "btc_1h_daily_rv_2020_2026.csv"
S2_RAW_MANIFEST = S2_DATA_DIR / "raw_zips_manifest.json"
S2_DATA_FREEZE_HASH = S2_DATA_DIR / "data_freeze_hash.txt"

S2_RESULTS_ROOT = SOURCE_ROOT / "results" / "study2"
S2_RUNS_ROOT = S2_RESULTS_ROOT / "runs"

PROTOCOL_PATH = PROJECT_ROOT / "docs" / "STUDY2_PROTOCOL.md"
PROTOCOL_HASH_PATH = PROJECT_ROOT / "docs" / "STUDY2_PROTOCOL_HASH.txt"

# ---------------------------------------------------------------------------
# Data window (pre-registered)
# ---------------------------------------------------------------------------
DATA_START = "2020-01-01"
DATA_END = "2026-09-30"          # 2026-10 zip not published yet (checked 2026-10-28)
DEV_START = "2020-01-01"
DEV_END = "2023-12-31"           # HPO via purged rolling-origin CV
VAL_START = "2024-01-01"
VAL_END = "2025-12-31"           # checkpoint only; never used for selection
TRAIN_POOL_END = "2025-12-31"    # final refit pool = DEV + VAL
TEST_START = "2026-01-01"
TEST_END = "2026-09-30"          # external test, executed once

EXPECTED_TOTAL_DAYS = 2464       # 2465 calendar days minus 1 dropped (A1: 2020-02-19, 19 bars)
DROPPED_DAYS_A1 = ("2020-02-19",)
BARS_PER_DAY = 24

BINANCE_VISION_URL = (
    "https://data.binance.vision/data/spot/monthly/klines/"
    "BTCUSDT/1h/BTCUSDT-1h-{month}.zip"
)
MONTHS = [
    f"{y}-{m:02d}"
    for y, m in [(y, m) for y in range(2020, 2027) for m in range(1, 13)]
    if "2020-01" <= f"{y}-{m:02d}" <= "2026-09"
]

# ---------------------------------------------------------------------------
# Target / features (pre-registered, section 2 of the protocol)
# ---------------------------------------------------------------------------
TARGET = "log_rv"
FEATURES = ["log_rv", "log_range", "log_volume", "log_absret", "rv_mean_5", "rv_mean_22"]
RV_EPS = 1e-12

# ---------------------------------------------------------------------------
# Optimization (pre-registered, sections 5-6)
# ---------------------------------------------------------------------------
SEEDS = (42, 123, 2024, 7, 99)
OPTUNA_SEED = 42
N_TRIALS = 50
N_CV_FOLDS = 5
PRUNER_STARTUP_TRIALS = 10
PRUNER_WARMUP_STEPS = 2
MAX_EPOCHS = 100
EARLY_STOP_PATIENCE = 10

SEARCH_SPACE = {
    "lookback": {"low": 10, "high": 30},
    "units": {"low": 16, "high": 128},
    "layers": {"choices": [1, 2]},
    "dropout": {"low": 0.05, "high": 0.40, "step": 0.05},
    "learning_rate": {"low": 3e-4, "high": 2e-3, "log": True},
    "batch_size": {"choices": [16, 32, 64]},
}

UNTUNED_LSTM = {
    "lookback": 21,
    "units": 64,
    "dropout": 0.20,
    "learning_rate": 1e-3,
    "batch_size": 32,
    "layers": 1,
}

# ---------------------------------------------------------------------------
# Statistics (pre-registered, section 8)
# ---------------------------------------------------------------------------
DM_HAC_LAG = 5
BOOTSTRAP_BLOCK = 20
BOOTSTRAP_REPS = 10_000
BOOTSTRAP_SEED = 42
ALPHA = 0.05

PRIMARY_BASELINES = ("persistence", "har_rv")
SECONDARY_BASELINES = ("garch11", "lstm_untuned")

MODELS = ("persistence", "har_rv", "garch11", "lstm_untuned", "lstm_optuna")


# ---------------------------------------------------------------------------
# Hash helpers
# ---------------------------------------------------------------------------
def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def protocol_hash() -> str:
    """SHA-256 of the frozen protocol document."""
    return sha256_file(PROTOCOL_PATH)
