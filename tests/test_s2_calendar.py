"""Synthetic calendar-gap contracts for Study 2 baselines."""

import numpy as np
import pandas as pd
import pytest

import s2_final_run as final_run
import s2_models as sm


def test_persistence_skips_target_when_prior_observation_crosses_gap():
    dates = pd.date_range("2024-01-01", periods=5, freq="D").delete(2).to_numpy()
    values = np.arange(len(dates), dtype=float)

    target_dates, predictions = final_run.persistence_predictions(dates, values)

    assert list(pd.to_datetime(target_dates)) == [pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-05")]
    assert predictions.tolist() == [0.0, 2.0]


def test_garch_daily_returns_restart_after_gap_without_multiday_return():
    dates = pd.date_range("2024-01-01", periods=6, freq="D").delete(2).to_numpy()
    closes = np.array([100.0, 101.0, 130.0, 131.0, 132.0])

    returns = sm.daily_log_returns_after_last_gap(dates, closes)

    assert returns.index.tolist() == [pd.Timestamp("2024-01-05"), pd.Timestamp("2024-01-06")]
    assert np.allclose(returns.to_numpy(), np.log(closes[-2:] / closes[-3:-1]))


def test_garch_returns_reject_invalid_closes():
    dates = pd.date_range("2024-01-01", periods=3, freq="D").to_numpy()

    with pytest.raises(ValueError, match="finite, positive, and aligned"):
        sm.daily_log_returns_after_last_gap(dates, np.array([1.0, 0.0, 2.0]))


def test_har_design_skips_windows_crossing_missing_calendar_day():
    dates = pd.date_range("2024-01-01", periods=55, freq="D").delete(30).to_numpy()
    values = np.linspace(-3.0, 2.0, len(dates))

    X, y = sm.har_design(values, dates)
    target_dates = pd.DatetimeIndex(dates)[22:]
    expected = []
    for t in range(21, len(values) - 1):
        span = pd.DatetimeIndex(dates)[t - 21 : t + 2]
        if len(span) == 23 and np.all(np.diff(span.values) == np.timedelta64(1, "D")):
            expected.append(pd.Timestamp(dates[t + 1]))

    assert X.shape == (len(y), 4)
    assert list(pd.to_datetime(expected)) == list(pd.to_datetime([
        d for d in target_dates if d in set(expected)
    ]))
    assert pd.Timestamp("2024-01-31") not in pd.to_datetime(expected)
    assert pd.Timestamp("2024-02-01") not in pd.to_datetime(expected)


def test_har_fit_predict_preserves_valid_target_date_alignment():
    dates = pd.date_range("2024-01-01", periods=60, freq="D").delete(30).to_numpy()
    values = np.sin(np.arange(len(dates), dtype=float) / 4.0)
    target_dates, predictions, _ = sm.har_fit_predict(values, dates, pd.Timestamp("2024-02-10"))

    assert len(target_dates) == len(predictions)
    assert np.isfinite(predictions).all()
    assert pd.Timestamp("2024-01-31") not in pd.to_datetime(target_dates)
    assert pd.Timestamp("2024-02-01") not in pd.to_datetime(target_dates)


def test_har_design_without_dates_retains_contiguous_behavior():
    values = np.linspace(-1.0, 1.0, 40)
    X, y = sm.har_design(values)
    assert X.shape == (len(values) - 22, 4)
    assert len(y) == len(values) - 22


def test_garch_forecasts_causal_to_future_gaps():
    rng = np.random.default_rng(42)
    dates_clean = pd.date_range("2023-08-01", "2024-02-28", freq="D")
    log_ret = rng.normal(0, 0.01, len(dates_clean))
    closes_clean = 100.0 * np.exp(np.cumsum(log_ret))

    df_fc_clean = sm.garch_forecasts(
        dates_clean.to_numpy(), closes_clean, "2024-01-01", "2024-01-31"
    )
    assert len(df_fc_clean) == 31

    # Extended dates with a calendar gap strictly after window_end (in March 2024)
    future_dates = pd.date_range("2024-03-01", "2024-04-15", freq="D").delete(10)
    dates_with_future_gap = dates_clean.append(future_dates)
    extra_ret = rng.normal(0, 0.01, len(future_dates))
    closes_with_gap = np.concatenate([closes_clean, closes_clean[-1] * np.exp(np.cumsum(extra_ret))])

    df_fc_with_gap = sm.garch_forecasts(
        dates_with_future_gap.to_numpy(), closes_with_gap, "2024-01-01", "2024-01-31"
    )

    assert len(df_fc_with_gap) == 31
    pd.testing.assert_series_equal(
        df_fc_clean.set_index("date")["log_var"],
        df_fc_with_gap.set_index("date")["log_var"],
    )

