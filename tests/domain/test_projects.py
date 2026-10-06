"""Automated tests for T005: Project persistence, original input, and lifecycle settings."""
import hashlib
from datetime import timedelta
import os
import unittest
from unittest.mock import patch
import uuid

os.environ.setdefault(
    "ALPHA_SECRET_KEY",
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils import timezone

from alpha.models.projects import (
    ContentMutationLockedError,
    ImmutableOriginalInputError,
    InputMode,
    LifecycleState,
    OriginalInput,
    Project,
    ProjectAccessDeniedError,
    ProjectDeletedError,
    ProjectNotFoundError,
    VisualStyle,
)
from alpha.persistence.cas import CASConflictError
from alpha.services.projects import (
    autosave_project_settings,
    create_project,
    get_project,
    rename_project,
    reopen_project,
)

User = get_user_model()


class ProjectPersistenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_a, _ = User.objects.get_or_create(username="creator_alpha_a")
        cls.user_b, _ = User.objects.get_or_create(username="creator_alpha_b")

    def setUp(self) -> None:
        self.token = str(uuid.uuid4())
        self.raw_topic = "  The History of Tea in Ancient China  \n\nExplore how tea became a global drink.  "

    def test_create_project_defaults_and_verbatim_original_input(self) -> None:
        """Verify project creation defaults and verbatim byte-level preservation of OriginalInput."""
        project, created = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
            input_mode=InputMode.TOPIC,
            input_language="en",
        )

        self.assertTrue(created)
        self.assertEqual(project.user, self.user_a)
        self.assertEqual(project.creation_token, self.token)
        self.assertEqual(project.rev, 1)
        self.assertEqual(project.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(project.input_mode, InputMode.TOPIC)
        self.assertEqual(project.title, "The History of Tea in Ancient China")

        # Frozen defaults verification
        self.assertEqual(project.target_duration_seconds, 300)  # 5 minutes
        self.assertEqual(project.target_language, "en")
        self.assertEqual(project.visual_style, VisualStyle.MINIMAL_ILLUSTRATION)
        self.assertTrue(project.captions_enabled)
        self.assertTrue(project.motion_enabled)
        self.assertFalse(project.music_enabled)
        self.assertFalse(project.render_locked)
        self.assertIsNone(project.current_render_lock_id)

        # Verbatim OriginalInput byte fidelity (Finding B3)
        orig = OriginalInput.objects.get(project=project)
        self.assertEqual(orig.input_mode, InputMode.TOPIC)
        self.assertEqual(orig.raw_text, self.raw_topic)  # Unstripped verbatim string!
        self.assertEqual(orig.input_language, "en")
        self.assertEqual(orig.byte_count, len(self.raw_topic.encode("utf-8")))
        self.assertEqual(orig.word_count, len(self.raw_topic.split()))
        expected_hash = hashlib.sha256(self.raw_topic.encode("utf-8")).hexdigest()
        self.assertEqual(orig.content_sha256, expected_hash)

    def test_idempotent_creation_token_prevents_duplicate_projects(self) -> None:
        """Verify repeated calls with the same creation token return existing project idempotently."""
        p1, created1 = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        self.assertTrue(created1)

        p2, created2 = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text="Different topic text should not override",
        )
        self.assertFalse(created2)
        self.assertEqual(p1.id, p2.id)
        self.assertEqual(p2.original_input.raw_text, self.raw_topic)
        self.assertEqual(Project.objects.filter(creation_token=self.token).count(), 1)

    def test_original_versus_current_data_separation(self) -> None:
        """Verify that modifying project settings or current content never alters immutable original input."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        initial_orig = OriginalInput.objects.get(project=project)
        initial_hash = initial_orig.content_sha256

        # Update project settings via autosave and rename
        rename_project(self.user_a, project.id, "Renamed Global Tea History")
        autosave_project_settings(
            self.user_a,
            project.id,
            expected_rev=2,
            updates={
                "target_language": "fr",
                "visual_style": VisualStyle.DOCUMENTARY_ILLUSTRATION,
                "music_enabled": True,
            },
        )

        project.refresh_from_db()
        self.assertEqual(project.title, "Renamed Global Tea History")
        self.assertEqual(project.target_language, "fr")
        self.assertEqual(project.rev, 3)

        # Assert OriginalInput remains completely identical
        refreshed_orig = OriginalInput.objects.get(project=project)
        self.assertEqual(refreshed_orig.raw_text, self.raw_topic)
        self.assertEqual(refreshed_orig.input_language, "en")
        self.assertEqual(refreshed_orig.content_sha256, initial_hash)

    def test_original_input_strict_immutability(self) -> None:
        """Verify OriginalInput raises ImmutableOriginalInputError if an update is attempted."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        orig = OriginalInput.objects.get(project=project)
        orig.raw_text = "Tampered text trying to overwrite input"
        with self.assertRaises(ImmutableOriginalInputError):
            orig.save()

    def test_rename_and_reopen_project(self) -> None:
        """Verify rename updates title, bumps rev, and reopen returns active project."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
            title="Initial Title",
        )
        self.assertEqual(project.rev, 1)

        renamed = rename_project(self.user_a, project.id, "Brand New Title")
        self.assertEqual(renamed.title, "Brand New Title")
        self.assertEqual(renamed.rev, 2)

        reopened = reopen_project(self.user_a, project.id)
        self.assertEqual(reopened.id, project.id)
        self.assertEqual(reopened.title, "Brand New Title")

        with self.assertRaises(ValueError):
            rename_project(self.user_a, project.id, "   ")

    def test_concurrent_autosave_revision_conflict(self) -> None:
        """Verify version-aware autosave rejects stale revisions and prevents overwriting newer edits."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        self.assertEqual(project.rev, 1)

        # Tab 1 performs edit with expected_rev=1 -> succeeds, rev becomes 2
        autosave_project_settings(
            self.user_a,
            project.id,
            expected_rev=1,
            updates={"music_enabled": True},
        )
        project.refresh_from_db()
        self.assertEqual(project.rev, 2)
        self.assertTrue(project.music_enabled)

        # Tab 2 had stale expected_rev=1 -> must raise CASConflictError
        with self.assertRaises(CASConflictError):
            autosave_project_settings(
                self.user_a,
                project.id,
                expected_rev=1,
                updates={"music_enabled": False, "target_language": "es"},
            )

        # Verify state was not modified by stale autosave
        project.refresh_from_db()
        self.assertEqual(project.rev, 2)
        self.assertTrue(project.music_enabled)
        self.assertEqual(project.target_language, "en")

    def test_content_mutation_guard_under_render_lock(self) -> None:
        """Verify all project content edits are blocked when render_locked=True (Finding B1)."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )

        # Set render lock on project directly
        Project.objects.filter(id=project.id).update(
            render_locked=True,
            current_render_lock_id="render-job-001",
            lifecycle_state=LifecycleState.RENDERING,
            rev=F("rev") + 1,
        )
        project.refresh_from_db()
        self.assertTrue(project.render_locked)
        self.assertFalse(project.is_content_mutation_allowed())

        # Edits must fail while render lock is active
        with self.assertRaises(ContentMutationLockedError):
            rename_project(self.user_a, project.id, "Illegal rename during render")

        with self.assertRaises(ContentMutationLockedError):
            autosave_project_settings(
                self.user_a,
                project.id,
                expected_rev=project.rev,
                updates={"target_duration_seconds": 600},
            )

        # Release lock
        Project.objects.filter(id=project.id).update(
            render_locked=False,
            current_render_lock_id=None,
            lifecycle_state=LifecycleState.ACTIVE,
            rev=F("rev") + 1,
        )
        project.refresh_from_db()
        self.assertTrue(project.is_content_mutation_allowed())

        # Edits now succeed
        rename_project(self.user_a, project.id, "Allowed rename after unlock")
        project.refresh_from_db()
        self.assertEqual(project.title, "Allowed rename after unlock")

    def test_interleaved_deletion_blocks_stale_autosave(self) -> None:
        """Verify stale autosave targeting deleted project cannot write or bypass guard (Finding B1)."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        stale_rev = project.rev

        # Simulate concurrent deletion that sets DELETED and bumps rev
        now = timezone.now()
        Project.objects.filter(id=project.id).update(
            lifecycle_state=LifecycleState.DELETED,
            deleted_at=now,
            retention_deadline=now + timedelta(days=7),
            rev=F("rev") + 1,
        )

        # Stale autosave with stale_rev must raise ProjectDeletedError or CASConflictError
        with self.assertRaises((ProjectDeletedError, CASConflictError)):
            autosave_project_settings(
                self.user_a,
                project.id,
                expected_rev=stale_rev,
                updates={"music_enabled": True},
            )

        # Verify project remains DELETED and music_enabled was NOT changed
        project.refresh_from_db()
        self.assertEqual(project.lifecycle_state, LifecycleState.DELETED)
        self.assertFalse(project.music_enabled)

        # Reopen of deleted project must also be rejected
        with self.assertRaises(ProjectDeletedError):
            reopen_project(self.user_a, project.id)

    def test_cross_project_isolation_and_ownership_rejection(self) -> None:
        """Verify user B cannot view, edit, or autosave user A's project records."""
        project_a, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )

        # User B cannot access project A
        with self.assertRaises(ProjectAccessDeniedError):
            get_project(self.user_b, project_a.id)

        with self.assertRaises(ProjectAccessDeniedError):
            rename_project(self.user_b, project_a.id, "Malicious rename")

        with self.assertRaises(ProjectAccessDeniedError):
            autosave_project_settings(
                self.user_b,
                project_a.id,
                expected_rev=project_a.rev,
                updates={"title": "Hacked title"},
            )

        with self.assertRaises(ProjectAccessDeniedError):
            reopen_project(self.user_b, project_a.id)

        # User B creating with same token creates an isolated project for user B
        project_b, created_b = create_project(
            user=self.user_b,
            creation_token=self.token,
            raw_text="User B's completely independent project",
        )
        self.assertTrue(created_b)
        self.assertNotEqual(project_a.id, project_b.id)
        self.assertEqual(project_b.user, self.user_b)

    def test_unallowed_autosave_fields_rejected(self) -> None:
        """Verify autosave rejects unauthorized fields (id, rev, user, storage_bytes)."""
        project, _ = create_project(
            user=self.user_a,
            creation_token=self.token,
            raw_text=self.raw_topic,
        )
        for forbidden in ["id", "rev", "user", "storage_bytes", "render_locked", "lifecycle_state"]:
            with self.assertRaises(ValueError):
                autosave_project_settings(
                    self.user_a,
                    project.id,
                    expected_rev=project.rev,
                    updates={forbidden: "illegal_value"},
                )

    def test_transactional_rollback_on_failed_original_input(self) -> None:
        """Verify atomic transaction rolls back Project creation if OriginalInput creation fails."""
        fail_token = str(uuid.uuid4())
        with patch.object(OriginalInput.objects, "create", side_effect=RuntimeError("Simulated DB error")):
            with self.assertRaises(RuntimeError):
                create_project(
                    user=self.user_a,
                    creation_token=fail_token,
                    raw_text=self.raw_topic,
                )

        # Assert no orphaned Project was created
        self.assertFalse(Project.objects.filter(creation_token=fail_token).exists())


if __name__ == "__main__":
    unittest.main()
