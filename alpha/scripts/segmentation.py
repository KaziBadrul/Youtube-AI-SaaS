"""
Deterministic sentence segmentation and staged scope review.

Implements versioned deterministic local rules for counting sentences,
producing exact script character spans, identifying structural ambiguities,
and enforcing downstream scope admission without external provider or LLM calls.
"""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import hashlib
import re
from typing import Any

COUNTER_VERSION = "s9-local-terminal-punctuation-v1"

# Terminal punctuation pattern covering English, Latin, and Bengali/Hindi scripts:
# . ! ? । (U+0964) ॥ (U+0965) followed by optional closing quotation or bracket,
# followed by whitespace or end of text.
TERMINAL = re.compile(r'''[.!?।॥]+["'”’»)\]}]*(?=\s|$)''')

# Structural ambiguity and concern patterns
AMBIGUITY_PATTERNS = {
    "abbreviation_or_initial": r"\b(?:Dr|Mr|Mrs|Ms|Prof|Sr|Jr|etc|vs|e\.g|i\.e)\.|\b[A-Z]\.",
    "decimal_or_numeric_punctuation": r"\d[.,]\d",
    "ellipses": r"\.{2,}|…",
    "quotation_or_bracket": r'''["“”‘’«»()\[\]]''',
    "no_whitespace_after_terminal": r"[.!?।॥][A-Za-z]",
    "line_or_list_structure": r"\n\s*(?:[-*#]|\d+[.)])",
}

# Frozen S9 tariff and exposure bounds
OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD = Decimal("0.0336")
HISTORICAL_IMAGE_ATTEMPT_MAX_USD = Decimal("0.139264")
PRELAUNCH_CEILING_USD = Decimal("40.00")

MISSING_COST_COMPONENTS = [
    "research/script real project usage",
    "factual checking where applicable",
    "image input/text/thinking",
    "TTS request usage",
    "justified retry distribution",
    "render/compute",
    "retained storage/backups/egress",
    "tax/fees/FX",
]


class SegmentationStatus:
    LOCAL_FIXTURE_VALID = "LOCAL_FIXTURE_VALID"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID_EMPTY = "INVALID_EMPTY"


class SegmentationError(Exception):
    """Base exception for deterministic segmentation errors."""
    pass


def segment_script(text: str) -> dict[str, Any]:
    """
    Deterministically segment script text into exact sentence spans and count.
    Preserves all approved characters, quotes, and punctuation.
    Flags structural ambiguity without using LLM calls.
    """
    if not isinstance(text, str):
        raise ValueError("script must be text")

    spans: list[dict[str, Any]] = []
    cursor = 0

    def append_span(left: int, right: int) -> None:
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if any(c.isalnum() for c in text[left:right]):
            spans.append({
                "start": left,
                "end": right,
                "text": text[left:right],
            })

    for match in TERMINAL.finditer(text):
        append_span(cursor, match.end())
        cursor = match.end()
    append_span(cursor, len(text))

    concerns: list[str] = []
    for name, pattern in AMBIGUITY_PATTERNS.items():
        if re.search(pattern, text):
            concerns.append(name)

    if spans and not TERMINAL.search(spans[-1]["text"]):
        concerns.append("unterminated_tail_counted_as_one_fragment")

    if not spans:
        status = SegmentationStatus.INVALID_EMPTY
    elif concerns:
        status = SegmentationStatus.REVIEW_REQUIRED
    else:
        status = SegmentationStatus.LOCAL_FIXTURE_VALID

    return {
        "counter_version": COUNTER_VERSION,
        "script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "sentence_count": len(spans),
        "predicted_image_count": len(spans),
        "spans": spans,
        "review_flags": concerns,
        "segmentation_status": status,
        "text_length": len(text),
        "word_count": len(text.split()),
    }


def credit_estimate(minutes: int | float | Decimal | None = None) -> Decimal:
    """
    Preliminary credit calculation for topic requests (minutes / 5).
    Default is 5 minutes (1.0 credit).
    """
    dur = Decimal(5) if minutes is None else Decimal(str(minutes))
    if not dur.is_finite() or dur <= 0:
        raise ValueError("positive finite duration required")
    return dur / Decimal(5)


def estimate_topic_preliminary_scope(minutes: int | float | Decimal | None = None) -> dict[str, Any]:
    """
    Calculate preliminary topic-duration heuristic estimate (approx 12 images/min).
    The 12/minute heuristic does not grant authority or fix final scene count.
    """
    dur = Decimal(5) if minutes is None else Decimal(str(minutes))
    credits = credit_estimate(dur)
    predicted_count = int(dur * 12)

    return {
        "phase": "TOPIC_PRELIMINARY",
        "predicted_images": predicted_count,
        "credit_estimate": str(credits),
        "credit_state": "PRELIMINARY_DURATION_ESTIMATE",
        "image_output_expected_USD": str(Decimal(predicted_count) * OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD),
        "image_output_rate": {
            "model": "gemini-3.1-flash-lite-image",
            "USD_per_1K_image": str(OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD),
            "source": "Owner-fixed S9 tariff; prior analysis.json, 2026-10-05",
        },
        "complete_expected_USD": None,
        "unresolved_components": MISSING_COST_COMPONENTS,
        "qualification": "Known image-output subtotal only, not complete cost or financial authority",
    }


def estimate_script_known_scope(script_scope: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate remaining scope once an approved script is known.
    Predicted generated images equals exact deterministic sentence count.
    Credits remain unresolved pending post-script policy.
    """
    count = script_scope["sentence_count"]
    return {
        "phase": "SCRIPT_KNOWN",
        "predicted_images": count,
        "credit_estimate": None,
        "credit_state": "UNRESOLVED_POST_SCRIPT_POLICY",
        "image_output_expected_USD": str(Decimal(count) * OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD),
        "image_output_rate": {
            "model": "gemini-3.1-flash-lite-image",
            "USD_per_1K_image": str(OWNER_FIXED_IMAGE_OUTPUT_TARIFF_USD),
            "source": "Owner-fixed S9 tariff; prior analysis.json, 2026-10-05",
        },
        "complete_expected_USD": None,
        "unresolved_components": MISSING_COST_COMPONENTS,
        "qualification": "Known image-output subtotal only, not complete cost or financial authority",
    }


def calculate_consumption(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize recorded execution spending and credit events."""
    known_credits = sum(
        (Decimal(str(e["credits"])) for e in events if e.get("credits") is not None),
        Decimal(0),
    )
    pending = [e["attempt_id"] for e in events if e.get("credits") is None]
    recorded_usd = sum(
        (Decimal(str(e["USD"])) for e in events if "USD" in e),
        Decimal(0),
    )

    return {
        "events": deepcopy(events),
        "recorded_USD": str(recorded_usd),
        "known_consumed_credits": str(known_credits),
        "total_consumed_credits": None if pending else str(known_credits),
        "pending_credit_policy_attempts": pending,
        "qualification": "All event amounts are synthetic accounting fixtures, not real spend/rates",
    }


def update_staged_scope(
    text: str,
    prior_estimate: dict[str, Any] | None,
    consumed_events: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Update staged estimation once script text is known.
    Replaces topic preliminary heuristic with exact sentence count.
    Preserves prior executed work and avoids double counting.
    """
    script_scope = segment_script(text)
    remaining = estimate_script_known_scope(script_scope)
    spent = calculate_consumption(consumed_events)

    known_plus_image = Decimal(spent["recorded_USD"]) + Decimal(remaining["image_output_expected_USD"])

    return {
        "prior_preliminary_estimate": deepcopy(prior_estimate),
        "script_scope": script_scope,
        "consumed": spent,
        "remaining_estimate": remaining,
        "projected_total": {
            "known_recorded_plus_image_output_USD": str(known_plus_image),
            "complete_expected_USD": None,
            "credits": None,
        },
        "old_estimate_is_not_added_to_total": True,
        "provider_calls": 0,
    }


def admit_scope_authority(
    plan: dict[str, Any],
    authority: dict[str, Any],
    consumed_events: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Downstream scope admission check.
    Verifies that enlarged sentence count (e.g. 214) or preliminary heuristics
    cannot grant financial or provider authority.
    """
    count = plan["script_scope"]["sentence_count"]
    liability = Decimal(count) * HISTORICAL_IMAGE_ATTEMPT_MAX_USD
    spent = Decimal(calculate_consumption(consumed_events)["recorded_USD"])

    reasons: list[str] = []

    if plan["script_scope"]["segmentation_status"] != SegmentationStatus.LOCAL_FIXTURE_VALID:
        reasons.append("SEGMENTATION_REVIEW_OR_INVALID_INPUT")

    if count > authority.get("fixture_authorized_image_count", 0):
        reasons.append("REVISED_SCOPE_REQUIRES_SUFFICIENT_AUTHORIZATION")

    if liability > Decimal(str(authority.get("image_liability_ceiling_USD", "0"))):
        reasons.append("IMAGE_EXPOSURE_EXCEEDS_OPERATION_AUTHORITY")

    if spent + liability > Decimal(str(authority.get("whole_request_ceiling_USD", "0"))):
        reasons.append("WHOLE_REQUEST_EXPOSURE_EXCEEDED")

    # Available monthly budget check against prelaunch ceiling
    shared_ceiling = Decimal(str(authority.get("monthly_operating_ceiling_USD", PRELAUNCH_CEILING_USD)))
    available = (
        shared_ceiling
        - Decimal(str(authority.get("recurring_obligations_USD", "0")))
        - Decimal(str(authority.get("other_spend_USD", "0")))
        - Decimal(str(authority.get("unknown_liabilities_USD", "0")))
        - spent
    )

    if liability > available:
        reasons.append("SHARED_BUDGET_INSUFFICIENT")

    if count > authority.get("available_image_requests", 0):
        reasons.append("PROVIDER_QUOTA_INSUFFICIENT")

    state = (
        "ADDITIONAL_AUTHORIZATION_OR_BUDGET_HANDLING_REQUIRED"
        if reasons
        else "WITHIN_SYNTHETIC_IMAGE_AUTHORITY_ONLY"
    )

    return {
        "state": state,
        "reasons": reasons,
        "conditional_image_liability_USD": str(liability),
        "available_shared_USD_after_consumed_and_holds": str(available),
        "consumed_retained": calculate_consumption(consumed_events),
        "authority_unchanged": deepcopy(authority),
        "maximum_complete_project_exposure": None,
        "can_submit_provider_request": False,
        "provider_calls": 0,
        "qualification": "Financial fixture only. Real quotas and provider enablement ungranted.",
    }
