"""
02_preprocessing.py — Data Preprocessing & Sequence Windowing Pipeline
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Deskripsi:
  1. Memuat dataset bersih BTC/USDT hasil unduhan dari Binance API.
  2. Partisi temporal 80:20 (In-Sample 80% vs Out-of-Sample 20% holdout test set).
  3. Penskalaan fitur Min-Max [0, 1] dengan protokol anti-data leakage (fit on train, transform on test).
  4. Penyediaan fungsi pembentukan jendela sekuensial (Sliding Window: X = L timesteps, y = t+1).
  5. Penyimpanan artefak prapemrosesan ke dalam folder data/processed/.
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
    """
    Membagi dataset secara kronologis murni (80% in-sample, 20% out-of-sample).
    """
    total_len = len(df)
    train_size = int(total_len * train_ratio)
    
    train_df = df.iloc[:train_size].copy().reset_index(drop=True)
    test_df = df.iloc[train_size:].copy().reset_index(drop=True)
    
    return train_df, test_df


def fit_scaler(train_df):
    """
    Melakukan fitting MinMaxScaler HANYA pada data in-sample (anti-leakage).
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(train_df[["close"]].values)
    return scaler


def transform_data(scaler, df):
    """
    Mentransformasikan data Close menggunakan scaler yang telah di-fit.
    """
    scaled_values = scaler.transform(df[["close"]].values)
    return scaled_values.flatten()


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
    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y


def prepare_and_save_data():
    print("=" * 70)
    print("PIPELINE DATA 02: PRAPEMROSESAN & PARTISI TEMPORAL BEBAS BOCOR")
    print("=" * 70)
    
    df = load_raw_data()
    total_obs = len(df)
    print(f"[1/4] Data mentah berhasil dimuat: {total_obs} observasi")
    print(f"      Rentang: {df['date'].min().strftime('%Y-%m-%d')} s.d. {df['date'].max().strftime('%Y-%m-%d')}")
    
    # Partisi 80:20
    train_df, test_df = split_temporal(df, train_ratio=0.80)
    n_train = len(train_df)
    n_test = len(test_df)
    
    print(f"\n[2/4] Partisi Temporal (80:20):")
    print(f"      - In-Sample (Train+Val) : {n_train} observasi ({n_train/total_obs*100:.1f}%)")
    print(f"        Periode: {train_df['date'].min().strftime('%Y-%m-%d')} s.d. {train_df['date'].max().strftime('%Y-%m-%d')}")
    print(f"      - Out-of-Sample (Test)   : {n_test} observasi ({n_test/total_obs*100:.1f}%)")
    print(f"        Periode: {test_df['date'].min().strftime('%Y-%m-%d')} s.d. {test_df['date'].max().strftime('%Y-%m-%d')}")
    
    # Fit Scaler pada In-Sample
    scaler = fit_scaler(train_df)
    train_scaled = transform_data(scaler, train_df)
    test_scaled = transform_data(scaler, test_df)
    
    print(f"\n[3/4] Penskalaan Fitur Min-Max Scaling (Anti-Data Leakage):")
    print(f"      - x_min (data latih): USD {scaler.data_min_[0]:,.2f}")
    print(f"      - x_max (data latih): USD {scaler.data_max_[0]:,.2f}")
    print(f"      - Skala konversi   : [0.0, 1.0]")
    
    # Simpan hasil prapemrosesan
    proc_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "data", "processed")
    os.makedirs(proc_dir, exist_ok=True)
    
    # 1. Simpan CSV partisi
    train_df.to_csv(os.path.join(proc_dir, "train_insample.csv"), index=False)
    test_df.to_csv(os.path.join(proc_dir, "test_outofsample.csv"), index=False)
    
    # 2. Simpan scaler
    scaler_path = os.path.join(proc_dir, "minmax_scaler.joblib")
    joblib.dump(scaler, scaler_path)
    
    # 3. Simpan metadata
    metadata = {
        "total_observations": total_obs,
        "n_train_insample": n_train,
        "n_test_outofsample": n_test,
        "train_start_date": train_df["date"].min().strftime("%Y-%m-%d"),
        "train_end_date": train_df["date"].max().strftime("%Y-%m-%d"),
        "test_start_date": test_df["date"].min().strftime("%Y-%m-%d"),
        "test_end_date": test_df["date"].max().strftime("%Y-%m-%d"),
        "scaler_min": float(scaler.data_min_[0]),
        "scaler_max": float(scaler.data_max_[0]),
    }
    meta_path = os.path.join(proc_dir, "preprocessing_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"\n[4/4] Artefak Prapemrosesan Berhasil Disimpan ke:")
    print(f"      -> {proc_dir}/train_insample.csv")
    print(f"      -> {proc_dir}/test_outofsample.csv")
    print(f"      -> {proc_dir}/minmax_scaler.joblib")
    print(f"      -> {proc_dir}/preprocessing_metadata.json")
    print("=" * 70)


if __name__ == "__main__":
    prepare_and_save_data()
