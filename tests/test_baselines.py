"""Causal naive baselines must not read the future and must align with holdout."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import config
from baselines import build_baseline_predictions, evaluate_baselines
from data_utils import load_processed_data


@pytest.fixture(scope="module")
def processed():
    return load_processed_data()


@pytest.fixture(scope="module")
def baseline_predictions(processed):
    train_df, test_df, _ = processed
    return build_baseline_predictions(train_df, test_df)


def test_baseline_length_dates_and_no_nulls(baseline_predictions):
    assert len(baseline_predictions) == config.EXPECTED_TEST_ROWS
    assert baseline_predictions["date"].iloc[0] == config.TEST_START_DATE
    assert baseline_predictions["date"].iloc[-1] == config.TEST_END_DATE
    assert not baseline_predictions.isna().any().any()


def test_persistence_is_lagged_actual(processed, baseline_predictions):
    train_df, test_df, _ = processed
    full = np.concatenate(
        [train_df["close"].to_numpy(dtype=float), test_df["close"].to_numpy(dtype=float)]
    )
    expected = full[len(train_df) - 1 : -1]
    np.testing.assert_allclose(
        baseline_predictions["predicted_persistence"].to_numpy(dtype=float), expected
    )
    # The first forecast must be the last in-sample close, not the first test close.
    assert baseline_predictions["predicted_persistence"].iloc[0] == pytest.approx(
        train_df["close"].iloc[-1]
    )


def test_seasonal_and_moving_average_use_only_past(processed, baseline_predictions):
    train_df, test_df, _ = processed
    full = np.concatenate(
        [train_df["close"].to_numpy(dtype=float), test_df["close"].to_numpy(dtype=float)]
    )
    n_train = len(train_df)
    for offset in (0, 1, 100, len(test_df) - 1):
        position = n_train + offset
        assert baseline_predictions["predicted_seasonal_naive_7"].iloc[offset] == pytest.approx(
            full[position - 7]
        )
        assert baseline_predictions["predicted_moving_average_7"].iloc[offset] == pytest.approx(
            full[position - 7 : position].mean()
        )


def test_drift_uses_in_sample_mean_difference(processed, baseline_predictions):
    train_df, test_df, _ = processed
    full = np.concatenate(
        [train_df["close"].to_numpy(dtype=float), test_df["close"].to_numpy(dtype=float)]
    )
    drift = float(np.mean(np.diff(train_df["close"].to_numpy(dtype=float))))
    n_train = len(train_df)
    assert baseline_predictions["predicted_drift"].iloc[0] == pytest.approx(
        full[n_train - 1] + drift
    )


def test_baseline_metrics_match_recomputation(processed, baseline_predictions):
    train_df, test_df, _ = processed
    payload = evaluate_baselines(
        baseline_predictions,
        run_id="unit_test",
        train_df=train_df,
        test_df=test_df,
        bootstrap=False,
    )
    for name, entry in payload["baselines"].items():
        column = entry["prediction_column"]
        actual = baseline_predictions["actual_close"].to_numpy(dtype=float)
        predicted = baseline_predictions[column].to_numpy(dtype=float)
        assert entry["metrics"]["RMSE"] == pytest.approx(
            np.sqrt(np.mean((actual - predicted) ** 2)), abs=0.01
        )
        assert entry["metrics"]["MAE"] == pytest.approx(
            np.mean(np.abs(actual - predicted)), abs=0.01
        )
    assert payload["best_baseline"] in payload["baselines"]
