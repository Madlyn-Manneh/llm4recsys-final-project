# Profile-augmented LLM transaction summaries for sparse-history financial asset recommendation: a development study

**Name:** Madlyn Manneh\
**Team:** Eight(8)\
**Date:** 2026-11-26\
**Assignment:** Homework 3: Test Your Project Idea (Session 3, Individual)\
**Repository:** https://github.com/Madlyn-Manneh/llm4recsys-final-project (folder Madlyn_Manneh/session3)

## Abstract

Retail investors in FAR-Trans have sparse purchase histories, so a transaction-only representation carries little signal. This report tests whether adding risk level and investment capacity to an LLM-written summary of a customer’s purchase history changes nDCG@10 for a Qwen3-1.7B reranker of the starter’s fixed 50 content-based candidates. On the team’s 200-user development sample (cutoff 2021-06-01, 30-day window, 24 users with future purchases), the profile-augmented arm D scores 0.0264 over all users, below the history-only arm C at 0.0286, and the shuffled-profile ablation E scores 0.0258. Each difference rests on a handful of users, and the ranker’s top 10 changes little with the summary text. I find no evidence that the profile fields help. These are development results.

## Introduction

Retail investors in FAR-Trans are heavily long-tailed. The dataset paper \[1\] reports that over half of the 29,090 customers have three or fewer transactions across the 2018 to 2022 period. For these sparse-history customers a transaction-only representation is thin, and an LLM summary of that history can collapse into generic phrasing. I ask whether adding two structured fields that the bank already records, the customer’s risk level and investment capacity, to that summary gives the ranker extra, non-leaking signal.

My research question (RQ4) is whether a profile-augmented summary changes nDCG@10 compared with a history-only summary, for FAR-Trans users with sparse purchase histories. Candidates, asset information, ranker template and metric are held constant; arm D differs from arm C only in the summary prompt, which adds the profile block and an instruction to relate it to the purchases. The outcome is the mean nDCG@10 against the assets bought in the following 30 days. For example, user U031 bought one asset in June 2021, at CBF position 3; the question is whether a summary, with or without the profile, moves it up (C ranks it 2nd, D 4th). A null or negative answer still says whether a longer, profile-dependent prompt is worth its cost for this subgroup.

I make three contributions: a two-stage LLM pipeline (summary step, then reranking) with a raw-history arm and the CBF control to separate the two steps; a seeded cyclic profile-shuffle ablation that tests whether the profile content, and not just the presence of a profile block, drives any change; and a hand-worked nDCG@10 check with an environment and runtime record that separates generation time from model start-up.

## Related Work

FAR-Trans \[1\] is the public financial asset recommendation dataset used here, with 29,090 customers, 806 assets and transactions from 2018 to 2022; its paper benchmarks price-based, transaction-based and hybrid recommenders but no LLM summary representation. The closest neighbours are LLM-based user profiles: LFM \[2\] turns a rating history into a natural-language profile, and EmbSum \[3\] uses LLM summaries of long histories to help a content-based ranker. In finance, FLARKO \[4\] gives an LLM knowledge graphs of transaction histories on FAR-Trans, and Conv-FinRe \[5\] is a conversational benchmark. Sabouri et al. \[6\] report smaller benefits of LLM user profiling in sparser environments, which matters for my sparse-history focus. The course’s provided baselines adapt LLM-Rec \[7\] and LLMRank \[8\]. None of these tests whether risk level and investment capacity added to an LLM history summary change nDCG@10 for sparse FAR-Trans users. I keep the candidates fixed, since an LLM encoder feeding retrieval would mix the representation with retrieval.

## Method

The pipeline treats the LLM as both an encoder and a ranker. (1) The starter builds each user’s context as of the cutoff: the Buy history before the cutoff, asset attributes and 50 CBF candidates; no future transaction enters a prompt. (2) For arms C, D and E the LLM first writes a short summary of the history, which becomes the investor information block; arm B puts the raw history there instead. (3) The ranker prompt lists the 50 candidates and the block and asks for ten candidate numbers as JSON; an invalid answer is replaced by the CBF top 10. (4) The starter scores the top 10 next to the four baselines. The ranker sees the profile fields only through the summary.

Five arms are compared, all sharing the same candidate set, asset information, ranker template and top-10 output, alongside the four provided baselines (Popularity, CBF, Latest buy, Latest buy or sell). Arm B passes the raw history, one line per asset, to the ranker without any summary, which isolates the summary step against the CBF control. Arm C is the LLM summary of the history only; it is the team’s Session 2 summary instruction, which Abaidullah’s (Dastan) report calls old C (his own fact-preserving summary is a different arm, not used here). Arm D is the summary plus risk level and investment capacity, flagged as observed or estimated; it is the primary comparison against C. Arm E is the one ablation: D with each available profile replaced by another user’s under a seeded cyclic permutation in which no user keeps their own, so E tests the profile values and not the profile block. Users with no available profile keep the not-available text. Only the investor block differs between arms.

The model is Qwen/Qwen3-1.7B at revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e, with thinking disabled, greedy decoding, seed 0, at most 120 summary and 60 ranking tokens, in float32 on CPU (Python 3.12.10, torch 2.11.0+cpu, transformers 4.57.6; AMD Ryzen 5 7430U, 15.4 GB RAM, Windows 11).

The development sample is the deterministic 100-user HW2 sample (warm users ordered by the SHA-256 of a salted customer identifier, first 100), extended by users 101 to 200 in the same order. The cutoff is 2021-06-01, the label window is the following 30 days, repeat purchases are allowed, each user has 50 content-based candidates, and users with no future purchases count as zero. All methods share users, cutoff, assets and labels, and every nDCG@10 is recomputed from the saved rankings. These are development results, not official benchmark scores.

Deviations and reproducibility. The protocol was committed before any HW3 model run (commit 479dde0ad88c5a9809f490d31a968e483ae3c059); the extension sample has its own protocol hash, 5bae3e69d666acbc9f80421ffd4a5b6733d197d10a0894822ecd6674cfb413f5. The first attempt of arm E failed at start-up with a network name-resolution error before any output was written and is not part of the results; the rerun and the extension runs used offline mode (HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1). Per-user result files contain customer identifiers and are not committed, because of the course data rule.

## Experiments

Table 1 reports the primary metric for the baselines and the four LLM arms on the 100-user primary sample and on the 200 pooled users. The mean is over all users of the sample, with empty truth counted as zero; the labelled columns are means over the 11 primary and 24 pooled users with future purchases.

| **Method** | **Primary all users** | **Primary labelled (11)** | **Pooled all users** | **Pooled labelled (24)** |
|:---|---:|---:|---:|---:|
| Popularity | 0.0286 | 0.2599 | 0.0342 | 0.2852 |
| Latest buy | 0.0277 | 0.2520 | 0.0474 | 0.3946 |
| Latest buy or sell | 0.0271 | 0.2464 | 0.0484 | 0.4033 |
| CBF (initial candidate order, matched control) | 0.0201 | 0.1827 | 0.0305 | 0.2539 |
| B (raw history, no summary) | 0.0228 | 0.2076 | 0.0304 | 0.2531 |
| C (summary only) | 0.0248 | 0.2257 | 0.0286 | 0.2385 |
| D (summary + risk level and capacity) | 0.0220 | 0.1996 | 0.0264 | 0.2196 |
| E (D with shuffled profiles) | 0.0209 | 0.1899 | 0.0258 | 0.2152 |

The profile arm D is below the history-only arm C by 0.0029 over all users and 0.0262 over the 11 labelled users; the shuffled-profile arm E is below D by 0.0011 and 0.0097. Table 2 gives the paired differences and the counts of users who score higher, lower or equal. These differences rest on very few users (the D-minus-C drop is driven by two labelled users, and one moves the other way), so I report no significance test. My reading is that there is no evidence that the profile fields help, and that the development difference is small and negative.

| **Pair** | **Primary all** | **Primary labelled** | **Primary higher / lower / equal** | **Pooled all** | **Pooled labelled** | **Pooled higher / lower / equal** |
|:---|---:|---:|---:|---:|---:|---:|
| D - C | -0.0029 | -0.0262 | 1 / 2 / 97 | -0.0023 | -0.0189 | 1 / 4 / 195 |
| E - D | -0.0011 | -0.0097 | 1 / 1 / 98 | -0.0005 | -0.0044 | 1 / 1 / 198 |
| C - B | 0.0020 | 0.0181 | 1 / 0 / 99 | -0.0018 | -0.0146 | 1 / 3 / 196 |
| B - CBF | 0.0027 | 0.0249 | 3 / 0 / 97 | -0.0001 | -0.0008 | 7 / 2 / 191 |

The top-10 lists reinforce this. D and C share an identical ordered top-10 for 43 of 100 users (mean overlap 8.12 of 10), and E and D for 62 (8.50). In E, 77 users receive a prompt that differs from D’s and 38 of them change their top-10; the 23 with an identical prompt keep an identical ranking.

Candidate coverage bounds what any method can achieve. Five of the 11 labelled users have none of their future purchases among their 50 candidates, so they score 0.0000 in CBF and every LLM arm; the oracle ceiling, which places purchased candidates first, is 0.0492 over all users and 0.4469 over labelled users.

### Two failure cases (labels U145 and U148 in the pooled results)

I examined the two users with the largest drop from the CBF order to arms C, D and E; a third user, U110 (CBF 0.3172, C, D and E 0.1564), also drops and is not examined.

For U145 the single future purchase, GRS015003007, was not bought before and sits at CBF position 2, so CBF earns 0.6309. All four LLM arms return valid top-10 lists that leave position 2 out, and score 0.0000; C, D and E return the same list, with five candidates from outside the CBF top 10.

For U148 the four future purchases are assets bought before; one, GRS003003035, sits at candidate position 2 and the other three are not among the candidates. CBF returns it at rank 2 (0.2463), B places it first (0.3904), and C, D and E return the same list without it (0.0000). So for both users the profile text and the shuffled profile did not change the output, and every output was valid.

Table 3 records the generation time of each arm, excluding model loading; no model was trained.

| **Arm** | **users** | **invalid outputs** | **generation seconds** |
|:--------|----------:|--------------------:|-----------------------:|
| B       |       100 |                   0 |                 5568.4 |
| C       |       100 |                   0 |                 8367.7 |
| D       |       100 |                   0 |                11205.8 |
| E       |       100 |                   0 |                10194.0 |

Model start-up was 17.6 seconds for B and 15.4 seconds for E, reported separately; there were no invalid outputs. The generation times of C and D come from my HW2 runs. Their run_meta.json files do not record the hash of llm_rerank.py, but the script committed with them (session2 folder, commit 0085d82, 16 November 2026) has the same SHA-256 as the script used for B, D7A34C1F9F715D7437CA5B2CC7989DBFF12348602495B8A427CF8E56FA7007BA, and the repository history shows no other version. Their start-up times were not recorded.

I also place the arms against the course-provided LLM comparison. On the same 100 users the provided encoder (LLM-Rec-inspired) scored 0.0254 and 0.2306 against its TF-IDF control at 0.0235 and 0.2140, and the provided ranker (LLMRank with fallback) scored 0.0201 and 0.1827, equal to the CBF order, with 22 of 100 responses invalid; these runs used different hardware, settings and candidate pools, so I state them alongside rather than as a control. On the pooled 200 users my teammate Dastan (Abaidullah Seikh) ran the provided ranker with the same 50 candidates: 0.0306 and 0.2551, with 46 of 200 responses invalid and replaced by the CBF order. His single 200-user run (protocol hash d46b45de…) has baselines equal to my pooled baselines to four decimals, which supports pooling my two runs. I did not re-run the ranker; the values are from his report and README.

The extension sample (users 101 to 200) was declared in the protocol before any model run; 13 of its 100 users have future purchases. On it the arms score 0.0379 and 0.2916 for B, 0.0324 and 0.2494 for C, and 0.0308 and 0.2366 for both D and E (all users, labelled users). Pooling both samples gives 200 users with 24 labelled; the pooled columns of Tables 1 and 2 report them.

The pooled picture repeats the primary one: D sits below C, E below D, and there is no evidence that the profile fields help. A seeded percentile bootstrap of the pooled paired differences (10,000 resamples) gives intervals that include zero for every comparison except D-minus-C over labelled users (-0.0421 to -0.0013); I treat these as descriptive, not as a significance test.

## Discussion

### Team Discussion

I proposed a shared protocol to the team: the 100 HW2 users plus a declared extension to users 101 to 200, cutoff 2021-06-01, 30-day window, top-50 candidates. Dastan agreed and reproduced the protocol hash, and Rustam confirmed that he will use the shared 200-user sample for RQ2 and reproduced the hash. Dastan ran the provided LLM ranker on the 200 users (see Experiments), added a held-out block of users 201 to 300 for his own arms, and proposed a benchmark method that places a user’s previously bought candidates first. The team agreed that the official set stays out of all tuning and that invalid outputs fall back to the CBF order. Which benchmark method to submit is unresolved: the course rules say the official item scope and protocol are still to be fixed by the instructor, and candidates beyond the top 50 may not be allowed, so the choice is held until the official protocol is released.

### Individual Contribution

I chose to continue RQ4 and decided what to run: the 100 HW2 users as the primary sample with a declared extension to users 101 to 200, arm B to separate the summary from the ranker, and arm E as the one ablation. I ran arms C and D in HW2 and arms B and E and the extension arms in HW3, through opencode, and read the outputs.

What I verified myself: I wrote the expected SHA-256 values and protocol hashes for every file opencode created and every run, and opencode compared them and stopped on any difference; I read the outputs. I specified a raw-data check for users U031 and U030 against transactions.csv, opencode ran it, and I compared it with the script’s output (every future purchase dated 2021-06-01 to 2021-06-30, latest history rows dated 2021-05-31 and 2021-03-09). I calculated nDCG@10 for both users by hand as the sum of 1/log2(rank+1) over purchased assets in the top 10, divided by the ideal sum for the same number of purchased assets. U031 has one purchased asset (ideal 1.0000), at rank 3 in CBF, rank 2 in B, C and E, and rank 4 in D, giving 1/log2(4) = 0.5000, 1/log2(3) = 0.6309 and 1/log2(5) = 0.4307. U030 has two distinct purchased assets (GRS014003032 was bought twice and counts once), so the ideal is 1 + 1/log2(3) = 1.6309; only GRS014003032 is among the candidates, at rank 1 in CBF, B, C and D (1.0000 / 1.6309 = 0.6131) and at rank 3 in E (0.5000 / 1.6309 = 0.3066). The script gives the same values to four decimals. The automatic recomputation of every nDCG@10 is done by analyze_hw3.py and is not my own verification.

### Limitations

Only 11 of the 100 primary users and 24 of the 200 pooled users have future purchases, and each paired difference between arms rests on between two and nine users whose score changed, so I report no significance test. Nine of the 24 pooled labelled users have none of their purchases among the 50 CBF candidates, so no reranker can score on them. The model is small (1.7 billion parameters) with short output limits. The prompts of C and D differ in more than the profile values (D adds the profile block and an instruction to relate it to the purchases), so D against C does not isolate the values alone; E keeps D’s prompt and swaps the values, but for 10 of the 87 primary users with a profile the donor’s profile text equals their own, so E equals D for them by construction. All results are development results on one cutoff and two samples.

### What worked, what the failures show, what surprised me, next step

What worked: writing the protocol, hashes and expected values before the runs, so opencode’s output could be compared with what I expected (opencode’s first make_hw3.py could not reproduce the reference hash, said so itself, and was replaced by the text I specified); reporting higher/lower/equal counts next to the means; and separating candidate coverage from ranking, which showed that nine of the 24 labelled users cannot be reached by any reranker.

Root cause of the failure cases: I did not find a single cause. A check of how often each candidate position is kept in the top 10 (session3/cand2_check.md) rules out the simplest explanation: candidate 2 is kept for 134 to 137 of 200 users in C, D and E, about as often as candidates 3 to 8, so the ranker does not systematically skip position 2. The table does show a position gradient: candidate 1 is kept for 192 to 196 users, while candidate 9 is kept for only 76 to 106 users and candidate 10 for 94 to 133 across the four LLM arms. Candidates can also be near-duplicates: for one extension user, candidates 1 to 3 have identical listed attributes, so nothing in the prompt separates them. My working explanation is that this 1.7B ranker orders mainly by position and surface attributes, which would also explain why C, D and E return the same list for U145 and U148. I have not tested it; the position-permutation run in the next step is the verification, and no fix has been applied. A position bias in LLM rankers is reported in \[8\], which is consistent with this but is not evidence for it in my data.

What surprised me: how little the summary text matters. E’s prompt differs from D’s for 80 of the 100 extension users, yet E and D score identically on that sample (0.0308 and 0.2366), and on the primary sample D and C give an identical top 10 for 43 of 100 users although 98 of the 100 D summaries mention risk. Yet the arms move assets far from the CBF order. The ranker seems to lean on the candidate list and use little of the summary, so the negative result shows that this ranker does not use the profile, not that the profile is uninformative.

Next step: I would test whether the ranker uses the summary at all, with a position control: rerun arms C and D on the same users and candidates with the candidate order in the prompt randomly permuted (fixed seed) and the output mapped back. If the top-10 changes follow candidate positions and not the summary text, the small differences between C, D and E are position effects and the negative D-minus-C result says little about the profile. I would change my conclusion only if a ranker whose output visibly depends on the summary gave D above C, and E below D, by more than the bootstrap interval on a sample with more labelled users. Each arm takes about 1.5 to 3 hours on my CPU for 100 users (Table 3), which is why I have not run it.

## AI Usage Disclosure

AI tools used. opencode v2.0.27, an AI coding agent, with DeepSeek V4.1 Flash for 18 assistant messages and DeepSeek V4 Pro for 329, according to the model fields of the export (347 in total). Qwen/Qwen3-1.7B is the model under study and was not used to write anything.

How AI was used. opencode created the files from my prompts, ran all commands and the model runs as background processes, wrote analyze_hw3.py from my specification, and committed the results with explicit file lists. It first drafted the text of this report from facts that I verified and I then edited. When opencode was given only a summary instead of the text, it wrote its own version of make_hw3.py; it reported that its hash differed from the reference, and I then gave it the exact text.

What I verified is listed in Individual Contribution. What I trusted without verification: the analysis script beyond its built-in checks (the bootstrap, history-size and ranker-behaviour sections), the starter’s truth construction, the provided ranker’s internals and my teammate’s ranker run, the contents of the FAR-Trans data itself, and the model outputs beyond the ones I read.

Session log. The submitted AI-session export is opencode’s native export, made after the last opencode step (madlyn_manneh_session3.json). It records two responses interrupted by a lost connection (ECONNRESET), after each of which opencode continued, and a first attempt at arm E that failed at start-up. It contained customer identifiers that opencode printed, so the submitted file is a documented derivative in which a script replaces each identifier by CUSTOMER-ID-001 and so on and changes nothing else.

## References

\[1\] J. Sanz-Cruzado, N. Droukas, and R. McCreadie, “FAR-Trans: An Investment Dataset for Financial Asset Recommendation,” arXiv:2407.08692, 2024. \[Online\]. Available: https://arxiv.org/abs/2407.08692

\[2\] J. Zhou, Y. Dai, and T. Joachims, “Language-Based User Profiles for Recommendation,” arXiv:2402.15623, 2024. \[Online\]. Available: https://arxiv.org/abs/2402.15623

\[3\] C. Zhang et al., “EmbSum: Leveraging the Summarization Capabilities of Large Language Models for Content-Based Recommendations,” in Proc. 18th ACM Conf. Recommender Systems (RecSys ’24), 2024; arXiv:2405.11441. \[Online\]. Available: https://arxiv.org/abs/2405.11441

\[4\] F. Spadea and O. Seneviratne, “Aligning Language Models with Investor and Market Behavior for Financial Recommendations,” arXiv:2510.15993, 2025. \[Online\]. Available: https://arxiv.org/abs/2510.15993

\[5\] Y. Wang et al., “Conv-FinRe: A Conversational and Longitudinal Benchmark for Utility-Grounded Financial Recommendation,” arXiv:2602.16990, 2026. \[Online\]. Available: https://arxiv.org/abs/2602.16990

\[6\] M. Sabouri, M. Mansoury, K. Lin, and B. Mobasher, “Effectiveness of LLMs in Temporal User Profiling for Recommendation,” arXiv:2511.00176, 2025. \[Online\]. Available: https://arxiv.org/abs/2511.00176

\[7\] H. Lyu et al., “LLM-Rec: Personalized Recommendation via Prompting Large Language Models,” in Findings of the Association for Computational Linguistics: NAACL 2024, pp. 583-612, 2024, doi: 10.18653/v1/2024.findings-naacl.39. \[Online\]. Available: https://aclanthology.org/2024.findings-naacl.39/

\[8\] Y. Hou et al., “Large Language Models are Zero-Shot Rankers for Recommender Systems,” in Advances in Information Retrieval (ECIR 2024); arXiv:2305.08845. \[Online\]. Available: https://arxiv.org/abs/2305.08845
