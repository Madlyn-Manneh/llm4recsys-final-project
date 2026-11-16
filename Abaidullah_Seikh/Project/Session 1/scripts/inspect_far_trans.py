#!/usr/bin/env python3
"""Read-only FAR-Trans inspection; generates Task 1 notes, not a homework report.

Python >=3.9, standard library only. Run from the Session 1 directory:
    python3 scripts/inspect_far_trans.py
All CSV cells are read as strings, preserving identifiers and decimal spelling.
No split, model, cleaning, or inference of questionnaire answers is performed.
"""

import argparse
import csv
import hashlib
import math
import platform
import re
import statistics
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


KEYS = {
    "transactions.csv": [("transactionID",), ("customerID", "transactionID"),
                         ("customerID", "ISIN", "transactionID")],
    "asset_information.csv": [("ISIN",), ("ISIN", "timestamp")],
    "customer_information.csv": [("customerID",), ("customerID", "timestamp")],
    "close_prices.csv": [("ISIN", "timestamp")],
    "limit_prices.csv": [("ISIN",)],
    "markets.csv": [("marketID",), ("exchangeID",)],
}
NUMBERS = {"totalValue", "units", "closePrice", "priceMinDate", "priceMaxDate", "profitability"}
DATES = {"timestamp", "lastQuestionnaireDate", "minDate", "maxDate"}
MARKERS = {"not_available", "nan", "na", "n/a", "null", "none", "unknown"}
RQ = ("Does using LLM-generated transaction-history summaries improve nDCG@10 for "
      "predicting future asset purchases compared with structured-history features "
      "for FAR-Trans users with sparse histories?")


def digest(path):
    with path.open("rb") as stream:
        return stream_digest(stream)


def stream_digest(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(block)
    return h.hexdigest()


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", "<br>")
    return "\n".join(["| " + " | ".join(map(cell, headers)) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |"] +
                     ["| " + " | ".join(map(cell, row)) + " |" for row in rows]) + "\n\n"


def literal(value):
    return "`" + value + "`" if value else "`\"\"` (empty field)"


def percentile(values, p):
    """Linear interpolation at (n-1)*p/100, matching the usual type-7 quantile."""
    x = sorted(values)
    pos = (len(x) - 1) * p / 100
    lo, hi = math.floor(pos), math.ceil(pos)
    return x[lo] + (x[hi] - x[lo]) * (pos - lo)


def scan(path):
    """Strict CSV parse, exact row/key duplication, missingness and type checks."""
    keys = KEYS[path.name]
    keep = path.name in {"transactions.csv", "asset_information.csv", "customer_information.csv", "limit_prices.csv"}
    s = dict(n=0, malformed=[], blank_records=0, rows=[], positions={}, full_duplicates=0,
             blanks=Counter(), markers=Counter(), whitespace=Counter(), invalid_dates=Counter(),
             dates=defaultdict(Counter), numeric=defaultdict(Counter), unique=defaultdict(set),
             categories=defaultdict(Counter), keys={k: Counter() for k in keys}, endpoints={})
    seen = set()
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader)
        if len(header) != len(set(header)):
            raise ValueError(f"Duplicate column names: {path}")
        s["header"] = header
        previous_line = reader.line_num
        for record_no, row in enumerate(reader, 1):
            start = previous_line + 1
            previous_line = reader.line_num
            if not row:
                s["blank_records"] += 1
            if len(row) != len(header):
                s["malformed"].append((record_no, start, reader.line_num, len(row)))
                continue
            s["n"] += 1
            tup = tuple(row)
            s["full_duplicates"] += tup in seen
            seen.add(tup)
            d = dict(zip(header, row))
            if keep:
                s["rows"].append(d)
            if path.name == "transactions.csv" and d["transactionID"] == "7590224":
                s["positions"][record_no] = (start, reader.line_num, d)
            if path.name == "asset_information.csv":
                s["positions"][record_no] = (start, reader.line_num, d)
            for key in keys:
                s["keys"][key][tuple(d[c] for c in key)] += 1
            for col, value in d.items():
                s["blanks"][col] += value.strip() == ""
                if value.strip().lower() in MARKERS:
                    s["markers"][(col, value)] += 1
                s["whitespace"][col] += value != value.strip()
                if col in {"customerID", "ISIN", "marketID", "exchangeID", "transactionID"}:
                    s["unique"][col].add(value)
                if col in {"transactionType", "channel", "customerType", "riskLevel", "investmentCapacity", "assetCategory", "assetSubCategory"}:
                    s["categories"][col][value] += 1
                if col in DATES and value:
                    try:
                        date.fromisoformat(value)
                        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                            raise ValueError(value)
                        s["dates"][col][value] += 1
                    except ValueError:
                        s["invalid_dates"][col] += 1
                if col in NUMBERS:
                    try:
                        v = float(value)
                        if not math.isfinite(v):
                            s["numeric"][col]["nonfinite"] += 1
                        else:
                            s["numeric"][col]["negative"] += v < 0
                            s["numeric"][col]["zero"] += v == 0
                    except ValueError:
                        s["numeric"][col]["unparseable"] += 1
            if path.name == "close_prices.csv":
                isin, day, price = row
                if isin not in s["endpoints"]:
                    s["endpoints"][isin] = [day, day, price, price]
                ep = s["endpoints"][isin]
                if day < ep[0]:
                    ep[0], ep[2] = day, price
                if day > ep[1]:
                    ep[1], ep[3] = day, price
    return s


def intro(title):
    return (f"# {title}\n\nStudent: Abaidullah Seikh  \nCourse: LLM4Rec, HSE University  \n"
            "Scope: Homework 1, Session 1, Task 1 inspection notes only.\n\n"
            "**AI-assisted inspection by OpenCode (openai/gpt-6-astra). Personal verification by "
            "the student is pending.** These files are not the final homework report.\n\n")


def raw_lines(path, start, end):
    with path.open(encoding="utf-8", newline="") as stream:
        return "".join(line for number, line in enumerate(stream, 1) if start <= number <= end).rstrip("\r\n")


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=root / "FAR-Trans")
    parser.add_argument("--output-dir", type=Path, default=root / "results")
    parser.add_argument("--archive", type=Path, default=root / "FAR-Trans.zip")
    args = parser.parse_args()
    data, out = args.data_dir.resolve(), args.output_dir.resolve()
    if out == data or data in out.parents:
        parser.error("Output must be outside the raw dataset directory")
    files = sorted(p for p in data.rglob("*") if p.is_file())
    before = {p.relative_to(data).as_posix(): digest(p) for p in files}
    archive_checks = {}
    archive_sha = None
    if args.archive.is_file():
        archive_sha = digest(args.archive)
        with zipfile.ZipFile(args.archive) as archive:
            for name, sha in before.items():
                candidates = [n for n in archive.namelist() if n == name or n.endswith("/" + name)]
                if len(candidates) != 1:
                    raise ValueError(f"Expected one archive member for {name}: {candidates}")
                with archive.open(candidates[0]) as stream:
                    archive_checks[name] = stream_digest(stream) == sha
        if not all(archive_checks.values()):
            raise ValueError("Local raw files differ from the supplied archive")
    stats = {}
    for name in KEYS:
        print(f"Inspecting {name} ...", flush=True)
        stats[name] = scan(data / name)
        if stats[name]["malformed"]:
            raise ValueError(f"Malformed CSV records in {name}: {stats[name]['malformed'][:5]}")
    tx, asset, cust, prices, limits, markets = (stats[n] for n in KEYS)
    types = tx["categories"]["transactionType"]
    totals = Counter(r["customerID"] for r in tx["rows"])
    buys = Counter(r["customerID"] for r in tx["rows"] if r["transactionType"] == "Buy")
    sells = Counter(r["customerID"] for r in tx["rows"] if r["transactionType"] == "Sell")
    users = sorted(totals)
    buy_counts = [buys[u] for u in users]
    buyer_counts = [v for v in buy_counts if v > 0]
    assert sum(totals.values()) == tx["n"]
    assert sum(buy_counts) == types["Buy"]
    assert sum(sells.values()) == types["Sell"]
    assert sum(types.values()) == tx["n"]
    qtext = (data / "questionnaires.csv").read_text(encoding="utf-8")
    questions = len(re.findall(r"^\s*\d+\. ", qtext, re.MULTILINE))
    sections = [s for s in qtext.splitlines() if s and not s[0].isspace()]

    inv = intro("Dataset inventory") + f"## Individual research question\n\n{RQ}\n\n"
    inv += ("## Sources read and scope\n\n"
            "- `FAR-Trans/README.txt`: file meanings, UTF-8 CSV conventions, CC-BY 4.0 license.\n"
            "- `session1_research_question_instructions (2).md`, v1.2: §2 fixes Top-10/nDCG@10 "
            "against future purchases but leaves the exact split, item scope and eligibility pending; "
            "§4 example A requires the same candidates, item information and downstream ranker; "
            "§6 requires personal checking of a raw record; §14 requires an authentic session export.\n"
            "- `LLM4Recsys 07. LLM-Based Recommendation and FAR-Trans Project.pdf`, pp. 12–16 "
            "(data, past-only inputs, shared benchmark), p. 18 (Session 1 milestone). "
            "The Top-5 diagram on p. 15 is illustrative; the shared output is Top-10.\n"
            "- These are locally supplied sources. No external paper or web source was independently opened.\n\n")
    inv += "## All files in the supplied dataset directory\n\n"
    rows = []
    for p in files:
        name = p.relative_to(data).as_posix()
        if name in stats:
            count, kind = f"{stats[name]['n']:,}", "CSV data records, header excluded"
        elif name == "questionnaires.csv":
            count, kind = f"N/A; {questions} questions, {len(sections)} sections", "Plain text, not a rectangular CSV; no customer answers"
        else:
            count, kind = "N/A", "Documentation text"
        rows.append((name, count, kind, f"{p.stat().st_size:,}"))
    inv += table(["File", "Record count", "Format/count definition", "Bytes"], rows)
    inv += "The supplied `FAR-Trans.zip` is the container archive, not an additional table.\n\n"
    for name, s in stats.items():
        inv += f"### `{name}`: exact ordered CSV column names\n\n```text\n{','.join(s['header'])}\n```\n\n"
    inv += "## Customers, assets and transactions\n\n"
    inv += table(["Measure", "Observed value"], [
        ("Transaction data records (excluding header)", f"{tx['n']:,}"),
        ("Distinct customerID in transactions", f"{len(users):,}"),
        ("Distinct customerID in customer_information", f"{len(cust['unique']['customerID']):,}"),
        ("Distinct traded ISIN (Buy or Sell)", f"{len(tx['unique']['ISIN']):,}"),
        ("Distinct purchased ISIN", f"{len({r['ISIN'] for r in tx['rows'] if r['transactionType'] == 'Buy'}):,}"),
        ("Distinct ISIN in asset_information", f"{len(asset['unique']['ISIN']):,}"),
        ("Distinct ISIN in close_prices", f"{len(prices['unique']['ISIN']):,}"),
        ("Distinct ISIN in limit_prices", f"{len(limits['unique']['ISIN']):,}"),
        *[(f"transactionType = {k}", f"{v:,}") for k, v in sorted(types.items())],
        ("Observed transaction date range (inclusive)", f"{min(tx['dates']['timestamp'])} to {max(tx['dates']['timestamp'])}"),
    ])
    inv += (f"The presentation p. 12 displays 388,049 transaction rows. Direct CSV parsing gives "
            f"**{tx['n']:,} data records**; including the single header gives {tx['n'] + 1:,} "
            "CSV records. Report the parsed data count, rather than copying the slide count. "
            "The slide also says the dataset includes reconstructed transactions; the raw schema "
            "has no explicit reconstruction/provenance flag, so this inspection does not identify "
            "individual rows as reconstructed.\n\n")
    inv += "## Fields relevant to RQ1\n\n" + table(["Source and exact fields", "Use and provenance"], [
        ("transactions: customerID, ISIN, timestamp, transactionType", "Released transaction records: user/item links, chronological histories, Buy labels in a future window once specified."),
        ("transactions: totalValue, units, channel, marketID", "Recorded context for summaries and matching structured aggregates; pre-cutoff only, with value/units quality checks."),
        ("transactions: transactionID", "Audit and duplicate checks; not a preference feature."),
        ("asset_information: assetName, assetShortName, assetCategory, assetSubCategory, sector, industry, marketID, timestamp", "Recorded descriptive metadata, including missing fields; join by ISIN with as-of timing. Both methods receive identical allowed metadata."),
        ("customer_information: customerType, riskLevel, investmentCapacity, lastQuestionnaireDate, timestamp", "Optional recorded profile snapshots; risk/capacity may be predicted or missing. Timing must be resolved before use; not required for a history-only comparison."),
        ("close_prices: ISIN, timestamp, closePrice", "Optional price context, only actually available past closes; not needed for the primary RQ."),
        ("limit_prices: minDate, maxDate, priceMinDate, priceMaxDate, profitability", "Full-series summaries; unsafe as historical features without recomputation from permitted past data."),
        ("markets: marketID, exchangeID, name, description, country, tradingDays, tradingHours, marketClass", "Optional market context; no version timestamp, historical availability is unproven."),
        ("questionnaires.csv", "Question wording and possible choices only; no observed customer answers. Do not generate demographic/profile answers."),
    ])
    inv += ("## Reproduction and integrity\n\n```bash\npython3 scripts/inspect_far_trans.py\n```\n\n"
            f"Runtime used for this generation: Python {platform.python_version()}; standard library only. "
            "The script reads raw inputs only, computes exact-string counts, and regenerates all four Markdown files. "
            "Date checks use ISO dates; quantiles use linear interpolation at `(n-1)*p/100`. "
            "All raw file SHA-256 values are checked again after inspection.\n\n")
    if archive_sha:
        inv += f"Supplied archive SHA-256: `{archive_sha}`. All {len(archive_checks)} dataset files match their archive members byte-for-byte. This establishes local archive consistency, not external download provenance.\n\n"
    else:
        inv += "Archive not found at the supplied path; local archive comparison was not performed.\n\n"
    inv += table(["Raw file", "SHA-256"], [(n, f"`{h}`") for n, h in before.items()])
    inv += ("The OpenCode conversation is the authentic AI work history. These generated notes are not a session "
            "export. No session log is rewritten or synthesized by this script. Preserve the native session and "
            "use OpenCode's native export for the eventual homework submission; a native export has not been created here.\n")

    verified = intro("AI-assisted verification of transaction 7590224")
    verified += f"Exact transactionID matches in `FAR-Trans/transactions.csv`: **{len(tx['positions'])}**.\n\n"
    for record_no, (start, end, r) in tx["positions"].items():
        verified += (f"## Original transaction\n\n- Original filename: `FAR-Trans/transactions.csv`.\n"
                     f"- One-based data-record index (header excluded): **{record_no}**.\n"
                     f"- One-based CSV record number (header included): **{record_no + 1}**.\n"
                     f"- Physical line(s), header at line 1: **{start}–{end}**.\n"
                     f"- Timestamp: `{r['timestamp']}` (date only; no time of day or timezone supplied).\n"
                     f"- Customer identifier: `{r['customerID']}` (released anonymized identifier).\n"
                     f"- Asset ISIN: `{r['ISIN']}`.\n"
                     "- Window/split: **unassigned; official cutoff/window and eligibility are pending**.\n\n")
        verified += table(["Exact column name (original order)", "Verbatim parsed field value"], [(c, literal(r[c])) for c in tx["header"]])
        verified += f"Original header and original raw record (CSV quoting preserved):\n\n```csv\n{raw_lines(data / 'transactions.csv', 1, 1)}\n{raw_lines(data / 'transactions.csv', start, end)}\n```\n\n"
        matches = [(n, a, b, d) for n, (a, b, d) in asset["positions"].items() if d["ISIN"] == r["ISIN"]]
        verified += f"## Matching asset metadata\n\nExact join: `asset_information.ISIN == transactions.ISIN`. Matching records: **{len(matches)}**. Every match is listed; no arbitrary latest-row selection.\n\n"
        for n, a, b, d in matches:
            verified += f"Source: `FAR-Trans/asset_information.csv`; one-based data record **{n}**, CSV record including header **{n + 1}**, physical line(s) **{a}–{b}**.\n\n"
            verified += table(["Exact column name", "Verbatim parsed field value"], [(c, literal(d[c])) for c in asset["header"]])
            verified += f"```csv\n{raw_lines(data / 'asset_information.csv', 1, 1)}\n{raw_lines(data / 'asset_information.csv', a, b)}\n```\n\n"
            verified += f"Metadata timestamp `{d['timestamp']}` is {'later than' if d['timestamp'] > r['timestamp'] else 'not later than'} the transaction date `{r['timestamp']}`. This is a provenance comparison, not an official split assignment or proof of historical availability.\n\n"
        verified += "All displayed fields are recorded raw-release values, not LLM predictions. Empty fields, if any, are shown explicitly; no customer profile or inferred questionnaire answer is attached. The release does not supply a per-transaction reconstruction flag.\n\n"
    verified += ("## Personal verification still required\n\n"
                 "1. Personally open the original `FAR-Trans/transactions.csv` in a text editor, without saving changes. "
                 "Read the header and search for the exact transactionID `7590224`; compare all nine fields and the location above.\n"
                 "2. Open the original `FAR-Trans/asset_information.csv`; search for the exact ISIN above. "
                 "Compare every matching row, including name, category, subcategory, sector, industry and timestamp.\n"
                 "3. Record your own verification date and what you actually checked separately. "
                 "Until then, describe this only as AI-assisted verification with personal checking pending.\n"
                 "4. Keep window/split unassigned until the instructor specifies the official protocol.\n")

    sparse = intro("Sparse-user analysis")
    sparse += ("## Counting definitions\n\nFull-release exploratory counts, **not pre-cutoff eligibility counts**. "
               "Each raw transaction row counts once, including repeated purchases of the same asset; "
               "these are event counts, not distinct-item counts. `total[u]`, `buy[u]`, and `sell[u]` "
               "are computed for every customer in transactions.csv by the script's Counters. "
               "Zero-Buy users are retained in the all-transaction-customer distribution.\n\n")
    sparse += table(["Population", "Users"], [
        ("Any transaction", f"{len(users):,}"), ("At least one Buy", f"{len(buyer_counts):,}"),
        ("No Buy among transaction customers", f"{len(users) - len(buyer_counts):,}"),
        ("Profile customers with no transaction", f"{len(cust['unique']['customerID'] - set(users)):,}"),
    ])
    distributions = {"All transactions per transaction customer": list(totals.values()),
                     "Buy events per transaction customer (zeros included)": buy_counts,
                     "Buy events per buyer (positive only)": buyer_counts,
                     "Sell events per transaction customer (zeros included)": [sells[u] for u in users]}
    sparse += "## Distribution\n\n" + table(["Population/count", "Min", "P10", "P25", "Median/P50", "P75", "P90", "P95", "P99", "Max", "Mean"], [
        [label] + [f"{percentile(v, p):,.2f}" for p in [0, 10, 25, 50, 75, 90, 95, 99, 100]] + [f"{statistics.mean(v):,.2f}"]
        for label, v in distributions.items()])
    sparse += "## Requested overlapping full-dataset Buy bands\n\n" + table(["Buy events (inclusive)", "Users", "% of all transaction customers", "% of buyers"], [
        (f"1–{k}", f"{sum(1 <= v <= k for v in buy_counts):,}", f"{100 * sum(1 <= v <= k for v in buy_counts) / len(users):.2f}%", f"{100 * sum(1 <= v <= k for v in buy_counts) / len(buyer_counts):.2f}%") for k in (3, 5, 10)])
    sparse += "## Non-overlapping Buy histogram\n\n" + table(["Buy events", "Users"], [
        (label, f"{sum(lo <= v <= hi for v in buy_counts):,}")
        for label, lo, hi in [("0", 0, 0), ("1", 1, 1), ("2–3", 2, 3), ("4–5", 4, 5), ("6–10", 6, 10), ("11–20", 11, 20), ("21–50", 21, 50), ("51–100", 51, 100), (">100", 101, max(buy_counts))]])
    sparse += ("## Provisional definition, not official\n\n"
               "Propose **1–5 Buy events strictly before the prediction cutoff** as an initial *purchase-sparse* "
               f"subgroup: the full-release median is {percentile(buy_counts, 50):g} Buy events, "
               f"P75 is {percentile(buy_counts, 75):g}, and the 1–5 band covers "
               f"{sum(1 <= v <= 5 for v in buy_counts):,} customers "
               f"({100 * sum(1 <= v <= 5 for v in buy_counts) / len(users):.2f}% of transaction customers). "
               "It provides a small, nonempty purchase history while leaving 1–3 and 1–10 as sensitivity bands. "
               "This is an exploratory threshold recommendation, not a discovered optimum or instructor rule.\n\n"
               "Because the RQ says transaction-history summaries, low Buy counts do not necessarily mean little "
               "total history: users can have many Sells. If summaries include both types, report total pre-cutoff "
               "events as well and consider a separately declared 1–5 total-event subgroup. Zero-Buy/zero-history "
               "users should be described separately rather than silently mixed into the proposed subgroup.\n\n")
    sparse_sell = [u for u in users if 1 <= buys[u] <= 5 and totals[u] > 10]
    sparse += f"Observed example of this distinction: **{len(sparse_sell):,}** customers with 1–5 full-release Buys have more than 10 total full-release transactions.\n\n"
    sparse += ("## Why these are not the official sparse-user population\n\n"
               "Full-release counts include transactions after any earlier prediction cutoff. Using those counts "
               "to select sparse users would condition selection on future activity. A customer with many "
               "full-release purchases may have only a few at the cutoff, while a full-release buyer may have "
               "zero purchases at that time. Item restrictions, history-window length, label definitions and "
               "evaluated-user eligibility remain pending (§2 of the supplied instructions). Future-purchase "
               "availability must be handled by that protocol, not silently assumed here.\n\n"
               "Once announced: select permitted historical transactions using the official boundary and item "
               "scope, recompute counts, freeze subgroup membership from past data only, then apply the shared "
               "evaluation eligibility. The proposed strict `< cutoff` convention must be reconciled with the "
               "official day-boundary rule. Dates have no intraday ordering. Both comparison arms must receive "
               "the same permitted history, metadata, candidates and ranker. No nDCG or model result is claimed.\n")

    quality = intro("Data-quality analysis and leakage risks")
    quality += ("## Check definitions\n\nCounts are computed on original string cells. Blank means empty or "
                "whitespace-only. Marker checks are case-insensitive exact matches after trimming for "
                "`Not_Available`, `nan`, `NA`, `N/A`, `null`, `None`, `unknown`; markers are reported separately "
                "from blank cells. No automatic NA conversion or imputation occurs. Duplicate counts mean "
                "extra records beyond the first, with repeated-key groups also reported. Repeated customer/asset "
                "identifiers may be legitimate snapshots, not necessarily errors.\n\n")
    quality += "## File-level checks\n\n" + table(["File", "Malformed-width records", "Blank records", "Exact duplicate rows (extra)", "Surrounding-whitespace cells"], [
        (n, len(s["malformed"]), s["blank_records"], s["full_duplicates"], sum(s["whitespace"].values())) for n, s in stats.items()])
    quality += "## Missing values: every CSV column\n\n" + table(["File", "Exact column", "Blank cells", "Marker cells"], [
        (n, c, s["blanks"][c], sum(v for (col, _), v in s["markers"].items() if col == c)) for n, s in stats.items() for c in s["header"]])
    quality += "### Literal missing-marker values\n\n" + table(["File", "Column", "Literal value", "Rows"], [
        (n, c, literal(v), k) for n, s in stats.items() for (c, v), k in sorted(s["markers"].items())])
    quality += "## Identifier and composite-key duplication\n\n" + table(["File", "Key", "Distinct keys", "Repeated-key groups", "Extra rows on key"], [
        (n, ", ".join(key), len(counts), sum(v > 1 for v in counts.values()), sum(v - 1 for v in counts.values()))
        for n, s in stats.items() for key, counts in s["keys"].items()])
    quality += "`exchangeID` may cover several markets; it is not assumed to be a unique market key. Same-identifier snapshots require timestamp-aware joins; same-identifier/same-date conflicts require explicit tie resolution.\n\n"
    repeated_ids = {key[0] for key, count in tx["keys"][("transactionID",)].items() if count > 1}
    examples = sorted(repeated_ids)[:5]
    duplicate_groups = defaultdict(list)
    for r in tx["rows"]:
        if r["transactionID"] in examples:
            duplicate_groups[r["transactionID"]].append(r)
    quality += "### Repeated transactionID examples\n\n" + table(
        ["transactionID (first five lexically sorted)", "Rows", "Distinct customers", "Distinct ISINs", "Fields that differ within group"],
        [(key, len(duplicate_groups[key]), len({r['customerID'] for r in duplicate_groups[key]}),
          len({r['ISIN'] for r in duplicate_groups[key]}),
          ", ".join(c for c in tx["header"] if len({r[c] for r in duplicate_groups[key]}) > 1))
         for key in examples])
    quality += ("A repeated transactionID alone is not evidence of a duplicated event. The composite-key "
                "counts above test additional context; preserve original record indices for audit and do not "
                "drop rows using transactionID alone. The release does not explain each identifier collision.\n\n")
    conflicting_asset_keys = {key for key, count in asset["keys"][("ISIN", "timestamp")].items() if count > 1}
    quality += "### Asset records sharing an ISIN and timestamp\n\n" + table(
        asset["header"], [[literal(r[c]) for c in asset["header"]] for r in asset["rows"]
                          if (r["ISIN"], r["timestamp"]) in conflicting_asset_keys])
    relations = [
        ("Transaction customers absent from customer_information", tx["unique"]["customerID"] - cust["unique"]["customerID"]),
        ("Profile customers absent from transactions", cust["unique"]["customerID"] - tx["unique"]["customerID"]),
        ("Traded ISIN absent from asset_information", tx["unique"]["ISIN"] - asset["unique"]["ISIN"]),
        ("Metadata ISIN never traded", asset["unique"]["ISIN"] - tx["unique"]["ISIN"]),
        ("Traded ISIN absent from close_prices", tx["unique"]["ISIN"] - prices["unique"]["ISIN"]),
        ("Transaction marketID absent from markets", tx["unique"]["marketID"] - markets["unique"]["marketID"]),
        ("Asset marketID absent from markets", asset["unique"]["marketID"] - markets["unique"]["marketID"]),
        ("close_prices ISIN absent from asset_information", prices["unique"]["ISIN"] - asset["unique"]["ISIN"]),
        ("limit_prices ISIN absent from close_prices", limits["unique"]["ISIN"] - prices["unique"]["ISIN"]),
    ]
    quality += "## Cross-file identifier coverage\n\n" + table(["Check", "Distinct unmatched identifiers", "First 10 sorted examples"], [
        (label, len(values), ", ".join(literal(v) for v in sorted(values)[:10]) or "—") for label, values in relations])
    isin_pattern = re.compile(r"[A-Z]{2}[A-Z0-9]{9}[0-9]\Z")
    quality += "### ISIN shape screening\n\n" + table(["File", "Distinct identifiers not matching standard 12-character shape", "First 10 examples"], [
        (n, len(bad), ", ".join(sorted(bad)[:10]) or "—") for n, s in stats.items() if "ISIN" in s["header"]
        for bad in [{v for v in s["unique"]["ISIN"] if not isin_pattern.fullmatch(v)}]])
    quality += "This is only a syntactic screen, not check-digit validation or proof that a security is invalid. Preserve original identifiers; do not guess corrections or merge similar strings.\n\n"
    quality += "## Dates and numeric checks\n\n" + table(["File", "Date column", "Minimum valid date", "Maximum valid date", "Invalid nonblank dates"], [
        (n, c, min(s["dates"][c], default="—"), max(s["dates"][c], default="—"), s["invalid_dates"][c])
        for n, s in stats.items() for c in s["header"] if c in DATES])
    quality += table(["File", "Numeric field", "Unparseable", "Nonfinite", "Negative", "Zero"], [
        (n, c, v["unparseable"], v["nonfinite"], v["negative"], v["zero"]) for n, s in stats.items() for c, v in s["numeric"].items()])
    quality += "Negative profitability can be a valid loss; zero/negative trade values or prices are flags for investigation, not automatic grounds to delete raw rows.\n\n"
    quality += "## Exact observed category values\n\n" + table(["File", "Column", "Value", "Rows"], [
        (n, c, literal(value), count) for n, s in stats.items() for c, counts in s["categories"].items() for value, count in sorted(counts.items())])
    future_q = [r for r in cust["rows"] if r["lastQuestionnaireDate"] and r["timestamp"] and r["lastQuestionnaireDate"] > r["timestamp"]]
    sentinel_q = sum(r["lastQuestionnaireDate"] == "2000-01-01" for r in cust["rows"])
    quality += "## Customer-profile provenance and timing\n\n"
    provenance = []
    for c in ["customerType", "riskLevel", "investmentCapacity", "lastQuestionnaireDate", "timestamp"]:
        counts = Counter("missing" if not r[c].strip() or r[c].strip().lower() in MARKERS else
                         "predicted/estimated (explicit Predicted_ prefix)" if r[c].startswith("Predicted_") else
                         "recorded, not explicitly marked predicted" for r in cust["rows"])
        provenance.extend((c, label, count) for label, count in sorted(counts.items()))
    quality += table(["Profile field", "Classification", "Rows"], provenance)
    quality += ("'Recorded, not explicitly marked predicted' is an observed release value, not independent "
                "confirmation of a customer's true state or an assurance of pre-cutoff availability. "
                "`lastQuestionnaireDate` describes the questionnaire, while `timestamp` is documented as "
                "last update. Preserve `Predicted_` flags; the release does not document the estimation model's "
                "training window or feature provenance. Raw investment-capacity spellings differ from examples "
                "in the README (e.g. underscore placement); use the observed category table above.\n\n")
    quality += (f"Observed questionnaire dates later than their own profile-row timestamp: **{len(future_q):,} rows**, "
                f"**{len({r['customerID'] for r in future_q}):,} distinct customers**. "
                f"`lastQuestionnaireDate == 2000-01-01` occurs in **{sentinel_q:,} rows**. "
                "The repeated 2000 date is a possible placeholder, not a confirmed missing-value code.\n\n")
    quality += "First five inconsistent rows in original file order:\n\n" + table(cust["header"], [[literal(r[c]) for c in cust["header"]] for r in future_q[:5]])
    asset_dates = defaultdict(list)
    for r in asset["rows"]:
        asset_dates[r["ISIN"]].append(r["timestamp"])
    no_prior_asset = sum(not any(d <= r["timestamp"] for d in asset_dates[r["ISIN"]]) for r in tx["rows"])
    tx_dates = tx["dates"]["timestamp"]
    quality += f"Transaction rows with no asset metadata row dated on/before their transaction date: **{no_prior_asset:,}**. This event-time diagnostic does not assign a prediction cutoff.\n\n"
    quality += "Most frequent transaction dates (possible concentration, not proof of reconstruction):\n\n" + table(["Date", "Transactions"], sorted(tx_dates.items(), key=lambda pair: (-pair[1], pair[0]))[:5])
    endpoint_errors = Counter()
    for r in limits["rows"]:
        ep = prices["endpoints"].get(r["ISIN"])
        if ep is None:
            endpoint_errors["ISIN missing in close_prices"] += 1
            continue
        for col, value in zip(["minDate", "maxDate", "priceMinDate", "priceMaxDate"], ep):
            equal = r[col] == value if col.endswith("Date") and col in {"minDate", "maxDate"} else math.isclose(float(r[col]), float(value), rel_tol=1e-9, abs_tol=1e-9)
            endpoint_errors[f"{col} mismatch"] += not equal
        if float(r["priceMinDate"]) != 0:
            expected = float(r["priceMaxDate"]) / float(r["priceMinDate"]) - 1
            endpoint_errors["profitability mismatch (relative/absolute tolerance 1e-9)"] += not math.isclose(float(r["profitability"]), expected, rel_tol=1e-9, abs_tol=1e-9)
        else:
            endpoint_errors["zero start price; ROI undefined"] += 1
        endpoint_errors["minDate after maxDate"] += r["minDate"] > r["maxDate"]
    quality += "## Price-summary consistency\n\n" + table(["Check against close-price endpoints / ROI formula", "Flagged rows"], sorted(endpoint_errors.items()))
    quality += "Endpoint consistency does not make full-series profitability safe for a historical prediction.\n\n"
    quality += "## Leakage: observed facts versus proposed safeguards\n\n" + table(["Risk", "Observed fact", "Proposed safeguard (not official protocol)"], [
        ("Post-cutoff transactions", f"Transactions span {min(tx_dates)} to {max(tx_dates)}. No official cutoff is supplied, so no post-cutoff count or train/test allocation can be asserted.", "When specified, isolate history before the cutoff and future Buy labels in the shared window. Filter before summaries, counts, vocabulary, popularity and preprocessing; never select sparse users from future counts."),
        ("Time-dependent asset metadata", f"Asset timestamps span {min(asset['dates']['timestamp'])} to {max(asset['dates']['timestamp'])}; repeated ISINs and composite-key checks are above.", "As-of join only metadata known by prediction time; do not backfill later versions. Resolve same-date conflicts and leave unavailable attributes missing. Last-update stamps alone do not prove archival availability."),
        ("Risk profiles and investment capacity", "Customer snapshots repeat; riskLevel and investmentCapacity contain explicitly Predicted_ values and missing markers.", "Prefer history-only inputs for the first comparison unless provenance is established. If included, use time-valid snapshots identically in both arms, retain observed/predicted/missing distinctions, and do not infer actual wealth or risk tolerance."),
        ("Predicted values", "The README says Predicted_ risk/capacity values are algorithmic; their training data and fit dates are not supplied.", "An apparently old row may still contain estimates based on later information. Exclude unverified estimates from the main historical comparison or justify provenance and test a declared ablation."),
        ("Questionnaire dates", f"{len(future_q):,} profile rows have lastQuestionnaireDate > timestamp; {sentinel_q:,} use 2000-01-01. questionnaires.csv contains no user answers.", "A timestamp-only join is insufficient. Require known questionnaire availability as well as snapshot availability; quarantine inconsistent/unknown cases pending clarification. Merely setting effective time to the later date is conservative but not proof of historical availability."),
        ("Future prices and full-period returns", f"Close prices extend to {max(prices['dates']['timestamp'])}. limit_prices contains maxDate, priceMaxDate and full-series profitability.", "Omit full-series price summaries from history features. If prices are used, build features from closes available before the decision; never use same-day close for an earlier intraday decision, future normalization or future returns."),
        ("Candidate availability and survivorship", "Full-release asset and price inventories span multiple years; markets.csv has no timestamp.", "Do not infer historical availability from eventual trading or series endpoints; apply the forthcoming shared universe and document residual survivorship/staleness."),
        ("LLM contamination and information asymmetry", "The homework names these risks; no LLM summaries or recommendations have been generated in this inspection.", "Later record model/version/knowledge cutoff, ground summaries in permitted inputs, avoid external future facts, and give the structured baseline the identical underlying information."),
    ])
    quality += "No cleaning is applied. These checks are screening diagnostics, not a certification of correctness or profitability. No recommendation model is trained and no split is invented.\n"

    after = {p.relative_to(data).as_posix(): digest(p) for p in files}
    if before != after:
        raise RuntimeError("Raw file hashes changed during inspection")
    # Generated artifacts live outside the raw tree; an existing raw file is never opened for writing.
    out.mkdir(parents=True, exist_ok=True)
    outputs = {"dataset_inventory.md": inv, "verified_transaction.md": verified,
               "sparse_user_analysis.md": sparse, "data_quality_analysis.md": quality}
    for name, text in outputs.items():
        target = out / name
        if target.is_symlink():
            raise ValueError(f"Refusing to overwrite a symlink: {target}")
        target.write_text(text, encoding="utf-8")
        print(f"Wrote {target}")
    print(f"Raw SHA-256 unchanged for {len(before)} files.")
    print(f"Transactions={tx['n']:,}; customers={len(users):,}; traded assets={len(tx['unique']['ISIN']):,}; types={dict(types)}")


if __name__ == "__main__":
    main()
