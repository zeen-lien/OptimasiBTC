"""Sequence window shape, alignment, and leakage checks."""

from __future__ import annotations

import numpy as np
import pytest

from data_utils import create_sequences


def test_sequence_shapes_and_target_alignment():
    series = np.arange(10, dtype=float)
    X, y = create_sequences(series, lookback=3)
    assert X.shape == (7, 3, 1)
    assert y.shape == (7,)
    assert X.dtype == np.float32
    np.testing.assert_array_equal(X[0, :, 0], [0.0, 1.0, 2.0])
    np.testing.assert_array_equal(y, np.arange(3, 10, dtype=np.float32))
    for index in range(len(y)):
        assert y[index] == series[index + 3]


def test_no_future_values_in_test_windows():
    train = np.arange(0, 100, dtype=float)
    test = np.arange(100, 120, dtype=float)
    lookback = 5
    combined = np.concatenate([train[-lookback:], test])
    X, y = create_sequences(combined, lookback)

    assert len(X) == len(test)
    assert X[0, :, 0].max() < 100.0
    assert y[0] == 100.0
    assert y[-1] == 119.0
    for index in range(len(X)):
        assert X[index, :, 0].max() < y[index]


def test_invalid_lookback_rejected():
    with pytest.raises(ValueError):
        create_sequences(np.arange(5), lookback=0)
    with pytest.raises(ValueError):
        create_sequences(np.arange(5), lookback=5)
