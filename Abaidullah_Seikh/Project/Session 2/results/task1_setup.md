# HW2 Task 1 — setup and baseline verification

**Student:** Abaidullah Seikh, Team 8. **Dataset:** FAR-Trans. **Course:** LLM4Rec, HSE University.

## Status and scope

Final selected pipeline: Madlyn's `llm_rerank.py`, using the starter's fixed CBF top-50. Only the Investor information block changes across A (structured), B (deterministic history text), and C (LLM summary). The current `structured_block()` is provisional; its intended Task 2 fix has not been applied. No A/B/C inference or scores exist. `far-trans-llm/` is reference only; its 26 tests passed during the earlier plan, but its ranker is not the selected implementation.

`Pipeline/` contained only `llm_rerank.py`; the root `README_rq4.md` was read separately. The starter contents, including `.gitignore`, were copied into Session 2. The official homework replaced the old root homework; its sole addition was the nine-line “Provided LLM baselines (optional starting points)” section. The Session 1 PDF was copied into `reference/`. Protected sources were not edited. The starter's requested test command passed **58 tests in 4.186 s**. Completed installation and baseline runs were retained, not repeated.

## Starter interfaces, candidates, and metric

- Plugin: `encode(context) -> {observed_history_ISIN: finite_nonnegative_weight}` and/or `rerank(context, candidate_ids) -> ten unique candidate ISINs`. Boolean, negative, nonfinite, and non-history weights are rejected. If both seams exist, encoded retrieval supplies the reranker's candidates. `extensions.py` is an identity encoder, not an LLM; it reproduces CBF.
- Saved response JSONL: one object per user, with `user_id`, `stage`, matching `protocol_hash`, and either `ranked_ids` (ranker: ten distinct strings from the candidate pool) or `history_weights` (encoder: observed-history weight mapping). Cohort/stage/hash mismatches are invalid. There are no model calls in the starter.
- Eligible assets have metadata strictly before the cutoff and a positive historical close price. Exact duplicate transaction rows and negative-ID reconstructed positions are excluded. History uses eligible pre-cutoff Buys; truth is distinct eligible future Buy ISINs, not transaction multiplicity.
- CBF uses normalized binary categorical token vectors for assetCategory, assetSubCategory, sector, industry, and marketID. The user profile is a normalized Buy-count-weighted sum. Assets are sorted by descending content score, then ascending ISIN; zero-profile users use popularity. The first 50 are the fixed reranker pool. Popularity counts distinct historical buying users. Repeat purchases are allowed.
- Binary nDCG@10: DCG sums `1/log2(rank+1)` at relevant positions; IDCG sums the first `min(10, number_of_truth_assets)` discounts. Empty truth is 0. The primary macro mean includes every selected user; the separately labeled nonempty mean includes only users with future purchases.
- `outputs/baseline/per_user.csv` stores individual scores and relevant counts; `predictions.csv` stores rankings; `metrics.json` stores aggregates; `protocol.json` stores full protocol/hash; `contexts.jsonl` stores historical input without truth IDs.
- Starter `--on-invalid` defaults to `error`. With `fallback`, caught per-user ValueError/KeyError/TypeError during custom evaluation substitutes that user's original CBF top ten and logs the error in `custom_failures`. Users remain evaluated. Global response-file failures are not all covered by this per-user fallback.

## Baselines: measured unchanged

Command, run from Session 2:

```bash
/usr/bin/time -v python3 starter.py run --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --output-dir outputs/baseline
```

| Method | Users | Future-purchase users | Empty truth | nDCG@10 all | nDCG@10 nonempty | README match |
|---|---:|---:|---:|---:|---:|---|
| popularity | 100 | 11 | 89 | 0.0286 | 0.2599 | yes |
| cbf | 100 | 11 | 89 | 0.0201 | 0.1827 | yes |
| latest_buy | 100 | 11 | 89 | 0.0277 | 0.2520 | yes |
| latest_buy_or_sell | 100 | 11 | 89 | 0.0271 | 0.2464 | yes |

Whole-run wall time: **10.77 s**; user time 10.22 s; system time 0.53 s; CPU 99%; peak RSS **590,340 KiB**. Exit status 0. These are whole-run measurements, not per-method timings. Reconstructed initial-position rows excluded: **38,019**. Custom failures: **0** (no custom method run).

Full protocol hash:

```text
50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417
```

Cutoff `2021-06-01` exclusive; future window `[2021-06-01, 2021-07-01)`; deterministic warm-user selection uses SHA-256 of `42:` plus user ID. The reference hash prefix matches; the team's full hash was not supplied.

## Context inspection (saved outputs only)

History contains **390 asset records**; candidates contain **5,000 records** (100 × 50). Counts below are record occurrences, not distinct assets. Missing means an attribute token is absent after starter filtering, not a missing dictionary key.

| Attribute | History present | History missing | Candidate present | Candidate missing |
|---|---:|---:|---:|---:|
| assetCategory | 390 | 0 | 5000 | 0 |
| assetSubCategory | 305 | 85 | 1918 | 3082 |
| sector | 326 | 64 | 1518 | 3482 |
| industry | 323 | 67 | 1518 | 3482 |
| marketID | 390 | 0 | 5000 | 0 |

History record keys: `attributes`, `buy_count`, `id`, `metadata_timestamp`, `name`. Candidate keys: the same except `buy_count`. Attributes are a list of `key=value` strings, not a nested attribute dictionary.

History is **descending Buy count, then ascending ISIN**, not chronological. All saved histories were checked against this order. Deciding code (`starter.py:154–156`):

```python
'history': [dict(asset(i), buy_count=n) for i, n in
            sorted(counts.items(), key=lambda p: (-p[1], p[0]))],
'candidate_assets': [asset(i) for i in cbf_ids[:candidate_count]],
```

No Sell events appear in contexts (zero literal `Sell` occurrences; history construction excludes non-Buys). Sell events are read separately only for the recency baseline and are not negative preferences. History metadata timestamps are asset metadata dates, not purchase dates.

**1 user** has more than `HISTORY_CAP=20` distinct history assets. The saved contexts themselves are not capped. Current shared Arm A uses all history; B/C consume `history[:20]`. This is a full-cohort information-parity issue for Task 2. None of the 1–5 Buy users can exceed 20 distinct assets.

Saved-output counts (`results/inspect_baseline.py`, read-only):

- **11 of 100** users have future purchases.
- **65** users have 1–5 historical Buy transactions (`sum(buy_count)`); **2 of 65** have future purchases.
- **18** future user–asset relevance labels, summed once per user from CBF `relevant_count`. This is not a count of raw future transaction rows.
- **Top-50 coverage: unverified.** The starter outputs omit truth ISINs; counts and top-10 nDCG do not identify which labels fall in ranks 11–50. The supplied reference **6 of 18** cannot be independently established using only these outputs. No raw future data were read to circumvent that restriction.

## Shared script: SHA-256, options, prompts, and generation

Both current copies have SHA-256:

```text
73a5e2b7d4b660fface3526fe29917199f2f2ce0443c77f7c100e83ad015b574
```

They match each other, but **do not match** the supplied team SHA-256:

```text
d7a34c1f9f715d7437ca5b2cc7989dbff12348602495b8a427cf8e56fa7007ba
```

The student reports Madlyn is sending the current file. No replacement or modification was made.

Every CLI option, determined by source inspection without running the script:

| Option | Default | Notes |
|---|---|---|
| `-h`, `--help` | argparse help action | exits after help |
| `--run-dir` | None; required | starter contexts/protocol directory |
| `--data-dir` | None; required | questionnaire dates |
| `--arm` | None; required | A/B/C/D |
| `--out-dir` | None; required | output directory |
| `--backend` | `hf` | hf/mock |
| `--model` | `Qwen/Qwen2.5-1.5B-Instruct` | must explicitly select Qwen3 for the intended run |
| `--revision` | None | intended pinned commit below |
| `--dtype` | `float32` | float32/bfloat16 |
| `--threads` | 0 | leaves torch thread default unchanged |
| `--seed` | 0 | passed to torch.manual_seed |
| `--max-users` | 0 | all input contexts; positive value takes prefix |
| `--summary-tokens` | 120 | summary max_new_tokens |
| `--rank-tokens` | 60 | ranking max_new_tokens |
| `--mock-fail-every` | 0 | mock plumbing only |

Exact `HFBackend.chat()` template call (`llm_rerank.py:224–225`):

```python
ids = self.tok.apply_chat_template(messages, add_generation_prompt=True,
                                   return_tensors='pt')
```

**It does not pass `enable_thinking=False`.** Thinking-off parity with the team is therefore not met. Greedy generation is explicit: `do_sample=False`, `max_new_tokens=max_new_tokens`, `pad_token_id=self.tok.eos_token_id`; the model is in eval mode and generation uses `torch.no_grad()`. No explicit context-limit check or truncation is implemented here. Do not transfer the instructor ranker's 8192/512 settings to this script.

For A/B/C the ranker sees no customer profile and no asset names. Candidates show numbered ISINs plus categorical attributes. B serializes ISIN/attributes/Buy count, with a cutoff header and no transaction dates. C summarizes the same B history into 3–4 sentences about asset kinds, markets, concentration, and repeats. A currently aggregates totals, distinct assets, repeated assets, and Buy-weighted top-five category/subcategory/market values. Only D adds risk/capacity to the summary input.

The requested ranking is JSON `{"ranking": [candidate_numbers]}`. Parsing extracts the first brace-delimited object, keeps integer non-boolean candidate numbers, removes out-of-range numbers and duplicates, and takes at most ten. Fewer than ten marks an invalid output. There is no regeneration or in-script CBF substitution; scoring the resulting `responses.jsonl` with starter `--on-invalid fallback` supplies CBF fallback. Completed arms would write `responses.jsonl`, `raw_log.jsonl`, and `run_meta.json`. These have not been generated.

## Local model verification — no download or inference

The user completed the download outside OpenCode. Verification used `snapshot_download(repo_id='Qwen/Qwen3-1.7B', revision='70d244cc86ccca08cf5af4e1e306ecf908b1ad5e', local_files_only=True)`, then local-only tokenizer/config loading with `trust_remote_code=False`.

Snapshot: `/home/dastan/.cache/huggingface/hub/models--Qwen--Qwen3-1.7B/snapshots/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`

| File | Bytes |
|---|---:|
| .gitattributes | 1570 |
| LICENSE | 11343 |
| README.md | 13963 |
| config.json | 726 |
| generation_config.json | 239 |
| merges.txt | 1671853 |
| model-00001-of-00002.safetensors | 3441185608 |
| model-00002-of-00002.safetensors | 622329984 |
| model.safetensors.index.json | 25605 |
| tokenizer.json | 11422654 |
| tokenizer_config.json | 9732 |
| vocab.json | 2776833 |
| **Total (12 nonempty files)** | **4079450110** |

Tokenizer: **Qwen2TokenizerFast**, vocabulary length **151669**. Config model type: **qwen3**; config `_commit_hash` equals **70d244cc86ccca08cf5af4e1e306ecf908b1ad5e**. Both safetensors headers open successfully: **310** tensor keys in shard 1 and **1** in shard 2. All **311** keys and their shard assignments match `model.safetensors.index.json`, verified by `results/verify_task1_artifacts.py`. This confirms local file presence and metadata readability; model tensor loading/inference was not performed.

## Environment

| Item | Verified value |
|---|---|
| Python | 3.14.4 (GCC 15.2.0) |
| torch | 2.11.0+cpu, installed from PyTorch CPU index |
| transformers | 4.57.6 |
| accelerate | 1.15.0 |
| huggingface_hub | 0.36.2 |
| CPU | Intel Core i7-6600U CPU @ 2.60GHz |
| Physical cores / logical CPUs | 2 / 4 |
| RAM | 11,848,441,856 bytes (about 11.03 GiB) |
| OS | Linux 7.0.0-42-generic, x86_64, glibc 2.43 |

## Match with team pipeline

“Yes” below means the supplied reference matches the verified local value at the stated precision; unspecified full references remain unverified. Execution settings are not inferred from CLI defaults.

| item | team value | my value | match yes/no |
|---|---|---|---|
| protocol_hash | prefix `50efd4aeb415`; full hash unverified | `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417` | yes, prefix only; full unverified |
| llm_rerank.py SHA-256 | `d7a34c1f9f715d7437ca5b2cc7989dbff12348602495b8a427cf8e56fa7007ba` | `73a5e2b7d4b660fface3526fe29917199f2f2ce0443c77f7c100e83ad015b574` | no; replacement pending |
| model | Qwen/Qwen3-1.7B | cached and locally verified; no arm run | yes, setup only |
| revision | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` | identical resolved config commit | yes |
| torch | 2.11.0 CPU | 2.11.0+cpu | yes |
| transformers | 4.57.6 | 4.57.6 | yes |
| thinking off | enable_thinking=False expected | argument missing | no |
| greedy decoding | do_sample=False | do_sample=False in source | yes, source only |
| popularity all/nonempty | 0.0286 / 0.2599 | 0.0286 / 0.2599 | yes |
| cbf all/nonempty | 0.0201 / 0.1827 | 0.0201 / 0.1827 | yes |
| latest_buy all/nonempty | 0.0277 / 0.2520 | 0.0277 / 0.2520 | yes |
| latest_buy_or_sell all/nonempty | 0.0271 / 0.2464 | 0.0271 / 0.2464 | yes |
| nonempty users | 11 / 100 | 11 / 100 | yes |
| sparse nonempty users | 2 / 65 | 2 / 65 | yes |
| future labels in top-50 | 6 / 18 | denominator 18 verified; numerator unverified | unverified |
| dtype | to confirm with Madlyn | default float32; run flag to confirm with Madlyn | unverified |
| threads | to confirm with Madlyn | default 0; run flag to confirm with Madlyn | unverified |
| seed | to confirm with Madlyn | default 0; run flag to confirm with Madlyn | unverified |
| summary token limit | to confirm with Madlyn | default 120; run flag to confirm with Madlyn | unverified |
| rank token limit | to confirm with Madlyn | default 60; run flag to confirm with Madlyn | unverified |

All long commands used a 1,800,000 ms timeout after the user's update. Earlier agent downloads timed out; the user's separate successful download is distinguished from the offline verification above. No unfinished download is reported as a completed model experiment.
