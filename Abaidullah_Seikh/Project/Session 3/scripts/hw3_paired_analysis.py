#!/usr/bin/env python3
"""Reproduce main-window scores and emit aggregate-only development analyses."""
from datetime import date
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10, validate_ranking

BASE = ROOT / 'outputs/baseline_200'
FINAL = ROOT / 'outputs/final_200'
OLD = ROOT.parent / 'Session 2/outputs'


def check(condition, message):
    if not condition:
        print('FAIL: ' + message, flush=True)
        raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()]


def mean(values):
    return sum(values) / len(values)


def sign_test(wins, losses):
    n = wins + losses
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(wins, losses) + 1)) / (2 ** n))


def wtl(differences):
    wins = sum(value > 0 for value in differences)
    losses = sum(value < 0 for value in differences)
    return {'wins': wins, 'ties': len(differences) - wins - losses, 'losses': losses,
            'sign_test_p': sign_test(wins, losses)}


def percentile(sorted_values, probability):
    index = (len(sorted_values) - 1) * probability
    lo, hi = math.floor(index), math.ceil(index)
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (index - lo)


def bootstrap(differences):
    # Reset seed for each pair: the same 10,000 paired user-index samples.
    rng = random.Random(0)
    n = len(differences)
    samples = sorted(sum(differences[rng.randrange(n)] for _ in range(n)) / n
                     for _ in range(10000))
    return [percentile(samples, .025), percentile(samples, .975)]


def baseline_rankings(users):
    raw = {}
    with (BASE / 'predictions.csv').open(newline='', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            key = (row['method'], row['user_id'])
            raw.setdefault(key, []).append((int(row['rank']), row['ISIN']))
    result = {}
    for name, method in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'), ('Popularity', 'popularity')):
        result[name] = {}
        for uid in users:
            rows = sorted(raw.get((method, uid), []))
            check([rank for rank, _ in rows] == list(range(1, 11)), 'baseline ranking length mismatch')
            result[name][uid] = [asset for _, asset in rows]
    return result


def apply_fallback(rows, contexts, cbf, protocol_hash=None):
    indexed = {row['user_id']: row for row in rows}
    check(len(rows) == len(indexed) == len(contexts), 'response count or duplicate mismatch')
    check(set(indexed) == {ctx['user_id'] for ctx in contexts}, 'response coverage mismatch')
    rankings, invalid = {}, []
    for position, ctx in enumerate(contexts, 1):
        uid = ctx['user_id']
        row = indexed[uid]
        check(row.get('stage') == 'ranker', 'response stage mismatch')
        if protocol_hash is not None:
            check(row.get('protocol_hash') == protocol_hash, 'response protocol mismatch')
        try:
            ranking = validate_ranking(row['ranked_ids'], [a['id'] for a in ctx['candidate_assets']])
        except (ValueError, KeyError, TypeError):
            invalid.append(position)
            ranking = cbf[uid]
        rankings[uid] = ranking
    return rankings, invalid


def main():
    output = FINAL / 'paired_analysis.json'
    check(not output.exists(), 'paired analysis output already exists; refusing to overwrite')
    protocol = json.loads((BASE / 'protocol.json').read_text())
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == 200 and users == protocol['users'], 'main cohort mismatch')
    data = ROOT.parent / 'Session 1/FAR-Trans'
    for name, expected in protocol['source_sha256'].items():
        check(sha(data / name) == expected, 'dataset source hash mismatch')
    days = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    assets, _, _, future, end, _ = load_data(data, protocol['cutoff'], days)
    check(end == protocol['end_exclusive'] and sorted(assets) == protocol['eligible_assets'],
          'truth protocol reconstruction mismatch')
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids'])
             for ctx in contexts}
    nonempty = [index for index, uid in enumerate(users) if truth[uid]]
    check(len(nonempty) == 24, 'nonempty truth count mismatch')
    rankings = baseline_rankings(users)
    invalid = {}
    for name in ('A', 'C'):
        rankings[name], invalid[name] = apply_fallback(
            jsonl(FINAL / f'{name}_responses.jsonl'), contexts, rankings['CBF'], protocol['protocol_hash'])
    check(invalid == {'A': [181], 'C': []}, 'unexpected invalid positions')
    scores = {name: [ndcg10(ranking[uid], truth[uid]) for uid in users]
              for name, ranking in rankings.items()}
    expected_display = {'A': '0.0302', 'C': '0.0282', 'CBF': '0.0305', 'Latest buy': '0.0474'}
    for name, expected in expected_display.items():
        check(f'{mean(scores[name]):.4f}' == expected, 'four-decimal score sanity mismatch')
    baseline_metrics = json.loads((BASE / 'metrics.json').read_text())['methods']
    for name, key in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'), ('Popularity', 'popularity')):
        check(math.isclose(mean(scores[name]), baseline_metrics[key]['ndcg_at_10'], abs_tol=1e-15),
              'full-precision baseline score mismatch')
    for name in ('A', 'C'):
        official = json.loads((FINAL / f'evaluation_{name}/metrics.json').read_text())
        check(math.isclose(mean(scores[name]), official['methods']['custom']['ndcg_at_10'], abs_tol=1e-15),
              'full-precision official arm score mismatch')
        check(len(official['custom_failures']) == len(invalid[name]), 'official fallback count mismatch')

    result = {
        'label': 'development results', 'users': 200, 'nonempty_truth_users': 24,
        'protocol_hash': protocol['protocol_hash'],
        'statistical_conventions': {
            'bootstrap': 'paired percentile bootstrap, 10000 resamples of all 200 users; '
                         'Python random.Random(0) reset for each pair; linear percentile interpolation',
            'sign_test': 'exact two-sided binomial p=0.5 over non-tied users; exact score equality for ties',
            'primary_empty_truth_policy': 'zero',
        },
        'sanity': {'checks_passed': len(expected_display), 'checks_failed': 0},
        'methods': {}, 'pairs': {}, 'copying': {},
    }
    for name in ('A', 'C', 'CBF', 'Latest buy', 'Popularity'):
        hits = [len(set(rankings[name][uid][:10]) & truth[uid]) for uid in users]
        result['methods'][name] = {
            'ndcg_at_10_all': mean(scores[name]),
            'ndcg_at_10_nonempty': mean([scores[name][i] for i in nonempty]),
            'users_with_at_least_one_hit': sum(count > 0 for count in hits),
            'total_hits_top10': sum(hits),
            'nonempty_users_scoring_zero': sum(scores[name][i] == 0 for i in nonempty),
            'fallbacks': len(invalid.get(name, [])),
        }
    for left, right in (('C', 'A'), ('A', 'CBF'), ('C', 'CBF'), ('C', 'Latest buy')):
        differences = [a - b for a, b in zip(scores[left], scores[right])]
        result['pairs'][f'{left} - {right}'] = {
            'mean_difference_all_200': mean(differences),
            'bootstrap_95_ci': bootstrap(differences),
            'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty]),
        }
    result['candidate_pool_ceiling'] = {
        'nonempty_users': len(nonempty),
        'nonempty_users_with_truth_in_top50': sum(
            bool(truth[ctx['user_id']] & {a['id'] for a in ctx['candidate_assets']})
            for ctx in contexts if truth[ctx['user_id']]),
    }
    for name in ('A', 'C'):
        exact = sum(rankings[name][uid] == rankings['CBF'][uid] for uid in users)
        same_set = sum(set(rankings[name][uid]) == set(rankings['CBF'][uid]) for uid in users)
        overlap = [len(set(rankings[name][uid]) & set(rankings['CBF'][uid])) for uid in users]
        result['copying'][name] = {
            'same_order_users': exact, 'same_set_different_order_users': same_set - exact,
            'mean_overlap_count_out_of_10': mean(overlap), 'mean_overlap_fraction': mean(overlap) / 10,
            'uses_official_fallback': True,
        }
    result['nonempty_split'] = {'positions_1_100': sum(i < 100 for i in nonempty),
                                'positions_101_200': sum(i >= 100 for i in nonempty)}
    check(jsonl(OLD / 'baseline/contexts.jsonl') == contexts[:100], 'old-C context identity mismatch')
    old_protocol = json.loads((OLD / 'baseline/protocol.json').read_text())
    old_c, old_invalid = apply_fallback(jsonl(OLD / 'arm_C/responses.jsonl'), contexts[:100],
                                        rankings['CBF'], old_protocol['protocol_hash'])
    old_scores = [ndcg10(old_c[uid], truth[uid]) for uid in users[:100]]
    old_difference = [new - old for new, old in zip(scores['C'][:100], old_scores)]
    result['old_C_ablation_first100'] = {
        'users': 100, 'nonempty_users': sum(i < 100 for i in nonempty),
        'mean_ndcg_all_100': {'old_C': mean(old_scores), 'new_C': mean(scores['C'][:100]),
                              'A': mean(scores['A'][:100])},
        'new_vs_old_all100': wtl(old_difference),
        'new_vs_old_nonempty': wtl([old_difference[i] for i in nonempty if i < 100]),
        'old_C_fallbacks': len(old_invalid),
    }
    uid = users[180]
    raw_invalid = [row for row in jsonl(ROOT / 'outputs/arm_A_101_200/raw_log.jsonl')
                   if row.get('valid') is False]
    check(len(raw_invalid) == 1 and raw_invalid[0]['user_id'] == uid, 'invalid raw-record identity mismatch')
    numbers = raw_invalid[0]['parsed_numbers']
    candidates = contexts[180]['candidate_assets']
    check(len(numbers) == len(set(numbers)) == 9 and all(1 <= n <= len(candidates) for n in numbers),
          'sensitivity parsed-number integrity mismatch')
    repaired = [candidates[number - 1]['id'] for number in numbers]
    original = {row['user_id']: row for row in jsonl(FINAL / 'A_responses.jsonl')}[uid]['ranked_ids']
    check(repaired == original, 'sensitivity nine IDs differ from saved response')
    for candidate in candidates:
        if candidate['id'] not in repaired:
            repaired.append(candidate['id'])
            break
    validate_ranking(repaired, [a['id'] for a in candidates])
    sensitivity_scores = list(scores['A'])
    sensitivity_scores[180] = ndcg10(repaired, truth[uid])
    result['invalid_A_sensitivity'] = {
        'label': 'sensitivity only, not the official score', 'position': 181,
        'nonempty_truth': bool(truth[uid]),
        'official_fallback_user_ndcg': scores['A'][180],
        'sensitivity_repair_user_ndcg': sensitivity_scores[180],
        'A_official_mean_all_200': mean(scores['A']),
        'A_official_mean_nonempty': mean([scores['A'][i] for i in nonempty]),
        'A_sensitivity_mean_all_200': mean(sensitivity_scores),
        'A_sensitivity_mean_nonempty': mean([sensitivity_scores[i] for i in nonempty]),
    }
    sources = [BASE / 'protocol.json', BASE / 'contexts.jsonl', BASE / 'predictions.csv',
               FINAL / 'A_responses.jsonl', FINAL / 'C_responses.jsonl', OLD / 'arm_C/responses.jsonl',
               ROOT / 'starter.py', ROOT / 'HW3_PROTOCOL.md', ROOT / 'HW3_PROTOCOL_AMENDMENT1.md']
    result['source_sha256'] = {str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path): sha(path)
                               for path in sources}
    result['analysis_script_sha256'] = sha(Path(__file__))
    output.parent.mkdir(exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')

    print('| Analysis | Aggregate result |')
    print('| --- | --- |')
    print('| Sanity | passed=4; failed=0; users=200; nonempty=24 |')
    for name, row in result['methods'].items():
        print(f'| {name} | nDCG all/nonempty={row["ndcg_at_10_all"]:.4f}/'
              f'{row["ndcg_at_10_nonempty"]:.4f}; hit users={row["users_with_at_least_one_hit"]}; '
              f'hits={row["total_hits_top10"]}; nonempty zeros={row["nonempty_users_scoring_zero"]}; '
              f'fallbacks={row["fallbacks"]} |')
    for pair, row in result['pairs'].items():
        count = row['nonempty_wins_ties_losses']
        ci = row['bootstrap_95_ci']
        print(f'| {pair} | mean={row["mean_difference_all_200"]:.4f}; '
              f'95% CI=[{ci[0]:.4f}, {ci[1]:.4f}]; '
              f'W/T/L (24)={count["wins"]}/{count["ties"]}/{count["losses"]}; '
              f'exact sign p={count["sign_test_p"]:.4f} |')
    print(f'| Candidate ceiling | {result["candidate_pool_ceiling"]["nonempty_users_with_truth_in_top50"]}/24 |')
    for name, row in result['copying'].items():
        print(f'| {name} copying | same order={row["same_order_users"]}; '
              f'same set/different order={row["same_set_different_order_users"]}; '
              f'mean overlap={row["mean_overlap_count_out_of_10"]:.4f}/10 |')
    split = result['nonempty_split']
    print(f'| Nonempty split | first100={split["positions_1_100"]}; second100={split["positions_101_200"]} |')
    ablation = result['old_C_ablation_first100']
    counts = ablation['new_vs_old_all100']
    means = ablation['mean_ndcg_all_100']
    print(f'| Old-C ablation (100) | old C={means["old_C"]:.4f}; new C={means["new_C"]:.4f}; '
          f'A={means["A"]:.4f}; nonempty={ablation["nonempty_users"]}; '
          f'W/T/L={counts["wins"]}/{counts["ties"]}/{counts["losses"]}; '
          f'exact sign p={counts["sign_test_p"]:.4f} |')
    counts = ablation['new_vs_old_nonempty']
    print(f'| Old-C ablation nonempty | W/T/L={counts["wins"]}/{counts["ties"]}/{counts["losses"]}; '
          f'exact sign p={counts["sign_test_p"]:.4f} |')
    sensitivity = result['invalid_A_sensitivity']
    print(f'| Invalid A position 181 | nonempty={sensitivity["nonempty_truth"]}; '
          f'official nDCG={sensitivity["official_fallback_user_ndcg"]:.4f}; '
          f'sensitivity nDCG={sensitivity["sensitivity_repair_user_ndcg"]:.4f} |')
    print(f'| A official | all/nonempty={sensitivity["A_official_mean_all_200"]:.4f}/'
          f'{sensitivity["A_official_mean_nonempty"]:.4f} |')
    print(f'| A sensitivity only, not the official score | '
          f'all/nonempty={sensitivity["A_sensitivity_mean_all_200"]:.4f}/'
          f'{sensitivity["A_sensitivity_mean_nonempty"]:.4f} |')
    print(f'scripts/hw3_paired_analysis.py SHA-256: {sha(Path(__file__))}')
    print(f'outputs/final_200/paired_analysis.json SHA-256: {sha(output)}')


if __name__ == '__main__':
    main()
