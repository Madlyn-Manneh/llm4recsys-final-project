"""Verify the C2 prompt-only edit without importing or loading a model."""
import ast
import json
import sys
from pathlib import Path
import psutil

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import llm_rerank as original
import llm_rerank_c2 as c2

expected = ('Write a summary of 3 to 4 sentences for a recommender system. "bought Nx" means N '
            'separate Buy transactions, not shares or units. Name every asset by its ISIN with its '
            'buy count. State which assets were bought more than once; if none were, say so. '
            'Describe the main asset categories, sectors and markets using only the attributes '
            'shown. Do not add any information that is not in the history.')
def outside_summary(path):
    text = path.read_text()
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == 'summary_prompt')
    lines = text.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1] + lines[node.end_lineno:])
assert outside_summary(root/'llm_rerank.py') == outside_summary(root/'llm_rerank_c2.py')
contexts = [json.loads(line) for line in (root/'outputs/sparse_baseline/contexts.jsonl').read_text().splitlines()]
for ctx in contexts:
    system, user = c2.summary_prompt(ctx, 'C', True)
    assert system == original.SUMMARY_SYSTEM
    assert user == original.history_block(ctx) + '\n\n' + expected
    for available in (False, True):
        assert original.summary_prompt(ctx, 'D', available) == c2.summary_prompt(ctx, 'D', available)
active = [(p.pid, p.info['cmdline']) for p in psutil.process_iter(['cmdline'])
          if any(Path(arg).name in ('llm_rerank.py','llm_rerank_c2.py') for arg in (p.info['cmdline'] or []))]
assert not active, f'Existing model processes: {active}'
print('PASS: only summary_prompt changed; exact new non-D text, identical SUMMARY_SYSTEM and D behaviour for all 30 contexts.')
print('PASS: no existing base or C2 model process.')
