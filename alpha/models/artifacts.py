"""Typed artifact models, shared immutable version envelope, and slot state axes."""
import hashlib
import json
import re
import uuid
from typing import Any, Dict, Optional

from django.db import models

from alpha.models.projects import Project, ProjectDomainError
from alpha.models.scenes import Scene, SceneNarrationVersion
from alpha.models.scripts import ScriptVersion


class ArtifactDomainError(ProjectDomainError):
    """Base exception for artifact and version envelope domain errors."""
    pass


class ImmutableArtifactVersionError(ArtifactDomainError):
    """Raised when an update to an existing ArtifactVersion is attempted."""
    pass


class CrossProjectArtifactReferenceError(ArtifactDomainError):
    """Raised when an artifact references an entity belonging to another project or scene."""
    pass


class InvalidArtifactPayloadError(ArtifactDomainError):
    """Raised when an artifact payload fails type, schema, or media boundary validation."""
    pass


class InvalidArtifactSelectionError(ArtifactDomainError):
    """Raised when an attempt to select an incompatible, cross-project, or invalid version occurs."""
    pass


class ArtifactVersionNotFoundError(ArtifactDomainError):
    """Raised when a requested artifact version is not found."""
    pass


class ArtifactSlotNotFoundError(ArtifactDomainError):
    """Raised when a requested artifact slot is not found."""
    pass


class ArtifactKind(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    AUDIO = "AUDIO", "Audio"
    TIMING = "TIMING", "Timing"
    CAPTION = "CAPTION", "Caption"


class ArtifactSourceType(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    EDITED = "EDITED", "User Edited"
    UPLOADED = "UPLOADED", "User Uploaded"
    RESTORED = "RESTORED", "Restored Version"


class GenerationOutcome(models.TextChoices):
    SUCCEEDED = "SUCCEEDED", "Succeeded"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
    UNCERTAIN = "UNCERTAIN", "Uncertain"


class SlotOutcome(models.TextChoices):
    NONE = "NONE", "No Attempt"
    SUCCEEDED = "SUCCEEDED", "Succeeded"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
    UNCERTAIN = "UNCERTAIN", "Uncertain"


SHA256_HEX_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def compute_canonical_json_hash(data: Any) -> str:
    """Compute deterministic SHA-256 hash over canonical JSON representation."""
    canonical_bytes = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(canonical_bytes).hexdigest()


class ArtifactVersion(models.Model):
    """
    Immutable typed artifact version with shared provenance and version envelope.
    Binary media stays outside SQLite (stored via opaque logical storage_key and byte_hash).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="artifact_versions",
    )
    scene = models.ForeignKey(
        Scene,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="artifact_versions",
    )
    kind = models.CharField(
        max_length=32,
        choices=ArtifactKind.choices,
        db_index=True,
    )
    version_number = models.IntegerField()
    source_type = models.CharField(
        max_length=32,
        choices=ArtifactSourceType.choices,
        default=ArtifactSourceType.GENERATED,
    )

    # Binary media reference fields (binary bytes stay outside SQLite)
    storage_key = models.CharField(max_length=512, blank=True, default="")
    byte_hash = models.CharField(max_length=64, blank=True, default="")
    byte_count = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=128, blank=True, default="")

    # Small structured payload fields (e.g. TIMING alignments, CAPTION cues)
    structured_payload = models.JSONField(null=True, blank=True)
    payload_schema_version = models.IntegerField(default=1)

    # Exact source-version references
    source_script_version = models.ForeignKey(
        ScriptVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="derived_artifacts",
    )
    source_narration_version = models.ForeignKey(
        SceneNarrationVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="derived_artifacts",
    )
    pinned_source_versions = models.JSONField(default=dict)

    # Model and configuration tracking
    provider = models.CharField(max_length=64, blank=True, default="")
    model = models.CharField(max_length=128, blank=True, default="")
    effective_config = models.JSONField(default=dict)
    effective_config_signature = models.CharField(max_length=64, blank=True, default="")

    # Validation and technical checks
    is_valid = models.BooleanField(default=True)
    validation_metadata = models.JSONField(default=dict)

    # Generation outcome & execution identifiers
    operation_id = models.CharField(max_length=64, blank=True, default="")
    attempt_id = models.CharField(max_length=64, blank=True, default="")
    generation_outcome = models.CharField(
        max_length=32,
        choices=GenerationOutcome.choices,
        default=GenerationOutcome.SUCCEEDED,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(version_number__gte=1),
                name="check_artifact_version_gte_1",
            ),
            models.UniqueConstraint(
                fields=["project", "scene", "kind", "version_number"],
                condition=models.Q(scene__isnull=False),
                name="unique_scene_artifact_version",
            ),
            models.UniqueConstraint(
                fields=["project", "kind", "version_number"],
                condition=models.Q(scene__isnull=True),
                name="unique_project_artifact_version",
            ),
        ]
        ordering = ["project", "scene", "kind", "-version_number"]

    def __str__(self) -> str:
        scope = f"scene={self.scene_id}" if self.scene_id else f"proj={self.project_id}"
        return f"ArtifactVersion({self.kind}, v={self.version_number}, {scope}, valid={self.is_valid})"

    def clean(self) -> None:
        """Validate typed payload constraints, cross-owner integrity, and immutable envelope."""
        # 1. Generation failure invariant: Generation failures do not create selectable valid versions
        if self.generation_outcome != GenerationOutcome.SUCCEEDED and self.is_valid:
            raise InvalidArtifactPayloadError(
                f"Generation outcome '{self.generation_outcome}' cannot create a valid artifact version; "
                "generation failures do not create selectable valid versions."
            )

        # 2. Cross-owner and cross-project checks
        if self.scene and self.scene.project_id != self.project_id:
            raise CrossProjectArtifactReferenceError(
                f"Scene {self.scene_id} belongs to project {self.scene.project_id}, not {self.project_id}."
            )
        if self.source_script_version and self.source_script_version.project_id != self.project_id:
            raise CrossProjectArtifactReferenceError(
                f"Source script version {self.source_script_version_id} belongs to project "
                f"{self.source_script_version.project_id}, not {self.project_id}."
            )
        if self.source_narration_version:
            if self.source_narration_version.scene.project_id != self.project_id:
                raise CrossProjectArtifactReferenceError(
                    f"Source narration version {self.source_narration_version_id} belongs to project "
                    f"{self.source_narration_version.scene.project_id}, not {self.project_id}."
                )
            if self.scene and self.source_narration_version.scene_id != self.scene_id:
                raise CrossProjectArtifactReferenceError(
                    f"Source narration version {self.source_narration_version_id} belongs to scene "
                    f"{self.source_narration_version.scene_id}, not {self.scene_id}."
                )

        # 3. Typed payload validation
        if self.kind in (ArtifactKind.IMAGE, ArtifactKind.AUDIO):
            # Binary media must stay outside SQLite
            if self.structured_payload is not None:
                raise InvalidArtifactPayloadError(
                    f"{self.kind} binary media must not store binary or structured payloads directly in SQLite."
                )
            if self.is_valid or self.storage_key:
                if not self.storage_key:
                    raise InvalidArtifactPayloadError(f"{self.kind} artifact requires a valid external storage_key.")
                if not self.byte_hash or not SHA256_HEX_RE.match(self.byte_hash):
                    raise InvalidArtifactPayloadError(f"{self.kind} artifact requires a 64-hex SHA-256 byte_hash.")
                if self.byte_count <= 0:
                    raise InvalidArtifactPayloadError(f"{self.kind} artifact byte_count must be > 0.")

            if self.kind == ArtifactKind.IMAGE and (self.is_valid or self.storage_key):
                if not self.mime_type.startswith("image/"):
                    raise InvalidArtifactPayloadError(
                        f"IMAGE mime_type must start with 'image/', got '{self.mime_type}'."
                    )
                width = self.validation_metadata.get("width")
                height = self.validation_metadata.get("height")
                if not isinstance(width, int) or width <= 0 or not isinstance(height, int) or height <= 0:
                    raise InvalidArtifactPayloadError(
                        "IMAGE validation_metadata must contain positive integer 'width' and 'height'."
                    )
            elif self.kind == ArtifactKind.AUDIO:
                if not self.mime_type.startswith("audio/"):
                    raise InvalidArtifactPayloadError(
                        f"AUDIO mime_type must start with 'audio/', got '{self.mime_type}'."
                    )
                duration_ms = self.validation_metadata.get("duration_ms")
                if not isinstance(duration_ms, (int, float)) or duration_ms <= 0:
                    raise InvalidArtifactPayloadError(
                        "AUDIO validation_metadata must contain positive 'duration_ms'."
                    )

        elif self.kind == ArtifactKind.TIMING:
            if not isinstance(self.structured_payload, dict):
                raise InvalidArtifactPayloadError("TIMING artifact requires a structured_payload dictionary.")
            words = self.structured_payload.get("words")
            if not isinstance(words, list):
                raise InvalidArtifactPayloadError("TIMING payload must include a 'words' list.")
            prev_end = 0
            for item in words:
                if not isinstance(item, dict):
                    raise InvalidArtifactPayloadError("Each word entry in TIMING payload must be a dictionary.")
                start_ms = item.get("start_ms")
                end_ms = item.get("end_ms")
                if not isinstance(start_ms, (int, float)) or start_ms < 0:
                    raise InvalidArtifactPayloadError("TIMING start_ms must be non-negative.")
                if not isinstance(end_ms, (int, float)) or end_ms < start_ms:
                    raise InvalidArtifactPayloadError("TIMING end_ms must be >= start_ms.")
                prev_end = max(prev_end, end_ms)

            # Auto-compute byte_hash if not provided
            if not self.byte_hash:
                self.byte_hash = compute_canonical_json_hash(self.structured_payload)
            if self.byte_count <= 0:
                self.byte_count = len(json.dumps(self.structured_payload).encode("utf-8"))

        elif self.kind == ArtifactKind.CAPTION:
            if not isinstance(self.structured_payload, dict):
                raise InvalidArtifactPayloadError("CAPTION artifact requires a structured_payload dictionary.")
            cues = self.structured_payload.get("cues")
            if not isinstance(cues, list):
                raise InvalidArtifactPayloadError("CAPTION payload must include a 'cues' list.")
            for cue in cues:
                if not isinstance(cue, dict):
                    raise InvalidArtifactPayloadError("Each cue entry in CAPTION payload must be a dictionary.")
                text = cue.get("text")
                start_ms = cue.get("start_ms")
                end_ms = cue.get("end_ms")
                if not isinstance(text, str) or not text.strip():
                    raise InvalidArtifactPayloadError("CAPTION cue text must be a non-empty string.")
                if not isinstance(start_ms, (int, float)) or start_ms < 0:
                    raise InvalidArtifactPayloadError("CAPTION cue start_ms must be non-negative.")
                if not isinstance(end_ms, (int, float)) or end_ms < start_ms:
                    raise InvalidArtifactPayloadError("CAPTION cue end_ms must be >= start_ms.")

            # Auto-compute byte_hash if not provided
            if not self.byte_hash:
                self.byte_hash = compute_canonical_json_hash(self.structured_payload)
            if self.byte_count <= 0:
                self.byte_count = len(json.dumps(self.structured_payload).encode("utf-8"))

        # 3. Effective config signature
        if self.effective_config and not self.effective_config_signature:
            self.effective_config_signature = compute_canonical_json_hash(self.effective_config)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Enforce strict immutability once persisted and validate domain constraints."""
        if self.pk and ArtifactVersion.objects.filter(pk=self.pk).exists():
            raise ImmutableArtifactVersionError(
                f"ArtifactVersion {self.pk} is immutable and cannot be updated."
            )
        self.clean()
        super().save(*args, **kwargs)


class ArtifactSlot(models.Model):
    """
    Stable typed content/asset slot scoped to a project or scene.
    Maintains 4 independent orthogonal state axes:
    1. Valid: Selected version passed technical checks (ArtifactVersion.is_valid).
    2. Selected: Currently selected version (selected_version FK or None).
    3. Compatible/Outdated: Input compatibility state (is_compatible bool).
    4. Review Needed: Semantic/override review flag (needs_review bool + reason).
    Additionally records last attempt outcome without overwriting selected good content.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="artifact_slots",
    )
    scene = models.ForeignKey(
        Scene,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="artifact_slots",
    )
    kind = models.CharField(
        max_length=32,
        choices=ArtifactKind.choices,
        db_index=True,
    )
    slot_key = models.CharField(max_length=64, default="default")

    # Axis 1 & 2: Selected version (must be valid)
    selected_version = models.ForeignKey(
        ArtifactVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_in_slots",
    )

    # Axis 3: Compatible / Outdated
    is_compatible = models.BooleanField(default=True)

    # Axis 4: Review Needed
    needs_review = models.BooleanField(default=False)
    review_reason = models.CharField(max_length=255, blank=True, default="")

    # Separate generation attempt history axis
    last_attempt_outcome = models.CharField(
        max_length=32,
        choices=SlotOutcome.choices,
        default=SlotOutcome.NONE,
    )
    last_attempt_id = models.CharField(max_length=64, blank=True, default="")
    last_attempt_error = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "scene", "kind", "slot_key"],
                condition=models.Q(scene__isnull=False),
                name="unique_scene_artifact_slot",
            ),
            models.UniqueConstraint(
                fields=["project", "kind", "slot_key"],
                condition=models.Q(scene__isnull=True),
                name="unique_project_artifact_slot",
            ),
        ]
        ordering = ["project", "scene", "kind", "slot_key"]

    def __str__(self) -> str:
        scope = f"scene={self.scene_id}" if self.scene_id else f"proj={self.project_id}"
        sel = f"v={self.selected_version.version_number}" if self.selected_version else "none"
        return f"ArtifactSlot({self.kind}:{self.slot_key}, {scope}, selected={sel}, comp={self.is_compatible})"

    def clean(self) -> None:
        """Validate cross-owner integrity and selection invariants."""
        if self.scene and self.scene.project_id != self.project_id:
            raise CrossProjectArtifactReferenceError(
                f"Scene {self.scene_id} belongs to project {self.scene.project_id}, not {self.project_id}."
            )
        if self.selected_version:
            if self.selected_version.project_id != self.project_id:
                raise CrossProjectArtifactReferenceError(
                    f"Selected version {self.selected_version_id} belongs to project "
                    f"{self.selected_version.project_id}, not {self.project_id}."
                )
            if self.selected_version.kind != self.kind:
                raise InvalidArtifactSelectionError(
                    f"Slot kind is {self.kind}, cannot select version of kind {self.selected_version.kind}."
                )
            if self.selected_version.scene_id != self.scene_id:
                raise CrossProjectArtifactReferenceError(
                    f"Selected version {self.selected_version_id} scope (scene={self.selected_version.scene_id}) "
                    f"does not match slot scope (scene={self.scene_id})."
                )
            if not self.selected_version.is_valid or self.selected_version.generation_outcome != GenerationOutcome.SUCCEEDED:
                raise InvalidArtifactSelectionError(
                    f"ArtifactVersion {self.selected_version_id} is not valid or did not succeed; "
                    "generation failures cannot create selectable versions."
                )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.clean()
        super().save(*args, **kwargs)


class ArtifactAttempt(models.Model):
    """
    Execution attempt record for an artifact slot.
    Preserves diagnostic outcome, failure reason, and provenance without modifying valid selections.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slot = models.ForeignKey(
        ArtifactSlot,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="artifact_attempts",
    )
    attempt_id = models.CharField(max_length=64)
    outcome = models.CharField(
        max_length=32,
        choices=GenerationOutcome.choices,
    )
    error_message = models.TextField(blank=True, default="")
    diagnostic_data = models.JSONField(default=dict)

    # Provider & config provenance
    provider = models.CharField(max_length=64, blank=True, default="")
    model = models.CharField(max_length=128, blank=True, default="")
    effective_config = models.JSONField(default=dict)
    pinned_source_versions = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slot", "-created_at"]

    def __str__(self) -> str:
        return f"ArtifactAttempt({self.attempt_id}, slot={self.slot_id}, outcome={self.outcome})"

    def clean(self) -> None:
        if self.slot.project_id != self.project_id:
            raise CrossProjectArtifactReferenceError(
                f"Slot project {self.slot.project_id} does not match attempt project {self.project_id}."
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.clean()
        super().save(*args, **kwargs)
