#!/usr/bin/env python3
"""Read-only local monitor. No execution or transition endpoints."""
from __future__ import annotations
import argparse
import datetime as dt
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import socket
import sys
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orchestrator import ROOT, Engine, SafetyError, redact


def tail(path, size=24000):
    if not path.is_file() or path.is_symlink():
        return ''
    with path.open('rb') as stream:
        stream.seek(max(0, path.stat().st_size - size))
        return redact(stream.read(size).decode(errors='replace'))


def safe_attempt(root, state):
    task_id = state.get('active_task_id') or state.get('last_task_id')
    run_id = state.get('run_id')
    record = state['tasks'].get(task_id, {})
    attempt = record.get('current_attempt', 0)
    if not re.fullmatch(r'T\d{3}', task_id or '') or not re.fullmatch(r'[a-f0-9]{32}', run_id or '') or not isinstance(attempt, int) or attempt < 1:
        return None
    path = root / '.orchestrator/runs' / task_id / run_id / f'attempt-{attempt:02d}'
    if not path.resolve().is_relative_to((root / '.orchestrator/runs').resolve()):
        return None
    return path


def load_dashboard(root=ROOT):
    try:
        engine = Engine(root)
        state = engine.state
        active = state.get('active_task_id')
        record = state['tasks'].get(active, {})
        process = state.get('process') or {}
        tasks = [{'id': t.id, 'title': t.title, 'phase': t.fields['Phase'],
                  'status': state['tasks'][t.id]['status'], 'optional': t.optional,
                  'dependencies': t.dependencies,
                  'dependencies_passed': sum(state['tasks'][d]['status'] == 'PASS' for d in t.dependencies)} for t in engine.tasks]
        directory = safe_attempt(Path(root), state)
        events = []
        for line in tail(Path(root) / '.orchestrator/events.jsonl').splitlines()[-50:]:
            try:
                value = json.loads(line)
                # Allowlist fields, never send arbitrary stored objects/config/environment.
                events.append({k: value.get(k) for k in ['timestamp', 'task_id', 'attempt', 'actor', 'event_type', 'status', 'message']})
            except ValueError:
                continue
        active_task = next((t for t in tasks if t['id'] == active), None)
        elapsed = 0
        if record.get('start_timestamp'):
            elapsed = max(0, int((dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(record['start_timestamp'])).total_seconds()))
        result = {'mode': state['mode'], 'active_task': active_task, 'attempt': record.get('current_attempt', 0),
                  'repair_count': record.get('repair_count', 0), 'elapsed_seconds': elapsed,
                  'process': {k: process.get(k) for k in ['actor', 'pid', 'pgid', 'started']},
                  'reviewer_verdict': record.get('reviewer_verdict'),
                  'blocker': record.get('blocker_reason') or state.get('blocker_reason'),
                  'completed': sum(t['status'] == 'PASS' for t in tasks),
                  'remaining': sum(t['status'] != 'PASS' for t in tasks), 'latest_commit': state.get('latest_commit'),
                  'tasks': tasks, 'events': events,
                  'codex_output': tail(directory / 'codex-output.txt') if directory else '',
                  'reviewer_output': tail(directory / 'reviewer-output.txt') if directory else '',
                  'last_codex_exit_code': record.get('last_codex_exit_code'),
                  'last_opencode_exit_code': record.get('last_opencode_exit_code')}
        # Redact values without corrupting JSON syntax.
        def clean(value):
            if isinstance(value, str):
                return redact(value)
            if isinstance(value, dict):
                return {k: clean(v) for k, v in value.items()}
            if isinstance(value, list):
                return [clean(v) for v in value]
            return value
        return clean(result)
    except (SafetyError, ValueError, OSError, KeyError) as error:
        return {'mode': 'BLOCKED', 'blocker': redact(str(error)), 'tasks': [], 'events': [], 'completed': 0, 'remaining': 0}


def handler_for(root):
    root = Path(root)
    assets = {'/': (root / 'templates/orchestrator/dashboard.html', 'text/html; charset=utf-8'),
              '/dashboard.css': (root / 'static/orchestrator/dashboard.css', 'text/css; charset=utf-8'),
              '/dashboard.js': (root / 'static/orchestrator/dashboard.js', 'text/javascript; charset=utf-8')}
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Block DNS-rebinding hosts. LAN/Tailscale IPs are accepted; no wildcard DNS.
            host = self.headers.get('Host', '').split(':')[0]
            if host not in {'localhost', '127.0.0.1', self.server.server_address[0]}:
                import ipaddress
                try:
                    address = ipaddress.ip_address(host)
                    if not (address.is_private or address.is_loopback or address in ipaddress.ip_network('100.64.0.0/10')):
                        raise ValueError()
                except ValueError:
                    self.send_error(403)
                    return
            path = urlsplit(self.path).path
            if path == '/api/status':
                body = json.dumps(load_dashboard(root)).encode()
                content_type = 'application/json'
            elif path in assets:
                file, content_type = assets[path]
                body = file.read_bytes()
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def do_POST(self):
            self.send_error(405, 'Monitoring only')
        do_PUT = do_POST
        do_DELETE = do_POST
        do_PATCH = do_POST
        def log_message(self, *_):
            pass
    return Handler


def lan_addresses():
    addresses = set()
    for name in (socket.gethostname(), socket.gethostname() + '.local'):
        try:
            for info in socket.getaddrinfo(name, None, socket.AF_INET):
                if not info[4][0].startswith('127.'):
                    addresses.add(info[4][0])
        except socket.gaierror:
            pass
    return sorted(addresses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port or Engine(ROOT).config['dashboard_port']
    server = ThreadingHTTPServer((args.host, port), handler_for(ROOT))
    print(f'Local:\nhttp://127.0.0.1:{port}', flush=True)
    if args.host == '0.0.0.0':
        addresses = lan_addresses()
        print('Phone/LAN:\n' + ('\n'.join(f'http://{address}:{port}' for address in addresses) or 'Find your Mac IP in System Settings → Wi-Fi → Details → TCP/IP.'), flush=True)
    elif args.host != '127.0.0.1':
        print(f'Phone/LAN:\nhttp://{args.host}:{port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
