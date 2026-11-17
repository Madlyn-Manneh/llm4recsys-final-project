# Session 2 — raw history versus LLM summary

Rustam Shangareev, Team 8. Individual RQ2: does summarizing the same transaction history improve future-purchase nDCG@10 under the same LLM reranker?

## What was actually run

The four unmodified course baselines and both B (raw text) and C (summary) were executed on the same required 100 users, one pinned Qwen/Qwen3-1.7B snapshot, the exact same 50 ordered candidates per user, and one H100. This is the Session 2 teaching protocol (history strictly before 2021-06-01; labels until 2021-07-01), not the provisional Session 1 2022 split. No teammate model scores were substituted.

| Method | All 100 | Nonempty 11 |
|---|---:|---:|
| Popularity | 0.0286 | 0.2599 |
| CBF | 0.0201 | 0.1827 |
| Latest buy | 0.0277 | 0.2520 |
| Latest buy or sell | 0.0271 | 0.2464 |
| B: raw history | 0.0228 | 0.2076 |
| C: LLM summary | 0.0248 | 0.2257 |

C minus B is 0.0019897000 over all users. The entire difference comes from one relevant asset moving from rank 9 to rank 3. No significant or general sparse-user benefit is claimed. Both arms have zero invalid rankings. Summary fidelity issues remain. `results/aggregate.json` contains exact public aggregates and cache-aware timing counts; full private local evidence retains raw prompts, outputs and independent recomputation.

## Reproduce

Use a fresh Linux Python 3.11.5 environment with one idle NVIDIA H100 80 GB and its compatible driver. The archived inference deliberately waits if no H100 is idle; it does not stop other jobs. Keep the notebook working directory at this `session2` folder. Allow roughly 5 GB for the pinned model plus the data and outputs. The measured environment used Torch 2.9.1+cu128, Transformers 4.57.6, HF Hub 0.36.2, float32, greedy decoding, seed 0, thinking off, TF32 off, SDPA. The summary/ranking budgets are 120/60 new tokens.

```bash
python -m pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
python -m pip install transformers==4.57.6 huggingface-hub==0.36.2 numpy==2.4.6 jupyter nbconvert ipykernel
export FAR_TRANS_ARCHIVE=/absolute/path/to/FAR-Trans.zip
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 reproduce_v1.ipynb --output reproduction.executed.ipynb
```

Obtain FAR-Trans from https://researchdata.gla.ac.uk/1658/ and retain the original ZIP (SHA-256 `d0d6cfe027732bab45fdcf9af80eff4fefddc789aedae9bdce0d3d6cfd05cfb6`). The setup stages this ZIP, fetches only the two pinned shared input files from team commit `31e7a2545f8f156f630d193ae9583828bbbdd7e5`, and downloads public Qwen revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`. All data/model/input hashes are checked. An offline Hub needs those files staged before launching; internet access is not assumed during inference.

The launcher runs the archived preparation, twice-seeded baseline, source/data verification, context-parity check, unchanged actual `inference_v4`, and unchanged `evaluate_v2` in separate processes. The source verifier is stopped before its historical blocked-network status report; its numerical checks are retained. Input setup and this launcher were added for portability after the measured run; they are not reported as additional experimental runs. Start with a fresh project copy because result paths intentionally refuse overwriting. Different CUDA/driver versions can affect near-tie outputs; record the actual environment rather than asserting cross-hardware identity.

Read final scores in `llm4rec_s2_rq2/recovered_v1/evaluation/results-summary.json` and per-user/prediction CSVs alongside it. `llm4rec_s2_rq2/requirements-inference-actual.txt` is the original measured dependency inventory; it includes packages layered over an existing CUDA environment and is not a standalone installation lock. The complete active text-inference dependency closure is recorded in `dependency-closure-requirements.txt` and `dependency-closure.json`; the latter also records the actual CUDA Torch build.

## Source and attribution

- `llm4rec_s2_rq2/inputs/starter.py`, `extensions.py`, `test_starter.py`: unchanged course commit `f6850861ea20a51e1fb018ee4e5f840c2ac759e0` (58 tests pass).
- `llm_rerank_original.py`: unchanged shared wrapper supplied by Madlyn Manneh; templates and valid-output parsing are reused.
- `notebooks/llm4rec_s2_rq2_inference_v4.ipynb`: exact executed model source, code SHA-256 `339442f910a7eb6559398d4a17f1fd15705116241a2f2876620ff8e1a848c47e`. Adds local GPU loading, verified offline snapshot, cache/logging, and a narrow TypeError guard for null/scalar rankings; invalid outputs retain starter CBF fallback.
- `notebooks/llm4rec_s2_rq2_evaluate_v2.ipynb`: exact scoring/reconciliation source. Preserves all users, independently recomputes nDCG, checks actual prompts and cached generations.
- Fixed summary-audit positions were chosen before inference: 0, 1, 2, 24, 49, 74, 99 (zero-based). No prompts were tuned after seeing outcomes.
- `SOURCE-PROVENANCE.json` pins source hashes and execution identity.

These are AI-assisted source and results. The student's personal verification is the separately reported single CBF nDCG arithmetic example. Model weights, FAR-Trans records, customer IDs and per-user generations are excluded from this source package; the pinned shared input files are fetched during reproduction. This experiment predicts purchases, not investment suitability or profit.
