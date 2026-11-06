"""[BAB 3 Â§3.1 | KONFIGURASI DAN PARAMETER RESMI STUDY 2]

Modul ini mendefinisikan konstanta, direktori berkas, dan konfigurasi praregistrasi
untuk Study 2: Peramalan Realized Volatility Harian Bitcoin Menggunakan LSTM dan Optuna.
Seluruh nilai mengacu pada protokol penelitian resmi (docs/STUDY2_PROTOCOL.md)
yang telah dibekukan dan di-hash sebelum pengujian data eksternal.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# ---------------------------------------------------------------------------
# [BAB 3 Â§3.2 | STRUKTUR DIREKTORI DAN REPRODUKSIBILITAS]
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
# [BAB 3 Â§3.4 | PEMBAGIAN PERIODE TEMPORAL DAN AMANDEMEN A1]
# ---------------------------------------------------------------------------
DATA_START = "2020-01-01"
DATA_END = "2026-09-30"          # Berkas kline Binance Vision Oktober 2026 belum rilis
DEV_START = "2020-01-01"
DEV_END = "2023-12-31"           # Jendela HPO / cross-validation (4 tahun)
VAL_START = "2024-01-01"
VAL_END = "2025-12-31"           # Jendela validasi internal / checkpoint
TRAIN_POOL_END = "2025-12-31"    # Kumpulan data latih final (DEV + VAL)
TEST_START = "2026-01-01"
TEST_END = "2026-09-30"          # Jendela uji eksternal (out-of-sample)

EXPECTED_TOTAL_DAYS = 2464       # 2.465 hari kalender minus 1 hari dikeluarkan (A1: 2020-02-19)
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
# [BAB 3 Â§3.3 | TARGET DAN FITUR VOLATILITAS]
# ---------------------------------------------------------------------------
TARGET = "log_rv"
FEATURES = ["log_rv", "log_range", "log_volume", "log_absret", "rv_mean_5", "rv_mean_22"]
RV_EPS = 1e-12

# ---------------------------------------------------------------------------
# [BAB 3 Â§3.6 | RUANG PENCARIAN HIPERPARAMETER DAN MULTI-SEED]
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
# [BAB 3 Â§3.7 | PENGUJIAN INFERENSI STATISTIK]
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
# [BAB 3 Â§3.2 | HELPER HASH DAN INTEGRITAS BUKTI]
# ---------------------------------------------------------------------------
def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    """Menghitung ringkasan SHA-256 berkas biner secara streaming."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    """Menghitung ringkasan SHA-256 dari string teks UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def protocol_hash() -> str:
    """Ringkasan SHA-256 berkas protokol praregistrasi resmi."""
    return sha256_file(PROTOCOL_PATH)
