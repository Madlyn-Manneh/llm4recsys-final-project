#!/usr/bin/env bash
set -euo pipefail
PYTHON='/home/dastan/Recommender Systems/Abaidullah_Seikh/Project/Session 2/.venv/bin/python'
exec "$PYTHON" - <<'PY'
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time

root = Path.cwd()
python = '/home/dastan/Recommender Systems/Abaidullah_Seikh/Project/Session 2/.venv/bin/python'
data = root.parent / 'Session 1' / 'FAR-Trans'
inputs = 'outputs/sparse_baseline_120'
protocol = json.loads((root / inputs / 'protocol.json').read_text())
protocol_hash = protocol['protocol_hash']
runs = [
    ('A', 'llm_rerank.py', '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da',
     'outputs/sparse_A'),
    ('C', 'llm_rerank_c2.py', '0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada',
     'outputs/sparse_C'),
    ('C', 'llm_rerank.py', '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da',
     'outputs/sparse_oldC'),
]


def now():
    return datetime.now().astimezone().isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def progress(message):
    print(f'HW3_PROGRESS {now()} {message}', flush=True)


def check(condition, message):
    if not condition:
        progress(f'ERROR {message}')
        sys.exit(1)


check(sha(root / 'HW3_PROTOCOL.md') ==
      '427e05eea001910c4c1f02169915ee5efbc27b5b5463fa0fdceb824ecd3c2146',
      'frozen protocol document hash mismatch')
check(protocol_hash == '5f470cfbb37d3985ea0996f564d059429b59fcd5dc747ff07632eb4e11589069',
      'sparse protocol hash mismatch')
contexts = [json.loads(line) for line in
            (root / inputs / 'contexts.jsonl').read_text().splitlines() if line.strip()]
users = (root / 'cohorts/sparse_window_users.txt').read_text().splitlines()
check(len(contexts) == len(users) == len(set(users)) == 120, 'sparse input count mismatch')
check([row['user_id'] for row in contexts] == protocol['users'] == users,
      'sparse user order mismatch')
check(protocol['cutoff'] == '2021-06-01' and protocol['end_exclusive'] == '2021-08-30'
      and protocol['candidate_count'] == 50 and protocol['cohort_selection'] == 'warm'
      and not protocol['exclude_seen'], 'sparse protocol settings mismatch')
for arm, script, expected, output in runs:
    check(sha(root / script) == expected, f'{script} source hash mismatch')
    check(not (root / output).exists(), f'{output} already exists')

for arm, script, expected, output in runs:
    check(sha(root / script) == expected, f'{script} source hash mismatch')
    out = root / output
    out.mkdir()
    command = [python, script, '--arm', arm, '--run-dir', inputs,
               '--out-dir', output, '--data-dir', str(data)]
    provenance = {
        'script': script,
        'script_sha256': sha(root / script),
        'contexts_sha256': sha(root / inputs / 'contexts.jsonl'),
        'protocol_json_sha256': sha(root / inputs / 'protocol.json'),
        'protocol_hash': protocol_hash,
        'exact_command': shlex.join(command),
        'command_argv': command,
        'working_directory': str(root),
        'start_time': now(),
    }
    provenance_path = out / 'run_provenance.json'

    def save_provenance():
        temporary = out / 'run_provenance.json.tmp'
        temporary.write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
        temporary.replace(provenance_path)

    save_provenance()
    progress(f'START {output} expected_users=120')
    started = time.monotonic()
    try:
        process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL)
    except OSError as error:
        provenance.update(end_time=now(), exit_code=127, launch_error=str(error))
        save_provenance()
        progress(f'ERROR {output} launch_failed exit_code=127')
        sys.exit(127)
    progress(f'RUNNING {output} model_pid={process.pid}')
    while True:
        try:
            code = process.wait(timeout=30)
            break
        except subprocess.TimeoutExpired:
            responses = out / 'responses.jsonl'
            written = responses.read_bytes().count(b'\n') if responses.exists() else 0
            progress(f'RUNNING {output} elapsed_seconds={int(time.monotonic() - started)} '
                     f'persisted_response_lines={written}/120')
    provenance.update(end_time=now(), exit_code=code)
    save_provenance()
    if code != 0:
        progress(f'ERROR {output} exit_code={code}; stopping sequence')
        sys.exit(code if code > 0 else 128 - code)
    progress(f'FINISH {output} exit_code=0')
progress('COMPLETE all three runs finished sequentially')
PY
