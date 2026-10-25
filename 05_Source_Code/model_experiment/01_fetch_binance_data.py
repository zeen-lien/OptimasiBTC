"""
01_fetch_binance_data.py — Data Acquisition Pipeline
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Deskripsi:
  Mengunduh data historis candlestick harian (daily OHLCV) pasangan BTC/USDT dari
  Binance Public REST API (/api/v3/klines) periode 1 Januari 2020 s.d. 31 Desember 2025.
  Dilengkapi prosedur audit kualitas data temporal (cek missing values, relasi OHLC, dsb).
"""

import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone


def fetch_binance_klines(
    symbol="BTCUSDT",
    interval="1d",
    start_str="2020-01-01",
    end_str="2025-12-31",
    limit=1000
):
    """
    Mengunduh candlestick harian BTC/USDT secara terpaginasi dari Binance Spot API.
    """
    base_url = "https://api.binance.com/api/v3/klines"
    
    # Konversi string tanggal ke millisecond timestamp (UTC)
    start_ts = int(datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_ts = int(datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000) + 86399999
    
    print(f"[1/4] Menginisiasi pengunduhan data {symbol} interval {interval}")
    print(f"      Rentang: {start_str} s.d. {end_str}")
    
    all_data = []
    current_start = start_ts
    call_count = 0
    
    while current_start < end_ts:
        call_count += 1
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_ts,
            "limit": limit
        }
        
        try:
            resp = requests.get(base_url, params=params, timeout=15)
            if resp.status_code != 200:
                print(f"[ERROR] HTTP {resp.status_code}: {resp.text}")
                break
            
            data = resp.json()
            if not data:
                break
            
            all_data.extend(data)
            last_open_time = data[-1][0]
            
            # Update current_start untuk batch berikutnya (tambah 1 hari)
            next_start = last_open_time + (24 * 60 * 60 * 1000)
            if next_start <= current_start:
                break
            current_start = next_start
            
            print(f"      Batch {call_count}: Diperoleh {len(data)} lilin (Total akumulasi: {len(all_data)})")
            time.sleep(0.2)  # Menghindari rate-limiting
            
        except Exception as e:
            print(f"[EXCEPTION] Gagal mengunduh batch: {e}")
            break
            
    # Format ke DataFrame
    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]
    df = pd.DataFrame(all_data, columns=columns)
    
    # Konversi timestamp dan tipe numerik
    df["datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")
    
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume"]
    for col in numeric_cols:
        df[col] = df[col].astype(float)
        
    # Filter rentang tanggal ketat
    df = df[(df["date"] >= start_str) & (df["date"] <= end_str)].copy()
    df = df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    return df


def audit_dataset(df):
    """
    Melakukan audit kualitas data temporal sesuai protokol Bab 3 Skripsi.
    """
    print("\n[2/4] Menjalankan Audit Kualitas Data Temporal:")
    print(f"      - Total observasi harian: {len(df)} baris")
    print(f"      - Periode aktual: {df['date'].min()} s.d. {df['date'].max()}")
    
    # 1. Missing Values
    null_counts = df[["open", "high", "low", "close", "volume"]].isnull().sum().sum()
    print(f"      - Nilai Kosong (NaN / Null): {null_counts} (Harus 0)")
    
    # 2. Cek Relasi Geometris Candlestick: High >= Open, Close and Low <= Open, Close
    ohlc_violations = df[
        (df["high"] < df["open"]) |
        (df["high"] < df["close"]) |
        (df["low"] > df["open"]) |
        (df["low"] > df["close"])
    ]
    print(f"      - Pelanggaran Relasi Harga OHLC: {len(ohlc_violations)} baris (Harus 0)")
    
    # 3. Cek Kontinuitas Tanggal (Celah Waktu / Date Gaps)
    df["dt"] = pd.to_datetime(df["date"])
    date_diffs = df["dt"].diff()
    gaps = date_diffs[date_diffs > pd.Timedelta(days=1)]
    print(f"      - Celah Waktu Tanggal (Date Gaps): {len(gaps)} (Harus 0)")
    
    # 4. Ringkasan Statistik Harga
    print("\n[3/4] Ringkasan Statistik Harga Penutupan (Close BTC/USDT):")
    print(f"      - Harga Minimum : USD {df['close'].min():,.2f} ({df.loc[df['close'].idxmin(), 'date']})")
    print(f"      - Harga Maksimum: USD {df['close'].max():,.2f} ({df.loc[df['close'].idxmax(), 'date']})")
    print(f"      - Rata-rata     : USD {df['close'].mean():,.2f}")
    print(f"      - Median        : USD {df['close'].median():,.2f}")
    print(f"      - Simpangan Baku: USD {df['close'].std():,.2f}")


def main():
    print("=" * 70)
    print("PIPELINE DATA 01: PENGUNDUHAN & AUDIT DATA HISTORIS BINANCE API")
    print("=" * 70)
    
    df = fetch_binance_klines(
        symbol="BTCUSDT",
        interval="1d",
        start_str="2020-01-01",
        end_str="2025-12-31"
    )
    
    audit_dataset(df)
    
    # Simpan ke CSV
    out_dir = os.path.join(r"d:\OneDrive\Desktop\jurnal", "05_Source_Code", "data", "raw")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BTCUSDT_daily_2020_2025.csv")
    
    cols_to_save = ["date", "open", "high", "low", "close", "volume", "quote_asset_volume", "number_of_trades"]
    df[cols_to_save].to_csv(out_path, index=False)
    
    print(f"\n[4/4] Data mentah berhasil disimpan ke:")
    print(f"      -> {out_path} ({len(df)} baris)")
    print("=" * 70)
    return out_path


if __name__ == "__main__":
    main()
