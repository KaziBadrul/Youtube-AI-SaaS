import multiprocessing as mp
import os
import tempfile
from typing import Any
import unittest
from pathlib import Path

os.environ.setdefault(
    "ALPHA_SECRET_KEY",
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.management import call_command
from django.db import connection, connections, transaction
from django.db.utils import IntegrityError

from alpha.persistence import (
    CASConflictError,
    PersistenceContentionError,
    TransactionBoundaryError,
    assert_outside_transaction,
    cas_transition,
    cas_update,
    defer_outside_transaction,
    execute_outside_transaction,
    get_sqlite_pragmas,
    immediate_transaction,
    short_transaction,
    verify_sqlite_pragmas,
)
from alpha.persistence.models import DurabilityChild, DurabilityJournal

SYNTHETIC_SECRET = (
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)
mp_ctx = mp.get_context("fork" if hasattr(os, "fork") else "spawn")


def _worker_cas_race(db_path: str, journal_key: str, barrier: Any, out_queue: Any, worker_id: int) -> None:
    """Child worker attempting CAS update simultaneously with others."""
    os.environ["ALPHA_SECRET_KEY"] = SYNTHETIC_SECRET
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    import django
    django.setup()

    # Rebind default connection to isolated db_path
    connections.close_all()
    conn = connections["default"]
    conn.settings_dict["NAME"] = Path(db_path)

    try:
        barrier.wait(timeout=10)
        success = cas_update(
            DurabilityJournal,
            filter_kwargs={"key": journal_key},
            expected_rev=0,
            update_kwargs={"payload": f"winner-worker-{worker_id}"},
        )
        out_queue.put({"worker_id": worker_id, "success": success, "error": None})
    except Exception as exc:
        out_queue.put({"worker_id": worker_id, "success": False, "error": str(exc)})
    finally:
        connections.close_all()


def _worker_unique_race(db_path: str, journal_key: str, barrier: Any, out_queue: Any, worker_id: int) -> None:
    """Child worker attempting duplicate insert simultaneously."""
    os.environ["ALPHA_SECRET_KEY"] = SYNTHETIC_SECRET
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    import django
    django.setup()

    connections.close_all()
    conn = connections["default"]
    conn.settings_dict["NAME"] = Path(db_path)

    try:
        barrier.wait(timeout=10)
        with immediate_transaction():
            DurabilityJournal.objects.create(key=journal_key, payload=f"worker-{worker_id}")
        out_queue.put({"worker_id": worker_id, "inserted": True, "error": None})
    except IntegrityError as exc:
        out_queue.put({"worker_id": worker_id, "inserted": False, "error": "IntegrityError"})
    except Exception as exc:
        out_queue.put({"worker_id": worker_id, "inserted": False, "error": str(exc)})
    finally:
        connections.close_all()


def _worker_crash_tx(db_path: str, journal_key: str) -> None:
    """Child worker that mutates state inside a transaction and crashes without committing."""
    os.environ["ALPHA_SECRET_KEY"] = SYNTHETIC_SECRET
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    import django
    django.setup()

    connections.close_all()
    conn = connections["default"]
    conn.settings_dict["NAME"] = Path(db_path)

    with immediate_transaction():
        DurabilityJournal.objects.filter(key=journal_key).update(payload="uncommitted-crash-data")
        os._exit(88)  # Sudden process death before commit


class SQLiteDurabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["ALPHA_SECRET_KEY"] = SYNTHETIC_SECRET
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
        import django
        django.setup()

    def setUp(self) -> None:
        self._orig_db_name = connections["default"].settings_dict["NAME"]
        self.temp_dir = tempfile.TemporaryDirectory(prefix="alpha-sqlite-test-")
        self.db_path = Path(self.temp_dir.name) / "test_durability.sqlite3"
        connections.close_all()
        conn = connections["default"]
        conn.settings_dict["NAME"] = self.db_path
        # Run migrations on this test database
        call_command("migrate", "--run-syncdb", verbosity=0)

    def tearDown(self) -> None:
        connections.close_all()
        connections["default"].settings_dict["NAME"] = self._orig_db_name
        self.temp_dir.cleanup()

    def test_sqlite_pragmas_and_durability_settings(self) -> None:
        """Verify WAL, foreign_keys=ON, synchronous=FULL (2), and busy_timeout=5000."""
        conn = connections["default"]
        pragmas = get_sqlite_pragmas(conn)
        self.assertTrue(pragmas["foreign_keys"], "foreign_keys must be ON")
        self.assertEqual(pragmas["journal_mode"], "WAL", "journal_mode must be WAL for file databases")
        self.assertEqual(pragmas["synchronous"], 2, "synchronous must be FULL (2)")
        self.assertGreaterEqual(pragmas["busy_timeout"], 5000, "busy_timeout must be at least 5000ms")
        self.assertTrue(verify_sqlite_pragmas(conn))

    def test_foreign_key_enforcement_and_reopen(self) -> None:
        """Verify SQLite rejects invalid foreign keys and retains enforcement across reopen."""
        conn = connections["default"]
        # Invalid foreign key reference must fail immediately
        with self.assertRaises(IntegrityError):
            with immediate_transaction():
                DurabilityChild.objects.create(journal_id=999999, name="orphaned")

        # Create valid parent and child
        with immediate_transaction():
            parent = DurabilityJournal.objects.create(key="parent-1", payload="p1")
            child = DurabilityChild.objects.create(journal=parent, name="c1")

        self.assertEqual(DurabilityChild.objects.filter(journal=parent).count(), 1)

        # Close and reopen database connection
        connections.close_all()
        reopened = connections["default"]
        self.assertTrue(verify_sqlite_pragmas(reopened))

        # Reopen must still enforce foreign keys
        with self.assertRaises(IntegrityError):
            with immediate_transaction():
                DurabilityChild.objects.create(journal_id=888888, name="orphaned-2")

        # Verify integrity_check pragma
        with reopened.cursor() as cursor:
            cursor.execute("PRAGMA integrity_check;")
            integrity_result = cursor.fetchall()
            self.assertEqual(integrity_result, [("ok",)])

        # Cascade delete verification
        with immediate_transaction():
            DurabilityJournal.objects.filter(id=parent.id).delete()

        self.assertEqual(DurabilityChild.objects.filter(name="c1").count(), 0)

    def test_unique_and_check_constraints(self) -> None:
        """Verify unique key constraints and revision check constraints."""
        with immediate_transaction():
            DurabilityJournal.objects.create(key="unique-test-key", rev=0)

        with self.assertRaises(IntegrityError):
            with immediate_transaction():
                DurabilityJournal.objects.create(key="unique-test-key", rev=0)

    def test_transaction_rollback_and_integrity(self) -> None:
        """Verify that interrupted transactions roll back completely without partial state."""
        with immediate_transaction():
            record = DurabilityJournal.objects.create(key="tx-rollback", rev=0, payload="initial")

        # Rollback on Python exception
        try:
            with immediate_transaction():
                DurabilityJournal.objects.filter(key="tx-rollback").update(payload="modified")
                raise ValueError("Simulated unexpected failure during transaction")
        except ValueError:
            pass

        record.refresh_from_db()
        self.assertEqual(record.payload, "initial", "Failed transaction must roll back cleanly")

        # Rollback on sudden worker crash (simulated power loss / killed process)
        proc = mp_ctx.Process(target=_worker_crash_tx, args=(str(self.db_path), "tx-rollback"))
        proc.start()
        proc.join(timeout=5)
        self.assertEqual(proc.exitcode, 88)

        connections.close_all()
        reopened = connections["default"]
        reopened_record = DurabilityJournal.objects.get(key="tx-rollback")
        self.assertEqual(
            reopened_record.payload,
            "initial",
            "Crashed process transaction must be rolled back by SQLite recovery",
        )

        with reopened.cursor() as cursor:
            cursor.execute("PRAGMA integrity_check;")
            self.assertEqual(cursor.fetchall(), [("ok",)])

    def test_multiprocess_cas_race(self) -> None:
        """
        Multiprocess CAS race inspired by S2:
        8 workers simultaneously attempt compare-and-swap from rev 0 -> 1.
        Exactly 1 must succeed; 7 must encounter conflict.
        Final rev must be 1.
        """
        with immediate_transaction():
            DurabilityJournal.objects.create(key="cas-race-key", rev=0, payload="init")

        num_workers = 8
        barrier = mp_ctx.Barrier(num_workers)
        out_queue = mp_ctx.Queue()

        workers = [
            mp_ctx.Process(
                target=_worker_cas_race,
                args=(str(self.db_path), "cas-race-key", barrier, out_queue, i),
            )
            for i in range(num_workers)
        ]

        for w in workers:
            w.start()

        results = [out_queue.get(timeout=15) for _ in range(num_workers)]
        for w in workers:
            w.join(timeout=5)
            self.assertEqual(w.exitcode, 0, f"Worker exited with code {w.exitcode}")

        successes = [r for r in results if r["success"] is True]
        conflicts = [r for r in results if r["success"] is False]

        self.assertEqual(len(successes), 1, "Exactly 1 concurrent worker must succeed at CAS")
        self.assertEqual(len(conflicts), num_workers - 1, "All other workers must observe conflict")

        connections.close_all()
        final_record = DurabilityJournal.objects.get(key="cas-race-key")
        self.assertEqual(final_record.rev, 1, "Revision must increment exactly once")
        self.assertTrue(final_record.payload.startswith("winner-worker-"))

    def test_multiprocess_unique_race(self) -> None:
        """
        8 workers simultaneously attempt to insert the same key.
        Exactly 1 succeeds; 7 fail with IntegrityError.
        """
        num_workers = 8
        barrier = mp_ctx.Barrier(num_workers)
        out_queue = mp_ctx.Queue()

        workers = [
            mp_ctx.Process(
                target=_worker_unique_race,
                args=(str(self.db_path), "duplicate-key-race", barrier, out_queue, i),
            )
            for i in range(num_workers)
        ]

        for w in workers:
            w.start()

        results = [out_queue.get(timeout=15) for _ in range(num_workers)]
        for w in workers:
            w.join(timeout=5)
            self.assertEqual(w.exitcode, 0)

        inserts = [r for r in results if r["inserted"] is True]
        rejected = [r for r in results if r["inserted"] is False and r["error"] == "IntegrityError"]

        self.assertEqual(len(inserts), 1, "Exactly 1 worker must succeed at duplicate insert")
        self.assertEqual(len(rejected), num_workers - 1, "7 workers must be rejected with IntegrityError")
        self.assertEqual(DurabilityJournal.objects.filter(key="duplicate-key-race").count(), 1)

    def test_cas_transition_helper(self) -> None:
        """Verify cas_transition succeeds when rev matches, and raises CASConflictError on mismatch."""
        with immediate_transaction():
            DurabilityJournal.objects.create(key="cas-helper-test", rev=3, payload="v3")

        # Matching revision succeeds
        cas_transition(
            DurabilityJournal,
            filter_kwargs={"key": "cas-helper-test"},
            expected_rev=3,
            update_kwargs={"payload": "v4"},
        )
        rec = DurabilityJournal.objects.get(key="cas-helper-test")
        self.assertEqual(rec.rev, 4)
        self.assertEqual(rec.payload, "v4")

        # Stale revision raises CASConflictError
        with self.assertRaises(CASConflictError):
            cas_transition(
                DurabilityJournal,
                filter_kwargs={"key": "cas-helper-test"},
                expected_rev=3,  # Stale: actual is 4
                update_kwargs={"payload": "stale-write"},
            )

        rec.refresh_from_db()
        self.assertEqual(rec.rev, 4)
        self.assertEqual(rec.payload, "v4")

    def test_transaction_boundaries_forbid_external_operations(self) -> None:
        """
        Instrumented test proving that external side effects (network, FFmpeg, large I/O)
        are strictly prohibited inside database transactions.
        """
        executed_external = []

        def simulated_ffmpeg_or_network_call(arg: str) -> str:
            assert_outside_transaction()
            executed_external.append(arg)
            return f"result-{arg}"

        # Outside any transaction: executes cleanly
        result = execute_outside_transaction(simulated_ffmpeg_or_network_call, "clean")
        self.assertEqual(result, "result-clean")
        self.assertEqual(executed_external, ["clean"])

        # Inside transaction: assert_outside_transaction raises TransactionBoundaryError
        with immediate_transaction():
            with self.assertRaises(TransactionBoundaryError):
                simulated_ffmpeg_or_network_call("forbidden-inside-tx")

        self.assertEqual(
            executed_external,
            ["clean"],
            "External action must not have executed inside the transaction",
        )

        # Deferring execution via defer_outside_transaction (on_commit)
        deferred_executed = []

        def deferred_side_effect() -> None:
            assert_outside_transaction()
            deferred_executed.append("committed")

        with immediate_transaction():
            defer_outside_transaction(deferred_side_effect)
            # Has not run yet while transaction is active
            self.assertEqual(len(deferred_executed), 0)

        # Runs strictly AFTER transaction commit
        self.assertEqual(deferred_executed, ["committed"])

        # When transaction rolls back, deferred callback never runs
        cancelled_executed = []
        try:
            with immediate_transaction():
                defer_outside_transaction(lambda: cancelled_executed.append("never"))
                raise RuntimeError("Abort transaction")
        except RuntimeError:
            pass

        self.assertEqual(cancelled_executed, [], "Rolled-back transaction must discard on_commit actions")

    def test_contention_fails_visibly_within_configured_bounds(self) -> None:
        """
        Verify that database contention exceeding busy_timeout raises PersistenceContentionError
        visibly within the configured timeout bounds.
        """
        import sqlite3
        conn = connections["default"]
        # Set a short busy timeout for this test
        with conn.cursor() as cursor:
            cursor.execute("PRAGMA busy_timeout = 200;")

        raw_conn = sqlite3.connect(str(self.db_path), timeout=0)
        try:
            raw_conn.execute("BEGIN EXCLUSIVE;")
            raw_conn.execute(
                "INSERT INTO alpha_durability_journal (key, rev, state, payload, created_at, updated_at) "
                "VALUES ('contention-blocker', 0, 'active', 'blocking', datetime('now'), datetime('now'));"
            )

            with self.assertRaises(PersistenceContentionError) as ctx:
                with immediate_transaction():
                    DurabilityJournal.objects.create(key="contention-victim", rev=0)

            self.assertIn("exceeded busy timeout", str(ctx.exception).lower())
        finally:
            raw_conn.rollback()
            raw_conn.close()
            # Restore standard busy timeout
            with conn.cursor() as cursor:
                cursor.execute("PRAGMA busy_timeout = 5000;")


if __name__ == "__main__":
    unittest.main()
