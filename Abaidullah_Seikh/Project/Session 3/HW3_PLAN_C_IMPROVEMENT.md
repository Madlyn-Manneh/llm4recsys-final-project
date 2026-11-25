Written: 2026-11-24T00:37:34+03:00

C+R: the existing C rankings (outputs/arm_C2_200, outputs/sparse_C) re-ordered by a deterministic repeat-first rule. No new model run. Uses only pre-cutoff history from the starter contexts; ranked IDs stay within the 50 candidates.
V1 (recency): candidates the user bought before the cutoff, ordered by most recent pre-cutoff buy date (ties: higher buy count, then C order), then the remaining slots in C's order.
V2 (count): same, ordered by pre-cutoff buy count (ties: more recent, then C order).
Check arm: A+R = A rankings with the V1 rule (does the summary still matter after the rule?).
Selection data: the course's main 200-user protocol. Selection rule: C+R = V1 or V2, whichever has the higher main-200 nDCG@10 (all users); the other is discarded. The sparse 120-user window is a robustness check only. All results are development results; the official evaluation set is the final test.
