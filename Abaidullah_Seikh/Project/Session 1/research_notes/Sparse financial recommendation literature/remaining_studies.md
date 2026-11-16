# Remaining studies: sparse financial recommendation literature

## 1. Which papers, local files, and publication identifiers were verified?

### Takeaway

All four remaining supplied PDFs were identified from their title blocks and read for abstract, methods, experiments, and conclusion. LangPTune's local arXiv title differs from its verified CIKM 2025 publication title; the financial-evaluation PDF is the published TOIS 2026 article. The alternative is spelled **Conv-FinRe**, with a verified SIGIR 2026 publication DOI and accessible arXiv full text. Publication identifiers and the versions supplying experimental evidence are distinguished below. [LangPTune publisher-deposited metadata](https://api.crossref.org/works?query.title=LangPTune&rows=2); [TOIS metadata](https://api.crossref.org/works/10.1145/3780097); [Conv-FinRe metadata](https://api.crossref.org/works/10.1145/3805712.3808658)

### Cited Findings

#### Scope, provenance, and reading record

- Research date: **2026-11-09**. User-supplied RQ: **Do LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?** The official class split is pending. These are assignment constraints, not paper findings.
- User provenance: the user has personally verified **transaction7590224 and asset metadata only**, not these papers. Paper verification below was performed during this research. No raw data, Task 1 outputs, PDF sources, or existing research notes were edited; no models were trained and no final homework report was produced.
- Read the requested `deep-research/references/researcher.md` first, then the PDF skill. Extracted the four remaining local PDFs with `pdftotext -layout` into temporary files under `/tmp/opencode/`. No paper download was needed for them. Existing temporary files and existing notes other than `far_trans.md` were not treated as evidence for this research.
- Read existing `research_notes/Sparse financial recommendation literature/far_trans.md` to carry forward already-completed FAR-Trans research. Read only the FAR-Trans local PDF's first page to confirm its identity; its earlier full-text research remains in that file.
- **FLARKO:** read all main-text sections, abstract, §§3–6 methods/setup, Tables 2–4 and §7 results, and §8 conclusion from local `2510.15993v1.pdf` (9 pages). [Corresponding version](https://arxiv.org/abs/2510.15993v1)
- **ACL/UPR:** read abstract, §§3–4 methodology/setup, §§5.1–5.4 results, Tables 1–3, §§6–8 conclusion/limitations, and Appendix A prompts/implementation/editing details from local `2024.acl-long.753.pdf` (14 pages, printed pp. 13971–13984). [Official full text](https://aclanthology.org/2024.acl-long.753.pdf)
- **LangPTune:** read abstract, §§3–4 methods/experiments, Tables 1–6, §5 conclusion, Appendix B hyperparameters and inspected prompt/split references in the extracted local `2410.18870v2.pdf`. Experimental claims below belong to **arXiv v2, 12 February 2025**, not an assumed identical final CIKM version. [Version record](https://arxiv.org/abs/2410.18870v2)
- **Investors:** read abstract, task/metric formulation §§3–5 including Theorem 5.6 and its main-text proof sketch, experimental setup §6, §7 results, §8.1/Table 5, §§9.2–11 follow-up experiment descriptions/results, and full §12 conclusion/limitations/data statement in local `373432.pdf`. The file has an ACM cover page followed by 56 article pages; printed `51:n` corresponds to PDF page `n+1`. Appendix proofs and all appendix significance matrices were not independently audited. [Published article DOI](https://doi.org/10.1145/3780097)
- **Conv-FinRe:** no supplied PDF corresponds to this study. Read accessible arXiv **v2** HTML abstract, complete §§3–4, Tables 2–5, and §5 conclusion. Output truncation occurred in references, after the complete main text. [Full text](https://arxiv.org/html/2602.16990v2)

#### Local PDF identification

| Local file in project root | Identification from file contents | Evidence version/status |
|---|---|---|
| `2407.08692v1.pdf` | **FAR-Trans: An Investment Dataset for Financial Asset Recommendation** | 11 July 2024 arXiv v1; already researched in `far_trans.md`; first-page identity checked here. [Record](https://arxiv.org/abs/2407.08692) |
| `2510.15993v1.pdf` | **Aligning Language Models with Investor and Market Behavior for Financial Recommendations**; framework name FLARKO | 14 October 2025 arXiv v1; title page contains ICAIF '25 bibliographic block and ACM DOI. [Record](https://arxiv.org/abs/2510.15993) |
| `2024.acl-long.753.pdf` | **Transparent and Scrutable Recommendations Using Natural Language User Profiles**; method UPR | ACL 2024 published long paper. [Official record](https://aclanthology.org/2024.acl-long.753/) |
| `2410.18870v2.pdf` | **End-to-end Training for Recommendation with Language-based User Profiles**; method LangPTune | February 2025 arXiv v2, earlier title of the CIKM 2025 study. [arXiv](https://arxiv.org/abs/2410.18870); [published-title metadata](https://api.crossref.org/works?query.title=LangPTune&rows=2) |
| `373432.pdf` | **Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations** | ACM TOIS 44(2), Article 51, published 2026; filename is not an arXiv identifier. Cover itself says `3780097.pdf`. [DOI metadata](https://api.crossref.org/works/10.1145/3780097) |

#### Verified bibliography: complete authors and distinct identifiers

1. **Fernando Spadea and Oshani Seneviratne. 2025. _Aligning Language Models with Investor and Market Behavior for Financial Recommendations._** In *Proceedings of the 6th ACM International Conference on AI in Finance* (ICAIF '25), pp. **509–517**. **Publication DOI: `10.1145/3768292.3770399`**. Online publication **14 November 2025**, print date **15 November 2025** in publisher-deposited Crossref metadata; local title block gives conference **15–18 November 2025, Singapore**. This is a published conference paper, not merely an unreviewed preprint. **Separate arXiv DOI: `10.48550/arXiv.2510.15993`**, v1 submitted 14 October 2025. FLARKO is the framework name, not an extra word at the beginning of the official title. [Crossref/ACM deposit](https://api.crossref.org/works/10.1145/3768292.3770399); [arXiv record with related publication DOI](https://arxiv.org/abs/2510.15993); [publisher URL](https://dl.acm.org/doi/10.1145/3768292.3770399)

2. **Jerome Ramos, Hossein A. Rahmani, Xi Wang, Xiao Fu, and Aldo Lipani. 2024. _Transparent and Scrutable Recommendations Using Natural Language User Profiles._** In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. **13971–13984**, Bangkok, Thailand, August 2024. Publisher: Association for Computational Linguistics. **Publication DOI: `10.18653/v1/2024.acl-long.753`**. Exact author spelling **Hossein** is verified against ACL and the PDF; the LangPTune bibliography's `Hossen` is not propagated. No arXiv DOI is needed for this citation, and an ACL paper ID must not be mistaken for one. [Official ACL bibliography/BibTeX](https://aclanthology.org/2024.acl-long.753/); [DOI](https://doi.org/10.18653/v1/2024.acl-long.753)

3. **Zhaolin Gao, Joyce Zhou, Yijia Dai, and Thorsten Joachims. 2025. _LangPTune: Optimizing Language-based User Profiles for Recommendation._** In *Proceedings of the 34th ACM International Conference on Information and Knowledge Management* (CIKM '25), pp. **707–717**, Seoul, Republic of Korea. **Publication DOI: `10.1145/3746252.3761369`**; online/print publication **10 November 2025** in the ACM Crossref deposit. **Separate preprint:** same four authors, _End-to-end Training for Recommendation with Language-based User Profiles_, arXiv:2410.18870, first submitted **24 October 2024**, v2 **12 February 2025**; **arXiv DOI `10.48550/arXiv.2410.18870`**. The local text explicitly introduces LangPTune, and the author repository links this arXiv record. Do not title the local v2 PDF as if its title page already contained the final CIKM title. [ACM-deposited record](https://api.crossref.org/works?query.title=LangPTune&rows=2); [publisher URL](https://dl.acm.org/doi/10.1145/3746252.3761369); [arXiv record](https://arxiv.org/abs/2410.18870); [author repository](https://github.com/ZhaolinGao/LangPTune)

4. **Javier Sanz-Cruzado, Richard McCreadie, Nikolaos Droukas, Craig Macdonald, and Iadh Ounis. 2026. _Investors Are (Not) Always Right: A Comparison of Transaction-Based and Profitability-Based Metrics for Financial Asset Recommendations._** *ACM Transactions on Information Systems* **44(2), Article 51, 56 pages**. **Publication DOI: `10.1145/3780097`**. Published online **28 January 2026**; issue/print metadata **February 2026** (Crossref gives 28 February). Local cover additionally records accepted **2 December 2025** and online accepted manuscript **10 December 2025**. Cite **2026** for the published article, not 2025 based on the accepted-manuscript date. The article's title block and Crossref use **Richard McCreadie**, whereas the automated cover renders `RICHARD M C MCCREADIE`; retain the article author form. No arXiv DOI was verified for this article. Dataset DOI `10.5525/gla.researchdata.1658` identifies data, not this article. [ACM deposit](https://api.crossref.org/works/10.1145/3780097); [publisher URL](https://dl.acm.org/doi/10.1145/3780097); local article pp. 51:1–51:2 and cover.

5. **Conv-FinRe has a version-specific author-list discrepancy. Do not silently merge the lists.**
   - **Published record:** **Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, Yuqing Guo, Fengran Mo, Jimin Huang, Yankai Chen, and Jian-Yun Nie. 2026. _Conv-FinRe: A Conversational and Longitudinal Benchmark for Utility-Grounded Financial Recommendation._** In *Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval* (SIGIR '26), pp. **3448–3455**, Melbourne, VIC, Australia. **Publication DOI: `10.1145/3805712.3808658`**. Online **19 July 2026**, print **20 July 2026**, per ACM's Crossref deposit. This record lists **13 authors**. [Publisher-deposited metadata](https://api.crossref.org/works/10.1145/3805712.3808658); [publisher URL](https://dl.acm.org/doi/10.1145/3805712.3808658)
   - **arXiv v2 read here:** **Yan Wang, Yi Han, Lingfei Qian, Yueru He, Xueqing Peng, Dongji Feng, Zhuohan Xie, Vincent Jim Zhang, Rosie Guo, Fengran Mo, Jimin Huang, Yankai Chen, Xue Liu, and Jian-Yun Nie** (**14 authors**). HTML title block renders **Xue (Steve) Liu**. Same title; **arXiv DOI `10.48550/arXiv.2602.16990`**. Official abstract page gives v1 **19 February 2026**, v2 **17 May 2026**, with comment “Accepted by SIGIR 2026 Resource Track. Pre-camera-ready version.” Search results displayed 18 February for v1, but use the version page's explicit timestamp, 19 February UTC. [arXiv abstract/history](https://arxiv.org/abs/2602.16990); [v2 title block and full text](https://arxiv.org/html/2602.16990v2)
   - Bibliographic caution: v2 HTML retains ACM template placeholders, including a fake **2018 Woodstock conference** and `XXXXXXX.XXXXXXX` DOI. These are unfilled template fields, **not** publication evidence. The actual publication DOI and year above are separately verified. Final-publisher full text was inaccessible, so the reason for the author-list changes was not established. [v2 title block](https://arxiv.org/html/2602.16990v2); [ACM deposit](https://api.crossref.org/works/10.1145/3805712.3808658)

### Inferences

- Use the official publication titles/years/DOIs in a bibliography, while explicitly marking local-version evidence where the final text was not checked. In particular, a CIKM 2025 citation does not establish that every arXiv v2 table survived unchanged in the final article. [Basis: LangPTune records above](https://arxiv.org/abs/2410.18870); [CIKM deposit](https://api.crossref.org/works?query.title=LangPTune&rows=2)
- For Conv-FinRe, use the 13-author publisher-deposited list when citing the SIGIR publication, or the 14-author list when explicitly citing arXiv v2. Do not substitute `Rosie` for `Yuqing`, or add/remove Xue Liu across versions without acknowledging the discrepancy. [Basis: arXiv](https://arxiv.org/abs/2602.16990); [Crossref](https://api.crossref.org/works/10.1145/3805712.3808658)

### Gaps

- ACM landing pages for LangPTune and Conv-FinRe returned HTTP 403. Their official DOI/title/year/venue metadata were recovered from **publisher-deposited Crossref records**, but final full-text equivalence with the arXiv versions remains unverified.
- No newly verified publisher DOI for FAR-Trans is supplied here; preserve the previous notes' distinction between the workshop paper's arXiv DOI and the dataset DOI.
- The four local main texts were sufficient for their assigned core readings. This is not a replication, code audit, exhaustive review of all cited works, or verification of every appendix/figure coordinate.

## 2. What do the full texts actually show, including numbers and experimental controls?

### Takeaway

The nearest methodological evidence is LangPTune, especially its **NoProfile** comparisons; it does not establish a general summary advantage. FLARKO is the closest same-dataset LLM study, but uses **structured JSON-LD knowledge graphs and KTO**, not LLM-generated transaction summaries, and evaluates **Hits@3 variants**, not nDCG@10. UPR supports feasibility and editability of review-derived profiles; the TOIS and Conv-FinRe papers support careful separation of purchase prediction from financial utility. [LangPTune §§4.2–4.5](https://arxiv.org/abs/2410.18870v2); [FLARKO §§3–7](https://arxiv.org/abs/2510.15993v1); [UPR §§3–5](https://aclanthology.org/2024.acl-long.753.pdf); [TOIS](https://doi.org/10.1145/3780097); [Conv-FinRe §§3–4](https://arxiv.org/html/2602.16990v2)

### Cited Findings

#### A. FLARKO: direct financial-domain relevance, different representation and target

**Method and temporal protocol**

- The personal KG (PKG) represents prior investor transactions with ISIN, buy/sell type, transaction value, and timestamp. The market KG (MKG) represents price summaries and category/sector/industry metadata. Both use subject–predicate–object triples serialized as **JSON-LD**. Price aggregation uses **10-week** periods; only periods ending before the recommendation date are included. PKG events are also filtered before that date. The pair is capped at **5,000 triples**. These are structured graph/price aggregations, not an LLM-written narrative summary of transaction history. **Locators: §3.1, PDF p. 4, Figs. 2–3.** [Full-text version](https://arxiv.org/abs/2510.15993v1)
- Prompts pass market and personal graphs and request three ISINs for the next **180 days / six months**. KTO desirability requires both an actual purchase within 180 days and a positive asset return in that period. Each prompt produces desirable/undesirable completion examples, each containing up to **20** assets. Thus alignment supervision combines future behavior and return; it is not simply optimizing purchase nDCG. **Locators: §§3.2–4, PDF pp. 4–5.** [Source](https://arxiv.org/abs/2510.15993v1)
- Training data span **2 January 2018–30 November 2021**, with recommendation prompts every four weeks from **1 August 2019–1 June 2021**; test data span **1 December 2021–29 November 2022**, with test prompts every two weeks from **1 December 2021–2 June 2022**. The authors use 180-day outcome buffers. **Locator: §6.1, PDF p. 6.** These are FLARKO's dates, not the class split or the FAR-Trans benchmark's 61 origins. [Source](https://arxiv.org/abs/2510.15993v1)
- Models: Qwen3 **0.6B, 1.7B, 4B, 8B**, with 8B excluded from federated training for compute reasons; LoRA rank **16**, alpha **64**, 4-bit quantization; context extended to **131,072** from **32,768** tokens using YaRN. Centralized training **3 epochs**; federated training **200 rounds**, **3 of 20 clients** sampled per round, **0.1 local epochs**. Simulated clients use customer type, risk level, and capacity for IID/non-IID allocation. **23,784** balanced labeled examples. **Locators: §§6.4–6.5, PDF p. 6.** [Source](https://arxiv.org/abs/2510.15993v1)
- Baselines: price-based random forest, linear regression, LightGBM; behavior-based popularity, LightGCN, ARM, MF, UB kNN; random. Evaluation uses **Pref@3**, **Prof@3**, **Comb@3**, described as Hits@3/hit rate against purchased, profitable, and intersection sets respectively. **Locators: §§6.2–6.3, PDF p. 6.** No nDCG@10 result is reported. [Source](https://arxiv.org/abs/2510.15993v1)

**Supported numerical findings — Table 2, PDF p. 7**

All values below are transcribed as **mean ± standard error of a proportion**, the caption's terminology. Do not call these confidence intervals or across-seed standard deviations. [Table 2](https://arxiv.org/abs/2510.15993v1)

| Centralized model | Context | Pref@3 | Prof@3 | Comb@3 |
|---|---|---:|---:|---:|
| Qwen3-0.6B | Combined | 0.0354 ± 0.0131 | 0.1010 ± 0.0214 | 0.0152 ± 0.0087 |
| Qwen3-0.6B | PKG | 0.4439 ± 0.0355 | 0.4694 ± 0.0356 | 0.2551 ± 0.0311 |
| Qwen3-1.7B | Combined | 0.0990 ± 0.0216 | 0.4975 ± 0.0354 | 0.0524 ± 0.0161 |
| Qwen3-1.7B | PKG | 0.4434 ± 0.0483 | 0.4528 ± 0.0483 | 0.2642 ± 0.0428 |
| Qwen3-1.7B | MKG | **0.5341 ± 0.0532** | 0.5169 ± 0.0530 | 0.3448 ± 0.0510 |
| Qwen3-1.7B | Nothing | 0.5000 ± 0.0566 | 0.6154 ± 0.0551 | **0.3718 ± 0.0547** |
| Qwen3-4B | Combined | 0.2740 ± 0.0522 | **0.6400 ± 0.0554** | 0.1644 ± 0.0434 |
| Qwen3-4B | PKG | 0.2973 ± 0.0751 | 0.4324 ± 0.0814 | 0.2973 ± 0.0751 |
| Qwen3-8B | Combined | 0.1136 ± 0.0478 | 0.5909 ± 0.0741 | 0.0682 ± 0.0380 |
| Qwen3-8B | PKG | 0.4528 ± 0.0684 | 0.5849 ± 0.0677 | 0.3585 ± 0.0659 |

- Table 3, PDF p. 8: non-IID federated Qwen3-4B **PKG Comb@3 = 0.3469 ± 0.0680**, versus **Combined 0.2353 ± 0.0514**; its Combined Prof@3 is **0.6176 ± 0.0589**. Table 4: IID Qwen3-4B PKG Comb@3 **0.3051 ± 0.0599**. These compare configurations/deployments, not prose versus structured history. [Tables 3–4](https://arxiv.org/abs/2510.15993v1)
- §7.3/Fig. 1 compares the models' **best results** from Tables 2–3 with baselines and reports better preference/joint hit rates, while many baselines do better on pure profitability. Exact baseline plot coordinates were **not digitized**; no numerical baseline improvement is invented here. [§7.3 and Fig. 1](https://arxiv.org/abs/2510.15993v1)
- **Internal overstatement:** §8 says the combination of PKG and MKG yields the strongest performance. Table 2 does not support that as a general statement: Combined is below PKG on **Pref@3 and Comb@3 for every centralized model size**; the best overall Comb@3 is the 1.7B **Nothing** row. §7.1 itself acknowledges combined-input degradation for smaller models. Report the actual table rather than repeating the broad conclusion unqualified. [Table 2, §7.1 and §8](https://arxiv.org/abs/2510.15993v1)

**Control assessment / limitations**

- Same FAR-Trans domain and nominal temporal protocol help relevance, but PKG/MKG/Nothing ablations **remove/change information**; comparisons against other algorithms change the ranker and often supervision/features. None is narrative-summary versus structured-history with matched information. No pre-cutoff sparse-user criterion or sparse-stratum result is reported. [§§3–7](https://arxiv.org/abs/2510.15993v1)
- The text does not establish exact evaluated user counts, identical instances/candidate lists across every ablation, already-held/repeat-purchase policy, invalid/duplicate ISIN handling, or a complete validation/tuning protocol. Its Hits@3 terminology lacks a full denominator/aggregation equation. Different reported proportion standard errors warrant checking denominators before assuming paired comparisons; this is a **verification gap**, not proof of changed cohorts. [§§6–7, Tables 2–4](https://arxiv.org/abs/2510.15993v1)
- The conclusion's generalizability, compliance, and interpretability claims are not an external-market test, regulatory certification, or quantified summary-fidelity result. This study cannot be cited as proof that LLM summaries help sparse users. [§6 opening; §8](https://arxiv.org/abs/2510.15993v1)

#### B. ACL UPR: review-derived profiles, warm-start rating prediction

**Method and experiment**

- Extract review features with a phrase-level sentiment toolkit, rank features using rating-derived utility/coverage/significance, group stems, and prompt Llama2-7B or Mistral-7B instruction models to produce a first-person NL profile. Default **top 5 features**, **5 sampled reviews per feature**, **200-token maximum**, temperature **0.7**; Appendix A.1 reports seed **0**. Fine-tune **GPT-2** for rating regression on profile plus **item title**, without user/item ID embeddings in this pipeline. **Locators: §§3.2–3.4, 4.4; pp. 13974–13976; Appendix A.1–A.3, p. 13981.** [Official PDF](https://aclanthology.org/2024.acl-long.753.pdf)
- Datasets: Amazon Movies and TV and TripAdvisor. Table 1: **4,811 users, 5,459 items, 288,693 records** (Amazon); **9,765 users, 6,280 items, 320,023 records** (TripAdvisor); mean records/user **60.01** and **32.77**. Split **8:1:1**; every user/item appears at least once in each split and each user has at least **5 training reviews**. The text does not specify a global chronological cutoff. **Locator: §4.1/Table 1, p. 13975.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)
- Primary task is rating prediction using RMSE/MAE. nDCG@10 and MAP are computed on **condensed lists containing only explicitly rated test items**; MAP relevance threshold **4.0**. This is not catalog-wide future-purchase retrieval, despite the shared nDCG@10 label. **Locator: §4.2, p. 13975.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)
- Baselines include MostPop, UserKNN, ItemKNN, MF, NeuMF, PETER+, PEPLER-MLP. §4.3 says Cornac baselines use default parameters; §4.4 describes training/validation tuning and Appendix A.3 specifies UPR's grid/early stopping. Equal baseline-specific tuning effort is not demonstrated. **Locators: pp. 13975–13976, 13981.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)

**Numbers — Table 2, p. 13977 (PDF p. 7)**

| Method | Amazon RMSE | Amazon MAE | Amazon nDCG@10 | TripAdvisor RMSE | TripAdvisor MAE | TripAdvisor nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|
| MostPop | 1.505 | 0.962 | 0.896 | 1.277 | 0.902 | 0.932 |
| MF | 0.925 | 0.686 | 0.941 | 0.786 | 0.599 | 0.960 |
| PETER+ | 0.924 | 0.685 | 0.941 | 0.803 | 0.621 | 0.958 |
| PEPLER-MLP | 0.925 | 0.672 | 0.941 | 0.793 | 0.606 | 0.959 |
| UPR (Llama2) | 0.944 | 0.678 | 0.938 | 0.804 | 0.616 | 0.955 |
| UPR (Mistral) | 0.941 | 0.679 | 0.940 | 0.804 | 0.610 | 0.952 |

Source for all cells: [Table 2](https://aclanthology.org/2024.acl-long.753.pdf). UPR is competitive but does **not** exceed MF's nDCG@10 on either dataset. The paper supplies no equivalence test establishing statistical parity in Table 2.

- Profile-quality study: **5 master's-student annotators**, **50 profiles per dataset**. Table 3 reports fluency **95%/92%**, informativeness **86%/82%**, conciseness **75%/72%**, relevance **90%/87%** (Amazon/TripAdvisor). Fleiss' kappa **0.82** in §5.3. These are judgments of generated profiles, not proof of improved investment outcomes or faithful transaction summaries. **Locators: §5.3/Table 3 pp. 13977–13978.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)
- Scrutability experiment selects **200 users**, edits profiles to like a target feature, and samples **100 feature-matching + 100 nonmatching test items**, repeating across **5 seeds**. Coverage@10 increases for the tested additions; no exact figure bars are transcribed. Appendix A.5 increases edit generation to **300 tokens**; A.6 finds only minor changes for negative-preference edits. This is a profile-edit intervention, not a summary-vs-history accuracy ablation. **Locators: §5.4, pp. 13978; Appendix A.5–A.6, p. 13982.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)
- Conclusion emphasizes competitive accuracy and immediate edits. Limitations include review dependence, mostly positive preferences (average rating **4/5**), slowness, profile information bottleneck, and hallucinated/inferred actors or characters. **Locators: §5.3 and §§6–8, pp. 13978–13979.** [Source](https://aclanthology.org/2024.acl-long.753.pdf)

**Control assessment**

- Nominal evaluation splits/lists are shared, but CF baselines consume interaction matrices while UPR uses selected textual reviews, item titles, and pretrained language knowledge with a different downstream predictor. No same-ranker structured-history baseline isolates representation. The top-feature ablation changes the amount of input information; editing experiments deliberately add preferences. [§§3–5](https://aclanthology.org/2024.acl-long.753.pdf)
- Warm-start minimum-history filtering is not a pre-cutoff sparse-financial-user cohort. Review content can directly express likes/dislikes absent from buy/sell logs. The paper does not provide a sufficiently explicit point-in-time audit of feature-statistic/profile construction to certify absence of future information under a chronological purchase task. This is not an accusation of proven leakage. [§§3.2, 4.1–4.4](https://aclanthology.org/2024.acl-long.753.pdf)

#### C. LangPTune: closest methodological prior work and strongest counterexample to automatic summary gains

**Method and evaluation**

- A profile encoder (Gemma-2B-it or Llama-3-8B-it) generates NL profiles from interaction-history item metadata and user reviews. An **Mxbai text-embedding decoder** scores profiles against item metadata by inner product and sorts candidates. **RLSO** optimizes the profile generator from downstream ranking reward; contrastive learning (**CL/InfoNCE**) optimizes the decoder; joint training alternates them. This is task-optimized profile generation, rather than a fixed zero-shot summarization treatment. **Locators: §§3.1–3.2, pp. 2–4; §4.3, pp. 5–6.** [Local-version source](https://arxiv.org/abs/2410.18870v2)
- Amazon Movie-TV and Books metadata include title, description, average rating, category, price; **user reviews are additional LLM input**. Filter sessions/items with fewer than **5 interactions**, item metadata over **512 tokens**, and histories over **1,024 tokens**. Each example has **4 distinct history items and 1 distinct future item**. These are deliberately short evaluation histories, but not a cohort of users known to be sparse before a common financial cutoff. **Locator: §4.1, p. 4.** [Source](https://arxiv.org/abs/2410.18870v2)
- Table 1, p. 5: Movie-TV train/validation/test sessions **14,698 / 1,392 / 1,392**, **10,533 items**, **87,410 interactions**; Books **4,404 / 361 / 361**, **4,819 items**, **25,630 interactions**. Main ranking metrics are **Recall@20, MRR@20, NDCG@20**, not nDCG@10. The decoder is formulated over the item catalog, and random/popularity baselines rank all items; do not substitute UPR's condensed-list evaluation. Exact seen-item masking and temporal train/test partition implementation were not audited. [§§3.1.1, 4.1–4.3 and Table 1](https://arxiv.org/abs/2410.18870v2)
- Baselines distinguish **LangPTune-0** (both pretrained/frozen), **LangPTune-CL** (train decoder only), **LangPTune-RLSO** (train encoder only), and full LangPTune. Black-box methods include NMF, LightGCN, MCL, BERT4REC, LLM2BERT4REC. Footnote 1 on p. 5 explicitly allows black-box training to use validation/test **history items**, and popularity also uses those observed histories. That is observed-context access, not necessarily future-target leakage, but is not a simple global temporal split. [§4.2 and footnote 1](https://arxiv.org/abs/2410.18870v2)
- All text-embedding variants use Mxbai architecture; **same architecture is not same fitted weights**. Each baseline is tuned on validation data. Maximum default profile length **512 tokens**. Appendix B lists materially different CL learning rates/update counts for NoProfile-CL versus full LangPTune. **Locators: §4.3 and Appendix B, pp. 13–14.** [Source](https://arxiv.org/abs/2410.18870v2)

**Numbers and relevant comparisons**

Table 2, p. 6, **NDCG@20**:

| Encoder | Variant | Movie-TV | Books |
|---|---|---:|---:|
| Gemma | LangPTune-0 | 0.0289 | 0.1743 |
| Gemma | LangPTune-CL | 0.0436 | 0.1984 |
| Gemma | LangPTune-RLSO | 0.0364 | 0.2400 |
| Gemma | Full LangPTune | **0.0446** | **0.2736** |
| Llama | LangPTune-0 | 0.0231 | 0.1753 |
| Llama | LangPTune-CL | 0.0456 | 0.2099 |
| Llama | LangPTune-RLSO | 0.0377 | 0.2224 |
| Llama | Full LangPTune | **0.0494** | **0.2393** |

Source: [Table 2](https://arxiv.org/abs/2410.18870v2). Reported full-vs-zero-shot relative improvements: **113.9%** (Llama/Movie-TV) and **57.0%** (Gemma/Books); these are **training/profile optimization gains**, not gains over structured-history features. Table 2 uses paired t-tests at **α = 0.05**; Gemma/Movie-TV full vs CL's **2.29%** has no significance asterisk.

- **Critical direct-history comparator:** §4.5.1 defines **NoProfile-0** as the same pretrained Mxbai encoder applied directly to the list of history-item metadata, with no profile-generation bottleneck; **NoProfile-CL** trains that embedding model with InfoNCE. Table 4, p. 7 (Llama/Movie-TV):

  | Representation/pipeline | Recall@20 | MRR@20 | NDCG@20 |
  |---|---:|---:|---:|
  | LangPTune, 64-token maximum | 0.0604 | 0.0201 | 0.0319 |
  | LangPTune, 128-token maximum | 0.0901 | 0.0313 | 0.0444 |
  | LangPTune, 256-token maximum | 0.0929 | 0.0352 | 0.0482 |
  | LangPTune, 512-token maximum | 0.0970 | 0.0358 | 0.0494 |
  | NoProfile-0 | 0.0760 | 0.0261 | 0.0372 |
  | **NoProfile-CL** | **0.1012** | **0.0408** | **0.0543** |

  All cells: [§4.5.1/Table 4](https://arxiv.org/abs/2410.18870v2). The authors explicitly discuss a language-profile information bottleneck and somewhat lower performance versus NoProfile-CL. **Derived arithmetic:** full 512-token LangPTune is **0.0049 lower NDCG@20**, about **9.0% below** NoProfile-CL; this is not a reported significance test. Table 4 supplies no significance marker for this pair.
- Fixed pretrained decoder comparison is possible in a limited sense: on Movie-TV, Llama **LangPTune-0 = 0.0231**, **NoProfile-0 = 0.0372**, and encoder-trained **LangPTune-RLSO = 0.0377**. Thus zero-shot summaries underperform direct input here; training the generator almost matches/slightly exceeds the direct-input score. These cross-table comparisons have the **same pretrained decoder**, but review inclusion, formatting/truncation, and significance for the exact pairs are not fully established. Do not dismiss this partial representation-control evidence, or inflate it into the user's financial experiment. [Tables 2/4; §§4.2.1, 4.5.1, 4.7](https://arxiv.org/abs/2410.18870v2)
- Table 3, p. 7: full LangPTune Movie-TV **0.0494** is below LightGCN **0.0525** and MCL **0.0563**; Books **0.2736** exceeds LightGCN **0.2586** and NMF **0.2323**. The method is not uniformly superior across datasets. [Table 3](https://arxiv.org/abs/2410.18870v2)
- Fig. 4/§4.5.2 reduces **total training data from 100% to 0.1%** and reports comparatively stable LangPTune performance. This is a **training-dataset-size** ablation, not per-user pre-cutoff sparsity stratification. No exact curve coordinates are extracted. [§4.5.2, p. 7](https://arxiv.org/abs/2410.18870v2)
- Interpretability study, Table 5, p. 8: human next-movie binary-choice accuracy **57.11% NoProfile-0**, **54.67% LangPTune-0**, **58.89% full LangPTune**. Full vs zero-shot difference is **not significant (p = 0.201)**; full vs NoProfile difference **p = 0.624**. Table 6 reports average completion times **34.76 s**, **28.77 s**, **29.15 s**, respectively (outlier-filtered). These are readability/usefulness diagnostics, not transaction-summary faithfulness or investment recommendation outcomes. [§4.6/Tables 5–6](https://arxiv.org/abs/2410.18870v2)
- §5 concludes that joint optimization improves over other language-profile variants and can be competitive with black-box methods; future work includes steerability studies, longer histories, and improved item descriptions. This is consistent with studying compression tradeoffs, not assuming every summary improves accuracy. [§5, p. 8](https://arxiv.org/abs/2410.18870v2)

**Control assessment**

- This is the **strongest methodological comparator among the requested studies**: it includes the missing profile-encoder ablation and a fixed-pretrained-decoder family. However, full LangPTune vs NoProfile-CL changes trained weights, training objectives/budgets, and compression. Metadata lists are also not the same as a tabular buy/sell/count/recency feature vector. [§§3–4, Appendix B](https://arxiv.org/abs/2410.18870v2)
- Input-information equivalence needs explicit checking: §4.1 adds reviews to the LLM, whereas §4.5.1 describes NoProfile input as item metadata. A same-information claim cannot be certified from those descriptions alone. Four-item histories and global interaction-count filters do not establish sparse eligibility before a common calendar cutoff. No FAR-Trans result, nDCG@10 summary effect, or sparse-investor subgroup result is provided. [§§4.1, 4.5.1](https://arxiv.org/abs/2410.18870v2)

#### D. Investors Are (Not) Always Right: strongest metric-interpretation source

**Methods and scope**

- Defines transaction relevance as a first acquisition in the future evaluation interval, excluding previously interacted assets from rankings. Theoretical analysis formalizes transaction-based and customer-independent profitability metrics; Theorem 5.6 establishes **zero correlation over all possible valid user–ranking pairs at fixed time/horizon**, under the stipulated properties. The authors call this “independence”; zero correlation alone is not generally statistical independence. Safest wording: the formal result supplies **no guaranteed positive relationship**, and is not a universal empirical law about every investor or utility metric. **Locators: §§3, 5.1–5.3, pp. 51:9–51:16.** [Published source](https://doi.org/10.1145/3780097)
- Uses FAR-Trans, binary acquisition matrix, **12 algorithms**, **61 temporal variants**, first origin **1 August 2019**, stated spacing two weeks, stated last origin **end of November 2021**. Prior data are available for training/validation; future acquisitions repeated from training are excluded. Test users require activity in both periods, and assets require test-period prices. Main horizon **6 months**. **Locator: §6.1, pp. 51:17–51:18.** [Source](https://doi.org/10.1145/3780097)
- Numerical metric definition is explicit: binary purchase gain and log2 rank discount for nDCG; equally weighted top-k ROI; **monthly ROI = (1 + ROI)^(30 / days(horizon)) − 1**. The “profitable” proportion uses **ROI ≥ 0**. **Locator: §6.2, Eqs. 7–12, pp. 51:19–51:20.** [Source](https://doi.org/10.1145/3780097)
- Algorithms extend the original FAR-Trans baseline set with **customer profile similarity (CPS)**, a demographic-neighbor method based on risk-appetite questionnaire features. Price models, transaction CF/ARM/popularity, and LightGBM regression/LambdaMART hybrids remain different information/model families. All hyperparameters are selected by **six-month ROI at 1 April 2019, 1 October 2019, and 31 January 2020**, not task-matched nDCG validation. **Locator: §6.3, pp. 51:20–51:21.** [Source](https://doi.org/10.1145/3780097)

**Numerical findings**

- §7/Fig. 4, p. 51:23: pooled correlation between **nDCG@10 and monthly ROI@10 = −0.13**, computed over approximately **1.5 million user × algorithm × temporal-variant values**, reported significantly different from zero at **p < 0.05**. This is **not** merely a correlation across 12 aggregate algorithm means. [§7/Fig. 4](https://doi.org/10.1145/3780097)
- Table 5, p. 51:24: **LightGCN nDCG@10 0.3404 / monthly ROI 0.0004**; **popularity 0.2710 / 0.0006**; **random forest 0.0237 / 0.0259**; **UB kNN 0.1599 / 0.0119**; **CPS 0.2722 / 0.0026**; market monthly ROI **0.0079**, customer **0.0018**. These reproduce the original FAR-Trans baseline values for shared algorithms, with CPS and additional metric analyses added. They must not be counted as an independent second replication of summary benefits. [§8.1/Table 5](https://doi.org/10.1145/3780097)
- §9.2 generates **10 synthetic datasets** of deliberately more effective investors and observes pooled correlation **+0.13** (Fig. 7, p. 51:31), showing dependence on investor generation/behavior assumptions rather than a universal negative relation. [§9.2](https://doi.org/10.1145/3780097)
- §10/Fig. 8, p. 51:32: per-date correlations vary from **−0.65 to 0.4**. §11 adds horizons **1, 3, 9, 12 months**; pooled values remain approximately **−0.13 to −0.05**, but date-level correlations differ substantially. **Locators: §§10–11, Figs. 8, 12–13, pp. 51:32–51:37.** [Source](https://doi.org/10.1145/3780097)
- Holding-time analysis peaks around **15–18 months** (§11/Fig. 10, p. 51:34); limitations report **79.86%** holding longer than a year (p. 51:40). This calculation assigns initial holdings to dataset day 1 and closes remaining holdings on the last day, so these are censored/simplified holding-time estimates, not exact intended investment horizons. [§11 and Limitations](https://doi.org/10.1145/3780097)
- Conclusion recommends complementary profitability evaluation, temporal reporting, attention to investor horizons and heterogeneity; it expressly says abandoning transaction-based evaluation would be premature. Dataset limitations: a single institution, partial portfolios, and omitted dividend/coupon income. The data statement says demographic information used could not be shared. **Locators: §12 and Limitations/Data Statement, pp. 51:38–51:41.** [Source](https://doi.org/10.1145/3780097)

**Control assessment / reporting concerns**

- No LLM-generated summary arm exists. Matching customer/asset subsets across metric families supports **metric comparison**, not representation-effect identification. Sparse-user eligibility or sparse-specific summary gains are not evaluated. [§§6–8](https://doi.org/10.1145/3780097)
- This article supplies the previously missing final-origin statement, but **61 origins**, **two-week spacing**, and **August 2019–November 2021** are not straightforwardly consistent as a literal regular schedule. Preserve the published statements; a date list/code check is still needed. Do not manufacture the official class schedule from them. [§6.1](https://doi.org/10.1145/3780097)
- ROI-based tuning dates overlap/follow early test origins; nested chronological model selection is not established. Overlapping six-month outcome windows and repeated users/models also mean pooled observations are not automatically independent replicates. These are design/inference concerns, not a recalculated rejection of the authors' findings. [§§6.1, 6.3, 7](https://doi.org/10.1145/3780097)
- CPS is not automatically reproducible from released FAR-Trans customer fields: the article explicitly states its demographic information could not be shared. The user has not verified those features. [§6.3 and Data Statement](https://doi.org/10.1145/3780097)

#### E. Conv-FinRe: verified alternative; conversational utility benchmark, not summary-feature ablation

**Task and data**

- Models rerank a fixed candidate set using onboarding dialogue, historical interaction dialogue, current market signals, and three advisor perspectives. Four reference views distinguish **user choice**, **rational utility**, **market momentum**, and **risk sensitivity**. Utility is a standardized seven-day-return term minus user-specific volatility and drawdown penalties. Parameters are fitted by regularized inverse optimization over a user's **full longitudinal decision trajectory**; they are not directly exposed as model inputs. **Locators: §§3.1–3.2, Eqs. 1–6.** [Full text](https://arxiv.org/html/2602.16990v2#S3)
- Real market prices plus **10 human participants' decisions in an asset simulator**, not historical FAR-Trans brokerage purchases. Universe **10 stocks**; stated price horizon **6 August–17 September 2025**, described as **30 days**. Questionnaire-grounded onboarding is **4 turns**; ongoing dialogues are **generated transformations** of the profiles and observed simulated decisions, not collected free-form human advisor conversations. **Locators: §3.3.1–3.3.2, Tables 2–3.** [Source](https://arxiv.org/html/2602.16990v2#S3.SS3)
- Table 3: **23 steps/user**, **230 prefix-conditioned instances**, **270 unique turns**, **3,450 prefix-expanded turns**; mean **15 turns/instance**, **4,320.2 tokens/instance**, range **1,818–7,252**. Do not describe 230 instances as 230 independent users or 3,450 turns as unique. [Table 3](https://arxiv.org/html/2602.16990v2#S3.T3)
- Metrics: **uNDCG** over the entire candidate ranking using calibrated utility as relevance; user-choice MRR and **HR@1/HR@3**; **Kendall τ** alignment with utility/momentum/risk advisors. Seven LLMs, unified **8,192-token input** and **126-token output** caps. This is not binary purchase-relevance nDCG@10, even though its universe contains ten items. [§§3.4–3.5](https://arxiv.org/html/2602.16990v2#S3.SS4)

**Numerical findings — Table 4**

| Model | uNDCG | MRR | HR@1 | HR@3 |
|---|---:|---:|---:|---:|
| Random | 0.73 ± 0.00 | 0.29 ± 0.01 | 0.10 ± 0.01 | 0.30 ± 0.01 |
| GPT-4o | 0.94 ± 0.00 | 0.56 ± 0.03 | 0.42 ± 0.03 | 0.60 ± 0.03 |
| Qwen2.5-72B-Instruct | 0.92 ± 0.01 | 0.63 ± 0.03 | 0.50 ± 0.03 | 0.69 ± 0.03 |
| Llama-3.3-70B-Instruct | **0.97 ± 0.00** | 0.52 ± 0.03 | 0.36 ± 0.03 | 0.59 ± 0.03 |
| Llama3-XuanYuan3-70B-Chat | 0.92 ± 0.00 | **0.65 ± 0.03** | **0.54 ± 0.03** | 0.69 ± 0.01 |

All cells: [Table 4](https://arxiv.org/html/2602.16990v2#S4.T4). The random baseline averages **1,000 uniform permutations per instance**. The inspected text/caption does not clearly define all reported ± quantities; retain them as reported uncertainty without relabeling them as confidence intervals or seed SDs.

- Table 5: Llama-3.3 alignment **τ utility 0.74 ± 0.02**, **momentum 0.73 ± 0.01**, **risk 0.17 ± 0.02**. High utility alignment does not establish independent risk-sensitive reasoning when advisor signals are correlated. [§4.2/Table 5](https://arxiv.org/html/2602.16990v2#S4.T5)
- §4.3 compares history **present vs absent**. Prose describes improvements for GPT-5.2, DeepSeek-V3.2, Qwen3-235B; little change for GPT-4o/Llama-3.3; degraded utility alignment for Qwen2.5/XuanYuan3. Exact figure differences were not digitized, and no numerical summary benefit is claimed. The ablation changes **available information**, not the encoding of the same history. [§4.3/Figs. 2–3](https://arxiv.org/html/2602.16990v2#S4.SS3)
- Quality checks: user agreement with expert-verbalized inferred risk profiles averaged **7.8/9**; three experts assessed one sampled step per user (**10 dialogue instances**) with mean plausibility **8.1/9**. These are small validation exercises, not proof of valid personal utility for all investors. [§3.3.2](https://arxiv.org/html/2602.16990v2#S3.SS3.SSS2)
- §5 concludes that behavioral alignment and utility alignment diverge, motivating multi-view evaluation. Its claims about domain-specialized models are based on this small benchmark and one listed finance-specific model. [§5](https://arxiv.org/html/2602.16990v2#S5)

**Control assessment / caveats**

- Nominal users/candidates are shared across evaluated LLMs and history ablations, but models differ and history removal changes information. No summary-versus-structured arm, FAR-Trans cohort, or pre-cutoff sparsity selection exists. [§§3–4](https://arxiv.org/html/2602.16990v2)
- Full-trajectory inverse fitting makes utility a **retrospectively calibrated reference**, not a pre-cutoff observed user preference. Because generated historical advisor messages are grounded in these references, strict prefix-only information provenance also needs checking before reusing the construction for future-purchase prediction. This is a temporal-design concern, not an established measured leakage effect. [§§3.2–3.3](https://arxiv.org/html/2602.16990v2#S3.SS2)
- Utility is an assumed return–risk model, not directly measured welfare. Its formula permits signed utilities; the stated uNDCG equations do not document shifting/clipping to nonnegative relevance. Consequently, do not assume conventional bounded binary-relevance nDCG interpretation or compare **0.97** with FAR-Trans **0.3404**. Code-level metric handling was not audited. [Eqs. 3, 7–8](https://arxiv.org/html/2602.16990v2#S3.SS4)
- Internal description issue: §3.3.1 claims coverage of **all eleven GICS sectors**, but Table 2 contains only **ten stocks** and ten listed sector labels. Do not repeat the all-eleven claim as established coverage. The phrase “30-day horizon” spans more than 30 calendar days; do not infer a calendar-day protocol without clarification. [§3.3.1/Table 2](https://arxiv.org/html/2602.16990v2#S3.T2)
- Ten participants, repeated prefixes, one short market period, generated dialogue and retrospective utility calibration limit external validity. The authors' behavioral interpretation labels are not independent measures of empathy or financial expertise. [§§3–4](https://arxiv.org/html/2602.16990v2)

### Inferences

- **No pooled effect size is justified:** these studies measure condensed rating-list nDCG@10, catalog next-item NDCG@20, financial Hits@3, purchase nDCG@10, or utility-grounded full-list nDCG. Their numeric scales and populations are not interchangeable. [UPR §4.2](https://aclanthology.org/2024.acl-long.753.pdf); [LangPTune §4](https://arxiv.org/abs/2410.18870v2); [FLARKO §6.3](https://arxiv.org/abs/2510.15993v1); [TOIS §6.2](https://doi.org/10.1145/3780097); [Conv-FinRe §3.4](https://arxiv.org/html/2602.16990v2#S3.SS4)
- The evidence supports testing a **two-sided question**: semantic abstraction might help generalization, while compression can discard predictive details, particularly with already short histories. LangPTune's direct-history scores and FLARKO's combined-context degradation provide concrete reasons not to presuppose the direction. [LangPTune Table 4](https://arxiv.org/abs/2410.18870v2); [FLARKO Table 2](https://arxiv.org/abs/2510.15993v1)
- A better purchase-prediction score can be a valid result for the user's narrowly stated RQ without implying better investment advice or returns. The TOIS paper challenges using transaction metrics **as profitability proxies**, not their descriptive ability to measure future-purchase prediction. [TOIS §§7, 12](https://doi.org/10.1145/3780097)

### Gaps

- No inspected paper directly reports the requested **same-information summary-versus-structured-history nDCG@10 effect for pre-cutoff sparse FAR-Trans users**.
- Most pertinent unresolved details: LangPTune final-version table equivalence and NoProfile review parity; FLARKO exact hit-rate denominators, candidate/cohort parity and sparse eligibility; TOIS exact date list and demographic-feature availability; Conv-FinRe final author/full-text reconciliation and point-in-time utility provenance.
- No exact values were inferred from plotted points/bars. No source experiment was rerun, and no stated significance claim was independently recalculated.

## 3. Which studies should the writer select, and what gap can be stated defensibly?

### Takeaway

Use **five core studies: FAR-Trans, LangPTune, FLARKO, ACL UPR, and Investors Are (Not) Always Right**. If constrained to three, choose **FAR-Trans + LangPTune + FLARKO**. Recommend **LangPTune as the nearest methodological prior work**, paired with **FLARKO as the nearest same-dataset LLM prior work**. Conv-FinRe is a verified optional evaluation-context alternative, less directly matched to the representation question. This is a relevance judgment based on the inspected methods, not a claim of exhaustive nearest-neighbor discovery across all literature. [FAR-Trans](https://arxiv.org/abs/2407.08692); [LangPTune](https://arxiv.org/abs/2410.18870v2); [FLARKO](https://arxiv.org/abs/2510.15993v1); [UPR](https://aclanthology.org/2024.acl-long.753/); [Investors](https://doi.org/10.1145/3780097); [Conv-FinRe](https://arxiv.org/abs/2602.16990)

### Cited Findings

#### Compact control/evidence matrix for the RQ

| Study | Same users/candidates across relevant comparison? | Same source information? | Fixed downstream ranker? | Pre-cutoff sparse eligibility? | What the evidence can support |
|---|---|---|---|---|---|
| FAR-Trans | Benchmark aligns eligible population/assets across methods/metrics, with future-activity/price filters | No: prices vs interactions vs hybrids | No | No sparse-specific evaluation | Dataset, sparsity motivation, future novel-purchase nDCG@10 benchmark. [§5](https://arxiv.org/abs/2407.08692) |
| FLARKO | Nominal temporal test; exact per-ablation cohort/candidate parity not established | No: PKG/MKG/combined/nothing | No across baseline families; input ablations are not summary arms | No | Feasibility of KG-grounded LLM recommendations on FAR-Trans, Hits@3 results. [§§6–7](https://arxiv.org/abs/2510.15993v1) |
| ACL UPR | Common splits and condensed test lists; editing experiments use another sampled list design | No: reviews/titles/pretrained knowledge vs ID interactions | No across accuracy baselines; fixed predictor for profile edits only | No; minimum 5 train reviews is warm-start inclusion | Review-derived profile feasibility, accuracy tradeoff and scrutability. [§§4–5](https://aclanthology.org/2024.acl-long.753.pdf) |
| LangPTune | Shared benchmark sessions/item universe; exact masking implementation not audited | Closest comparator, but NoProfile review parity unresolved | **Yes in frozen-Mxbai variants**; no for separately trained full vs NoProfile-CL | No; fixed 4-item histories are not naturally sparse cohort selection | Closest compression/direct-input comparison and optimization evidence; no universal summary advantage. [§4.5/Table 4](https://arxiv.org/abs/2410.18870v2) |
| Investors | Explicit common population/assets for comparing metrics | Different model families use different data | No representation comparison | No | Purchase accuracy and financial returns are distinct evaluation targets. [§§6–8](https://doi.org/10.1145/3780097) |
| Conv-FinRe | Fixed 10 participants/10 stocks, repeated prefix conditions | No: history present/absent changes information | Same LLM within history ablation, different across models | No | Multi-view evaluation and limits of behavioral imitation in a simulated conversational setting. [§§3–4](https://arxiv.org/html/2602.16990v2) |

#### Recommended selection and role

1. **FAR-Trans (mandatory foundation):** dataset, transaction construction, sparse-history motivation, popularity baseline and purchase-target definition. Carry forward existing `far_trans.md`, including its warnings about reconstructed initial buys and paper-vs-local counts. Its whole-period “over 50% have 3 or fewer transactions” is **not** a train-only sparse label. [FAR-Trans §§3.3, 5](https://arxiv.org/abs/2407.08692)
2. **LangPTune (nearest method):** explicitly compares language profiles against direct history-metadata representations and exposes a compression bottleneck. Best anchor for the research gap and a non-presumptive hypothesis. Cite CIKM publication details, but identify v2 as the experimental text inspected. [§4.5.1/Table 4](https://arxiv.org/abs/2410.18870v2); [publication record](https://api.crossref.org/works?query.title=LangPTune&rows=2)
3. **FLARKO (nearest application):** same FAR-Trans dataset and LLM use; distinguish KG serialization/KTO/market signals from narrative transaction-summary features and nDCG@10. [§§3–7](https://arxiv.org/abs/2510.15993v1)
4. **ACL UPR (profile rationale):** shows how LLM summaries can become user representations and how edits affect recommendations; offers published nDCG@10 with a fundamentally different condensed-list target. [§§3–5](https://aclanthology.org/2024.acl-long.753.pdf)
5. **Investors (evaluation discipline):** strongest directly relevant explanation of why predicting purchases is not the same as improving returns, with explicit financial metric formulas and temporal confounders. [§§5–12](https://doi.org/10.1145/3780097)

For four papers, keep the first three and choose **Investors** when evaluation validity is the priority, or **UPR** when the writer needs more depth on language-profile construction. Conv-FinRe can replace a contextual paper if a recent conversational benchmark is explicitly required, but should not displace FAR-Trans/LangPTune/FLARKO for this RQ. [Basis: control matrix above](https://arxiv.org/html/2602.16990v2#S3)

### Inferences

#### Defensible gap statement for the writer

> Among the studies inspected, language-based profiles have been evaluated for review-driven recommendation, and KG-grounded LLMs have been evaluated on FAR-Trans. However, these sources do not establish whether replacing structured pre-cutoff transaction-history features with LLM-generated summaries improves purchase-prediction nDCG@10 for a pre-defined sparse-history FAR-Trans cohort under matched users, candidates, source information, and downstream ranking conditions. LangPTune offers the closest methodological comparison and shows that a direct-history comparator can outperform a profile bottleneck.

This is a **bounded conclusion about the inspected studies**, not “the first ever” or “no prior work exists.” [Basis: LangPTune §4.5.1](https://arxiv.org/abs/2410.18870v2); [FLARKO §§3–7](https://arxiv.org/abs/2510.15993v1); [UPR §§3–5](https://aclanthology.org/2024.acl-long.753.pdf)

#### Research-design implications to preserve for later synthesis (not an approved implementation)

- **Define the estimand before borrowing scores:** future purchases of any asset versus only new-to-user assets, evaluation horizon, eligible catalog, and zero-relevant-user treatment. FAR-Trans/TOIS remove previously acquired/interacted assets; that may differ from the user's eventual task. Class decisions remain pending. [FAR-Trans §5](https://arxiv.org/abs/2407.08692); [TOIS §§3, 6](https://doi.org/10.1145/3780097)
- **Sparsity is a pre-cutoff property:** explicitly choose buy events, all transaction events, or distinct acquired assets as the counting unit; do not use whole-period activity or test activity to define the sparse band. Distinguish zero-history cold start from sparse warm start. Any test-activity requirement is a separate evaluability condition and should be reported as such. [Basis: FAR-Trans §§3.3, 5.2](https://arxiv.org/abs/2407.08692)
- **Representation must be the intended treatment:** give both arms the same historical events and permitted asset metadata/customer information; match recency windows, candidate/relevance rules, users and train/validation/test periods. Prose must not gain access to market information, risk questionnaires, reviews, or future outcomes absent from the structured arm. [Basis: FLARKO input ablations](https://arxiv.org/abs/2510.15993v1); [LangPTune §4.1/4.5](https://arxiv.org/abs/2410.18870v2)
- **Specify what “fixed ranker” means:** a fixed architecture with equally tuned but separately fitted models is a weaker control than identical fitted downstream weights; representation-specific input adapters may themselves change capacity. LangPTune has informative frozen-decoder comparisons but joint training is not fixed-weight treatment. Later synthesis should state the intended comparison precisely rather than equating these designs. [Basis: LangPTune §§3.2, 4.2, 4.5, Appendix B](https://arxiv.org/abs/2410.18870v2)
- **Handle provenance in summaries:** reconstructed holdings, adjusted dates/amounts, and simulated customer fields must not be verbalized as independently observed dated purchases or established risk traits. Prior FAR-Trans research documents the release construction; this session did not re-audit the raw records. [FAR-Trans §3.3.1/§3.4](https://arxiv.org/abs/2407.08692)
- **Separate accuracy from utility and faithfulness:** report nDCG@10 as purchase prediction for the stated RQ; any profitability or interpretability claim needs its own evidence. A coherent summary can still lose predictive information or invent preferences. [TOIS §12](https://doi.org/10.1145/3780097); [UPR §5.3/§7](https://aclanthology.org/2024.acl-long.753.pdf); [LangPTune §4.5](https://arxiv.org/abs/2410.18870v2)
- **Keep uncertainty paired and temporally aware:** shared users/candidates allow paired score differences; repeated time windows/users should not be treated as independent without justification. No effect size for the proposed FAR-Trans summary comparison is available yet. [Basis: TOIS §§6–7](https://doi.org/10.1145/3780097)

### Gaps

#### Remaining evidence gaps for handoff

1. **Class protocol:** official split/cutoff, horizon, sparse threshold/counting unit, candidate policy, repeat purchases, and approved feature sources are pending. No paper's protocol is substituted for the instructor's.
2. **Direct RQ evidence:** no measured matched summary-vs-structured effect for sparse FAR-Trans users; both benefit and harm remain plausible. No trained model or proposed experiment result is claimed.
3. **Version access:** final CIKM LangPTune and SIGIR Conv-FinRe full texts were not accessible through their ACM landing pages. Local/arXiv findings are version-qualified. Conv-FinRe's author-list discrepancy remains explicitly recorded.
4. **Reproducibility:** no source-code audit for candidate masks, sampling, invalid outputs, NoProfile reviews, metric preprocessing, or chronology. No raw FAR-Trans/customer-feature re-verification in this task.
5. **Literature breadth:** additional works referenced by these papers were not fully researched; no exhaustive novelty claim is supportable. Figure-only numerical differences were not digitized.

#### Exact URL/access ledger

The following URLs were requested in this session. DOI/publisher links elsewhere serve as canonical citations; do not infer successful landing-page access unless listed as such here.

| Requested URL | Outcome/use |
|---|---|
| `https://arxiv.org/abs/2510.15993` | Success; FLARKO title/authors/version/arXiv and related ACM DOI |
| `https://aclanthology.org/2024.acl-long.753/` | Success; official ACL title/authors/year/venue/pages/DOI |
| `https://arxiv.org/abs/2410.18870` | Success; earlier LangPTune title, authors, v1/v2 dates, arXiv DOI |
| `https://api.crossref.org/works?query.title=ConvFinRe&rows=3` | Zero matches for unhyphenated title query; not evidence of nonexistence |
| `https://api.crossref.org/works/10.1145/3780097` | Success; ACM-deposited TOIS metadata |
| `https://api.crossref.org/works/10.1145/3768292.3770399` | Success; ACM-deposited FLARKO metadata |
| `https://api.crossref.org/works?query.title=LangPTune&rows=2` | Success; single relevant CIKM publication record with official DOI |
| `https://arxiv.org/search/?query=ConvFinRe&searchtype=all&abstracts=show&order=-announced_date_first&size=50` | No exact unhyphenated match |
| `https://www.google.com/search?q=%22ConvFinRe%22` | JavaScript/retry page; no useful results |
| `https://www.bing.com/search?q=%22ConvFinRe%22` | Irrelevant results; not used as paper evidence |
| `https://dl.acm.org/doi/10.1145/3746252.3761369` | HTTP 403; final LangPTune full text not accessed |
| `https://github.com/ZhaolinGao/LangPTune` | Success; author repository links arXiv and describes data/training; implementation not audited |
| `https://api.openalex.org/works?search=ConvFinRe&per-page=3` | Zero matches for unhyphenated query |
| `https://api.semanticscholar.org/graph/v1/paper/search?query=ConvFinRe&limit=3&fields=title,authors,year,url,externalIds,openAccessPdf` | HTTP 429; no usable evidence |
| `https://html.duckduckgo.com/html/?q=%22ConvFinRe%22` | No exact-match results |
| `https://html.duckduckgo.com/html/?q=ConvFinRec+financial+recommendation` | Success; discovered correctly hyphenated Conv-FinRe arXiv, ACM DOI and author repository links; primary sources then opened |
| `https://api.crossref.org/works?query.title=conversational%20financial%20recommendation&rows=3&select=title,author,DOI,published,container-title,URL` | Results not the target; not used as substantive evidence |
| `https://arxiv.org/search/?query=conversational+financial+recommendation&searchtype=all&abstracts=show&order=-announced_date_first&size=50` | Success; target found among results; unrelated studies not researched |
| `https://arxiv.org/abs/2602.16990` | Success; Conv-FinRe 14-author arXiv list, version dates, acceptance comment, arXiv DOI |
| `https://arxiv.org/html/2602.16990v2` | Success; read complete main text through conclusion; truncation only later in references |
| `https://api.crossref.org/works/10.1145/3805712.3808658` | Success; ACM-deposited SIGIR publication details and 13-author list |
| `https://www.cs.cornell.edu/people/tj/publications/` | HTTP 403; no author-site final LangPTune version recovered |
| `https://dl.acm.org/doi/10.1145/3805712.3808658` | HTTP 403; final Conv-FinRe full text not accessed |

The sole new project deliverable from this continuation is this research-notes file. The separate writer can synthesize requested results files from these notes and `far_trans.md` without attributing paper verification to the user.
