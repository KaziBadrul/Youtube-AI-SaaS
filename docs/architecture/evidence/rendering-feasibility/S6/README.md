# S6 — Rendering and caption feasibility

2026-10-05. **VERDICT: PASS — local feasibility at the documented fixture scope.**
No production application, paid service or provider capability was implemented.
Historical S1–S5/S7/S8 evidence is unchanged. The original FFmpeg capability gap
and first-run failures remain recorded, not rewritten as prior success.

## Runtime

Homebrew FFmpeg/ffprobe **9.0.2**, `/opt/homebrew/Cellar/ffmpeg/9.0.2`.
Supports libx264, AAC, zoompan, scale, overlay, concat and amix; lacks subtitles,
ass and drawtext. Full version/build/filter/encoder inventories are retained.

Viable caption correction: **HarfBuzz 11.3.2 + FreeType 2.13.2** shape/raster
Unicode glyphs; Pillow 12.0.0 composes transparent caption PNGs. FFmpeg overlays
them at deterministic cue times. The Pillow wheel lacked RAQM, so RAQM was not
silently assumed. This is a local Python-worker capability, not another service.
Isolated dependencies are pinned in [requirements.lock](requirements.lock) and
[runtime.json](runtime.json); the primary Python/FFmpeg environment is unchanged.

Fonts: Noto Sans 2.015, Noto Sans Bengali 3.011 and Noto Sans Devanagari 2.007,
from the official Google Fonts repository under SIL OFL 1.1. Sources, licenses,
versions and hashes are in [fonts.json](fonts.json) and retained OFL text files.
Font binaries stay under `/private/tmp/s6-render-fonts`, not in the repository.
Future runtime packaging must preserve these licenses and verify exact font
coverage/shaping; no final product-wide font choice is frozen.

## Environment

macOS **26.5 (25F71)**, arm64 MacBook Air, Apple M5, 10 cores (4 performance /
6 efficiency), **16 GiB RAM**, initial **331 GiB available disk**, Python 3.12.14.
Read-only system/FFmpeg/font inventories: [environment.json](environment.json).
Sandbox-denied system/process inspection and the approved local corrections are
retained in [initial-findings.json](initial-findings.json).

## 3 / 5 / 10 minute results

All final renders: **1920×1080, exact 30 fps, H.264/yuv420p, AAC 48 kHz mono,
MP4 with faststart**, captions/motion/music enabled. These are nonuniform,
S5-density fixtures with 34/56/112 scenes, not trivial two-scene videos.

| Duration | Scenes | Render pipeline wall | Output MB | Scratch peak MB* | Peak FFmpeg RSS MB | Representative FFmpeg CPU** |
|---|---:|---:|---:|---:|---:|---:|
| 3 min | 34 | 44.64 s | 17.88 | 32.47 | 149.62 | 133.5% |
| 5 min | 56 | 79.42 s | 29.43 | 53.38 | 149.95 | 132.7% |
| 10 min | 112 | 237.20 s | 59.55 | 108.16 | 149.98 | 132.5% |

MB are decimal. Wall times include sequential video-clip encoding and final mux,
excluding deterministic input-fixture creation and output validation. The
ten-minute full worker interval, including those stages, was approximately
253.32 seconds from recorded process start through final observer result.
These are measurements on this machine, not completion guarantees or economics.

*Scratch is an observed/conservative upper bound from retained per-scene clips,
logs/recipes and prepublication candidate, not total durable assets/history or
all competing filesystem activity. **100% means one CPU core; sampled cumulative
FFmpeg CPU time divided by render wall excludes Python preparation/validation.
The ten-minute worker/process-tree observed RSS peak was **638.62 MB**, including
validation; it is more representative than FFmpeg memory alone.

Receipts: `project-*-benchmark.json`, `project-*-validation.json`,
[S6-results.json](S6-results.json), attempt command lists and logs under `scratch/`.
First YUV420-motion outputs/receipts remain under `first-motion-420-results/`.

## Scene timing

Visual start comes from the mapped next narration start; previous image covers
the pause, first image begins at zero, and last image covers narration end.
One continuous narration WAV is muxed once; per-scene clips contain **video
only**. Scene mappings never become narration cut instructions.

Every frame's protected color marker was decoded and compared with expected
ordered scene IDs: **32,400 frames** across the three benchmarks, with no missing,
blank or out-of-order frames. Tolerance was declared before execution: first
30fps frame not earlier than mapped start, maximum one frame (**33.333 ms**).
Maximum measured transition error was **32.626 ms**. Exact comparisons are in
per-render validation JSON. Nonuniform durations derive from the accepted S5
mapping pattern; synthetic scaling is explicitly recorded, not presented as
new speech alignment. A separate existing-S5 speech control uses actual mapped
next starts for its first three scenes.

## Captions

**English PASS**: normal/short/long wrapped captions, punctuation, apostrophes,
quotes and numbers. Decoded beginning/middle/end and two-line frames inspected.
54px text, at most two lines, fixed 1600×180 overlay at (160,880); glyphs stay
inside the frame and box. Overlong text is rejected rather than clipped or
silently shrunk. Parameters demonstrate readability, not final UI typography.

| Language | Font | Technical result | Decoded frame |
|---|---|---|---|
| English | Noto Sans | PASS | [frame](frames/language-en-decoded.png) |
| Spanish | Noto Sans | PASS | [frame](frames/language-es-decoded.png) |
| French | Noto Sans | PASS | [frame](frames/language-fr-decoded.png) |
| Bangla | Noto Sans Bengali | PASS | [frame](frames/language-bn-decoded.png) |
| Hindi | Noto Sans Devanagari | PASS | [frame](frames/language-hi-decoded.png) |

Exact strings, line breaks, glyph/cluster data, fonts and visual findings are in
[multilingual-results.json](multilingual-results.json). Codex inspected decoded
MP4 frames, including Bengali ক্ষ/প্র/শ্র and Devanagari क्ष/श्र/ज्ञ shaping;
no broken split marks, missing glyphs, fallback or clipping observed. This is
technical shaping evidence, not translation quality or experimental-language
narration validation. Only English has invitation-quality scope.

Cue metadata is finite, positive, ordered, nonoverlapping and within project
duration. ON/OFF files demonstrate presence/absence; the frame immediately before
and at a cue end is checked by frame index. Disabled captions do not retain a
caption-font/timing blocker. Synthesized tone fixtures establish metadata
rendering, not spoken-word synchronization; S5 supplies speech mapping evidence.

## Motion

**ON/OFF PASS.** Gentle 2.5% centered zoom on every scene, with 3840×2160 input,
YUV444 before zoompan, then delivery YUV420. Initial subsampled crop rounding
failed the predefined one-output-pixel step limit; the correction passed all
benchmark scenes, maximum measured centroid step **0.835 px**, with no black
corners, frame escape or first-image-only bug. Timing is unchanged.

OFF produces identical precompression frame hashes for every control scene;
decoded geometry is stable. Lossy H.264 temporal pixel refinement is retained
as a measurement finding, not mislabeled as motion. [Control results](control-results.json).

## Music

**ON/OFF PASS.** Full-duration locally generated tone/music fixture ends exactly
with the project; no stochastic selection, looping ambiguity or paid asset.
Fixed music gain 0.12; no normalization or time stretching. Full decoded AAC is
compared with the expected narration-only or narration-plus-music signal.

The separate 12-second **existing S5 speech** control demonstrates signal
preservation, music at **17.48 dB below narration RMS**, no clipping and no music
contribution when OFF. Intentional source pauses are preserved; completeness
checks reject missing energy where the reference is active, not legitimate
silence. [Speech/music results](real-narration-results.json). This is not a new
narration-quality/listening-panel claim.

## Cancellation

**PASS.** A substantial 600-second FFmpeg render starts with recorded PID/group,
precise start and boot identities. Cancellation sends SIGTERM and observes exit;
a stubborn two-member group exercises bounded SIGKILL escalation. No tracked
execution remains. Lock releases only after confirmed cessation, incomplete
outputs stay unregistered/private and are quarantined, previous immutable export
hash remains available. Persistent cancellation also blocks the next media step.
[Lifecycle evidence](lifecycle-results.json), `lifecycle-state/` and failure results.

## Interruption / recovery

**PASS, one host only.** Worker deliberately exits while FFmpeg survives. Stale
state retains the lock; incorrect start identity refuses termination. Recovery
inspects/terminates the recorded old group before releasing the lock. Local retry
reuses existing image/audio hashes and produces validated output without AI.
An initial sandbox-denied launch was explicitly inspected/recovered; it was never
counted as a successful export. Host-power loss/multi-host recovery not claimed.

## Output validation

FFmpeg exit 0 alone cannot register an export. Demonstrated checks: existing
file/container, H.264 and AAC streams, 1080p/30fps, duration within the predeclared
one-video-frame plus one-AAC-frame bound (54.667 ms), **full decode**, exact expected
frame count/order/coverage, complete decoded audio sample coverage and signal
comparison, no missing active audio/clipping, caption presence/absence and visual
inspection, seeked beginning/middle/end frames, moov before mdat for faststart.
No output `-shortest` is used as narration proof.

Candidates remain attempt-private until validation; registration pins immutable
file/hash and switches a convenience alias only afterward. Prior validated
exports survive failures/cancellation. [Export registry](export-registrations.json).

## Failure fixtures

**19 input/output/security checks plus lifecycle injections PASS.** Missing/corrupt
image, missing/corrupt narration, invalid mapping/order, out-of-duration caption,
invalid font/overflow, FFmpeg nonzero, incomplete output, missing audio, wrong
resolution, unsafe asset/audio/output paths, actual shaped option-injection text,
disabled-caption branch and persistent cancellation all reject or behave safely.
[Failure results](failure-results.json). Initial harness/capability/motion/float
findings are preserved in `initial-findings.json`, not weakened into passes.

## Security boundary

**PASS at fixture boundary.** Assets resolve through internal IDs/private roots;
display filenames are ignored. Commands are argv lists, never shell strings.
Caption text—including option/shell-looking fixture text—is shaped into pixels,
not filter options. Font choices are curated/hash-verified; output labels and
scratch paths are controlled/unique; escaping paths fail preflight. No complete
upload/tenant system is implemented; S1 remains the authorization-boundary proof.

## Web responsiveness

Django 5.2.17 command persists to disposable SQLite and returns; dispatcher then
starts a **separate Python worker**. During the ten-minute render, **973 status
requests**, mean **0.600 ms**, maximum **8.554 ms**; admission **0.948 ms**.
No HTTP request stays open for the render. Test-client evidence is not browser,
network or production-load validation. [Web witness](web-boundary-results.json).

## Remaining uncertainty / architecture implication

The **one persistent host + Django + Python worker + controlled FFmpeg** design
remains supported. Local caption shaping resolves the workstation's text-filter
gap without another paid service. No material unresolved requirement blocked
this spike, and none was silently changed.

Target-host/Linux builds, full asset-complexity workloads, supervision packaging,
CPU/storage admission limits, font/layout tuning and broader linguistic checks
remain production/operational validation. Benchmark data do not select a host,
guarantee performance, prove Alpha invitation quality or establish economics.
S9 remains unexecuted. Synthetic audio does not establish speech quality.

## Reproduction / evidence inventory

See [disposable scripts and commands](../../../../../spikes/rendering-feasibility/README.md),
[PLAN.md](PLAN.md), environment/build reports, source manifests under `fixtures/`,
per-attempt `commands.json`, validation/failure JSON and [hashes.json](hashes.json).
Fonts/dependencies are temporary local assets; any later setup requires network
permission and matching hashes. No model downloads were used. Independent
reproduction should use a fresh evidence copy to preserve historical results.

**Confirmed: zero AI/provider calls, zero paid services, S9 not executed,
production implementation not started, TASKS.md not generated, nothing deployed
or purchased. All eight original S5 source WAV hashes remain unchanged.**
