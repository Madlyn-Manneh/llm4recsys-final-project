# Language-profile recommendation studies: evidence for sparse-history FAR-Trans RQ

Research notes for coordinator; prepared 2026-11-09 for Abaidullah Seikh's Task2 question: **Do LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?** This is a literature evidence record, not a final homework report or verification of student work. Course split remains pending. FAR-Trans was read separately first; no data analysis or changes to original data/Task1 outputs were made here. Publication metadata and the particular full-text versions read are distinguished below.

## 1. Paper A — what does UPR establish?

### Takeaway

UPR establishes that LLM-generated natural-language profiles from **written reviews** can support a reasonably competitive, editable **warm-start rating predictor**. It does not establish an improvement over structured histories for sparse users: its nDCG@10 is calculated on condensed lists of already-rated test items, and MF slightly exceeds every UPR nDCG result. [Published full text, §§3–5, Table 2](https://aclanthology.org/2024.acl-long.753.pdf)

### Cited Findings

**Verified citation and access**

- **Exact title:** *Transparent and Scrutable Recommendations Using Natural Language User Profiles*. **Complete authors in order:** Jerome Ramos; Hossein A. Rahmani; Xi Wang; Xiao Fu; Aldo Lipani. **Year/venue:** 2024, *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Bangkok, Thailand; Association for Computational Linguistics; August 2024; **pp. 13971–13984**. **Publication DOI: `10.18653/v1/2024.acl-long.753`**. Verified against official Anthology metadata and the publication PDF first page. [Official record and BibTeX](https://aclanthology.org/2024.acl-long.753/); [DOI](https://doi.org/10.18653/v1/2024.acl-long.753)
- **Version actually opened/read:** official ACL proceedings PDF, including abstract (p.13971), methodology (§3, pp.13973–13975), experimental setup (§4, pp.13975–13976), results (§5, pp.13976–13978), conclusion/limitations (§§6–7, p.13979), and relevant appendices/prompts (pp.13981–13984). PDF downloaded and text extracted locally as `/tmp/opencode/language_profiles_acl2024.pdf` and `.txt`. [Original full text](https://aclanthology.org/2024.acl-long.753.pdf)
- **Preprint chronology:** arXiv `2402.05810`, v1 **8 February 2024**, v2 **18 July 2024**; arXiv DOI `10.48550/arXiv.2402.05810`. Publication and first-preprint years are both 2024. ArXiv abstract/metadata was opened, but results here are sourced to the ACL PDF rather than an assumed identical arXiv version. **Metadata discrepancy:** arXiv spells the second author “Hossen A. Rahmani”; official ACL metadata and PDF say **“Hossein A. Rahmani”**, which is used in the publication citation. [arXiv record](https://arxiv.org/abs/2402.05810); [ACL record](https://aclanthology.org/2024.acl-long.753/)

**Method and information flow**

- UPR = **User Profile Recommendation**. Stage 1 extracts/ranks preference features from review explanations and ratings; stage 2 asks an instruction-tuned LLM to turn selected review passages into a first-person holistic profile; stage 3 fine-tunes a separate GPT-2 model for rating regression given the profile plus candidate **item title**. Neither user IDs nor item IDs are provided to UPR's profile-generation/recommendation prompts. This is not an LLM that directly emits a future-purchase top-10 list. [§§3.1–3.4, 4.4 and Appendix A.2](https://aclanthology.org/2024.acl-long.753.pdf)
- Feature ranking uses normalized ratings, feature coverage, and a statistical-significance discount; utility is `|r(f)| × cov(f) × sig(f)`. Features are stem-grouped, and generic features are manually removed. The paper describes aggregating ratings as an “average,” but printed Eq.(1) shows a sum; implementation would need checking before exact reproduction. Selected preferences can include dislikes. [§3.2, Eqs.(1)–(4), p.13974](https://aclanthology.org/2024.acl-long.753.pdf)
- Default generation: **Llama2-7B instruction-tuned or Mistral-7B instruction-tuned**, top **5 features**, **5 reviews per feature**, maximum **200 generated tokens**, temperature **0.7**. Thus this is a filtered review summary, not a lossless serialization of every history field. GPT-2 is trained with AdamW, batch size 8, learning rate `3e-4`; profiles are generated zero-shot, rather than the generator being optimized end-to-end for ranking. [§§3.3, 4.4, pp.13974–13976](https://aclanthology.org/2024.acl-long.753.pdf)
- Recommendation prompt explicitly asks, after the profile, for a 1–5 rating of `{title}`; training scales ratings to 0–1 and rescales for evaluation. Appendix A.3 lists learning-rate, scheduler, and batch-size exploration, 10 epochs maximum and stopping after 3 epochs without improvement. [Appendices A.2–A.3, p.13981](https://aclanthology.org/2024.acl-long.753.pdf)

**Data, splitting, metrics and baselines**

- Amazon Movies and TV (**Amazon-MT**) and **TripAdvisor hotels**, using explainable-recommendation datasets with user ID, item ID, 1–5 rating, and an explanation extracted from a written review. Missing-title records are excluded. An **8:1:1 train/validation/test split** is used, with every user and item occurring in each split and **at least five training reviews per user**. This is explicitly warm-start; §4.1 does not establish a chronological future-purchase split. [§4.1, p.13975](https://aclanthology.org/2024.acl-long.753.pdf)
- Table 1: Amazon-MT **4,811 users, 5,459 items, 288,693 records, 60.01 records/user**; TripAdvisor **9,765 users, 6,280 items, 320,023 records, 32.77 records/user**. Counts are for processed datasets, not sparse-user subgroups. [Table 1, p.13975](https://aclanthology.org/2024.acl-long.753.pdf)
- Metrics: **RMSE, MAE, MAP, nDCG@10**. MAP uses relevance threshold **4.0**. Critically, MAP/nDCG use **condensed lists: only items explicitly rated in the test set are considered**. The high nDCG values below must not be compared numerically with whole-catalog future-purchase retrieval. [§4.2, p.13975; Table 2](https://aclanthology.org/2024.acl-long.753.pdf)
- Baselines: MostPop by rating count; UserKNN with BM25 reweighting; ItemKNN with cosine; MF; NeuMF; **PETER+** (transformer rating/explanation model); **PEPLER-MLP** (GPT-2-based rating/explanation model). CF models use IDs/interactions; the explainable baselines also center user/item identifiers rather than a scrutable language profile. §4.3 says Cornac defaults for the initial baseline group, while §4.4 discusses validation tuning generally; no strong matched-optimization claim should be inferred. [§§4.3–4.4, pp.13975–13976](https://aclanthology.org/2024.acl-long.753.pdf)

**Numerical results — exact Table 2 values**

All entries in this table are from **Table 2, p.13977**, in the **published ACL PDF**; lower is better for RMSE/MAE, higher for nDCG/MAP. [Source](https://aclanthology.org/2024.acl-long.753.pdf)

| Model | Amazon RMSE | Amazon MAE | Amazon nDCG@10 | Amazon MAP | TripAdvisor RMSE | TripAdvisor MAE | TripAdvisor nDCG@10 | TripAdvisor MAP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MostPop | 1.505 | .962 | .896 | .815 | 1.277 | .902 | .932 | .857 |
| UserKNN | .960 | .707 | .935 | .864 | .836 | .634 | .952 | .883 |
| Item-KNN | 1.045 | .790 | .897 | .823 | .890 | .683 | .953 | .852 |
| MF | .925 | .686 | .941 | .870 | .786 | .599 | .960 | .891 |
| NeuMF | .943 | .694 | .936 | .866 | .819 | .634 | .955 | .886 |
| PETER+ | .924 | .685 | .941 | .870 | .803 | .621 | .958 | .889 |
| PEPLER-MLP | .925 | .672 | .941 | .869 | .793 | .606 | .959 | .889 |
| UPR (Llama2) | .944 | .678 | .938 | .866 | .804 | .616 | .955 | .885 |
| UPR (Mistral) | .941 | .679 | .940 | .870 | .804 | .610 | .952 | .887 |

- The strongest UPR nDCG is **.940 vs MF .941** on Amazon and **.955 vs MF .960** on TripAdvisor. “Competitive” is supported descriptively; blanket “summaries improve ranking over structured history” is not. Table 2 supplies neither uncertainty intervals nor significance tests for these comparisons. [Table 2; discussion §5.1](https://aclanthology.org/2024.acl-long.753.pdf)
- §5.2 / Figure 2 varies the number of selected **features** from 1 to 5, not the number of past interactions per user. More features reduce RMSE/MAE with diminishing returns. This is not a sparse-user study; no exact plot values are transcribed here. [§5.2 and Figure 2, pp.13976–13977](https://aclanthology.org/2024.acl-long.753.pdf)
- Profile quality study: five master's-student annotators judged 50 profiles per domain. Table 3 satisfaction rates (Amazon / TripAdvisor): fluency **95% / 92%**, informativeness **86% / 82%**, conciseness **75% / 72%**, relevance **90% / 87%**; Fleiss' kappa **0.82**. These are the paper's participants, unrelated to any verification of the student for this task. [§5.3, Table 3, pp.13977–13978](https://aclanthology.org/2024.acl-long.753.pdf)
- Scrutability test: sample **200 users** not mentioning a target preference, use Mistral to add it, rank **100 target-feature + 100 other items**, repeat five seeds, and measure target-feature **Coverage@10**. Coverage rises for positive additions (Figure 3), without retraining; negative preference edits yield only small decreases (Appendix A.6 / Figure 4). Coverage here means fraction of top-10 items with the target feature, not catalog coverage or predictive nDCG. [§5.4, pp.13977–13978; Appendix A.6, p.13982](https://aclanthology.org/2024.acl-long.753.pdf)
- Conclusion emphasizes comparable recommendation performance plus profile editability, with future work on multi-turn updates and bias. Limitations: dependence on review quality, loss of rarely mentioned preferences, predominantly positive reviews (average rating approximately 4/5), difficulty with negative preferences, LLM latency, information bottleneck/cognitive-load trade-off, and hallucinated inferred facts. [§5.3; §§6–8, pp.13978–13979](https://aclanthology.org/2024.acl-long.753.pdf)

### Inferences

- **Causal isolation: no.** UPR versus MF/NeuMF changes representation, predictor architecture, optimization, and available semantic information. UPR sees review-derived preferences and item titles plus pretrained language knowledge; conventional CF is not a matched structured-feature pipeline with that same information. PETER+/PEPLER comparisons are also different architectures/objectives. The top-k feature ablation holds much of UPR's machinery similar but never compares summaries with raw/structured histories under one fixed ranker. [Basis: §§3–5](https://aclanthology.org/2024.acl-long.753.pdf)
- **Directness to RQ: conceptual/methodological, low empirical directness.** It motivates generating and using an editable profile and warns about lossy summarization, but its warm-start explicit-rating target, review-rich inputs and condensed ranking differ from sparse transaction-based future asset purchases. Sharing the label nDCG@10 does not align the evaluation tasks. [Basis: §§4.1–4.2, 7](https://aclanthology.org/2024.acl-long.753.pdf)

### Gaps

- No FAR-Trans or asset-purchase experiment, no 0/1/2/3-interaction subgroup evaluation, and no isolated summary-versus-structured-input treatment were found in the read full text. UPR deliberately requires at least five training reviews. [Scope and setup](https://aclanthology.org/2024.acl-long.753.pdf)
- Publication full text is accessible; there is no full-text access gap for A. Exact split chronology and implementation-level prevention of held-out review information entering feature/profile construction would require a code audit; these notes do not certify either or allege leakage. The paper's broad wording about features over the dataset is insufficient for such a certification. [§§3.2, 4.1, 4.4](https://aclanthology.org/2024.acl-long.753.pdf)

## 2. Paper B — what does LangPTune establish, and what is its verified publication?

### Takeaway

**LangPTune is a CIKM 2025 publication**, DOI **`10.1145/3746252.3761369`**, with a differently titled 2024/2025 arXiv manuscript. The original arXiv v2 full text shows that optimizing profile generation improves on untrained language profiles for **four-item histories**, but its closest raw-history ablation favors **NoProfile-CL (.0543) over LangPTune (.0494)** on Movie-TV nDCG@20. This is valuable methodological evidence, not a demonstrated benefit on sparse FAR-Trans nDCG@10. [Official accepted-paper list](https://cikm2025.org/program/accepted-papers); [ACM-deposited metadata](https://api.crossref.org/works/10.1145/3746252.3761369); [Original manuscript, Tables 2–4](https://arxiv.org/html/2410.18870v2)

### Cited Findings

**Verified publication citation, title changes and access provenance**

- **Exact publication title:** *LangPTune: Optimizing Language-based User Profiles for Recommendation*. **Complete authors in order:** Zhaolin Gao; Joyce Zhou; Yijia Dai; Thorsten Joachims. **Publication:** *Proceedings of the 34th ACM International Conference on Information and Knowledge Management* (**CIKM '25**), ACM, **2025**, **pp.707–717**, Seoul, Republic of Korea. **DOI: `10.1145/3746252.3761369`**; Crossref's publisher-deposited online/print date is **10 November 2025**. These are not inferred from arXiv formatting. [ACM-deposited Crossref record, retrieved successfully with curl](https://api.crossref.org/works/10.1145/3746252.3761369); [Publication DOI](https://doi.org/10.1145/3746252.3761369)
- **Independent official venue/title/author verification:** CIKM 2025's official accepted-paper list includes **fp8779**, the exact LangPTune publication title, and all four authors. The official conference homepage announces ACM proceedings availability on 10 November 2025 and links proceedings DOI **10.1145/3746252**. These corroborate the proceedings identity in ACM's metadata. [Official accepted papers](https://cikm2025.org/program/accepted-papers); [Official conference/proceedings announcement](https://cikm2025.org/)
- **Original full-text version read:** *End-to-end Training for Recommendation with Language-based User Profiles*, **arXiv `2410.18870v2`, 12 February 2025**. First submission **v1, 24 October 2024**. Preprint DOI **`10.48550/arXiv.2410.18870`** is distinct from the ACM DOI. Read original arXiv HTML and downloaded original v2 PDF; abstract, methods (§3), experiments (§4 including Tables 1–6), conclusion (§5), and relevant appendix inputs were inspected. Local PDF/text: `/tmp/opencode/langptune_arxiv_v2.pdf` and `.txt`. **All experimental numbers below are explicitly v2 manuscript results, not independently checked numbers from ACM's final typeset version.** [arXiv metadata/history](https://arxiv.org/abs/2410.18870); [Versioned HTML](https://arxiv.org/html/2410.18870v2); [Versioned PDF](https://arxiv.org/pdf/2410.18870v2)
- **Version linkage:** first author's publication page labels the older-titled arXiv work **CIKM 2025** and reports its acceptance; the code repository uses that title and links the same arXiv ID. This connects the alternate title to the publication, but does not prove every table remained unchanged. [Author's page](https://zhaolingao.github.io/); [Authors' implementation repository](https://github.com/ZhaolinGao/LangPTune)
- **Access gap:** ACM article landing page, `/doi/full/` and PDF endpoint returned **HTTP 403**. The publication metadata is verified from the official conference and ACM's Crossref deposit; the final ACM full text was not accessible in this session. ArXiv v2 is an original author manuscript and was actually opened, not merely an abstract. Its HTML includes bogus ACM template placeholders (“2018,” Woodstock, `XXXXXXX.XXXXXXX`); these are **not** publication metadata. [Attempted ACM article](https://dl.acm.org/doi/10.1145/3746252.3761369); [Attempted ACM PDF](https://dl.acm.org/doi/pdf/10.1145/3746252.3761369); [v2 HTML header](https://arxiv.org/html/2410.18870v2)

**Method — what is optimized?**

- **Profile encoder π:** an LLM maps the sequence of interacted items, annotated with item metadata and user reviews, to a natural-language preference profile. **Recommender decoder σ:** text embedding model **Mxbai (`mixedbread-ai/mxbai-embed-large-v1`)** embeds profile and each candidate's metadata; an inner product scores them and sorting forms the ranking. The model formulation ranks the item collection rather than asking an LLM to select from a tiny prompt candidate set. [§3.1, Eqs.(1)–(3), v2 pp.2–3](https://arxiv.org/html/2410.18870v2#S3.SS1)
- **RLSO (Reinforcement Learning for System Optimization):** sample two profiles for one history, evaluate downstream ranking reward against held-out-within-training future items, and regress relative rewards against relative profile log probabilities. The derivation uses a KL-constrained update. **CL:** train the Mxbai decoder with InfoNCE to prefer the future positive over other items in a batch. LangPTune alternates decoder CL and profile-generator RLSO, so the main approach changes **both generator and ranker**. [§3.2, Eqs.(4)–(10), Algorithm 1, v2 pp.3–4](https://arxiv.org/html/2410.18870v2#S3.SS2)
- Encoders: **Gemma-2B-it (`google/gemma-2b-it`)** with LoRA; **Llama-3-8B-Instruct** with the final four layers trained. Maximum profile **512 tokens**; Mxbai full-parameter training. Uses NDCG reward, batch standardization, optional additional KL-to-initial-policy penalty and a penalty for excessive generation length. Training is substantial: paper reports 8 A6000 GPUs, approximately two days for Llama experiments and one day for Gemma, with decoder iterations about one hour. [§4.3, Eq.(11), v2 pp.5–6](https://arxiv.org/html/2410.18870v2#S4.SS3)

**Datasets, history regime, metrics and controls**

- **Amazon-Movie-TV and Amazon-Books**. Inputs include item **title, description, average rating, category and price**, plus the user's **review text and rating** in the generation prompt. Appendix A explicitly orders reviewed items chronologically, oldest to newest. These are richer observations than transaction IDs/counts alone. [§4.1 and Appendix A](https://arxiv.org/html/2410.18870v2#S4.SS1); [Input examples](https://arxiv.org/html/2410.18870v2#A1)
- Filter sessions/items with fewer than **5 interactions**, remove item metadata exceeding **512 tokens** and histories exceeding **1,024 tokens**. Each example uses **4 historical items to predict 1 future item**, all five distinct. Thus there is genuine **short-history input**, but not a zero-history test or a test across natural history-count strata. [§4.1, v2 pp.4–5](https://arxiv.org/html/2410.18870v2#S4.SS1)
- Table 1: Movie-TV **14,698 / 1,392 / 1,392 train/validation/test sessions**, **10,533 items**, **87,410 interactions**; Books **4,404 / 361 / 361 sessions**, **4,819 items**, **25,630 interactions**. Metrics in reported tables are **Recall@20, MRR@20, NDCG@20**, not @10. [Table 1 and §4.1, v2 p.5; Tables 2–4](https://arxiv.org/html/2410.18870v2#S4.T1)
- **Language-profile controls:** LangPTune-0 = pretrained generator and decoder, no task training; LangPTune-CL = train only decoder, freeze generator; LangPTune-RLSO = train only generator, freeze decoder; full LangPTune = train both. These are comparable pipeline variants inspired by prior approaches, **not literal reproductions** of UPR's GPT-2 regression model. [§4.2.1, v2 p.5](https://arxiv.org/html/2410.18870v2#S4.SS2.SSS1)
- **Conventional controls:** Random; Most Popular; NMF; LightGCN with BPR; MCL; BERT4REC; LLM2BERT4REC. Ordinary black-box methods use user/item histories without rich textual metadata; **LLM2BERT4REC is an important exception**, initializing item representations from text-description embeddings. Popularity and all black-box baselines may use history items from validation/test users during training, excluding their future target as described. This is transductive history availability, not an untouched-user inductive cold-start benchmark. Each baseline is tuned on validation data. [§§4.2.2–4.3, footnote 1, v2 p.5](https://arxiv.org/html/2410.18870v2#S4.SS2.SSS2)

**Numerical results — v2 Table 2, p.6**

The following are exact original-manuscript Table 2 entries. All three metrics use **@20**. Full-model relative improvements over zero-shot NDCG are **54.3% / 57.0%** for Gemma (Movie-TV / Books), and **113.9% / 36.5%** for Llama. These percentages compare **training procedures within language-profile pipelines**, not summaries against structured inputs. [Table 2](https://arxiv.org/html/2410.18870v2#S4.T2)

| Encoder | Method | Movie-TV Recall | Movie-TV MRR | Movie-TV NDCG | Books Recall | Books MRR | Books NDCG |
|---|---|---:|---:|---:|---:|---:|---:|
| Gemma | LangPTune-0 | .0643 | .0189 | .0289 | .3397 | .1269 | .1743 |
| Gemma | LangPTune-CL | .0863 | .0317 | .0436 | .3587 | .1516 | .1984 |
| Gemma | LangPTune-RLSO | .0746 | .0253 | .0364 | .4212 | .1872 | .2400 |
| Gemma | LangPTune | .0859 | .0327 | .0446 | .4375 | .2151 | .2736 |
| Llama | LangPTune-0 | .0535 | .0146 | .0231 | .3370 | .1285 | .1753 |
| Llama | LangPTune-CL | .0938 | .0319 | .0456 | .3995 | .1539 | .2099 |
| Llama | LangPTune-RLSO | .0763 | .0289 | .0377 | .3913 | .1728 | .2224 |
| Llama | LangPTune | .0970 | .0358 | .0494 | .4212 | .1860 | .2393 |

- Table 2 paired t-tests use **α=.05**. Full LangPTune's NDCG improvement over CL-only on Movie-TV/Gemma is **2.29% and not marked significant**; Llama's corresponding improvement is **8.33% and marked significant**. Avoid claiming universal statistically significant superiority or universal improvement in all metrics: Gemma Movie-TV Recall is .0859 versus CL-only .0863. [Table 2 and §4.4.1](https://arxiv.org/html/2410.18870v2#S4.T2)

**Conventional comparisons — v2 Table 3, p.7**

Table 3 uses the LangPTune encoder chosen on validation performance (Llama for Movie-TV, Gemma for Books). Exact NDCG@20 values below. [Table 3; §4.4.2](https://arxiv.org/html/2410.18870v2#S4.T3)

| Model | Movie-TV NDCG@20 | Books NDCG@20 |
|---|---:|---:|
| Random | .0006 | .0014 |
| Most Popular | .0039 | .0729 |
| NMF | .0350 | .2323 |
| LightGCN | .0525 | .2586 |
| MCL | .0563 | .2134 |
| BERT4REC | .0384 | .2235 |
| LLM2BERT4REC | .0423 | .2343 |
| LangPTune | .0494 | .2736 |

- LangPTune beats the listed black-box models on Books; on Movie-TV it is **5.90% below LightGCN** and **12.3% below MCL** in NDCG@20, both marked significant. Books improvement over LightGCN is **5.80%**, marked significant. Richer descriptions and possible stronger pretrained book knowledge are the authors' explanations/hypotheses, not experimentally isolated causal findings. [Table 3 and §4.4.2](https://arxiv.org/html/2410.18870v2#S4.T3)

**Most relevant ablation — v2 Table 4, p.7**

NoProfile-0 feeds the history's **raw item-metadata list directly into the same pretrained Mxbai embedding model**, bypassing generation; NoProfile-CL trains that direct-history embedding model with InfoNCE. This is much closer to the representation question than comparing LangPTune to MF. The textual raw-history baseline is still not a conventional tabular structured-feature predictor. [§4.5.1 and Table 4](https://arxiv.org/html/2410.18870v2#S4.SS5.SSS1)

| Movie-TV method | Profile max tokens | Recall@20 | MRR@20 | NDCG@20 |
|---|---:|---:|---:|---:|
| LangPTune (Llama) | 64 | .0604 | .0201 | .0319 |
| LangPTune (Llama) | 128 | .0901 | .0313 | .0444 |
| LangPTune (Llama) | 256 | .0929 | .0352 | .0482 |
| LangPTune (Llama) | 512 | .0970 | .0358 | .0494 |
| NoProfile-0 | N/A | .0760 | .0261 | .0372 |
| NoProfile-CL | N/A | .1012 | .0408 | .0543 |

- Authors interpret direct-history NoProfile-CL's advantage as evidence of the summary **information bottleneck**. The .0494 versus .0543 difference is **−.0049 absolute**, approximately **−9.0% relative** (our arithmetic from displayed values, not a reported significance result). The table does not give a significance test for this pair. [Table 4 and §4.5.1](https://arxiv.org/html/2410.18870v2#S4.T4)
- A particularly useful fixed-decoder comparison is possible across Tables 2 and 4 on Movie-TV: **NoProfile-0 .0372**, Llama **LangPTune-0 .0231**, and Llama **LangPTune-RLSO .0377**. Both -0 and -RLSO use an unchanged pretrained decoder; RLSO changes generator training. This shows neither zero-shot summarization nor joint optimization should automatically be equated with a benefit from summary generation alone. Exact input-field parity (especially user reviews versus raw metadata), preprocessing/truncation parity and significance of the .0005 RLSO/NoProfile-0 difference are not established here. [Tables 2, 4; §§4.2.1, 4.5.1, 4.7](https://arxiv.org/html/2410.18870v2)

**Sparse/cold-start and interpretability evidence**

- **Training-data-size ablation:** reduce Movie-TV training data from **100% to 0.1%**; Figure 4 shows LangPTune degrading less than MCL/LLM2BERT4REC. Authors suggest usefulness for cold-start when little training data exists. This varies **global training-set size**, not the number of observations available for each evaluated user (fixed four), and is not a direct zero-history/new-user or natural sparse-cohort experiment. No invented point values are read from the plot. [§4.5.2, Figure 4, v2 p.7](https://arxiv.org/html/2410.18870v2#S4.SS5.SSS2)
- Interpretability experiment: **450 Movie-TV test items**, human or **GPT-4-0613** chooses between the true next movie and one random alternative, with alternatives consistent across profile variants. Table 5 human accuracy: raw **57.11%**, zero-shot profile **54.67%**, trained profile **58.89%**; GPT-4: **75.56%, 73.33%, 76.67%** respectively. Human trained-vs-zero-shot **p=.201**; trained-vs-raw **p=.624**: neither is significant. This is a two-choice usefulness/readability proxy, not rank-10 accuracy or comprehensive faithfulness validation. [§4.6, Table 5, v2 pp.7–8](https://arxiv.org/html/2410.18870v2#S4.SS6)
- Table 6 mean response duration: raw **34.76 seconds**, zero-shot profile **28.77**, trained profile **29.15**; mean word counts **465, 292, 256** respectively, after reported outlier filtering. Results suggest a reading-effort trade-off, not proof of improved predictive ranking. [Table 6, v2 p.8](https://arxiv.org/html/2410.18870v2#S4.T6)
- Conclusion: jointly optimized profiles are competitive while remaining readable; user **steerability through manual profile edits** and accommodating **longer histories** or better item descriptions are future work. Unlike UPR, the v2 conclusion does not report a completed manual-edit steerability experiment. [§5, v2 p.8](https://arxiv.org/html/2410.18870v2#S5)

### Inferences

- **Main comparison does not isolate summary generation.** LangPTune versus CF changes textual side information, pretrained knowledge, model capacity and optimization; versus LangPTune-0 it changes both training components. “+113.9%” is not an estimate of a summary-versus-structured-history effect. [Basis: §§3.2, 4.2–4.4](https://arxiv.org/html/2410.18870v2)
- **Some useful component isolation exists.** RLSO versus -0 holds the decoder fixed and tests optimizing the generator, but both generate summaries. NoProfile-0 versus -0 gets closer to a fixed-ranking-model summary/no-summary comparison; full LangPTune versus NoProfile-CL holds decoder family similar but learns different parameters. Thus it would be wrong to say the paper has no relevant ablation, or that it cleanly answers the exact FAR-Trans representation RQ. [Basis: §§4.2.1, 4.5.1, 4.7](https://arxiv.org/html/2410.18870v2)
- **Closest of these two on future-item ranking with short histories:** B. It combines four past interactions, future-item prediction, and a direct-history bypass; its nearest-control result cautions that profile compression can lose ranking information. This is a local methodological assessment only; the coordinator should select overall nearest prior work across the full literature set. [Basis: §§4.1, 4.5.1](https://arxiv.org/html/2410.18870v2)

### Gaps

- **Final-version content gap:** ACM full text unavailable (403); the title/venue/authors/pages/DOI are verified, but experimental revisions between February 2025 arXiv v2 and November 2025 proceedings remain unchecked. Use version-aware citations for all reported numbers. [Publication metadata](https://api.crossref.org/works/10.1145/3746252.3761369); [Read version](https://arxiv.org/abs/2410.18870v2)
- No FAR-Trans, asset-purchase, nDCG@10, true zero-history, or stratified history-count result was found in v2. The five-interaction filtering excludes the very-short-history users before constructing four-item inputs. [§4.1](https://arxiv.org/html/2410.18870v2#S4.SS1)
- The read sections establish chronological prompt order and a future item but do not fully specify a global calendar-based train/test protocol equivalent to prospective financial prediction. Candidate exclusions, exact negative-sampling implementation, raw-history review-field parity, and snapshot timing of metadata/average ratings need code-level verification before reproduction. No repository execution or data audit was performed. [§§3.1, 4.1–4.3, Appendix A](https://arxiv.org/html/2410.18870v2); [Repository](https://github.com/ZhaolinGao/LangPTune)

## 3. Cross-paper assessment — methodological proximity and implications for the Task2 RQ

### Takeaway

The evidence supports **testing** natural-language profiles as a representation, not predicting a positive FAR-Trans result in advance. UPR supplies the review-to-profile/editability design; LangPTune supplies the stronger future-item and short-history precedent, plus a crucial counterexample where direct history beats generated profiles. Neither demonstrates the requested sparse-user financial nDCG@10 effect. [A, §§4–7](https://aclanthology.org/2024.acl-long.753.pdf); [B, §§4.1–4.5](https://arxiv.org/html/2410.18870v2)

### Cited Findings

- **Local comparison:** A uses ≥5 training reviews/user, warm-start ratings, GPT-2 regression, nDCG@10 on rated-test-only lists; B uses exactly four historical items, next-item ranking through Mxbai, and nDCG@20, with raw-history controls. Neither uses financial transactions. [A, §§3.4, 4.1–4.2](https://aclanthology.org/2024.acl-long.753.pdf); [B, §§3.1, 4.1, 4.5.1](https://arxiv.org/html/2410.18870v2)
- **Immediate methodological predecessors identified by the papers:** UPR explicitly calls Sanner et al. (2023), *Large Language Models are Competitive Near Cold-start Recommenders for Language- and Item-based Preferences*, most similar, distinguishing its human-written preferences/near-cold-start scenario from UPR's generated-review profiles/warm-start setting. UPR also builds on Balog et al. (2019)'s feature-ranking/set-preference approach. These descriptions are from A's related-work section; those predecessor full texts were not separately researched in this assignment. [A, §§2.2–3.2 and references](https://aclanthology.org/2024.acl-long.753.pdf)
- LangPTune explicitly connects its zero-shot baseline to **Joyce Zhou, Yijia Dai and Thorsten Joachims (2024), *Language-Based User Profiles for Recommendation*, arXiv:2402.15623**; it cites UPR and PALR as motivations for training only a downstream recommender on generated profiles. This is an immediate method lineage, not a verified claim that those works demonstrate financial or sparse-user benefits. [B, §2, §4.2.1, reference list](https://arxiv.org/html/2410.18870v2); [Predecessor locator, not separately full-text reviewed](https://arxiv.org/abs/2402.15623)

### Inferences

- **Provisional local nearest-method recommendation:** prioritize **LangPTune** when explaining why a summary-to-embedding-to-ranking design with short histories is plausible, and cite **UPR** for the earlier automated profile-generation/editability premise. The overall nearest paper and final Task2 literature choice remain with the coordinator, who has the separate FAR-Trans and other-paper evidence. [Basis: A §§3–5; B §§3–4](https://arxiv.org/html/2410.18870v2)
- **Define the treatment narrowly.** To answer the stated RQ, compare the same pre-cutoff transactions and allowed asset attributes represented as structured features versus LLM summaries, with a common candidate set, target purchases, ranking/evaluation protocol and training budget. If both representations require different encoders, hold the downstream scoring architecture/objective fixed and acknowledge the encoder difference; literal frozen-decoder ablations can supplement rather than substitute for structured-feature comparisons. A text-serialized-history baseline and a deterministic/template summary would help distinguish semantic generation from mere formatting/compression. These are proposed controls motivated by A's confounds and B's NoProfile ablation, not procedures the two papers jointly validate for finance. [Basis: A §§4.3–5.1](https://aclanthology.org/2024.acl-long.753.pdf); [B §§4.2, 4.5.1](https://arxiv.org/html/2410.18870v2)
- **Information parity matters.** Reviews reveal explicit sentiment and rich item semantics in both papers. Transaction records alone do not necessarily reveal the same motives. A summary that introduces external descriptions, extra asset attributes or unsupported investor preferences changes information as well as representation. Keep those sources matched across conditions, or explicitly label the experiment as augmentation. This is a transfer-risk inference, not a finding about FAR-Trans performance. [Basis: A §§3.1–3.3, 5.3; B §4.1 and Appendix A](https://arxiv.org/html/2410.18870v2)
- **Sparse is not synonymous with cold-start.** Four historical observations, few total training sessions, unseen users, unseen items and zero interactions are distinct conditions. Define sparse cohorts using only the training history, report their sizes and paired nDCG@10 differences, and avoid pooling them into an unqualified cold-start claim. Neither A's feature-count ablation nor B's training-size curve supplies that missing cohort result. [Basis: A §5.2](https://aclanthology.org/2024.acl-long.753.pdf); [B §§4.1, 4.5.2](https://arxiv.org/html/2410.18870v2)
- **No metric extrapolation:** A's .94-scale condensed-list nDCG and B's .02–.27-scale full-item-ranking nDCG@20 arise from different relevance/candidate protocols. Neither can be converted into an expected FAR-Trans nDCG@10 gain. The strongest defensible synthesis is “profile optimization can outperform zero-shot profiles; summaries may also lose useful history information.” [Basis: A §4.2/Table 2](https://aclanthology.org/2024.acl-long.753.pdf); [B Tables 2–4](https://arxiv.org/html/2410.18870v2)

### Gaps

- **Still unresolved for the student RQ:** the sparse-history threshold, permitted information, precise future-purchase label/candidate policy, course-prescribed split and the actual FAR-Trans paired comparison. These are assignment/design questions, not gaps that can be filled with either paper's results.
- **Access summary:** A proceedings full text read successfully; B original arXiv v2 full text read successfully and official publication metadata verified, but B final ACM full text blocked. Bibliographic certainty does not imply verified equivalence of preprint and proceedings experiments. [A official source](https://aclanthology.org/2024.acl-long.753/); [B official acceptance](https://cikm2025.org/program/accepted-papers); [B publisher-deposited metadata](https://api.crossref.org/works/10.1145/3746252.3761369); [B read manuscript](https://arxiv.org/abs/2410.18870v2)
