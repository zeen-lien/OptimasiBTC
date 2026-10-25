"""Provenance checks: Optuna DB, metrics JSON, and run manifests agree."""

from __future__ import annotations

import json
import sqlite3

import pytest

import config


def _best_complete_trial(db_path):
    connection = sqlite3.connect(db_path)
    try:
        row = connection.execute(
            """
            SELECT t.number, tv.value
            FROM trials AS t
            JOIN trial_values AS tv ON tv.trial_id = t.trial_id
            WHERE t.state = 'COMPLETE' AND tv.objective = 0
            ORDER BY tv.value ASC
            LIMIT 1
            """
        ).fetchone()
        if row is None:
            raise AssertionError("Tidak ada trial COMPLETE di database Optuna")
        number, value = row
        params = {}
        for name, param_value, distribution_json in connection.execute(
            """
            SELECT param_name, param_value, distribution_json
            FROM trial_params
            WHERE trial_id = (SELECT trial_id FROM trials WHERE number = ?)
            """,
            (number,),
        ).fetchall():
            distribution = json.loads(distribution_json)
            if distribution.get("name") == "CategoricalDistribution":
                choices = distribution["attributes"]["choices"]
                params[name] = choices[int(param_value)]
            else:
                params[name] = param_value
        return number, value, params
    finally:
        connection.close()


def test_optuna_best_trial_matches_metrics_json():
    metrics = json.loads(
        (config.LEGACY_METRICS_DIR / "metrics_tier3.json").read_text(encoding="utf-8")
    )
    number, value, params = _best_complete_trial(config.LEGACY_STUDY_DB)

    assert metrics["best_trial_number"] == number
    assert metrics["best_cv_loss"] == pytest.approx(value, abs=1e-6)

    hyper = metrics["hyperparameters"]
    assert hyper["lookback"] == int(params["lookback"])
    assert hyper["units"] == int(params["units"])
    assert hyper["dropout"] == pytest.approx(params["dropout"])
    assert hyper["learning_rate"] == pytest.approx(params["learning_rate"], rel=1e-12)
    assert hyper["batch_size"] == int(params["batch_size"])
    assert hyper["layers"] == int(params["layers"])


def test_tier3_metrics_describe_its_actual_protocol():
    metrics = json.loads(
        (config.LEGACY_METRICS_DIR / "metrics_tier3.json").read_text(encoding="utf-8")
    )
    assert metrics["metrics"]["RMSE"] == pytest.approx(2338.22, abs=0.01)
    assert metrics["metrics"]["MAE"] == pytest.approx(1784.27, abs=0.01)
    assert metrics["metrics"]["MAPE"] == pytest.approx(1.81, abs=0.01)
    # Fase 1 still carries the legacy protocol; Fase 2 must change this.
    assert metrics.get("loss") in (None, "mean_absolute_error")
