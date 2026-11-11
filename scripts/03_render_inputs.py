import csv
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "FAR-Trans"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

CUTOFF = pd.Timestamp("2022-05-31")

# Identify customer from record_example.txt
record_text = (RESULTS / "record_example.txt").read_text(encoding="utf-8")
import re
m = re.search(r"customerID:\s*(\S+)", record_text)
if not m:
    raise SystemExit("customerID not found in record_example.txt")
cid = m.group(1)

# Load data
tx_raw = list(csv.DictReader((DATA / "transactions.csv").open(encoding="utf-8")))
ci_raw = list(csv.DictReader((DATA / "customer_information.csv").open(encoding="utf-8")))
ai_raw = list(csv.DictReader((DATA / "asset_information.csv").open(encoding="utf-8")))

# Asset info lookup: latest row with timestamp <= cutoff, else latest
def asset_row(isin):
    rows = [r for r in ai_raw if r["ISIN"] == isin]
    if not rows:
        return None
    eligible = [r for r in rows if pd.Timestamp(r["timestamp"]) <= CUTOFF]
    pool = eligible if eligible else rows
    return max(pool, key=lambda r: pd.Timestamp(r["timestamp"]))

# Strict profile row (latest with timestamp<=cutoff and lastQuestionnaireDate<=cutoff)
prof_rows = [r for r in ci_raw if r["customerID"] == cid
             and pd.Timestamp(r["timestamp"]) <= CUTOFF
             and pd.Timestamp(r["lastQuestionnaireDate"]) <= CUTOFF]
if not prof_rows:
    raise SystemExit("no strict profile row")
prof = max(prof_rows, key=lambda r: pd.Timestamp(r["timestamp"]))

def classify_field(val):
    s = str(val)
    if s.startswith("Predicted_"):
        return "predicted"
    if s == "Not_Available":
        return "missing"
    return "observed"

# History transactions on/before cutoff for this customer
hist_tx = [r for r in tx_raw if r["customerID"] == cid and pd.Timestamp(r["timestamp"]) <= CUTOFF]
hist_tx.sort(key=lambda r: (r["timestamp"], r["transactionID"]))

# Build arm C text lines
c_lines = []
for r in hist_tx:
    a = asset_row(r["ISIN"])
    cat = a["assetCategory"] if a else "unknown"
    sub = a["assetSubCategory"] if a and a["assetSubCategory"] else "unknown"
    name = a["assetName"] if a else "unknown"
    sector = (a["sector"].strip() if a and a["sector"].strip() else "unknown")
    industry = (a["industry"].strip() if a and a["industry"].strip() else "unknown")
    c_lines.append(
        f"{r['timestamp']} | {r['transactionType']} | {cat} / {sub} | {r['ISIN']} | "
        f"sector: {sector} | industry: {industry} | value: {r['totalValue']} | units: {r['units']}"
    )

# Arm D: same text + profile block
profile_block = (
    "\n[PROFILE]\n"
    f"riskLevel: {prof['riskLevel']} ({classify_field(prof['riskLevel'])})\n"
    f"investmentCapacity: {prof['investmentCapacity']} ({classify_field(prof['investmentCapacity'])})\n"
    "[/PROFILE]\n"
)
d_text = "History as of 2022-05-31:\n" + "\n".join(c_lines) + ("\n" + profile_block if c_lines else profile_block)

# Arm A structured features
n = len(hist_tx)
n_buy = sum(1 for r in hist_tx if r["transactionType"] == "Buy")
n_sell = sum(1 for r in hist_tx if r["transactionType"] == "Sell")
cat_counts = Counter()
sector_counts = Counter()
industry_counts = Counter()
subcat_counts = Counter()
for r in hist_tx:
    a = asset_row(r["ISIN"])
    cat_counts[a["assetCategory"] if a else "unknown"] += 1
    subcat_counts[(a["assetSubCategory"].strip() if a and a["assetSubCategory"] and a["assetSubCategory"].strip() else "unknown")] += 1
    sector_counts[(a["sector"].strip() if a and a["sector"].strip() else "unknown")] += 1
    industry_counts[(a["industry"].strip() if a and a["industry"].strip() else "unknown")] += 1

def shares(counter, total):
    return {k: (v / total if total else 0.0) for k, v in counter.items()}

first_date = min((r["timestamp"] for r in hist_tx), default=None)
last_date = max((r["timestamp"] for r in hist_tx), default=None)
days_last_to_cutoff = (CUTOFF - pd.Timestamp(last_date)).days if last_date else None

held_isins = sorted(set(r["ISIN"] for r in hist_tx))
total_units = sum(float(r["units"]) for r in hist_tx)

arm_a = {
    "history_window": f"transactions with timestamp <= {CUTOFF.date()}",
    "n_transactions": n,
    "n_buy": n_buy,
    "n_sell": n_sell,
    "first_transaction_date": first_date,
    "last_transaction_date": last_date,
    "days_from_last_tx_to_cutoff": days_last_to_cutoff,
    "counts_by_category": dict(cat_counts),
    "shares_by_category": shares(cat_counts, n),
    "counts_by_subcategory": dict(subcat_counts),
    "counts_by_sector": dict(sector_counts),
    "shares_by_sector": shares(sector_counts, n),
    "counts_by_industry": dict(industry_counts),
    "shares_by_industry": shares(industry_counts, n),
    "held_assets": held_isins,
    "total_value": sum(float(r["totalValue"]) for r in hist_tx),
    "total_units": total_units,
}

arm_a_plus = json.loads(json.dumps(arm_a))
arm_a_plus["riskLevel"] = prof["riskLevel"]
arm_a_plus["riskLevel_status"] = classify_field(prof["riskLevel"])
arm_a_plus["investmentCapacity"] = prof["investmentCapacity"]
arm_a_plus["investmentCapacity_status"] = classify_field(prof["investmentCapacity"])

out = []
def w(s=""):
    out.append(s)

w("TEMPLATE LABEL: PROPOSAL, pending team agreement")
w(f"customer_index: {cid}")
w("")
w("=== Arm C input (transaction-only history text) ===")
w("History as of 2022-05-31:")
w("\n".join(c_lines) if c_lines else "(no history transactions)")
w("")
w("=== Arm D input (same text + profile block) ===")
w(d_text)
w("")
w("=== Arm A input (structured features, no profile) ===")
w(json.dumps(arm_a, indent=2, sort_keys=True, default=str))
w("")
w("=== Arm A+profile input (structured features + profile fields) ===")
w(json.dumps(arm_a_plus, indent=2, sort_keys=True, default=str))

text = "\n".join(out) + "\n"
(RESULTS / "arm_inputs_example.txt").write_text(text, encoding="utf-8")
print(text)