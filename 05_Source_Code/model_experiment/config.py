"""
config.py - Central project paths, seeds, and experiment constants.

All experiment scripts should import paths from here instead of hard-coding
Windows absolute paths. The project root is resolved relative to this file:

    05_Source_Code/model_experiment/config.py
    parents[0] = model_experiment
    parents[1] = 05_Source_Code
    parents[2] = project root
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Project root and directories
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "05_Source_Code"
DATA_ROOT = SOURCE_ROOT / "data"
RAW_DATA_DIR = DATA_ROOT / "raw"
PROCESSED_DIR = DATA_ROOT / "processed"
RESULTS_ROOT = SOURCE_ROOT / "results"
RUNS_ROOT = RESULTS_ROOT / "runs"
MODELS_ROOT = SOURCE_ROOT / "models"
NASKAH_DIR = PROJECT_ROOT / "03_Naskah_Skripsi"
GENERATORS_DIR = SOURCE_ROOT / "generators"

# Legacy artifact locations (kept for backward compatibility)
RAW_DATA_PATH = RAW_DATA_DIR / "BTCUSDT_daily_2020_2025.csv"
TRAIN_PATH = PROCESSED_DIR / "train_insample.csv"
TEST_PATH = PROCESSED_DIR / "test_outofsample.csv"
SCALER_PATH = PROCESSED_DIR / "minmax_scaler.joblib"
PREPROCESSING_METADATA_PATH = PROCESSED_DIR / "preprocessing_metadata.json"

LEGACY_METRICS_DIR = RESULTS_ROOT / "metrics"
LEGACY_FIGURES_DIR = RESULTS_ROOT / "figures"
LEGACY_STUDY_DB = RESULTS_ROOT / "optuna_study.db"
LEGACY_TRIALS_CSV = RESULTS_ROOT / "optuna_trials_history.csv"
LEGACY_SUMMARY_JSON = RESULTS_ROOT / "benchmark_comparison_summary.json"
LEGACY_SUMMARY_CSV = RESULTS_ROOT / "benchmark_comparison_table.csv"

# ---------------------------------------------------------------------------
# Reproducibility defaults
# ---------------------------------------------------------------------------
DEFAULT_SEEDS: tuple[int, ...] = (42, 123, 2024, 7, 99)
DEFAULT_TRAIN_RATIO = 0.80
DEFAULT_EPOCHS = 100
DEFAULT_OPTUNA_TRIALS = 50
DEFAULT_CV_SPLITS = 5

# Uncertainty quantification for the 439-day holdout. Blocks of 7 days keep
# short-range serial dependence; 2000 resamples give stable percentile CIs.
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_BLOCK_SIZE = 7
CONFIDENCE_LEVEL = 0.95

# Dataset contract. These values are asserted by tests/test_data.py.
DATASET_START_DATE = "2020-01-01"
DATASET_END_DATE = "2025-12-31"
EXPECTED_RAW_ROWS = 2192
EXPECTED_TRAIN_ROWS = 1753
EXPECTED_TEST_ROWS = 439
TEST_START_DATE = "2024-10-19"
TEST_END_DATE = "2025-12-31"

# Legacy configurations. They are recorded in manifests so the old results
# remain traceable; Fase 2/3 will introduce controlled experiment variants.
TIER1_CONFIG = {
    "lookback": 30,
    "units": 50,
    "dropout": 0.2,
    "learning_rate": 0.001,
    "batch_size": 32,
    "layers": 1,
    "epochs": DEFAULT_EPOCHS,
    "loss": "mean_squared_error",
    "optimizer": "adam",
    "scheduler": None,
    "early_stopping": {"monitor": "val_loss", "patience": 10},
}
TIER2_CONFIG = {
    "lookback": 60,
    "units": 128,
    "dropout": 0.2,
    "learning_rate": 0.001,
    "batch_size": 10,
    "layers": 1,
    "epochs": DEFAULT_EPOCHS,
    "loss": "mean_squared_error",
    "optimizer": "adam",
    "scheduler": None,
    "early_stopping": {"monitor": "val_loss", "patience": 10},
}
# Frozen best trial #36 from the pre-repair Optuna study. Used only for
# --retrain and as a manifest fallback, never as an optimization input.
TIER3_CONFIG = {
    "lookback": 22,
    "units": 100,
    "dropout": 0.1,
    "learning_rate": 0.001966341994199387,
    "batch_size": 16,
    "layers": 1,
    "epochs": DEFAULT_EPOCHS,
    "loss": "mean_absolute_error",
    "optimizer": "adam",
    "scheduler": "reduce_lr_on_plateau",
    "early_stopping": {"monitor": "val_loss", "patience": 12},
}
TIER3_STUDY_NAME = "lstm_bitcoin_optuna_tpe"

# Single source of truth for the Tier 3 search space.
# Keep this synchronized with the thesis tables and generator text.
SEARCH_SPACE = {
    "lookback": {"low": 7, "high": 30, "type": "int"},
    "units": {"low": 32, "high": 128, "type": "int"},
    "dropout": {"low": 0.10, "high": 0.40, "step": 0.05, "type": "float"},
    "learning_rate": {"low": 5e-4, "high": 2e-3, "log": True, "type": "float"},
    "batch_size": {"choices": [16, 32, 64], "type": "categorical"},
    "layers": {"low": 1, "high": 2, "type": "int"},
}


def ensure_project_directories() -> None:
    """Create the directories required by the pipeline if they do not exist."""
    for path in (
        RAW_DATA_DIR,
        PROCESSED_DIR,
        RESULTS_ROOT,
        RUNS_ROOT,
        MODELS_ROOT,
        NASKAH_DIR,
        GENERATORS_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Optional dependency versions (used only for run manifests)
# ---------------------------------------------------------------------------
def package_versions() -> dict[str, str]:
    """Return versions of the main packages without importing TensorFlow."""
    import importlib.metadata as metadata

    packages = [
        "tensorflow",
        "optuna",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "joblib",
        "requests",
        "python-docx",
        "docxcompose",
        "pillow",
        "sqlalchemy",
        "pytest",
    ]
    versions: dict[str, str] = {}
    for name in packages:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "not-installed"
    return versions
