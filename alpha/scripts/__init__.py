"""Deterministic script segmentation and estimation services."""
from alpha.scripts.segmentation import (
    COUNTER_VERSION,
    SegmentationError,
    SegmentationStatus,
    admit_scope_authority,
    estimate_script_known_scope,
    estimate_topic_preliminary_scope,
    segment_script,
    update_staged_scope,
)

__all__ = [
    "COUNTER_VERSION",
    "SegmentationStatus",
    "SegmentationError",
    "segment_script",
    "estimate_topic_preliminary_scope",
    "estimate_script_known_scope",
    "update_staged_scope",
    "admit_scope_authority",
]
