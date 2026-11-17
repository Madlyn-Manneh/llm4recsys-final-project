# Task 2 — Arm A definition and real-model three-user smoke test

**Student:** Abaidullah Seikh, Team 8. **Dataset:** FAR-Trans. **Pipeline:** Madlyn's shared `llm_rerank.py`, with only the RQ1 owner's specified `structured_block()` replacement.

## Outcome

All three real-model smoke runs completed: **A 0/3 invalid, B 0/3 invalid, C 0/3 invalid**. None of the **nine** raw ranking outputs contains `<think>` or `</think>` (case-insensitive check). Each response maps to ten distinct ISINs in that user's unchanged top-50 candidate pool. This is an execution/format smoke test, not an nDCG comparison or evidence of improved recommendation quality. Summary factuality is discussed below; valid rankings do not imply faithful summaries.

The student reports that Madlyn confirmed the five attributes and history order and agreed to the corrected A. The definition was drafted with Claude (claude.ai) and previously checked there on fake data/mock plumbing; **the results here use the real HF model, never mock**.

## Provenance and SHA-256

| File | SHA-256 |
|---|---|
| `llm_rerank_old_73a5e2b7.py` (archive, untouched) | `73a5e2b7d4b660fface3526fe29917199f2f2ce0443c77f7c100e83ad015b574` |
| `Pipeline/llm_rerank.py` (team original, untouched) | `d7a34c1f9f715d7437ca5b2cc7989dbff12348602495b8a427cf8e56fa7007ba` |
| `llm_rerank_original.py` (unedited current copy) | `d7a34c1f9f715d7437ca5b2cc7989dbff12348602495b8a427cf8e56fa7007ba` |
| **`llm_rerank.py` (corrected Arm A, used for all smoke runs)** | **`85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da`** |

The required team hash matched before the edit. AST-located source comparison confirmed that everything outside `structured_block()` is byte-for-byte identical to the preserved current copy. The replacement includes the two blank lines in the supplied docstring. B/C functions, ranker template, backend, defaults, and parsing were not changed.

Earlier attempts stopped at the user's required hash gate while the old file was still in Pipeline. Two subsequent Arm A tool executions were interrupted before any smoke output directory was created. After explicit continuation, the three completed runs below were obtained. No failed or interrupted attempt contributes a fabricated runtime or response.

## What Madlyn changed from the old version

Output of `diff -u llm_rerank_old_73a5e2b7.py llm_rerank_original.py` (file timestamps omitted):

```diff
--- llm_rerank_old_73a5e2b7.py
+++ llm_rerank_original.py
@@ -221,12 +221,17 @@
     def chat(self, system, user, max_new_tokens):
         messages = [{'role': 'system', 'content': system},
                     {'role': 'user', 'content': user}]
-        ids = self.tok.apply_chat_template(messages, add_generation_prompt=True,
-                                           return_tensors='pt')
+        # enable_thinking=False is read by Qwen3's chat template (thinking off,
+        # as in the provided far-trans-llm baselines); other templates ignore it.
+        text = self.tok.apply_chat_template(messages, tokenize=False,
+                                            add_generation_prompt=True,
+                                            enable_thinking=False)
+        enc = self.tok(text, return_tensors='pt')
         with self.torch.no_grad():
-            out = self.model.generate(ids, max_new_tokens=max_new_tokens,
+            out = self.model.generate(**enc, max_new_tokens=max_new_tokens,
                                       do_sample=False,
                                       pad_token_id=self.tok.eos_token_id)
+        ids = enc['input_ids']
         return self.tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).strip()

     def meta(self):
@@ -248,8 +253,8 @@
     p.add_argument('--arm', choices=['A', 'B', 'C', 'D'], required=True)
     p.add_argument('--out-dir', type=Path, required=True)
     p.add_argument('--backend', choices=['hf', 'mock'], default='hf')
-    p.add_argument('--model', default='Qwen/Qwen2.5-1.5B-Instruct')
-    p.add_argument('--revision', default=None, help='HF commit hash; record it')
+    p.add_argument('--model', default='Qwen/Qwen3-1.7B')
+    p.add_argument('--revision', default='70d244cc86ccca08cf5af4e1e306ecf908b1ad5e', help='HF commit hash; record it')
     p.add_argument('--dtype', default='float32', choices=['float32', 'bfloat16'])
     p.add_argument('--threads', type=int, default=0)
     p.add_argument('--seed', type=int, default=0)
```

These are all differences: Qwen3 model/revision defaults, explicit thinking-off template rendering, and tokenization returning the encoding (including attention mask) used via `generate(**enc)`. The revision is unchanged by my Arm A fix. `HFBackend.chat()` explicitly passes **`enable_thinking=False`** and generation explicitly uses **`do_sample=False`**.

## Arm A-only diff

Output of `diff -u llm_rerank_original.py llm_rerank.py` (timestamps omitted):

```diff
--- llm_rerank_original.py
+++ llm_rerank.py
@@ -102,23 +102,39 @@


 def structured_block(ctx):
-    """Arm A (PROVISIONAL): fixed-format counts, computed without an LLM."""
+    """Arm A (RQ1 owner's definition): fixed-format features of exactly the
+    history arm B shows, computed without an LLM.
+
+
+    Parity with B: same HISTORY_CAP rows; per-ISIN buy counts in B's order
+    (buy count desc, then ISIN); the five starter attributes, each as a share
+    of buys. A missing value is left out, as B leaves it out, so shares can
+    sum to less than 100%. Only the form differs: aggregated features (A)
+    versus one line per asset (B)."""
     from collections import Counter
-    rows = ctx['history']
+    rows = ctx['history'][:HISTORY_CAP]           # same rows as history_block()
     total = sum(a['buy_count'] for a in rows)
     lines = [f"Structured history features as of {ctx['cutoff']} (Buy transactions only):",
              f"- total Buy transactions: {total}",
              f"- distinct assets bought: {len(rows)}",
              f"- assets bought more than once: {sum(a['buy_count'] > 1 for a in rows)}"]
-    for key in ('assetCategory', 'assetSubCategory', 'marketID'):
+    if len(ctx['history']) > HISTORY_CAP:
+        lines.append(f"- features cover {HISTORY_CAP} of {len(ctx['history'])} assets "
+                     f"(same cap as arm B)")
+    per_asset = sorted(rows, key=lambda a: (-a['buy_count'], a['id']))
+    lines.append('- buys per asset (ISIN): ' +
+                 ', '.join(f"{a['id']} ({a['buy_count']})" for a in per_asset))
+    for key in ('assetCategory', 'assetSubCategory', 'sector', 'industry', 'marketID'):
         counts = Counter()
         for a in rows:
-            value = next((t.split('=', 1)[1] for t in a['attributes']
-                          if t.startswith(key + '=')), 'unknown')
-            counts[value] += a['buy_count']
-        top = ', '.join(f'{v} ({n})' for v, n in sorted(counts.items(),
-                        key=lambda kv: (-kv[1], kv[0]))[:5])
-        lines.append(f'- {key} (buys): {top}')
+            for t in a['attributes']:
+                if t.startswith(key + '='):
+                    counts[t.split('=', 1)[1]] += a['buy_count']
+        if counts:                                # absent everywhere -> absent, as in B
+            shares = ', '.join(f'{v} {n}/{total} ({100 * n / max(total, 1):.0f}%)'
+                               for v, n in sorted(counts.items(),
+                                                  key=lambda kv: (-kv[1], kv[0])))
+            lines.append(f'- {key} (share of buys): {shares}')
     return '\n'.join(lines)


```

## Real-user A/B parity check

User **`7F4C738BC9D4A144C518`**, the first selected user, has two history assets. Exact blocks:

**Arm A**

```text
Structured history features as of 2021-06-01 (Buy transactions only):
- total Buy transactions: 2
- distinct assets bought: 2
- assets bought more than once: 0
- buys per asset (ISIN): GRF000022001 (1), GRF000093002 (1)
- assetCategory (share of buys): mtf 2/2 (100%)
- assetSubCategory (share of buys): bond 1/2 (50%), money market 1/2 (50%)
- marketID (share of buys): aedak 2/2 (100%)
```

**Arm B**

```text
History as of 2021-06-01 (Buy transactions only):
- GRF000022001 | assetCategory: mtf, assetSubCategory: money market, marketID: aedak | bought 1x
- GRF000093002 | assetCategory: mtf, assetSubCategory: bond, marketID: aedak | bought 1x
```

Both use precisely these two ISINs in the same order, with one Buy each. Both contain `mtf`, `money market`, `bond`, and `aedak`. Sector and industry are absent in both. The A shares use the same two Buys as denominator; no unknown values are invented.

`results/check_task2_parity.py` also checked **all 100 real contexts** without model calls: the capped rows are already ordered by descending Buy count then ISIN; the A per-ISIN sequence/counts and B lines match those rows; all five attributes' observed values and Buy-weighted fractions appear in A; an attribute absent everywhere is omitted. The one user with more than 20 history assets is now capped in A as in B/C.

**Interpretation:** the same source rows, ISIN counts, and observed attribute values are used. A aggregates the attribute distribution, while B retains each value's association with an individual ISIN. The definition is not a lossless alternative serialization of B; no stronger information-equivalence claim is made. Rounded percentages may not sum to 100%, and omitted attributes can leave their exact shares below 100%.

## Commands and identical settings

Run sequentially from `/home/dastan/Recommender Systems/Project/Session 2`, each with a **1,800,000 ms** tool timeout:

```bash
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm A --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --max-users 3 --out-dir outputs/smoke_A
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm B --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --max-users 3 --out-dir outputs/smoke_B
.venv/bin/python llm_rerank.py --run-dir outputs/baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm C --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --max-users 3 --out-dir outputs/smoke_C
```

Unchanged shared defaults: HF backend; float32; threads flag 0 (leaves torch's default unchanged, not zero execution threads); seed 0; summary limit 120 new tokens; rank limit 60 new tokens. Thinking explicitly off; greedy decoding. A/B do not call the summarizer, although the summary-token default is still recorded in their metadata. No prompts, parsing, candidate ordering, or fallback policy were adjusted after seeing results.

Environment: Python **3.14.4**, torch **2.11.0+cpu**, transformers **4.57.6**; Intel Core i7-6600U, 2 physical cores/4 logical CPUs, RAM 11,848,441,856 bytes. `hardware.processor` is an empty string in run metadata; the CPU name comes from Task 1's `lscpu`, not from that field.

The model emitted a `torch_dtype` deprecation warning and a notice that temperature/top_p/top_k generation-config flags may be ignored. `do_sample=False` remained explicitly set. These notices did not abort any completed run; the shared code was not changed in response.

Full shared protocol hash, recorded in every arm and response:

```text
50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417
```

The hash describes the original 100-user starter cohort. `--max-users 3` takes its first three contexts without recomputing the hash; these are three-user smoke outputs, not completed 100-user responses suitable for evaluating the full cohort without missing-user fallbacks.

## Recorded smoke metadata

Values below come directly from each `outputs/smoke_*/run_meta.json`:

| Arm | Users | invalid_outputs | wall_seconds_whole_arm | resolved_commit | dtype |
|---|---:|---:|---:|---|---|
| A | 3 | 0 | 233.2 | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` | `torch.float32` |
| B | 3 | 0 | 220.8 | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` | `torch.float32` |
| C | 3 | 0 | 321.5 | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` | `torch.float32` |

All use model `Qwen/Qwen3-1.7B`, requested revision equal to resolved commit, and generation settings `{do_sample: false, seed: 0, summary_max_new_tokens: 120, rank_max_new_tokens: 60}`. No fallback was needed or applied during these inference runs.

Despite its name, `wall_seconds_whole_arm` starts **after backend/model loading and questionnaire/context loading**, immediately before the per-user loop. It includes prompt construction in the loop, generation (and summaries in C), parsing and per-user log writing; it excludes model-load/startup time and writing the final metadata. It is not externally measured end-to-end command time.

## Every raw rank_output

These are original candidate numbers, not ISIN aliases invented for the report. The script maps them through each user's fixed candidate list.

### Arm A

User `7F4C738BC9D4A144C518`:

```json
{"ranking": [1, 8, 2, 3, 4, 5, 7, 6, 16, 15]}
```

User `B6E50192F1453975F157`:

```json
{"ranking": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
```

User `8A30590EA4AE29504AEE`:

```json
{"ranking": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
```

### Arm B

User `7F4C738BC9D4A144C518`:

```json
{"ranking": [1, 8, 2, 3, 4, 5, 7, 20, 21, 22]}
```

User `B6E50192F1453975F157`:

```json
{"ranking": [1, 14, 15, 16, 17, 18, 20, 21, 22, 23]}
```

User `8A30590EA4AE29504AEE`:

```json
{"ranking": [1, 2, 3, 4, 5, 6, 7, 11, 12, 13]}
```

### Arm C

User `7F4C738BC9D4A144C518`:

```json
{"ranking": [1, 8, 7, 2, 3, 4, 5, 6, 10, 11]}
```

User `B6E50192F1453975F157`:

```json
{"ranking": [1, 14, 15, 16, 17, 18, 20, 21, 22, 23]}
```

User `8A30590EA4AE29504AEE`:

```json
{"ranking": [1, 3, 4, 5, 6, 7, 9, 10, 11, 12]}
```

## Arm C: each summary alongside its source history

The shared summarizer asks for 3–4 sentences about kinds of assets/markets, concentration and repeated purchases; only the history below is supplied as investor evidence. The complete summary prompts and rank prompts remain in the raw logs. The following summaries are **verbatim model output, not endorsed facts**.

### User `7F4C738BC9D4A144C518`

History:

```text
History as of 2021-06-01 (Buy transactions only):
- GRF000022001 | assetCategory: mtf, assetSubCategory: money market, marketID: aedak | bought 1x
- GRF000093002 | assetCategory: mtf, assetSubCategory: bond, marketID: aedak | bought 1x
```

Summary:

```text
The investor purchases a single unit of a money market fund (GRF000022001) and a single unit of a bond fund (GRF000093002), both from the same market (aedak). The purchases are concentrated in two distinct asset categories: money market and bond. The investor has made two separate purchases, indicating a level of repetition in their buying behavior.
```

Check: `1x` means one Buy transaction, **not one unit**. Each asset has one Buy, so claiming repetition from two different one-off purchases is misleading. Money market/bond are supplied subcategories, not two distinct values of assetCategory (both are `mtf`).

### User `B6E50192F1453975F157`

History:

```text
History as of 2021-06-01 (Buy transactions only):
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
```

Summary:

```text
The investor purchases a single bond in the oil and gas extraction and refining sector, indicating a focus on this specific industry. The transaction is concentrated, as only one asset is listed. The purchase does not show repetition, as it is a single buy transaction.
```

Check: one listed asset and no repeat are supported. It calls an industry a sector (supplied sector is `corporate`) and infers “focus” from a single transaction. Market `xath` and the ISIN are omitted.

### User `8A30590EA4AE29504AEE`

History:

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 3x
- GRS014003032 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS434003000 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - renewable, marketID: xath, sector: utilities | bought 2x
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS191213008 | assetCategory: stock, assetSubCategory: large cap, industry: engineering & construction, marketID: xath, sector: industrials | bought 1x
- GRS213213002 | assetCategory: stock, industry: engineering & construction, marketID: xath, sector: industrials | bought 1x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

Summary:

```text
The investor primarily purchases large-cap stocks in the financial services, utilities, and industrials sectors, with a focus on banks, engineering & construction, and renewable energy. They bought 3x shares of one stock in financial services and 2x shares of another in utilities, indicating a relatively concentrated portfolio. The investor also made repeated purchases of stocks in the financial services and industrials sectors, suggesting a preference for these areas.
```

Check: the named sectors/industries and stock emphasis occur in the input. Counts are again rendered as “shares,” although units were not supplied. Each industrial asset has only one Buy; multiple events in a sector do not show repeat buying of the same asset. One three-Buy asset has no sector, which the summary loses; all ISINs and market `xath` are omitted. A purchase history alone does not establish current portfolio concentration or a persistent preference. No prompt was edited in response to these findings.

## Full 100-user runtime estimates

Linear extrapolation: **recorded three-user arm time × 100/3**. These are rough estimates of the timed arm loop only, not measured full-run results or end-to-end times.

| Arm | Measured 3-user seconds | Seconds/user | Estimated 100-user seconds | Estimated minutes | Estimated hours |
|---|---:|---:|---:|---:|---:|
| A | 233.2 | 77.73 | 7773.3 | 129.6 | 2.16 |
| B | 220.8 | 73.60 | 7360.0 | 122.7 | 2.04 |
| C | 321.5 | 107.17 | 10716.7 | 178.6 | 2.98 |

Combined serial estimate: approximately **7.18 hours**, plus model startup for each arm and other excluded work. The first three users are not a representative random timing sample: their histories have 2, 1, and 7 distinct assets, whereas some full-cohort histories reach the 20-asset cap. Prompt length, output length, CPU contention, memory pressure and thermal state can change runtime. C has one extra model call per user. No calibrated prediction interval is available from a single three-user run. The earlier 30-minute tool timeout is sufficient for these smoke commands but would be shorter than each estimated 100-user run.

## Saved evidence and verification

Each of `outputs/smoke_A/`, `outputs/smoke_B/`, `outputs/smoke_C/` contains:

- `run_meta.json`: arm, users, invalid count, loop runtime, model/revision, dtype and generation settings;
- `raw_log.jsonl`: complete prompts, raw outputs, parsed candidate numbers, validity, and summaries for C;
- `responses.jsonl`: three user records with `stage=ranker`, original protocol hash and mapped ISIN lists.

`results/inspect_task2_smoke.py` re-parsed all nine outputs, checked user order, response ISIN mapping, shared template construction, protocol/revision/settings, distinct candidate membership and absence of think tags. It also verified that each C summary prompt contains the expected source history. All checks passed. `results/check_task2_parity.py` verified the edit boundary and real-input A/B parity. Both are read-only inspection helpers; neither generates model results. Hashes were checked again after inference and remained as listed above.

Task 1 documents intentionally describe the earlier setup state (old script and no arm inference). This report records the subsequent replacement, Arm A correction and completed smoke tests. No full-cohort method evaluation or nDCG score has been generated for A, B or C.
