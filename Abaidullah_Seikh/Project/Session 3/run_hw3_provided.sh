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
ranker = root.parent / 'Session 2/far-trans-llm/ranker.py'
starter = root / 'starter.py'
verification_path = root / 'outputs/provided_llm_200_prepare/input_verification.json'
out = root / 'outputs/provided_llm_200'


def now():
    return datetime.now().astimezone().isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def progress(message):
    print(f'HW3_PROGRESS {now()} {message}', flush=True)


def check(condition, message):
    if not condition:
        progress(f'ERROR {message}')
        sys.exit(1)


check(sha(ranker) == '7c6b81794f7da10aab053074d86525b63d64aef10a08ff54ff5b6b8fa5de9f24',
      'provided ranker source hash mismatch')
check(sha(starter) == 'c19b21adeb824737d09835fb5b8818e2d310fee83e5af909eaf8897ea1705b24',
      'starter source hash mismatch')
check(sha(verification_path) == 'd61847f99eda8302e96c5a738a3df38be57b06794a5a6cbcef547ce288cda77e',
      'input verification hash mismatch')
verification = json.loads(verification_path.read_text())
check(verification['users'] == 200 and verification['same_users_in_order']
      and verification['same_candidate_sets'], 'prepare-only input compatibility failed')
for name, expected in verification['sha256'].items():
    check(sha(root / name) == expected, 'verified input artifact changed')
contexts = [json.loads(line) for line in
            (root / 'outputs/baseline_200/contexts.jsonl').read_text().splitlines() if line.strip()]
check(len(contexts) == len({row['user_id'] for row in contexts}) == 200, 'input count mismatch')
check(not out.exists(), 'provided output directory already exists')
available = next(int(line.split()[1]) * 1024 for line in Path('/proc/meminfo').read_text().splitlines()
                 if line.startswith('MemAvailable:'))
check(available >= 6.5 * 1024 ** 3, 'MemAvailable below 6.5 GiB')

command = [python, str(ranker), '--starter-dir', str(root),
           '--data-dir', '../Session 1/FAR-Trans', '--cutoff', '2021-06-01',
           '--horizon-days', '30', '--max-users', '200', '--candidate-count', '50',
           '--model', 'Qwen/Qwen3-1.7B', '--revision', '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e',
           '--device', 'cpu', '--on-invalid', 'fallback', '--output-dir', 'outputs/provided_llm_200']
out.mkdir()
provenance = {
    'script': str(ranker), 'script_sha256': sha(ranker),
    'starter': str(starter), 'starter_sha256': sha(starter),
    'support_sources_sha256': {path.name: sha(path) for path in
                               (ranker.parent / 'data_adapter.py', ranker.parent / 'runtime.py')},
    'exact_command': shlex.join(command), 'command_argv': command,
    'working_directory': str(root), 'start_time': now(),
    'baseline_protocol_hash': verification['baseline_protocol_hash'],
    'input_verification_sha256': sha(verification_path),
    'input_verification': verification,
    'protocol_hash_compatibility_reason': verification['launch_reason'],
    'defaults': {'shuffle_seed': None, 'history_events': 15, 'allow_download': False},
    'environment': {'PYTHONDONTWRITEBYTECODE': '1'},
    'mem_available_gib_at_start': available / 1024 ** 3,
}


def save_provenance():
    temporary = out / 'run_provenance.json.tmp'
    temporary.write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
    temporary.replace(out / 'run_provenance.json')


save_provenance()
progress('START outputs/provided_llm_200 expected_users=200')
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL)
except OSError as error:
    provenance.update(end_time=now(), exit_code=127, launch_error=str(error))
    save_provenance()
    progress('ERROR outputs/provided_llm_200 launch_failed exit_code=127')
    sys.exit(127)
progress(f'RUNNING outputs/provided_llm_200 model_pid={process.pid}')
while True:
    try:
        code = process.wait(timeout=60)
        break
    except subprocess.TimeoutExpired:
        responses = out / 'ranker_responses.jsonl'
        completed = responses.read_bytes().count(b'\n') if responses.exists() else 0
        progress(f'RUNNING outputs/provided_llm_200 elapsed_seconds={int(time.monotonic() - started)} '
                 f'completed_users={completed}/200')
provenance.update(end_time=now(), exit_code=code)
save_provenance()
if code != 0:
    progress(f'ERROR outputs/provided_llm_200 exit_code={code}')
    sys.exit(code if code > 0 else 128 - code)
progress('FINISH outputs/provided_llm_200 exit_code=0')
PY
