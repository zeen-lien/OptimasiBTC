"""Fase 2 CV protocol: per-fold scaler and purge/embargo checks."""

from __future__ import annotations

import numpy as np
import pytest

from cv_utils import (
    build_fold_sequences,
    purged_time_folds,
    scaler_bounds,
    window_raw_indices,
)
from data_utils import load_processed_data


@pytest.fixture(scope="module")
def raw_in_sample():
    train_df, _, _ = load_processed_data()
    return train_df["close"].to_numpy(dtype=float)


def test_folds_are_chronological_and_purged(raw_in_sample):
    lookback = 22
    folds = list(purged_time_folds(len(raw_in_sample), n_splits=5, gap=lookback))
    assert len(folds) == 5
    for fold, train_idx, val_idx in folds:
        assert train_idx.max() < val_idx.min()
        assert val_idx[0] - train_idx[-1] - 1 == lookback
        assert len(val_idx) > 0


def test_fold_scaler_uses_train_values_only(raw_in_sample):
    lookback = 22
    for fold, train_idx, val_idx in purged_time_folds(len(raw_in_sample), 5, lookback):
        bundle = build_fold_sequences(raw_in_sample, train_idx, val_idx, lookback, fold)
        low, high = scaler_bounds(bundle.scaler)
        assert low == pytest.approx(raw_in_sample[train_idx].min())
        assert high == pytest.approx(raw_in_sample[train_idx].max())
        # Validation may exceed the training range; it must not influence it.
        assert low <= raw_in_sample[val_idx].min()
        assert high >= raw_in_sample[val_idx].min()


def test_validation_windows_do_not_overlap_training_windows(raw_in_sample):
    lookback = 22
    for fold, train_idx, val_idx in purged_time_folds(len(raw_in_sample), 5, lookback):
        bundle = build_fold_sequences(raw_in_sample, train_idx, val_idx, lookback, fold)
        train_windows = window_raw_indices(
            int(train_idx[0]), len(bundle.X_train), lookback
        )
        val_windows = window_raw_indices(
            int(val_idx[0]) - lookback, len(bundle.X_val), lookback
        )
        assert not (train_windows & val_windows)


def test_validation_targets_match_raw_usd(raw_in_sample):
    lookback = 10
    fold, train_idx, val_idx = next(purged_time_folds(len(raw_in_sample), 5, lookback))
    bundle = build_fold_sequences(raw_in_sample, train_idx, val_idx, lookback, fold)
    np.testing.assert_allclose(bundle.y_val_usd, raw_in_sample[val_idx])
    assert bundle.X_val.shape[1:] == (lookback, 1)
    assert len(bundle.X_val) == len(val_idx)


def test_too_few_samples_rejected():
    with pytest.raises(ValueError):
        list(purged_time_folds(5, n_splits=5, gap=1))
