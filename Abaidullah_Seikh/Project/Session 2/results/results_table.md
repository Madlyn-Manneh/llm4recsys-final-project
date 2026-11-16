# HW2 results — FAR-Trans, Team 8

All 100 selected users are retained; 11 have future purchases and 89 have empty truth. Scores are displayed to four decimals.

| Method | Users | Users with future purchases | nDCG@10 all users | nDCG@10 nonempty truth | Runtime | Failed cases |
|---|---:|---:|---:|---:|---|---:|
| Popularity | 100 | 11 | 0.0286 | 0.2599 | 10.77 s, whole starter run, all four baselines | 0 |
| CBF (no-rerank control: candidates are the CBF top 50) | 100 | 11 | 0.0201 | 0.1827 | 10.77 s, whole starter run, all four baselines | 0 |
| Latest buy | 100 | 11 | 0.0277 | 0.2520 | 10.77 s, whole starter run, all four baselines | 0 |
| Latest buy or sell | 100 | 11 | 0.0271 | 0.2464 | 10.77 s, whole starter run, all four baselines | 0 |
| Arm A (structured) | 100 | 11 | 0.0204 | 0.1851 | 6296.8 s, whole arm, excluding model loading | 0 |
| Arm B (history text) | 100 | 11 | 0.0228 | 0.2076 | 6346.9 s, whole arm, excluding model loading | 0 |
| Arm C (LLM summary) | 100 | 11 | 0.0248 | 0.2257 | 9604.6 s, whole arm, excluding model loading (C includes summaries) | 0 |

Sources: baseline rows copied from `outputs/arm_A_eval/metrics.json`, identical in `outputs/arm_B_eval/metrics.json` and `outputs/arm_C_eval/metrics.json` and the original baseline. A/B/C rows use the respective evaluation files, method `custom`. Arm runtimes and invalid counts use `outputs/arm_A/run_meta.json`, `outputs/arm_B/run_meta.json`, and `outputs/arm_C/run_meta.json`. Classical failed cases are 0 (no model output to validate); each arm has 0 starter custom failures as well as 0 invalid model rankings.

The four baseline rows share one externally measured 10.77-second run; the time is not charged four times. Arm timers exclude model loading and initial context/questionnaire reading, and do not include this separate scoring run. Arm C includes both summary and ranking calls.

Full shared protocol hash: `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417`. All evaluation protocols are exactly equal to the baseline protocol, and all four baseline aggregate blocks match at full saved precision.
