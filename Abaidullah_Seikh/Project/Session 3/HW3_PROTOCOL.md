# HW3 development protocol — Abaidullah Seikh, RQ1

## Status and scope

Pre-registration of the development comparisons below, recorded after verifying the shared 200-user starter run and before new HW3 LLM inference. Results will be labelled **development results**. The four starter baseline results were already inspected during setup; this is not a claim of an unseen test set or pre-registration before those baseline results.

Customer identifiers, instantiated prompts, model responses, and cohort membership files remain local and are not included in this document.

## Main development protocol

- Cohort: the 200 warm users selected by the unchanged starter in `outputs/baseline_200`, in starter order. Positions 1–100 and 101–200 refer to that order.
- Cutoff: `2021-06-01`; historical information is strictly before the cutoff.
- Future purchase window: 30 days, from `2021-06-01` inclusive to `2021-07-01` exclusive.
- Candidates: the starter's fixed top-50 CBF candidates for each user; rerankers return ten unique candidate assets.
- Repeat purchases allowed (`exclude_seen = false`).
- Preserve the starter's eligible-asset, exact-full-row duplicate, and reconstructed-initial-position exclusion policies.
- Full protocol hash: `d46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697`.

## Arms

1. Four starter baselines: `popularity`, `cbf`, `latest_buy`, and `latest_buy_or_sell`.
2. CBF candidate order as the matched no-rerank control: the first ten of the same ordered top-50 candidates shown to the rerankers. This is the CBF baseline expressed as the matched control, not an additional independent method.
3. **A — structured history:** my `llm_rerank.py`, SHA-256 `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da`. Reuse the verified HW2 results for positions 1–100; generate positions 101–200 in a later run.
4. **C — team summary:** positions 1–100 from my HW2 run; positions 101–200 from my teammate's shared run, conditional on a three-user identity check of the applicable contexts, candidates, prompt construction, model revision, and generation settings. Do not merge on user coverage alone. Record the check and source provenance before accepting the shared run.
5. **C′ — fact-preserving-summary ablation:** `llm_rerank_c2.py`, SHA-256 `0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada`. Uses the fact-preserving summary instruction, a revision made after the HW2 failure analysis. Run on all 200 users; label this as a post-HW2-analysis development ablation.
6. **Provided LLM comparison:** the provided `far-trans-llm` ranker. Who runs it is to be agreed with the team; document its configuration and comparability to this protocol before reporting results.

For A, C, and C′, retain the shared ranking template and generation settings except for the specified representation/summary intervention. Reference setup: Qwen/Qwen3-1.7B revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, CPU float32, deterministic generation (`do_sample = false`, seed 0), summary limit 120 new tokens, ranking limit 60 new tokens. Historical representation uses the script's 20-asset cap; candidate count remains 50.

## Sparse development window — separate analysis

- This is a separate, explicitly labelled **sparse development window**, not a replacement for the main 200-user cohort.
- Eligible users have 1–5 Buy transactions in the starter-eligible, deduplicated, non-reconstructed history strictly before `2021-06-01`. Count transactions, not distinct assets, and use the full eligible history rather than the LLM representation's 20-asset cap.
- Use the starter's own warm-user order across all eligible warm users; filter by the 1–5 Buy condition and take the first 120. Do not restrict selection to the main cohort.
- Keep the same cutoff, asset eligibility, candidate construction, top-50 candidates, and repeat-purchase policy; use `--horizon-days 90` for later evaluation. The evaluation window ends `2021-08-30` exclusive.
- Arms: four starter baselines, CBF order as matched no-rerank control, A, C, and C′.
- Cohort preparation must use only pre-cutoff eligible history, without computing future truth, metrics, or running starter evaluation. Stop if the available starter functions cannot satisfy that restriction. Store the selected list locally at `cohorts/sparse_window_users.txt`; never commit it or print its identifiers.
- The current shared ranking template explicitly says “next 30 days.” Preserve that template for this development comparison and disclose that its rankings are evaluated over a 90-day sparse window; do not silently change the prompt or either frozen script.

## Metrics and reporting

- Primary: mean nDCG@10 over all evaluated users, with empty future truth contributing zero.
- Secondary: mean nDCG@10 among users with future purchases, together with the number of those users. Also report total evaluated users.
- Paired comparisons on the same users: **A − C** and **C′ − C**, computed from per-user nDCG@10. Report the cohort and denominator explicitly; do not silently drop empty-truth users from the primary comparison.
- Display metrics and paired differences to four decimal places; preserve full precision in local machine-readable artifacts.
- Label all reported measurements **development results**, distinguishing the main and sparse windows.
- Report summary-generation time separately from ranking time. The archived HW2 metadata records whole-arm loop time only; do not infer a measured stage-time split from it. Mark that split unavailable where it was not recorded.

## Provenance

The user has resolved the attribution of the HW2 arm A results for positions 1–100 to `llm_rerank.py` SHA-256 `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` on the following evidence:

- `Session 2/README_hw2_dastan.md` explicitly records that full script hash as used for A/B/C and documents the arm A command.
- The script's last-modified timestamp is `2026-11-16 00:59:29.367930457 +0300`. The user identifies the arm A loop as approximately 04:37–06:22 the same day; the saved arm A outputs have last-modified timestamps around `06:22:10 +0300`, consistent with the recorded loop duration of 6296.8 seconds.
- The archived raw-log format matches the script's `structured_block()` representation.
- The script does not record its own source hash in any output. This attribution is accepted documentary and circumstantial provenance, not a run-generated source-hash attestation.

The first 100 contexts in the 200-user run were verified identical to the HW2 baseline contexts, with the same users in the same order: **100/100 identical**. The HW2 arm A responses cover exactly those 100 users, without duplicate users.

**From now on, I record the script SHA-256 next to every LLM run**, along with the model revision, input protocol hash, configuration, and hashes of the relevant input/output artifacts. Preserve original archived files.

The HW2 protocol hash is `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417`; it differs from the 200-user protocol because the cohort differs. Proposed reuse procedure, not yet performed: after context/candidate identity and coverage checks, create a separate derived response file whose copied HW2 rows are rebound to the full 200-user protocol hash, merge with the new second-half rows, and retain a manifest recording source hashes, original protocol hashes, accepted script provenance, and the rebinding. Never edit the original responses. Validate all 200 unique users and rankings and score with the starter's error-on-invalid policy.

## Verified setup

The six source files were copied byte-for-byte from Session 2. SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `starter.py` | `c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24` |
| `extensions.py` | `c80ddbe27846d2f0ca49ce4a66365f4951db2a226b141f5ce1b3b3fdc94114a9` |
| `test_starter.py` | `a3a86f98d67f2416a99b1ea70e495ab3b82b3a1e5a8f4a908f0a6bae8e53d1c1` |
| `llm_rerank.py` | `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` |
| `llm_rerank_c2.py` | `0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada` |
| `requirements.txt` | `9b6ea5637de959cbf5474378f0c538a74bc9103b6ec8e0687e888cf090bc9510` |

Reused the Session 2 virtual environment by absolute path: Python 3.14.4; torch 2.11.0+cpu; transformers 4.57.6; accelerate 1.15.0; huggingface_hub 0.36.2. The pinned model snapshot exists in the local Hugging Face cache. Unit tests: 58 tests, OK. No new LLM inference was performed during this setup.
