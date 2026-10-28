"""
s2_models.py - Sequence building, LSTM, and statistical model baselines.

Shared by the untuned LSTM, the Optuna HPO loop, and the final run:
- build_samples(): lookback windows over the frozen daily frame; windows are
  only constructed when all days are calendar-contiguous and feature-complete
  (protocol section 2 and amendment A1);
- fit_scaler(): StandardScaler on training rows only (target included);
- build_lstm_model(): small stack, MSE loss on standardized log-RV;
- har_fit / har_predict(): HAR-RV via least squares (no intercept-free tricks);
- garch_forecasts(): GARCH(1,1) QML on daily log returns x100, refit expanding
  at the start of each month, one-step conditional variance in log scale.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

import s2_config as cfg

os_environ_tf = None  # TF imported lazily in builders


# ---------------------------------------------------------------------------
# Sample construction
# ---------------------------------------------------------------------------
def build_samples(
    df: pd.DataFrame,
    lookback: int,
    feature_cols: list[str] | None = None,
    target_col: str = cfg.TARGET,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Return (X, y, feature_end_dates, target_dates).

    Sample for target day T uses features of the lookback days ending at T-1
    (i.e., prediction of log_rv_{t+1} from day <= t). Windows are kept only if
    every involved day exists, is contiguous, and has no NaN features/target.
    """
    feature_cols = feature_cols or cfg.FEATURES
    dates = df["date"].to_numpy()
    feats = df[feature_cols].to_numpy(dtype=float)
    target = df[target_col].to_numpy(dtype=float)
    n_days = len(df)
    date_int = df["date"].map(pd.Timestamp.timestamp).to_numpy()

    X_list, y_list, fend_list, tdate_list = [], [], [], []
    for i in range(n_days - lookback):          # window ends at i, target at i+1
        j = i + lookback                        # target row index
        # calendar contiguity across the whole window (feature days + target day)
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


def fit_scaler(X_train: np.ndarray, y_train: np.ndarray):
    scaler_x = StandardScaler().fit(X_train.reshape(len(X_train), -1))
    scaler_y = StandardScaler().fit(y_train.reshape(-1, 1))
    return scaler_x, scaler_y


def transform_xy(scaler_x, scaler_y, X: np.ndarray, y: np.ndarray):
    Xs = scaler_x.transform(X.reshape(len(X), -1)).reshape(X.shape)
    ys = scaler_y.transform(y.reshape(-1, 1)).reshape(-1)
    return Xs, ys


# ---------------------------------------------------------------------------
# LSTM
# ---------------------------------------------------------------------------
def build_lstm_model(
    lookback: int, units: int, dropout: float, learning_rate: float,
    layers: int = 1, n_features: int | None = None,
):
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
    _ = EarlyStopping  # referenced for API parity; actual callbacks built in train loop
    return model


def train_one(
    X_train, y_train, X_val, y_val, params: dict, seed: int,
    max_epochs: int = cfg.MAX_EPOCHS, patience: int = cfg.EARLY_STOP_PATIENCE,
):
    """Train one LSTM; deterministic for (seed, params, data)."""
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
# HAR-RV
# ---------------------------------------------------------------------------
def har_design(log_rv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Rows t = 21..n-2: target log_rv[t+1] from day-t information
    [log_rv[t], mean(log_rv[t-6..t]), mean(log_rv[t-21..t]), 1].
    """
    y = log_rv[22:]
    daily = log_rv[21:-1]
    weekly = np.array([log_rv[t - 6 : t + 1].mean() for t in range(21, len(log_rv) - 1)])
    monthly = np.array([log_rv[t - 21 : t + 1].mean() for t in range(21, len(log_rv) - 1)])
    X = np.column_stack([np.ones_like(daily), daily, weekly, monthly])
    return X, y


def har_fit_predict(log_rv: np.ndarray, dates: np.ndarray, train_end_ts: float):
    """Fit HAR on rows whose TARGET day <= train_end; predict all later rows."""
    X, y = har_design(log_rv)
    target_dates = dates[22:]
    beta, *_ = np.linalg.lstsq(X[target_dates <= train_end_ts],
                               y[target_dates <= train_end_ts], rcond=None)
    preds = X @ beta
    return target_dates, preds, beta


# ---------------------------------------------------------------------------
# GARCH(1,1)
# ---------------------------------------------------------------------------
def garch_forecasts(
    dates: np.ndarray, closes: np.ndarray,
    window_start: str, window_end: str,
) -> pd.DataFrame:
    """
    Walk-forward GARCH(1,1), one-step conditional variance per day.

    For each calendar month inside [window_start, window_end]:
      - refit (QML, Normal) expanding on all returns up to the last day of the
        previous month;
      - apply the fitted parameters to the full observed sample (arch .fix)
        and extract the filtered one-step-ahead variance for every day of the
        month (uses only returns up to each day t -> no leakage).
    Returns DataFrame [date, log_var] for the requested window.
    """
    from arch import arch_model

    idx = pd.DatetimeIndex(dates)
    log_ret = pd.Series(np.diff(np.log(np.asarray(closes, float))),
                        index=idx[1:]).dropna()
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
        # start at the cutoff day: its one-step row forecasts the 1st of month
        start_pos = int(np.searchsorted(log_ret.index.values, np.datetime64(cutoff)))
        fc = fixed.forecast(horizon=1, start=start_pos, reindex=False)
        # row at position p forecasts variance of day p+1 (one step ahead)
        var_pct = fc.variance.iloc[:, 0].to_numpy()
        fc_days = log_ret.index[start_pos + 1 : start_pos + 1 + len(var_pct)]
        for d, v in zip(fc_days, var_pct):
            if pd.Timestamp(window_start) <= d <= pd.Timestamp(window_end):
                out.append((d, float(np.log(v / 1e4))))
    return pd.DataFrame(out, columns=["date", "log_var"]).drop_duplicates("date")
