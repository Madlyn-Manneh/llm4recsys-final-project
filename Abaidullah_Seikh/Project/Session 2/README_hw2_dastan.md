# HW2 — FAR-Trans history representation experiment

Abaidullah Seikh, Team 8, LLM4Rec, HSE University.

Research question: do generated history summaries change future-purchase nDCG@10 compared with structured history for sparse users? The shared pipeline reranks the starter's fixed CBF top-50; only the Investor information block changes. A uses structured counts and attribute shares; B uses deterministic history text; C summarizes that same history text before ranking. These are measurements on the 100-user teaching protocol, not a final project test protocol.

## Source identity

| Source | SHA-256 |
|---|---|
| Team script, unedited current version | `d7a34c1f9f715d7437ca5b2cc7989dbff12348602495b8a427cf8e56fa7007ba` |
| My `llm_rerank.py`, used for A/B/C | `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` |

Only `structured_block()` differs. It uses the same first 20 history assets as B/C, per-ISIN Buy counts in descending Buy-count/ascending ISIN order, and all five starter attributes as Buy-weighted shares. Missing attributes are omitted. Shares preserve aggregate attribute values but not their association with each ISIN as in B. The student reports that Madlyn agreed to this definition. The shared backend, B/C logic, ranking template, parser, and generation settings are unchanged.

`starter.py` is the unchanged instructor starter. The optional `far-trans-llm/` package is reference only and is not used for these model runs.

## Environment and installation

Recorded interpreter: **Python 3.14.4**. Torch **2.11.0+cpu**, transformers **4.57.6**, accelerate **1.15.0**, huggingface_hub **0.36.2**. Hardware: Intel Core i7-6600U, 2 physical cores/4 logical CPUs, 11,848,441,856 bytes RAM. CPU float32 inference.

From the Session 2 directory containing `starter.py` and `llm_rerank.py`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install transformers==4.57.6 accelerate==1.15.0 huggingface_hub==0.36.2
```

`requirements.txt` records the same pins with the additional PyTorch CPU index. The split commands above explicitly select the CPU source for torch. Confirm that the installed build reports `2.11.0+cpu`.

## Data, model, and protocol

The data directory must contain the four original CSVs. The local run path was:

```bash
DATA="/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans"
```

Model: **Qwen/Qwen3-1.7B**, pinned revision **70d244cc86ccca08cf5af4e1e306ecf908b1ad5e**. The model must already be in the Hugging Face cache; it is not committed. This snapshot was completed separately by the student and checked offline via local-only tokenizer/config loading and safetensors headers. No download or model regeneration was performed during scoring/analysis.

Starter defaults: cutoff June 1, 2021 exclusive; 30-day future Buy window ending July 1 exclusive; 100 deterministic warm users; repeat purchases allowed; 50 CBF candidates. Both means retain their stated denominators: 100 all users, including 89 empty truth, and 11 nonempty users. Sparse means 1–5 pre-cutoff eligible Buys; the 65-user sparse subgroup is not substituted for the full evaluation cohort.

## Exact baseline command

```bash
/usr/bin/time -v python3 starter.py run --data-dir "$DATA" --output-dir outputs/baseline
```

The saved baseline run took 10.77 seconds for all four methods together. `outputs/baseline` supplies the frozen contexts and protocol consumed by every arm.

## Exact full-arm commands

Run sequentially, as overnight, in C → A → B order. These commands reproduce inference and should only be run intentionally in a new experiment; do not overwrite the archived measured outputs.

```bash
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "$DATA" --arm C --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/arm_C
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "$DATA" --arm A --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/arm_A
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "$DATA" --arm B --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/arm_B
```

No `--max-users` flag: default **0** means all 100 input contexts. Other unchanged defaults: backend **hf**, dtype **float32**, threads flag **0** (torch default left unchanged), seed **0**, summary max_new_tokens **120**, rank max_new_tokens **60**, mock-fail-every **0** (irrelevant to HF). The current defaults also name the same model and pinned revision, but both were supplied explicitly. The tokenizer chat-template call sets **enable_thinking=False**; generation sets **do_sample=False**. No sampling, prompt modification between runs, few-shot examples, candidate permutation, or new retrieval model was introduced.

A/B each make one ranking call per user; C makes a summary call and a ranking call. No customer risk/capacity or asset names appear in the A/B/C model inputs. Each arm writes `responses.jsonl`, `raw_log.jsonl`, and `run_meta.json` locally under its output directory.

## Exact scoring commands — no model invocation

```bash
python3 starter.py run --data-dir "$DATA" --output-dir outputs/arm_A_eval --stage ranker --responses outputs/arm_A/responses.jsonl --on-invalid fallback
python3 starter.py run --data-dir "$DATA" --output-dir outputs/arm_B_eval --stage ranker --responses outputs/arm_B/responses.jsonl --on-invalid fallback
python3 starter.py run --data-dir "$DATA" --output-dir outputs/arm_C_eval --stage ranker --responses outputs/arm_C/responses.jsonl --on-invalid fallback
```

Fallback replaces a caught per-user invalid custom response with that user's CBF ranking and records a custom failure. Measured A/B/C each have **0 invalid outputs and 0 scoring custom failures**, so none required fallback. No users were dropped. Evaluation protocols exactly match the original baseline; all four baseline metric blocks match at full saved precision.

Full protocol hash:

```text
50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417
```

## Results and analysis

- `results/results_table.md`: seven methods, both nDCG means, runtimes and failed cases, copied from named evaluation/metadata files.
- `results/task3_analysis_aggregate.md`: descriptive paired differences, recall, sparse subgroup means, candidate-order behaviour, repeat-asset recommendations, coverage and token/time aggregates. No conclusions or statistical claims are supplied.
- Local-only `results/task3_analysis.md`: same aggregates plus identified sparse-user scores, label coverage by user, and ten seed-42 summary/history samples for the student's own manual factuality check.
- Local-only `results/task3_tokens_per_user_LOCAL.csv`: tokenizer counts per user/stage. Prompt counts reconstruct the actual chat template; saved-text output token counts exclude unrecoverable stripped special tokens. Individual user latencies are not logged; mean seconds/user is recorded arm time / 100.

Recorded whole-arm loop times: A **6296.8 s**, B **6346.9 s**, C **9604.6 s**. These exclude model loading and initial context/questionnaire reading; C includes summary generation. They are not cold end-to-end command times and do not include later scoring.

## Commit preparation

Proposed allowlist only:

1. `llm_rerank.py`
2. `requirements.txt`
3. `README_hw2_dastan.md`
4. `results/results_table.md`
5. `results/task3_analysis_aggregate.md`

Generated prompts, summaries, raw customer IDs, predictions, per-user scores, tokens-per-user tables, logs, and dataset/model caches stay local. In particular, exclude `outputs/`, `reference/`, `.venv/`, `results/task2_smoke.md`, `results/task3_analysis.md`, `results/session1_report_extracted.txt`, and other local notes containing user-level material. Do not stage the whole folder. The existing `.gitignore` ignores outputs but does not by itself exclude every local result document; use an explicit allowlist.

**Prompt-text distinction requiring confirmation:** the required source file `llm_rerank.py` necessarily contains the shared static prompt templates and their construction code. It contains no saved, customer-instantiated prompts or customer IDs. The four proposed documentation/dependency files contain neither actual prompt text nor raw customer IDs. If “no prompt text committed” literally includes source-code templates, `llm_rerank.py` cannot satisfy that rule unchanged; confirm the instructor's intended distinction before staging it. No prompt templates were removed or altered for commit preparation.

No commit or remote creation is performed by these instructions. The team repository URL/location must be confirmed before staging or committing.
