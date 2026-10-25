"""Single source of truth for thesis numbers.

Every document generator imports :class:`FinalResults` instead of hardcoding
metrics.  The class reads ``05_Source_Code/results/summary_final.json`` written
by ``08_analyze_results.py --publish`` and refuses incomplete, unpublished, or
protocol-drifted runs.

The module also provides Indonesian number formatting so tables and prose use
one convention: thousands separator ``.`` and decimal separator ``,``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from doc_paths import RESULTS_ROOT

FINAL_SUMMARY_PATH = RESULTS_ROOT / "summary_final.json"
MODEL_ORDER = ("E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7")
METRICS = ("RMSE", "MAE", "MAPE")
MODEL_LABELS = {
    "E0": "Persistence",
    "E1": "Tier 1 default",
    "E2": "Tier 2 manual",
    "E3": "Ablasi MSE / tanpa scheduler",
    "E4": "Ablasi MAE / tanpa scheduler",
    "E5": "Ablasi MSE / ReduceLROnPlateau",
    "E6": "Ablasi MAE / ReduceLROnPlateau",
    "E7": "Tier 3 HPO penuh (usulan)",
}


class ResultsError(RuntimeError):
    """Raised when a final summary is missing or not safe to publish."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise ResultsError(
            f"File hasil final tidak ditemukan: {path}. "
            "Jalankan 08_analyze_results.py --publish terlebih dahulu."
        ) from exc
    except json.JSONDecodeError as exc:
        raise ResultsError(f"File hasil final bukan JSON yang valid: {path}") from exc
    if not isinstance(payload, dict):
        raise ResultsError(f"File hasil final harus berupa objek JSON: {path}")
    return payload


def _number(value: Any, field: str) -> float:
    if value is None:
        raise ResultsError(f"Nilai {field} tidak tersedia pada summary final")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ResultsError(f"Nilai {field} bukan angka: {value!r}") from exc


def format_number(value: Any, decimals: int = 2, signed: bool = False) -> str:
    """Format a number with Indonesian separators (``1.234,56``)."""
    number = _number(value, "format_number")
    text = f"{number:+,.{decimals}f}" if signed else f"{number:,.{decimals}f}"
    return text.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".")


def format_usd(value: Any, decimals: int = 2, signed: bool = False) -> str:
    return f"USD {format_number(value, decimals, signed)}"


def format_pct(value: Any, decimals: int = 2, signed: bool = False) -> str:
    return f"{format_number(value, decimals, signed)}%"


def format_interval(
    low: Any, high: Any, unit: str = "usd", decimals: int = 2
) -> str:
    if unit == "usd":
        return f"{format_usd(low, decimals)}–{format_usd(high, decimals)}"
    if unit == "pct":
        return f"{format_pct(low, decimals)}–{format_pct(high, decimals)}"
    return f"{format_number(low, decimals)}–{format_number(high, decimals)}"


class FinalResults:
    """Validated accessor for ``summary_final.json``.

    Parameters
    ----------
    payload:
        Parsed summary dictionary.  Exposed for tests; production code should
        use :meth:`load`.
    source:
        Path used only for error messages and run-directory resolution.
    """

    def __init__(self, payload: Mapping[str, Any], source: Path | None = None):
        self.payload: dict[str, Any] = dict(payload)
        self.source = Path(source) if source else None

    # ------------------------------------------------------------------
    # Loading and validation
    # ------------------------------------------------------------------
    @classmethod
    def load(
        cls,
        path: Path | str | None = None,
        require_complete: bool = True,
    ) -> "FinalResults":
        source = Path(path) if path else FINAL_SUMMARY_PATH
        results = cls(_read_json(source), source=source)
        if require_complete:
            results.validate()
        return results

    def validate(self) -> None:
        status = self.payload.get("status")
        if status != "complete":
            raise ResultsError(
                "Summary final belum lengkap "
                f"(status={status!r}, missing={self.payload.get('missing_models')}). "
                "Jangan membangun naskah dari hasil parsial."
            )
        missing = [key for key in MODEL_ORDER if key not in self.models]
        if missing:
            raise ResultsError(f"Summary final kehilangan model: {', '.join(missing)}")
        seed_issues = self.payload.get("seed_coverage_issues") or {}
        if seed_issues:
            raise ResultsError(f"Cakupan seed tidak lengkap: {seed_issues}")
        hash_issues = self.payload.get("protocol_hash_issues") or {}
        if hash_issues:
            raise ResultsError(
                "Hash protokol/requirements berubah sejak run dimulai: "
                f"{hash_issues}"
            )
        expected = int(self.payload.get("expected_seeds") or 1)
        if expected > 1:
            for key in MODEL_ORDER[1:]:
                aggregate = self.aggregate(key, "MAE")
                if not aggregate or aggregate.get("n_seeds") != expected:
                    raise ResultsError(
                        f"{key} tidak memiliki {expected} seed; "
                        f"ditemukan {None if not aggregate else aggregate.get('n_seeds')}"
                    )
        verdict = self.payload.get("headline") or {}
        if not verdict or verdict.get("status") == "incomplete":
            raise ResultsError("Verdict ilmiah belum tersedia pada summary final")

    # ------------------------------------------------------------------
    # Basic metadata
    # ------------------------------------------------------------------
    @property
    def run_id(self) -> str:
        run_id = self.payload.get("run_id")
        if not run_id:
            raise ResultsError("run_id tidak tersedia pada summary final")
        return str(run_id)

    @property
    def run_dir(self) -> Path:
        return RESULTS_ROOT / "runs" / self.run_id

    @property
    def figures_dir(self) -> Path:
        return self.run_dir / "figures"

    @property
    def predictions_dir(self) -> Path:
        return self.run_dir / "predictions"

    @property
    def data(self) -> dict[str, Any]:
        return self.payload.get("data") or {}

    @property
    def protocol(self) -> dict[str, Any]:
        return self.payload.get("protocol") or {}

    @property
    def environment(self) -> dict[str, Any]:
        return self.payload.get("environment") or {}

    @property
    def verdict(self) -> dict[str, Any]:
        return self.payload.get("headline") or {}

    @property
    def claim_rule(self) -> dict[str, Any]:
        return self.payload.get("claim_rule") or {}

    @property
    def models(self) -> dict[str, dict[str, Any]]:
        return self.payload.get("models") or {}

    @property
    def expected_seeds(self) -> int:
        return int(self.payload.get("expected_seeds") or 1)

    @property
    def data_hash(self) -> dict[str, str]:
        return self.payload.get("data_hash") or {}

    # ------------------------------------------------------------------
    # Model accessors
    # ------------------------------------------------------------------
    def model(self, key: str) -> dict[str, Any]:
        try:
            return self.models[key]
        except KeyError as exc:
            raise ResultsError(f"Model {key} tidak ada pada summary final") from exc

    def label(self, key: str) -> str:
        return MODEL_LABELS.get(key, self.model(key).get("model", key))

    def metrics(self, key: str) -> dict[str, float]:
        metrics = self.model(key).get("metrics") or {}
        return {metric: _number(metrics.get(metric), f"{key}.{metric}") for metric in METRICS}

    def metric(self, key: str, metric: str) -> float:
        return self.metrics(key)[metric]

    def ci(self, key: str, metric: str) -> dict[str, float]:
        intervals = self.model(key).get("confidence_intervals") or {}
        if metric not in intervals:
            raise ResultsError(f"CI {metric} untuk {key} tidak tersedia")
        return intervals[metric]

    def aggregate(self, key: str, metric: str) -> dict[str, float] | None:
        seed_payload = self.model(key).get("multi_seed") or {}
        aggregate = seed_payload.get("aggregate") or {}
        if metric in aggregate:
            return aggregate[metric]
        if key == "E0":
            value = self.metric(key, metric)
            return {
                "mean": value,
                "std": 0.0,
                "min": value,
                "max": value,
                "n_seeds": 1,
            }
        return None

    def per_seed(self, key: str) -> dict[str, dict[str, float]]:
        seed_payload = self.model(key).get("multi_seed") or {}
        return seed_payload.get("per_seed") or {}

    def training(self, key: str) -> dict[str, Any]:
        training = self.model(key).get("training")
        if training is None:
            training = (self.payload.get("training") or {}).get(key) or {}
        return training

    def final_configuration(self) -> dict[str, Any]:
        config = self.payload.get("final_configuration") or self.training("E7")
        if not config:
            raise ResultsError("Konfigurasi final E7 tidak tersedia")
        return config

    def hyperparameters(self, key: str) -> dict[str, Any]:
        return self.training(key).get("hyperparameters") or {}

    def improvement(self, key: str, reference: str, metric: str = "MAE") -> float:
        """Positive means ``key`` has lower error than ``reference``."""
        reference_value = self.metric(reference, metric)
        if reference_value == 0:
            raise ResultsError(f"Referensi {reference} bernilai nol untuk {metric}")
        return (reference_value - self.metric(key, metric)) / reference_value * 100.0

    # ------------------------------------------------------------------
    # Paired comparisons and claims
    # ------------------------------------------------------------------
    @property
    def paired_comparisons(self) -> dict[str, dict[str, Any]]:
        return self.payload.get("paired_comparisons") or {}

    def comparison(self, label: str) -> dict[str, Any]:
        try:
            return self.paired_comparisons[label]
        except KeyError as exc:
            raise ResultsError(f"Perbandingan {label} tidak tersedia") from exc

    def comparison_metric(self, label: str, metric: str = "MAE") -> dict[str, float]:
        payload = self.comparison(label).get("metrics") or {}
        if metric not in payload:
            raise ResultsError(f"Metrik {metric} tidak ada pada perbandingan {label}")
        return payload[metric]

    def is_improvement(
        self, label: str, metric: str = "MAE", require_ci: bool = True
    ) -> bool:
        """True only when the paired difference is negative and CI excludes zero."""
        comparison = self.comparison_metric(label, metric)
        point_better = float(comparison["difference_b_minus_a"]) < 0
        ci_excludes_zero = float(comparison["ci_high"]) < 0
        return bool(point_better and (ci_excludes_zero or not require_ci))

    def is_significant(self, label: str, metric: str = "MAE") -> bool:
        return self.is_improvement(label, metric, require_ci=True)

    @property
    def best_overall(self) -> dict[str, Any]:
        ranking = self.payload.get("ranking_by_mae") or []
        if not ranking:
            raise ResultsError("Peringkat MAE tidak tersedia")
        return ranking[0]

    @property
    def best_lstm(self) -> dict[str, Any]:
        ranking = self.payload.get("lstm_ranking_by_mae") or []
        if not ranking:
            raise ResultsError("Peringkat LSTM tidak tersedia")
        return ranking[0]

    def summary_rows(self) -> list[dict[str, Any]]:
        """Rows for the main benchmark table, ordered E0..E7."""
        rows: list[dict[str, Any]] = []
        for key in MODEL_ORDER:
            metrics = self.metrics(key)
            aggregate = self.aggregate(key, "MAE") or {}
            rows.append(
                {
                    "run": key,
                    "label": self.label(key),
                    "loss": self.model(key).get("loss", "-"),
                    "scheduler": self.model(key).get("scheduler", "-"),
                    "hpo": bool(self.model(key).get("hpo")),
                    "RMSE": metrics["RMSE"],
                    "MAE": metrics["MAE"],
                    "MAPE": metrics["MAPE"],
                    "MAE_mean": aggregate.get("mean", metrics["MAE"]),
                    "MAE_std": aggregate.get("std", 0.0),
                    "n_seeds": aggregate.get("n_seeds", 1),
                }
            )
        return rows

    def ablation_rows(self) -> list[dict[str, Any]]:
        """E3-E6 factorial rows with effect sizes against E3."""
        rows = []
        for key in ("E3", "E4", "E5", "E6"):
            metrics = self.metrics(key)
            aggregate = self.aggregate(key, "MAE") or {}
            rows.append(
                {
                    "run": key,
                    "loss": self.model(key).get("loss", "-"),
                    "scheduler": self.model(key).get("scheduler", "-"),
                    "RMSE": metrics["RMSE"],
                    "MAE": metrics["MAE"],
                    "MAPE": metrics["MAPE"],
                    "MAE_mean": aggregate.get("mean", metrics["MAE"]),
                    "MAE_std": aggregate.get("std", 0.0),
                    "delta_MAE_vs_E3": self.improvement(key, "E3", "MAE"),
                }
            )
        return rows
