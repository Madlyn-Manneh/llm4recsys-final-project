# Task 3b commit-content audit (local preparation only)

No files were staged or committed. Only the five paths below are proposed.

Checked against all 29090 distinct raw customer IDs found in the original customer and transaction CSVs, plus complete instantiated prompts, source-history blocks, summaries, and ranking outputs from all 300 full-run raw-log records.

| Proposed file | Raw customer ID matches | Saved instantiated text matches | SHA-256 |
|---|---:|---:|---|
| `llm_rerank.py` | 0 | 0 | `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da` |
| `requirements.txt` | 0 | 0 | `9b6ea5637de959cbf5474378f0c538a74bc9103b6ec8e0687e888cf090bc9510` |
| `README_hw2_dastan.md` | 0 | 0 | `c738cf3874a81526f1ec45bb579488c9e9d7565d5001921e8eaa6e1a78e13c80` |
| `results/results_table.md` | 0 | 0 | `c5db7edcfbd22a29a3c014530343811c01361b822fbb35ef6e0c30ecdc97bb6a` |
| `results/task3_analysis_aggregate.md` | 0 | 0 | `c97c00ae35eb629ed28a42977585d130fb3d0b829f57f741b4c7b6fd64859cb3` |

## Literal prompt-text policy

`llm_rerank.py` contains the static `RANK_SYSTEM` and `SUMMARY_SYSTEM` source templates and prompt-building functions, as required to keep inference reproducible. Thus a literal rule prohibiting all prompt text, including source templates, does not pass for that file. No generated/customer-instantiated prompts or raw customer IDs occur in any allowlisted file. The source was not modified to conceal or remove templates. Confirm whether source-code templates are permitted before committing.

## Local-only exclusions

`outputs/` (all prompts, summaries, responses, predictions, metrics with IDs, protocol users and logs); `.venv/`; data/model files; `reference/`; old/original script copies unless separately requested; `results/task1_setup.md`; `results/task2_smoke.md`; `results/task3_runs.md`; `results/task3_analysis.md`; `results/task3_tokens_per_user_LOCAL.csv`; `results/session1_to_session2.md`; `results/session1_report_extracted.txt`; local analysis/inspection helpers and session exports. The explicit allowlist avoids accidentally staging these; existing ignore rules alone are insufficient for local result notes.

Repository availability is checked separately. No repository, remote, commit or staging area is created by this audit.
