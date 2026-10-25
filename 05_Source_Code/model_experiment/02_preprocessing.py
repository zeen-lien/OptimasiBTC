"""
02_preprocessing.py - Chronological split and leakage-safe final scaler.

The final scaler is fit on the in-sample partition only. Cross-validation
scalers are handled separately in Fase 2; this script produces the frozen
train/test split used by the final models.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib

import config
import run_utils
from data_utils import fit_scaler, load_raw_data, split_temporal, transform_data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Partisi temporal dan Min-Max scaling")
    run_utils.add_run_arguments(parser)
    parser.add_argument("--raw-path", default=None, help="CSV mentah eksplisit")
    parser.add_argument("--train-ratio", type=float, default=config.DEFAULT_TRAIN_RATIO)
    return parser.parse_args(argv)


def resolve_raw_path(args, paths: run_utils.RunPaths) -> Path:
    candidates = []
    if args.raw_path:
        candidates.append(Path(args.raw_path))
    candidates.append(paths.raw_dir / "BTCUSDT_daily_2020_2025.csv")
    candidates.append(config.RAW_DATA_PATH)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Data mentah tidak ditemukan. Jalankan 01_fetch_binance_data.py lebih dulu. "
        f"Kandidat: {[str(path) for path in candidates]}"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started_at = run_utils.utc_now()
    paths = run_utils.run_context_from_args(args, stage="preprocessing")

    if paths.legacy:
        print("[WARNING] Mode legacy: artefak processed lama dapat tertimpa.")

    raw_path = resolve_raw_path(args, paths)
    df = load_raw_data(raw_path)
    total_obs = len(df)
    if total_obs != config.EXPECTED_RAW_ROWS:
        raise ValueError(
            f"Jumlah observasi {total_obs} tidak sesuai kontrak "
            f"{config.EXPECTED_RAW_ROWS}. Periksa data mentah."
        )

    print("=" * 70)
    print("PIPELINE DATA 02: PRAPEMROSESAN & PARTISI TEMPORAL BEBAS BOCOR")
    print("=" * 70)
    print(f"[1/4] Data mentah dimuat: {total_obs} observasi")
    print(f"      Rentang: {df['date'].min():%Y-%m-%d} s.d. {df['date'].max():%Y-%m-%d}")
    print(f"      Sumber: {raw_path}")

    train_df, test_df = split_temporal(df, train_ratio=args.train_ratio)
    n_train, n_test = len(train_df), len(test_df)

    if n_train != config.EXPECTED_TRAIN_ROWS or n_test != config.EXPECTED_TEST_ROWS:
        raise ValueError(
            f"Split menghasilkan {n_train}/{n_test}, diharapkan "
            f"{config.EXPECTED_TRAIN_ROWS}/{config.EXPECTED_TEST_ROWS}"
        )

    print("\n[2/4] Partisi temporal:")
    print(f"      - In-sample : {n_train} observasi ({n_train / total_obs * 100:.1f}%)")
    print(f"        {train_df['date'].min():%Y-%m-%d} s.d. {train_df['date'].max():%Y-%m-%d}")
    print(f"      - Out-of-sample: {n_test} observasi ({n_test / total_obs * 100:.1f}%)")
    print(f"        {test_df['date'].min():%Y-%m-%d} s.d. {test_df['date'].max():%Y-%m-%d}")

    scaler = fit_scaler(train_df)
    train_scaled = transform_data(scaler, train_df)
    test_scaled = transform_data(scaler, test_df)
    print("\n[3/4] Min-Max scaling (fit hanya pada in-sample):")
    print(f"      - x_min: USD {scaler.data_min_[0]:,.2f}")
    print(f"      - x_max: USD {scaler.data_max_[0]:,.2f}")

    proc_dir = config.PROCESSED_DIR if paths.legacy else paths.processed_dir
    proc_dir.mkdir(parents=True, exist_ok=True)
    train_path = proc_dir / "train_insample.csv"
    test_path = proc_dir / "test_outofsample.csv"
    scaler_path = proc_dir / "minmax_scaler.joblib"
    metadata_path = proc_dir / "preprocessing_metadata.json"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    joblib.dump(scaler, scaler_path)

    metadata = {
        "source_raw": str(Path(raw_path).resolve()),
        "source_raw_sha256": run_utils.sha256_file(raw_path),
        "total_observations": total_obs,
        "train_ratio": args.train_ratio,
        "n_train_insample": n_train,
        "n_test_outofsample": n_test,
        "train_start_date": train_df["date"].min().strftime("%Y-%m-%d"),
        "train_end_date": train_df["date"].max().strftime("%Y-%m-%d"),
        "test_start_date": test_df["date"].min().strftime("%Y-%m-%d"),
        "test_end_date": test_df["date"].max().strftime("%Y-%m-%d"),
        "scaler_min": float(scaler.data_min_[0]),
        "scaler_max": float(scaler.data_max_[0]),
        "scaler_fit_partition": "train_insample_only",
        "train_scaled_shape": int(train_scaled.shape[0]),
        "test_scaled_shape": int(test_scaled.shape[0]),
    }
    with metadata_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(metadata, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print("\n[4/4] Artefak prapemrosesan disimpan:")
    for path in (train_path, test_path, scaler_path, metadata_path):
        print(f"      -> {path.resolve()}")
    print("=" * 70)

    if not paths.legacy:
        stage_config = {
            "stage": "preprocessing",
            "raw_path": str(Path(raw_path).resolve()),
            "train_ratio": args.train_ratio,
            "processed_dir": str(proc_dir.resolve()),
            "n_train": n_train,
            "n_test": n_test,
            "train_period": [metadata["train_start_date"], metadata["train_end_date"]],
            "test_period": [metadata["test_start_date"], metadata["test_end_date"]],
            "scaler_fit_partition": "train_insample_only",
            "seed": args.seed,
        }
        run_utils.bootstrap_run(paths, "preprocessing", stage_config, inputs=[raw_path])
        run_utils.record_stage(
            paths,
            "preprocessing",
            status="success",
            started_at=started_at,
            stage_config=stage_config,
            inputs=[raw_path],
            outputs=[train_path, test_path, scaler_path, metadata_path],
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
