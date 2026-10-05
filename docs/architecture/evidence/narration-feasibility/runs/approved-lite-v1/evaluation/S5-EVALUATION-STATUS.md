# S5 evaluation status

**Status: READY_FOR_OWNER_LISTENING**

The listening package is ready, but automated word-fidelity and scene-audio
alignment evidence is blocked in this environment. No strategy is selected and
S5 is not passed.

## Evidence integrity

All eight expected provider WAVs exist under `../audio/`. The SHA-256 values
match `S5-GENERATION-RESULTS.json` exactly. All eight decode successfully as
mono, 24,000 Hz, 16-bit PCM WAV files.

| Call | Manifest purpose | Duration | Bytes | SHA-256 verified |
|---:|---|---:|---:|---|
| 1 | A, Scene 19 original | 13.72 s | 664,626 | yes |
| 2 | A, Scene 20 original | 7.80 s | 380,466 | yes |
| 3 | A, Scene 21 original | 2.76 s | 138,546 | yes |
| 4 | B/C shared initial, Scenes 1–32 | 171.48 s | 8,237,106 | yes |
| 5 | A/C isolated, edited Scene 20 | 8.12 s | 395,826 | yes |
| 6 | B, edited Scenes 1–32 | 170.80 s | 8,204,466 | yes |
| 7 | C context, edited Scenes 19–21 | 23.56 s | 1,136,946 | yes |
| 8 | Restoration, original Scene 20 alternate delivery | 8.84 s | 430,386 | yes |

Manifest association is unambiguous through the retained attempt receipts,
audio paths, and matching hashes. The eight WAV sources were not modified.

## Word fidelity

The manifest establishes the approved input text and the generation outputs are
valid audio, but it does not establish what was spoken. No local transcription
or forced-alignment result was available:

- `faster_whisper` is not installed and no model weights are present.
- `rapidfuzz`, `numpy`, `soundfile`, `scipy`, and `librosa` are not installed.
- `score_alignment.py` scores reviewed word-timestamp JSON; it does not
  transcribe audio.

Therefore missing, added, repeated, changed, truncated, unexpected, and
pronunciation-error words remain unestablished automatically. Human listening
is required for the supplied candidates. Machine evidence must not be inferred
from duration or silence detection.

## Alignment

Reliable automated Scene Narration Text → Source Narration Audio mapping is not
established. Calls 4, 6, and 7 have no word timestamps. FFmpeg silence detection
can identify quiet intervals, but it cannot identify word boundaries or prove
that a boundary belongs to Scene 19, 20, or 21. I therefore did not use guessed
boundaries to fabricate B/C comparison files.

The exact blocker is: **no offline ASR/forced-alignment runtime and model
weights are available for Calls 4, 6, or 7, and no reviewed word-boundary JSON
exists for those calls.**

Smallest next step: either provide an already-installed offline alignment
runtime with its model weights, or manually review the Calls 4, 6, and 7 audio
and supply reviewed ordered word timestamps/boundaries. No provider request is
needed for this step.

## Listening package

Directory: `evaluation/`

- `candidate_alpha.wav` — A initial comparison: Calls 1 + 2 + 3.
- `candidate_beta.wav` — isolated correction comparison: Calls 1 + 5 + 3.
- `candidate_gamma.wav` — Call 4 source, full coherent baseline.
- `candidate_delta.wav` — Call 6 source, full coherent correction.
- `candidate_epsilon.wav` — Call 7 source, context-assisted correction.
- `candidate_zeta.wav` — Call 8 source, alternate-delivery restoration.
- `LISTENING_SCORE_SHEET.md` — blank owner score sheet.
- `private-listening-map.json` — private label mapping; do not use it to
  pre-populate scores.

Recommended listening order: alpha, beta, gamma/delta, epsilon, then zeta
against the original Scene 20 source Call 2. The A and isolated-correction
assemblies use deterministic stream-copy concatenation only. No crossfade,
normalization, time stretching, pitch correction, or other concealment was
applied.

The required B baseline-region, C isolated replacement, C context replacement,
and B full-regeneration region files remain pending reviewed Call 4/6/7 scene
boundaries.

## Objective correction comparison

Measured from the completed experiment manifests. “Unaffected regenerated” is
the approved text outside edited Scene 20 that was included in the paid
request; it is not a quality judgment.

| Comparison | Requests | Approved words in request | UTF-8 bytes | Unaffected words regenerated | Unaffected percentage | Usage tariff equivalent | Source preservation | Alignment work |
|---|---:|---:|---:|---:|---:|---:|---|---|
| A isolated Scene 20 correction (Call 5) | 1 | 23 | 120 | 0 | 0% | $0.001575 | Calls 1 and 3 retained; Call 2 retained in history | Scene 20 only, subject to review |
| B full coherent correction (Call 6) | 1 | 498 | 2,887 | 475 | 95.38% | $0.033128 | Call 4 remains retained; corrected source is a new full segment | Full 498-word segment must be remapped |
| C context-assisted correction (Call 7) | 1 | 73 | 407 | 50 | 68.49% | $0.004572 | Call 4 remains retained; only Scene 20 may be selected after review | 73-word context mapping required; 23 words selected |
| Restoration alternate delivery (Call 8) | 1 | 23 | 124 | 0 | 0% | $0.001713 | Original Call 2 retained; Call 8 is a separate version | Scene 20 range must be reviewed |

Duration observations: Call 6 is 0.68 s shorter than Call 4; Call 5 is 0.32 s
longer than Call 2; Call 7 is 23.56 s; Call 8 is 1.04 s longer than Call 2.
These are duration differences only and do not establish fidelity, boundary
quality, or splice quality.

## Objective disqualifications

No candidate is objectively disqualified yet by measured word fidelity or
mapping failure because those measurements were not available. No candidate is
eligible to pass: mandatory fidelity and reviewed mapping evidence are still
missing. Subjective scores must remain blank until owner listening.

## Remaining S5 work

Return the completed score sheet with, for each applicable candidate:

1. scores from 0–2 or N/A for each dimension;
2. time-coded notes for any missing/repeated/changed words, clipping,
   unexpected speech, boundary defect, audible splice, or context leakage;
3. whether word fidelity is a definite 2 or ambiguous;
4. whether Call 8 sounds materially different in delivery from Call 2;
5. if possible, reviewed Scene 19/20/21 start/end boundaries for Calls 4, 6,
   and 7, or an offline alignment result.

Owner listening is required before any A/B/C strategy decision. This evaluation
does not mark S5 PASS.

## Scope confirmation

- Zero additional provider requests were made.
- Gemini was not called.
- Original generated WAVs were not modified.
- S5 was not marked PASS.
- No strategy was selected.
- S6 and S9 were not executed.
- Production implementation was not started.
- `TASKS.md` was not generated.
- Nothing was deployed or purchased.
