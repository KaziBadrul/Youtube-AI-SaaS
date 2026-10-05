# Owner boundary review and visual timing clarification — 2026-10-05

The owner reported checking every supplied transition clip and finding all OK. Record all 62 reviewed transition regions for Calls 4 and 6 as owner-approved at the listening scope. This supplies the previously missing human scene-transition review; no numerical boundary-error tolerance or exact word/sample annotation was returned.

The owner clarified that image changes use the next scene narration start, not the previous narration end. The original sheet displayed pause midpoints; those remain historical candidates, not the current visual scheduling rule. Use each transition's recorded `right_word_start` as the visual marker. The previous image covers the pause. The first image covers source start and the last image continues through source duration. Source narration remains continuous; ordinary image transitions do not splice audio.

## Focus transitions under the clarified rule

| Source | Scene 19 → 20 image change | Scene 20 → 21 image change |
|---|---:|---:|
| Call 4 | 112.020s | 119.780s |
| Call 6 | 109.600s | 117.120s |

The original Call 6 pause midpoint markers, 109.400s and 116.680s, are not image transition times under this rule. All next-start times are available in `validation-results.json` as `right_word_start`. Owner approval establishes publishable scene-transition regions in these sources, not independently measured word-level precision or safe source extraction endpoints.

S5 remains **NOT_YET_PASS at the complete accepted gate scope**. Human scene-boundary review is resolved for these two recordings. Structural checks and 13 conservative gate fixtures remain supporting evidence; they do not establish general automatic alignment accuracy, full actual-token correspondence, multi-segment joins or scene-only restoration/reorder extraction. Do not claim those passed solely from owner approval of image transitions. B initial + B whole affected-segment corrections remains selected; no new paid experiment is authorized.

This records the owner decision without changing historical results, source audio or the review sheet. No provider calls, S6/S9, production implementation, TASKS.md, deployment or purchases.
