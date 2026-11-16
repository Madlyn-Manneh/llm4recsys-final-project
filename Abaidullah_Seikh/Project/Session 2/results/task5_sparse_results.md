# Supplementary cohort: 30 sparse users with future purchases; not the HW2 default protocol

Descriptive results only; no conclusions or significance claims. The main HW2 results are unchanged. The cohort is selected on having nonempty future truth: only the conditional nonempty mean is meaningful. The all-selected-user and nonempty means coincide because all 30 users are labelled; this is not the default 100-user all-user population mean.

## Completion and evaluation checks

- Completion checked on 2026-11-16 at approximately 15:42 +03:00. All C/A/B DONE markers are present; no FAILED marker appears. All raw logs have exactly 30 lines; no llm_rerank.py process was running.
- C finished at 12:33:51, A at 13:04:28, B at 13:34:06, November 16 (+03:00), from the saved loop log.
- All three complete evaluation protocol objects exactly match the supplementary baseline. The four baseline aggregate blocks match at full saved precision in every evaluation.
- Protocol hash: `0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b`.
- The unchanged starter constructs truth; source CSV hashes were checked against the supplementary protocol. Every custom per-user score was verified with starter.ndcg10 using predictions.csv and eligible truth.
- Protected model script SHA-256 remains `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da`.

## Seven-method table

| Method | Users | Users with future purchases | nDCG@10 all users | nDCG@10 nonempty truth | Runtime | Failed cases |
|---|---:|---:|---:|---:|---|---:|
| Popularity | 30 | 30 | 0.2955 | 0.2955 | Not measured for supplementary baseline run | 0 |
| CBF (fixed top-50 no-rerank control) | 30 | 30 | 0.3843 | 0.3843 | Not measured for supplementary baseline run | 0 |
| Latest buy | 30 | 30 | 0.5338 | 0.5338 | Not measured for supplementary baseline run | 0 |
| Latest buy or sell | 30 | 30 | 0.5238 | 0.5238 | Not measured for supplementary baseline run | 0 |
| Arm A (structured) | 30 | 30 | 0.4051 | 0.4051 | 1821.5 s, whole arm, excluding model loading | 0 |
| Arm B (history text) | 30 | 30 | 0.3439 | 0.3439 | 1764.1 s, whole arm, excluding model loading | 0 |
| Arm C (LLM summary) | 30 | 30 | 0.3846 | 0.3846 | 2723.8 s, whole arm, excluding model loading (includes summaries) | 0 |

Baseline rows are copied from `outputs/sparse_arm_A_eval/metrics.json`, confirmed identical to `outputs/sparse_baseline/metrics.json` and the B/C evaluation baseline blocks. Arm rows use method `custom` in the respective `outputs/sparse_arm_{A,B,C}_eval/metrics.json`; invalid counts and times use `outputs/sparse_arm_{A,B,C}/run_meta.json`.

The supplementary baseline command was not externally timed. The main protocol’s 10.77-second baseline runtime is not reused here. Arm timers exclude model loading, initial context/questionnaire reading and later scoring. They include the per-user loop, generation, parsing and log writes. Classical failed cases are 0 (no model output to validate).

| Arm | invalid_outputs | Scoring custom_failures | wall_seconds_whole_arm |
|---|---:|---:|---:|
| A | 0 | 0 | 1821.5 |
| B | 0 | 0 | 1764.1 |
| C | 0 | 0 | 2723.8 |

All three arms used the HF backend, Qwen/Qwen3-1.7B at resolved revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, float32 CPU, greedy decoding and explicit thinking off, seed 0, summary budget 120 and ranking budget 60 new tokens. No model was rerun for scoring or this analysis.

## Paired nDCG@10 differences

Calculated before rounding from custom per_user.csv. Better/equal/worse compares C with the named comparator at full saved precision. All-selected and nonempty populations are the same 30 users.

| Comparison | Users | Mean difference | C better | Equal | C worse | Sum of differences |
|---|---:|---:|---:|---:|---:|---:|
| C−A | 30 | -0.02053634 | 5 | 20 | 5 | -0.616090295854 |
| C−B | 30 | 0.04061788 | 6 | 21 | 3 | 1.218536537397 |

## Hits, Recall@10 and CBF overlap

A hit is a distinct relevant ISIN in the top ten. Recall@10 = hits / number of distinct eligible future ISINs per user; reported means are macro means, not pooled micro recall. CBF overlap is the mean set-intersection size (0–10) and fraction with the original CBF top ten.

| Arm | Users with ≥1 hit (of 30) | Total hits | Recall@10 all selected users | Recall@10 nonempty | Mean CBF top-10 overlap | Mean overlap fraction |
|---|---:|---:|---:|---:|---:|---:|
| A | 19 | 20 | 0.58333333 | 0.58333333 | 8.7000 | 0.8700 |
| B | 17 | 18 | 0.53333333 | 0.53333333 | 7.6333 | 0.7633 |
| C | 19 | 20 | 0.58333333 | 0.58333333 | 6.2333 | 0.6233 |

## Summary mentions and differing-user count

- **11 of 30** C summaries mention at least one exact, case-sensitive history ISIN. This is string presence only, not a factuality judgment.
- **14 of 30** users have different saved nDCG@10 between at least two arms; **16** have equal scores in all three. This counts score differences, not all changes in recommendation lists.
- Evaluation-only top-50 coverage remains **23 of 41** future user–asset labels.

Detailed identified users, truth ISINs, hit positions, scores and verbatim histories/summaries are saved only in `results/task5_sparse_differing_LOCAL.md` and must never be committed. This aggregate report contains no raw customer IDs, histories, prompts, summaries or per-user rows.
