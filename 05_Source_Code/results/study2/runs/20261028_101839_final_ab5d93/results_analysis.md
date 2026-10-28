# Study 2 Analysis (20261028_101839_final_ab5d93)

## VAL (n=731)

| Model | QLIKE | MAE_logRV | RMSE_logRV |
|---|---|---|---|
| lstm_optuna | 0.49372 | 0.75375 | 0.96071 |
| lstm_untuned | 0.43238 | 0.72278 | 0.92472 |
| persistence | 0.76115 | 0.90005 | 1.12565 |
| har_rv | 0.42676 | 0.71494 | 0.91463 |
| garch11 | 0.45779 | 0.93518 | 1.19949 |

### Comparisons (a = lstm_optuna)
- vs persistence: ΔQLIKE mean -0.26743; DM p(one-sided)=0.0000; boot 95% CI [-0.34170, -0.16315]
- vs har_rv: ΔQLIKE mean +0.06696; DM p(one-sided)=1.0000; boot 95% CI [0.03621, 0.09665]
- vs garch11: ΔQLIKE mean +0.03593; DM p(one-sided)=0.8665; boot 95% CI [-0.03685, 0.09819]
- vs lstm_untuned: ΔQLIKE mean +0.06134; DM p(one-sided)=1.0000; boot 95% CI [0.03931, 0.08020]

## TEST (n=273)

| Model | QLIKE | MAE_logRV | RMSE_logRV |
|---|---|---|---|
| lstm_optuna | 0.40333 | 0.66620 | 0.88531 |
| lstm_untuned | 0.34422 | 0.58659 | 0.76144 |
| persistence | 0.80521 | 0.85026 | 1.09996 |
| har_rv | 0.46846 | 0.68046 | 0.90767 |
| garch11 | 0.44898 | 0.93533 | 1.18944 |

### Comparisons (a = lstm_optuna)
- vs persistence: ΔQLIKE mean -0.40188; DM p(one-sided)=0.0000; boot 95% CI [-0.55787, -0.22960]
- vs har_rv: ΔQLIKE mean -0.06513; DM p(one-sided)=0.0534; boot 95% CI [-0.14468, -0.00840]
- vs garch11: ΔQLIKE mean -0.04564; DM p(one-sided)=0.1822; boot 95% CI [-0.11977, 0.04563]
- vs lstm_untuned: ΔQLIKE mean +0.05911; DM p(one-sided)=0.9724; boot 95% CI [-0.01878, 0.12355]

**VERDICT: mixed_beats_but_not_significant**
