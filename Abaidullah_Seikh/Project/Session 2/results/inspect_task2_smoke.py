"""Read and validate the completed real-model smoke artifacts; no generation."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import llm_rerank as pipeline

contexts, protocol = pipeline.load_run(root / 'outputs/baseline')
users = [c['user_id'] for c in contexts[:3]]
candidates = {c['user_id']: c['candidate_assets'] for c in contexts[:3]}
report_path = root / 'results/task2_smoke.md'
report = report_path.read_text() if report_path.exists() else None
for arm in 'ABC':
    directory = root / 'outputs' / ('smoke_' + arm)
    meta = json.loads((directory / 'run_meta.json').read_text())
    logs = [json.loads(line) for line in (directory / 'raw_log.jsonl').read_text().splitlines()]
    responses = [json.loads(line) for line in (directory / 'responses.jsonl').read_text().splitlines()]
    assert [r['user_id'] for r in logs] == users == [r['user_id'] for r in responses]
    assert meta['protocol_hash'] == protocol['protocol_hash']
    assert meta['resolved_commit'] == '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e'
    assert meta['backend'] == 'hf' and meta['dtype'] == 'torch.float32'
    assert meta['generation'] == {'do_sample': False, 'seed': 0, 'summary_max_new_tokens': 120, 'rank_max_new_tokens': 60}
    assert sum(not r['valid'] for r in logs) == meta['invalid_outputs']
    print('\nARM', arm, 'META', json.dumps(meta))
    print('100-user estimate seconds/minutes/hours:', meta['wall_seconds_whole_arm']*100/3,
          meta['wall_seconds_whole_arm']*100/3/60, meta['wall_seconds_whole_arm']*100/3/3600)
    for log, response, ctx in zip(logs, responses, contexts[:3]):
        output = log['rank_output']
        if report is not None:
            assert output in report, 'Raw ranking missing or altered in the report'
        assert '<think>' not in output.lower() and '</think>' not in output.lower()
        parsed = pipeline.parse_ranking(output, len(candidates[log['user_id']]))
        assert log['parsed_numbers'] == parsed
        assert response['ranked_ids'] == [candidates[log['user_id']][i-1]['id'] for i in parsed]
        assert len(response['ranked_ids']) == 10 == len(set(response['ranked_ids']))
        assert response['protocol_hash'] == protocol['protocol_hash']
        expected_info = (pipeline.structured_block(ctx) if arm == 'A' else
                         pipeline.history_block(ctx) if arm == 'B' else log['summary'])
        assert log['rank_prompt'] == pipeline.rank_prompt(ctx, expected_info)[1]
        print('USER', log['user_id'], 'RAW rank_output:', output)
        if arm == 'C':
            if report is not None:
                assert log['summary'] in report, 'Summary missing or altered in the report'
                assert pipeline.history_block(ctx) in report, 'Source history missing or altered in the report'
            assert log['summary_prompt'] == pipeline.summary_prompt(ctx, 'C', log['questionnaire_before_cutoff'])[1]
            print('HISTORY:\n' + pipeline.history_block(ctx))
            print('SUMMARY:\n' + log['summary'])
    print('PASS: three valid unique top-50 rankings, correct shared prompt, settings and commit; no think tags.')
