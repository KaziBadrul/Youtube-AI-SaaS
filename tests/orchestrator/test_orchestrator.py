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
