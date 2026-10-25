"""
data_utils.py - Shared data and sequence utilities for model experiments.

Paths come from config.py; no Windows absolute paths live here anymore.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import config


def load_raw_data(filepath: Path | str | None = None) -> pd.DataFrame:
    path = Path(filepath) if filepath is not None else config.RAW_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"File data mentah tidak ditemukan: {path}")

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def split_temporal(df: pd.DataFrame, train_ratio: float = 0.80) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split chronologically into in-sample and out-of-sample partitions."""
    if not 0 < train_ratio < 1:
        raise ValueError(f"train_ratio harus di antara 0 dan 1, diterima: {train_ratio}")
    train_size = int(len(df) * train_ratio)
    train_df = df.iloc[:train_size].copy().reset_index(drop=True)
    test_df = df.iloc[train_size:].copy().reset_index(drop=True)
    return train_df, test_df


def fit_scaler(train_df: pd.DataFrame) -> MinMaxScaler:
    """Fit MinMaxScaler on the in-sample close price only."""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(train_df[["close"]].values)
    return scaler


def transform_data(scaler: MinMaxScaler, df: pd.DataFrame) -> np.ndarray:
    return scaler.transform(df[["close"]].values).flatten()


def create_sequences(series: np.ndarray, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Build (X, y) sliding windows.

    X[i] = series[i : i + lookback]
    y[i] = series[i + lookback]  (the value immediately after the window)

    Returns X with shape (samples, lookback, 1) and y with shape (samples,).
    """
    if lookback < 1:
        raise ValueError("lookback harus >= 1")
    series = np.asarray(series).reshape(-1)
    if len(series) <= lookback:
        raise ValueError(
            f"Panjang series ({len(series)}) harus lebih besar dari lookback ({lookback})"
        )

    windows = np.lib.stride_tricks.sliding_window_view(series, lookback)
    X = windows[:-1].astype(np.float32)
    y = series[lookback:].astype(np.float32)
    return X.reshape(-1, lookback, 1), y


def load_processed_data(
    processed_dir: Path | str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, MinMaxScaler]:
    """Load train/test partitions and the final scaler."""
    proc_dir = Path(processed_dir) if processed_dir is not None else config.PROCESSED_DIR
    train_path = proc_dir / "train_insample.csv"
    test_path = proc_dir / "test_outofsample.csv"
    scaler_path = proc_dir / "minmax_scaler.joblib"

    missing = [str(path) for path in (train_path, test_path, scaler_path) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Artefak prapemrosesan tidak lengkap: " + ", ".join(missing)
        )

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    scaler = joblib.load(scaler_path)
    return train_df, test_df, scaler
