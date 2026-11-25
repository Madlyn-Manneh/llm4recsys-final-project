#!/usr/bin/env python3
"""Pre-registered repeat-first development experiment; no model calls."""
import csv
from datetime import date
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10, scan_recent_events, validate_ranking
from hw3_paired_analysis import apply_fallback, bootstrap, check, jsonl, sha, wtl

PLAN = ROOT / 'HW3_PLAN_C_IMPROVEMENT.md'
PLAN_HASH = 'fa99792f07dfdb8b48a63235ba8652a1aeca8a6080ac0cea0343445e69ad1402'
METHODS = ('C', 'V1', 'V2', 'A+R', 'A', 'CBF', 'Latest buy', 'Latest buy or sell')
WINDOWS = {
    'main_200': ('outputs/baseline_200', 'outputs/final_200', 200,
                 'outputs/final_200/A_responses.jsonl', 'outputs/arm_C2_200/responses.jsonl'),
    'sparse_120': ('outputs/sparse_baseline_120', 'outputs/sparse_scores', 120,
                   'outputs/sparse_A/responses.jsonl', 'outputs/sparse_C/responses.jsonl'),
}


def mean(values):
    return sum(values) / len(values)


def saved_baselines(folder, users):
    groups = {}
    with (folder / 'predictions.csv').open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            groups.setdefault(row['method'], {}).setdefault(row['user_id'], []).append(
                (int(row['rank']), row['ISIN']))
    result = {}
    for label, method in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'),
                           ('Latest buy or sell', 'latest_buy_or_sell')):
        result[label] = {}
        for uid in users:
            rows = sorted(groups[method][uid])
            check([rank for rank, _ in rows] == list(range(1, 11)), 'baseline ranking count mismatch')
            result[label][uid] = [asset for _, asset in rows]
    return result


def repeat_first(context, base_order, latest, variant):
    # User clarified before diagnostics: promote repeats from all 50 candidates.
    # Complete the 10-item model order with starter candidate order for tie-breaking.
    candidate_ids = [asset['id'] for asset in context['candidate_assets']]
    counts = {asset['id']: asset['buy_count'] for asset in context['history']}
    extended = base_order + [isin for isin in candidate_ids if isin not in base_order]
    position = {isin: index for index, isin in enumerate(extended)}
    repeats = [isin for isin in candidate_ids if isin in counts]
    check(all(isin in latest for isin in repeats), 'repeat candidate missing pre-cutoff Buy date')
    if variant == 'V1':
        key = lambda isin: (-date.fromisoformat(latest[isin]).toordinal(), -counts[isin], position[isin])
    else:
        key = lambda isin: (-counts[isin], -date.fromisoformat(latest[isin]).toordinal(), position[isin])
    ranking = sorted(repeats, key=key)[:10]
    for isin in base_order:
        if len(ranking) == 10:
            break
        if isin not in ranking:
            ranking.append(isin)
    return validate_ranking(ranking, candidate_ids)


def evaluate(name, specification):
    baseline_rel, destination_rel, n, a_rel, c_rel = specification
    baseline, destination = ROOT / baseline_rel, ROOT / destination_rel
    protocol = json.loads((baseline / 'protocol.json').read_text())
    contexts = jsonl(baseline / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == n and users == protocol['users'], 'cohort mismatch')
    data = ROOT.parent / 'Session 1/FAR-Trans'
    for filename, expected in protocol['source_sha256'].items():
        check(sha(data / filename) == expected, 'dataset source hash mismatch')
    horizon = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    assets, _, history, future, end, _ = load_data(data, protocol['cutoff'], horizon)
    check(end == protocol['end_exclusive'] and sorted(assets) == protocol['eligible_assets'],
          'truth protocol reconstruction mismatch')
    # Recency comes from the starter's own pre-cutoff-only event result; counts
    # and the universe of previously bought assets come from frozen contexts.
    events = scan_recent_events(data, protocol['cutoff'], assets)
    latest = {}
    for ctx in contexts:
        uid = ctx['user_id']
        counts = {asset['id']: asset['buy_count'] for asset in ctx['history']}
        check(counts == dict(history.get(uid, {})), 'context history differs from starter history')
        last = {}
        for timestamp, isin, kind in events.get(uid, []):
            check(timestamp < protocol['cutoff'], 'future event encountered in repeat-first input')
            if kind == 'Buy' and isin in counts:
                last[isin] = max(last.get(isin, timestamp), timestamp)
        latest[uid] = last
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids'])
             for ctx in contexts}
    nonempty = [index for index, uid in enumerate(users) if truth[uid]]
    rankings = saved_baselines(baseline, users)
    invalid = {}
    for arm, response in (('A', ROOT / a_rel), ('C', ROOT / c_rel)):
        rankings[arm], invalid[arm] = apply_fallback(
            jsonl(response), contexts, rankings['CBF'], protocol['protocol_hash'])
    for label, source, variant in (('V1', 'C', 'V1'), ('V2', 'C', 'V2'), ('A+R', 'A', 'V1')):
        rankings[label] = {ctx['user_id']: repeat_first(
            ctx, rankings[source][ctx['user_id']], latest[ctx['user_id']], variant) for ctx in contexts}
    scores = {method: [ndcg10(rankings[method][uid], truth[uid]) for uid in users] for method in METHODS}
    baseline_metrics = json.loads((baseline / 'metrics.json').read_text())['methods']
    for label, key in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'), ('Latest buy or sell', 'latest_buy_or_sell')):
        check(math.isclose(mean(scores[label]), baseline_metrics[key]['ndcg_at_10'], abs_tol=1e-15),
              'baseline score sanity mismatch')
    for arm in ('A', 'C'):
        evaluation = destination / (f'evaluation_{arm}' if name == 'main_200' else arm)
        metrics = json.loads((evaluation / 'metrics.json').read_text())
        check(math.isclose(mean(scores[arm]), metrics['methods']['custom']['ndcg_at_10'], abs_tol=1e-15),
              'official arm score sanity mismatch')
        check(len(invalid[arm]) == len(metrics['custom_failures']), 'official fallback count mismatch')

    repeat_truth_users = 0
    new_truth_users = 0
    repeat_truth_in_pool = 0
    candidate_repeat_counts = []
    for ctx in contexts:
        uid = ctx['user_id']
        bought = {asset['id'] for asset in ctx['history']}
        candidates = {asset['id'] for asset in ctx['candidate_assets']}
        repeated_truth = truth[uid] & bought
        repeat_truth_users += bool(repeated_truth)
        new_truth_users += bool(truth[uid] - bought)
        repeat_truth_in_pool += bool(repeated_truth & candidates)
        candidate_repeat_counts.append(len(bought & candidates))
    result = {
        'label': 'development results', 'window': name, 'users': n,
        'nonempty_truth_users': len(nonempty), 'horizon_days': horizon,
        'protocol_hash': protocol['protocol_hash'], 'plan_sha256': sha(PLAN),
        'clarification_before_diagnostics': {
            'scope': 'User selected: promote from all 50 candidates',
            'ties': 'C/A top-10 order first; starter candidate order for assets absent from that ranking',
            'remaining_slots': 'Fill from the original C/A ranking, preserving its order',
            'recency_source': 'starter.scan_recent_events pre-cutoff Buy dates; counts from frozen contexts',
        },
        'diagnostics': {
            'nonempty_users_with_repeat_truth': repeat_truth_users,
            'nonempty_users_with_new_truth': new_truth_users,
            'repeat_and_new_user_counts_can_overlap': True,
            'users_with_previously_bought_candidate': sum(count > 0 for count in candidate_repeat_counts),
            'mean_previously_bought_candidates_per_user': mean(candidate_repeat_counts),
            'repeat_truth_users_with_repeated_truth_in_top50': repeat_truth_in_pool,
        },
        'official_fallbacks': {arm: len(positions) for arm, positions in invalid.items()},
        'methods': {method: {'ndcg_at_10_all': mean(scores[method]),
                             'ndcg_at_10_nonempty': mean([scores[method][i] for i in nonempty])}
                    for method in METHODS},
        'statistical_conventions': {
            'bootstrap': f'10000 paired resamples of all {n} users; Python random.Random(0) reset for each pair; '
                         'percentile CI with linear interpolation',
            'wins_ties_losses': 'nonempty-truth users only; exact score equality for ties',
            'sign_test': 'exact two-sided binomial p=0.5 on non-tied users',
        },
        'analysis_script_sha256': sha(Path(__file__)),
    }
    source_paths = [baseline / 'protocol.json', baseline / 'contexts.jsonl', baseline / 'predictions.csv',
                    ROOT / a_rel, ROOT / c_rel, ROOT / 'starter.py', ROOT / 'scripts/hw3_paired_analysis.py']
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha(path) for path in source_paths}
    return result, scores, nonempty


def main():
    check(sha(PLAN) == PLAN_HASH, 'pre-registration plan hash mismatch')
    targets = {name: ROOT / spec[1] / 'repeat_first.json' for name, spec in WINDOWS.items()}
    check(all(not path.exists() for path in targets.values()), 'repeat-first output exists; refusing to overwrite')
    protected = [path for directory in ('outputs', 'cohorts', 'scripts')
                 for path in (ROOT / directory).rglob('*') if path.is_file()]
    protected += [path for path in ROOT.iterdir() if path.is_file() and
                  (path.name.startswith(('HW3_PROTOCOL', 'run_hw3_')) or path == PLAN)]
    frozen = {path: sha(path) for path in protected}
    evaluated = {name: evaluate(name, spec) for name, spec in WINDOWS.items()}
    main_result = evaluated['main_200'][0]['methods']
    v1, v2 = main_result['V1']['ndcg_at_10_all'], main_result['V2']['ndcg_at_10_all']
    check(v1 != v2, 'main V1 and V2 tie; pre-registration does not specify a tie-break, selection requires clarification')
    chosen = 'V1' if v1 > v2 else 'V2'
    for name, (result, scores, nonempty) in evaluated.items():
        result['selection'] = {'chosen_C_plus_R': chosen, 'discarded_variant': 'V2' if chosen == 'V1' else 'V1',
                               'selection_data': 'main_200 only', 'criterion': 'higher mean nDCG@10 over all 200',
                               'main_V1_ndcg_at_10': v1, 'main_V2_ndcg_at_10': v2,
                               'sparse_role': 'robustness check only'}
        result['pairs'] = {}
        for label, left, right in (('V1 - C', 'V1', 'C'), ('V2 - C', 'V2', 'C'),
                                    ('C+R - A+R', chosen, 'A+R'),
                                    ('C+R - Latest buy or sell', chosen, 'Latest buy or sell'),
                                    ('C+R - A', chosen, 'A')):
            differences = [a - b for a, b in zip(scores[left], scores[right])]
            result['pairs'][label] = {
                'left_method': left, 'right_method': right, 'mean_difference_all': mean(differences),
                'bootstrap_95_ci': bootstrap(differences),
                'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty]),
            }
    check(all(sha(path) == expected for path, expected in frozen.items()), 'existing protected file changed')
    for name, (result, _, _) in evaluated.items():
        result['protected_existing_files_checked_unchanged'] = len(frozen)
        with targets[name].open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(f'C+R selection: {chosen}; main V1={v1:.4f}; main V2={v2:.4f}')
    for name, (result, _, _) in evaluated.items():
        print(f'\n{name}: users={result["users"]}; nonempty={result["nonempty_truth_users"]}')
        diag = result['diagnostics']
        print(f'Repeat truth users={diag["nonempty_users_with_repeat_truth"]}; '
              f'new truth users={diag["nonempty_users_with_new_truth"]}; '
              f'repeated truth in top50={diag["repeat_truth_users_with_repeated_truth_in_top50"]}/'
              f'{diag["nonempty_users_with_repeat_truth"]}')
        print(f'Users with previously bought candidate={diag["users_with_previously_bought_candidate"]}; '
              f'mean count={diag["mean_previously_bought_candidates_per_user"]:.4f}')
        print('| Method | nDCG@10 all | nDCG@10 non-empty |')
        print('| --- | ---: | ---: |')
        for method, row in result['methods'].items():
            print(f'| {method} | {row["ndcg_at_10_all"]:.4f} | {row["ndcg_at_10_nonempty"]:.4f} |')
        print('| Pair | Mean difference | Bootstrap 95% CI | W/T/L non-empty | Exact sign p |')
        print('| --- | ---: | --- | --- | ---: |')
        for pair, row in result['pairs'].items():
            ci, counts = row['bootstrap_95_ci'], row['nonempty_wins_ties_losses']
            print(f'| {pair} | {row["mean_difference_all"]:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] | '
                  f'{counts["wins"]}/{counts["ties"]}/{counts["losses"]} | {counts["sign_test_p"]:.4f} |')
    print(f'Protected existing files unchanged: {len(frozen)}')
    for path in (PLAN, Path(__file__), *targets.values()):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
