#!/usr/bin/env python3
"""
Executable test runner establishing named test categories and offline discipline.

Categories:
  unit        - Exact money/time conversions, bounded parsers, pure helpers
  domain      - Typed versions, projections, invalidation, consent, configuration
  database    - Constraints, migrations, WAL/CAS races, rollback, durability
  integration - Fake providers through admission -> registration/accounting
  financial   - Shared/project/creator limits, reservations, billed failure
  worker      - Global lane, fences, crash windows, restart, process cessation
  security    - Sessions/CSRF, cross-user isolation, upload paths, owner checks
  media       - Hash/decode/range coverage, continuous narration, captions, render
  ui          - Desktop/mobile themes, layout, focus, contrast, reduced motion
  e2e         - Core fake journeys, selective correction, interruption, recovery
  regression  - Complete full offline regression suite across all categories
"""
import argparse
import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SYNTHETIC_SECRET = (
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

CATEGORIES = {
    "unit": ["tests.unit"],
    "domain": ["tests.domain"],
    "database": ["tests.database"],
    "integration": ["tests.integration"],
    "financial": ["tests.financial"],
    "worker": ["tests.worker"],
    "security": ["tests.security"],
    "media": ["tests.media"],
    "ui": ["tests.ui"],
    "e2e": ["tests.e2e"],
    "regression": [
        "tests.test_foundation",
        "tests.test_harness",
        "tests.unit",
        "tests.domain",
        "tests.database",
        "tests.integration",
        "tests.financial",
        "tests.worker",
        "tests.security",
        "tests.media",
        "tests.ui",
        "tests.e2e",
    ],
}


def bootstrap_offline_environment() -> None:
    """Ensure environment is configured for offline, zero-network execution."""
    os.environ.setdefault("ALPHA_SECRET_KEY", SYNTHETIC_SECRET)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # Ensure repository root is in sys.path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    # Activate global network trap
    from tests.framework.network import install_global_network_trap

    install_global_network_trap()

    # Bootstrap Django
    import django

    django.setup()


def run_category(category_name: str, verbosity: int = 2, failfast: bool = False) -> bool:
    """Run all test suites associated with the given category."""
    if category_name not in CATEGORIES:
        print(f"Unknown test category: '{category_name}'. Available: {', '.join(CATEGORIES.keys())}")
        return False

    bootstrap_offline_environment()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    modules = CATEGORIES[category_name]
    for mod_name in modules:
        mod_dir = BASE_DIR / mod_name.replace(".", "/")
        if mod_dir.is_dir():
            discovered = loader.discover(
                start_dir=str(mod_dir),
                pattern="test_*.py",
                top_level_dir=str(BASE_DIR),
            )
            suite.addTests(discovered)
        else:
            try:
                loaded = loader.loadTestsFromName(mod_name)
                suite.addTests(loaded)
            except Exception as exc:
                print(f"Warning: Could not load tests from '{mod_name}': {exc}")

    runner = unittest.TextTestRunner(verbosity=verbosity, failfast=failfast)
    result = runner.run(suite)
    return result.wasSuccessful()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run offline test suites by category with strict network prohibition.",
    )
    parser.add_argument(
        "category",
        nargs="?",
        default="regression",
        choices=list(CATEGORIES.keys()),
        help="Named test category to run (default: regression)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available test categories and exit",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=2,
        help="Increase output verbosity",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet output",
    )
    parser.add_argument(
        "--failfast",
        action="store_true",
        help="Stop on first failure",
    )

    args = parser.parse_args()

    if args.list:
        print("Available test categories:")
        for cat in CATEGORIES:
            print(f"  - {cat}")
        sys.exit(0)

    verbosity = 0 if args.quiet else args.verbose
    success = run_category(args.category, verbosity=verbosity, failfast=args.failfast)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
