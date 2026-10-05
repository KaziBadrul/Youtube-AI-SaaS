"""Offline T001 proof. Synthetic configuration never authorizes providers."""
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from config.environment import load_config
from django.core.exceptions import ImproperlyConfigured

ROOT = Path(__file__).resolve().parents[2]
SECRET = "synthetic-offline-test-key-0123456789-abcdefghijklmnopqrstuvwxyz"


def environment(profile="owner-local"):
    # Do not inherit product credentials or settings into test subprocesses.
    return {"PATH": os.defpath, "ALPHA_PROFILE": profile, "ALPHA_SECRET_KEY": SECRET,
            "DJANGO_SETTINGS_MODULE": "config.settings", "PYTHONDONTWRITEBYTECODE": "1"}


def run_code(code, profile="owner-local"):
    return subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                          env=environment(profile), capture_output=True, text=True, timeout=30)


class ConfigurationTests(unittest.TestCase):
    def test_local_defaults_and_secret_redaction(self):
        config = load_config(environment())
        self.assertEqual(config.allowed_hosts, ("localhost", "127.0.0.1", "[::1]"))
        self.assertFalse(config.providers_enabled)
        self.assertNotIn(SECRET, repr(config))

    def test_invited_requires_hosts(self):
        env = environment("invited-alpha")
        with self.assertRaises(ImproperlyConfigured):
            load_config(env)
        env["ALPHA_ALLOWED_HOSTS"] = "alpha.example.test"
        self.assertEqual(load_config(env).profile, "invited-alpha")

    def test_missing_and_weak_secrets(self):
        for secret in ("", "short", "x" * 60, "django-insecure-" + SECRET):
            with self.subTest(secret_length=len(secret)):
                env = environment()
                env["ALPHA_SECRET_KEY"] = secret
                with self.assertRaises(ImproperlyConfigured) as caught:
                    load_config(env)
                if secret:
                    self.assertNotIn(secret, str(caught.exception))

    def test_unknown_settings_profiles_and_provider_enablement(self):
        for key, value in (("ALPHA_UNKNOWN", SECRET), ("ALPHA_PROFILE", SECRET),
                           ("ALPHA_PROVIDERS_ENABLED", "true"), ("ALPHA_PROVIDERS_ENABLED", "garbage")):
            with self.subTest(key=key, value=value):
                env = environment()
                env[key] = value
                with self.assertRaises(ImproperlyConfigured) as caught:
                    load_config(env)
                self.assertNotIn(SECRET, str(caught.exception))

    def test_bad_hosts_and_local_remote_binding(self):
        for hosts in ("", "*", ".example.test", "https://example.test", "localhost:8000", "localhost,", "example.test"):
            env = environment()
            env["ALPHA_ALLOWED_HOSTS"] = hosts
            with self.subTest(hosts=hosts), self.assertRaises(ImproperlyConfigured):
                load_config(env)


class ProcessTests(unittest.TestCase):
    def test_import_wsgi_checks_and_smoke_without_network(self):
        code = '''
import socket
from unittest.mock import patch

def denied(*args, **kwargs):
    raise AssertionError("network forbidden")

with patch.object(socket.socket, "connect", denied), patch.object(socket.socket, "connect_ex", denied), patch.object(socket, "create_connection", denied), patch.object(socket, "getaddrinfo", denied):
    import config.wsgi
    import alpha.worker
    import alpha.maintenance
    from django.core.management import call_command
    from django.test import Client
    call_command("check")
    client = Client(enforce_csrf_checks=True)
    assert client.get("/health/", HTTP_HOST="localhost").json() == {"status": "ok"}
    assert client.post("/health/", HTTP_HOST="localhost").status_code == 403
    for path in ("/signup/", "/media/private.png", "/private/alpha.sqlite3", "/worker/", "/maintenance/"):
        assert client.get(path, HTTP_HOST="localhost").status_code == 404
    assert client.get("/health/", HTTP_HOST="untrusted.test").status_code == 400
    import sys
    assert not any(name.startswith("spikes") for name in sys.modules)
'''
        result = run_code(code)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_separate_processes_refuse_with_or_without_configuration(self):
        for module, role in (("alpha.worker", "production worker"), ("alpha.maintenance", "maintenance")):
            for configured in (False, True):
                env = environment()
                if not configured:
                    del env["ALPHA_SECRET_KEY"]
                result = subprocess.run([sys.executable, "-m", module], cwd=ROOT, env=env,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 2)
                self.assertIn(role, result.stderr)
                self.assertIn("execution unavailable" if configured else "configuration rejected", result.stderr)
                self.assertNotIn(SECRET, result.stderr)

    def test_invited_security_and_smoke(self):
        code = '''
import os
os.environ["ALPHA_ALLOWED_HOSTS"] = "alpha.example.test"
import config.wsgi
from django.conf import settings
from django.test import Client
assert not settings.DEBUG
assert settings.SESSION_COOKIE_SECURE and settings.CSRF_COOKIE_SECURE
assert settings.SESSION_COOKIE_HTTPONLY and settings.CSRF_COOKIE_HTTPONLY
assert settings.X_FRAME_OPTIONS == "DENY"
assert not settings.ALPHA_PROVIDERS_ENABLED
client = Client(enforce_csrf_checks=True)
assert client.get("/health/", HTTP_HOST="alpha.example.test").status_code == 301
response = client.get("/health/", HTTP_HOST="alpha.example.test", secure=True)
assert response.json() == {"status": "ok"}
assert response["X-Frame-Options"] == "DENY"
assert client.post("/health/", HTTP_HOST="alpha.example.test", secure=True).status_code == 403
'''
        result = run_code(code, "invited-alpha")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_web_does_not_import_process_execution(self):
        result = run_code('''
import config.wsgi
import sys
assert "alpha.worker" not in sys.modules
assert "alpha.maintenance" not in sys.modules
assert "alpha.processes" not in sys.modules
''')
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
