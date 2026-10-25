"""
01_fetch_binance_data.py - Data acquisition and temporal quality audit.

Downloads daily BTC/USDT klines from the Binance public REST API, validates
that the series is complete and internally consistent, and only then writes
the CSV. Partial downloads fail loudly instead of silently producing a short
dataset.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

import config
import run_utils

BASE_URL = "https://api.binance.com/api/v3/klines"
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_INTERVAL = "1d"
DEFAULT_START = config.DATASET_START_DATE
DEFAULT_END = config.DATASET_END_DATE


def _to_utc_millis(date_str: str) -> int:
    return int(
        datetime.strptime(date_str, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp()
        * 1000
    )


def fetch_binance_klines(
    symbol: str = DEFAULT_SYMBOL,
    interval: str = DEFAULT_INTERVAL,
    start_str: str = DEFAULT_START,
    end_str: str = DEFAULT_END,
    limit: int = 1000,
    max_retries: int = 5,
) -> pd.DataFrame:
    """Download paginated klines. Raise RuntimeError after exhausting retries."""
    start_ts = _to_utc_millis(start_str)
    end_ts = _to_utc_millis(end_str) + 86_399_999

    print(f"[1/4] Mengunduh data {symbol} interval {interval}")
    print(f"      Rentang: {start_str} s.d. {end_str}")

    all_data: list[list] = []
    current_start = start_ts
    call_count = 0

    while current_start <= end_ts:
        call_count += 1
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_ts,
            "limit": limit,
        }

        last_error: Exception | None = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(BASE_URL, params=params, timeout=30)
                if response.status_code == 429 or response.status_code >= 500:
                    raise requests.HTTPError(
                        f"HTTP {response.status_code}: {response.text[:200]}"
                    )
                response.raise_for_status()
                data = response.json()
                last_error = None
                break
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt == max_retries:
                    break
                wait_seconds = min(2 ** attempt, 30)
                print(
                    f"      [RETRY {attempt}/{max_retries}] Batch {call_count} gagal: "
                    f"{exc}. Menunggu {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

        if last_error is not None:
            raise RuntimeError(
                f"Gagal mengunduh batch {call_count} setelah {max_retries} percobaan: "
                f"{last_error}"
            ) from last_error

        if not data:
            break

        all_data.extend(data)
        last_open_time = int(data[-1][0])
        next_start = last_open_time + 86_400_000
        if next_start <= current_start:
            raise RuntimeError(
                f"API tidak memajukan waktu: current_start={current_start}, "
                f"next_start={next_start}"
            )
        current_start = next_start

        print(
            f"      Batch {call_count}: {len(data)} lilin "
            f"(total {len(all_data)})"
        )
        time.sleep(0.2)

    if not all_data:
        raise RuntimeError("API Binance tidak mengembalikan data apa pun.")

    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore",
    ]
    df = pd.DataFrame(all_data, columns=columns)
    df["datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")

    numeric_cols = [
        "open", "high", "low", "close", "volume", "quote_asset_volume",
        "number_of_trades",
    ]
    for column in numeric_cols:
        df[column] = pd.to_numeric(df[column], errors="raise")

    df = df[(df["date"] >= start_str) & (df["date"] <= end_str)].copy()
    df = df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


def validate_dataset(
    df: pd.DataFrame,
    start_str: str = DEFAULT_START,
    end_str: str = DEFAULT_END,
    expected_rows: int | None = None,
) -> pd.DataFrame:
    """Fail on incomplete or inconsistent data before it reaches the pipeline."""
    required = {"date", "open", "high", "low", "close", "volume"}
    missing_columns = required.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ada: {sorted(missing_columns)}")

    work = df.copy()
    work["date"] = pd.to_datetime(work["date"], errors="raise")
    work = work.sort_values("date").reset_index(drop=True)

    expected_dates = pd.date_range(start=start_str, end=end_str, freq="D")
    expected_count = expected_rows if expected_rows is not None else len(expected_dates)
    if len(work) != expected_count:
        raise ValueError(
            f"Jumlah baris tidak lengkap: {len(work)} (diharapkan {expected_count})"
        )

    duplicate_count = int(work["date"].duplicated().sum())
    if duplicate_count:
        raise ValueError(f"Terdapat {duplicate_count} tanggal duplikat")

    missing_dates = expected_dates.difference(pd.DatetimeIndex(work["date"]))
    if len(missing_dates):
        preview = ", ".join(date.strftime("%Y-%m-%d") for date in missing_dates[:5])
        raise ValueError(f"Terdapat {len(missing_dates)} tanggal hilang: {preview}")

    null_counts = work[["open", "high", "low", "close", "volume"]].isna().sum()
    if int(null_counts.sum()):
        raise ValueError(f"Nilai kosong ditemukan: {null_counts[null_counts > 0].to_dict()}")

    ohlc_violations = work[
        (work["high"] < work["open"])
        | (work["high"] < work["close"])
        | (work["low"] > work["open"])
        | (work["low"] > work["close"])
        | (work["high"] < work["low"])
        | (work[["open", "high", "low", "close"]] <= 0).any(axis=1)
    ]
    if len(ohlc_violations):
        raise ValueError(
            f"Terdapat {len(ohlc_violations)} pelanggaran relasi OHLC/harga non-positif"
        )

    return work.drop(columns=["datetime"], errors="ignore")


def audit_dataset(df: pd.DataFrame) -> dict:
    """Print and return a compact quality report."""
    print("\n[2/4] Audit kualitas data temporal:")
    print(f"      - Total observasi harian: {len(df)} baris")
    print(f"      - Periode aktual: {df['date'].min():%Y-%m-%d} s.d. {df['date'].max():%Y-%m-%d}")

    null_counts = int(df[["open", "high", "low", "close", "volume"]].isna().sum().sum())
    ohlc_violations = int(
        (
            (df["high"] < df["open"])
            | (df["high"] < df["close"])
            | (df["low"] > df["open"])
            | (df["low"] > df["close"])
        ).sum()
    )
    gaps = int((df["date"].diff() > pd.Timedelta(days=1)).sum())

    print(f"      - Nilai kosong: {null_counts} (harus 0)")
    print(f"      - Pelanggaran OHLC: {ohlc_violations} (harus 0)")
    print(f"      - Celah tanggal: {gaps} (harus 0)")

    print("\n[3/4] Ringkasan statistik close BTC/USDT:")
    print(f"      - Minimum : USD {df['close'].min():,.2f} ({df.loc[df['close'].idxmin(), 'date']:%Y-%m-%d})")
    print(f"      - Maksimum: USD {df['close'].max():,.2f} ({df.loc[df['close'].idxmax(), 'date']:%Y-%m-%d})")
    print(f"      - Rata-rata: USD {df['close'].mean():,.2f}")
    print(f"      - Median   : USD {df['close'].median():,.2f}")
    print(f"      - Std. dev : USD {df['close'].std():,.2f}")

    return {
        "rows": len(df),
        "start_date": df["date"].min().strftime("%Y-%m-%d"),
        "end_date": df["date"].max().strftime("%Y-%m-%d"),
        "null_values": null_counts,
        "ohlc_violations": ohlc_violations,
        "date_gaps": gaps,
        "close_min": float(df["close"].min()),
        "close_max": float(df["close"].max()),
        "close_mean": float(df["close"].mean()),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unduh dan validasi data harian Binance")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument("--interval", default=DEFAULT_INTERVAL)
    parser.add_argument("--start", default=DEFAULT_START)
    parser.add_argument("--end", default=DEFAULT_END)
    parser.add_argument("--expected-rows", type=int, default=None)
    parser.add_argument(
        "--reuse-local",
        action="store_true",
        help="Salin data mentah yang sudah ada (offline) alih-alih mengunduh",
    )
    parser.add_argument("--output", default=None, help="Path CSV keluaran eksplisit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="fetch")

    if paths.legacy:
        print("[WARNING] Mode legacy: file data mentah lama dapat tertimpa.")

    stage_config = {
        "stage": "fetch",
        "symbol": args.symbol,
        "interval": args.interval,
        "start": args.start,
        "end": args.end,
        "reuse_local": bool(args.reuse_local),
        "seed": args.seed,
    }

    if args.reuse_local:
        source = config.RAW_DATA_PATH
        if not source.exists():
            raise FileNotFoundError(f"Data lokal untuk --reuse-local tidak ada: {source}")
        print(f"[1/4] Menggunakan data lokal: {source}")
        df = pd.read_csv(source)
        df = validate_dataset(
            df,
            start_str=args.start,
            end_str=args.end,
            expected_rows=args.expected_rows,
        )
    else:
        df = fetch_binance_klines(
            symbol=args.symbol,
            interval=args.interval,
            start_str=args.start,
            end_str=args.end,
        )
        df = validate_dataset(
            df,
            start_str=args.start,
            end_str=args.end,
            expected_rows=args.expected_rows,
        )

    audit = audit_dataset(df)

    output_path = (
        Path(args.output)
        if args.output
        else paths.raw_dir / "BTCUSDT_daily_2020_2025.csv"
    )
    if paths.legacy and args.output is None:
        output_path = config.RAW_DATA_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "date", "open", "high", "low", "close", "volume",
        "quote_asset_volume", "number_of_trades",
    ]
    df[columns].to_csv(output_path, index=False)
    output_path_abs = output_path.resolve()

    print(f"\n[4/4] Data mentah tersimpan: {output_path_abs} ({len(df)} baris)")
    print("=" * 70)

    if not paths.legacy:
        config_payload = {**stage_config, "output": str(output_path_abs)}
        run_utils.bootstrap_run(paths, "fetch", config_payload)
        run_utils.record_stage(
            paths,
            "fetch",
            status="success",
            started_at=started_at,
            stage_config=config_payload,
            inputs={"raw_source": source} if args.reuse_local else None,
            outputs=[output_path_abs],
            extra={"audit": audit},
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
