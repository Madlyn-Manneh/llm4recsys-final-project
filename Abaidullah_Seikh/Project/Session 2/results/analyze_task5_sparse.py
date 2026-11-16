"""Evaluate saved supplementary sparse runs; no model imports or generation."""
import csv
import hashlib
import json
import statistics
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import starter

out = root / 'outputs'
results = root / 'results'
read_json = lambda path: json.loads(path.read_text())
read_jsonl = lambda path: [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
protocol = read_json(out / 'sparse_baseline/protocol.json')
baseline = read_json(out / 'sparse_baseline/metrics.json')
contexts = {c['user_id']: c for c in read_jsonl(out / 'sparse_baseline/contexts.jsonl')}
users = protocol['users']
assert len(users) == len(contexts) == 30
assert users == (root / 'cohorts/sparse_labelled.txt').read_text().splitlines()
assert protocol['protocol_hash'] == '0dcf62736b07cd927359ba330ce7dcda3165ef907f9aa1f0b902834fb169926b'
assert hashlib.sha256((root / 'llm_rerank.py').read_bytes()).hexdigest() == '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'
log_text = (out / 'sparse_runs.log').read_text()
assert 'FAILED' not in log_text
assert all(f'ARM {arm} DONE' in log_text for arm in 'CAB')
data = root.parent / 'Session 1/FAR-Trans'
for name, digest in protocol['source_sha256'].items():
    assert hashlib.sha256((data / name).read_bytes()).hexdigest() == digest
assets, profiles, history, truth, end, excluded = starter.load_data(data, '2021-06-01', 30)
assert end == protocol['end_exclusive']
relevant = {u: truth.get(u, set()) & set(contexts[u]['eligible_asset_ids']) for u in users}
assert all(relevant.values())
assert all(1 <= sum(history[u].values()) <= 5 for u in users)
metrics, metadata, scores, rankings, raw = {}, {}, {}, {}, {}
for arm in 'ABC':
    evaluation = out / f'sparse_arm_{arm}_eval'
    run = out / f'sparse_arm_{arm}'
    assert read_json(evaluation / 'protocol.json') == protocol
    metrics[arm] = read_json(evaluation / 'metrics.json')
    assert metrics[arm]['protocol_hash'] == protocol['protocol_hash']
    for method, values in baseline['methods'].items():
        assert metrics[arm]['methods'][method] == values
    metadata[arm] = read_json(run / 'run_meta.json')
    assert metadata[arm]['users'] == 30 and metadata[arm]['invalid_outputs'] == 0
    assert metadata[arm]['protocol_hash'] == protocol['protocol_hash']
    assert metadata[arm]['resolved_commit'] == '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e'
    raw_rows = read_jsonl(run / 'raw_log.jsonl')
    assert len(raw_rows) == 30 and [r['user_id'] for r in raw_rows] == users
    raw[arm] = {r['user_id']: r for r in raw_rows}
    assert all(r['valid'] for r in raw_rows)
    with (evaluation / 'per_user.csv').open(newline='') as stream:
        per_user = [r for r in csv.DictReader(stream) if r['method'] == 'custom']
    assert len(per_user) == 30 and {r['user_id'] for r in per_user} == set(users)
    scores[arm] = {r['user_id']: float(r['ndcg_at_10']) for r in per_user}
    rankings[arm] = {u: {} for u in users}
    with (evaluation / 'predictions.csv').open(newline='') as stream:
        for row in csv.DictReader(stream):
            if row['method'] == 'custom':
                rank = int(row['rank'])
                assert rank not in rankings[arm][row['user_id']]
                rankings[arm][row['user_id']][rank] = row['ISIN']
    for row in per_user:
        u = row['user_id']
        assert int(row['relevant_count']) == len(relevant[u])
        assert set(rankings[arm][u]) == set(range(1, 11))
        ranking = [rankings[arm][u][i] for i in range(1, 11)]
        pool = [a['id'] for a in contexts[u]['candidate_assets']]
        starter.validate_ranking(ranking, pool)
        assert starter.ndcg10(ranking, relevant[u]) == scores[arm][u]
        if not metrics[arm]['custom_failures']:
            assert ranking == [pool[i-1] for i in raw[arm][u]['parsed_numbers']]

mean = statistics.mean
differing = [u for u in users if len({scores[a][u] for a in 'ABC'}) > 1]
mention_count = sum(any(a['id'] in raw['C'][u]['summary'] for a in contexts[u]['history']) for u in users)
lines = ['# Supplementary cohort: 30 sparse users with future purchases; not the HW2 default protocol', '',
         'Descriptive results only; no conclusions or significance claims. The main HW2 results are unchanged. The cohort is selected on having nonempty future truth: only the conditional nonempty mean is meaningful. The all-selected-user and nonempty means coincide because all 30 users are labelled; this is not the default 100-user all-user population mean.', '',
         '## Completion and evaluation checks', '',
         '- Completion checked on 2026-11-16 at approximately 15:42 +03:00. All C/A/B DONE markers are present; no FAILED marker appears. All raw logs have exactly 30 lines; no llm_rerank.py process was running.',
         '- C finished at 12:33:51, A at 13:04:28, B at 13:34:06, November 16 (+03:00), from the saved loop log.',
         '- All three complete evaluation protocol objects exactly match the supplementary baseline. The four baseline aggregate blocks match at full saved precision in every evaluation.',
         '- Protocol hash: `' + protocol['protocol_hash'] + '`.',
         '- The unchanged starter constructs truth; source CSV hashes were checked against the supplementary protocol. Every custom per-user score was verified with starter.ndcg10 using predictions.csv and eligible truth.',
         '- Protected model script SHA-256 remains `85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da`.', '',
         '## Seven-method table', '',
         '| Method | Users | Users with future purchases | nDCG@10 all users | nDCG@10 nonempty truth | Runtime | Failed cases |',
         '|---|---:|---:|---:|---:|---|---:|']
for method, name in [('popularity', 'Popularity'), ('cbf', 'CBF (fixed top-50 no-rerank control)'), ('latest_buy', 'Latest buy'), ('latest_buy_or_sell', 'Latest buy or sell')]:
    m = metrics['A']['methods'][method]
    lines.append(f"| {name} | {m['users']} | {m['nonempty_truth_users']} | {m['ndcg_at_10']:.4f} | {m['ndcg_at_10_nonempty']:.4f} | Not measured for supplementary baseline run | 0 |")
for arm, name in [('A', 'structured'), ('B', 'history text'), ('C', 'LLM summary')]:
    m = metrics[arm]['methods']['custom']
    time_text = f"{metadata[arm]['wall_seconds_whole_arm']:.1f} s, whole arm, excluding model loading"
    if arm == 'C':
        time_text += ' (includes summaries)'
    lines.append(f"| Arm {arm} ({name}) | {m['users']} | {m['nonempty_truth_users']} | {m['ndcg_at_10']:.4f} | {m['ndcg_at_10_nonempty']:.4f} | {time_text} | {metadata[arm]['invalid_outputs']} |")
lines += ['', 'Baseline rows are copied from `outputs/sparse_arm_A_eval/metrics.json`, confirmed identical to `outputs/sparse_baseline/metrics.json` and the B/C evaluation baseline blocks. Arm rows use method `custom` in the respective `outputs/sparse_arm_{A,B,C}_eval/metrics.json`; invalid counts and times use `outputs/sparse_arm_{A,B,C}/run_meta.json`.', '',
          'The supplementary baseline command was not externally timed. The main protocol’s 10.77-second baseline runtime is not reused here. Arm timers exclude model loading, initial context/questionnaire reading and later scoring. They include the per-user loop, generation, parsing and log writes. Classical failed cases are 0 (no model output to validate).', '',
          '| Arm | invalid_outputs | Scoring custom_failures | wall_seconds_whole_arm |', '|---|---:|---:|---:|']
for arm in 'ABC':
    lines.append(f"| {arm} | {metadata[arm]['invalid_outputs']} | {len(metrics[arm]['custom_failures'])} | {metadata[arm]['wall_seconds_whole_arm']:.1f} |")
lines += ['', 'All three arms used the HF backend, Qwen/Qwen3-1.7B at resolved revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, float32 CPU, greedy decoding and explicit thinking off, seed 0, summary budget 120 and ranking budget 60 new tokens. No model was rerun for scoring or this analysis.', '',
          '## Paired nDCG@10 differences', '',
          'Calculated before rounding from custom per_user.csv. Better/equal/worse compares C with the named comparator at full saved precision. All-selected and nonempty populations are the same 30 users.', '',
          '| Comparison | Users | Mean difference | C better | Equal | C worse | Sum of differences |', '|---|---:|---:|---:|---:|---:|---:|']
for other in 'AB':
    delta = [scores['C'][u]-scores[other][u] for u in users]
    lines.append(f'| C−{other} | 30 | {mean(delta):.8f} | {sum(x>0 for x in delta)} | {sum(x==0 for x in delta)} | {sum(x<0 for x in delta)} | {sum(delta):.12f} |')
lines += ['', '## Hits, Recall@10 and CBF overlap', '',
          'A hit is a distinct relevant ISIN in the top ten. Recall@10 = hits / number of distinct eligible future ISINs per user; reported means are macro means, not pooled micro recall. CBF overlap is the mean set-intersection size (0–10) and fraction with the original CBF top ten.', '',
          '| Arm | Users with ≥1 hit (of 30) | Total hits | Recall@10 all selected users | Recall@10 nonempty | Mean CBF top-10 overlap | Mean overlap fraction |', '|---|---:|---:|---:|---:|---:|---:|']
for arm in 'ABC':
    hits = [len(set(rankings[arm][u].values()) & relevant[u]) for u in users]
    recalls = [h/len(relevant[u]) for h, u in zip(hits, users)]
    overlaps = [len(set(rankings[arm][u].values()) & {a['id'] for a in contexts[u]['candidate_assets'][:10]}) for u in users]
    lines.append(f'| {arm} | {sum(h>0 for h in hits)} | {sum(hits)} | {mean(recalls):.8f} | {mean(recalls):.8f} | {mean(overlaps):.4f} | {mean(overlaps)/10:.4f} |')
covered = sum(len(relevant[u] & {a['id'] for a in contexts[u]['candidate_assets']}) for u in users)
lines += ['', '## Summary mentions and differing-user count', '',
          f'- **{mention_count} of 30** C summaries mention at least one exact, case-sensitive history ISIN. This is string presence only, not a factuality judgment.',
          f'- **{len(differing)} of 30** users have different saved nDCG@10 between at least two arms; **{30-len(differing)}** have equal scores in all three. This counts score differences, not all changes in recommendation lists.',
          f'- Evaluation-only top-50 coverage remains **{covered} of {sum(map(len,relevant.values()))}** future user–asset labels.', '',
          'Detailed identified users, truth ISINs, hit positions, scores and verbatim histories/summaries are saved only in `results/task5_sparse_differing_LOCAL.md` and must never be committed. This aggregate report contains no raw customer IDs, histories, prompts, summaries or per-user rows.']
aggregate = '\n'.join(lines) + '\n'
assert not any(uid in aggregate for uid in profiles)

local = ['# Supplementary sparse cohort: differing users — LOCAL ONLY', '',
         '**Contains raw customer IDs, histories and model summaries. Never commit. Not the HW2 default protocol.**', '',
         'Descriptive listing only; no judgments about the summaries or ranking results. Sources are custom per_user.csv and predictions.csv from the three supplementary evaluation directories, plus the saved B/C raw logs. Truth is from imported unchanged starter.load_data(), intersected with eligible IDs. All 30 custom scores were recomputed with starter.ndcg10 and checked against saved scores. Only this supplementary selected population is described.', '',
         'Protocol hash: `' + protocol['protocol_hash'] + '`.', '',
         f'**{len(differing)} users** have differing nDCG@10; listed in cohort/protocol order. Displayed nDCG values have four decimals; differences use full-precision scores.', '',
         '| User ID | True ISIN count | A nDCG@10 | B nDCG@10 | C nDCG@10 | C−A | C−B |', '|---|---:|---:|---:|---:|---:|---:|']
for u in differing:
    local.append(f'| {u} | {len(relevant[u])} | {scores["A"][u]:.4f} | {scores["B"][u]:.4f} | {scores["C"][u]:.4f} | {scores["C"][u]-scores["A"][u]:.12f} | {scores["C"][u]-scores["B"][u]:.12f} |')
local += ['', '## Sum-to-mean checks', '', '| Comparison | Sum over differing users | All-30 sum | All-30 mean |', '|---|---:|---:|---:|']
for other in 'AB':
    subtotal = sum(scores['C'][u]-scores[other][u] for u in differing)
    total = sum(scores['C'][u]-scores[other][u] for u in users)
    assert abs(subtotal-total) < 1e-14
    local.append(f'| C−{other} | {subtotal:.12f} | {total:.12f} | {total/30:.12f} |')
local += ['', 'Histories are extracted verbatim from C’s summary_prompt and checked equal to B’s actual Investor information block. Hit positions are 1-based; all hits are listed, not only the first. No assessment of retained or dropped information is supplied.']
for u in differing:
    text, separator, instruction = raw['C'][u]['summary_prompt'].partition('\n\n')
    assert separator
    b_history = raw['B'][u]['rank_prompt'].split('\n', 1)[1].split('\n\nCandidate assets:', 1)[0]
    assert text == b_history
    local += ['', f'## User `{u}`', '', f'**True ISIN count:** {len(relevant[u])}. **True ISINs:** ' + ', '.join(f'`{i}`' for i in sorted(relevant[u])), '',
              '| Arm | Every hit: ISIN and position (1–10) | nDCG@10 |', '|---|---|---:|']
    for arm in 'ABC':
        hits = [(rank, isin) for rank, isin in sorted(rankings[arm][u].items()) if isin in relevant[u]]
        hit_text = '; '.join(f'`{isin}` at position {rank}' for rank, isin in hits) or '(no hits)'
        local.append(f'| {arm} | {hit_text} | {scores[arm][u]:.4f} |')
    local += ['', f'**C−A:** {scores["C"][u]-scores["A"][u]:.12f}. **C−B:** {scores["C"][u]-scores["B"][u]:.12f}.', '',
              '**Arm B history (same history supplied to C’s summarizer):**', '', '```text', text, '```', '',
              '**Arm C summary:**', '', '```text', raw['C'][u]['summary'], '```']
local_report = '\n'.join(local) + '\n'
for path, text in [(results/'task5_sparse_results.md', aggregate), (results/'task5_sparse_differing_LOCAL.md', local_report)]:
    assert not path.exists(), f'Refusing to overwrite {path.name}'
    with path.open('x') as stream:
        stream.write(text)
print('All protocol, baseline, per-user nDCG and saved ranking checks passed.')
print('custom_failures:', {a: metrics[a]['custom_failures'] for a in 'ABC'})
print('Differing users:', len(differing), '/30; summaries mentioning history ISIN:', mention_count, '/30')
print('Wrote task5_sparse_results.md (aggregate, ID checked) and task5_sparse_differing_LOCAL.md.')
