# HW3 runtime

| Arm | users | wall_seconds_whole_arm | start time | end time | implied start-up seconds |
|---|---|---|---|---|---|
| B | 100 | 5568.4 | 2026-11-22 11:40:11 | 2026-11-22 13:13:17 | 17.6 |
| C | 100 | 8367.7 | HW2 run, not recorded | not recorded | - |
| D | 100 | 11205.8 | HW2 run, not recorded | not recorded | - |
| E | 100 | 10194.0 | 2026-11-22 16:08:42 | 2026-11-22 18:58:52 | 15.4 |

No model training was done.

The first arm E attempt (outputs\hw3_E.log, about 13:14) failed at start-up with a network name-resolution error before any output was written and is not part of the results.

The E rerun used HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1.
