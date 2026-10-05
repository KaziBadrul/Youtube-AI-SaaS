import contextlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import orchestrator as o
from tools import orchestrator_dashboard as dashboard

REPORT = 'IMPLEMENTATION_COMPLETE\nCHANGED_FILES:\n- alpha.py\nTESTS_RUN:\n- offline test\nRESULTS:\n- passed\nBLOCKERS:\nNONE\n'
FAIL = 'VERDICT: FAIL\nREASONS:\n- missing negative test\nREQUIRED_FIXES:\n- add the negative test\nBLOCKER: NONE'

class Crash(BaseException):
    pass

class FakeRunner:
    def __init__(self, reviews=None, codex=None, mutation=None, control=None):
        self.reviews = list(reviews or ['VERDICT: PASS'])
        self.codex = codex or REPORT
        self.calls = []
        self.mutation = mutation
        self.control_action = control
    def run(self, engine, actor, prompt, directory):
        self.calls.append((actor, engine.state['active_task_id'], prompt))
        if actor == 'codex':
            (engine.root / 'alpha.py').write_text('value = ' + str(len(self.calls)) + '\n')
            output, code = self.codex, 0
        else:
            review = self.reviews.pop(0)
            output, code = review if isinstance(review, tuple) else (review, 0)
            if self.mutation:
                self.mutation(engine)
        (directory / f'{actor}-output.txt').write_text(output)
        (directory / f'{actor}-stderr.txt').write_text('')
        if self.control_action and actor == 'codex':
            o.request_control(engine.root, self.control_action)
        return {'exit_code': code, 'duration': .01, 'stopped': False, 'output': output}

class RepoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # Exact T001 contract, limited fixture repo with necessary source headings.
        tasks, global_rules = o.parse_tasks(o.ROOT / 'TASKS.md')
        self.root.joinpath('TASKS.md').write_text(global_rules + '\n' + tasks[0].contract + '\n')
        self.root.joinpath('docs/architecture').mkdir(parents=True)
        self.root.joinpath('docs/ARCHITECTURE.md').write_text('## Runtime shape\nLocal fixture contract.\n')
        self.root.joinpath('docs/architecture/ARCHITECTURE_FREEZE.md').write_text('## Scope and frozen boundaries\nFixture only.\n')
        self.root.joinpath('.orchestrator').mkdir()
        config = dict(o.DEFAULT_CONFIG, auto_continue_after_pass=False)
        o.atomic_json(self.root / '.orchestrator/config.json', config)
        self.root.joinpath('.gitignore').write_text('.orchestrator/*\n!.orchestrator/config.json\n')
        for cmd in [('init', '-q'), ('config', 'user.name', 'Fixture'), ('config', 'user.email', 'fixture@example.test'), ('add', 'TASKS.md', 'docs', '.gitignore', '.orchestrator/config.json'), ('commit', '-qm', 'fixture baseline')]:
            o.git(self.root, *cmd)
    def tearDown(self):
        self.tmp.cleanup()
    def engine(self, runner=None):
        return o.Engine(self.root, runner or FakeRunner())
    def run_engine(self, runner=None):
        engine = self.engine(runner)
        engine.run(verify=False)
        return engine
    def assert_blocked(self, runner, fragment):
        engine = self.engine(runner)
        with self.assertRaises(o.SafetyError) as error:
            engine.run(verify=False)
        self.assertIn(fragment, str(error.exception))
        self.assertEqual('BLOCKED', json.loads((self.root / '.orchestrator/state.json').read_text())['mode'])
        return engine

    def test_real_tasks_parse(self):
        tasks, rules = o.parse_tasks(o.ROOT / 'TASKS.md')
        self.assertEqual(94, len(tasks))
        self.assertEqual(['T001', 'T002'], tasks[2].dependencies)
        self.assertTrue(tasks[92].optional)
        self.assertIn('ZERO external provider/API calls', rules)
        self.assertEqual(set(o.FIELDS), set(tasks[0].fields))
    def test_initial_t001_selection(self):
        engine = self.engine()
        self.assertEqual('T001', o.next_task(engine.tasks, engine.state, engine.config).id)
    def test_dependency_not_selected(self):
        tasks, _ = o.parse_tasks(o.ROOT / 'TASKS.md')
        state = o.initial_state(tasks, 'hash')
        state['tasks']['T001']['status'] = 'BLOCKED'
        self.assertIsNone(o.next_task(tasks, state, o.DEFAULT_CONFIG))
    def test_order_after_dependencies(self):
        tasks, _ = o.parse_tasks(o.ROOT / 'TASKS.md')
        state = o.initial_state(tasks, 'hash')
        state['tasks']['T001']['status'] = 'PASS'
        self.assertEqual('T002', o.next_task(tasks, state, o.DEFAULT_CONFIG).id)
    def test_optional_requires_activation(self):
        tasks, _ = o.parse_tasks(o.ROOT / 'TASKS.md')
        state = o.initial_state(tasks, 'hash')
        for task in tasks:
            if not task.optional:
                state['tasks'][task.id]['status'] = 'PASS'
        self.assertIsNone(o.next_task(tasks, state, o.DEFAULT_CONFIG))
        self.assertEqual('T093', o.next_task(tasks, state, dict(o.DEFAULT_CONFIG, activated_optional_tasks=['T093'])).id)
    def test_exactly_one_active(self):
        tasks, _ = o.parse_tasks(o.ROOT / 'TASKS.md')
        state = o.initial_state(tasks, 'hash')
        state['active_task_id'] = 'T001'
        state['tasks']['T001']['status'] = 'IN_PROGRESS'
        state['tasks']['T002']['status'] = 'REVIEW'
        with self.assertRaises(o.SafetyError):
            o.validate_state(state, tasks)
    def test_cycle_detection(self):
        text = self.root.joinpath('TASKS.md').read_text().replace('Dependencies:\n- None', 'Dependencies:\n- T001')
        self.root.joinpath('TASKS.md').write_text(text)
        with self.assertRaises(o.SafetyError):
            o.parse_tasks(self.root / 'TASKS.md')
    def test_unknown_dependency(self):
        text = self.root.joinpath('TASKS.md').read_text().replace('Dependencies:\n- None', 'Dependencies:\n- T999')
        self.root.joinpath('TASKS.md').write_text(text)
        with self.assertRaises(o.SafetyError):
            o.parse_tasks(self.root / 'TASKS.md')
    def test_codex_complete(self):
        self.assertEqual(['alpha.py'], o.parse_implementation(REPORT))
    def test_codex_blocked(self):
        runner = FakeRunner(codex='TASK_BLOCKED\nMissing decision/evidence: need policy')
        self.assert_blocked(runner, 'TASK_BLOCKED')
        self.assertEqual(1, len(runner.calls))
    def test_spec_blocked(self):
        self.assert_blocked(FakeRunner(codex='SPEC_BLOCKED\nContradictory requirement'), 'TASK_BLOCKED')
    def test_pass_parser(self):
        self.assertEqual(('PASS', None), o.parse_verdict('Independent tests passed.\nVERDICT: PASS\n'))
    def test_fail_parser(self):
        verdict, findings = o.parse_verdict(FAIL)
        self.assertEqual('FAIL', verdict)
        self.assertIn('negative test', findings['required_fixes'])
    def test_malformed_verdicts(self):
        for text in ['', 'Looks good', 'Probably passes', 'PASS with caveats', 'VERDICT: PASS with caveats', 'VERDICT: PASS\nextra', 'VERDICT: PASS\nVERDICT: PASS', 'VERDICT: FAIL']:
            with self.subTest(text=text), self.assertRaises(o.SafetyError):
                o.parse_verdict(text)
    def test_reviewer_failure_not_pass(self):
        self.assert_blocked(FakeRunner(reviews=[('VERDICT: PASS', 1)]), 'process failure')
    def test_malformed_review_blocks(self):
        self.assert_blocked(FakeRunner(reviews=['Mostly correct']), 'verdict')
    def test_repair_loop_same_task(self):
        runner = FakeRunner(reviews=[FAIL, 'VERDICT: PASS'])
        engine = self.run_engine(runner)
        self.assertEqual(['codex', 'reviewer', 'codex', 'reviewer'], [c[0] for c in runner.calls])
        self.assertEqual({'T001'}, {c[1] for c in runner.calls})
        self.assertIn('missing negative test', runner.calls[2][2])
        self.assertEqual(1, engine.state['tasks']['T001']['repair_count'])
    def test_three_repair_cutoff(self):
        runner = FakeRunner(reviews=[FAIL] * 4)
        engine = self.assert_blocked(runner, 'repair limit')
        self.assertEqual(8, len(runner.calls))
        self.assertEqual(3, engine.state['tasks']['T001']['repair_count'])
        self.assertEqual(4, engine.state['tasks']['T001']['current_attempt'])
    def test_review_owner_blocker_no_repair(self):
        runner = FakeRunner(reviews=[FAIL.replace('BLOCKER: NONE', 'BLOCKER: Owner policy needed')])
        self.assert_blocked(runner, 'Owner policy')
        self.assertEqual(2, len(runner.calls))
    def test_pass_scoped_checkpoint(self):
        before = o.head(self.root)
        engine = self.run_engine()
        self.assertEqual('PASS', engine.state['tasks']['T001']['status'])
        self.assertNotEqual(before, o.head(self.root))
        self.assertEqual(['alpha.py'], o.git(self.root, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').decode().splitlines())
        self.assertFalse(o.git(self.root, 'diff', '--cached').strip())
        self.assertIn('T001: establish', o.git(self.root, 'show', '-s', '--format=%s').decode())
    def test_crash_after_commit_before_state(self):
        engine = self.engine()
        with patch.object(engine, 'finalize_checkpoint', side_effect=Crash()):
            with self.assertRaises(Crash):
                engine.run(verify=False)
        committed = o.head(self.root)
        engine2 = self.engine()
        engine2.run(resume=True, verify=False)
        self.assertEqual(committed, o.head(self.root))
        self.assertEqual('PASS', engine2.state['tasks']['T001']['status'])
        self.assertEqual(1, len(o.git(self.root, 'log', '--format=%s', '--grep=Orchestrator-Checkpoint').decode().splitlines()))
    def test_crash_before_commit_state_write(self):
        engine = self.engine()
        real_save = engine.save
        def crash():
            if engine.state['tasks']['T001'].get('checkpoint_intent'):
                raise Crash()
            real_save()
        with patch.object(engine, 'save', side_effect=crash), self.assertRaises(Crash):
            engine.run(verify=False)
        runner = FakeRunner()
        resumed = self.engine(runner)
        resumed.run(resume=True, verify=False)
        self.assertEqual([], runner.calls)
        self.assertEqual('PASS', resumed.state['tasks']['T001']['status'])
    def test_dirty_unrelated_preserved(self):
        user = self.root / 'user.txt'
        user.write_text('uncommitted owner work')
        self.run_engine()
        self.assertEqual('uncommitted owner work', user.read_text())
        self.assertNotIn('user.txt', o.git(self.root, 'ls-tree', '--name-only', 'HEAD').decode())
    def test_dirty_overlap_blocks(self):
        self.root.joinpath('alpha.py').write_text('owner work')
        self.assert_blocked(FakeRunner(), 'overlap')
        self.assertEqual(1, len(o.git(self.root, 'log', '--oneline').decode().splitlines()))
    def test_staged_user_change_blocks(self):
        self.root.joinpath('user.txt').write_text('owner work')
        o.git(self.root, 'add', 'user.txt')
        runner = FakeRunner()
        self.assert_blocked(runner, 'staged changes')
        self.assertEqual([], runner.calls)
        self.assertIn('user.txt', o.git(self.root, 'diff', '--cached', '--name-only').decode())
    def test_review_modifications_preserved_and_block(self):
        runner = FakeRunner(mutation=lambda engine: (engine.root / 'alpha.py').write_text('reviewer wrote this'))
        self.assert_blocked(runner, 'reviewer/concurrent editor changed')
        self.assertEqual('reviewer wrote this', self.root.joinpath('alpha.py').read_text())
    def test_review_untracked_change_detection(self):
        self.assert_blocked(FakeRunner(mutation=lambda e: (e.root / 'surprise.py').write_text('x')), 'changed repository')
    def test_protected_doc_changes_block(self):
        runner = FakeRunner(mutation=lambda e: (e.root / 'TASKS.md').write_text('tamper'))
        # Reviewer fingerprint rejects it before runtime history can advance.
        self.assert_blocked(runner, 'changed repository')
    def test_pause_after_codex_before_reviewer(self):
        runner = FakeRunner(control='pause')
        engine = self.run_engine(runner)
        self.assertEqual(1, len(runner.calls))
        self.assertEqual('PAUSED', engine.state['mode'])
        self.assertEqual('REVIEW', engine.state['tasks']['T001']['status'])
        resumed_runner = FakeRunner()
        resumed = self.engine(resumed_runner)
        resumed.run(resume=True, verify=False)
        self.assertEqual(['reviewer'], [c[0] for c in resumed_runner.calls])
    def test_stop_mailbox_no_pid_kill(self):
        o.request_control(self.root, 'stop')
        self.assertEqual('stop', self.engine().control())
        self.assertNotIn('pid', json.loads(self.root.joinpath('.orchestrator/control.json').read_text()))
    def test_kernel_lock_stale_file(self):
        self.root.joinpath('.orchestrator/lock').write_text('{"pid":99999999}')
        with o.RepositoryLock(self.root):
            with self.assertRaises(o.SafetyError):
                with o.RepositoryLock(self.root):
                    pass
        with o.RepositoryLock(self.root):
            pass
    def test_atomic_write_failure_preserves_previous(self):
        path = self.root / '.orchestrator/example.json'
        o.atomic_json(path, {'old': True})
        with patch('orchestrator.os.replace', side_effect=OSError('crash')), self.assertRaises(OSError):
            o.atomic_json(path, {'new': True})
        self.assertEqual({'old': True}, json.loads(path.read_text()))
        self.assertEqual([], list(path.parent.glob('.example.json.*')))
    def test_corrupt_state_not_reset(self):
        self.root.joinpath('.orchestrator/state.json').write_text('{')
        with self.assertRaises(o.SafetyError):
            self.engine()
    def test_empty_legacy_placeholder(self):
        self.root.joinpath('.orchestrator/state.json').write_text('')
        self.assertEqual('IDLE', self.engine().state['mode'])
    def test_dashboard_initial_state(self):
        value = dashboard.load_dashboard(self.root)
        self.assertEqual('IDLE', value['mode'])
        self.assertEqual(0, value['completed'])
        self.assertEqual(1, value['remaining'])
    def test_dashboard_redaction_and_allowlist(self):
        engine = self.engine()
        engine.state['secret'] = 'DO_NOT_PUBLISH'
        engine.state['blocker_reason'] = 'api_key=secretvalue'
        engine.save()
        value = json.dumps(dashboard.load_dashboard(self.root))
        self.assertNotIn('DO_NOT_PUBLISH', value)
        self.assertNotIn('secretvalue', value)
        self.assertIn('REDACTED', value)
    def test_dashboard_read_only_http(self):
        server = dashboard.ThreadingHTTPServer(('127.0.0.1', 0), dashboard.handler_for(self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = http.client.HTTPConnection('127.0.0.1', server.server_port)
            for method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                connection.request(method, '/api/run')
                response = connection.getresponse()
                self.assertEqual(405, response.status)
                response.read()
            connection.request('GET', '/api/status')
            response = connection.getresponse()
            self.assertEqual(200, response.status)
            self.assertEqual('IDLE', json.loads(response.read())['mode'])
            connection.request('GET', '/../../.env')
            response = connection.getresponse()
            self.assertEqual(404, response.status)
            response.read()
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    def test_dry_run_no_subprocess_or_writes(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch('orchestrator.subprocess.run', side_effect=AssertionError('subprocess forbidden')), patch('orchestrator.subprocess.Popen', side_effect=AssertionError('agent forbidden')):
            result = o.dry_run(self.root)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual('T001', result['next_task'])
    def test_runtime_symlink_rejected(self):
        (self.root / '.orchestrator/state.json').symlink_to(self.root / 'TASKS.md')
        with self.assertRaises(o.SafetyError):
            self.engine()

    def test_secret_checkpoint_rejected(self):
        self.root.joinpath('bad.py').write_text('key = "sk-abcdefghijklmnopqrstuvwxyz"')
        self.assertFalse(o.checkpoint_safe_path('bad.py', self.root))
        self.assertFalse(o.checkpoint_safe_path('.env', self.root))
        self.assertFalse(o.checkpoint_safe_path('asset.mp4', self.root))
    def test_blocked_resume_never_clears_blocker(self):
        self.assert_blocked(FakeRunner(codex='TASK_BLOCKED\nMissing: owner evidence'), 'TASK_BLOCKED')
        runner = FakeRunner()
        with self.assertRaises(o.SafetyError):
            self.engine(runner).run(resume=True, verify=False)
        self.assertEqual([], runner.calls)
    def test_interrupted_without_receipt_blocks(self):
        engine = self.engine()
        engine.state.update(active_task_id='T001', run_id='a' * 32)
        engine.state['tasks']['T001'].update(status='IN_PROGRESS', current_attempt=1, baseline=o.baseline(self.root))
        engine.save()
        with self.assertRaises(o.SafetyError):
            engine.run(resume=True, verify=False)
    def test_agent_environment_drops_product_credentials(self):
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'secret', 'TAVILY_API_KEY': 'secret', 'AWS_SECRET_ACCESS_KEY': 'secret'}):
            env = o.agent_environment()
        self.assertNotIn('GOOGLE_API_KEY', env)
        self.assertNotIn('TAVILY_API_KEY', env)
        self.assertEqual('1', env['CI'])


    def test_post_review_concurrent_edit_rejected(self):
        engine = self.engine()
        original = engine.checkpoint
        def concurrent(task):
            (self.root / 'alpha.py').write_text('unreviewed user edit')
            return original(task)
        with patch.object(engine, 'checkpoint', side_effect=concurrent), self.assertRaises(o.SafetyError) as error:
            engine.run(verify=False)
        self.assertIn('bytes changed after independent review', str(error.exception))
        self.assertEqual(1, len(o.git(self.root, 'log', '--oneline').decode().splitlines()))

    def test_checkpoint_recovery_preserves_concurrent_staged_edit(self):
        engine = self.engine()
        with patch.object(engine, 'finalize_checkpoint', side_effect=Crash()), self.assertRaises(Crash):
            engine.run(verify=False)
        (self.root / 'alpha.py').write_text('concurrent staged version')
        o.git(self.root, 'add', 'alpha.py')
        with self.assertRaises(o.SafetyError):
            self.engine().run(resume=True, verify=False)
        self.assertIn('concurrent staged version', o.git(self.root, 'show', ':alpha.py').decode())

    def test_reviewer_timeout_blocks(self):
        class TimeoutRunner(FakeRunner):
            def run(self, engine, actor, prompt, directory):
                result = super().run(engine, actor, prompt, directory)
                if actor == 'reviewer':
                    result.update(stopped=True, termination_reason='timeout')
                return result
        self.assert_blocked(TimeoutRunner(), 'reviewer timeout')

    def prerequisite_blocked(self):
        engine = self.engine()
        engine.state.update(active_task_id='T001', run_id='b' * 32, mode='BLOCKED',
                            blocker_reason='TASK_BLOCKED: Offline Django runtime required')
        engine.state['tasks']['T001'].update(
            status='BLOCKED', blocker_reason=engine.state['blocker_reason'],
            current_attempt=1, repair_count=2, last_codex_exit_code=0,
            baseline=o.baseline(self.root), git_head_before=o.head(self.root))
        directory = engine.attempt_dir('T001')
        directory.mkdir(parents=True)
        (directory / 'codex-output.txt').write_text('TASK_BLOCKED\nOffline prerequisite missing')
        engine.save()
        return engine

    def test_unblock_correct_task_preserves_history_no_agent(self):
        engine = self.prerequisite_blocked()
        old = json.loads(json.dumps(engine.state['tasks']['T001']))
        evidence = engine.attempt_dir('T001') / 'codex-output.txt'
        spec = (self.root / 'TASKS.md').read_bytes()
        with patch('orchestrator.verify_capabilities', side_effect=AssertionError('CLI probes forbidden')):
            engine.unblock('T001', 'Installed local Django runtime')
        state = self.engine().state
        record = state['tasks']['T001']
        self.assertEqual('PAUSED', state['mode'])
        self.assertEqual('T001', state['active_task_id'])
        self.assertEqual('NOT_STARTED', record['status'])
        self.assertIsNone(record['blocker_reason'])
        self.assertIsNone(state['blocker_reason'])
        self.assertEqual(1, record['current_attempt'])
        self.assertEqual(2, record['repair_count'])
        self.assertIsNone(record['git_head_after'])
        self.assertEqual([], engine.runner.calls)
        self.assertEqual(old, record['reconciliations'][0]['previous_record'])
        self.assertIn('TASK_BLOCKED', evidence.read_text())
        self.assertEqual(spec, (self.root / 'TASKS.md').read_bytes())
        events = [json.loads(line) for line in (self.root / '.orchestrator/events.jsonl').read_text().splitlines()]
        self.assertEqual(1, len(events))
        self.assertEqual('BLOCKER_RECONCILED', events[0]['event_type'])
        self.assertEqual('T001', events[0]['task_id'])
        self.assertEqual(old['blocker_reason'], events[0]['previous_blocker'])
        self.assertEqual('Installed local Django runtime', events[0]['operator_reason'])
        self.assertTrue(events[0]['timestamp'])

    def test_unblock_wrong_task_rejected(self):
        engine = self.prerequisite_blocked()
        before = (self.root / '.orchestrator/state.json').read_bytes()
        with self.assertRaises(o.SafetyError):
            engine.unblock('T002', 'Prerequisite provided')
        self.assertEqual(before, (self.root / '.orchestrator/state.json').read_bytes())

    def test_unblock_not_blocked_rejected(self):
        with self.assertRaises(o.SafetyError):
            self.engine().unblock('T001', 'Prerequisite provided')

    def test_unblock_controlled_subprocess_rejected(self):
        engine = self.prerequisite_blocked()
        engine.state['process'] = {'actor': 'codex', 'pid': 999999, 'pgid': 999999}
        engine.save()
        with self.assertRaises(o.SafetyError):
            engine.unblock('T001', 'Prerequisite provided')
        self.assertEqual('BLOCKED', self.engine().state['mode'])

    def test_unblock_owned_child_rejected(self):
        engine = self.prerequisite_blocked()
        engine.child = object()
        with self.assertRaises(o.SafetyError):
            engine.unblock('T001', 'Prerequisite provided')

    def test_unblock_missing_blocker_rejected(self):
        engine = self.prerequisite_blocked()
        engine.state['tasks']['T001']['blocker_reason'] = None
        engine.save()
        with self.assertRaises(o.SafetyError):
            engine.unblock('T001', 'Prerequisite provided')

    def test_unblock_reason_required(self):
        engine = self.prerequisite_blocked()
        for reason in ['', '   ', None]:
            with self.subTest(reason=reason), self.assertRaises(o.SafetyError):
                engine.unblock('T001', reason)

    def test_unblock_human_review_and_spec_blockers_rejected(self):
        for reason in ['HUMAN_REVIEW_REQUIRED: repair limit exhausted', 'TASK_BLOCKED: SPEC_BLOCKED\nMaterial contradiction']:
            engine = self.prerequisite_blocked() if not (self.root / '.orchestrator/state.json').exists() else self.engine()
            engine.state['blocker_reason'] = reason
            engine.state['tasks']['T001']['blocker_reason'] = reason
            engine.save()
            with self.subTest(reason=reason), self.assertRaises(o.SafetyError):
                engine.unblock('T001', 'Prerequisite provided')

    def test_unblock_repeated_rejected(self):
        engine = self.prerequisite_blocked()
        engine.unblock('T001', 'Prerequisite provided')
        before = (self.root / '.orchestrator/state.json').read_bytes()
        with self.assertRaises(o.SafetyError):
            self.engine().unblock('T001', 'Prerequisite provided')
        self.assertEqual(before, (self.root / '.orchestrator/state.json').read_bytes())

    def test_unblock_lock_owner_rejected(self):
        engine = self.prerequisite_blocked()
        with o.RepositoryLock(self.root), self.assertRaises(o.SafetyError):
            engine.unblock('T001', 'Prerequisite provided')

    def test_unblock_staged_change_rejected(self):
        engine = self.prerequisite_blocked()
        (self.root / 'owner.txt').write_text('owner work')
        o.git(self.root, 'add', 'owner.txt')
        with self.assertRaises(o.SafetyError):
            engine.unblock('T001', 'Prerequisite provided')
        self.assertIn('owner.txt', o.git(self.root, 'diff', '--cached', '--name-only').decode())

    def test_unblock_then_resume_retries_same_task_from_beginning(self):
        engine = self.prerequisite_blocked()
        # Owner may checkpoint an operational prerequisite while the task is blocked.
        (self.root / '.gitignore').write_text((self.root / '.gitignore').read_text() + '.venv/\n')
        o.git(self.root, 'add', '.gitignore')
        o.git(self.root, 'commit', '-qm', 'owner prerequisite')
        engine.unblock('T001', 'Repository-local prerequisite supplied')
        runner = FakeRunner()
        resumed = self.engine(runner)
        resumed.run(resume=True, verify=False)
        self.assertEqual(['codex', 'reviewer'], [c[0] for c in runner.calls])
        self.assertEqual({'T001'}, {c[1] for c in runner.calls})
        self.assertEqual(2, resumed.state['tasks']['T001']['current_attempt'])
        self.assertEqual(2, resumed.state['tasks']['T001']['repair_count'])
        self.assertEqual('PASS', resumed.state['tasks']['T001']['status'])
        self.assertTrue((self.root / '.orchestrator/runs/T001' / resumed.state['run_id'] / 'attempt-01/codex-output.txt').exists())

    def test_unblock_partial_implementation_preserved_and_reviewed(self):
        engine = self.prerequisite_blocked()
        (self.root / 'alpha.py').write_text('partial work from blocked attempt')
        engine.unblock('T001', 'Prerequisite provided')
        record = engine.state['tasks']['T001']
        self.assertIn('alpha.py', record['baseline']['dirty'])
        self.assertEqual('partial work from blocked attempt', (self.root / 'alpha.py').read_text())
        # A retry cannot accidentally absorb old partial work as newly attributable edits.
        runner = FakeRunner()
        with self.assertRaises(o.SafetyError):
            self.engine(runner).run(resume=True, verify=False)
        self.assertEqual(['codex'], [c[0] for c in runner.calls])

    def test_unblock_crash_before_intent_write_retains_blocker(self):
        engine = self.prerequisite_blocked()
        before = (self.root / '.orchestrator/state.json').read_bytes()
        with patch('orchestrator.os.replace', side_effect=OSError('interrupted')), self.assertRaises(OSError):
            engine.unblock('T001', 'Prerequisite provided')
        self.assertEqual(before, (self.root / '.orchestrator/state.json').read_bytes())
        self.engine().unblock('T001', 'Prerequisite provided')
        self.assertEqual('NOT_STARTED', self.engine().state['tasks']['T001']['status'])

    def test_unblock_crash_after_audit_before_final_write_recovers(self):
        engine = self.prerequisite_blocked()
        save = engine.save
        def crash_final():
            if engine.state['mode'] == 'PAUSED':
                raise Crash()
            save()
        with patch.object(engine, 'save', side_effect=crash_final), self.assertRaises(Crash):
            engine.unblock('T001', 'Prerequisite provided')
        blocked = self.engine()
        self.assertEqual('BLOCKED', blocked.state['mode'])
        with self.assertRaises(o.SafetyError):
            blocked.run(resume=True, verify=False)
        blocked.unblock('T001', 'Prerequisite provided')
        self.assertEqual('NOT_STARTED', self.engine().state['tasks']['T001']['status'])
        events = (self.root / '.orchestrator/events.jsonl').read_text()
        self.assertEqual(1, events.count('BLOCKER_RECONCILED'))
        self.assertEqual(1, len(self.engine().state['tasks']['T001']['reconciliations']))

    def test_unblock_crash_before_audit_recovers(self):
        engine = self.prerequisite_blocked()
        with patch.object(engine, 'event', side_effect=Crash()), self.assertRaises(Crash):
            engine.unblock('T001', 'Prerequisite provided')
        self.assertEqual('BLOCKED', self.engine().state['mode'])
        self.engine().unblock('T001', 'Prerequisite provided')
        self.assertEqual('PAUSED', self.engine().state['mode'])

    def test_unblock_crash_truncated_event_append_recovers(self):
        engine = self.prerequisite_blocked()
        def partial_event(*args, **kwargs):
            (self.root / '.orchestrator/events.jsonl').write_text('{"event_type":')
            raise Crash()
        with patch.object(engine, 'event', side_effect=partial_event), self.assertRaises(Crash):
            engine.unblock('T001', 'Prerequisite provided')
        self.engine().unblock('T001', 'Prerequisite provided')
        lines = (self.root / '.orchestrator/events.jsonl').read_text().splitlines()
        self.assertEqual('{"event_type":', lines[0])
        self.assertEqual('BLOCKER_RECONCILED', json.loads(lines[1])['event_type'])
        self.assertEqual('PAUSED', self.engine().state['mode'])

    def test_unblock_changed_pending_baseline_rejected(self):
        engine = self.prerequisite_blocked()
        with patch.object(engine, 'event', side_effect=Crash()), self.assertRaises(Crash):
            engine.unblock('T001', 'Prerequisite provided')
        (self.root / 'owner.txt').write_text('new work after interrupted command')
        with self.assertRaises(o.SafetyError):
            self.engine().unblock('T001', 'Prerequisite provided')
        self.assertEqual('BLOCKED', self.engine().state['mode'])

    def test_unblock_cli_requires_task_and_reason(self):
        for args in [['unblock'], ['unblock', 'T001'], ['unblock', '--reason', 'fixed'], ['unblock', 'T001', '--reason', ' ']]:
            with self.subTest(args=args), contextlib.redirect_stderr(__import__('io').StringIO()), self.assertRaises(SystemExit):
                o.main(args)
        engine = self.prerequisite_blocked()
        with patch.object(o, 'ROOT', self.root), contextlib.redirect_stdout(__import__('io').StringIO()):
            self.assertEqual(0, o.main(['unblock', 'T001', '--reason', 'Local runtime supplied']))
        self.assertEqual('NOT_STARTED', self.engine().state['tasks']['T001']['status'])

    def test_real_subprocess_adapter_with_fake_executables(self):
        fake = self.root / '.orchestrator/fake_agent.py'
        fake.write_text('''import sys,pathlib
actor=sys.argv[1]
if actor=='codex':
    sys.stdin.read()
    pathlib.Path('alpha.py').write_text('value=1\\n')
    report="IMPLEMENTATION_COMPLETE\\nCHANGED_FILES:\\n- alpha.py\\nTESTS_RUN:\\n- fake\\nRESULTS:\\n- passed\\nBLOCKERS:\\nNONE\\n"
    pathlib.Path(sys.argv[sys.argv.index('-o')+1]).write_text(report)
    print('fake implementation log',flush=True)
else:
    print('VERDICT: PASS',flush=True)
print('fake stderr',file=sys.stderr,flush=True)
''')
        with patch.object(o, 'CODEX_BASE', [sys.executable, str(fake), 'codex']), patch.object(o, 'REVIEW_BASE', [sys.executable, str(fake), 'reviewer']):
            engine = self.engine(o.ProcessRunner())
            engine.run(verify=False)
        self.assertEqual('PASS', engine.state['tasks']['T001']['status'])
        self.assertIsNone(engine.state['process'])
        self.assertIn('CODEX_OUTPUT', self.root.joinpath('.orchestrator/events.jsonl').read_text())

    def test_stop_terminates_owned_fake_process_group(self):
        fake = self.root / '.orchestrator/fake_sleep.py'
        fake.write_text('import time\nprint("started",flush=True)\ntime.sleep(60)\n')
        engine = self.engine(o.ProcessRunner())
        def stop():
            for _ in range(100):
                if engine.child is not None:
                    o.request_control(self.root, 'stop')
                    return
                time.sleep(.02)
        thread = threading.Thread(target=stop, daemon=True)
        thread.start()
        with patch.object(o, 'CODEX_BASE', [sys.executable, str(fake)]), self.assertRaises(o.SafetyError):
            engine.run(verify=False)
        thread.join(timeout=2)
        self.assertIsNone(engine.child)
        self.assertEqual('BLOCKED', engine.state['mode'])

if __name__ == '__main__':
    unittest.main()
