"""Post-hoc evaluation of saved runs. No model weights, inference, or output edits."""
import csv
import hashlib
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import starter
import llm_rerank as pipeline
from transformers import AutoTokenizer

OUT = ROOT / 'outputs'
RESULTS = ROOT / 'results'
REV = '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e'
DATA = ROOT.parent / 'Session 1' / 'FAR-Trans'
read_json = lambda path: json.loads(path.read_text())
read_jsonl = lambda path: [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
baseline = read_json(OUT / 'baseline/metrics.json')
protocol = read_json(OUT / 'baseline/protocol.json')
contexts = read_jsonl(OUT / 'baseline/contexts.jsonl')
ctx = {c['user_id']: c for c in contexts}
users = protocol['users']
assert len(users) == len(ctx) == 100
assert hashlib.sha256((ROOT / 'llm_rerank.py').read_bytes()).hexdigest() == '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'
for name, digest in protocol['source_sha256'].items():
    assert hashlib.sha256((DATA / name).read_bytes()).hexdigest() == digest

# This is the starter's own construction, imported unchanged, not a new label policy.
assets, profiles, history, truth, end, excluded = starter.load_data(DATA, protocol['cutoff'], 30)
assert end == protocol['end_exclusive']
relevant = {u: truth.get(u, set()) & set(ctx[u]['eligible_asset_ids']) for u in users}
nonempty = [u for u in users if relevant[u]]
sparse = [u for u in users if 1 <= sum(a['buy_count'] for a in ctx[u]['history']) <= 5]
sparse_nonempty = [u for u in sparse if relevant[u]]
assert len(nonempty) == 11 and len(sparse) == 65 and len(sparse_nonempty) == 2
assert sum(len(v) for v in relevant.values()) == 18

metrics, meta, records, logs, rankings = {}, {}, {}, {}, {}
for arm in 'ABC':
    directory = OUT / ('arm_' + arm + '_eval')
    metrics[arm] = read_json(directory / 'metrics.json')
    assert read_json(directory / 'protocol.json') == protocol
    assert metrics[arm]['protocol_hash'] == baseline['protocol_hash']
    for method, values in baseline['methods'].items():
        assert metrics[arm]['methods'][method] == values
    with (directory / 'per_user.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    records[arm] = {r['user_id']: r for r in rows if r['method'] == 'custom'}
    assert set(records[arm]) == set(users)
    for u, row in records[arm].items():
        assert int(row['relevant_count']) == len(relevant[u])
    meta[arm] = read_json(OUT / ('arm_' + arm) / 'run_meta.json')
    logs[arm] = read_jsonl(OUT / ('arm_' + arm) / 'raw_log.jsonl')
    assert [r['user_id'] for r in logs[arm]] == users
    assert meta[arm]['users'] == 100 and meta[arm]['invalid_outputs'] == 0
    assert meta[arm]['resolved_commit'] == REV and meta[arm]['protocol_hash'] == protocol['protocol_hash']
    assert meta[arm]['generation'] == {'do_sample': False, 'seed': 0, 'summary_max_new_tokens': 120, 'rank_max_new_tokens': 60}
    responses = read_jsonl(OUT / ('arm_' + arm) / 'responses.jsonl')
    assert [r['user_id'] for r in responses] == users
    rankings[arm] = {r['user_id']: r['ranked_ids'] for r in responses}
    for log in logs[arm]:
        u = log['user_id']
        pool = [a['id'] for a in ctx[u]['candidate_assets']]
        assert log['valid'] and '<think>' not in log['rank_output'].lower()
        assert rankings[arm][u] == [pool[i-1] for i in log['parsed_numbers']]
        starter.validate_ranking(rankings[arm][u], pool)
        assert starter.ndcg10(rankings[arm][u], relevant[u]) == float(records[arm][u]['ndcg_at_10'])

mean = statistics.mean
ndcg = lambda arm, u: float(records[arm][u]['ndcg_at_10'])
table = ['# HW2 results — FAR-Trans, Team 8', '',
         'All 100 selected users are retained; 11 have future purchases and 89 have empty truth. Scores are displayed to four decimals.', '',
         '| Method | Users | Users with future purchases | nDCG@10 all users | nDCG@10 nonempty truth | Runtime | Failed cases |',
         '|---|---:|---:|---:|---:|---|---:|']
for method, title in [('popularity', 'Popularity'), ('cbf', 'CBF (no-rerank control: candidates are the CBF top 50)'), ('latest_buy', 'Latest buy'), ('latest_buy_or_sell', 'Latest buy or sell')]:
    m = metrics['A']['methods'][method]
    table.append(f"| {title} | {m['users']} | {m['nonempty_truth_users']} | {m['ndcg_at_10']:.4f} | {m['ndcg_at_10_nonempty']:.4f} | 10.77 s, whole starter run, all four baselines | 0 |")
for arm, title in [('A', 'structured'), ('B', 'history text'), ('C', 'LLM summary')]:
    m = metrics[arm]['methods']['custom']
    table.append(f"| Arm {arm} ({title}) | {m['users']} | {m['nonempty_truth_users']} | {m['ndcg_at_10']:.4f} | {m['ndcg_at_10_nonempty']:.4f} | {meta[arm]['wall_seconds_whole_arm']:.1f} s, whole arm, excluding model loading" + (' (C includes summaries)' if arm == 'C' else '') + f" | {meta[arm]['invalid_outputs']} |")
table += ['', 'Sources: baseline rows copied from `outputs/arm_A_eval/metrics.json`, identical in `outputs/arm_B_eval/metrics.json` and `outputs/arm_C_eval/metrics.json` and the original baseline. A/B/C rows use the respective evaluation files, method `custom`. Arm runtimes and invalid counts use `outputs/arm_A/run_meta.json`, `outputs/arm_B/run_meta.json`, and `outputs/arm_C/run_meta.json`. Classical failed cases are 0 (no model output to validate); each arm has 0 starter custom failures as well as 0 invalid model rankings.', '', 'The four baseline rows share one externally measured 10.77-second run; the time is not charged four times. Arm timers exclude model loading and initial context/questionnaire reading, and do not include this separate scoring run. Arm C includes both summary and ranking calls.', '', 'Full shared protocol hash: `' + protocol['protocol_hash'] + '`. All evaluation protocols are exactly equal to the baseline protocol, and all four baseline aggregate blocks match at full saved precision.']
(RESULTS / 'results_table.md').write_text('\n'.join(table) + '\n')

lines = ['# Task 3b — descriptive aggregate analysis', '',
         'No statistical, causal, or substantive conclusions are drawn here. All analyses use the same 100 users. Empty truth contributes zero to nDCG and to the all-user macro Recall@10 defined below. Future labels are used only for evaluation after generation, never as model input.', '',
         '## Evaluation checks', '',
         '- All three evaluation protocol objects exactly equal `outputs/baseline/protocol.json`.',
         '- Full protocol hash: `' + protocol['protocol_hash'] + '`.',
         '- Four baseline aggregate blocks exactly match the original saved values in every evaluation.',
         '- A/B/C each have 100 responses, 0 invalid outputs and 0 custom failures. Per-user nDCG was cross-checked using the imported starter metric and evaluated rankings.', '',
         '## a. Paired nDCG@10 differences', '',
         'Better/equal/worse compares C with its comparator at full saved float precision (no rounding before comparison).', '',
         '| Difference | Users | Mean difference | C better | Equal | C worse |', '|---|---:|---:|---:|---:|---:|']
for other in 'AB':
    for cohort, group in [('all', users), ('nonempty', nonempty)]:
        differences = [ndcg('C', u)-ndcg(other, u) for u in group]
        lines.append(f'| C−{other}, {cohort} | {len(group)} | {mean(differences):.8f} | {sum(d>0 for d in differences)} | {sum(d==0 for d in differences)} | {sum(d<0 for d in differences)} |')
lines += ['', '## b. Hits and Recall@10', '',
          'Recall@10 per user = distinct relevant ISINs in top ten / distinct eligible future Buy ISINs; empty truth is 0. Means below are macro means, not pooled micro recall. Hits are independently counted from evaluated rankings and imported starter truth.', '',
          '| Arm | Nonempty users with ≥1 hit (of 11) | Total hits | Recall@10 all (100) | Recall@10 nonempty (11) |', '|---|---:|---:|---:|---:|']
for arm in 'ABC':
    hits = {u: len(set(rankings[arm][u]) & relevant[u]) for u in users}
    recall = {u: hits[u]/len(relevant[u]) if relevant[u] else 0.0 for u in users}
    lines.append(f'| {arm} | {sum(hits[u]>0 for u in nonempty)} | {sum(hits.values())} | {mean(recall.values()):.8f} | {mean(recall[u] for u in nonempty):.8f} |')
lines += ['', '## c. Sparse users (1–5 historical Buys)', '',
          'Sparse means sum of saved eligible-history buy_count is 1–5, not 1–5 distinct assets. There are 65 sparse users: 2 with future purchases and 63 with empty truth. Individual values and identifiers are in the local-only analysis; this file contains aggregates only.', '',
          '| Arm | Sparse all-user nDCG@10 (65) | Sparse nonempty nDCG@10 (2) |', '|---|---:|---:|']
for arm in 'ABC':
    lines.append(f'| {arm} | {mean(ndcg(arm,u) for u in sparse):.8f} | {mean(ndcg(arm,u) for u in sparse_nonempty):.8f} |')
lines += ['', '## d. Candidate-order behaviour', '',
          'Overlap is set intersection size with the CBF top ten (0–10); its fraction is overlap/10. Candidate numbers are positions in the original fixed top-50 pool. Ascending means strictly increasing returned candidate numbers, not necessarily consecutive or 1–10.', '',
          '| Arm | Mean overlap count | Mean overlap fraction | Candidate 1 ranked first (of 100) | Ascending rankings (of 100) |', '|---|---:|---:|---:|---:|']
for arm in 'ABC':
    overlap = [len(set(rankings[arm][u]) & {a['id'] for a in ctx[u]['candidate_assets'][:10]}) for u in users]
    numbers = [r['parsed_numbers'] for r in logs[arm]]
    lines.append(f'| {arm} | {mean(overlap):.4f} | {mean(overlap)/10:.4f} | {sum(n[0]==1 for n in numbers)} | {sum(n==sorted(n) for n in numbers)} |')
lines += ['', '## e. Previously bought assets in recommendations', '',
          'A repeated asset is a recommendation whose ISIN occurs anywhere in the full pre-cutoff Buy history, not only its capped prompt rows. This measures recommendations, not observed future repeat transactions.', '',
          '| Arm | Users with ≥1 previously bought asset (of 100) | Previously bought recommendation slots (of 1000) | Mean count/user | Slot fraction |', '|---|---:|---:|---:|---:|']
for arm in 'ABC':
    repeats = [len(set(rankings[arm][u]) & set(history.get(u, {}))) for u in users]
    lines.append(f'| {arm} | {sum(n>0 for n in repeats)} | {sum(repeats)} | {mean(repeats):.4f} | {sum(repeats)/1000:.4f} |')
coverage = []
for u in nonempty:
    pool = {a['id'] for a in ctx[u]['candidate_assets']}
    coverage.append((u, sorted(relevant[u]), sorted(relevant[u] & pool)))
covered = sum(len(hit) for _, _, hit in coverage)
lines += ['', '## f. Candidate label coverage (evaluation only)', '',
          f'Using the unchanged imported `starter.load_data()` truth construction and its eligible-ID intersection, **{covered} of 18** future user–asset labels fall in their user’s fixed top-50 pool, across **{sum(bool(hit) for _,_,hit in coverage)}** users. The team reference **6/18 ' + ('matches' if covered == 6 else 'does not match') + '**. User IDs and covered labels are listed only in the local-only report.', '',
          'The CSV source hashes were checked against the original protocol before loading truth. Exact duplicates and negative-ID initial positions, Buy-only relevance, strict cutoff/horizon, and eligible assets are handled by the starter rather than reimplemented.']
summary_mentions = sum(any(a['id'] in r['summary'] for a in ctx[r['user_id']]['history']) for r in logs['C'])
lines += ['', '## g. Summary ISIN mentions and manual-check sample', '',
          f'**{summary_mentions} of 100** C summaries mention at least one exact, case-sensitive ISIN from that user’s full history. This is a string-presence count, not a factuality judgment.', '',
          'Ten summaries and their exact history texts are in local-only `results/task3_analysis.md`. Selection uses `random.Random(42).sample(protocol_users, 10)` in the saved protocol order. No summary judgments are made in this task.']

# Reconstruct exactly HFBackend.chat's prompt formatting, locally, with no model loaded.
tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3-1.7B', revision=REV, local_files_only=True)
token_rows = []
def tokens(text):
    return len(tokenizer(text, add_special_tokens=False)['input_ids'])
def prompt_tokens(system, user):
    text = tokenizer.apply_chat_template([{'role': 'system', 'content': system}, {'role': 'user', 'content': user}], tokenize=False, add_generation_prompt=True, enable_thinking=False)
    return len(tokenizer(text, return_tensors=None)['input_ids'])
for arm in 'ABC':
    for record in logs[arm]:
        row = {'arm': arm, 'user_id': record['user_id'], 'rank_prompt_tokens': prompt_tokens(pipeline.RANK_SYSTEM, record['rank_prompt']), 'rank_output_tokens': tokens(record['rank_output']), 'summary_prompt_tokens': 0, 'summary_output_tokens': 0}
        if arm == 'C':
            row.update(summary_prompt_tokens=prompt_tokens(pipeline.SUMMARY_SYSTEM, record['summary_prompt']), summary_output_tokens=tokens(record['summary']))
        token_rows.append(row)
lines += ['', '## h. Tokens and latency', '',
          'Prompt counts reconstruct the actual system/user chat template with the pinned local Qwen3 tokenizer, add_generation_prompt=True and enable_thinking=False, then tokenize as HFBackend.chat does. They include chat formatting. Output counts re-tokenize saved decoded/stripped text without special tokens; EOS and removed special tokens are not recoverable, so these are saved-text token counts, not exact model generation-token usage. No model or inference was loaded. Summary tokens are included only for C.', '',
          '| Arm | Stage | Prompt total | Prompt mean | Prompt min/median/max | Output total | Output mean | Output min/median/max |', '|---|---|---:|---:|---|---:|---:|---|']
for arm in 'ABC':
    for stage in (['rank', 'summary'] if arm == 'C' else ['rank']):
        rows = [r for r in token_rows if r['arm'] == arm]
        p = [r[stage+'_prompt_tokens'] for r in rows]
        o = [r[stage+'_output_tokens'] for r in rows]
        lines.append(f'| {arm} | {stage} | {sum(p)} | {mean(p):.2f} | {min(p)}/{statistics.median(p):g}/{max(p)} | {sum(o)} | {mean(o):.2f} | {min(o)}/{statistics.median(o):g}/{max(o)} |')
lines += ['', '| Arm | Combined prompt tokens | Combined saved-output tokens | Whole-arm seconds | Mean seconds/user |', '|---|---:|---:|---:|---:|']
for arm in 'ABC':
    rows = [r for r in token_rows if r['arm'] == arm]
    seconds = meta[arm]['wall_seconds_whole_arm']
    lines.append(f"| {arm} | {sum(r['rank_prompt_tokens']+r['summary_prompt_tokens'] for r in rows)} | {sum(r['rank_output_tokens']+r['summary_output_tokens'] for r in rows)} | {seconds:.1f} | {seconds/100:.3f} |")
lines += ['', 'Seconds/user is whole-arm recorded loop time / 100, excluding model loading and initial context/questionnaire reads; C includes summaries. Raw logs have no per-call or per-user timing, so individual latency distributions cannot be recovered. No individual timings, monetary cost, energy cost, or significance results are invented.', '',
          'Sources: `outputs/arm_{A,B,C}_eval/per_user.csv`, `predictions.csv`/saved response rankings, `metrics.json`, baseline contexts/protocol, original run metadata and raw logs. Analysis helpers, per-user token tables, truth identifiers, and raw examples remain local.']
aggregate = '\n'.join(lines) + '\n'
(RESULTS / 'task3_analysis_aggregate.md').write_text(aggregate)
local = [aggregate.replace('# Task 3b — descriptive aggregate analysis', '# Task 3b — descriptive analysis (LOCAL ONLY: IDs and prompts)'), '', '## Local-only detail: sparse nonempty users', '', '| User ID | Historical Buys | Future labels | A nDCG@10 | B nDCG@10 | C nDCG@10 |', '|---|---:|---:|---:|---:|---:|']
for u in sparse_nonempty:
    local.append(f"| {u} | {sum(history[u].values())} | {len(relevant[u])} | {ndcg('A',u):.8f} | {ndcg('B',u):.8f} | {ndcg('C',u):.8f} |")
local += ['', '## Local-only detail: top-50 label coverage by user', '', '| User ID | Future label ISINs | In top-50 ISINs |', '|---|---|---|']
for u, labels, in_pool in coverage:
    local.append(f"| {u} | {', '.join(labels)} | {', '.join(in_pool) or '(none)'} |")
local += ['', '## Local-only: ten summaries for the student’s manual check', '', 'Fixed seed 42; selection from protocol order, without replacement. Text is verbatim; no factuality judgment is supplied.']
by_user = {r['user_id']: r for r in logs['C']}
for i, u in enumerate(random.Random(42).sample(users, 10), 1):
    r = by_user[u]
    history_text = r['summary_prompt'].split('\n\n', 1)[0]
    assert history_text == pipeline.history_block(ctx[u])
    local += ['', f'### Sample {i} — {u}', '', '**History**', '', '```text', history_text, '```', '', '**Summary**', '', '```text', r['summary'], '```']
(RESULTS / 'task3_analysis.md').write_text('\n'.join(local) + '\n')
with (RESULTS / 'task3_tokens_per_user_LOCAL.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(token_rows[0]))
    writer.writeheader()
    writer.writerows(token_rows)
print('Verified protocols, baseline values, cohort coverage, all saved nDCG values and responses.')
print('custom_failures:', {a: metrics[a]['custom_failures'] for a in 'ABC'})
print('Coverage:', covered, '/18; summaries mentioning history ISIN:', summary_mentions, '/100')
print('Wrote results_table.md, task3_analysis.md, task3_analysis_aggregate.md, task3_tokens_per_user_LOCAL.csv')
