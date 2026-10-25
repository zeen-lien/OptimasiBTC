"""The controlled matrix must isolate exactly one factor per comparison."""

from __future__ import annotations

import pytest

import config
from experiment_matrix import (
    EXPERIMENTS,
    EXPERIMENTS_BY_KEY,
    EXPERIMENT_KEYS,
    build_analysis_command,
    build_command,
    matrix_plan,
    parse_only,
    validate_matrix,
)


def test_matrix_has_e0_through_e7_in_order():
    assert tuple(experiment.key for experiment in EXPERIMENTS) == EXPERIMENT_KEYS
    assert EXPERIMENT_KEYS == ("E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7")


def test_ablation_factorial_only_varies_loss_and_scheduler():
    e3 = EXPERIMENTS_BY_KEY["E3"]
    expected = {
        "E3": ("mse", "none"),
        "E4": ("mae", "none"),
        "E5": ("mse", "plateau"),
        "E6": ("mae", "plateau"),
    }
    for key, (loss, scheduler) in expected.items():
        experiment = EXPERIMENTS_BY_KEY[key]
        assert (experiment.loss, experiment.scheduler) == (loss, scheduler)
        assert experiment.script == e3.script
        assert experiment.hpo is False
        assert experiment.tag != e3.tag if key != "E3" else experiment.tag == e3.tag


def test_e7_is_the_only_hpo_and_is_the_proposed_model():
    hpo_runs = [experiment.key for experiment in EXPERIMENTS if experiment.hpo]
    assert hpo_runs == ["E7"]
    assert EXPERIMENTS_BY_KEY["E7"].role == "proposed_model"


def test_validate_matrix_rejects_broken_design():
    broken = list(EXPERIMENTS)
    broken[3] = EXPERIMENTS_BY_KEY["E3"].__class__(
        **{**EXPERIMENTS_BY_KEY["E3"].__dict__, "loss": "mae"}
    )
    with pytest.raises(ValueError):
        validate_matrix(broken)


def test_build_command_forwards_controlled_settings(tmp_path):
    command = build_command(
        EXPERIMENTS_BY_KEY["E4"],
        run_id="matrix_test",
        root=tmp_path,
        seed=42,
        seeds=(42, 123),
        epochs=3,
        patience=12,
        trials=5,
        screening_epochs=2,
        cv_splits=3,
        processed_dir=None,
    )
    joined = " ".join(command)
    assert "07_run_ablation.py" in joined
    assert "--tag e4_mae_none" in joined
    assert "--loss mae" in joined
    assert "--scheduler none" in joined
    assert "--epochs 3" in joined
    assert "--seeds 42,123" in joined
    assert "--patience 12" in joined
    assert "--run-id matrix_test" in joined
    assert "--project-root" in joined


def test_e1_and_e3_share_loss_scheduler_and_epoch_rules(tmp_path):
    common = dict(
        run_id="matrix_test",
        root=tmp_path,
        seed=42,
        seeds=(42, 123),
        epochs=3,
        patience=12,
        trials=5,
        screening_epochs=2,
        cv_splits=3,
        processed_dir=None,
    )
    e1 = " ".join(build_command(EXPERIMENTS_BY_KEY["E1"], **common))
    e3 = " ".join(build_command(EXPERIMENTS_BY_KEY["E3"], **common))
    for flag in ("--epochs 3", "--seeds 42,123", "--patience 12"):
        assert flag in e1
        assert flag in e3
    assert EXPERIMENTS_BY_KEY["E1"].loss == EXPERIMENTS_BY_KEY["E3"].loss == "mse"
    assert EXPERIMENTS_BY_KEY["E1"].scheduler == EXPERIMENTS_BY_KEY["E3"].scheduler == "none"


def test_e7_command_passes_hpo_budget(tmp_path):
    command = build_command(
        EXPERIMENTS_BY_KEY["E7"],
        run_id="matrix_test",
        root=tmp_path,
        seed=42,
        seeds=(42,),
        epochs=1,
        patience=12,
        trials=7,
        screening_epochs=2,
        cv_splits=3,
        processed_dir=None,
    )
    joined = " ".join(command)
    assert "05_optimize_optuna_tier3.py" in joined
    assert "--trials 7" in joined
    assert "--screening-epochs 2" in joined
    assert "--cv-splits 3" in joined
    # E7 must not be turned into a fixed-parameter ablation.
    assert "--loss" not in joined
    assert "--scheduler" not in joined


def test_parse_only_rejects_unknown_run():
    assert parse_only("E3,E4") == ("E3", "E4")
    with pytest.raises(ValueError):
        parse_only("E3,E9")


def test_analysis_command_marks_partial_runs_and_publish(tmp_path):
    command = build_analysis_command(
        run_id="matrix_test",
        root=tmp_path,
        seed=42,
        allow_partial=True,
        publish=False,
    )
    joined = " ".join(command)
    assert "08_analyze_results.py" in joined
    assert "--allow-partial" in joined
    assert "--publish" not in joined

    full = " ".join(
        build_analysis_command(
            run_id="matrix_test",
            root=tmp_path,
            seed=42,
            allow_partial=False,
            publish=True,
        )
    )
    assert "--allow-partial" not in full
    assert "--publish" in full


def test_seed_list_always_includes_primary_first():
    from experiment_matrix import parse_seed_list

    assert parse_seed_list("123,2024", primary=42) == (42, 123, 2024)
    assert parse_seed_list(None, primary=7) == (7, 42, 123, 2024, 99)
    assert parse_seed_list(None, primary=7) != config.DEFAULT_SEEDS


def test_matrix_plan_records_hypotheses_and_comparisons():
    plan = matrix_plan(
        run_id="matrix_test",
        seed=42,
        seeds=(42, 123),
        epochs=1,
        patience=12,
        trials=5,
        screening_epochs=2,
        cv_splits=3,
    )
    assert len(plan["experiments"]) == 8
    assert "E1_vs_E3" in plan["comparisons"]
    assert "E7_vs_E6" in plan["comparisons"]
    assert all(experiment["hypothesis"] for experiment in plan["experiments"])
