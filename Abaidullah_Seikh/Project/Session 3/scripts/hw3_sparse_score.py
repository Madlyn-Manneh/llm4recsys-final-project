#!/usr/bin/env python3
"""Score frozen sparse responses with starter fallback; print aggregates only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from starter import validate_ranking

EXPECTED = '5f470cfbb37d3985ea0996f564d059429b59fcd5dc747ff07632eb4e11589069'
BASE = ROOT / 'outputs/sparse_baseline_120'
DEST = ROOT / 'outputs/sparse_scores'
ARMS = ('A', 'C', 'oldC')


def check(condition, message):
    if not condition:
        print('FAIL: ' + message, flush=True)
        raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def main():
    check(not DEST.exists(), 'sparse_scores already exists; refusing to overwrite')
    contexts = jsonl(BASE / 'contexts.jsonl')
    users = [row['user_id'] for row in contexts]
    protocol = json.loads((BASE / 'protocol.json').read_text())
    cohort = (ROOT / 'cohorts/sparse_window_users.txt').read_text().splitlines()
    check(len(users) == len(set(users)) == 120 and users == protocol['users'] == cohort,
          'sparse cohort mismatch')
    check(protocol['protocol_hash'] == EXPECTED and protocol['cutoff'] == '2021-06-01'
          and protocol['end_exclusive'] == '2021-08-30' and protocol['candidate_count'] == 50
          and protocol['cohort_selection'] == 'warm' and not protocol['exclude_seen'],
          'sparse protocol mismatch')
    baseline = json.loads((BASE / 'metrics.json').read_text())
    source_paths = [ROOT / 'outputs' / f'sparse_{arm}' / 'responses.jsonl' for arm in ARMS]
    protected = [BASE / name for name in ('protocol.json', 'contexts.jsonl', 'metrics.json')]
    protected += source_paths + [ROOT / 'cohorts/sparse_window_users.txt', ROOT / 'HW3_PROTOCOL.md',
                                 ROOT / 'HW3_PROTOCOL_AMENDMENT1.md']
    frozen = {path: sha(path) for path in protected}
    invalid = {}
    for arm, path in zip(ARMS, source_paths):
        records = jsonl(path)
        indexed = {row['user_id']: row for row in records}
        check(len(records) == len(indexed) == 120 and set(indexed) == set(users),
              'source response coverage mismatch')
        invalid[arm] = 0
        for ctx in contexts:
            row = indexed[ctx['user_id']]
            check(row.get('protocol_hash') == EXPECTED and row.get('stage') == 'ranker',
                  'source response protocol or stage mismatch')
            try:
                validate_ranking(row['ranked_ids'], [a['id'] for a in ctx['candidate_assets']])
            except (ValueError, KeyError, TypeError):
                invalid[arm] += 1
        meta = json.loads((path.parent / 'run_meta.json').read_text())
        check(meta['invalid_outputs'] == invalid[arm], 'source invalid count mismatch')
    DEST.mkdir()
    summary = {'label': 'sparse development results', 'users': 120,
               'nonempty_truth_users': baseline['methods']['cbf']['nonempty_truth_users'],
               'protocol_hash': EXPECTED, 'scoring_rule': 'starter --on-invalid fallback',
               'methods': {}, 'sources_sha256': {str(p.relative_to(ROOT)): h for p, h in frozen.items()},
               'scoring_script_sha256': sha(Path(__file__))}
    for label, key in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'),
                       ('Latest buy or sell', 'latest_buy_or_sell'), ('Popularity', 'popularity')):
        summary['methods'][label] = dict(baseline['methods'][key], invalid_rows=0, fallbacks=0)
    for arm, path in zip(ARMS, source_paths):
        output = DEST / arm
        command = [sys.executable, str(ROOT / 'starter.py'), 'run',
                   '--stage', 'ranker', '--responses', str(path), '--on-invalid', 'fallback',
                   '--data-dir', '../Session 1/FAR-Trans', '--cutoff', '2021-06-01',
                   '--horizon-days', '90', '--users-file', 'cohorts/sparse_window_users.txt',
                   '--cohort', 'warm', '--output-dir', str(output)]
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        check(completed.returncode == 0, f'{arm} scoring exit code {completed.returncode}')
        metrics = json.loads((output / 'metrics.json').read_text())
        check(metrics['protocol_hash'] == EXPECTED, 'regenerated protocol hash mismatch')
        check((output / 'contexts.jsonl').read_bytes() == (BASE / 'contexts.jsonl').read_bytes(),
              'regenerated sparse contexts differ')
        check(all(metrics['methods'][key] == row for key, row in baseline['methods'].items()),
              'regenerated baseline metrics differ')
        failures = len(metrics['custom_failures'])
        check(failures == invalid[arm], 'fallback count differs from invalid count')
        row = metrics['methods']['custom']
        check(row['users'] == 120, 'evaluated count mismatch')
        summary['methods'][arm] = dict(row, invalid_rows=invalid[arm], fallbacks=failures)
        print(f'{arm}: nDCG_all_120={row["ndcg_at_10"]:.4f} '
              f'nDCG_nonempty={row["ndcg_at_10_nonempty"]:.4f} '
              f'invalid_rows={invalid[arm]} fallbacks={failures}', flush=True)
    check(all(sha(path) == expected for path, expected in frozen.items()), 'protected source changed')
    summary_path = DEST / 'scoring_summary.json'
    with summary_path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(summary, indent=2) + '\n')
    print('| Method | nDCG@10 all 120 | nDCG@10 non-empty | Fallbacks |')
    print('| --- | ---: | ---: | ---: |')
    for name, row in summary['methods'].items():
        print(f'| {"old C" if name == "oldC" else name} | {row["ndcg_at_10"]:.4f} | '
              f'{row["ndcg_at_10_nonempty"]:.4f} | {row["fallbacks"]} |')
    print(f'scripts/hw3_sparse_score.py SHA-256: {sha(Path(__file__))}')
    for path in sorted(DEST.rglob('*.json')):
        print(f'{path.relative_to(ROOT)} SHA-256: {sha(path)}')


if __name__ == '__main__':
    main()
