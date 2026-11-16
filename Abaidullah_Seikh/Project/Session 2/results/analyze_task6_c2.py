"""Analyze saved C2 and earlier sparse runs; no model calls or output changes."""
import csv
import difflib
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import starter

# Fixed deterministic lexical rules, recorded before inspecting C2 outputs.
NO_REPEAT_PATTERNS = [
    r'\bno\s+(?:repeat(?:ed)?|repetition(?:s)?)\s+(?:buy\s+)?(?:purchases?|transactions?|buying)\b',
    r'\b(?:does|do|did)\s+not\s+(?:appear\s+to\s+)?(?:have\s+|show\s+(?:any\s+)?|make\s+(?:any\s+)?|engage\s+in\s+)?repeat(?:ed)?(?:\s+(?:buy\s+)?(?:purchases?|transactions?|buying))?\b',
    r'\b(?:has|have|had)\s+not\s+(?:made\s+)?(?:any\s+)?repeat(?:ed)?\s+(?:purchases?|buys?|transactions?)\b',
    r'\b(?:no|without)\s+(?:evidence|signs?|indication)\s+of\s+(?:repeat(?:ed)?\s+(?:purchases?|buying)|repetition)\b',
    r'\b(?:no|not)\s+repetition\b',
    r'\b(?:no|none\s+of\s+the)\s+assets?\s+(?:was|were|has\s+been|have\s+been)\s+(?:bought|purchased)\s+more\s+than\s+once\b',
    r'\b(?:did|does|do)\s+not\s+(?:buy|purchase)\s+(?:any\s+asset|the\s+same\s+asset)\s+more\s+than\s+once\b',
]
NO_REPEAT = [re.compile(p, re.I) for p in NO_REPEAT_PATTERNS]
QUANTITY_WORDS = re.compile(r'\b(?:share|shares|unit|units)\b', re.I)
read_json = lambda p: json.loads(p.read_text())
read_jsonl = lambda p: [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
out = root / 'outputs'
protocol = read_json(out/'sparse_baseline/protocol.json')
users = protocol['users']
assert len(users) == 30
contexts = {c['user_id']: c for c in read_jsonl(out/'sparse_baseline/contexts.jsonl')}
data = root.parent / 'Session 1/FAR-Trans'
for name, digest in protocol['source_sha256'].items():
    assert hashlib.sha256((data/name).read_bytes()).hexdigest() == digest
assets, profiles, history, truth, end, excluded = starter.load_data(data, '2021-06-01', 30)
relevant = {u: truth.get(u, set()) & set(contexts[u]['eligible_asset_ids']) for u in users}
assert all(relevant.values()) and end == protocol['end_exclusive']
baseline = read_json(out/'sparse_baseline/metrics.json')
metrics, metadata, scores, logs = {}, {}, {}, {}
for arm in ('A', 'B', 'C', 'C2'):
    evaluation = out / f'sparse_arm_{arm}_eval'
    run = out / f'sparse_arm_{arm}'
    assert read_json(evaluation/'protocol.json') == protocol
    metrics[arm] = read_json(evaluation/'metrics.json')
    assert metrics[arm]['protocol_hash'] == protocol['protocol_hash']
    for method, row in baseline['methods'].items():
        assert metrics[arm]['methods'][method] == row
    metadata[arm] = read_json(run/'run_meta.json')
    assert metadata[arm]['users'] == 30
    assert metadata[arm]['resolved_commit'] == '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e'
    assert metadata[arm]['generation'] == {'do_sample':False,'seed':0,'summary_max_new_tokens':120,'rank_max_new_tokens':60}
    raw = read_jsonl(run/'raw_log.jsonl')
    assert len(raw) == 30 and [r['user_id'] for r in raw] == users
    assert sum(not r['valid'] for r in raw) == metadata[arm]['invalid_outputs']
    logs[arm] = {r['user_id']:r for r in raw}
    with (evaluation/'per_user.csv').open(newline='') as stream:
        rows = [r for r in csv.DictReader(stream) if r['method'] == 'custom']
    assert len(rows) == 30 and {r['user_id'] for r in rows} == set(users)
    scores[arm] = {r['user_id']:float(r['ndcg_at_10']) for r in rows}
    predictions = {u:{} for u in users}
    with (evaluation/'predictions.csv').open(newline='') as stream:
        for row in csv.DictReader(stream):
            if row['method'] == 'custom':
                predictions[row['user_id']][int(row['rank'])] = row['ISIN']
    for row in rows:
        u = row['user_id']
        assert int(row['relevant_count']) == len(relevant[u])
        assert set(predictions[u]) == set(range(1,11))
        ranking = [predictions[u][i] for i in range(1,11)]
        starter.validate_ranking(ranking, [a['id'] for a in contexts[u]['candidate_assets']])
        assert starter.ndcg10(ranking,relevant[u]) == scores[arm][u]

original_hash = hashlib.sha256((root/'llm_rerank.py').read_bytes()).hexdigest()
c2_hash = hashlib.sha256((root/'llm_rerank_c2.py').read_bytes()).hexdigest()
assert original_hash == '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'
assert c2_hash == '0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada'
lines = ['# Exploratory: prompt designed after inspecting Arm C errors; not pre-registered', '',
         '## Scope and provenance', '',
         'Sparse supplementary cohort only: the same 30 users selected for having 1–5 historical eligible Buys and nonempty future purchases. This is not the default 100-user HW2 protocol. Only the conditional nonempty-truth mean is meaningful; all-selected-user and nonempty means coincide. Main results and prior model outputs were not changed. Descriptive measurements only; no conclusions, semantic factuality judgments or significance claims.', '',
         '- Original script SHA-256: `' + original_hash + '`.',
         '- C2 copy SHA-256: `' + c2_hash + '`.',
         '- C2 changes only the non-D task text in summary_prompt(). SUMMARY_SYSTEM, D behaviour, ranker template, parser, defaults and token limits remain identical. The internal --arm is C; C2 is the experiment/output label.',
         '- Model: Qwen/Qwen3-1.7B, resolved revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, CPU float32, thinking off, greedy decoding, seed 0, threads flag 0, 120 summary and 60 ranking max_new_tokens.',
         '- Protocol hash: `' + protocol['protocol_hash'] + '`. C2 evaluation protocol exactly equals the sparse baseline, and all four baseline aggregate blocks match at full saved precision.', '',
         '## Prompt-only diff', '', '```diff']
lines += list(difflib.unified_diff((root/'llm_rerank.py').read_text().splitlines(), (root/'llm_rerank_c2.py').read_text().splitlines(), fromfile='llm_rerank.py', tofile='llm_rerank_c2.py', lineterm=''))
lines += ['```', '', '## Launch and completion', '',
          'Initial detached launch: 2026-11-16 16:50:04 +03:00, supervisor 75145. The waiting tool call was interrupted; on continuation the process was absent and its log ended during checkpoint loading, with no raw output or metadata. Cause unverified. That log was preserved as outputs/sparse_c2_interrupted_20261116T165004.log. No results or timing were inferred from it.', '',
          'Identical retry: process start 2026-11-16 17:38:42 +03:00 (launch returned 17:38:43), supervisor 75926, model process 75929. The two-minute check passed, but the kernel killed model PID 75929 for global out-of-memory at 17:57:44. Its log and partial directory were preserved as outputs/sparse_c2_oom_20261116T175744.log and outputs/sparse_arm_C2_oom_20261116T175744/. A further user-authorized retry at 19:03:36, supervisor 81026/model 81029, was also killed by the kernel for OOM at 19:04:09 during checkpoint loading; its log was preserved as outputs/sparse_c2_oom_20261116T190409.log. Neither produced completed results.', '',
          'After another explicit continuation, the identical command was launched again at 2026-11-16 19:38:22 +03:00 (returned 19:38:23), supervisor 82133/model 82136. At 19:40:31, elapsed 2 min 7 s, it was running with both shards loaded and 0 flushed raw-log lines. The earlier sparse C timing suggested roughly 20:24 plus startup, but the process exceeded that estimate. At 20:31 it was still active at about 193% CPU, with 0 flushed rows, about 1.1 GiB available RAM and 3.7/4 GiB swap used. No settings or external applications were changed by the agent. Completion and elapsed time below are taken from the successful run metadata, not inferred from these interim checks.', '',
          'Detached command:', '', '```bash',
          'setsid nohup systemd-inhibit --what=sleep:idle --why="HW2 exploratory sparse C2" .venv/bin/python llm_rerank_c2.py --run-dir outputs/sparse_baseline --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --arm C --model Qwen/Qwen3-1.7B --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e --out-dir outputs/sparse_arm_C2 < /dev/null > outputs/sparse_c2.log 2>&1 &', '```', '',
          'Scoring uses the unchanged starter, only after confirming 30 raw rows and completed run_meta.json:', '', '```bash',
          'python3 starter.py run --data-dir "/home/dastan/Recommender Systems/Project/Session 1/FAR-Trans" --output-dir outputs/sparse_arm_C2_eval --users-file cohorts/sparse_labelled.txt --stage ranker --responses outputs/sparse_arm_C2/responses.jsonl --on-invalid fallback', '```', '',
          '## a. Sparse-cohort scores and timings', '',
          '| Method | Users | Nonempty users | nDCG@10 all selected users | nDCG@10 nonempty | Invalid outputs | Scoring failures | Wall time |', '|---|---:|---:|---:|---:|---:|---:|---|']
cbf = metrics['C2']['methods']['cbf']
lines.append(f"| CBF | 30 | 30 | {cbf['ndcg_at_10']:.4f} | {cbf['ndcg_at_10_nonempty']:.4f} | 0 (not model-generated) | 0 | Not measured for supplementary baseline |")
for arm in ('A','B','C','C2'):
    m = metrics[arm]['methods']['custom']
    lines.append(f"| {arm} | 30 | 30 | {m['ndcg_at_10']:.4f} | {m['ndcg_at_10_nonempty']:.4f} | {metadata[arm]['invalid_outputs']} | {len(metrics[arm]['custom_failures'])} | {metadata[arm]['wall_seconds_whole_arm']:.1f} s |")
lines += ['', 'Wall times are recorded whole-arm loop times, excluding model loading and initial context/questionnaire reading; C and C2 include summary generation. Scoring time is separate and unmeasured. A/B/C values come from earlier unchanged sparse runs. C2 rows use outputs/sparse_arm_C2_eval/metrics.json and outputs/sparse_arm_C2/run_meta.json.', '',
          '| Comparison | Users | Mean nDCG@10 difference | C2 better | Equal | C2 worse |', '|---|---:|---:|---:|---:|---:|']
for other in ('C','A'):
    delta = [scores['C2'][u]-scores[other][u] for u in users]
    lines.append(f'| C2−{other} | 30 | {statistics.mean(delta):.8f} | {sum(x>0 for x in delta)} | {sum(x==0 for x in delta)} | {sum(x<0 for x in delta)} |')
lines += ['', 'Paired calculations use full saved per-user precision before rounding. All 30 users, including any invalid-output fallback cases, are retained. Each saved nDCG value was checked with starter.ndcg10 against unchanged starter truth and evaluation rankings.', '',
          '## b. Deterministic summary string checks', '',
          'The history is the actual capped text supplied to the summarizer, extracted from summary_prompt and checked equal across C/C2. ISIN presence is an exact case-sensitive substring check. Counts are parsed from the corresponding “bought Nx” lines; no external asset knowledge or semantic classifier is used.', '',
          '| Check | C | C2 |', '|---|---:|---:|']
stats = {}
for arm in ('C','C2'):
    total_isins = named_isins = all_repeat_users = repeat_users = quantity_users = contradiction_users = 0
    fractions = []
    for u in users:
        r = logs[arm][u]
        text = r['summary_prompt'].split('\n\n',1)[0]
        assert text == logs['C'][u]['summary_prompt'].split('\n\n',1)[0]
        pairs = re.findall(r'^- (\S+) \| .* \| bought (\d+)x$',text,flags=re.M)
        expected_rows = contexts[u]['history'][:20]
        assert pairs == [(a['id'],str(a['buy_count'])) for a in expected_rows]
        summary = r['summary']
        isins = {isin for isin,count in pairs}
        repeated = {isin for isin,count in pairs if int(count)>=2}
        named = {isin for isin in isins if isin in summary}
        total_isins += len(isins)
        named_isins += len(named)
        fractions.append(len(named)/len(isins))
        if repeated:
            repeat_users += 1
            all_repeat_users += int(repeated <= named)
        quantity_users += bool(QUANTITY_WORDS.search(summary))
        contradiction_users += bool(repeated and any(pattern.search(summary) for pattern in NO_REPEAT))
    stats[arm] = dict(total=total_isins,named=named_isins,macro=statistics.mean(fractions),repeat_users=repeat_users,all_repeat=all_repeat_users,quantity=quantity_users,no_repeat=contradiction_users)
format_values = [
    ('Share of history ISIN occurrences named (pooled across users)', lambda s: f"{s['named']}/{s['total']} ({s['named']/s['total']:.4%})"),
    ('Mean per-user share of history ISINs named', lambda s: f"{s['macro']:.4%}"),
    ('Users with ≥1 repeated asset: all repeated ISINs named', lambda s: f"{s['all_repeat']}/{s['repeat_users']} ({s['all_repeat']/s['repeat_users']:.4%})"),
    ('Summaries containing share/shares/unit/units (whole words)', lambda s: f"{s['quantity']}/30"),
    ('Summaries matching no-repeat wording when history has a repeated asset', lambda s: f"{s['no_repeat']}/30 (among {s['repeat_users']} repeated-history users)"),
]
for label, formatter in format_values:
    lines.append(f'| {label} | {formatter(stats["C"])} | {formatter(stats["C2"])} |')
lines += ['', '“Pooled” denominator counts each distinct history asset once per user (the same ISIN in two users counts twice). The mean per-user fraction is also shown to avoid confusing pooled and macro coverage. The repeated-asset denominator contains only users with at least one asset having buy_count≥2; users without repeats are excluded rather than counted as vacuous successes. These checks test naming only, not whether a named ISIN has the right count or attributes.', '',
          'Quantity-word count uses case-insensitive regex `\\b(?:share|shares|unit|units)\\b`. A summary saying “not shares” still counts; the check records words, not errors.', '',
          'No-repeat detection is case-insensitive and matches any of these predeclared patterns when at least one history asset has buy_count≥2:', '', '```text']
lines += NO_REPEAT_PATTERNS
lines += ['```', '',
          'Regex matches are a surface wording diagnostic, not a semantic contradiction adjudication. Unmatched paraphrases can be missed, and matched quotations or negated context can be counted. No rule was adapted after inspecting C2 output. String checks do not establish overall factuality, faithful asset-count mappings, absence of hallucinations, or summary completeness. The shared 120-token output limit is unchanged; automatic counts include exactly the saved summaries, including any truncated text.', '',
          'The report is aggregate-only: no raw customer IDs, per-user scores, histories, generated summaries, or instantiated prompts. The prompt diff above is source-template text, not customer data. All raw records stay in local outputs/.']
report = '\n'.join(lines) + '\n'
assert not any(u in report for u in profiles)
target = root/'results/task6_c2.md'
if target.exists():
    previous = target.read_text()
    assert 'Status — incomplete:' in previous, 'Refusing to overwrite a completed C2 report'
    archive = root/'results/task6_c2_incomplete_20261116.md'
    assert not archive.exists(), 'Refusing to overwrite prior status archive'
    with archive.open('x') as stream:
        stream.write(previous)
with target.open('w') as stream:
    stream.write(report)
print('All evaluations/protocols/baselines/per-user scores verified; report has no raw customer IDs.')
print(json.dumps(stats,indent=2))
print('Wrote results/task6_c2.md')
