import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "FAR-Trans"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

CUTOFF = pd.Timestamp("2022-05-31")
FUTURE_START = pd.Timestamp("2022-06-01")
FUTURE_END = pd.Timestamp("2022-11-30")

out = []

def w(s=""):
    out.append(s)

# (a) rows, customers and assets per file
w("=== (a) rows, customers and assets per file ===")
files = {
    "customer_information.csv": DATA / "customer_information.csv",
    "transactions.csv": DATA / "transactions.csv",
    "asset_information.csv": DATA / "asset_information.csv",
    "markets.csv": DATA / "markets.csv",
    "close_prices.csv": DATA / "close_prices.csv",
    "limit_prices.csv": DATA / "limit_prices.csv",
}
for name, path in files.items():
    df = pd.read_csv(path)
    cust = df["customerID"].nunique() if "customerID" in df.columns else "NA"
    assets = df["ISIN"].nunique() if "ISIN" in df.columns else "NA"
    w(f"{name}: rows={len(df)}, customers={cust}, assets={assets}")

# Load transactions
tx = pd.read_csv(DATA / "transactions.csv")
tx["timestamp"] = pd.to_datetime(tx["timestamp"], errors="coerce")
cust_info = pd.read_csv(DATA / "customer_information.csv")
cust_info["timestamp"] = pd.to_datetime(cust_info["timestamp"], errors="coerce")
cust_info["lastQuestionnaireDate"] = pd.to_datetime(cust_info["lastQuestionnaireDate"], errors="coerce")
asset_info = pd.read_csv(DATA / "asset_information.csv")

# (b) per-customer transaction counts (all transactions)
w("")
w("=== (b) per-customer transaction counts (all transactions) ===")
counts = tx.groupby("customerID").size()
w(f"customers_with_transactions={counts.shape[0]}")
w(f"min={counts.min()}, max={counts.max()}, mean={counts.mean():.4f}, median={counts.median():.4f}")
w(f"sum={counts.sum()}")
for lo, hi, label in [(1,1,"1"),(2,2,"2"),(3,5,"3-5"),(6,20,"6-20"),(21,10**9,">20")]:
    n = int(((counts>=lo)&(counts<=hi)).sum())
    w(f"customers_with_{label}_transactions={n}")

# (c) users with >=1 future Buy, bucketed by history tx before cutoff
w("")
w("=== (c) future-Buy users by history-transaction bucket (UNOFFICIAL split) ===")
w(f"cutoff={CUTOFF.date()}, future_window={FUTURE_START.date()}..{FUTURE_END.date()}, label=Buy")
history_counts = tx[tx["timestamp"] <= CUTOFF].groupby("customerID").size()
future_buy_users = set(tx[(tx["timestamp"] >= FUTURE_START) & (tx["timestamp"] <= FUTURE_END) & (tx["transactionType"] == "Buy")]["customerID"].unique())
all_users = set(tx["customerID"].unique())
buckets = [(0,0,"0"),(1,2,"1-2"),(3,5,"3-5"),(6,20,"6-20"),(21,10**9,">20")]
for lo, hi, label in buckets:
    if lo == 0 and hi == 0:
        users = [u for u in all_users if history_counts.get(u, 0) == 0]
    else:
        users = [u for u in all_users if lo <= history_counts.get(u, 0) <= hi]
    n_users = len(users)
    n_future = sum(1 for u in users if u in future_buy_users)
    pct = (100.0 * n_future / n_users) if n_users else 0.0
    w(f"bucket_{label}: users={n_users}, with_future_Buy={n_future}, pct={pct:.2f}")

# (d) sector and industry missingness by assetCategory
w("")
w("=== (d) sector/industry missingness by assetCategory ===")
ai = asset_info.copy()
ai["sector_missing"] = ai["sector"].isna() | (ai["sector"].astype(str).str.strip() == "")
ai["industry_missing"] = ai["industry"].isna() | (ai["industry"].astype(str).str.strip() == "")
g = ai.groupby("assetCategory").agg(
    rows=("ISIN", "size"),
    sector_missing=("sector_missing", "sum"),
    industry_missing=("industry_missing", "sum"),
)
for cat, r in g.iterrows():
    sm = int(r["sector_missing"]); im = int(r["industry_missing"]); n = int(r["rows"])
    w(f"{cat}: rows={n}, sector_missing={sm} ({100.0*sm/n:.2f}%), industry_missing={im} ({100.0*im/n:.2f}%)")

# (e) customer_information checks
w("")
w("=== (e) customer_information checks ===")
ci = cust_info.copy()
rows_lqd_later = int((ci["lastQuestionnaireDate"] > ci["timestamp"]).sum())
w(f"rows_where_lastQuestionnaireDate_later_than_timestamp={rows_lqd_later}")
sub = ci[ci["timestamp"] <= CUTOFF]
rows_ts_le_cutoff_lqd_gt = int((sub["lastQuestionnaireDate"] > CUTOFF).sum())
w(f"rows_where_timestamp_le_cutoff_and_lastQuestionnaireDate_gt_cutoff={rows_ts_le_cutoff_lqd_gt}")
risk_pred = int(ci["riskLevel"].astype(str).str.startswith("Predicted_").sum())
cap_pred = int(ci["investmentCapacity"].astype(str).str.startswith("Predicted_").sum())
risk_share = 100.0 * risk_pred / len(ci)
cap_share = 100.0 * cap_pred / len(ci)
w(f"riskLevel_Predicted_rows={risk_pred}, share={risk_share:.2f}%")
w(f"investmentCapacity_Predicted_rows={cap_pred}, share={cap_share:.2f}%")
w(f"customer_information_rows_total={len(ci)}")

# (f) sparse bucket (1-5 history tx): profile on/before cutoff + distributions
w("")
w("=== (f) sparse bucket (1-5 history tx) profile on/before cutoff ===")
sparse_users = [u for u in all_users if 1 <= history_counts.get(u, 0) <= 5]
w(f"sparse_users={len(sparse_users)}")
prof = ci[ci["timestamp"] <= CUTOFF].copy()
prof = prof.sort_values("timestamp")
latest_prof = prof.drop_duplicates(subset=["customerID"], keep="last")
sparse_with_prof = [u for u in sparse_users if u in set(latest_prof["customerID"])]
w(f"sparse_users_with_profile_row_on_or_before_cutoff={len(sparse_with_prof)}")
w(f"sparse_users_without_profile_row_on_or_before_cutoff={len(sparse_users)-len(sparse_with_prof)}")
sp = latest_prof[latest_prof["customerID"].isin(sparse_users)]
w("riskLevel distribution (sparse, latest profile <= cutoff):")
for val, n in sp["riskLevel"].value_counts(dropna=False).items():
    w(f"  {val}={int(n)}")
w("investmentCapacity distribution (sparse, latest profile <= cutoff):")
for val, n in sp["investmentCapacity"].value_counts(dropna=False).items():
    w(f"  {val}={int(n)}")

text = "\n".join(out) + "\n"
(RESULTS / "profile.txt").write_text(text, encoding="utf-8")
print(text)
PY