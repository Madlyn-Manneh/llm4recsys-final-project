# RQ2 development evaluation

All 200 users retained; 24 nonempty truth users; 176 empty truth users score zero.
History before 2021-06-01; eligible Buy truth in [2021-06-01, 2021-07-01). All frozen starter baselines independently matched.

| Method | Users | Nonempty truth | nDCG@10 all | nDCG@10 nonempty | Hit coverage all |
|---|---:|---:|---:|---:|---:|
| popularity | 200 | 24 | 0.0342 | 0.2852 | 0.0800 |
| cbf | 200 | 24 | 0.0305 | 0.2539 | 0.0700 |
| latest_buy | 200 | 24 | 0.0474 | 0.3946 | 0.0950 |
| latest_buy_or_sell | 200 | 24 | 0.0484 | 0.4033 | 0.0950 |
| raw | 200 | 24 | 0.0304 | 0.2531 | 0.0650 |
| summary | 200 | 24 | 0.0286 | 0.2385 | 0.0600 |
| template | 200 | 24 | 0.0334 | 0.2784 | 0.0700 |
| supplied ranker (separate comparison) | 200 | 24 | 0.0306 | 0.2551 | 0.0700 |

## Paired differences

Descriptive paired differences; full precision in JSON/CSV. No significance or generalization claim.

| Difference / subset | n | Mean delta | Improved | Worsened | Unchanged |
|---|---:|---:|---:|---:|---:|
| summary_minus_raw / all | 200 | -0.0018 | 1 | 3 | 196 |
| summary_minus_raw / nonempty_truth | 24 | -0.0146 | 1 | 3 | 20 |
| summary_minus_raw / sparse | 128 | 0.0000 | 0 | 0 | 128 |
| template_minus_raw / all | 200 | 0.0030 | 6 | 5 | 189 |
| template_minus_raw / nonempty_truth | 24 | 0.0253 | 6 | 5 | 13 |
| template_minus_raw / sparse | 128 | 0.0034 | 1 | 0 | 127 |
| summary_minus_template / all | 200 | -0.0048 | 5 | 6 | 189 |
| summary_minus_template / nonempty_truth | 24 | -0.0398 | 5 | 6 | 13 |
| summary_minus_template / sparse | 128 | -0.0034 | 0 | 1 | 127 |

## Candidate reachability and failures

Pool reaches truth for 15 users; 9 nonempty users have no reachable truth. Reachable user–truth pairs: 18/60.
Pool oracle nDCG@10: 0.0581 all / 0.4844 nonempty. Oracle hit coverage: 0.0750 all / 0.6250 nonempty. IDCG always includes all eligible truth.

| Variant | Repairs | Fallbacks | Rank caps | Context errors | Reachable users with no top-10 hit | Mean oracle gap |
|---|---:|---:|---:|---:|---:|---:|
| raw | 0 | 0 | 0 | 0 | 2 | 0.0278 |
| summary | 2 | 0 | 0 | 0 | 3 | 0.0295 |
| template | 1 | 0 | 0 | 0 | 1 | 0.0247 |
| provided | 0 | 47 | 0 | 1 | 1 | 0.0275 |

Summary generation: 0 missing/empty, 4 capped, 0 context errors. Caps can leave an incomplete summary; they are not automatic hallucination labels.

## Changes and failure context

| Pair / outcome | Users | Same order | Any fallback | Any repair | Summary cap | Empty truth | Nonempty, no reachable truth |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| summary_minus_raw / improved | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| summary_minus_raw / worsened | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| summary_minus_raw / unchanged | 196 | 71 | 0 | 2 | 0 | 176 | 9 |
| template_minus_raw / improved | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| template_minus_raw / worsened | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| template_minus_raw / unchanged | 189 | 60 | 0 | 1 | 0 | 176 | 9 |
| summary_minus_template / improved | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| summary_minus_template / worsened | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| summary_minus_template / unchanged | 189 | 37 | 0 | 3 | 0 | 176 | 9 |

## Sparse history (descriptive)

1–5 eligible pre-cutoff Buy rows: 128 users; 3 nonempty truth; 2 reachable. Pool oracle mean: 0.0156. Coverage and sample size limit interpretation.

| Method | nDCG@10 all sparse | nDCG@10 nonempty sparse |
|---|---:|---:|
| popularity | 0.0049 | 0.2103 |
| cbf | 0.0049 | 0.2103 |
| latest_buy | 0.0039 | 0.1667 |
| latest_buy_or_sell | 0.0030 | 0.1290 |
| raw | 0.0000 | 0.0000 |
| summary | 0.0000 | 0.0000 |
| template | 0.0034 | 0.1436 |
| provided | 0.0039 | 0.1667 |

## Timing and interpretation

- data_preparation_seconds: 0.0566
- checkpoint_wait_and_verification_seconds: 6.4536
- model_load_seconds: 2.8544
- template_generation_seconds: 0.1514
- matched_inference_stage_wall_seconds: 247.3102
- provided_inference_stage_wall_seconds: 322.7602
- pre_hub_offline_preparation_seconds: unmeasured
- timing_note: Stage wall time includes tokenization, generation, logging; excludes between-stage prompt construction. Pre-Hub download/packaging time is unmeasured. No end-to-end inference wall time was logged.
- evaluation_before_output_seconds: 6.5201

- Development purchase-label relevance only; repeated Buys allowed; all 200 retained.
- Fresh starter CBF near-tie order can vary with Python hash seed; the verified frozen candidate order and baseline predictions are authoritative.
- Supplied ranker is separate: profile, names, dates, full counts, recent events and 512 output tokens.
- Raw vs summary changes compression procedure as well as wording. Template uses visible rows only.
- Template greedily packs whole entries round-robin; a rejected entry can be followed by a shorter accepted one.
- Same planned batches of eight; context rejection can change effective generation batch membership.
- Capped output is a truncation flag, not automatically an invalid ranking or hallucination.
- Summary audits are pending human review; omission alone is not hallucination.
- No final-project split, investment suitability, or benchmark placement claim.

## Audit and student check

See [summary-audit.md](summary-audit.md) and [summary-audit.jsonl](summary-audit.jsonl) for actual inputs, summaries and pending review fields.
Audit positions: 1, 2, 3, 25, 50, 69, 75, 100, 101, 125, 145, 148, 150, 175, 200.
See [failure-examples.jsonl](failure-examples.jsonl) for up to three actual examples per variant and failure flag, including raw outputs and candidate-number mapping. Overlapping flags are retained.
The real example U148 is in [student-hand-check.md](student-hand-check.md) and [student-hand-check.json](student-hand-check.json). Its reference was computed by this script; the student worksheet remains unperformed and unattributed.

Anonymized labels are frozen cohort positions; no customer ID mapping is exported. Treat these research artifacts as pseudonymized, not a formal anonymization guarantee.
