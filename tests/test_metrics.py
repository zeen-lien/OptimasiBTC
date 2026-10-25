"""Recompute metrics from prediction CSVs and compare with the saved JSON."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

import config


@pytest.mark.parametrize("tier", [1, 2, 3])
def test_metrics_match_predictions(tier):
    metrics_path = config.LEGACY_METRICS_DIR / f"metrics_tier{tier}.json"
    predictions_path = config.RESULTS_ROOT / f"predictions_tier{tier}.csv"
    assert metrics_path.exists(), metrics_path
    assert predictions_path.exists(), predictions_path

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))["metrics"]
    frame = pd.read_csv(predictions_path)
    assert len(frame) == config.EXPECTED_TEST_ROWS

    actual = frame["actual_close"].to_numpy(dtype=float)
    predicted = frame[f"predicted_close_tier{tier}"].to_numpy(dtype=float)
    recomputed = {
        "RMSE": float(np.sqrt(np.mean((actual - predicted) ** 2))),
        "MAE": float(np.mean(np.abs(actual - predicted))),
        "MAPE": float(np.mean(np.abs((actual - predicted) / actual)) * 100.0),
    }
    for key, value in recomputed.items():
        assert metrics[key] == pytest.approx(value, abs=0.02), key

    np.testing.assert_allclose(frame["error"], actual - predicted, atol=0.02)
    np.testing.assert_allclose(
        frame["abs_pct_error"], np.abs((actual - predicted) / actual) * 100.0, atol=0.02
    )


def test_prediction_dates_are_identical_across_tiers():
    dates = []
    for tier in (1, 2, 3):
        frame = pd.read_csv(config.RESULTS_ROOT / f"predictions_tier{tier}.csv")
        dates.append(pd.to_datetime(frame["date"]))
    assert dates[0].equals(dates[1])
    assert dates[0].equals(dates[2])
    assert dates[0].iloc[0].strftime("%Y-%m-%d") == config.TEST_START_DATE
    assert dates[0].iloc[-1].strftime("%Y-%m-%d") == config.TEST_END_DATE
