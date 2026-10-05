# S5 final B + B mapping closure — 2026-10-05

**S5: PASS at the owner-defined existing B + B narration/mapping evidence scope.** B coherent multi-scene generation is selected for initial narration and whole affected-segment corrections. Continuous narration is not cut at scene boundaries. This supersedes earlier NOT_YET_PASS conclusions under the latest explicit user scope, without rewriting historical findings or claiming the broader original protocol was executed.

## Owner acoustic evidence

The boundary sheet was read unchanged: its 62 finding cells are blank. No OK entries were fabricated. The owner's explicit session statement that every clip was checked and all were OK is retained in `../boundary-validation-v1/OWNER-BOUNDARY-REVIEW.md`. That approval applies to each listed region. No adjusted or uncertain finding was supplied. Explicit row findings take precedence over blanket approval; the parser flags uncertainty and rejects unknown findings or out-of-clip/order-breaking adjustments.

The reviewed sheet proposal remains a pause-midpoint candidate. The next-start image marker is separately recorded under the owner's explicit timing clarification. Owner-reviewed transition regions plus this rule establish usable visual timing; they do not prove exact word onsets or audio-extraction endpoints. Waveform energy and ASR silence are not boundary acceptance evidence.

| Call | Transition | Reviewed proposal | Next-start image timestamp |
|---|---|---:|---:|
| 4 | 18 → 19 | 97.650 | 98.200 |
| 4 | 19 → 20 | 112.020 | 112.020 |
| 4 | 20 → 21 | 119.780 | 119.780 |
| 4 | 21 → 22 | 122.760 | 122.760 |
| 6 | 18 → 19 | 96.010 | 96.840 |
| 6 | 19 → 20 | 109.400 | 109.600 |
| 6 | 20 → 21 | 116.680 | 117.120 |
| 6 | 21 → 22 | 119.590 | 119.800 |

All other transitions have the same approval and structural checks; no repeat review is required. The prior cropped Scene 18 timestamp refinement remains explicitly an ASR estimate.

## Mandatory mapping audit

- Each call maps Scenes 1–32 in order. Visual intervals cover the entire source with no gaps/overlap, using the next scene's start.
- Each accounts for 498/498 expected tokens once. Call 4 accounts for 504/504 recognized tokens; Call 6 accounts for 505/505. No unexplained recognized speech remains.
- Owner fidelity findings resolve all disagreements; the retained offline crop provides a range for the owner-confirmed `I`. No material omission/repetition/order error remains in this evidence. This is not an absolute guarantee against unrecognized speech.
- The accepted extra `a` stays separate from approved text/request provenance and is explicitly represented in token/scene mappings.
- Both real mapping representations pass structural validation. Sixteen damaged representations are rejected; thirteen sequence fixtures pass, including repeated-phrase ambiguity, truncation, omission, repetition, ordering and absent review.
- Call 6 has independently derived mappings, revised Scene 20 text provenance and its own source hash; obsolete Call 4 timing is not reused. Call 4 source and historical mappings remain preserved.
- All eight original source WAV hashes match and complete PCM decoding passes.

Owner listening supports coherent quality; rejection of stitching supersedes C1 preference rather than that evidence. The completed mappings close the remaining owner-defined B + B criterion. Each retains source/text/alignment versions, group correspondence, speech ranges, visual intervals and separate review/extraction states. `b-composition.json` selects the complete Call 6 replacement while preserving Call 4 history; no audio was cut or concatenated.

## Limitations and tuning

PASS is bounded architecture evidence with human review, not general unattended alignment, calibrated confidence or exact per-word acoustic truth. Compounds/numeric spellings have group ASR ranges rather than invented subword timings. New audio requires fresh source-bound review when uncertain. Final rendered captions were not generated/assessed here.

Audio extraction, scene-only restoration, reorder/delete joins and multi-segment joining were not acoustically validated here. Their accepted safeguards remain mandatory; no unsafe cutting, silent regeneration or restoration-scope change is authorized. They are not new owner listening tasks for this explicitly continuous B mapping closure. Original representative 3/5/10-minute and size/configuration tests were not executed by this local run. Earlier uncertainty remains historical evidence.

Segment byte/word targets, provider margins, oversized/configuration-conflict handling, confidence/review thresholds and quota pacing remain unfrozen. S9 owns production economics; S5 does not establish architecture freeze/invitation readiness. Generation history remains eight submissions/eight WAVs, zero retries/unknown/capacity failures, $0.07897 tariff equivalent within $1.024000; not independently reconciled billing. B correction uses one existing request, 498 regenerated words and $0.033128 tariff equivalent; prior history/unrelated segments remain preserved.

## Reproduction and files

Run `python3 spikes/narration-feasibility/check_mapping_closure.py` and `python3 spikes/narration-feasibility/finalize_b_mapping_review.py`. Standard library only; no network, ASR rerun, model fetch or source writes. Outputs: `closure-results.json`, both `call-*-reviewed-mapping.json` files and `b-composition.json`, with source/review/mapping hashes. Prior planning, preflight, generation and review sheets are unchanged.

No further owner action required. Zero provider calls, source WAV modifications or model downloads. S6/S9 and production implementation untouched; no TASKS.md, deployment or purchases.
