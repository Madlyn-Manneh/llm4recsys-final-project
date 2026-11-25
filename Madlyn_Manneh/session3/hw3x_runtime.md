# HW3x runtime (extension sample)

| Arm | users | wall_seconds_whole_arm | start time | end time | implied start-up seconds |
|---|---|---|---|---|---|
| C | 100 | 8682.8 | 2026-11-22 21:10:21 | 2026-11-22 23:35:22 | 17.6 |
| D | 100 | 9993.8 | 2026-11-22 23:35:25 | 2026-11-23 02:22:14 | 15.4 |
| E | 100 | 9939.8 | 2026-11-23 02:22:16 | 2026-11-23 05:08:10 | 14.1 |
| B | 100 | 4985.8 | 2026-11-23 05:08:12 | 2026-11-23 06:31:32 | 13.9 |

No model was trained.

All four arms ran in offline mode (HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1) as one background chain.

The extension sample was run as a separate users-file run (protocol hash 5bae3e69d666acbc9f80421ffd4a5b6733d197d10a0894822ecd6674cfb413f5).
