# Financial recommendation evaluation: Investors Are (Not) Always Right

Research evidence for Abaidullah Seikh's Task2; checked **2026-11-09**. Research question supplied by the user: **Do LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?** These are research notes, not the final homework report. Verification below was performed by this research assistant; it must not be described as the student's personal paper verification. The user's reported Task1 verification concerned a transaction only.

## 1. What is the verified publication, and which version was read?

### Takeaway

The named study is a published, refereed 2026 ACM journal article, not merely an unverified forthcoming paper. Its earlier online accepted manuscript dates to December 2025; that date must be distinguished from the January 2026 final publication. No separate preprint DOI was verified. [ACM](https://dl.acm.org/doi/10.1145/3780097); [institutional record](https://eprints.gla.ac.uk/373432/).

### Cited Findings

- **Verified bibliography:** Javier Sanz-Cruzado, Richard McCreadie, Nikolaos Droukas, Craig Macdonald, and Iadh Ounis. **2026. “Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations.” ACM Transactions on Information Systems 44(2), Article 51, 1–56. DOI: 10.1145/3780097.** The exact final title ends in the plural **Recommendations**. All five authors, in this order, are verified against ACM, its publisher-deposited Crossref metadata, and the article's actual title/reference pages. [ACM](https://dl.acm.org/doi/10.1145/3780097); [DOI resolver](https://doi.org/10.1145/3780097); [published PDF](https://eprints.gla.ac.uk/373432/2/373432.pdf).
- **Publication chronology:** received 22 January 2025; revised 14 September 2025; accepted 2 December 2025; **Online AM (accepted manuscript): 10 December 2025**; final **Published: 28 January 2026**. ACM assigns it to volume 44, issue 2 (February 2026); Crossref records the issue's print date as 28 February 2026. The repository record was deposited 5 December 2025. These are different events, not competing publication years. [ACM, Publication History](https://dl.acm.org/doi/10.1145/3780097); [published PDF, download cover](https://eprints.gla.ac.uk/373432/2/373432.pdf); [repository dates](https://eprints.gla.ac.uk/373432/).
- **Version actually read:** official ACM version-of-record HTML, including the author abstract, task definition, theoretical analysis, experimental setup, results, discussion, conclusion, limitations, and data statement. Also downloaded the repository's explicitly labelled **Published Version** PDF and extracted its text to corroborate the title, dates, Figure 4 discussion, Table 5, and statistical appendix. The PDF has an ACM download cover in addition to article pages 51:1–51:56. Thus article page 51:24 is not physical PDF page 24. [HTML full text](https://dl.acm.org/doi/10.1145/3780097); [repository version label](https://eprints.gla.ac.uk/373432/); [published PDF](https://eprints.gla.ac.uk/373432/2/373432.pdf).
- **Earlier author manuscript:** downloaded the author's `tois2025.pdf` and read its first two pages. It uses a December 2025 reference template, placeholder volume/issue “1, 1,” and a blank DOI field (`https://doi.org/`). The author publications page also calls the article December 2025 while linking the final ACM DOI. This is evidence of an earlier manuscript/date convention, not evidence of a different journal DOI or a separately registered preprint DOI. The repository metadata uses the singular “recommendation,” whereas the final article title is plural. Prefer the publisher's final title and 2026 date. [Author manuscript](https://javiersanzcruza.github.io/assets/papers/tois2025.pdf); [author publications](https://javiersanzcruza.github.io/pubs); [repository](https://eprints.gla.ac.uk/373432/).
- **Earlier related work is a distinct 2022 workshop paper:** the journal article's Introduction explicitly expands an earlier one-year empirical study, “On Transaction-Based Metrics as a Proxy for Profitability of Financial Asset Recommendations,” by the same five authors. The institutional record identifies the 3rd Workshop on Personalization & Recommender Systems in Financial Services, associated with RecSys 2022, and marks it published/refereed. No DOI appears on the opened workshop record. Do not relabel this predecessor as a 2025/2026 preprint of the final journal article. [Journal §1 and reference 51](https://dl.acm.org/doi/10.1145/3780097#sec-1); [2022 record](https://eprints.gla.ac.uk/278306/).

### Inferences

- Cite **2026, DOI 10.1145/3780097** in Task2. If explaining apparent 2025 citations, explicitly say “accepted manuscript online 10 December 2025; final article published 28 January 2026.” There is no verified basis to supply an arXiv DOI for this title. [ACM publication history](https://dl.acm.org/doi/10.1145/3780097).

### Gaps

- No separately registered preprint/date/DOI was found through arXiv title and author searches or the exact-title DataCite search. This is a **search outcome**, not proof that no preprint exists anywhere. The earlier version that can actually be dated is ACM's online accepted manuscript, under the same article record/DOI. Full search/access details appear in §3 below.
- The published PDF's automatically generated download cover has an odd expanded McCreadie name and “Bank of Greece” affiliation; the article's own title page, contact block, ACM HTML author list, and Crossref agree on **Richard McCreadie** and **National Bank of Greece** for Droukas. Bibliography follows the actual article rather than the cover artifact. [Published PDF](https://eprints.gla.ac.uk/373432/2/373432.pdf).

## 2. What did the paper test, and what demonstrates metric disagreement?

### Takeaway

The paper studies whether transaction-based measures of future purchasing and price-based measures of investment profitability can substitute for each other. On FAR-Trans, model comparisons and pooled correlations show disagreement; neither the theoretical result nor the empirical findings imply that purchase-prediction nDCG is inappropriate for a research question explicitly about predicting purchases. [§§4–8](https://dl.acm.org/doi/10.1145/3780097).

### Cited Findings

#### Problem and theoretical claim

- The paper defines FAR as ranking assets a customer has not previously interacted with. Its three main questions concern the theoretical relation between transaction/profitability metrics, their empirical relation, and factors influencing those relations. It is an evaluation-methodology study comparing existing algorithms, not a proposed LLM summarization system. [§3](https://dl.acm.org/doi/10.1145/3780097#sec-3); [§4](https://dl.acm.org/doi/10.1145/3780097#sec-4).
- Theorem 5.6 states that, for fixed assets, cutoff and evaluation interval, the two metric families are independent over **all possible user–ranking pairs**, with correlation zero. The calculation in §5.3 factorizes the expectation of the metric product and establishes zero covariance under that theoretical construction. It is not a claim that real-user metric values always have zero correlation; §6 explicitly explains why nonrandom investors and algorithm selection can yield different empirical relations. The theory also assumes customer-independent profitability, whose limitations are discussed in §12. [§5.3, Theorem 5.6 and Equations 1–6](https://dl.acm.org/doi/10.1145/3780097#sec-5-3); [§6](https://dl.acm.org/doi/10.1145/3780097#sec-6); [§12 limitations](https://dl.acm.org/doi/10.1145/3780097#sec-12-1).

#### Data and splitting

- **Yes, FAR-Trans is used.** The empirical data cover January 2018–November 2022, a Greek-market snapshot from a large European financial institution, with stocks, bonds, mutual funds, prices, and customer buy/sell logs. Table 3 reports **806 unique assets**, **321 assets with investments**, **29,090 unique customers**, **388,049 transactions (154,103 unique)**, **228,913 acquisitions (89,884 unique)**, and **703,303 price observations**. These are the paper's dataset-description counts, not counts for each post-filtered split or for a sparse-user cohort. [§6.1, Table 3](https://dl.acm.org/doi/10.1145/3780097#sec-6-1).
- Acquisition is converted to binary relevance/interest: an acquired asset is 1, otherwise 0. Repeated investments are not separate graded-relevance levels. For a customer who acquires the same asset in both training and test, the overlapping asset interactions are kept only in training. The recommendation task consequently emphasizes **previously unseen assets**, not repeated purchases of an already acquired asset. [§3](https://dl.acm.org/doi/10.1145/3780097#sec-3); [§6.1](https://dl.acm.org/doi/10.1145/3780097#sec-6-1).
- **61 temporal variants**, recommendation dates from **1 August 2019 to end-November 2021**, described as spaced two weeks apart. History before each date is for training/validation; subsequent information is for evaluation. The first split begins training at **1 January 2018**. The main evaluation horizon is **six months**; §11 also tests **1, 3, 9 and 12 months**. The paper describes the date span as two years four months, so “two-year study” is shorthand. [§6.1 and Figure 2](https://dl.acm.org/doi/10.1145/3780097#sec-6-1); [§11](https://dl.acm.org/doi/10.1145/3780097#sec-11).
- Post-split filtering requires customers to have history before recommendation and test-period interaction; evaluated assets must have pricing information during the test period. This is not a zero-history cold-start evaluation, and users with no test-period activity are not represented in the evaluation population. [§6.1, Dataset Cleaning (Post-Split)](https://dl.acm.org/doi/10.1145/3780097#sec-6-1).
- **Hyperparameters are selected to maximize six-month ROI**, at **1 April 2019, 1 October 2019, and 31 January 2020**. This matters when using the reported nDCG scores as baselines: the study does not claim all algorithms were tuned to maximize purchase nDCG. [§6.3, final paragraph](https://dl.acm.org/doi/10.1145/3780097#sec-6-3).

#### Algorithms

The 12 methods are explicitly enumerated in §6.3 and Table 5. [§6.3](https://dl.acm.org/doi/10.1145/3780097#sec-6-3); [Table 5](https://dl.acm.org/doi/10.1145/3780097#tab5).

| Family | Methods | Inputs/target |
|---|---|---|
| Sanity baseline | Random | Random asset ranking |
| Price-based | Linear regression; random forest regression; LightGBM regression | Historical closing-price technical indicators; predict future six-month ROI |
| Transaction-based, nonpersonalized | Popularity | Number of prior purchases |
| Collaborative/history-based | LightGCN; matrix factorization (MF); user-based kNN; Apriori association-rule mining (ARM) | Customer–asset acquisitions and co-acquisition patterns |
| Demographic | Customer profile similarity (CPS) | User-kNN-style similarity based on risk-questionnaire profile |
| Hybrid | Hybrid-regression; Hybrid-nDCG | Outputs of preceding recommenders as features; LightGBM ROI regression or LambdaMART optimizing nDCG |

Price features include average price, historical ROI, volatility, MACD, momentum, rate of change, relative strength index, detrended price oscillator, ROI/volatility, and rolling minima/maxima. These are market features, not natural-language descriptions of transaction histories. [§6.3, Table 4](https://dl.acm.org/doi/10.1145/3780097#sec-6-3).

#### Metrics and their meaning

- **nDCG@10**: normalized discounted cumulative gain on binary future acquisitions of previously unseen assets; relevant items near the top receive larger weight through `1/log2(rank+1)`. The ideal ranking normalizes each user's DCG. This measures agreement with subsequent purchase behavior, not price appreciation or financial welfare. [§6.2, Equations 7–9](https://dl.acm.org/doi/10.1145/3780097#sec-6-2).
- **ROI@10**: arithmetic mean of the price returns of the top ten assets over the fixed horizon, representing equal monetary investment in each recommended asset. **Monthly ROI@10** is `(1 + ROI@10)^(30 / horizon_days) - 1`; it is a 30-day-equivalent compounded rate computed from that horizon's hypothetical portfolio return. It is not the raw six-month return, an annual return, or realized investor profit. [§6.2, Equations 10–12](https://dl.acm.org/doi/10.1145/3780097#sec-6-2).
- Secondary metrics are **%prof@10**, the proportion of recommended assets with nonnegative ROI, and **Volatility@10**, daily-return standard deviation averaged across recommended assets. A high proportion of nonnegative assets need not imply high aggregate return. [§6.2](https://dl.acm.org/doi/10.1145/3780097#sec-6-2).

#### Verified numerical findings

1. **Pooled correlation is weakly negative:** **Pearson r = −0.13** between nDCG@10 and monthly ROI@10, six-month horizon. The calculation pools approximately **1.5 million user × algorithm × temporal-variant metric observations**. This is not the correlation of only 12 algorithm means: Figure 4(a) plots those means, whereas Figure 4(b) reports pooled correlations. Authors report **p < 0.05**, with further tests in Appendix C.2/Table C5. Exact location: **§7, Figure 4(b), article p. 51:23**. [§7](https://dl.acm.org/doi/10.1145/3780097#sec-7); [published PDF](https://eprints.gla.ac.uk/373432/2/373432.pdf).

2. **Model preference reverses with evaluation objective.** The following are exact **Table 5 / §8.1 / article p. 51:24** values, averaged over the **61 temporal splits**, for the **six-month evaluation horizon**, cutoff **10**. ROI values are reported decimal monthly-equivalent rates, not percentages or six-month totals. [Table 5](https://dl.acm.org/doi/10.1145/3780097#tab5); [published PDF](https://eprints.gla.ac.uk/373432/2/373432.pdf).

| Method | nDCG@10 | Monthly ROI@10 |
|---|---:|---:|
| Random | 0.0106 | 0.0071 |
| Random forest regression | 0.0237 | 0.0259 |
| Linear regression | 0.0215 | 0.0249 |
| LightGBM regression | 0.0221 | 0.0225 |
| Popularity | 0.2710 | 0.0006 |
| LightGCN | **0.3404** | 0.0004 |
| ARM | 0.2556 | 0.0007 |
| MF | 0.1780 | 0.0038 |
| User-based kNN | 0.1599 | 0.0119 |
| CPS | 0.2722 | 0.0026 |
| Hybrid-nDCG | 0.2313 | 0.0063 |
| Hybrid-regression | 0.0261 | 0.0132 |

   LightGCN is strongest on the reported purchase nDCG, while random forest is strongest on the reported monthly ROI. These are **overall evaluated-population results**, not sparse-user results and not LLM-summary improvements. All the averaged ROI values in this table are positive; underperforming another method or a market benchmark must not be misreported as an average monetary loss. The paper discusses losses at particular dates separately in §8.2/Figure 5. [§§8.1–8.2](https://dl.acm.org/doi/10.1145/3780097#sec-8).

3. **Synthetic effective investors change the sign:** authors replace actual investors with synthetic ones, preserving the price universe and approximately the acquisition-count distribution, selecting assets using future ROI among the **top 50** and generating **10 synthetic datasets**. The pooled metric correlation becomes **+0.13**. Exact locations: construction **§9.2.1**, repetitions **§9.2.2**, result **§9.2.3/Figure 7(b)**. This is deliberately hindsight-informed synthetic behavior, not performance attained by real expert investors or a deployable recommendation method. [§9.2](https://dl.acm.org/doi/10.1145/3780097#sec-9-2).

4. **Time-specific disagreement varies materially:** §10/Figure 8(a) reports per-split correlation varying from approximately **−0.65 to +0.4**, over algorithm–customer pairs within each split. §11.2.1/Figure 12 reports pooled correlations remaining slightly negative across horizons, approximately **−0.13 to −0.05**, while §11.2.2/Figure 13 shows stronger changes at particular dates. Thus neither a uniformly negative relation at every date nor universal incompatibility of the objectives is supported. [§10](https://dl.acm.org/doi/10.1145/3780097#sec-10); [§11.2](https://dl.acm.org/doi/10.1145/3780097#sec-11-2).

#### Conclusion and author-stated limitations

- The authors conclude that transaction metrics cannot stand in for profitability and recommend evaluating both when assessing a financial recommendation system's broader utility. They explicitly say it would be premature to abandon transaction-based evaluation. They emphasize recommendation date, investor effectiveness relative to the market, and investment horizon as relevant factors. [§12](https://dl.acm.org/doi/10.1145/3780097#sec-12).
- Limitations include a single institution/market dataset; only a partial view of users' portfolios; price-based return omitting dividends and bond coupons; fixed shared horizons although individuals hold assets for different lengths; tested horizons of at most one year; equal-allocation/customer-independent profitability that does not encode personal goals or portfolio weights. Holding-time estimation is censored by the dataset boundaries. [§11, opening discussion](https://dl.acm.org/doi/10.1145/3780097#sec-11); [§12 limitations](https://dl.acm.org/doi/10.1145/3780097#sec-12-1).
- The data statement says that demographic information could not be publicly shared because of sensitivity. The public release therefore does not automatically support reproducing the CPS baseline or every hybrid feature. The paper links the FAR-Trans data DOI, **10.5525/gla.researchdata.1658**; this is a **dataset DOI**, not the journal DOI or a preprint DOI. [Data Statement](https://dl.acm.org/doi/10.1145/3780097#sec-13).

### Inferences

- The strongest defensible interpretation is **metric non-substitutability**. Better future-purchase ranking does not warrant claiming better investment returns; conversely, better ROI does not establish better purchase prediction. The model results provide concrete evidence of this distinction. [§§7–8](https://dl.acm.org/doi/10.1145/3780097#sec-7).
- The authors call their theorem “independence,” but zero covariance alone is not a general proof of statistical independence for arbitrary random variables. When summarizing, attribute their terminology and retain the all-user–ranking-pairs assumptions rather than asserting unconditional independence in real markets. This is a mathematical interpretation of the displayed proof, not an independently replicated theorem result. [§5.3](https://dl.acm.org/doi/10.1145/3780097#sec-5-3).
- Statistical significance of the pooled correlation should not be equated with a large effect or a causal effect of increasing nDCG. Users recur across algorithms/dates and the temporal windows overlap; the described Student t-tests do not establish cluster-robust uncertainty for those dependencies. This is a methodological caution inferred from the design, not an author-reported correction. [§6.1](https://dl.acm.org/doi/10.1145/3780097#sec-6-1); [§7](https://dl.acm.org/doi/10.1145/3780097#sec-7); [Appendix C.2](https://dl.acm.org/doi/10.1145/3780097#app-1-sec-3-2).

### Gaps

- **Unresolved numeric distinction:** Table 5's “Market average” monthly ROI is **0.0079**, while Table 6's average asset monthly ROI is **0.004259**. These may reflect different aggregation orders (monthly-equivalent return of a portfolio versus mean of asset-level monthly-equivalent returns), but the text read does not explicitly reconcile them. Do not silently combine these values or assert a single interchangeable market baseline. The principal evidence above uses model-versus-model comparisons instead. [Table 5](https://dl.acm.org/doi/10.1145/3780097#tab5); [§9.1/Table 6](https://dl.acm.org/doi/10.1145/3780097#sec-9-1).
- **Temporal validation ambiguity:** the ROI-selection dates listed in §6.3 are not all earlier than the first recommendation date, and six-month outcomes extend beyond those dates. The exact nesting of model selection for each early evaluation split is not explained in the read setup. Treat this as a replication/chronological-validation question, not a proven leakage finding. [§§6.1–6.3](https://dl.acm.org/doi/10.1145/3780097#sec-6).
- No experiment was rerun, no original dataset was downloaded here, and no confidence interval or sparse-user numerical result was inferred from the paper's aggregate tables.

## 3. How does this support Task2, and what are the access and evidence boundaries?

### Takeaway

This is strong **evaluation-context and baseline evidence** for Task2, with direct FAR-Trans and nDCG@10 relevance. It is **not direct evidence** that LLM summaries improve sparse-history purchase prediction. The proposed representation comparison remains an empirical question. [§§6–8](https://dl.acm.org/doi/10.1145/3780097#sec-6).

### Cited Findings

- **LLM summaries:** no evaluated algorithm generates natural-language transaction-history summaries; no summary prompting, summary encoder, or summary-vs-structured input ablation appears in the method inventory or experiments. The ACM website's separate “AI Summary” interface is a publisher feature, not a component or experiment of the study. [§6.3](https://dl.acm.org/doi/10.1145/3780097#sec-6-3); [ACM abstract/interface](https://dl.acm.org/doi/10.1145/3780097).
- **Sparse users:** the paper does discuss an acquisition-count distribution in which most customers acquire a single asset, especially when motivating the synthetic generation. It does **not** define a sparse-history cohort and report its nDCG separately, nor vary controlled training-history lengths to estimate a summary benefit. A full-dataset acquisition distribution is not a pre-cutoff sparsity analysis. [§6.1/Figure 3(f)](https://dl.acm.org/doi/10.1145/3780097#sec-6-1); [§9.2.1](https://dl.acm.org/doi/10.1145/3780097#sec-9-2-1).
- **Controlled history representation:** algorithms differ in architecture, input sources and learning objectives. Comparing collaborative filtering, pricing models and hybrids does not isolate the effect of narrating the same history. [§6.3](https://dl.acm.org/doi/10.1145/3780097#sec-6-3).

### Inferences

- **Preserve the user's target:** use future-purchase **nDCG@10 as the primary outcome**. Describe any improvement as better ranking of subsequently purchased assets. Profitability can be contextual or secondary if the experiment calls for it; the paper does not require changing this RQ into return prediction. This is an application of its distinction between objectives. [§6.2](https://dl.acm.org/doi/10.1145/3780097#sec-6-2); [§12](https://dl.acm.org/doi/10.1145/3780097#sec-12).
- **Design implications, not tested findings:** define sparsity using training-only history; supply summaries and structured features with the same pre-cutoff information; keep users, candidate assets, future-purchase labels, horizon, downstream ranking conditions and evaluation cutoff fixed where possible; tune for the primary purchase metric with chronological validation. Report the sparse cohort separately. These controls are needed to answer the user's representation question and were not supplied by this study. The paper motivates chronological evaluation and careful label/horizon definitions. [§6.1](https://dl.acm.org/doi/10.1145/3780097#sec-6-1); [§11](https://dl.acm.org/doi/10.1145/3780097#sec-11).
- **Baseline choices:** popularity is an important inexpensive comparator, alongside suitable structured-history methods such as user-kNN, MF, or LightGCN. The table's high popularity nDCG makes it unsafe to assume personalization alone is sufficient. Its exact published scores are contextual references rather than guaranteed replication targets, especially after restricting to sparse users. [§8.1/Table 5](https://dl.acm.org/doi/10.1145/3780097#sec-8-1).
- **Clarify repeat purchases:** the paper removes previously seen assets from the target. If Task2 intends to predict all future purchases, including rebuys, explicitly distinguish that task from the paper's novel-asset evaluation before comparing scores. [§3](https://dl.acm.org/doi/10.1145/3780097#sec-3); [§6.1](https://dl.acm.org/doi/10.1145/3780097#sec-6-1).

### Gaps

#### Exact retrieval/access log

All URLs below were actually opened/requested on **2026-11-09**. Section-anchor links elsewhere in these notes identify locations within the opened ACM full text; they were not separate fetches. Links merely displayed by a source were not treated as opened sources.

**Successful primary/registry sources and files:**

1. `https://api.crossref.org/works?query.title=Investors%20Are%20%28Not%29%20Always%20Right%3A%20A%20Comparison%20of%20Transaction-Based%20and%20Profitability-Based%20Metrics%20for%20Financial%20Asset%20Recommendations&rows=3` — exact matching first result; verified title, authors, DOI, journal, volume/issue, final online/print dates, received/accepted dates. Other returned works were irrelevant.
2. `https://dl.acm.org/doi/10.1145/3780097` — **full original HTML successfully read**. Author abstract, §§1–4, §5.3, §§6–12, Data Statement, and relevant statistical appendix checked. Main evidence is final publisher content, not search snippets or an AI-generated summary.
3. `https://doi.org/10.1145/3780097` — returned matching formatted citation.
4. `https://eprints.gla.ac.uk/373432/` — final publication metadata, refereed/published status, repository deposit date and published-PDF version label.
5. `https://eprints.gla.ac.uk/373432/2/373432.pdf` — downloaded successfully using curl; parsed with `pdftotext -layout`. Local artifacts: `/tmp/opencode/financial_evaluation_published.pdf` and `/tmp/opencode/financial_evaluation_published.txt`. Original article text was read primarily in HTML; PDF used for exact corroboration and page locations. No claim of independently redoing experiments or auditing every appendix proof.
6. `https://javiersanzcruza.github.io/` — author's acceptance announcement dated 2 December 2025; also lists an earlier 24 June 2024 talk with a similar title. The talk date is not a verified publication/preprint date.
7. `https://javiersanzcruza.github.io/pubs` — links author manuscript, final DOI, and earlier workshop work; uses December 2025 for this article.
8. `https://javiersanzcruza.github.io/assets/papers/tois2025.pdf` — author manuscript downloaded; first two pages extracted/read. Local artifacts: `/tmp/opencode/financial_evaluation_author.pdf` and `/tmp/opencode/financial_evaluation_author_front.txt`. Front matter has December 2025 placeholders and no populated DOI. Not used as the source for final numerical results.
9. `https://eprints.gla.ac.uk/278306/` — 2022 predecessor's metadata. Record labels its accepted-version file restricted to repository staff; that PDF was not requested or read. No predecessor DOI verified.

**Discovery searches, negative results and failed access:**

10. `https://www.google.com/search?q=%22Investors+Are+%28Not%29+Always+Right%22` — JavaScript/access fallback page, no usable search results.
11. `https://www.google.com/search?q=%22Investors+Are%22+%22Profitability-Based%22&gbv=1` — again no usable results.
12. `https://www.bing.com/search?q=%22Investors+Are+%28Not%29+Always+Right%22` — said no results; contradicted as a discovery outcome by successful ACM/Crossref verification, not evidence of paper absence.
13. `https://www.bing.com/search?q=%22Investors%22+%22Sanz-Cruzado%22` — returned unrelated YouTube-help results; not used for academic claims.
14. `https://dl.acm.org/doi/pdf/10.1145/3780097` — **HTTP 403** via webfetch. Fulltext access recovered through official HTML and the institution's published PDF; no final fulltext access gap remains.
15. `https://export.arxiv.org/api/query?search_query=ti:%22Investors%20Are%22&max_results=5` — broad/unhelpful results, no matching paper in returned entries.
16. `https://export.arxiv.org/api/query?search_query=ti:profitability%20AND%20au:Sanz-Cruzado&max_results=10` — zero results.
17. `https://export.arxiv.org/api/query?search_query=ti:Transaction-Based%20AND%20ti:Profitability-Based&max_results=5` — zero results.
18. `https://export.arxiv.org/api/query?search_query=ti:Investors%20AND%20ti:Metrics&max_results=10` — zero results.
19. `https://arxiv.org/search/?query=Investors+Are+%28Not%29+Always+Right&searchtype=title&abstracts=show&order=-announced_date_first&size=50` — no results.
20. `https://arxiv.org/search/?query=profitability&searchtype=title&abstracts=show&order=-announced_date_first&size=50` — overly broad, first page of 505 results; not exhaustively read or used to prove absence.
21. `https://arxiv.org/search/?query=Sanz-Cruzado%2C+Javier&searchtype=author&abstracts=show&order=-announced_date_first&size=100` — three results (other financial papers, including FAR-Trans), not the named study. This search does not rule out all alternative author-name indexing.
22. `https://eprints.gla.ac.uk/cgi/search/simple?q=Investors+Are+Not+Always+Right&_action_search=Search&_order=bytitle&basic_srchtype=ALL&_satisfyall=ALL` — broad irrelevant results, first page did not locate target.
23. `https://eprints.gla.ac.uk/cgi/search/simple?q=%22Transaction-Based%22&_action_search=Search` — successful discovery of 2026 article and 2022 predecessor.
24. `https://api.datacite.org/dois?query=titles.title:%22Investors%20Are%22&page[size]=10` — 13 total results, first 10 unrelated; then narrowed rather than assuming exhaustive absence.
25. `https://api.datacite.org/dois?query=titles.title:%22Investors%20Are%20%28Not%29%20Always%20Right%22&page[size]=25` — zero exact-title results; no separate preprint DOI verified.

#### Remaining evidence boundaries

- No direct estimate is available from this paper for LLM-summary uplift, sparse-user uplift, or the effect of controlled history representation. Those are the proposed Task2 experiment's unknowns.
- No separately registered preprint DOI/date can be supplied confidently. The verified earlier **Online AM date is 10 December 2025**, the author manuscript carries a December 2025 template, and the final journal DOI is **10.1145/3780097**.
- The FAR-Trans source paper was assigned to a separate researcher and was not reread here. The present dataset claims are specifically verified in this journal article's §6.1 and Data Statement.
- PDF skill was read before attempting PDF retrieval/parsing; no subdelegation was used. Work produced only these evidence notes and temporary retrieval artifacts; no raw data, Task1 outputs, or final homework report were edited.
