# Profile-augmented LLM transaction summaries for sparse-history financial asset recommendation: a development study

**Name:** Madlyn Manneh
**Team:** Eight(8)
**Repository:** https://github.com/Madlyn-Manneh/llm4recsys-final-project
**Protocol commit:** 479dde0ad88c5a9809f490d31a968e483ae3c059
**Primary-results commit:** 3d4ca46f07d6d01d1500d489d4c63e24af082139
**Final experiment commit:** 0e27423802474e8e4320400cd90feb7c42b2299c

## Abstract

Financial asset recommendation for retail investors with sparse transaction histories is difficult because a behaviour-only representation carries little signal. This report tests whether appending two structured profile fields, risk level and investment capacity, to an LLM-written summary of a customer's transaction history changes ranking accuracy on FAR-Trans, compared with a summary of the history alone. The pipeline uses the LLM in two stages: a summary step (encoder-like) followed by a reranking step that orders the starter's fixed top-50 content-based candidates. On the deterministic 100-user development sample with a 2021-06-01 cutoff and a 30-day evaluation window, the profile-augmented arm (D) scored a mean nDCG@10 of 0.0220 over all users and 0.1996 over the 11 users with future purchases, slightly below the history-only arm (C) at 0.0248 and 0.2257. The shuffled-profile ablation (E) scored 0.0209 and 0.1899. These are development results; I find no evidence that adding the profile fields improves ranking, and I do not report a significance test because only 11 primary users, and 24 pooled users, have future purchases. Pooling the two 100-user samples leaves D below C and E below D, matching the primary result.

## Introduction

Retail investors in FAR-Trans are heavily long-tailed. The dataset paper reports that over half of the 29,090 customers have three or fewer transactions across the 2018 to 2022 period. For these sparse-history customers a transaction-only representation is thin, and an LLM summary of that history can collapse into generic phrasing. The open question I address is whether adding two structured fields that the bank already records, the customer's risk level and investment capacity, to that summary gives the downstream ranker additional, non-leaking signal that improves the common top-10 output.

My research question (RQ4) is therefore whether a profile-augmented summary changes nDCG@10 compared with a history-only summary, for FAR-Trans users with sparse purchase histories. The candidate set, asset information, ranker template, and evaluation metric are held constant. Arm D differs from arm C in the summary prompt, which adds the profile block and an instruction to relate the profile to the purchases. The outcome is the mean nDCG@10 against the assets the user actually buys in the following 30 days. This is a narrow representation question with a falsifiable answer: either the two profile fields change ranking, or they do not. A null or negative answer is still informative about whether a longer, profile-dependent prompt is worth its cost for this subgroup.

I make three contributions. First, I implement a two-stage LLM pipeline in which a summary step feeds a reranking step, and I separate the two contributions with a raw-history arm and the content-based control. Second, I run a seeded cyclic profile-shuffle ablation that replaces each user's profile with another user's profile while keeping everything else fixed, which tests whether the profile content itself rather than the presence of a profile block drives any change. Third, I record a hand-worked nDCG@10 example for one user and an environment and runtime trace that distinguishes generation time from model start-up.

## Related Work

FAR-Trans is the shared financial asset recommendation dataset and benchmark used here, with 29,090 customers, 806 assets, and transactions from 2018 to 2022. Its paper benchmarks classical price-based, transaction-based, and hybrid recommenders with top-10 nDCG@10, but it provides no LLM summary representation, so my question operates inside its evaluation frame rather than against an existing LLM result.

The closest methodological neighbours are LLM-based user profiling and recommendation systems. LFM turns a user's rating history into a compact, human-readable profile and predicts from that summary, and it argues for interpretability and shorter input length. EmbSum shows that offline LLM-generated summaries of long engagement histories can help a content-based ranker. FLARKO uses LLMs with knowledge graphs encoding transaction histories and asset trends for financial recommendation, and it reports behavioural alignment and profitability on FAR-Trans, though it uses structured graphs rather than a free-text summary. Conv-FinRe contributes a conversational, longitudinal benchmark for utility-grounded financial recommendation. Sabouri et al. study temporal LLM user profiling on Movies&TV and Video Games and report smaller benefits in sparser environments, which is directly relevant to my sparse-history focus. [[REF: LLM-Rec]] and [[REF: LLMRank]] are the two prompting approaches that the course's provided encoder and ranker baselines adapt.

None of these studies tests whether adding risk level and investment capacity to an LLM transaction-history summary changes nDCG@10 on sparse FAR-Trans users, which is the specific comparison I run.

## Method

The pipeline treats the LLM as both an encoder and a ranker. The summary step turns the customer's pre-cutoff Buy history into a short natural-language description of the kinds of assets and markets the customer buys, how concentrated the purchases are, and whether purchases repeat. The ranker step then orders the starter's fixed top-50 content-based candidates using that summary as the investor information block. The ranker never sees the profile fields directly in the history-only arm; in the profile arm it reaches the ranker only through the summary.

Five arms are compared, all sharing the same candidate set, asset information, ranker template, and top-10 output. The four provided baselines are Popularity, CBF, Latest buy, and Latest buy or sell. Arm B passes the raw history text, one line per asset, to the same ranker without any LLM summary, which isolates the summary step against the content-based control. Arm C is the LLM summary of the history only. Arm D is the summary plus risk level and investment capacity, flagged as observed or estimated, and this is the primary comparison against C. Arm E is the one ablation: it is D, but each user whose profile is available at the cutoff receives another user's profile under a deterministic, seeded cyclic permutation in which no user keeps their own profile, and users with no available profile keep the not-available text.

The model is Qwen/Qwen3-1.7B at revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e, with thinking disabled, greedy decoding, seed 0, at most 120 summary tokens and 60 ranking tokens, in float32 on CPU. The environment is Python 3.12.10, torch 2.11.0+cpu, and transformers 4.57.6 on an AMD Ryzen 5 7430U with 6 cores, 12 logical processors, 15.4 GB of RAM, and Windows 11.

The development sample is the deterministic 100-user HW2 sample: warm users with a pre-cutoff history, ordered by the SHA-256 of a salted customer identifier, taking the first 100. The cutoff is 2021-06-01, the label window is the following 30 days, repeat purchases are allowed, and each user has 50 content-based candidates. Users with no future purchases count as zero in the primary mean. All methods share the same users, cutoff, eligible assets, labels, and evaluation rules, and the same protocol hash is recorded across runs. These are development results, not official benchmark scores. Every nDCG@10 value is recomputed from the saved rankings and checked against the saved per-user files.

Deviations and reproducibility. The protocol was committed before any HW3 model run (commit 479dde0ad88c5a9809f490d31a968e483ae3c059). The extension sample (users 101 to 200) was run as a separate users-file run with its own protocol hash, 5bae3e69d666acbc9f80421ffd4a5b6733d197d10a0894822ecd6674cfb413f5, and the shuffle of arm E was done inside each run. The first attempt of arm E failed at start-up with a network name-resolution error before any output was written and is not part of the results; the rerun used HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1, as did the extension runs. Per-user result files contain customer identifiers and are not committed, because of the course data rule. The committed copies of the result files have LF line endings, while the local copies have CRLF, so the two forms have different SHA-256 values; the report cites the committed (LF) form.

## Experiments

Table 1 reports the primary metric for the four baselines and the four LLM arms on the 100-user development sample. The primary mean is over all 100 users, with empty truth counted as zero; the second column is the mean over the 11 users with future purchases.

| Method | nDCG@10 (all users) | nDCG@10 (11 labelled) |
|---|---:|---:|
| Popularity | 0.0286 | 0.2599 |
| Latest buy | 0.0277 | 0.2520 |
| Latest buy or sell | 0.0271 | 0.2464 |
| CBF (initial candidate order, matched control) | 0.0201 | 0.1827 |
| B (raw history, no summary) | 0.0228 | 0.2076 |
| C (summary only) | 0.0248 | 0.2257 |
| D (summary + risk level and capacity) | 0.0220 | 0.1996 |
| E (D with shuffled profiles) | 0.0209 | 0.1899 |

The profile arm D is below the history-only arm C by 0.0029 over all users and by 0.0262 over the 11 labelled users. The shuffled-profile arm E is below D by 0.0011 overall and 0.0097 over labelled users. Table 2 gives the paired differences and the counts of users who score higher, lower, or equal.

| Pair | all users | labelled | higher / lower / equal |
|---|---:|---:|---:|
| D - C | -0.0029 | -0.0262 | 1 / 2 / 97 |
| E - D | -0.0011 | -0.0097 | 1 / 1 / 98 |
| C - B | 0.0020 | 0.0181 | 1 / 0 / 99 |
| B - CBF | 0.0027 | 0.0249 | 3 / 0 / 97 |

These differences rest on very few users: the D-minus-C drop of 0.0262 is driven by two labelled users, and one labelled user moves the other way. I report no significance test because only 11 users have future purchases. My reading is that there is no evidence that the profile fields help, and that the development difference is small and negative.

The top-10 lists reinforce this. D and C share an identical ordered top-10 for 43 of 100 users with a mean overlap of 8.12 of 10 assets. E and D share 62 identical lists with a mean overlap of 8.50. In D, 98 of the 100 summaries mention the word risk and 97 mention capacity, against none of C's, so the profile text reaches the summary in almost every case. Of the 100 users, 87 have a profile available at the cutoff and 13 do not; D differs from C in the top-10 for 48 of the 87 with a profile and for 9 of the 13 without. In the E ablation, 77 users receive a prompt that differs from D, 0 keep their own profile, and 23 have an identical prompt; of the 77 whose prompt differs, 38 change their top-10 relative to D, while all 23 with an identical prompt keep an identical ranking.

Candidate coverage bounds what any of these methods can achieve. Five of the 11 labelled users have none of their future purchases among their 50 candidates, and the oracle ceiling, which places purchased candidates first, is 0.0492 over all users and 0.4469 over labelled users. A reranker cannot recover a purchase that is not among the 50 candidates, so those five users score 0.0000 in CBF and in every LLM arm. For the other six labelled users the oracle ceiling shows how much the ordering of the candidates could matter.

### Two failure cases (labels U145 and U148 in the pooled results)

I examined the two users with the largest drop in nDCG@10 from the CBF order to arms C, D, and E. A third user, U110, also scores below CBF in every LLM arm (CBF 0.3172, B 0.2021, C, D, and E 0.1564) and is not examined here.

For U145 the single future purchase is GRS015003007, which the user had not bought before and which sits at position 2 among the 50 CBF candidates. The CBF baseline returns it at rank 2 and earns nDCG@10 of 0.6309. Arms B, C, D, and E all produce valid top-10 lists that leave position 2 out. Arm B returns candidate numbers 1, 3, 6, 8, 14, 15, 16, 17, 18, and 19. Arms C, D, and E each return 1, 3, 4, 5, 8, 13, 19, 20, 23, and 24, which includes five candidates from outside the CBF top 10. All four arms score nDCG@10 of 0.0000 for this user.

For U148 the four future purchases are assets the user had bought before. One of them, GRS003003035, sits among the 50 candidates at position 2, and the other three are not among the candidates. The CBF baseline returns GRS003003035 at rank 2 and earns nDCG@10 of 0.2463. Arm B returns 2, 12, 1, 3, 4, 5, 6, 7, 8, and 10, which places it first, and scores 0.3904. Arms C, D, and E each return 1, 3, 4, 5, 6, 7, 8, 9, 10, and 11, leave position 2 out, and score 0.0000.

Arms C, D, and E return identical top-10 lists for both users, so the profile text and the shuffled profile did not change the output in these two cases. Every output was valid.

Table 3 records the generation loop time for each arm, which excludes model loading and data preparation; no model training was performed.

| Arm | users | invalid outputs | generation seconds |
|---|---:|---:|---:|
| B | 100 | 0 | 5568.4 |
| C | 100 | 0 | 8367.7 |
| D | 100 | 0 | 11205.8 |
| E | 100 | 0 | 10194.0 |

Model start-up was 17.6 seconds for B and 15.4 seconds for E, reported separately from generation. There were no invalid outputs.

I also place the arms against the course-provided LLM comparison on the same 100 users. The provided encoder (LLM-Rec-inspired) scored 0.0254 over all users and 0.2306 over labelled users against its original-text TF-IDF control at 0.0235 and 0.2140, while the provided ranker (LLMRank with fallback) scored 0.0201 and 0.1827, equal to the initial candidate order, with 22 of 100 responses invalid and falling back. These provided runs used different hardware, settings, and candidate pools, so I state them alongside rather than as a strict control.

On the pooled 200 users, my teammate Dastan ran the provided LLMRank ranker with the same 50 candidates on a CPU: 0.0306 over all users and 0.2551 over the 24 labelled users. His metrics file confirms these two values and reproduces my pooled CBF and baseline values to four decimals; the count of 46 of 200 invalid outputs (replaced by the CBF order) and his settings are from his message to the team, and I did not re-run the ranker [[CHECK: his settings manifest]].

For the labelled user U031, the nDCG@10 values follow directly from the rank of the single purchased asset; my own calculation is in the Individual Contribution section. That user has one future purchase, GRS419003009, which sits at candidate position 3. CBF ranks it third with a term of 0.5000, B and C rank it second with 0.6309, D ranks it fourth with 0.4307, and E ranks it second with 0.6309, and the ideal DCG is a single term of 1.0000, so each nDCG@10 equals the DCG term divided by one.

An extension of 100 further users (users 101 to 200) is declared in the protocol and its baselines are already computed: on that sample, 13 of 100 users have future purchases, and the baselines score 0.0408 and 0.3141 for CBF, 0.0670 and 0.5153 for Latest buy, 0.0697 and 0.5361 for Latest buy or sell, and 0.0399 and 0.3066 for Popularity. The four extension LLM arms were then run in offline mode as a single background chain. On the extension sample the arms score 0.0379 over all users and 0.2916 over the 13 labelled users for B, 0.0324 and 0.2494 for C, and 0.0308 and 0.2366 for both D and E, so D is below C by 0.0017 overall and 0.0128 over labelled users while E equals D.

Pooling the primary and extension samples gives 200 users with 24 labelled users. Table 4 reports the pooled nDCG@10 and Table 5 the pooled paired differences.

| Method | nDCG@10 (all users) | nDCG@10 (24 labelled) |
|---|---:|---:|
| Popularity | 0.0342 | 0.2852 |
| Latest buy | 0.0474 | 0.3946 |
| Latest buy or sell | 0.0484 | 0.4033 |
| CBF (initial candidate order, matched control) | 0.0305 | 0.2539 |
| B (raw history, no summary) | 0.0304 | 0.2531 |
| C (summary only) | 0.0286 | 0.2385 |
| D (summary + risk level and capacity) | 0.0264 | 0.2196 |
| E (D with shuffled profiles) | 0.0258 | 0.2152 |

| Pair | all users | labelled | higher / lower / equal |
|---|---:|---:|---:|
| D - C | -0.0023 | -0.0189 | 1 / 4 / 195 |
| E - D | -0.0005 | -0.0044 | 1 / 1 / 198 |
| C - B | -0.0018 | -0.0146 | 1 / 3 / 196 |
| B - CBF | -0.0001 | -0.0008 | 7 / 2 / 191 |

The pooled picture repeats the primary one. D sits below C and E sits below D, every difference rests on a small number of labelled users, and there is no evidence that the profile fields help. Three descriptive diagnostics complete the picture. The LLM arms depart widely from the CBF order: the ten listed assets sit at a mean candidate position of 5.50 for CBF and between 8.47 and 9.82 for the four arms, and between 106 and 147 of the 200 users have at least one asset from candidate positions 11 to 50 in their top 10. By history size, the pooled sample splits into 160 users with 1 to 5 history assets and 40 users with 6 or more, and the arms stay below the recency baselines in both groups. A seeded percentile bootstrap of the pooled paired differences with 10,000 resamples gives intervals that include zero for every comparison except D-minus-C over labelled users (-0.0421 to -0.0013); the D-minus-C interval over all users has an upper bound of 0.0000; these are descriptive intervals and I do not treat them as a significance test. The extension run took 8682.8, 9993.8, 9939.8, and 4985.8 generation seconds for C, D, E, and B, with no invalid outputs.

## Discussion

### Team Discussion

I proposed a shared protocol to the team: the 100 HW2 users plus a declared extension to users 101 to 200, cutoff 2021-06-01, 30-day window, top-50 candidates. Dastan agreed and reproduced the protocol hash, and Rustam confirmed that he will use the shared 200-user sample for RQ2 and reproduced the protocol hash. Dastan ran the provided LLM ranker on the 200 users (see Experiments), added a further held-out block of users 201 to 300 for his own arms, and proposed a benchmark method that places a user's previously bought candidates first. The team has not yet decided which method to submit, and the course rules say the official item scope and protocol are still to be fixed by the instructor [[FILL: what the team decided on the benchmark method, which version of arm A is adopted, and what remains unresolved]].

### Individual Contribution

I chose to continue RQ4 and decided what to run: the 100 HW2 users as the primary sample with a declared extension to users 101 to 200, arm B to separate the summary from the ranker, and arm E as the one ablation. I ran arms C and D in HW2, and arms B and E and the extension arms in HW3, through opencode, and I read the outputs.

What I verified myself: I wrote the expected SHA-256 values and the expected protocol hashes for every file opencode created and every run, and opencode compared them and stopped on any difference; I read the outputs. I specified the raw-data check for users U031 and U030 against transactions.csv, opencode ran it, and I compared it with the script's output (every future purchase dated from 2021-06-01 to 2021-06-30, latest history rows dated 2021-05-31 and 2021-03-09). I calculated nDCG@10 for U031 and U030 by hand [[FILL: my numbers, and whether they match the script to four decimals]]. The recomputation of every nDCG@10 and the other automatic checks are done by analyze_hw3.py and are not my own verification.

### Limitations

Only 11 of the 100 primary users and 24 of the 200 pooled users have future purchases, and each paired difference between arms rests on between two and nine users whose score changed, so I report no significance test; the bootstrap intervals are descriptive. Nine of the 24 pooled labelled users have none of their purchases among the 50 CBF candidates, so no reranker can score on them. The model has 1.7 billion parameters and ran on CPU with output limits of 120 and 60 tokens. The prompts of C and D differ in more than the profile values: D adds the profile block and an instruction to relate the profile to the purchases, so D against C does not isolate the profile values alone. Arm E keeps D's prompt and swaps the profile values, which separates the values from the extra text only partly, because for 10 of the 87 primary users with a profile the donor's profile text equals their own, so E equals D for them by construction. All results are development results on one cutoff and two samples.

## AI Usage Disclosure

I used opencode, an AI coding agent, as my AI tool [[FILL: opencode version]].

opencode (DeepSeek V4.1 Flash for the first 18 assistant messages and DeepSeek V4 Pro for the remaining ones, according to the model fields of the export [[FILL: update the message counts from the final export]]) created the files from my prompts, ran all commands, ran the models as background processes, wrote analyze_hw3.py from the specification, and committed the results with explicit file lists. Two incidents are visible in the export: when opencode was given only a summary instead of the text, it wrote its own version of make_hw3.py and the hash check caught it; and its first version of the bootstrap code used a different seed and sampling method than specified, which the line-by-line check of expected values caught.

Qwen/Qwen3-1.7B is the model under study and was not used to write anything. The text of this report was drafted by opencode from facts that I verified, and I edited it [[FILL: confirm or change]]. The AI-session export is opencode's native export, made after the last opencode step [[FILL: file name]]. It contained customer identifiers that opencode printed while working, so the submitted file is a documented derivative in which a script replaces each identifier by CUSTOMER-ID-001 and so on and changes nothing else [[FILL: SHA-256 of the original export and of the derivative]] [[FILL: the instructor confirmed that a documented derivative is accepted]].

## References

Sanz-Cruzado, Droukas, and McCreadie. FAR-Trans: An Investment Dataset for Financial Asset Recommendation, 2024. https://arxiv.org/abs/2407.08692

Spadea and Seneviratne. Aligning Language Models with Investor and Market Behavior for Financial Recommendations, 2025. https://arxiv.org/abs/2510.15993

Zhou, Dai, and Joachims. LFM (LLM-IGS), 2024.

Zhang et al. EmbSum, 2024.

Wang et al. Conv-FinRe, 2026. https://arxiv.org/abs/2602.16990

Sabouri et al. Effectiveness of LLMs in Temporal User Profiling for Recommendation, 2025. https://arxiv.org/abs/2511.00176

[[REF: LLM-Rec (Lyu et al., Findings of NAACL 2024)]]

[[REF: LLMRank (Hou et al., ECIR 2024)]]
