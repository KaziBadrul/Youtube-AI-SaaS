"""Automated domain tests for script versions and stable scene projections."""
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from alpha.models.projects import (
    ContentMutationLockedError,
    ImmutableOriginalInputError,
    InputMode,
    LifecycleState,
    OriginalInput,
    Project,
    ProjectAccessDeniedError,
    ProjectDeletedError,
)
from alpha.models.scenes import (
    ImmutableSceneNarrationError,
    InvalidSceneOrderError,
    Scene,
    SceneNarrationVersion,
    SceneNotFoundError,
)
from alpha.models.scripts import (
    ImmutableScriptVersionError,
    InvalidSpanError,
    MismatchedSourceVersionError,
    ScriptProjection,
    ScriptSourceType,
    ScriptVersion,
    ScriptVersionNotFoundError,
)
from alpha.services.projects import create_project
from alpha.services.script_projection import (
    compute_projection_payload,
    create_script_version,
    get_active_scenes,
    get_current_script_projection,
    get_current_script_text,
    get_scene,
    get_script_version,
    initialize_scenes_from_script,
    remove_scene_from_active_order,
    reorder_scenes,
    restore_scene_narration,
    update_scene_narration,
    update_scene_visuals,
)

User = get_user_model()


class ScriptProjectionDomainTests(TestCase):
    """
    Test suite verifying script version persistence, stable scene projections,
    source-span round trips, stable scene identities under reordering,
    atomic conflict rejection, and immutable original input preservation.
    """

    def setUp(self) -> None:
        self.user_a = User.objects.create_user(
            username="creator_a",
            email="creator_a@example.com",
            password="test-password-alpha-123",
        )
        self.user_b = User.objects.create_user(
            username="creator_b",
            email="creator_b@example.com",
            password="test-password-alpha-456",
        )

        self.project_a, _ = create_project(
            user=self.user_a,
            creation_token="proj-token-script-001",
            raw_text="Initial Topic: Educational guide to the solar system.",
            input_mode=InputMode.TOPIC,
            title="Solar System Production",
        )

    def test_script_version_creation_and_immutability(self) -> None:
        """Verify project-scoped script versions increment monotonically and remain immutable."""
        v1 = create_script_version(
            user=self.user_a,
            project_id=self.project_a.id,
            text="The solar system consists of the Sun and planetary bodies.",
            source_type=ScriptSourceType.GENERATED,
        )
        self.assertEqual(v1.version_number, 1)
        self.assertEqual(v1.project_id, self.project_a.id)
        self.assertTrue(v1.content_sha256)
        self.assertGreater(v1.word_count, 0)
        self.assertGreater(v1.byte_count, 0)

        v2 = create_script_version(
            user=self.user_a,
            project_id=self.project_a.id,
            text="The solar system consists of the Sun, eight planets, and celestial bodies.",
            source_type=ScriptSourceType.EDITED,
        )
        self.assertEqual(v2.version_number, 2)

        # Immutability enforcement on existing ScriptVersion
        with self.assertRaises(ImmutableScriptVersionError):
            v1.text = "Attempting mutation"
            v1.save()

    def test_projection_and_source_span_round_trips_unicode_and_punctuation(self) -> None:
        """
        Verify source-span round trips and script projection handling Unicode,
        punctuation, emojis, and non-ASCII characters with exact code-point fidelity.
        """
        complex_script_text = (
            "সূর্য আমাদের সৌরজগতের কেন্দ্র। 🌞\n\n"
            "Le Café des Planètes — “Mercure, Vénus, et la Terre!”…\n\n"
            "宇宙の旅へようこそ！ 🚀"
        )
        script_version = create_script_version(
            user=self.user_a,
            project_id=self.project_a.id,
            text=complex_script_text,
            source_type=ScriptSourceType.GENERATED,
        )

        # Locate exact Unicode spans in the source script
        part1 = "সূর্য আমাদের সৌরজগতের কেন্দ্র। 🌞"
        part2 = "Le Café des Planètes — “Mercure, Vénus, et la Terre!”…"
        part3 = "宇宙の旅へようこそ！ 🚀"

        start1 = complex_script_text.index(part1)
        end1 = start1 + len(part1)
        self.assertEqual(complex_script_text[start1:end1], part1)

        start2 = complex_script_text.index(part2)
        end2 = start2 + len(part2)
        self.assertEqual(complex_script_text[start2:end2], part2)

        start3 = complex_script_text.index(part3)
        end3 = start3 + len(part3)
        self.assertEqual(complex_script_text[start3:end3], part3)

        scene_specs = [
            {
                "narration_text": part1,
                "visual_description": "Sun shining brightly in space with solar flares.",
                "generation_prompt": "Minimalist digital illustration of a radiant sun, warm ambient lighting.",
                "source_start_char": start1,
                "source_end_char": end1,
            },
            {
                "narration_text": part2,
                "visual_description": "Cosmic view showing Mercury, Venus, and Earth in alignment.",
                "generation_prompt": "Stylized orbital view of inner solar system rocky planets.",
                "source_start_char": start2,
                "source_end_char": end2,
            },
            {
                "narration_text": part3,
                "visual_description": "Rocket ship voyaging into deep starry cosmos.",
                "generation_prompt": "Sleek rocket traversing deep starfields, cinematic warm tones.",
                "source_start_char": start3,
                "source_end_char": end3,
            },
        ]

        projection, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=script_version.id,
            scene_specs=scene_specs,
        )

        self.assertEqual(len(scenes), 3)
        self.assertEqual(projection.scene_count, 3)

        # Source span verification for all scenes
        for idx, scene in enumerate(scenes):
            source_span_text = script_version.text[
                scene.source_start_char : scene.source_end_char
            ]
            self.assertEqual(source_span_text, scene.narration_text)
            self.assertEqual(scene.order_index, idx)
            self.assertTrue(scene.is_active)
            self.assertFalse(scene.review_flags.get("visual_review_needed", False))

        # Projection text round trip: slice projected_text using projection scene_spans
        for span_info in projection.scene_spans:
            sliced = projection.text[
                span_info["start_char"] : span_info["end_char"]
            ]
            self.assertEqual(sliced, span_info["narration_text"])

        # Spliced text exactly equals scenes joined by double newline
        expected_projected_text = f"{part1}\n\n{part2}\n\n{part3}"
        self.assertEqual(projection.text, expected_projected_text)

        # Verify distinguished fields
        self.assertEqual(scenes[0].visual_description, "Sun shining brightly in space with solar flares.")
        self.assertEqual(
            scenes[0].generation_prompt,
            "Minimalist digital illustration of a radiant sun, warm ambient lighting.",
        )
        self.assertNotEqual(scenes[0].narration_text, scenes[0].visual_description)
        self.assertNotEqual(scenes[0].visual_description, scenes[0].generation_prompt)

    def test_invalid_source_span_rejected_without_state_change(self) -> None:
        """Verify invalid spans or mismatched span text are rejected with InvalidSpanError."""
        script_text = "Scene one text. Scene two text."
        script_version = create_script_version(
            user=self.user_a,
            project_id=self.project_a.id,
            text=script_text,
        )

        # Span out of bounds
        bad_specs_oob = [
            {
                "narration_text": "Scene one text.",
                "source_start_char": 0,
                "source_end_char": 9999,
            }
        ]
        with self.assertRaises(InvalidSpanError):
            initialize_scenes_from_script(
                user=self.user_a,
                project_id=self.project_a.id,
                script_version_id=script_version.id,
                scene_specs=bad_specs_oob,
            )

        # Mismatched text slice
        bad_specs_mismatch = [
            {
                "narration_text": "Completely wrong text",
                "source_start_char": 0,
                "source_end_char": 15,
            }
        ]
        with self.assertRaises(InvalidSpanError):
            initialize_scenes_from_script(
                user=self.user_a,
                project_id=self.project_a.id,
                script_version_id=script_version.id,
                scene_specs=bad_specs_mismatch,
            )

        # Ensure no scenes were persisted
        self.assertEqual(Scene.objects.filter(project=self.project_a).count(), 0)
        self.assertIsNone(get_current_script_projection(self.user_a, self.project_a.id))

    def test_stable_scene_ids_after_order_changes_and_persistence_reload(self) -> None:
        """
        Verify scene UUIDs survive reordering independently of order index,
        reopened projects reproduce exact accepted order, and projection updates atomically.
        """
        script_text = "First paragraph. Second paragraph. Third paragraph."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)

        p1 = "First paragraph."
        p2 = "Second paragraph."
        p3 = "Third paragraph."
        s1 = script_text.index(p1)
        s2 = script_text.index(p2)
        s3 = script_text.index(p3)

        projection, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": p1, "source_start_char": s1, "source_end_char": s1 + len(p1)},
                {"narration_text": p2, "source_start_char": s2, "source_end_char": s2 + len(p2)},
                {"narration_text": p3, "source_start_char": s3, "source_end_char": s3 + len(p3)},
            ],
        )

        id_1, id_2, id_3 = scenes[0].id, scenes[1].id, scenes[2].id

        # Reorder scenes to: [Scene 3, Scene 1, Scene 2]
        new_order = [id_3, id_1, id_2]
        updated_proj = reorder_scenes(
            user=self.user_a,
            project_id=self.project_a.id,
            new_scene_order_ids=new_order,
            expected_projection_rev=projection.projection_rev,
        )

        self.assertEqual(updated_proj.projection_rev, projection.projection_rev + 1)
        self.assertEqual(updated_proj.active_scene_ids, [str(id_3), str(id_1), str(id_2)])
        self.assertEqual(updated_proj.text, f"{p3}\n\n{p1}\n\n{p2}")

        # Simulate reload from database (reopening project)
        reloaded_scenes = get_active_scenes(self.user_a, self.project_a.id)
        self.assertEqual(len(reloaded_scenes), 3)

        # Verify exact identities survived reordering independently of index
        self.assertEqual(reloaded_scenes[0].id, id_3)
        self.assertEqual(reloaded_scenes[0].order_index, 0)
        self.assertEqual(reloaded_scenes[0].narration_text, p3)

        self.assertEqual(reloaded_scenes[1].id, id_1)
        self.assertEqual(reloaded_scenes[1].order_index, 1)
        self.assertEqual(reloaded_scenes[1].narration_text, p1)

        self.assertEqual(reloaded_scenes[2].id, id_2)
        self.assertEqual(reloaded_scenes[2].order_index, 2)
        self.assertEqual(reloaded_scenes[2].narration_text, p2)

        # Single source of truth query returns updated reordered projection
        current_script = get_current_script_text(self.user_a, self.project_a.id)
        self.assertEqual(current_script, f"{p3}\n\n{p1}\n\n{p2}")

    def test_invalid_reorder_requests_rejected(self) -> None:
        """Verify reordering rejects duplicate IDs, alien IDs, or incomplete sets."""
        script_text = "A. B."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": "A.", "source_start_char": 0, "source_end_char": 2},
                {"narration_text": "B.", "source_start_char": 3, "source_end_char": 5},
            ],
        )

        # Duplicate ID
        with self.assertRaises(InvalidSceneOrderError):
            reorder_scenes(
                user=self.user_a,
                project_id=self.project_a.id,
                new_scene_order_ids=[scenes[0].id, scenes[0].id],
                expected_projection_rev=proj.projection_rev,
            )

        # Alien UUID not in active set
        alien_uuid = uuid.uuid4()
        with self.assertRaises(InvalidSceneOrderError):
            reorder_scenes(
                user=self.user_a,
                project_id=self.project_a.id,
                new_scene_order_ids=[scenes[0].id, alien_uuid],
                expected_projection_rev=proj.projection_rev,
            )

        # Missing one scene
        with self.assertRaises(InvalidSceneOrderError):
            reorder_scenes(
                user=self.user_a,
                project_id=self.project_a.id,
                new_scene_order_ids=[scenes[0].id],
                expected_projection_rev=proj.projection_rev,
            )

    def test_conflicting_transactions_and_mismatched_source_versions_rejected(self) -> None:
        """
        Verify that concurrent or stale projection and scene edits are rejected,
        transactions roll back cleanly, and committed work is preserved.
        """
        script_text = "Sentence one. Sentence two."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": "Sentence one.", "source_start_char": 0, "source_end_char": 13},
                {"narration_text": "Sentence two.", "source_start_char": 14, "source_end_char": 27},
            ],
        )

        target_scene = scenes[0]

        # Stale projection revision update attempt
        with self.assertRaises(MismatchedSourceVersionError):
            update_scene_narration(
                user=self.user_a,
                project_id=self.project_a.id,
                scene_id=target_scene.id,
                new_narration_text="Updated sentence one.",
                expected_scene_rev=target_scene.rev,
                expected_projection_rev=999,  # Stale!
            )

        # Verify rollback: scene narration and projection unchanged
        target_scene.refresh_from_db()
        proj.refresh_from_db()
        self.assertEqual(target_scene.narration_text, "Sentence one.")
        self.assertEqual(proj.text, "Sentence one.\n\nSentence two.")
        self.assertEqual(proj.projection_rev, 1)

        # Stale scene revision update attempt
        with self.assertRaises(MismatchedSourceVersionError):
            update_scene_narration(
                user=self.user_a,
                project_id=self.project_a.id,
                scene_id=target_scene.id,
                new_narration_text="Updated sentence one.",
                expected_scene_rev=999,  # Stale!
                expected_projection_rev=proj.projection_rev,
            )

        # Perform valid update
        updated_scene, updated_proj = update_scene_narration(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=target_scene.id,
            new_narration_text="Sentence one revised.",
            expected_scene_rev=target_scene.rev,
            expected_projection_rev=proj.projection_rev,
        )

        self.assertEqual(updated_scene.narration_text, "Sentence one revised.")
        self.assertEqual(updated_scene.rev, 2)
        self.assertTrue(updated_scene.review_flags.get("visual_review_needed"))
        self.assertEqual(updated_proj.projection_rev, 2)
        self.assertEqual(updated_proj.text, "Sentence one revised.\n\nSentence two.")

        # Historical narration versions recorded
        self.assertEqual(updated_scene.narration_versions.count(), 2)

    def test_original_input_strict_preservation_throughout_all_scene_operations(self) -> None:
        """
        Verify OriginalInput remains strictly immutable and unmutated across
        script version creation, scene planning, narration edits, reordering, and deletion.
        """
        orig = OriginalInput.objects.get(project=self.project_a)
        orig_raw = orig.raw_text
        orig_sha = orig.content_sha256
        orig_words = orig.word_count
        orig_bytes = orig.byte_count

        # 1. Create script version
        sv = create_script_version(
            user=self.user_a,
            project_id=self.project_a.id,
            text="Alpha script text.",
        )

        # 2. Initialize scene
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": "Alpha script text.", "source_start_char": 0, "source_end_char": 18}
            ],
        )

        # 3. Edit scene narration
        update_scene_narration(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scenes[0].id,
            new_narration_text="Beta script text revised.",
            expected_scene_rev=1,
            expected_projection_rev=1,
        )

        # 4. Check OriginalInput in database
        orig.refresh_from_db()
        self.assertEqual(orig.raw_text, orig_raw)
        self.assertEqual(orig.content_sha256, orig_sha)
        self.assertEqual(orig.word_count, orig_words)
        self.assertEqual(orig.byte_count, orig_bytes)

        # 5. Direct modification attempt raises ImmutableOriginalInputError
        with self.assertRaises(ImmutableOriginalInputError):
            orig.raw_text = "Illegal overwrite"
            orig.save()

    def test_scene_removal_from_active_order_and_provenance_preservation(self) -> None:
        """
        Verify removing a scene preserves its historical record and provenance
        while re-indexing active scenes and updating the script projection.
        """
        script_text = "Scene 1. Scene 2. Scene 3."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": "Scene 1.", "source_start_char": 0, "source_end_char": 8},
                {"narration_text": "Scene 2.", "source_start_char": 9, "source_end_char": 17},
                {"narration_text": "Scene 3.", "source_start_char": 18, "source_end_char": 26},
            ],
        )

        # Remove Scene 2 from active order
        scene_2 = scenes[1]
        updated_proj = remove_scene_from_active_order(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scene_2.id,
            expected_projection_rev=proj.projection_rev,
        )

        self.assertEqual(updated_proj.scene_count, 2)
        self.assertEqual(updated_proj.text, "Scene 1.\n\nScene 3.")
        self.assertEqual(updated_proj.active_scene_ids, [str(scenes[0].id), str(scenes[2].id)])

        # Scene 2 record still exists in database (provenance preserved for history/renders)
        scene_2.refresh_from_db()
        self.assertFalse(scene_2.is_active)
        self.assertIsNone(scene_2.order_index)

        # Active scenes re-indexed
        active = get_active_scenes(self.user_a, self.project_a.id)
        self.assertEqual(len(active), 2)
        self.assertEqual(active[0].id, scenes[0].id)
        self.assertEqual(active[0].order_index, 0)
        self.assertEqual(active[1].id, scenes[2].id)
        self.assertEqual(active[1].order_index, 1)

    def test_scene_narration_restoration(self) -> None:
        """Verify restoring historical narration text updates projection and appends version record."""
        script_text = "Original narration text."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {"narration_text": script_text, "source_start_char": 0, "source_end_char": len(script_text)}
            ],
        )
        scene = scenes[0]

        # Edit to v2
        scene, proj = update_scene_narration(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scene.id,
            new_narration_text="Second narration revision.",
            expected_scene_rev=1,
            expected_projection_rev=1,
        )
        self.assertEqual(scene.narration_text, "Second narration revision.")
        self.assertEqual(proj.text, "Second narration revision.")

        # Edit to v3
        scene, proj = update_scene_narration(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scene.id,
            new_narration_text="Third narration revision.",
            expected_scene_rev=2,
            expected_projection_rev=2,
        )
        self.assertEqual(scene.narration_text, "Third narration revision.")

        # Restore v1
        restored_scene, restored_proj = restore_scene_narration(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scene.id,
            target_narration_version_number=1,
            expected_scene_rev=3,
            expected_projection_rev=3,
        )
        self.assertEqual(restored_scene.narration_text, "Original narration text.")
        self.assertEqual(restored_proj.text, "Original narration text.")
        self.assertEqual(restored_scene.narration_versions.count(), 4)

        # Historical SceneNarrationVersion is immutable
        hist_v1 = restored_scene.narration_versions.get(version_number=1)
        with self.assertRaises(ImmutableSceneNarrationError):
            hist_v1.text = "Illegal edit"
            hist_v1.save()

    def test_visual_updates_do_not_alter_narration_or_projection(self) -> None:
        """Verify updating visual description and generation prompt leaves narration and projection untouched."""
        script_text = "Narration words."
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text=script_text)
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[
                {
                    "narration_text": script_text,
                    "visual_description": "Initial description",
                    "generation_prompt": "Initial prompt",
                    "source_start_char": 0,
                    "source_end_char": len(script_text),
                }
            ],
        )
        scene = scenes[0]

        updated_scene = update_scene_visuals(
            user=self.user_a,
            project_id=self.project_a.id,
            scene_id=scene.id,
            visual_description="Updated description",
            generation_prompt="Updated prompt",
            expected_scene_rev=scene.rev,
        )

        self.assertEqual(updated_scene.visual_description, "Updated description")
        self.assertEqual(updated_scene.generation_prompt, "Updated prompt")
        self.assertEqual(updated_scene.narration_text, script_text)

        # Projection is unchanged
        proj.refresh_from_db()
        self.assertEqual(proj.text, script_text)
        self.assertEqual(proj.projection_rev, 1)

    def test_cross_user_isolation_rejects_unauthorized_access(self) -> None:
        """Verify user B cannot access or mutate user A's scripts, scenes, or projections."""
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text="Secret text.")
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[{"narration_text": "Secret text.", "source_start_char": 0, "source_end_char": 12}],
        )

        with self.assertRaises(ProjectAccessDeniedError):
            get_active_scenes(self.user_b, self.project_a.id)

        with self.assertRaises(ProjectAccessDeniedError):
            get_current_script_projection(self.user_b, self.project_a.id)

        with self.assertRaises(ProjectAccessDeniedError):
            update_scene_narration(
                user=self.user_b,
                project_id=self.project_a.id,
                scene_id=scenes[0].id,
                new_narration_text="Hacked text",
                expected_scene_rev=1,
                expected_projection_rev=1,
            )

    def test_content_mutation_guard_under_render_lock_and_deleted_state(self) -> None:
        """Verify all script and scene mutations are rejected when render lock is active or project is deleted."""
        sv = create_script_version(user=self.user_a, project_id=self.project_a.id, text="Guard text.")
        proj, scenes = initialize_scenes_from_script(
            user=self.user_a,
            project_id=self.project_a.id,
            script_version_id=sv.id,
            scene_specs=[{"narration_text": "Guard text.", "source_start_char": 0, "source_end_char": 11}],
        )

        # 1. Lock project
        self.project_a.render_locked = True
        self.project_a.save()

        with self.assertRaises(ContentMutationLockedError):
            create_script_version(self.user_a, self.project_a.id, "Locked attempt")

        with self.assertRaises(ContentMutationLockedError):
            update_scene_narration(
                user=self.user_a,
                project_id=self.project_a.id,
                scene_id=scenes[0].id,
                new_narration_text="Locked edit",
                expected_scene_rev=1,
                expected_projection_rev=1,
            )

        with self.assertRaises(ContentMutationLockedError):
            reorder_scenes(self.user_a, self.project_a.id, [scenes[0].id], expected_projection_rev=1)

        with self.assertRaises(ContentMutationLockedError):
            remove_scene_from_active_order(self.user_a, self.project_a.id, scenes[0].id, expected_projection_rev=1)

        # 2. Unlock and soft-delete
        self.project_a.render_locked = False
        self.project_a.lifecycle_state = LifecycleState.DELETED
        self.project_a.save()

        with self.assertRaises(ProjectDeletedError):
            update_scene_narration(
                user=self.user_a,
                project_id=self.project_a.id,
                scene_id=scenes[0].id,
                new_narration_text="Deleted edit",
                expected_scene_rev=1,
                expected_projection_rev=1,
            )
