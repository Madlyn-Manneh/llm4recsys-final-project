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
protocol_hash = 'd46b45deaf2c2f955c52fa020082971947d5ac8e27073a90d1c5384f648af697'
runs = [
    ('A', 'llm_rerank.py', '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da',
     'outputs/A_101_200_input', 'outputs/arm_A_101_200', 100),
    ('C', 'llm_rerank_c2.py', '0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada',
     'outputs/baseline_200', 'outputs/arm_C2_200', 200),
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
# Check both jobs before starting either one; never overwrite archived runs.
for arm, script, expected, inputs, output, count in runs:
    check(sha(root / script) == expected, f'{script} source hash mismatch')
    check(not (root / output).exists(), f'{output} already exists')
    check(len((root / inputs / 'contexts.jsonl').read_bytes().splitlines()) == count,
          f'{inputs} context count mismatch')
    check(json.loads((root / inputs / 'protocol.json').read_text())['protocol_hash'] == protocol_hash,
          f'{inputs} protocol hash mismatch')

for arm, script, expected, inputs, output, count in runs:
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
    progress(f'START {output} expected_users={count}')
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
                     f'persisted_response_lines={written}/{count}')
    provenance.update(end_time=now(), exit_code=code)
    save_provenance()
    if code != 0:
        progress(f'ERROR {output} exit_code={code}; stopping sequence')
        sys.exit(code if code > 0 else 128 - code)
    progress(f'FINISH {output} exit_code=0')
progress('COMPLETE both runs finished sequentially')
PY
