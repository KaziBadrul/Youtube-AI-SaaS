"""Deterministic provider test doubles and isolated process execution controls."""
import os
import subprocess
import sys
from typing import Any, NamedTuple


class ProcessResult(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def run_isolated_process(
    code: str,
    extra_env: dict[str, str] | None = None,
    timeout: float = 15.0,
    enforce_network_trap: bool = True,
) -> ProcessResult:
    """
    Execute python code in a separate process with isolated environment
    and optional network trap prefix.
    """
    env = os.environ.copy()
    env.setdefault(
        "ALPHA_SECRET_KEY",
        "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )
    env.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    if extra_env:
        env.update(extra_env)

    prefix = ""
    if enforce_network_trap:
        prefix = (
            "from tests.framework.network import install_global_network_trap\n"
            "install_global_network_trap()\n"
        )

    full_code = prefix + code

    proc = subprocess.run(
        [sys.executable, "-c", full_code],
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return ProcessResult(
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


class FakeProviderResponse:
    """Deterministic synthetic provider response fixture."""

    @staticmethod
    def text_generation(prompt: str, seed: int = 42) -> dict[str, Any]:
        return {
            "synthetic": True,
            "prompt": prompt,
            "seed": seed,
            "content": f"[SYNTHETIC_GENERATION_FOR_{hash(prompt) % 10000}]",
            "model": "fake-text-model-v1",
            "usage": {"input_tokens": 50, "output_tokens": 120},
        }

    @staticmethod
    def image_generation(prompt: str, seed: int = 42) -> dict[str, Any]:
        return {
            "synthetic": True,
            "prompt": prompt,
            "seed": seed,
            "image_bytes": b"RIFF\x24\x00\x00\x00WEBPVP8 \x18\x00\x00\x000\x01\x00\x9d\x01\x2a\x01\x00\x01\x00",
            "dimensions": (1920, 1080),
            "mime_type": "image/webp",
        }

    @staticmethod
    def tts_generation(text: str, voice: str = "voice-a") -> dict[str, Any]:
        return {
            "synthetic": True,
            "text": text,
            "voice": voice,
            "audio_bytes": b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00",
            "duration_seconds": 2.5,
            "mime_type": "audio/wav",
        }
