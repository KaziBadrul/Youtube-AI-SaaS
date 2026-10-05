# S5 boundary and mapping validation — local evidence

Latest update: the owner reviewed all 62 transition clips and reported all OK. [Owner review and clarified visual timing](OWNER-BOUNDARY-REVIEW.md) supersedes the pending human-transition-review status below. Image changes use `right_word_start`, not the historical midpoint candidates. This does not certify exact extraction endpoints or general automated mapping accuracy.

**S5: NOT_YET_PASS.** B initial + B whole affected-segment correction remains selected. This audit establishes structural feasibility, not independent acoustic accuracy.

## Measured result

Calls 4 and 6 source hashes match the retained alignment provenance. PCM decoded; every recognized word has a finite positive-duration range within source duration, and word ranges are ordered without overlap. All 32 scene mappings per source were retained with immutable source hash, scene text version, historical alignment provenance and current validation state. Every current boundary state is **REVIEW_REQUIRED**; historical `VALID` ASR labels are preserved separately rather than promoted to trusted mappings.

There are 62 transition candidates. Candidate visual/timing transitions are midpoints between the left scene's last ASR word end and right scene's first ASR word start. They are neither reviewed acoustic speech ranges nor proposed narration cuts. Initial/corrected B source audio stays continuous. No splice or repaired narration was created.

| Source | Scene 19 → 20 | Scene 20 → 21 | ASR gap at each transition |
|---|---:|---:|---|
| Call 4 | 112.020s | 119.780s | 0.000s / 0.000s |
| Call 6 | 109.400s | 116.680s | 0.400s / 0.880s |

RMS measurements in 20ms neighborhoods are observations, not speech detection. Some ASR-reported pause midpoints contain appreciable signal: Call 4 18→19 is approximately −19.73 dBFS; Call 6 18→19 approximately −16.68 dBFS. Thus ASR gaps cannot establish silence ownership or safe cutting. No thresholds are claimed as acoustic acceptance criteria.

The owner's reviewed numeric/compound differences, confirmed Call 4 `is`, `I`, `in`, and explicitly accepted extra article remain fidelity evidence. A reviewed word's existence does not establish its timestamp. In particular, the missing recognized `I` has no measured individual range; compound splits need many-to-one correspondence, and accepted additional speech must be represented. This audit does not fabricate those word ranges.

## Fail-closed witness

The disposable exact-sequence gate passed 13 fixtures: normal multi-scene, very short scene, punctuation, natural pause, substitution, omission, repetition, repeated phrase near boundary, ambiguous boundary, truncation, overlap, no acoustic reference and cross-scene ordering error. Bad cases are INVALID or REVIEW_REQUIRED. Repeated-phrase matching is intentionally conservative and may reject an otherwise context-resolvable mapping. A structurally clean unique sequence without reviewed acoustic reference is REVIEW_REQUIRED.

These tests validate this isolated gate, not the legacy ASR runner or a production implementation. They do not establish real-world sensitivity or reject every imaginable error. Real owner-approved variations require explicit token correspondence; the fixture gate does not automatically bless substitutions or insertions.

## Exact blocker and smallest next step

No independent time-coded acoustic reference has been supplied for the scene boundaries. WhisperX, torch, torchaudio, transformers, ctc_segmentation and stable_whisper are absent from the existing temporary ASR environment. No dependency or model was downloaded/installed here. The audit reuses existing Whisper output; ASR similarity and ordered timestamps alone are insufficient under the accepted S5 criteria.

Use [BOUNDARY_REVIEW.md](BOUNDARY_REVIEW.md) and its linked source clips. Each clip preserves original mono 24kHz PCM16 samples, from 1.5 seconds before the left endpoint through 1.5 seconds after the right endpoint, rounded to source sample frames. No normalization, fades, stretching or other audio transformation was used. Exact frame ranges and derived hashes are in `validation-results.json`.

For each transition, record OK if it occurs between the specified scene phrases, an adjusted absolute source time if displaced, or uncertain. Prioritize Scenes 18→19, 19→20, 20→21 and 21→22 in both calls, then review the remaining transitions. Do not cut continuous B audio at these markers. An owner-reviewed transition reference can support scene-level visual mapping; exact first/last word ranges and ambiguous word timestamps still require review/refinement. If a clip provides insufficient context, use the full unchanged source. No additional provider request is necessary for this review.

## Reproduction and integrity

Run `python3 spikes/narration-feasibility/validate_mapping_evidence.py` from the repository root. Standard library only; no credentials, SDK or network operations. It reads retained WAV/JSON/text, writes derived boundary clips and evidence, and reruns fixture assertions. Reproduction regenerates the blank boundary sheet; preserve completed owner reviews separately before rerunning.

Sources were hashed before/after this audit and unchanged; all 62 derived WAVs decode with matching recorded hashes. No provider calls, S6/S9, production implementation, TASKS.md, deployment or purchases.
