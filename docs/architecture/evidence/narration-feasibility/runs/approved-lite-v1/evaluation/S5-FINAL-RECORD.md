# S5 final evaluation record

Final owner-defined B + B mapping gate update, 2026-10-05: **S5 PASS** at existing evidence scope. [Final closure](../b-mapping-final-v1/README.md) supersedes historical NOT_YET_PASS conclusions below. Independent owner transition review, explicit fidelity findings, source-bound mappings and deterministic rejection evidence close the continuous B mapping criterion. This does not claim the original broader protocol or safe extraction/restoration joins were executed; all historical evidence is preserved.

Date: 2026-10-04

## Current owner decision — supersedes the historical hybrid below

The owner reported disliking stitching and explicitly selected **B for both initial generation and corrections**. Current policy and evidence are recorded in [b-only-review-v1](../b-only-review-v1/README.md). B + C1 below is historical, not the current policy. Calls 4/6 provide existing coherent initial/corrected evidence. S5 remains **NOT_YET_PASS** pending validated scene/audio mapping; no further C1 splice listening is needed to select the correction strategy.

The alignment-closure `VALID` labels below are provisional ASR coverage labels, not independently reviewed boundary acceptance. The runner does not establish full unexpected-token, repeated-phrase ambiguity or acoustic-boundary rejection. Its synthetic scorer tests do not independently prove that the per-call mapping runner fails closed. Historical C1 trims used stream-copy seeking and differ from requested ranges; they are not sample-exact mapping evidence. These limitations remain recorded rather than converted to PASS.

## S5 final verdict

**S5: NOT_YET_PASS**

The owner selected the B + C1 hybrid after listening to the generated
candidates and reported that all candidates were very good with strong
consistency. That supports the subjective quality decision. It does not prove
the mandatory technical mapping criterion required by S5.

## Selected architecture

### Initial generation — B

Creator-facing narration remains scene-based. Deterministic orchestration groups
contiguous approved scene narration into coherent provider-facing generation
segments. Each segment records its ordered scene membership, exact narration
versions, effective voice/language/delivery, segmentation policy, provider/model
configuration, attempt identity and source provenance.

One scene does not imply one TTS request. A segment may contain multiple
contiguous scenes. The exploratory 3,000-byte cap and historical approximately
500-word heuristic remain evidence inputs, not production constants.

### Edit/correction — C1

When a creator edits an existing scene, the system preserves the previous text,
audio and mapping versions, generates the corrected scene independently, and
stores it as a new immutable source narration version. The derived project
narration may then compose unaffected ranges from the original coherent source
with the corrected scene range from the isolated source.

The system must recompute or review affected timing and alignment, mark
dependent captions/timing/render artifacts outdated as required, and leave
unchanged sibling scenes untouched. C2 context-assisted correction is not the
selected default and must not be introduced as an uncosted fallback.

## Evidence

Objective generation evidence:

- 8 real provider submissions;
- 8 successful, valid WAV outputs;
- 0 retries;
- 0 unknown outcomes;
- 0 capacity failures;
- usage-derived paid-tariff equivalent: **$0.07897**;
- experiment authorization ceiling: **$1.024000**;
- all source WAV hashes and basic audio properties verified;
- source WAVs preserved unchanged.

Owner listening evidence:

- all evaluated candidates were reported as very good;
- voice consistency was reported as strong;
- the owner selected B initial generation plus C1 isolated correction;
- the owner decision did not provide reviewed word timestamps or scene-range
  boundary measurements.

## Mandatory criterion audit

| Criterion | Status | Evidence basis |
|---|---|---|
| Word fidelity | Unresolved | Owner listening was positive, but no ASR or reviewed word-level transcript exists. |
| Voice consistency | Supported by owner listening | Owner reported strong consistency. |
| Prosody continuity | Subjective support only | No quantitative or time-coded score sheet was returned. |
| Pacing continuity | Subjective support only | No reviewed timing score or objective comparison was returned. |
| Generation-segment boundaries | **Unresolved** | No validated Call 4 segment/scene boundary record exists. |
| Technically viable scene/audio mapping | **Unresolved** | Calls 4, 6, and 7 lack reviewed word timestamps and validated mappings. |
| Correction-region naturalness | Subjective support only | Owner reported candidates were very good; no returned time-coded score sheet. |
| Acceptable surgical splice | **Unresolved** | C1 derived audio was prepared, but the required Call 4 scene boundaries and splice evidence were not validated. |
| No clipping | Subjective support only | WAV decoding passed; decoding does not establish no audible clipping. |
| No missing/repeated narration | **Unresolved** | No machine transcription or reviewed word transcript exists. |
| No context leakage | **Unresolved** | C2 context audio was retained for comparison, but no validated C1/C2 word-range mapping exists. |
| Overall publishability | Subjective support only | Owner reported strong quality; mandatory technical evidence remains incomplete. |

The unresolved mapping criterion prevents S5 PASS under the accepted protocol.
The positive listening decision is recorded and does not get rewritten as
objective alignment evidence.

## Artifact and provenance implications

The selected policy requires explicit support for mixed source narration:

```text
Scenes 1–19  → source segment A
Scene 20     → isolated correction source C1
Scenes 21–32 → source segment A
```

Each source remains immutable and retains model, voice, delivery/configuration,
approved text/version, provider provenance and attempt identity. The derived
project narration stores ordered scene ranges, source hashes, mapping versions,
local offsets and join policy. Restoration of different delivery retains that
delivery metadata and does not silently change project-wide voice settings.

If correction generation fails, the current selected narration remains active.
If generation succeeds but alignment or splice validation fails, the output
remains history-only and is not selected as publishable current narration.

## Remaining tuning

S5 intentionally does not freeze:

- final segment byte/token limits;
- final word-count target;
- exact segmentation policy version;
- provider input/output safety margins;
- handling of oversized scenes;
- quota pacing and concurrency settings;
- exact mapping/ASR runtime and confidence thresholds;
- join/pause policy;
- correction timing and caption refresh implementation;
- production cost distribution across representative 3/5/10-minute projects.

These remain bounded implementation and measurement decisions. S9 owns
production economics; this experiment alone does not establish them.

## Remaining architecture gates

S6 and S9 remain unexecuted. S4-R is conditionally passed at its documented
architecture scope. S1, S2, S3, S7 and S8 passed only at their stated local
fixture scopes and retain their limitations.

No additional provider calls, S6/S9 execution, production implementation,
`TASKS.md`, deployment or purchase occurred during this finalization.

## Alignment-closure update

The narrowly scoped local alignment experiment is recorded in
`../alignment-closure-v1/`. The cached `Systran/faster-whisper-base` model was
used locally with word timestamps. The run made no provider calls and preserved
all source WAVs.

The recognizer produced complete mappings for Call 5 Scene 20 and Scenes 20 and
21 in Calls 4 and 6, but Call 4 Scene 19 remains `REVIEW_REQUIRED` because the recognized text
contains `and` where the approved text contains `in`, in addition to a
compound-word split. Call 6 Scene 19 and Call 7 Scene 19 also remain
`REVIEW_REQUIRED` for the compound-word split. Calls 4, 6 and 7 contain other
ASR substitutions/splits outside the focus region. These are not silently
accepted as exact approved-word fidelity.

A deterministic C1-derived full composition and compact Scenes 19–21
comparison were created from the Call 4 Scene 20 candidate range and Call 5.
Because these files were not part of the previous owner listening set, the
current state is **READY_FOR_FINAL_SPLICE_LISTENING**. S5 remains **NOT_YET_PASS**
until the derived splice is listened to and the review-required word/boundary
evidence is resolved.
