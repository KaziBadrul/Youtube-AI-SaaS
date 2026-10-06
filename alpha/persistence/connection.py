"""SQLite connection durability and PRAGMA configuration."""
import sqlite3
from typing import Any
from django.db.backends.signals import connection_created


def configure_sqlite_connection(sender: Any, connection: Any, **kwargs: Any) -> None:
    """Enforce SQLite WAL, foreign keys, synchronous durability, and busy handling."""
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("PRAGMA journal_mode = WAL;")
            cursor.execute("PRAGMA synchronous = FULL;")
            cursor.execute("PRAGMA busy_timeout = 5000;")


def register_sqlite_pragmas() -> None:
    """Connect SQLite PRAGMA configuration to Django connection creation signal."""
    connection_created.connect(
        configure_sqlite_connection,
        dispatch_uid="alpha_sqlite_durability_pragmas",
    )


def get_sqlite_pragmas(connection: Any) -> dict[str, Any]:
    """Inspect and return active PRAGMA settings on the provided SQLite connection."""
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]
        cursor.execute("PRAGMA synchronous;")
        synchronous = cursor.fetchone()[0]
        cursor.execute("PRAGMA foreign_keys;")
        foreign_keys = cursor.fetchone()[0]
        cursor.execute("PRAGMA busy_timeout;")
        busy_timeout = cursor.fetchone()[0]
    return {
        "journal_mode": str(journal_mode).upper(),
        "synchronous": int(synchronous),  # 2 is FULL
        "foreign_keys": bool(foreign_keys),
        "busy_timeout": int(busy_timeout),
    }


def verify_sqlite_pragmas(connection: Any) -> bool:
    """Verify that required SQLite durability pragmas are active."""
    pragmas = get_sqlite_pragmas(connection)
    is_in_memory = (
        getattr(connection, "is_in_memory_db", lambda: False)()
        or pragmas["journal_mode"] == "MEMORY"
    )
    expected_journal = "MEMORY" if is_in_memory else "WAL"
    return (
        pragmas["foreign_keys"] is True
        and pragmas["synchronous"] >= 2  # 2 is FULL
        and pragmas["busy_timeout"] >= 5000
        and pragmas["journal_mode"] == expected_journal
    )
