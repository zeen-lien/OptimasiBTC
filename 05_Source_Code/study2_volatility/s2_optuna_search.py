"""[BAB 3 §3.6 | OPTIMASI HIPERPARAMETER DENGAN OPTUNA (TPE)]

Modul pencarian hiperparameter resmi untuk model usulan Study 2 (Protokol Bagian 5):
- Algoritma: Tree-structured Parzen Estimator (TPE, Bergstra et al. 2011) seed 42, 50 trials.
- Mekanisme pemangkasan: MedianPruner (startup=10, warmup=2) untuk efisiensi komputasi.
- Fungsi objektif: Rerata kerugian QLIKE (Patton 2011) pada 5 fold purged rolling-origin CV.
- Isolasi data: CSV harian dimuat penuh, tetapi seluruh baris setelah `DEV_END` (2023-12-31)
  dibuang sebelum pembentukan sampel. Data 2024–2026 tidak pernah dipakai untuk memilih
  hyperparameter, menghitung objektif CV, atau menentukan model final.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

import s2_config as cfg
import s2_models as sm
import s2_runlog
from s2_stats import qlike


def sample_params(trial: optuna.Trial) -> dict:
    """
    [BAB 3 §3.6 | RUANG PENCARIAN HIPERPARAMETER]
    Mengambil sampel nilai konfigurasi arsitektur dari search space praregistrasi:
    lookback (10-30), units (16-128), layers (1-2), dropout (0.05-0.40),
    learning rate (3e-4 s.d. 2e-3 log scale), dan batch size (16, 32, 64).
    """
    ss = cfg.SEARCH_SPACE
    return {
        "lookback": trial.suggest_int("lookback", ss["lookback"]["low"], ss["lookback"]["high"]),
        "units": trial.suggest_int("units", ss["units"]["low"], ss["units"]["high"]),
        "layers": trial.suggest_categorical("layers", ss["layers"]["choices"]),
        "dropout": trial.suggest_float("dropout", ss["dropout"]["low"], ss["dropout"]["high"],
                                       step=ss["dropout"]["step"]),
        "learning_rate": trial.suggest_float("learning_rate", ss["learning_rate"]["low"],
                                             ss["learning_rate"]["high"], log=True),
        "batch_size": trial.suggest_categorical("batch_size", ss["batch_size"]["choices"]),
    }


def cv_qlike(params: dict, dev: pd.DataFrame, max_epochs: int, verbose: bool = True):
    """
    [BAB 3 §3.6 | CROSS-VALIDATION PURGED ROLLING-ORIGIN]
    Mengevaluasi kombinasi hiperparameter pada 5 lipatan dev dengan TimeSeriesSplit.
    Scaler fit murni pada lipatan train; prediksi di-inverse transform ke skala asli sebelum skor QLIKE dihitung.
    """
    lookback = params["lookback"]
    X, y, _, tdates = sm.build_samples(dev, lookback=lookback)
    splitter = TimeSeriesSplit(n_splits=cfg.N_CV_FOLDS, gap=lookback + 1)
    fold_scores = []
    for fold, (tr, va) in enumerate(splitter.split(X)):
        scaler_x, scaler_y = sm.fit_scaler(X[tr], y[tr])
        Xtr, ytr = sm.transform_xy(scaler_x, scaler_y, X[tr], y[tr])
        Xva, yva = sm.transform_xy(scaler_x, scaler_y, X[va], y[va])
        model, best_epoch = sm.train_one(Xtr, ytr, Xva, yva, params, seed=42,
                                         max_epochs=max_epochs)
        pred_log_rv = scaler_y.inverse_transform(model.predict(Xva, verbose=0)).reshape(-1)
        score = qlike(y[va], pred_log_rv)
        fold_scores.append({"fold": fold, "qlike": score, "best_epoch": best_epoch,
                            "n_train": int(len(tr)), "n_val": int(len(va))})
        if verbose:
            print(f"  fold {fold}: qlike={score:.5f} best_epoch={best_epoch} "
                  f"n_train={len(tr)} n_val={len(va)}", flush=True)
    return float(np.mean([f["qlike"] for f in fold_scores])), fold_scores


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    n_trials = 1 if args.smoke else cfg.N_TRIALS
    max_epochs = 2 if args.smoke else cfg.MAX_EPOCHS

    df = s2_data_load_dev()
    run_id, run_dir = s2_runlog.new_run(
        "optuna_smoke" if args.smoke else "optuna_hpo",
        {"n_trials": n_trials, "max_epochs": max_epochs, "dev_only": True},
    )

    log_path = run_dir / "logs" / "optuna.log"
    def logp(msg: str) -> None:
        print(msg, flush=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    sampler = optuna.samplers.TPESampler(seed=cfg.OPTUNA_SEED)
    pruner = optuna.pruners.MedianPruner(n_startup_trials=cfg.PRUNER_STARTUP_TRIALS,
                                         n_warmup_steps=cfg.PRUNER_WARMUP_STEPS)
    study = optuna.create_study(direction="minimize", sampler=sampler, pruner=pruner,
                                study_name="s2_qlike")
    trial_rows = []

    def objective(trial: optuna.Trial) -> float:
        params = sample_params(trial)
        logp(f"[trial {trial.number}] {json.dumps(params)}")
        lookback = params["lookback"]
        X, y, _, _ = sm.build_samples(df, lookback=lookback)
        splitter = TimeSeriesSplit(n_splits=cfg.N_CV_FOLDS, gap=lookback + 1)
        fold_scores, folds_meta = [], []
        for fold, (tr, va) in enumerate(splitter.split(X)):
            scaler_x, scaler_y = sm.fit_scaler(X[tr], y[tr])
            Xtr, ytr = sm.transform_xy(scaler_x, scaler_y, X[tr], y[tr])
            Xva, yva = sm.transform_xy(scaler_x, scaler_y, X[va], y[va])
            model, best_epoch = sm.train_one(Xtr, ytr, Xva, yva, params, seed=42,
                                             max_epochs=max_epochs)
            pred_log_rv = scaler_y.inverse_transform(
                model.predict(Xva, verbose=0)).reshape(-1)
            score = qlike(y[va], pred_log_rv)
            fold_scores.append(score)
            folds_meta.append({"fold": fold, "qlike": score, "best_epoch": best_epoch,
                               "n_train": int(len(tr)), "n_val": int(len(va))})
            trial.report(score, step=fold)
            if trial.should_prune():
                logp(f"[trial {trial.number}] pruned after fold {fold}")
                raise optuna.TrialPruned(f"pruned after fold {fold}")
        mean_q = float(np.mean(fold_scores))
        trial_rows.append({"trial": trial.number, **params, "mean_cv_qlike": mean_q,
                           **{f"fold{m['fold']}_qlike": m["qlike"] for m in folds_meta}})
        logp(f"[trial {trial.number}] mean_cv_qlike={mean_q:.5f} "
             f"folds={[round(s, 4) for s in fold_scores]}")
        return mean_q

    try:
        study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    finally:
        pd.DataFrame(trial_rows).to_csv(run_dir / "trials.csv", index=False)
        if len(study.trials) and study.best_trial is not None:
            best = {"best_trial": study.best_trial.number,
                    "best_params": study.best_trial.params,
                    "best_value": study.best_trial.value}
            (run_dir / "best_params.json").write_text(json.dumps(best, indent=2),
                                                      encoding="utf-8")
            logp(f"[best] trial {study.best_trial.number} "
                 f"params={json.dumps(study.best_trial.params)} "
                 f"value={study.best_trial.value:.5f}")

    # Full study record (incl. pruned trials).
    records = [{"number": t.number, "state": str(t.state),
                "params": t.params, "value": t.value} for t in study.trials]
    (run_dir / "study_all_trials.json").write_text(json.dumps(records, indent=2),
                                                   encoding="utf-8")


def s2_data_load_dev() -> pd.DataFrame:
    import s2_data as sd
    df = sd.load_daily()
    dev = df[df["date"] <= cfg.DEV_END].reset_index(drop=True)
    if dev["date"].max() != pd.Timestamp(cfg.DEV_END):
        raise AssertionError("Dev window boundary salah.")
    return dev


if __name__ == "__main__":
    main()
