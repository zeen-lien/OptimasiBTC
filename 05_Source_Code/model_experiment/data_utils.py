"""
data_utils.py — Shared Utilities for Model Experiments
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib


def load_raw_data(filepath=None):
    if filepath is None:
        filepath = os.path.join(
            r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "data", "raw", "BTCUSDT_daily_2020_2025.csv"
        )
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File data mentah tidak ditemukan: {filepath}")
    
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def split_temporal(df, train_ratio=0.80):
    total_len = len(df)
    train_size = int(total_len * train_ratio)
    train_df = df.iloc[:train_size].copy().reset_index(drop=True)
    test_df = df.iloc[train_size:].copy().reset_index(drop=True)
    return train_df, test_df


def create_sequences(series, lookback):
    """
    Membentuk pasangan sekuen X (lookback steps) dan target y (1 step ke depan).
    Input:
      series: 1D array bernilai ternormalisasi
      lookback: integer L (panjang jendela historis)
    Output:
      X: 3D array berdimensi (samples, lookback, 1)
      y: 1D array berdimensi (samples,)
    """
    X, y = [], []
    for i in range(len(series) - lookback):
        X.append(series[i : i + lookback])
        y.append(series[i + lookback])
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y


def load_processed_data():
    """
    Memuat data train dan test yang telah dipartisi beserta fit scaler.
    """
    proc_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "data", "processed")
    train_df = pd.read_csv(os.path.join(proc_dir, "train_insample.csv"))
    test_df = pd.read_csv(os.path.join(proc_dir, "test_outofsample.csv"))
    scaler = joblib.load(os.path.join(proc_dir, "minmax_scaler.joblib"))
    return train_df, test_df, scaler
