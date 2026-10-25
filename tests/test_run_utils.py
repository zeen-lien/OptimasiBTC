"""Run isolation and manifest behavior."""

from __future__ import annotations

from datetime import datetime

import pytest

import run_utils


def test_make_run_id_is_traceable():
    run_id = run_utils.make_run_id(
        stage="tier3", seed=42, timestamp=datetime(2026, 10, 25, 14, 30, 0)
    )
    assert run_id == "2026-10-25_143000_tier3_seed42"


def test_invalid_run_id_rejected(tmp_path):
    with pytest.raises(ValueError):
        run_utils.resolve_run_paths(run_id="../escape", root=tmp_path)
    with pytest.raises(ValueError):
        run_utils.resolve_run_paths(run_id="contains space", root=tmp_path)


def test_bootstrap_and_record_stage(tmp_path):
    paths = run_utils.resolve_run_paths(run_id="unit_test", root=tmp_path)
    assert paths.run_dir == tmp_path / "05_Source_Code" / "results" / "runs" / "unit_test"
    for directory in (
        paths.metrics_dir,
        paths.predictions_dir,
        paths.figures_dir,
        paths.logs_dir,
        paths.models_dir,
        paths.processed_dir,
    ):
        assert directory.is_dir()

    input_file = tmp_path / "input.csv"
    input_file.write_text("date,close\n2020-01-01,1\n", encoding="utf-8")
    output_file = paths.metrics_dir / "metrics_tier1.json"
    output_file.write_text('{"ok": true}\n', encoding="utf-8")

    started = run_utils.utc_now()
    run_utils.bootstrap_run(
        paths, "tier1", {"seed": 42, "lookback": 30}, inputs=[input_file]
    )
    run_utils.record_stage(
        paths,
        "tier1",
        status="success",
        started_at=started,
        stage_config={"seed": 42},
        inputs=[input_file],
        outputs=[output_file],
    )

    manifest = run_utils.read_json(paths.manifest_path)
    config_payload = run_utils.read_json(paths.config_path)
    hashes = run_utils.read_json(paths.data_hash_json_path)

    assert manifest["run_id"] == "unit_test"
    assert manifest["stages"]["tier1"]["status"] == "success"
    assert config_payload["stages"]["tier1"]["seed"] == 42
    assert any("input.csv" in key for key in hashes)
    assert any("metrics_tier1.json" in key for key in hashes)
    assert paths.env_path.exists()
    assert paths.git_commit_path.exists()
    assert paths.data_hash_path.exists()


def test_sha256_file(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_bytes(b"abc")
    assert run_utils.sha256_file(path) == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_legacy_paths_do_not_create_run_directory(tmp_path):
    paths = run_utils.resolve_run_paths(legacy=True, root=tmp_path, create=False)
    assert paths.legacy is True
    assert paths.metrics_dir == tmp_path / "05_Source_Code" / "results" / "metrics"
    assert not (tmp_path / "05_Source_Code" / "results" / "runs").exists()


def test_bootstrap_hashes_protocol_and_requirements(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "PROTOCOL.md").write_text("protocol v1\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("numpy==1\n", encoding="utf-8")

    paths = run_utils.resolve_run_paths(run_id="governed", root=tmp_path)
    run_utils.bootstrap_run(paths, "test", {"seed": 42})
    hashes = run_utils.read_json(paths.data_hash_json_path)
    assert "docs/PROTOCOL.md" in hashes
    assert "requirements.txt" in hashes
