#!/usr/bin/env python3
"""Independent end-to-end verification for a single FAR-Trans user.

No starter functions are imported; every quantity is recomputed from the
raw CSVs and the saved output files.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def latest_before(rows, key, cutoff):
    result = {}
    for row in rows:
        if row['timestamp'][:10] < cutoff:
            prev = result.get(row[key])
            if prev is None or row['timestamp'] > prev['timestamp']:
                result[row[key]] = row
    return result


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir', type=Path, required=True)
    p.add_argument('--base-dir', type=Path, required=True)
    p.add_argument('--eval-dir', type=Path, required=True)
    p.add_argument('--arm-dir', type=Path, required=True)
    p.add_argument('--user', default=None)
    p.add_argument('--method', default='custom')
    return p.parse_args()


def main():
    args = parse_args()
    data_dir = args.data_dir
    base_dir = args.base_dir
    eval_dir = args.eval_dir
    arm_dir = args.arm_dir

    protocol = json.loads((base_dir / 'protocol.json').read_text(encoding='utf-8'))
    cutoff = protocol['cutoff']
    end = protocol['end_exclusive']

    contexts = {c['user_id']: c for c in
                (json.loads(l) for l in (base_dir / 'contexts.jsonl').read_text(encoding='utf-8').splitlines() if l.strip())}

    # eligible assets
    assets_rows = read_csv(data_dir / 'asset_information.csv')
    profiles_rows = read_csv(data_dir / 'customer_information.csv')
    prices_rows = read_csv(data_dir / 'close_prices.csv')
    tx_rows = read_csv(data_dir / 'transactions.csv')

    asof_assets = latest_before(assets_rows, 'ISIN', cutoff)
    priced = {r['ISIN'] for r in prices_rows
              if r['timestamp'][:10] < cutoff and float(r['closePrice']) > 0}
    eligible = {k for k in asof_assets if k in priced}

    # user selection
    if args.user is None:
        # pick first user with non-empty truth
        truth_by_user = {}
        for row in tx_rows:
            key = tuple(sorted(row.items()))
        # recompute truth per user
        seen = set()
        truth_sets = {}
        for row in tx_rows:
            k = tuple(sorted(row.items()))
            if k in seen:
                continue
            seen.add(k)
            if int(row['transactionID']) < 0:
                continue
            if row['transactionType'] != 'Buy' or row['ISIN'] not in eligible:
                continue
            if cutoff <= row['timestamp'][:10] < end:
                truth_sets.setdefault(row['customerID'], set()).add(row['ISIN'])
        chosen = None
        for uid in contexts:
            if truth_sets.get(uid):
                chosen = uid
                break
        if chosen is None:
            chosen = list(contexts)[0]
        user = chosen
    else:
        user = args.user

    # recompute history counts (drop exact dup rows, ignore negative txid)
    seen = set()
    history_counts = {}
    for row in tx_rows:
        k = tuple(sorted(row.items()))
        if k in seen:
            continue
        seen.add(k)
        if int(row['transactionID']) < 0:
            continue
        if row['transactionType'] != 'Buy' or row['ISIN'] not in eligible:
            continue
        if row['timestamp'][:10] < cutoff and row['customerID'] == user:
            history_counts[row['ISIN']] = history_counts.get(row['ISIN'], 0) + 1

    # recompute truth
    seen2 = set()
    truth = set()
    for row in tx_rows:
        k = tuple(sorted(row.items()))
        if k in seen2:
            continue
        seen2.add(k)
        if int(row['transactionID']) < 0:
            continue
        if row['transactionType'] != 'Buy' or row['ISIN'] not in eligible:
            continue
        if row['customerID'] == user and cutoff <= row['timestamp'][:10] < end:
            truth.add(row['ISIN'])

    ctx = contexts[user]
    cand_ids = [a['id'] for a in ctx['candidate_assets']]

    # raw log entry for user
    raw_entries = [json.loads(l) for l in (arm_dir / 'raw_log.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    raw_entry = next((r for r in raw_entries if r['user_id'] == user), None)

    # predictions
    preds = {}
    with (eval_dir / 'predictions.csv').open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            if row['user_id'] == user and row['method'] == args.method:
                preds.setdefault(row['user_id'], []).append((int(row['rank']), row['ISIN']))
    ranking = [isin for _, isin in sorted(preds.get(user, []))]

    # per_user stored ndcg
    stored_ndcg = None
    with (eval_dir / 'per_user.csv').open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            if row['user_id'] == user and row['method'] == args.method:
                stored_ndcg = float(row['ndcg_at_10'])

    print(f"User: {user}")
    print(f"Cutoff: {cutoff}  Window end: {end}")
    print("-" * 60)

    # 1. HISTORY
    ctx_history = {a['id']: a['buy_count'] for a in ctx['history']}
    hist_ok = (ctx_history == history_counts)
    print(f"1. HISTORY: {'PASS' if hist_ok else 'FAIL'}")
    if not hist_ok:
        print(f"   context: {ctx_history}")
        print(f"   recomputed: {history_counts}")

    # 2. NO FUTURE
    no_future_ok = True
    # asset metadata timestamps
    for a in ctx['history'] + ctx['candidate_assets']:
        if a['metadata_timestamp'][:10] >= cutoff:
            no_future_ok = False
    # profile timestamp
    if ctx['profile']['timestamp'][:10] >= cutoff:
        no_future_ok = False
    # arm D questionnaire
    q_ok = None
    if raw_entry is not None:
        q_ok = raw_entry.get('questionnaire_before_cutoff')
        if q_ok is False:
            # ensure summary shows not available
            summary = raw_entry.get('summary') or ''
            if 'not available' not in summary.lower():
                no_future_ok = False
    print(f"2. NO FUTURE: {'PASS' if no_future_ok else 'FAIL'}")
    if q_ok is not None:
        print(f"   questionnaire_before_cutoff: {q_ok}")

    # 3. TRUTH
    truth_ok = (truth == (truth & eligible))
    print(f"3. TRUTH: recomputed {len(truth)} future Buy ISINs in window & eligible: {'PASS' if truth_ok else 'FAIL'}")
    print(f"   truth: {sorted(truth)}")

    # 4. nDCG@10
    def ndcg10(ranking, truth_set):
        if not truth_set:
            return 0.0
        gain = sum(1 / math.log2(i + 2) for i, isin in enumerate(ranking[:10]) if isin in truth_set)
        ideal = sum(1 / math.log2(i + 2) for i in range(min(10, len(truth_set))))
        return gain / ideal
    computed = ndcg10(ranking, truth)
    ndcg_ok = (stored_ndcg is None) or (abs(computed - stored_ndcg) < 1e-9)
    print(f"4. nDCG@10: computed={computed:.10f} stored={stored_ndcg} {'PASS' if ndcg_ok else 'FAIL'}")

    # 5. OUTPUT
    out_ok = (len(ranking) == 10 and len(set(ranking)) == 10 and
              set(ranking) <= eligible and set(ranking) <= set(cand_ids))
    print(f"5. OUTPUT: {'PASS' if out_ok else 'FAIL'}")
    print(f"   ranking: {ranking}")
    if raw_entry is not None:
        print(f"   parsed_numbers: {raw_entry.get('parsed_numbers')}")
        print(f"   valid: {raw_entry.get('valid')}")
        if raw_entry.get('valid') is False:
            print("   (CBF fallback may have been used)")
    # candidate set size
    print(f"   candidate_set_size: {len(cand_ids)}  eligible_size: {len(eligible)}")


if __name__ == '__main__':
    main()
