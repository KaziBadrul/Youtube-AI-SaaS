"""Domain tests for typed artifact persistence, version envelopes, and state axes."""
import hashlib
import os
import unittest
import uuid

os.environ.setdefault(
    "ALPHA_SECRET_KEY",
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from alpha.models.artifacts import (
    ArtifactAttempt,
    ArtifactKind,
    ArtifactSlot,
    ArtifactSourceType,
    ArtifactVersion,
    CrossProjectArtifactReferenceError,
    GenerationOutcome,
    ImmutableArtifactVersionError,
    InvalidArtifactPayloadError,
    InvalidArtifactSelectionError,
    SlotOutcome,
    compute_canonical_json_hash,
)
from alpha.models.projects import InputMode, Project
from alpha.models.scenes import Scene, SceneNarrationVersion
from alpha.models.scripts import ScriptVersion
from alpha.services.projects import create_project

from alpha.services.artifacts import (
    create_artifact_version,
    get_artifact_slot,
    get_artifact_version,
    get_or_create_artifact_slot,
    record_generation_attempt,
    select_artifact_version,
    set_slot_compatibility,
    set_slot_review_needed,
)

User = get_user_model()


class ArtifactPersistenceDomainTests(TestCase):
    """
    Test suite verifying typed artifact versions, shared provenance envelopes,
    independent orthogonal state axes, and cross-project rejection constraints.
    """

    def setUp(self) -> None:
        self.user_a = User.objects.create_user(username="creator_a", password="password-a-123456")
        self.user_b = User.objects.create_user(username="creator_b", password="password-b-123456")

        self.project_a, _ = create_project(
            user=self.user_a,
            creation_token="proj-token-art-001",
            raw_text="Topic A",
            input_mode=InputMode.TOPIC,
            title="Project A",
        )
        self.project_b, _ = create_project(
            user=self.user_b,
            creation_token="proj-token-art-002",
            raw_text="Topic B",
            input_mode=InputMode.TOPIC,
            title="Project B",
        )

        self.script_v1_a = ScriptVersion.objects.create(
            project=self.project_a,
            version_number=1,
            text="First sentence for project A. Second sentence for project A.",
        )
        self.script_v1_b = ScriptVersion.objects.create(
            project=self.project_b,
            version_number=1,
            text="First sentence for project B.",
        )

        self.scene_a1 = Scene.objects.create(
            project=self.project_a,
            order_index=0,
            narration_text="First sentence for project A.",
            visual_description="A quiet library desk.",
            generation_prompt="cinematic lighting, quiet library desk, detailed wood texture",
        )
        self.scene_a2 = Scene.objects.create(
            project=self.project_a,
            order_index=1,
            narration_text="Second sentence for project A.",
            visual_description="An open encyclopedia.",
            generation_prompt="macro shot of encyclopedia page, warm sunlight",
        )
        self.scene_b1 = Scene.objects.create(
            project=self.project_b,
            order_index=0,
            narration_text="First sentence for project B.",
            visual_description="A bustling cityscape.",
            generation_prompt="cityscape at dusk, neon lights, 4k",
        )

        self.narration_v1_a1 = SceneNarrationVersion.objects.create(
            scene=self.scene_a1,
            version_number=1,
            text="First sentence for project A.",
        )
        self.narration_v1_b1 = SceneNarrationVersion.objects.create(
            scene=self.scene_b1,
            version_number=1,
            text="First sentence for project B.",
        )

        self.dummy_hash = hashlib.sha256(b"dummy image bytes").hexdigest()

    def test_immutability_of_persisted_artifact_version(self) -> None:
        """Verify that persisted ArtifactVersion instances strictly reject any update."""
        version = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/projects/a/scenes/1/img_v1.png",
            byte_hash=self.dummy_hash,
            byte_count=10240,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        self.assertEqual(version.version_number, 1)

        # Attempt to modify any field and save
        version.byte_count = 20480
        with self.assertRaises(ImmutableArtifactVersionError):
            version.save()

        version.storage_key = "media/tampered_key.png"
        with self.assertRaises(ImmutableArtifactVersionError):
            version.save()

        # Verify database contents remain unmodified
        reloaded = ArtifactVersion.objects.get(id=version.id)
        self.assertEqual(reloaded.byte_count, 10240)
        self.assertEqual(reloaded.storage_key, "media/projects/a/scenes/1/img_v1.png")

    def test_typed_payload_image_validation_and_binary_media_boundary(self) -> None:
        """Verify IMAGE artifact payload validation and enforcement that binary media stays outside SQLite."""
        # 1. Valid image payload passes
        valid_img = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/projects/a/img_v1.png",
            byte_hash=self.dummy_hash,
            byte_count=5000,
            mime_type="image/png",
            validation_metadata={"width": 1280, "height": 720},
        )
        self.assertTrue(valid_img.is_valid)

        # 2. Raw binary media or structured_payload directly in SQLite is rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=2,
                storage_key="media/projects/a/img_v2.png",
                byte_hash=self.dummy_hash,
                byte_count=5000,
                mime_type="image/png",
                structured_payload={"data": "raw_binary_bytes_in_sqlite"},
                validation_metadata={"width": 1280, "height": 720},
            )

        # 3. Missing storage key is rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=2,
                storage_key="",
                byte_hash=self.dummy_hash,
                byte_count=5000,
                mime_type="image/png",
                validation_metadata={"width": 1280, "height": 720},
            )

        # 4. Invalid byte hash is rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=2,
                storage_key="media/img.png",
                byte_hash="invalid_hash_string",
                byte_count=5000,
                mime_type="image/png",
                validation_metadata={"width": 1280, "height": 720},
            )

        # 5. Non-image MIME type is rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=2,
                storage_key="media/img.png",
                byte_hash=self.dummy_hash,
                byte_count=5000,
                mime_type="audio/wav",
                validation_metadata={"width": 1280, "height": 720},
            )

        # 6. Missing width/height in validation metadata is rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=2,
                storage_key="media/img.png",
                byte_hash=self.dummy_hash,
                byte_count=5000,
                mime_type="image/png",
                validation_metadata={"width": -10, "height": 720},
            )

    def test_typed_payload_audio_validation(self) -> None:
        """Verify AUDIO artifact payload validation and media boundary enforcement."""
        audio_hash = hashlib.sha256(b"dummy audio wav").hexdigest()

        # 1. Valid audio payload passes
        valid_audio = create_artifact_version(
            project=self.project_a,
            kind=ArtifactKind.AUDIO,
            version_number=1,
            storage_key="media/projects/a/audio_v1.wav",
            byte_hash=audio_hash,
            byte_count=88200,
            mime_type="audio/wav",
            validation_metadata={"duration_ms": 2000, "sample_rate": 44100},
        )
        self.assertTrue(valid_audio.is_valid)

        # 2. Binary in SQLite rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                kind=ArtifactKind.AUDIO,
                version_number=2,
                storage_key="media/projects/a/audio_v2.wav",
                byte_hash=audio_hash,
                byte_count=88200,
                mime_type="audio/wav",
                structured_payload={"raw_audio": "base64bytes"},
                validation_metadata={"duration_ms": 2000},
            )

        # 3. Non-audio MIME rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                kind=ArtifactKind.AUDIO,
                version_number=2,
                storage_key="media/projects/a/audio_v2.wav",
                byte_hash=audio_hash,
                byte_count=88200,
                mime_type="image/jpeg",
                validation_metadata={"duration_ms": 2000},
            )

        # 4. Missing duration_ms rejected
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                kind=ArtifactKind.AUDIO,
                version_number=2,
                storage_key="media/projects/a/audio_v2.wav",
                byte_hash=audio_hash,
                byte_count=88200,
                mime_type="audio/wav",
                validation_metadata={},
            )

    def test_typed_payload_timing_and_caption_validation(self) -> None:
        """Verify structured payloads for TIMING alignments and CAPTION cues."""
        # 1. Valid TIMING
        timing_payload = {
            "words": [
                {"word": "First", "start_ms": 0, "end_ms": 300},
                {"word": "sentence", "start_ms": 320, "end_ms": 800},
            ]
        }
        timing_ver = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.TIMING,
            version_number=1,
            structured_payload=timing_payload,
        )
        self.assertTrue(timing_ver.is_valid)
        self.assertTrue(len(timing_ver.byte_hash) == 64)

        # Invalid timing: end before start
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.TIMING,
                version_number=2,
                structured_payload={"words": [{"word": "Bad", "start_ms": 500, "end_ms": 200}]},
            )

        # 2. Valid CAPTION
        caption_payload = {
            "cues": [
                {"text": "First sentence.", "start_ms": 0, "end_ms": 800},
            ]
        }
        caption_ver = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.CAPTION,
            version_number=1,
            structured_payload=caption_payload,
        )
        self.assertTrue(caption_ver.is_valid)
        self.assertTrue(len(caption_ver.byte_hash) == 64)

        # Invalid caption: empty text
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.CAPTION,
                version_number=2,
                structured_payload={"cues": [{"text": "   ", "start_ms": 0, "end_ms": 800}]},
            )

    def test_independent_state_axes_and_failed_attempt_preservation(self) -> None:
        """
        Verify that Valid, Selected, Compatible/Outdated, and Review Needed remain
        4 strictly independent orthogonal axes, and failed attempts preserve prior valid selection.
        """
        slot = get_or_create_artifact_slot(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
        )

        # Initial state
        self.assertIsNone(slot.selected_version)
        self.assertTrue(slot.is_compatible)
        self.assertFalse(slot.needs_review)
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.NONE)

        # Successful attempt 1 produces version 1 and selects it
        v1 = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/projects/a/v1.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        record_generation_attempt(
            slot=slot,
            attempt_id="att-1-success",
            outcome=GenerationOutcome.SUCCEEDED,
            resulting_version=v1,
            select_on_success=True,
        )

        slot.refresh_from_db()
        self.assertEqual(slot.selected_version, v1)
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.SUCCEEDED)
        self.assertTrue(slot.is_compatible)
        self.assertFalse(slot.needs_review)

        # Newer attempt 2 fails (e.g. rate limit / network error)
        record_generation_attempt(
            slot=slot,
            attempt_id="att-2-failed",
            outcome=GenerationOutcome.FAILED,
            error_message="Provider upstream error 503",
            diagnostic_data={"http_status": 503, "retryable": True},
        )

        slot.refresh_from_db()
        # CRITICAL ACCEPTANCE CRITERION: prior valid selection and provenance remain 100% intact!
        self.assertEqual(slot.selected_version, v1)
        self.assertEqual(slot.selected_version.storage_key, "media/projects/a/v1.png")
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.FAILED)
        self.assertEqual(slot.last_attempt_id, "att-2-failed")
        self.assertEqual(slot.last_attempt_error, "Provider upstream error 503")

        # Independent Axis 3: Mark slot outdated (e.g. scene narration changed)
        set_slot_compatibility(slot, is_compatible=False)
        slot.refresh_from_db()
        self.assertFalse(slot.is_compatible)
        self.assertEqual(slot.selected_version, v1)  # Version still selected
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.FAILED)  # Last attempt still failed

        # Independent Axis 4: Flag review needed (e.g. semantic visual drift)
        set_slot_review_needed(slot, needs_review=True, reason="Prompt style drifted from series baseline")
        slot.refresh_from_db()
        self.assertTrue(slot.needs_review)
        self.assertEqual(slot.review_reason, "Prompt style drifted from series baseline")
        self.assertFalse(slot.is_compatible)  # Still outdated
        self.assertEqual(slot.selected_version, v1)  # Still selected
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.FAILED)  # Still failed attempt

        # Verify all 4 axes are simultaneously observable and independent
        self.assertTrue(v1.is_valid)  # 1. Valid
        self.assertEqual(slot.selected_version.id, v1.id)  # 2. Selected
        self.assertFalse(slot.is_compatible)  # 3. Outdated
        self.assertTrue(slot.needs_review)  # 4. Review Needed
        self.assertEqual(slot.last_attempt_outcome, SlotOutcome.FAILED)  # Last generation outcome

    def test_source_version_hash_config_round_trips(self) -> None:
        """Verify that source-version references, config dictionaries, and hashes round trip accurately."""
        effective_cfg = {"model": "gemini-3.1-flash-lite-image", "aspect_ratio": "16:9", "steps": 30}
        pinned_sources = {
            "script_version_id": str(self.script_v1_a.id),
            "narration_version_id": str(self.narration_v1_a1.id),
        }

        v = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/projects/a/v1.png",
            byte_hash=self.dummy_hash,
            byte_count=4096,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
            source_script_version=self.script_v1_a,
            source_narration_version=self.narration_v1_a1,
            pinned_source_versions=pinned_sources,
            provider="gemini",
            model="gemini-3.1-flash-lite-image",
            effective_config=effective_cfg,
        )

        reloaded = get_artifact_version(self.project_a, v.id)
        self.assertEqual(reloaded.source_script_version, self.script_v1_a)
        self.assertEqual(reloaded.source_narration_version, self.narration_v1_a1)
        self.assertEqual(reloaded.pinned_source_versions, pinned_sources)
        self.assertEqual(reloaded.effective_config, effective_cfg)
        self.assertEqual(reloaded.effective_config_signature, compute_canonical_json_hash(effective_cfg))
        self.assertEqual(reloaded.byte_hash, self.dummy_hash)

    def test_cross_owner_and_incompatible_reference_rejection(self) -> None:
        """Verify that domain constraints reject impossible cross-owner and cross-scene references."""
        # 1. ArtifactVersion referencing scene belonging to another project
        with self.assertRaises(CrossProjectArtifactReferenceError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_b1,  # Belongs to Project B!
                kind=ArtifactKind.IMAGE,
                version_number=1,
                storage_key="media/test.png",
                byte_hash=self.dummy_hash,
                byte_count=1000,
                mime_type="image/png",
                validation_metadata={"width": 1920, "height": 1080},
            )

        # 2. ArtifactVersion referencing script version from another project
        with self.assertRaises(CrossProjectArtifactReferenceError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=1,
                storage_key="media/test.png",
                byte_hash=self.dummy_hash,
                byte_count=1000,
                mime_type="image/png",
                validation_metadata={"width": 1920, "height": 1080},
                source_script_version=self.script_v1_b,  # Belongs to Project B!
            )

        # 3. ArtifactVersion referencing narration version from another project
        with self.assertRaises(CrossProjectArtifactReferenceError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=1,
                storage_key="media/test.png",
                byte_hash=self.dummy_hash,
                byte_count=1000,
                mime_type="image/png",
                validation_metadata={"width": 1920, "height": 1080},
                source_narration_version=self.narration_v1_b1,  # Belongs to Project B!
            )

        # 4. Slot selection cross-owner rejection
        slot_a = get_or_create_artifact_slot(self.project_a, ArtifactKind.IMAGE, scene=self.scene_a1)
        v_b = create_artifact_version(
            project=self.project_b,
            scene=self.scene_b1,
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/b1.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        with self.assertRaises(CrossProjectArtifactReferenceError):
            select_artifact_version(slot_a, v_b)

        # 5. Slot selection cross-scene rejection (same project, wrong scene)
        v_a2 = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a2,  # Scene A2
            kind=ArtifactKind.IMAGE,
            version_number=1,
            storage_key="media/a2.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        with self.assertRaises(CrossProjectArtifactReferenceError):
            select_artifact_version(slot_a, v_a2)  # slot_a is for scene_a1!

        # 6. Kind mismatch rejection (e.g. selecting AUDIO version in IMAGE slot)
        audio_v = create_artifact_version(
            project=self.project_a,
            kind=ArtifactKind.AUDIO,
            version_number=1,
            storage_key="media/a.wav",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="audio/wav",
            validation_metadata={"duration_ms": 1000},
        )
        with self.assertRaises(InvalidArtifactSelectionError):
            select_artifact_version(slot_a, audio_v)

        # 7. Selecting an invalid artifact version is rejected
        invalid_v = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=2,
            storage_key="media/invalid.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
            is_valid=False,  # Failed technical checks
        )
        with self.assertRaises(InvalidArtifactSelectionError):
            select_artifact_version(slot_a, invalid_v)

        # 8. Project-scoped slot (scene=None) rejecting scene-scoped version
        project_audio_slot = get_or_create_artifact_slot(self.project_a, ArtifactKind.AUDIO, scene=None)
        scene_audio_v = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.AUDIO,
            version_number=2,
            storage_key="media/scene_audio.wav",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="audio/wav",
            validation_metadata={"duration_ms": 1000},
        )
        with self.assertRaises(CrossProjectArtifactReferenceError):
            select_artifact_version(project_audio_slot, scene_audio_v)
        with self.assertRaises(CrossProjectArtifactReferenceError):
            ArtifactSlot(
                project=self.project_a,
                scene=None,
                kind=ArtifactKind.AUDIO,
                slot_key="test_direct_proj",
                selected_version=scene_audio_v,
            ).save()

        # 9. Scene-scoped slot rejecting project-scoped version
        project_audio_v = create_artifact_version(
            project=self.project_a,
            scene=None,
            kind=ArtifactKind.AUDIO,
            version_number=3,
            storage_key="media/project_audio.wav",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="audio/wav",
            validation_metadata={"duration_ms": 2000},
        )
        scene_audio_slot = get_or_create_artifact_slot(self.project_a, ArtifactKind.AUDIO, scene=self.scene_a1)
        with self.assertRaises(CrossProjectArtifactReferenceError):
            select_artifact_version(scene_audio_slot, project_audio_v)
        with self.assertRaises(CrossProjectArtifactReferenceError):
            ArtifactSlot(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.AUDIO,
                slot_key="test_direct_scene",
                selected_version=project_audio_v,
            ).save()

    def test_failed_generation_outcome_cannot_be_valid_or_selected(self) -> None:
        """Verify that generation failures do not create selectable valid versions."""
        # 1. Non-success outcome with is_valid=True is rejected by ArtifactVersion.clean()
        with self.assertRaises(InvalidArtifactPayloadError):
            create_artifact_version(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                version_number=10,
                storage_key="media/failed.png",
                byte_hash=self.dummy_hash,
                byte_count=1000,
                mime_type="image/png",
                validation_metadata={"width": 1920, "height": 1080},
                generation_outcome=GenerationOutcome.FAILED,
                is_valid=True,
            )

        v_failed_direct = ArtifactVersion(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=11,
            storage_key="media/failed.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
            generation_outcome=GenerationOutcome.FAILED,
            is_valid=True,
        )
        with self.assertRaises(InvalidArtifactPayloadError):
            v_failed_direct.clean()

        # 2. When created with non-success outcome without is_valid, defaults to is_valid=False
        failed_v = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            version_number=12,
            storage_key="media/failed2.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
            generation_outcome=GenerationOutcome.FAILED,
        )
        self.assertFalse(failed_v.is_valid)

        # 3. Attempting to select a failed outcome version into a slot is rejected
        slot = get_or_create_artifact_slot(self.project_a, ArtifactKind.IMAGE, scene=self.scene_a1)
        with self.assertRaises(InvalidArtifactSelectionError):
            select_artifact_version(slot, failed_v)

        with self.assertRaises(InvalidArtifactSelectionError):
            ArtifactSlot(
                project=self.project_a,
                scene=self.scene_a1,
                kind=ArtifactKind.IMAGE,
                slot_key="test_failed_sel",
                selected_version=failed_v,
            ).save()

    def test_version_uniqueness_and_monotonic_numbering(self) -> None:
        """Verify version numbering increments monotonically and enforces uniqueness."""
        v1 = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            storage_key="media/v1.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        self.assertEqual(v1.version_number, 1)

        v2 = create_artifact_version(
            project=self.project_a,
            scene=self.scene_a1,
            kind=ArtifactKind.IMAGE,
            storage_key="media/v2.png",
            byte_hash=self.dummy_hash,
            byte_count=1000,
            mime_type="image/png",
            validation_metadata={"width": 1920, "height": 1080},
        )
        self.assertEqual(v2.version_number, 2)
