#!/usr/bin/env python3
"""Planned unblinding: aggregate held-out block analysis, with no model selection."""
from datetime import date
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10, scan_recent_events
from hw3_paired_analysis import apply_fallback, bootstrap, check, jsonl, sha, wtl
from hw3_repeat_first import repeat_first
from hw3_sparse_analysis import read_rankings
from hw3_block_score import BASE, DEST, EXPECTED, REGISTRATIONS, existing_hashes


def mean(values):
    return sum(values) / len(values)


def main():
    output = DEST / 'block_analysis.json'
    check(not output.exists(), 'block analysis output exists; refusing to overwrite')
    frozen = existing_hashes()
    for name, expected in REGISTRATIONS.items():
        check(sha(ROOT / name) == expected, 'registration or repeat-first source hash mismatch')
    protocol = json.loads((BASE / 'protocol.json').read_text())
    summary = json.loads((DEST / 'scoring_summary.json').read_text())
    check(protocol['protocol_hash'] == summary['protocol_hash'] == EXPECTED, 'block protocol mismatch')
    for path, expected in summary['source_sha256'].items():
        check(sha(ROOT / path) == expected, 'block scoring source hash mismatch')
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == 100 and users == protocol['users'], 'block cohort mismatch')
    data = ROOT.parent / 'Session 1/FAR-Trans'
    for name, expected in protocol['source_sha256'].items():
        check(sha(data / name) == expected, 'dataset source hash mismatch')
    horizon = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    assets, _, history, future, end, _ = load_data(data, protocol['cutoff'], horizon)
    check(horizon == 30 and end == '2021-07-01' and sorted(assets) == protocol['eligible_assets'],
          'truth reconstruction protocol mismatch')
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids']) for ctx in contexts}
    nonempty = [i for i, uid in enumerate(users) if truth[uid]]
    check(len(nonempty) == summary['nonempty_truth_users'], 'nonempty denominator mismatch')
    base_rankings = read_rankings(BASE / 'predictions.csv')
    rankings = {name: base_rankings[key] for name, key in
                (('Latest buy or sell', 'latest_buy_or_sell'), ('Latest buy', 'latest_buy'),
                 ('Popularity', 'popularity'), ('CBF', 'cbf'))}
    invalid = {}
    for arm in ('A', 'C'):
        rankings[arm], invalid[arm] = apply_fallback(
            jsonl(ROOT / 'outputs' / f'block_{arm}/responses.jsonl'), contexts, rankings['CBF'], EXPECTED)
        check(rankings[arm] == read_rankings(DEST / arm / 'predictions.csv')['custom'],
              'reconstructed official arm rankings mismatch')
    events = scan_recent_events(data, protocol['cutoff'], assets)
    latest = {}
    for ctx in contexts:
        uid = ctx['user_id']
        check({a['id']: a['buy_count'] for a in ctx['history']} == dict(history.get(uid, {})),
              'frozen block history differs from starter history')
        last = {}
        for timestamp, isin, kind in events.get(uid, []):
            check(timestamp < protocol['cutoff'], 'future event in repeat-first history')
            if kind == 'Buy':
                last[isin] = max(last.get(isin, timestamp), timestamp)
        latest[uid] = last
    rankings['C+R'] = {ctx['user_id']: repeat_first(ctx, rankings['C'][ctx['user_id']],
                                                  latest[ctx['user_id']], 'V2') for ctx in contexts}
    check(rankings['C+R'] == read_rankings(DEST / 'C_plus_R/predictions.csv')['custom'],
          'unchanged V2 rule reconstruction mismatch')
    values = {name: [ndcg10(by_user[uid], truth[uid]) for uid in users] for name, by_user in rankings.items()}
    for name, scores in values.items():
        reference = summary['methods'][name]
        check(math.isclose(mean(scores), reference['ndcg_at_10'], abs_tol=1e-15)
              and math.isclose(mean([scores[i] for i in nonempty]), reference['ndcg_at_10_nonempty'], abs_tol=1e-15),
              'block per-user score sanity mismatch')
    result = {
        'label': 'held-out development block, reported separately and not pooled',
        'users': 100, 'starter_positions': [201, 300], 'nonempty_truth_users': len(nonempty),
        'protocol_hash': EXPECTED, 'horizon_days': horizon, 'registrations_sha256': REGISTRATIONS,
        'C_plus_R': 'Unchanged V2, selected on main 200; no block selection or tuning',
        'sanity': {'methods_passed': len(values), 'methods_failed': 0},
        'statistical_conventions': {
            'bootstrap': '10000 paired resamples of all 100 users, Python random.Random(0) reset for each pair; '
                         'percentile interval with linear interpolation',
            'wins_ties_losses': 'nonempty-truth users only; exact score equality for ties',
            'sign_test': 'exact two-sided binomial p=0.5 over non-tied users',
            'empty_truth_policy': 'zero in primary mean',
        },
        'methods': summary['methods'], 'pairs': {}, 'invalid_rows': {}, 'copying': {},
    }
    for left, right in (('C+R', 'C'), ('C+R', 'A'), ('C', 'A'),
                         ('C+R', 'Latest buy or sell'), ('A', 'CBF'), ('C', 'CBF')):
        differences = [a - b for a, b in zip(values[left], values[right])]
        result['pairs'][f'{left} - {right}'] = {
            'mean_difference_all_100': mean(differences), 'bootstrap_95_ci': bootstrap(differences),
            'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty]),
        }
    candidate_ceiling = repeat_users = repeat_in_pool = 0
    for ctx in contexts:
        uid = ctx['user_id']
        candidates = {a['id'] for a in ctx['candidate_assets']}
        bought = {a['id'] for a in ctx['history']}
        candidate_ceiling += bool(truth[uid] & candidates)
        repeat_users += bool(truth[uid] & bought)
        repeat_in_pool += bool(truth[uid] & bought & candidates)
    result['diagnostics'] = {'candidate_ceiling_nonempty_users': candidate_ceiling,
                              'nonempty_users': len(nonempty), 'repeat_truth_users': repeat_users,
                              'repeat_truth_users_with_repeat_in_top50': repeat_in_pool}
    for arm in ('A', 'C'):
        exact = sum(rankings[arm][uid] == rankings['CBF'][uid] for uid in users)
        same_set = sum(set(rankings[arm][uid]) == set(rankings['CBF'][uid]) for uid in users)
        result['copying'][arm] = {
            'same_order_users': exact, 'same_set_including_same_order_users': same_set,
            'same_set_different_order_users': same_set - exact,
            'mean_overlap_count_out_of_10': mean([
                len(set(rankings[arm][uid]) & set(rankings['CBF'][uid])) for uid in users]),
        }
        check(len(invalid[arm]) == summary['methods'][arm]['fallbacks'], 'invalid/fallback count mismatch')
        result['invalid_rows'][arm] = {
            'count': len(invalid[arm]), 'block_positions': invalid[arm],
            'nonempty_truth_by_position': [
                {'block_position': position, 'starter_position': position + 200,
                 'nonempty_truth': bool(truth[users[position - 1]])} for position in invalid[arm]],
        }
    result['cross_window_summary'] = {}
    for label, path, role in (
        ('main_200', ROOT / 'outputs/final_200/repeat_first.json', 'selection'),
        ('sparse_120', ROOT / 'outputs/sparse_scores/repeat_first.json', 'robustness'),
    ):
        previous = json.loads(path.read_text())
        check(previous['selection']['chosen_C_plus_R'] == 'V2', 'previous-window variant differs from frozen V2')
        result['cross_window_summary'][label] = {
            'role': role, 'users': previous['users'], 'nonempty_truth_users': previous['nonempty_truth_users'],
            'C_plus_R_minus_C': previous['pairs']['V2 - C']['mean_difference_all'],
            'C_plus_R_minus_A': previous['pairs']['C+R - A']['mean_difference_all'],
            'source_sha256': sha(path),
        }
    result['cross_window_summary']['block_100'] = {
        'role': 'held-out', 'users': 100, 'nonempty_truth_users': len(nonempty),
        'C_plus_R_minus_C': result['pairs']['C+R - C']['mean_difference_all_100'],
        'C_plus_R_minus_A': result['pairs']['C+R - A']['mean_difference_all_100'],
    }
    sources = [BASE / 'protocol.json', BASE / 'contexts.jsonl', BASE / 'predictions.csv',
               DEST / 'scoring_summary.json', DEST / 'C_plus_R_responses.jsonl']
    sources += [ROOT / 'outputs' / f'block_{arm}' / filename for arm in ('A', 'C')
                for filename in ('responses.jsonl', 'run_meta.json', 'run_provenance.json')]
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha(path) for path in sources}
    result['analysis_script_sha256'] = sha(Path(__file__))
    check(all(sha(path) == expected for path, expected in frozen.items()), 'existing protected file changed')
    result['protected_existing_files_checked_unchanged'] = len(frozen)
    with output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(f'Sanity: methods_passed={len(values)} methods_failed=0; block_users=100 nonempty={len(nonempty)}')
    print('| Held-out pair | Mean difference | Bootstrap 95% CI | W/T/L nonempty | Exact sign p |')
    print('| --- | ---: | --- | --- | ---: |')
    for pair, row in result['pairs'].items():
        ci, counts = row['bootstrap_95_ci'], row['nonempty_wins_ties_losses']
        print(f'| {pair} | {row["mean_difference_all_100"]:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] | '
              f'{counts["wins"]}/{counts["ties"]}/{counts["losses"]} | {counts["sign_test_p"]:.4f} |')
    print(f'Candidate ceiling: {candidate_ceiling}/{len(nonempty)}; repeat_truth_users={repeat_users}; '
          f'repeat_truth_in_top50={repeat_in_pool}/{repeat_users}')
    for arm in ('A', 'C'):
        row = result['copying'][arm]
        print(f'{arm} copying: same_order={row["same_order_users"]}; '
              f'same_set={row["same_set_including_same_order_users"]}; '
              f'same_set_different_order={row["same_set_different_order_users"]}; '
              f'mean_overlap={row["mean_overlap_count_out_of_10"]:.4f}/10')
        bad = result['invalid_rows'][arm]
        flags = ', '.join(f'block_position={r["block_position"]},starter_position={r["starter_position"]},'
                          f'nonempty={r["nonempty_truth"]}' for r in bad['nonempty_truth_by_position']) or 'none'
        print(f'{arm} invalid: count={bad["count"]}; {flags}')
    print('| Window | Role | C+R minus C | C+R minus A |')
    print('| --- | --- | ---: | ---: |')
    for label, row in result['cross_window_summary'].items():
        print(f'| {label} | {row["role"]} | {row["C_plus_R_minus_C"]:.4f} | {row["C_plus_R_minus_A"]:.4f} |')
    print(f'Protected existing files unchanged: {len(frozen)}')
    for path in (ROOT / 'scripts/hw3_block_score.py', Path(__file__), *sorted(DEST.rglob('*.json'))):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
