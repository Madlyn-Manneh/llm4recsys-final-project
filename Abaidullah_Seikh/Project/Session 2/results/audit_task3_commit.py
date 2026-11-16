"""Read-only allowlist content audit; writes a local audit note, never stages files."""
import ast
import csv
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data = root.parent / 'Session 1/FAR-Trans'
allowlist = ['llm_rerank.py', 'requirements.txt', 'README_hw2_dastan.md',
             'results/results_table.md', 'results/task3_analysis_aggregate.md']
ids = set()
for name in ('customer_information.csv', 'transactions.csv'):
    with (data / name).open(encoding='utf-8-sig', newline='') as stream:
        ids.update(row['customerID'] for row in csv.DictReader(stream) if row['customerID'])
rendered = set()
for arm in 'ABC':
    for line in (root / f'outputs/arm_{arm}/raw_log.jsonl').read_text().splitlines():
        record = json.loads(line)
        for key in ('rank_prompt', 'summary_prompt', 'summary', 'rank_output'):
            if record.get(key):
                rendered.add(record[key])
        if record.get('summary_prompt'):
            rendered.add(record['summary_prompt'].split('\n\n', 1)[0])

report = ['# Task 3b commit-content audit (local preparation only)', '',
          'No files were staged or committed. Only the five paths below are proposed.', '',
          f'Checked against all {len(ids)} distinct raw customer IDs found in the original customer and transaction CSVs, plus complete instantiated prompts, source-history blocks, summaries, and ranking outputs from all 300 full-run raw-log records.', '',
          '| Proposed file | Raw customer ID matches | Saved instantiated text matches | SHA-256 |', '|---|---:|---:|---|']
for name in allowlist:
    path = root / name
    text = path.read_text()
    id_hits = sum(uid in text for uid in ids)
    rendered_hits = sum(value in text for value in rendered)
    assert id_hits == 0 and rendered_hits == 0, f'Content audit failed for {name}: IDs={id_hits}, saved text={rendered_hits}'
    report.append(f'| `{name}` | {id_hits} | {rendered_hits} | `{hashlib.sha256(path.read_bytes()).hexdigest()}` |')

# Source templates are intentionally visible, not mislabeled as absent.
source = (root / 'llm_rerank.py').read_text()
tree = ast.parse(source)
templates = [n.targets[0].id for n in tree.body if isinstance(n, ast.Assign)
             and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
             and n.targets[0].id in ('RANK_SYSTEM', 'SUMMARY_SYSTEM')]
assert sorted(templates) == ['RANK_SYSTEM', 'SUMMARY_SYSTEM']
report += ['', '## Literal prompt-text policy', '',
           '`llm_rerank.py` contains the static `RANK_SYSTEM` and `SUMMARY_SYSTEM` source templates and prompt-building functions, as required to keep inference reproducible. Thus a literal rule prohibiting all prompt text, including source templates, does not pass for that file. No generated/customer-instantiated prompts or raw customer IDs occur in any allowlisted file. The source was not modified to conceal or remove templates. Confirm whether source-code templates are permitted before committing.', '',
           '## Local-only exclusions', '',
           '`outputs/` (all prompts, summaries, responses, predictions, metrics with IDs, protocol users and logs); `.venv/`; data/model files; `reference/`; old/original script copies unless separately requested; `results/task1_setup.md`; `results/task2_smoke.md`; `results/task3_runs.md`; `results/task3_analysis.md`; `results/task3_tokens_per_user_LOCAL.csv`; `results/session1_to_session2.md`; `results/session1_report_extracted.txt`; local analysis/inspection helpers and session exports. The explicit allowlist avoids accidentally staging these; existing ignore rules alone are insufficient for local result notes.', '',
           'Repository availability is checked separately. No repository, remote, commit or staging area is created by this audit.']
(root / 'results/task3_commit_preparation.md').write_text('\n'.join(report) + '\n')
print('PASS: five proposed files have zero raw customer IDs and zero saved instantiated-text matches.')
print('POLICY CHECK: llm_rerank.py contains static prompt templates; literal no-prompt-text compliance requires clarification.')
print('Audit note: results/task3_commit_preparation.md')
