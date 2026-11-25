#!/usr/bin/env python3
"""Planned benchmark-block unblinding and B1/B2 selection; no model calls."""
from datetime import date
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10, scan_recent_events, validate_ranking
from hw3_paired_analysis import apply_fallback, bootstrap, check, jsonl, sha, wtl
from hw3_repeat_first import repeat_first
from hw3_sparse_analysis import read_rankings
from hw3_c_all import starter_run

PLAN = ROOT / 'BENCH_PLAN_301_400.md'
OLD = ROOT / 'outputs/block_301_400'
NEW = ROOT / 'outputs/all_cand_block3_100'
DEST = ROOT / 'outputs/bench_scores'
SOURCE = ROOT / 'outputs/block3_A'
LABELS = {'Latest buy or sell': 'latest_buy_or_sell', 'Latest buy': 'latest_buy',
          'Popularity': 'popularity', 'CBF': 'cbf'}


def mean(values):
    return sum(values) / len(values)


def buy_or_sell_repeat_first(context, a_order, events, cutoff):
    """B2: only previously BOUGHT assets qualify; Buy/Sell dates set their order."""
    candidates = [asset['id'] for asset in context['candidate_assets']]
    counts = {asset['id']: asset['buy_count'] for asset in context['history']}
    repeats = [isin for isin in candidates if isin in counts]
    latest = {}
    for timestamp, isin, kind in events:
        check(timestamp < cutoff, 'future event in B2 inputs')
        if isin in counts and kind in ('Buy', 'Sell'):
            latest[isin] = max(latest.get(isin, timestamp), timestamp)
    check(all(isin in latest for isin in repeats), 'previously bought asset missing an eligible event date')
    # A order precedes original CBF candidate order for assets A did not rank.
    extended = a_order + [isin for isin in candidates if isin not in a_order]
    position = {isin: index for index, isin in enumerate(extended)}
    ranking = sorted(repeats, key=lambda isin: (
        -date.fromisoformat(latest[isin]).toordinal(), -counts[isin], position[isin]))[:10]
    for isin in a_order:
        if len(ranking) == 10:
            break
        if isin not in ranking:
            ranking.append(isin)
    return validate_ranking(ranking, candidates)


def main():
    check(sha(PLAN) == '8364b5f311bdf8a842734eabd6ca5805c10be9623ce01b4a94c64bf26b5d43d4',
          'benchmark plan hash mismatch')
    check(sha(ROOT / 'scripts/hw3_repeat_first.py') ==
          'e1401a71475dcd50c0db56f01284f0086e76a6d12f1e0d9846c1a088a067c437', 'B1 source hash mismatch')
    check(not NEW.exists() and not DEST.exists(), 'benchmark output exists; refusing to overwrite')
    protected = [p for folder in ('outputs', 'cohorts', 'scripts') for p in (ROOT / folder).rglob('*') if p.is_file()]
    protected += [p for p in ROOT.iterdir() if p.is_file() and
                  p.name.startswith(('HW3_', 'BENCH_', 'run_hw3_', 'run_bench_'))]
    frozen = {p: sha(p) for p in protected}
    protocol = json.loads((OLD / 'protocol.json').read_text())
    prior_contexts = jsonl(OLD / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in prior_contexts]
    check(len(users) == len(set(users)) == 100 and users == protocol['users'] ==
          (ROOT / 'cohorts/block_301_400_users.txt').read_text().splitlines(), 'benchmark cohort mismatch')
    meta = json.loads((SOURCE / 'run_meta.json').read_text())
    provenance = json.loads((SOURCE / 'run_provenance.json').read_text())
    check(provenance['exit_code'] == 0 and bool(provenance.get('end_time')) and meta['users'] == 100,
          'benchmark inference incomplete')
    check(provenance['script_sha256'] == sha(ROOT / 'llm_rerank.py') ==
          '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da', 'A source hash mismatch')
    count = len(protocol['eligible_assets'])
    common = ['--users-file', 'cohorts/block_301_400_users.txt', '--cutoff', '2021-06-01',
              '--horizon-days', '30', '--cohort', 'warm', '--data-dir', '../Session 1/FAR-Trans',
              '--candidate-count', str(count)]
    new_protocol, new_metrics = starter_run(common, NEW)
    contexts = jsonl(NEW / 'contexts.jsonl')
    same_users = [ctx['user_id'] for ctx in contexts] == users == new_protocol['users']
    same_first50 = len(contexts) == 100 and all(
        [a['id'] for a in ctx['candidate_assets'][:50]] == [a['id'] for a in old['candidate_assets']]
        for ctx, old in zip(contexts, prior_contexts))
    old_metrics = json.loads((OLD / 'metrics.json').read_text())
    unchanged = new_metrics['methods'] == old_metrics['methods']
    all_assets = new_protocol['candidate_count'] == count and all(
        len(ctx['candidate_assets']) == count and {a['id'] for a in ctx['candidate_assets']} ==
        set(protocol['eligible_assets']) for ctx in contexts)
    print(f'Same users/order: {same_users}; first50 same order: {same_first50}; baselines identical: {unchanged}', flush=True)
    print(f'All eligible candidates: {all_assets}; eligible_assets={count}; protocol_hash={new_protocol["protocol_hash"]}', flush=True)
    check(same_users and same_first50 and unchanged and all_assets, 'all-eligible benchmark input mismatch')
    baseline_rankings = read_rankings(NEW / 'predictions.csv')
    rankings = {name: baseline_rankings[key] for name, key in LABELS.items()}
    source_rows = jsonl(SOURCE / 'responses.jsonl')
    rankings['A'], invalid = apply_fallback(source_rows, prior_contexts, rankings['CBF'], protocol['protocol_hash'])
    check(len(invalid) == meta['invalid_outputs'], 'A invalid count mismatch')
    data = ROOT.parent / 'Session 1/FAR-Trans'
    for filename, expected in protocol['source_sha256'].items():
        check(sha(data / filename) == expected, 'dataset source hash mismatch')
    assets, _, history, future, end, _ = load_data(data, '2021-06-01', 30)
    check(end == protocol['end_exclusive'] == '2021-07-01' and sorted(assets) == protocol['eligible_assets'],
          'truth reconstruction protocol mismatch')
    events = scan_recent_events(data, '2021-06-01', assets)
    latest_buy = {}
    for ctx in contexts:
        uid = ctx['user_id']
        check({a['id']: a['buy_count'] for a in ctx['history']} == dict(history.get(uid, {})),
              'context history differs from starter history')
        last = {}
        for timestamp, isin, kind in events.get(uid, []):
            check(timestamp < '2021-06-01', 'future event in rule inputs')
            if kind == 'Buy':
                last[isin] = max(last.get(isin, timestamp), timestamp)
        latest_buy[uid] = last
    rankings['B1'] = {ctx['user_id']: repeat_first(ctx, rankings['A'][ctx['user_id']],
                                                  latest_buy[ctx['user_id']], 'V2') for ctx in contexts}
    rankings['B2'] = {ctx['user_id']: buy_or_sell_repeat_first(
        ctx, rankings['A'][ctx['user_id']], events.get(ctx['user_id'], []), '2021-06-01') for ctx in contexts}
    DEST.mkdir()
    scored = {}
    for method in ('A', 'B1', 'B2'):
        responses = DEST / f'{method}_responses.jsonl'
        if method == 'A':
            source_by_user = {row['user_id']: row for row in source_rows}
            records = [dict(source_by_user[uid], protocol_hash=new_protocol['protocol_hash']) for uid in users]
        else:
            records = [{'user_id': uid, 'stage': 'ranker', 'protocol_hash': new_protocol['protocol_hash'],
                        'ranked_ids': rankings[method][uid]} for uid in users]
        with responses.open('x', encoding='utf-8') as stream:
            stream.write(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in records))
        output = DEST / method
        scored_protocol, metrics = starter_run(common, output, responses)
        check(scored_protocol['protocol_hash'] == new_protocol['protocol_hash'] and
              (output / 'contexts.jsonl').read_bytes() == (NEW / 'contexts.jsonl').read_bytes(),
              'method score used different all-eligible inputs')
        check(all(metrics['methods'][key] == values for key, values in new_metrics['methods'].items()),
              'method-scoring baselines changed')
        wanted = len(invalid) if method == 'A' else 0
        check(len(metrics['custom_failures']) == wanted, 'method fallback count mismatch')
        check(read_rankings(output / 'predictions.csv')['custom'] == rankings[method], 'scored rankings differ')
        scored[method] = {'metrics': metrics['methods']['custom'], 'fallbacks': wanted,
                          'derived_response_sha256': sha(responses)}
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids']) for ctx in contexts}
    nonempty = [index for index, uid in enumerate(users) if truth[uid]]
    scores = {name: [ndcg10(by_user[uid], truth[uid]) for uid in users] for name, by_user in rankings.items()}
    result = {
        'label': 'benchmark-method selection on fresh block 301–400; not used for HW3 conclusions',
        'users': 100, 'starter_positions': [301, 400], 'nonempty_truth_users': len(nonempty),
        'plan_sha256': sha(PLAN), 'original_protocol_hash': protocol['protocol_hash'],
        'all_eligible_protocol_hash': new_protocol['protocol_hash'], 'eligible_assets': count,
        'checks': {'same_users_order': same_users, 'first50_same_order': same_first50,
                   'baselines_identical': unchanged, 'all_eligible': all_assets},
        'rules': {'B1': 'unchanged repeat_first V2 using pre-cutoff Buy counts',
                  'B2': 'previously BOUGHT eligible assets only; most recent pre-cutoff Buy-or-Sell date; '
                        'ties: higher Buy count, then A order, then CBF order; remaining slots in A order'},
        'source_model_fallbacks': len(invalid), 'methods': {}, 'pairs': {},
        'statistical_conventions': {'bootstrap': '10000 paired resamples of all 100 users, Python random.Random(0) '
                                                'reset for each pair; percentile CI with linear interpolation',
                                    'wins_ties_losses': 'nonempty users only; exact score equality for ties',
                                    'sign_test': 'exact two-sided binomial p=0.5 over non-tied users',
                                    'empty_truth_policy': 'zero in primary mean'},
    }
    for name in (*LABELS, 'A', 'B1', 'B2'):
        all_mean = mean(scores[name])
        nonempty_mean = mean([scores[name][i] for i in nonempty])
        reference = scored[name]['metrics'] if name in scored else new_metrics['methods'][LABELS[name]]
        check(math.isclose(all_mean, reference['ndcg_at_10'], abs_tol=1e-15) and
              math.isclose(nonempty_mean, reference['ndcg_at_10_nonempty'], abs_tol=1e-15),
              'analysis did not reproduce starter score')
        result['methods'][name] = {'ndcg_at_10_all': all_mean, 'ndcg_at_10_nonempty': nonempty_mean,
                                   'nonempty_truth_users': len(nonempty),
                                   'fallbacks': scored[name]['fallbacks'] if name in scored else 0,
                                   'seconds_per_user': meta['wall_seconds_whole_arm'] / 100 if name == 'A' else None}
    for left, right in (('B2', 'B1'), ('B1', 'Latest buy or sell'), ('B2', 'Latest buy or sell'), ('B1', 'A')):
        differences = [a - b for a, b in zip(scores[left], scores[right])]
        result['pairs'][f'{left} - {right}'] = {'mean_difference_all_100': mean(differences),
                                               'bootstrap_95_ci': bootstrap(differences),
                                               'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty])}
    b1, b2 = mean(scores['B1']), mean(scores['B2'])
    selected = 'B2' if b2 > b1 else 'B1'
    result['selection'] = {'selected_variant': selected, 'criterion': 'higher all-100 mean nDCG@10; tie → B1',
                            'B1_ndcg_at_10': b1, 'B2_ndcg_at_10': b2, 'exact_tie': b1 == b2}
    sources = [PLAN, SOURCE / 'responses.jsonl', SOURCE / 'run_meta.json', SOURCE / 'run_provenance.json',
               OLD / 'protocol.json', OLD / 'contexts.jsonl', NEW / 'protocol.json', NEW / 'contexts.jsonl',
               ROOT / 'scripts/hw3_repeat_first.py', ROOT / 'starter.py']
    result['source_sha256'] = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    result['derived_response_sha256'] = {method: item['derived_response_sha256'] for method, item in scored.items()}
    result['analysis_script_sha256'] = sha(Path(__file__))
    check(all(sha(p) == expected for p, expected in frozen.items()), 'existing protected file changed')
    result['protected_existing_files_checked_unchanged'] = len(frozen)
    with (DEST / 'bench_select.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print('| Benchmark method | nDCG@10 all 100 | nDCG@10 nonempty | Nonempty users | Fallbacks | A seconds/user |')
    print('| --- | ---: | ---: | ---: | ---: | ---: |')
    for name, row in result['methods'].items():
        seconds = '—' if row['seconds_per_user'] is None else f'{row["seconds_per_user"]:.4f}'
        print(f'| {name} | {row["ndcg_at_10_all"]:.4f} | {row["ndcg_at_10_nonempty"]:.4f} | '
              f'{row["nonempty_truth_users"]} | {row["fallbacks"]} | {seconds} |')
    print('| Pair | Mean difference | Bootstrap 95% CI | W/T/L nonempty | Exact sign p |')
    print('| --- | ---: | --- | --- | ---: |')
    for name, comparison in result['pairs'].items():
        ci, counts = comparison['bootstrap_95_ci'], comparison['nonempty_wins_ties_losses']
        print(f'| {name} | {comparison["mean_difference_all_100"]:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] | '
              f'{counts["wins"]}/{counts["ties"]}/{counts["losses"]} | {counts["sign_test_p"]:.4f} |')
    print(f'Selected variant: {selected}; exact_tie={b1 == b2}')
    print(f'Protected existing files unchanged: {len(frozen)}')
    generated = [p for folder in (NEW, DEST) for p in folder.rglob('*') if p.is_file()]
    with (DEST / 'FILES_SHA256.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps({str(p.relative_to(ROOT)): sha(p) for p in sorted(generated)}, indent=2) + '\n')
    for path in (Path(__file__), *sorted(NEW.rglob('*.json')), *sorted(DEST.rglob('*.json'))):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')
    for path in sorted(DEST.glob('*_responses.jsonl')):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
