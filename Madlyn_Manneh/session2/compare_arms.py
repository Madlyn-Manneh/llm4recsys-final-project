#!/usr/bin/env python3
"""Results table and paired C-vs-D comparison for RQ4 (read-only).

Reads only already-saved output files: starter metrics, per-user scores,
predictions, and llm_rerank.py logs. It never recomputes rankings or calls a
model.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

BASELINE_NAMES = {
    'popularity': 'Popularity',
    'cbf': 'CBF',
    'latest_buy': 'Latest buy',
    'latest_buy_or_sell': 'Latest buy or sell',
}

PROFILE_WORDS = ('risk', 'conservative', 'aggressive', 'balanced', 'moderate',
                 'capacity', 'profile', 'income', 'growth', 'investor',
                 'suitability', 'tolerance')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()]


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def per_user_map(path, method):
    return {row['user_id']: row for row in read_csv(path) if row['method'] == method}


def prediction_map(path, method):
    result = {}
    for row in read_csv(path):
        if row['method'] == method:
            result.setdefault(row['user_id'], []).append((int(row['rank']), row['ISIN']))
    return {uid: [isin for _, isin in sorted(rows)] for uid, rows in result.items()}


def fmt(value):
    return 'n/a' if value is None else f'{value:.4f}'


def method_row(label, aggregate, runtime, failed):
    return (f"| {label} | {aggregate.get('users', 'n/a')} | "
            f"{aggregate.get('nonempty_truth_users', 'n/a')} | "
            f"{fmt(aggregate.get('ndcg_at_10'))} | "
            f"{fmt(aggregate.get('ndcg_at_10_nonempty'))} | {runtime} | {failed} |")


def protocol_hash(directory):
    path = Path(directory) / 'protocol.json'
    if path.exists():
        return read_json(path).get('protocol_hash')
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-dir', type=Path, required=True)
    parser.add_argument('--arm-c-dir', type=Path, required=True)
    parser.add_argument('--eval-c-dir', type=Path, required=True)
    parser.add_argument('--arm-d-dir', type=Path, required=True)
    parser.add_argument('--eval-d-dir', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--baseline-runtime', default='not timed separately')
    args = parser.parse_args()

    base_metrics = read_json(args.base_dir / 'metrics.json')
    c_metrics = read_json(args.eval_c_dir / 'metrics.json')
    d_metrics = read_json(args.eval_d_dir / 'metrics.json')
    c_meta = read_json(args.arm_c_dir / 'run_meta.json')
    d_meta = read_json(args.arm_d_dir / 'run_meta.json')

    base_hash = protocol_hash(args.base_dir) or base_metrics.get('protocol_hash')
    c_hash = protocol_hash(args.eval_c_dir) or c_meta.get('protocol_hash')
    d_hash = protocol_hash(args.eval_d_dir) or d_meta.get('protocol_hash')
    hashes_match = (base_hash is not None and base_hash == c_hash == d_hash)

    c_users = per_user_map(args.eval_c_dir / 'per_user.csv', 'custom')
    d_users = per_user_map(args.eval_d_dir / 'per_user.csv', 'custom')
    cbf_users = per_user_map(args.base_dir / 'per_user.csv', 'cbf')
    c_pred = prediction_map(args.eval_c_dir / 'predictions.csv', 'custom')
    d_pred = prediction_map(args.eval_d_dir / 'predictions.csv', 'custom')

    users = [uid for uid in c_users if uid in d_users]

    def ndcg(store, uid):
        try:
            return float(store[uid]['ndcg_at_10'])
        except (KeyError, ValueError):
            return 0.0

    def relevant(uid):
        for store in (c_users, d_users, cbf_users):
            if uid in store:
                try:
                    return int(store[uid]['relevant_count'])
                except (KeyError, ValueError):
                    return 0
        return 0

    diffs = [ndcg(d_users, uid) - ndcg(c_users, uid) for uid in users]
    nonempty_users = [uid for uid in users if relevant(uid) > 0]
    diffs_nonempty = [ndcg(d_users, uid) - ndcg(c_users, uid) for uid in nonempty_users]

    def mean(values):
        return sum(values) / len(values) if values else None

    higher = sum(1 for d in diffs if d > 1e-12)
    lower = sum(1 for d in diffs if d < -1e-12)
    equal = len(diffs) - higher - lower

    identical_order = 0
    same_set_different_order = 0
    overlaps = []
    for uid in users:
        c_list = c_pred.get(uid, [])
        d_list = d_pred.get(uid, [])
        overlaps.append(len(set(c_list) & set(d_list)))
        if c_list and d_list and c_list == d_list:
            identical_order += 1
        elif c_list and d_list and set(c_list) == set(d_list):
            same_set_different_order += 1

    c_invalid = c_meta.get('invalid_outputs', 0)
    d_invalid = d_meta.get('invalid_outputs', 0)
    d_profile_unavailable = d_meta.get('arm_D_profile_unavailable_users')

    d_raw = {row['user_id']: row for row in read_jsonl(args.arm_d_dir / 'raw_log.jsonl')}
    keyword_counts = {word: 0 for word in PROFILE_WORDS}
    summaries = 0
    for row in d_raw.values():
        summary = (row.get('summary') or '').lower()
        if not summary:
            continue
        summaries += 1
        for word in PROFILE_WORDS:
            keyword_counts[word] += summary.count(word)
    keyword_total = sum(keyword_counts.values())

    lines = []
    lines.append('# RQ4 results: Arm C vs Arm D')
    lines.append('')
    lines.append('Teaching settings: cutoff **2021-06-01**, 30-day evaluation window, '
                 '**100 users** (starter defaults, not the final project protocol).')
    lines.append('')
    lines.append(f"Protocol hash identical across baseline, arm C and arm D: "
                 f"**{'yes' if hashes_match else 'no'}**")
    lines.append('')
    if not hashes_match:
        lines.append(f'- baseline: `{base_hash}`')
        lines.append(f'- arm C: `{c_hash}`')
        lines.append(f'- arm D: `{d_hash}`')
        lines.append('')
    lines.append('## Results table')
    lines.append('')
    lines.append('| Method | Users | Users with future purchases | nDCG@10 (all users) | '
                 'nDCG@10 (nonempty truth) | Runtime | Failed cases |')
    lines.append('|---|---:|---:|---:|---:|---:|---:|')
    for key, label in BASELINE_NAMES.items():
        aggregate = base_metrics.get('methods', {}).get(key, {})
        lines.append(method_row(label, aggregate, args.baseline_runtime, 0))
    c_runtime = f"{c_meta.get('wall_seconds_whole_arm', 'n/a')} s"
    d_runtime = f"{d_meta.get('wall_seconds_whole_arm', 'n/a')} s"
    lines.append(method_row('Arm C', c_metrics.get('methods', {}).get('custom', {}),
                            c_runtime, c_invalid))
    lines.append(method_row('Arm D', d_metrics.get('methods', {}).get('custom', {}),
                            d_runtime, d_invalid))
    lines.append('')
    lines.append('## Paired comparison: Arm D minus Arm C (same 100 users)')
    lines.append('')
    lines.append(f'- Mean nDCG@10 difference (all users): **{fmt(mean(diffs))}**')
    lines.append(f'- Mean nDCG@10 difference (nonempty truth, {len(nonempty_users)} users): '
                 f'**{fmt(mean(diffs_nonempty))}**')
    lines.append(f'- Users where D scored higher: **{higher}**')
    lines.append(f'- Users where D scored lower: **{lower}**')
    lines.append(f'- Users where D scored equal: **{equal}**')
    lines.append(f'- Identical top-10 lists (same order): **{identical_order}**')
    lines.append(f'- Same set of assets in a different order: **{same_set_different_order}**')
    lines.append(f'- Mean top-10 overlap (out of 10): **{fmt(mean(overlaps))}**')
    lines.append(f'- Invalid model outputs (CBF fallbacks): arm C **{c_invalid}**, '
                 f'arm D **{d_invalid}**')
    lines.append(f'- Arm D users with an unavailable profile at the cutoff: '
                 f'**{d_profile_unavailable}**')
    lines.append(f'- Rough profile-keyword count in D summaries ({summaries} summaries): '
                 f'**{keyword_total}**')
    lines.append('  - ' + ', '.join(f'{word}: {keyword_counts[word]}'
                                    for word in PROFILE_WORDS))
    lines.append('')
    lines.append('## Users with future purchases')
    lines.append('')
    lines.append('| User | CBF nDCG@10 | C nDCG@10 | D nDCG@10 | D - C | C and D identical top-10 |')
    lines.append('|---|---:|---:|---:|---:|---|')
    for uid in nonempty_users:
        cbf_value = ndcg(cbf_users, uid)
        c_value = ndcg(c_users, uid)
        d_value = ndcg(d_users, uid)
        identical = 'yes' if c_pred.get(uid) and c_pred.get(uid) == d_pred.get(uid) else 'no'
        lines.append(f'| {uid} | {fmt(cbf_value)} | {fmt(c_value)} | {fmt(d_value)} | '
                     f'{fmt(d_value - c_value)} | {identical} |')
    lines.append('')

    report = '\n'.join(lines).rstrip('\n') + '\n'
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding='utf-8', newline='')
    print(report)


if __name__ == '__main__':
    main()
