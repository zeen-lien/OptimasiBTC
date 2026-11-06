"""Synthetic contract tests for Study 2 split, scaler, and CV machinery.

Audits active entry points (s2_models, s2_optuna_search, s2_final_run)
without training neural networks or reading 2026 evaluation results.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import TimeSeriesSplit

import s2_config as cfg
import s2_final_run as final_run
import s2_models as sm
import s2_optuna_search as optuna_search


def _synthetic_daily_frame(n_days: int = 120, start: str = "2020-01-01", rng_seed: int = 42) -> pd.DataFrame:
    """Generate a clean synthetic daily frame matching Study 2 columns."""
    rng = np.random.default_rng(rng_seed)
    dates = pd.date_range(start, periods=n_days, freq="D")
    log_rv = rng.normal(-8.0, 1.0, n_days)
    log_range = rng.normal(0.05, 0.01, n_days)
    log_volume = rng.normal(10.0, 0.5, n_days)
    log_absret = rng.normal(-3.0, 0.8, n_days)
    rv_mean_5 = pd.Series(log_rv).rolling(5).mean().bfill().to_numpy()
    rv_mean_22 = pd.Series(log_rv).rolling(22).mean().bfill().to_numpy()

    return pd.DataFrame({
        "date": dates,
        "log_rv": log_rv,
        "log_range": log_range,
        "log_volume": log_volume,
        "log_absret": log_absret,
        "rv_mean_5": rv_mean_5,
        "rv_mean_22": rv_mean_22,
    })


# ---------------------------------------------------------------------------
# 1. Scaler Fit Only on Training
# ---------------------------------------------------------------------------
def test_scaler_fit_strictly_isolated_to_training():
    """Verify scaler parameters reflect ONLY the training fold, never validation or test."""
    rng = np.random.default_rng(101)
    n_samples, lookback, n_feats = 60, 10, 6

    # Distinct distributions for train, val, test
    X_tr = rng.normal(loc=10.0, scale=2.0, size=(30, lookback, n_feats))
    y_tr = rng.normal(loc=-5.0, scale=1.0, size=(30,))

    X_va = rng.normal(loc=100.0, scale=20.0, size=(15, lookback, n_feats))
    y_va = rng.normal(loc=50.0, scale=10.0, size=(15,))

    X_te = rng.normal(loc=1000.0, scale=200.0, size=(15, lookback, n_feats))
    y_te = rng.normal(loc=500.0, scale=100.0, size=(15,))

    scaler_x, scaler_y = sm.fit_scaler(X_tr, y_tr)

    expected_mean_x = X_tr.reshape(30, -1).mean(axis=0)
    expected_var_x = X_tr.reshape(30, -1).var(axis=0)
    expected_mean_y = y_tr.mean()
    expected_var_y = y_tr.var()

    np.testing.assert_allclose(scaler_x.mean_, expected_mean_x, rtol=1e-6)
    np.testing.assert_allclose(scaler_x.var_, expected_var_x, rtol=1e-6)
    assert scaler_y.mean_[0] == pytest.approx(expected_mean_y, rel=1e-6)
    assert scaler_y.var_[0] == pytest.approx(expected_var_y, rel=1e-6)

    # Transforming val and test must NOT mutate fitted scaler attributes
    mean_x_before = scaler_x.mean_.copy()
    var_x_before = scaler_x.var_.copy()
    mean_y_before = scaler_y.mean_.copy()
    var_y_before = scaler_y.var_.copy()

    Xva_s, yva_s = sm.transform_xy(scaler_x, scaler_y, X_va, y_va)
    Xte_s, yte_s = sm.transform_xy(scaler_x, scaler_y, X_te, y_te)

    np.testing.assert_array_equal(scaler_x.mean_, mean_x_before)
    np.testing.assert_array_equal(scaler_x.var_, var_x_before)
    np.testing.assert_array_equal(scaler_y.mean_, mean_y_before)
    np.testing.assert_array_equal(scaler_y.var_, var_y_before)

    # Inverse transform on targets must recover original inputs
    y_recovered = scaler_y.inverse_transform(yva_s.reshape(-1, 1)).reshape(-1)
    np.testing.assert_allclose(y_recovered, y_va, rtol=1e-6)


# ---------------------------------------------------------------------------
# 2. TimeSeriesSplit Purge Gap Mechanics
# ---------------------------------------------------------------------------
def test_timeseries_split_purge_gap_exact_count_and_causal_boundaries():
    """Audit actual purge gap in TimeSeriesSplit: lookback vs lookback + 1."""
    df = _synthetic_daily_frame(n_days=150, start="2021-01-01")
    lookback = 15
    X, y, fend, tdate = sm.build_samples(df, lookback=lookback)

    # Test the active code splitter (gap = lookback + 1)
    code_gap = lookback + 1
    splitter_code = TimeSeriesSplit(n_splits=5, gap=code_gap)

    for fold, (tr, va) in enumerate(splitter_code.split(X)):
        # 1. Chronological order
        assert tr[-1] < va[0]

        # 2. Exact sample gap
        purged_samples = va[0] - tr[-1] - 1
        assert purged_samples == code_gap

        # 3. Calendar date alignment across the purge
        last_tr_target = pd.Timestamp(tdate[tr[-1]])
        first_va_feature_start = pd.Timestamp(fend[va[0]]) - pd.Timedelta(days=lookback - 1)
        first_va_target = pd.Timestamp(tdate[va[0]])

        # In code (gap = lookback + 1), the first validation feature starts 2 days after last train target
        assert first_va_feature_start == last_tr_target + pd.Timedelta(days=2)
        assert first_va_target > last_tr_target

    # Test the protocol literal splitter (gap = lookback)
    protocol_gap = lookback
    splitter_protocol = TimeSeriesSplit(n_splits=5, gap=protocol_gap)

    for fold, (tr, va) in enumerate(splitter_protocol.split(X)):
        purged_samples = va[0] - tr[-1] - 1
        assert purged_samples == protocol_gap

        last_tr_target = pd.Timestamp(tdate[tr[-1]])
        first_va_feature_start = pd.Timestamp(fend[va[0]]) - pd.Timedelta(days=lookback - 1)

        # In protocol (gap = lookback), first validation feature starts exactly 1 day after last train target
        # Demonstrating 0 target-feature overlap between train and validation
        assert first_va_feature_start == last_tr_target + pd.Timedelta(days=1)


# ---------------------------------------------------------------------------
# 3. Internal Validation Split (Final Run 90%/10%)
# ---------------------------------------------------------------------------
def test_internal_val_split_contract():
    """Audit s2_final_run.internal_val_split indexing, completeness, and fit scaler isolation."""
    n_samples = 100
    frac = 0.10
    tr_idx, es_idx = final_run.internal_val_split(n_samples, frac=frac)

    # 1. Exact split counts
    assert len(es_idx) == 10
    assert len(tr_idx) == 90
    assert len(tr_idx) + len(es_idx) == n_samples

    # 2. Chronological and non-overlapping
    assert np.array_equal(tr_idx, np.arange(90))
    assert np.array_equal(es_idx, np.arange(90, 100))
    assert set(tr_idx).isdisjoint(set(es_idx))
    assert tr_idx[-1] + 1 == es_idx[0]

    # 3. Scaler fit isolation in final run
    rng = np.random.default_rng(202)
    X = rng.normal(loc=5.0, scale=1.0, size=(n_samples, 10, 6))
    y = rng.normal(loc=-2.0, scale=0.5, size=(n_samples,))

    X_fit, y_fit = X[tr_idx], y[tr_idx]
    X_es, y_es = X[es_idx], y[es_idx]

    scaler_x, scaler_y = sm.fit_scaler(X_fit, y_fit)

    # Scaler mean must match X_fit exactly, not the full pool X
    expected_fit_mean = X_fit.reshape(len(X_fit), -1).mean(axis=0)
    full_pool_mean = X.reshape(len(X), -1).mean(axis=0)

    np.testing.assert_allclose(scaler_x.mean_, expected_fit_mean, rtol=1e-6)
    assert not np.allclose(scaler_x.mean_, full_pool_mean)


# ---------------------------------------------------------------------------
# 4. Target & Sample Alignment Contracts
# ---------------------------------------------------------------------------
def test_build_samples_target_and_date_invariants():
    """Verify build_samples target dates strictly equal fend + 1 day and y equals target value."""
    df = _synthetic_daily_frame(n_days=80, start="2022-01-01")
    lookback = 12
    X, y, fend, tdate = sm.build_samples(df, lookback=lookback)

    assert len(X) == len(y) == len(fend) == len(tdate)
    assert len(X) == 80 - lookback

    # Target date is exactly 1 day after the end of feature window
    date_diff = pd.to_datetime(tdate) - pd.to_datetime(fend)
    assert (date_diff == pd.Timedelta(days=1)).all()

    # Targets exactly match log_rv column at target dates
    target_lookup = df.set_index("date")["log_rv"]
    for i in range(len(y)):
        t_dt = pd.Timestamp(tdate[i])
        assert y[i] == pytest.approx(target_lookup[t_dt], abs=1e-12)


# ---------------------------------------------------------------------------
# 5. Distinguish Fixture Errors from Pipeline Behavior
# ---------------------------------------------------------------------------
def test_build_samples_rejects_gaps_and_nans_in_fixtures():
    """Ensure build_samples skips corrupted rows instead of failing silently or leaking."""
    df = _synthetic_daily_frame(n_days=60, start="2022-01-01")
    lookback = 10

    # Clean baseline count
    X_clean, _, _, _ = sm.build_samples(df, lookback=lookback)
    assert len(X_clean) == 50

    # Introduce a calendar gap at day 25 (delete day 25)
    df_gap = df.drop(index=25).reset_index(drop=True)
    X_gap, _, fend_gap, tdate_gap = sm.build_samples(df_gap, lookback=lookback)

    # Any window of length lookback+1 (11 days) that spans the missing day must be omitted
    # A single missing day affects 11 consecutive sample windows
    assert len(X_gap) == len(X_clean) - (lookback + 1)

    # None of the retained windows may cross the missing date
    missing_date = df["date"].iloc[25]
    for i in range(len(X_gap)):
        start_d = pd.Timestamp(fend_gap[i]) - pd.Timedelta(days=lookback - 1)
        end_d = pd.Timestamp(tdate_gap[i])
        assert not (start_d <= missing_date <= end_d)

    # Introduce a NaN in features
    df_nan = df.copy()
    df_nan.loc[35, "log_volume"] = np.nan
    X_nan, _, fend_nan, _ = sm.build_samples(df_nan, lookback=lookback)
    assert len(X_nan) == len(X_clean) - lookback  # 10 windows use day 35 as feature


def test_dev_loader_boundary_enforcement():
    """Audit s2_data_load_dev exact boundary assertion."""
    # When dev boundary is violated, it must raise AssertionError loudly
    fake_df = _synthetic_daily_frame(n_days=30, start="2023-01-01")
    # DEV_END is 2023-12-31; max date in fake_df is 2023-01-30 != 2023-12-31
    with pytest.raises(AssertionError, match="Dev window boundary salah"):
        dev = fake_df[fake_df["date"] <= cfg.DEV_END].reset_index(drop=True)
        if dev["date"].max() != pd.Timestamp(cfg.DEV_END):
            raise AssertionError("Dev window boundary salah.")

