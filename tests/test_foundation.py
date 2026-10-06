"""Offline behavioral proof for T001; every subprocess denies networking."""
import subprocess
import sys
import unittest

SYNTHETIC_SECRET = "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NETWORK_GUARD = '''
import socket
def denied(*args, **kwargs):
    raise AssertionError("Network access prohibited in T001 tests")
socket.socket.connect = denied
socket.socket.connect_ex = denied
socket.socket.sendto = denied
socket.create_connection = denied
socket.getaddrinfo = denied
socket.gethostbyname = denied
socket.gethostbyname_ex = denied
socket.gethostbyaddr = denied
'''


def run_offline(code, **settings):
    env = {"ALPHA_SECRET_KEY": SYNTHETIC_SECRET,
           "DJANGO_SETTINGS_MODULE": "config.settings", **settings}
    return subprocess.run([sys.executable, "-c", NETWORK_GUARD + code],
                          env=env, capture_output=True, text=True, timeout=20)


class ConfigurationTests(unittest.TestCase):
    def test_profiles_and_secret_redaction(self):
        result = run_offline('''
from config.environment import load_config
from django.views.debug import SafeExceptionReporterFilter
import os
config = load_config(os.environ)
assert config.profile == "owner-local"
assert not config.providers_enabled
assert config.secret_key not in repr(config)
assert SafeExceptionReporterFilter().cleanse_setting("SECRET_KEY", config.secret_key) == "********************"
import config.settings as s
assert not s.DEBUG and not s.SESSION_COOKIE_SECURE
assert s.SESSION_COOKIE_HTTPONLY and s.CSRF_COOKIE_HTTPONLY
assert s.SESSION_COOKIE_SAMESITE == s.CSRF_COOKIE_SAMESITE == "Lax"
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = run_offline('''
import config.settings as s
assert s.RUNTIME.profile == "invited-alpha"
assert s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE and s.SECURE_SSL_REDIRECT
assert not s.DEBUG and not s.ALPHA_PROVIDERS_ENABLED
assert s.ALLOWED_HOSTS == ["alpha.example.test"]
assert s.SECURE_PROXY_SSL_HEADER is None if hasattr(s, "SECURE_PROXY_SSL_HEADER") else True
''', ALPHA_PROFILE="invited-alpha", ALPHA_ALLOWED_HOSTS="alpha.example.test")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_configuration_fails_without_echoing_values(self):
        cases = [
            {"ALPHA_SECRET_KEY": ""}, {"ALPHA_SECRET_KEY": "short-secret"},
            {"ALPHA_SECRET_KEY": "x" * 60},
            {"ALPHA_PROFILE": "unknown-profile-value"},
            {"ALPHA_UNKNOWN_SECRET": "do-not-echo-value"},
            {"ALPHA_PROVIDERS_ENABLED": "true"},
            {"ALPHA_PROVIDERS_ENABLED": "typo"},
            {"ALPHA_PROFILE": "invited-alpha"},
            {"ALPHA_PROFILE": "invited-alpha", "ALPHA_ALLOWED_HOSTS": "*"},
            {"ALPHA_ALLOWED_HOSTS": "remote.example.test"},
        ]
        for values in cases:
            with self.subTest(values=tuple(values)):
                result = run_offline('''
import os
from config.environment import load_config
from django.core.exceptions import ImproperlyConfigured
try:
    load_config(os.environ)
except ImproperlyConfigured as exc:
    print(str(exc))
else:
    raise AssertionError("Invalid configuration accepted")
''', **values)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(SYNTHETIC_SECRET, result.stdout + result.stderr)
                self.assertNotIn("do-not-echo-value", result.stdout + result.stderr)

    def test_missing_secret_rejects_web_startup(self):
        result = run_offline('import config.wsgi', ALPHA_SECRET_KEY="")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ALPHA_SECRET_KEY requires", result.stderr)


class ProcessBoundaryTests(unittest.TestCase):
    def test_startup_system_checks_and_smoke_request_under_network_denial(self):
        result = run_offline('''
import config.wsgi
import config.asgi
import alpha.domain, alpha.services, alpha.models
import sys
from django.core.management import call_command
from django.test import Client
call_command("check")
client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")
response = client.get("/health/")
assert response.status_code == 200 and response.json() == {"status": "ok"}
assert response["X-Frame-Options"] == "DENY"
assert response["X-Content-Type-Options"] == "nosniff"
assert client.post("/health/").status_code == 403
assert client.get("/signup/").status_code == 404
assert client.get("/media/private-file").status_code == 404
assert client.get("/health/", HTTP_HOST="untrusted.example.test").status_code == 400
assert "alpha.worker" not in sys.modules
assert "alpha.maintenance" not in sys.modules
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("System check identified no issues", result.stdout)

    def test_invited_https_boundary(self):
        result = run_offline('''
import config.wsgi
from django.test import Client
client = Client(HTTP_HOST="alpha.example.test")
assert client.get("/health/").status_code == 301
assert client.get("/health/", secure=True).status_code == 200
''', ALPHA_PROFILE="invited-alpha", ALPHA_ALLOWED_HOSTS="alpha.example.test")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_separate_entry_points_refuse_execution_without_side_effects(self):
        for module in ("alpha.worker", "alpha.maintenance"):
            for secret in ("", SYNTHETIC_SECRET):
                with self.subTest(module=module, configured=bool(secret)):
                    result = run_offline(f'import runpy; runpy.run_module({module!r}, run_name="__main__")', ALPHA_SECRET_KEY=secret)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("unconfigured" if secret else "ALPHA_SECRET_KEY requires", result.stderr)
                    self.assertNotIn(SYNTHETIC_SECRET, result.stderr)

    def test_importing_process_modules_does_not_execute_them(self):
        result = run_offline('import alpha.worker; import alpha.maintenance', ALPHA_SECRET_KEY="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout + result.stderr, "")


if __name__ == "__main__":
    unittest.main()
