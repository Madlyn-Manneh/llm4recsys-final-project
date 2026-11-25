# HW3 Protocol — Amendment 1
Written: 2026-11-23T12:39:14+03:00. Written after both runs finished (A 101–200 at 2026-11-22 21:38, C 200 at 2026-11-23 03:28) and before any of their outputs were scored or inspected.
Decision made earlier: proposed to the team in the team chat on 2026-11-22 at about 20:30 MSK, before any 200-user output of the fact-preserving summary existed. Team confirmation: pending.
Base protocol: HW3_PROTOCOL.md, SHA-256 427e05eea001910c4c1f02169915ee5efbc27b5b5463fa0fdceb824ecd3c2146 (unchanged).
## Change
- Team arm C = fact-preserving summary (llm_rerank_c2.py, SHA-256 0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada). Output: outputs/arm_C2_200.
- The earlier team summary (llm_rerank.py, arm C) becomes the ablation "old C", reported on users 1–100 (Session 2 rows) and on the sparse window.
- Main comparison: C vs A. Everything else in HW3_PROTOCOL.md is unchanged.
## Reason
In Session 2 the old summary dropped exact facts (asset IDs kept 17/58 vs 56/58; repeats named 5/10 vs 9/10). Session 2 sparse results (new vs old, 6/19/5 better/same/worse) were seen before this decision and are disclosed.
