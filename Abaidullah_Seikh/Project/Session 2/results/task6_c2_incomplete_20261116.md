# Exploratory: prompt designed after inspecting Arm C errors; not pre-registered

## Status — incomplete: latest retry running after earlier OOM terminations

No completed C2 result exists yet. Earlier attempts were terminated by the Linux out-of-memory killer; the latest user-authorized retry is running, as detailed below. It has not been scored. No C2 nDCG, paired effects, validity rate, completed runtime or factuality counts are reported. Main results, the shared scripts, and earlier experiment outputs remain unchanged.

This is restricted to the same supplementary 30 sparse users selected for having future purchases. It is not the default HW2 protocol. Any eventual score describes the conditional nonempty-truth population only.

## Verified source change

| File | SHA-256 |
|---|---|
| Unchanged `llm_rerank.py` | `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` |
| New `llm_rerank_c2.py` | `0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada` |

Only the non-D task text in `summary_prompt()` changes. All source outside that function is byte-for-byte identical. The new task string was checked against the exact requested text for all 30 contexts; `SUMMARY_SYSTEM` and the original D prompt behaviour were also checked unchanged. No model was called by those checks.

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

## Launch record

Model: Qwen/Qwen3-1.7B, revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`. Unchanged settings: float32 CPU, HF backend, seed 0, threads flag 0, greedy generation, thinking off, 120 summary tokens, 60 rank tokens. Internally `--arm C` is used; C2 is the experiment/output label.

```bash
setsid nohup systemd-inhibit --what=sleep:idle --why="HW2 exploratory sparse C2" .venv/bin/python llm_rerank_c2.py --run-dir outputs/sparse_baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm C --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/sparse_arm_C2 < /dev/null > outputs/sparse_c2.log 2>&1 &
```

- Initial launch: **2026-11-16 16:50:04 +03:00**, supervisor PID 75145. The waiting tool was interrupted. On continuation, the process was absent, the log ended during checkpoint loading, and no raw output or metadata existed. The cause of this first termination was not independently established. Its log was preserved as `outputs/sparse_c2_interrupted_20261116T165004.log`.
- Identical retry: process start **17:38:42 +03:00** (launch returned 17:38:43), supervisor **75926**, model process **75929**.
- Check at **17:40:49**, elapsed **2 min 6 s**: both processes were running, both checkpoint shards were loaded, and the raw log existed with 0 flushed lines. The rough estimate based on earlier sparse C's 2723.8-second loop time was completion around **18:24 +03:00**, plus startup; that estimate was not achieved.
- Subsequent check at **17:58:26**: both processes were absent; `outputs/sparse_arm_C2/raw_log.jsonl` had **0 lines**. No `run_meta.json` was produced.

The kernel journal gives the concrete retry failure at **17:57:44 +03:00**:

```text
oom-kill: ... global_oom ... task=python,pid=75929,uid=1000
Out of memory: Killed process 75929 (python) total-vm:8991108kB, anon-rss:7712980kB, file-rss:8kB, shmem-rss:4kB ...
```

The process had approximately **7.36 GiB** resident anonymous memory at termination. The application log ended with a multiprocessing resource-tracker warning about a leaked semaphore; the kernel message, not that warning alone, establishes the out-of-memory cause for the retry. No settings were changed, no other applications were stopped, and no further retry was launched after this diagnosis.

## Pending scoring and analysis

### Further user-authorized retry — also terminated by OOM

On the user's next continuation, the previous failed retry's log was preserved as `outputs/sparse_c2_oom_20261116T175744.log` and its partial output directory as `outputs/sparse_arm_C2_oom_20261116T175744/`. Before relaunch, source hashes and the exact prompt-only change were verified again, and no model process was active. Memory at 19:03:06 showed approximately **6.3 GiB available RAM** and **1.4 GiB free swap**.

The identical detached command was relaunched at **2026-11-16 19:03:36 +03:00**, supervisor PID **81026**, model PID **81029**. The waiting tool call was interrupted. On continuation at **19:23:26**, no process remained; checkpoint loading had stopped after the first shard. No new raw log or completed metadata existed.

The kernel journal confirms another out-of-memory termination at **19:04:09 +03:00**:

```text
oom-kill: ... global_oom ... task=python,pid=81029,uid=1000
Out of memory: Killed process 81029 (python) total-vm:9629728kB, anon-rss:7199252kB, file-rss:8kB, shmem-rss:4kB ...
```

The model process had about **6.87 GiB** resident anonymous memory at termination. This is a second independently confirmed OOM, not a model response or completed run. No further retry was started after confirming it. No applications were stopped and no dtype, threads, token limits, prompt, model revision, or other settings were changed to work around it. Scoring and aggregate analysis remain blocked until a successful run can complete with sufficient memory.

The supplementary protocol remains:

### Latest user-authorized retry — running at last check

The 19:04:09 OOM log was preserved as `outputs/sparse_c2_oom_20261116T190409.log`. No model process was active before relaunch and both source hashes were unchanged. At 19:38:06, available RAM was about 6.8 GiB and free swap about 1.6 GiB.

The same command was launched at **2026-11-16 19:38:22 +03:00** (returned 19:38:23), supervisor **82133**, model **82136**. The **19:40:31** check confirmed the process running after 2 min 7 s with both checkpoint shards loaded. The original sparse C timing gave a rough finish estimate of about **20:24**, plus startup, but that estimate was exceeded.

At **20:33:44**, elapsed **55 min 20 s**, the process was still running at about 193% CPU and the raw log still had **0 flushed lines**. At 20:31, available RAM was about 1.1 GiB and 3.7/4 GiB of swap was used. No reliable remaining time or completed-user count could be recovered from these buffered files. The existing process is being left running, without a restart or model-setting change. Scoring will occur only if 30 records and completed metadata become available.

```text
0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b
```

Scoring is pending until a successful run has 30 raw-log records and completed metadata. No `outputs/sparse_arm_C2_eval` run was made in this task.

Prepared analysis-only helper: `results/analyze_task6_c2.py` (not executed). It specifies exact/case-sensitive ISIN naming checks, pooled and per-user coverage, a denominator restricted to users with repeated assets for the “all repeated assets named” check, case-insensitive whole-word share/shares/unit/units counts, and predeclared regexes for no-repeat wording. These are deterministic string checks, not semantic judgments. Counts and paired comparisons remain pending; no findings are inferred from absent or buffered output.

This report is aggregate-only and contains no raw customer IDs or instantiated customer prompts/summaries. Source-template text above is the requested code diff. No conclusions about C2 effectiveness or summary fidelity are available.
