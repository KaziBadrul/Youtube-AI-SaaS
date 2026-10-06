"""Compare-and-swap (CAS) and exclusion helpers for SQLite concurrency."""
from typing import Any
from django.db.models import F, Model, QuerySet
from alpha.persistence.transactions import immediate_transaction


class CASConflictError(Exception):
    """Raised when a compare-and-swap update detects a version or revision mismatch."""
    pass


def cas_update(
    queryset_or_model: type[Model] | QuerySet[Any],
    filter_kwargs: dict[str, Any],
    expected_rev: int,
    update_kwargs: dict[str, Any],
    rev_field: str = "rev",
    using: str | None = None,
) -> bool:
    """
    Atomically update a record if and only if its revision matches expected_rev.

    Increments `rev_field` by 1 and applies `update_kwargs`.
    Returns True if exactly 1 row was modified, False if revision mismatched or not found.
    """
    if isinstance(queryset_or_model, type) and issubclass(queryset_or_model, Model):
        qs = queryset_or_model.objects
    else:
        qs = queryset_or_model

    if using:
        qs = qs.using(using)

    combined_filter = dict(filter_kwargs)
    combined_filter[rev_field] = expected_rev

    combined_updates = dict(update_kwargs)
    combined_updates[rev_field] = F(rev_field) + 1

    with immediate_transaction(using=using):
        rows_affected = qs.filter(**combined_filter).update(**combined_updates)

    return rows_affected == 1


def cas_transition(
    queryset_or_model: type[Model] | QuerySet[Any],
    filter_kwargs: dict[str, Any],
    expected_rev: int,
    update_kwargs: dict[str, Any],
    rev_field: str = "rev",
    using: str | None = None,
) -> None:
    """
    Perform a compare-and-swap update; raise CASConflictError if a conflict occurs.
    """
    success = cas_update(
        queryset_or_model=queryset_or_model,
        filter_kwargs=filter_kwargs,
        expected_rev=expected_rev,
        update_kwargs=update_kwargs,
        rev_field=rev_field,
        using=using,
    )
    if not success:
        raise CASConflictError(
            f"Compare-and-swap failed for filter {filter_kwargs}: "
            f"expected {rev_field}={expected_rev} does not match current state."
        )
