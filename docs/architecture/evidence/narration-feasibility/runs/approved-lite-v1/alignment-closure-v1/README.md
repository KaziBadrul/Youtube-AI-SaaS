# S5 local alignment-closure experiment

Status: **READY_FOR_FINAL_SPLICE_LISTENING**

This is a disposable local evidence run. It made no provider calls and did not
modify any retained source WAV.

## Method

The existing external alignment implementation is
`../YoutubeAI/python-scripts/make_timestamps.py`. It uses
`faster-whisper` `base` on CPU with `int8`, word timestamps, VAD and RapidFuzz
scene matching. Its fuzzy threshold and normalization are insufficient as the
sole S5 acceptance method because it can skip unmatched scenes and does not
prove complete word coverage.

For this closure run, the locally cached
`Systran/faster-whisper-base` model was used with word timestamps. The approved
manifest text remained authoritative. A conservative ordered sequence alignment
compared every expected token to recognized tokens. Scene mappings were marked
`VALID` only with complete ordered coverage; substitutions, omissions, split
words and other uncertainty were marked `REVIEW_REQUIRED`. Overlap or missing
ranges would be `INVALID`.

Environment and model provenance are in `environment.json`. Raw recognized words,
timestamps, expected tokens, opcodes and every scene mapping are in the three
`call-*-alignment.json` files.

## Coverage and fidelity result

| Call | Expected tokens | Recognized words | Matched | Unmatched expected | Unexpected recognized | VALID scenes | REVIEW_REQUIRED scenes | INVALID scenes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 498 | 504 | 483 | 15 | 21 | 22 | 10 | 0 |
| 5 | 23 | 23 | 23 | 0 | 0 | 1 | 0 | 0 |
| 6 | 498 | 505 | 486 | 12 | 19 | 23 | 9 | 0 |
| 7 | 73 | 74 | 72 | 1 | 2 | 2 | 1 | 0 |

The main recognized substitutions/splits include `AM` → `a .m.`, number-word
forms such as `twelve` → `12`, `twenty-two` → `22`, compound-word splits such
as `middle-aged` → `middle -aged`, and Call 4 `in` → `and`. These cannot be
silently accepted as exact approved-word fidelity.

## Scenes 19–21

| Call | Scene | Start | End | Duration | Coverage | Confidence | Status |
|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 19 | 98.200 | 112.020 | 13.820 | 95.12% | 0.908 | REVIEW_REQUIRED |
| 4 | 20 | 112.020 | 119.780 | 7.760 | 100% | 0.921 | VALID |
| 4 | 21 | 119.780 | 122.760 | 2.980 | 100% | 0.920 | VALID |
| 6 | 19 | 96.840 | 109.200 | 12.360 | 97.56% | 0.945 | REVIEW_REQUIRED |
| 6 | 20 | 109.600 | 116.240 | 6.640 | 100% | 0.912 | VALID |
| 6 | 21 | 117.120 | 119.380 | 2.260 | 100% | 0.968 | VALID |
| 7 | 19 | 0.000 | 13.280 | 13.280 | 97.56% | 0.942 | REVIEW_REQUIRED |
| 7 | 20 | 13.960 | 19.860 | 5.900 | 100% | 0.932 | VALID |
| 7 | 21 | 20.480 | 23.300 | 2.820 | 100% | 0.981 | VALID |

Call 4 Scene 20 has a technically usable candidate range, but the adjacent
Scene 19 mapping is not complete. The run therefore does not establish full
approved narration coverage for the coherent source.

## C1 derived splice

The derived files are:

- `B_C1_DERIVED_FULL.wav`
- `B_C1_DERIVED_SCENES_19_21.wav`

The full composition uses Call 4 through 112.02 seconds, inserts the validated
Call 5 Scene 20 range (`0.0–7.58` seconds; measured PCM trim 7.594667 seconds),
then resumes Call 4 at 119.78 seconds. The measured full output duration is
171.337333 seconds, a -0.142667 second delta from Call 4. The compact Scenes
19–21 file is 24.405333 seconds.

Processing was deterministic PCM WAV trimming and stream-copy concatenation. No
crossfade, normalization, time stretching, pitch correction or concealment was
used. Exact recipes and source hashes are in `composition-manifest.json`.

Because this derived splice was not part of the earlier owner listening set,
the correct S5 state is `READY_FOR_FINAL_SPLICE_LISTENING`.

## Failure behavior

Synthetic/local failure cases are in `failure-case-results.json`. The scorer
rejects substitutions, omissions, repetitions, overlapping ranges and truncated
audio. Ambiguous or incomplete provider mappings remain non-selectable.

## Reproduction

The local run used:

```text
HF_HUB_OFFLINE=1 /private/tmp/s5-align-venv/bin/python /private/tmp/s5_align_closure.py
```

The retained inputs are the exact manifest text and WAV paths from the S5
generation results. The temporary runner was not production code. The
dependency/model details and hashes are retained in `environment.json` and the
per-call JSON files.

## Closure result

The experiment establishes that local word-level alignment is technically
possible and that the selected Scene 20 ranges can be located as candidates.
It does not yet establish complete exact word fidelity for Calls 4/6/7 or a
publishable C1 splice, because Call 4 Scene 19 and other ASR substitutions/split
words remain review-required. Final owner listening of the two derived C1 files
is required before S5 can be marked PASS.
