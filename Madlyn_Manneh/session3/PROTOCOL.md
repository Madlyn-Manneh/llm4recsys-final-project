# HW3 development protocol (RQ4)

Madlyn Manneh, team Eight(8) (registered name to be confirmed). Written before any HW3 model run. These are development settings, not official benchmark settings.

## Question
Does adding risk level and investment capacity to an LLM-generated history summary change nDCG@10 compared with a summary of the history only (arm D against arm C)? LLM role: both. The summary step turns the purchase history into LLM-written text (encoder-like), and the ranker reranks the starter's fixed top-50 CBF candidates using that text. Their contributions are separated with arm B and the CBF control (see Arms).

## Development sample
- Starter selection rule: warm users (with history before the cutoff), ordered by sha256("42:" + customerID), first N.
- Primary sample: N = 100, the HW2 sample. Protocol hash expected from "python starter.py run --data-dir data/FAR-Trans --output-dir <dir>" on this data: 50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417
- Declared extension: N = 200, i.e. users 101 to 200 added, run only if time allows and only for all four arms. Protocol hash expected from the same command with --max-users 200: d46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697
- Primary and extension results are both reported. Pooled 200-user results are reported only if every arm completes on all 200 users. Which one is reported is not chosen after seeing results.
- HW2 outputs for the first 100 users are reused only if llm_rerank.py has the hash below and their contexts are identical in the 200-user starter run.
- Cutoff 2021-06-01. Label window: the following 30 days. Repeat purchases allowed. Top-50 candidates. Users with no future purchases count as zero.

## Model and generation settings
- Qwen/Qwen3-1.7B, revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e, thinking off, greedy decoding, seed 0.
- At most 120 summary tokens and 60 ranking tokens. float32 on CPU.
- llm_rerank.py SHA-256 for arms B, C and D: D7A34C1F9F715D7437CA5B2CC7989DBFF12348602495B8A427CF8E56FA7007BA
- Only the "Investor information" block of the ranking prompt differs between arms.

## Arms
- CBF: the starter's CBF order, the initial candidate order (matched control for the ranker).
- B: same ranker and candidates, raw history instead of the LLM summary. B against CBF gives the ranker's contribution. C against B gives the summary's contribution.
- C: summary of the purchase history only.
- D: summary plus risk level and investment capacity. A profile whose questionnaire date is on or after the cutoff reads "not available at the cutoff". D against C gives the profile's contribution.
- E (the one ablation): as D, but each user receives another user's profile. The assignment is a deterministic permutation with seed 0 in which no user keeps their own profile, among users with a profile available at the cutoff. Users with no available profile keep the "not available at the cutoff" text. The mapping is saved to a file and hashed before any run.

## Metrics and controls
- Primary: mean nDCG@10 over all evaluated users. Also the mean over users with future purchases, with their count. Four decimals.
- Baselines: Popularity, CBF, Latest buy, Latest buy or sell.
- Provided LLM comparison: the far-trans-llm rows (original-text TF-IDF CBF, LLM-Rec-inspired encoder, LLMRank with fallback), reported with their different hardware, settings and candidate pools stated.
- Paired differences reported: D minus C, E minus D, C minus B, B minus CBF.

## Rules
- Same users, cutoff, candidates and evaluation rules for every method.
- Invalid outputs, repairs and fallbacks are recorded.
- The official evaluation set is not used to choose or tune anything.
- A change to this file after a run starts is added as a dated amendment, not an overwrite.

## Amendment 1 (before any HW3 model run)
- Arm E is run with llm_rerank_hw3.py, a copy of llm_rerank.py with only arm E added. make_hw3.py builds it and checks the source hash first. llm_rerank_hw3.py SHA-256: 7D31585F30AA14D3BF648B856F39BA8499E97389C58CF204BBC47BECF390D869. Arms B, C and D keep using llm_rerank.py.
- On the mock backend, llm_rerank.py and llm_rerank_hw3.py give byte-identical outputs for arms B, C and D.
- The arm E shuffle is a seeded cyclic permutation (seed 0) within each starter run directory: primary users 1 to 100, and users 101 to 200 as a separate run if the extension is run. Primary E results therefore do not depend on the extension.
- Primary sample: 87 users have a profile available at the cutoff and none keeps their own. The expected SHA-256 of profile_shuffle_map.json is D2D1020EACF3EB2E1E8FD56D08242A5D9632E5E12F511B283DD290D734FAB702.
- For 10 of those 87 users the donor's profile text is identical to their own, so their E prompt equals their D prompt by construction. E is reported for all 87 and for the 77 whose prompt changed.
