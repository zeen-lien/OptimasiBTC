"""
stats_utils.py - Uncertainty quantification for forecast errors.

The thesis compares tiers on a single 439-day holdout. A point estimate alone
cannot tell whether a difference is meaningful, so this module adds:

- moving-block bootstrap confidence intervals for RMSE/MAE/MAPE, which keep
  short-range serial dependence in the residuals;
- a paired bootstrap for the error difference between two models evaluated on
  the same dates;
- mean/std aggregation for multi-seed runs.

All routines are deterministic for a given seed.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)

METRIC_NAMES: tuple[str, ...] = ("RMSE", "MAE", "MAPE")

_METRIC_FUNCTIONS = {
    "RMSE": lambda y_true, y_pred: float(np.sqrt(mean_squared_error(y_true, y_pred))),
    "MAE": lambda y_true, y_pred: float(mean_absolute_error(y_true, y_pred)),
    "MAPE": lambda y_true, y_pred: float(
        mean_absolute_percentage_error(y_true, y_pred) * 100.0
    ),
}


def _as_arrays(y_true, y_pred) -> tuple[np.ndarray, np.ndarray]:
    true = np.asarray(y_true, dtype=float).reshape(-1)
    pred = np.asarray(y_pred, dtype=float).reshape(-1)
    if len(true) != len(pred):
        raise ValueError(f"Panjang y_true ({len(true)}) != y_pred ({len(pred)})")
    if len(true) < 2:
        raise ValueError("Butuh minimal 2 observasi untuk bootstrap")
    if not np.isfinite(true).all() or not np.isfinite(pred).all():
        raise ValueError("y_true/y_pred mengandung NaN atau inf")
    return true, pred


def moving_block_indices(
    n_samples: int,
    block_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Draw one moving-block bootstrap sample of row indices.

    Blocks are contiguous runs of length ``block_size`` drawn with replacement
    from all valid start positions. The concatenation is truncated to
    ``n_samples``.
    """
    if block_size < 1:
        raise ValueError("block_size harus >= 1")
    block_size = min(int(block_size), n_samples)
    n_blocks = int(np.ceil(n_samples / block_size))
    starts = rng.integers(0, n_samples - block_size + 1, size=n_blocks)
    indices = np.concatenate(
        [np.arange(start, start + block_size) for start in starts]
    )
    return indices[:n_samples]


def bootstrap_metric_ci(
    y_true,
    y_pred,
    metrics: Iterable[str] = METRIC_NAMES,
    n_resamples: int = 2000,
    confidence: float = 0.95,
    block_size: int = 7,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """
    Percentile moving-block bootstrap CI for each metric.

    Returns ``{metric: {estimate, ci_low, ci_high, std_error, n_resamples}}``.
    """
    if not 0 < confidence < 1:
        raise ValueError("confidence harus di antara 0 dan 1")
    if n_resamples < 100:
        raise ValueError("n_resamples minimal 100 agar CI stabil")

    true, pred = _as_arrays(y_true, y_pred)
    metric_names = tuple(metrics)
    unknown = set(metric_names).difference(_METRIC_FUNCTIONS)
    if unknown:
        raise ValueError(f"Metrik tidak dikenal: {sorted(unknown)}")

    estimates = {name: _METRIC_FUNCTIONS[name](true, pred) for name in metric_names}
    rng = np.random.default_rng(seed)
    samples = {name: np.empty(n_resamples, dtype=float) for name in metric_names}

    for index in range(n_resamples):
        row_idx = moving_block_indices(len(true), block_size, rng)
        sample_true = true[row_idx]
        sample_pred = pred[row_idx]
        for name in metric_names:
            samples[name][index] = _METRIC_FUNCTIONS[name](sample_true, sample_pred)

    alpha = (1.0 - confidence) / 2.0
    result: dict[str, dict[str, float]] = {}
    for name in metric_names:
        values = samples[name]
        result[name] = {
            "estimate": float(estimates[name]),
            "ci_low": float(np.quantile(values, alpha)),
            "ci_high": float(np.quantile(values, 1.0 - alpha)),
            "std_error": float(np.std(values, ddof=1)),
            "n_resamples": int(n_resamples),
            "block_size": int(min(block_size, len(true))),
            "confidence": float(confidence),
        }
    return result


def paired_bootstrap_difference(
    y_true,
    y_pred_a,
    y_pred_b,
    metric: str = "MAE",
    n_resamples: int = 2000,
    confidence: float = 0.95,
    block_size: int = 7,
    seed: int = 42,
) -> dict[str, float]:
    """
    Bootstrap CI for ``metric(b) - metric(a)`` on identical dates.

    Negative values mean model B has lower error than model A. ``p_value`` is
    the two-sided bootstrap sign probability, i.e. the share of resamples
    whose difference falls on the opposite side of zero, doubled. It is a
    descriptive stability measure, not a substitute for a formal test.
    """
    if metric not in _METRIC_FUNCTIONS:
        raise ValueError(f"Metrik tidak dikenal: {metric}")

    true, pred_a = _as_arrays(y_true, y_pred_a)
    _, pred_b = _as_arrays(y_true, y_pred_b)

    point_a = _METRIC_FUNCTIONS[metric](true, pred_a)
    point_b = _METRIC_FUNCTIONS[metric](true, pred_b)
    point_diff = point_b - point_a

    rng = np.random.default_rng(seed)
    diffs = np.empty(n_resamples, dtype=float)
    for index in range(n_resamples):
        row_idx = moving_block_indices(len(true), block_size, rng)
        sample_true = true[row_idx]
        diffs[index] = _METRIC_FUNCTIONS[metric](
            sample_true, pred_b[row_idx]
        ) - _METRIC_FUNCTIONS[metric](sample_true, pred_a[row_idx])

    alpha = (1.0 - confidence) / 2.0
    share_above = float(np.mean(diffs >= 0.0))
    share_below = float(np.mean(diffs <= 0.0))
    p_value = float(min(1.0, 2.0 * min(share_above, share_below)))
    return {
        "metric": metric,
        "estimate_a": float(point_a),
        "estimate_b": float(point_b),
        "difference_b_minus_a": float(point_diff),
        "relative_change_percent": float(
            (point_diff / point_a) * 100.0 if point_a != 0 else np.nan
        ),
        "ci_low": float(np.quantile(diffs, alpha)),
        "ci_high": float(np.quantile(diffs, 1.0 - alpha)),
        "p_value": p_value,
        "n_resamples": int(n_resamples),
        "block_size": int(min(block_size, len(true))),
        "confidence": float(confidence),
    }


def aggregate_seed_metrics(
    per_seed: Mapping[str, Mapping[str, float]],
    metrics: Sequence[str] = METRIC_NAMES,
) -> dict[str, dict[str, float]]:
    """
    Summarize ``{seed: {metric: value}}`` as mean/std/min/max per metric.

    Both plain (``"RMSE"``) and rounded JSON keys are accepted.
    """
    if not per_seed:
        raise ValueError("per_seed kosong")

    summary: dict[str, dict[str, float]] = {}
    for metric in metrics:
        values = np.array(
            [float(payload[metric]) for payload in per_seed.values()], dtype=float
        )
        summary[metric] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
            "min": float(values.min()),
            "max": float(values.max()),
            "n_seeds": int(len(values)),
        }
    return summary
