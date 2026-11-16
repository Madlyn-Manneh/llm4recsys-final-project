# Task 3b — descriptive analysis (LOCAL ONLY: IDs and prompts)

No statistical, causal, or substantive conclusions are drawn here. All analyses use the same 100 users. Empty truth contributes zero to nDCG and to the all-user macro Recall@10 defined below. Future labels are used only for evaluation after generation, never as model input.

## Evaluation checks

- All three evaluation protocol objects exactly equal `outputs/baseline/protocol.json`.
- Full protocol hash: `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417`.
- Four baseline aggregate blocks exactly match the original saved values in every evaluation.
- A/B/C each have 100 responses, 0 invalid outputs and 0 custom failures. Per-user nDCG was cross-checked using the imported starter metric and evaluated rankings.

## a. Paired nDCG@10 differences

Better/equal/worse compares C with its comparator at full saved float precision (no rounding before comparison).

| Difference | Users | Mean difference | C better | Equal | C worse |
|---|---:|---:|---:|---:|---:|
| C−A, all | 100 | 0.00446395 | 3 | 97 | 0 |
| C−A, nonempty | 11 | 0.04058133 | 3 | 8 | 0 |
| C−B, all | 100 | 0.00198970 | 1 | 99 | 0 |
| C−B, nonempty | 11 | 0.01808818 | 1 | 10 | 0 |

## b. Hits and Recall@10

Recall@10 per user = distinct relevant ISINs in top ten / distinct eligible future Buy ISINs; empty truth is 0. Means below are macro means, not pooled micro recall. Hits are independently counted from evaluated rankings and imported starter truth.

| Arm | Nonempty users with ≥1 hit (of 11) | Total hits | Recall@10 all (100) | Recall@10 nonempty (11) |
|---|---:|---:|---:|---:|
| A | 5 | 5 | 0.03666667 | 0.33333333 |
| B | 5 | 5 | 0.03666667 | 0.33333333 |
| C | 5 | 5 | 0.03666667 | 0.33333333 |

## c. Sparse users (1–5 historical Buys)

Sparse means sum of saved eligible-history buy_count is 1–5, not 1–5 distinct assets. There are 65 sparse users: 2 with future purchases and 63 with empty truth. Individual values and identifiers are in the local-only analysis; this file contains aggregates only.

| Arm | Sparse all-user nDCG@10 (65) | Sparse nonempty nDCG@10 (2) |
|---|---:|---:|
| A | 0.00000000 | 0.00000000 |
| B | 0.00000000 | 0.00000000 |
| C | 0.00000000 | 0.00000000 |

## d. Candidate-order behaviour

Overlap is set intersection size with the CBF top ten (0–10); its fraction is overlap/10. Candidate numbers are positions in the original fixed top-50 pool. Ascending means strictly increasing returned candidate numbers, not necessarily consecutive or 1–10.

| Arm | Mean overlap count | Mean overlap fraction | Candidate 1 ranked first (of 100) | Ascending rankings (of 100) |
|---|---:|---:|---:|---:|
| A | 9.0400 | 0.9040 | 83 | 74 |
| B | 7.2400 | 0.7240 | 93 | 89 |
| C | 6.4700 | 0.6470 | 91 | 84 |

## e. Previously bought assets in recommendations

A repeated asset is a recommendation whose ISIN occurs anywhere in the full pre-cutoff Buy history, not only its capped prompt rows. This measures recommendations, not observed future repeat transactions.

| Arm | Users with ≥1 previously bought asset (of 100) | Previously bought recommendation slots (of 1000) | Mean count/user | Slot fraction |
|---|---:|---:|---:|---:|
| A | 95 | 210 | 2.1000 | 0.2100 |
| B | 95 | 200 | 2.0000 | 0.2000 |
| C | 94 | 188 | 1.8800 | 0.1880 |

## f. Candidate label coverage (evaluation only)

Using the unchanged imported `starter.load_data()` truth construction and its eligible-ID intersection, **6 of 18** future user–asset labels fall in their user’s fixed top-50 pool, across **6** users. The team reference **6/18 matches**. User IDs and covered labels are listed only in the local-only report.

The CSV source hashes were checked against the original protocol before loading truth. Exact duplicates and negative-ID initial positions, Buy-only relevance, strict cutoff/horizon, and eligible assets are handled by the starter rather than reimplemented.

## g. Summary ISIN mentions and manual-check sample

**20 of 100** C summaries mention at least one exact, case-sensitive ISIN from that user’s full history. This is a string-presence count, not a factuality judgment.

Ten summaries and their exact history texts are in local-only `results/task3_analysis.md`. Selection uses `random.Random(42).sample(protocol_users, 10)` in the saved protocol order. No summary judgments are made in this task.

## h. Tokens and latency

Prompt counts reconstruct the actual system/user chat template with the pinned local Qwen3 tokenizer, add_generation_prompt=True and enable_thinking=False, then tokenize as HFBackend.chat does. They include chat formatting. Output counts re-tokenize saved decoded/stripped text without special tokens; EOS and removed special tokens are not recoverable, so these are saved-text token counts, not exact model generation-token usage. No model or inference was loaded. Summary tokens are included only for C.

| Arm | Stage | Prompt total | Prompt mean | Prompt min/median/max | Output total | Output mean | Output min/median/max |
|---|---|---:|---:|---|---:|---:|---|
| A | rank | 194334 | 1943.34 | 1572/1892/2495 | 3480 | 34.80 | 34/34/39 |
| B | rank | 189449 | 1894.49 | 1513/1849/2492 | 3641 | 36.41 | 34/36/42 |
| C | rank | 177748 | 1777.48 | 1527/1650/2292 | 3712 | 37.12 | 34/37/42 |
| C | summary | 27992 | 279.92 | 140/203/996 | 7089 | 70.89 | 50/67/120 |

| Arm | Combined prompt tokens | Combined saved-output tokens | Whole-arm seconds | Mean seconds/user |
|---|---:|---:|---:|---:|
| A | 194334 | 3480 | 6296.8 | 62.968 |
| B | 189449 | 3641 | 6346.9 | 63.469 |
| C | 205740 | 10801 | 9604.6 | 96.046 |

Seconds/user is whole-arm recorded loop time / 100, excluding model loading and initial context/questionnaire reads; C includes summaries. Raw logs have no per-call or per-user timing, so individual latency distributions cannot be recovered. No individual timings, monetary cost, energy cost, or significance results are invented.

Sources: `outputs/arm_{A,B,C}_eval/per_user.csv`, `predictions.csv`/saved response rankings, `metrics.json`, baseline contexts/protocol, original run metadata and raw logs. Analysis helpers, per-user token tables, truth identifiers, and raw examples remain local.


## Local-only detail: sparse nonempty users

| User ID | Historical Buys | Future labels | A nDCG@10 | B nDCG@10 | C nDCG@10 |
|---|---:|---:|---:|---:|---:|
| 6B15913A38A56CB253E0 | 2 | 1 | 0.00000000 | 0.00000000 | 0.00000000 |
| 0E72D1BF99E858EEE1AA | 4 | 1 | 0.00000000 | 0.00000000 | 0.00000000 |

## Local-only detail: top-50 label coverage by user

| User ID | Future label ISINs | In top-50 ISINs |
|---|---|---|
| 870E814DB274CFA95600 | GRS014003032, GRS191213008 | GRS014003032 |
| 6BAA2D5FBCCEAB57C473 | GRS419003009 | GRS419003009 |
| 94A16DE0F59F24BB77C2 | GRS393503008 | GRS393503008 |
| 6FA5BF73C309CE8E9ED5 | GRS260333000, GRS282183003, GRS298343005, GRS395363005, GRS419003009, GRS518003009 | GRS260333000 |
| 6B15913A38A56CB253E0 | GRF000045002 | GRF000045002 |
| 29C0592F254DB2430C00 | GRS281003004 | (none) |
| 0E72D1BF99E858EEE1AA | GRS372003004 | (none) |
| D63DFAE7E53493A5ADD5 | GRS015003007 | (none) |
| 5087D23F907F90F3DDD1 | GRS003003035 | GRS003003035 |
| 8A220D47B1644E4FD349 | GRS281003004 | (none) |
| 5180B50A10AAD1C7D0F8 | GRS343313003, GRS372003004 | (none) |

## Local-only: ten summaries for the student’s manual check

Fixed seed 42; selection from protocol order, without replacement. Text is verbatim; no factuality judgment is supplied.

### Sample 1 — 5F48B46AE99C0343270D

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS426003000 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas refining & marketing, marketID: xath, sector: energy | bought 2x
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
- GRS395363005 | assetCategory: stock, assetSubCategory: large cap, industry: financial data & stock exchanges, marketID: xath, sector: financial services | bought 1x
```

**Summary**

```text
The investor primarily purchases large-cap stocks in the financial services and energy sectors, with a notable focus on banks and financial data. They also buy corporate bonds in the oil and gas sector. The purchases are relatively concentrated, with the investor buying multiple instances of certain assets, indicating a preference for specific industries. The investor shows some repetition in their purchases, particularly in the financial services and energy sectors.
```

### Sample 2 — F54AF314CC31B6E5B275

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 2x
```

**Summary**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically within the banks and regional banking industry. The purchases are concentrated in a single asset category, with 2x the quantity bought. The investor shows a tendency to repeat purchases of similar assets, indicating a consistent interest in this type of investment.
```

### Sample 3 — F92A51D29569DCB1C868

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Summary**

```text
The investor purchases large-cap stocks in the financial services sector, specifically in the banks - regional category, with a focus on market ID xath. They have made two separate purchases, indicating a relatively low level of concentration. The purchases are not repeated, as only two assets were bought.
```

### Sample 4 — 0F275A69F2B1B6FE8F04

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 6x
- GRS298343005 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas integrated, marketID: xath, sector: energy | bought 5x
- GRS372003004 | assetCategory: stock, industry: building products & equipment, marketID: xath, sector: industrials | bought 5x
- GRS393503008 | assetCategory: stock, assetSubCategory: large cap, industry: conglomerates, marketID: xath, sector: industrials | bought 5x
- GRS260333000 | assetCategory: stock, assetSubCategory: large cap, industry: telecom services, marketID: xath, sector: communication services | bought 4x
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 2x
- GRS222213001 | assetCategory: stock, industry: engineering & construction, marketID: xath, sector: industrials | bought 2x
- GRS395363005 | assetCategory: stock, assetSubCategory: large cap, industry: financial data & stock exchanges, marketID: xath, sector: financial services | bought 2x
- GRS434003000 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - renewable, marketID: xath, sector: utilities | bought 2x
- GRS518003009 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - independent power producers, marketID: xath, sector: utilities | bought 2x
- GRS191213008 | assetCategory: stock, assetSubCategory: large cap, industry: engineering & construction, marketID: xath, sector: industrials | bought 1x
- GRS204003008 | assetCategory: stock, assetSubCategory: large cap, industry: household & personal products, marketID: xath, sector: consumer defensive | bought 1x
- GRS239003007 | assetCategory: stock, industry: textile manufacturing, marketID: xath, sector: consumer cyclical | bought 1x
- GRS281003004 | assetCategory: stock, industry: metal fabrication, marketID: xath, sector: industrials | bought 1x
- GRS426003000 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas refining & marketing, marketID: xath, sector: energy | bought 1x
```

**Summary**

```text
The investor primarily purchases large-cap stocks across various industries, including energy, financial services, industrials, and utilities. The purchases are concentrated in the energy sector, with several entries related to oil & gas refining & marketing, and financial services. The investor buys assets in the same market (xath) and shows a pattern of buying multiple times, with some assets purchased multiple times (e.g., 6x for GRS003003035, 5x for several others). The overall purchase pattern indicates a focus on diversified large-cap stocks in industrial and energy sectors.
```

### Sample 5 — EF36A0A4BF8B80601DA2

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS343313003 | assetCategory: stock, industry: gambling, marketID: xath, sector: consumer cyclical | bought 5x
- GRS346003007 | assetCategory: stock, industry: packaging & containers, marketID: xath, sector: consumer cyclical | bought 2x
- GRS395363005 | assetCategory: stock, assetSubCategory: large cap, industry: financial data & stock exchanges, marketID: xath, sector: financial services | bought 1x
```

**Summary**

```text
The investor primarily purchases stocks in the consumer cyclical and financial services sectors, with a focus on large-cap stocks in the financial data and stock exchanges industry. They have made multiple purchases of the same asset, with the largest single purchase being 5x of a stock in the gambling sector. The purchases are concentrated in a limited number of assets, indicating a relatively focused investment strategy.
```

### Sample 6 — 508B4F986C71CD2B8136

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS014003032 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Summary**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically within the banks and regional banking industry. The purchase is concentrated in a single asset, indicating a high level of concentration in one asset. The investor does not show any repeated purchases, as only one transaction is recorded.
```

### Sample 7 — F3B6B4C7E1F815C1FFE6

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRF000031002 | assetCategory: mtf, assetSubCategory: balanced, marketID: aedak | bought 2x
- GRF000032000 | assetCategory: mtf, assetSubCategory: balanced, marketID: aedak | bought 2x
- GRF000036001 | assetCategory: mtf, assetSubCategory: balanced, marketID: aedak | bought 2x
- GRF000045002 | assetCategory: mtf, assetSubCategory: money market, marketID: aedak | bought 2x
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
- GRF000023009 | assetCategory: mtf, assetSubCategory: bond, marketID: aedak | bought 1x
```

**Summary**

```text
The investor primarily purchases assets in the mtf (mutual fund or trust fund) category, including balanced funds and money market funds, with a focus on the aedak market. They have made multiple purchases of these assets, with some assets bought twice, indicating a level of concentration in specific funds. Additionally, the investor has made a single purchase of a corporate bond in the oil and gas sector, suggesting some diversification into different industries.
```

### Sample 8 — 0BFFD9C891A98BAD971B

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
- GRC5211214B5 | assetCategory: bond, assetSubCategory: corporate, industry: other financial institutions, marketID: xath, sector: corporate | bought 1x
```

**Summary**

```text
The investor purchases bonds from the oil and gas extraction and refining sector and other financial institutions, with both transactions occurring in the market ID "xath." The purchases are concentrated in the corporate sector and are made from a single market, indicating a relatively focused investment strategy. The investor has made two separate purchases, each of 1x, suggesting a pattern of repeated buying of similar assets.
```

### Sample 9 — 421B8C42D925AE7D3498

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 2x
- GRS298343005 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas integrated, marketID: xath, sector: energy | bought 1x
- GRS426003000 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas refining & marketing, marketID: xath, sector: energy | bought 1x
```

**Summary**

```text
The investor primarily purchases large-cap stocks in the energy sector, specifically in the oil & gas integrated and oil & gas refining & marketing categories. They have made two purchases of the same asset, GRS003003035, and one purchase of another asset, GRS298343005. The purchases are concentrated in the energy sector and are not diversified across different assets.
```

### Sample 10 — 06AE8AC72FD5B2D0FC6D

**History**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS110116001 | assetCategory: stock, marketID: xath | bought 2x
```

**Summary**

```text
This investor buys two shares of GRS110116001, a stock, in the market identified as xath. The purchase is concentrated in a single asset and market, indicating a high level of concentration. The investor does not appear to repeat purchases of the same asset or market.
```
