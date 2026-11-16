# Reference verification and evidence provenance

**Student:** Abaidullah Seikh  
**Course:** LLM4Rec, HSE University  
**Scope:** Task2 literature preparation; bibliography, version and claim audit.

## What “verified” means in these notes

This file synthesizes the supplied evidence records, which document original-source research on **2026-11-09**. That date is inherited from the records, not a newly invented retrieval date. **This synthesis pass read the five evidence-note files and three Task1 outputs; it did not newly fetch academic pages or parse the PDFs.** “Full text read” below describes the documented earlier research. “Publication metadata verified” means a title/author/venue/DOI check against an official venue, publisher, repository or publisher-deposited Crossref record; it does not mean the final publisher article was read.

The underlying records are [far_trans.md](../research_notes/Sparse%20financial%20recommendation%20literature/far_trans.md), [remaining_studies.md](../research_notes/Sparse%20financial%20recommendation%20literature/remaining_studies.md), [financial_llm_studies.md](../research_notes/Sparse%20financial%20recommendation%20literature/financial_llm_studies.md), [language_profile_studies.md](../research_notes/Sparse%20financial%20recommendation%20literature/language_profile_studies.md), and [financial_evaluation.md](../research_notes/Sparse%20financial%20recommendation%20literature/financial_evaluation.md). All were read, including the continuation of `remaining_studies.md`. Their exact access logs retain failed discovery searches; the source ledger below concentrates on academic evidence, bibliographic corroboration and material access failures.

**AI disclosure:** OpenCode (`openai/gpt-6-astra`) assisted with the literature synthesis and checks against those notes. **Personal paper verification by Abaidullah Seikh is pending.** The user's personal-verification statement covers **transaction7590224 and asset metadata**, not papers, every Task1 statistic, or an independent replication. Existing Task1 boilerplate is not rewritten here; this distinction records the user's clarification. No paper experiment, significance test, code implementation or figure coordinate was independently replicated during synthesis.

### Access-status summary

| Study | Original academic text documented as read | Publication metadata status | Final-text boundary |
|---|---|---|---|
| FAR-Trans | arXiv v1 HTML, main text through conclusion; local PDF first-page identity checked | arXiv, official workshop and institutional record | Workshop acceptance verified; separate proceedings DOI not verified; no claim of a separate publisher version |
| FLARKO | arXiv v1 HTML and local v1 PDF, main methods/results/conclusion | ACM-deposited Crossref and arXiv related DOI | ACM landing/PDF blocked (403); final-version equivalence unchecked |
| ACL UPR | Official published ACL PDF and corresponding local PDF, main text and relevant appendices | Official ACL metadata/PDF | Published full text available and read |
| LangPTune | arXiv v2 HTML/PDF and local v2 PDF, Tables 1–6 and relevant appendices | ACM-deposited Crossref, official CIKM accepted list and author linkage | Final ACM landing/full/PDF blocked (403); v2 findings cannot be labeled verified final CIKM findings |
| Investors | Final ACM HTML; institution's published-version PDF; supplied local published PDF | ACM, Crossref, institutional record and article title block | Final full text read despite direct ACM PDF 403; author manuscript only first two pages read |
| Conv-FinRe | arXiv v1/v2 HTML; findings use v2 | ACM-deposited Crossref; arXiv acceptance/version record | Final ACM pages/PDF blocked (403); author-list and possible text changes unresolved |

## 1. FAR-Trans — selected foundation

**Complete citation:** Javier Sanz-Cruzado, Nikolaos Droukas, and Richard McCreadie. **2024.** *FAR-Trans: An Investment Dataset for Financial Asset Recommendation.* **IJCAI-24 Workshop on Recommender Systems in Finance (Fin-RecSys)**, Jeju, Republic of Korea, **4 August 2024**. Original evidence version: **arXiv:2407.08692v1**, submitted **11 July 2024**. Cite the workshop, not IJCAI main track. No page range or proceedings DOI was verified in the inspected records. ([arXiv](https://arxiv.org/abs/2407.08692); [official workshop](https://sites.google.com/view/fin-recsys2024/); [program](https://sites.google.com/view/fin-recsys2024/program))

**Identifiers:** **10.48550/arXiv.2407.08692** is the **arXiv/preprint DOI**, not a proceedings DOI. **10.5525/gla.researchdata.1658** is the **dataset DOI**, not the paper DOI. The institutional publication record has a June metadata value, whereas the official workshop date is 4 August; the latter is used for the event. Its `Mccreadie` capitalization is normalized to the article's **McCreadie**, not treated as a different author. ([Publication record](https://eprints.gla.ac.uk/id/eprint/328250); [dataset record](https://researchdata.gla.ac.uk/1658/))

**Reading boundary:** `far_trans.md` documents original HTML abstract, introduction, dataset construction, all §5 methods/results including Tables 1–2 and complete §6 conclusion. A second request exposed the conclusion after initial output truncation. `remaining_studies.md` checked the local PDF's first page for identity; it did not claim a second complete PDF reading.

| Claims used | Supporting source locations |
|---|---|
| Data scope; 806 assets, 321 invested assets, 29,090 customers, 388,049 transactions, 228,913 acquisitions, 159,136 sales, 703,303 prices | [§3/Table 1](https://arxiv.org/html/2407.08692v1#S3.T1) |
| Price cleaning; reconstructed initial buys from end-period balance; moved dates and estimated amounts | [§3.1.1](https://arxiv.org/html/2407.08692v1#S3.SS1.SSS1), [§3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1) |
| Over 50% with ≤3 full-period transactions; popularity concentration | [§3.3.2/Fig.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2); prose, not digitized figure bars |
| Estimated customer fields | [§3.4.2–3.4.3](https://arxiv.org/html/2407.08692v1#S3.SS4.SSS2) |
| New-to-user purchase target; binary acquisitions; 61 origins; six-month tests; repeat filtering; eligible users/assets | [§5.1](https://arxiv.org/html/2407.08692v1#S5.SS1), [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1) |
| nDCG@10/monthly ROI@10 definitions; 11 algorithms, price features, ROI-based tuning dates | [§5.2.2](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS2), [§5.2.3](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS3) |
| Complete 11-method results and market/customer references; LightGCN 0.3404, popularity 0.2710, RF ROI 0.0259 | [§5.3/Table 2](https://arxiv.org/html/2407.08692v1#S5.T2) |
| Purchase/profitability distinction and future work | [§6](https://arxiv.org/html/2407.08692v1#S6) |

**Unresolved:** Table 1 says 806 assets while §3.2 says 807; local traded counts differ from the paper. The “unique” transaction-count key is not fully defined. Exact origin list, candidate counts, nested tuning chronology and sparse-specific outcomes are absent from the inspected text. Reconstructed events imply a potential point-in-time issue, not a measured leakage magnitude. Separate publisher DOI **not verified** is not proof that none exists.

## 2. FLARKO — selected same-dataset LLM prior work

**Complete publication citation:** Fernando Spadea and Oshani Seneviratne. **2025.** *Aligning Language Models with Investor and Market Behavior for Financial Recommendations.* In **Proceedings of the 6th ACM International Conference on AI in Finance (ICAIF '25)**, ACM, **509–517**. Conference: **15–18 November 2025**, Singapore. **Publication DOI: [10.1145/3768292.3770399](https://doi.org/10.1145/3768292.3770399)**. ACM-deposited metadata: online **14 November 2025**, print **15 November 2025**. **FLARKO is the framework name**, not a title prefix. ([Crossref](https://api.crossref.org/works/10.1145/3768292.3770399))

**Preprint identity:** same title and two authors, **arXiv:2510.15993v1**, submitted **14 October 2025**; separate **arXiv DOI 10.48550/arXiv.2510.15993**. The local PDF includes an ICAIF bibliographic block and DOI, but it is the **v1 author version used for findings**, not an independently compared final publisher PDF. ([arXiv](https://arxiv.org/abs/2510.15993))

**Reading boundary:** original HTML abstract, §§3–5 method, §§6–7 experiments and complete §8 conclusion; local nine-page PDF main text, Tables 2–4 and results/conclusion. Initial HTML truncation was followed by reading the saved remainder. ACM landing and PDF requests returned 403; Crossref supplies publication metadata, not hidden full-text access.

| Claims used | Supporting source locations |
|---|---|
| PKG transaction fields; MKG metadata/ten-week price aggregates; JSON-LD; 5,000-triple cap; pre-date filtering | [§3.1/Figs.2–3](https://arxiv.org/html/2510.15993v1#S3.SS1), local PDF p.4 |
| Three output ISINs; 180-day purchase-and-positive-return KTO labels | [§3.2](https://arxiv.org/html/2510.15993v1#S3.SS2), [§4](https://arxiv.org/html/2510.15993v1#S4), PDF pp.4–5 |
| Train/test dates, conventional baselines, Hits@3 variants | [§6.1–6.3](https://arxiv.org/html/2510.15993v1#S6.SS1), PDF p.6 |
| Qwen3 sizes, 23,784 examples, LoRA/federated setup | [§6.4–6.5](https://arxiv.org/html/2510.15993v1#S6.SS4), PDF p.6 |
| Centralized PKG/Combined scores; distinct maxima; Nothing Comb@3 0.3718 ± 0.0547 | [§7.1/Table 2](https://arxiv.org/html/2510.15993v1#S7.T2), PDF p.7; ± is standard error of a proportion |
| Federated input-specific results | [§7.2/Tables 3–4](https://arxiv.org/html/2510.15993v1#S7.T3), PDF p.8; follow table captions where prose cross-references conflict |
| Baseline comparison qualitative only; broad conclusion requires qualification | [§7.3/Fig.1](https://arxiv.org/html/2510.15993v1#S7.SS3), [§8](https://arxiv.org/html/2510.15993v1#S8); plot coordinates not digitized |

**Unresolved:** exact per-ablation cohort/candidate parity, hit denominators, repeat policy, invalid/duplicate outputs and validation details. Different standard errors prompt denominator checking; they do not prove different cohorts. “Nothing” is context removal, not an established zero-history cohort. Final publisher equality remains unchecked.

## 3. ACL UPR — selected profile-construction precedent

**Complete publication citation:** Jerome Ramos, Hossein A. Rahmani, Xi Wang, Xiao Fu, and Aldo Lipani. **2024.** *Transparent and Scrutable Recommendations Using Natural Language User Profiles.* In **Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)**, **13971–13984**, Bangkok, Thailand, **August 2024**. Association for Computational Linguistics. **Publication DOI: [10.18653/v1/2024.acl-long.753](https://doi.org/10.18653/v1/2024.acl-long.753)**. Author spelling **Hossein** follows the official ACL page and PDF. ([Official record/BibTeX](https://aclanthology.org/2024.acl-long.753/))

**Separate preprint metadata:** arXiv:2402.05810, v1 **8 February 2024**, v2 **18 July 2024**; **arXiv DOI 10.48550/arXiv.2402.05810**. The arXiv metadata spells the second author's given name **Hossen**. This discrepancy is recorded, not propagated into the verified publication citation. The ACL identifier is not an arXiv ID. ([arXiv record](https://arxiv.org/abs/2402.05810))

**Reading boundary:** official fourteen-page published PDF and corresponding local file; abstract, §§3–4 methods/setup, §§5.1–5.4 results, conclusion/limitations/ethics and relevant Appendix A prompts, implementation and edits. This is published full-text evidence, not an abstract-only reading.

| Claims used | Supporting sections/pages in [official PDF](https://aclanthology.org/2024.acl-long.753.pdf) |
|---|---|
| Feature extraction/ranking; Llama2/Mistral profiles; GPT-2 rating regression | §§3.2–3.4, 4.4; pp.13974–13976 |
| Five features/five reviews/200 tokens and implementation | §4.4; Appendix A.1–A.3, p.13981 |
| Dataset sizes, 8:1:1 split, ≥5 training reviews, all users/items in all splits | §4.1/Table 1, p.13975 |
| RMSE/MAE/MAP and condensed rated-test-item nDCG@10 | §4.2, p.13975 |
| MF 0.941/0.960 vs UPR Llama2 0.938/0.955 and Mistral 0.940/0.952 | §5.1/Table 2, p.13977 (physical PDF p.7) |
| Five annotators, fifty profiles/domain, 90%/87% relevance | §5.3/Table 3, pp.13977–13978 |
| 200 users, 100+100 item lists, five-seed edit/coverage experiment | §5.4, p.13978; Appendix A.5–A.6, p.13982 |
| Hallucination, review dependence, bottleneck and negative-preference limits | §5.3; §§6–8, pp.13978–13979 |

**Unresolved:** global split chronology and point-in-time construction of review features/profiles were not code-audited. Prose describes rating aggregation as an average while Eq.(1) prints a sum; no implementation resolution is assumed. UPR's ranking results are not all-catalog purchase nDCG, and Table 2 does not establish statistical equivalence with MF. No final-text access gap remains.

## 4. LangPTune — selected nearest methodological prior work

**Complete publication citation:** Zhaolin Gao, Joyce Zhou, Yijia Dai, and Thorsten Joachims. **2025.** *LangPTune: Optimizing Language-based User Profiles for Recommendation.* In **Proceedings of the 34th ACM International Conference on Information and Knowledge Management (CIKM '25)**, ACM, **707–717**, Seoul, Republic of Korea. **Publication DOI: [10.1145/3746252.3761369](https://doi.org/10.1145/3746252.3761369)**. ACM-deposited online/print publication date: **10 November 2025**. The official accepted-paper list includes the exact title and all four authors under **fp8779**. ([Crossref](https://api.crossref.org/works/10.1145/3746252.3761369); [CIKM accepted papers](https://cikm2025.org/program/accepted-papers))

**Complete evidence-version citation:** Zhaolin Gao, Joyce Zhou, Yijia Dai, and Thorsten Joachims. **2025 [v2; first submitted 2024].** *End-to-end Training for Recommendation with Language-based User Profiles.* **arXiv:2410.18870v2**, **12 February 2025**; v1 **24 October 2024**. Separate **arXiv DOI: 10.48550/arXiv.2410.18870**. The author page and repository connect the earlier title/arXiv record to the CIKM work. The local `2410.18870v2.pdf` title must remain the earlier title. ([arXiv history](https://arxiv.org/abs/2410.18870); [author page](https://zhaolingao.github.io/); [repository](https://github.com/ZhaolinGao/LangPTune))

**Reading boundary:** original v2 HTML and PDF, including abstract, §§3–4, Tables 1–6, §5 conclusion, Appendix A inputs and Appendix B hyperparameters. Final ACM landing, `/doi/full/` and PDF requests returned **403**. Publication metadata is verified, but **all reported experimental numbers are v2 results**. The preprint's 2018/Woodstock/template DOI fields are placeholders, not valid publication metadata.

| Claims used | Supporting v2 locations |
|---|---|
| LLM profile encoder, Mxbai inner-product decoder, RLSO/CL alternating optimization | [§§3.1–3.2/Eqs.1–10/Algorithm 1](https://arxiv.org/html/2410.18870v2#S3), pp.2–4 |
| Metadata/review inputs; 4 historical + 1 future distinct item; length and ≥5-interaction filtering | [§4.1](https://arxiv.org/html/2410.18870v2#S4.SS1), pp.4–5; [Appendix A](https://arxiv.org/html/2410.18870v2#A1) |
| Session/item counts; Recall/MRR/NDCG@20; baseline observed-context access | [Table 1](https://arxiv.org/html/2410.18870v2#S4.T1), §4.2/footnote 1, p.5 |
| Frozen versus trained components; same architecture ≠ same learned weights | §§4.2–4.3, pp.5–6; Appendix B, pp.13–14 |
| Llama Movie-TV 0.0231→0.0494; Gemma Books 0.1743→0.2736; relative improvements are training gains | [§4.4.1/Table 2](https://arxiv.org/html/2410.18870v2#S4.T2), p.6 |
| Movie-TV LightGCN 0.0525, MCL 0.0563; Books LightGCN 0.2586 vs LangPTune 0.2736 | [§4.4.2/Table 3](https://arxiv.org/html/2410.18870v2#S4.T3), p.7 |
| Direct history and profile lengths; **NoProfile-CL 0.0543 > 512-token profile 0.0494** | [§4.5.1/Table 4](https://arxiv.org/html/2410.18870v2#S4.T4), p.7; NDCG@20, Movie-TV/Llama |
| Frozen Mxbai partial control: NoProfile-0 0.0372, profile-0 0.0231, profile-RLSO 0.0377 | Tables 2/4; §§4.2.1, 4.5.1, 4.7; exact pairwise significance and input parity unestablished |
| Global training-size ablation, not per-user sparse strata | [§4.5.2/Fig.4](https://arxiv.org/html/2410.18870v2#S4.SS5.SSS2), p.7; no curve coordinates digitized |
| Human choice 57.11%/54.67%/58.89%; p=0.201 and p=0.624; reading times | [§4.6/Tables 5–6](https://arxiv.org/html/2410.18870v2#S4.SS6), pp.7–8 |
| Conclusion and longer-history/steerability future work | [§5](https://arxiv.org/html/2410.18870v2#S5), p.8 |

**Unresolved:** final CIKM table equivalence; NoProfile versus generator review-field parity; truncation/masking; global time split; metadata snapshot timing; exact adapter/training comparability. NoProfile consumes raw item-metadata text, not a conventional tabular buy/sell/count/recency vector. Full LangPTune and NoProfile-CL have different fitted weights and training settings. Table 4's **−0.0049**, approximately **−9.0%** profile disadvantage is derived arithmetic, not a reported significance result.

## 5. Investors — selected metric-interpretation source

**Complete publication citation:** Javier Sanz-Cruzado, Richard McCreadie, Nikolaos Droukas, Craig Macdonald, and Iadh Ounis. **2026.** *Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations.* **ACM Transactions on Information Systems 44(2), Article 51, 56 pages**. **Publication DOI: [10.1145/3780097](https://doi.org/10.1145/3780097)**. Title ends in plural **Recommendations**. ([ACM](https://dl.acm.org/doi/10.1145/3780097); [Crossref](https://api.crossref.org/works/10.1145/3780097))

**Chronology:** received **22 January 2025**; revised **14 September 2025**; accepted **2 December 2025**; online accepted manuscript **10 December 2025**; final online publication **28 January 2026**; **February 2026** issue (Crossref print date **28 February**). The repository deposit of **5 December 2025** is not the final publication date. The author's manuscript has December 2025 placeholders and no populated DOI; only its first two pages were read. No separate arXiv/preprint DOI was verified. The **2022 workshop predecessor** is a distinct earlier paper, not a 2025 preprint of this article. ([ACM publication history](https://dl.acm.org/doi/10.1145/3780097); [repository](https://eprints.gla.ac.uk/373432/); [author manuscript](https://javiersanzcruza.github.io/assets/papers/tois2025.pdf); [2022 record](https://eprints.gla.ac.uk/278306/))

**Reading boundary:** final publisher HTML main text through conclusion/limitations/Data Statement, relevant statistical appendix, institution's explicitly labeled published PDF for corroboration, and supplied local PDF. Earlier research inspected appendix evidence, but did not independently audit all proofs/significance matrices. Direct ACM PDF access failed, **not final full-text access as a whole**. `373432.pdf` has an ACM download cover plus 56 article pages; its cover calls the underlying file `3780097.pdf`. Printed **51:n corresponds to physical PDF page n+1**. The cover's odd expanded McCreadie name is not used; article title block/ACM/Crossref agree on **Richard McCreadie**.

| Claims used | Supporting final-publication locations |
|---|---|
| Formal task and metric families; zero correlation under all-valid-user/ranking construction | [§§3–5, Theorem 5.6/Eqs.1–6](https://dl.acm.org/doi/10.1145/3780097#sec-5-3), pp.51:9–51:16 |
| FAR-Trans, 61 temporal variants, six months, date span and eligibility | [§6.1/Table 3/Fig.2](https://dl.acm.org/doi/10.1145/3780097#sec-6-1), pp.51:17–51:18 |
| Binary nDCG and `(1+ROI)^(30/days)−1` monthly conversion | [§6.2/Eqs.7–12](https://dl.acm.org/doi/10.1145/3780097#sec-6-2), pp.51:19–51:20 |
| Twelve algorithms including CPS; ROI-selected hyperparameters | [§6.3/Table 4](https://dl.acm.org/doi/10.1145/3780097#sec-6-3), pp.51:20–51:21 |
| Pooled r=−0.13, ~1.5 million observations, reported p<0.05 | [§7/Fig.4(b)](https://dl.acm.org/doi/10.1145/3780097#sec-7), p.51:23; Appendix C.2/Table C5 |
| LightGCN/popularity/RF values repeat original benchmark; CPS 0.2722/0.0026 | [§8.1/Table 5](https://dl.acm.org/doi/10.1145/3780097#tab5), p.51:24 |
| Ten synthetic effective-investor datasets, r=+0.13 | [§9.2/Fig.7](https://dl.acm.org/doi/10.1145/3780097#sec-9-2), p.51:31; hindsight-informed synthetic construction |
| Date-specific r≈−0.65 to +0.4; additional horizons 1/3/9/12 months | [§10/Fig.8](https://dl.acm.org/doi/10.1145/3780097#sec-10), p.51:32; §11/Figs.12–13, pp.51:36–51:37 |
| Keep transaction evaluation but distinguish returns; partial portfolios, omitted income, unshared demographic data | [§12/limitations](https://dl.acm.org/doi/10.1145/3780097#sec-12), [Data Statement](https://dl.acm.org/doi/10.1145/3780097#sec-13), pp.51:38–51:41 |

**Unresolved:** literal compatibility of 61 dates/two-week spacing/August 2019–November 2021; nested tuning chronology; correlated observations in pooled tests; public reproducibility of CPS. Table 5's market monthly ROI **0.0079** differs from Table 6's average asset monthly ROI **0.004259**; different aggregation is a hypothesis, not a verified reconciliation. The synthesis does not merge these baselines. Theorem terminology is attributed: zero covariance is not generally sufficient for statistical independence.

## 6. Conv-FinRe — investigated alternative

**Complete publication citation (13-author publisher-deposited list):** Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, **Yuqing Guo**, Fengran Mo, Jimin Huang, Yankai Chen, and Jian-Yun Nie. **2026.** *Conv-FinRe: A Conversational and Longitudinal Benchmark for Utility-Grounded Financial Recommendation.* In **Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '26)**, ACM, **3448–3455**, Melbourne, VIC, Australia. **Publication DOI: [10.1145/3805712.3808658](https://doi.org/10.1145/3805712.3808658)**. Online **19 July 2026**, print **20 July 2026**. This bibliography is verified against the ACM Crossref deposit, **not a blocked final PDF title page**. ([Publication metadata](https://api.crossref.org/works/10.1145/3805712.3808658))

**Complete arXiv v2 citation (14-author list):** Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, **Rosie Guo**, Fengran Mo, Jimin Huang, Yankai Chen, **Xue Liu**, and Jian-Yun Nie. **2026.** *Conv-FinRe: A Conversational and Longitudinal Benchmark for Utility-Grounded Financial Recommendation.* **arXiv:2602.16990v2**, **17 May 2026**; first submission **19 February 2026 UTC**. HTML styles Xue Liu as **Xue (Steve) Liu**. **arXiv DOI: 10.48550/arXiv.2602.16990**. The arXiv comment says accepted by the SIGIR 2026 Resource Track, pre-camera-ready. ([arXiv history](https://arxiv.org/abs/2602.16990); [v2 title block](https://arxiv.org/html/2602.16990v2))

**Unresolved author conflict:** no evidence establishes whether Yuqing and Rosie refer to the same person or why Xue Liu is absent from the publication record. Do not merge, silently substitute or “correct” either list. A search display's 18 February date does not override the arXiv record's explicit 19 February UTC timestamp. The HTML's 2018 Woodstock/`XXXXXXX.XXXXXXX` ACM template fields are not publication evidence.

**Reading boundary:** both original arXiv v1/v2 HTML main texts were opened; **v2** supplies all findings here, including complete §§3–5 and Tables 2–5. Reference-list truncation occurred after the main text. No supplied project PDF was mapped to this study. ACM landing/abstract/PDF requests returned 403; publication changes and author reconciliation remain unchecked. The author GitHub README was read as moving `main`, not a commit-pinned code audit; `ConvFinRe` is its task-name spelling.

| Claims used | Supporting v2 locations |
|---|---|
| Fixed-candidate reranking, advisor views, full-trajectory inverse-fitted utility | [§§3.1–3.2/Eqs.1–6](https://arxiv.org/html/2602.16990v2#S3.SS1) |
| Ten participants/ten stocks; simulator choices, generated dialogues; stated 30 days and 6 Aug–17 Sep 2025 | [§3.3.1–3.3.2/Table 2](https://arxiv.org/html/2602.16990v2#S3.SS3) |
| 23 steps/user, 230 instances, 270 unique/3,450 expanded turns | [Table 3](https://arxiv.org/html/2602.16990v2#S3.T3) |
| uNDCG, choice MRR/HR and Kendall τ; model list and caps | [§§3.4–3.5](https://arxiv.org/html/2602.16990v2#S3.SS4) |
| Llama-3.3 uNDCG 0.97 ± 0.00; XuanYuan3 MRR 0.65 ± 0.03, HR@1 0.54 ± 0.03; random 1,000 permutations | [§4.1/Table 4](https://arxiv.org/html/2602.16990v2#S4.T4) |
| Advisor correlations; model-dependent history/no-history response | [§4.2/Table 5](https://arxiv.org/html/2602.16990v2#S4.T5), [§4.3/Figs.2–3](https://arxiv.org/html/2602.16990v2#S4.SS3) |
| Distinct behavioral and utility alignment conclusion | [§5](https://arxiv.org/html/2602.16990v2#S5) |

**Unresolved:** uncertainty estimator for printed ±, generation details, prefix-only provenance after full-trajectory utility fitting, and signed-utility/IDCG treatment. Ten stocks do not establish the prose's “all eleven GICS sectors” claim. The stated 30-day horizon is not inferred to mean thirty consecutive calendar days. History removal is not information-equivalent representation control. uNDCG is not purchase-relevance nDCG@10.

## Local PDF identity and version mapping

The mappings below were established in `remaining_studies.md` from file title blocks/content, not merely filenames. Paths are relative to the project root; the files were not altered for this synthesis.

| Local file | Actual identity/version | Evidentiary treatment |
|---|---|---|
| `2407.08692v1.pdf` | *FAR-Trans: An Investment Dataset for Financial Asset Recommendation*, arXiv v1, 11 July 2024 | First page checked locally; full-text claims from documented v1 HTML reading |
| `2510.15993v1.pdf` | *Aligning Language Models with Investor and Market Behavior for Financial Recommendations*, FLARKO, arXiv v1, 14 October 2025; 9 pages | Local main text read; ICAIF block/DOI does not certify final publisher equality |
| `2024.acl-long.753.pdf` | *Transparent and Scrutable Recommendations Using Natural Language User Profiles*, ACL published version; 14 pages, 13971–13984 | Published text read; author spelling follows this and official ACL record |
| `2410.18870v2.pdf` | **End-to-end Training for Recommendation with Language-based User Profiles**, 12 February 2025 arXiv v2 | LangPTune method, earlier title; every experimental table cited as v2 |
| `373432.pdf` | *Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations*, TOIS 44(2), Article 51, 2026 | Published version; 57 physical pages including cover; `373432` is not an arXiv ID |
| No supplied PDF mapped | Conv-FinRe, arXiv v2 | Original HTML evidence; final SIGIR metadata separately verified |

## URLs actually opened in the documented research

The following are **successful source requests recorded in the evidence notes**, not claims of new requests in this writing pass. Section/table fragments used above are internal locators and need not have been fetched separately. Canonical DOI hyperlinks are identifiers; a clickable DOI alone does not demonstrate successful retrieval. The ledger is selective for evidence-bearing sources; complete discovery/failure logs remain in the linked research notes.

### FAR-Trans source ledger

| Exact requested URL | Recorded outcome/use |
|---|---|
| https://arxiv.org/abs/2407.08692 | Success: title, authors, version, workshop comment and arXiv DOI |
| https://arxiv.org/html/2407.08692v1 | Success: original main text/Tables 1–2; initial output truncated late |
| https://arxiv.org/html/2407.08692v1#S6 | Success: complete conclusion recovered in text-format article response |
| https://sites.google.com/view/fin-recsys2024/ | Success: workshop date/location |
| https://sites.google.com/view/fin-recsys2024/program | Success: accepted paper entry |
| https://researchdata.gla.ac.uk/1658/ | Success: dataset DOI, collection dates, license and publication linkage; ZIP not downloaded |
| https://eprints.gla.ac.uk/id/eprint/328250 | Success: institutional publication BibTeX; no separate DOI field |
| https://doi.org/10.5525/gla.researchdata.1658 | HTTP 500 on attempted resolution; underlying data record recovered directly |

### FLARKO and Conv-FinRe source ledger

| Exact requested URL | Recorded outcome/use |
|---|---|
| https://arxiv.org/abs/2510.15993 | Success: FLARKO metadata/version and related publication DOI |
| https://arxiv.org/html/2510.15993v1 | Success: original FLARKO main text; saved remainder read through conclusion |
| https://api.crossref.org/works/10.1145/3768292.3770399 | Success: ACM-deposited title, authors, venue/pages/dates/DOI |
| https://dl.acm.org/doi/10.1145/3768292.3770399 | HTTP 403; publisher landing unavailable |
| https://dl.acm.org/doi/pdf/10.1145/3768292.3770399 | HTTP 403; publisher PDF unavailable |
| https://arxiv.org/abs/2602.16990 | Success: Conv-FinRe arXiv authors, dates, acceptance and DOI |
| https://arxiv.org/html/2602.16990v1 | Success: original v1 main text |
| https://arxiv.org/html/2602.16990v2 | Success: original v2 main text/conclusion; source for findings |
| https://api.crossref.org/works/10.1145/3805712.3808658 | Success: publication metadata and distinct 13-author list |
| https://github.com/The-FinAI/Conv-FinRe | Success: README/task spelling/resources; no implementation audit |
| https://dl.acm.org/doi/10.1145/3805712.3808658 | HTTP 403 |
| https://dl.acm.org/doi/abs/10.1145/3805712.3808658 | HTTP 403 |
| https://dl.acm.org/doi/pdf/10.1145/3805712.3808658 | HTTP 403; final full text not obtained |

### UPR and LangPTune source ledger

| Exact requested URL | Recorded outcome/use |
|---|---|
| https://aclanthology.org/2024.acl-long.753/ | Success: official publication metadata/BibTeX |
| https://aclanthology.org/2024.acl-long.753.pdf | Downloaded/read: published full text |
| https://arxiv.org/abs/2402.05810 | Opened: preprint dates/DOI and Hossen/Hossein metadata discrepancy; results use ACL PDF |
| https://arxiv.org/abs/2410.18870 | Success: earlier title, authors, v1/v2 chronology and arXiv DOI |
| https://arxiv.org/html/2410.18870v2 | Opened/read: original v2 methods, results and conclusion |
| https://arxiv.org/pdf/2410.18870v2 | Downloaded/read: original v2 PDF |
| https://api.crossref.org/works?query.title=LangPTune&rows=2 | Success: matching CIKM publication record |
| https://api.crossref.org/works/10.1145/3746252.3761369 | Successfully retrieved with curl in language-profile research: ACM-deposited metadata |
| https://cikm2025.org/program/accepted-papers | Opened: official title/all authors, fp8779 |
| https://cikm2025.org/ | Opened: conference/proceedings announcement |
| https://zhaolingao.github.io/ | Opened: author linkage of older title and CIKM acceptance |
| https://github.com/ZhaolinGao/LangPTune | Success: author repository/arXiv linkage; no execution/code audit |
| https://dl.acm.org/doi/10.1145/3746252.3761369 | HTTP 403; metadata verification is not landing-page reading |
| https://dl.acm.org/doi/full/10.1145/3746252.3761369 | HTTP 403 reported for full-text endpoint |
| https://dl.acm.org/doi/pdf/10.1145/3746252.3761369 | HTTP 403; final PDF not obtained |

### Investors source ledger

| Exact requested URL | Recorded outcome/use |
|---|---|
| https://api.crossref.org/works/10.1145/3780097 | Success: final publication metadata |
| https://dl.acm.org/doi/10.1145/3780097 | **Success: final original HTML**, main evidence and publication history |
| https://doi.org/10.1145/3780097 | Success: matching formatted citation |
| https://eprints.gla.ac.uk/373432/ | Success: record, version label and deposit date |
| https://eprints.gla.ac.uk/373432/2/373432.pdf | Downloaded/parsed: explicitly labeled published version; exact numerical/page corroboration |
| https://javiersanzcruza.github.io/ | Opened: author acceptance announcement; talk date not treated as publication |
| https://javiersanzcruza.github.io/pubs | Opened: author manuscript/final DOI/predecessor links |
| https://javiersanzcruza.github.io/assets/papers/tois2025.pdf | Downloaded; **first two pages only** read; December 2025 placeholder front matter |
| https://eprints.gla.ac.uk/278306/ | Opened: distinct 2022 predecessor metadata; restricted PDF not read |
| https://dl.acm.org/doi/pdf/10.1145/3780097 | HTTP 403; recovered final text through HTML and published repository PDF |

Search snippets, irrelevant search results and failed title queries were not used as method/result evidence. No metadata access is upgraded into a claim of reading final text. Additional predecessors mentioned in these papers were not fully investigated as part of this six-study synthesis.

## Local measurements and unresolved cross-source differences

The following are read from existing Task1 outputs, **not remeasured**. They do not establish the eventual train/test population. The user verification of a transaction and metadata does not resolve publication discrepancies.

| Claim used | Local source/definition | Relation to literature |
|---|---|---|
| 388,048 transaction rows; 228,913 Buys; 159,135 Sells; 29,090 customers | [dataset_inventory.md](dataset_inventory.md), “Customers, assets and transactions”; header excluded | Paper Table 1: 388,049 / 228,913 / 159,136 / 29,090. One header explains a possible counting difference arithmetically, not its actual cause |
| 320 traded ISINs; 806 metadata ISINs; 807 price ISINs | Same inventory | Paper Table 1: 321 invested/806 unique; paper prose also says 807. Definitions/snapshot differences unresolved |
| Transactions through 2022-11-30; prices through 2022-11-29 | [data_quality_analysis.md](data_quality_analysis.md), date table | Institutional collection interval ends 2022-11-29; retain source-specific dates |
| Median total events 3; median Buys 2; 1–3: 21,237/73.00%; 1–5: 23,663/81.34%; 1–10: 25,736/88.47% | [sparse_user_analysis.md](sparse_user_analysis.md), full-release event counts and overlapping Buy bands | Paper's “over 50% ≤3” counts all transactions, not Buy events or pre-cutoff cohort membership |
| 360 customers with 1–5 Buys have >10 total events | Same sparse analysis | Purchase-sparse and total-history-sparse are different |
| 388 sector blanks and 439 industry blanks across 836 metadata rows; 3 repeated ISIN/date keys | [data_quality_analysis.md](data_quality_analysis.md), missing/key tables | Row-level quality context; not missing-user counts; summaries must preserve missingness/conflicts |
| 12,501 profile rows have questionnaire date after snapshot timestamp | Same data-quality file, “Customer-profile provenance and timing” | Timestamp-only availability is insufficient; this is not proof of a specific experimental leakage effect |

No local event is classified as reconstructed from its date alone: the raw schema has no explicit provenance flag. Institutional metadata last modification on 18 February 2026 does not establish byte equality with the authors' 2024 experimental snapshot. Task1's archive consistency establishes local integrity, not external snapshot identity.

## Cross-check record and remaining verification

The selected references have complete author lists checked against the evidence notes; official publication titles/venues are separated from manuscript titles. Every numerical table in [literature_review.md](literature_review.md) has a source/version/metric locator. In particular: FAR-Trans ROI is monthly; UPR nDCG@10 is condensed-list; LangPTune's **0.0543 versus 0.0494 is NDCG@20 in v2 Table 4**; FLARKO uses Hits@3 variants and proportion standard errors; Investors' −0.13 pools user–algorithm–date observations; Conv-FinRe uNDCG uses utility gain and unspecified ± semantics.

The evidence supports neither “all papers show summaries outperform structured histories” nor a literature-wide first-ever claim. Pending verification includes the student's own paper checks, final LangPTune/FLARKO/Conv-FinRe text equivalence, Conv-FinRe author reconciliation, and implementation details identified above. These are specific evidence boundaries, not fabricated negative findings or a new class protocol.
