"""Script version persistence and stable scene projection services."""
import hashlib
from typing import Any
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from alpha.models.projects import (
    ContentMutationLockedError,
    LifecycleState,
    ProjectDeletedError,
    ProjectNotFoundError,
)
from alpha.models.scenes import (
    InvalidSceneOrderError,
    Scene,
    SceneNarrationVersion,
    SceneNotFoundError,
)
from alpha.models.scripts import (
    InvalidSpanError,
    MismatchedSourceVersionError,
    ScriptDomainError,
    ScriptProjection,
    ScriptSourceType,
    ScriptVersion,
    ScriptVersionNotFoundError,
)
from alpha.persistence.transactions import immediate_transaction
from alpha.services.projects import get_project

SCENE_PROJECTION_SEPARATOR = "\n\n"


def compute_projection_payload(
    scenes: list[Scene],
    separator: str = SCENE_PROJECTION_SEPARATOR,
) -> dict[str, Any]:
    """
    Deterministically build projected script text and source span mappings
    from an ordered list of active scenes.
    """
    text_parts: list[str] = []
    spans: list[dict[str, Any]] = []
    current_offset = 0

    for scene in scenes:
        narration = scene.narration_text
        start_char = current_offset
        end_char = current_offset + len(narration)
        text_parts.append(narration)
        spans.append({
            "scene_id": str(scene.id),
            "start_char": start_char,
            "end_char": end_char,
            "narration_text": narration,
        })
        current_offset = end_char + len(separator)

    projected_text = separator.join(text_parts)
    text_bytes = projected_text.encode("utf-8")
    content_sha256 = hashlib.sha256(text_bytes).hexdigest()

    return {
        "text": projected_text,
        "content_sha256": content_sha256,
        "word_count": len(projected_text.split()),
        "byte_count": len(text_bytes),
        "scene_count": len(scenes),
        "active_scene_ids": [str(s.id) for s in scenes],
        "scene_spans": spans,
    }


def create_script_version(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    text: str,
    source_type: str = ScriptSourceType.GENERATED,
) -> ScriptVersion:
    """
    Create an immutable ScriptVersion record for a project.
    Validates server-side user ownership and project mutation locks.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot create script version for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot create script version for project {project_id}: content mutation is locked."
        )

    if not text or not text.strip():
        raise ValueError("Script version text must not be empty.")

    with immediate_transaction():
        max_ver = (
            ScriptVersion.objects.filter(project=project).aggregate(
                m=models.Max("version_number")
            )["m"]
            or 0
        )
        next_ver = max_ver + 1

        script_version = ScriptVersion.objects.create(
            project=project,
            version_number=next_ver,
            text=text,
            source_type=source_type,
        )

    return script_version


def initialize_scenes_from_script(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    script_version_id: uuid.UUID | str,
    scene_specs: list[dict[str, Any]],
    expected_projection_rev: int | None = None,
) -> tuple[ScriptProjection, list[Scene]]:
    """
    Decompose an approved script version into ordered stable Scene records
    and establish the project's current ScriptProjection atomically.

    Distinguishes narration text, visual description, and generation prompt.
    Validates source spans against script_version.text with exact char fidelity.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot initialize scenes for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot initialize scenes for project {project_id}: content mutation is locked."
        )

    try:
        script_version = ScriptVersion.objects.get(id=script_version_id, project=project)
    except ScriptVersion.DoesNotExist:
        raise ScriptVersionNotFoundError(
            f"ScriptVersion {script_version_id} not found in project {project_id}."
        )

    if not scene_specs:
        raise ValueError("scene_specs must not be empty.")

    # Validate each scene specification before entering mutation
    for idx, spec in enumerate(scene_specs):
        narration = spec.get("narration_text", "")
        if not narration or not narration.strip():
            raise ValueError(f"Scene spec at index {idx} has empty narration_text.")

        start_char = spec.get("source_start_char", 0)
        end_char = spec.get("source_end_char", 0)

        if not (0 <= start_char <= end_char <= len(script_version.text)):
            raise InvalidSpanError(
                f"Scene spec at index {idx} has invalid span [{start_char}:{end_char}] "
                f"for script length {len(script_version.text)}."
            )

        extracted = script_version.text[start_char:end_char]
        if extracted != narration:
            raise InvalidSpanError(
                f"Scene spec at index {idx} narration text does not match "
                f"script_version text at [{start_char}:{end_char}]. "
                f"Expected {narration!r}, found {extracted!r}."
            )

    with immediate_transaction():
        # Check existing projection revision if supplied
        existing_proj = ScriptProjection.objects.filter(project=project).first()
        if existing_proj and expected_projection_rev is not None:
            if existing_proj.projection_rev != expected_projection_rev:
                raise MismatchedSourceVersionError(
                    f"Projection revision mismatch: expected {expected_projection_rev}, "
                    f"found {existing_proj.projection_rev}."
                )

        # Deactivate any previous active scenes
        Scene.objects.filter(project=project, is_active=True).update(
            is_active=False,
            order_index=None,
        )

        created_scenes: list[Scene] = []
        for idx, spec in enumerate(scene_specs):
            scene = Scene.objects.create(
                project=project,
                order_index=idx,
                is_active=True,
                source_script_version=script_version,
                source_start_char=spec.get("source_start_char", 0),
                source_end_char=spec.get("source_end_char", 0),
                narration_text=spec["narration_text"],
                visual_description=spec.get("visual_description", ""),
                generation_prompt=spec.get("generation_prompt", ""),
                rev=1,
            )
            SceneNarrationVersion.objects.create(
                scene=scene,
                version_number=1,
                text=scene.narration_text,
            )
            created_scenes.append(scene)

        proj_payload = compute_projection_payload(created_scenes)

        if existing_proj:
            for k, v in proj_payload.items():
                setattr(existing_proj, k, v)
            existing_proj.source_script_version = script_version
            existing_proj.projection_rev += 1
            existing_proj.save()
            projection = existing_proj
        else:
            projection = ScriptProjection.objects.create(
                project=project,
                source_script_version=script_version,
                projection_rev=1,
                **proj_payload,
            )

    return projection, created_scenes


def update_scene_narration(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    scene_id: uuid.UUID | str,
    new_narration_text: str,
    expected_scene_rev: int,
    expected_projection_rev: int,
) -> tuple[Scene, ScriptProjection]:
    """
    Atomically update a scene's narration text and recompute the script projection.
    Rejects mismatched scene revisions or projection revisions with MismatchedSourceVersionError.
    Flags visual review on the edited scene while preserving OriginalInput and other scenes.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot update scene narration for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot update scene narration for project {project_id}: content mutation is locked."
        )

    if not new_narration_text or not new_narration_text.strip():
        raise ValueError("new_narration_text must not be empty.")

    with immediate_transaction():
        scene = Scene.objects.filter(id=scene_id, project=project, is_active=True).first()
        if not scene:
            raise SceneNotFoundError(f"Active Scene {scene_id} not found in project {project_id}.")

        projection = ScriptProjection.objects.filter(project=project).first()
        if not projection:
            raise ScriptDomainError(f"Project {project_id} has no active ScriptProjection.")

        if projection.projection_rev != expected_projection_rev:
            raise MismatchedSourceVersionError(
                f"Projection revision mismatch: expected {expected_projection_rev}, "
                f"found {projection.projection_rev}."
            )

        if scene.rev != expected_scene_rev:
            raise MismatchedSourceVersionError(
                f"Scene revision mismatch: expected {expected_scene_rev}, "
                f"found {scene.rev}."
            )

        # Update scene narration and flag visual review
        scene.narration_text = new_narration_text
        scene.rev += 1
        flags = dict(scene.review_flags)
        flags["visual_review_needed"] = True
        scene.review_flags = flags
        scene.save(update_fields=["narration_text", "rev", "review_flags", "updated_at"])

        # Record immutable narration version
        max_ver = (
            SceneNarrationVersion.objects.filter(scene=scene).aggregate(
                m=models.Max("version_number")
            )["m"]
            or 0
        )
        SceneNarrationVersion.objects.create(
            scene=scene,
            version_number=max_ver + 1,
            text=new_narration_text,
        )

        # Recompute script projection across all active scenes in active order
        active_scenes = list(
            Scene.objects.filter(project=project, is_active=True).order_by("order_index")
        )
        proj_payload = compute_projection_payload(active_scenes)
        for k, v in proj_payload.items():
            setattr(projection, k, v)
        projection.projection_rev += 1
        projection.save()

    return scene, projection


def update_scene_visuals(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    scene_id: uuid.UUID | str,
    visual_description: str | None = None,
    generation_prompt: str | None = None,
    expected_scene_rev: int | None = None,
) -> Scene:
    """
    Update a scene's visual description or generation prompt without altering narration text.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot update scene visuals for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot update scene visuals for project {project_id}: content mutation is locked."
        )

    with immediate_transaction():
        scene = Scene.objects.filter(id=scene_id, project=project, is_active=True).first()
        if not scene:
            raise SceneNotFoundError(f"Active Scene {scene_id} not found in project {project_id}.")

        if expected_scene_rev is not None and scene.rev != expected_scene_rev:
            raise MismatchedSourceVersionError(
                f"Scene revision mismatch: expected {expected_scene_rev}, found {scene.rev}."
            )

        update_fields = ["rev", "updated_at"]
        if visual_description is not None:
            scene.visual_description = visual_description
            update_fields.append("visual_description")
        if generation_prompt is not None:
            scene.generation_prompt = generation_prompt
            update_fields.append("generation_prompt")

        scene.rev += 1
        scene.save(update_fields=update_fields)

    return scene


def reorder_scenes(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    new_scene_order_ids: list[uuid.UUID | str],
    expected_projection_rev: int,
) -> ScriptProjection:
    """
    Reorder active scenes atomically and synchronize the script projection.
    Verifies that the provided list is an exact permutation of active scene IDs.
    Scene identities (UUIDs) survive reordering independently of order index.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot reorder scenes for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot reorder scenes for project {project_id}: content mutation is locked."
        )

    with immediate_transaction():
        projection = ScriptProjection.objects.filter(project=project).first()
        if not projection:
            raise ScriptDomainError(f"Project {project_id} has no active ScriptProjection.")

        if projection.projection_rev != expected_projection_rev:
            raise MismatchedSourceVersionError(
                f"Projection revision mismatch: expected {expected_projection_rev}, "
                f"found {projection.projection_rev}."
            )

        active_scenes = {
            str(s.id): s
            for s in Scene.objects.filter(project=project, is_active=True)
        }

        order_str_ids = [str(sid) for sid in new_scene_order_ids]

        if len(order_str_ids) != len(active_scenes) or set(order_str_ids) != set(active_scenes.keys()):
            raise InvalidSceneOrderError(
                f"new_scene_order_ids must be an exact permutation of active scene IDs. "
                f"Expected set {set(active_scenes.keys())}, received {set(order_str_ids)}."
            )

        if len(order_str_ids) != len(set(order_str_ids)):
            raise InvalidSceneOrderError("Duplicate scene IDs found in new_scene_order_ids.")

        ordered_scenes: list[Scene] = []
        for idx, sid in enumerate(order_str_ids):
            scene = active_scenes[sid]
            scene.order_index = idx
            scene.save(update_fields=["order_index", "updated_at"])
            ordered_scenes.append(scene)

        proj_payload = compute_projection_payload(ordered_scenes)
        for k, v in proj_payload.items():
            setattr(projection, k, v)
        projection.projection_rev += 1
        projection.save()

    return projection


def remove_scene_from_active_order(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    scene_id: uuid.UUID | str,
    expected_projection_rev: int,
) -> ScriptProjection:
    """
    Remove a scene from the active order while preserving its record and historical assets.
    Re-indexes remaining scenes and synchronizes the script projection atomically.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot remove scene for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot remove scene for project {project_id}: content mutation is locked."
        )

    with immediate_transaction():
        projection = ScriptProjection.objects.filter(project=project).first()
        if not projection:
            raise ScriptDomainError(f"Project {project_id} has no active ScriptProjection.")

        if projection.projection_rev != expected_projection_rev:
            raise MismatchedSourceVersionError(
                f"Projection revision mismatch: expected {expected_projection_rev}, "
                f"found {projection.projection_rev}."
            )

        scene = Scene.objects.filter(id=scene_id, project=project, is_active=True).first()
        if not scene:
            raise SceneNotFoundError(f"Active Scene {scene_id} not found in project {project_id}.")

        scene.is_active = False
        scene.order_index = None
        scene.save(update_fields=["is_active", "order_index", "updated_at"])

        remaining_scenes = list(
            Scene.objects.filter(project=project, is_active=True).order_by("order_index")
        )
        for idx, s in enumerate(remaining_scenes):
            s.order_index = idx
            s.save(update_fields=["order_index", "updated_at"])

        proj_payload = compute_projection_payload(remaining_scenes)
        for k, v in proj_payload.items():
            setattr(projection, k, v)
        projection.projection_rev += 1
        projection.save()

    return projection


def restore_scene_narration(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    scene_id: uuid.UUID | str,
    target_narration_version_number: int,
    expected_scene_rev: int,
    expected_projection_rev: int,
) -> tuple[Scene, ScriptProjection]:
    """
    Restore an earlier narration text version for a scene.
    Updates the active scene text and synchronizes the script projection atomically.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot restore scene narration for deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot restore scene narration for project {project_id}: content mutation is locked."
        )

    with immediate_transaction():
        scene = Scene.objects.filter(id=scene_id, project=project, is_active=True).first()
        if not scene:
            raise SceneNotFoundError(f"Active Scene {scene_id} not found in project {project_id}.")

        projection = ScriptProjection.objects.filter(project=project).first()
        if not projection:
            raise ScriptDomainError(f"Project {project_id} has no active ScriptProjection.")

        if projection.projection_rev != expected_projection_rev:
            raise MismatchedSourceVersionError(
                f"Projection revision mismatch: expected {expected_projection_rev}, "
                f"found {projection.projection_rev}."
            )

        if scene.rev != expected_scene_rev:
            raise MismatchedSourceVersionError(
                f"Scene revision mismatch: expected {expected_scene_rev}, "
                f"found {scene.rev}."
            )

        target_version = SceneNarrationVersion.objects.filter(
            scene=scene,
            version_number=target_narration_version_number,
        ).first()
        if not target_version:
            raise ScriptDomainError(
                f"Narration version {target_narration_version_number} not found for scene {scene_id}."
            )

        scene.narration_text = target_version.text
        scene.rev += 1
        scene.save(update_fields=["narration_text", "rev", "updated_at"])

        # Record restoration as latest version
        max_ver = (
            SceneNarrationVersion.objects.filter(scene=scene).aggregate(
                m=models.Max("version_number")
            )["m"]
            or 0
        )
        SceneNarrationVersion.objects.create(
            scene=scene,
            version_number=max_ver + 1,
            text=target_version.text,
        )

        active_scenes = list(
            Scene.objects.filter(project=project, is_active=True).order_by("order_index")
        )
        proj_payload = compute_projection_payload(active_scenes)
        for k, v in proj_payload.items():
            setattr(projection, k, v)
        projection.projection_rev += 1
        projection.save()

    return scene, projection


def get_active_scenes(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
) -> list[Scene]:
    """Retrieve active scenes for a project in stable order index sequence."""
    project = get_project(user, project_id)
    return list(Scene.objects.filter(project=project, is_active=True).order_by("order_index"))


def get_scene(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    scene_id: uuid.UUID | str,
) -> Scene:
    """Retrieve a specific scene with server-side project isolation."""
    project = get_project(user, project_id)
    scene = Scene.objects.filter(id=scene_id, project=project).first()
    if not scene:
        raise SceneNotFoundError(f"Scene {scene_id} not found in project {project_id}.")
    return scene


def get_current_script_projection(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
) -> ScriptProjection | None:
    """Retrieve the current ScriptProjection for a project if initialized."""
    project = get_project(user, project_id)
    return ScriptProjection.objects.filter(project=project).first()


def get_script_version(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    version_number: int,
) -> ScriptVersion:
    """Retrieve an immutable ScriptVersion by project and version number."""
    project = get_project(user, project_id)
    ver = ScriptVersion.objects.filter(project=project, version_number=version_number).first()
    if not ver:
        raise ScriptVersionNotFoundError(
            f"ScriptVersion {version_number} not found in project {project_id}."
        )
    return ver


def get_current_script_text(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
) -> str:
    """
    Get current script text following ARTIFACT_MODEL.md single source of truth:
    - If active scene projection exists with scenes, returns projected text.
    - Else if script version exists, returns latest script version text.
    - Else returns original input text.
    """
    project = get_project(user, project_id)
    proj = ScriptProjection.objects.filter(project=project).first()
    if proj and proj.scene_count > 0:
        return proj.text

    latest_ver = (
        ScriptVersion.objects.filter(project=project)
        .order_by("-version_number")
        .first()
    )
    if latest_ver:
        return latest_ver.text

    if hasattr(project, "original_input"):
        return project.original_input.raw_text

    return ""
