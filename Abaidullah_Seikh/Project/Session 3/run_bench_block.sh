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
inputs = 'outputs/block_301_400'
output = 'outputs/block3_A'
script = 'llm_rerank.py'
expected_script = '85328db5d618b03a19287a59a853444f7a2e60885247c0d495a46f47a23667da'
expected_protocol = '6030d7f4a7b175bce50b0e2a6f90dd6eb2a64df5fbc69827b5ac5f1ab64a3764'


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


check(sha(root / 'BENCH_PLAN_301_400.md') ==
      '8364b5f311bdf8a842734eabd6ca5805c10be9623ce01b4a94c64bf26b5d43d4',
      'benchmark plan hash mismatch')
check(sha(root / 'starter.py') ==
      'c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24',
      'starter hash mismatch')
check(sha(root / script) == expected_script, 'arm A source hash mismatch')
check(sha(root / 'scripts/hw3_repeat_first.py') ==
      'e1401a71475dcd50c0db56f01284f0086e76a6d12f1e0d9846c1a088a067c437',
      'registered repeat-first source hash mismatch')
cohort = root / 'cohorts/block_301_400_users.txt'
check(sha(cohort) == '373e60e90fa6685e982d04d42eb687c30eb01b8009bf1324fd4f36cceac8aac6',
      'benchmark cohort hash mismatch')
protocol = json.loads((root / inputs / 'protocol.json').read_text())
check(protocol['protocol_hash'] == expected_protocol, 'benchmark protocol hash mismatch')
unsigned = {key: value for key, value in protocol.items() if key != 'protocol_hash'}
check(hashlib.sha256(json.dumps(unsigned, sort_keys=True).encode()).hexdigest() == expected_protocol,
      'benchmark protocol content hash mismatch')
contexts = [json.loads(line) for line in
            (root / inputs / 'contexts.jsonl').read_text().splitlines() if line.strip()]
users = cohort.read_text().splitlines()
check(len(contexts) == len(users) == len(set(users)) == 100, 'benchmark input count mismatch')
check([row['user_id'] for row in contexts] == users == protocol['users'], 'benchmark user order mismatch')
check(protocol['cutoff'] == '2021-06-01' and protocol['end_exclusive'] == '2021-07-01'
      and protocol['candidate_count'] == 50 and protocol['cohort_selection'] == 'warm'
      and not protocol['exclude_seen'], 'benchmark prompt-input settings mismatch')
check(all(len(ctx['candidate_assets']) == 50 for ctx in contexts), 'benchmark candidate count mismatch')
out = root / output
check(not out.exists(), 'benchmark A output already exists')
available = next(int(line.split()[1]) * 1024 for line in Path('/proc/meminfo').read_text().splitlines()
                 if line.startswith('MemAvailable:'))
check(available >= 6.5 * 1024 ** 3, 'MemAvailable below 6.5 GiB')
out.mkdir()
command = [python, script, '--arm', 'A', '--run-dir', inputs,
           '--out-dir', output, '--data-dir', '../Session 1/FAR-Trans']
provenance = {
    'script': script, 'script_sha256': sha(root / script),
    'starter_sha256': sha(root / 'starter.py'),
    'contexts_sha256': sha(root / inputs / 'contexts.jsonl'),
    'protocol_json_sha256': sha(root / inputs / 'protocol.json'),
    'protocol_hash': expected_protocol, 'cohort_sha256': sha(cohort),
    'registration_sha256': sha(root / 'BENCH_PLAN_301_400.md'),
    'exact_command': shlex.join(command), 'command_argv': command,
    'working_directory': str(root), 'start_time': now(),
    'blind_rule': 'No fresh-block metrics, truth counts, nonempty counts, or baseline scores inspected.',
    'candidate_policy': '50-candidate prompt for A; registered B1/B2 rules later use all eligible assets.',
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
    progress(f'ERROR {output} exit_code={code}')
    sys.exit(code if code > 0 else 128 - code)
progress(f'FINISH {output} exit_code=0')
PY
