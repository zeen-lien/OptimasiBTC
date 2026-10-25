"""
analysis_utils.py - Pure helpers for post-hoc error analysis.

These functions do not train models. They operate on aligned actual/predicted
arrays and are unit-tested independently of the pipeline so the residual and
regime analysis cannot silently drift from the thesis definitions.

Market context labels are deliberately ex-ante: the regime of day ``t`` uses
the trailing 30-day return ending at ``t-1``, and volatility of day ``t`` uses
the last 7 daily log returns ending at ``t-1``. This avoids labelling a day
with information that was not available before its forecast.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from experiment_utils import compute_metrics


def improvement_percent(baseline: float, candidate: float) -> float:
    """Percentage reduction of ``candidate`` relative to ``baseline``.

    Positive values mean the candidate has a lower error.
    """
    baseline = float(baseline)
    candidate = float(candidate)
    if baseline == 0:
        return float("nan")
    return (baseline - candidate) / baseline * 100.0


def residual_statistics(actual, predicted) -> dict:
    """Distribution summary of ``actual - predicted`` residuals."""
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    if len(actual) != len(predicted):
        raise ValueError("Panjang actual dan predicted harus sama")
    if len(actual) < 2:
        raise ValueError("Butuh minimal 2 observasi")
    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("actual/predicted mengandung NaN atau inf")

    residuals = actual - predicted
    std = float(np.std(residuals, ddof=0))
    if std > 0:
        skewness = float(np.mean((residuals - residuals.mean()) ** 3) / std**3)
        excess_kurtosis = float(np.mean((residuals - residuals.mean()) ** 4) / std**4 - 3.0)
    else:
        skewness = 0.0
        excess_kurtosis = 0.0

    quantiles = np.quantile(residuals, [0.05, 0.25, 0.50, 0.75, 0.95])
    absolute = np.abs(residuals)
    safe_actual = np.where(np.abs(actual) > 0, np.abs(actual), np.nan)
    percentage = np.abs(residuals) / safe_actual
    metrics = compute_metrics(actual, predicted)
    return {
        "n": int(len(residuals)),
        "mean": float(residuals.mean()),
        "std": std,
        "min": float(residuals.min()),
        "max": float(residuals.max()),
        "q05": float(quantiles[0]),
        "q25": float(quantiles[1]),
        "median": float(quantiles[2]),
        "q75": float(quantiles[3]),
        "q95": float(quantiles[4]),
        "skewness": skewness,
        "excess_kurtosis": excess_kurtosis,
        "mae": float(metrics["MAE"]),
        "rmse": float(metrics["RMSE"]),
        "mean_absolute_error": float(absolute.mean()),
        "max_absolute_error": float(absolute.max()),
        "share_within_1_percent": float(np.nanmean(percentage <= 0.01)),
        "share_within_2_percent": float(np.nanmean(percentage <= 0.02)),
        "share_within_5_percent": float(np.nanmean(percentage <= 0.05)),
    }


def directional_accuracy(actual, predicted, previous_close) -> dict:
    """One-step direction accuracy relative to the previous actual close."""
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    previous_close = np.asarray(previous_close, dtype=float).reshape(-1)
    if not (len(actual) == len(predicted) == len(previous_close)):
        raise ValueError("actual, predicted, previous_close harus sama panjang")
    if len(actual) < 2:
        raise ValueError("Butuh minimal 2 observasi")

    actual_direction = np.sign(actual - previous_close)
    predicted_direction = np.sign(predicted - previous_close)
    non_flat = actual_direction != 0
    if not non_flat.any():
        return {
            "accuracy": None,
            "n": 0,
            "correct": 0,
            "up_accuracy": None,
            "down_accuracy": None,
            "predicted_flat_share": float(np.mean(predicted_direction == 0)),
        }

    actual_direction = actual_direction[non_flat]
    predicted_direction = predicted_direction[non_flat]
    correct = predicted_direction == actual_direction
    up = actual_direction > 0
    down = actual_direction < 0
    return {
        "accuracy": float(correct.mean()),
        "n": int(non_flat.sum()),
        "correct": int(correct.sum()),
        "up_accuracy": float(correct[up].mean()) if up.any() else None,
        "down_accuracy": float(correct[down].mean()) if down.any() else None,
        "predicted_flat_share": float(np.mean(predicted_direction == 0)),
        "n_up": int(up.sum()),
        "n_down": int(down.sum()),
    }


def market_context(
    train_close,
    test_close,
    test_dates: Sequence,
    regime_lookback: int = 30,
    bull_threshold: float = 0.05,
    bear_threshold: float = -0.05,
    vol_window: int = 7,
    vol_quantile: float = 0.75,
) -> pd.DataFrame:
    """Ex-ante regime and volatility labels for every holdout day.

    - Regime: trailing ``regime_lookback``-day return ending at ``t-1``.
    - High volatility: rolling ``vol_window``-day standard deviation of daily
      log returns ending at ``t-1``, using the in-sample 75th percentile as the
      threshold.
    """
    train_close = np.asarray(train_close, dtype=float).reshape(-1)
    test_close = np.asarray(test_close, dtype=float).reshape(-1)
    dates = pd.to_datetime(pd.Series(test_dates)).dt.strftime("%Y-%m-%d").to_numpy()
    if len(test_close) != len(dates):
        raise ValueError("test_close dan test_dates harus sama panjang")
    if len(train_close) <= regime_lookback + 1:
        raise ValueError("In-sample terlalu pendek untuk regime lookback")
    if vol_window < 2:
        raise ValueError("vol_window minimal 2")

    combined = np.concatenate([train_close, test_close])
    log_returns = np.diff(np.log(combined))
    n_train = len(train_close)
    positions = np.arange(n_train, len(combined))

    if positions[0] - regime_lookback < 0:
        raise ValueError("In-sample tidak cukup untuk regime lookback")

    train_vol = np.array(
        [
            np.std(log_returns[position - vol_window : position], ddof=1)
            for position in range(vol_window, n_train)
        ],
        dtype=float,
    )
    if len(train_vol) < 10:
        raise ValueError("In-sample terlalu pendek untuk volatility window")
    threshold = float(np.quantile(train_vol, vol_quantile))

    rows = []
    for position, date in zip(positions, dates, strict=True):
        trailing_return = float(
            combined[position - 1] / combined[position - 1 - regime_lookback] - 1.0
        )
        if trailing_return > bull_threshold:
            regime = "bull"
        elif trailing_return < bear_threshold:
            regime = "bear"
        else:
            regime = "sideways"
        volatility = float(
            np.std(log_returns[position - vol_window : position], ddof=1)
        )
        rows.append(
            {
                "date": date,
                "trailing_return_30d": trailing_return,
                "regime": regime,
                "volatility_7d": volatility,
                "high_volatility": volatility > threshold,
            }
        )
    frame = pd.DataFrame(rows)
    frame.attrs["volatility_threshold"] = threshold
    frame.attrs["regime_lookback"] = int(regime_lookback)
    frame.attrs["bull_threshold"] = float(bull_threshold)
    frame.attrs["bear_threshold"] = float(bear_threshold)
    return frame


def metrics_for_mask(actual, predicted, mask) -> dict | None:
    """Metric subset for a boolean mask, or ``None`` when too few rows."""
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    mask = np.asarray(mask, dtype=bool).reshape(-1)
    if len(mask) != len(actual):
        raise ValueError("Mask harus sepanjang actual")
    if int(mask.sum()) < 2:
        return None
    metrics = compute_metrics(actual[mask], predicted[mask])
    return {"n": int(mask.sum()), **{key: float(value) for key, value in metrics.items()}}


def worst_cases(dates, actual, predicted, n: int = 5) -> list[dict]:
    """Largest absolute errors with date and signed error."""
    dates = pd.to_datetime(pd.Series(dates)).dt.strftime("%Y-%m-%d").to_numpy()
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    if not (len(dates) == len(actual) == len(predicted)):
        raise ValueError("dates, actual, predicted harus sama panjang")
    order = np.argsort(np.abs(actual - predicted))[::-1][: int(n)]
    return [
        {
            "date": str(dates[index]),
            "actual": float(actual[index]),
            "predicted": float(predicted[index]),
            "error": float(actual[index] - predicted[index]),
            "absolute_error": float(abs(actual[index] - predicted[index])),
            "absolute_percentage_error": float(
                abs(actual[index] - predicted[index]) / abs(actual[index]) * 100.0
            )
            if actual[index] != 0
            else None,
        }
        for index in order
    ]


def regime_summary(
    context: pd.DataFrame,
    actual,
    predicted,
    regimes: Iterable[str] = ("bull", "bear", "sideways"),
) -> dict:
    """MAE/RMSE/MAPE per ex-ante regime."""
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    if len(context) != len(actual):
        raise ValueError("Konteks dan prediksi harus sama panjang")
    summary = {}
    for regime in regimes:
        mask = context["regime"].to_numpy() == regime
        summary[regime] = metrics_for_mask(actual, predicted, mask)
    return summary
