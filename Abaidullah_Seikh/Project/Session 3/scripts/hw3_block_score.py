#!/usr/bin/env python3
"""Planned held-out block scoring with official fallback and frozen C+R V2."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import scan_recent_events
from hw3_paired_analysis import apply_fallback, check, jsonl, sha
from hw3_repeat_first import repeat_first
from hw3_sparse_analysis import read_rankings

BASE = ROOT / 'outputs/block_201_300'
DEST = ROOT / 'outputs/block_scores'
EXPECTED = 'e126569ce481716d7039c495e2c7fedbbbe552e308b819b84c4be87b0eb5fe8d'
REGISTRATIONS = {
    'HW3_BLOCK_201_300.md': 'a99403c56472dde79a5767c7c85a34826ecbc34e8f9c0d8c1187df91a7d18bb6',
    'HW3_PLAN_C_IMPROVEMENT.md': 'fa99792f07dfdb8b48a63235ba8652a1aeca8a6080ac0cea0343445e69ad1402',
    'HW3_PLAN_C_IMPROVEMENT_CLARIFICATION.md': '68311cda32e608c805bc0cc1ca3f9b0b50b3c232bb2e1da5d58bf2c7a7fe96ab',
    'scripts/hw3_repeat_first.py': 'e1401a71475dcd50c0db56f01284f0086e76a6d12f1e0d9846c1a088a067c437',
}


def existing_hashes():
    paths = [p for folder in ('outputs', 'cohorts', 'scripts') for p in (ROOT / folder).rglob('*') if p.is_file()]
    paths += [p for p in ROOT.iterdir() if p.is_file() and p.name.startswith(('HW3_', 'run_hw3_'))]
    return {p: sha(p) for p in paths}


def main():
    check(not DEST.exists(), 'block_scores exists; refusing to overwrite')
    frozen = existing_hashes()
    for name, expected in REGISTRATIONS.items():
        check(sha(ROOT / name) == expected, 'registration or repeat-first hash mismatch')
    protocol = json.loads((BASE / 'protocol.json').read_text())
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [ctx['user_id'] for ctx in contexts]
    check(len(users) == len(set(users)) == 100 and users == protocol['users'] ==
          (ROOT / 'cohorts/block_201_300_users.txt').read_text().splitlines(), 'block cohort mismatch')
    check(protocol['protocol_hash'] == EXPECTED and protocol['cutoff'] == '2021-06-01'
          and protocol['end_exclusive'] == '2021-07-01' and protocol['candidate_count'] == 50
          and protocol['cohort_selection'] == 'warm' and not protocol['exclude_seen'], 'block protocol mismatch')
    baseline = json.loads((BASE / 'metrics.json').read_text())
    baseline_rankings = read_rankings(BASE / 'predictions.csv')
    cbf = baseline_rankings['cbf']
    rankings, invalid, times = {}, {}, {}
    for arm in ('A', 'C'):
        source = ROOT / 'outputs' / f'block_{arm}'
        rankings[arm], invalid[arm] = apply_fallback(jsonl(source / 'responses.jsonl'), contexts, cbf, EXPECTED)
        meta = json.loads((source / 'run_meta.json').read_text())
        provenance = json.loads((source / 'run_provenance.json').read_text())
        check(provenance['exit_code'] == 0 and bool(provenance.get('end_time')) and meta['users'] == 100,
              'block inference incomplete')
        check(meta['invalid_outputs'] == len(invalid[arm]), 'recorded invalid count mismatch')
        times[arm] = meta['wall_seconds_whole_arm'] / 100
    DEST.mkdir()
    summary = {'label': 'held-out development block; reported separately, not pooled',
               'users': 100, 'starter_positions': [201, 300], 'protocol_hash': EXPECTED,
               'nonempty_truth_users': baseline['methods']['cbf']['nonempty_truth_users'],
               'C_plus_R_variant': 'V2, unchanged, selected on main 200 only',
               'scoring_rule': 'starter --on-invalid fallback', 'methods': {},
               'registration_sha256': REGISTRATIONS, 'score_script_sha256': sha(Path(__file__))}
    for name, key in (('Latest buy or sell', 'latest_buy_or_sell'), ('Latest buy', 'latest_buy'),
                       ('Popularity', 'popularity'), ('CBF', 'cbf')):
        summary['methods'][name] = dict(baseline['methods'][key], invalid_rows=0, fallbacks=0,
                                        seconds_per_user=None, rule_overhead_unmeasured=False)

    def score(arm, response, output_name, expected_invalid):
        output = DEST / output_name
        check(not output.exists(), 'block score directory exists; refusing to overwrite')
        command = [sys.executable, str(ROOT / 'starter.py'), 'run', '--stage', 'ranker',
                   '--responses', str(response), '--on-invalid', 'fallback',
                   '--users-file', 'cohorts/block_201_300_users.txt', '--cutoff', '2021-06-01',
                   '--horizon-days', '30', '--cohort', 'warm', '--data-dir', '../Session 1/FAR-Trans',
                   '--output-dir', str(output)]
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        check(completed.returncode == 0, f'{arm} scoring exit code {completed.returncode}')
        metrics = json.loads((output / 'metrics.json').read_text())
        check(metrics['protocol_hash'] == EXPECTED and (output / 'contexts.jsonl').read_bytes() ==
              (BASE / 'contexts.jsonl').read_bytes(), 'regenerated block protocol or contexts differ')
        check(all(metrics['methods'][key] == values for key, values in baseline['methods'].items()),
              'regenerated baseline metrics differ')
        check(len(metrics['custom_failures']) == expected_invalid, 'fallback count mismatch')
        check(read_rankings(output / 'predictions.csv')['custom'] == rankings[arm], 'scored rankings differ')
        summary['methods'][arm] = dict(metrics['methods']['custom'], invalid_rows=expected_invalid,
                                       fallbacks=expected_invalid, seconds_per_user=times.get(arm, times['C']),
                                       rule_overhead_unmeasured=arm == 'C+R')

    for arm in ('A', 'C'):
        score(arm, ROOT / 'outputs' / f'block_{arm}/responses.jsonl', arm, len(invalid[arm]))
    events = scan_recent_events(ROOT.parent / 'Session 1/FAR-Trans', protocol['cutoff'], set(protocol['eligible_assets']))
    latest = {}
    for uid in users:
        last = {}
        for timestamp, isin, kind in events.get(uid, []):
            check(timestamp < protocol['cutoff'], 'future event in repeat-first history')
            if kind == 'Buy':
                last[isin] = max(last.get(isin, timestamp), timestamp)
        latest[uid] = last
    rankings['C+R'] = {ctx['user_id']: repeat_first(ctx, rankings['C'][ctx['user_id']],
                                                  latest[ctx['user_id']], 'V2') for ctx in contexts}
    derived = DEST / 'C_plus_R_responses.jsonl'
    with derived.open('x', encoding='utf-8') as stream:
        for uid in users:
            stream.write(json.dumps({'user_id': uid, 'stage': 'ranker', 'protocol_hash': EXPECTED,
                                     'ranked_ids': rankings['C+R'][uid]}) + '\n')
    score('C+R', derived, 'C_plus_R', 0)
    check(all(sha(path) == expected for path, expected in frozen.items()), 'existing protected file changed')
    sources = [BASE / 'protocol.json', BASE / 'contexts.jsonl', BASE / 'metrics.json',
               ROOT / 'outputs/block_A/responses.jsonl', ROOT / 'outputs/block_C/responses.jsonl']
    summary['source_sha256'] = {str(path.relative_to(ROOT)): sha(path) for path in sources}
    summary['C_plus_R_responses_sha256'] = sha(derived)
    summary['protected_existing_files_checked_unchanged'] = len(frozen)
    with (DEST / 'scoring_summary.json').open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(summary, indent=2) + '\n')
    print('| Held-out method | nDCG@10 all 100 | nDCG@10 nonempty | Nonempty users | Fallbacks | Seconds/user |')
    print('| --- | ---: | ---: | ---: | ---: | --- |')
    for name, row in summary['methods'].items():
        seconds = '—' if row['seconds_per_user'] is None else f'{row["seconds_per_user"]:.4f}'
        if row['rule_overhead_unmeasured']:
            seconds += ' + unmeasured rule'
        print(f'| {name} | {row["ndcg_at_10"]:.4f} | {row["ndcg_at_10_nonempty"]:.4f} | '
              f'{row["nonempty_truth_users"]} | {row["fallbacks"]} | {seconds} |')
    print(f'scripts/hw3_block_score.py SHA-256: {sha(Path(__file__))}')
    for path in sorted(DEST.rglob('*.json')):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')
    print(f'{derived.relative_to(ROOT)} SHA-256: {sha(derived)}')


if __name__ == '__main__':
    main()
