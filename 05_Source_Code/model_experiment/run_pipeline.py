"""
run_pipeline.py — Master Orchestration Script for Bitcoin LSTM Experiment
Skripsi: Optimasi Hyperparameter LSTM Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin
Penulis: Zaini Leon Musthofa Kamal (NIM: 231240001455)
Prodi: S1 Teknik Informatika — FST UNISNU Jepara

Penggunaan:
  python run_pipeline.py --all                 (Jalankan seluruh pipeline 01 s.d. 06)
  python run_pipeline.py --stage data          (Jalankan tahapan akuisisi & prapemrosesan)
  python run_pipeline.py --stage tier1         (Jalankan pelatihan Tier 1 Baseline)
  python run_pipeline.py --stage tier2         (Jalankan pelatihan Tier 2 Manual)
  python run_pipeline.py --stage tier3         (Jalankan optimasi Tier 3 Optuna)
  python run_pipeline.py --stage eval          (Jalankan komparasi & visualisasi)
"""

import sys
import argparse
import subprocess


def run_script(script_name):
    print(f"\n>>> MENJALANKAN: {script_name} <<<")
    res = subprocess.run([sys.executable, script_name], check=True)
    if res.returncode != 0:
        print(f"[FAILED] Script {script_name} gagal dengan kode {res.returncode}")
        sys.exit(res.returncode)


def main():
    parser = argparse.ArgumentParser(description="Master Pipeline Runner Skripsi Bitcoin LSTM Optuna")
    parser.add_argument("--all", action="store_true", help="Jalankan seluruh pipeline end-to-end")
    parser.add_argument("--stage", choices=["data", "tier1", "tier2", "tier3", "eval"], help="Pilih stage tertentu")
    parser.add_argument("--trials", type=int, default=50, help="Jumlah trial untuk Optuna (default: 50)")
    args = parser.parse_args()

    if args.all or args.stage == "data":
        run_script("01_fetch_binance_data.py")
        run_script("02_preprocessing.py")
        if not args.all:
            return

    if args.all or args.stage == "tier1":
        run_script("03_train_baseline_tier1.py")
        if not args.all:
            return

    if args.all or args.stage == "tier2":
        run_script("04_train_manual_tier2.py")
        if not args.all:
            return

    if args.all or args.stage == "tier3":
        run_script("05_optimize_optuna_tier3.py")
        if not args.all:
            return

    if args.all or args.stage == "eval":
        run_script("06_evaluate_and_compare.py")
        if not args.all:
            return

    if not args.all and not args.stage:
        parser.print_help()


if __name__ == "__main__":
    main()
