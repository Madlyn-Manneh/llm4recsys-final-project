# Task 5 — supplementary labelled sparse-user experiment

**Status: supplementary baselines completed; model arms launched, not scored.** The main 100-user HW2 results, their inputs, and their outputs are unchanged.

## Cohort rule and provenance

The cohort uses the instructor starter's unchanged functions, imported by local helper `results/prepare_task5_sparse.py`:

1. `starter.load_data(data_dir, '2021-06-01', 30)` supplies eligible assets, eligible historical Buy counts and future truth. Its own policy removes exact duplicate transaction rows and negative-ID reconstructed positions; eligibility requires pre-cutoff metadata and a positive pre-cutoff close price.
2. `starter.select_users(profiles, history, 'warm', 0, None)` selects all as-of-known warm users in the exact starter order: SHA-256 of `42:` plus user ID, then user ID. This preserves the starter's known-profile requirement for `--users-file`.
3. Filter that ordered list to users with **1–5 total eligible historical Buy transactions** (sum of counts, not distinct assets), strictly before **2021-06-01**, and **nonempty eligible future Buy truth** in **[2021-06-01, 2021-07-01)**.
4. Take the first **30** qualifying users. No new sorting or truth-loading implementation was substituted for the starter functions.

**224 users qualify in total; 30 were selected.** All selected users have nonempty eligible history and nonempty future truth. Their IDs are saved only in **`cohorts/sparse_labelled.txt`**, which is **local only and must never be committed**. The original CSV hashes were verified against the main baseline protocol before cohort construction. Cohort construction and coverage inspection make no model calls.

**Selection caveat:** this is explicitly selected on having future purchases. It is an evaluation population choice, not a feature or model input. Only the **conditional nonempty-truth mean** is meaningful for this supplementary experiment. The displayed all-user mean is numerically identical because all 30 users have nonempty truth; it is not the main protocol's all-user population mean and should not be compared as such. This is not an independently selected future-unobserved deployment cohort.

## Supplementary baseline run

Run from `/home/dastan/Recommender Systems/Project/Session 2`:

```bash
python3 starter.py run --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --output-dir outputs/sparse_baseline --users-file cohorts/sparse_labelled.txt
```

The `--users-file` supplied these exact 30 IDs; all other starter defaults were retained (CBF candidate count 50, repeat purchases allowed, same cutoff/horizon). The output contexts were checked to match the cohort file in order. Custom failures: **0**, with no custom method used in this baseline run.

| Baseline | Users | Nonempty users | nDCG@10 all selected users | nDCG@10 nonempty truth |
|---|---:|---:|---:|---:|
| Popularity | 30 | 30 | 0.2955 | 0.2955 |
| CBF | 30 | 30 | 0.3843 | 0.3843 |
| Latest buy | 30 | 30 | 0.5338 | 0.5338 |
| Latest buy or sell | 30 | 30 | 0.5238 | 0.5238 |

Source: `outputs/sparse_baseline/metrics.json`; values rounded to four decimals only for display. Empty-truth users: **0**. No supplementary model-arm scores have been computed.

New full protocol hash:

```text
0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b
```

This is distinct from the main 100-user hash. The supplementary arm inputs come only from this new baseline output directory.

## Label coverage — evaluation only

The cohort contains **41 distinct future user–asset labels**. Of these, **23** fall inside their user's fixed CBF top-50 pool, distributed across **21 of 30 users**; **9 users** have no future label in their pool. Coverage was computed by intersecting the starter-returned truth ISIN sets with each saved context's candidate IDs and eligible IDs. These are label counts, not raw future transaction counts.

Truth availability was used for cohort selection and these evaluation diagnostics. No future ISINs or counts were added to contexts or prompts. `llm_rerank.py` receives only the starter's saved historical contexts/protocol and its usual as-of questionnaire lookup. Its inputs and prompts were not modified.

## Protected source hashes

Checked before cohort preparation and again after launching:

| File | SHA-256 |
|---|---|
| `llm_rerank.py` | `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` |
| `starter.py` | `c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24` |

Neither script was edited. The original main baseline/evaluation/model-run outputs were not overwritten.

## Detached supplementary run

- **Process start:** **2026-11-16 11:48:06 +03:00** (`ps`); the launch command returned at 11:48:07.
- Supervisor PID / session ID: **68822** (`systemd-inhibit`).
- Serial loop PID: **68825** (`bash`).
- Current model PID at launch check: **68826**, **Arm C**.
- Order: **C → A → B**, sequentially, one active model process.
- Combined log: **`outputs/sparse_runs.log`**.
- Model outputs: **`outputs/sparse_arm_C/`**, then **`outputs/sparse_arm_A/`**, then **`outputs/sparse_arm_B/`**.

Exact loop, launched from Session 2, with a separate session, `nohup`, disconnected stdin and sleep/idle inhibition:

```bash
setsid nohup systemd-inhibit --what=sleep:idle --why="HW2 supplementary sparse runs" bash -c '
for ARM in C A B; do
  .venv/bin/python llm_rerank.py --run-dir outputs/sparse_baseline \
    --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" \
    --arm $ARM --model Qwen/Qwen3-1.7B \
    --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
    --out-dir outputs/sparse_arm_$ARM || echo "ARM $ARM FAILED"
  echo "ARM $ARM DONE $(date)"
done' < /dev/null > outputs/sparse_runs.log 2>&1 &
```

No `--max-users` flag: default 0 consumes all **30 supplementary contexts**. All other smoke/full-run defaults are unchanged: HF backend; float32 CPU; threads flag 0 (torch default); seed 0; summary max_new_tokens 120; rank max_new_tokens 60; explicit thinking off and greedy `do_sample=False`. No other model job was running before launch.

As in the requested main loop, failure prints `FAILED` and proceeds to the next arm; the unconditional `DONE` marker alone is not proof of success. Completion and response counts will need checking later before scoring.

## Check after two minutes

At **2026-11-16 11:50:13 +03:00**, elapsed **2 min 6 s**:

- `ps` confirmed supervisor **68822** was running in its independent session.
- Process listing confirmed loop **68825** and Arm C model process **68826**.
- `systemd-inhibit --list --no-pager` confirmed an active **sleep:idle block**, reason **HW2 supplementary sparse runs**, PID **68822**. No inhibitor fallback was needed.
- `outputs/sparse_arm_C/raw_log.jsonl` existed with **0 flushed lines**. Writes are buffered, so this is not an exact live completed-user count.
- The tail of `outputs/sparse_runs.log` showed checkpoint loading completed (two shards, about 10 seconds), a `torch_dtype` deprecation notice, and the same temperature/top_p/top_k notice seen in the completed main runs. There was no failure or completion marker at this check.

No arms were scored, no completion was awaited, and the job was left running.

## Estimated finish time

Use the **measured main 100-user runs**, not the earlier three-user extrapolations: C **96.046 s/user**, A **62.968 s/user**, B **63.469 s/user**, each from recorded whole-arm loop time / 100. Multiply by 30 and accumulate from the supplementary process start.

| Arm | Prior mean seconds/user | Estimated 30-user loop time | Cumulative projected finish (+03:00, Nov. 16) |
|---|---:|---:|---|
| C | 96.046 | 2881.38 s (48.0 min) | about 12:36 |
| A | 62.968 | 1889.04 s (31.5 min) | about 13:08 |
| B | 63.469 | 1904.07 s (31.7 min) | about 13:39 |

Combined projected loop time: **6674.49 s**, about **1 hour 51 minutes**. Approximate completion is **13:39 +03:00**, plus excluded model startup and other overhead. This is a rough estimate, not a measured finish time. The supplementary histories are restricted to 1–5 Buys and may have different prompt lengths; CPU load, thermal state, memory pressure and generated lengths can change timing. No prediction interval is available.

## Local-only materials

`cohorts/sparse_labelled.txt`, `outputs/sparse_baseline/` (including protocol users and contexts), `outputs/sparse_arm_*/`, and `outputs/sparse_runs.log` contain user-level information or model inputs/outputs and must stay local. The cohort file is outside the existing `outputs/` ignore rule; an explicit commit allowlist is required. Nothing was staged or committed in this task.
