"""Bootstrap uncertainty and multi-seed aggregation checks."""

from __future__ import annotations

import numpy as np
import pytest

from stats_utils import (
    aggregate_seed_metrics,
    bootstrap_metric_ci,
    moving_block_indices,
    paired_bootstrap_difference,
)


@pytest.fixture(scope="module")
def sample_errors():
    rng = np.random.default_rng(7)
    y_true = 40_000 + np.cumsum(rng.normal(0, 500, 200))
    y_pred = y_true + rng.normal(0, 900, 200)
    return y_true, y_pred


def test_moving_block_indices_have_requested_length_and_valid_range():
    rng = np.random.default_rng(1)
    indices = moving_block_indices(437, block_size=10, rng=rng)
    assert len(indices) == 437
    assert indices.min() >= 0
    assert indices.max() < 437


def test_bootstrap_ci_is_deterministic_and_brackets_estimate(sample_errors):
    y_true, y_pred = sample_errors
    first = bootstrap_metric_ci(y_true, y_pred, n_resamples=300, seed=11)
    second = bootstrap_metric_ci(y_true, y_pred, n_resamples=300, seed=11)
    assert first == second
    for metric in ("RMSE", "MAE", "MAPE"):
        entry = first[metric]
        assert entry["ci_low"] <= entry["estimate"] <= entry["ci_high"]


def test_bootstrap_ci_rejects_invalid_arguments(sample_errors):
    y_true, y_pred = sample_errors
    with pytest.raises(ValueError):
        bootstrap_metric_ci(y_true, y_pred, n_resamples=10)
    with pytest.raises(ValueError):
        bootstrap_metric_ci(y_true[:-1], y_pred, n_resamples=200)
    with pytest.raises(ValueError):
        bootstrap_metric_ci(y_true, y_pred, metrics=("MSE",), n_resamples=200)


def test_paired_bootstrap_identical_predictions_show_no_difference(sample_errors):
    y_true, y_pred = sample_errors
    result = paired_bootstrap_difference(y_true, y_pred, y_pred, n_resamples=300)
    assert result["difference_b_minus_a"] == pytest.approx(0.0)
    assert result["ci_low"] == pytest.approx(0.0)
    assert result["ci_high"] == pytest.approx(0.0)
    assert result["p_value"] == pytest.approx(1.0)


def test_paired_bootstrap_detects_clearly_worse_model(sample_errors):
    y_true, y_pred = sample_errors
    worse = y_pred + 5_000.0
    result = paired_bootstrap_difference(y_true, y_pred, worse, n_resamples=500, seed=3)
    assert result["difference_b_minus_a"] > 0
    assert result["ci_low"] > 0
    assert result["p_value"] < 0.05


def test_aggregate_seed_metrics_mean_and_std():
    per_seed = {
        "42": {"RMSE": 100.0, "MAE": 80.0, "MAPE": 2.0},
        "123": {"RMSE": 120.0, "MAE": 90.0, "MAPE": 2.4},
    }
    summary = aggregate_seed_metrics(per_seed)
    assert summary["RMSE"]["mean"] == pytest.approx(110.0)
    assert summary["RMSE"]["std"] == pytest.approx(np.sqrt(200.0))
    assert summary["MAPE"]["mean"] == pytest.approx(2.2)
    assert summary["MAE"]["n_seeds"] == 2
