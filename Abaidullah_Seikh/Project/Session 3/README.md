# Session 3 — RQ1, Ranker

Abaidullah Seikh. FAR-Trans history-representation experiments and deterministic repeat-first rules.

## Purpose and status

RQ1 compares structured history (A) with fact-preserving generated summaries (C) at the Ranker seam.
The same CBF candidate pool is used for matched reranking comparisons. C+R adds a deterministic rule.
**All measurements here are development results**, not official-test results.
The 200-user block selected C+R V2; the separate sparse window checked robustness.
Positions 201–300 were frozen before unblinding and are reported separately, never pooled.
The later all-candidate variant used all three already-observed development sets.
Positions 301–400 selected a benchmark method (B1); those results are not used for HW3 conclusions.

## Environment and course reference

- Python 3.14.4; torch 2.11.0+cpu; transformers 4.57.6.
- accelerate 1.15.0; huggingface_hub 0.36.2; CPU float32 inference.
- Model: Qwen/Qwen3-1.7B.
- Model revision: `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`.
- A/C generation: greedy, seed 0, thinking disabled; summary budget 120, ranking budget 60.
- Provided LLM comparison: greedy, thinking disabled, context limit 8192, ranking budget 512.
- Course starter: <https://github.com/dryjins/RecSys-LLMs>. Course files are not copied here.
- Required starter SHA-256:
  `c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24`.
- Local data directory: `../Session 1/FAR-Trans`; dataset files and model cache are not committed.
- Local interpreter was reused from the adjacent Session 2 `.venv`; no reinstall was performed.
- Starter verification: 58 unit tests passed.

The scripts preserve the original local paths and expect the course starter and local artifacts.
They are historical execution helpers, not a self-contained data/model distribution.

## Pre-registration trail

| File | SHA-256 |
| --- | --- |
| [HW3_BLOCK_201_300.md](HW3_BLOCK_201_300.md) | `a99403c56472dde79a5767c7c85a34826ecbc34e8f9c0d8c1187df91a7d18bb6` |
| [HW3_PLAN_C_ALL.md](HW3_PLAN_C_ALL.md) | `f3aace44fa9c19d9ef39b15781a5b0063d1939bcfac9ebaf5b667c0290229caf` |
| [HW3_PLAN_C_IMPROVEMENT.md](HW3_PLAN_C_IMPROVEMENT.md) | `fa99792f07dfdb8b48a63235ba8652a1aeca8a6080ac0cea0343445e69ad1402` |
| [HW3_PLAN_C_IMPROVEMENT_CLARIFICATION.md](HW3_PLAN_C_IMPROVEMENT_CLARIFICATION.md) | `68311cda32e608c805bc0cc1ca3f9b0b50b3c232bb2e1da5d58bf2c7a7fe96ab` |
| [HW3_PROTOCOL.md](HW3_PROTOCOL.md) | `427e05eea001910c4c1f02169915ee5efbc27b5b5463fa0fdceb824ecd3c2146` |
| [HW3_PROTOCOL_AMENDMENT1.md](HW3_PROTOCOL_AMENDMENT1.md) | `33f0f5c126f0e38efcc661b2b4518fc3664419852cc9c1938a29d0853b515a06` |
| [BENCH_PLAN_301_400.md](BENCH_PLAN_301_400.md) | `8364b5f311bdf8a842734eabd6ca5805c10be9623ce01b4a94c64bf26b5d43d4` |

The original protocol is unchanged. Amendment 1 makes the fact-preserving summary team arm C.
The original summary is the old-C ablation. The repeat-first clarification was answered before its scores.
C+R V2 was selected on the first 200 users. All-candidate post-processing is a later single-variant experiment.
The benchmark plan selected between B1 (Buy-count V2) and B2 (Buy-or-Sell recency); B1 was selected.

## Metrics and interpretation

Primary nDCG@10 is the mean over every cohort user, with empty future truth contributing zero.
Non-empty-truth means are secondary. Repeat purchases are allowed.
Cutoff: 2021-06-01. Main and numbered blocks use 30 days; the sparse window uses 90 days.
The unchanged model template still asks about 30 days in the sparse-window experiment.
Reported fallback-inclusive scores replace an entire invalid ranking with CBF top 10.
The provided comparison uses its own parser; starter rescoring reproduced its aggregate score.
Bootstrap intervals use 10,000 paired user resamples and seed 0; sign tests are exact and two-sided.
Summary time was not separately recorded; C−A timing differences are estimates, not stage measurements.

## Aggregate development results

### Main 200 — selection development set

Users: **200**; users with non-empty truth: **24**.

| Method | nDCG@10 all | nDCG@10 non-empty |
| --- | ---: | ---: |
| Latest buy or sell | 0.0484 | 0.4033 |
| Latest buy | 0.0474 | 0.3946 |
| Popularity | 0.0342 | 0.2852 |
| CBF | 0.0305 | 0.2539 |
| A | 0.0302 | 0.2514 |
| C | 0.0282 | 0.2352 |
| C+R | 0.0386 | 0.3219 |
| A+R-all | 0.0526 | 0.4387 |
| C+R-all | 0.0530 | 0.4416 |
| P — provided LLM | 0.0306 | 0.2551 |

### Sparse 120 — 90-day robustness window

Users: **120**; users with non-empty truth: **8**.

| Method | nDCG@10 all | nDCG@10 non-empty |
| --- | ---: | ---: |
| Latest buy or sell | 0.0221 | 0.3311 |
| Latest buy | 0.0204 | 0.3058 |
| Popularity | 0.0085 | 0.1272 |
| CBF | 0.0141 | 0.2116 |
| A | 0.0161 | 0.2413 |
| C | 0.0178 | 0.2664 |
| C+R | 0.0208 | 0.3125 |
| A+R-all | 0.0203 | 0.3038 |
| C+R-all | 0.0208 | 0.3125 |
| old C | 0.0036 | 0.0538 |

### Positions 201–300 — held-out development block

Users: **100**; users with non-empty truth: **14**.

| Method | nDCG@10 all | nDCG@10 non-empty |
| --- | ---: | ---: |
| Latest buy or sell | 0.0592 | 0.4227 |
| Latest buy | 0.0546 | 0.3899 |
| Popularity | 0.0143 | 0.1025 |
| CBF | 0.0445 | 0.3179 |
| A | 0.0421 | 0.3009 |
| C | 0.0445 | 0.3179 |
| C+R | 0.0467 | 0.3339 |
| A+R-all | 0.0507 | 0.3618 |
| C+R-all | 0.0507 | 0.3618 |

### Positions 301–400 — benchmark-method selection only

Users: **100**; users with non-empty truth: **13**.

| Method | nDCG@10 all | nDCG@10 non-empty |
| --- | ---: | ---: |
| Latest buy or sell | 0.0463 | 0.3558 |
| Latest buy | 0.0484 | 0.3727 |
| Popularity | 0.0449 | 0.3455 |
| CBF | 0.0339 | 0.2606 |
| A | 0.0339 | 0.2606 |
| B1 | 0.0478 | 0.3679 |
| B2 | 0.0431 | 0.3315 |

The A/C model inputs used 50 candidates. All-candidate rule variants can promote any eligible previously bought asset.
C+R and C+R-all use count-first V2. A+R in the earlier analyses uses recency V1; A+R-all uses V2.
All-candidate evaluation protocols contain 767 eligible assets; baseline scores remained unchanged.
The main A arm has one fallback; sparse A has one; block A has one; benchmark A has one.
The provided ranker has 46/200 fallbacks. C has no invalid outputs in these windows.

## Exact execution commands, in order

These commands reproduce inference and scoring only when the required local inputs exist.
Run in the local Session 3 working directory. Runners refuse existing output directories.
Do not rerun them over archived measured outputs. Wait for each inference service to finish before scoring it.
The numbered plans, amendments and local cohort files were created at the documented checkpoints.

```bash
PY="/home/dastan/Recommender Systems/Abaidullah_Seikh/Project/Session 2/.venv/bin/python"
DATA="../Session 1/FAR-Trans"

# 1. Course setup and frozen main cohort.
"$PY" -m unittest discover -s . -p "test_*.py"
"$PY" starter.py run --data-dir "$DATA" --max-users 200 --output-dir outputs/baseline_200
"$PY" prepare_sparse_window.py

# 2. Main A positions 101–200 use a separate, unchanged context slice.
"$PY" - <<'PY'
from pathlib import Path
source = Path("outputs/baseline_200")
target = Path("outputs/A_101_200_input")
target.mkdir()
(target / "contexts.jsonl").write_bytes(
    b"".join((source / "contexts.jsonl").read_bytes().splitlines(keepends=True)[100:200]))
(target / "protocol.json").write_bytes((source / "protocol.json").read_bytes())
PY
systemd-run --user --unit=hw3-main --working-directory="$PWD" /bin/bash -c \
  'bash run_hw3_main.sh > logs/hw3_main.log 2>&1'

# 3. After main completion and Amendment 1, merge preserved HW2 A with the new half, then score.
"$PY" scripts/hw3_merge_score.py merge
"$PY" scripts/hw3_merge_score.py score

# 4. Sparse baseline and main paired analysis; then sequential sparse inference.
"$PY" starter.py run --data-dir "$DATA" --cutoff 2021-06-01 --horizon-days 90 \
  --users-file cohorts/sparse_window_users.txt --cohort warm --output-dir outputs/sparse_baseline_120
"$PY" scripts/hw3_paired_analysis.py
systemd-run --user --unit=hw3-sparse --working-directory="$PWD" /bin/bash -c \
  'bash run_hw3_sparse.sh > logs/hw3_sparse.log 2>&1'
"$PY" scripts/hw3_sparse_score.py
"$PY" scripts/hw3_sparse_analysis.py

# 5. After the C+R plan and clarification: deterministic V1/V2 comparison, no model calls.
"$PY" scripts/hw3_repeat_first.py

# 6. Provided ranker: first prepare and verify its local users/candidates.
RANKER="../Session 2/far-trans-llm/ranker.py"
"$PY" "$RANKER" --starter-dir "$PWD" --data-dir "$DATA" \
  --cutoff 2021-06-01 --horizon-days 30 --max-users 200 --candidate-count 50 \
  --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
  --device cpu --on-invalid fallback --output-dir outputs/provided_llm_200_prepare --prepare-only
# Local input_verification.json must record identical users/order and candidate identities/order/sets.
# run_hw3_provided.sh checks its exact recorded hash. Prepared prompts and verification artifacts stay local.
systemd-run --user --unit=hw3-provided --working-directory="$PWD" /bin/bash -c \
  'bash run_hw3_provided.sh > logs/hw3_provided.log 2>&1'
"$PY" scripts/hw3_provided_analysis.py

# 7. After freezing positions 201–300 and creating the local users file, generate blind artifacts.
"$PY" starter.py run --users-file cohorts/block_201_300_users.txt --cutoff 2021-06-01 \
  --horizon-days 30 --cohort warm --data-dir "$DATA" --output-dir outputs/block_201_300 \
  > logs/block_201_300_starter.log 2>&1
systemd-run --user --unit=hw3-block --working-directory="$PWD" /bin/bash -c \
  'bash run_hw3_block.sh > logs/hw3_block.log 2>&1'
# Planned unblinding after completion:
"$PY" scripts/hw3_block_score.py
"$PY" scripts/hw3_block_analysis.py

# 8. After the single-variant all-candidate plan:
"$PY" scripts/hw3_c_all.py

# 9. Benchmark plan, local cohort positions 301–400, blind A, then planned selection.
"$PY" starter.py run --users-file cohorts/block_301_400_users.txt --cutoff 2021-06-01 \
  --horizon-days 30 --cohort warm --data-dir "$DATA" --candidate-count 50 \
  --output-dir outputs/block_301_400 > logs/block_301_400_starter.log 2>&1
systemd-run --user --unit=bench-block --working-directory="$PWD" /bin/bash -c \
  'bash run_bench_block.sh > logs/bench_block.log 2>&1'
"$PY" scripts/bench_select.py
```

For the two numbered cohort files, the original local preparation used the starter functions:
`select_users(profiles, history, "warm", 300, None)[200:300]` and
`select_users(profiles, history, "warm", 400, None)[300:400]` after `load_data`.
The first 200/300 users were checked against the already frozen prefixes; overlap checks passed.
Neither cohort was filtered using future truth. Cohort files remain local.

The provided ranker and the course starter must be obtained from the course, not from this folder.
Its prepare-only format has no protocol hash. Identical users and candidate lists justified the recorded run.
The canonical provided responses also need schema conversion; the analysis helper preserves invalid status
so starter fallback reproduces the provided effective rankings. No regeneration or extra repair is added.

## Aggregate artifacts

The `results/` files are copies of the named local aggregate analyses and run metadata.
Names under `results/run_meta/` identify both the run and whether the source was metadata or provenance.
HW2 A/C metadata are included because the first half and old-C ablation reuse those runs.
One failed main-A launch is retained as metadata evidence; the kernel identified an OOM kill.
Copied `main_200/provided_analysis.json` was excluded after three ID-regex matches.
Copied provided-run provenance was excluded because its full command exceeded the 400-character string gate.
Their originals remain local; only the safe provided aggregate means appear in the table above.

## Not committed

- `outputs/`, `cohorts/`, `logs/`, and `__pycache__/`.
- Every JSONL file, per-user predictions/scores/rows, customer-instantiated prompts and summaries.
- Customer-ID cohort files, `protocol.json`, `contexts.jsonl`, generation logs and generation caches.
- FAR-Trans data, model cache, virtual environments, and downloaded course packages.
- Course `starter.py`, `extensions.py`, `test_starter.py`, and `homework3.md`.

This follows the course rule: keep raw customer identifiers and generated user-level material local.
The committed reranker source contains static templates and schema field names, not saved customer prompts.
