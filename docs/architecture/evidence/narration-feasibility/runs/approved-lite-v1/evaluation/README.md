# S5 evaluation workspace

This directory contains derived evaluation material only. The eight retained
provider WAVs under `../audio/` are the immutable sources and were not modified.

## Deterministic derived audio

- `A_COMPARISON.wav`: Calls 1, 2, and 3 concatenated in order with stream-copy
  concatenation. No crossfade, normalization, time stretching, pitch change or
  other audio processing was applied.
- `A_ISOLATED_CORRECTION_COMPARISON.wav`: Calls 1, 5, and 3 concatenated in
  order. This is the directly bounded isolated Scene 20 comparison available
  without Call 4 scene boundaries.

The required Call 4-derived B/C files were not fabricated. No reviewed word or
scene boundaries exist for Call 4, 6, or 7, and no local ASR/forced-alignment
runtime or model weights are available. Silence detection alone is not accepted
as word alignment evidence.

## Neutral listening labels

The following labels intentionally do not reveal strategy names:

| Label | Audio |
|---|---|
| `candidate_alpha.wav` | `A_COMPARISON.wav` |
| `candidate_beta.wav` | `A_ISOLATED_CORRECTION_COMPARISON.wav` |
| `candidate_gamma.wav` | source Call 4 WAV |
| `candidate_delta.wav` | source Call 6 WAV |
| `candidate_epsilon.wav` | source Call 7 WAV |
| `candidate_zeta.wav` | source Call 8 WAV |

The private mapping is in `private-listening-map.json`. It is not a score sheet
and must not be used to pre-populate subjective scores.

## Required owner listening

Use the score sheet in `LISTENING_SCORE_SHEET.md`. Start with the directly
bounded A comparison, then the isolated correction comparison, then the raw
Call 4/6/7 comparison, and finish with Call 8 restoration. The raw Call 4/6/7
files are included for listening context only; their scene boundaries remain
unreviewed.
