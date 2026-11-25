# RQ2: test transaction-history summarization

I compare the team's fixed Buy-history text with a Qwen-written summary of the exact same text. The LLM ranks a fixed pool, and a separate LLM call creates the text representation in the summary condition. No model is trained. The matched control for reranking is the original CBF order.

## Development cohort

- The first 200 warm FAR-Trans users in the unchanged course starter's deterministic SHA-256 order (seed 42). History strictly before 2021-06-01; eligible Buy labels in `[2021-06-01, 2021-07-01)`. Repeated purchases are permitted. All 200 users stay in every comparison.
- Use the local starter snapshot from the protocol verification on 24 November. Its full protocol hash is `d46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697`. Freeze the 50 ordered CBF candidates per user rather than relying on the protocol hash alone. The order digest (comma-separated ISINs per user, LF between users, no trailing LF) is `8047bbccbbe66f0bc420df36b06484c4f0888fe18deb8caf0897f1d4903acb04`.
- Report a descriptive sparse subgroup (1–5 eligible pre-cutoff Buys, with the starter's row filters). The shared 200-user teaching sample is primary. Subgroup size and coverage limit the conclusion; the official final-project split is not used.

## Comparisons and ablation

1. **Raw history:** the shared `history_block` over at most 20 historical ISINs, ordered by descending Buy count then ISIN. No Sell, price, profile, asset name or transaction date is added to this comparison.
2. **LLM summary:** the shared summary prompt takes that identical block. Its output replaces the raw block in the same ranker prompt.
3. **Template summary:** replace just the generative summarization step with a deterministic text template. Render total Buys and distinct assets among the visible rows, counts by category and market, and top ISINs with Buy counts. Attribute counts are sorted by frequency then label; retain only complete clauses within 120 tokenizer tokens. These are two choices of summarization procedure, not a pure test of sentence wording alone.

Use the shared `rank_prompt`, the same 50 ordered candidates, Qwen3-1.7B revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, greedy decoding with thinking disabled, at most 120 new summary tokens and 60 new rank tokens. Run all three variants on physical GPU 3 (H100) on JupyterHub, with float32, TF32 disabled and the same batch partition. Use the starter top ten if the output cannot yield ten valid unique candidates. Count repairs separately from fallbacks. Record the model, dependencies, hardware, batch settings and measured times. The original Qwen checkpoint is not quantized.

Report all four unchanged starter baselines (Popularity, CBF, Latest buy, Latest buy or sell), our three variants, and the course's provided LLM ranker. Where matching order for a shared run is unavailable, cite its reported aggregate with that caveat or rerun the supplied ranker prompts and validation on our ordered snapshot. The course ranker intentionally differs in its prompt, inputs and output budget. Keep such a comparison separate from the matched raw/summary intervention.

## Scoring and error analysis

- Mean binary nDCG@10 across all 200 users is primary; users without future Buys contribute zero. Also report the mean and sample size over users with at least one eligible future Buy. Round displayed estimates to four decimals; retain full precision.
- Compare paired per-user results: summary minus raw (primary), template minus raw, and summary minus template. Descriptively inspect improved, worsened and unchanged users; separate missing candidates from failures to rank present candidates, and account for invalid outputs. Report hit coverage and an oracle ceiling for the fixed pool.
- Audit the summary against its actual input for user positions 1, 2, 3, 25, 50, 75, 100, 101, 125, 150, 175 and 200, plus the strongest paired changes. Check omissions and unsupported assertions without treating every omission as hallucination. One new hand-worked check is reserved for the student and is attributed only if performed.
- Separate offline data/model preparation and inference wall time. No claims about investment suitability or benchmark placement follow from development purchase labels.
