"""Script version and projection models."""
import hashlib
import uuid
from typing import Any

from django.db import models

from alpha.models.projects import Project, ProjectDomainError


class ScriptDomainError(ProjectDomainError):
    """Base exception for script and projection domain errors."""
    pass


class ScriptVersionNotFoundError(ScriptDomainError):
    """Raised when a requested script version is not found."""
    pass


class MismatchedSourceVersionError(ScriptDomainError):
    """Raised when a projection or script update specifies a mismatched source version or revision."""
    pass


class InvalidSpanError(ScriptDomainError):
    """Raised when a source span does not match script text or exceeds bounds."""
    pass


class ImmutableScriptVersionError(ScriptDomainError):
    """Raised when an update to an existing ScriptVersion is attempted."""
    pass


class ScriptSourceType(models.TextChoices):
    GENERATED = "GENERATED", "Generated Script"
    EDITED = "EDITED", "User Edited Script"
    PROJECTED = "PROJECTED", "Projected From Scenes"
    FACTUAL_CORRECTION = "FACTUAL_CORRECTION", "Factual Correction"
    RESTORED = "RESTORED", "Restored Script"


class ScriptVersion(models.Model):
    """
    Immutable approved production script version scoped to a project.
    Represents whole-project script text before scene decomposition or historical snapshots.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="script_versions",
    )
    version_number = models.IntegerField()
    text = models.TextField()
    source_type = models.CharField(
        max_length=32,
        choices=ScriptSourceType.choices,
        default=ScriptSourceType.GENERATED,
    )
    content_sha256 = models.CharField(max_length=64)
    word_count = models.IntegerField()
    byte_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "version_number"],
                name="unique_project_script_version_number",
            ),
            models.CheckConstraint(
                condition=models.Q(version_number__gte=1),
                name="check_script_version_gte_1",
            ),
        ]
        ordering = ["project", "-version_number"]

    def __str__(self) -> str:
        return f"ScriptVersion(project={self.project_id}, v={self.version_number}, words={self.word_count})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Enforce strict immutability once persisted."""
        if self.pk and ScriptVersion.objects.filter(pk=self.pk).exists():
            raise ImmutableScriptVersionError(
                f"ScriptVersion {self.pk} is immutable and cannot be updated."
            )
        if not self.content_sha256:
            text_bytes = self.text.encode("utf-8")
            self.byte_count = len(text_bytes)
            self.word_count = len(self.text.split())
            self.content_sha256 = hashlib.sha256(text_bytes).hexdigest()
        super().save(*args, **kwargs)


class ScriptProjection(models.Model):
    """
    Current script projection derived deterministically from active ordered scenes' narration.
    Serves as the single source of truth for script text once scenes exist.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="script_projection",
    )
    text = models.TextField(blank=True, default="")
    content_sha256 = models.CharField(max_length=64, blank=True, default="")
    word_count = models.IntegerField(default=0)
    byte_count = models.IntegerField(default=0)
    scene_count = models.IntegerField(default=0)

    # Active ordered scene IDs and projection spans
    active_scene_ids = models.JSONField(default=list)
    scene_spans = models.JSONField(default=list)

    # Pinned source script version if initialized from an approved script
    source_script_version = models.ForeignKey(
        ScriptVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projections",
    )

    projection_rev = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(projection_rev__gte=1),
                name="check_projection_rev_gte_1",
            ),
        ]

    def __str__(self) -> str:
        return f"ScriptProjection(project={self.project_id}, scenes={self.scene_count}, rev={self.projection_rev})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Calculate counts and SHA-256 over UTF-8 text."""
        text_bytes = self.text.encode("utf-8")
        self.byte_count = len(text_bytes)
        self.word_count = len(self.text.split())
        self.content_sha256 = hashlib.sha256(text_bytes).hexdigest()
        self.scene_count = len(self.active_scene_ids)
        super().save(*args, **kwargs)
