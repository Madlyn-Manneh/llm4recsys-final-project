"""Read-only checks of local snapshot metadata and report quotation fidelity."""
import json
import re
from pathlib import Path
from safetensors import safe_open

root = Path(__file__).resolve().parent
snapshot = Path('/home/dastan/.cache/huggingface/hub/models--Qwen--Qwen3-1.7B/snapshots/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e')
index = json.loads((snapshot / 'model.safetensors.index.json').read_text())
actual = {}
for shard in sorted(set(index['weight_map'].values())):
    with safe_open(str(snapshot / shard), framework='pt', device='cpu') as stream:
        actual.update({key: shard for key in stream.keys()})
assert actual == index['weight_map'], 'Shard headers do not match weight index'
print('All', len(actual), 'tensor keys match the shard index; no tensors loaded.')

source = (root / 'session1_report_extracted.txt').read_text()
for label in ('2. Users and subgroups', '4. Baseline', '5. Proposed method',
              '6. Controls and ablation', '7. Primary metric', '9. Seeds, repeats, cost',
              '10. Four session plan'):
    source = source.replace(label, '')
normalize = lambda text: re.sub(r'\s+', ' ', text).strip()
source = normalize(source)
report = (root / 'session1_to_session2.md').read_text()
quotes = []
current = []
for line in report.splitlines() + ['']:
    if line.startswith('>'):
        if line[1:].strip():
            current.append(line[1:].strip())
        elif current:
            quotes.append(normalize(' '.join(current)))
            current = []
    elif current:
        quotes.append(normalize(' '.join(current)))
        current = []
for number, quote in enumerate(quotes, 1):
    assert quote in source, f'Quotation {number} does not match PDF extraction'
print('All', len(quotes), 'quotation blocks match the extracted PDF (layout normalized).')
for name in ('task1_setup.md', 'session1_to_session2.md'):
    assert (root / name).stat().st_size > 0
    print(name, (root / name).stat().st_size, 'bytes')
