"""Tests for the generated number audit."""

from __future__ import annotations

import json

import build_number_audit
from results_context import FinalResults


def _summary() -> dict:
    models = {}
    for index in range(8):
        mae = 1579.8 if index == 0 else 1700.0 + index * 10
        models[f"E{index}"] = {
            "run": f"E{index}",
            "model": f"Model {index}",
            "metrics": {"RMSE": mae * 1.3, "MAE": mae, "MAPE": mae / 1000},
            "confidence_intervals": {
                "RMSE": {"ci_low": mae, "ci_high": mae * 2},
                "MAE": {"ci_low": mae - 20, "ci_high": mae + 20},
                "MAPE": {"ci_low": 1.0, "ci_high": 2.0},
            },
            "multi_seed": None
            if index == 0
            else {
                "seeds": [42, 123, 2024, 7, 99],
                "aggregate": {
                    metric: {
                        "mean": mae,
                        "std": 5.0,
                        "min": mae - 5,
                        "max": mae + 5,
                        "n_seeds": 5,
                    }
                    for metric in ("RMSE", "MAE", "MAPE")
                },
            },
            "training": {
                "loss": "mae",
                "scheduler": "plateau",
                "hyperparameters": {
                    "lookback": 22,
                    "units": 100,
                    "dropout": 0.1,
                    "learning_rate": 0.00197,
                    "batch_size": 16,
                    "layers": 1,
                },
                "epochs_run": 46,
                "total_trials": 50,
                "best_trial_number": 44,
                "best_cv_loss": 689.89,
                "optimization_time_seconds": 1200.0,
                "training_time_seconds": 34.0,
            },
        }
    models["E0"]["training"] = {"model": "persistence"}
    comparison = {
        "model_a": "E0",
        "model_b": "E7",
        "metrics": {
            metric: {
                "difference_b_minus_a": 100.0,
                "relative_change_percent": 5.0,
                "ci_low": 50.0,
                "ci_high": 150.0,
                "p_value": 0.02,
            }
            for metric in ("RMSE", "MAE", "MAPE")
        },
    }
    return {
        "run_id": "audit_test",
        "status": "complete",
        "missing_models": [],
        "expected_seeds": 5,
        "seed_coverage_issues": {},
        "protocol_hash_issues": {},
        "primary_metric": "MAE",
        "data": {
            "n_train": 1753,
            "n_test": 439,
            "test_period": ["2024-10-19", "2025-12-31"],
            "statistics": {
                "n_observations": 2192,
                "period": ["2020-01-01", "2025-12-31"],
                "min": 4800.0,
                "min_date": "2020-03-12",
                "max": 124658.54,
                "max_date": "2025-10-06",
                "mean": 47182.88,
                "median": 39732.62,
                "std": 31418.23,
            },
        },
        "protocol": {
            "bootstrap": {
                "block_size_days": 7,
                "n_resamples": 2000,
                "confidence": 0.95,
            }
        },
        "baselines": {
            "persistence": {
                "metrics": {"RMSE": 2167.24, "MAE": 1579.8, "MAPE": 1.62}
            }
        },
        "models": models,
        "ranking_by_mae": [{"run": "E0", "model": "Persistence", "MAE": 1579.8}],
        "lstm_ranking_by_mae": [{"run": "E6", "model": "Model 6", "MAE": 1760.0}],
        "final_configuration": models["E7"]["training"],
        "headline": {
            "status": "proposed_not_better_than_persistence",
            "claim": "E7 tidak lebih baik daripada persistence pada MAE titik.",
        },
        "paired_comparisons": {"E7_vs_persistence": comparison},
        "environment": {
            "python_version": "3.14.7",
            "packages": {"tensorflow": "2.22.0rc0", "optuna": "5.0.0"},
        },
    }


def test_number_audit_contains_sources_and_verdict(tmp_path):
    path = tmp_path / "summary_final.json"
    path.write_text(json.dumps(_summary()), encoding="utf-8")
    results = FinalResults.load(path)
    text = build_number_audit.build_number_audit(results)

    assert "# Audit Angka Naskah" in text
    assert "`audit_test`" in text
    assert "| E0 |" in text
    assert "| E7 |" in text
    assert "`final_configuration.best_trial_number`" in text
    assert "`paired_comparisons.E7_vs_persistence.metrics.MAE`" in text
    assert "proposed_not_better_than_persistence" in text
    assert "RMSE 2.338,22" in text
    assert "1.579,80" in text


def test_number_audit_writes_file(tmp_path):
    summary = tmp_path / "summary_final.json"
    summary.write_text(json.dumps(_summary()), encoding="utf-8")
    output = tmp_path / "docs" / "NUMBER_AUDIT.md"
    written = build_number_audit.write_number_audit(output, summary)
    assert written == output
    assert "Audit Angka Naskah" in output.read_text(encoding="utf-8")
