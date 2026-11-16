# FAR-Trans: original-paper evidence for Abaidullah Seikh's Task 2

## 1. What publication was verified, and what does the dataset actually contain?

### Takeaway
The original full text is **Javier Sanz-Cruzado, Nikolaos Droukas, and Richard McCreadie (2024), “FAR-Trans: An Investment Dataset for Financial Asset Recommendation,” arXiv:2407.08692v1**, accepted at the **IJCAI-24 Workshop on Recommender Systems in Finance (Fin-RecSys)**. Its financial transaction histories include reconstructed and adjusted events; the released histories must not automatically be described as entirely unmodified observed purchases. [arXiv record](https://arxiv.org/abs/2407.08692); [full text, §3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1); [institutional publication record](https://eprints.gla.ac.uk/id/eprint/328250)

### Cited Findings

#### Research scope and provenance
- Assignment: evidence notes for student **Abaidullah Seikh**. RQ supplied by the user: **Do LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?** This wording and the Task 1 observations below are user-provided context, not claims sourced to the paper.
- Research performed on **2026-11-09**. The first action was reading the requested local `deep-research/references/researcher.md`. Only FAR-Trans was researched as a paper. Supporting pages were its arXiv record/full text, its official workshop pages, and its institutional data/publication records. The bibliography and other titles appearing on those pages were not followed into other-paper research.
- **Actually read:** the original arXiv HTML full text, including abstract, introduction, dataset construction (§3), task/methodology (§5.1–5.2), all Table 2 results and discussion (§5.3), and the complete conclusion (§6). Reading used HTML; no PDF download or PDF parsing was needed. The first rendered response truncated after the beginning of the conclusion; the subsequent text-format request exposed the complete conclusion. [full text](https://arxiv.org/html/2407.08692v1); [second full-text request](https://arxiv.org/html/2407.08692v1#S6)

#### Verified bibliography and identifiers
- Title and author order exactly as above. The paper identifies Sanz-Cruzado and McCreadie with the University of Glasgow, and Droukas with the National Bank of Greece. [full-text title block](https://arxiv.org/html/2407.08692v1)
- **Year/version:** 2024; the arXiv submission history lists only **v1, 11 July 2024, 17:30:04 UTC**. This is the version underlying every section/table claim in these notes. [arXiv record](https://arxiv.org/abs/2407.08692)
- **Venue:** arXiv says “Accepted at the IJCAI-2024 Workshop on Recommender Systems in Finance (Fin-RecSys).” The official program independently lists FAR-Trans as an accepted paper in the 11:00–11:30 slot, presented by Richard McCreadie. The workshop home page gives **4 August 2024, Jeju, Republic of Korea**. Cite as a workshop paper, not an IJCAI main-track paper. [arXiv](https://arxiv.org/abs/2407.08692); [official program](https://sites.google.com/view/fin-recsys2024/program); [official workshop home](https://sites.google.com/view/fin-recsys2024/)
- The institutional publication endpoint returned a BibTeX `@inproceedings` record with year 2024 and booktitle `IJCAI-24 Workshop on Recommender Systems in Finance (Fin-RecSys)`. Its `month = {June}` is a repository metadata value; do not replace the independently verified August workshop date with it. The repository BibTeX capitalizes the third surname `Mccreadie`, while the paper title block uses **McCreadie**, which is retained here. [institutional publication record](https://eprints.gla.ac.uk/id/eprint/328250)
- **arXiv DOI:** `10.48550/arXiv.2407.08692`, explicitly identified as arXiv-issued via DataCite. This is a preprint identifier, **not a separately verified publisher/proceedings DOI**. [arXiv record](https://arxiv.org/abs/2407.08692)
- **Dataset DOI:** `10.5525/gla.researchdata.1658`, identifying the University of Glasgow **data collection**, not the paper. The institutional data page confirms publisher, copyright holder National Bank of Greece, CC BY 4.0 files, deposit on 21 June 2024, and a collection period of **2 January 2018–29 November 2022**. This more precise interval is repository metadata; the paper describes January 2018–November 2022. [dataset record](https://researchdata.gla.ac.uk/1658/); [paper, §3](https://arxiv.org/html/2407.08692v1#S3)

#### Dataset contents and published statistics
- The paper describes a large European financial institution's data representing investment opportunities available to Greek investors, including stocks, bonds, mutual funds, prices, anonymized customers, and buy/sell transaction logs. Assets also span other European markets and some US securities. Its “first public dataset” claim is best retained in the qualified form used in §3: to the authors' knowledge, the first public FAR dataset containing **both** asset prices and investment transactions. §2.2 acknowledges an earlier public portfolio dataset lacking price/identifying information; it would be misleading to claim no earlier public financial recommendation data existed. [§2.2](https://arxiv.org/html/2407.08692v1#S2.SS2); [§3](https://arxiv.org/html/2407.08692v1#S3); [§3.2](https://arxiv.org/html/2407.08692v1#S3.SS2)
- **Table 1, verbatim values:** 806 unique assets; 321 assets with investments; 38 unique markets; 703,303 price points; 29,090 unique customers; transactions **388,049 (154,103 unique)**; acquisitions **228,913 (89,884 unique)**; sales **159,136 (64,219 unique)**. The parenthetical “unique” counts are preserved as the table labels them: the paper does not sufficiently define their deduplication key to safely relabel them as distinct user–item pairs. [Table 1](https://arxiv.org/html/2407.08692v1#S3.T1)
- Table 1 also gives whole-period average returns of **37.16% by assets** and **22.89% by customers**, with **54.28% profitable assets** and **54.56% customers with profits**. These are dataset descriptive statistics, not the monthly top-10 recommendation ROI in Table 2. [Table 1](https://arxiv.org/html/2407.08692v1#S3.T1)
- Asset metadata include asset type/subtype, name, trading market, and sector/industry where available. Customer data include bank segment, risk profile, and investment capacity. Risk profiles are estimated for **7,141** customers and capacity for **7,318**, rather than all being directly questionnaire-observed. [§3.2](https://arxiv.org/html/2407.08692v1#S3.SS2); [§3.4.2–3.4.3](https://arxiv.org/html/2407.08692v1#S3.SS4.SSS2)
- Transaction fields described by the paper are customer/asset identifiers, buy/sell type, date, number of shares, total monetary value, and execution channel. [§3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1)

#### Reconstruction and preprocessing: essential qualifications
1. Remove transactions without a customer identifier; adjust acquired/sold share counts for stock splits. For fractional shares after reverse splits, assume cash-in-lieu and add a sale on the split date. [§3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1)
2. Reconstruct purchases backing sales of pre-existing holdings. Short exact quote: **“we recreate those asset buys.”** If a customer's final 2022 balance for an asset is negative, add a buy for the excess sold shares at the earliest available price date, usually **2 January 2018**. These entries represent inferred prior holdings, not demonstrated purchases made on that assigned date. [§3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1)
3. Move transactions falling outside the asset price series to the closest date with a price. Add a sale if the customer still holds an asset after the price series ends. Estimate transaction value as adjusted share count multiplied by closing price on the transaction date. [§3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1)
4. Prices are deduplicated and cleaned; assets with zero closing prices or gaps longer than ten days are removed. Duplicate-value resolution uses proximity to preceding five-day prices, or following five days when currency changes mid-day; isolated extreme spikes are corrected; prices are converted to euros and adjusted for splits; remaining gaps use preceding five-day moving averages. These are release-construction operations, not a statement that the student's raw files should be changed. [§3.1.1](https://arxiv.org/html/2407.08692v1#S3.SS1.SSS1)
5. The paper attributes the January 2018 transaction spike to reconstructed prior holdings. Most recorded activity is January 2020–November 2022, exceeding 5,000 interactions monthly; January 2018–December 2019 generally has 1,000–2,000 monthly trades apart from that initial spike. [§3.3.2, Fig. 2(a)](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2)

#### Paper-versus-Task-1 discrepancies: preserve both records

The local values below come **only from the user's supplied Task 1 measurements**, not from a new file inspection in this research. The paper column is sourced to [Table 1](https://arxiv.org/html/2407.08692v1#S3.T1).

| Quantity | Paper Table 1 | User-provided Task 1 measurement | Interpretation |
|---|---:|---:|---|
| Transaction data records | 388,049 | **388,048 data rows + header** | Paper exceeds data-row count by 1; cause unverified |
| Customers | 29,090 | **29,090** | Counts agree |
| Assets traded / ISINs appearing in trades | 321 | **320 traded ISINs** | Difference of 1; equivalence of counting definitions and cause unresolved |
| Unique assets / metadata ISINs | 806 | **806 metadata ISINs** | Counts agree with Table 1 |

- Internal paper inconsistency: §3.2 says **807** assets with prices, and §3.3.2 says **321 out of 807**, while Table 1 says **806** unique assets. Also, §3.3.2 says the **top 12** assets account for **more than 50%** of interactions, whereas §5.3 describes **10** assets accounting for **around 50%**. Preserve these distinctions instead of silently harmonizing them. [§3.2](https://arxiv.org/html/2407.08692v1#S3.SS2); [§3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2); [Table 1](https://arxiv.org/html/2407.08692v1#S3.T1); [§5.3](https://arxiv.org/html/2407.08692v1#S5.SS3)
- User provenance correction: the user states they **personally verified transaction 7590224 and metadata, not papers**. This is not independent verification of the publication, a claim that this transaction explains the count discrepancy, or evidence of any particular transaction contents. No local raw data or Task 1 outputs were edited or remeasured here.

### Inferences
- A one-row difference compatible with header-inclusive counting is only a hypothesis, not an established explanation. The traded-asset discrepancy and the paper's internal 806/807 inconsistency remain separate unresolved issues. Their existence does not justify deleting or manufacturing records. [basis: Table 1](https://arxiv.org/html/2407.08692v1#S3.T1); user-provided counts above
- Because reconstructed early buys depend on balances computed through the end of 2022, an early-timestamp history in the released dataset is not automatically a strictly contemporaneously observed history. This is a **potential point-in-time validity issue**, not a demonstrated measurement of leakage or its effect on nDCG. Both representations would need the same treatment of reconstructed events to make a controlled comparison. [basis: §3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1)

### Gaps
- No separate published/proceedings DOI was present in the inspected arXiv record, institutional publication BibTeX, or official workshop pages. **Not verified** is the appropriate claim; this is not proof that none exists. The arXiv DOI and dataset DOI must remain distinct.
- The paper does not identify transaction 7590224 or resolve the user's local discrepancies. No transaction-specific interpretation is asserted.
- The institutional data page was last modified **18 February 2026**; its current metadata are not proof that downloadable file contents are byte-identical to the authors' 2024 experimental snapshot. No archive was downloaded or compared. [dataset record](https://researchdata.gla.ac.uk/1658/)

## 2. What exactly was evaluated, and what numerical results were reported?

### Takeaway
The paper evaluates **11 methods across 61 temporal variants**, with past history for training and **six months of future acquisitions** for evaluation, excluding already-bought assets and retaining users active in both train and test. **LightGCN has the highest aggregate nDCG@10, 0.3404**, compared with **popularity 0.2710**; these are neither sparse-user-specific results nor results from the pending class protocol. [§5.1–5.3](https://arxiv.org/html/2407.08692v1#S5); [Table 2](https://arxiv.org/html/2407.08692v1#S5.T2)

### Cited Findings

#### Task, split, and eligibility: the paper's stated protocol
- **Target:** rank assets for investor `u` at time `t`. Formally, the candidate ranking is a subset of `I \ I_u(t)`, where `I_u(t)` is defined as assets the customer **bought** before `t`. Thus this is prediction of new-to-user acquisitions, not unrestricted prediction of repeat purchases. The following prose uses “interacted” more broadly; retain the explicitly purchase-based mathematical definition when explaining the benchmark. [§5.1](https://arxiv.org/html/2407.08692v1#S5.SS1)
- **Input interaction representation:** binary user–item interest matrix, `Rel(u,i)=1.0` if the customer acquired the asset and `0.0` otherwise. The stated representation is not a graded rating based on share count, spending, frequency, or sale amount. [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **61 time points:** first `t0 = 1 August 2019`, providing approximately 1.5 years' initial training history. The paper says points are **“spaced two weeks apart”**, then illustrates mid-August and beginning of September. This is the published description; it does not give a complete date list. [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **Training:** pricing and transaction data prior to each `t`, implying an expanding past-history window rather than a stated fixed-length rolling training window. **Test:** prices and transactions in `(t, t + Δt)`, with `Δt = six months`. No random 80/20 split or leave-one-out split is specified. [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **Repeat purchases:** if a customer acquires an asset in both train and test, retain the training interactions only. **Customer inclusion:** retain customers with at least one interaction in **both** training and test. **Asset inclusion:** require pricing throughout the complete test period. The authors explain that this aligns customer/asset subsets for transaction and profitability metrics. [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **Candidate scope:** formally the available asset set minus previously purchased assets, with the complete-test-pricing filter above. The paper does not state that candidates are limited to the 321 globally traded assets, and it does not report a sampled-negative evaluation. Neither an exact per-window candidate count nor an additional train-interacted-item restriction is specified. [§5.1](https://arxiv.org/html/2407.08692v1#S5.SS1); [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **Metrics:** `nDCG@10` with relevance based on acquisition during the next six months; and `ROI@10`, the **monthly average** return of an equally weighted portfolio of the ten recommended assets held for that six-month horizon. A Table 2 ROI of 0.0259 is therefore reported as **2.59% monthly**, not 2.59% total six-month ROI. The paper does not provide the ROI annualization/monthly conversion equation. [§5.2.2](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS2)
- **Aggregation:** Table 2 columns are metrics averaged over all considered time points. The text does not spell out the exact within-window user aggregation or provide user counts/weights per window. [§5.3](https://arxiv.org/html/2407.08692v1#S5.SS3)
- **Hyperparameter selection:** for **each algorithm**, select parameters maximizing **ROI at six months** at three dates: **1 April 2019, 1 October 2019, 31 January 2020**. This is what the text states even though Hybrid-nDCG's learning objective is nDCG. Do not rewrite this as nDCG-based model selection. [§5.2.3, final paragraph](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS3)

#### Algorithms and features
All descriptions in the following list come from [§5.2.3](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS3); the cited algorithms' original papers were not separately opened.

1. **Random:** random asset recommendations as a sanity check.
2. **Price-based random forest**, **linear regression**, and **LightGBM regression**: predict ROI at `t + six months`, using close-price technical features: average price, ROI, volatility, moving average convergence divergence, momentum, rate of change, relative strength index, detrended close oscillator, ROI/volatility ratio, and prior-period maximum/minimum values. Exact feature lookback windows are not enumerated.
3. **Popularity:** rank by the number of past purchases; non-personalized. The text does not fully reconcile event-count popularity with its binary-matrix preprocessing, so do not silently assert a distinct-buyers implementation.
4. **LightGCN**, **matrix factorization (MF)**, **user-based kNN (UB kNN)**: collaborative-filtering approaches using transaction information.
5. **ARM:** Apriori association-rule mining.
6. **Hybrid-regression:** LightGBM regression predicting six-month profitability.
7. **Hybrid-nDCG:** LightGBM's LambdaMART ranking implementation optimizing nDCG. Both hybrids use outputs of the preceding recommendation algorithms as features; they are not LLM/text-summary hybrids.

#### Numerical benchmark: complete Table 2 transcription

Every numeric cell below is from **§5.3, Table 2**, averaged over the considered time points, at recommendation cutoff 10. ROI is recorded on the paper's decimal scale. [Table 2](https://arxiv.org/html/2407.08692v1#S5.T2)

| Data source | Algorithm/reference | nDCG@10 | ROI@10 |
|---|---|---:|---:|
| None | Random | 0.0106 | 0.0071 |
| Prices | Random forest | 0.0237 | **0.0259** |
| Prices | Linear regression | 0.0215 | 0.0249 |
| Prices | LightGBM | 0.0221 | 0.0225 |
| Transactions | Popularity | 0.2710 | 0.0006 |
| Transactions | LightGCN | **0.3404** | 0.0004 |
| Transactions | ARM | 0.2556 | 0.0007 |
| Transactions | MF | 0.1780 | 0.0038 |
| Transactions | UB kNN | 0.1599 | 0.0119 |
| Hybrid | Hybrid-nDCG | 0.2313 | 0.0063 |
| Hybrid | Hybrid-regression | 0.0261 | 0.0132 |
| Reference | Market average | — | 0.0079 |
| Reference | Customer average | — | 0.0018 |

- Only LightGCN exceeds popularity in nDCG among the tested methods. Price-based methods produce substantially lower nDCG values, even though all three exceed the market-average monthly ROI of 0.0079. UB kNN and Hybrid-regression also exceed that market ROI reference. This is an observed ranking in this benchmark, not a significance-tested or universally optimal model ordering. [Table 2 and §5.3](https://arxiv.org/html/2407.08692v1#S5.T2)
- **Conclusion actually read:** the authors distinguish methods effective at finding profitable assets from those predicting customer investments; non-personalized price prediction is better on the former, while collaborative filtering excels on the latter. Their proposed future work includes portfolio construction/optimization and investor/asset modelling. [§6](https://arxiv.org/html/2407.08692v1#S6)

### Inferences
- From the reported values, LightGCN exceeds popularity by **0.0694 absolute nDCG@10**, approximately **25.6% relative** (`(0.3404−0.2710)/0.2710`). This arithmetic is derived here, not a separately reported experimental result; it is not evidence of an LLM effect. [basis: Table 2](https://arxiv.org/html/2407.08692v1#S5.T2)
- Six-month test windows at approximately fortnightly origins overlap substantially. The 61 values therefore should not automatically be treated as 61 independent replicates for significance testing. [basis: §5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- The stated tuning dates are not all earlier than the first evaluation origin: October 2019 and January 2020 follow August 2019, and six-month tuning outcome periods can overlap evaluation periods. The text does not establish nested, time-isolated model selection. This is a reproducibility/temporal-separation concern, not proof of the exact implementation or a quantified leakage effect. [basis: §5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1); [§5.2.3](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS3)
- ROI-based hyperparameter selection can affect an nDCG comparison. These scores should be described as published baselines under their documented selection procedure, not as every method's best attainable nDCG under task-matched tuning. [basis: §5.2.3](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS3)

### Gaps
- Exact list/final date of the 61 origins, literal fourteen-day versus twice-monthly scheduling, timestamp boundary implementation, eligible user/item counts per origin, and treatment of items unseen in training are not fully specified. Do not manufacture a final cutoff from the approximate description.
- The paper does not report parameter grids/selected values, seeds, number of repeated stochastic runs, confidence intervals, significance tests, per-window results, or sparse-user-stratified results in Table 2/§5. It gives no sufficiently detailed separate validation protocol to resolve the tuning chronology.
- Precise gain/discount/ideal-ranking formula and tie handling for nDCG, handling of zero-relevant users beyond the stated filter, and exact ROI monthly conversion are not provided in this text. Referring to cited metric/method papers would require additional research outside this first-paper-only task.
- **Instructor protocol pending:** all splits/windows above belong to the paper's example/recommended benchmark. They are **not an established official class split**, and this research does not prescribe them as one.

## 3. What evidence does this provide for the sparse-history LLM-summary RQ, and what remains untested?

### Takeaway
FAR-Trans strongly motivates the dataset, future-purchase prediction target, nDCG@10 outcome, and the relevance of sparse histories. It provides **no direct evidence that LLM-generated transaction-history summaries improve nDCG@10**, and no representation-controlled experiment on sparse users. [§3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2); [§5](https://arxiv.org/html/2407.08692v1#S5); [§6](https://arxiv.org/html/2407.08692v1#S6)

### Cited Findings
- **Direct sparsity evidence:** §3.3.2 states **“over 50% of the users have 3 or less transactions between 2018 and 2022”** and approximately **650 customers have more than 100 transactions**. This concerns whole-period transactions, not a training-cutoff sparse-user cohort, unique purchased assets, or purchases only. [§3.3.2, Fig. 2(b)](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2)
- **Popularity evidence:** §3.3.2 reports that 75% of traded assets have over 20 interactions, 58% have over 100, and the top 12 concentrate over half the interactions. Popularity's 0.2710 nDCG@10 exceeds MF, ARM, UB kNN, and Hybrid-nDCG. These observations make popularity a material benchmark consideration rather than an ignorable trivial comparator. [§3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2); [Table 2](https://arxiv.org/html/2407.08692v1#S5.T2)
- **Evaluated population:** users must have interactions both before and after the recommendation time. The paper reports results for that eligible population, not every one of the 29,090 customers and not explicitly the sparsest half. [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
- **Representation evidence:** the transaction representation is a binary acquisition matrix; price models use technical indicators; hybrids combine model outputs. No evaluated method produces natural-language histories or compares an LLM summary against structured history with the same downstream predictor. The 11-model inventory and Table 2 exhaust the stated experimental comparison. [§5.2.1–5.2.3](https://arxiv.org/html/2407.08692v1#S5.SS2); [Table 2](https://arxiv.org/html/2407.08692v1#S5.T2)

### Inferences

The following are **research-design implications inferred from this paper**, not experiments performed or instructor-approved choices:

1. **Separate motivation from effect evidence.** The whole-period long tail motivates studying sparse histories, but it cannot establish that language summaries help those users. The relevant effect size, sign, and uncertainty are all unmeasured here. [basis: §3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2); [§5](https://arxiv.org/html/2407.08692v1#S5)
2. **Define sparsity using available training history.** A future-cutoff experiment needs an explicit training-only counting unit: transaction events, buy events, or distinct bought assets. The paper's whole-2018–2022 statistic is not a ready-made sparse-user label. Reconstructed initial buys and sell events can change those counts. [basis: §3.3.1–3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3); [§5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS2.SSS1)
3. **Distinguish sparse warm-start users from zero-history users.** The published train/test activity requirement excludes zero-history users and users without eligible future activity. Its aggregate score cannot be generalized directly to cold-start or inactive investors. Some very sparse histories may not survive novel-acquisition/test-activity filtering. [basis: §5.1–5.2.1](https://arxiv.org/html/2407.08692v1#S5.SS1)
4. **Hold information and modelling conditions constant for the representation claim.** Compare summaries and structured features derived from the same pre-cutoff events, with matched access to metadata/customer profiles, the same candidate universe, relevance targets, cohort, evaluation windows, downstream ranking method, and tuning budget. Otherwise a difference may reflect additional information or a different model, rather than history representation. The paper compares different algorithms/data sources; it does not supply this causal isolation. [basis: §5.2](https://arxiv.org/html/2407.08692v1#S5.SS2)
5. **Track provenance inside histories.** A language summary can mistakenly verbalize reconstructed holdings as real dated purchases, estimated amounts as exact execution values, or simulated profiles as confirmed traits. These possibilities follow from documented release construction; the paper does not measure LLM hallucination or summary fidelity. Equal preprocessing alone does not establish point-in-time authenticity of both inputs. [basis: §3.3.1](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS1); [§3.4.2–3.4.3](https://arxiv.org/html/2407.08692v1#S3.SS4.SSS2)
6. **Match the purchase target explicitly.** The paper predicts previously unpurchased assets over six months. If the student's intended target includes repeat purchases, or uses another horizon, its nDCG is a different experimental quantity; direct numeric comparison with 0.3404 would be inappropriate without harmonization. The pending instructor protocol decides this, not the paper alone. [basis: §5.1–5.2.2](https://arxiv.org/html/2407.08692v1#S5.SS1)
7. **Keep utility claims narrow.** Improved nDCG would support future observed-purchase prediction under the chosen evaluation, not necessarily higher profitability, lower risk, better financial advice, or improved welfare. The paper explicitly finds a divergence between transaction prediction and ROI. [basis: Table 2](https://arxiv.org/html/2407.08692v1#S5.T2); [§6](https://arxiv.org/html/2407.08692v1#S6)
8. **Generalization is bounded.** One institution's Greek-investor opportunity set, a relatively small and popularity-concentrated asset universe, and the January 2018–November 2022 market period limit claims about other brokers, asset catalogs, countries, or market regimes. This is an inference from dataset scope, not an external validation result. [basis: §3](https://arxiv.org/html/2407.08692v1#S3); [§3.3.2](https://arxiv.org/html/2407.08692v1#S3.SS3.SSS2)

### Gaps
- **Explicit RQ assessment:** this paper is a foundational dataset/benchmark source and sparsity motivation, **not affirmative or negative experimental evidence for LLM summaries**. It contains no LLM model/prompt specification, summary quality assessment, sparse-cohort nDCG, summary-versus-structured ablation, or paired representation comparison. This paper alone cannot establish a literature-wide novelty claim; only its own untested scope is established.
- No class-approved split, horizon, candidate policy, sparse threshold, feature set, or model-selection procedure was supplied. These remain pending rather than inferred from FAR-Trans's benchmark.
- No PDF-specific access gap exists: the original HTML was readable. Numerical figure coordinates/bars were not separately digitized; sparsity and popularity figures quoted here come from the accompanying prose, not visual estimates.

#### Exact URL/access ledger

These are the exact web URLs requested in this research, in request-group order. Section/table fragment links elsewhere in these notes are locators inside the already-opened full text, not claims of separate browsing.

| URL requested | Outcome and use |
|---|---|
| `https://arxiv.org/abs/2407.08692` | Success; title, author order, v1 submission history, workshop acceptance comment, arXiv DOI |
| `https://arxiv.org/html/2407.08692v1` | Success, Markdown; original full text including Tables 1–2; tool response truncated late in main text/references |
| `https://sites.google.com/view/fin-recsys2024/` | Success; official workshop title, date, location |
| `https://doi.org/10.5525/gla.researchdata.1658` | **HTTP 500**; DOI resolver failed on this attempt; subsequently recovered underlying institutional record directly |
| `https://arxiv.org/html/2407.08692v1#S6` | Success, text; returned full article, including complete conclusion; later truncation was in references |
| `https://sites.google.com/view/fin-recsys2024/program` | Success; independently verified FAR-Trans accepted-paper program entry |
| `https://researchdata.gla.ac.uk/1658/` | Success; official dataset metadata, DOI, collection interval, related FAR-Trans publication link; ZIP/README not downloaded |
| `https://eprints.gla.ac.uk/id/eprint/328250` | Success; returned institutional BibTeX for this paper, not publisher full text; no DOI field supplied |

No other paper full text was opened. No model was trained. The only intended project change is this evidence-notes file.
