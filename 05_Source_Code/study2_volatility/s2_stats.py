"""
s2_stats.py - Pre-registered uncertainty quantification for Study 2.

Implements protocol section 8 exactly:
- QLIKE on the log-variance scale:  mean(exp(e) - e - 1),  e = y - y_hat;
- Diebold-Mariano test on daily loss differences with Newey-West
  (Bartlett kernel, lag = DM_HAC_LAG = 5), one-sided (model better => mean(d)<0);
- moving-block bootstrap CI for the mean loss difference
  (block = 20 days, reps = 10,000, seed = 42).

All routines are deterministic for a given seed.
"""

from __future__ import annotations

import numpy as np

import s2_config as cfg


# ---------------------------------------------------------------------------
# Losses
# ---------------------------------------------------------------------------
def qlike_per_obs(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """QLIKE on log-variance scale, per observation (>=0, lower is better)."""
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    return np.exp(e) - e - 1.0


def qlike(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(qlike_per_obs(y_true, y_pred).mean())


def mae_rmse_logrv(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    return {"MAE_logRV": float(np.abs(e).mean()),
            "RMSE_logRV": float(np.sqrt((e ** 2).mean()))}


# ---------------------------------------------------------------------------
# Diebold-Mariano (Newey-West / Bartlett)
# ---------------------------------------------------------------------------
def dm_test(loss_diff: np.ndarray, lag: int = cfg.DM_HAC_LAG) -> dict[str, float]:
    """
    DM statistic for H1: mean(d) < 0 (model better than baseline).
    Returns the statistic, the one-sided p-value, and the mean difference.
    """
    d = np.asarray(loss_diff, float).reshape(-1)
    d = d[~np.isnan(d)]
    n = len(d)
    dbar = float(d.mean())
    dc = d - dbar
    gamma0 = float((dc ** 2).mean())
    var = gamma0
    for l in range(1, lag + 1):
        gamma_l = float((dc[l:] * dc[:-l]).mean())
        w = 1.0 - l / (lag + 1.0)          # Bartlett weight
        var += 2.0 * w * gamma_l
    var = max(var, 1e-24)
    dm = dbar / np.sqrt(var / n)
    from math import erf, sqrt

    p_one_sided = 0.5 * (1.0 + erf(dm / sqrt(2.0)))  # P(Z <= dm); better => small p
    return {"dm_stat": float(dm), "p_one_sided": float(p_one_sided),
            "mean_diff": dbar, "n": int(n)}


# ---------------------------------------------------------------------------
# Moving-block bootstrap
# ---------------------------------------------------------------------------
def moving_block_bootstrap_mean_ci(
    diff: np.ndarray,
    block: int = cfg.BOOTSTRAP_BLOCK,
    reps: int = cfg.BOOTSTRAP_REPS,
    seed: int = cfg.BOOTSTRAP_SEED,
    alpha: float = cfg.ALPHA,
) -> dict[str, float]:
    """Percentile CI for the mean of a daily loss-difference series."""
    d = np.asarray(diff, float).reshape(-1)
    d = d[~np.isnan(d)]
    n = len(d)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts_max = n - block
    means = np.empty(reps)
    for b in range(reps):
        starts = rng.integers(0, starts_max + 1, size=n_blocks)
        idx = (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:n]
        means[b] = d[idx].mean()
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    # one-sided bootstrap p-value for H1: mean < 0 (fraction of bootstrap means >= 0)
    p_one_sided = float((means >= 0.0).mean())
    return {"ci_low": float(lo), "ci_high": float(hi),
            "mean_diff": float(d.mean()), "p_boot_one_sided": p_one_sided,
            "n": int(n), "block": int(block), "reps": int(reps)}


def paired_loss_diff(
    dates_a: np.ndarray, loss_a: np.ndarray,
    dates_b: np.ndarray, loss_b: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Align two per-day loss series on their common dates; return (dates, a-b)."""
    da = pd_dates = np.asarray(dates_a)
    db = np.asarray(dates_b)
    common, ia, ib = np.intersect1d(da, db, return_indices=True)
    if len(common) == 0:
        raise ValueError("Tidak ada tanggal yang beririsan.")
    return common, np.asarray(loss_a, float)[ia] - np.asarray(loss_b, float)[ib]
