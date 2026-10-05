# S5 narration feasibility evidence

[S5 plan, rubric and historical proposed calls](S5-PLAN.md). The authorized
eight-call generation experiment completed, and the owner listening evaluation
selected the B + C1 hybrid policy. **S5: NOT_YET_PASS** because the mandatory
technical scene/audio mapping criterion remains unverified. See the [final
evaluation record](runs/approved-lite-v1/evaluation/S5-FINAL-RECORD.md).

Evidence: fixture-manifest.json, real-call-manifest.json, request-counts.json, local-results.json. Reproduce with `python3 spikes/narration-feasibility/prepare.py`.

Retained initial finding: first preparation run stopped with `AssertionError: source scenes text matches scene JSON`. Inspection found Scene 35 contains extra words in 03_scenes.json. Resolution explicitly pins script.txt as experiment text, records mismatch [35], and keeps original files intact. No claim these versions agree. No failed provider call occurred.

Historical audio calibrates density only. Synthetic sample-range/scoring checks prove local mechanics, not speech quality, provider response format or production reliability. Existing S3/S7 are reused for state/recovery semantics; no production narration infrastructure is created.

The retained generation evidence records eight real provider submissions, eight
valid WAV outputs, zero retries, zero unknown outcomes, and a usage-derived
paid-tariff equivalent of $0.07897 within the authorized $1.024000 ceiling. No
additional provider request was made during evaluation. The owner reported all
listened candidates as very good with strong consistency and selected coherent
multi-scene initial generation (B) plus isolated surgical scene correction (C1).
That decision does not replace the missing reviewed word timestamps and scene
audio mappings for Calls 4, 6, and 7; therefore the gate remains NOT_YET_PASS.
