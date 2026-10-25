"""
03_train_baseline_tier1.py — Training & Evaluation Tier 1: LSTM Default (Baseline Kontrol)
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Spesifikasi Konfigurasi Tier 1:
  - Lookback Window (L) : 30 hari
  - Hidden Units        : 50 neuron (1 layer LSTM)
  - Dropout Rate        : 0.2
  - Optimizer           : Adam (Learning Rate = 0.001)
  - Batch Size          : 32
  - Epochs              : 100 (EarlyStopping patience=10)
  - Loss Function       : Mean Squared Error (MSE)
"""

import os
import json
import time
import numpy as np
import pandas as pd
import joblib

# Suppress TensorFlow logging warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

from data_utils import create_sequences, load_processed_data


def set_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)


def build_tier1_model(lookback=30, units=50, dropout=0.2, learning_rate=0.001):
    model = Sequential([
        LSTM(units, input_shape=(lookback, 1), return_sequences=False),
        Dropout(dropout),
        Dense(1)
    ])
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_squared_error"
    )
    return model


def run_tier1_experiment():
    print("=" * 70)
    print("EKSPERIMEN TIER 1: LSTM DEFAULT (BASELINE KONTROL)")
    print("=" * 70)
    set_seed(42)
    
    # 1. Load Data & Scaler
    proc_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "data", "processed")
    train_df = pd.read_csv(os.path.join(proc_dir, "train_insample.csv"))
    test_df = pd.read_csv(os.path.join(proc_dir, "test_outofsample.csv"))
    scaler = joblib.load(os.path.join(proc_dir, "minmax_scaler.joblib"))
    
    train_scaled = scaler.transform(train_df[["close"]].values).flatten()
    test_scaled = scaler.transform(test_df[["close"]].values).flatten()
    
    lookback = 30
    batch_size = 32
    units = 50
    dropout = 0.2
    lr = 0.001
    epochs = 100
    
    print(f"[1/5] Membentuk Sekuen Data (Lookback = {lookback} hari):")
    # Training sequences
    X_train, y_train = create_sequences(train_scaled, lookback)
    
    # Testing sequences: sertakan L titik terakhir train agar semua titik test terprediksi
    test_full = np.concatenate([train_scaled[-lookback:], test_scaled])
    X_test, y_test = create_sequences(test_full, lookback)
    
    print(f"      - Dimensi X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"      - Dimensi X_test : {X_test.shape}, y_test : {y_test.shape}")
    print(f"      - Jumlah target uji (Out-of-Sample): {len(y_test)} hari")
    
    # 2. Build Model
    print(f"\n[2/5] Membangun Arsitektur LSTM Tier 1:")
    print(f"      - LSTM Layer: 1 layer ({units} units), Dropout={dropout}")
    print(f"      - Optimizer: Adam (LR={lr}), Batch Size={batch_size}")
    model = build_tier1_model(lookback, units, dropout, lr)
    model.summary(print_fn=lambda x: print(f"        {x}"))
    
    # Callbacks
    model_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "models", "tier1_baseline")
    os.makedirs(model_dir, exist_ok=True)
    best_weights_path = os.path.join(model_dir, "tier1_best_weights.keras")
    
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True, verbose=0),
        ModelCheckpoint(best_weights_path, monitor="val_loss", save_best_only=True, verbose=0)
    ]
    
    # 3. Train Model
    print(f"\n[3/5] Melatih Model Tier 1 (Epochs Max: {epochs}, Validation Split: 10%)...")
    start_time = time.time()
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1
    )
    training_time = time.time() - start_time
    actual_epochs = len(history.history["loss"])
    print(f"      -> Pelatihan selesai dalam {training_time:.2f} detik ({actual_epochs} epochs)")
    
    # 4. Predict & Invert Scale
    print(f"\n[4/5] Melakukan Prediksi pada Data Out-of-Sample (Holdout Test)...")
    y_pred_scaled = model.predict(X_test, verbose=0)
    
    # Inverse transform to USD
    y_test_usd = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    y_pred_usd = scaler.inverse_transform(y_pred_scaled).flatten()
    
    # 5. Evaluate Metrics
    rmse = float(np.sqrt(mean_squared_error(y_test_usd, y_pred_usd)))
    mae = float(mean_absolute_error(y_test_usd, y_pred_usd))
    mape = float(mean_absolute_percentage_error(y_test_usd, y_pred_usd) * 100.0)
    
    print("\n[5/5] HASIL EVALUASI METRIK OUT-OF-SAMPLE (TIER 1):")
    print(f"      - RMSE : USD {rmse:,.2f}")
    print(f"      - MAE  : USD {mae:,.2f}")
    print(f"      - MAPE : {mape:.2f}%")
    
    # Save Metrics
    metrics_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "results", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)
    metrics_data = {
        "tier": "Tier 1 (LSTM Default)",
        "hyperparameters": {
            "lookback": lookback,
            "units": units,
            "dropout": dropout,
            "learning_rate": lr,
            "batch_size": batch_size,
            "layers": 1,
            "epochs_run": actual_epochs
        },
        "training_time_seconds": round(training_time, 2),
        "metrics": {
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "MAPE": round(mape, 2)
        }
    }
    with open(os.path.join(metrics_dir, "metrics_tier1.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)
        
    # Save Predictions CSV
    pred_df = pd.DataFrame({
        "date": test_df["date"].values,
        "actual_close": y_test_usd,
        "predicted_close_tier1": y_pred_usd,
        "error": y_test_usd - y_pred_usd,
        "abs_pct_error": np.abs((y_test_usd - y_pred_usd) / y_test_usd) * 100.0
    })
    pred_path = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "results", "predictions_tier1.csv")
    pred_df.to_csv(pred_path, index=False)
    print(f"      -> Metrik disimpan ke: {metrics_dir}/metrics_tier1.json")
    print(f"      -> Prediksi disimpan ke: {pred_path}")
    print("=" * 70)
    return metrics_data


if __name__ == "__main__":
    run_tier1_experiment()
