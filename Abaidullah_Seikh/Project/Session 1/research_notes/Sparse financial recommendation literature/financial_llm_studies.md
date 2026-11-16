# FLARKO and Conv-FinRe: evidence for Abaidullah Seikh's sparse-history Task 2 RQ

## 1. What does FLARKO establish?

### Takeaway
**FLARKO is the more directly relevant of these two works**, because it evaluates LLM-based financial asset recommendation on FAR-Trans using historical transactions and future acquisitions. Its experiment is KG-grounded recommendation with behavioral/profitability alignment and top-3 hit metrics, not a sparse-user, summary-versus-structured-history nDCG@10 comparison. [Full text, §§3–4, 6–7](https://arxiv.org/html/2510.15993v1)

### Cited Findings

#### Bibliographic metadata, status, and version
- **Fernando Spadea and Oshani Seneviratne (2025). “Aligning Language Models with Investor and Market Behavior for Financial Recommendations.”** Published in **Proceedings of the 6th ACM International Conference on AI in Finance (ICAIF ’25)**, pp. **509–517**, ACM; conference in Singapore, November 15–18, 2025. Publisher-deposited metadata give online publication **November 14, 2025** and print publication **November 15, 2025**. It should not now be described as only an unpublished preprint. [Author full-text title block](https://arxiv.org/html/2510.15993v1); [ACM-deposited Crossref record](https://api.crossref.org/works/10.1145/3768292.3770399)
- **Proceedings DOI: `10.1145/3768292.3770399`.** Separate **arXiv DOI: `10.48550/arXiv.2510.15993`**. arXiv lists only **v1, October 14, 2025, 03:24:20 UTC**. All method/result locators below refer to **arXiv:2510.15993v1**, not an independently compared publisher version of record. [arXiv record](https://arxiv.org/abs/2510.15993); [Crossref](https://api.crossref.org/works/10.1145/3768292.3770399)
- FLARKO expands to **Financial Language-model for Asset Recommendation with Knowledge-graph Optimization**. Both authors are affiliated with Rensselaer Polytechnic Institute. [Abstract/title block](https://arxiv.org/html/2510.15993v1)

#### Actual data, temporal protocol, and population
- **Evaluated dataset: FAR-Trans.** The paper describes transaction histories, asset-price histories, and investor profiles. It does not report a second independently evaluated dataset. Its §6 statement that results should generalize to other markets/datasets is an author expectation, not external validation. [§6](https://arxiv.org/html/2510.15993v1#S6)
- **Training data:** January 2, 2018–November 30, 2021; prompts every four weeks from August 1, 2019–June 1, 2021. **Test data interval:** December 1, 2021–November 29, 2022; test prompts every two weeks from December 1, 2021–June 2, 2022. The subsequent **180 days** supply purchase/profitability labels; the endpoint buffers are explicitly intended to allow label construction. [§6.1](https://arxiv.org/html/2510.15993v1#S6.SS1)
- Context construction filters transactions to dates **before RECOMMENDATION_DATE**, and price-summary intervals must end before that date. §6.1 does not fully resolve whether test PKGs retain all pre-December-2021 history or only transactions in its stated test interval. Do not silently impose the original FAR-Trans paper's full protocol on this separate experiment. [§3.1](https://arxiv.org/html/2510.15993v1#S3.SS1); [§6.1](https://arxiv.org/html/2510.15993v1#S6.SS1)
- Federated experiments simulate **20 clients**, with IID versus synthetic non-IID distributions over customer type (Mass, Premium, Legal Entity, Professional), risk level (Conservative, Moderate, Aggressive), and investment capacity. **23,784 labeled prompt-completion examples**, evenly divided into desirable and undesirable completions, are reported. These are training examples, not a stated number of distinct investors or evaluation instances. [§6.4](https://arxiv.org/html/2510.15993v1#S6.SS4)
- **Sparse/cold subgroup:** no sparse-user cohort, purchase-count cutoff, zero-history user experiment, or sparse-stratified result is defined in §§6–7. The “Nothing” input ablation is context removal from a fine-tuned model, not an established cold-start cohort. [§§6–7](https://arxiv.org/html/2510.15993v1#S6); [Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)

#### Method: structured graph context and trained recommendation, not generated history summaries
- A **Personal Knowledge Graph (PKG)** encodes transaction ISIN, buy/sell type, monetary value, and timestamp. A **Market Knowledge Graph (MKG)** encodes price histories and asset category, sector, and industry. Both are subject–predicate–object graphs serialized in **JSON-LD**. Redundant triples are pruned and the graph pair is capped at **5,000 triples**. [§3.1](https://arxiv.org/html/2510.15993v1#S3.SS1)
- MKG **TenWeekPriceSummary** entities contain period high, low, average, and end prices over **10-week intervals**. This is numeric price aggregation, not an LLM-generated prose summary of a customer's transaction history. [§3.1, MKG Construction and Fig. 3](https://arxiv.org/html/2510.15993v1#S3.SS1)
- The LLM is prompted as a financial analyst, receives PKG/MKG JSON-LD, and returns an introductory sentence plus **three asset ISINs** for the next six months. There is no separate text-summary encoder feeding an otherwise fixed conventional ranker. [§3.2](https://arxiv.org/html/2510.15993v1#S3.SS2)
- **Kahneman–Tversky Optimization (KTO)** fine-tunes the LLM using binary desirable/undesirable completions. A desirable asset must be **purchased in the following 180 days AND yield a positive return** over that horizon. Each prompt yields two training examples, with up to **20 asset recommendations per completion**. This objective differs from optimizing purchase-only nDCG. [§4](https://arxiv.org/html/2510.15993v1#S4)
- Models are **Qwen3-0.6B, 1.7B, 4B, 8B**, with 8B excluded from federation for compute reasons. The paper reports YaRN extension from 32,768 to 131,072 tokens, LoRA rank **16**, alpha **64**, 4-bit quantization, and **3 centralized epochs**. Federation uses **200 rounds**, **3 of 20 clients** per round, **0.1 local epochs**, approximately three epochs per client overall. [§6.5](https://arxiv.org/html/2510.15993v1#S6.SS5)

#### Baselines, information access, and metrics
- **Price-based:** Random Forest, Linear Regression, LightGBM, using asset-price history (described as non-behavioral MKG data). **Behavior-based:** Popularity, LightGCN, ARM, MF, UB kNN, using transaction history (behavioral PKG data). Uniform Random uses neither. These baseline families have different predictors and information sources; the paper does not establish an identical-ranker representation comparison. [§6.2](https://arxiv.org/html/2510.15993v1#S6.SS2); [§7.3](https://arxiv.org/html/2510.15993v1#S7.SS3)
- Input ablations are **Combined (PKG+MKG), PKG, MKG, Nothing**. They change available context; none is a structured-feature versus LLM-prose encoding of exactly the same transaction history. [§7.1, Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)
- Reported metrics are **Pref@3** (hits against future purchased assets), **Prof@3** (hits against profitable assets), and **Comb@3** (hits against their intersection). §6.3 calls these Hits@3/hit-rate variants but does not provide a full denominator/aggregation equation. **No nDCG@10 result is reported.** Do not relabel these numbers precision, nDCG, realized return, or a causal adoption rate. [§6.3](https://arxiv.org/html/2510.15993v1#S6.SS3)

#### Supported numerical results and exact locators

Selected rows of **§7.1, Table 2 (CenFLARKO)**; every value below is reported as **mean ± standard error of a proportion**. [Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)

| Qwen3 model / input | Pref@3 | Prof@3 | Comb@3 |
|---|---:|---:|---:|
| 0.6B / Combined | 0.0354 ± 0.0131 | 0.1010 ± 0.0214 | 0.0152 ± 0.0087 |
| 0.6B / PKG | 0.4439 ± 0.0355 | 0.4694 ± 0.0356 | 0.2551 ± 0.0311 |
| 1.7B / Combined | 0.0990 ± 0.0216 | 0.4975 ± 0.0354 | 0.0524 ± 0.0161 |
| 1.7B / PKG | 0.4434 ± 0.0483 | 0.4528 ± 0.0483 | 0.2642 ± 0.0428 |
| 1.7B / MKG | **0.5341 ± 0.0532** | 0.5169 ± 0.0530 | 0.3448 ± 0.0510 |
| 1.7B / Nothing | 0.5000 ± 0.0566 | 0.6154 ± 0.0551 | **0.3718 ± 0.0547** |
| 4B / Combined | 0.2740 ± 0.0522 | **0.6400 ± 0.0554** | 0.1644 ± 0.0434 |
| 4B / PKG | 0.2973 ± 0.0751 | 0.4324 ± 0.0814 | 0.2973 ± 0.0751 |
| 8B / PKG | 0.4528 ± 0.0684 | 0.5849 ± 0.0677 | 0.3585 ± 0.0659 |

- The centralized maxima for Pref@3, Prof@3, and Comb@3 come from **three different model/input combinations**. Most importantly, the best Comb@3 is **1.7B with no explicit KG context**. A sentence suggesting all three maxima belong to a single combined-context system would be incorrect. [Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)
- **Non-IID FedFLARKO, §7.2 Table 3:** 1.7B/PKG Pref@3 **0.3909 ± 0.0348**; 4B/Combined Prof@3 **0.6176 ± 0.0589**; 4B/PKG Comb@3 **0.3469 ± 0.0680**. **IID Table 4:** 4B/PKG Comb@3 **0.3051 ± 0.0599**. These are input/model-specific outcomes, not sparse-user outcomes. [Table 3](https://arxiv.org/html/2510.15993v1#S7.T3); [Table 4](https://arxiv.org/html/2510.15993v1#S7.T4)
- §7.3/Fig. 1 report that selected FLARKO results exceed conventional baselines on Pref@3/Comb@3, while many baselines do better on Prof@3. Exact conventional-baseline coordinates are graphical, not supplied in a numeric table in the inspected HTML; they were **not digitized**, so no numeric gain over LightGCN/popularity is asserted here. [§7.3](https://arxiv.org/html/2510.15993v1#S7.SS3); [Fig. 1](https://arxiv.org/html/2510.15993v1#S1.F1)
- **Conclusion qualification:** §8 says combining MKG and PKG yields the strongest performance and refers to outperforming “traditional and LLM-based baselines.” However, Table 2 shows combined context is not best for Pref@3 or Comb@3 in any model, and §6.2 enumerates conventional baselines rather than an external LLM-baseline suite. Use the actual table and named comparisons rather than adopting the conclusion's broad wording. §7.1 itself acknowledges combined-context degradation, especially for smaller models. [§8](https://arxiv.org/html/2510.15993v1#S8); [§6.2](https://arxiv.org/html/2510.15993v1#S6.SS2); [§7.1/Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)

### Inferences
- This paper supports **feasibility of history-grounded LLM asset recommendation on the same dataset**, not an estimated effect of language summarization. KTO training, graph construction, market information, model architecture, and input removal vary across comparisons. [Basis: §§3–4](https://arxiv.org/html/2510.15993v1#S3); [§§6–7](https://arxiv.org/html/2510.15993v1#S6)
- Strong no-context results and weak combined-context results make it especially inappropriate to claim the tables prove that richer or textual history representation necessarily improves personalized predictions. The paper's proposed explanations (context-length difficulty, learned financial patterns) are hypotheses rather than isolated mechanism tests. [Basis: §7.1/Table 2](https://arxiv.org/html/2510.15993v1#S7.T2)
- Its “behavioral alignment” is offline agreement with recorded future purchases. This does not itself show that users followed generated recommendations in deployment. [Basis: §§4, 6.1, 6.3](https://arxiv.org/html/2510.15993v1#S4)

### Gaps
- ACM landing page and PDF both returned **403**. The original author arXiv HTML was accessible, and **abstract, method (§§3–5), experiments (§§6–7), and complete conclusion (§8) were read**. Publisher metadata are independently verified via ACM's Crossref deposit; publisher/full-text equality remains unchecked.
- §§6–7 do not fully specify evaluated user counts, filtering, minimum history length, candidate count/universe, exclusion of previous purchases, invalid/duplicate generated ISIN handling, baseline hyperparameter/tuning budgets, and a complete metric aggregation formula. No paired significance test for representation effects is reported there. These are reproducibility gaps, not proof that the implementation is wrong. [§§6–7](https://arxiv.org/html/2510.15993v1#S6)
- The prose around Tables 3–4 contains cross-reference errors: non-IID discussion points to Table 4 although Table 3 is labeled non-IID. This note follows table captions and row values. No code reproduction or figure digitization was performed. [§7.2](https://arxiv.org/html/2510.15993v1#S7.SS2)

## 2. What is Conv-FinRe, and how close is it to the RQ?

### Takeaway
The verified academic name is **“Conv-FinRe: A Conversational and Longitudinal Benchmark for Utility-Grounded Financial Recommendation” (2026)**. It studies conversational history and financial ranking, but **does not evaluate FAR-Trans**, does not define sparse-history subgroups, and its **uNDCG measures modeled utility rather than future-purchase relevance**. [arXiv record](https://arxiv.org/abs/2602.16990); [full text, §§3–4](https://arxiv.org/html/2602.16990v2)

### Cited Findings

#### Bibliography and version-specific author discrepancy
- **Published proceedings record:** Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, **Yuqing Guo**, Fengran Mo, Jimin Huang, Yankai Chen, and Jian-Yun Nie (**13 authors**). **Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR ’26)**, ACM, pp. **3448–3455**, Melbourne, Australia. Online publication **July 19, 2026**; print date **July 20, 2026**. **Proceedings DOI `10.1145/3805712.3808658`.** This author list is specifically the ACM-deposited Crossref record, not a claim of having inspected the blocked publisher PDF title page. [Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1145/3805712.3808658)
- **arXiv author list:** Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, **Rosie Guo**, Fengran Mo, Jimin Huang, Yankai Chen, **Xue Liu**, and Jian-Yun Nie (**14 authors**). Full text styles Xue Liu as **Xue (Steve) Liu**. Do not silently combine this with the proceedings author list or presume why the names changed. [arXiv record](https://arxiv.org/abs/2602.16990); [v2 title block](https://arxiv.org/html/2602.16990v2)
- **arXiv versions:** v1 submitted **February 19, 2026, 01:29:50 UTC**; v2 revised **May 17, 2026, 16:40:11 UTC**. The record says **“Accepted by SIGIR 2026 Resource Track. Pre-camera-ready version.”** The separately verified July proceedings publication makes “preprint only” inaccurate as of this research date. **arXiv DOI `10.48550/arXiv.2602.16990`**, distinct from the ACM DOI. [arXiv record](https://arxiv.org/abs/2602.16990); [Crossref](https://api.crossref.org/works/10.1145/3805712.3808658)
- Both original **v1 and v2 HTML full texts were opened**. The evidence below uses **v2**. Its title block still contains ACM template placeholders (`XXXXXXX.XXXXXXX`, a 2018 Woodstock conference, and 2018 copyright text); these are **not valid bibliographic metadata**. A visible v1→v2 change is XOM's beta in Table 2, **0.55→0.95**; no exhaustive version diff is claimed. [v1](https://arxiv.org/html/2602.16990v1); [v2](https://arxiv.org/html/2602.16990v2)
- The authors' repository links this exact title/arXiv record and uses **`ConvFinRe` as an evaluation task name**, explaining the unhyphenated name in the request. Its README still cites the 14-author arXiv version. The repository was read as a moving `main` page on November 9, 2026, not as a commit-pinned implementation audit. [Author repository](https://github.com/The-FinAI/Conv-FinRe)

#### Dataset, population, chronology, and sparsity
- **Data actually used:** authors' own **Conv-FinRe benchmark**, combining Yahoo Finance daily/intraday prices with a questionnaire and investment-simulation decisions from **10 human participants**. It is neither a FAR-Trans subset nor recorded bank customers' actual purchases. FAR-Trans appears in related work and Table 1 only as a benchmark comparison. [§1/Table 1](https://arxiv.org/html/2602.16990v2#S1.T1); [§3.3.1](https://arxiv.org/html/2602.16990v2#S3.SS3.SSS1)
- Fixed **10-stock** universe: **PG, MRK, VZ, LIN, XOM, JPM, AMZN, MMM, SPG, TSLA**. Price horizon is described as **30 days, August 6–September 17, 2025**; preserve both the stated duration and dates rather than interpreting this as 30 consecutive calendar days. Candidate strata use market beta from five-year monthly returns. [§3.3.1/Table 2](https://arxiv.org/html/2602.16990v2#S3.T2)
- Participants provide demographics, financial capacity, investment experience, and risk attitudes, then make incremental buy decisions in an asset simulator with portfolio return/volatility feedback. The advisory dialogue is subsequently **generated from** profiles and these trajectories; it is not a transcript of human advisory conversations. [§3.3.1–3.3.2](https://arxiv.org/html/2602.16990v2#S3.SS3)
- **Table 3:** 10 users × **23 steps/user = 230 prefix-conditioned instances**; **270 unique turns**, **3,450 prefix-expanded turns**; context **4–26 turns**, average **15**; **1,818–7,252 tokens**, average **4,320.2**, using `cl100k_base`. The four-turn onboarding already supplies rich profile information before longitudinal history accumulates. [§3.3.2/Table 3](https://arxiv.org/html/2602.16990v2#S3.T3)
- **Sparse/cold subgroup:** no threshold on transaction/buy counts, no FAR-Trans sparse cohort, and no separately reported zero-history-investor cohort. §4.3 analyzes early-to-late decision steps and history/no-history contexts; **steps 1–10** are an early/middle phase, not a defined sparse-user cutoff. [§4.3](https://arxiv.org/html/2602.16990v2#S4.SS3)

#### Method and controls
- An LLM **reranks the fixed candidate stock set** using onboarding dialogue, earlier interaction history, verbalized market information, and heterogeneous advisor signals. The three advisor principles are **rational utility**, **market momentum**, and **risk sensitivity**; a fourth reference is the participant's observed choice. [§3.1, Eqs. 1–2](https://arxiv.org/html/2602.16990v2#S3.SS1)
- Utility is `U = standardized_return − λ_i × standardized_variance − γ_i × standardized_drawdown`, with preceding **7-day** market windows. Time-invariant user-specific `λ_i, γ_i` are fitted via regularized multinomial-logit inverse optimization over the user's **entire trajectory, t=1…T**. These parameters construct reference/advisor signals; the paper says the latent utility function is not explicitly shown to the evaluated LLM. [§3.2, Eqs. 3–6](https://arxiv.org/html/2602.16990v2#S3.SS2)
- Generated conversations contain verbalized survey profiles, advisor recommendations, past decisions, and subjective justifications consistent with those decisions. Thus they contain more than a compressed transaction log. **Risk-tolerance summaries** appear in validation, where **financial experts** translate fitted parameters into language and participants rate agreement **7.8/9**; this is not an evaluated LLM-generated history-summary treatment. Dialogue plausibility is **8.1/9**, based on one sampled step per user, three experts, four criteria. [§3.3.2](https://arxiv.org/html/2602.16990v2#S3.SS3.SSS2)
- Evaluated rankers: **GPT-5.2, GPT-4o, DeepSeek-V3.2, Qwen3-235B-A22B-Instruct, Qwen2.5-72B-Instruct, Llama-3.3-70B-Instruct, Llama3-XuanYuan3-70B-Chat**. Unified LM Evaluation Harness, max input **8,192 tokens**, max generated output **126 tokens**. No task-specific KTO/alignment training is reported. [§3.5](https://arxiv.org/html/2602.16990v2#S3.SS5)
- **Random baseline:** **1,000 uniformly random permutations per instance**. §4.3 compares with/without longitudinal conversation history for the same model families, but **no structured-history-feature ranker baseline** appears in §3.5/Table 4. The no-history comparison removes information rather than recoding the same history. Exact retained prompt fields are not fully documented in that discussion; the author README confirms separate history/no-history dataset releases, without proving feature parity. [Table 4](https://arxiv.org/html/2602.16990v2#S4.T4); [§4.3](https://arxiv.org/html/2602.16990v2#S4.SS3); [repository](https://github.com/The-FinAI/Conv-FinRe)

#### Metrics and supported results
- **uNDCG:** gain is the fitted utility, discounted over **all candidates** (`k=1…|S_t|`), normalized by utility-optimal DCG. Although there are ten candidates, this is **not purchase-relevance nDCG@10**. **MRR, HR@1, HR@3** measure recovery of the participant's selected stock; **Expert Alignment Score** is mean Kendall's τ with each advisor ranking. [§3.4, Eqs. 7–12](https://arxiv.org/html/2602.16990v2#S3.SS4)

Complete **§4.1, Table 4** transcription. The table prints ± values but the inspected main text/caption does **not clearly identify their uncertainty estimator**; do not label them standard errors, confidence intervals, or run-to-run standard deviations without further verification. [Table 4](https://arxiv.org/html/2602.16990v2#S4.T4)

| Model | uNDCG | MRR | HR@1 | HR@3 |
|---|---:|---:|---:|---:|
| Random | 0.73 ± 0.00 | 0.29 ± 0.01 | 0.10 ± 0.01 | 0.30 ± 0.01 |
| GPT-5.2 | 0.94 ± 0.03 | 0.46 ± 0.02 | 0.29 ± 0.03 | 0.51 ± 0.03 |
| GPT-4o | 0.94 ± 0.00 | 0.56 ± 0.03 | 0.42 ± 0.03 | 0.60 ± 0.03 |
| DeepSeek-V3.2 | 0.92 ± 0.00 | 0.51 ± 0.03 | 0.37 ± 0.03 | 0.55 ± 0.03 |
| Qwen3-235B-A22B-Instruct | 0.94 ± 0.00 | 0.47 ± 0.02 | 0.30 ± 0.03 | 0.52 ± 0.03 |
| Qwen2.5-72B-Instruct | 0.92 ± 0.01 | 0.63 ± 0.03 | 0.50 ± 0.03 | 0.69 ± 0.03 |
| Llama-3.3-70B-Instruct | **0.97 ± 0.00** | 0.52 ± 0.03 | 0.36 ± 0.03 | 0.59 ± 0.03 |
| Llama3-XuanYuan3-70B-Chat | 0.92 ± 0.00 | **0.65 ± 0.03** | **0.54 ± 0.03** | **0.69 ± 0.01** |

- **§4.2, Table 5:** Llama-3.3-70B has τ(utility) **0.74 ± 0.02**, τ(momentum) **0.73 ± 0.01**, τ(risk) **0.17 ± 0.02**. GPT-5.2's risk alignment is **0.28 ± 0.02**, DeepSeek's **0.26 ± 0.02**, XuanYuan3's **0.15 ± 0.02**. These are advisor-ranking correlations, not financial returns or purchase nDCG. [Table 5](https://arxiv.org/html/2602.16990v2#S4.T5)
- **§4.3/Figs. 2–3:** the prose reports history benefits for GPT-5.2, DeepSeek-V3.2 and Qwen3-235B; limited change for GPT-4o and Llama-3.3-70B; and degraded utility alignment for Qwen2.5-72B and XuanYuan3. Exact plotted deltas were not digitized. This is evidence of **model-dependent utility-alignment responses to additional conversation history**, not uniformly positive history effects. [§4.3](https://arxiv.org/html/2602.16990v2#S4.SS3)
- **Conclusion actually read:** the authors emphasize a tension between utility-based ranking and observed-choice alignment and motivate separating long-term preferences from short-term behavior. “Rational quality” remains defined by their fitted utility model; no realized long-term welfare improvement is established in this experiment. [§5](https://arxiv.org/html/2602.16990v2#S5); [§3.2](https://arxiv.org/html/2602.16990v2#S3.SS2)

### Inferences
- The experiment is useful **adjacent evidence about conversational context and the choice of recommendation target**. Its history/no-history analysis cannot identify a representation-only effect because the control does not retain the same history in structured form, and the generated conversations include profile/advisor information. [Basis: §§3.1–3.3](https://arxiv.org/html/2602.16990v2#S3); [§4.3](https://arxiv.org/html/2602.16990v2#S4.SS3)
- Fitting latent preferences over `H_1:T` makes the utility reference **retrospective** relative to early decision steps. Since utility/risk advice is generated from those fitted preferences, a strictly forward-prediction adaptation would need to inspect and time-isolate that construction. This is a protocol distinction/potential leakage pathway, not a measured leakage effect or proof that the authors' diagnostic benchmark is invalid. [Basis: §§3.1–3.3, especially Eqs. 5–6](https://arxiv.org/html/2602.16990v2#S3.SS2)
- Ten participants, ten candidates, synthetic dialogue, a short common market interval, and correlated prefix instances limit transfer to FAR-Trans's sparse bank-customer histories. Neither early steps nor “nohistory” constitute a validated sparse financial-user subgroup. [Basis: §3.3/Table 3](https://arxiv.org/html/2602.16990v2#S3.T3); [§4.3](https://arxiv.org/html/2602.16990v2#S4.SS3)
- There are internal reporting issues worth preserving: the text claims coverage of **all eleven GICS sectors** despite listing only ten single-sector stocks, and beta strata in Table 2 have **3/2/5** members rather than an especially even allocation. The larger concern for this task is that these are a small constructed candidate set, not FAR-Trans candidate assets. [Basis: §3.3.1/Table 2](https://arxiv.org/html/2602.16990v2#S3.T2)

### Gaps
- ACM abstract and PDF endpoints returned **403**. Original arXiv v1 and v2 full text were accessible: **abstract, full method (§3), results (§4), and conclusion (§5) were read**. Publisher-version content changes and the cause of the author-list discrepancy are unresolved; no author identity equivalence is assumed.
- No sparse-history cutoff, sparse-specific nDCG, structured-history comparator, or representation-matched experiment appears in the inspected methods/results. No class split is implied. [§§3–4](https://arxiv.org/html/2602.16990v2#S3)
- The text does not fully specify the conversation-generation LLM/prompt/decoding settings, the uncertainty estimator, a separate temporal fit/validation split for latent preferences, or exact numerical history/no-history deltas. Code notebooks and evaluation implementation were not audited. [§§3–4](https://arxiv.org/html/2602.16990v2#S3)
- **Metric implementation question:** Eqs. 3 and 7 use standardized quantities and direct utility gains, which can be negative; the inspected definition does not explain a nonnegative transformation or how problematic IDCG values are handled. Consequently, the usual bounded-nDCG interpretation and reported random value **0.73** should not be reverse-engineered into purchase relevance or assumed implementation details. Code verification remains necessary if reusing this metric. [§3.2/Eq. 3](https://arxiv.org/html/2602.16990v2#S3.SS2); [§3.4/Eqs. 7–8](https://arxiv.org/html/2602.16990v2#S3.SS4); [Table 4](https://arxiv.org/html/2602.16990v2#S4.T4)

## 3. Which is nearest, what is the defensible gap, and what sources were opened?

### Takeaway
**Recommend FLARKO provisionally as the nearer of these two works; retain Conv-FinRe as adjacent evidence. Final nearest-work selection remains coordinated. Neither inspected experiment establishes whether LLM-generated summaries improve purchase-based nDCG@10 over structured features for sparse FAR-Trans users under matched information and ranking conditions.** This is a section-bounded assessment, not a literature-wide novelty claim. [FLARKO §§3–4, 6–7](https://arxiv.org/html/2510.15993v1); [Conv-FinRe §§3–4](https://arxiv.org/html/2602.16990v2)

### Cited Findings

| RQ requirement | FLARKO | Conv-FinRe |
|---|---|---|
| FAR-Trans users | Yes, §6.1 | No; own 10-person simulation, §3.3 |
| Future purchase behavior | Purchase membership within 180 days, §§4/6.1 | Simulator choice at each decision step, §§3.3–3.4 |
| LLM-generated transaction-history summary | No; structured PKG and numeric MKG summaries, §3 | Generated advisory dialogue/profile verbalization, not standalone transaction summary, §3.3 |
| Structured-history control with same information | No; algorithm/data-source comparisons and graph-input removal | No; LLM comparisons, random rankings, history/no-history |
| Identical downstream ranker for representation contrast | No such contrast | Same models in history ablation, but history information removed rather than re-encoded |
| Purchase-relevance nDCG@10 | No; Pref/Prof/Comb@3, §6.3 | No; utility-gain uNDCG, choice MRR/HR@1/3, §3.4 |
| Defined sparse/cold cohort and cutoff | Not reported in §§6–7 | Not reported in §§3–4 |

Sources for all matrix entries: [FLARKO §§3–4](https://arxiv.org/html/2510.15993v1#S3), [§§6–7](https://arxiv.org/html/2510.15993v1#S6); [Conv-FinRe §3](https://arxiv.org/html/2602.16990v2#S3), [§4](https://arxiv.org/html/2602.16990v2#S4).

- **Safe gap formulation:** “FLARKO evaluates KG-grounded, KTO-aligned LLM recommendations on FAR-Trans using top-3 purchase/profitability hits (§§3–4, 6–7), while Conv-FinRe evaluates conversational context and utility/choice alignment in a separate participant simulation (§§3–4). These evaluated designs do not isolate the effect of replacing structured transaction-history features with LLM-generated summaries for sparse FAR-Trans users under a fixed purchase-based nDCG@10 protocol.” [FLARKO](https://arxiv.org/html/2510.15993v1); [Conv-FinRe](https://arxiv.org/html/2602.16990v2)

### Inferences
- To test the supplied RQ, both arms should derive from **identical pre-cutoff history events**, with the same treatment of purchases/sales and reconstructed entries; equal customer/asset metadata and price information; the same eligible users, candidate assets, repeat-purchase policy, future horizon, and purchase relevance; and the same ranker and comparable tuning budget. Otherwise an effect can reflect information access, candidate filtering, or model differences. This is a design implication of the mismatches above, not an experiment already run by either paper. [Basis: FLARKO §§3–7](https://arxiv.org/html/2510.15993v1#S3); [Conv-FinRe §§3–4](https://arxiv.org/html/2602.16990v2#S3)
- Define sparsity from **training-only available history**, stating whether the count is transaction events, buys, or unique bought assets, and distinguish sparse warm-start from zero-history users. Neither paper supplies an empirically validated cutoff for this RQ. [Basis: FLARKO §6](https://arxiv.org/html/2510.15993v1#S6); [Conv-FinRe §3.3](https://arxiv.org/html/2602.16990v2#S3.SS3)
- A positive purchase-nDCG result would support **prediction of observed purchases**, not automatically profitability, suitability, preference discovery, or investor welfare. Both works distinguish behavioral alignment from financial utility/profitability in their objectives and metrics. [FLARKO §§4/6.3](https://arxiv.org/html/2510.15993v1#S6.SS3); [Conv-FinRe §§3.4/5](https://arxiv.org/html/2602.16990v2#S3.SS4)

### Gaps
- **Effect status: unestablished by these papers.** No defensible numeric effect size, positive/negative conclusion, or confidence interval for the exact student RQ can be extracted from them. The absence of the experiment in these two full texts is not evidence that no other publication has conducted it.
- **User-supplied context:** the official class split remains pending. The user personally checked original transactions and metadata, **not these papers**. Research date is **November 9, 2026**. The assignment and these provenance constraints are supplied context, not publication claims.
- The pre-existing `far_trans.md` was read for context, without duplicating FAR-Trans research. This task did not inspect or modify raw data or Task 1 outputs, train models, execute repository code, or write the final homework report. Only this evidence note was created in the project.

#### Exact URL/access ledger and version identifiers

The URLs below are the actual requests made during this task. Fragment links in the evidence above are locators within opened full texts, not additional requests. Search results were used for discovery only; paper claims rely on original full texts and publisher-deposited metadata.

**Primary full texts, metadata, and author resource**

| Exact URL requested | Outcome / use |
|---|---|
| `https://arxiv.org/abs/2510.15993` | Success; FLARKO v1 history, authors, arXiv DOI, related ACM DOI |
| `https://arxiv.org/html/2510.15993v1` | Success; original FLARKO full text. Initial response truncated before §7.3; saved output was read at lines 790–849 to obtain complete §7.3, §8 conclusion, §9 and bibliography context |
| `https://api.crossref.org/works/10.1145/3768292.3770399` | Success; ACM-deposited FLARKO publication record, pages/dates/DOI |
| `https://dl.acm.org/doi/10.1145/3768292.3770399` | 403; publisher landing page unavailable |
| `https://arxiv.org/abs/2602.16990` | Success; Conv-FinRe v1/v2 dates, author list, SIGIR Resource Track acceptance |
| `https://arxiv.org/html/2602.16990v1` | Success; original v1, complete main text visible, later reference output truncated |
| `https://api.crossref.org/works/10.1145/3805712.3808658` | Success; ACM-deposited published metadata, 13-author list, DOI, pages, dates |
| `https://dl.acm.org/doi/abs/10.1145/3805712.3808658` | 403; publisher abstract unavailable |
| `https://arxiv.org/html/2602.16990v2` | Success in text format; complete main text and conclusion read; version used for Conv-FinRe findings |
| `https://dl.acm.org/doi/pdf/10.1145/3805712.3808658` | 403; no publisher PDF obtained |
| `https://dl.acm.org/doi/pdf/10.1145/3768292.3770399` | 403; no publisher PDF obtained |
| `https://github.com/The-FinAI/Conv-FinRe` | Success; author README, task-name correspondence, history/no-history resources; moving main, no commit pinned |

**Discovery requests, including unsuccessful searches**

| Exact URL requested | Outcome |
|---|---|
| `https://www.google.com/search?q=%22ConvFinRe%22` | JavaScript/retry page, no useful results |
| `https://api.crossref.org/works?query=ConvFinRe&rows=5` | Zero results for unhyphenated name |
| `https://www.google.com/search?q=%22ConvFinRe%22&gbv=1` | No useful result content |
| `https://www.bing.com/search?q=%22ConvFinRe%22` | Irrelevant plant-care results; rejected as discovery evidence |
| `https://api.crossref.org/works?query.title=conversational%20financial%20recommendation&rows=5` | Unrelated candidate records; not used for substantive claims |
| `https://arxiv.org/search/?query=ConvFinRe&searchtype=all&abstracts=show&order=-announced_date_first&size=50` | Zero results for unhyphenated name |
| `https://api.crossref.org/works?query=conversational%20financial%20large%20language&rows=10&select=title,author,DOI,published,container-title` | Unrelated records |
| `https://api.github.com/search/repositories?q=ConvFinRe` | Zero results for unhyphenated name |
| `https://html.duckduckgo.com/html/?q=%22ConvFinRe%22` | No exact-match results |
| `https://api.openalex.org/works?search=ConvFinRe&per-page=5` | Zero results; no substantive evidence used |
| `https://api.crossref.org/works?query.title=financial%20recommendations%20conversational&filter=from-pub-date:2023-01-01&rows=20&select=title,author,DOI,published,container-title` | Unrelated records |
| `https://html.duckduckgo.com/html/?q=ConvFinRe+recommendation` | Successful discovery via spelling expansion to Conv-FinRe; arXiv, author GitHub, and ACM DOI found |
| `https://html.duckduckgo.com/html/?q=%22conversational%22+%22financial%22+%22recommendation%22+LLM` | Corroborating discovery of same arXiv and author repository |
| `https://api.crossref.org/works?query.title=conversational%20financial&rows=10&select=title,author,DOI,published,container-title` | Other candidate titles, not researched further |

PDF skill was loaded before publisher PDF requests. No PDF download or parsing succeeded or was needed for the accessible author HTML full texts. The requested researcher guidance was read as the first action. No subdelegation was used.
