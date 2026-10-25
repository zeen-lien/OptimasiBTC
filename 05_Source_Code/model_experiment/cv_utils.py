"""
cv_utils.py - Leakage-safe time-series cross-validation.

Protocol (Fase 2):
- expanding-window TimeSeriesSplit on raw in-sample close prices;
- purge gap equal to the trial lookback, so no raw observation is shared by
  a training window and a validation window;
- MinMaxScaler fit on the training fold only;
- validation predictions inverse-transformed to USD before scoring.

The holdout test set is never passed to this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler

from data_utils import create_sequences


@dataclass
class FoldSequences:
    fold: int
    train_idx: np.ndarray
    val_idx: np.ndarray
    scaler: MinMaxScaler
    X_train: np.ndarray
    y_train: np.ndarray
    X_val: np.ndarray
    y_val: np.ndarray
    y_val_usd: np.ndarray


def purged_time_folds(
    n_samples: int,
    n_splits: int = 5,
    gap: int = 0,
) -> Iterator[tuple[int, np.ndarray, np.ndarray]]:
    """Yield ``(fold, train_idx, val_idx)`` with a purge gap between them."""
    if n_samples <= n_splits:
        raise ValueError(
            f"n_samples={n_samples} terlalu kecil untuk {n_splits} fold"
        )
    splitter = TimeSeriesSplit(n_splits=n_splits, gap=max(0, int(gap)))
    for fold, (train_idx, val_idx) in enumerate(splitter.split(np.arange(n_samples))):
        yield fold, train_idx, val_idx


def fit_fold_scaler(train_values: np.ndarray) -> MinMaxScaler:
    """Fit MinMaxScaler on training-fold raw values only."""
    values = np.asarray(train_values, dtype=float).reshape(-1, 1)
    if len(values) == 0:
        raise ValueError("Training fold kosong; tidak bisa fit scaler")
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(values)
    return scaler


def build_fold_sequences(
    raw_series: np.ndarray,
    train_idx: np.ndarray,
    val_idx: np.ndarray,
    lookback: int,
    fold: int = 0,
) -> FoldSequences:
    """
    Build train/validation sequences for one purged fold.

    The validation inputs use the raw observations immediately before the
    validation block (available at forecast time). Because ``gap=lookback``,
    those observations are not part of the training block.
    """
    raw_series = np.asarray(raw_series, dtype=float).reshape(-1)
    train_idx = np.asarray(train_idx, dtype=int)
    val_idx = np.asarray(val_idx, dtype=int)

    if len(train_idx) <= lookback:
        raise ValueError(
            f"Fold {fold}: train length {len(train_idx)} <= lookback {lookback}"
        )
    if len(val_idx) == 0:
        raise ValueError(f"Fold {fold}: validation kosong")
    if val_idx[0] - lookback < 0:
        raise ValueError(f"Fold {fold}: tidak ada sejarah cukup sebelum validation")

    train_raw = raw_series[train_idx]
    val_start = int(val_idx[0])
    val_end = int(val_idx[-1]) + 1
    val_raw = raw_series[val_start:val_end]
    val_input_raw = raw_series[val_start - lookback : val_end]

    scaler = fit_fold_scaler(train_raw)
    train_scaled = scaler.transform(train_raw.reshape(-1, 1)).ravel()
    val_input_scaled = scaler.transform(val_input_raw.reshape(-1, 1)).ravel()

    X_train, y_train = create_sequences(train_scaled, lookback)
    X_val, y_val = create_sequences(val_input_scaled, lookback)

    if len(X_val) != len(val_raw):
        raise AssertionError(
            f"Fold {fold}: panjang X_val {len(X_val)} != val_raw {len(val_raw)}"
        )

    return FoldSequences(
        fold=fold,
        train_idx=train_idx,
        val_idx=val_idx,
        scaler=scaler,
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        y_val_usd=val_raw,
    )


def scaler_bounds(scaler: MinMaxScaler) -> tuple[float, float]:
    return float(scaler.data_min_[0]), float(scaler.data_max_[0])


def window_raw_indices(start: int, n_windows: int, lookback: int) -> set[int]:
    """Raw indices used by a contiguous block of sliding windows."""
    used: set[int] = set()
    for offset in range(n_windows):
        used.update(range(start + offset, start + offset + lookback))
    return used
