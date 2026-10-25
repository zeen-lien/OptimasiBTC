"""
experiment_utils.py - Shared training, metric, and persistence helpers.

Keeping these in one place prevents Tier 1/2/3 from drifting apart in the
way metrics, prediction columns, and provenance are produced.
"""

from __future__ import annotations

import os
import random
import time
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy, and TensorFlow (imported lazily)."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    import tensorflow as tf

    tf.random.set_seed(seed)
    try:
        tf.keras.utils.set_random_seed(seed)
    except AttributeError:  # older TF
        pass


def build_lstm_model(
    lookback: int,
    units: int,
    dropout: float,
    learning_rate: float,
    layers: int = 1,
    loss: str = "mean_squared_error",
):
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.optimizers import Adam

    model = Sequential()
    model.add(Input(shape=(lookback, 1)))
    for layer_idx in range(layers):
        return_sequences = layer_idx < layers - 1
        layer_units = units if layer_idx == 0 else max(16, units // (2 ** layer_idx))
        model.add(LSTM(layer_units, return_sequences=return_sequences))
        model.add(Dropout(dropout))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss=loss)
    return model


def make_test_sequences(
    train_scaled: np.ndarray,
    test_scaled: np.ndarray,
    lookback: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Attach the last in-sample window so every test day is predicted once."""
    from data_utils import create_sequences

    test_full = np.concatenate([train_scaled[-lookback:], test_scaled])
    return create_sequences(test_full, lookback)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "MAPE": float(mean_absolute_percentage_error(y_true, y_pred) * 100.0),
    }


def rounded_metrics(metrics: Mapping[str, float]) -> dict[str, float]:
    return {key: round(float(value), 2) for key, value in metrics.items()}


def parse_seeds(value: str | None, primary: int) -> list[int]:
    """
    Parse ``--seeds`` and always include the primary seed first.

    ``--seeds`` accepts a comma-separated list (e.g. ``"42,123,2024"``).
    Duplicates are removed while preserving order.
    """
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
    return seeds


def build_predictions_frame(
    dates: Any,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    prediction_column: str,
) -> pd.DataFrame:
    if len(dates) != len(y_true) or len(y_true) != len(y_pred):
        raise ValueError(
            f"Panjang tanggal/aktual/prediksi tidak sama: {len(dates)}/{len(y_true)}/{len(y_pred)}"
        )
    return pd.DataFrame(
        {
            "date": pd.to_datetime(pd.Series(dates)).dt.strftime("%Y-%m-%d"),
            "actual_close": y_true,
            prediction_column: y_pred,
            "error": y_true - y_pred,
            "abs_pct_error": np.abs((y_true - y_pred) / y_true) * 100.0,
        }
    )


def resolve_processed_dir(
    run_processed_dir: Path,
    legacy_processed_dir: Path,
) -> tuple[Path, str]:
    """Prefer this run's processed data, then fall back to frozen legacy data."""
    required = ("train_insample.csv", "test_outofsample.csv", "minmax_scaler.joblib")
    if all((run_processed_dir / name).exists() for name in required):
        return run_processed_dir, "run"
    if all((legacy_processed_dir / name).exists() for name in required):
        return legacy_processed_dir, "legacy"
    raise FileNotFoundError(
        "Data processed tidak ditemukan di run maupun folder legacy: "
        f"{run_processed_dir}, {legacy_processed_dir}"
    )


class Timer:
    """Small context manager for wall-clock timings."""

    def __init__(self) -> None:
        self.started_at = time.perf_counter()

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started_at
