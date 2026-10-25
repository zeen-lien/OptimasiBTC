"""Final-analysis helpers: verdicts must follow the published decision rule."""

from __future__ import annotations

import pytest

from importlib import import_module

analyze = import_module("08_analyze_results")


def _model(mae: float) -> dict:
    return {"metrics": {"RMSE": mae * 2, "MAE": mae, "MAPE": 1.0}}


def _comparison(ci_low: float, ci_high: float) -> dict:
    return {
        "metrics": {
            "MAE": {"ci_low": ci_low, "ci_high": ci_high, "p_value": 0.01},
        }
    }


def test_verdict_incomplete_without_e7_or_persistence():
    verdict = analyze.build_verdict({"E7": _model(100.0)}, {})
    assert verdict["status"] == "incomplete"


def test_verdict_accepts_lower_mae_only_when_ci_excludes_zero():
    models = {"E0": _model(200.0), "E7": _model(150.0)}
    verdict = analyze.build_verdict(models, {"E7_vs_persistence": _comparison(-80.0, -20.0)})
    assert verdict["status"] == "proposed_lower_mae_ci_excludes_zero"
    assert verdict["ci_excludes_zero"] is True
    assert verdict["relative_improvement_percent"] == pytest.approx(25.0)


def test_verdict_does_not_claim_significance_when_ci_includes_zero():
    models = {"E0": _model(200.0), "E7": _model(150.0)}
    verdict = analyze.build_verdict(models, {"E7_vs_persistence": _comparison(-80.0, 5.0)})
    assert verdict["status"] == "proposed_lower_mae_ci_includes_zero"
    assert verdict["ci_excludes_zero"] is False


def test_verdict_reports_negative_result_without_spin():
    models = {"E0": _model(150.0), "E7": _model(200.0)}
    verdict = analyze.build_verdict(models, {"E7_vs_persistence": _comparison(10.0, 90.0)})
    assert verdict["status"] == "proposed_not_better_than_persistence"
    assert verdict["relative_improvement_percent"] < 0


def test_metric_consistency_rejects_large_mismatch():
    recorded = {"RMSE": 100.0, "MAE": 80.0, "MAPE": 2.0}
    analyze.check_metric_consistency(
        "E3", recorded, {"RMSE": 100.02, "MAE": 79.99, "MAPE": 2.0}
    )
    with pytest.raises(ValueError):
        analyze.check_metric_consistency(
            "E3", recorded, {"RMSE": 101.0, "MAE": 80.0, "MAPE": 2.0}
        )


def test_markdown_table_formats_numbers_and_missing_values():
    import pandas as pd

    frame = pd.DataFrame(
        {
            "Run": ["E0", "E7"],
            "MAE": [1579.8, float("nan")],
            "HPO": [False, True],
        }
    )
    text = analyze.format_markdown_table(frame)
    assert "| Run | MAE | HPO |" in text
    assert "1,579.80" in text
    assert "| Tidak |" in text
    assert "| Ya |" in text
    assert "-" in text


def test_training_summary_reads_best_trial_and_hyperparameters():
    payload = {
        "loss": "mean_absolute_error",
        "scheduler": "reduce_lr_on_plateau",
        "early_stopping": {"monitor": "val_loss", "patience": 12},
        "hyperparameters": {
            "lookback": 22,
            "units": 100,
            "dropout": 0.1,
            "learning_rate": 0.001966,
            "batch_size": 16,
            "layers": 1,
            "epochs_max": 100,
            "epochs_run": 37,
        },
        "final_training_time_seconds": 12.5,
        "total_trials": 50,
        "best_trial_number": 36,
        "best_cv_loss": 1234.5,
        "sampler_seed": 42,
    }
    summary = analyze.training_summary(payload, "E7")
    assert summary["hyperparameters"]["lookback"] == 22
    assert summary["epochs_run"] == 37
    assert summary["training_time_seconds"] == pytest.approx(12.5)
    assert summary["total_trials"] == 50
    assert summary["best_trial_number"] == 36
    assert summary["best_cv_loss"] == pytest.approx(1234.5)


def test_training_summary_for_persistence_is_explicit():
    assert analyze.training_summary({}, "E0") == {"model": "persistence"}


def test_seed_coverage_flags_silently_short_runs():
    models = {
        "E0": {"multi_seed": None},
        "E3": {"multi_seed": {"aggregate": {"MAE": {"n_seeds": 5}}}},
        "E4": {"multi_seed": {"aggregate": {"MAE": {"n_seeds": 3}}}},
        "E7": {"multi_seed": None},
    }
    issues = analyze.seed_coverage(models, expected_seeds=5)
    assert issues == {"E4": 3, "E7": None}
    assert analyze.seed_coverage(models, expected_seeds=1) == {}


def test_protocol_hash_issues_detects_post_start_edits(tmp_path):
    import json

    (tmp_path / "docs").mkdir()
    protocol = tmp_path / "docs" / "PROTOCOL.md"
    requirements = tmp_path / "requirements.txt"
    protocol.write_text("protocol v1", encoding="utf-8")
    requirements.write_text("tensorflow==2.22.0rc0\n", encoding="utf-8")
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    hashes = {
        "docs/PROTOCOL.md": analyze.file_sha256(protocol),
        "requirements.txt": analyze.file_sha256(requirements),
    }
    (run_dir / "data_hash.json").write_text(json.dumps(hashes), encoding="utf-8")

    assert analyze.protocol_hash_issues(tmp_path, run_dir) == {}

    protocol.write_text("protocol v2", encoding="utf-8")
    issues = analyze.protocol_hash_issues(tmp_path, run_dir)
    assert set(issues) == {"docs/PROTOCOL.md"}
    assert issues["docs/PROTOCOL.md"]["actual"] != issues["docs/PROTOCOL.md"]["recorded"]


def _prediction_frame(dates, actual, predicted, column):
    import pandas as pd

    return pd.DataFrame(
        {"date": dates, "actual_close": actual, column: predicted}
    )


def test_align_frames_rejects_shifted_or_mismatched_actuals():
    import numpy as np
    import pandas as pd

    dates = pd.date_range("2025-01-01", periods=10)
    actual = np.linspace(100, 109, 10)
    e1 = _prediction_frame(
        dates, actual, actual - 0.5, "predicted_close_tier1"
    )
    e2 = _prediction_frame(
        dates, actual, actual - 1.0, "predicted_close_tier2"
    )
    aligned_dates, series, aligned = analyze.align_frames(
        {"E1": e1, "E2": e2}, "E1"
    )
    assert len(aligned_dates) == 10
    assert aligned["E2"][0] == pytest.approx(99.0)

    shifted = _prediction_frame(
        dates + pd.Timedelta(days=1), actual, actual - 1.0, "predicted_close_tier2"
    )
    with pytest.raises(ValueError):
        analyze.align_frames({"E1": e1, "E2": shifted}, "E1")

    mismatched = _prediction_frame(
        dates, actual + 1.0, actual - 1.0, "predicted_close_tier2"
    )
    with pytest.raises(AssertionError):
        analyze.align_frames({"E1": e1, "E2": mismatched}, "E1")
