# Offline Test Suites and Fixture Discipline (T003)

This directory houses the offline automated test suites and testing infrastructure for the Private Alpha codebase.

## Core Rules

1. **Zero External Network**: All standard test suites run strictly offline. Outbound sockets, DNS queries, HTTP clients, and provider SDK fetches are intercepted by `NetworkTrap` and raise `NetworkAccessDeniedError`.
2. **Zero API Key Requirements**: Standard test suites run without external provider credentials or live accounts, using deterministic synthetic fixtures.
3. **Fixture Immutability and Hashing**: Canonical fixtures (in `tests/fixtures/`) are cryptographically hashed with SHA-256 (`.sha256`). Any unauthorized modification raises `FixtureTamperedError`.
4. **Disposable Workspaces**: Tests mutating files must use `disposable_workspace()` context managers to ensure test isolation and complete filesystem cleanup on both success and failure.
5. **Deterministic Test Doubles**: Clocks (`FakeClock` / `freeze_time`) and provider responses (`FakeProviderResponse`) provide deterministic timing and synthetic outputs.

---

## Executable Category Test Commands

Use `python3 run_tests.py <category>` or `.venv/bin/python run_tests.py <category>`.

### Named Categories

| Category | Command | Behavioral Focus |
|---|---|---|
| **Unit** | `python3 run_tests.py unit` | Exact money/time conversions, bounded parsers, pure helpers |
| **Domain** | `python3 run_tests.py domain` | Typed versions, projections, invalidation/preservation, consent and configuration |
| **Database** | `python3 run_tests.py database` | Constraints, migrations, WAL/CAS races, rollback and durability |
| **Integration** | `python3 run_tests.py integration` | Fake providers through admission → registration/accounting and current selection |
| **Financial** | `python3 run_tests.py financial` | Shared/project/creator limits, reservations, billed failure, uncertainty, replay |
| **Worker** | `python3 run_tests.py worker` | Global lane, fences, crash windows, restart, unknown outcomes and process cessation |
| **Security** | `python3 run_tests.py security` | Sessions/CSRF, cross-user resources/ranges, uploads/paths, owner-only authority |
| **Media / Render** | `python3 run_tests.py media` | Hash/decode/range coverage, continuous narration, captions, frame order |
| **UI** | `python3 run_tests.py ui` | Desktop/mobile themes, layout, focus, contrast, reduced motion |
| **E2E** | `python3 run_tests.py e2e` | Core fake journeys, selective correction, interruption, deletion/restore |
| **Full Regression** | `python3 run_tests.py regression` | Runs all test suites across all categories and framework verification |

### Listing Categories

```sh
python3 run_tests.py --list
```

### Standard Django / Unittest Invocation

You can also run tests directly with python/unittest:

```sh
ALPHA_SECRET_KEY="synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## Testing Utilities

Located in `tests/framework/`:

- `NetworkTrap`, `install_global_network_trap()`: Prevents outbound network connections.
- `disposable_workspace(fixtures=[...])`: Provides isolated temporary execution directories with guaranteed teardown.
- `compute_file_sha256()`, `verify_fixture_integrity()`: Enforces SHA-256 fixture checksums.
- `FakeClock`, `freeze_time()`: Freezes and advances time deterministically.
- `run_isolated_process(code)`: Executes subprocesses under isolated environment and default network trap.
- `FakeProviderResponse`: Generates typed synthetic model responses.
