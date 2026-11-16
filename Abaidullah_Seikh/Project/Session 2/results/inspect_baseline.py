"""Read-only inspection of the starter's saved outputs; no source-data access."""
import csv
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent.parent / 'outputs' / 'baseline'
contexts = [json.loads(line) for line in (root / 'contexts.jsonl').read_text().splitlines()]
scores = {r['user_id']: r for r in csv.DictReader((root / 'per_user.csv').open()) if r['method'] == 'cbf'}
print('protocol_hash:', json.loads((root / 'protocol.json').read_text())['protocol_hash'])
for block in ('history', 'candidate_assets'):
    rows = [a for c in contexts for a in c[block]]
    print(block, 'records:', len(rows), 'record keys:', sorted(set().union(*(a.keys() for a in rows))))
    present = Counter(t.split('=', 1)[0] for a in rows for t in a['attributes'])
    print('attribute present/missing:', {k: [present[k], len(rows)-present[k]] for k in
          ('assetCategory', 'assetSubCategory', 'sector', 'industry', 'marketID')})
    print('history order verified:', all(c['history'] == sorted(c['history'], key=lambda a: (-a['buy_count'], a['id'])) for c in contexts))
print('users with >20 history assets:', sum(len(c['history']) > 20 for c in contexts))
sparse = [c for c in contexts if 1 <= sum(a['buy_count'] for a in c['history']) <= 5]
print('sparse users:', len(sparse))
print('sparse users with future purchases:', sum(int(scores[c['user_id']]['relevant_count']) > 0 for c in sparse))
print('all users with future purchases:', sum(int(r['relevant_count']) > 0 for r in scores.values()))
print('future user-asset labels (not raw transaction count):', sum(int(r['relevant_count']) for r in scores.values()))
print('literal Sell occurrences:', (root / 'contexts.jsonl').read_text().count('Sell'))
print('candidate coverage: unverified; outputs contain relevant_count and nDCG but no truth ISINs')
