#!/usr/bin/env python3
"""Prepare a local sparse cohort using strictly pre-cutoff information only."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

from starter import latest_before, select_users, rows


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=root.parent / 'Session 1' / 'FAR-Trans')
    args = parser.parse_args()
    cutoff = '2021-06-01'

    assets = latest_before(args.data_dir / 'asset_information.csv', 'ISIN', cutoff)
    profiles = latest_before(args.data_dir / 'customer_information.csv', 'customerID', cutoff)
    priced = {row['ISIN'] for row in rows(args.data_dir / 'close_prices.csv')
              if row['timestamp'][:10] < cutoff and float(row['closePrice']) > 0}
    assets = {isin: asset for isin, asset in assets.items() if isin in priced}

    history = defaultdict(Counter)
    seen = set()
    for row in rows(args.data_dir / 'transactions.csv'):
        # Future rows are discarded before any deduplication, storage, or counts.
        if row['timestamp'][:10] >= cutoff:
            continue
        key = tuple(sorted(row.items()))
        if key in seen:
            continue
        seen.add(key)
        if int(row['transactionID']) < 0:
            continue
        if row['transactionType'] != 'Buy' or row['ISIN'] not in assets:
            continue
        history[row['customerID']][row['ISIN']] += 1

    warm = select_users(profiles, history, 'warm', 0, None)
    contexts = [json.loads(line) for line in
                (root / 'outputs' / 'baseline_200' / 'contexts.jsonl').read_text(
                    encoding='utf-8').splitlines() if line.strip()]
    order_pass = sum(index < len(warm) and index < len(contexts)
                     and warm[index] == contexts[index]['user_id'] for index in range(200))
    totals_pass = sum(sum(history[ctx['user_id']].values()) ==
                      sum(asset['buy_count'] for asset in ctx['history'])
                      for ctx in contexts[:200])
    print(f'Warm-order check: pass={order_pass} fail={200 - order_pass}')
    print(f'Buy-total check: pass={totals_pass} fail={200 - totals_pass}')
    if len(contexts) != 200 or order_pass != 200 or totals_pass != 200:
        return 1

    qualifying = [uid for uid in warm if 1 <= sum(history[uid].values()) <= 5]
    selected = qualifying[:120]
    print(f'Warm users: {len(warm)}')
    print(f'Qualifying users: {len(qualifying)}')
    print(f'Selected users: {len(selected)}')
    if len(selected) != 120:
        return 1
    output = root / 'cohorts' / 'sparse_window_users.txt'
    if output.exists():
        raise FileExistsError('Sparse cohort output already exists; refusing to overwrite')
    output.parent.mkdir(parents=True, exist_ok=True)
    content = ('\n'.join(selected) + '\n').encode('utf-8')
    output.write_bytes(content)
    print(f'Cohort SHA-256: {hashlib.sha256(content).hexdigest()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
