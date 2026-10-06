"""Transaction boundaries for external callbacks and operations."""
from collections.abc import Callable
from typing import Any, TypeVar
from django.db import DEFAULT_DB_ALIAS, transaction

R = TypeVar("R")


class TransactionBoundaryError(RuntimeError):
    """
    Raised when an external side effect (network call, FFmpeg execution, large
    filesystem manipulation) is attempted while holding an active database transaction.
    """
    pass


def assert_outside_transaction(using: str | None = None) -> None:
    """
    Assert that the caller is strictly outside any active database transaction.
    Raises TransactionBoundaryError if inside an atomic transaction block.
    """
    alias = using or DEFAULT_DB_ALIAS
    connection = transaction.get_connection(alias)
    if connection.in_atomic_block:
        raise TransactionBoundaryError(
            f"External operation is prohibited inside database transactions on alias '{alias}'. "
            "Network calls, FFmpeg execution, and large filesystem writes must occur outside transactions."
        )


def execute_outside_transaction(
    action: Callable[..., R],
    *args: Any,
    using: str | None = None,
    **kwargs: Any,
) -> R:
    """
    Execute an action verifying that no database transaction is currently open.
    """
    assert_outside_transaction(using=using)
    return action(*args, **kwargs)


def defer_outside_transaction(
    callback: Callable[[], Any],
    using: str | None = None,
) -> None:
    """
    Execute a callback immediately if outside a transaction, or defer execution
    via transaction.on_commit so that it runs strictly after commit has succeeded.
    """
    alias = using or DEFAULT_DB_ALIAS
    connection = transaction.get_connection(alias)
    if connection.in_atomic_block:
        transaction.on_commit(callback, using=alias)
    else:
        callback()
