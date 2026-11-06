"""[BAB 3 §3.7 | METRIK EVALUASI DAN PENGUJIAN INFERENSI STATISTIK]

Modul ini mengimplementasikan metrik evaluasi peramalan volatilitas dan prosedur
inferensi statistik praregistrasi resmi (Protokol Bab 7 & 8):
1. `qlike_per_obs()` & `qlike()`: Metrik kerugian utama Quasi-Likelihood (QLIKE) bentuk robust Patton (2011)
   pada skala log-variance: L(y, y_hat) = exp(e) - e - 1, di mana e = y - y_hat (selalu >= 0).
2. `mae_rmse_logrv()`: Metrik sekunder deviasi absolut (MAE) dan akar kuadrat galat (RMSE).
3. `dm_test()`: Uji signifikansi komparatif Diebold-Mariano (1995) satu arah dengan estimasi varians
   HAC Newey-West (1987) berbobot kernel Bartlett (lag = 5).
4. `moving_block_bootstrap_mean_ci()`: Interval kepercayaan persentil 95% moving-block bootstrap
   (Künsch 1989) dengan panjang blok 20 hari, 10.000 replikasi, dan seed 42.
"""

from __future__ import annotations

import numpy as np

import s2_config as cfg


# ---------------------------------------------------------------------------
# [BAB 3 §3.7 | METRIK KERUGIAN ASIMETRIS DAN KESALAHAN PREDIKSI]
# ---------------------------------------------------------------------------
def qlike_per_obs(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    [BAB 3 §3.7 | QLIKE PER OBSERVASI (PATTON 2011)]
    Menghitung kerugian QLIKE harian pada skala log-variance:
        e_t = y_true_t - y_pred_t
        loss_t = exp(e_t) - e_t - 1
    Memberikan penalti asimetris lebih berat pada under-prediction volatilitas dibanding over-prediction.
    """
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    return np.exp(e) - e - 1.0


def qlike(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    [BAB 3 §3.7 | METRIK PRIMER: RATA-RATA LOSS QLIKE]
    Rata-rata QLIKE seluruh observasi pada jendela evaluasi. Nilai lebih rendah menunjukkan akurasi lebih tinggi.
    """
    return float(qlike_per_obs(y_true, y_pred).mean())


def mae_rmse_logrv(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """
    [BAB 3 §3.7 | METRIK SEKUNDER: MAE DAN RMSE]
    Mean Absolute Error dan Root Mean Squared Error pada skala log realized volatility.
    """
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    return {"MAE_logRV": float(np.abs(e).mean()),
            "RMSE_logRV": float(np.sqrt((e ** 2).mean()))}


# ---------------------------------------------------------------------------
# [BAB 3 §3.7 | PENGUJIAN HIPOTESIS DIEBOLD-MARIANO (HAC NEWEY-WEST)]
# ---------------------------------------------------------------------------
def dm_test(loss_diff: np.ndarray, lag: int = cfg.DM_HAC_LAG) -> dict[str, float]:
    """
    [BAB 3 §3.7 | UJI DIEBOLD-MARIANO SATU ARAH]
    Menguji hipotesis satu arah H1: mean(d) < 0 (model usulan memiliki loss lebih rendah secara signifikan).
    Menggunakan koreksi autokorelasi HAC Newey-West dengan kernel segitiga Bartlett hingga lag=5.
    """
    d = np.asarray(loss_diff, float).reshape(-1)
    d = d[~np.isnan(d)]
    n = len(d)
    dbar = float(d.mean())
    dc = d - dbar
    gamma0 = float((dc ** 2).mean())
    var = gamma0
    for l in range(1, lag + 1):
        gamma_l = float((dc[l:] * dc[:-l]).mean())
        w = 1.0 - l / (lag + 1.0)          # Pembobotan Bartlett
        var += 2.0 * w * gamma_l
    var = max(var, 1e-24)
    dm = dbar / np.sqrt(var / n)
    from math import erf, sqrt

    p_one_sided = 0.5 * (1.0 + erf(dm / sqrt(2.0)))  # P(Z <= dm)
    return {"dm_stat": float(dm), "p_one_sided": float(p_one_sided),
            "mean_diff": dbar, "n": int(n)}


# ---------------------------------------------------------------------------
# [BAB 3 §3.7 | MOVING-BLOCK BOOTSTRAP CONFIDENCE INTERVAL (KÜNSCH 1989)]
# ---------------------------------------------------------------------------
def moving_block_bootstrap_mean_ci(
    diff: np.ndarray,
    block: int = cfg.BOOTSTRAP_BLOCK,
    reps: int = cfg.BOOTSTRAP_REPS,
    seed: int = cfg.BOOTSTRAP_SEED,
    alpha: float = cfg.ALPHA,
) -> dict[str, float]:
    """
    [BAB 3 §3.7 | INTERVAL KEPERCAYAAN MOVING-BLOCK BOOTSTRAP]
    Mengestimasi interval kepercayaan persentil 95% atas perbedaan loss rerata delta QLIKE.
    Blok berukuran 20 hari mempertahankan struktur dependensi serial data deret waktu harian.
    Syarat kesuksesan praregistrasi: batas atas CI (ci_high) harus < 0.
    """
    d = np.asarray(diff, float).reshape(-1)
    d = d[~np.isnan(d)]
    n = len(d)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts_max = n - block
    means = np.empty(reps)
    for b in range(reps):
        starts = rng.integers(0, starts_max + 1, size=n_blocks)
        idx = (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:n]
        means[b] = d[idx].mean()
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    p_one_sided = float((means >= 0.0).mean())
    return {"ci_low": float(lo), "ci_high": float(hi),
            "mean_diff": float(d.mean()), "p_boot_one_sided": p_one_sided,
            "n": int(n), "block": int(block), "reps": int(reps)}


def paired_loss_diff(
    dates_a: np.ndarray, loss_a: np.ndarray,
    dates_b: np.ndarray, loss_b: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    [BAB 3 §3.7 | PENYELARASAN SELISIH LOSS BERPASANGAN]
    Menyelaraskan dua deret loss harian berdasarkan irisan tanggal observasi yang sama (a - b).
    """
    da = np.asarray(dates_a)
    db = np.asarray(dates_b)
    common, ia, ib = np.intersect1d(da, db, return_indices=True)
    if len(common) == 0:
        raise ValueError("Tidak ada tanggal yang beririsan.")
    return common, np.asarray(loss_a, float)[ia] - np.asarray(loss_b, float)[ib]
