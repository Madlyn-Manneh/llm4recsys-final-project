# Task 3a — overnight full-run launch

## Active job

- **Start:** 2026-11-16 **01:56:29 +03:00**, from process start time.
- Working directory: `/home/dastan/Recommender Systems/Project/Session 2`.
- Detached supervisor PID / session ID: **47263** (`systemd-inhibit`).
- Serial loop PID: **47268** (`bash`).
- Current model process PID: **47269** (Arm C).
- Order: **C → A → B**, one model process at a time.
- Outputs: `outputs/arm_C`, `outputs/arm_A`, `outputs/arm_B`.
- Combined stdout/stderr: `outputs/full_runs.log`.
- **No `--max-users` flag**: shared default 0 selects all 100 saved baseline contexts.

SHA-256 checked before launching and again at the status check:

```text
85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da
```

This is the corrected Arm A script used by all three smoke tests. No code or model settings were changed for the full runs.

## Launch command

The same requested serial loop was launched under `setsid` as well as `nohup`, with stdin disconnected, to isolate the background process session from a tool-session interruption:

```bash
setsid nohup systemd-inhibit --what=sleep:idle --why="HW2 runs" bash -c '
for ARM in C A B; do
  .venv/bin/python llm_rerank.py --run-dir outputs/baseline \
    --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" \
    --arm $ARM --model Qwen/Qwen3-1.7B \
    --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/arm_$ARM \
    || echo "ARM $ARM FAILED"
  echo "ARM $ARM DONE $(date)"
done' < /dev/null > outputs/full_runs.log 2>&1 &
```

Unchanged smoke defaults: HF backend, float32, greedy decoding, thinking off, seed 0, threads flag 0, summary limit 120 new tokens, rank limit 60 new tokens. No other model workload was launched. Each arm starts only when the preceding command exits. As requested, failures are logged and the loop continues; `DONE` alone is not proof of success because it is printed even after a failure. Completed metadata, row counts, and absence of `FAILED` must be checked later.

## Initial interrupted launch and recovery

The initial requested `nohup systemd-inhibit ...` launch returned PID **46859**, at **2026-11-16T01:54:06+03:00**. The waiting tool call was interrupted. On continuation at 01:55:54, no supervisor, loop, or reranker process remained; no `arm_C` directory had been created. Its log ended during checkpoint loading with a resource-tracker semaphore warning; it did not show an inhibitor refusal. The cause of termination was not established.

That log was preserved as `outputs/full_runs_interrupted_20261116T015406.log`. The single replacement job above was then launched in a separate session. The launch tool exceeded its default 120-second tool timeout, but the detached job survived; the subsequent `ps` check confirmed this. No duplicate model processes remained.

## Status after about two minutes

At approximately **2026-11-16 01:58:53 +03:00**, elapsed **2 min 24 s**:

| PID | Parent PID | Session ID | State | Command |
|---:|---:|---:|---|---|
| 47263 | 2936 | 47263 | Ss | systemd-inhibit supervisor |
| 47268 | 47263 | 47263 | S | serial C/A/B bash loop |
| 47269 | 47268 | 47263 | Rl | .venv/bin/python llm_rerank.py, Arm C |

Arm C showed approximately **186% CPU** and **7,321,716 KiB RSS** in this snapshot. `systemd-inhibit --list --no-pager` confirmed an active **block** inhibitor for **sleep:idle**, reason **HW2 runs**, PID **47263**. The inhibitor was accepted; no uninhibited fallback was needed.

`tail -n 20 outputs/full_runs.log` showed (progress display normalized):

```text
`torch_dtype` is deprecated! Use `dtype` instead!
Loading checkpoint shards: 0%| 0/2
Loading checkpoint shards: 50%| 1/2 [00:07<00:07, 7.58s/it]
Loading checkpoint shards: 100%| 2/2 [00:08<00:00, 3.62s/it]
Loading checkpoint shards: 100%| 2/2 [00:08<00:00, 4.22s/it]
The following generation flags are not valid and may be ignored: ['temperature', 'top_p', 'top_k']. Set `TRANSFORMERS_VERBOSITY=info` for more details.
```

Line count at that check:

```text
0 outputs/arm_C/raw_log.jsonl
```

The log file exists but had no flushed complete lines yet. Shared script file writes are buffered, so this count alone is not a reliable live completed-user counter. The process was actively running; no completion, final runtime, validity count, or evaluation score is claimed here. Arms A and B had not started at this check.

The job has been left running. No wait for completion, scoring, or additional model execution was performed after this launch check.
