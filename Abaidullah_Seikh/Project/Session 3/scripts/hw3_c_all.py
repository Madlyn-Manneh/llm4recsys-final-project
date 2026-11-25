#!/usr/bin/env python3
"""One pre-registered all-eligible repeat-first variant; no model calls or selection."""
from datetime import date
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import load_data, ndcg10, scan_recent_events
from hw3_paired_analysis import apply_fallback, bootstrap, check, jsonl, sha, wtl
from hw3_repeat_first import repeat_first
from hw3_sparse_analysis import read_rankings

PLAN = ROOT / 'HW3_PLAN_C_ALL.md'
DEST = ROOT / 'outputs/all_cand_scores'
BASELINES = {'Latest buy or sell': 'latest_buy_or_sell', 'Latest buy': 'latest_buy',
             'Popularity': 'popularity', 'CBF': 'cbf'}
SETS = {
    'main_200': {'old': 'outputs/baseline_200', 'new': 'outputs/all_cand_main_200', 'n': 200,
                 'A': 'outputs/final_200/A_responses.jsonl', 'C': 'outputs/arm_C2_200/responses.jsonl',
                 'users_file': None, 'previous': 'outputs/final_200/repeat_first.json'},
    'sparse_120': {'old': 'outputs/sparse_baseline_120', 'new': 'outputs/all_cand_sparse_120', 'n': 120,
                    'A': 'outputs/sparse_A/responses.jsonl', 'C': 'outputs/sparse_C/responses.jsonl',
                    'users_file': 'cohorts/sparse_window_users.txt',
                    'previous': 'outputs/sparse_scores/repeat_first.json'},
    'block_100': {'old': 'outputs/block_201_300', 'new': 'outputs/all_cand_block_100', 'n': 100,
                   'A': 'outputs/block_A/responses.jsonl', 'C': 'outputs/block_C/responses.jsonl',
                   'users_file': 'cohorts/block_201_300_users.txt',
                   'previous': 'outputs/block_scores/scoring_summary.json'},
}
METHOD_KEYS = {'A': 'A', 'C': 'C', 'C+R': 'C_R_50', 'A+R-all': 'A_R_all', 'C+R-all': 'C_R_all'}


def mean(values):
    return sum(values) / len(values)


def starter_run(common, output, responses=None):
    check(not output.exists(), 'all-candidate scoring directory exists; refusing to overwrite')
    command = [sys.executable, str(ROOT / 'starter.py'), 'run', *common, '--output-dir', str(output)]
    if responses is not None:
        command += ['--stage', 'ranker', '--responses', str(responses), '--on-invalid', 'fallback']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    check(result.returncode == 0, f'starter scoring exit code {result.returncode}')
    return json.loads((output / 'protocol.json').read_text()), json.loads((output / 'metrics.json').read_text())


def main():
    check(sha(PLAN) == 'f3aace44fa9c19d9ef39b15781a5b0063d1939bcfac9ebaf5b667c0290229caf',
          'all-candidate pre-registration hash mismatch')
    check(sha(ROOT / 'scripts/hw3_repeat_first.py') ==
          'e1401a71475dcd50c0db56f01284f0086e76a6d12f1e0d9846c1a088a067c437', 'repeat-first source hash mismatch')
    check(not DEST.exists() and all(not (ROOT / spec['new']).exists() for spec in SETS.values()),
          'an all-candidate output directory exists; refusing to overwrite')
    protected = [p for folder in ('outputs', 'cohorts', 'scripts') for p in (ROOT / folder).rglob('*') if p.is_file()]
    protected += [p for p in ROOT.iterdir() if p.is_file() and p.name.startswith(('HW3_', 'run_hw3_'))]
    frozen = {p: sha(p) for p in protected}
    # All sets and the single V2 variant are fixed before any new score inspection.
    prepared = {}
    for name, spec in SETS.items():
        old = ROOT / spec['old']
        protocol = json.loads((old / 'protocol.json').read_text())
        old_contexts = jsonl(old / 'contexts.jsonl')
        count = len(protocol['eligible_assets'])
        horizon = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
        common = ['--data-dir', '../Session 1/FAR-Trans', '--cutoff', protocol['cutoff'],
                  '--horizon-days', str(horizon), '--cohort', protocol['cohort_selection'],
                  '--candidate-count', str(count)]
        check(not protocol['exclude_seen'], 'unexpected exclude-seen policy')
        if spec['users_file'] is None:
            common += ['--max-users', str(spec['n'])]
        else:
            common += ['--users-file', spec['users_file']]
        new = ROOT / spec['new']
        new_protocol, new_metrics = starter_run(common, new)
        contexts = jsonl(new / 'contexts.jsonl')
        users = [ctx['user_id'] for ctx in contexts]
        same_users = len(users) == len(set(users)) == spec['n'] and users == protocol['users']
        first50 = len(contexts) == len(old_contexts) and all(
            [a['id'] for a in ctx['candidate_assets'][:50]] == [a['id'] for a in prior['candidate_assets']]
            for ctx, prior in zip(contexts, old_contexts))
        all_eligible = new_protocol['candidate_count'] == count and all(
            len(ctx['candidate_assets']) == count and
            {a['id'] for a in ctx['candidate_assets']} == set(protocol['eligible_assets']) for ctx in contexts)
        print(f'{name}: same_users_order={same_users}; first50_same_order={first50}; all_eligible={all_eligible}', flush=True)
        print(f'{name}: protocol_hash={new_protocol["protocol_hash"]}; eligible_assets={count}', flush=True)
        check(same_users and first50 and all_eligible, 'expanded candidate input mismatch')
        old_metrics = json.loads((old / 'metrics.json').read_text())
        unchanged = new_metrics['methods'] == old_metrics['methods']
        print(f'{name}: baselines_unchanged={unchanged}', flush=True)
        check(unchanged, 'all-candidate baseline metrics changed')
        prepared[name] = dict(spec=spec, old=old, new=new, protocol=protocol, new_protocol=new_protocol,
                              old_contexts=old_contexts, contexts=contexts, users=users, common=common,
                              metrics=new_metrics, horizon=horizon, eligible_count=count)
    DEST.mkdir()
    truth_cache = {}
    events_cache = {}
    results = {'label': 'development results; separate windows, no pooling', 'variant_count': 1,
               'selection': 'none', 'plan_sha256': sha(PLAN),
               'repeat_first_script_sha256': sha(ROOT / 'scripts/hw3_repeat_first.py'),
               'analysis_script_sha256': sha(Path(__file__)),
               'interpretation': 'C was generated from 50-candidate prompts and is unchanged. '
                                 'This is a deterministic all-eligible repeat-first post-processing comparison, '
                                 'not a new all-candidate LLM run.',
               'statistical_conventions': {
                   'bootstrap': '10000 paired user resamples per window; Python random.Random(0) reset per pair; '
                                'percentile intervals with linear interpolation',
                   'wins_ties_losses': 'nonempty-truth users only; exact equality for ties',
                   'sign_test': 'exact two-sided binomial p=0.5 on non-tied users',
                   'empty_truth_policy': 'zero in primary mean'}, 'windows': {}}
    for name, info in prepared.items():
        spec, protocol = info['spec'], info['protocol']
        contexts, old_contexts, users = info['contexts'], info['old_contexts'], info['users']
        baseline = read_rankings(info['new'] / 'predictions.csv')
        rankings = {label: baseline[key] for label, key in BASELINES.items()}
        source_rows, source_invalid = {}, {}
        for arm in ('A', 'C'):
            source_rows[arm] = jsonl(ROOT / spec[arm])
            rankings[arm], source_invalid[arm] = apply_fallback(
                source_rows[arm], old_contexts, rankings['CBF'], protocol['protocol_hash'])
        data = ROOT.parent / 'Session 1/FAR-Trans'
        key = (protocol['cutoff'], info['horizon'])
        if key not in truth_cache:
            loaded = load_data(data, protocol['cutoff'], info['horizon'])
            truth_cache[key] = (loaded[0], loaded[2], loaded[3], loaded[4])
            del loaded
        assets, history, future, end = truth_cache[key]
        check(end == protocol['end_exclusive'] and sorted(assets) == protocol['eligible_assets'],
              'expanded evaluation truth protocol mismatch')
        if protocol['cutoff'] not in events_cache:
            events_cache[protocol['cutoff']] = scan_recent_events(data, protocol['cutoff'], assets)
        events = events_cache[protocol['cutoff']]
        latest = {}
        for ctx in contexts:
            uid = ctx['user_id']
            check({a['id']: a['buy_count'] for a in ctx['history']} == dict(history.get(uid, {})),
                  'context Buy history differs from starter history')
            last = {}
            for timestamp, isin, kind in events.get(uid, []):
                check(timestamp < protocol['cutoff'], 'future information in repeat-first input')
                if kind == 'Buy':
                    last[isin] = max(last.get(isin, timestamp), timestamp)
            latest[uid] = last
        rankings['C+R'] = {ctx['user_id']: repeat_first(ctx, rankings['C'][ctx['user_id']],
                                                       latest[ctx['user_id']], 'V2') for ctx in old_contexts}
        for label, source_arm in (('A+R-all', 'A'), ('C+R-all', 'C')):
            rankings[label] = {ctx['user_id']: repeat_first(ctx, rankings[source_arm][ctx['user_id']],
                                                          latest[ctx['user_id']], 'V2') for ctx in contexts}
        destination = DEST / name
        destination.mkdir()
        score_artifacts = {}
        for label, method_key in METHOD_KEYS.items():
            response_path = destination / f'{method_key}_responses.jsonl'
            # A/C retain their original model-ranked IDs, including invalid rows.
            # Only the protocol hash is rebound; the starter applies its fallback.
            if label in ('A', 'C'):
                indexed = {r['user_id']: r for r in source_rows[label]}
                records = [dict(indexed[uid], protocol_hash=info['new_protocol']['protocol_hash']) for uid in users]
            else:
                records = [{'user_id': uid, 'stage': 'ranker',
                            'protocol_hash': info['new_protocol']['protocol_hash'],
                            'ranked_ids': rankings[label][uid]} for uid in users]
            with response_path.open('x', encoding='utf-8') as stream:
                stream.write(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in records))
            scoring_folder = destination / method_key
            scored_protocol, metrics = starter_run(info['common'], scoring_folder, response_path)
            check(scored_protocol['protocol_hash'] == info['new_protocol']['protocol_hash'] and
                  (scoring_folder / 'contexts.jsonl').read_bytes() == (info['new'] / 'contexts.jsonl').read_bytes(),
                  'method scoring did not use the same all-candidate contexts')
            check(all(metrics['methods'][key] == row for key, row in info['metrics']['methods'].items()),
                  'method scoring baseline metrics changed')
            wanted_invalid = len(source_invalid[label]) if label in source_invalid else 0
            check(len(metrics['custom_failures']) == wanted_invalid, 'method fallback count mismatch')
            check(read_rankings(scoring_folder / 'predictions.csv')['custom'] == rankings[label],
                  'starter-scored ranking differs from derived ranking')
            score_artifacts[label] = {'metrics': metrics['methods']['custom'],
                                      'fallbacks': len(metrics['custom_failures']),
                                      'response_sha256': sha(response_path)}
        truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids']) for ctx in contexts}
        nonempty = [i for i, uid in enumerate(users) if truth[uid]]
        values = {label: [ndcg10(by_user[uid], truth[uid]) for uid in users] for label, by_user in rankings.items()}
        old_cr = json.loads((ROOT / spec['previous']).read_text())
        if name == 'block_100':
            previous_mean = old_cr['methods']['C+R']['ndcg_at_10']
        else:
            check(old_cr['selection']['chosen_C_plus_R'] == 'V2', 'previous selected variant differs from V2')
            previous_mean = old_cr['methods']['V2']['ndcg_at_10_all']
        check(math.isclose(mean(values['C+R']), previous_mean, abs_tol=1e-15), 'old 50-candidate C+R score mismatch')
        method_results = {}
        ordered_labels = [*BASELINES, 'A', 'C', 'C+R', 'A+R-all', 'C+R-all']
        for label in ordered_labels:
            scores = values[label]
            all_mean, nonempty_mean = mean(scores), mean([scores[i] for i in nonempty])
            if label in score_artifacts:
                scored = score_artifacts[label]['metrics']
                check(math.isclose(all_mean, scored['ndcg_at_10'], abs_tol=1e-15) and
                      math.isclose(nonempty_mean, scored['ndcg_at_10_nonempty'], abs_tol=1e-15),
                      'analysis did not reproduce starter scores')
            method_results[label] = {'ndcg_at_10_all': all_mean, 'ndcg_at_10_nonempty': nonempty_mean,
                                     'fallbacks': score_artifacts.get(label, {}).get('fallbacks', 0)}
        pairs = {}
        for reference in ('C+R', 'Latest buy or sell', 'A+R-all'):
            differences = [a - b for a, b in zip(values['C+R-all'], values[reference])]
            pairs[f'C+R-all - {reference}'] = {
                'mean_difference_all': mean(differences), 'bootstrap_95_ci': bootstrap(differences),
                'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty])}
        window_result = {
            'users': len(users), 'nonempty_truth_users': len(nonempty), 'eligible_assets': info['eligible_count'],
            'original_protocol_hash': protocol['protocol_hash'],
            'all_candidate_protocol_hash': info['new_protocol']['protocol_hash'],
            'same_users_in_order': True, 'first50_same_order': True, 'baselines_unchanged': True,
            'methods': method_results, 'pairs': pairs,
            'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in
                              (ROOT / spec['A'], ROOT / spec['C'], ROOT / spec['previous'],
                               info['old'] / 'contexts.jsonl', info['new'] / 'contexts.jsonl')},
            'source_model_invalid_counts': {arm: len(positions) for arm, positions in source_invalid.items()},
            'scored_response_sha256': {label: entry['response_sha256'] for label, entry in score_artifacts.items()},
        }
        results['windows'][name] = window_result
    check(all(sha(path) == expected for path, expected in frozen.items()), 'existing protected file changed')
    results['protected_existing_files_checked_unchanged'] = len(frozen)
    with (DEST / 'c_all.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(results, indent=2, allow_nan=False) + '\n')
    for name, row in results['windows'].items():
        print(f'\n{name}: users={row["users"]}; nonempty={row["nonempty_truth_users"]}; baselines_unchanged=True')
        print('| Method | nDCG@10 all | nDCG@10 nonempty |')
        print('| --- | ---: | ---: |')
        for label, score in row['methods'].items():
            print(f'| {label} | {score["ndcg_at_10_all"]:.4f} | {score["ndcg_at_10_nonempty"]:.4f} |')
        print('| Pair | Mean difference | Bootstrap 95% CI | W/T/L nonempty | Exact sign p |')
        print('| --- | ---: | --- | --- | ---: |')
        for label, comparison in row['pairs'].items():
            ci, counts = comparison['bootstrap_95_ci'], comparison['nonempty_wins_ties_losses']
            print(f'| {label} | {comparison["mean_difference_all"]:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] | '
                  f'{counts["wins"]}/{counts["ties"]}/{counts["losses"]} | {counts["sign_test_p"]:.4f} |')
    generated = []
    for spec in SETS.values():
        generated.extend(p for p in (ROOT / spec['new']).rglob('*') if p.is_file())
    generated.extend(p for p in DEST.rglob('*') if p.is_file())
    file_manifest = {str(path.relative_to(ROOT)): sha(path) for path in sorted(generated)}
    manifest_path = DEST / 'FILES_SHA256.json'
    with manifest_path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(file_manifest, indent=2) + '\n')
    print(f'Protected existing files unchanged: {len(frozen)}')
    print(f'New generated artifacts hashed: {len(file_manifest)}')
    for path in (PLAN, Path(__file__), DEST / 'c_all.json', manifest_path):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
