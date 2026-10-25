"""Data contract, split integrity, and final-scaler leakage checks."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import config
from data_utils import load_raw_data, load_processed_data


@pytest.fixture(scope="module")
def raw_df():
    return load_raw_data()


def test_raw_row_count_and_period(raw_df):
    assert len(raw_df) == config.EXPECTED_RAW_ROWS
    assert raw_df["date"].min().strftime("%Y-%m-%d") == config.DATASET_START_DATE
    assert raw_df["date"].max().strftime("%Y-%m-%d") == config.DATASET_END_DATE


def test_dates_unique_continuous_and_no_nulls(raw_df):
    assert raw_df["date"].is_unique
    assert (raw_df["date"].diff().dropna() == pd.Timedelta(days=1)).all()
    assert int(raw_df[["open", "high", "low", "close", "volume"]].isna().sum().sum()) == 0


def test_ohlc_relations(raw_df):
    assert (raw_df["high"] >= raw_df[["open", "close", "low"]].max(axis=1)).all()
    assert (raw_df["low"] <= raw_df[["open", "close", "high"]].min(axis=1)).all()
    assert (raw_df[["open", "high", "low", "close"]] > 0).all().all()


def test_split_sizes_and_boundaries():
    train_df = pd.read_csv(config.TRAIN_PATH)
    test_df = pd.read_csv(config.TEST_PATH)
    assert len(train_df) == config.EXPECTED_TRAIN_ROWS
    assert len(test_df) == config.EXPECTED_TEST_ROWS
    assert train_df["date"].iloc[0] == config.DATASET_START_DATE
    assert test_df["date"].iloc[0] == config.TEST_START_DATE
    assert test_df["date"].iloc[-1] == config.TEST_END_DATE
    assert train_df["date"].iloc[-1] < test_df["date"].iloc[0]


def test_final_scaler_is_fit_on_train_only():
    train_df, test_df, scaler = load_processed_data()
    train_min = float(train_df["close"].min())
    train_max = float(train_df["close"].max())
    assert np.isclose(scaler.data_min_[0], train_min)
    assert np.isclose(scaler.data_max_[0], train_max)
    assert scaler.data_max_[0] < float(test_df["close"].max())
    assert len(train_df) == config.EXPECTED_TRAIN_ROWS
    assert len(test_df) == config.EXPECTED_TEST_ROWS
