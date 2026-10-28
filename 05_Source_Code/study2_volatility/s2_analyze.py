"""
s2_analyze.py - One-shot analysis of the Study 2 final run (protocol section 9).

Reads one final run directory, evaluates the pre-registered endpoints on the
2026 test window, and writes:
    results_analysis.json   - all metrics, DM tests, bootstrap CIs, verdict
    results_analysis.md     - human-readable summary
    PROVENANCE_NOTE.md      - what was seen when (smoke footnote)

This script is run ONCE, after s2_final_run.py produced the full 5-seed run.
Re-running with the same inputs is deterministic and harmless; what is
forbidden is changing inputs after seeing results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import s2_config as cfg
import s2_runlog
from s2_stats import (
    dm_test,
    mae_rmse_logrv,
    moving_block_bootstrap_mean_ci,
    paired_loss_diff,
    qlike,
    qlike_per_obs,
)


def load_preds(run_dir: Path, window: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    lstm = {}
    for name in ("untuned", "optuna"):
        df = pd.read_csv(run_dir / f"predictions_lstm_{name}_{window}.csv",
                         parse_dates=["date"])
        lstm[name] = df
    baselines = pd.read_csv(run_dir / f"predictions_baselines_{window}.csv",
                            parse_dates=["date"])
    return lstm, baselines


def eval_pair(window: str, y_true: np.ndarray, dates: np.ndarray,
              pred_a: np.ndarray, label_a: str,
              pred_b: np.ndarray, label_b: str) -> dict:
    """QLIKE both + DM + bootstrap on daily QLIKE differences (a vs b)."""
    qa = qlike_per_obs(y_true, pred_a)
    qb = qlike_per_obs(y_true, pred_b)
    res = {
        "a": label_a, "b": label_b, "n": int(len(y_true)),
        "qlike": {label_a: qlike(y_true, pred_a), label_b: qlike(y_true, pred_b)},
        **{f"{label_a}_{k}": v for k, v in mae_rmse_logrv(y_true, pred_a).items()},
        **{f"{label_b}_{k}": v for k, v in mae_rmse_logrv(y_true, pred_b).items()},
    }
    d = qa - qb
    res["dm"] = dm_test(d)
    res["bootstrap"] = moving_block_bootstrap_mean_ci(d)
    return res


def analyze_window(window: str, lstm: dict, baselines: pd.DataFrame) -> dict:
    base = baselines
    optuna_df = lstm["optuna"]
    untuned_df = lstm["untuned"]

    merged = (optuna_df.merge(untuned_df, on="date", suffixes=("_opt", "_unt"))
              .merge(base, on="date"))
    y = merged["y_true"].to_numpy()
    dates = merged["date"].to_numpy()

    preds = {
        "lstm_optuna": merged["y_hat_mean_opt"].to_numpy(),
        "lstm_untuned": merged["y_hat_mean_unt"].to_numpy(),
        "persistence": merged["persistence"].to_numpy(),
        "har_rv": merged["har_rv"].to_numpy(),
        "garch11": merged["garch11"].to_numpy(),
    }
    out = {"window": window, "n_eval": int(len(y)), "models": {}, "comparisons": {}}
    out["models"] = {k: {"qlike": qlike(y, v), **mae_rmse_logrv(y, v)}
                     for k, v in preds.items()}

    # Primary comparisons (seed-averaged Optuna-LSTM vs primary baselines).
    for b in cfg.PRIMARY_BASELINES:
        out["comparisons"][f"lstm_optuna_vs_{b}"] = eval_pair(
            window, y, dates, preds["lstm_optuna"], "lstm_optuna", preds[b], b)
    # Secondary.
    for b in cfg.SECONDARY_BASELINES:
        out["comparisons"][f"lstm_optuna_vs_{b}"] = eval_pair(
            window, y, dates, preds["lstm_optuna"], "lstm_optuna", preds[b], b)

    out["optuna_per_seed_qlike"] = {
        f"seed{s}": qlike(y, merged[f"y_hat_seed{s}_opt"].to_numpy())
        for s in cfg.SEEDS}
    out["untuned_per_seed_qlike"] = {
        f"seed{s}": qlike(y, merged[f"y_hat_seed{s}_unt"].to_numpy())
        for s in cfg.SEEDS}

    if window == "test":
        prim = [out["comparisons"][f"lstm_optuna_vs_{b}"] for b in cfg.PRIMARY_BASELINES]
        beats = all(
            out["models"]["lstm_optuna"]["qlike"] < out["models"][b]["qlike"]
            for b in cfg.PRIMARY_BASELINES)
        dm_ok = all(c["dm"]["p_one_sided"] < cfg.ALPHA for c in prim)
        ci_ok = all(c["bootstrap"]["ci_high"] < 0.0 for c in prim)
        if beats and dm_ok and ci_ok:
            out["verdict"] = "positive"
        elif beats:
            out["verdict"] = "mixed_beats_but_not_significant"
        else:
            out["verdict"] = "negative"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True)
    args = ap.parse_args()
    run_dir = args.run

    verify = {
        "protocol_sha256": cfg.protocol_hash(),
        "protocol_recorded": cfg.PROTOCOL_HASH_PATH.read_text().strip(),
        "daily_csv_sha256": cfg.sha256_file(cfg.S2_DAILY_CSV),
    }
    assert verify["protocol_sha256"] == verify["protocol_recorded"]

    results = {"run_dir": str(run_dir), "verification": verify,
               "alpha": cfg.ALPHA, "dm_hac_lag": cfg.DM_HAC_LAG,
               "bootstrap": {"block": cfg.BOOTSTRAP_BLOCK,
                             "reps": cfg.BOOTSTRAP_REPS,
                             "seed": cfg.BOOTSTRAP_SEED}}

    for window in ("val", "test"):
        lstm, baselines = load_preds(run_dir, window)
        results[window] = analyze_window(window, lstm, baselines)

    out_json = run_dir / "results_analysis.json"
    out_md = run_dir / "results_analysis.md"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = [f"# Study 2 Analysis ({run_dir.name})", ""]
    for window in ("val", "test"):
        w = results[window]
        lines += [f"## {window.upper()} (n={w['n_eval']})", "",
                  "| Model | QLIKE | MAE_logRV | RMSE_logRV |", "|---|---|---|---|"]
        for k, v in w["models"].items():
            lines.append(f"| {k} | {v['qlike']:.5f} | {v['MAE_logRV']:.5f} "
                         f"| {v['RMSE_logRV']:.5f} |")
        lines += ["", "### Comparisons (a = lstm_optuna)"]
        for key, c in w["comparisons"].items():
            dm = c["dm"]; bt = c["bootstrap"]
            lines.append(
                f"- vs {c['b']}: ΔQLIKE mean {dm['mean_diff']:+.5f}; "
                f"DM p(one-sided)={dm['p_one_sided']:.4f}; "
                f"boot 95% CI [{bt['ci_low']:.5f}, {bt['ci_high']:.5f}]")
        if window == "test":
            lines += ["", f"**VERDICT: {w['verdict']}**"]
        lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
