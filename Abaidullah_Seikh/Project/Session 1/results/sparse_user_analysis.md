# Sparse-user analysis

Student: Abaidullah Seikh  
Course: LLM4Rec, HSE University  
Scope: Homework 1, Session 1, Task 1 inspection notes only.

**AI-assisted inspection by OpenCode (openai/gpt-6-astra). Personal verification by the student is pending.** These files are not the final homework report.

## Counting definitions

Full-release exploratory counts, **not pre-cutoff eligibility counts**. Each raw transaction row counts once, including repeated purchases of the same asset; these are event counts, not distinct-item counts. `total[u]`, `buy[u]`, and `sell[u]` are computed for every customer in transactions.csv by the script's Counters. Zero-Buy users are retained in the all-transaction-customer distribution.

| Population | Users |
| --- | --- |
| Any transaction | 29,090 |
| At least one Buy | 29,090 |
| No Buy among transaction customers | 0 |
| Profile customers with no transaction | 0 |

## Distribution

| Population/count | Min | P10 | P25 | Median/P50 | P75 | P90 | P95 | P99 | Max | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All transactions per transaction customer | 1.00 | 1.00 | 2.00 | 3.00 | 7.00 | 21.00 | 46.00 | 194.00 | 6,288.00 | 13.34 |
| Buy events per transaction customer (zeros included) | 1.00 | 1.00 | 1.00 | 2.00 | 4.00 | 13.00 | 28.00 | 114.11 | 4,047.00 | 7.87 |
| Buy events per buyer (positive only) | 1.00 | 1.00 | 1.00 | 2.00 | 4.00 | 13.00 | 28.00 | 114.11 | 4,047.00 | 7.87 |
| Sell events per transaction customer (zeros included) | 0.00 | 0.00 | 1.00 | 1.00 | 3.00 | 8.10 | 18.00 | 83.11 | 2,241.00 | 5.47 |

## Requested overlapping full-dataset Buy bands

| Buy events (inclusive) | Users | % of all transaction customers | % of buyers |
| --- | --- | --- | --- |
| 1–3 | 21,237 | 73.00% | 73.00% |
| 1–5 | 23,663 | 81.34% | 81.34% |
| 1–10 | 25,736 | 88.47% | 88.47% |

## Non-overlapping Buy histogram

| Buy events | Users |
| --- | --- |
| 0 | 0 |
| 1 | 13,906 |
| 2–3 | 7,331 |
| 4–5 | 2,426 |
| 6–10 | 2,073 |
| 11–20 | 1,393 |
| 21–50 | 1,167 |
| 51–100 | 443 |
| >100 | 351 |

## Provisional definition, not official

Propose **1–5 Buy events strictly before the prediction cutoff** as an initial *purchase-sparse* subgroup: the full-release median is 2 Buy events, P75 is 4, and the 1–5 band covers 23,663 customers (81.34% of transaction customers). It provides a small, nonempty purchase history while leaving 1–3 and 1–10 as sensitivity bands. This is an exploratory threshold recommendation, not a discovered optimum or instructor rule.

Because the RQ says transaction-history summaries, low Buy counts do not necessarily mean little total history: users can have many Sells. If summaries include both types, report total pre-cutoff events as well and consider a separately declared 1–5 total-event subgroup. Zero-Buy/zero-history users should be described separately rather than silently mixed into the proposed subgroup.

Observed example of this distinction: **360** customers with 1–5 full-release Buys have more than 10 total full-release transactions.

## Why these are not the official sparse-user population

Full-release counts include transactions after any earlier prediction cutoff. Using those counts to select sparse users would condition selection on future activity. A customer with many full-release purchases may have only a few at the cutoff, while a full-release buyer may have zero purchases at that time. Item restrictions, history-window length, label definitions and evaluated-user eligibility remain pending (§2 of the supplied instructions). Future-purchase availability must be handled by that protocol, not silently assumed here.

Once announced: select permitted historical transactions using the official boundary and item scope, recompute counts, freeze subgroup membership from past data only, then apply the shared evaluation eligibility. The proposed strict `< cutoff` convention must be reconciled with the official day-boundary rule. Dates have no intraday ordering. Both comparison arms must receive the same permitted history, metadata, candidates and ranker. No nDCG or model result is claimed.
