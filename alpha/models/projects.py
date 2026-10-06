"""Project, original input, and lifecycle models."""
import hashlib
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class InputMode(models.TextChoices):
    TOPIC = "TOPIC", "Topic Prompt"
    PASTED_SCRIPT = "PASTED_SCRIPT", "Pasted Script"


class LifecycleState(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RENDERING = "RENDERING", "Rendering"
    DELETED = "DELETED", "Soft Deleted"
    PURGED = "PURGED", "Purged"


class VisualStyle(models.TextChoices):
    MINIMAL_ILLUSTRATION = "MINIMAL_ILLUSTRATION", "Minimal Illustration"
    STORYBOOK = "STORYBOOK", "Storybook"
    DOCUMENTARY_ILLUSTRATION = "DOCUMENTARY_ILLUSTRATION", "Documentary Illustration"


# Project domain exceptions
class ProjectDomainError(Exception):
    """Base exception for project domain errors."""
    pass


class ProjectNotFoundError(ProjectDomainError):
    """Raised when a requested project does not exist."""
    pass


class ProjectAccessDeniedError(ProjectDomainError):
    """Raised when a user attempts to access an isolated project they do not own."""
    pass


class ContentMutationLockedError(ProjectDomainError):
    """Raised when content modification is attempted while a render lock or operation is active."""
    pass


class ProjectOperationInProgressError(ProjectDomainError):
    """Raised when an operation (like deletion) is attempted during active generation/rendering."""
    pass


class ProjectDeletedError(ProjectDomainError):
    """Raised when an edit is attempted on a deleted project."""
    pass


class RetentionWindowExpiredError(ProjectDomainError):
    """Raised when attempting to restore a project past its 7-day retention deadline."""
    pass


class ImmutableOriginalInputError(ProjectDomainError):
    """Raised when attempting to modify an immutable OriginalInput record."""
    pass


class Project(models.Model):
    """
    Project root entity representing an editable production owned by a user.
    Maintains revision counters for CAS concurrency and enforces render locking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    creation_token = models.CharField(max_length=128, db_index=True)
    title = models.CharField(max_length=255)
    rev = models.IntegerField(default=1)

    lifecycle_state = models.CharField(
        max_length=32,
        choices=LifecycleState.choices,
        default=LifecycleState.ACTIVE,
    )
    input_mode = models.CharField(
        max_length=32,
        choices=InputMode.choices,
        default=InputMode.TOPIC,
    )

    # Creative controls and frozen defaults:
    # 5-minute topic, Minimal Illustration, English, captions on, motion on, music off
    target_duration_seconds = models.IntegerField(default=300)
    target_language = models.CharField(max_length=16, default="en")
    visual_style = models.CharField(
        max_length=64,
        choices=VisualStyle.choices,
        default=VisualStyle.MINIMAL_ILLUSTRATION,
    )
    captions_enabled = models.BooleanField(default=True)
    motion_enabled = models.BooleanField(default=True)
    music_enabled = models.BooleanField(default=False)
    voice_id = models.CharField(max_length=64, blank=True, default="")

    # Render locking & content-mutation guard
    render_locked = models.BooleanField(default=False)
    current_render_lock_id = models.CharField(max_length=128, blank=True, null=True)

    # Deletion & retention metadata
    deleted_at = models.DateTimeField(null=True, blank=True)
    retention_deadline = models.DateTimeField(null=True, blank=True)

    # Storage attribution
    storage_bytes = models.BigIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "creation_token"],
                name="unique_user_project_creation_token",
            ),
            models.CheckConstraint(
                condition=models.Q(rev__gte=1),
                name="check_project_rev_gte_1",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Project({self.id}, title={self.title!r}, rev={self.rev}, state={self.lifecycle_state})"

    def is_content_mutation_allowed(self) -> bool:
        """
        Check whether project content can be modified.
        Prohibited while render lock is active or when project is not ACTIVE.
        """
        if self.render_locked or self.lifecycle_state != LifecycleState.ACTIVE:
            return False
        return True


class OriginalInput(models.Model):
    """
    Immutable submitted topic or pasted-script snapshot.
    Preserved byte- and word-faithful independently of downstream script adaptations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="original_input",
    )
    input_mode = models.CharField(max_length=32, choices=InputMode.choices)
    raw_text = models.TextField()
    input_language = models.CharField(max_length=16, default="en")

    word_count = models.IntegerField()
    byte_count = models.IntegerField()
    content_sha256 = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"OriginalInput(project_id={self.project_id}, mode={self.input_mode}, words={self.word_count})"

    def save(self, *args, **kwargs) -> None:
        """Enforce strict immutability: once created, updates are strictly forbidden."""
        if self.pk and OriginalInput.objects.filter(pk=self.pk).exists():
            raise ImmutableOriginalInputError(
                f"OriginalInput {self.pk} is immutable and cannot be updated."
            )

        # Compute counts and hash on initial save if not set
        if not self.content_sha256:
            text_bytes = self.raw_text.encode("utf-8")
            self.byte_count = len(text_bytes)
            self.word_count = len(self.raw_text.split())
            self.content_sha256 = hashlib.sha256(text_bytes).hexdigest()

        super().save(*args, **kwargs)
