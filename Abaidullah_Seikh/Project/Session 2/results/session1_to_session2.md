# Session 1 → Session 2: RQ1 continuity and protocol changes

**Abaidullah Seikh — Team 8 — FAR-Trans — LLM4Rec, HSE University**

Source for Session 1 claims: `reference/seikh_abaidullah_session1_report.pdf`, extracted read-only with `pdftotext -layout` to `results/session1_report_extracted.txt`. Original and reference-copy SHA-256 both equal `451cfc7f4705340e7dfa86939fd837a5ac76024ae95efa347ea64db2b83f9913`. Quotations below preserve extracted wording, with line wrapping normalized. These are historical proposals, not adopted Session 2 settings or independently revalidated literature claims.

Session 2 facts come from the inspected starter, `llm_rerank.py`, official homework, project milestones, saved baseline outputs, and local environment/model checks. The selected pipeline is **Madlyn's shared reranker**, not the instructor's optional ranker. No A/B/C run or effect estimate exists yet.

## Kept from Session 1

| Item | Session 1 source | Where it appears in Session 2 |
|---|---|---|
| RQ1: summaries versus structured history for sparse users | §1.1; Table 3 row 1 | A versus C implemented as different Investor information blocks in `llm_rerank.py`; effectiveness remains untested |
| A structured, B deterministic text, C generated summary | §3.1; Table 3 rows 4–6 | `structured_block()`, `history_block()`, `summary_prompt()` and the `--arm` branch |
| B versus C as a summary-step control | §3.1, §3.3, §5.4 | C summarizes exactly the history text produced for B; shared `rank_prompt()` |
| Sparse means 1–5 earlier Buy transactions | §1.1; Table 3 row 2; §5.4 | output-only subgroup inspection using `sum(buy_count)`; 65 users, 2 nonempty. It is not a cohort-selection option in the shared script |
| Future-purchase nDCG@10 and ten distinct ISINs | Table 3 row 7; §4.2 | `starter.ndcg10()`, `validate_ranking()`, response evaluation |
| Shared candidate pool and ranking stage across arms | §3.1; §4.1 | saved starter CBF top-50, shared `rank_prompt()`, same numbered candidate order |
| ISIN identifiers, not asset names | §3.3; Table 3 row 6 | `history_block()` and `rank_prompt()` omit names, although contexts retain them |
| Exclude risk/capacity from RQ1 | §3.3; §5.4 | A/B/C ranker receives no profile; only separate Arm D incorporates profile through summaries |
| Past-only facts and no invented returns | §3.2–3.4; Table 3 row 11 | starter as-of filtering; `assert_no_future()`, `SUMMARY_SYSTEM`, `RANK_SYSTEM` |
| Cost/error/provenance awareness | Table 3 rows 8–9; §4.3 | planned `raw_log.jsonl`, `responses.jsonl`, `run_meta.json`; actual baseline timing is external. Token/cost accounting is not implemented in this script |
| Literature motivation and bounded interpretation | §2; references [1]–[5] | retained as rationale, not evidence that this reranker improves RQ1 or as directly comparable benchmarks |

## Changed in Session 2

“Team decision” denotes the selected shared implementation or user-stated current plan, rather than an independently observed team meeting. “Starter” denotes the required teaching protocol. Any future implementation or unspecified setting is labeled unverified.

| Session 1 plan (section) | Session 2 implementation verified here | Reason |
|---|---|---|
| GPT-6 Astra or DeepSeek primary summary model; optional GLM (§3.2; Table 3 row 5) | Qwen/Qwen3-1.7B snapshot/config/tokenizer verified at `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`; no inference. Current script still defaults to Qwen2.5 and requires explicit override | **team decision** to use a shared open-weight model; official HW2 requires runnable open-weight inference |
| Frozen mxbai text encoder, fitted numeric adapter, shared item vectors and cosine ranking (§3.1, §3.3; Table 3 rows 4–6) | Madlyn's LLM reranker over starter fixed CBF top-50; same `rank_prompt()` for A/B/C, only Investor information differs. No encoder training or numeric adapter | **team decision** on shared reranker; **starter** candidate/evaluation seam |
| May 31, 2022 inclusive history; June–November 2022 future labels (§3.1, §4.1) | Inputs strictly before June 1, 2021; labels June 1–30, 2021, ending July 1 exclusive | **starter**, mandated HW2 defaults replace unofficial split |
| Sparse cohort as primary evaluation population (§1.1; Table 3 row 2) | All 100 deterministic warm users retained; 65 satisfy 1–5 retained eligible historical Buys, of whom only 2 have future labels. Sparse subgroup analysis is not yet an arm result | **starter** full matched teaching cohort; sparse remains RQ1 subgroup |
| Sell events retained in all arms (§3.3; Table 3 row 2; §5.4) | Contexts and shared A/B/C inputs are Buy-only. Sells occur only in the separate latest_buy_or_sell baseline | **starter** context constraint; not a test of Sell-aware representations |
| Chronological date/Buy-Sell/ISIN event text (§3.3) | B/C history is aggregated per asset, descending Buy count then ISIN; cutoff header but no transaction dates or recency. Asset metadata dates are not event dates | **starter** context schema and **team decision** to use it directly; unlike the optional instructor ranker, this pipeline does not add dated events |
| A: counts, recency, categorical shares, optional amount/unit summaries by direction/ISIN with missing indicators (Table 3 row 4) | Current provisional A: total Buys, distinct assets, count of repeated assets, Buy-weighted top-five assetCategory/assetSubCategory/marketID counts, missing categorical tokens as unknown. No recency, amounts, Sell direction, sector/industry aggregates, fitted adapter, or explicit missing masks. Task 2 fix pending, **unverified** | **team decision** provisional implementation; **starter** lacks event dates/amounts in contexts |
| Common fact table and shared history cap (§3.1, §3.3; Table 3 row 6) | A currently uses all history; B/C use first 20 distinct assets. One full-cohort user exceeds cap; no sparse user can. Corrected parity is **unverified** | **team decision** current cap; provisional A requires review before controlled inference |
| Missing sector/industry written explicitly unknown (§3.3) | Starter omits missing tokens; B/C show only supplied attribute tokens. A uses unknown for missing aggregate categories. No external imputation | **starter** tokenization plus **team decision** serialization |
| Adapter seeds 42, 2026, 3407; US$50 and 48 GPU-hour pilot (Table 3 row 9; §4.3) | No adapter; script default torch seed 0, greedy `do_sample=False`, default 120 summary/60 rank token limits. Actual flags **to confirm with Madlyn**. No monetary, energy, or arm generation cost measured | **team decision** shared CPU pipeline; old training/API budget is not a verified HW2 budget |
| Same frozen B/C encoder; text representation comparison (§3.1; §2.4) | B/C now compare direct history versus generated summary **inside an LLM ranking prompt**, not a frozen embedding encoder | **team decision** changes the scientific estimand; conclusions must name this reranker |
| Model revisions/settings recorded (§3.2–3.3) | Model pinned locally; current script hash differs from supplied team hash, and `enable_thinking=False` is missing. Revised script and thinking-off match **unverified/pending** | Reproducibility check; replacement file expected from Madlyn, no unauthorized patch |
| S2 evaluator/baselines, S3 text/LLM arms, S4 paired uncertainty/report (Table 3 row 10) | `project_FKN.md` §5: S2 implementation/baselines plus minimal selected LLM method; S3 main comparison/ablations/error analysis; S4 reproducible results/presentation. Here tests/baselines/setup completed; A/B/C inference still pending | Course milestones and official HW2 require actual model implementation/comparison; setup alone is not a completed HW2 method result |

## What HW2 can and cannot answer about RQ1

The retained question is whether C improves on A for sparse histories; B controls for deterministic textual presentation. In Session 2, this can only be tested as a **prompt-representation comparison within the shared LLM reranker**, conditional on the starter's fixed CBF candidates, Buy-only aggregated histories, and short teaching window. It cannot validate the original mxbai/cosine/adapter design, Sell-aware chronological summaries, investment suitability, returns, or causal product value.

The baseline sample contains **100 users, 11 nonempty and 89 empty truth**. The sparse subgroup is **65 users, only 2 nonempty and 63 empty truth**. Under the starter's zero policy, a sparse all-user mean will equal the sparse nonempty mean multiplied by 2/65 if the same users are retained. Thus evidence about RQ1 is concentrated in just two labeled sparse users. Any future improvement here is a narrow demonstration, not robust evidence of a general sparse-user benefit. Do not drop empty truth or invalid generations to improve the mean.

There are **18 distinct future user–asset labels** across the full cohort. The team-provided candidate coverage **6/18 is unverified under the outputs-only restriction**: contexts expose candidates but not truth IDs, while per-user scores expose only label counts and nDCG@10. If that reference is later independently verified, the other labels would be unreachable by any reranker confined to the pool; no such coverage measurement is claimed here. Sparse-user candidate coverage is likewise unverified.

No C-minus-A or C-minus-B estimate, arm runtime, invalid rate, summary factuality result, or statistical uncertainty is available. Before interpreting a future comparison, the replacement shared file, thinking-off setting, actual flags and provisional A definition must be recorded. The cap discrepancy affects one full-cohort user and should be resolved or explicitly disclosed. These are observed setup issues, not invented method results.

## Exact Session 1 quotations

### §1.1 — RQ1 and arm roles

> 1.1 Individual research question (RQ1). Does using LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?
> Structured features (A) are my baseline and summaries (C) the intervention. The common outcome is future purchase nDCG@10 for the same users. Following the team discussion, sparse means 1 to 5 Buy transactions in the permitted history; earlier Sell transactions remain eligible as inputs. This tests history representation, not investment advice.

### §3.1 — matched arm definitions

> 3.1 Matched representation comparison. I propose a common timestamped fact table F(u,t) for each user u and prediction cutoff t. For the provisional May 31, 2022 boundary, historical transactions through that date are inputs and June 1 to November 30 purchases are future labels; this split remains unofficial until the instructor specifies the benchmark. As-of asset metadata joins must likewise exclude later revisions. Arm A aggregates matched facts into numeric counts, recency, categorical shares and optional amounts. Arm B serializes these facts into deterministic text. Arm C summarizes exactly the B text using the chosen LLM, without customer profile fields. The eligible assets, item vectors, ranking function and training labels are shared. Numeric A requires a fitted adapter to the common item space; B and C use the same frozen text encoder. Hence A versus C is a pipeline comparison, while B versus C better isolates summarization.

### §3.3 — information parity and text definition

> 3.3 Information parity and model controls. The working text template has one line per event in chronological order: date | Buy/Sell | ISIN | category / subcategory | sector: value | industry: value. Missing sector or industry is written as "unknown". ISIN identifiers are proposed instead of asset names to reduce reliance on pretrained company knowledge, although this does not remove that risk. Sell events are included in all three arms. The treatment of monetary value, units, channel, market ID and maximum history length must be fixed before the experiment; a historical field used in one arm must also be available to the others. B and C use the same frozen text encoder, item embeddings and cosine ranking; A maps its structured features to the common item space. Customer risk and investment capacity are excluded from RQ1. I will document the prompt, input cap, model revision, decoding settings and seed where applicable.

### Table 3, row 2 — population

> Primary: eligible users with 1–5 historical Buy transactions (team agreed). Sell events remain valid historical inputs. Use the instructor cohort when released; 0 Buy and higher-activity groups are secondary only if eligibility permits.

### Table 3, rows 4–6 — A, C, B

**Row 4, Baseline:**

> A: time valid counts, recency, categorical shares and optional amount/unit summaries by direction and ISIN, with missing indicators. Numeric user adapter into shared item space; popularity is diagnostic, not the matched main comparator.

**Row 5, Proposed method:**

> C: I will choose one primary summary model before test evaluation: OpenAI GPT-6 Astra (gpt-6-astra) or DeepSeek V4.1 Flash (deepseek-flash). Its output is encoded by a frozen mxbai-embed-large-v1 checkpoint. All arms share item vectors and cosine ranking. The other model and GLM-5.3 Flash are optional robustness checks.

**Row 6, Controls and ablation:**

> B: deterministic chronological text with ISIN identifiers, no asset names, and missing values shown as unknown. B and C share the frozen encoder, item embeddings and ranker. Fix the monetary fields and history cap before testing. Compare C with B to examine the summary step.

### Table 3, row 7 — primary metric

> One Top 10 ranked list of distinct ISINs per eligible user; relevant items are distinct ISINs bought in the subsequent window. Report matched mean nDCG@10 and C minus A.

### Table 3, row 9 — seeds, repeats, cost

> Proposed adapter seeds: 42, 2026, 3407. Cache fixed input and summaries; log API model, served revision, supported settings, token usage and cost. Planning pilot: 100 histories, US$50 and 48 GPU hours. Choose the primary model on development feasibility, not test performance. No costs or model results have been measured.

### Table 3, row 10 — four-session plan

> S1: source record, literature and design. S2: chronological evaluator and structured baselines. S3: text and LLM arms with factuality audit. S4: paired evaluation, uncertainty and report.

### §5.4 — team discussion and individual position

> The November 8 to 10 team discussion considered structured features (A), deterministic history text (B), generated summaries (C), direct LLM ranking, history length analysis and customer profile information. I proposed the sparse history A versus C comparison with a common item space. Rustam proposed RQ2, comparing B with C while holding the text encoder, item vectors and ranker fixed. Madlyn's separate primary question is RQ4, studying the addition of customer risk level and investment capacity. I treat that as one distinct question, not part of my history representation experiment. History length remains a possible subgroup analysis within RQ1. These are discussion outcomes and proposals, not empirical results.
>
> The team agreed to define sparse users by 1 to 5 historical Buy events and to retain Sell events as history input. Rustam and Madlyn supported a common frozen text encoder, item embeddings and ranker for B and C. Rustam proposed May 31, 2022 as a provisional cutoff and ISIN identifiers rather than asset names; the official split and full text schema remain unconfirmed. We initially discussed a single shared summary model, but later agreed that each member may propose a different model and report its settings. I originally favored DeepSeek, and I now want to assess whether GPT-6 Astra is practical as an alternative for my Arm C. I will choose one before test evaluation and regard the other, and possibly GLM, as optional sensitivity analyses. My primary question remains A versus C, using B as the control.

### References [1]–[5], quoted from the report

> [1] J. Sanz-Cruzado, N. Droukas, and R. McCreadie, “FAR-Trans: An Investment Dataset for Financial Asset Recommendation,” IJCAI-24 Workshop on Recommender Systems in Finance (Fin-RecSys), Jeju, South Korea, 2024. [Online]. Available: https://arxiv.org/abs/2407.08692

> [2] F. Spadea and O. Seneviratne, “Aligning Language Models with Investor and Market Behavior for Financial Recommendations,” in Proc. 6th ACM International Conference on AI in Finance (ICAIF), pp. 509–517, 2025. doi: 10.1145/3768292.3770399. [Online]. Available: https://arxiv.org/abs/2510.15993

> [3] J. Ramos, H. A. Rahmani, X. Wang, X. Fu, and A. Lipani, “Transparent and Scrutable Recommendations Using Natural Language User Profiles,” in Proc. 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 13971–13984, 2024. doi: 10.18653/v1/2024.acl-long.753

> [4] Z. Gao, J. Zhou, Y. Dai, and T. Joachims, “LangPTune: Optimizing Language-based User Profiles for Recommendation,” in Proc. 34th ACM International Conference on Information and Knowledge Management (CIKM), pp. 707–717, 2025. doi: 10.1145/3746252.3761369. Reported v2 manuscript results refer to “End-to-end Training for Recommendation with Language-based User Profiles,” arXiv:2410.18870v2, Feb. 2025: https://arxiv.org/abs/2410.18870

> [5] J. Sanz-Cruzado, R. McCreadie, N. Droukas, C. Macdonald, and I. Ounis, “Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations,” ACM Transactions on Information Systems, vol. 44, no. 2, art. 51, 2026. doi: 10.1145/3780097.

The report's §2 uses [1] for the dataset/classical benchmark, [2] for same-domain LLM context, [3]–[4] for language user profiles, and [5] to distinguish purchase accuracy from profitability. This session did not fetch or independently validate these papers or transfer their scores into the HW2 results.
