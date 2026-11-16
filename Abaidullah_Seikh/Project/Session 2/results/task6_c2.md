# Exploratory: prompt designed after inspecting Arm C errors; not pre-registered

## Scope and provenance

Sparse supplementary cohort only: the same 30 users selected for having 1–5 historical eligible Buys and nonempty future purchases. This is not the default 100-user HW2 protocol. Only the conditional nonempty-truth mean is meaningful; all-selected-user and nonempty means coincide. Main results and prior model outputs were not changed. Descriptive measurements only; no conclusions, semantic factuality judgments or significance claims.

- Original script SHA-256: `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da`.
- C2 copy SHA-256: `0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada`.
- C2 changes only the non-D task text in summary_prompt(). SUMMARY_SYSTEM, D behaviour, ranker template, parser, defaults and token limits remain identical. The internal --arm is C; C2 is the experiment/output label.
- Model: Qwen/Qwen3-1.7B, resolved revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, CPU float32, thinking off, greedy decoding, seed 0, threads flag 0, 120 summary and 60 ranking max_new_tokens.
- Protocol hash: `0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b`. C2 evaluation protocol exactly equals the sparse baseline, and all four baseline aggregate blocks match at full saved precision.

## Prompt-only diff

```diff
--- llm_rerank.py
+++ llm_rerank_c2.py
@@ -149,6 +149,12 @@
     task = ('Write a summary of 3 to 4 sentences describing the kinds of assets and '
             'markets this investor buys, how concentrated the purchases are, and '
             'whether they repeat purchases.')
+    if arm != 'D':
+        task = ('Write a summary of 3 to 4 sentences for a recommender system. "bought Nx" means N '
+                'separate Buy transactions, not shares or units. Name every asset by its ISIN with its '
+                'buy count. State which assets were bought more than once; if none were, say so. '
+                'Describe the main asset categories, sectors and markets using only the attributes '
+                'shown. Do not add any information that is not in the history.')
     if arm == 'D':
         parts.append(profile_block(ctx, questionnaire_ok))
         task = task[:-1] + ', and note how the profile relates to the purchases.'
```

## Launch and completion

**Completed successfully**, confirmed at **2026-11-16 21:20:07 +03:00**: 30 raw-log records, 30 unique-user responses, completed metadata, and no active model process. C2 has **0 invalid outputs** and **0 scoring custom failures**. The unchanged starter and team-source hashes were verified again after scoring. Earlier failed attempts are distinguished from this completed run below; their time is not included in the successful run's recorded runtime.

Initial detached launch: 2026-11-16 16:50:04 +03:00, supervisor 75145. The waiting tool call was interrupted; on continuation the process was absent and its log ended during checkpoint loading, with no raw output or metadata. Cause unverified. That log was preserved as outputs/sparse_c2_interrupted_20261116T165004.log. No results or timing were inferred from it.

Identical retry: process start 2026-11-16 17:38:42 +03:00 (launch returned 17:38:43), supervisor 75926, model process 75929. The two-minute check passed, but the kernel killed model PID 75929 for global out-of-memory at 17:57:44. Its log and partial directory were preserved as outputs/sparse_c2_oom_20261116T175744.log and outputs/sparse_arm_C2_oom_20261116T175744/. A further user-authorized retry at 19:03:36, supervisor 81026/model 81029, was also killed by the kernel for OOM at 19:04:09 during checkpoint loading; its log was preserved as outputs/sparse_c2_oom_20261116T190409.log. Neither produced completed results.

After another explicit continuation, the identical command was launched again at 2026-11-16 19:38:22 +03:00 (returned 19:38:23), supervisor 82133/model 82136. At 19:40:31, elapsed 2 min 7 s, it was running with both shards loaded and 0 flushed raw-log lines. The earlier sparse C timing suggested roughly 20:24 plus startup, but the process exceeded that estimate. At 20:31 it was still active at about 193% CPU, with 0 flushed rows, about 1.1 GiB available RAM and 3.7/4 GiB swap used. No settings or external applications were changed by the agent. Completion and elapsed time below are taken from the successful run metadata, not inferred from these interim checks.

Detached command:

```bash
setsid nohup systemd-inhibit --what=sleep:idle --why="HW2 exploratory sparse C2" .venv/bin/python llm_rerank_c2.py --run-dir outputs/sparse_baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm C --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/sparse_arm_C2 < /dev/null > outputs/sparse_c2.log 2>&1 &
```

Scoring uses the unchanged starter, only after confirming 30 raw rows and completed run_meta.json:

```bash
python3 starter.py run --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --output-dir outputs/sparse_arm_C2_eval --users-file cohorts/sparse_labelled.txt --stage ranker --responses outputs/sparse_arm_C2/responses.jsonl --on-invalid fallback
```

## a. Sparse-cohort scores and timings

| Method | Users | Nonempty users | nDCG@10 all selected users | nDCG@10 nonempty | Invalid outputs | Scoring failures | Wall time |
|---|---:|---:|---:|---:|---:|---:|---|
| CBF | 30 | 30 | 0.3843 | 0.3843 | 0 (not model-generated) | 0 | Not measured for supplementary baseline |
| A | 30 | 30 | 0.4051 | 0.4051 | 0 | 0 | 1821.5 s |
| B | 30 | 30 | 0.3439 | 0.3439 | 0 | 0 | 1764.1 s |
| C | 30 | 30 | 0.3846 | 0.3846 | 0 | 0 | 2723.8 s |
| C2 | 30 | 30 | 0.3925 | 0.3925 | 0 | 0 | 5026.4 s |

Wall times are recorded whole-arm loop times, excluding model loading and initial context/questionnaire reading; C and C2 include summary generation. Scoring time is separate and unmeasured. A/B/C values come from earlier unchanged sparse runs. C2 rows use outputs/sparse_arm_C2_eval/metrics.json and outputs/sparse_arm_C2/run_meta.json.

| Comparison | Users | Mean nDCG@10 difference | C2 better | Equal | C2 worse |
|---|---:|---:|---:|---:|---:|
| C2−C | 30 | 0.00795688 | 6 | 19 | 5 |
| C2−A | 30 | -0.01257946 | 5 | 21 | 4 |

Paired calculations use full saved per-user precision before rounding. All 30 users, including any invalid-output fallback cases, are retained. Each saved nDCG value was checked with starter.ndcg10 against unchanged starter truth and evaluation rankings.

## b. Deterministic summary string checks

The history is the actual capped text supplied to the summarizer, extracted from summary_prompt and checked equal across C/C2. ISIN presence is an exact case-sensitive substring check. Counts are parsed from the corresponding “bought Nx” lines; no external asset knowledge or semantic classifier is used.

| Check | C | C2 |
|---|---:|---:|
| Share of history ISIN occurrences named (pooled across users) | 17/58 (29.3103%) | 56/58 (96.5517%) |
| Mean per-user share of history ISINs named | 36.6667% | 95.8333% |
| Users with ≥1 repeated asset: all repeated ISINs named | 5/10 (50.0000%) | 9/10 (90.0000%) |
| Summaries containing share/shares/unit/units (whole words) | 3/30 | 6/30 |
| Summaries matching no-repeat wording when history has a repeated asset | 1/30 (among 10 repeated-history users) | 4/30 (among 10 repeated-history users) |

“Pooled” denominator counts each distinct history asset once per user (the same ISIN in two users counts twice). The mean per-user fraction is also shown to avoid confusing pooled and macro coverage. The repeated-asset denominator contains only users with at least one asset having buy_count≥2; users without repeats are excluded rather than counted as vacuous successes. These checks test naming only, not whether a named ISIN has the right count or attributes.

Quantity-word count uses case-insensitive regex `\b(?:share|shares|unit|units)\b`. A summary saying “not shares” still counts; the check records words, not errors.

No-repeat detection is case-insensitive and matches any of these predeclared patterns when at least one history asset has buy_count≥2:

```text
\bno\s+(?:repeat(?:ed)?|repetition(?:s)?)\s+(?:buy\s+)?(?:purchases?|transactions?|buying)\b
\b(?:does|do|did)\s+not\s+(?:appear\s+to\s+)?(?:have\s+|show\s+(?:any\s+)?|make\s+(?:any\s+)?|engage\s+in\s+)?repeat(?:ed)?(?:\s+(?:buy\s+)?(?:purchases?|transactions?|buying))?\b
\b(?:has|have|had)\s+not\s+(?:made\s+)?(?:any\s+)?repeat(?:ed)?\s+(?:purchases?|buys?|transactions?)\b
\b(?:no|without)\s+(?:evidence|signs?|indication)\s+of\s+(?:repeat(?:ed)?\s+(?:purchases?|buying)|repetition)\b
\b(?:no|not)\s+repetition\b
\b(?:no|none\s+of\s+the)\s+assets?\s+(?:was|were|has\s+been|have\s+been)\s+(?:bought|purchased)\s+more\s+than\s+once\b
\b(?:did|does|do)\s+not\s+(?:buy|purchase)\s+(?:any\s+asset|the\s+same\s+asset)\s+more\s+than\s+once\b
```

Regex matches are a surface wording diagnostic, not a semantic contradiction adjudication. Unmatched paraphrases can be missed, and matched quotations or negated context can be counted. No rule was adapted after inspecting C2 output. String checks do not establish overall factuality, faithful asset-count mappings, absence of hallucinations, or summary completeness. The shared 120-token output limit is unchanged; automatic counts include exactly the saved summaries, including any truncated text.

The report is aggregate-only: no raw customer IDs, per-user scores, histories, generated summaries, or instantiated prompts. The prompt diff above is source-template text, not customer data. All raw records stay in local outputs/.
