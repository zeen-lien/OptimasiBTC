"""[BAB 4 §4.1 | ANALISIS HASIL EVALUASI DAN PENILAIAN KRITERIA KESUKSESAN]

Modul ini membaca berkas prediksi luaran dari `s2_final_run.py`, memverifikasi integritas
penyelarasan data (alignment check), menghitung metrik performa komparatif (QLIKE, MAE, RMSE),
menjalankan uji statistik Diebold-Mariano dan block bootstrap, serta menetapkan status verdict akhir:
- `results_analysis.json`: Rekapitulasi kuantitatif lengkap seluruh metrik dan inferensi.
- `results_analysis.md`: Ringkasan tabular ramah-baca untuk pelaporan Bab 4 skripsi.
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


def load_preds(run_dir: Path, window: str) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    [BAB 4 §4.1 | PEMUATAN PREDIKSI MODEL]
    Memuat berkas CSV prediksi LSTM (untuned & optuna) dan baseline (persistence, HAR, GARCH)
    untuk jendela evaluasi yang diminta ('val' atau 'test').
    """
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
    """
    [BAB 4 §4.2 | EVALUASI KOMPARATIF BERPASANGAN]
    Menghitung skor QLIKE kedua model, metrik MAE/RMSE, selisih loss harian (a - b),
    uji satu-arah Diebold-Mariano, dan interval kepercayaan 95% moving-block bootstrap.
    """
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


def validate_prediction_alignment(frames: list[pd.DataFrame]) -> None:
    """
    [BAB 4 §4.1 | VALIDASI KESELARASAN PREDIKSI (FAIL-CLOSED)]
    Menjamin integritas data evaluasi: menolak secara tegas bila terdapat tanggal duplikat,
    tanggal hilang/berlebih, urutan tidak monoton meningkat, nilai NaN/tak-hingga,
    atau bila deret nilai aktual y_true berbeda antar-model.
    """
    if not frames:
        raise ValueError("No prediction frames supplied")
    reference_dates: np.ndarray | None = None
    reference_actual: np.ndarray | None = None
    for index, frame in enumerate(frames):
        if "date" not in frame.columns or "y_true" not in frame.columns:
            raise ValueError(f"Prediction frame {index} lacks date or y_true")
        if bool(frame["date"].isna().any()) or bool(frame["y_true"].isna().any()):
            raise ValueError(f"Prediction frame {index} has null date or y_true")
        if frame["date"].duplicated().any():
            raise ValueError(f"Prediction frame {index} has duplicate dates")
        dates = pd.to_datetime(frame["date"], errors="coerce")
        if dates.isna().any() or not dates.is_monotonic_increasing:
            raise ValueError(f"Prediction frame {index} dates are invalid or unsorted")
        actual = frame["y_true"].to_numpy(dtype=float)
        if not np.isfinite(actual).all():
            raise ValueError(f"Prediction frame {index} has non-finite y_true")
        if reference_dates is None:
            reference_dates, reference_actual = dates.to_numpy(), actual
        elif not np.array_equal(reference_dates, dates.to_numpy()):
            raise ValueError(f"Prediction frame {index} date set/order differs")
        elif not np.array_equal(reference_actual, actual):
            raise ValueError(f"Prediction frame {index} y_true differs")


def analyze_window(window: str, lstm: dict, baselines: pd.DataFrame) -> dict:
    """
    [BAB 4 §4.2 | ANALISIS JENDELA DAN PENETAPAN STATUS KESUKSESAN PROTOKOL]
    Menggabungkan seluruh model pada tanggal evaluasi yang selaras sempurna.
    Mengevaluasi komparasi primer (vs persistence dan HAR-RV) dan sekunder (vs GARCH dan LSTM-untuned).
    Menentukan vonis praregistrasi pada jendela test: positive, mixed, atau negative.
    """
    base = baselines
    optuna_df = lstm["optuna"]
    untuned_df = lstm["untuned"]
    validate_prediction_alignment([optuna_df, untuned_df, base])

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

    # Komparasi primer: Optuna-LSTM (rata-rata 5 seed) vs baseline primer (persistence & HAR-RV)
    for b in cfg.PRIMARY_BASELINES:
        out["comparisons"][f"lstm_optuna_vs_{b}"] = eval_pair(
            window, y, dates, preds["lstm_optuna"], "lstm_optuna", preds[b], b)
    # Komparasi sekunder
    for b in cfg.SECONDARY_BASELINES:
        out["comparisons"][f"lstm_optuna_vs_{b}"] = eval_pair(
            window, y, dates, preds["lstm_optuna"], "lstm_optuna", preds[b], b)

    out["optuna_per_seed_qlike"] = {
        f"seed{s}": qlike(y, merged[f"y_hat_seed{s}_opt"].to_numpy())
        for s in cfg.SEEDS}
    out["untuned_per_seed_qlike"] = {
        f"seed{s}": qlike(y, merged[f"y_hat_seed{s}_unt"].to_numpy())
        for s in cfg.SEEDS}

    # Kriteria kesuksesan praregistrasi resmi (Protokol Bagian 9)
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
