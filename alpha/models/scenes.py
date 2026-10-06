"""Scene models and narration version envelopes."""
import hashlib
import uuid
from typing import Any

from django.db import models

from alpha.models.projects import Project
from alpha.models.scripts import ScriptDomainError, ScriptVersion


class SceneDomainError(ScriptDomainError):
    """Base exception for scene domain errors."""
    pass


class SceneNotFoundError(SceneDomainError):
    """Raised when a requested scene is not found."""
    pass


class InvalidSceneOrderError(SceneDomainError):
    """Raised when scene reordering receives invalid or non-matching scene IDs."""
    pass


class ImmutableSceneNarrationError(SceneDomainError):
    """Raised when an update to an existing SceneNarrationVersion is attempted."""
    pass


class Scene(models.Model):
    """
    Stable project-owned scene identity independent of order, filenames, and line numbers.
    Distinguishes narration text, visual description, and generation prompt.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="scenes",
    )
    order_index = models.IntegerField(null=True, blank=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    # Source span in the script version from which this scene was decomposed
    source_script_version = models.ForeignKey(
        ScriptVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="derived_scenes",
    )
    source_start_char = models.IntegerField(default=0)
    source_end_char = models.IntegerField(default=0)

    # Distinct content fields:
    # 1. Spoken narration text
    narration_text = models.TextField()
    # 2. Plain-language visual concept / description
    visual_description = models.TextField(blank=True, default="")
    # 3. Provider-facing image generation prompt
    generation_prompt = models.TextField(blank=True, default="")

    review_flags = models.JSONField(default=dict)
    rev = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rev__gte=1),
                name="check_scene_rev_gte_1",
            ),
            models.CheckConstraint(
                condition=models.Q(source_start_char__gte=0),
                name="check_scene_start_char_gte_0",
            ),
            models.CheckConstraint(
                condition=models.Q(source_end_char__gte=models.F("source_start_char")),
                name="check_scene_end_gte_start",
            ),
        ]
        ordering = ["project", "order_index"]

    def __str__(self) -> str:
        return f"Scene({self.id}, project={self.project_id}, order={self.order_index}, rev={self.rev})"


class SceneNarrationVersion(models.Model):
    """
    Immutable historical narration text version for a scene.
    Preserves exact approved spoken words for inspection and restoration.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name="narration_versions",
    )
    version_number = models.IntegerField()
    text = models.TextField()
    content_sha256 = models.CharField(max_length=64)
    word_count = models.IntegerField()
    byte_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["scene", "version_number"],
                name="unique_scene_narration_version_number",
            ),
            models.CheckConstraint(
                condition=models.Q(version_number__gte=1),
                name="check_scene_narration_version_gte_1",
            ),
        ]
        ordering = ["scene", "-version_number"]

    def __str__(self) -> str:
        return f"SceneNarrationVersion(scene={self.scene_id}, v={self.version_number})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Enforce immutability and calculate text digest."""
        if self.pk and SceneNarrationVersion.objects.filter(pk=self.pk).exists():
            raise ImmutableSceneNarrationError(
                f"SceneNarrationVersion {self.pk} is immutable and cannot be updated."
            )
        if not self.content_sha256:
            text_bytes = self.text.encode("utf-8")
            self.byte_count = len(text_bytes)
            self.word_count = len(self.text.split())
            self.content_sha256 = hashlib.sha256(text_bytes).hexdigest()
        super().save(*args, **kwargs)
