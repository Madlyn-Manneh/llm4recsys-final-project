"""Inspect real saved inputs and verify the single-function change; no model calls."""
import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import llm_rerank as pipeline

original = (root / 'llm_rerank_original.py').read_text()
modified = (root / 'llm_rerank.py').read_text()
def without_function(text):
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == 'structured_block')
    lines = text.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1] + lines[node.end_lineno:])
assert without_function(original) == without_function(modified)
assert 'enable_thinking=False' in ast.get_source_segment(modified, next(
    n for n in ast.walk(ast.parse(modified)) if isinstance(n, ast.FunctionDef) and n.name == 'chat'
    and any(isinstance(x, ast.Attribute) and x.attr == 'apply_chat_template' for x in ast.walk(n))))
contexts = [json.loads(line) for line in (root / 'outputs/baseline/contexts.jsonl').read_text().splitlines()]
ctx = next(c for c in contexts if len(c['history']) > 1)
a, b = pipeline.structured_block(ctx), pipeline.history_block(ctx)
print('Only structured_block differs: PASS; thinking-off argument: PASS')
print('USER', ctx['user_id'])
print('ARM A\n' + a)
print('ARM B\n' + b)

for context in contexts:
    rows = context['history'][:pipeline.HISTORY_CAP]
    assert rows == sorted(rows, key=lambda row: (-row['buy_count'], row['id']))
    a = pipeline.structured_block(context)
    b = pipeline.history_block(context)
    counts_a = re.search(r'^- buys per asset \(ISIN\): (.*)$', a, re.M).group(1)
    counts_a = re.findall(r'([^ ,]+) \((\d+)\)', counts_a)
    assert counts_a == [(row['id'], str(row['buy_count'])) for row in rows]
    for row in rows:
        assert f"- {row['id']} | {pipeline.attrs(row)} | bought {row['buy_count']}x" in b
    for key in ('assetCategory', 'assetSubCategory', 'sector', 'industry', 'marketID'):
        counts = Counter()
        for row in rows:
            for token in row['attributes']:
                if token.startswith(key + '='):
                    counts[token.split('=', 1)[1]] += row['buy_count']
        total = sum(row['buy_count'] for row in rows)
        for value, count in counts.items():
            assert f'{value} {count}/{total} ({100*count/max(total, 1):.0f}%)' in a
        if not counts:
            assert f'- {key} (share of buys):' not in a
print('All 100 real contexts: same capped ISIN/count sequence, attribute values and weighted shares: PASS')
print('Attribute values are aggregated in A; per-asset attribute associations are not retained by this definition.')
