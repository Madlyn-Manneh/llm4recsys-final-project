"""Prepare and inspect a supplementary cohort with imported starter functions."""
import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import starter

assert hashlib.sha256((root / 'llm_rerank.py').read_bytes()).hexdigest() == '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'
source_protocol = json.loads((root / 'outputs/baseline/protocol.json').read_text())
data = root.parent / 'Session 1/FAR-Trans'
for name, digest in source_protocol['source_sha256'].items():
    assert hashlib.sha256((data / name).read_bytes()).hexdigest() == digest
assets, profiles, history, truth, end, excluded = starter.load_data(data, '2021-06-01', 30)
assert end == '2021-07-01'
# select_users supplies the starter's exact SHA256('42:' + uid), uid order.
ordered_warm = starter.select_users(profiles, history, 'warm', 0, None)
eligible = set(assets)
qualifying = [u for u in ordered_warm if 1 <= sum(history[u].values()) <= 5
              and truth.get(u, set()) & eligible]
selected = qualifying[:30]
assert selected
cohort_path = root / 'cohorts/sparse_labelled.txt'
if sys.argv[1] == 'build':
    assert not cohort_path.exists(), 'Refusing to overwrite a cohort file'
    cohort_path.parent.mkdir(exist_ok=True)
    with cohort_path.open('x') as stream:
        stream.write('\n'.join(selected) + '\n')
    print(json.dumps({'total_qualifying_users': len(qualifying), 'selected': len(selected),
                      'cohort_file': str(cohort_path), 'ordering': 'starter.select_users warm, limit=0, then filter and take first 30'}))
elif sys.argv[1] == 'inspect':
    assert cohort_path.read_text().splitlines() == selected
    directory = root / 'outputs/sparse_baseline'
    protocol = json.loads((directory / 'protocol.json').read_text())
    metrics = json.loads((directory / 'metrics.json').read_text())
    contexts = [json.loads(line) for line in (directory / 'contexts.jsonl').read_text().splitlines()]
    assert protocol['users'] == selected == [c['user_id'] for c in contexts]
    assert protocol['candidate_count'] == 50 and not protocol['exclude_seen']
    labels = sum(len(truth[u] & set(c['eligible_asset_ids'])) for u, c in zip(selected, contexts))
    covered_by_user = [len(truth[c['user_id']] & {a['id'] for a in c['candidate_assets']}) for c in contexts]
    result = {'total_qualifying_users': len(qualifying), 'selected': len(selected),
              'protocol_hash': protocol['protocol_hash'], 'future_labels': labels,
              'labels_in_top50': sum(covered_by_user), 'users_with_label_in_top50': sum(n > 0 for n in covered_by_user),
              'baseline_metrics': metrics['methods']}
    for row in metrics['methods'].values():
        assert row['users'] == row['nonempty_truth_users'] == len(selected)
        assert row['ndcg_at_10'] == row['ndcg_at_10_nonempty']
    print(json.dumps(result, indent=2))
else:
    raise ValueError('Use build or inspect')
