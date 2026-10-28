"""
s2_data.py - Fetch, aggregate, verify, and freeze Study 2 data.

Pipeline (pre-registered in docs/STUDY2_PROTOCOL.md, hashed 2026-10-28):
1. Download Binance Vision monthly 1h klines BTCUSDT, 2020-01 .. 2026-09.
2. Parse each zip (handles ms vs us timestamps and optional header rows).
3. Aggregate to UTC-daily bars: exactly 24 hourly bars per day is REQUIRED.
4. Compute rv, log_rv, and the six pre-registered features.
5. Fail loudly on any integrity violation; then freeze CSV + hashes.

Run:
    python s2_data.py              # download if needed, build, verify, freeze
    python s2_data.py --verify     # only re-verify frozen artifacts
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

import s2_config as cfg


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
def download_month(month: str, dest_dir: Path, timeout: int = 120) -> dict:
    url = cfg.BINANCE_VISION_URL.format(month=month)
    dest = dest_dir / f"BTCUSDT-1h-{month}.zip"
    if dest.exists():
        r = requests.head(url, timeout=timeout)
        remote_size = int(r.headers.get("content-length", "0") or 0)
        if r.status_code == 200 and remote_size in (0, dest.stat().st_size):
            return {"month": month, "url": url, "bytes": dest.stat().st_size,
                    "sha256": cfg.sha256_file(dest), "cached": True}

    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return {"month": month, "url": url, "bytes": len(r.content),
            "sha256": cfg.sha256_file(dest), "cached": False}


def download_all(dest_dir: Path) -> list[dict]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    infos = []
    for month in cfg.MONTHS:
        info = download_month(month, dest_dir)
        infos.append(info)
        print(f"[fetch] {month}: {info['bytes']:,} bytes "
              f"({'cached' if info['cached'] else 'downloaded'})")
    return infos


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
KLINE_COLUMNS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "count",
    "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]


def load_month_zip(zip_path: Path) -> pd.DataFrame:
    """Read one monthly kline zip into a normalized UTC-indexed frame."""
    with zipfile.ZipFile(zip_path) as zf:
        inner = zf.namelist()[0]
        with zf.open(inner) as f:
            df = pd.read_csv(f, header=None, names=KLINE_COLUMNS)

    # Drop a header row if the file happens to include one.
    first = str(df.iloc[0, 0])
    if not first.lstrip("-").isdigit():
        df = df.iloc[1:].reset_index(drop=True)

    df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="raise")

    ts = df["open_time"].astype("int64")
    # Binance Vision mixes milliseconds (older dumps) and microseconds (newer).
    if ts.max() > 10 ** 14:  # microseconds
        ts = ts // 1000
    df["open_time"] = pd.to_datetime(ts, unit="ms", utc=True)
    df = df.sort_values("open_time").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def aggregate_daily(month_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    parts = []
    for month, df in month_frames.items():
        utc_day = df["open_time"].dt.floor("D").dt.tz_localize(None)
        g = df.groupby(utc_day)
        day = pd.DataFrame({
            "open": g["open"].first(),
            "high": g["high"].max(),
            "low": g["low"].min(),
            "close": g["close"].last(),
            "volume": g["volume"].sum(),
            "n_bars": g.size(),
        })
        parts.append(day)

    daily = pd.concat(parts).sort_index()
    daily.index = pd.DatetimeIndex(daily.index)
    daily.index.name = "date"
    daily = daily[~daily.index.duplicated(keep="last")]

    # A1 integrity: drop days with < 20 hourly bars (Binance maintenance gaps).
    too_thin = daily.index[daily["n_bars"] < 20]
    if len(too_thin):
        print(f"[A1] dropping days with n_bars<20: "
              f"{[(str(d.date()), int(daily.loc[d, 'n_bars'])) for d in too_thin]}")
    daily = daily.drop(too_thin)
    partial = daily.index[daily["n_bars"] != cfg.BARS_PER_DAY]
    if len(partial):
        print(f"[A1] kept partial days (20-23 bars): "
              f"{[(str(d.date()), int(daily.loc[d, 'n_bars'])) for d in partial]}")

    # Validation and test windows must be complete (24 bars), no exceptions.
    vt = daily.loc[cfg.VAL_START:]
    if (vt["n_bars"] != cfg.BARS_PER_DAY).any():
        bad = [(str(d.date()), int(vt.loc[d, "n_bars"]))
               for d in vt.index[vt["n_bars"] != 24]]
        raise AssertionError(f"Hari tidak-komplet di window validasi/test: {bad}")

    # Calendar continuity apart from the dropped days.
    full_range = pd.date_range(cfg.DATA_START, cfg.DATA_END, freq="D")
    expected = full_range.difference(pd.DatetimeIndex(too_thin))
    if not daily.index.equals(expected):
        raise AssertionError("Kalender harian tidak kontinu / tidak sesuai ekspektasi A1.")
    if daily[["open", "high", "low", "close", "volume"]].isna().any().any():
        raise AssertionError("NaN pada OHLCV harian.")
    if not ((daily["high"] >= daily[["open", "close", "low"]].max(axis=1)).all()
            and (daily["low"] <= daily[["open", "close", "high"]].min(axis=1)).all()):
        raise AssertionError("Relasi OHLC harian dilanggar.")
    if not (daily[["open", "high", "low", "close"]] > 0).all().all():
        raise AssertionError("Ada harga <= 0.")

    # Pre-registered target and features (protocol section 2).
    log_hl = np.log(daily["high"] / daily["low"])
    rv = aggregate_rv(month_frames).reindex(daily.index)

    daily["rv"] = rv
    daily["log_rv"] = np.log(daily["rv"] + cfg.RV_EPS)
    daily["log_range"] = log_hl
    daily["log_volume"] = np.log(daily["volume"] + cfg.RV_EPS)
    ret_1d = np.log(daily["close"]) - np.log(daily["close"].shift(1))
    contiguous = daily.index.to_series().diff() == pd.Timedelta(days=1)
    ret_1d = ret_1d.where(contiguous)  # NaN across calendar gaps (excluded later)
    daily["log_absret"] = np.log(ret_1d.abs() + cfg.RV_EPS)
    daily["rv_mean_5"] = daily["log_rv"].rolling(5).mean()
    daily["rv_mean_22"] = daily["log_rv"].rolling(22).mean()
    return daily.reset_index()


def aggregate_rv(month_frames: dict[str, pd.DataFrame]) -> pd.Series:
    """Daily realized variance = sum of squared hourly log(open->close) moves."""
    rows = []
    for _, df in month_frames.items():
        ret = np.log(df["close"]) - np.log(df["open"])
        sq = (ret ** 2).groupby(df["open_time"].dt.floor("D").dt.tz_localize(None)).sum()
        rows.append(sq)
    rv = pd.concat(rows).sort_index()
    rv.index = pd.DatetimeIndex(rv.index)
    rv = rv[~rv.index.duplicated(keep="last")]
    rv.name = "rv"
    return rv


# ---------------------------------------------------------------------------
# Build & freeze
# ---------------------------------------------------------------------------
def build(force_redownload: bool = False) -> pd.DataFrame:
    if force_redownload:
        for p in cfg.S2_RAW_ZIP_DIR.glob("*.zip"):
            p.unlink()
    infos = download_all(cfg.S2_RAW_ZIP_DIR)
    cfg.S2_RAW_MANIFEST.write_text(
        json.dumps(infos, indent=2), encoding="utf-8"
    )

    month_frames = {
        info["month"]: load_month_zip(cfg.S2_RAW_ZIP_DIR / f"BTCUSDT-1h-{info['month']}.zip")
        for info in infos
    }
    daily = aggregate_daily(month_frames)

    expected_cols = ["date", "open", "high", "low", "close", "volume", "n_bars",
                     "rv", "log_rv", "log_range", "log_volume", "log_absret",
                     "rv_mean_5", "rv_mean_22"]
    daily = daily[expected_cols]
    assert len(daily) == cfg.EXPECTED_TOTAL_DAYS, f"rows {len(daily)} != {cfg.EXPECTED_TOTAL_DAYS}"

    cfg.S2_DAILY_CSV.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(cfg.S2_DAILY_CSV, index=False)
    freeze_hashes()
    return daily


def freeze_hashes() -> None:
    daily_sha = cfg.sha256_file(cfg.S2_DAILY_CSV)
    manifest_sha = cfg.sha256_file(cfg.S2_RAW_MANIFEST)
    payload = {
        "daily_csv_sha256": daily_sha,
        "raw_zips_manifest_sha256": manifest_sha,
        "protocol_sha256": cfg.protocol_hash(),
        "rows": cfg.EXPECTED_TOTAL_DAYS,
        "window": f"{cfg.DATA_START}..{cfg.DATA_END}",
    }
    cfg.S2_DATA_FREEZE_HASH.write_text(json.dumps(payload, indent=2) + "\n",
                                       encoding="utf-8")
    print(f"[freeze] daily_csv sha256 = {daily_sha}")
    print(f"[freeze] protocol sha256 = {cfg.protocol_hash()}")


def verify_frozen() -> None:
    payload = json.loads(cfg.S2_DATA_FREEZE_HASH.read_text(encoding="utf-8"))
    assert cfg.sha256_file(cfg.S2_DAILY_CSV) == payload["daily_csv_sha256"], \
        "daily CSV hash mismatch"
    assert cfg.sha256_file(cfg.S2_RAW_MANIFEST) == payload["raw_zips_manifest_sha256"], \
        "manifest hash mismatch"
    assert cfg.protocol_hash() == payload["protocol_sha256"], "protocol hash mismatch"
    print("[verify] all hashes match; data frozen and consistent with protocol.")


def load_daily() -> pd.DataFrame:
    df = pd.read_csv(cfg.S2_DAILY_CSV, parse_dates=["date"])
    assert len(df) == cfg.EXPECTED_TOTAL_DAYS
    return df


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if args.verify:
        verify_frozen()
        return
    df = build(force_redownload=args.force)
    print(df.head(3).to_string())
    print(df.tail(3).to_string())
    print("shape:", df.shape)
    print("rv stats:", df["rv"].describe().to_string())


if __name__ == "__main__":
    main()
