"""Short transaction primitives for SQLite durability and exclusion."""
import contextlib
import time
from typing import Any, Callable, Generator
from django.db import DEFAULT_DB_ALIAS, transaction
from django.db.utils import OperationalError


class PersistenceContentionError(OperationalError):
    """Raised when SQLite contention exceeds configured busy handling bounds."""
    pass


class TransactionDurationWarning(RuntimeWarning):
    """Warning issued when a short transaction exceeds its expected duration budget."""
    pass


@contextlib.contextmanager
def immediate_transaction(
    using: str | None = None,
    savepoint: bool = True,
) -> Generator[None, None, None]:
    """
    Execute a short write transaction with SQLite IMMEDIATE exclusion.

    With SQLite, BEGIN IMMEDIATE acquires a RESERVED lock at the beginning
    of the transaction, ensuring concurrent writers wait up to busy_timeout
    rather than causing deferred deadlocks.
    """
    alias = using or DEFAULT_DB_ALIAS
    try:
        with transaction.atomic(using=alias, savepoint=savepoint):
            yield
    except OperationalError as exc:
        msg = str(exc).lower()
        if "database is locked" in msg or "busy" in msg:
            raise PersistenceContentionError(
                f"Database contention exceeded busy timeout on alias '{alias}': {exc}"
            ) from exc
        raise


@contextlib.contextmanager
def short_transaction(
    using: str | None = None,
    max_duration_seconds: float = 5.0,
) -> Generator[None, None, None]:
    """
    Enforce that a write transaction remains short and within budget.
    Raises PersistenceContentionError if the database is busy/locked.
    """
    start_time = time.perf_counter()
    with immediate_transaction(using=using):
        yield
    elapsed = time.perf_counter() - start_time
    if elapsed > max_duration_seconds:
        import warnings
        warnings.warn(
            f"Transaction on {using or DEFAULT_DB_ALIAS} took {elapsed:.3f}s, exceeding budget {max_duration_seconds}s",
            TransactionDurationWarning,
            stacklevel=2,
        )
