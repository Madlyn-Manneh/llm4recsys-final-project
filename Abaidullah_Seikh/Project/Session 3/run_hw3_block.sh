#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
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
data = '../Session 1/FAR-Trans'
inputs = 'outputs/block_201_300'
expected_protocol = 'e126569ce481716d7039c495e2c7fedbbbe552e308b819b84c4be87b0eb5fe8d'
runs = [
    ('A', 'llm_rerank.py', '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da',
     'outputs/block_A'),
    ('C', 'llm_rerank_c2.py', '0df30c0e913209daa7ce823e0c0f7569f16ca3059a7bfe4a57bd853792f28ada',
     'outputs/block_C'),
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


check(sha(root / 'HW3_BLOCK_201_300.md') ==
      'a99403c56472dde79a5767c7c85a34826ecbc34e8f9c0d8c1187df91a7d18bb6',
      'held-out block registration hash mismatch')
check(sha(root / 'HW3_PROTOCOL.md') ==
      '427e05eea001910c4c1f02169915ee5efbc27b5b5463fa0fdceb824ecd3c2146',
      'base protocol document hash mismatch')
check(sha(root / 'starter.py') ==
      'c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24',
      'starter hash mismatch')
cohort = root / 'cohorts/block_201_300_users.txt'
check(sha(cohort) == '486242db9b78ccfa1743075bfbda5dee9945571defbc518d76e8993bba54dd59',
      'block cohort hash mismatch')
protocol = json.loads((root / inputs / 'protocol.json').read_text())
check(protocol['protocol_hash'] == expected_protocol, 'block protocol hash mismatch')
unsigned = {key: value for key, value in protocol.items() if key != 'protocol_hash'}
check(hashlib.sha256(json.dumps(unsigned, sort_keys=True).encode()).hexdigest() == expected_protocol,
      'block protocol content hash mismatch')
contexts = [json.loads(line) for line in
            (root / inputs / 'contexts.jsonl').read_text().splitlines() if line.strip()]
users = cohort.read_text().splitlines()
check(len(contexts) == len(users) == len(set(users)) == 100, 'block input count mismatch')
check([row['user_id'] for row in contexts] == users == protocol['users'], 'block user order mismatch')
check(protocol['cutoff'] == '2021-06-01' and protocol['end_exclusive'] == '2021-07-01'
      and protocol['candidate_count'] == 50 and protocol['cohort_selection'] == 'warm'
      and not protocol['exclude_seen'], 'block protocol settings mismatch')
check(all(len(ctx['candidate_assets']) == 50 for ctx in contexts), 'block candidate count mismatch')
for arm, script, expected, output in runs:
    check(sha(root / script) == expected, f'{script} source hash mismatch')
    check(not (root / output).exists(), f'{output} already exists')
input_hashes = {'contexts_sha256': sha(root / inputs / 'contexts.jsonl'),
                'protocol_json_sha256': sha(root / inputs / 'protocol.json')}

for arm, script, expected, output in runs:
    check(sha(root / script) == expected, f'{script} source hash mismatch')
    check(sha(root / inputs / 'contexts.jsonl') == input_hashes['contexts_sha256']
          and sha(root / inputs / 'protocol.json') == input_hashes['protocol_json_sha256'],
          'block inputs changed during sequence')
    out = root / output
    out.mkdir()
    command = [python, script, '--arm', arm, '--run-dir', inputs,
               '--out-dir', output, '--data-dir', data]
    provenance = {
        'script': script, 'script_sha256': sha(root / script),
        **input_hashes, 'protocol_hash': expected_protocol,
        'starter_sha256': sha(root / 'starter.py'), 'cohort_sha256': sha(cohort),
        'registration_sha256': sha(root / 'HW3_BLOCK_201_300.md'),
        'exact_command': shlex.join(command), 'command_argv': command,
        'working_directory': str(root), 'start_time': now(),
        'blind_rule': 'No block metrics, truth counts, nonempty counts, or baseline scores inspected.',
    }

    def save_provenance():
        temporary = out / 'run_provenance.json.tmp'
        temporary.write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
        temporary.replace(out / 'run_provenance.json')

    save_provenance()
    progress(f'START {output} expected_users=100')
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
                     f'persisted_response_lines={written}/100')
    provenance.update(end_time=now(), exit_code=code)
    save_provenance()
    if code != 0:
        progress(f'ERROR {output} exit_code={code}; stopping sequence')
        sys.exit(code if code > 0 else 128 - code)
    progress(f'FINISH {output} exit_code=0')
progress('COMPLETE both block runs finished sequentially')
PY
