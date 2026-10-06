"""Fixture integrity preservation, hashing, and disposable workspace discipline."""
import contextlib
import hashlib
import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Generator, Iterable


class FixtureTamperedError(RuntimeError):
    """Raised when a fixture's content does not match its recorded canonical hash."""
    pass


def compute_file_sha256(path: Path | str) -> str:
    """Calculate the SHA-256 digest of a fixture file."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Fixture file not found: {p}")
    hasher = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_fixture_integrity(fixture_path: Path | str, expected_sha256: str) -> None:
    """
    Verify that the fixture matches its expected hash.
    Raises FixtureTamperedError if a mismatch is detected.
    """
    actual = compute_file_sha256(fixture_path)
    if actual.lower() != expected_sha256.lower():
        raise FixtureTamperedError(
            f"Fixture integrity violation for '{fixture_path}': "
            f"expected SHA-256 {expected_sha256}, got {actual}."
        )


def make_readonly(path: Path) -> None:
    """Recursively set read-only file permissions on path."""
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                current_mode = child.stat().st_mode
                child.chmod(current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    elif path.is_file():
        current_mode = path.stat().st_mode
        path.chmod(current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


@contextlib.contextmanager
def disposable_workspace(
    fixtures: Iterable[Path | str] | None = None,
    prefix: str = "alpha-test-ws-",
) -> Generator[Path, None, None]:
    """
    Context manager providing an isolated, disposable directory.

    If fixtures are provided, they are copied into the workspace.
    Guarantees cleanup on exit even when unhandled exceptions occur.
    """
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    ws_path = Path(temp_dir).resolve()
    try:
        if fixtures:
            for fix in fixtures:
                src = Path(fix)
                if not src.exists():
                    raise FileNotFoundError(f"Fixture does not exist: {src}")
                dest = ws_path / src.name
                if src.is_dir():
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
        yield ws_path
    finally:
        # Restore permissions if made read-only before removing
        for root, dirs, files in os.walk(temp_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    os.chmod(fpath, stat.S_IWUSR | stat.S_IRUSR)
                except OSError:
                    pass
            for dname in dirs:
                dpath = os.path.join(root, dname)
                try:
                    os.chmod(dpath, stat.S_IRWXU)
                except OSError:
                    pass
        shutil.rmtree(temp_dir, ignore_errors=True)
