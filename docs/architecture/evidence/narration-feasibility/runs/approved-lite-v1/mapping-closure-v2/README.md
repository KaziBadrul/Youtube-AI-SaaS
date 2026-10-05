# S5 local mapping closure — 2026-10-05

## Verdict

**Local reviewed scene/visual mapping: PASS at Calls 4/6 fixture scope. S5 overall: NOT_YET_PASS at the complete accepted protocol scope.** B initial + B affected-segment correction remains owner-selected. The missing mapping evidence for these two continuous sources is now supplied; do not confuse this with proven unattended alignment accuracy or safe audio extraction/restoration/reorder joins.

## Method and measured coverage

Reuse retained Whisper-base word observations, exact approved manifest text, owner-reviewed disagreement findings, explicit article-variation acceptance and approval of all 62 transition regions. Record exact and many-to-one token correspondences separately from authoritative words. No generic fuzzy tolerance or edit-distance cutoff accepts differences. Every non-exact correspondence is whitelisted against the specific owner finding. Every approved index and every recognized index is accounted for exactly once, with scene membership and version provenance.

| Source | Approved tokens accounted | Recognized tokens accounted | Scenes | Unresolved timestamp groups |
|---|---:|---:|---:|---:|
| Call 4 | 498/498 | 504/504 | 32 | 0 |
| Call 6 | 498/498 | 505/505 | 32 | 0 |

This is correspondence coverage under owner review, not an ASR exact-match score. Numeric spellings and split compounds retain group-level ASR ranges rather than invented individual subtoken timestamps. The extra article is explicitly associated with its scene and actual audio range. Approved script/request text remains unchanged.

A sample-exact copy of Call 4 92.1–94.9 seconds was recognized using the existing cached Whisper-base model, CPU int8, no VAD, no text prompt and no prior-text conditioning. It recovered the owner-confirmed `I` at approximately 92.760–93.080 seconds. Cropped estimates for the following words replace overlapping whole-source estimates together in the derived mapping, without changing historical JSON. The scene 18 mapped start becomes 92.760 seconds rather than 92.700. This 60ms estimate refinement creates no new audio splice. `scene18-probe-recognition.json` retains all observations. This is the same recognizer on a different input window, not independent forced alignment; word timestamps remain estimates.

## Visual mapping and B composition

Each scene retains source audio hash/version, exact scene-text hash, ASR provenance, alignment version, token-group references, speech range, visual interval and separate validation state. Source audio is continuous. Image i changes at scene i+1's mapped narration start; preceding image covers the pause. First/last images cover source start/end. Visual intervals cover the full source with no gaps or overlap.

| Source | Scene 19 speech range | Scene 20 speech range | Scene 21 speech range |
|---|---|---|---|
| Call 4 | 98.200–112.020 | 112.020–119.780 | 119.780–122.760 |
| Call 6 | 96.840–109.200 | 109.600–116.240 | 117.120–119.380 |

For Call 6 the image transition times are 109.600 and 117.120 seconds, not the previous scene's end or pause midpoint. The B edit selects Call 6 as the complete replacement source for the same 32-scene membership. Call 4, its text, mappings and provenance remain history; no old source ranges are spliced into Call 6. Other project segments would remain unchanged by policy; this fixture contains only one segment and does not acoustically demonstrate multi-segment joins.

## Fail-closed evidence

Both real derived mappings pass finite ordered token/group range checks, complete once-only expected/recognized accounting, unambiguous scene membership, source version checks and next-start visual continuity. Sixteen mutations of those actual representations are rejected: missing/repeated correspondences, unresolved timestamps, truncation/out-of-range timestamps, unreviewed differences, source-version mismatch, ambiguous scene membership and incorrect visual transition.

Thirteen sequence fixtures also pass, including normal/short/punctuation/pauses, substitution, omission, repetition, repeated phrase/ambiguous boundary, truncation, overlap, scene order and absent acoustic reference. The exact-match witness conservatively rejects repeated phrases; it does not silently choose among plausible matches. These are local structural gates with owner-reviewed inputs, not a production automatic acoustic validation system. New audio does not inherit existing owner approvals; uncertain/unreviewed differences remain non-selectable.

## Remaining scope and uncertainty

For these recordings, the owner-reviewed scene-transition criterion and technically usable continuous-source visual mapping are established. No additional listening is requested for ordinary B scene/image transitions.

The accepted S5 plan also requires safe scene-only restoration and reorder/delete joins using source ranges, and representative/boundary cases beyond this compact single-segment screen. Visual markers are not validated acoustic extraction endpoints; those transformations were not constructed or accepted here. The plan explicitly distinguishes this screen from the full 3/5/10-minute protocol. Those historical requirements are not silently waived. S5 overall therefore remains NOT_YET_PASS, with the Calls 4/6 mapping blocker narrowed to the completed fixture scope. No new provider call is authorized by this conclusion. Exact production segmentation, confidence thresholds, model variability and production economics remain unfrozen; S9 remains unexecuted.

## Reproduction

From repository root:

```sh
python3 spikes/narration-feasibility/local_mapping_closure.py
/private/tmp/s5-align-venv/bin/python spikes/narration-feasibility/local_word_probe.py
python3 spikes/narration-feasibility/local_mapping_closure.py
python3 spikes/narration-feasibility/check_mapping_closure.py
```

The first command creates the probe crop, the second uses local cached weights, the third integrates retained probe observations, and the fourth validates positive/negative cases. No provider SDK or request is used. The model/version/compatibility shim follows `../alignment-closure-v1/environment.json`; no dependency/model was installed or downloaded. If the temporary environment/cache is absent, report the requirement; do not silently fetch it. JSON retains source and derived hashes. Source WAV hashes were reverified unchanged.

No S6/S9, production implementation, TASKS.md, deployment or purchases occurred.
