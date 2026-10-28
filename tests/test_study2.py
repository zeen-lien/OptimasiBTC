"""Study 2 unit tests: samples, stats, HAR, data freeze integrity.

These tests never train a model and never read the 2026 predictions; they
verify the frozen data artifacts and the deterministic machinery.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import s2_config as cfg
import s2_models as sm
from s2_stats import (
    dm_test,
    mae_rmse_logrv,
    moving_block_bootstrap_mean_ci,
    paired_loss_diff,
    qlike,
    qlike_per_obs,
)


@pytest.fixture(scope="module")
def daily():
    import s2_data as sd
    return sd.load_daily()


# ---------------------------------------------------------------------------
# Frozen data
# ---------------------------------------------------------------------------
def test_data_freeze_hashes_match():
    import s2_data as sd
    payload = __import__("json").loads(cfg.S2_DATA_FREEZE_HASH.read_text())
    assert cfg.sha256_file(cfg.S2_DAILY_CSV) == payload["daily_csv_sha256"]
    assert cfg.protocol_hash() == payload["protocol_sha256"]
    assert cfg.protocol_hash() == cfg.PROTOCOL_HASH_PATH.read_text().strip()


def test_daily_shape_and_boundaries(daily):
    assert len(daily) == cfg.EXPECTED_TOTAL_DAYS
    assert daily["date"].iloc[0] == pd.Timestamp(cfg.DATA_START)
    assert daily["date"].iloc[-1] == pd.Timestamp(cfg.DATA_END)
    assert "2020-02-19" not in daily["date"].dt.strftime("%Y-%m-%d").values


def test_val_test_windows_complete_24_bars(daily):
    vt = daily[daily["date"] >= cfg.VAL_START]
    assert (vt["n_bars"] == 24).all()


def test_rv_positive_and_logrv_finite(daily):
    assert (daily["rv"] > 0).all()
    assert np.isfinite(daily["log_rv"]).all()


def test_features_no_future_leakage(daily):
    """rv_mean_5/22 must equal trailing means of log_rv (causal)."""
    lr = daily["log_rv"]
    assert np.allclose(daily["rv_mean_5"][4:], lr.rolling(5).mean()[4:])
    assert np.allclose(daily["rv_mean_22"][21:], lr.rolling(22).mean()[21:])


# ---------------------------------------------------------------------------
# Samples
# ---------------------------------------------------------------------------
def test_build_samples_alignment(daily):
    X, y, fend, tdate = sm.build_samples(daily, lookback=10)
    assert X.shape == (len(y), 10, 6)
    # target day must be the day after the last feature day
    assert (pd.to_datetime(tdate) - pd.to_datetime(fend) == pd.Timedelta(days=1)).all()
    # y equals log_rv on the target date
    lookup = daily.set_index(daily["date"].dt.strftime("%Y-%m-%d"))["log_rv"]
    for i in (0, len(y) // 2, len(y) - 1):
        key = pd.Timestamp(tdate[i]).strftime("%Y-%m-%d")
        assert abs(y[i] - lookup[key]) < 1e-10


def test_build_samples_exclude_gap_windows(daily):
    X, y, fend, tdate = sm.build_samples(daily, lookback=10)
    fd = pd.to_datetime(fend)
    td = pd.to_datetime(tdate)
    # windows ending 2020-02-18 (target 02-19, dropped day) must not exist
    assert not (fd == pd.Timestamp("2020-02-18")).any()
    # windows spanning the gap must not exist -> no target 2020-02-20 either
    assert not (td == pd.Timestamp("2020-02-20")).any()


def test_build_samples_no_nan(daily):
    for lb in (10, 21, 30):
        X, y, _, _ = sm.build_samples(daily, lookback=lb)
        assert np.isfinite(X).all()
        assert np.isfinite(y).all()


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
def test_qlike_zero_at_perfect_and_nonnegative():
    y = np.array([-8.0, -7.5, -6.2])
    assert qlike(y, y) == pytest.approx(0.0, abs=1e-12)
    assert (qlike_per_obs(y, y + 0.3) >= 0).all()
    assert (qlike_per_obs(y, y - 0.3) >= 0).all()


def test_qlike_asymmetric_penalty():
    y = np.zeros(5)
    under = qlike_per_obs(y, np.full(5, -1.0)).mean()   # predict too low variance
    over = qlike_per_obs(y, np.full(5, 1.0)).mean()
    assert under > over  # under-prediction penalized more


def test_dm_test_sign_and_p(daily):
    rng = np.random.default_rng(0)
    n = 273
    d = rng.normal(-0.05, 0.3, n)
    res = dm_test(d)
    assert res["dm_stat"] < 0
    assert res["p_one_sided"] < 0.5
    res2 = dm_test(-d)
    assert res2["p_one_sided"] > 0.5


def test_bootstrap_ci_contains_mean_and_p_direction():
    rng = np.random.default_rng(1)
    d = rng.normal(-0.04, 0.25, 273)
    res = moving_block_bootstrap_mean_ci(d)
    assert res["ci_low"] <= res["mean_diff"] <= res["ci_high"]
    assert res["p_boot_one_sided"] < 0.5


def test_paired_loss_diff_alignment():
    dates_a = np.array([0, 1, 2, 3])
    dates_b = np.array([1, 2, 3, 4])
    la = np.array([0.1, 0.2, 0.3, 0.4])
    lb = np.array([0.05, 0.15, 0.25, 0.35])
    common, d = paired_loss_diff(dates_a, la, dates_b, lb)
    assert common.tolist() == [1, 2, 3]
    assert np.allclose(d, [0.15, 0.15, 0.15])


# ---------------------------------------------------------------------------
# HAR design
# ---------------------------------------------------------------------------
def test_har_design_shapes(daily):
    lr = daily["log_rv"].to_numpy()
    X, y = sm.har_design(lr)
    assert X.shape == (len(lr) - 22, 4)
    assert y.shape == (len(lr) - 22,)
    assert np.isfinite(X).all()


def test_har_beta_plausible(daily):
    lr = daily["log_rv"].to_numpy()
    dates = daily["date"].to_numpy()
    td, preds, beta = sm.har_fit_predict(lr, dates, np.datetime64(cfg.DEV_END))
    assert len(td) == len(preds)
    assert np.isfinite(preds).all()
    # daily coefficient positive (volatility persistence)
    assert beta[1] > 0
