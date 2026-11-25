"""Local derived-response preparation and aggregate-only scoring."""
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from starter import validate_ranking

OLD = ROOT.parent / 'Session 2' / 'outputs'
FINAL = ROOT / 'outputs' / 'final_200'
BASE = ROOT / 'outputs' / 'baseline_200'
EXPECTED = 'd46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697'
SCRIPTS = {
    'A': ('llm_rerank.py', '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'),
    'C': ('llm_rerank_c2.py', '0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada'),
}


def check(condition, message):
    if not condition:
        print('FAIL: ' + message, flush=True)
        sys.exit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()]


def keyed(records, expected_count):
    result = {row['user_id']: row for row in records}
    check(len(records) == expected_count and len(result) == expected_count,
          'response row or unique-user count mismatch')
    return result


def invalid_positions(records, contexts):
    positions = []
    for pos, ctx in enumerate(contexts, 1):
        row = records[ctx['user_id']]
        check(row['stage'] == 'ranker', 'response stage mismatch')
        try:
            validate_ranking(row['ranked_ids'], [a['id'] for a in ctx['candidate_assets']])
        except (ValueError, KeyError, TypeError):
            positions.append(pos)
    return positions


def merge():
    check(not FINAL.exists(), 'final_200 already exists; refusing to overwrite')
    check(sha(ROOT / 'HW3_PROTOCOL.md') ==
          '427e05eea001910c4c1f02169915ee5efbc27b5b5463fa0fdceb824ecd3c2146',
          'base protocol document hash mismatch')
    for name, expected in SCRIPTS.values():
        check(sha(ROOT / name) == expected, 'reranker source hash mismatch')
    contexts = read(BASE / 'contexts.jsonl')
    users = [row['user_id'] for row in contexts]
    check(len(users) == 200 and len(set(users)) == 200, 'baseline context count mismatch')
    protocol = json.loads((BASE / 'protocol.json').read_text())
    check(protocol['protocol_hash'] == EXPECTED and protocol['users'] == users,
          'baseline protocol or order mismatch')
    check(read(OLD / 'baseline' / 'contexts.jsonl') == contexts[:100],
          'HW2 contexts not identical to first 100 main contexts')
    source_paths = {
        'A_first': OLD / 'arm_A' / 'responses.jsonl',
        'A_second': ROOT / 'outputs' / 'arm_A_101_200' / 'responses.jsonl',
        'C': ROOT / 'outputs' / 'arm_C2_200' / 'responses.jsonl',
    }
    first = keyed(read(source_paths['A_first']), 100)
    second = keyed(read(source_paths['A_second']), 100)
    c = keyed(read(source_paths['C']), 200)
    check(set(first) == set(users[:100]) and set(second) == set(users[100:])
          and set(c) == set(users), 'source cohort coverage mismatch')
    old_hash = json.loads((OLD / 'baseline' / 'protocol.json').read_text())['protocol_hash']
    check(all(row['protocol_hash'] == old_hash for row in first.values()),
          'HW2 response protocol mismatch')
    check(all(row['protocol_hash'] == EXPECTED for row in list(second.values()) + list(c.values())),
          'new response protocol mismatch')
    a_sources = {**first, **second}
    merged = [dict(a_sources[uid], protocol_hash=EXPECTED) for uid in users]
    a = keyed(merged, 200)
    invalid_a = invalid_positions(a, contexts)
    invalid_c = invalid_positions(c, contexts)
    check(invalid_a == [181] and invalid_c == [], 'unexpected invalid-response counts or positions')
    for name, folder, wanted in (
        ('A_first', OLD / 'arm_A', 0),
        ('A_second', ROOT / 'outputs' / 'arm_A_101_200', len(invalid_a)),
        ('C', ROOT / 'outputs' / 'arm_C2_200', len(invalid_c)),
    ):
        meta = json.loads((folder / 'run_meta.json').read_text())
        check(meta['invalid_outputs'] == wanted, 'source invalid count mismatch')
    source_hashes = {name: sha(path) for name, path in source_paths.items()}
    FINAL.mkdir()
    a_file, c_file = FINAL / 'A_responses.jsonl', FINAL / 'C_responses.jsonl'
    a_file.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in merged),
                      encoding='utf-8')
    c_file.write_bytes(source_paths['C'].read_bytes())
    checks = {}
    for arm, path, sources in (('A', a_file, a_sources), ('C', c_file, c)):
        rows = read(path)
        identical = sum(row['ranked_ids'] == sources[row['user_id']]['ranked_ids'] for row in rows)
        count, unique = len(rows), len({row['user_id'] for row in rows})
        check(count == unique == identical == 200, 'merged response integrity mismatch')
        check(all(row['protocol_hash'] == EXPECTED for row in rows), 'merged protocol mismatch')
        checks[arm] = {'rows': count, 'unique_users': unique, 'ranked_ids_identical_to_source': identical}
        print(f'{arm}: rows={count} unique_users={unique} ranked_ids_identical_to_source={identical}')
        print(f'{path.name} SHA-256: {sha(path)}')
    manifest = {
        'protocol_hash': EXPECTED,
        'base_protocol_document_sha256': sha(ROOT / 'HW3_PROTOCOL.md'),
        'amendment1_sha256': sha(ROOT / 'HW3_PROTOCOL_AMENDMENT1.md'),
        'baseline_contexts_sha256': sha(BASE / 'contexts.jsonl'),
        'baseline_protocol_json_sha256': sha(BASE / 'protocol.json'),
        'invalid_rows': {'A': {'count': len(invalid_a), 'positions': invalid_a}, 'C': 0},
        'scoring_rule': 'starter --on-invalid fallback (team rule, Session 2)',
        'checks': checks,
        'files': {
            'A_responses.jsonl': {
                'sha256': sha(a_file), 'script': SCRIPTS['A'][0], 'script_sha256': SCRIPTS['A'][1],
                'sources': [
                    {'path': str(source_paths['A_first']), 'sha256': source_hashes['A_first'],
                     'baseline_order_positions': [1, 100], 'rows': 100,
                     'original_protocol_hash': old_hash},
                    {'path': str(source_paths['A_second']), 'sha256': source_hashes['A_second'],
                     'baseline_order_positions': [101, 200], 'rows': 100,
                     'original_protocol_hash': EXPECTED},
                ],
                'rebound_rows': {'baseline_order_positions': [1, 100], 'count': 100,
                                 'from_protocol_hash': old_hash, 'to_protocol_hash': EXPECTED},
                'construction': 'All 200 rows in baseline context order; protocol_hash set to the '
                                '200-user hash on all rows; ranked_ids and other fields unchanged.',
                'hw2_script_attribution': 'Accepted documentary provenance in HW3_PROTOCOL.md; '
                                          'the archived HW2 script did not record its own hash.',
            },
            'C_responses.jsonl': {
                'sha256': sha(c_file), 'script': SCRIPTS['C'][0], 'script_sha256': SCRIPTS['C'][1],
                'sources': [{'path': str(source_paths['C']), 'sha256': source_hashes['C'],
                             'rows': 200, 'original_protocol_hash': EXPECTED}],
                'rebound_rows': {'count': 0}, 'construction': 'Byte-identical copy.',
            },
        },
    }
    manifest_path = FINAL / 'MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    for name, path in source_paths.items():
        check(sha(path) == source_hashes[name], 'source response file changed')
        print(f'{name} source SHA-256: {source_hashes[name]}')
    print(f'MANIFEST.json SHA-256: {sha(manifest_path)}')


def score():
    protocol = json.loads((BASE / 'protocol.json').read_text())
    manifest = json.loads((FINAL / 'MANIFEST.json').read_text())
    baseline = json.loads((BASE / 'metrics.json').read_text())
    protected = [ROOT / 'HW3_PROTOCOL.md', ROOT / 'HW3_PROTOCOL_AMENDMENT1.md',
                 BASE / 'protocol.json', BASE / 'contexts.jsonl', BASE / 'metrics.json']
    for item in manifest['files'].values():
        protected.extend(Path(source['path']) for source in item['sources'])
    frozen = {path: sha(path) for path in protected}
    days = (date.fromisoformat(protocol['end_exclusive']) - date.fromisoformat(protocol['cutoff'])).days
    common = ['run', '--data-dir', str(ROOT.parent / 'Session 1' / 'FAR-Trans'),
              '--cutoff', protocol['cutoff'], '--horizon-days', str(days),
              '--max-users', str(len(protocol['users'])), '--cohort', protocol['cohort_selection'],
              '--candidate-count', str(protocol['candidate_count']),
              '--stage', 'ranker', '--on-invalid', 'fallback']
    if protocol['exclude_seen']:
        common.append('--exclude-seen')
    results = {}
    for arm in ('A', 'C'):
        response = FINAL / f'{arm}_responses.jsonl'
        check(sha(response) == manifest['files'][response.name]['sha256'], 'derived response hash mismatch')
        output = FINAL / f'evaluation_{arm}'
        check(not output.exists(), 'evaluation output already exists; refusing to overwrite')
        command = [sys.executable, str(ROOT / 'starter.py'), *common,
                   '--responses', str(response), '--output-dir', str(output)]
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if completed.returncode != 0:
            # Starter errors can contain customer IDs; do not emit captured output.
            print(f'{arm}: scoring_exit_code={completed.returncode}', flush=True)
            sys.exit(1)
        metrics = json.loads((output / 'metrics.json').read_text())
        check(metrics['protocol_hash'] == EXPECTED, 'scoring protocol hash mismatch')
        check((output / 'contexts.jsonl').read_bytes() == (BASE / 'contexts.jsonl').read_bytes(),
              'scoring contexts differ from baseline')
        check(all(metrics['methods'][name] == values for name, values in baseline['methods'].items()),
              'scoring baseline metrics differ from frozen baseline')
        invalid = manifest['invalid_rows']['A']['count'] if arm == 'A' else manifest['invalid_rows']['C']
        fallbacks = len(metrics['custom_failures'])
        check(fallbacks == invalid, 'fallback count differs from validated invalid count')
        row = metrics['methods']['custom']
        check(row['users'] == 200, 'evaluated user count mismatch')
        lines = (f'{arm}: nDCG@10_all_200={row["ndcg_at_10"]:.4f} '
                 f'nDCG@10_nonempty_truth={row["ndcg_at_10_nonempty"]:.4f} '
                 f'invalid_rows={invalid} fallbacks_used={fallbacks}\n')
        (FINAL / f'score_{arm}.txt').write_text(lines, encoding='utf-8')
        print(lines, end='', flush=True)
        results[arm] = (row, fallbacks)
    check(all(sha(path) == expected for path, expected in frozen.items()), 'protected file hash changed')
    print('\n| Method | nDCG@10 all 200 | nDCG@10 non-empty truth | Fallbacks |')
    print('| --- | ---: | ---: | ---: |')
    for label, key in (('CBF', 'cbf'), ('Latest buy', 'latest_buy'),
                       ('Latest buy or sell', 'latest_buy_or_sell'), ('Popularity', 'popularity')):
        row = baseline['methods'][key]
        print(f'| {label} | {row["ndcg_at_10"]:.4f} | {row["ndcg_at_10_nonempty"]:.4f} | 0 |')
    for arm, (row, fallback) in results.items():
        print(f'| {arm} | {row["ndcg_at_10"]:.4f} | {row["ndcg_at_10_nonempty"]:.4f} | {fallback} |')


if __name__ == '__main__':
    {'merge': merge, 'score': score}[sys.argv[1]]()
