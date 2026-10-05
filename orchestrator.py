#!/usr/bin/env python3
"""Local deterministic task runner. No product code or live provider authority."""
from __future__ import annotations
import argparse
import contextlib
import dataclasses
import datetime as dt
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parent
STATUSES = {'NOT_STARTED', 'IN_PROGRESS', 'REVIEW', 'PASS', 'FAIL', 'BLOCKED'}
FIELDS = ['Status', 'Phase', 'Objective', 'Why', 'Dependencies', 'Source of Truth',
          'Likely Files', 'Requirements', 'Acceptance Criteria', 'Required Automated Tests',
          'Manual Verification', 'Financial / Provider Impact', 'Security / Ownership Impact',
          'Failure / Recovery Behavior', 'Out of Scope', 'Reviewer Notes', 'Completion Authority']
DEFAULT_CONFIG = {'max_repair_attempts': 3, 'agent_timeout_seconds': 7200,
                  'dashboard_port': 8765, 'auto_continue_after_pass': True,
                  'activated_optional_tasks': []}
CODEX_BASE = ['codex', '-a', 'never', 'exec', '--sandbox', 'workspace-write',
              '--ignore-user-config', '--ephemeral', '--color', 'never']
REVIEW_BASE = ['opencode', 'run', '--standalone', '--auto', '--format', 'default']

class SafetyError(RuntimeError):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def redact(text):
    # Never publish full environment/config. Conservative best-effort log redaction.
    text = re.sub(r'(?i)((?:api[_-]?key|access[_-]?token|authorization|password|secret)\s*[=:]\s*)([^\s,;]+)', r'\1[REDACTED]', str(text))
    text = re.sub(r'(?i)bearer\s+[^\s"\']+', 'Bearer [REDACTED]', text)
    text = re.sub(r'\b(?:sk-[A-Za-z0-9_-]{8,}|AIza[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]+)\b', '[REDACTED]', text)
    text = re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?(?:-----END [^-]*PRIVATE KEY-----|$)', '[REDACTED PRIVATE KEY]', text)
    return text


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            os.chmod(name, 0o600)
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@dataclasses.dataclass
class Task:
    id: str
    title: str
    fields: dict
    contract: str
    dependencies: list[str]
    optional: bool


def parse_tasks(path):
    text = Path(path).read_text()
    matches = list(re.finditer(r'^### (T\d{3}): (.+)$', text, re.M))
    if not matches:
        raise SafetyError('TASKS.md has no task contracts')
    tasks = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[match.start():end]
        # Phase/footer sections are outside the exact task contract.
        boundary = re.search(r'^## ', chunk, re.M)
        if boundary:
            chunk = chunk[:boundary.start()]
        fields = {}
        positions = list(re.finditer(r'^(' + '|'.join(re.escape(f) for f in FIELDS) + r'):(.*)$', chunk, re.M))
        for j, item in enumerate(positions):
            if item[1] in fields:
                raise SafetyError(f'Duplicate field in {match[1]}: {item[1]}')
            finish = positions[j + 1].start() if j + 1 < len(positions) else len(chunk)
            fields[item[1]] = (item[2] + chunk[item.end():finish]).strip()
        missing = set(FIELDS) - fields.keys()
        if missing or any(not fields.get(f) for f in FIELDS):
            raise SafetyError(f'Incomplete contract {match[1]}: {sorted(missing)}')
        if fields['Status'] not in STATUSES:
            raise SafetyError(f'Invalid declared status: {match[1]}')
        dep_text = fields['Dependencies']
        deps = re.findall(r'^- (T\d{3})\s*$', dep_text, re.M)
        if not deps and dep_text != '- None':
            raise SafetyError(f'Malformed dependencies: {match[1]}')
        if len(set(deps)) != len(deps):
            raise SafetyError(f'Duplicate dependencies: {match[1]}')
        optional = bool(re.search(r'^(?:Conditional|Optional)\b', match[2], re.I) or
                        re.search(r'leave NOT_STARTED until separately requested', fields['Requirements']))
        tasks.append(Task(match[1], match[2], fields, chunk.strip(), deps, optional))
    by_id = {t.id: t for t in tasks}
    if len(by_id) != len(tasks):
        raise SafetyError('Duplicate task IDs')
    visited, visiting = set(), set()
    def visit(task_id):
        if task_id not in by_id:
            raise SafetyError(f'Unknown dependency {task_id}')
        if task_id in visiting:
            raise SafetyError(f'Dependency cycle at {task_id}')
        if task_id in visited:
            return
        visiting.add(task_id)
        for dep in by_id[task_id].dependencies:
            visit(dep)
        visiting.remove(task_id)
        visited.add(task_id)
    for task in tasks:
        visit(task.id)
    # Cross-check the authoritative summary if present.
    summary = re.findall(r'^\| (T\d{3}) \| (None|T\d{3}(?:, T\d{3})*) \|$', text, re.M)
    if summary:
        if len(summary) != len(tasks):
            raise SafetyError('Dependency summary incomplete')
        for task_id, deps in summary:
            expected = [] if deps == 'None' else deps.split(', ')
            if task_id not in by_id or expected != by_id[task_id].dependencies:
                raise SafetyError(f'Dependency summary disagrees: {task_id}')
    return tasks, text[:matches[0].start()].strip()


def initial_state(tasks, spec_hash):
    return {'schema_version': 1, 'tasks_hash': spec_hash, 'run_id': None,
            'mode': 'IDLE', 'active_task_id': None, 'process': None,
            'latest_commit': None, 'tasks': {t.id: {'status': 'NOT_STARTED',
            'current_attempt': 0, 'repair_count': 0, 'start_timestamp': None,
            'last_transition_timestamp': None, 'last_codex_exit_code': None,
            'last_opencode_exit_code': None, 'reviewer_verdict': None,
            'blocker_reason': None, 'git_head_before': None, 'git_head_after': None}
            for t in tasks}}


def validate_state(state, tasks):
    if state.get('schema_version') != 1 or set(state.get('tasks', {})) != {t.id for t in tasks}:
        raise SafetyError('Unknown/corrupt runtime state; do not reset acceptance history')
    active = []
    for task in tasks:
        record = state['tasks'][task.id]
        if record.get('status') not in STATUSES:
            raise SafetyError('Invalid runtime status')
        if record['status'] in {'IN_PROGRESS', 'REVIEW', 'FAIL'}:
            active.append(task.id)
        if record['status'] == 'PASS' and any(state['tasks'][d]['status'] != 'PASS' for d in task.dependencies):
            raise SafetyError(f'PASS without accepted dependencies: {task.id}')
    if len(active) > 1 or (active and state.get('active_task_id') != active[0]):
        raise SafetyError('More than one active task or inconsistent active task')
    if state.get('active_task_id') and state['active_task_id'] not in state['tasks']:
        raise SafetyError('Unknown active task')


def load_state(root, tasks):
    spec_hash = digest((root / 'TASKS.md').read_bytes())
    path = root / '.orchestrator/state.json'
    if not path.exists() or not path.read_bytes().strip():
        return initial_state(tasks, spec_hash)
    try:
        state = json.loads(path.read_text())
    except (ValueError, OSError) as error:
        raise SafetyError('Corrupt state.json; operator recovery required') from error
    validate_state(state, tasks)
    if state['tasks_hash'] != spec_hash:
        raise SafetyError('TASKS.md changed since runtime initialization; human reconciliation required')
    return state


def next_task(tasks, state, config):
    validate_state(state, tasks)
    if state.get('active_task_id') or state.get('mode') == 'BLOCKED' or any(r['status'] == 'BLOCKED' for r in state['tasks'].values()):
        return None
    activated = config.get('activated_optional_tasks', [])
    if any(tid not in {t.id for t in tasks if t.optional} for tid in activated):
        raise SafetyError('Invalid optional activation list')
    return next((t for t in tasks if state['tasks'][t.id]['status'] == 'NOT_STARTED'
                 and (not t.optional or t.id in activated)
                 and all(state['tasks'][d]['status'] == 'PASS' for d in t.dependencies)), None)


class RepositoryLock:
    def __init__(self, root):
        self.path = root / '.orchestrator/lock'
        self.stream = None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(self.path.parent, 0o700)
        if self.path.is_symlink():
            raise SafetyError('Refusing a symlinked lock file')
        self.stream = self.path.open('a+')
        try:
            fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.stream.seek(0)
            info = self.stream.read(4096)
            self.stream.close()
            raise SafetyError(f'Another orchestrator owns the kernel lock: {info}')
        self.stream.seek(0)
        self.stream.truncate()
        self.stream.write(json.dumps({'pid': os.getpid(), 'started': now(), 'repository': str(self.path.parent.parent)}))
        self.stream.flush()
        os.fsync(self.stream.fileno())
        return self
    def __exit__(self, *args):
        fcntl.flock(self.stream, fcntl.LOCK_UN)
        self.stream.close()
        # Never unlink: waiters must refer to the same inode.


def git(root, *args, env=None):
    result = subprocess.run(['git', *args], cwd=root, env=env, capture_output=True, check=False)
    if result.returncode:
        raise SafetyError(f'git {args[0]} failed: {redact(result.stderr.decode(errors="replace"))}')
    return result.stdout


def head(root):
    return git(root, 'rev-parse', 'HEAD').decode().strip()


def fingerprint(root):
    # Include all tracked and nonignored untracked files; never follow symlinks.
    paths = set(git(root, 'ls-files', '-z').decode().split('\0'))
    paths.update(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
    result = {}
    for name in sorted(paths - {''}):
        if name.startswith('.orchestrator/') and name != '.orchestrator/config.json':
            continue
        p = root / name
        if not p.is_symlink() and not p.resolve().is_relative_to(root.resolve()):
            raise SafetyError('Repository path escapes working root: ' + name)
        if p.is_symlink():
            result[name] = {'hash': digest(os.readlink(p).encode()), 'mode': 'symlink'}
        elif p.is_file():
            result[name] = {'hash': digest(p.read_bytes()), 'mode': p.stat().st_mode & 0o777}
        else:
            result[name] = None
    return result


def differences(before, after):
    return sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))


def dirty_paths(root):
    # NUL-safe names, including rename/copy sources. Avoid parsing quoted status lines.
    tracked = set(git(root, 'diff', '--name-only', '-z', 'HEAD').decode().split('\0'))
    untracked = set(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
    return sorted((tracked | untracked) - {''})


def baseline(root):
    return {'head': head(root), 'files': fingerprint(root), 'dirty': dirty_paths(root),
            'index': digest(git(root, 'ls-files', '--stage', '-z')),
            'status': git(root, 'status', '--porcelain=v1', '-z').decode()}


def protected_path(path):
    return (path in {'TASKS.md', 'AGENTS.md', 'CLAUDE.md', 'GLOSSARY.md', 'orchestrator.py'}
            or path in {'docs/README.md', 'docs/ALPHA_PRODUCT_SPEC.md', 'docs/ARCHITECTURE.md',
                            'docs/ARTIFACT_MODEL.md', 'docs/JOB_EXECUTION_MODEL.md', 'docs/COST_MODEL.md',
                            'docs/UX_FLOWS.md', 'docs/DESIGN.md', 'docs/VALIDATION_PLAN.md',
                            'docs/PRODUCT_DECISIONS.md', 'docs/FEATURE_ROADMAP.md',
                            'docs/ARCHITECTURE_SPIKES.md', 'docs/ARCHITECTURE_DISCOVERY.md',
                            'docs/PIPELINE_INVESTIGATION.md', 'docs/ORCHESTRATOR.md'}
            or path.startswith(('docs/architecture/', 'docs/adr/', 'spikes/', 'demo-video-example/', 'design-', '.agents/', '.opencode/', '.orchestrator/',
                                'tools/orchestrator', 'templates/orchestrator/', 'static/orchestrator/', 'tests/orchestrator/')))


def checkpoint_safe_path(path, root):
    parts = Path(path).parts
    if not parts or Path(path).is_absolute() or '..' in parts or (root / path).is_symlink() or not (root / path).resolve().is_relative_to(root.resolve()):
        return False
    if protected_path(path) or any(p.startswith('.env') or p in {'.git', '__pycache__', 'node_modules', '.venv', 'media', 'exports', 'generated'} for p in parts):
        return False
    if Path(path).suffix.lower() in {'.mp4', '.wav', '.mp3', '.png', '.jpg', '.jpeg', '.webp', '.sqlite3', '.db', '.pem', '.key', '.p12'}:
        return False
    if (root / path).is_file():
        data = (root / path).read_bytes()
        if b'\x00' in data or len(data) > 2_000_000:
            return False
        if re.search(rb'(?:-----BEGIN [^-]*PRIVATE KEY|\bsk-[A-Za-z0-9_-]{16,}|\bAIza[A-Za-z0-9_-]{20,}|\bghp_[A-Za-z0-9_]{20,})', data):
            return False
        if re.search(rb'(?i)(?:api_key|password|secret|access_token)\s*=\s*[\"\'][A-Za-z0-9_/-]{16,}[\"\']', data):
            return False
    return True


def source_sections(root, task):
    sections = []
    for path, heading in re.findall(r'\[[^\]]+\]\(([^)]+)\), section \*\*([^*]+)\*\*', task.fields['Source of Truth']):
        file = (root / path).resolve()
        if not file.is_relative_to(root.resolve()) or not file.is_file():
            raise SafetyError(f'Invalid source reference {path}')
        text = file.read_text()
        match = re.search(r'^(#{1,6}) ' + re.escape(heading) + r'\s*$', text, re.M)
        if not match:
            raise SafetyError(f'Missing source heading {path}: {heading}')
        following = re.search(r'^#{1,' + str(len(match[1])) + r'} ', text[match.end():], re.M)
        end = match.end() + following.start() if following else len(text)
        sections.append(f'\nSOURCE: {path}\n{text[match.start():end].strip()}')
    return '\n'.join(sections)


RULES = '''IMPLEMENT ONLY THIS TASK. Do not start another task or edit TASKS.md/statuses.
Do not mark yourself PASS, commit, stage, push, rewrite history, broaden scope, or modify frozen documents.
Do not resolve owner decisions by guessing. Return TASK_BLOCKED or SPEC_BLOCKED when necessary.
ZERO product provider/API calls, zero paid spend, no deployment, accounts or purchases.
No reading unrelated user files/secrets, global machine changes or destructive cleanup.
Use offline fakes/tests. Agent-service communication is separate from product-provider authority.
Only the orchestrator may checkpoint after independent review. Preserve all pre-existing changes.
'''


def codex_prompt(root, task, global_rules, base, findings=''):
    return (f'{RULES}\nACTIVE TASK: {task.id}: {task.title}\n'
            f'GLOBAL EXECUTION CONTRACT:\n{global_rules}\nEXACT TASK CONTRACT:\n{task.contract}\n'
            f'{source_sections(root, task)}\nGIT BASELINE (do not alter):\n{json.dumps(base, indent=2)}\n'
            f'PREVIOUS REVIEW FINDINGS (repair this SAME task only):\n{findings or "None"}\n'
            'Final output must be:\nIMPLEMENTATION_COMPLETE\nCHANGED_FILES:\n- path\nTESTS_RUN:\n- command\n'
            'RESULTS:\n- result\nBLOCKERS:\nNONE\n'
            'Or: TASK_BLOCKED\nMissing decision/evidence: ...\nWhy required now: ...\n'
            'Frozen documents/sections checked: ...\nSmallest owner decision/evidence needed: ...\n')


def reviewer_prompt(root, task, global_rules, base, diff, report):
    return (f'You are an INDEPENDENT REVIEWER. Do not trust Codex claims. Read/test only; DO NOT implement fixes.\n{RULES}\n'
            'Inspect actual repository/diff, independently run or verify required tests, check EVERY acceptance criterion '
            'and caused regressions. Inspect financial/security negative paths and races. For UI inspect required visual evidence; '
            'functional tests alone are insufficient. Missing manual/owner evidence is a blocker.\n'
            f'{global_rules}\nEXACT TASK CONTRACT:\n{task.contract}\n{source_sections(root, task)}\n'
            f'GIT BASELINE:\n{json.dumps(base, indent=2)}\nACTUAL DIFF/WORKTREE:\n{diff}\n'
            f'UNTRUSTED CODEX REPORT:\n{report}\n'
            'End with exactly one final verdict block (no trailing explanation):\nVERDICT: PASS\n'
            'or:\nVERDICT: FAIL\nREASONS:\n- concrete blocking finding\nREQUIRED_FIXES:\n'
            '- exact within-task correction\nBLOCKER: optional missing owner decision/evidence (or NONE)\n')


def parse_implementation(text):
    if re.search(r'^(TASK_BLOCKED|SPEC_BLOCKED)\b', text, re.M):
        raise SafetyError('TASK_BLOCKED: ' + redact(text[-12000:]))
    match = re.search(r'^IMPLEMENTATION_COMPLETE\s*\nCHANGED_FILES:\s*\n([\s\S]*?)\nTESTS_RUN:\s*\n[\s\S]+?\nRESULTS:\s*\n[\s\S]+?\nBLOCKERS:\s*\nNONE\s*$', text)
    if not match or len(re.findall(r'^IMPLEMENTATION_COMPLETE\s*$', text, re.M)) != 1:
        raise SafetyError('HUMAN_REVIEW_REQUIRED: malformed Codex completion report')
    paths = []
    for line in match[1].splitlines():
        line = line.strip()
        if line in {'NONE', '- NONE'}:
            continue
        if not line.startswith('- '):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: CHANGED_FILES must contain exact - path entries')
        paths.append(line[2:].strip().strip('`'))
    return paths


def parse_verdict(text):
    if re.search(r'^(TASK_BLOCKED|SPEC_BLOCKED)\b', text, re.M):
        raise SafetyError('TASK_BLOCKED: ' + redact(text[-12000:]))
    matches = list(re.finditer(r'^VERDICT:', text, re.M))
    if len(matches) != 1:
        raise SafetyError('HUMAN_REVIEW_REQUIRED: missing/ambiguous review verdict')
    block = text[matches[0].start():].strip()
    if block == 'VERDICT: PASS':
        return 'PASS', None
    match = re.fullmatch(r'VERDICT: FAIL\nREASONS:\n(- [^\n]+(?:\n- [^\n]+)*)\nREQUIRED_FIXES:\n(- [^\n]+(?:\n- [^\n]+)*)(?:\nBLOCKER: ([^\n]+))?', block)
    if not match:
        raise SafetyError('HUMAN_REVIEW_REQUIRED: malformed final verdict block')
    return 'FAIL', {'reasons': match[1], 'required_fixes': match[2], 'blocker': match[3]}


def verify_capabilities():
    # Help only; never invokes an agent/session/model.
    for command, flags in [(['codex', '--help'], ['--ask-for-approval', 'never']),
                           (['codex', 'exec', '--help'], ['--sandbox', '--ignore-user-config', '--ephemeral', '--output-last-message']),
                           (['opencode', '--help'], ['--auto']),
                           (['opencode', 'run', '--help'], ['--auto', '--standalone', '--format', '--file'])]:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        help_text = result.stdout + result.stderr
        if result.returncode or any(f not in help_text for f in flags):
            raise SafetyError(f'Installed CLI capability mismatch: {command}')


def agent_environment():
    # Keep CLI auth via HOME, but do not inherit product keys or arbitrary environment.
    allowed = {'PATH', 'HOME', 'USER', 'LOGNAME', 'TMPDIR', 'LANG', 'LC_ALL', 'TERM', 'SSL_CERT_FILE', 'SSL_CERT_DIR'}
    env = {k: v for k, v in os.environ.items() if k in allowed}
    env.update({'CI': '1', 'GIT_TERMINAL_PROMPT': '0', 'PYTHONUNBUFFERED': '1'})
    return env


def process_identity(pid):
    result = subprocess.run(['ps', '-p', str(pid), '-o', 'lstart=', '-o', 'pgid=', '-o', 'args='], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def request_control(root, action):
    # A separate mailbox prevents racing state writers. Stop never kills a saved PID.
    directory = root / '.orchestrator'
    if not directory.exists():
        raise SafetyError('No initialized orchestrator to control')
    atomic_json(directory / 'control.json', {'action': action, 'requested': now(), 'nonce': uuid.uuid4().hex})


class ProcessRunner:
    def run(self, engine, actor, prompt, directory):
        output_path = directory / f'{actor}-output.txt'
        stderr_path = directory / f'{actor}-stderr.txt'
        final_path = directory / 'codex-final.txt'
        command = CODEX_BASE + ['-C', str(engine.root), '-o', str(final_path), '-'] if actor == 'codex' else REVIEW_BASE + ['--file', str(directory / 'reviewer-prompt.txt'), 'Review the attached task contract independently.']
        started = time.monotonic()
        with output_path.open('w') as out, stderr_path.open('w') as err:
            process = subprocess.Popen(command, cwd=engine.root, env=agent_environment(), stdin=subprocess.PIPE if actor == 'codex' else subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            engine.child = process
            engine.state['process'] = {'pid': process.pid, 'pgid': process.pid, 'identity': process_identity(process.pid),
                                       'started': now(), 'actor': actor, 'command': command}
            process_info = dict(engine.state['process'])
            engine.save()
            engine.event('CODEX_STARTED' if actor == 'codex' else 'REVIEW_STARTED', actor, f'{actor} process {process.pid}')
            if actor == 'codex':
                # A writer thread avoids deadlock on a prompt larger than the pipe buffer.
                import threading
                def write_prompt():
                    try:
                        process.stdin.write(prompt.encode())
                        process.stdin.close()
                    except (BrokenPipeError, OSError):
                        pass
                threading.Thread(target=write_prompt, daemon=True).start()
            selector = selectors.DefaultSelector()
            for pipe, stream in [(process.stdout, out), (process.stderr, err)]:
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, stream)
            stopped = False
            termination_reason = None
            terminate_at = None
            try:
                while selector.get_map() or process.poll() is None:
                    control = engine.control()
                    if engine.interrupted or control == 'stop' or time.monotonic() - started > engine.config['agent_timeout_seconds']:
                        stopped = True
                        termination_reason = termination_reason or ('timeout' if time.monotonic() - started > engine.config['agent_timeout_seconds'] else 'stop')
                        if terminate_at is None:
                            terminate_at = time.monotonic()
                            # Only our live Popen child/session, never a stale PID.
                            if process.poll() is None:
                                os.killpg(process.pid, signal.SIGTERM)
                        elif time.monotonic() - terminate_at > 3:
                            with contextlib.suppress(ProcessLookupError):
                                os.killpg(process.pid, signal.SIGKILL)
                    for key, _ in selector.select(timeout=0.2):
                        data = os.read(key.fileobj.fileno(), 8192)
                        if not data:
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                            continue
                        value = redact(data.decode(errors='replace'))
                        key.data.write(value)
                        key.data.flush()
                        # Events contain counts only; output remains in private attempt logs.
                        engine.event('CODEX_OUTPUT' if actor == 'codex' else 'REVIEW_OUTPUT', actor, f'{len(data)} output bytes')
                code = process.wait()
            finally:
                selector.close()
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGTERM)
                engine.child = None
                engine.state['process'] = None
            result = {'exit_code': code, 'duration': time.monotonic() - started, 'stopped': stopped, 'termination_reason': termination_reason, 'process': process_info,
                      'output': redact(final_path.read_text()) if actor == 'codex' and final_path.exists() else output_path.read_text()}
            if final_path.exists():
                final_path.write_text(redact(final_path.read_text()))
            engine.save()
            return result


class Engine:
    def __init__(self, root, runner=None):
        self.root = Path(root).resolve()
        for name in ['.orchestrator', '.orchestrator/config.json', '.orchestrator/state.json', '.orchestrator/runs', '.orchestrator/control.json', '.orchestrator/events.jsonl']:
            if (self.root / name).is_symlink():
                raise SafetyError('Refusing symlinked orchestration runtime: ' + name)
        self.tasks, self.global_rules = parse_tasks(self.root / 'TASKS.md')
        self.config = dict(DEFAULT_CONFIG)
        path = self.root / '.orchestrator/config.json'
        if path.exists():
            self.config.update(json.loads(path.read_text()))
        if not isinstance(self.config['max_repair_attempts'], int) or not 0 <= self.config['max_repair_attempts'] <= 100:
            raise SafetyError('Invalid repair limit')
        if not isinstance(self.config['agent_timeout_seconds'], (int, float)) or not math.isfinite(self.config['agent_timeout_seconds']) or self.config['agent_timeout_seconds'] <= 0:
            raise SafetyError('Invalid timeout')
        if not isinstance(self.config['auto_continue_after_pass'], bool) or not isinstance(self.config['activated_optional_tasks'], list):
            raise SafetyError('Invalid continuation/optional activation configuration')
        self.state = load_state(self.root, self.tasks)
        self.runner = runner or ProcessRunner()
        self.child = None
        self.interrupted = False

    def save(self):
        validate_state(self.state, self.tasks)
        atomic_json(self.root / '.orchestrator/state.json', self.state)

    def event(self, kind, actor='orchestrator', message=''):
        task_id = self.state.get('active_task_id')
        record = self.state['tasks'].get(task_id, {})
        value = {'timestamp': now(), 'run_id': self.state['run_id'], 'task_id': task_id,
                 'attempt': record.get('current_attempt', 0), 'actor': actor, 'event_type': kind,
                 'status': record.get('status', self.state['mode']), 'message': redact(message).splitlines()[0][:400] if message else ''}
        path = self.root / '.orchestrator/events.jsonl'
        with path.open('a') as stream:
            stream.write(json.dumps(value) + '\n')
            stream.flush()
            os.fsync(stream.fileno())

    def control(self):
        path = self.root / '.orchestrator/control.json'
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text()).get('action')
        except (OSError, ValueError):
            return 'stop'  # fail closed on a corrupt mailbox

    def block(self, reason):
        task_id = self.state.get('active_task_id')
        if task_id:
            record = self.state['tasks'][task_id]
            record.update(status='BLOCKED', blocker_reason=redact(reason), last_transition_timestamp=now())
        self.state['mode'] = 'BLOCKED'
        self.state['blocker_reason'] = redact(reason)
        self.save()
        self.event('TASK_BLOCKED' if reason.startswith('TASK_BLOCKED') else 'HUMAN_REVIEW_REQUIRED', message=reason)

    def transition(self, task_id, status):
        self.state['tasks'][task_id].update(status=status, last_transition_timestamp=now())
        self.save()

    def check_baseline(self, record):
        base = record['baseline']
        if head(self.root) != base['head'] or digest(git(self.root, 'ls-files', '--stage', '-z')) != base['index']:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: Git HEAD/index changed outside checkpoint authority')
        after = fingerprint(self.root)
        changed = differences(base['files'], after)
        if set(changed) & set(base['dirty']):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: changes overlap pre-existing dirty files')
        if any(protected_path(p) for p in changed):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: agent changed protected instructions/frozen/tooling files')
        return changed, after

    def attempt_dir(self, task_id):
        record = self.state['tasks'][task_id]
        return self.root / '.orchestrator/runs' / task_id / self.state['run_id'] / f'attempt-{record["current_attempt"]:02d}'

    def checkpoint(self, task):
        record = self.state['tasks'][task.id]
        changed, files = self.check_baseline(record)
        reported = record['reported_files']
        if files != record.get('review_fingerprint'):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: bytes changed after independent review')
        if set(changed) != set(reported) or not changed:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: actual changed files disagree with report, or empty checkpoint')
        if any(not checkpoint_safe_path(p, self.root) for p in changed):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: unsafe/secret/media/protected checkpoint path')
        # Private index keeps the user index untouched and stages only accepted paths.
        directory = self.attempt_dir(task.id)
        index = directory / 'checkpoint-index'
        with contextlib.suppress(FileNotFoundError):
            index.unlink()
        env = dict(os.environ, GIT_INDEX_FILE=str(index))
        git(self.root, 'read-tree', record['git_head_before'], env=env)
        git(self.root, 'add', '--', *changed, env=env)
        tree = git(self.root, 'write-tree', env=env).decode().strip()
        subject = f'{task.id}: {task.title[0].lower() + task.title[1:]}'
        message = subject + '\n\nOrchestrator-Checkpoint: ' + record['checkpoint_token'] + '\n'
        record['checkpoint_intent'] = {'tree': tree, 'parent': record['git_head_before'], 'paths': changed,
                                       'fingerprint': files, 'message': message}
        self.save()  # durable intent BEFORE commit
        if fingerprint(self.root) != files or head(self.root) != record['git_head_before']:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: repository changed while preparing checkpoint')
        # commit-tree never runs agent-installed hooks and cannot stage unrelated paths.
        sha = git(self.root, 'commit-tree', tree, '-p', record['git_head_before'], '-m', message).decode().strip()
        record['checkpoint_intent']['commit'] = sha
        self.save()  # if interrupted before update-ref, resume can finish this exact object
        git(self.root, 'update-ref', 'HEAD', sha, record['git_head_before'])
        self.finalize_checkpoint(task, sha)

    def finalize_checkpoint(self, task, sha):
        record = self.state['tasks'][task.id]
        intent = record['checkpoint_intent']
        # Index reconciliation only touches accepted paths whose index is still the original.
        for path in intent['paths']:
            from_parent = git(self.root, 'diff', '--cached', '--name-only', intent['parent'], '--', path).strip()
            from_commit = git(self.root, 'diff', '--cached', '--name-only', sha, '--', path).strip()
            if from_parent and from_commit:
                raise SafetyError('HUMAN_REVIEW_REQUIRED: concurrent staged edit overlaps checkpoint')
        git(self.root, 'reset', '-q', sha, '--', *intent['paths'])
        record.update(status='PASS', git_head_after=sha, last_transition_timestamp=now(), checkpoint_complete=True)
        self.state.update(latest_commit=sha, active_task_id=None)
        self.save()
        self.event('GIT_CHECKPOINT_CREATED', message=f'{task.id} {sha}')
        self.event('TASK_PASS', message=task.id)

    def reconcile_checkpoint(self, task):
        record = self.state['tasks'][task.id]
        intent = record.get('checkpoint_intent')
        if not intent:
            self.checkpoint(task)
            return
        current = head(self.root)
        sha = intent.get('commit')
        if current == intent['parent']:
            if not sha:
                # No ref changed: re-create the checkpoint only from verified reviewed bytes.
                self.checkpoint(task)
                return
            if fingerprint(self.root) != intent['fingerprint']:
                raise SafetyError('HUMAN_REVIEW_REQUIRED: files changed during interrupted checkpoint')
            git(self.root, 'update-ref', 'HEAD', sha, intent['parent'])
        elif current != sha:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: unexpected HEAD during checkpoint reconciliation')
        if fingerprint(self.root) != intent['fingerprint']:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: reviewed bytes changed after commit')
        if git(self.root, 'show', '-s', '--format=%T', sha).decode().strip() != intent['tree']:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: checkpoint tree mismatch')
        self.finalize_checkpoint(task, sha)

    def diff_for_review(self, changed):
        chunks = [git(self.root, 'status', '--short').decode(), git(self.root, 'diff', '--no-ext-diff', 'HEAD', '--', *changed).decode(errors='replace') if changed else '']
        tracked = set(git(self.root, 'ls-files', '-z').decode().split('\0'))
        for path in changed:
            if path not in tracked and (self.root / path).is_file():
                if not checkpoint_safe_path(path, self.root):
                    raise SafetyError('HUMAN_REVIEW_REQUIRED: unsafe new file in review')
                chunks.append(f'NEW FILE {path}\n{(self.root / path).read_text()}')
        return '\n'.join(chunks)

    def review(self, task):
        record = self.state['tasks'][task.id]
        directory = self.attempt_dir(task.id)
        changed, before = self.check_baseline(record)
        if set(changed) != set(record['reported_files']):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: Codex file report differs from actual changes')
        prompt = reviewer_prompt(self.root, task, self.global_rules, record['baseline'], self.diff_for_review(changed), record['codex_report'])
        (directory / 'reviewer-prompt.txt').write_text(prompt)
        record['review_fingerprint'] = before
        self.transition(task.id, 'REVIEW')
        result = self.runner.run(self, 'reviewer', prompt, directory)
        record['last_opencode_exit_code'] = result['exit_code']
        atomic_json(directory / 'reviewer-result.json', result)
        self.save()
        self.event('REVIEW_COMPLETED', 'reviewer', f'exit={result["exit_code"]}')
        self.finish_review(task, result)

    def finish_review(self, task, result):
        record = self.state['tasks'][task.id]
        changed = differences(record['review_fingerprint'], fingerprint(self.root))
        if changed:
            # No rollback: authorship under concurrent editor activity cannot be proven.
            raise SafetyError('HUMAN_REVIEW_REQUIRED: reviewer/concurrent editor changed repository: ' + ', '.join(changed))
        self.check_baseline(record)
        if result.get('termination_reason') == 'timeout':
            raise SafetyError('HUMAN_REVIEW_REQUIRED: reviewer timeout')
        if result.get('stopped'):
            self.state['mode'] = 'PAUSED'
            self.save()
            return
        if result['exit_code'] != 0:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: reviewer process failure')
        verdict, findings = parse_verdict(result['output'])
        record['reviewer_verdict'] = verdict
        record['findings'] = findings
        self.event('REVIEW_PASS' if verdict == 'PASS' else 'REVIEW_FAIL', 'reviewer', verdict)
        if verdict == 'PASS':
            record['checkpoint_token'] = record.get('checkpoint_token') or uuid.uuid4().hex
            # PASS only follows independent verdict; active ID retained until checkpoint reconciles.
            self.transition(task.id, 'PASS')
            self.checkpoint(task)
        else:
            self.transition(task.id, 'FAIL')
            blocker = findings.get('blocker')
            if blocker and blocker.upper() != 'NONE':
                raise SafetyError('TASK_BLOCKED: ' + blocker)
            if record['repair_count'] >= self.config['max_repair_attempts']:
                raise SafetyError('HUMAN_REVIEW_REQUIRED: automatic repair limit exhausted')

    def implement(self, task):
        record = self.state['tasks'][task.id]
        changed, current_files = self.check_baseline(record)
        if (record['current_attempt'] == 0 and changed) or (record.get('review_fingerprint') and current_files != record['review_fingerprint']):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: repository changed before agent launch')
        if record['status'] == 'FAIL':
            record['repair_count'] += 1
            self.event('REPAIR_STARTED', message=task.id)
        record['current_attempt'] += 1
        directory = self.attempt_dir(task.id)
        directory.mkdir(parents=True, exist_ok=False)
        prompt = codex_prompt(self.root, task, self.global_rules, record['baseline'], json.dumps(record.get('findings')) if record.get('findings') else '')
        (directory / 'codex-prompt.txt').write_text(prompt)
        self.transition(task.id, 'IN_PROGRESS')
        result = self.runner.run(self, 'codex', prompt, directory)
        record['last_codex_exit_code'] = result['exit_code']
        atomic_json(directory / 'codex-result.json', result)
        atomic_json(directory / 'metadata.json', {'task_id': task.id, 'attempt': record['current_attempt'], 'run_id': self.state['run_id'], 'codex': result})
        self.save()
        self.event('CODEX_COMPLETED', 'codex', f'exit={result["exit_code"]}')
        self.check_baseline(record)
        if result.get('stopped'):
            raise SafetyError('HUMAN_REVIEW_REQUIRED: implementation interrupted; inspect partial work before resuming')
        if result['exit_code'] != 0:
            raise SafetyError('HUMAN_REVIEW_REQUIRED: Codex process failure')
        record['reported_files'] = parse_implementation(result['output'])
        record['codex_report'] = result['output']
        self.transition(task.id, 'REVIEW')  # durable completion before possible pause
        if self.control() in {'pause', 'stop'}:
            self.state['mode'] = 'PAUSED'
            self.save()
            return
        self.review(task)

    def recover(self):
        if self.state.get('process'):
            process = self.state['process']
            groups = subprocess.run(['ps', '-axo', 'pgid='], capture_output=True, text=True)
            group_present = str(process.get('pgid')) in groups.stdout.split()
            if group_present or (process_identity(process['pid']) == process.get('identity') and process.get('identity')):
                raise SafetyError('HUMAN_REVIEW_REQUIRED: prior agent may still be alive; do not relaunch or kill stale PID')
            self.state['process'] = None
            self.save()
        task_id = self.state.get('active_task_id')
        if not task_id:
            return
        task = next(t for t in self.tasks if t.id == task_id)
        record = self.state['tasks'][task_id]
        if record['status'] == 'PASS':
            self.reconcile_checkpoint(task)
        elif record['status'] == 'IN_PROGRESS':
            path = self.attempt_dir(task_id) / 'codex-result.json'
            if not path.exists():
                raise SafetyError('HUMAN_REVIEW_REQUIRED: interrupted implementation has no durable completion receipt')
            result = json.loads(path.read_text())
            if result['exit_code'] or result.get('stopped'):
                raise SafetyError('HUMAN_REVIEW_REQUIRED: incomplete interrupted implementation')
            self.check_baseline(record)
            record['reported_files'] = parse_implementation(result['output'])
            record['codex_report'] = result['output']
            self.transition(task_id, 'REVIEW')
        elif record['status'] == 'REVIEW':
            path = self.attempt_dir(task_id) / 'reviewer-result.json'
            if path.exists() and not json.loads(path.read_text()).get('stopped'):
                self.finish_review(task, json.loads(path.read_text()))
            else:
                if record.get('review_fingerprint') and record['review_fingerprint'] != fingerprint(self.root):
                    raise SafetyError('HUMAN_REVIEW_REQUIRED: changes during interrupted review')
                self.check_baseline(record)
                # Start a fresh independent review of unchanged bytes, never reimplement.
                self.review(task)

    def run(self, resume=False, verify=True):
        with RepositoryLock(self.root):
            self.state = load_state(self.root, self.tasks)  # reload AFTER lock acquisition
            if self.state['mode'] == 'BLOCKED':
                raise SafetyError('HUMAN_REVIEW_REQUIRED: persisted blocker requires explicit operator reconciliation; resume does not clear it')
            if self.state.get('active_task_id') and not resume:
                raise SafetyError('Use resume for an interrupted active task')
            if verify:
                verify_capabilities()
            # An old pause/stop mailbox is explicitly consumed only on operator run/resume.
            with contextlib.suppress(FileNotFoundError):
                (self.root / '.orchestrator/control.json').unlink()
            if not self.state['run_id']:
                self.state['run_id'] = uuid.uuid4().hex
            self.state['mode'] = 'RUNNING'
            self.save()
            self.event('ORCHESTRATOR_STARTED')
            old_handlers = {}
            def interrupt(*_):
                self.interrupted = True
            if __import__('threading').current_thread() is __import__('threading').main_thread():
                for sig in (signal.SIGINT, signal.SIGTERM):
                    old_handlers[sig] = signal.signal(sig, interrupt)
            try:
                if resume:
                    self.recover()
                while True:
                    if self.interrupted or self.control() in {'pause', 'stop'} or self.state['mode'] == 'PAUSED':
                        self.state['mode'] = 'PAUSED'
                        self.save()
                        self.event('ORCHESTRATOR_STOPPED' if self.control() == 'stop' or self.interrupted else 'ORCHESTRATOR_PAUSED')
                        break
                    task_id = self.state.get('active_task_id')
                    if task_id:
                        task = next(t for t in self.tasks if t.id == task_id)
                        status = self.state['tasks'][task_id]['status']
                        if status == 'REVIEW':
                            self.review(task)
                        elif status in {'NOT_STARTED', 'FAIL'}:
                            self.implement(task)
                        else:
                            raise SafetyError('HUMAN_REVIEW_REQUIRED: inconsistent active lifecycle')
                    else:
                        task = next_task(self.tasks, self.state, self.config)
                        if not task:
                            self.state['mode'] = 'IDLE'
                            self.save()
                            break
                        base = baseline(self.root)
                        # Existing staged changes make any HEAD advancement ambiguous.
                        if git(self.root, 'diff', '--cached', '--name-only').strip():
                            raise SafetyError('HUMAN_REVIEW_REQUIRED: pre-existing staged changes; unstage/checkpoint separately')
                        self.state['active_task_id'] = task.id
                        self.state['last_task_id'] = task.id
                        self.state['tasks'][task.id].update(baseline=base, git_head_before=base['head'], start_timestamp=now())
                        self.save()
                        self.event('TASK_SELECTED', message=task.title)
                        self.implement(task)
                    if not self.state.get('active_task_id') and not self.config['auto_continue_after_pass']:
                        self.state['mode'] = 'IDLE'
                        self.save()
                        break
            except (SafetyError, OSError, ValueError, KeyError) as error:
                self.block(str(error))
                raise SafetyError(str(error)) from error
            finally:
                for sig, handler in old_handlers.items():
                    signal.signal(sig, handler)


def dry_run(root):
    # Intentionally NO subprocesses, lock, mkdir, state writes, probes or agent launches.
    engine = Engine(root)
    task = next_task(engine.tasks, engine.state, engine.config)
    if not task:
        return {'next_task': None, 'mode': engine.state['mode'], 'message': 'No eligible task; inspect persisted state/activation gates'}
    base = {'head': 'HEAD will be verified at run time', 'dirty': 'Exact Git/file baseline captured before implementation'}
    return {'next_task': task.id, 'title': task.title, 'task_count': len(engine.tasks),
            'codex_command': CODEX_BASE + ['-C', str(engine.root), '-o', '<attempt>/codex-final.txt', '-'],
            'opencode_command': REVIEW_BASE + ['--file', '<attempt>/reviewer-prompt.txt', 'Review the attached task contract independently.'],
            'codex_prompt': codex_prompt(engine.root, task, engine.global_rules, base),
            'reviewer_prompt_template': reviewer_prompt(engine.root, task, engine.global_rules, base, '<actual diff captured after implementation>', '<untrusted Codex report>'),
            'capabilities': 'Commands verified from installed CLI help during tooling development; run rechecks capabilities',
            'mutations': 'NONE; no agents, subprocesses, state writes or commits'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', choices=['status', 'run', 'resume', 'pause', 'stop'], default='status')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.dry_run:
            print(json.dumps(dry_run(ROOT), indent=2))
        elif args.command in {'pause', 'stop'}:
            request_control(ROOT, args.command)
            print(f'{args.command} requested; controller will handle its owned process safely')
        else:
            engine = Engine(ROOT)
            if args.command == 'status':
                task = next_task(engine.tasks, engine.state, engine.config)
                print(json.dumps({'mode': engine.state['mode'], 'active_task_id': engine.state['active_task_id'],
                                  'next_task': task.id if task else None, 'completed': sum(r['status'] == 'PASS' for r in engine.state['tasks'].values()),
                                  'total': len(engine.tasks), 'blocker': engine.state.get('blocker_reason')}, indent=2))
            else:
                engine.run(resume=args.command == 'resume')
        return 0
    except (SafetyError, OSError, ValueError) as error:
        print(redact(str(error)), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
