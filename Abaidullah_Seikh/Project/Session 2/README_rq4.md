# Shared team pipeline: arms A, B, C, D (CPU only, 16 GB RAM is enough)

All arms use the same ranking step (top-50 starter candidates, ten numbers out).
Only the "Investor information" block changes:
  A structured counts (PROVISIONAL, confirm with the RQ1 owner) | B raw history text
  C LLM summary                                                 | D LLM summary + profile (RQ4)

Setup (once; copy llm_rerank.py next to starter.py):
    python3 -m venv .venv && source .venv/bin/activate
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    pip install transformers accelerate

1. Baselines + shared contexts (all four provided baselines):
    python3 starter.py run --data-dir DATA --output-dir outputs/baseline

2. Smoke test, 3 users (keep the exact HF commit hash you use in --revision):
    python3 llm_rerank.py --run-dir outputs/baseline --data-dir DATA --arm D \
        --model Qwen/Qwen2.5-1.5B-Instruct --revision <commit> --max-users 3 \
        --out-dir outputs/smoke_D

3. Full arms, identical settings (only --arm changes). Needed for RQ4: C and D.
    python3 llm_rerank.py --run-dir outputs/baseline --data-dir DATA --arm C --model ... --revision <commit> --out-dir outputs/arm_C
    python3 llm_rerank.py --run-dir outputs/baseline --data-dir DATA --arm D --model ... --revision <commit> --out-dir outputs/arm_D

4. Score each arm with the starter (same flags as step 1, so protocol_hash matches):
    python3 starter.py run --data-dir DATA --output-dir outputs/arm_C_eval --stage ranker --responses outputs/arm_C/responses.jsonl --on-invalid fallback
    python3 starter.py run --data-dir DATA --output-dir outputs/arm_D_eval --stage ranker --responses outputs/arm_D/responses.jsonl --on-invalid fallback

Do not use `starter.py export-prompts` for the LLM arms (its prompts contain asset names).
Never report --backend mock outputs: they only test the plumbing.
Each arm writes run_meta.json (model, commit, settings, hardware, whole-arm wall time)
and raw_log.jsonl (every prompt and output) for the report and the verification check.
