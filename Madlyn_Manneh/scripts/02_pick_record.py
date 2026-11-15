import csv
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "FAR-Trans"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

CUTOFF = pd.Timestamp("2022-05-31")
FUTURE_START = pd.Timestamp("2022-06-01")
FUTURE_END = pd.Timestamp("2022-11-30")

# Read raw lines for verbatim output
def raw_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

tx_path = DATA / "transactions.csv"
ci_path = DATA / "customer_information.csv"
ai_path = DATA / "asset_information.csv"

tx_raw = raw_lines(tx_path)
ci_raw = raw_lines(ci_path)
ai_raw = raw_lines(ai_path)

tx_header = tx_raw[0]
ci_header = ci_raw[0]
ai_header = ai_raw[0]

# Parse transactions
tx_rows = list(csv.DictReader(tx_raw))
# index by file line number (header is line 1)
tx_line_no = {i: i + 2 for i in range(len(tx_rows))}  # not used; compute directly

# Build per-customer Buy counts
from collections import defaultdict
hist_buy = defaultdict(int)
future_buy = defaultdict(int)
cust_tx_indices = defaultdict(list)
for idx, row in enumerate(tx_rows):
    cid = row["customerID"]
    ts = pd.Timestamp(row["timestamp"])
    cust_tx_indices[cid].append(idx)
    if row["transactionType"] == "Buy":
        if ts <= CUTOFF:
            hist_buy[cid] += 1
        elif FUTURE_START <= ts <= FUTURE_END:
            future_buy[cid] += 1

# Profile rows
ci_rows = list(csv.DictReader(ci_raw))
# strict rule: timestamp <= cutoff AND lastQuestionnaireDate <= cutoff
strict_profile_users = set()
for row in ci_rows:
    ts = pd.Timestamp(row["timestamp"])
    lqd = pd.Timestamp(row["lastQuestionnaireDate"])
    if ts <= CUTOFF and lqd <= CUTOFF:
        strict_profile_users.add(row["customerID"])

# Pick customer
candidates = []
for cid in cust_tx_indices:
    if 1 <= hist_buy[cid] <= 5 and future_buy[cid] >= 1 and cid in strict_profile_users:
        candidates.append(cid)
candidates.sort()
if not candidates:
    raise SystemExit("No qualifying customer found")
cid = candidates[0]

# Latest profile row with timestamp <= cutoff (strict)
ci_indices_for_cust = [i for i, r in enumerate(ci_rows) if r["customerID"] == cid and pd.Timestamp(r["timestamp"]) <= CUTOFF and pd.Timestamp(r["lastQuestionnaireDate"]) <= CUTOFF]
ci_idx = max(ci_indices_for_cust, key=lambda i: pd.Timestamp(ci_rows[i]["timestamp"]))
ci_line_no = ci_idx + 2  # 1-based file line

# Matching assets
isins = sorted(set(r["ISIN"] for r in tx_rows if r["customerID"] == cid))
ai_indices = []
for isin in isins:
    for i, r in enumerate(ai_raw[1:], start=2):
        # parse roughly by csv
        pass
# parse asset rows properly
ai_parsed = list(csv.DictReader(ai_raw))
ai_match_indices = [i for i, r in enumerate(ai_parsed) if r["ISIN"] in isins]

out = []
def w(s=""):
    out.append(s)

w("=== Selected customer ===")
w(f"customerID: {cid}")
w(f"history_Buy_count (<=cutoff): {hist_buy[cid]}")
w(f"future_Buy_count (window): {future_buy[cid]}")
w("")

w("=== transactions.csv (verbatim lines) ===")
w(f"file: data/FAR-Trans/transactions.csv")
w(f"header (line 1): {tx_header}")
w("fields: " + ", ".join(tx_header.split(",")))
for idx, row in enumerate(tx_rows):
    if row["customerID"] == cid:
        ln = idx + 2
        w(f"line {ln}: {tx_raw[ln-1]}")
        w(f"  raw values: {tx_raw[ln-1]}")
w("")

w("=== customer_information.csv (latest profile row, strict rule) ===")
w(f"file: data/FAR-Trans/customer_information.csv")
w(f"header (line 1): {ci_header}")
ci_row = ci_rows[ci_idx]
w(f"line {ci_line_no}: {ci_raw[ci_line_no-1]}")
w(f"raw values: {ci_raw[ci_line_no-1]}")
w(f"profile timestamp: {ci_row['timestamp']}")
w(f"lastQuestionnaireDate: {ci_row['lastQuestionnaireDate']}")
w("")
w("Profile field classification (timestamp of profile row = %s):" % ci_row["timestamp"])
for field in ["customerID", "customerType", "riskLevel", "investmentCapacity", "lastQuestionnaireDate", "timestamp"]:
    val = ci_row[field]
    if field in ("riskLevel", "investmentCapacity"):
        if str(val).startswith("Predicted_"):
            cls = "predicted/estimated"
        elif str(val) == "Not_Available":
            cls = "missing"
        else:
            cls = "observed"
    elif field == "lastQuestionnaireDate":
        cls = "observed" if pd.Timestamp(val) != pd.Timestamp("2000-01-01") else "missing/placeholder"
    else:
        cls = "observed"
    after = ""
    if field in ("lastQuestionnaireDate",) and pd.Timestamp(val) > CUTOFF:
        after = "  [DATED AFTER CUTOFF]"
    if field == "timestamp" and pd.Timestamp(val) > CUTOFF:
        after = "  [DATED AFTER CUTOFF]"
    w(f"  {field}: value={val!r}, class={cls}, timestamp={ci_row['timestamp']}{after}")
w("")

w("=== asset_information.csv (matching rows) ===")
w(f"file: data/FAR-Trans/asset_information.csv")
w(f"header (line 1): {ai_header}")
for isin in isins:
    w(f"-- ISIN {isin} --")
    for i, r in enumerate(ai_parsed):
        if r["ISIN"] == isin:
            # find line number in raw file
            # locate by matching raw line content
            pass
    # find raw line numbers by scanning
    for ln, raw in enumerate(ai_raw[1:], start=2):
        # parse the raw line via csv to get ISIN (first field)
        if raw.split(",")[0] == isin:
            w(f"line {ln}: {raw}")

text = "\n".join(out) + "\n"
(RESULTS / "record_example.txt").write_text(text, encoding="utf-8")
print(text)