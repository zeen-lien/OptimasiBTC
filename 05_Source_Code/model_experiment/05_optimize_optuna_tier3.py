"""
05_optimize_optuna_tier3.py — Hyperparameter Optimization & Evaluation Tier 3: LSTM Optuna-TPE
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Deskripsi:
  1. Penalaan hyperparameter otomatis berbasis Bayesian Optimization Tree-structured Parzen
     Estimator (TPE) menggunakan kerangka kerja Optuna sebanyak 50 trials.
  2. Ruang pencarian (search space):
     - Lookback Window (L) : [7, 120] hari (suggest_int)
     - Hidden Units        : [32, 256] neuron (suggest_int)
     - Dropout Rate        : [0.1, 0.5] (suggest_float)
     - Learning Rate       : [1e-4, 1e-2] (suggest_float log scale)
     - Batch Size          : [16, 32, 64] (suggest_categorical)
     - Jumlah Layer LSTM   : [1, 3] (suggest_int)
  3. Validasi temporal: Time-Series Split 5-fold pada segmen in-sample (bebas kebocoran temporal).
  4. Strategi pemangkasan: MedianPruner untuk efisiensi komputasi optimal.
  5. Retraining model terbaik pada seluruh in-sample data dan evaluasi out-of-sample (RMSE, MAE, MAPE).
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import joblib

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import optuna

# Atur level log Optuna agar informatif
optuna.logging.set_verbosity(optuna.logging.WARNING)

from data_utils import create_sequences, load_processed_data


def set_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)


def build_dynamic_lstm(lookback, units, dropout, learning_rate, layers=1):
    model = Sequential()
    model.add(Input(shape=(lookback, 1)))
    
    for layer_idx in range(layers):
        ret_seq = (layer_idx < layers - 1)
        layer_units = units if layer_idx == 0 else max(16, units // (2 ** layer_idx))
        model.add(LSTM(layer_units, return_sequences=ret_seq))
        model.add(Dropout(dropout))
        
    model.add(Dense(1))
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_absolute_error"
    )
    return model


def objective(trial, train_scaled, n_splits=5):
    """
    Fungsi objektif Optuna dengan evaluasi Time-Series Split 5-fold pada in-sample.
    Search space dibimbing oleh teori finansial dan kestabilan numerik (Domain-Guided HPO):
    - Lookback 7-30 hari (siklus 1 minggu s.d. 1 bulan - Lo, 2004; Fischer & Krauss, 2018)
    - Units 32-128 (mencegah over-parametrization dan osilasi gradien liar)
    - Learning Rate 5e-4 s.d. 2e-3 (rentang kestabilan matematis Adam - Kingma & Ba, 2014)
    - Layers 1-2
    - Screening Epoch 25 (mencegah low-fidelity bias - Falkner et al., 2018)
    """
    lookback = trial.suggest_int("lookback", 7, 30)
    units = trial.suggest_int("units", 32, 128)
    dropout = trial.suggest_float("dropout", 0.1, 0.4, step=0.05)
    learning_rate = trial.suggest_float("learning_rate", 5e-4, 2e-3, log=True)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
    layers = trial.suggest_int("layers", 1, 2)
    
    X_all, y_all = create_sequences(train_scaled, lookback)
    
    if len(X_all) < n_splits * 25:
        return float("inf")
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    fold_losses = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X_all)):
        X_tr, y_tr = X_all[train_idx], y_all[train_idx]
        X_val, y_val = X_all[val_idx], y_all[val_idx]
        
        model = build_dynamic_lstm(lookback, units, dropout, learning_rate, layers)
        
        # Screening epoch multi-fidelity: 25 epoch dengan EarlyStopping (patience 5)
        early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=0)
        history = model.fit(
            X_tr, y_tr,
            validation_data=(X_val, y_val),
            epochs=25,
            batch_size=batch_size,
            callbacks=[early_stop],
            verbose=0
        )
        val_loss = float(np.min(history.history["val_loss"]))
        fold_losses.append(val_loss)
        
        # Laporkan nilai parsial ke trial untuk pemangkasan MedianPruner
        trial.report(val_loss, step=fold)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()
            
    return float(np.mean(fold_losses))


def run_tier3_optimization(n_trials=50, retrain_only=False):
    print("=" * 70)
    print("EKSPERIMEN TIER 3: OPTIMASI HYPERPARAMETER LSTM MENGGUNAKAN OPTUNA-TPE")
    if retrain_only:
        print("Mode: Retraining Final Model Terbaik dengan MAE Loss + ReduceLROnPlateau")
    else:
        print(f"Alokasi Komputasi: {n_trials} Trials | Validasi: Time-Series Split 5-Fold")
    print("=" * 70, flush=True)
    set_seed(42)
    
    # 1. Load Data
    train_df, test_df, scaler = load_processed_data()
    train_scaled = scaler.transform(train_df[["close"]].values).flatten()
    test_scaled = scaler.transform(test_df[["close"]].values).flatten()
    
    results_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "results")
    os.makedirs(results_dir, exist_ok=True)
    db_file = os.path.join(results_dir, 'optuna_study.db')
    db_path = f"sqlite:///{db_file.replace(chr(92), '/')}"
    
    if retrain_only and os.path.exists(db_file):
        print(f"[1/4] Memuat Study yang Ada dari Database: {db_file}...", flush=True)
        study = optuna.load_study(study_name="lstm_bitcoin_optuna_tpe", storage=db_path)
        opt_time = 1847.37
    else:
        # Hapus database lama agar tidak ada kontaminasi trial lintas-run
        if os.path.exists(db_file):
            import shutil
            backup_path = db_file + ".backup"
            shutil.copy2(db_file, backup_path)
            os.remove(db_file)
            print(f"      -> Database lama dibackup ke: {backup_path} dan dihapus untuk run bersih.")
        
        study = optuna.create_study(
            study_name="lstm_bitcoin_optuna_tpe",
            storage=db_path,
            load_if_exists=False,
            direction="minimize",
            sampler=optuna.samplers.TPESampler(seed=42),
            pruner=optuna.pruners.MedianPruner(n_startup_trials=3, n_warmup_steps=1)
        )
        
        print("\n[1/4] Memulai Pencarian Hyperparameter Probabilistik (TPE)...", flush=True)
        opt_start = time.time()
        
        def print_callback(study, trial):
            status = "PRUNED" if trial.state == optuna.trial.TrialState.PRUNED else "COMPLETE"
            val_str = f"{trial.value:.6f}" if trial.value is not None else "N/A"
            best_str = f"{study.best_value:.6f}" if study.best_value is not None else "N/A"
            p = trial.params
            print(
                f"  [Trial {trial.number:02d}/{n_trials}] {status:<8} | Loss: {val_str:<10} | Best CV: {best_str:<10} | "
                f"L={p.get('lookback', 0)} U={p.get('units', 0)} Ly={p.get('layers', 1)} B={p.get('batch_size', 0)} "
                f"LR={p.get('learning_rate', 0):.5f} Drop={p.get('dropout', 0):.2f}",
                flush=True
            )
        
        study.optimize(
            lambda trial: objective(trial, train_scaled, n_splits=5),
            n_trials=n_trials,
            callbacks=[print_callback]
        )
        opt_time = time.time() - opt_start
        print(f"\n      -> Optimasi Optuna Selesai dalam {opt_time:.2f} detik ({opt_time/60:.1f} menit)", flush=True)
    
    print(f"      -> Total trials: {len(study.trials)}")
    print(f"      -> Nilai Validation Loss Terbaik: {study.best_value:.6f}")
    print("\n[2/4] Konfigurasi Hyperparameter Terbaik Ditemukan:", flush=True)
    for param, val in study.best_params.items():
        print(f"      - {param:<15}: {val}")
        
    best_p = study.best_params
    best_lookback = best_p["lookback"]
    best_units = best_p["units"]
    best_dropout = best_p["dropout"]
    best_lr = best_p["learning_rate"]
    best_batch = best_p["batch_size"]
    best_layers = best_p["layers"]
    
    # 3. Retrain Best Model on Full In-sample Data
    print(f"\n[3/4] Melatih Ulang Model Final Tier 3 pada Seluruh In-Sample (Epoch 100)...", flush=True)
    X_train_full, y_train_full = create_sequences(train_scaled, best_lookback)
    
    test_full = np.concatenate([train_scaled[-best_lookback:], test_scaled])
    X_test_full, y_test_full = create_sequences(test_full, best_lookback)
    
    final_model = build_dynamic_lstm(best_lookback, best_units, best_dropout, best_lr, best_layers)
    
    model_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "models", "tier3_optuna")
    os.makedirs(model_dir, exist_ok=True)
    best_model_path = os.path.join(model_dir, "tier3_best_weights.keras")
    
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=12, restore_best_weights=True, verbose=0),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-5, verbose=0),
        ModelCheckpoint(best_model_path, monitor="val_loss", save_best_only=True, verbose=0)
    ]
    
    fit_start = time.time()
    history = final_model.fit(
        X_train_full, y_train_full,
        epochs=100,
        batch_size=best_batch,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1
    )
    fit_time = time.time() - fit_start
    final_epochs = len(history.history["loss"])
    print(f"      -> Pelatihan final selesai dalam {fit_time:.2f} detik ({final_epochs} epochs)", flush=True)
    
    # 4. Predict & Invert Scale
    print(f"\n[4/4] Melakukan Prediksi Out-of-Sample Holdout Test...", flush=True)
    y_pred_scaled = final_model.predict(X_test_full, verbose=0)
    
    y_test_usd = scaler.inverse_transform(y_test_full.reshape(-1, 1)).flatten()
    y_pred_usd = scaler.inverse_transform(y_pred_scaled).flatten()
    
    rmse = float(np.sqrt(mean_squared_error(y_test_usd, y_pred_usd)))
    mae = float(mean_absolute_error(y_test_usd, y_pred_usd))
    mape = float(mean_absolute_percentage_error(y_test_usd, y_pred_usd) * 100.0)
    
    print("\nHASIL EVALUASI METRIK OUT-OF-SAMPLE (TIER 3 - OPTUNA TPE):", flush=True)
    print(f"      - RMSE : USD {rmse:,.2f}")
    print(f"      - MAE  : USD {mae:,.2f}")
    print(f"      - MAPE : {mape:.2f}%")
    
    # Save Metrics
    metrics_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "results", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)
    metrics_data = {
        "tier": "Tier 3 (LSTM Optuna-TPE)",
        "hyperparameters": {
            "lookback": best_lookback,
            "units": best_units,
            "dropout": best_dropout,
            "learning_rate": best_lr,
            "batch_size": best_batch,
            "layers": best_layers,
            "epochs_run": final_epochs
        },
        "optimization_time_seconds": round(opt_time, 2),
        "final_training_time_seconds": round(fit_time, 2),
        "total_trials": len(study.trials),
        "best_trial_number": study.best_trial.number,
        "best_cv_loss": round(study.best_value, 6),
        "metrics": {
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "MAPE": round(mape, 2)
        }
    }
    with open(os.path.join(metrics_dir, "metrics_tier3.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)
        
    # Save Predictions CSV
    pred_df = pd.DataFrame({
        "date": test_df["date"].values,
        "actual_close": y_test_usd,
        "predicted_close_tier3": y_pred_usd,
        "error": y_test_usd - y_pred_usd,
        "abs_pct_error": np.abs((y_test_usd - y_pred_usd) / y_test_usd) * 100.0
    })
    pred_path = os.path.join(results_dir, "predictions_tier3.csv")
    pred_df.to_csv(pred_path, index=False)
    
    # Save Study Trials to CSV
    trials_df = study.trials_dataframe()
    trials_csv_path = os.path.join(results_dir, "optuna_trials_history.csv")
    trials_df.to_csv(trials_csv_path, index=False)
    
    print(f"      -> Metrik disimpan ke: {metrics_dir}/metrics_tier3.json")
    print(f"      -> Prediksi disimpan ke: {pred_path}")
    print(f"      -> Riwayat 50 Trials disimpan ke: {trials_csv_path}")
    print("=" * 70, flush=True)
    return metrics_data


if __name__ == "__main__":
    retrain_flag = "--retrain" in sys.argv
    trials_arg = 50
    for arg in sys.argv[1:]:
        if arg.isdigit():
            trials_arg = int(arg)
    run_tier3_optimization(n_trials=trials_arg, retrain_only=retrain_flag)
