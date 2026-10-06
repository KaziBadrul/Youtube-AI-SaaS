"""Offline test framework primitives and disciplines."""
from tests.framework.clock import FakeClock, freeze_time
from tests.framework.doubles import (
    FakeProviderResponse,
    ProcessResult,
    run_isolated_process,
)
from tests.framework.fixtures import (
    FixtureTamperedError,
    compute_file_sha256,
    disposable_workspace,
    make_readonly,
    verify_fixture_integrity,
)
from tests.framework.network import (
    NetworkAccessDeniedError,
    NetworkTrap,
    install_global_network_trap,
    uninstall_global_network_trap,
)

__all__ = [
    "NetworkTrap",
    "NetworkAccessDeniedError",
    "install_global_network_trap",
    "uninstall_global_network_trap",
    "compute_file_sha256",
    "verify_fixture_integrity",
    "FixtureTamperedError",
    "disposable_workspace",
    "make_readonly",
    "FakeClock",
    "freeze_time",
    "ProcessResult",
    "run_isolated_process",
    "FakeProviderResponse",
]
