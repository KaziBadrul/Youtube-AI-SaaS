"""Artifact service layer: version persistence, slot management, and attempt tracking."""
from typing import Any, Dict, Optional
import uuid

from django.db import models, transaction

from alpha.models.artifacts import (
    ArtifactAttempt,
    ArtifactDomainError,
    ArtifactKind,
    ArtifactSlot,
    ArtifactSlotNotFoundError,
    ArtifactSourceType,
    ArtifactVersion,
    ArtifactVersionNotFoundError,
    CrossProjectArtifactReferenceError,
    GenerationOutcome,
    InvalidArtifactPayloadError,
    InvalidArtifactSelectionError,
    SlotOutcome,
    compute_canonical_json_hash,
)
from alpha.models.projects import Project
from alpha.models.scenes import Scene, SceneNarrationVersion
from alpha.models.scripts import ScriptVersion


@transaction.atomic
def create_artifact_version(
    project: Project,
    kind: str,
    scene: Optional[Scene] = None,
    version_number: Optional[int] = None,
    source_type: str = ArtifactSourceType.GENERATED,
    storage_key: str = "",
    byte_hash: str = "",
    byte_count: int = 0,
    mime_type: str = "",
    structured_payload: Optional[Dict[str, Any]] = None,
    payload_schema_version: int = 1,
    source_script_version: Optional[ScriptVersion] = None,
    source_narration_version: Optional[SceneNarrationVersion] = None,
    pinned_source_versions: Optional[Dict[str, Any]] = None,
    provider: str = "",
    model: str = "",
    effective_config: Optional[Dict[str, Any]] = None,
    effective_config_signature: str = "",
    is_valid: Optional[bool] = None,
    validation_metadata: Optional[Dict[str, Any]] = None,
    operation_id: str = "",
    attempt_id: str = "",
    generation_outcome: str = GenerationOutcome.SUCCEEDED,
) -> ArtifactVersion:
    """
    Persist an immutable typed ArtifactVersion.
    If version_number is not provided, it is automatically computed as next monotonic integer.
    """
    if is_valid is None:
        is_valid = (generation_outcome == GenerationOutcome.SUCCEEDED)
    if version_number is None:
        qs = ArtifactVersion.objects.filter(project=project, kind=kind)
        if scene is not None:
            qs = qs.filter(scene=scene)
        else:
            qs = qs.filter(scene__isnull=True)
        max_ver = qs.aggregate(m=models.Max("version_number"))["m"] or 0
        version_number = max_ver + 1

    version = ArtifactVersion(
        project=project,
        scene=scene,
        kind=kind,
        version_number=version_number,
        source_type=source_type,
        storage_key=storage_key,
        byte_hash=byte_hash,
        byte_count=byte_count,
        mime_type=mime_type,
        structured_payload=structured_payload,
        payload_schema_version=payload_schema_version,
        source_script_version=source_script_version,
        source_narration_version=source_narration_version,
        pinned_source_versions=pinned_source_versions or {},
        provider=provider,
        model=model,
        effective_config=effective_config or {},
        effective_config_signature=effective_config_signature,
        is_valid=is_valid,
        validation_metadata=validation_metadata or {},
        operation_id=operation_id,
        attempt_id=attempt_id,
        generation_outcome=generation_outcome,
    )
    version.save()
    return version


@transaction.atomic
def get_or_create_artifact_slot(
    project: Project,
    kind: str,
    scene: Optional[Scene] = None,
    slot_key: str = "default",
) -> ArtifactSlot:
    """Retrieve or create an ArtifactSlot scoped to project (and optionally scene)."""
    if scene is not None and scene.project_id != project.id:
        raise CrossProjectArtifactReferenceError(
            f"Scene {scene.id} belongs to project {scene.project_id}, not {project.id}."
        )

    slot, _ = ArtifactSlot.objects.get_or_create(
        project=project,
        scene=scene,
        kind=kind,
        slot_key=slot_key,
    )
    return slot


@transaction.atomic
def select_artifact_version(
    slot: ArtifactSlot,
    version: Optional[ArtifactVersion],
) -> ArtifactSlot:
    """
    Select an artifact version into a slot.
    Passing None clears the current selection without deleting prior versions.
    """
    if version is not None:
        if version.project_id != slot.project_id:
            raise CrossProjectArtifactReferenceError("Cannot select artifact version from another project.")
        if version.kind != slot.kind:
            raise InvalidArtifactSelectionError(
                f"Cannot select version of kind {version.kind} into slot of kind {slot.kind}."
            )
        if version.scene_id != slot.scene_id:
            raise CrossProjectArtifactReferenceError(
                "Cannot select artifact version belonging to a different scene or project scope into this slot."
            )
        if not version.is_valid or version.generation_outcome != GenerationOutcome.SUCCEEDED:
            raise InvalidArtifactSelectionError(
                f"ArtifactVersion {version.id} is invalid or non-succeeded and cannot be selected."
            )

    slot.selected_version = version
    slot.save()
    return slot


@transaction.atomic
def record_generation_attempt(
    slot: ArtifactSlot,
    attempt_id: str,
    outcome: str,
    error_message: str = "",
    diagnostic_data: Optional[Dict[str, Any]] = None,
    provider: str = "",
    model: str = "",
    effective_config: Optional[Dict[str, Any]] = None,
    pinned_source_versions: Optional[Dict[str, Any]] = None,
    resulting_version: Optional[ArtifactVersion] = None,
    select_on_success: bool = True,
) -> ArtifactAttempt:
    """
    Record an execution attempt for a slot.
    If outcome is FAILED, CANCELLED, or UNCERTAIN, the slot's prior valid selection is preserved.
    """
    attempt = ArtifactAttempt.objects.create(
        slot=slot,
        project=slot.project,
        attempt_id=attempt_id,
        outcome=outcome,
        error_message=error_message,
        diagnostic_data=diagnostic_data or {},
        provider=provider,
        model=model,
        effective_config=effective_config or {},
        pinned_source_versions=pinned_source_versions or {},
    )

    slot.last_attempt_outcome = outcome
    slot.last_attempt_id = attempt_id
    slot.last_attempt_error = error_message

    if outcome == GenerationOutcome.SUCCEEDED and resulting_version is not None and select_on_success:
        select_artifact_version(slot, resulting_version)
    else:
        slot.save()

    return attempt


@transaction.atomic
def set_slot_compatibility(slot: ArtifactSlot, is_compatible: bool) -> ArtifactSlot:
    """Set the compatible/outdated state axis of an artifact slot."""
    slot.is_compatible = is_compatible
    slot.save(update_fields=["is_compatible", "updated_at"])
    return slot


@transaction.atomic
def set_slot_review_needed(
    slot: ArtifactSlot,
    needs_review: bool,
    reason: str = "",
) -> ArtifactSlot:
    """Set the review-needed state axis and reason of an artifact slot."""
    slot.needs_review = needs_review
    slot.review_reason = reason if needs_review else ""
    slot.save(update_fields=["needs_review", "review_reason", "updated_at"])
    return slot


def get_artifact_slot(
    project: Project,
    kind: str,
    scene: Optional[Scene] = None,
    slot_key: str = "default",
) -> ArtifactSlot:
    """Retrieve an artifact slot or raise ArtifactSlotNotFoundError."""
    try:
        return ArtifactSlot.objects.get(
            project=project,
            scene=scene,
            kind=kind,
            slot_key=slot_key,
        )
    except ArtifactSlot.DoesNotExist:
        raise ArtifactSlotNotFoundError(
            f"ArtifactSlot not found for project={project.id}, kind={kind}, slot_key={slot_key}."
        )


def get_artifact_version(
    project: Project,
    version_id: uuid.UUID,
) -> ArtifactVersion:
    """Retrieve an artifact version by id ensuring project ownership."""
    try:
        return ArtifactVersion.objects.get(id=version_id, project=project)
    except ArtifactVersion.DoesNotExist:
        raise ArtifactVersionNotFoundError(
            f"ArtifactVersion {version_id} not found in project {project.id}."
        )
