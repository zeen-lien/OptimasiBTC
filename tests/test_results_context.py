"""Tests for the single source of truth used by document generators."""

from __future__ import annotations

import json

import pytest

import results_context


def _model(index: int, *, seeds: int = 5, mae: float | None = None) -> dict:
    value = 1600.0 + index * 100 if mae is None else mae
    aggregate = {
        metric: {
            "mean": value,
            "std": 10.0,
            "min": value - 10.0,
            "max": value + 10.0,
            "n_seeds": seeds,
        }
        for metric in ("RMSE", "MAE", "MAPE")
    }
    return {
        "run": f"E{index}",
        "model": f"Model {index}",
        "metrics": {"RMSE": value * 1.4, "MAE": value, "MAPE": value / 1000.0},
        "confidence_intervals": {
            "RMSE": {"estimate": value * 1.4, "ci_low": value, "ci_high": value * 1.8},
            "MAE": {"estimate": value, "ci_low": value - 50, "ci_high": value + 50},
            "MAPE": {"estimate": value / 1000.0, "ci_low": 0.1, "ci_high": 0.2},
        },
        "multi_seed": {
            "seeds": list(range(seeds)),
            "per_seed": {},
            "aggregate": aggregate,
        },
        "training": {
            "loss": "mae" if index >= 4 else "mse",
            "scheduler": "plateau" if index in (5, 6, 7) else None,
            "hyperparameters": {
                "lookback": 15 + index,
                "units": 100,
                "dropout": 0.2,
                "learning_rate": 0.001,
                "batch_size": 16,
                "layers": 1,
                "epochs_run": 40,
            },
            "epochs_run": 40,
            "training_time_seconds": 12.0,
        },
    }


def _summary() -> dict:
    models = {f"E{index}": _model(index) for index in range(8)}
    models["E7"] = _model(7, mae=1479.8)
    models["E0"] = {
        "run": "E0",
        "model": "Persistence",
        "metrics": {"RMSE": 2167.24, "MAE": 1579.8, "MAPE": 1.62},
        "confidence_intervals": {
            "RMSE": {"estimate": 2167.24, "ci_low": 2000.0, "ci_high": 2300.0},
            "MAE": {"estimate": 1579.8, "ci_low": 1450.0, "ci_high": 1700.0},
            "MAPE": {"estimate": 1.62, "ci_low": 1.4, "ci_high": 1.8},
        },
        "multi_seed": None,
        "training": {"model": "persistence"},
    }
    comparison = {
        "model_a": "E0",
        "model_b": "E7",
        "metrics": {
            "MAE": {
                "difference_b_minus_a": -100.0,
                "relative_change_percent": -6.3,
                "ci_low": -180.0,
                "ci_high": -20.0,
                "p_value": 0.01,
            },
            "RMSE": {
                "difference_b_minus_a": -200.0,
                "relative_change_percent": -9.0,
                "ci_low": -300.0,
                "ci_high": -100.0,
                "p_value": 0.01,
            },
            "MAPE": {
                "difference_b_minus_a": -0.1,
                "relative_change_percent": -6.0,
                "ci_low": -0.2,
                "ci_high": -0.01,
                "p_value": 0.01,
            },
        },
    }
    return {
        "schema_version": 1,
        "run_id": "final_test",
        "status": "complete",
        "missing_models": [],
        "expected_seeds": 5,
        "seed_coverage_issues": {},
        "protocol_hash_issues": {},
        "data": {"n_train": 1753, "n_test": 439},
        "models": models,
        "ranking_by_mae": [{"run": "E0", "model": "Persistence", "MAE": 1579.8}],
        "lstm_ranking_by_mae": [
            {"run": "E6", "model": "Model 6", "MAE": 2200.0}
        ],
        "final_configuration": models["E7"]["training"],
        "headline": {"status": "proposed_lower_mae_ci_excludes_zero"},
        "paired_comparisons": {"E7_vs_persistence": comparison},
    }


def test_loader_rejects_partial_and_seed_short_runs(tmp_path):
    payload = _summary()
    payload["status"] = "partial"
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(results_context.ResultsError, match="belum lengkap"):
        results_context.FinalResults.load(path)

    payload["status"] = "complete"
    payload["seed_coverage_issues"] = {"E7": 3}
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(results_context.ResultsError, match="Cakupan seed"):
        results_context.FinalResults.load(path)


def test_loader_rejects_protocol_drift_and_missing_model(tmp_path):
    payload = _summary()
    payload["protocol_hash_issues"] = {"docs/PROTOCOL.md": {"recorded": "a", "actual": "b"}}
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(results_context.ResultsError, match="Hash protokol"):
        results_context.FinalResults.load(path)

    payload = _summary()
    del payload["models"]["E5"]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(results_context.ResultsError, match="kehilangan model"):
        results_context.FinalResults.load(path)


def test_accessors_follow_summary_values(tmp_path):
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(_summary()), encoding="utf-8")
    results = results_context.FinalResults.load(path)

    assert results.run_id == "final_test"
    assert results.metric("E0", "MAE") == pytest.approx(1579.8)
    assert results.aggregate("E0", "MAE")["n_seeds"] == 1
    assert results.aggregate("E7", "MAE")["mean"] == pytest.approx(1479.8)
    assert results.training("E7")["hyperparameters"]["lookback"] == 22
    assert results.best_overall["run"] == "E0"
    assert results.best_lstm["run"] == "E6"
    assert results.expected_seeds == 5


def test_comparison_claim_requires_negative_ci(tmp_path):
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(_summary()), encoding="utf-8")
    results = results_context.FinalResults.load(path)
    assert results.is_significant("E7_vs_persistence")
    assert results.improvement("E7", "E0", "MAE") > 0

    payload = _summary()
    payload["paired_comparisons"]["E7_vs_persistence"]["metrics"]["MAE"]["ci_high"] = 5.0
    path.write_text(json.dumps(payload), encoding="utf-8")
    results = results_context.FinalResults.load(path)
    assert not results.is_significant("E7_vs_persistence")
    assert results.is_improvement("E7_vs_persistence", require_ci=False)


def test_summary_and_ablation_rows_are_ordered(tmp_path):
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(_summary()), encoding="utf-8")
    results = results_context.FinalResults.load(path)
    rows = results.summary_rows()
    assert [row["run"] for row in rows] == list(results_context.MODEL_ORDER)
    ablation = results.ablation_rows()
    assert [row["run"] for row in ablation] == ["E3", "E4", "E5", "E6"]
    assert all("delta_MAE_vs_E3" in row for row in ablation)


def test_indonesian_number_formatting():
    assert results_context.format_number(1579.8) == "1.579,80"
    assert results_context.format_usd(2338.22) == "USD 2.338,22"
    assert results_context.format_pct(1.81) == "1,81%"
    assert results_context.format_number(0.00197, decimals=5) == "0,00197"
    assert results_context.format_interval(1500, 1600) == "USD 1.500,00–USD 1.600,00"
