# Differing users across arms A, B, C — LOCAL ONLY

**Contains raw customer IDs and history/summary text. Never commit this report.**

Descriptive listing only. No model was loaded or run. Source scores and rankings are method `custom` from `outputs/arm_A_eval`, `outputs/arm_B_eval`, and `outputs/arm_C_eval` (`per_user.csv`, `predictions.csv`). Truth was reconstructed by importing the unchanged `starter.load_data()` and intersecting its truth sets with each user’s eligible IDs, exactly as in starter evaluation. Source CSV hashes and all evaluation protocols were checked against the original baseline. All 100 user scores were cross-checked with imported `starter.ndcg10()`.

Full protocol hash: `50efd4aeb415ba6f0c66dd0793a7c2033cdc32a42b86b58eebbca3e81eaf3417`.

**3 of 100 users** have different saved nDCG@10 between at least two arms. Users are listed in protocol order. Differences are computed before rounding. Hit positions are one-based; only relevant recommended ISINs are listed. True ISINs are distinct eligible future Buy labels, not transaction rows.

## Complete list and per-user differences

| User ID | True ISIN count | A nDCG@10 | B nDCG@10 | C nDCG@10 | C−A (unrounded calculation, shown to 12 decimals) | C−B (shown to 12 decimals) |
|---|---:|---:|---:|---:|---:|---:|
| 6BAA2D5FBCCEAB57C473 | 1 | 0.5000 | 0.6309 | 0.6309 | 0.130929753571 | 0.000000000000 |
| 94A16DE0F59F24BB77C2 | 1 | 0.5000 | 0.6309 | 0.6309 | 0.130929753571 | 0.000000000000 |
| 5087D23F907F90F3DDD1 | 1 | 0.3155 | 0.3010 | 0.5000 | 0.184535123214 | 0.198970004336 |

## Sum-to-mean verification

Users not listed have identical A/B/C scores, so they contribute zero to both paired sums. Each all-user mean is the sum of the full-precision per-user differences divided by 100, not the sum of rounded displayed nDCG scores.

| Comparison | Sum over listed users | Sum over all 100 users | Sum / 100 | Rounded to 8 decimals | Task 3b reported mean | Match |
|---|---:|---:|---:|---:|---:|---|
| C−A | 0.446394630357186 | 0.446394630357186 | 0.004463946303572 | 0.00446395 | 0.00446395 | yes |
| C−B | 0.198970004336019 | 0.198970004336019 | 0.001989700043360 | 0.00198970 | 0.00198970 | yes |

## Per-user hits, Arm B history and Arm C summary

History is copied verbatim from the history portion of Arm C’s saved `summary_prompt`. It was checked to equal the Investor information block in the same user’s actual Arm B `rank_prompt`. Summaries are copied verbatim from Arm C `raw_log.jsonl`. No assessment of what was retained, omitted or inferred is supplied.

### User `6BAA2D5FBCCEAB57C473`

**Number of true ISINs:** 1

**True ISINs:** `GRS419003009`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS419003009` at position 3 | 0.5000 |
| B | `GRS419003009` at position 2 | 0.6309 |
| C | `GRS419003009` at position 2 | 0.6309 |

**C−A:** 0.130929753571. **C−B:** 0.000000000000.

**Arm B history text (also the history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 8x
- GRS419003009 | assetCategory: stock, assetSubCategory: large cap, industry: gambling, marketID: xath, sector: consumer cyclical | bought 5x
- GRS014003032 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS343313003 | assetCategory: stock, industry: gambling, marketID: xath, sector: consumer cyclical | bought 1x
- GRS393503008 | assetCategory: stock, assetSubCategory: large cap, industry: conglomerates, marketID: xath, sector: industrials | bought 1x
- GRS518003009 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - independent power producers, marketID: xath, sector: utilities | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks across various industries, including gambling, banks - regional, conglomerates, and utilities. They buy these assets in relatively concentrated quantities, with the highest number of purchases (8x) for a single asset and the rest spread across multiple assets. The investor shows a tendency to repeat purchases of certain assets, particularly those in the consumer cyclical and financial services sectors.
```

### User `94A16DE0F59F24BB77C2`

**Number of true ISINs:** 1

**True ISINs:** `GRS393503008`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS393503008` at position 3 | 0.5000 |
| B | `GRS393503008` at position 2 | 0.6309 |
| C | `GRS393503008` at position 2 | 0.6309 |

**C−A:** 0.130929753571. **C−B:** 0.000000000000.

**Arm B history text (also the history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS393503008 | assetCategory: stock, assetSubCategory: large cap, industry: conglomerates, marketID: xath, sector: industrials | bought 6x
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 4x
- GRS239003007 | assetCategory: stock, industry: textile manufacturing, marketID: xath, sector: consumer cyclical | bought 4x
- GRS337003008 | assetCategory: stock, industry: rental & leasing services, marketID: xath, sector: industrials | bought 4x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS434003000 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - renewable, marketID: xath, sector: utilities | bought 3x
- GRS298343005 | assetCategory: stock, assetSubCategory: large cap, industry: oil & gas integrated, marketID: xath, sector: energy | bought 2x
- GRS395363005 | assetCategory: stock, assetSubCategory: large cap, industry: financial data & stock exchanges, marketID: xath, sector: financial services | bought 2x
- GRS518003009 | assetCategory: stock, assetSubCategory: large cap, industry: utilities - independent power producers, marketID: xath, sector: utilities | bought 2x
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS096003009 | assetCategory: stock, assetSubCategory: large cap, industry: specialty retail, marketID: xath, sector: consumer cyclical | bought 1x
- GRS260333000 | assetCategory: stock, assetSubCategory: large cap, industry: telecom services, marketID: xath, sector: communication services | bought 1x
- GRS419003009 | assetCategory: stock, assetSubCategory: large cap, industry: gambling, marketID: xath, sector: consumer cyclical | bought 1x
- GRS495003006 | assetCategory: stock, assetSubCategory: large cap, industry: airlines, marketID: xath, sector: industrials | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks across various industries, including industrials, financial services, energy, utilities, and consumer cyclical sectors. The purchases are concentrated in the xath market, with the majority of transactions (6x, 4x, 3x, 2x) focused on stocks in the financial services, energy, and industrials sectors. The investor shows a pattern of repeated purchases, particularly in the financial services and industrials sectors, with some assets being bought multiple times.
```

### User `5087D23F907F90F3DDD1`

**Number of true ISINs:** 1

**True ISINs:** `GRS003003035`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS003003035` at position 8 | 0.3155 |
| B | `GRS003003035` at position 9 | 0.3010 |
| C | `GRS003003035` at position 3 | 0.5000 |

**C−A:** 0.184535123214. **C−B:** 0.198970004336.

**Arm B history text (also the history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS314003005 | assetCategory: stock, industry: packaged foods, marketID: xath, sector: consumer defensive | bought 11x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 7x
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 3x
- GRS372003004 | assetCategory: stock, industry: building products & equipment, marketID: xath, sector: industrials | bought 2x
- GRS014003032 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases stocks in the consumer defensive, financial services, and industrials sectors, with a focus on large-cap stocks. They have made concentrated purchases, with the largest single transaction being 11x in a packaged foods stock, followed by 7x in banks-regional stocks and 3x in large-cap stocks across multiple industries. The investor shows a tendency to repeat purchases in certain asset categories, particularly in financial services and industrials.
```
