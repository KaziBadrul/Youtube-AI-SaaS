# S5 current decision — B initial + B corrections

## Status and owner decision

Latest local closure: [mapping-closure-v2](../mapping-closure-v2/README.md) establishes owner-reviewed continuous-source scene/visual mapping for Calls 4/6. All expected/recognized tokens are explicitly accounted for; cropped offline recognition recovers the missing `I` range; both mapping representations pass structural checks and 16 bad mutations fail closed. The local mapping screen passes. S5 overall remains NOT_YET_PASS under the complete accepted protocol because safe extraction/restoration/reorder and broader segment evidence are not established by visual transition approval. Earlier missing-review notes below are historical.

Local boundary audit: [boundary-validation-v1](../boundary-validation-v1/README.md) retains 64 provisional scene mappings, verifies ordered word timing, passes 13 fail-closed witness fixtures and supplies 62 sample-exact transition review clips. Independent acoustic reference remains missing; S5 is NOT_YET_PASS. All historical `VALID` ASR labels are treated as REVIEW_REQUIRED for current acceptance.

Latest owner clarification: Call 4 audibly says `curtain in The Wizard of Oz and realize`, matching approved text. The earlier `in/and` clarification request is resolved; see the [fidelity amendment and owner clarification](FIDELITY-POLICY-AMENDMENT.md). Reviewed boundaries and mapping reliability remain unresolved.

Latest fidelity policy: the owner explicitly approved severity-based review and the meaning-preserving `out of a mug` variation. [Amendment](FIDELITY-POLICY-AMENDMENT.md) supersedes the exact-word disqualification reported below. Request provenance and approved text remain unchanged. Material errors and ambiguous mappings remain blocking; S5 is still NOT_YET_PASS.

**S5: NOT_YET_PASS.** The owner reported disliking stitching, then explicitly selected B for both initial generation and corrections. This supersedes the previous B + C1 preference; historical planning, generation, alignment and listening evidence remains unchanged. No objective failure of coherent generation has been established by that preference change.

2026-10-05 owner fidelity update: the completed review resolves many ASR formatting/substitution disagreements, but confirms an extra spoken `a` in both Calls 4 and 6 relative to submitted approved text. These outputs fail current exact-word fidelity; Call 4's `in/and` region also needs clarification. See [owner findings](OWNER-FIDELITY-FINDINGS.md). The remaining work is therefore no longer mapping alone. The completed owner review must not be overwritten by rerunning `review_sources.py`, which generates a blank review sheet.

The original coherent source is Call 4. The corrected coherent source is Call 6, which regenerates Scenes 1–32 with only Scene 20's approved words changed. Use these complete original files, without cutting or stitching scene audio:

- Initial: `../audio/call-04/attempt-04/source.wav`
- Corrected: `../audio/call-06/attempt-06/source.wav`

All eight source hashes, complete PCM decoding and format/duration were reverified in `source-integrity.json`. No source was modified. No new provider call was made.

## Selected behavior

Creator narration remains scene-based. Deterministic grouping produces coherent contiguous provider-facing segments with explicit scene/text-version membership. A scene boundary is a timing/visual mapping inside continuous audio; it does not require an audio cut or separate TTS request.

Editing a scene regenerates its containing segment using the changed approved words and unchanged sibling words. Freeze membership for that correction; do not globally rebatch unaffected segments. Retain all old text/audio/mapping versions and all unaffected segments. A corrected segment is a new immutable source, not an overwrite. Recompute its scene mappings and dependent timing/captions; update later project offsets and invalidate the derived narration/render according to dependencies. Preserve images, with visual review for the edited scene. Explain the affected segment scope and optional cost details truthfully in the scene-facing operation.

Failed generation preserves current selections and records the failed attempt. Technically generated output whose fidelity/alignment validation fails stays in history, without silent publishable selection. No automatic isolated correction or hidden additional paid fallback is selected.

SourceNarrationAudio → SceneAudioMapping[] remains necessary for scene visuals, captions, timing and restoration. Mapping records must retain immutable source/version/hash, scene text version, source ranges, alignment version, validation state/confidence and provenance. Whole-segment replacement selects new mappings for every sibling in that segment; other segments may reference their existing sources. Accepted scene-only historical restoration still requires safe range extraction/joins and explicit compound approval when words differ; it must not silently restore siblings or project-wide voice settings.

## Existing measured correction evidence

| Property | B correction (Call 6) |
|---|---:|
| Requests | 1; zero retries |
| Approved words regenerated | 498 |
| Narration UTF-8 bytes regenerated | 2,887 (excluding style/request overhead) |
| Edited scene words | 23 |
| Unchanged sibling words regenerated | 475 (95.38% of regenerated words) |
| Unaffected narration inside affected segment regenerated | 100% |
| Old source bytes preserved | 100% retained as history; none reused in the selected replacement segment |
| New selected source duration | 170.80 seconds |
| Initial source duration | 171.48 seconds |
| Duration delta | −0.68 seconds |
| Usage-derived paid-tariff equivalent | $0.033128 |
| New mapping work | All 32 scenes of the replacement segment; later global offsets refresh |

Unrelated segments remain reusable by policy; this single-segment fixture does not measure their preservation in a real multi-segment recording. Experiment-wide totals remain eight submissions/eight WAVs, zero retries/unknown outcomes/capacity failures, $0.07897 tariff equivalent within $1.024000 authorization. These are historical tariff equivalents, not independently verified bills or production economics. S9 remains unexecuted.

One initial request per segment and one correction request per affected segment are scope implications, not throughput guarantees. RPM/RPD/TPM are provider/account constraints and need current verification before any future authorized run. Existing quota evidence is historical; it does not establish present remaining capacity. No additional quota was consumed here.

## Exact remaining mapping blocker

Calls 4/6 have local Whisper word timestamps and ordered token comparison, but not reviewed, complete authoritative-text-to-audio mappings. Call 4 matched 483/498 expected tokens; Call 6 matched 486/498 under the original strict tokenizer. Numeric spellings/compound splits explain some disagreements; others may be material (Call 4 `is/was`, missing `I`, `in/and`; both recognize an extra `a` near the mug sentence). ASR output is evidence, not the spoken-word verdict.

`FIDELITY_REVIEW.md` lists exact padded listening windows and approved/recognized disagreements for both sources, with blank findings. Resolving these disagreements by listening is necessary but does not alone establish automatic mapping reliability.

The prior runner's `VALID` labels mean token coverage under its matching logic. They do not prove reviewed acoustic boundaries, absence of unexpected words, repeated-phrase disambiguation or comprehensive fail-closed mapping behavior. Synthetic scorer rejection is not proof that the actual mapping runner rejects every bad mapping. No definitive forced alignment or independent boundary-error reference exists.

Smallest closure work: review disputed audio against exact approved text; create a reviewed boundary reference for Calls 4/6; compare timestamp boundaries against it; retain reproducible failure cases that exercise the actual mapping gate, including repeated phrases and ambiguity. Do not select mappings with unresolved material differences. No model download or extra TTS is inherently required for this review; further local work may reveal additional tool requirements. Owner listening previously supports coherent quality; the strategy change does not request another surgical splice.

B removes the isolated edit splice, not joins between distinct generation segments or scene-only restoration/reorder joins. Those accepted requirements are not waived. Segment byte/word targets, configuration boundaries, oversized-scene handling, alignment runtime/thresholds, pause ownership and quota pacing remain unfrozen. The compact evidence does not establish arbitrary 3/5/10-minute or multi-segment acoustic reliability.

## Reproduction and limits

`review_sources.py` uses Python standard library only to verify retained WAVs and derive disagreement windows from existing JSON; run from any working directory with `python3 review_sources.py` on this workspace. It makes no network/provider calls and does not run ASR, alter audio or certify mappings.

S6/S9 were not executed, production implementation was not started, TASKS.md was not generated, and nothing was deployed or purchased.
