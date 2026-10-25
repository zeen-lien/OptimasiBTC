"""Residual, directional, and ex-ante market-context helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis_utils import (
    directional_accuracy,
    improvement_percent,
    market_context,
    metrics_for_mask,
    regime_summary,
    residual_statistics,
    worst_cases,
)


def test_improvement_percent_sign_and_zero_baseline():
    assert improvement_percent(100.0, 80.0) == pytest.approx(20.0)
    assert improvement_percent(100.0, 120.0) == pytest.approx(-20.0)
    assert np.isnan(improvement_percent(0.0, 10.0))


def test_residual_statistics_are_consistent_with_errors():
    actual = np.array([100.0, 110.0, 90.0, 120.0])
    predicted = np.array([95.0, 115.0, 95.0, 118.0])
    stats = residual_statistics(actual, predicted)
    assert stats["n"] == 4
    assert stats["mean"] == pytest.approx(np.mean(actual - predicted))
    assert stats["mae"] == pytest.approx(np.mean(np.abs(actual - predicted)))
    assert stats["max_absolute_error"] == pytest.approx(5.0)
    assert stats["share_within_5_percent"] == pytest.approx(0.75)
    assert stats["q05"] <= stats["median"] <= stats["q95"]


def test_directional_accuracy_uses_previous_close():
    previous = np.array([100.0, 100.0, 100.0])
    actual = np.array([101.0, 99.0, 100.0])
    predicted = np.array([100.5, 100.5, 100.0])
    result = directional_accuracy(actual, predicted, previous)
    # Up call is correct, down call is wrong, flat actual day is excluded.
    assert result["n"] == 2
    assert result["accuracy"] == pytest.approx(0.5)
    assert result["correct"] == 1


def test_directional_accuracy_flat_predictions_are_counted():
    previous = np.array([100.0, 100.0])
    actual = np.array([101.0, 99.0])
    predicted = np.array([100.0, 100.0])
    result = directional_accuracy(actual, predicted, previous)
    assert result["accuracy"] == pytest.approx(0.0)
    assert result["predicted_flat_share"] == pytest.approx(1.0)


def test_worst_cases_are_sorted_by_absolute_error():
    dates = pd.date_range("2025-01-01", periods=4)
    actual = np.array([100.0, 100.0, 100.0, 100.0])
    predicted = np.array([99.0, 90.0, 100.5, 97.0])
    cases = worst_cases(dates, actual, predicted, n=3)
    assert [case["date"] for case in cases] == ["2025-01-02", "2025-01-04", "2025-01-01"]
    assert cases[0]["absolute_error"] == pytest.approx(10.0)


def test_market_context_is_ex_ante_and_deterministic():
    rng = np.random.default_rng(11)
    train_close = 30_000 * np.exp(np.cumsum(rng.normal(0.001, 0.02, 300)))
    test_close = train_close[-1] * np.exp(np.cumsum(rng.normal(0.0, 0.02, 50)))
    dates = pd.date_range("2025-01-01", periods=50)
    context = market_context(train_close, test_close, dates)

    assert len(context) == 50
    assert set(context["regime"]).issubset({"bull", "bear", "sideways"})
    assert context["high_volatility"].dtype == bool
    assert context.attrs["volatility_threshold"] > 0

    # Changing future test prices must not change the first day's ex-ante label.
    altered = test_close.copy()
    altered[1:] *= 1.5
    altered_context = market_context(train_close, altered, dates)
    assert altered_context.loc[0, "regime"] == context.loc[0, "regime"]
    assert altered_context.loc[0, "trailing_return_30d"] == pytest.approx(
        context.loc[0, "trailing_return_30d"]
    )


def test_regime_summary_returns_none_for_tiny_group():
    context = pd.DataFrame({"regime": ["bull"] * 5 + ["bear"] * 5 + ["sideways"] * 1})
    actual = np.linspace(100, 120, 11)
    predicted = actual + 1.0
    summary = regime_summary(context, actual, predicted)
    assert summary["bull"]["n"] == 5
    assert summary["sideways"] is None
    assert metrics_for_mask(actual, predicted, np.ones(11, dtype=bool))["n"] == 11
