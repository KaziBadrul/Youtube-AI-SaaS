# S9 revision 9 — local Linux CPU/RAM envelopes

2026-10-05. **S9: NOT_YET_PASS.** Authorized local/free Linux resource spike only. No production implementation, TASKS.md, deployment/purchase, paid generation, credit policy, tester allowance or architecture freeze. $30/month ceiling unchanged. No S9 V7 token-preflight experiment.

**Finding:** the application workload can complete inside the tested **1-CPU/2-GB cgroup when maintenance is serialized**, but this has little measured RAM margin. The tested full-memory backup overlapping render is **unsafe at 2 GB** (one actual kernel OOM kill). **2 CPU/4 GB completed all tested phases including overlap**. These are application-container findings, not certification of a complete VPS or selection of a host.

## Scope, reused evidence and isolation

Read current source-of-truth index/Alpha specification, accepted architecture, cost/spike constraints, S9 v8's resource/storage/backup findings, existing S5 B+B closure/local model and source receipts, S6 renderer/input/output validation and S8 full-memory backup implementation. Reuse existing 112-scene ten-minute S6 fixtures, initial Call4 source audio, existing Whisper base weights, Noto fonts and historical images. No narration/image/provider regeneration. No changes to approved text, selected S5 mappings, source WAVs or product requirements.

Docker Desktop was already installed but stopped; it was started with explicit tool approval. No Docker Desktop CPU/RAM settings were changed. Cached Python Debian image is **linux/amd64**; tests run under **x86-64 emulation on Apple Silicon**. Test image has Python **3.12.14**, Debian Bookworm/glibc2.36, LinuxKit kernel **7.0.14**, FFmpeg **5.1.9-0+deb12u1**, Django **5.2.17**, Gunicorn **23.0.0**, faster-whisper **1.2.1**, CTranslate2 **4.8.2**, PyAV **19.0.1** and the recorded Pillow/HarfBuzz/FreeType/font stack. Exact package freeze/environment in each profile's `environment.json`; image identity in [image inspection](v9/image-inspect.json).

Software setup was documented before installation: disposable Debian FFmpeg/libgomp packages (~131 MB archives) plus pinned PyPI dependencies (~160+ MB wheels), approximately **300 MB package downloads**, no paid service. Image size **1,598,677,378 bytes** from Docker inspection (layer size, not complete host disk minimum). Existing Whisper base model **145,217,532 bytes** and companion tokenizer/config/vocabulary were copied locally into `/private/tmp/s9-v9-model` and mounted read-only; [original hash receipt](v9/local-model-receipt.json). **No separate Whisper/model-fetch operation** occurred. Faster-whisper's downloaded software wheel contains its bundled VAD asset; do not describe this as zero software/model-asset downloads of every kind. Fonts were mounted read-only, not redistributed as binaries.

Containers ran serially, external networking disabled, no published ports, original repository/model/font mounts read-only and distinct derived-output mounts writable. Private HTTP requests used container loopback only. No cloud/account/provider submission or production web deployment. Test containers are stopped; Docker Desktop and the reusable disposable image remain available, without altering unrelated containers.

## Exact resource limits and measurement

User's 2/4 GB labels are modeled as **decimal 2,000,000,000 / 4,000,000,000 bytes**, not silently 2/4 GiB. Linux page-rounds them down to **1,999,998,976 / 3,999,997,952** bytes. CPU CFS quotas are **100000/100000** and **200000/100000** (one/two CPU equivalents). `memory-swap` equals memory; `memory.swap.max=0` verifies **no swap**. PIDs capped at256. Startup verifies actual cgroup limits before workload execution; a preserved initial preflight failure revealed page rounding and ran no workload.

[Docker resource documentation](https://docs.docker.com/engine/containers/resource_constraints/), retrieved2026-10-05, supports these hard CPU/memory/no-swap controls. Cgroups constrain aggregate application usage; they do not turn shared host CPU into a native dedicated VPS core. CPU throttling counters are retained. Container `/proc` can expose the host CPU count; explicit encode/inference thread limits and quota control bound CPU authority.

Every0.5 seconds the parent sampled total cgroup memory, kernel peak/events, CPU/throttling counters, process RSS sums and writable-output bytes. RSS sums can double-count shared pages; kernel memory peak includes charged cache, so these are distinct measures. A minimal persistent Gunicorn/Django web process, one controlled worker and SQLite WAL status store shared the same envelope. Loopback status probes every~0.25 seconds persisted latency/failure receipts during phases. This is not production ORM load, authenticated browser/network/concurrent-user or public latency certification.

| Test | Kernel memory peak | OOM kills | Failed web probes | Application result |
|---|---:|---:|---:|---|
| 1 CPU / 2 GB, overlap | 1.999999 GB | 1 | 0 | FAIL_OR_PARTIAL |
| 2 CPU / 4 GB, overlap | 2.252620 GB | 0 | 0 | PASS |
| 1 CPU / 2 GB, serialized | 1.972355 GB | 0 | 0 | PASS |

**Full-host limitation:** Docker's Linux VM reports ~8.32 GB total RAM and10 CPUs. The guest kernel, Docker daemon, underlying VM and some host/cache overhead sit outside each application cgroup. Whole-server OS, SSH/reverse proxy, supervision/monitoring and 3–5-user workload overhead remain unvalidated. The serial2-GB application peak is **1.972355 GB (~1.837 GiB)**, leaving only **27.645 MB** below the requested2-GB cap; binary2-GiB hosts differ, but that is not proof their OS margin suffices. Four-GB peak **2.252620 GB (~2.098 GiB)** has more application headroom. Native shared-host timing/contention remains UNKNOWN. Do not infer a validated minimum host RAM from these local application results.

## Workloads and measured results

1. **Standalone full-memory backup sensitivity:** five independent project namespaces,60 historical image files each, one existing five-minute48-kHz synthetic narration and one existing five-minute export/project plus SQLite snapshot. **311 files,426,714,542 uncompressed payload bytes;426,781,033-byte encrypted ZIP_STORED archive**. No compression/dedup savings. SQLite backup API, local AES-GCM encryption, authenticated plaintext/hash roundtrip plus stored-file hash receipt; temporary key discarded. No remote upload, full-volume S8 deletion-journal/provider purge/key recovery or operational restore claim.
2. **Ten-minute render:** existing112 scenes,1920×1080/30fps H.264/AAC, gentle motion, caption overlays and music. One continuous narration input; mapped starts drive visuals, not narration cuts. Original S6 thresholds remain unchanged.
3. **Overlap stress:** launch another full-memory backup15 seconds into render while web stays alive. This is maintenance-concurrency stress, not authorization for two production generation jobs. At2GB the backup child exited**-9**, kernel recorded**oom_kill=1**; web/render survived. At4GB overlap completed and authenticated archive hashes verified, OOM0.
4. **Alignment resource phase:** tool-free local CPU/int8 Whisper base transcription of existing Call4 (171.48s), beam5, word timestamps and VAD, existing PyAV compatibility shim, no network/models fetched. This establishes model load/transcription resource feasibility, not newly accepted word fidelity/scene boundaries or production alignment implementation. Existing S5 maps remain authoritative.
5. **Cancellation:** live FFmpeg process group receives SIGTERM, bounded3s SIGKILL fallback exists, actual graceful cessation<0.3s, no live group members. Incomplete video never enters success registry. Both successful profiles preserve the prior validated export and pass SQLite integrity. Forced escalation/restart supervision and physical host crash were not newly exercised here; preserve S3/S7 limits.

| Profile | Phase | Wall time | Sampled current-memory peak | Web p95 | Result |
|---|---|---:|---:|---:|---|
| 2cpu-4gb | backup_standalone | 3.801s | 1.970 GB | 3.61 ms | PASS |
| 2cpu-4gb | backup_overlap | 5.051s | 2.117 GB | 14.15 ms | PASS |
| 2cpu-4gb | render | 276.289s | 0.941 GB | 7.67 ms | PASS |
| 2cpu-4gb | alignment | 29.747s | 1.275 GB | 5.13 ms | PASS |
| 1cpu-2gb-serial | backup_standalone | 3.809s | 1.854 GB | 3.09 ms | PASS |
| 1cpu-2gb-serial | render | 100.512s | 1.042 GB | 53.42 ms | PASS |
| 1cpu-2gb-serial | alignment | 50.520s | 1.245 GB | 49.22 ms | PASS |

Four-GB full render phase **276.289s** includes encoding/mux/full validation; encoding+initial mux receipt **249.134s**. Local alignment **29.747s**. Initial one-CPU encodes/mux took roughly **383.026s including the failed metadata check**; its default concat output was not publishable. The one-CPU repaired serial confirmation **100.512s** reuses those encoded clips and performs corrected mux/full validation while Django stays live, then alignment **50.520s**. It is **not a100-second fresh render benchmark**. No repeated scene encoding or invented comparable successful first-run wall time. Separate successful frame-grid repair also retains its own time/commands. These emulated timings do not predict native provider speed or operating economics.

Recorded writable-output disk peaks: ~**538.729 MB** first failing overlap (includes leftover failed archive), **430.948 MB**4GB, **426.842 MB** serialized2GB. These include transient archives/intermediates/candidate and logs, not only render scratch. Mounted source fixtures, image layers/model/fonts/baseOS are additional once-counted disk; don't multiply scratch by creator count or count one moved candidate twice. Root disk size/latency/full-disk behavior was not constrained/tested. The witness footprint is small relative to candidate50/80GB roots, but retained real images/versions/logs and complete base disk margin remain unresolved.

## Linux FFmpeg portability finding and exact repair

The unchanged Mac/S6 stream-copy concat recipe on Debian FFmpeg5.1.9 produced18,000 frames, but `avg_frame_rate=540000/18001`, video duration600.033333. The strict original30fps check correctly **rejected** it. Adding explicit clip durations=count/30 reduced drift but left599.999935s/one-track-tick rounding; this also failed unchanged tolerance. Both failed derived artifacts and logs remain preserved; no registration as successful, no tolerance relaxation.

Candidate Linux mux repair: video-only stream-copy bitstream filter

`setts=pts=N/(30*TB):dts=N/(30*TB):duration=1/(30*TB)`.

This assigns the exact frame grid required by this controlled still-image/no-B-frame fixture, without reencoding, dropping/duplicating frames, audio cuts or changed narration source. [Official setts semantics](https://ffmpeg.org/ffmpeg-bitstream-filters.html#setts) and [5.1 source](https://www.ffmpeg.org/doxygen/5.1/setts__bsf_8c_source.html), retrieved2026-10-05. It is not general timestamp repair for arbitrary uploaded/B-frame media. This is a documented disposable runtime compatibility adjustment, not a new production architecture or frozen FFmpeg policy.

The repaired outputs pass **full** existing S6 validation: MP4, H.264/AAC,1920×1080, exact30/1,600s,18,000 decoded frames,111 ordered mapped transitions within1/30s, no blank frames, complete continuous synthetic narration samples, >20dB reference-mix SNR (measured~56.94dB), no clipping/gaps, captions present at beginning/middle/end. No success is inferred merely from ffprobe metadata/FFmpeg exit0. Hashes and recipes under profile folders; source audio/images remain immutable.

First disposable controller iteration also copied a prior successful backup receipt after the overlap child failed. The aggregator rejects/invalidate-marks that **stale receipt** using child exit/OOM evidence. It cannot override failure or become a success. The corrected subsequent controller copies a receipt only after successful child completion. [Portability/integrity history](v9/PORTABILITY.md) and original controller/source archives preserve the mistake; it is not rewritten out of history. These are witness fixes only.

## Caption-platform check

Fresh Linux HarfBuzz/FreeType/Pillow captions using the existing fonts and known S6 strings for **English, Spanish, French, Bangla and Hindi** match their previously visually validated S6 references **byte-for-byte in decoded RGBA pixels**. All five: fallbackfalse, clippingfalse. [Caption receipts/screens](v9/captions/captions-result.json). This is stronger than merely seeing glyphs; it ties shaping/wrapping to known reference output, without claiming translation quality. No new owner visual review required for these identical fixtures. Fonts/source/reference assets unchanged.

## Economics/architecture consequences

V8 candidate prices and cash qualifications are reused, not refreshed or selected: nominal$12 one-CPU/2GiB host and$24 two-CPU/4GiB host remain alternatives, with$30 total ceiling. The small application envelope is **not disproved** by failed overlap: serialization worked locally. Nevertheless, almost-full application RAM and missing wholeOS proof mean the$12 VM cannot yet be certified. FourGB has stronger measured application headroom, but its$24 nominal host leaves only~$5.995 under the V8 partial-backup/zero-uplift sensitivity; that is not a full variable generation budget or allowance. Do not select by cheap headline or silently enlarge budget.

One-host Django + controlled worker + SQLite + host-local media + FFmpeg remains supported **at this local application scope**, with maintenance scheduling/memory bounds needing validation. No new render service, Redis, managed database or active object-storage architecture introduced. S8's full-memory ZIP/AES prototype is unsuitable for unbounded retained volume: archival RAM grows with bytes. Serialization is a tested local option, not frozen production policy; staging/streaming may reduce memory, but no production backup implementation is chosen here.

Still unresolved for S9: full Linux guest/OS and actual host margins/performance/recovery; production backup memory/throughput, off-machine purge/restore/journal/key custody; real selected-image sizes/failures/retries; complete expected project cost and enforceable whole-project maximum (including untouched V7 token-preflight); tax/payment/FX and owner reserve; retained versions/traffic/base disk; credits/edits and cost-grounded Alpha capacity/allowances. No credits or prices invented, no S9 PASS merely from successful local phases.

**Single smallest useful next step:** a separately authorized whole-Linux-guest2GB resource check (OS/supervision included) with serialized maintenance and these existing artifacts. The present near-cap result cannot answer that full-host sizing question. No paid cloud benchmark or provisioning implied; any required additional VM/runtime download must be disclosed before proceeding. Do not automatically start another revision.

## Verification, preservation and reproducibility

**38 aggregate verification assertions PASS**, including rejection of the observed2-GB OOM/stale receipt; that does not turn the failing workload into PASS. Successful profiles verify actual limits, no swap/OOM, full output coverage/timing/audio/caption checks, cancellation/previous-export preservation, web probes, unchanged original model weights and five-language exact reference pixels. Raw per-phase outcomes remain explicit.

**All2,034 pre-existing evidence/script files unchanged**, including originalS5 WAVs andS6 fixtures/exports. Live S9 index previous bytes archived before its new pointer; [before manifest](v9/preservation-before.json). Model originals rehashed. No historical evidence writer rerun. [Results](v9/RESULTS.json), each profile's environment/samples/probes/receipts, [commands](v9/COMMANDS.md), [plan](v9/PLAN.md) and image build log retain exact inputs/resource flags and failures. Source hashes for disposable implementation:

- `Dockerfile`: `61f34f438e67c061300e11f561442f091dac3da87376f194a00d4cc775d544ad`
- `captions.py`: `32b07687d8908915272991ccbc0fe752fdd4d66c33ea12c0e9ed0b3885d55472`
- `controller.py`: `aa171bc7b5de0808c17d74a7be0e37e75f6cd2f0863a321cc51151cec6c867ee`
- `grid_remux.py`: `5b49c2b993bcb97f4dc2d54c52f8956db38ae9e38d9773c7ddd714b9c3785fc8`
- `phase.py`: `f5c621ee53ea9eb98c1139f25646c210337277853f001a454f2f36994fe42bdf`
- `remux_check.py`: `8b7d6c32057254735e3d9e322b604be1e4a56799efc0b4df6e644d7e00adfcc8`
- `serial_controller.py`: `87ff94cd859f67adc9798f7e18087b0e281b6506facac2495802067fb1056832`
- `serial_phase.py`: `ccecf73e368ede80a879f2994ff2d33a9368f223444a00c33c873449adb518e7`
- `summarize.py`: `5589caedbae7bc87f3ac563a5280d066a8f233b097e253c411cf6cd73ef3b44a`
- `web.py`: `5003368c347a95eafafd1fb97cb2dcd5a3926aa9365e905d827acac52a8ecfdc`

Boundary confirmation: **zero AI/provider generation calls; $0 paid spend; Debian/PyPI dependency downloads only, no separate Whisper weight/model fetch; original source media unchanged; production/TASKS.md untouched; no deployment/provisioning/account/purchase; no V7 preflight or final credits/allowances; S9 NOT_YET_PASS.** Stop after V9.
