"""Persistence primitives, SQLite connection configuration, and transaction boundaries."""
from alpha.persistence.boundaries import (
    TransactionBoundaryError,
    assert_outside_transaction,
    defer_outside_transaction,
    execute_outside_transaction,
)
from alpha.persistence.cas import (
    CASConflictError,
    cas_transition,
    cas_update,
)
from alpha.persistence.connection import (
    configure_sqlite_connection,
    get_sqlite_pragmas,
    register_sqlite_pragmas,
    verify_sqlite_pragmas,
)
from alpha.persistence.transactions import (
    PersistenceContentionError,
    immediate_transaction,
    short_transaction,
)

__all__ = [
    "configure_sqlite_connection",
    "register_sqlite_pragmas",
    "get_sqlite_pragmas",
    "verify_sqlite_pragmas",
    "immediate_transaction",
    "short_transaction",
    "PersistenceContentionError",
    "cas_update",
    "cas_transition",
    "CASConflictError",
    "TransactionBoundaryError",
    "assert_outside_transaction",
    "execute_outside_transaction",
    "defer_outside_transaction",
]
