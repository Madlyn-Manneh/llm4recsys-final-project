# Supplementary sparse cohort: differing users — LOCAL ONLY

**Contains raw customer IDs, histories and model summaries. Never commit. Not the HW2 default protocol.**

Descriptive listing only; no judgments about the summaries or ranking results. Sources are custom per_user.csv and predictions.csv from the three supplementary evaluation directories, plus the saved B/C raw logs. Truth is from imported unchanged starter.load_data(), intersected with eligible IDs. All 30 custom scores were recomputed with starter.ndcg10 and checked against saved scores. Only this supplementary selected population is described.

Protocol hash: `0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b`.

**14 users** have differing nDCG@10; listed in cohort/protocol order. Displayed nDCG values have four decimals; differences use full-precision scores.

| User ID | True ISIN count | A nDCG@10 | B nDCG@10 | C nDCG@10 | C−A | C−B |
|---|---:|---:|---:|---:|---:|---:|
| 3FAB1216645DBF9FC391 | 1 | 0.4307 | 0.0000 | 0.0000 | -0.430676558073 | 0.000000000000 |
| DEE685C08495625E2CB3 | 1 | 0.3155 | 0.3155 | 0.3869 | 0.071387930449 | 0.071387930449 |
| 6FD92260F5CD59010BDA | 1 | 0.6309 | 0.4307 | 0.4307 | -0.200253195498 | 0.000000000000 |
| 6CCB559F48BD168BB227 | 1 | 0.0000 | 0.0000 | 0.3333 | 0.333333333333 | 0.333333333333 |
| 5EF4173222C69D6AFA85 | 1 | 0.6309 | 0.6309 | 1.0000 | 0.369070246429 | 0.369070246429 |
| B169103F59DFB249D32D | 1 | 0.5000 | 1.0000 | 0.5000 | 0.000000000000 | -0.500000000000 |
| D08E5E05063833CA4EBF | 1 | 1.0000 | 0.6309 | 1.0000 | 0.000000000000 | 0.369070246429 |
| 36A1D10726F401E8CD08 | 1 | 1.0000 | 0.6309 | 1.0000 | 0.000000000000 | 0.369070246429 |
| AAAE25FF4E9700C47E3E | 1 | 1.0000 | 0.3869 | 0.3562 | -0.643792812892 | -0.030645620127 |
| E6A83433DE641AC29D80 | 2 | 0.2372 | 0.0000 | 0.3066 | 0.069375883613 | 0.306573596383 |
| B3A2A04F88AE062E7C41 | 1 | 0.5000 | 1.0000 | 1.0000 | 0.500000000000 | 0.000000000000 |
| CC41DAC17629A7642FA4 | 1 | 0.6309 | 0.3155 | 0.3155 | -0.315464876786 | 0.000000000000 |
| FC64C3A0F91B83228770 | 1 | 1.0000 | 0.6309 | 0.6309 | -0.369070246429 | 0.000000000000 |
| F5A532DB556FA729588B | 1 | 0.4307 | 0.5000 | 0.4307 | 0.000000000000 | -0.069323441927 |

## Sum-to-mean checks

| Comparison | Sum over differing users | All-30 sum | All-30 mean |
|---|---:|---:|---:|
| C−A | -0.616090295854 | -0.616090295854 | -0.020536343195 |
| C−B | 1.218536537397 | 1.218536537397 | 0.040617884580 |

Histories are extracted verbatim from C’s summary_prompt and checked equal to B’s actual Investor information block. Hit positions are 1-based; all hits are listed, not only the first. No assessment of retained or dropped information is supplied.

## User `3FAB1216645DBF9FC391`

**True ISIN count:** 1. **True ISINs:** `GRS015003007`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS015003007` at position 4 | 0.4307 |
| B | (no hits) | 0.0000 |
| C | (no hits) | 0.0000 |

**C−A:** -0.430676558073. **C−B:** 0.000000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically within the banks and regional banking industry. The purchase is concentrated in a single asset, indicating a high level of concentration. The investor does not show any repeated purchases, as only one transaction is recorded.
```

## User `DEE685C08495625E2CB3`

**True ISIN count:** 1. **True ISINs:** `GRS003003035`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS003003035` at position 8 | 0.3155 |
| B | `GRS003003035` at position 8 | 0.3155 |
| C | `GRS003003035` at position 5 | 0.3869 |

**C−A:** 0.071387930449. **C−B:** 0.071387930449.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically within the banks and regional banking industry. The purchase is concentrated in a single asset, indicating a high level of concentration in one asset. The investor does not show any repeated purchases, as only one transaction is recorded.
```

## User `6FD92260F5CD59010BDA`

**True ISIN count:** 1. **True ISINs:** `GRS015003007`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS015003007` at position 2 | 0.6309 |
| B | `GRS015003007` at position 4 | 0.4307 |
| C | `GRS015003007` at position 4 | 0.4307 |

**C−A:** -0.200253195498. **C−B:** 0.000000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 2x
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 2x
```

**Arm C summary:**

```text
The investor purchases two shares of large-cap stocks in the financial services sector, specifically in the banks-regional category, and another two shares of a large-cap stock in the same market. The purchases are concentrated in two different assets, with each purchase occurring twice. The investor shows a level of repetition in their buying behavior, as they buy the same type of assets multiple times.
```

## User `6CCB559F48BD168BB227`

**True ISIN count:** 1. **True ISINs:** `GRS003003035`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | (no hits) | 0.0000 |
| B | (no hits) | 0.0000 |
| C | `GRS003003035` at position 7 | 0.3333 |

**C−A:** 0.333333333333. **C−B:** 0.333333333333.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS191213008 | assetCategory: stock, assetSubCategory: large cap, industry: engineering & construction, marketID: xath, sector: industrials | bought 1x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS501003008 | assetCategory: stock, industry: financial data & stock exchanges, marketID: enax, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services sector, with a focus on banks and regional banks, and also includes some investments in industrials and financial data & stock exchanges. The purchases are concentrated in the financial services sector, with multiple entries for the same industry. The investor shows a tendency to repeat purchases of similar assets, particularly in the financial services sector.
```

## User `5EF4173222C69D6AFA85`

**True ISIN count:** 1. **True ISINs:** `GRS003003035`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS003003035` at position 2 | 0.6309 |
| B | `GRS003003035` at position 2 | 0.6309 |
| C | `GRS003003035` at position 1 | 1.0000 |

**C−A:** 0.369070246429. **C−B:** 0.369070246429.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 2x
```

**Arm C summary:**

```text
The investor buys two shares of a large-cap stock (GRS003003035) in the market XATH, indicating a focus on a single asset. The purchase is concentrated, with the investor buying two units of the same asset. The transaction does not show any repetition of purchases, as only one transaction is recorded.
```

## User `B169103F59DFB249D32D`

**True ISIN count:** 1. **True ISINs:** `GRS014003032`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS014003032` at position 3 | 0.5000 |
| B | `GRS014003032` at position 1 | 1.0000 |
| C | `GRS014003032` at position 3 | 0.5000 |

**C−A:** 0.000000000000. **C−B:** -0.500000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS191213008 | assetCategory: stock, assetSubCategory: large cap, industry: engineering & construction, marketID: xath, sector: industrials | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services and industrials sectors. They have made multiple purchases of the same asset, with 3x of GRS015003007 and 1x of GRS191213008. The purchases are concentrated in two distinct market categories, indicating a focus on specific industries and regions.
```

## User `D08E5E05063833CA4EBF`

**True ISIN count:** 1. **True ISINs:** `GRS004013009`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS004013009` at position 1 | 1.0000 |
| B | `GRS004013009` at position 2 | 0.6309 |
| C | `GRS004013009` at position 1 | 1.0000 |

**C−A:** 0.000000000000. **C−B:** 0.369070246429.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS004013009 | assetCategory: stock, industry: banks - regional, marketID: xath, sector: financial services | bought 4x
```

**Arm C summary:**

```text
This investor primarily purchases stocks in the banking and regional financial services sectors, specifically within the market ID xath. The purchase history shows a concentrated investment in a single asset, GRS004013009, with 4 buy transactions. The investor appears to repeat purchases of the same asset, indicating a potential preference for this particular stock.
```

## User `36A1D10726F401E8CD08`

**True ISIN count:** 1. **True ISINs:** `GRS004013009`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS004013009` at position 1 | 1.0000 |
| B | `GRS004013009` at position 2 | 0.6309 |
| C | `GRS004013009` at position 1 | 1.0000 |

**C−A:** 0.000000000000. **C−B:** 0.369070246429.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS004013009 | assetCategory: stock, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases stocks in the banking and regional financial services sector, specifically in the market identified as xath. The purchase is concentrated in a single asset, GRS004013009, indicating a focused investment strategy. The investor has made a single buy transaction, suggesting a lack of repetition in their purchases.
```

## User `AAAE25FF4E9700C47E3E`

**True ISIN count:** 1. **True ISINs:** `GRF000030004`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRF000030004` at position 1 | 1.0000 |
| B | `GRF000030004` at position 5 | 0.3869 |
| C | `GRF000030004` at position 6 | 0.3562 |

**C−A:** -0.643792812892. **C−B:** -0.030645620127.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
- GRF000030004 | assetCategory: mtf, assetSubCategory: bond, marketID: aedak | bought 1x
```

**Arm C summary:**

```text
The investor purchases bonds from the oil and gas extraction and refining sector, with the majority of their investments in corporate bonds. They have made two distinct purchases: one in the GRC4261213D5 category and another in the GRF000030004 category. The purchases are not repeated, indicating a focus on different assets within the same sector.
```

## User `E6A83433DE641AC29D80`

**True ISIN count:** 2. **True ISINs:** `GRS001003037`, `GRS314003005`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS001003037` at position 5 | 0.2372 |
| B | (no hits) | 0.0000 |
| C | `GRS001003037` at position 3 | 0.3066 |

**C−A:** 0.069375883613. **C−B:** 0.306573596383.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically within the banks and regional banking industry. The purchase is concentrated in a single asset, indicating a high level of concentration. The investor does not show any repeated purchases, as only one transaction is recorded.
```

## User `B3A2A04F88AE062E7C41`

**True ISIN count:** 1. **True ISINs:** `GRS014003032`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS014003032` at position 3 | 0.5000 |
| B | `GRS014003032` at position 1 | 1.0000 |
| C | `GRS014003032` at position 1 | 1.0000 |

**C−A:** 0.500000000000. **C−B:** 0.000000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 1x
- GRS015003007 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
- GRS323003012 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases large-cap stocks in the financial services sector, specifically in banks-regional and financial services industries. They have made three separate purchases of similar assets, indicating some level of repetition. The purchases are concentrated in the same market (xath) and asset categories, suggesting a focused investment strategy.
```

## User `CC41DAC17629A7642FA4`

**True ISIN count:** 1. **True ISINs:** `LU0147414022`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `LU0147414022` at position 2 | 0.6309 |
| B | `LU0147414022` at position 8 | 0.3155 |
| C | `LU0147414022` at position 8 | 0.3155 |

**C−A:** -0.315464876786. **C−B:** 0.000000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- LU0147414022 | assetCategory: mtf, assetSubCategory: equity, marketID: xlux | bought 2x
```

**Arm C summary:**

```text
The investor buys equity assets categorized under "mtf" with a market ID of "xlux," indicating a focus on a specific market. The purchase is concentrated, with 2x the quantity of the asset. The investor does not appear to repeat purchases of the same asset, as there is only one transaction recorded.
```

## User `FC64C3A0F91B83228770`

**True ISIN count:** 1. **True ISINs:** `GRS003003035`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS003003035` at position 1 | 1.0000 |
| B | `GRS003003035` at position 2 | 0.6309 |
| C | `GRS003003035` at position 2 | 0.6309 |

**C−A:** -0.369070246429. **C−B:** 0.000000000000.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS003003035 | assetCategory: stock, assetSubCategory: large cap, marketID: xath | bought 3x
- GRC4261213D5 | assetCategory: bond, assetSubCategory: corporate, industry: oil and gas extraction and refining, marketID: xath, sector: corporate | bought 1x
- GRF000023009 | assetCategory: mtf, assetSubCategory: bond, marketID: aedak | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases stocks and bonds, with a focus on large-cap stocks and corporate bonds. They have made multiple purchases of a single stock (GRS003003035) and a single bond (GRC4261213D5), indicating some level of concentration in specific assets. The purchase of a mortgage-backed security (GRF000023009) suggests exposure to a different market, possibly with a different risk profile. The investor shows some repetition in their purchases, particularly for the stock and bond assets.
```

## User `F5A532DB556FA729588B`

**True ISIN count:** 1. **True ISINs:** `GRS014003032`

| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |
|---|---|---:|
| A | `GRS014003032` at position 4 | 0.4307 |
| B | `GRS014003032` at position 3 | 0.5000 |
| C | `GRS014003032` at position 4 | 0.4307 |

**C−A:** 0.000000000000. **C−B:** -0.069323441927.

**Arm B history (same history supplied to C’s summarizer):**

```text
History as of 2021-06-01 (Buy transactions only):
- GRS004013009 | assetCategory: stock, industry: banks - regional, marketID: xath, sector: financial services | bought 3x
- GRS014003032 | assetCategory: stock, assetSubCategory: large cap, industry: banks - regional, marketID: xath, sector: financial services | bought 1x
```

**Arm C summary:**

```text
The investor primarily purchases stocks in the financial services sector, specifically in the banks - regional category, with a focus on the market ID xath. They have made multiple purchases of the same asset, with 3x of GRS004013009 and 1x of GRS014003032. The purchases are concentrated in a single asset category and sector, indicating a focused investment strategy.
```
