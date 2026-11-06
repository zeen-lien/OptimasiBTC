"""Kontrak alignment analyzer Study 2 tanpa membaca prediksi final."""

import pandas as pd
import pytest

import s2_analyze as analyze


def _frames():
    dates = pd.date_range("2025-01-01", periods=3, freq="D")
    optuna = pd.DataFrame({"date": dates, "y_true": [1.0, 2.0, 3.0], "y_hat_mean": [0.9, 1.9, 2.9]})
    untuned = pd.DataFrame({"date": dates, "y_true": [1.0, 2.0, 3.0], "y_hat_mean": [0.8, 1.8, 2.8]})
    baseline = pd.DataFrame({"date": dates, "y_true": [1.0, 2.0, 3.0], "persistence": [1.1, 2.1, 3.1], "har_rv": [1.2, 2.2, 3.2], "garch11": [1.3, 2.3, 3.3]})
    return optuna, untuned, baseline


def test_validate_prediction_alignment_accepts_equal_date_sets_and_targets():
    frames = _frames()
    analyze.validate_prediction_alignment(frames)


@pytest.mark.parametrize("mutate", ["duplicate", "missing", "extra", "actual", "unsorted"])
def test_validate_prediction_alignment_rejects_invalid_frames(mutate):
    frames = list(_frames())
    frame = frames[1]
    if mutate == "duplicate":
        frames[1] = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    elif mutate == "missing":
        frames[1] = frame.iloc[:-1].copy()
    elif mutate == "extra":
        extra = frame.iloc[[-1]].copy()
        extra["date"] = pd.Timestamp("2025-01-04")
        frames[1] = pd.concat([frame, extra], ignore_index=True)
    elif mutate == "actual":
        frames[1].loc[1, "y_true"] += 0.01
    else:
        frames[1] = frame.iloc[::-1].reset_index(drop=True)

    with pytest.raises(ValueError):
        analyze.validate_prediction_alignment(frames)
