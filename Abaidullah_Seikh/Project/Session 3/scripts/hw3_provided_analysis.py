#!/usr/bin/env python3
"""Convert, independently score, and analyse the frozen provided-ranker run."""
import csv
from datetime import date, datetime
import importlib.util
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

BASE = ROOT / 'outputs/baseline_200'
FINAL = ROOT / 'outputs/final_200'
PROVIDED = ROOT / 'outputs/provided_llm_200'
EXPECTED = 'd46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697'
RANKER_HASH = '7c6b81794f7da10aab053074d86525b63d64aef10a08ff54ff5b6b8fa5de9f24'


def mean(values):
    return sum(values) / len(values)


def saved_rankings(path):
    groups = {}
    with path.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            groups.setdefault(row['method'], {}).setdefault(row['user_id'], []).append(
                (int(row['rank']), row['ISIN']))
    result = {}
    for method, by_user in groups.items():
        result[method] = {}
        for uid, rows in by_user.items():
            rows.sort()
            check([rank for rank, _ in rows] == list(range(1, 11)), 'saved ranking length mismatch')
            result[method][uid] = [asset for _, asset in rows]
    return result


def main():
    new_files = [FINAL / name for name in
                 ('P_responses.jsonl', 'MANIFEST_P.json', 'provided_analysis.json', 'score_P.txt')]
    evaluation = FINAL / 'evaluation_P'
    check(not evaluation.exists() and all(not path.exists() for path in new_files),
          'new provided scoring output already exists; refusing to overwrite')
    existing = [path for folder in ('outputs', 'cohorts', 'scripts')
                for path in (ROOT / folder).rglob('*') if path.is_file()]
    existing += [path for path in ROOT.iterdir() if path.is_file() and
                 path.name.startswith(('HW3_', 'run_hw3_'))]
    frozen = {path: sha(path) for path in existing}
    protocol = json.loads((BASE / 'protocol.json').read_text())
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == 200 and users == protocol['users']
          and protocol['protocol_hash'] == EXPECTED, 'baseline cohort or protocol mismatch')
    provenance = json.loads((PROVIDED / 'run_provenance.json').read_text())
    check(provenance['exit_code'] == 0 and bool(provenance.get('end_time')), 'provided run incomplete')
    ranker_path = Path(provenance['script'])
    check(provenance['script_sha256'] == sha(ranker_path) == RANKER_HASH, 'ranker hash mismatch')
    check(provenance['starter_sha256'] == sha(ROOT / 'starter.py'), 'starter hash mismatch')
    for filename, expected in provenance['support_sources_sha256'].items():
        check(sha(ranker_path.parent / filename) == expected, 'provided support-source hash mismatch')
    verified = provenance['input_verification']
    check(verified['same_users_in_order'] and verified['same_candidate_sets'], 'prepared input mismatch')
    for filename, expected in verified['sha256'].items():
        check(sha(ROOT / filename) == expected, 'verified input source changed')
    source = PROVIDED / 'final_responses.jsonl'
    records = jsonl(source)
    indexed = {row['user_id']: row for row in records}
    coverage = len(records) == len(indexed) == 200 and set(indexed) == set(users)
    print(f'Canonical responses: rows={len(records)} unique_users={len(indexed)} same_users={coverage}', flush=True)
    check(coverage, 'canonical response coverage mismatch')
    manifest = json.loads((PROVIDED / 'run_manifest.json').read_text())
    check(manifest['users'] == users, 'provided manifest user order mismatch')
    check(manifest['cutoff'] == protocol['cutoff'] and manifest['end_exclusive'] == protocol['end_exclusive']
          and manifest['candidate_count'] == protocol['candidate_count'] and manifest['repeat_allowed']
          and manifest['data_sha256'] == protocol['source_sha256'], 'provided manifest data policy mismatch')
    check(manifest['runtime']['shuffle_seed'] is None and manifest['runtime']['history_events'] == 15,
          'provided run differs from verified prepare-only settings')
    own_predictions = saved_rankings(PROVIDED / 'predictions.csv')
    base_predictions = saved_rankings(BASE / 'predictions.csv')
    cbf = base_predictions['cbf']
    check(own_predictions['candidate_order_first10'] == cbf, 'matched candidate-order control differs from CBF')
    check(all(own_predictions['candidate_order_first10'][ctx['user_id']] ==
              [asset['id'] for asset in ctx['candidate_assets'][:10]] for ctx in contexts),
          'provided matched control differs from frozen candidate order')
    # Import the provided parser only: its inference runtime is not instantiated.
    sys.path.insert(0, str(ranker_path.parent))
    spec = importlib.util.spec_from_file_location('provided_ranker_parser', ranker_path)
    provided_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provided_module)
    derived, invalid_positions = [], []
    for position, ctx in enumerate(contexts, 1):
        uid = ctx['user_id']
        row = indexed[uid]
        allowed = {asset['id'] for asset in ctx['candidate_assets']}
        try:
            ranking, repaired = provided_module.parse_ranking(row.get('raw_response'), allowed)
            invalid = False
            check(repaired == row['parse_repaired'], 'provided parse-repair flag mismatch')
        except (ValueError, TypeError, KeyError):
            ranking, invalid = [], True
        check(invalid == bool(row['fallback']), 'parsed invalid status differs from saved fallback flag')
        effective = cbf[uid] if invalid else ranking
        check(effective == own_predictions['llmrank'][uid], 'parsed/fallback ranking differs from provided predictions')
        if invalid:
            invalid_positions.append(position)
        derived.append({'user_id': uid, 'stage': 'ranker', 'protocol_hash': EXPECTED, 'ranked_ids': ranking})
    check(len(invalid_positions) == manifest['runtime']['raw_invalid_count'] == len(manifest['failures']),
          'provided invalid/fallback count mismatch')
    p_file = FINAL / 'P_responses.jsonl'
    with p_file.open('x', encoding='utf-8') as stream:
        stream.write(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in derived))
    p_manifest = {
        'source': str(source.relative_to(ROOT)), 'source_sha256': sha(source),
        'source_predictions': str((PROVIDED / 'predictions.csv').relative_to(ROOT)),
        'source_predictions_sha256': sha(PROVIDED / 'predictions.csv'),
        'original_hash': None, 'new_protocol_hash': EXPECTED,
        'reason': 'Provided canonical responses contain no protocol hash or ranked_ids; '
                  'users, candidate identities/order, data hashes, and matched control verified identical.',
        'schema_conversion': 'Valid raw responses parsed with unchanged provided ranker.parse_ranking; '
                             'all effective rankings verified identical to saved llmrank predictions. '
                             'Invalid responses encoded as empty ranked_ids to preserve invalid status '
                             'and reproduce full CBF fallback in starter scoring. No regeneration or repair added.',
        'rebound_rows': {'count': 200, 'baseline_order_positions': [1, 200], 'from_protocol_hash': None},
        'rows': 200, 'unique_users': 200, 'invalid_rows': len(invalid_positions),
        'invalid_positions': invalid_positions, 'script_sha256': RANKER_HASH,
        'starter_sha256': provenance['starter_sha256'],
        'input_verification': verified, 'output_sha256': sha(p_file),
        'scoring_rule': 'starter --on-invalid fallback',
    }
    with (FINAL / 'MANIFEST_P.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(p_manifest, indent=2) + '\n')
    days = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    command = [sys.executable, str(ROOT / 'starter.py'), 'run', '--data-dir', '../Session 1/FAR-Trans',
               '--cutoff', protocol['cutoff'], '--horizon-days', str(days), '--max-users', str(len(users)),
               '--cohort', protocol['cohort_selection'], '--candidate-count', str(protocol['candidate_count']),
               '--stage', 'ranker', '--responses', str(p_file), '--on-invalid', 'fallback',
               '--output-dir', str(evaluation)]
    if protocol['exclude_seen']:
        command.append('--exclude-seen')
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    check(completed.returncode == 0, f'starter scoring exit code {completed.returncode}')
    scoring = json.loads((evaluation / 'metrics.json').read_text())
    check(scoring['protocol_hash'] == EXPECTED and
          (evaluation / 'contexts.jsonl').read_bytes() == (BASE / 'contexts.jsonl').read_bytes(),
          'scoring protocol or contexts mismatch')
    row = scoring['methods']['custom']
    own_metrics = json.loads((PROVIDED / 'metrics.json').read_text())
    matches = all(f'{row[key]:.4f}' == f'{own_metrics["llmrank"][key]:.4f}'
                  for key in ('ndcg_at_10', 'ndcg_at_10_nonempty'))
    check(matches and all(math.isclose(row[key], own_metrics['llmrank'][key], abs_tol=1e-15)
                          for key in ('ndcg_at_10', 'ndcg_at_10_nonempty')), 'provided and starter scores differ')
    check(len(scoring['custom_failures']) == len(invalid_positions), 'starter fallback count differs')
    score_line = (f'P: nDCG_all_200={row["ndcg_at_10"]:.4f} nDCG_nonempty={row["ndcg_at_10_nonempty"]:.4f} '
                  f'invalid_rows={len(invalid_positions)} fallbacks={len(scoring["custom_failures"])}\n')
    with (FINAL / 'score_P.txt').open('x', encoding='utf-8') as stream:
        stream.write(score_line)
    print(score_line, end='', flush=True)
    print(f'Matches provided own llmrank metrics to 4 decimals: {matches}', flush=True)

    data = ROOT.parent / 'Session 1/FAR-Trans'
    for filename, expected in protocol['source_sha256'].items():
        check(sha(data / filename) == expected, 'dataset source changed')
    assets, _, _, future, end, _ = load_data(data, protocol['cutoff'], days)
    check(end == protocol['end_exclusive'], 'truth window mismatch')
    truth = {ctx['user_id']: future.get(ctx['user_id'], set()) & set(ctx['eligible_asset_ids']) for ctx in contexts}
    nonempty = [i for i, uid in enumerate(users) if truth[uid]]
    check(len(nonempty) == 24, 'nonempty truth denominator mismatch')
    rankings = {name: base_predictions[key] for name, key in
                (('Latest buy or sell', 'latest_buy_or_sell'), ('Latest buy', 'latest_buy'),
                 ('Popularity', 'popularity'), ('CBF', 'cbf'))}
    fallbacks = {name: 0 for name in rankings}
    for arm in ('A', 'C'):
        rankings[arm], invalid = apply_fallback(jsonl(FINAL / f'{arm}_responses.jsonl'), contexts, cbf, EXPECTED)
        fallbacks[arm] = len(invalid)
    repeat_results = json.loads((FINAL / 'repeat_first.json').read_text())
    check(repeat_results['selection']['chosen_C_plus_R'] == 'V2', 'repeat-first selection mismatch')
    events = scan_recent_events(data, protocol['cutoff'], assets)
    latest = {}
    for uid in users:
        last = {}
        for timestamp, isin, kind in events.get(uid, []):
            if kind == 'Buy':
                last[isin] = max(last.get(isin, timestamp), timestamp)
        latest[uid] = last
    for name, source_arm, variant in (('C+R', 'C', 'V2'), ('A+R', 'A', 'V1')):
        rankings[name] = {ctx['user_id']: repeat_first(ctx, rankings[source_arm][ctx['user_id']],
                                                    latest[ctx['user_id']], variant) for ctx in contexts}
        fallbacks[name] = fallbacks[source_arm]
    rankings['P'], p_invalid = apply_fallback(derived, contexts, cbf, EXPECTED)
    check(p_invalid == invalid_positions and rankings['P'] == own_predictions['llmrank'],
          'analysed provided rankings mismatch')
    fallbacks['P'] = len(p_invalid)
    scores = {name: [ndcg10(by_user[uid], truth[uid]) for uid in users] for name, by_user in rankings.items()}
    check(math.isclose(mean(scores['P']), row['ndcg_at_10'], abs_tol=1e-15), 'provided analysis score sanity mismatch')
    for name, reference in (('C+R', 'V2'), ('A+R', 'A+R')):
        check(math.isclose(mean(scores[name]), repeat_results['methods'][reference]['ndcg_at_10_all'], abs_tol=1e-15),
              'repeat-first reconstruction score mismatch')
    a_first = json.loads((ROOT.parent / 'Session 2/outputs/arm_A/run_meta.json').read_text())
    a_second = json.loads((ROOT / 'outputs/arm_A_101_200/run_meta.json').read_text())
    c_meta = json.loads((ROOT / 'outputs/arm_C2_200/run_meta.json').read_text())
    check(a_first['users'] + a_second['users'] == 200 and c_meta['users'] == 200, 'timing denominator mismatch')
    a_seconds = (a_first['wall_seconds_whole_arm'] + a_second['wall_seconds_whole_arm']) / 200
    c_seconds = c_meta['wall_seconds_whole_arm'] / 200
    p_wall = (datetime.fromisoformat(provenance['end_time']) - datetime.fromisoformat(provenance['start_time'])).total_seconds()
    timing = {'A': a_seconds, 'C': c_seconds, 'C+R': c_seconds, 'A+R': a_seconds, 'P': p_wall / 200}
    pairs = {}
    for reference in ('CBF', 'A', 'C', 'C+R', 'Latest buy or sell'):
        differences = [a - b for a, b in zip(scores['P'], scores[reference])]
        pairs[f'P - {reference}'] = {'mean_difference_all_200': mean(differences),
                                   'bootstrap_95_ci': bootstrap(differences),
                                   'nonempty_wins_ties_losses': wtl([differences[i] for i in nonempty])}
    hits = [len(set(rankings['P'][uid]) & truth[uid]) for uid in users]
    same_order = sum(rankings['P'][uid] == cbf[uid] for uid in users)
    same_set = sum(set(rankings['P'][uid]) == set(cbf[uid]) for uid in users)
    overlap = mean([len(set(rankings['P'][uid]) & set(cbf[uid])) for uid in users])
    result = {
        'label': 'development results', 'users': 200, 'nonempty_truth_users': 24, 'protocol_hash': EXPECTED,
        'provided_own_metrics_match': matches, 'pairs': pairs,
        'statistical_conventions': {'bootstrap': '10000 paired resamples of all 200 users; Python random.Random(0) '
                                                'reset for each pair; percentile CI with linear interpolation',
                                    'sign_test': 'exact two-sided binomial p=0.5 over non-tied users',
                                    'wins_ties_losses': '24 nonempty users; exact score equality for ties'},
        'P_hit_users': sum(n > 0 for n in hits), 'P_total_hits_top10': sum(hits),
        'P_copying': {'same_order': same_order, 'same_set_including_same_order': same_set,
                      'same_set_different_order': same_set - same_order, 'mean_overlap_out_of_10': overlap},
        'P_invalid': {'count': len(invalid_positions), 'positions': invalid_positions,
                       'nonempty_truth_by_position': [{'position': pos, 'nonempty_truth': bool(truth[users[pos - 1]])}
                                                     for pos in invalid_positions]},
        'P_wall_seconds': p_wall, 'P_seconds_per_user': p_wall / 200, 'P_device': manifest['runtime']['device'],
        'timing_scope': 'A is combined HW2-first100 and HW3-second100 generation-loop time /200; C is generation-loop '
                        'time /200; C+R and A+R show the source model component only, rule overhead unmeasured. '
                        'P is full command-wall time including loading/preparation/scoring. These timing scopes differ.',
        'methods': {name: {'ndcg_at_10_all': mean(values),
                           'ndcg_at_10_nonempty': mean([values[i] for i in nonempty]), 'fallbacks': fallbacks[name],
                           'seconds_per_user': timing.get(name),
                           'rule_overhead_unmeasured': name in ('C+R', 'A+R')}
                    for name, values in scores.items()},
        'source_sha256': {str(path.relative_to(ROOT)): sha(path) for path in
                          (source, PROVIDED / 'predictions.csv', PROVIDED / 'metrics.json',
                           PROVIDED / 'run_manifest.json', PROVIDED / 'run_provenance.json',
                           FINAL / 'repeat_first.json', ROOT / 'scripts/hw3_repeat_first.py')},
        'analysis_script_sha256': sha(Path(__file__)),
    }
    check(all(sha(path) == expected for path, expected in frozen.items()), 'existing protected file changed')
    result['protected_existing_files_checked_unchanged'] = len(frozen)
    with (FINAL / 'provided_analysis.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print('| Pair | Mean difference | Bootstrap 95% CI | W/T/L nonempty | Exact sign p |')
    print('| --- | ---: | --- | --- | ---: |')
    for name, comparison in pairs.items():
        ci, counts = comparison['bootstrap_95_ci'], comparison['nonempty_wins_ties_losses']
        print(f'| {name} | {comparison["mean_difference_all_200"]:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] | '
              f'{counts["wins"]}/{counts["ties"]}/{counts["losses"]} | {counts["sign_test_p"]:.4f} |')
    print(f'P hit users={result["P_hit_users"]}; total hits={result["P_total_hits_top10"]}; '
          f'same CBF order={same_order}; same set={same_set}; different order={same_set-same_order}; mean overlap={overlap:.4f}/10')
    print('Invalid positions/nonempty: ' + ', '.join(f'{item["position"]}:{item["nonempty_truth"]}'
          for item in result['P_invalid']['nonempty_truth_by_position']))
    print(f'P command wall seconds={p_wall:.4f}; seconds/user={p_wall/200:.4f}; device={result["P_device"]}')
    print('| Main-200 method | nDCG@10 all | nDCG@10 nonempty | Fallbacks | Seconds/user |')
    print('| --- | ---: | ---: | ---: | --- |')
    for name, method in result['methods'].items():
        seconds = '—' if method['seconds_per_user'] is None else f'{method["seconds_per_user"]:.4f}'
        if method['rule_overhead_unmeasured']:
            seconds += ' + unmeasured rule'
        print(f'| {name} | {method["ndcg_at_10_all"]:.4f} | {method["ndcg_at_10_nonempty"]:.4f} | '
              f'{method["fallbacks"]} | {seconds} |')
    print(f'Protected existing files unchanged: {len(frozen)}')
    for path in (Path(__file__), *new_files, evaluation / 'protocol.json', evaluation / 'metrics.json'):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
