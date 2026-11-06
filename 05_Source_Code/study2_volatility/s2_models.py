"""[BAB 3 §3.5 | PEMODELAN SEKUENS, ARSITEKTUR LSTM, DAN MODEL BASELINE]

Modul inti untuk pemrosesan sekuens deret waktu dan pembangunan model Study 2:
1. `build_samples()`: Pembentukan tensor sekuens 3D (sampel x lookback x fitur) dengan
   penolakan tegas (fail-closed) terhadap jendela yang melintasi celah kalender (Amandemen A1).
2. `fit_scaler()` & `transform_xy()`: Standarisasi z-score fit HANYA pada data latih fold.
3. `build_lstm_model()` & `train_one()`: Arsitektur LSTM teregulasi dropout, loss MSE pada target
   log-RV terstandarisasi, dan early stopping deterministik berbasis seed.
4. `har_design()` & `har_fit_predict()`: Model ekonometrika Heterogeneous Autoregressive (HAR-RV Corsi 2009)
   dengan estimasi parameter OLS tanpa bobot buatan.
5. `garch_forecasts()`: Model GARCH(1,1) Bollerslev (1986) dengan estimasi QML dan skema expanding
   window bulanan satu-langkah-ke-depan (one-step-ahead).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

import s2_config as cfg

os_environ_tf = None  # TensorFlow diimpor secara dinamis saat pembangunan model


# ---------------------------------------------------------------------------
# [BAB 3 §3.3 | KONSTRUKSI JENDELA SAMPEL & INTEGRITAS CELAH KALENDER A1]
# ---------------------------------------------------------------------------
def build_samples(
    df: pd.DataFrame,
    lookback: int,
    feature_cols: list[str] | None = None,
    target_col: str = cfg.TARGET,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    [BAB 3 §3.3 | KONSTRUKSI SAMPEL SEKUENS]
    Membangun pasangan fitur sekuens X dan target y untuk peramalan 1 hari ke depan.

    Prinsip Kausalitas dan Anti-Leakage:
    - Target hari T (log_rv_T) diramalkan murni dari fitur lookback hari sebelumnya:
      rentang hari T-lookback sampai T-1 (fitur hari <= t meramalkan log_rv_{t+1}).
    - Sesuai Amandemen Protokol A1, setiap jendela yang memuat nilai NaN atau melintasi
      hari kalender yang hilang (misal maintenance Binance 2020-02-19) DITOLAK (dikeluarkan).

    Returns:
        tuple: (X [N, lookback, n_features], y [N], feature_end_dates [N], target_dates [N])
    """
    feature_cols = feature_cols or cfg.FEATURES
    dates = df["date"].to_numpy()
    feats = df[feature_cols].to_numpy(dtype=float)
    target = df[target_col].to_numpy(dtype=float)
    n_days = len(df)
    date_int = df["date"].map(pd.Timestamp.timestamp).to_numpy()

    X_list, y_list, fend_list, tdate_list = [], [], [], []
    for i in range(n_days - lookback):          # jendela fitur berakhir di i + lookback - 1
        j = i + lookback                        # indeks baris target
        # Kontiguitas kalender penuh: interval antar baris harus tepat 86.400 detik (1 hari)
        if not np.all(np.diff(date_int[i : j + 1]) == 86400.0):
            continue
        if np.isnan(feats[i:j]).any() or np.isnan(target[j]):
            continue
        X_list.append(feats[i:j])
        y_list.append(target[j])
        fend_list.append(dates[i + lookback - 1])
        tdate_list.append(dates[j])

    X = np.asarray(X_list, dtype=float)
    y = np.asarray(y_list, dtype=float)
    return X, y, np.asarray(fend_list), np.asarray(tdate_list)


# ---------------------------------------------------------------------------
# [BAB 3 §3.4 | ISOLASI STANDARISASI DATA LATIH]
# ---------------------------------------------------------------------------
def fit_scaler(X_train: np.ndarray, y_train: np.ndarray):
    """
    [BAB 3 §3.4 | STANDARISASI HANYA PADA DATA LATIH]
    Mengepaskan StandardScaler (mean=0, std=1) HANYA pada partisi data latih (training fold/fit).
    Mencegah kebocoran data (data leakage) dari partisi validasi atau uji ke dalam parameter skala.
    """
    scaler_x = StandardScaler().fit(X_train.reshape(len(X_train), -1))
    scaler_y = StandardScaler().fit(y_train.reshape(-1, 1))
    return scaler_x, scaler_y


def transform_xy(scaler_x, scaler_y, X: np.ndarray, y: np.ndarray):
    """
    [BAB 3 §3.4 | TRANSFORMASI SKALA DATA]
    Menerapkan transformasi z-score pada fitur X dan target y menggunakan scaler yang telah di-fit.
    """
    Xs = scaler_x.transform(X.reshape(len(X), -1)).reshape(X.shape)
    ys = scaler_y.transform(y.reshape(-1, 1)).reshape(-1)
    return Xs, ys


# ---------------------------------------------------------------------------
# [BAB 3 §3.5 | ARSITEKTUR MODEL LSTM DAN PROSEDUR PELATIHAN]
# ---------------------------------------------------------------------------
def build_lstm_model(
    lookback: int, units: int, dropout: float, learning_rate: float,
    layers: int = 1, n_features: int | None = None,
):
    """
    [BAB 3 §3.5 | SPESIFIKASI ARSITEKTUR LSTM]
    Membangun model Sequential Keras berisi 1 atau 2 layer LSTM, regulasi Dropout,
    dan 1 unit Dense linear untuk regresi. Fungsi objektif loss menggunakan MSE
    terhadap target log-RV yang terstandarisasi.
    """
    import os
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
    from tensorflow.keras.models import Sequential

    n_features = n_features or len(cfg.FEATURES)
    model = Sequential()
    model.add(Input(shape=(lookback, n_features)))
    for k in range(layers):
        return_seq = k < layers - 1
        model.add(LSTM(units, return_sequences=return_seq))
        model.add(Dropout(dropout))
    model.add(Dense(1))
    model.compile(
        optimizer=__import__("tensorflow").keras.optimizers.Adam(learning_rate),
        loss="mean_squared_error",
    )
    _ = EarlyStopping
    return model


def train_one(
    X_train, y_train, X_val, y_val, params: dict, seed: int,
    max_epochs: int = cfg.MAX_EPOCHS, patience: int = cfg.EARLY_STOP_PATIENCE,
):
    """
    [BAB 3 §3.5 | PELATIHAN DAN EARLY STOPPING DETERMINISTIK]
    Melatih satu instans model LSTM secara deterministik untuk kombinasi (seed, params, data).
    Memantau val_loss dengan EarlyStopping(patience=10, restore_best_weights=True).
    Mengembalikan model berbobot optimal dan indeks epoch terbaik.
    """
    import random

    import tensorflow as tf

    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    try:
        tf.keras.utils.set_random_seed(seed)
    except AttributeError:
        pass

    model = build_lstm_model(
        lookback=params["lookback"], units=params["units"],
        dropout=params["dropout"], learning_rate=params["learning_rate"],
        layers=params["layers"], n_features=X_train.shape[2],
    )
    hist = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=max_epochs, batch_size=params["batch_size"], shuffle=False,
        verbose=0,
        callbacks=[tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=patience, restore_best_weights=True)],
    )
    best_epoch = int(np.argmin(hist.history["val_loss"])) + 1
    return model, best_epoch


# ---------------------------------------------------------------------------
# [BAB 3 §3.5 | BASELINE PRIMARY: MODEL HAR-RV (CORSI 2009)]
# ---------------------------------------------------------------------------
def har_design(
    log_rv: np.ndarray, dates: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    [BAB 3 §3.5 | MATRIKS DESAIN HAR-RV]
    Membangun matriks regresi HAR-RV:
      log_rv_{t+1} = beta_0 + beta_d * log_rv_t + beta_w * mean(log_rv_{t-6..t}) + beta_m * mean(log_rv_{t-21..t}) + eps.
    Jika dates disertakan, setiap baris yang rentang historisnya (22 hari) atau targetnya (t+1)
    melintasi celah kalender (>1 hari) akan ditolak secara ketat.
    """
    log_rv = np.asarray(log_rv, dtype=float)
    date_index = pd.DatetimeIndex(dates) if dates is not None else None
    rows, targets = [], []
    for t in range(21, len(log_rv) - 1):
        if date_index is not None:
            span = date_index[t - 21 : t + 2]
            if len(span) != 23 or not np.all(np.diff(span.values) == np.timedelta64(1, "D")):
                continue
        vals = log_rv[t - 21 : t + 1]
        if len(vals) != 22 or not np.isfinite(vals).all() or not np.isfinite(log_rv[t + 1]):
            continue
        rows.append([1.0, log_rv[t], log_rv[t - 6 : t + 1].mean(), vals.mean()])
        targets.append(log_rv[t + 1])
    return np.asarray(rows, dtype=float).reshape(-1, 4), np.asarray(targets, dtype=float)


def har_fit_predict(log_rv: np.ndarray, dates: np.ndarray, train_end_ts: float):
    """
    [BAB 3 §3.5 | ESTIMASI PARAMETER OLS DAN PREDIKSI HAR-RV]
    Mengepaskan koefisien beta OLS pada sampel valid dengan target_date <= train_end.
    Menghasilkan vektor ramalan untuk seluruh baris sampel kontigu yang tersedia.
    """
    log_rv = np.asarray(log_rv, dtype=float)
    date_index = pd.DatetimeIndex(dates)
    X, y = har_design(log_rv, dates)
    target_dates = np.asarray([
        date_index[t + 1]
        for t in range(21, len(log_rv) - 1)
        if len(date_index[t - 21 : t + 2]) == 23
        and np.all(np.diff(date_index[t - 21 : t + 2].values) == np.timedelta64(1, "D"))
        and np.isfinite(log_rv[t - 21 : t + 2]).all()
    ])
    if len(target_dates) != len(y):
        raise ValueError("HAR sample/date alignment invariant failed")
    train_mask = pd.DatetimeIndex(target_dates) <= pd.Timestamp(train_end_ts)
    if not train_mask.any():
        raise ValueError("No valid HAR training samples before train_end")
    beta, *_ = np.linalg.lstsq(X[train_mask], y[train_mask], rcond=None)
    return target_dates, X @ beta, beta


# ---------------------------------------------------------------------------
# [BAB 3 §3.5 | BASELINE SECONDARY: MODEL GARCH(1,1) (BOLLERSLEV 1986)]
# ---------------------------------------------------------------------------
def daily_log_returns_after_last_gap(dates: np.ndarray, closes: np.ndarray) -> pd.Series:
    """
    [BAB 3 §3.5 | RETURN HARIAN BEBAS CELAH MULTI-HARI]
    Mengekstrak log return harian dari segmen kontigu kalender terakhir.
    Return multi-hari yang melintasi celah kalender dibuang agar tidak merusak estimasi varians.
    """
    idx = pd.DatetimeIndex(dates)
    close_values = np.asarray(closes, dtype=float)
    if idx.has_duplicates or not idx.is_monotonic_increasing:
        raise ValueError("GARCH input dates must be unique and increasing")
    if len(close_values) != len(idx) or not np.isfinite(close_values).all() or (close_values <= 0).any():
        raise ValueError("GARCH closes must be finite, positive, and aligned with dates")
    if len(idx) < 2:
        return pd.Series(dtype=float, index=pd.DatetimeIndex([]))
    contiguous = np.diff(idx.values) == np.timedelta64(1, "D")
    gaps = np.flatnonzero(~contiguous)
    first_return_pos = int(gaps[-1] + 1) if len(gaps) else 0
    returns = np.diff(np.log(close_values))[first_return_pos:]
    return_dates = idx[1:][first_return_pos:]
    if len(return_dates) > 1 and not np.all(np.diff(return_dates.values) == np.timedelta64(1, "D")):
        raise ValueError("GARCH final return segment is not calendar-contiguous")
    return pd.Series(returns, index=return_dates)


def garch_forecasts(
    dates: np.ndarray, closes: np.ndarray,
    window_start: str, window_end: str,
) -> pd.DataFrame:
    """
    [BAB 3 §3.5 | PERAMALAN WALK-FORWARD GARCH(1,1) EXPANDING WINDOW]
    Untuk setiap bulan kalender di dalam [window_start, window_end]:
    1. Refit GARCH(1,1) QML Normal pada seluruh return hingga akhir bulan sebelumnya (cutoff).
    2. Terapkan parameter pada deret data (.fix) untuk mengekstrak varians bersyarat 1-hari-ke-depan
       secara kausal (tanpa kebocoran informasi masa depan).
    3. Input dibatasi strictly <= window_end agar kebal terhadap celah kalender masa depan.
    """
    date_idx = pd.DatetimeIndex(dates)
    w_end_ts = pd.Timestamp(window_end)
    valid_mask = date_idx <= w_end_ts
    dates_causal = np.asarray(dates)[valid_mask]
    closes_causal = np.asarray(closes)[valid_mask]
    log_ret = daily_log_returns_after_last_gap(dates_causal, closes_causal)
    if log_ret.empty:
        raise ValueError("GARCH has no daily returns after calendar-gap handling")

    from arch import arch_model

    log_ret = log_ret.dropna()
    months = sorted({(d.year, d.month) for d in log_ret.index
                     if pd.Timestamp(window_start) <= d <= pd.Timestamp(window_end)})

    out = []
    for y, m in months:
        month_first = pd.Timestamp(year=y, month=m, day=1)
        cutoff = month_first - pd.Timedelta(days=1)
        train = log_ret[log_ret.index <= cutoff] * 100.0
        res = arch_model(train, mean="Constant", vol="GARCH", p=1, q=1,
                         dist="normal").fit(disp="off", show_warning=False)
        am_full = arch_model(log_ret * 100.0, mean="Constant", vol="GARCH",
                             p=1, q=1, dist="normal")
        fixed = am_full.fix(res.params)
        # Mulai dari cutoff: baris one-step meramalkan tanggal 1 bulan target
        start_pos = int(np.searchsorted(log_ret.index.values, np.datetime64(cutoff)))
        fc = fixed.forecast(horizon=1, start=start_pos, reindex=False)
        var_pct = fc.variance.iloc[:, 0].to_numpy()
        fc_days = log_ret.index[start_pos + 1 : start_pos + 1 + len(var_pct)]
        for d, v in zip(fc_days, var_pct):
            if pd.Timestamp(window_start) <= d <= pd.Timestamp(window_end):
                out.append((d, float(np.log(v / 1e4))))
    return pd.DataFrame(out, columns=["date", "log_var"]).drop_duplicates("date")
