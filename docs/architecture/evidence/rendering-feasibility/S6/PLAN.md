# S6 local feasibility spike — pre-execution plan

Authorized: local/free rendering/caption feasibility only. No AI/provider calls,
paid services, production application, S9, TASKS.md, deployment or purchases.
Current user requirements govern all pass criteria. Prior evidence stays intact.

Read: docs/README.md, ALPHA_PRODUCT_SPEC.md, ARCHITECTURE.md,
ARCHITECTURE_SPIKES.md, DESIGN.md, UX_FLOWS.md, JOB_EXECUTION_MODEL.md,
root AGENTS.md and CLAUDE.md. No docs/AGENTS.md exists; root instructions apply.
S1/S3/S7/S8 reports and process supervision witness inspected; S5 mapping
closure supplies continuous narration and next-scene-start visual semantics.

Primary FFmpeg 9.0.2 lacks subtitles/ass/drawtext. Candidate correction is
deterministic caption PNG overlays, using Pillow RAQM (HarfBuzz/FriBiDi) layout,
with explicit OFL Noto fonts. No FFmpeg replacement or primary-environment change.

Before installation: isolated /private/tmp/s6-render-venv, PyPI binary packages
Pillow 12.0.0 (~5 MB), numpy 2.2.6 (~15 MB), psutil 7.0.0 (~0.3 MB),
fonttools 4.60.1 (~3 MB), uharfbuzz 0.51.0 (~1 MB). Versions/sizes will be
recorded; initial failures retained. Reason: image/caption construction,
vectorized deterministic audio/frame analysis, process resource sampling,
explicit glyph coverage/shaping inspection. No speech/AI models.

Fonts: Noto Sans, Noto Sans Bengali, Noto Sans Devanagari from official
Google Fonts/notofonts repositories, SIL OFL. Download to temporary private
runtime only, not repository. Record source/license/hash; do not redistribute
font binaries as spike evidence. Pillow RAQM support is checked before use.
Sources: https://pillow.readthedocs.io/en/stable/reference/features.html and
https://github.com/notofonts/bengali (OFL and shaping proof resources).

Render fixtures: 180/300/600 seconds; scene counts based on S5 32 scenes per
171.48 seconds, with deterministic nonuniform durations. One continuous local
synthetic narration WAV per fixture, not one audio file per scene; no quality
claim. Deterministic marked images, caption cues, quiet generated music.
Use fixed 1920x1080/30fps, libx264/AAC, one worker lane, bounded threads.
Scene timing tolerance: first output frame whose timestamp is not before the
mapped next start; maximum 1/30 second quantization, fixed before execution.
AAC/container duration tolerance: one AAC frame plus one video frame (about
55 ms at 48 kHz). Full audio decode/sample coverage and comparison to expected
continuous mix, not -shortest or exit 0, establish narration coverage.

Output checks include full decode, stream/container/duration, scene markers,
caption timing/presence/safe placement, no black/gap frames, motion and audio
continuity. Compare controls ON/OFF, visual beginning/middle/end and multilingual
conjunct shaping. Failures retain previous export; publish only after validation.
Process-group cancellation/recovery preserve lock until cessation, and reject
malformed inputs/outputs. Render runs in a separate worker process; no HTTP
request must remain open. All code is disposable under spikes/rendering-feasibility.
