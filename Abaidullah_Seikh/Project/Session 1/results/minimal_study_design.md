# Minimal study design — Task 3

**Student:** Abaidullah Seikh  
**Course:** LLM4Rec, HSE University  
**Dataset:** FAR-Trans  
**Status:** Proposed design for review. No model training or recommendation experiment has been performed.

## One primary RQ

**RQ1:** Do LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?

In the professor's template: **We test whether LLM-generated transaction-history summaries improve future-purchase nDCG@10 over structured-history features for FAR-Trans users with provisionally 1–5 pre-cutoff Buy events.** This restates the same question; B and subgroup analyses are controls, not additional primary RQs.

## Complete 12-field table

The twelve fields below correspond to §8 of `session1_research_question_instructions (2).md`; labels follow the user's Task 3 wording (the instructions spell “Seeds, repeats and cost” as “Seeds, repeats, cost”). All numerical settings are proposed unless explicitly labelled Task 1 observations or published evidence. Full operational details are in [evaluation_plan.md](evaluation_plan.md).

| Field | Concrete proposal and present status |
|---|---|
| RQ and scope | Primary contrast **C minus A** on sparse-user nDCG@10. Change the historical user representation while holding permissible source facts, evaluated instances, candidates, item vectors, scoring function and label windows constant. B is an attribution control. Scope is offline future-purchase ranking; no profitability, suitability, personal financial advice, live trading or causal business-outcome claim. |
| Evaluated users and subgroups | Use the instructor's evaluated users when announced; export Top-10 for every required user. Primary subgroup: **1–5 Buy events before each cutoff**, counted over the full permitted historical window, not future outcomes. Auxiliary non-overlapping bands: 0 Buys (split true zero-history from sell-only), 6–10 light, >10 heavy; 1–3 and 1–10 are overlapping sensitivity bands. Eligibility and subgroup membership are identical across arms. Task 1's full-release median 2 Buys and 23,663 users with 1–5 Buys motivate, but do not populate, the provisional subgroup. |
| Data fields used | `transactions.csv`: `customerID` for joins, `ISIN` for asset joins/aliases, `transactionID` plus original record index for audit, `transactionType`, `timestamp`, `totalValue`, `units` for a shared historical fact table. `asset_information.csv`: `ISIN`, `assetCategory`, `assetSubCategory`, `sector`, `industry`, `timestamp` for as-of descriptive features and candidate vectors. Raw names, original customer/transaction identifiers, channel and market are excluded from **all model inputs** in the primary design. Profiles, questionnaire fields, close prices and full-series profitability are excluded from all arms. The complete authentic nine-field record and matching metadata are preserved below, including fields not used by the model. |
| Baseline(s) | **A:** numerical/categorical vector of the shared per-asset, Buy/Sell history aggregates: counts, within-type category distributions, first/last-event recency, total/mean recorded value and per-asset units, with missing indicators and training-only scaling. A linear user adapter maps to the common item-embedding dimension. Retain all fields in the shared fact table; no extra raw-event access for C. A training-only popularity ranking is an additional diagnostic, not the information-matched primary comparator. |
| Proposed method | **C:** frozen `Qwen/Qwen3-1.7B`, non-thinking mode, generates up to **256 new tokens per fact-table chunk**; summarize only supplied facts. Encode summaries with frozen `mixedbread-ai/mxbai-embed-large-v1`, then train a linear user adapter. Use the identical frozen item embeddings and parameter-free cosine scoring used by A. Model revisions/tokenizer/runtime hashes will be pinned before the pilot; none has been run. |
| Ablations and controls | Include **B**, deterministic text of exactly the same historical fact table, encoded with the same frozen text encoder and linear adapter architecture as C. B-versus-A tests the text-encoding package; C-versus-B tests adding generated compression/abstraction, with remaining length effects disclosed. Share source-field manifests, candidate/label hashes, as-of joins, item vectors, training examples, optimization budget and scoring formula. User adapters are fitted separately; report parameter counts and pretrained-encoder asymmetry. No claim of identical full-model weights. |
| Primary metric | **nDCG@10 against distinct future purchased assets**, with Top-10 ranked lists and paired C-minus-A effects on the fixed sparse cohort. Proposed binary gains and `[cutoff, window_end)` labels; history strictly before cutoff. Per-cutoff user macro-average, then equal average across cutoffs for the RQ, plus the official benchmark aggregation separately if different. Empty-label and repeat-purchase handling require instructor confirmation; provisional rules and denominators are explicit in the evaluation plan. |
| Secondary metrics | Recall@10, catalog coverage@10, cohort/candidate/label coverage, non-sparse and sensitivity-band nDCG@10, B contrasts, factual-error/omission audit, generation-failure rate, input/output tokens and latency/cost. No ROI metric is planned for this four-session behavioral-prediction question. These are diagnostic outcomes, not replacements for the shared primary metric. |
| Seeds, repeats and cost | **42, 2026, 3407** for three matched adapter-training runs per arm; one cached greedy C generation per history, reused across runs. Fixed prompt, `enable_thinking=False`, `do_sample=False`, 256-token output cap; sampling temperature/top-p/top-k inactive. Start with **100 historical development snapshots**, not final test users selected by outcomes. Planning estimate: **0.5–2 GPU-hours pilot; 8–32 GPU-hours main generation/embedding/training plus 2–6 CPU-hours preparation/analysis**, conditional on one 24-GB GPU and the actual protocol size. Ceiling **US$50 and 48 GPU-hours total**, including pilot/retries; stop at either ceiling and reassess scope transparently. Log actual time, tokens, hardware, failures and charges. No measured costs yet. |
| Feasibility in four sessions | **S1:** inspection, genuine record, AI-assisted literature review completed; this design is proposed for student review. **S2:** build/test configurable chronological evaluator, freeze confirmed protocol, implement A and popularity, pilot encoders on development only. **S3:** cache C summaries and B text, run controlled A/B/C comparison and factuality checks. **S4:** complete three-seed runs, paired uncertainty, sensitivity/error analysis, reproducibility and student-authored reporting. No LLM fine-tuning or multi-model search is planned. |
| Ethical and leakage risks | Keep anonymized records local; do not re-identify or link to outside identities. Remove original identifiers/names from prompts, preserve missingness, prohibit invented preferences and use fact checks plus human review. Filter events/metadata at every historical origin; never use future prices or complete-release sparse counts. Reconstructed buys and adjusted values are release-level provenance limitations, not certain observed decisions. Exclude predicted/stale customer profiles; keep repeated transaction IDs unless a valid composite-key issue is demonstrated. Record pretrained-model contamination uncertainty and evaluate by time period for market-regime shifts. See the risk-to-action table in the evaluation plan. |
| Current state | Completed: dataset inspection, data-quality/sparsity analysis, genuine transaction and asset verification (student confirms independent terminal check), AI-assisted five-paper review and preliminary gap. Proposed here: arguments and study design. Not completed: official protocol, trained A baseline, C/B experiments, A-versus-C measurement, runtime/budget measurement, confirmed personal verification of all papers. **Next task:** implement a read-only, configurable history/candidate/label builder with boundary/as-of/parity tests, then connect it to the instructor's announced protocol before training. |

## Exact personally verified data example

**Verification provenance:** the student states that they independently checked this transaction and asset metadata against the original CSVs using Linux terminal commands. Task 3 also rechecked the raw lines with AI assistance. This does not establish personal verification of the papers or every computed statistic.

**Source:** `FAR-Trans/transactions.csv`  
**transactionID:** `7590224`  
**Location:** physical line **2**, CSV record **2** including header, data record **1** excluding header.  
**Window/split:** **unassigned**, because the instructor's cutoff/window and eligibility rules are pending.  
**Timestamp:** `2020-03-27`, date only; no intraday time or timezone is supplied.

```csv
customerID,ISIN,transactionID,transactionType,timestamp,totalValue,units,channel,marketID
00017496858921195E5A,GRS434003000,7590224,Buy,2020-03-27,11000.0,5000.0,Internet Banking,XATH
```

**Matching source:** `FAR-Trans/asset_information.csv`  
**Join:** exact `ISIN = GRS434003000`; one matching row in the inspected release.  
**Location:** physical line **338**, CSV record **338** including header, data record **337** excluding header.

```csv
ISIN,assetName,assetShortName,assetCategory,assetSubCategory,marketID,sector,industry,timestamp
GRS434003000,PPC SA,ΔΕΗ,Stock,Large Cap,XATH,Utilities,Utilities - Renewable,2018-01-02
```

### Observed, predicted/estimated and missing information

| Information | Classification and timing | Treatment |
|---|---|---|
| Transaction identifiers, Buy type, timestamp, channel and market | Observed **values in the released file**, not inferred values. No field in this example is blank. | Audit exact strings. Use original identifiers only locally for joins; map ISIN to an opaque alias for model inputs. |
| `totalValue = 11000.0`, `units = 5000.0` | Recorded release values. FAR-Trans §3.3 describes value estimation from closing prices and split-adjusted units; these must not be called untouched observed execution quantities. | Preserve raw spellings in the example; model fields are explicitly “recorded value/units,” not proof of wealth or conviction. |
| Asset category, subcategory, sector and industry | Recorded descriptive fields, none missing in this matching row; last-update stamp `2018-01-02`. | Use only an allowed as-of snapshot. This timestamp predates the example transaction but does not assign it to a split or prove every attribute was archived then. |
| Customer risk, capacity and questionnaire answers | **Not used or inferred.** In the wider release, `Predicted_` labels are estimates, `Not_Available` denotes missingness, and questionnaire text contains no answers. | Exclude the complete customer-profile table from the primary comparison. No risk classification is attached to this customer. |
| Reconstruction status | Unknown for this row: the release contains reconstructed transactions but has no per-row reconstruction flag. | Do not call this particular Buy reconstructed or definitely contemporaneously observed. Record the dataset limitation and the sensitivity policy below. |

The exact record is an audit example, not the customer's complete historical input, a recommendation or an invented LLM summary. Recency cannot be computed for it until a cutoff is specified.

## Baseline, proposed method and control

All arms start with **one deterministic fact table `F(u,t)`** computed from the same permitted pre-cutoff transactions. It aggregates each asset alias and Buy/Sell type into event count, first/last age in days, total/mean recorded value, total/mean units, and as-of category/subcategory/sector/industry. Totals, distinct-asset counts, missing indicators and category shares are included. No raw chronology or profile information is supplied only to C. This bounds the experiment to summaries of a common structured history fact table, rather than allowing C a richer raw event sequence than A.

- **A:** structured numeric/categorical encoding of `F(u,t)` → trainable linear adapter.
- **B:** lossless deterministic text rendering of `F(u,t)` → frozen text encoder → trainable linear adapter.
- **C:** LLM summary of that same text → the same frozen text encoder → trainable linear adapter.
- **Shared scoring:** normalize the adapter output and score its dot product with the **same frozen candidate-item vectors**. The scoring function has no arm-specific learned head. Item descriptions contain only opaque alias and allowed categorical metadata, identically for every arm. Candidate ranking, Top-10 selection and tie-breaking are shared.

A and the text arms have different input spaces and potentially different adapter parameter counts. This is a controlled comparison of **representation pipelines**, not a proof that a pretrained encoder has no effect. B and C have identical encoder/adapter architectures and training budgets, which provides the closer generation-stage control. The official homework's same-ranker requirement is interpreted as a shared downstream scoring function and item representations with documented user-side encoders; this interpretation should be confirmed with the instructor.

## Methodological assumptions needing confirmation

| Choice | Proposed working assumption | Confirmation required |
|---|---|---|
| Temporal split and horizon | A configurable cutoff `t` and end `e`; `timestamp < t` history and `t <= timestamp < e` labels; earlier train/validation labels must mature before subsequent prediction origins. No dates or horizon length are assigned here. | Instructor's date boundaries, windows and allowed training data. |
| Sparse definition | 1–5 historical Buy **events** in the full permitted history; both Buys and Sells contribute facts; report total-history size too. | Whether the instructor specifies a different eligibility/counting rule. |
| Candidate universe | Use official as-of candidates. Development fallback: assets with a metadata row before the cutoff; include previously bought assets unless the official rule excludes them. Never require future trading/price survival. | Official item scope, availability and repeat-purchase policy. |
| Labels and empty outcomes | Distinct Buy ISINs within candidate scope; provisionally average the RQ metric over users with at least one in-scope future Buy, logging all exclusions and producing lists for all required users. | Official relevance, zero-label handling and aggregation. |
| Ranker control | Shared frozen item vectors and identical cosine scoring; separately fitted linear user adapters. | Whether “same downstream ranker” requires a stricter fixed-weight user-side control. |
| Metadata/provenance | Latest permitted snapshot strictly before cutoff; field-level conflicts become missing. Record release-level reconstruction uncertainty. | Whether these fields are allowed and whether source reconstruction flags can be obtained. |
| Resources | Local frozen Qwen3-1.7B and Mxbai inference, 100-snapshot pilot, three seeds, US$50/48-GPU-hour ceiling. | Available hardware, exact checkpoint revisions, actual throughput and permission for any paid compute; these are not measured or authorized purchases. |

## Current state and validation

The design addresses all **12** required §8 fields; the separate research/business paragraphs follow §7. All five academic sources, including FAR-Trans, are linked with primary-source section checks in [research_importance_and_business_value.md](research_importance_and_business_value.md). [evaluation_plan.md](evaluation_plan.md) defines parity, formulas, temporal boundaries, costs and practical safeguards. The proposed threshold and protocol assumptions are labelled; no official split, team agreement, personal paper verification or experimental result is asserted.

**AI-use and authorship:** OpenCode assisted with source checking and drafting. The student must review and personally author the eventual report. No final PDF, trained model or synthetic session history is created in Task 3. Earlier records are preserved as historical artifacts; this file records the student's subsequent genuine-record verification statement without rewriting the past session.
