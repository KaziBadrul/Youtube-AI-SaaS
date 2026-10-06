"""Automated verification suite for T003 test harness and offline discipline."""
import http.client
import os
import socket
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path

from tests.framework.clock import FakeClock, freeze_time
from tests.framework.doubles import (
    FakeProviderResponse,
    run_isolated_process,
)
from tests.framework.fixtures import (
    FixtureTamperedError,
    compute_file_sha256,
    disposable_workspace,
    verify_fixture_integrity,
)
from tests.framework.network import (
    NetworkAccessDeniedError,
    NetworkTrap,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class NetworkTrapTests(unittest.TestCase):
    def test_network_trap_catches_socket_connect(self) -> None:
        """Verify socket.connect is trapped and raises NetworkAccessDeniedError."""
        with NetworkTrap():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                with self.assertRaises(NetworkAccessDeniedError):
                    sock.connect(("8.8.8.8", 53))

    def test_network_trap_catches_dns_resolution(self) -> None:
        """Verify DNS lookups (getaddrinfo, gethostbyname) are trapped."""
        with NetworkTrap():
            with self.assertRaises(NetworkAccessDeniedError):
                socket.gethostbyname("api.google.com")
            with self.assertRaises(NetworkAccessDeniedError):
                socket.getaddrinfo("generativelanguage.googleapis.com", 443)

    def test_network_trap_catches_urllib_request(self) -> None:
        """Verify urllib.request is trapped and raises NetworkAccessDeniedError."""
        with NetworkTrap():
            with self.assertRaises(NetworkAccessDeniedError):
                urllib.request.urlopen("https://api.google.com/models")

    def test_network_trap_simulated_sdk_model_fetch(self) -> None:
        """
        Simulate an SDK client initialization and model fetch attempting outbound HTTP.
        Proves that provider SDK network calls are trapped and denied.
        """
        def simulated_sdk_client_fetch_models() -> list[str]:
            conn = http.client.HTTPSConnection("generativelanguage.googleapis.com", timeout=2)
            conn.request("GET", "/v1beta/models?key=fake-key")
            resp = conn.getresponse()
            return [resp.status]

        with NetworkTrap():
            with self.assertRaises(NetworkAccessDeniedError):
                simulated_sdk_client_fetch_models()


class FixtureDisciplineTests(unittest.TestCase):
    def test_fixture_hash_preservation(self) -> None:
        """Verify fixture SHA-256 digest matches recorded reference."""
        fixture_file = FIXTURES_DIR / "sample_script.txt"
        sha_file = FIXTURES_DIR / "sample_script.txt.sha256"

        self.assertTrue(fixture_file.exists(), f"Missing fixture file: {fixture_file}")
        self.assertTrue(sha_file.exists(), f"Missing sha file: {sha_file}")

        expected_hash = sha_file.read_text().strip()
        actual_hash = compute_file_sha256(fixture_file)
        self.assertEqual(actual_hash, expected_hash)
        # verify_fixture_integrity should succeed without error
        verify_fixture_integrity(fixture_file, expected_hash)

    def test_fixture_tampering_detected(self) -> None:
        """Verify tampering with a fixture file is caught and raises FixtureTamperedError."""
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            tf.write("original untampered content")
            tf.flush()
            tmp_path = Path(tf.name)

        try:
            expected_hash = compute_file_sha256(tmp_path)
            # Tamper with file
            tmp_path.write_text("tampered malicious content")

            with self.assertRaises(FixtureTamperedError) as ctx:
                verify_fixture_integrity(tmp_path, expected_hash)
            self.assertIn("integrity violation", str(ctx.exception).lower())
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_disposable_workspace_isolation_and_cleanup(self) -> None:
        """Verify disposable workspace provides isolation and cleans up on normal exit."""
        fixture_file = FIXTURES_DIR / "sample_script.txt"
        ws_location = None

        with disposable_workspace(fixtures=[fixture_file]) as ws:
            ws_location = ws
            self.assertTrue(ws.is_dir())
            copied_file = ws / "sample_script.txt"
            self.assertTrue(copied_file.exists())
            # Mutate file in workspace
            copied_file.write_text("modified in workspace")
            self.assertEqual(copied_file.read_text(), "modified in workspace")
            # Original fixture is unaffected
            self.assertNotEqual(fixture_file.read_text(), "modified in workspace")

        # After context exit, temporary workspace must be completely removed
        self.assertFalse(ws_location.exists(), "Workspace directory must be cleaned up")

    def test_disposable_workspace_cleanup_on_failed_test(self) -> None:
        """Verify workspace is cleanly destroyed even when an exception/failure occurs."""
        ws_location = None
        try:
            with disposable_workspace() as ws:
                ws_location = ws
                (ws / "artifact.dat").write_bytes(b"data")
                raise RuntimeError("Simulated test assertion failure")
        except RuntimeError:
            pass

        self.assertIsNotNone(ws_location)
        self.assertFalse(ws_location.exists(), "Workspace must be cleaned up after error")


class DeterministicDoublesTests(unittest.TestCase):
    def test_fake_clock_determinism(self) -> None:
        """Verify FakeClock freezes time and advances deterministically."""
        with freeze_time() as clock:
            t0 = clock.time()
            m0 = clock.monotonic()

            clock.advance(30.0)
            self.assertEqual(clock.time() - t0, 30.0)
            self.assertEqual(clock.monotonic() - m0, 30.0)

            # verify negative advance is rejected
            with self.assertRaises(ValueError):
                clock.advance(-5.0)

    def test_isolated_process_and_crash_fixtures(self) -> None:
        """Verify run_isolated_process runs code, traps network, and detects crashes."""
        # Clean execution
        res = run_isolated_process("print('hello offline')")
        self.assertEqual(res.returncode, 0)
        self.assertIn("hello offline", res.stdout)

        # Crash detection (e.g. exit code 88)
        crash_res = run_isolated_process("import os; os._exit(88)")
        self.assertEqual(crash_res.returncode, 88)

        # Network trap enforced by default inside subprocess
        net_res = run_isolated_process(
            "import socket; sock = socket.socket(); sock.connect(('8.8.8.8', 53))"
        )
        self.assertNotEqual(net_res.returncode, 0)
        self.assertIn("NetworkAccessDeniedError", net_res.stderr)

    def test_fake_provider_response_fixtures(self) -> None:
        """Verify synthetic provider responses are deterministic and labeled synthetic."""
        text_resp = FakeProviderResponse.text_generation("test prompt")
        self.assertTrue(text_resp["synthetic"])
        self.assertEqual(text_resp["model"], "fake-text-model-v1")

        img_resp = FakeProviderResponse.image_generation("scene visual")
        self.assertTrue(img_resp["synthetic"])
        self.assertEqual(img_resp["dimensions"], (1920, 1080))
        self.assertEqual(img_resp["mime_type"], "image/webp")

        tts_resp = FakeProviderResponse.tts_generation("Hello world")
        self.assertTrue(tts_resp["synthetic"])
        self.assertEqual(tts_resp["mime_type"], "audio/wav")
        self.assertEqual(tts_resp["duration_seconds"], 2.5)


class CommandDiscoveryTests(unittest.TestCase):
    def test_command_discovery_smoke(self) -> None:
        """Verify run_tests.py discovers categories and --list runs cleanly."""
        res = run_isolated_process(
            "import subprocess, sys\n"
            "p = subprocess.run([sys.executable, 'run_tests.py', '--list'], capture_output=True, text=True)\n"
            "print('RC:', p.returncode)\n"
            "print('OUT:', p.stdout)\n"
            "assert p.returncode == 0\n"
            "for cat in ['unit', 'domain', 'database', 'integration', 'financial', 'worker', 'security', 'media', 'ui', 'e2e', 'regression']:\n"
            "    assert cat in p.stdout, f'Missing category: {cat}'\n"
        )
        self.assertEqual(res.returncode, 0, f"Command discovery failed: {res.stderr}")
        self.assertIn("RC: 0", res.stdout)


if __name__ == "__main__":
    unittest.main()
