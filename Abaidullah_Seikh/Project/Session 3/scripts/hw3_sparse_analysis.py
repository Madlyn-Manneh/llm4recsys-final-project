#!/usr/bin/env python3
"""Aggregate sparse-window analysis, using the main analysis's paired methods."""
import csv
from datetime import date
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10
from hw3_paired_analysis import apply_fallback, bootstrap, check, jsonl, sha, wtl

BASE = ROOT / 'outputs/sparse_baseline_120'
DEST = ROOT / 'outputs/sparse_scores'
ARMS = ('A', 'C', 'oldC')
LABELS = {'CBF': 'cbf', 'Latest buy': 'latest_buy',
          'Latest buy or sell': 'latest_buy_or_sell', 'Popularity': 'popularity'}


def mean(values):
    return sum(values) / len(values)


def read_rankings(path):
    groups = {}
    with path.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            groups.setdefault(row['method'], {}).setdefault(row['user_id'], []).append(
                (int(row['rank']), row['ISIN']))
    result = {}
    for method, by_user in groups.items():
        result[method] = {}
        for uid, rows in by_user.items():
            ordered = sorted(rows)
            check([rank for rank, _ in ordered] == list(range(1, 11)), 'saved ranking length mismatch')
            result[method][uid] = [asset for _, asset in ordered]
    return result


def main():
    output = DEST / 'sparse_analysis.json'
    check(not output.exists(), 'sparse analysis output exists; refusing to overwrite')
    protocol = json.loads((BASE / 'protocol.json').read_text())
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == 120 and users == protocol['users'], 'sparse cohort mismatch')
    summary = json.loads((DEST / 'scoring_summary.json').read_text())
    check(protocol['protocol_hash'] == summary['protocol_hash'] ==
          '5f470cfbb37d3985ea0996f564d059429b59fcd5dc747ff07632eb4e11589069', 'sparse protocol mismatch')
    for path, expected in summary['sources_sha256'].items():
        check(sha(ROOT / path) == expected, 'scoring source hash mismatch')
    data = ROOT.parent / 'Session 1/FAR-Trans'
    for name, expected in protocol['source_sha256'].items():
        check(sha(data / name) == expected, 'dataset source hash mismatch')
    horizon = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    assets, _, _, future, end, _ = load_data(data, protocol['cutoff'], horizon)
    check(horizon == 90 and end == '2021-08-30' and sorted(assets) == protocol['eligible_assets'],
          'truth reconstruction protocol mismatch')
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids'])
             for ctx in contexts}
    nonempty = [i for i, uid in enumerate(users) if truth[uid]]
    check(len(nonempty) == summary['nonempty_truth_users'] == 8, 'nonempty truth count mismatch')
    saved = read_rankings(BASE / 'predictions.csv')
    rankings = {label: saved[key] for label, key in LABELS.items()}
    invalid = {}
    for arm in ARMS:
        records = jsonl(ROOT / 'outputs' / f'sparse_{arm}' / 'responses.jsonl')
        rankings[arm], invalid[arm] = apply_fallback(records, contexts, rankings['CBF'], protocol['protocol_hash'])
        official = read_rankings(DEST / arm / 'predictions.csv')['custom']
        check(rankings[arm] == official, 'reconstructed official fallback rankings differ')
        check(len(invalid[arm]) == summary['methods'][arm]['fallbacks'], 'fallback count mismatch')
    values = {name: [ndcg10(by_user[uid], truth[uid]) for uid in users]
              for name, by_user in rankings.items()}
    for name, scores in values.items():
        reference = summary['methods'][name]
        avg, avg_nonempty = mean(scores), mean([scores[i] for i in nonempty])
        check(f'{avg:.4f}' == f'{reference["ndcg_at_10"]:.4f}'
              and f'{avg_nonempty:.4f}' == f'{reference["ndcg_at_10_nonempty"]:.4f}',
              'four-decimal scoring sanity mismatch')
        check(math.isclose(avg, reference['ndcg_at_10'], abs_tol=1e-15), 'full-precision score mismatch')

    result = {
        'label': 'sparse development results', 'users': 120, 'nonempty_truth_users': len(nonempty),
        'protocol_hash': protocol['protocol_hash'], 'horizon_days': horizon,
        'sanity': {'methods_passed': len(values), 'methods_failed': 0},
        'statistical_conventions': {
            'bootstrap': 'paired percentile bootstrap, 10000 resamples of all 120 users; '
                         'Python random.Random(0) reset for each pair; linear percentile interpolation',
            'sign_test': 'exact two-sided binomial p=0.5 over non-tied users; exact score equality for ties',
            'empty_truth_policy': 'zero in primary mean',
        },
        'methods': {}, 'pairs': {}, 'copying': {}, 'invalid_rows': {},
    }
    for name, scores in values.items():
        hits = [len(set(rankings[name][uid][:10]) & truth[uid]) for uid in users]
        result['methods'][name] = {
            'ndcg_at_10_all': mean(scores), 'ndcg_at_10_nonempty': mean([scores[i] for i in nonempty]),
            'users_with_at_least_one_hit': sum(n > 0 for n in hits), 'total_hits_top10': sum(hits),
            'nonempty_users_scoring_zero': sum(scores[i] == 0 for i in nonempty),
            'fallbacks': len(invalid.get(name, [])),
        }
    for left, right in (('C', 'A'), ('C', 'oldC'), ('A', 'CBF'), ('C', 'CBF'), ('C', 'Latest buy')):
        diff = [a - b for a, b in zip(values[left], values[right])]
        result['pairs'][f'{left} - {right}'] = {
            'mean_difference_all_120': mean(diff), 'bootstrap_95_ci': bootstrap(diff),
            'nonempty_wins_ties_losses': wtl([diff[i] for i in nonempty]),
        }
    result['candidate_pool_ceiling'] = {
        'nonempty_users': len(nonempty),
        'nonempty_users_with_truth_in_top50': sum(
            bool(truth[ctx['user_id']] & {a['id'] for a in ctx['candidate_assets']})
            for ctx in contexts if truth[ctx['user_id']]),
    }
    for arm in ARMS:
        exact = sum(rankings[arm][uid] == rankings['CBF'][uid] for uid in users)
        same_set = sum(set(rankings[arm][uid]) == set(rankings['CBF'][uid]) for uid in users)
        overlap = mean([len(set(rankings[arm][uid]) & set(rankings['CBF'][uid])) for uid in users])
        result['copying'][arm] = {'same_order_users': exact, 'same_set_different_order_users': same_set - exact,
                                  'mean_overlap_count_out_of_10': overlap, 'uses_official_fallback': True}
        result['invalid_rows'][arm] = {
            'count': len(invalid[arm]), 'positions': invalid[arm],
            'nonempty_truth_by_position': [{'position': pos, 'nonempty_truth': bool(truth[users[pos - 1]])}
                                           for pos in invalid[arm]],
        }
    sparse_timing = {}
    for arm in ARMS:
        meta = json.loads((ROOT / 'outputs' / f'sparse_{arm}' / 'run_meta.json').read_text())
        check(meta['users'] == 120, 'sparse timing denominator mismatch')
        sparse_timing[arm] = {'wall_seconds': meta['wall_seconds_whole_arm'], 'users': 120,
                              'seconds_per_user': meta['wall_seconds_whole_arm'] / 120}
    main_timing = {}
    for arm, folder, expected, count in (
        ('A', ROOT / 'outputs/arm_A_101_200', 7316.4, 100),
        ('C', ROOT / 'outputs/arm_C2_200', 20965.7, 200),
        ('oldC', ROOT.parent / 'Session 2/outputs/arm_C', 9604.6, 100),
    ):
        meta = json.loads((folder / 'run_meta.json').read_text())
        check(meta['users'] == count and meta['wall_seconds_whole_arm'] == expected,
              'main timing reference mismatch')
        main_timing[arm] = {'wall_seconds': expected, 'users': count, 'seconds_per_user': expected / count}
    result['timing'] = {
        'label': 'A ≈ ranking only; C − A per user ≈ summary cost (estimate, stage times not recorded)',
        'scope': 'main A: positions 101–200; main C: all 200; main oldC: HW2 positions 1–100; '
                 'sparse: same 120 users for all three arms; whole-arm loop times exclude loading',
        'main': main_timing, 'sparse': sparse_timing,
        'main_C_minus_A_seconds_per_user_estimate': main_timing['C']['seconds_per_user'] - main_timing['A']['seconds_per_user'],
        'sparse_C_minus_A_seconds_per_user_estimate': sparse_timing['C']['seconds_per_user'] - sparse_timing['A']['seconds_per_user'],
    }
    paths = [BASE / 'protocol.json', BASE / 'contexts.jsonl', BASE / 'predictions.csv',
             DEST / 'scoring_summary.json', ROOT / 'scripts/hw3_paired_analysis.py']
    paths += [ROOT / 'outputs' / f'sparse_{arm}' / filename for arm in ARMS
              for filename in ('responses.jsonl', 'run_meta.json', 'run_provenance.json')]
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha(path) for path in paths}
    result['analysis_script_sha256'] = sha(Path(__file__))
    with output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print('| Analysis | Aggregate result |')
    print('| --- | --- |')
    print(f'| Sanity | methods passed={len(values)}; failed=0; users=120; nonempty={len(nonempty)} |')
    for name, row in result['methods'].items():
        print(f'| {name} | nDCG all/nonempty={row["ndcg_at_10_all"]:.4f}/{row["ndcg_at_10_nonempty"]:.4f}; '
              f'hit users={row["users_with_at_least_one_hit"]}; hits={row["total_hits_top10"]}; '
              f'nonempty zeros={row["nonempty_users_scoring_zero"]}; fallbacks={row["fallbacks"]} |')
    for pair, row in result['pairs'].items():
        counts = row['nonempty_wins_ties_losses']
        ci = row['bootstrap_95_ci']
        print(f'| {pair} | mean={row["mean_difference_all_120"]:.4f}; CI=[{ci[0]:.4f}, {ci[1]:.4f}]; '
              f'W/T/L={counts["wins"]}/{counts["ties"]}/{counts["losses"]}; sign p={counts["sign_test_p"]:.4f} |')
    print(f'| Candidate ceiling | {result["candidate_pool_ceiling"]["nonempty_users_with_truth_in_top50"]}/{len(nonempty)} |')
    for arm in ARMS:
        row = result['copying'][arm]
        print(f'| {arm} copying | same order={row["same_order_users"]}; '
              f'same set/different order={row["same_set_different_order_users"]}; '
              f'mean overlap={row["mean_overlap_count_out_of_10"]:.4f}/10 |')
        row = result['invalid_rows'][arm]
        flags = ', '.join(f'{item["position"]}: nonempty={item["nonempty_truth"]}'
                          for item in row['nonempty_truth_by_position']) or 'none'
        print(f'| {arm} invalid | count={row["count"]}; positions={row["positions"]}; {flags} |')
    for arm in ARMS:
        print(f'| {arm} timing | main seconds/user={main_timing[arm]["seconds_per_user"]:.4f} '
              f'(n={main_timing[arm]["users"]}); sparse={sparse_timing[arm]["seconds_per_user"]:.4f} (n=120) |')
    print(f'| A ≈ ranking only; C − A per user ≈ summary cost (estimate, stage times not recorded) | '
          f'main={result["timing"]["main_C_minus_A_seconds_per_user_estimate"]:.4f} s; '
          f'sparse={result["timing"]["sparse_C_minus_A_seconds_per_user_estimate"]:.4f} s |')
    print(f'scripts/hw3_sparse_score.py SHA-256: {sha(ROOT / "scripts/hw3_sparse_score.py")}')
    print(f'scripts/hw3_sparse_analysis.py SHA-256: {sha(Path(__file__))}')
    print(f'outputs/sparse_scores/scoring_summary.json SHA-256: {sha(DEST / "scoring_summary.json")}')
    print(f'outputs/sparse_scores/sparse_analysis.json SHA-256: {sha(output)}')


if __name__ == '__main__':
    main()
