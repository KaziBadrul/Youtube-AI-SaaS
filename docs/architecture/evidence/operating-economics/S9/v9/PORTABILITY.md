# Preserved portability findings and repairs

Original Debian FFmpeg5.1 stream-copy concat output had 18,000 frames but avg_frame_rate 540000/18001 and video duration600.033333. The unchanged strict30fps validator rejected it; output was not registered. Explicit per-clip duration=count/30 reduced accumulated rounding but left a one-tick error (599.999935, avg30.000003...), also rejected. Both derived failures remain intact.

Candidate repair: final video-only stream-copy bitstream filter `setts=pts=N/(30*TB):dts=N/(30*TB):duration=1/(30*TB)`. This assigns the exact frame-grid timestamps already required by Scene Audio Mappings. No H.264 re-encode, frame drop/duplication, narration cuts, audio change or artistic processing. Frame count, every scene transition and continuous audio must pass the original S6 validator; a nicer ffprobe header alone is insufficient.

Official semantics: https://ffmpeg.org/ffmpeg-bitstream-filters.html#setts and version-specific https://www.ffmpeg.org/doxygen/5.1/setts__bsf_8c_source.html (retrieved2026-10-05). Applies only to this known no-B-frame CFR still-image fixture; arbitrary uploaded video/B-frame reorder is outside Alpha/S9 witness and is not blindly retimestamped.

First controller iteration copied an older successful backup receipt after overlap child was OOM-killed. Phase exit/kernel events reject that stale receipt; it is explicitly invalidated, not counted as successful overlap or rewritten as new evidence. The second iteration only copies receipts on successful child exit. Original controller/adapted-render code is archived; this is a disposable evidence-integrity fix, not production implementation. All conclusions use attempt success and validated output, never receipt filename or Docker exit status alone.
