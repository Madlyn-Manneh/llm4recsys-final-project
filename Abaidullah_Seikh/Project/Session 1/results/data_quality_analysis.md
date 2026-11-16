# Data-quality analysis and leakage risks

Student: Abaidullah Seikh  
Course: LLM4Rec, HSE University  
Scope: Homework 1, Session 1, Task 1 inspection notes only.

**AI-assisted inspection by OpenCode (openai/gpt-6-astra). Personal verification by the student is pending.** These files are not the final homework report.

## Check definitions

Counts are computed on original string cells. Blank means empty or whitespace-only. Marker checks are case-insensitive exact matches after trimming for `Not_Available`, `nan`, `NA`, `N/A`, `null`, `None`, `unknown`; markers are reported separately from blank cells. No automatic NA conversion or imputation occurs. Duplicate counts mean extra records beyond the first, with repeated-key groups also reported. Repeated customer/asset identifiers may be legitimate snapshots, not necessarily errors.

## File-level checks

| File | Malformed-width records | Blank records | Exact duplicate rows (extra) | Surrounding-whitespace cells |
| --- | --- | --- | --- | --- |
| transactions.csv | 0 | 0 | 0 | 0 |
| asset_information.csv | 0 | 0 | 0 | 0 |
| customer_information.csv | 0 | 0 | 0 | 0 |
| close_prices.csv | 0 | 0 | 0 | 0 |
| limit_prices.csv | 0 | 0 | 0 | 0 |
| markets.csv | 0 | 0 | 0 | 1 |

## Missing values: every CSV column

| File | Exact column | Blank cells | Marker cells |
| --- | --- | --- | --- |
| transactions.csv | customerID | 0 | 0 |
| transactions.csv | ISIN | 0 | 0 |
| transactions.csv | transactionID | 0 | 0 |
| transactions.csv | transactionType | 0 | 0 |
| transactions.csv | timestamp | 0 | 0 |
| transactions.csv | totalValue | 0 | 0 |
| transactions.csv | units | 0 | 0 |
| transactions.csv | channel | 0 | 0 |
| transactions.csv | marketID | 0 | 0 |
| asset_information.csv | ISIN | 0 | 0 |
| asset_information.csv | assetName | 24 | 0 |
| asset_information.csv | assetShortName | 1 | 0 |
| asset_information.csv | assetCategory | 0 | 0 |
| asset_information.csv | assetSubCategory | 269 | 0 |
| asset_information.csv | marketID | 0 | 0 |
| asset_information.csv | sector | 388 | 0 |
| asset_information.csv | industry | 439 | 0 |
| asset_information.csv | timestamp | 0 | 0 |
| customer_information.csv | customerID | 0 | 0 |
| customer_information.csv | customerType | 0 | 0 |
| customer_information.csv | riskLevel | 0 | 344 |
| customer_information.csv | investmentCapacity | 0 | 347 |
| customer_information.csv | lastQuestionnaireDate | 0 | 0 |
| customer_information.csv | timestamp | 0 | 0 |
| close_prices.csv | ISIN | 0 | 0 |
| close_prices.csv | timestamp | 0 | 0 |
| close_prices.csv | closePrice | 0 | 0 |
| limit_prices.csv | ISIN | 0 | 0 |
| limit_prices.csv | minDate | 0 | 0 |
| limit_prices.csv | maxDate | 0 | 0 |
| limit_prices.csv | priceMinDate | 0 | 0 |
| limit_prices.csv | priceMaxDate | 0 | 0 |
| limit_prices.csv | profitability | 0 | 0 |
| markets.csv | exchangeID | 0 | 0 |
| markets.csv | marketID | 0 | 0 |
| markets.csv | name | 0 | 0 |
| markets.csv | description | 0 | 0 |
| markets.csv | country | 0 | 0 |
| markets.csv | tradingDays | 0 | 0 |
| markets.csv | tradingHours | 1 | 0 |
| markets.csv | marketClass | 0 | 0 |

### Literal missing-marker values

| File | Column | Literal value | Rows |
| --- | --- | --- | --- |
| customer_information.csv | investmentCapacity | `Not_Available` | 347 |
| customer_information.csv | riskLevel | `Not_Available` | 344 |

## Identifier and composite-key duplication

| File | Key | Distinct keys | Repeated-key groups | Extra rows on key |
| --- | --- | --- | --- | --- |
| transactions.csv | transactionID | 359128 | 23388 | 28920 |
| transactions.csv | customerID, transactionID | 388048 | 0 | 0 |
| transactions.csv | customerID, ISIN, transactionID | 388048 | 0 | 0 |
| asset_information.csv | ISIN | 806 | 28 | 30 |
| asset_information.csv | ISIN, timestamp | 833 | 3 | 3 |
| customer_information.csv | customerID | 29090 | 2263 | 3378 |
| customer_information.csv | customerID, timestamp | 32468 | 0 | 0 |
| close_prices.csv | ISIN, timestamp | 703303 | 0 | 0 |
| limit_prices.csv | ISIN | 807 | 0 | 0 |
| markets.csv | marketID | 38 | 0 | 0 |
| markets.csv | exchangeID | 29 | 7 | 9 |

`exchangeID` may cover several markets; it is not assumed to be a unique market key. Same-identifier snapshots require timestamp-aware joins; same-identifier/same-date conflicts require explicit tie resolution.

### Repeated transactionID examples

| transactionID (first five lexically sorted) | Rows | Distinct customers | Distinct ISINs | Fields that differ within group |
| --- | --- | --- | --- | --- |
| 10001684 | 3 | 3 | 1 | customerID |
| 10001692 | 2 | 2 | 1 | customerID |
| 10001703 | 2 | 2 | 1 | customerID |
| 10001726 | 3 | 3 | 1 | customerID |
| 10001738 | 4 | 4 | 1 | customerID |

A repeated transactionID alone is not evidence of a duplicated event. The composite-key counts above test additional context; preserve original record indices for audit and do not drop rows using transactionID alone. The release does not explain each identifier collision.

### Asset records sharing an ISIN and timestamp

| ISIN | assetName | assetShortName | assetCategory | assetSubCategory | marketID | sector | industry | timestamp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `LU0055631609` | `BlackRock Global Funds - World Gold Fund A2` | `GOLD` | `Stock` | `""` (empty field) | `CCLX` | `Sector Equity Precious Metals` | `""` (empty field) | `2018-01-02` |
| `LU0055631609` | `BlackRock Global Funds - World Gold Fund A2` | `GOLD` | `MTF` | `Equity` | `CCLX` | `""` (empty field) | `""` (empty field) | `2018-01-02` |
| `IE00B66F4759` | `iShares € High Yield Corp Bond UCITS ETF EUR (Dist) \| IHYG` | `HY` | `Stock` | `""` (empty field) | `XLON` | `EUR High Yield Bond` | `""` (empty field) | `2018-01-02` |
| `IE00B66F4759` | `iShares € High Yield Corp Bond UCITS ETF EUR (Dist) \| IHYG` | `HY` | `MTF` | `Bond` | `XLON` | `""` (empty field) | `""` (empty field) | `2018-01-02` |
| `IE00BCRY6003` | `Ishares Usd Short Dur Hy Crp` | `SDHY` | `Stock` | `""` (empty field) | `XLON` | `""` (empty field) | `""` (empty field) | `2018-04-27` |
| `IE00BCRY6003` | `Ishares Usd Short Dur Hy Crp` | `SDHY` | `MTF` | `Other` | `XLON` | `""` (empty field) | `""` (empty field) | `2018-04-27` |

## Cross-file identifier coverage

| Check | Distinct unmatched identifiers | First 10 sorted examples |
| --- | --- | --- |
| Transaction customers absent from customer_information | 0 | — |
| Profile customers absent from transactions | 0 | — |
| Traded ISIN absent from asset_information | 0 | — |
| Metadata ISIN never traded | 486 | `AU3CB0228823`, `AU3CB0237725`, `AU3CB0237881`, `AU3CB0258465`, `AU3SG0001985`, `AU3SG0002199`, `BE0974293251`, `BMG375851091`, `CA037833CY47`, `CA580135CD12` |
| Traded ISIN absent from close_prices | 0 | — |
| Transaction marketID absent from markets | 0 | — |
| Asset marketID absent from markets | 0 | — |
| close_prices ISIN absent from asset_information | 1 | `GRX497003012` |
| limit_prices ISIN absent from close_prices | 0 | — |

### ISIN shape screening

| File | Distinct identifiers not matching standard 12-character shape | First 10 examples |
| --- | --- | --- |
| transactions.csv | 2 | 100974271034, XSTITANBOND27 |
| asset_information.csv | 2 | 100974271034, XSTITANBOND27 |
| close_prices.csv | 2 | 100974271034, XSTITANBOND27 |
| limit_prices.csv | 2 | 100974271034, XSTITANBOND27 |

This is only a syntactic screen, not check-digit validation or proof that a security is invalid. Preserve original identifiers; do not guess corrections or merge similar strings.

## Dates and numeric checks

| File | Date column | Minimum valid date | Maximum valid date | Invalid nonblank dates |
| --- | --- | --- | --- | --- |
| transactions.csv | timestamp | 2018-01-02 | 2022-11-30 | 0 |
| asset_information.csv | timestamp | 2018-01-01 | 2022-10-31 | 0 |
| customer_information.csv | lastQuestionnaireDate | 2000-01-01 | 2022-11-23 | 0 |
| customer_information.csv | timestamp | 2000-01-01 | 2022-11-30 | 0 |
| close_prices.csv | timestamp | 2018-01-01 | 2022-11-29 | 0 |
| limit_prices.csv | minDate | 2018-01-01 | 2022-10-31 | 0 |
| limit_prices.csv | maxDate | 2018-01-19 | 2022-11-29 | 0 |

| File | Numeric field | Unparseable | Nonfinite | Negative | Zero |
| --- | --- | --- | --- | --- | --- |
| transactions.csv | totalValue | 0 | 0 | 0 | 0 |
| transactions.csv | units | 0 | 0 | 0 | 0 |
| close_prices.csv | closePrice | 0 | 0 | 0 | 0 |
| limit_prices.csv | priceMinDate | 0 | 0 | 0 | 0 |
| limit_prices.csv | priceMaxDate | 0 | 0 | 0 | 0 |
| limit_prices.csv | profitability | 0 | 0 | 360 | 9 |

Negative profitability can be a valid loss; zero/negative trade values or prices are flags for investigation, not automatic grounds to delete raw rows.

## Exact observed category values

| File | Column | Value | Rows |
| --- | --- | --- | --- |
| transactions.csv | transactionType | `Buy` | 228913 |
| transactions.csv | transactionType | `Sell` | 159135 |
| transactions.csv | channel | `Branch` | 71266 |
| transactions.csv | channel | `Internet Banking` | 250805 |
| transactions.csv | channel | `Phone Banking` | 65977 |
| asset_information.csv | assetCategory | `Bond` | 225 |
| asset_information.csv | assetCategory | `MTF` | 318 |
| asset_information.csv | assetCategory | `Stock` | 293 |
| asset_information.csv | assetSubCategory | `""` (empty field) | 269 |
| asset_information.csv | assetSubCategory | `Balanced` | 8 |
| asset_information.csv | assetSubCategory | `Bond` | 108 |
| asset_information.csv | assetSubCategory | `Bonds` | 1 |
| asset_information.csv | assetSubCategory | `Corporate` | 170 |
| asset_information.csv | assetSubCategory | `Equity` | 107 |
| asset_information.csv | assetSubCategory | `Government` | 55 |
| asset_information.csv | assetSubCategory | `Large Cap` | 24 |
| asset_information.csv | assetSubCategory | `Money Market` | 19 |
| asset_information.csv | assetSubCategory | `Other` | 73 |
| asset_information.csv | assetSubCategory | `Structured` | 2 |
| customer_information.csv | customerType | `Inactive` | 211 |
| customer_information.csv | customerType | `Legal Entity` | 80 |
| customer_information.csv | customerType | `Mass` | 19810 |
| customer_information.csv | customerType | `Premium` | 10321 |
| customer_information.csv | customerType | `Professional` | 2046 |
| customer_information.csv | riskLevel | `Aggressive` | 3202 |
| customer_information.csv | riskLevel | `Balanced` | 8684 |
| customer_information.csv | riskLevel | `Conservative` | 2916 |
| customer_information.csv | riskLevel | `Income` | 10048 |
| customer_information.csv | riskLevel | `Not_Available` | 344 |
| customer_information.csv | riskLevel | `Predicted_Aggressive` | 298 |
| customer_information.csv | riskLevel | `Predicted_Balanced` | 1430 |
| customer_information.csv | riskLevel | `Predicted_Conservative` | 2842 |
| customer_information.csv | riskLevel | `Predicted_Income` | 2704 |
| customer_information.csv | investmentCapacity | `CAP_30K_80K` | 5529 |
| customer_information.csv | investmentCapacity | `CAP_80K_300K` | 4220 |
| customer_information.csv | investmentCapacity | `CAP_GT300K` | 888 |
| customer_information.csv | investmentCapacity | `CAP_LT30K` | 14030 |
| customer_information.csv | investmentCapacity | `Not_Available` | 347 |
| customer_information.csv | investmentCapacity | `Predicted_CAP_30K_80K` | 965 |
| customer_information.csv | investmentCapacity | `Predicted_CAP_80K_300K` | 1025 |
| customer_information.csv | investmentCapacity | `Predicted_CAP_GT300K` | 15 |
| customer_information.csv | investmentCapacity | `Predicted_CAP_LT30K` | 5449 |

## Customer-profile provenance and timing

| Profile field | Classification | Rows |
| --- | --- | --- |
| customerType | recorded, not explicitly marked predicted | 32468 |
| riskLevel | missing | 344 |
| riskLevel | predicted/estimated (explicit Predicted_ prefix) | 7274 |
| riskLevel | recorded, not explicitly marked predicted | 24850 |
| investmentCapacity | missing | 347 |
| investmentCapacity | predicted/estimated (explicit Predicted_ prefix) | 7454 |
| investmentCapacity | recorded, not explicitly marked predicted | 24667 |
| lastQuestionnaireDate | recorded, not explicitly marked predicted | 32468 |
| timestamp | recorded, not explicitly marked predicted | 32468 |

'Recorded, not explicitly marked predicted' is an observed release value, not independent confirmation of a customer's true state or an assurance of pre-cutoff availability. `lastQuestionnaireDate` describes the questionnaire, while `timestamp` is documented as last update. Preserve `Predicted_` flags; the release does not document the estimation model's training window or feature provenance. Raw investment-capacity spellings differ from examples in the README (e.g. underscore placement); use the observed category table above.

Observed questionnaire dates later than their own profile-row timestamp: **12,501 rows**, **12,048 distinct customers**. `lastQuestionnaireDate == 2000-01-01` occurs in **7,275 rows**. The repeated 2000 date is a possible placeholder, not a confirmed missing-value code.

First five inconsistent rows in original file order:

| customerID | customerType | riskLevel | investmentCapacity | lastQuestionnaireDate | timestamp |
| --- | --- | --- | --- | --- | --- |
| `DED5BF19E23CCCFEE322` | `Premium` | `Balanced` | `CAP_80K_300K` | `2021-11-30` | `2021-03-19` |
| `3E8D8E4E07CD3210F25F` | `Mass` | `Income` | `CAP_30K_80K` | `2021-11-03` | `2018-01-02` |
| `F2D15B652031EDFBEB7F` | `Mass` | `Conservative` | `CAP_LT30K` | `2020-04-01` | `2018-01-02` |
| `A7B4D996481D603A57F6` | `Premium` | `Balanced` | `CAP_30K_80K` | `2022-11-17` | `2020-03-19` |
| `577BA995A03A381996D9` | `Mass` | `Conservative` | `CAP_LT30K` | `2021-06-02` | `2018-01-02` |

Transaction rows with no asset metadata row dated on/before their transaction date: **0**. This event-time diagnostic does not assign a prediction cutoff.

Most frequent transaction dates (possible concentration, not proof of reconstruction):

| Date | Transactions |
| --- | --- |
| 2018-01-02 | 35739 |
| 2021-03-19 | 3022 |
| 2021-07-16 | 2719 |
| 2021-11-12 | 1899 |
| 2022-01-21 | 1803 |

## Price-summary consistency

| Check against close-price endpoints / ROI formula | Flagged rows |
| --- | --- |
| maxDate mismatch | 0 |
| minDate after maxDate | 0 |
| minDate mismatch | 0 |
| priceMaxDate mismatch | 0 |
| priceMinDate mismatch | 0 |
| profitability mismatch (relative/absolute tolerance 1e-9) | 0 |

Endpoint consistency does not make full-series profitability safe for a historical prediction.

## Leakage: observed facts versus proposed safeguards

| Risk | Observed fact | Proposed safeguard (not official protocol) |
| --- | --- | --- |
| Post-cutoff transactions | Transactions span 2018-01-02 to 2022-11-30. No official cutoff is supplied, so no post-cutoff count or train/test allocation can be asserted. | When specified, isolate history before the cutoff and future Buy labels in the shared window. Filter before summaries, counts, vocabulary, popularity and preprocessing; never select sparse users from future counts. |
| Time-dependent asset metadata | Asset timestamps span 2018-01-01 to 2022-10-31; repeated ISINs and composite-key checks are above. | As-of join only metadata known by prediction time; do not backfill later versions. Resolve same-date conflicts and leave unavailable attributes missing. Last-update stamps alone do not prove archival availability. |
| Risk profiles and investment capacity | Customer snapshots repeat; riskLevel and investmentCapacity contain explicitly Predicted_ values and missing markers. | Prefer history-only inputs for the first comparison unless provenance is established. If included, use time-valid snapshots identically in both arms, retain observed/predicted/missing distinctions, and do not infer actual wealth or risk tolerance. |
| Predicted values | The README says Predicted_ risk/capacity values are algorithmic; their training data and fit dates are not supplied. | An apparently old row may still contain estimates based on later information. Exclude unverified estimates from the main historical comparison or justify provenance and test a declared ablation. |
| Questionnaire dates | 12,501 profile rows have lastQuestionnaireDate > timestamp; 7,275 use 2000-01-01. questionnaires.csv contains no user answers. | A timestamp-only join is insufficient. Require known questionnaire availability as well as snapshot availability; quarantine inconsistent/unknown cases pending clarification. Merely setting effective time to the later date is conservative but not proof of historical availability. |
| Future prices and full-period returns | Close prices extend to 2022-11-29. limit_prices contains maxDate, priceMaxDate and full-series profitability. | Omit full-series price summaries from history features. If prices are used, build features from closes available before the decision; never use same-day close for an earlier intraday decision, future normalization or future returns. |
| Candidate availability and survivorship | Full-release asset and price inventories span multiple years; markets.csv has no timestamp. | Do not infer historical availability from eventual trading or series endpoints; apply the forthcoming shared universe and document residual survivorship/staleness. |
| LLM contamination and information asymmetry | The homework names these risks; no LLM summaries or recommendations have been generated in this inspection. | Later record model/version/knowledge cutoff, ground summaries in permitted inputs, avoid external future facts, and give the structured baseline the identical underlying information. |

No cleaning is applied. These checks are screening diagnostics, not a certification of correctness or profitability. No recommendation model is trained and no split is invented.
