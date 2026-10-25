"""Generate ``docs/NUMBER_AUDIT.md`` from the published final summary.

The audit answers one question for every headline number in the thesis:
*which machine-readable field produced it?*  It is generated, never edited by
hand, so the manuscript and the audit cannot drift apart silently.

Run after ``08_analyze_results.py --publish``::

    python 05_Source_Code/generators/build_number_audit.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import results_context
from doc_paths import PROJECT_ROOT
from results_context import FinalResults, format_number, format_pct, format_usd

DEFAULT_OUTPUT = PROJECT_ROOT / "docs" / "NUMBER_AUDIT.md"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _metric_row(results: FinalResults, key: str) -> str:
    metrics = results.metrics(key)
    ci = results.ci(key, "MAE")
    aggregate = results.aggregate(key, "MAE") or {}
    return (
        f"| {key} | {results.label(key)} | {format_usd(metrics['RMSE'])} | "
        f"{format_usd(metrics['MAE'])} | {format_pct(metrics['MAPE'])} | "
        f"{format_usd(ci['ci_low'])}–{format_usd(ci['ci_high'])} | "
        f"{format_number(aggregate.get('std', 0.0))} | "
        f"{aggregate.get('n_seeds', 1)} |"
    )


def _comparison_row(results: FinalResults, label: str) -> str:
    payload = results.comparison(label)
    mae = results.comparison_metric(label, "MAE")
    return (
        f"| {label} | {payload.get('model_a')} → {payload.get('model_b')} | "
        f"{format_usd(mae['difference_b_minus_a'], signed=True)} | "
        f"{format_usd(mae['ci_low'], signed=True)}–"
        f"{format_usd(mae['ci_high'], signed=True)} | "
        f"{format_pct(mae['relative_change_percent'], signed=True)} |"
    )


def build_number_audit(results: FinalResults) -> str:
    data = results.data
    stats = data.get("statistics") or {}
    protocol = results.protocol
    bootstrap = protocol.get("bootstrap") or {}
    config = results.final_configuration()
    hyper = config.get("hyperparameters") or {}
    environment = results.environment.get("packages") or {}
    verdict = results.verdict
    best_overall = results.best_overall
    best_lstm = results.best_lstm

    summary_hash = (
        _sha256(results.source) if results.source and results.source.exists() else "tidak tersedia"
    )

    lines: list[str] = [
        "# Audit Angka Naskah",
        "",
        "Dokumen ini dihasilkan otomatis oleh",
        "`05_Source_Code/generators/build_number_audit.py` dari",
        "`05_Source_Code/results/summary_final.json`. Jangan mengedit manual.",
        "",
        "## 1. Sumber Tunggal",
        "",
        "| Item | Nilai |",
        "|---|---|",
        f"| Run ID | `{results.run_id}` |",
        f"| Summary | `{results.source}` |",
        f"| SHA-256 summary | `{summary_hash}` |",
        f"| Jumlah observasi | {format_number(data.get('n_train', 0), 0)} in-sample + "
        f"{format_number(data.get('n_test', 0), 0)} holdout = "
        f"{format_number(stats.get('n_observations', 0), 0)} |",
        f"| Periode data | {stats.get('period', ['-', '-'])[0]} s.d. "
        f"{stats.get('period', ['-', '-'])[1]} |",
        f"| Periode holdout | {data.get('test_period', ['-', '-'])[0]} s.d. "
        f"{data.get('test_period', ['-', '-'])[1]} |",
        f"| Bootstrap | moving block {bootstrap.get('block_size_days', '-')} hari, "
        f"{format_number(bootstrap.get('n_resamples', 0), 0)} resample, "
        f"CI {format_pct((bootstrap.get('confidence', 0) or 0) * 100, 0)} |",
        f"| Seed | {results.expected_seeds} seed |",
        "",
        "## 2. Statistik Deskriptif Data",
        "",
        "| Parameter | Nilai | Sumber |",
        "|---|---:|---|",
        f"| Harga minimum | {format_usd(stats.get('min', 0))} | "
        f"`data.statistics.min` |",
        f"| Tanggal minimum | {stats.get('min_date', '-')} | "
        f"`data.statistics.min_date` |",
        f"| Harga maksimum | {format_usd(stats.get('max', 0))} | "
        f"`data.statistics.max` |",
        f"| Tanggal maksimum | {stats.get('max_date', '-')} | "
        f"`data.statistics.max_date` |",
        f"| Rata-rata | {format_usd(stats.get('mean', 0))} | "
        f"`data.statistics.mean` |",
        f"| Median | {format_usd(stats.get('median', 0))} | "
        f"`data.statistics.median` |",
        f"| Simpangan baku | {format_usd(stats.get('std', 0))} | "
        f"`data.statistics.std` |",
        "",
        "## 3. Baseline dan Model",
        "",
        "| Run | Model | RMSE | MAE | MAPE | CI 95% MAE | Std MAE antar-seed | n seed |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key in results_context.MODEL_ORDER:
        lines.append(_metric_row(results, key))

    lines += [
        "",
        "Sumber: `models.{E0..E7}.metrics`, `models.{E0..E7}.confidence_intervals.MAE`, "
        "dan `models.{E1..E7}.multi_seed.aggregate.MAE`.",
        "",
        "## 4. Baseline Naif",
        "",
        "| Baseline | RMSE | MAE | MAPE | Sumber |",
        "|---|---:|---:|---:|---|",
    ]
    baselines = results.payload.get("baselines") or {}
    for name, payload in baselines.items():
        metrics = payload.get("metrics") or {}
        lines.append(
            f"| {name} | {format_usd(metrics.get('RMSE', 0))} | "
            f"{format_usd(metrics.get('MAE', 0))} | "
            f"{format_pct(metrics.get('MAPE', 0))} | `baselines.{name}.metrics` |"
        )
    if not baselines:
        lines.append("| - | - | - | - | `baselines` tidak tersedia |")

    lines += [
        "",
        "## 5. Ablasi Loss dan Scheduler",
        "",
        "| Run | Loss | Scheduler | RMSE | MAE | MAPE | Delta MAE vs E3 |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for row in results.ablation_rows():
        lines.append(
            f"| {row['run']} | {row['loss']} | {row['scheduler']} | "
            f"{format_usd(row['RMSE'])} | {format_usd(row['MAE'])} | "
            f"{format_pct(row['MAPE'])} | "
            f"{format_pct(row['delta_MAE_vs_E3'], signed=True)} |"
        )
    lines += [
        "",
        "Delta positif berarti MAE lebih rendah daripada E3. Sumber: "
        "`models.{E3..E6}.metrics` dan `improvement_vs.e3`.",
        "",
        "## 6. Perbandingan Berpasangan",
        "",
        "| Perbandingan | Arah | Selisih MAE (B - A) | CI 95% | Perubahan relatif |",
        "|---|---|---:|---:|---:|",
    ]
    for label in results.paired_comparisons:
        lines.append(_comparison_row(results, label))

    lines += [
        "",
        "Selisih negatif berarti model B lebih baik. CI adalah moving-block "
        "bootstrap pada tanggal yang sama; `p_value` bukan uji formal.",
        "",
        "## 7. Verdict Ilmiah",
        "",
        "| Item | Nilai | Sumber |",
        "|---|---|---|",
        f"| Status | `{verdict.get('status', '-')}` | `headline.status` |",
        f"| Metrik utama | {results.payload.get('primary_metric', 'MAE')} | "
        f"`primary_metric` |",
        f"| MAE E7 vs persistence | "
        f"{format_pct(results.improvement('E7', 'E0', 'MAE'), signed=True)} | "
        f"`models.E7.metrics.MAE` vs `models.E0.metrics.MAE` |",
        f"| CI selisih E7-persistence | "
        f"{format_usd(results.comparison_metric('E7_vs_persistence', 'MAE')['ci_low'], signed=True)}–"
        f"{format_usd(results.comparison_metric('E7_vs_persistence', 'MAE')['ci_high'], signed=True)} | "
        f"`paired_comparisons.E7_vs_persistence.metrics.MAE` |",
        f"| Terbaik keseluruhan (MAE) | {best_overall.get('run')} "
        f"({format_usd(best_overall.get('MAE', 0))}) | `best_by_mae` |",
        f"| LSTM terbaik (MAE) | {best_lstm.get('run')} "
        f"({format_usd(best_lstm.get('MAE', 0))}) | `lstm_ranking_by_mae[0]` |",
    ]
    claim = verdict.get("claim")
    if claim:
        lines += ["", f"> {claim}", ""]

    lines += [
        "## 8. Konfigurasi Final E7",
        "",
        "| Parameter | Nilai | Sumber |",
        "|---|---:|---|",
        f"| Lookback | {hyper.get('lookback', '-')} hari | "
        f"`final_configuration.hyperparameters.lookback` |",
        f"| Units | {hyper.get('units', '-')} | "
        f"`final_configuration.hyperparameters.units` |",
        f"| Dropout | {format_number(hyper.get('dropout', 0), 2)} | "
        f"`final_configuration.hyperparameters.dropout` |",
        f"| Learning rate | {format_number(hyper.get('learning_rate', 0), 5)} | "
        f"`final_configuration.hyperparameters.learning_rate` |",
        f"| Batch size | {hyper.get('batch_size', '-')} | "
        f"`final_configuration.hyperparameters.batch_size` |",
        f"| Layers | {hyper.get('layers', '-')} | "
        f"`final_configuration.hyperparameters.layers` |",
        f"| Epoch berjalan | {config.get('epochs_run', '-')} | "
        f"`final_configuration.epochs_run` |",
        f"| Total trials | {config.get('total_trials', '-')} | "
        f"`final_configuration.total_trials` |",
        f"| Trial terbaik | {config.get('best_trial_number', '-')} | "
        f"`final_configuration.best_trial_number` |",
        f"| CV loss terbaik | {format_number(config.get('best_cv_loss', 0))} | "
        f"`final_configuration.best_cv_loss` |",
        f"| Waktu optimasi | {format_number(config.get('optimization_time_seconds', 0), 1)} detik | "
        f"`final_configuration.optimization_time_seconds` |",
        f"| Waktu latih final | {format_number(config.get('training_time_seconds', 0), 1)} detik | "
        f"`final_configuration.training_time_seconds` |",
        "",
        "## 9. Environment",
        "",
        "| Paket | Versi |",
        "|---|---|",
    ]
    for package in (
        "python_version",
        "tensorflow",
        "optuna",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "python-docx",
    ):
        version = (
            results.environment.get("python_version")
            if package == "python_version"
            else environment.get(package)
        )
        lines.append(f"| {package} | {version or '-'} |")

    lines += [
        "",
        "## 10. Larangan Angka Lama",
        "",
        "Angka berikut berasal dari snapshot pra-perbaikan dan **tidak boleh** "
        "muncul sebagai hasil final:",
        "",
        "| Angka lama | Konteks | Status |",
        "|---|---|---|",
        "| RMSE 2.338,22 / MAE 1.784,27 / MAPE 1,81% | Tier 3 pra-perbaikan | Diganti angka E7 final |",
        "| Best trial #44, lookback 14, units 80 | Konfigurasi pra-perbaikan | Diganti konfigurasi E7 final |",
        "| Split 85% | Replikasi Tier 2 lama | Diganti split 80:20 (1.753/439) |",
        "| Batch 10 / units 128 sebagai klaim kausal | Narasi lama | Dihapus atau dijadikan deskriptif |",
        "",
        "Verifikasi otomatis ada di `verify_full_skripsi.py`.",
        "",
    ]
    return "\n".join(lines)


def write_number_audit(
    output: Path = DEFAULT_OUTPUT,
    summary_path: Path | str | None = None,
) -> Path:
    results = FinalResults.load(summary_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_number_audit(results), encoding="utf-8")
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bangun audit angka naskah")
    parser.add_argument("--summary", default=None, help="Path summary_final.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        path = write_number_audit(Path(args.output), args.summary)
    except results_context.ResultsError as exc:
        print(f"[ERROR] {exc}")
        return 2
    print(f"[SUCCESS] Number audit ditulis ke {path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
