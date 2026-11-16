# Task 3b — descriptive aggregate analysis

No statistical, causal, or substantive conclusions are drawn here. All analyses use the same 100 users. Empty truth contributes zero to nDCG and to the all-user macro Recall@10 defined below. Future labels are used only for evaluation after generation, never as model input.

## Evaluation checks

- All three evaluation protocol objects exactly equal `outputs/baseline/protocol.json`.
- Full protocol hash: `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417`.
- Four baseline aggregate blocks exactly match the original saved values in every evaluation.
- A/B/C each have 100 responses, 0 invalid outputs and 0 custom failures. Per-user nDCG was cross-checked using the imported starter metric and evaluated rankings.

## a. Paired nDCG@10 differences

Better/equal/worse compares C with its comparator at full saved float precision (no rounding before comparison).

| Difference | Users | Mean difference | C better | Equal | C worse |
|---|---:|---:|---:|---:|---:|
| C−A, all | 100 | 0.00446395 | 3 | 97 | 0 |
| C−A, nonempty | 11 | 0.04058133 | 3 | 8 | 0 |
| C−B, all | 100 | 0.00198970 | 1 | 99 | 0 |
| C−B, nonempty | 11 | 0.01808818 | 1 | 10 | 0 |

## b. Hits and Recall@10

Recall@10 per user = distinct relevant ISINs in top ten / distinct eligible future Buy ISINs; empty truth is 0. Means below are macro means, not pooled micro recall. Hits are independently counted from evaluated rankings and imported starter truth.

| Arm | Nonempty users with ≥1 hit (of 11) | Total hits | Recall@10 all (100) | Recall@10 nonempty (11) |
|---|---:|---:|---:|---:|
| A | 5 | 5 | 0.03666667 | 0.33333333 |
| B | 5 | 5 | 0.03666667 | 0.33333333 |
| C | 5 | 5 | 0.03666667 | 0.33333333 |

## c. Sparse users (1–5 historical Buys)

Sparse means sum of saved eligible-history buy_count is 1–5, not 1–5 distinct assets. There are 65 sparse users: 2 with future purchases and 63 with empty truth. Individual values and identifiers are in the local-only analysis; this file contains aggregates only.

| Arm | Sparse all-user nDCG@10 (65) | Sparse nonempty nDCG@10 (2) |
|---|---:|---:|
| A | 0.00000000 | 0.00000000 |
| B | 0.00000000 | 0.00000000 |
| C | 0.00000000 | 0.00000000 |

## d. Candidate-order behaviour

Overlap is set intersection size with the CBF top ten (0–10); its fraction is overlap/10. Candidate numbers are positions in the original fixed top-50 pool. Ascending means strictly increasing returned candidate numbers, not necessarily consecutive or 1–10.

| Arm | Mean overlap count | Mean overlap fraction | Candidate 1 ranked first (of 100) | Ascending rankings (of 100) |
|---|---:|---:|---:|---:|
| A | 9.0400 | 0.9040 | 83 | 74 |
| B | 7.2400 | 0.7240 | 93 | 89 |
| C | 6.4700 | 0.6470 | 91 | 84 |

## e. Previously bought assets in recommendations

A repeated asset is a recommendation whose ISIN occurs anywhere in the full pre-cutoff Buy history, not only its capped prompt rows. This measures recommendations, not observed future repeat transactions.

| Arm | Users with ≥1 previously bought asset (of 100) | Previously bought recommendation slots (of 1000) | Mean count/user | Slot fraction |
|---|---:|---:|---:|---:|
| A | 95 | 210 | 2.1000 | 0.2100 |
| B | 95 | 200 | 2.0000 | 0.2000 |
| C | 94 | 188 | 1.8800 | 0.1880 |

## f. Candidate label coverage (evaluation only)

Using the unchanged imported `starter.load_data()` truth construction and its eligible-ID intersection, **6 of 18** future user–asset labels fall in their user’s fixed top-50 pool, across **6** users. The team reference **6/18 matches**. User IDs and covered labels are listed only in the local-only report.

The CSV source hashes were checked against the original protocol before loading truth. Exact duplicates and negative-ID initial positions, Buy-only relevance, strict cutoff/horizon, and eligible assets are handled by the starter rather than reimplemented.

## g. Summary ISIN mentions and manual-check sample

**20 of 100** C summaries mention at least one exact, case-sensitive ISIN from that user’s full history. This is a string-presence count, not a factuality judgment.

Ten summaries and their exact history texts are in local-only `results/task3_analysis.md`. Selection uses `random.Random(42).sample(protocol_users, 10)` in the saved protocol order. No summary judgments are made in this task.

## h. Tokens and latency

Prompt counts reconstruct the actual system/user chat template with the pinned local Qwen3 tokenizer, add_generation_prompt=True and enable_thinking=False, then tokenize as HFBackend.chat does. They include chat formatting. Output counts re-tokenize saved decoded/stripped text without special tokens; EOS and removed special tokens are not recoverable, so these are saved-text token counts, not exact model generation-token usage. No model or inference was loaded. Summary tokens are included only for C.

| Arm | Stage | Prompt total | Prompt mean | Prompt min/median/max | Output total | Output mean | Output min/median/max |
|---|---|---:|---:|---|---:|---:|---|
| A | rank | 194334 | 1943.34 | 1572/1892/2495 | 3480 | 34.80 | 34/34/39 |
| B | rank | 189449 | 1894.49 | 1513/1849/2492 | 3641 | 36.41 | 34/36/42 |
| C | rank | 177748 | 1777.48 | 1527/1650/2292 | 3712 | 37.12 | 34/37/42 |
| C | summary | 27992 | 279.92 | 140/203/996 | 7089 | 70.89 | 50/67/120 |

| Arm | Combined prompt tokens | Combined saved-output tokens | Whole-arm seconds | Mean seconds/user |
|---|---:|---:|---:|---:|
| A | 194334 | 3480 | 6296.8 | 62.968 |
| B | 189449 | 3641 | 6346.9 | 63.469 |
| C | 205740 | 10801 | 9604.6 | 96.046 |

Seconds/user is whole-arm recorded loop time / 100, excluding model loading and initial context/questionnaire reads; C includes summaries. Raw logs have no per-call or per-user timing, so individual latency distributions cannot be recovered. No individual timings, monetary cost, energy cost, or significance results are invented.

Sources: `outputs/arm_{A,B,C}_eval/per_user.csv`, `predictions.csv`/saved response rankings, `metrics.json`, baseline contexts/protocol, original run metadata and raw logs. Analysis helpers, per-user token tables, truth identifiers, and raw examples remain local.
