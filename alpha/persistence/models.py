"""Durable persistence models establishing relational constraints and CAS support."""
from django.db import models


class DurabilityJournal(models.Model):
    """
    Core persistence record establishing versioning, CAS semantics,
    and integrity constraints in SQLite.
    """
    key = models.CharField(max_length=128, unique=True)
    rev = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=64, default="active")
    payload = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "alpha"
        db_table = "alpha_durability_journal"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rev__gte=0),
                name="durability_journal_rev_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"DurabilityJournal(key={self.key}, rev={self.rev}, state={self.state})"


class DurabilityChild(models.Model):
    """
    Child record with strict foreign key reference to DurabilityJournal,
    demonstrating SQLite foreign key constraint enforcement.
    """
    journal = models.ForeignKey(
        DurabilityJournal,
        on_delete=models.CASCADE,
        related_name="children",
    )
    name = models.CharField(max_length=128)

    class Meta:
        app_label = "alpha"
        db_table = "alpha_durability_child"
        constraints = [
            models.UniqueConstraint(
                fields=["journal", "name"],
                name="durability_unique_journal_child_name",
            ),
        ]

    def __str__(self) -> str:
        return f"DurabilityChild(journal_id={self.journal_id}, name={self.name})"
