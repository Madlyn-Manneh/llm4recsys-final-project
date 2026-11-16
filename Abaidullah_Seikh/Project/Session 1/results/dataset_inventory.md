# Dataset inventory

Student: Abaidullah Seikh  
Course: LLM4Rec, HSE University  
Scope: Homework 1, Session 1, Task 1 inspection notes only.

**AI-assisted inspection by OpenCode (openai/gpt-6-astra). Personal verification by the student is pending.** These files are not the final homework report.

## Individual research question

Does using LLM-generated transaction-history summaries improve nDCG@10 for predicting future asset purchases compared with structured-history features for FAR-Trans users with sparse histories?

## Sources read and scope

- `FAR-Trans/README.txt`: file meanings, UTF-8 CSV conventions, CC-BY 4.0 license.
- `session1_research_question_instructions (2).md`, v1.2: §2 fixes Top-10/nDCG@10 against future purchases but leaves the exact split, item scope and eligibility pending; §4 example A requires the same candidates, item information and downstream ranker; §6 requires personal checking of a raw record; §14 requires an authentic session export.
- `LLM4Recsys 07. LLM-Based Recommendation and FAR-Trans Project.pdf`, pp. 12–16 (data, past-only inputs, shared benchmark), p. 18 (Session 1 milestone). The Top-5 diagram on p. 15 is illustrative; the shared output is Top-10.
- These are locally supplied sources. No external paper or web source was independently opened.

## All files in the supplied dataset directory

| File | Record count | Format/count definition | Bytes |
| --- | --- | --- | --- |
| README.txt | N/A | Documentation text | 7,135 |
| asset_information.csv | 836 | CSV data records, header excluded | 83,851 |
| close_prices.csv | 703,303 | CSV data records, header excluded | 22,668,996 |
| customer_information.csv | 32,468 | CSV data records, header excluded | 2,408,798 |
| limit_prices.csv | 807 | CSV data records, header excluded | 56,622 |
| markets.csv | 38 | CSV data records, header excluded | 11,771 |
| questionnaires.csv | N/A; 25 questions, 5 sections | Plain text, not a rectangular CSV; no customer answers | 7,216 |
| transactions.csv | 388,048 | CSV data records, header excluded | 35,651,778 |

The supplied `FAR-Trans.zip` is the container archive, not an additional table.

### `transactions.csv`: exact ordered CSV column names

```text
customerID,ISIN,transactionID,transactionType,timestamp,totalValue,units,channel,marketID
```

### `asset_information.csv`: exact ordered CSV column names

```text
ISIN,assetName,assetShortName,assetCategory,assetSubCategory,marketID,sector,industry,timestamp
```

### `customer_information.csv`: exact ordered CSV column names

```text
customerID,customerType,riskLevel,investmentCapacity,lastQuestionnaireDate,timestamp
```

### `close_prices.csv`: exact ordered CSV column names

```text
ISIN,timestamp,closePrice
```

### `limit_prices.csv`: exact ordered CSV column names

```text
ISIN,minDate,maxDate,priceMinDate,priceMaxDate,profitability
```

### `markets.csv`: exact ordered CSV column names

```text
exchangeID,marketID,name,description,country,tradingDays,tradingHours,marketClass
```

## Customers, assets and transactions

| Measure | Observed value |
| --- | --- |
| Transaction data records (excluding header) | 388,048 |
| Distinct customerID in transactions | 29,090 |
| Distinct customerID in customer_information | 29,090 |
| Distinct traded ISIN (Buy or Sell) | 320 |
| Distinct purchased ISIN | 320 |
| Distinct ISIN in asset_information | 806 |
| Distinct ISIN in close_prices | 807 |
| Distinct ISIN in limit_prices | 807 |
| transactionType = Buy | 228,913 |
| transactionType = Sell | 159,135 |
| Observed transaction date range (inclusive) | 2018-01-02 to 2022-11-30 |

The presentation p. 12 displays 388,049 transaction rows. Direct CSV parsing gives **388,048 data records**; including the single header gives 388,049 CSV records. Report the parsed data count, rather than copying the slide count. The slide also says the dataset includes reconstructed transactions; the raw schema has no explicit reconstruction/provenance flag, so this inspection does not identify individual rows as reconstructed.

## Fields relevant to RQ1

| Source and exact fields | Use and provenance |
| --- | --- |
| transactions: customerID, ISIN, timestamp, transactionType | Released transaction records: user/item links, chronological histories, Buy labels in a future window once specified. |
| transactions: totalValue, units, channel, marketID | Recorded context for summaries and matching structured aggregates; pre-cutoff only, with value/units quality checks. |
| transactions: transactionID | Audit and duplicate checks; not a preference feature. |
| asset_information: assetName, assetShortName, assetCategory, assetSubCategory, sector, industry, marketID, timestamp | Recorded descriptive metadata, including missing fields; join by ISIN with as-of timing. Both methods receive identical allowed metadata. |
| customer_information: customerType, riskLevel, investmentCapacity, lastQuestionnaireDate, timestamp | Optional recorded profile snapshots; risk/capacity may be predicted or missing. Timing must be resolved before use; not required for a history-only comparison. |
| close_prices: ISIN, timestamp, closePrice | Optional price context, only actually available past closes; not needed for the primary RQ. |
| limit_prices: minDate, maxDate, priceMinDate, priceMaxDate, profitability | Full-series summaries; unsafe as historical features without recomputation from permitted past data. |
| markets: marketID, exchangeID, name, description, country, tradingDays, tradingHours, marketClass | Optional market context; no version timestamp, historical availability is unproven. |
| questionnaires.csv | Question wording and possible choices only; no observed customer answers. Do not generate demographic/profile answers. |

## Reproduction and integrity

```bash
python3 scripts/inspect_far_trans.py
```

Runtime used for this generation: Python 3.14.4; standard library only. The script reads raw inputs only, computes exact-string counts, and regenerates all four Markdown files. Date checks use ISO dates; quantiles use linear interpolation at `(n-1)*p/100`. All raw file SHA-256 values are checked again after inspection.

Supplied archive SHA-256: `d0d6cfe027732bab45fdcf9af80eff4fefddc789aedae9bdce0d3d6cfd05cfb6`. All 8 dataset files match their archive members byte-for-byte. This establishes local archive consistency, not external download provenance.

| Raw file | SHA-256 |
| --- | --- |
| README.txt | `5aa20b492c9fe18c8b5a147ad13fae99862c78aea59cbf542b734b5eef9ea072` |
| asset_information.csv | `33f9897b14087068fba53a0bc9e24a0031b096bd3ad3e977e534153f29b7a590` |
| close_prices.csv | `6ba1fe8390b31dfb3ab4e3e824910f9e8da4684cb6074cdb82eb6422a323656d` |
| customer_information.csv | `c4ad52ebca90e32bf3df5eb64f362b7a3437b77d978b22627cc46927fe7064af` |
| limit_prices.csv | `b5a9bc304e2a4a31f5e3d0959b22c5c6135b69f13ce6f92123fc7e1e92600c8f` |
| markets.csv | `009d5764b5eb59e979d8c22954482cf7bb8ed5fdb3382a6fb03f3c6cd1316960` |
| questionnaires.csv | `f4a902f7ac344f70708433a40d33163972da1652d6f91a42e3e280b17eedcea0` |
| transactions.csv | `358871fa1311a802799df86e56c3d633513566965b01412d058e0f8fbe6cd54b` |

The OpenCode conversation is the authentic AI work history. These generated notes are not a session export. No session log is rewritten or synthesized by this script. Preserve the native session and use OpenCode's native export for the eventual homework submission; a native export has not been created here.
