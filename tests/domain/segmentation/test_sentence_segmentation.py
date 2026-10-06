"""Automated tests for deterministic sentence segmentation and scope review."""
from decimal import Decimal
import unittest

from alpha.scripts.segmentation import (
    COUNTER_VERSION,
    HISTORICAL_IMAGE_ATTEMPT_MAX_USD,
    OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD,
    PRELAUNCH_CEILING_USD,
    SegmentationStatus,
    admit_scope_authority,
    credit_estimate,
    estimate_script_known_scope,
    estimate_topic_preliminary_scope,
    segment_script,
    update_staged_scope,
)


class SentenceSegmentationDomainTests(unittest.TestCase):
    """
    Test suite verifying deterministic local sentence segmentation,
    staged image scope estimation, and downstream scope admission.
    """

    def test_topic_duration_heuristics_versus_known_n_and_repetitions(self) -> None:
        """
        Verify 3/5/10 duration preliminary estimates (12 images/min)
        and ensure known script replaces topic heuristics with exact N.
        """
        # 3, 5, 10 minute preliminary duration estimates
        for minutes, expected_count, expected_credits in [
            (3, 36, "0.6"),
            (5, 60, "1.0"),
            (10, 120, "2.0"),
        ]:
            est = estimate_topic_preliminary_scope(minutes)
            self.assertEqual(est["predicted_images"], expected_count)
            self.assertEqual(Decimal(est["credit_estimate"]), Decimal(expected_credits))
            self.assertEqual(est["phase"], "TOPIC_PRELIMINARY")
            self.assertEqual(
                Decimal(est["image_output_expected_USD"]),
                Decimal(expected_count) * OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD,
            )

        # Fractional duration
        self.assertEqual(credit_estimate(6), Decimal("1.2"))
        self.assertEqual(credit_estimate(), Decimal("1.0"))  # default 5 minutes

        # Invalid duration inputs rejected
        for invalid in [0, -1, "-5"]:
            with self.assertRaises(ValueError):
                credit_estimate(invalid)

        # Build fixture script of 47 sentences
        script_47 = " ".join(
            f"Sentence number {i} describes a distinct concept."
            for i in range(1, 48)
        )

        # Deterministic repetitions: 20 repetitions produce identical results
        first_run = segment_script(script_47)
        self.assertEqual(first_run["sentence_count"], 47)
        self.assertEqual(first_run["counter_version"], COUNTER_VERSION)

        for _ in range(20):
            repeated = segment_script(script_47)
            self.assertEqual(repeated, first_run)

        # Known script updates staged estimate: replaces 60 images with 47
        prior_5min_est = estimate_topic_preliminary_scope(5)
        consumed_events = [
            {"attempt_id": "attempt-research-1", "kind": "research", "USD": "0.008", "credits": None},
            {"attempt_id": "attempt-script-1", "kind": "script", "USD": "0.012", "credits": None},
        ]
        staged = update_staged_scope(script_47, prior_5min_est, consumed_events)

        self.assertEqual(staged["remaining_estimate"]["predicted_images"], 47)
        self.assertEqual(Decimal(staged["consumed"]["recorded_USD"]), Decimal("0.020"))
        # Old preliminary estimate is not added to new total
        self.assertTrue(staged["old_estimate_is_not_added_to_total"])
        self.assertEqual(staged["provider_calls"], 0)
        # Post-script credit conversion is pending, not assumed images / 60
        self.assertIsNone(staged["remaining_estimate"]["credit_estimate"])

    def test_exact_punctuation_unicode_spans_and_ambiguity_fixtures(self) -> None:
        """
        Verify exact terminal punctuation handling across English, Bengali, and Hindi,
        closing quotes/brackets preservation, and structural ambiguity detection.
        """
        witness_cases = [
            {"text": "A fact. A question? Yes!", "count": 3, "flag": None},
            {"text": "Price is 3.14 units. Next.", "count": 2, "flag": "decimal_or_numeric_punctuation"},
            {"text": "Dr. Smith arrived. Next.", "count": 3, "flag": "abbreviation_or_initial"},
            {"text": "Wait... then continue.", "count": 2, "flag": "ellipses"},
            {"text": 'She said "Ready?" Then we left.', "count": 2, "flag": "quotation_or_bracket"},
            {"text": 'He said “Go!” Then she ran.', "count": 2, "flag": "quotation_or_bracket"},
            {"text": "প্রথম বাক্য। দ্বিতীয় বাক্য।", "count": 2, "flag": None},
            {"text": "पहला वाक्य। दूसरा वाक्य।", "count": 2, "flag": None},
            {"text": "Double dari sentence॥ Next sentence.", "count": 2, "flag": None},
            {"text": "Unpunctuated fragment", "count": 1, "flag": "unterminated_tail_counted_as_one_fragment"},
            {"text": "Word. " * 500, "count": 500, "flag": None},
            {"text": "... !!", "count": 0, "flag": None},
        ]

        for case in witness_cases:
            text = case["text"]
            res = segment_script(text)
            self.assertEqual(
                res["sentence_count"],
                case["count"],
                f"Failed for case text: {text!r}",
            )

            # Verify every character span round-trips exactly
            for span in res["spans"]:
                extracted = text[span["start"] : span["end"]]
                self.assertEqual(extracted, span["text"])

            if case["flag"]:
                self.assertIn(
                    case["flag"],
                    res["review_flags"],
                    f"Expected flag {case['flag']!r} in {res['review_flags']}",
                )
                self.assertEqual(res["segmentation_status"], SegmentationStatus.REVIEW_REQUIRED)

        # Empty punctuation string results in INVALID_EMPTY
        empty_res = segment_script("... !!")
        self.assertEqual(empty_res["sentence_count"], 0)
        self.assertEqual(empty_res["segmentation_status"], SegmentationStatus.INVALID_EMPTY)

    def test_pasted_script_known_scope_without_preliminary_heuristic(self) -> None:
        """Verify pasted script reports exact known sentence count without applying 60-image heuristic."""
        script_7 = " ".join(f"Sentence {i} is here." for i in range(1, 8))
        res = segment_script(script_7)
        self.assertEqual(res["sentence_count"], 7)
        self.assertEqual(res["segmentation_status"], SegmentationStatus.LOCAL_FIXTURE_VALID)

        staged = update_staged_scope(script_7, prior_estimate=None, consumed_events=[])
        self.assertEqual(staged["remaining_estimate"]["predicted_images"], 7)
        self.assertEqual(Decimal(staged["consumed"]["recorded_USD"]), Decimal("0"))

    def test_pathological_count_and_scope_admission_enforcement(self) -> None:
        """
        Verify downstream scope admission blocks enlarged counts (e.g. 214)
        when exceeding authorized limits, proving model output cannot enlarge authority.
        """
        script_214 = " ".join(f"Fact number {i} is presented clearly." for i in range(1, 215))
        res_214 = segment_script(script_214)
        self.assertEqual(res_214["sentence_count"], 214)
        self.assertEqual(res_214["segmentation_status"], SegmentationStatus.LOCAL_FIXTURE_VALID)

        events = [
            {"attempt_id": "attempt-1", "USD": "0.010", "credits": None},
        ]
        plan_214 = update_staged_scope(script_214, prior_estimate=None, consumed_events=events)

        authority = {
            "fixture_authorized_image_count": 60,
            "image_liability_ceiling_USD": "8.355840",
            "whole_request_ceiling_USD": "8.50",
            "recurring_obligations_USD": "12.00",
            "other_spend_USD": "0.00",
            "unknown_liabilities_USD": "0.50",
            "available_image_requests": 60,
            "monthly_operating_ceiling_USD": "40.00",
        }

        # Admission check on 214 sentences with 60-image authority
        decision = admit_scope_authority(plan_214, authority, events)

        self.assertEqual(
            decision["state"],
            "ADDITIONAL_AUTHORIZATION_OR_BUDGET_HANDLING_REQUIRED",
        )
        self.assertIn("REVISED_SCOPE_REQUIRES_SUFFICIENT_AUTHORIZATION", decision["reasons"])
        self.assertIn("IMAGE_EXPOSURE_EXCEEDS_OPERATION_AUTHORITY", decision["reasons"])
        self.assertIn("PROVIDER_QUOTA_INSUFFICIENT", decision["reasons"])
        self.assertFalse(decision["can_submit_provider_request"])
        self.assertEqual(decision["provider_calls"], 0)

        # Plan for 47 sentences fits within 60-image authority
        script_47 = " ".join(f"Sentence {i} is concise." for i in range(1, 48))
        plan_47 = update_staged_scope(script_47, prior_estimate=None, consumed_events=events)
        decision_47 = admit_scope_authority(plan_47, authority, events)

        self.assertEqual(decision_47["state"], "WITHIN_SYNTHETIC_IMAGE_AUTHORITY_ONLY")
        self.assertEqual(decision_47["reasons"], [])

    def test_review_required_script_blocks_admission(self) -> None:
        """Verify scripts flagged REVIEW_REQUIRED (e.g. abbreviations) block admission."""
        script_with_abbr = "Dr. Jekyll examined the vial. Mr. Hyde vanished."
        res = segment_script(script_with_abbr)
        self.assertEqual(res["segmentation_status"], SegmentationStatus.REVIEW_REQUIRED)

        plan = update_staged_scope(script_with_abbr, prior_estimate=None, consumed_events=[])
        authority = {
            "fixture_authorized_image_count": 60,
            "image_liability_ceiling_USD": "10.00",
            "whole_request_ceiling_USD": "10.00",
            "recurring_obligations_USD": "0.00",
            "other_spend_USD": "0.00",
            "unknown_liabilities_USD": "0.00",
            "available_image_requests": 60,
            "monthly_operating_ceiling_USD": "40.00",
        }
        decision = admit_scope_authority(plan, authority, [])

        self.assertEqual(
            decision["state"],
            "ADDITIONAL_AUTHORIZATION_OR_BUDGET_HANDLING_REQUIRED",
        )
        self.assertIn("SEGMENTATION_REVIEW_OR_INVALID_INPUT", decision["reasons"])

    def test_budget_and_quota_exhaustion_blocks_admission(self) -> None:
        """Verify budget and quota limits block admission even when count fits authority."""
        script_10 = " ".join(f"Sentence {i}." for i in range(1, 11))
        plan = update_staged_scope(script_10, prior_estimate=None, consumed_events=[])

        # Available quota = 0
        zero_quota_auth = {
            "fixture_authorized_image_count": 60,
            "image_liability_ceiling_USD": "10.00",
            "whole_request_ceiling_USD": "10.00",
            "recurring_obligations_USD": "0.00",
            "other_spend_USD": "0.00",
            "unknown_liabilities_USD": "0.00",
            "available_image_requests": 0,
            "monthly_operating_ceiling_USD": "40.00",
        }
        dec_quota = admit_scope_authority(plan, zero_quota_auth, [])
        self.assertIn("PROVIDER_QUOTA_INSUFFICIENT", dec_quota["reasons"])

        # Available shared budget insufficient
        tight_budget_auth = {
            "fixture_authorized_image_count": 60,
            "image_liability_ceiling_USD": "10.00",
            "whole_request_ceiling_USD": "10.00",
            "recurring_obligations_USD": "35.00",
            "other_spend_USD": "4.00",
            "unknown_liabilities_USD": "0.99",
            "available_image_requests": 60,
            "monthly_operating_ceiling_USD": "40.00",
        }
        dec_budget = admit_scope_authority(plan, tight_budget_auth, [])
        self.assertIn("SHARED_BUDGET_INSUFFICIENT", dec_budget["reasons"])
