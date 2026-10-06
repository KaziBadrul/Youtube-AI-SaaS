"""Project lifecycle and persistence service contracts."""
from typing import Any
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import IntegrityError

from alpha.models.projects import (
    ContentMutationLockedError,
    InputMode,
    LifecycleState,
    OriginalInput,
    Project,
    ProjectAccessDeniedError,
    ProjectDeletedError,
    ProjectNotFoundError,
    VisualStyle,
)
from alpha.persistence.cas import CASConflictError, cas_transition
from alpha.persistence.transactions import immediate_transaction


ALLOWED_AUTOSAVE_FIELDS = {
    "title",
    "target_duration_seconds",
    "target_language",
    "visual_style",
    "captions_enabled",
    "motion_enabled",
    "music_enabled",
    "voice_id",
}


def create_project(
    user: AbstractBaseUser,
    creation_token: str,
    raw_text: str,
    input_mode: str = InputMode.TOPIC,
    input_language: str = "en",
    title: str | None = None,
    settings_overrides: dict[str, Any] | None = None,
) -> tuple[Project, bool]:
    """
    Create a new Project and immutable OriginalInput record idempotently.
    Stores raw_text verbatim without stripping to maintain exact byte fidelity.
    If creation_token already exists for user, returns existing project without duplication.
    """
    if not creation_token:
        raise ValueError("creation_token must not be empty.")

    # Idempotent lookup
    existing = Project.objects.filter(user=user, creation_token=creation_token).first()
    if existing:
        return existing, False

    if not raw_text or not raw_text.strip():
        raise ValueError("raw_text must not be empty.")

    # Auto-generate title if omitted from first non-empty line
    stripped_text = raw_text.strip()
    first_line = stripped_text.splitlines()[0][:60].strip()
    project_title = title.strip() if title and title.strip() else first_line
    if not project_title:
        project_title = "Untitled Project"

    # Merge settings with frozen defaults:
    # 5-min duration, Minimal Illustration, English, captions ON, motion ON, music OFF
    opts = settings_overrides or {}
    duration = int(opts.get("target_duration_seconds", 300))
    target_lang = str(opts.get("target_language", "en"))
    style = str(opts.get("visual_style", VisualStyle.MINIMAL_ILLUSTRATION))
    captions = bool(opts.get("captions_enabled", True))
    motion = bool(opts.get("motion_enabled", True))
    music = bool(opts.get("music_enabled", False))
    voice = str(opts.get("voice_id", ""))

    try:
        with immediate_transaction():
            project = Project.objects.create(
                user=user,
                creation_token=creation_token,
                title=project_title,
                input_mode=input_mode,
                target_duration_seconds=duration,
                target_language=target_lang,
                visual_style=style,
                captions_enabled=captions,
                motion_enabled=motion,
                music_enabled=music,
                voice_id=voice,
            )
            OriginalInput.objects.create(
                project=project,
                input_mode=input_mode,
                raw_text=raw_text,  # Verbatim input bytes preserved
                input_language=input_language,
            )
        return project, True
    except IntegrityError:
        # Race condition on unique constraint: return the winner
        existing = Project.objects.filter(user=user, creation_token=creation_token).first()
        if existing:
            return existing, False
        raise


def get_project(user: AbstractBaseUser, project_id: uuid.UUID | str) -> Project:
    """
    Retrieve project and enforce server-side user ownership isolation.
    """
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise ProjectNotFoundError(f"Project {project_id} does not exist.")

    if project.user_id != user.id:
        raise ProjectAccessDeniedError(f"User {user.id} does not have access to project {project_id}.")

    return project


def rename_project(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    new_title: str,
    expected_rev: int | None = None,
) -> Project:
    """
    Rename project with atomic ownership, revision, and mutation-guard enforcement.
    """
    clean_title = new_title.strip()
    if not clean_title:
        raise ValueError("new_title must not be empty.")

    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot rename deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot rename project {project_id}: content mutation is locked."
        )

    rev_to_check = expected_rev if expected_rev is not None else project.rev

    # Atomic CAS filter includes ACTIVE state and render_locked=False to prevent interleaved bypass
    filter_kwargs = {
        "id": project.id,
        "user": user,
        "lifecycle_state": LifecycleState.ACTIVE,
        "render_locked": False,
    }

    try:
        cas_transition(
            Project,
            filter_kwargs=filter_kwargs,
            expected_rev=rev_to_check,
            update_kwargs={"title": clean_title},
        )
    except CASConflictError:
        # Check if failure was caused by concurrent lifecycle state change
        current = Project.objects.filter(id=project.id, user=user).first()
        if current:
            if current.lifecycle_state == LifecycleState.DELETED:
                raise ProjectDeletedError(f"Cannot rename deleted project {project_id}.")
            if not current.is_content_mutation_allowed():
                raise ContentMutationLockedError(
                    f"Cannot rename project {project_id}: content mutation is locked."
                )
        raise

    project.refresh_from_db()
    return project


def reopen_project(user: AbstractBaseUser, project_id: uuid.UUID | str) -> Project:
    """
    Reopen project for editing, verifying active state and isolation.
    Rejects deleted or purged projects.
    """
    project = get_project(user, project_id)
    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot reopen deleted project {project_id}.")
    if project.lifecycle_state == LifecycleState.PURGED:
        raise ProjectNotFoundError(f"Project {project_id} has been permanently purged.")
    return project


def autosave_project_settings(
    user: AbstractBaseUser,
    project_id: uuid.UUID | str,
    expected_rev: int,
    updates: dict[str, Any],
) -> Project:
    """
    Version-aware autosave for project settings using CAS transition.
    Atomically checks ACTIVE lifecycle state and render_locked=False inside CAS.
    Stale autosave attempts raise CASConflictError to prevent overwriting newer edits.
    """
    project = get_project(user, project_id)

    if project.lifecycle_state == LifecycleState.DELETED:
        raise ProjectDeletedError(f"Cannot autosave deleted project {project_id}.")

    if not project.is_content_mutation_allowed():
        raise ContentMutationLockedError(
            f"Cannot autosave project {project_id}: content mutation is locked."
        )

    # Validate update keys
    validated_updates: dict[str, Any] = {}
    for k, v in updates.items():
        if k not in ALLOWED_AUTOSAVE_FIELDS:
            raise ValueError(f"Field {k!r} is not an allowed autosave setting.")
        validated_updates[k] = v

    if not validated_updates:
        return project

    # Atomic CAS filter includes ACTIVE state and render_locked=False
    filter_kwargs = {
        "id": project.id,
        "user": user,
        "lifecycle_state": LifecycleState.ACTIVE,
        "render_locked": False,
    }

    try:
        cas_transition(
            Project,
            filter_kwargs=filter_kwargs,
            expected_rev=expected_rev,
            update_kwargs=validated_updates,
        )
    except CASConflictError:
        # Check if conflict was caused by concurrent lifecycle state change
        current = Project.objects.filter(id=project.id, user=user).first()
        if current:
            if current.lifecycle_state == LifecycleState.DELETED:
                raise ProjectDeletedError(f"Cannot autosave deleted project {project_id}.")
            if not current.is_content_mutation_allowed():
                raise ContentMutationLockedError(
                    f"Cannot autosave project {project_id}: content mutation is locked."
                )
        raise

    project.refresh_from_db()
    return project
