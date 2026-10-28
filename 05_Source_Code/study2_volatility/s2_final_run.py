"""
s2_final_run.py - Final Study 2 model runs (protocol sections 4 & 6).

For each of the two LSTM variants (untuned, optuna) x 5 seeds:
  - "val" fit:   train on DEV (2020-2023) only, predict 2024-2025 (checkpoint);
  - "test" fit:  train on the full pool (2020-2025), predict 2026 (external test).
Early stopping uses the last 10% of the training samples (chronological,
inside the training region only). Scalers are fit on training samples only.

Baselines (persistence, HAR-RV, GARCH) get causal predictions for both windows.
The 2026 test window is only *predicted* here; analysis is a separate script
run once, after this run finishes (protocol section 10).

Run:
    python s2_final_run.py --hpo_run <run_dir_with_best_params.json>
    python s2_final_run.py --hpo_run <...> --smoke   # 2 epochs, 2 seeds
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import s2_config as cfg
import s2_data as sd
import s2_models as sm
import s2_runlog
from s2_stats import mae_rmse_logrv, qlike


def verify_gate() -> None:
    recorded = json.loads(cfg.S2_DATA_FREEZE_HASH.read_text(encoding="utf-8"))
    assert cfg.protocol_hash() == cfg.PROTOCOL_HASH_PATH.read_text().strip(), \
        "protokol berubah setelah dikunci"
    assert cfg.sha256_file(cfg.S2_DAILY_CSV) == recorded["daily_csv_sha256"], \
        "data harian berubah setelah dibekukan"
    print("[gate] protocol & data hashes verified.")


def load_best_params(hpo_run: Path) -> dict:
    best = json.loads((hpo_run / "best_params.json").read_text(encoding="utf-8"))
    print(f"[hpo] best trial {best['best_trial']} value={best['best_value']:.5f} "
          f"params={best['best_params']}")
    return best["best_params"]


def internal_val_split(n: int, frac: float = 0.10) -> tuple[np.ndarray, np.ndarray]:
    n_val = max(1, int(round(n * frac)))
    return np.arange(n - n_val), np.arange(n - n_val, n)


def run_lstm_variant(
    name: str, params: dict, df: pd.DataFrame, seeds: list[int], smoke: bool,
    run_dir: Path,
) -> None:
    max_epochs = 2 if smoke else cfg.MAX_EPOCHS
    lookback = params["lookback"]
    dev = df[df["date"] <= cfg.DEV_END]
    pool = df[df["date"] <= cfg.TRAIN_POOL_END]

    jobs = [("val", dev, cfg.VAL_START, cfg.VAL_END),
            ("test", pool, cfg.TEST_START, cfg.TEST_END)]
    for job, train_df, w_start, w_end in jobs:
        Xtr_all, ytr_all, _, _ = sm.build_samples(train_df, lookback=lookback)
        tr_idx, es_idx = internal_val_split(len(Xtr_all))
        X_fit, y_fit = Xtr_all[tr_idx], ytr_all[tr_idx]
        X_es, y_es = Xtr_all[es_idx], ytr_all[es_idx]
        scaler_x, scaler_y = sm.fit_scaler(X_fit, y_fit)
        Xf, yf = sm.transform_xy(scaler_x, scaler_y, X_fit, y_fit)
        Xe, ye = sm.transform_xy(scaler_x, scaler_y, X_es, y_es)

        # Prediction inputs: causal windows over the full frozen frame.
        Xall, yall, _, tall = sm.build_samples(df, lookback=lookback)
        w_mask = (tall >= np.datetime64(w_start)) & (tall <= np.datetime64(w_end))
        Xw, yw, tw = Xall[w_mask], yall[w_mask], tall[w_mask]
        Xw_s, _ = sm.transform_xy(scaler_x, scaler_y, Xw, yw)

        seed_preds = {}
        epochs_seen = []
        for seed in seeds:
            model, best_epoch = sm.train_one(Xf, yf, Xe, ye, params, seed=seed,
                                             max_epochs=max_epochs)
            p_log = scaler_y.inverse_transform(model.predict(Xw_s, verbose=0)).reshape(-1)
            seed_preds[seed] = p_log
            epochs_seen.append(best_epoch)
        yhat_mean = np.mean(list(seed_preds.values()), axis=0)

        out = pd.DataFrame({"date": tw, "y_true": yw, "y_hat_mean": yhat_mean})
        for seed, arr in seed_preds.items():
            out[f"y_hat_seed{seed}"] = arr
        pred_path = run_dir / f"predictions_lstm_{name}_{job}.csv"
        out.to_csv(pred_path, index=False)

        per_seed = {s: qlike(yw, arr) for s, arr in seed_preds.items()}
        metrics = {
            "model": f"lstm_{name}", "fit": job,
            "params": params, "lookback": lookback,
            "n_train_fit": int(len(Xf)), "n_train_es": int(len(Xe)),
            "n_eval": int(len(tw)), "window": f"{w_start}..{w_end}",
            "qlike_mean_forecast": qlike(yw, yhat_mean),
            "qlike_per_seed": per_seed,
            "best_epochs": epochs_seen,
            **mae_rmse_logrv(yw, yhat_mean),
        }
        (run_dir / f"metrics_lstm_{name}_{job}.json").write_text(
            json.dumps(metrics, indent=2), encoding="utf-8")
        print(f"[lstm_{name}/{job}] QLIKE(mean-forecast)="
              f"{metrics['qlike_mean_forecast']:.5f} n={len(tw)} "
              f"best_epochs={epochs_seen}")


def run_baselines(df: pd.DataFrame, run_dir: Path) -> None:
    dates = df["date"].to_numpy()
    log_rv = df["log_rv"].to_numpy()
    closes = df["close"].to_numpy()
    log_rv_s = pd.Series(log_rv, index=pd.DatetimeIndex(dates))

    windows = [("val", cfg.VAL_START, cfg.VAL_END, cfg.DEV_END),
               ("test", cfg.TEST_START, cfg.TEST_END, cfg.TRAIN_POOL_END)]
    for job, w_start, w_end, fit_end in windows:
        w_mask = (dates >= np.datetime64(w_start)) & (dates <= np.datetime64(w_end))
        w_dates = dates[w_mask]
        y_true = log_rv[w_mask]

        persistence = log_rv_s.shift(1).reindex(pd.DatetimeIndex(w_dates)).to_numpy()
        assert not np.isnan(persistence).any(), f"persistence NaN di {job}"

        td, har_pred, beta = sm.har_fit_predict(log_rv, dates, np.datetime64(fit_end))
        har_s = pd.Series(har_pred, index=pd.DatetimeIndex(td)).reindex(
            pd.DatetimeIndex(w_dates)).to_numpy()
        assert not np.isnan(har_s).any(), f"HAR NaN di {job}"

        garch = sm.garch_forecasts(dates, closes, w_start, w_end)
        garch_s = (garch.set_index("date")["log_var"]
                   .reindex(pd.DatetimeIndex(w_dates)).to_numpy())
        assert not np.isnan(garch_s).any(), f"GARCH NaN di {job}"

        out = pd.DataFrame({"date": w_dates, "y_true": y_true,
                            "persistence": persistence, "har_rv": har_s,
                            "garch11": garch_s})
        out.to_csv(run_dir / f"predictions_baselines_{job}.csv", index=False)

        metrics = {"window": f"{w_start}..{w_end}", "n_eval": int(len(w_dates))}
        for name, preds in [("persistence", persistence), ("har_rv", har_s),
                            ("garch11", garch_s)]:
            metrics[name] = {"qlike": qlike(y_true, preds),
                             **mae_rmse_logrv(y_true, preds)}
        (run_dir / f"metrics_baselines_{job}.json").write_text(
            json.dumps(metrics, indent=2), encoding="utf-8")
        print(f"[baselines/{job}] " + " ".join(
            f"{k}={v['qlike']:.5f}" for k, v in metrics.items() if isinstance(v, dict)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hpo_run", type=Path, required=True)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    verify_gate()
    df = sd.load_daily()
    seeds = cfg.SEEDS if not args.smoke else [42, 123]
    run_id, run_dir = s2_runlog.new_run(
        "final_smoke" if args.smoke else "final",
        {"hpo_run": str(args.hpo_run), "seeds": list(seeds), "smoke": args.smoke})

    run_baselines(df, run_dir)
    untuned = dict(cfg.UNTUNED_LSTM)
    run_lstm_variant("untuned", untuned, df, seeds, args.smoke, run_dir)
    best_params = load_best_params(args.hpo_run)
    run_lstm_variant("optuna", best_params, df, seeds, args.smoke, run_dir)
    print(f"[done] artifacts in {run_dir}")


if __name__ == "__main__":
    main()
