# S9 revision 11 — final local host-sizing experiment

2026-10-05. **Resource verdict: SAFE_ENOUGH_FOR_ALPHA at the tested local fixture scope. S9: NOT_YET_PASS.** Whole native Linux guest, **2 vCPU / 4 GiB**, no swap, serialized memory-heavy maintenance. All required phases and unchanged media checks completed. Minimum available RAM **1,790,922,752 bytes (1.668 GiB / 41.698% of configured RAM)**; no OOM, swap or failed status probes. This qualifies the 4-GiB class locally without selecting a hosting vendor or claiming a real-provider benchmark.

**Explicit owner decision:** this is the last host-sizing experiment unless it fails. This experiment passed at its stated resource scope; **local host-sizing work is now closed**. Do not automatically schedule smaller/larger/actual-provider sizing experiments because limitations remain documented. No additional sizing experiment was started. Overall S9 financial/operational gates remain separate.

## Isolation, reuse and environment

Read current source-of-truth index/spec/architecture/cost/spike requirements and V10 report/underlying controller, phase, validator and results; reuse V8–V10/S2/S3/S6/S7/S8 evidence already inspected. Same architecture: one persistent guest, minimal Django/Gunicorn status web boundary, controlled Python worker, active SQLite WAL, FFmpeg, local Whisper, captions/fonts and encrypted backup. No production implementation or alternative service.

Reused the stopped **Lima2.2.1 / Apple Virtualization.framework** native ARM64 Ubuntu24.04.5 guest from V10 on Apple M5/macOS26.5. VM retains its old disposable name `s9-v10`; **actual inspection**, not its name, proves this run's 2CPUs/4GiB. Only stopped-VM CPU/RAM configuration and controller hardware assertions changed. Original effective V10 configuration is archived; all historical host evidence remains immutable. Existing guest `/out` and `/work` were moved intact to `/out-v10-preserved` and `/work-v10-preserved`; V11 uses fresh directories. No downloads/installations were needed or performed. No primary Docker/host settings changed.

Kernel **6.8.0-142-generic**, aarch64, Python3.12.3, FFmpeg6.1.1-3ubuntu5, Django5.2.17, Gunicorn23.0.0, faster-whisper1.2.1, CTranslate2 4.8.2, PyAV19.0.1 and the unchanged caption/font stack. Exact package freeze, services, filesystem and kernel in [environment](v11/guest/environment.json). Normal Linux init/SSH/network/logging/admin/services remain inside guest RAM. Scheduled package-maintenance timers paused inside this VM; backup runs only after confirmed heavy-work cessation. No stripping normal services, swap/cache dropping, reduced fixture or weakened validator.

Actual VM allocation **4,294,967,296 bytes (4 GiB)**, 2 vCPU; kernel-visible `MemTotal` **4,094,386,176 bytes**, guest-reserved **200,581,120 bytes** counted in whole-guest unavailable RAM. **No swap/zram/zswap use or swap-in/out activity.** Ext4 root on50GiB virtual disk, all reused media/model/fonts and scratch inside the guest; no host shared mounts/application containers/Rosetta. Source waveform/model/font bytes unchanged.

## Measurements and results

Global `/proc/meminfo`, vmstat, memory/CPU/I/O PSI, kernel logs, RSS/tree diagnostics, disk and loopback web probes include kernel/services/cache and observer overhead. Whole unavailable = configured4GiB minus `MemAvailable`; conventional kernel-visible usage and raw free/cache/slab also retained. **2,225 samples**, median interval0.1045s, max0.1143s. These are sampled peaks/minima, not an exact kernel high-water mark. RSS can double-count shared pages; `MemAvailable` is reclaimable-headroom estimation. No universal safe percentage or production SLA invented.

| Phase | Wall seconds | Peak whole unavailable GB | Minimum available GB | Headroom of4GiB | Result |
|---|---:|---:|---:|---:|---|
| Guest idle | 9.97 sampled | 0.5532 | 3.7418 | 87.12% | Measured |
| Django + worker idle | 10.06 sampled | 0.5841 | 3.7109 | 86.40% | Measured |
| Existing Call4 Whisper | 11.630 | 1.1576 | 3.1373 | 73.05% | PASS |
| Fresh ten-minute render | 180.923 | 0.8818 | 3.4131 | 79.47% | PASS |
| Full media validation | 16.610 | 1.2104 | 3.0846 | 71.82% | PASS |
| Serialized encrypted backup | 1.753 | **2.5040** | **1.7909** | **41.70%** | PASS |
| Cancellation scenario | 2.134 | 0.7099 | 3.5851 | 83.47% | PASS |

GB decimal. Guest-reserved RAM is included in whole pressure. At worst, kernel-visible unavailable RAM2,303,463,424 bytes plus reserved200,581,120 = **2,504,044,544 bytes**. In contrast V10 had31.90MB available and reclaim stalls. This run retains substantial measured reserve without swap. No sampled memory PSI-full increase in any listed phase, no kernel OOM event/counter increase. This is positive evidence for this finite workload, not safety for unbounded retained media or future arbitrary service load.

**886 Django status probes, zero failures/timeouts**. Render p95 **3.26ms**, max **5.27ms**; backup max **2.46ms**. Raw CPU saturation/PSI and all phase probe distributions retained. These minimal private loopback probes do not certify full authenticated3–5-user/HTTPS load or provider speed. Alignment/render timing differences are observations on this machine, not linear vCPU speedup or completion promises.

Backup behavior is byte-identical source code to V10: **311 files / 426,718,638 payload bytes**, in-memory ZIP_STORED + AES-GCM + full authenticated decrypt/hash roundtrip, **426,785,130-byte archive**,1.492s core work /1.753s whole phase. No streaming redesign/compression savings used. Temporary key discarded and stage removed after verification. Memory remains size-proportional; safe retained-volume bounds and off-machine purge/journal/head/key recovery remain open S9/implementation issues, without reopening host-sizing merely by inference.

## Output, cancellation and disk

Freshly encoded112scene ten-minute fixture with captions, gentle motion, music and one continuous narration stream. Scene mappings drive visuals rather than audio cuts. Full unchanged S6 validator: playable MP4/H.264/AAC,1920×1080, exact30fps/600s, successful full decode,18,000frames,111ordered transitions within1/30s, no blank frames,28,800,000 continuous audio samples,56.9456dB reference SNR, no clipping/gaps, captions at beginning/middle/end. Retains documented V9 exact-packet-grid mux adaptation. Synthetic audio proves render continuity, not new narration quality; S5 fidelity/mappings untouched.

**Final MP4 is byte-identical to V10**:59,491,123bytes, SHA256`2c958a022b2f905255c1cba13647e0f2fc89ec98ae820863848404cf90a4a63e`. [Validation](v11/guest/render-result.json), [derived export](v11/guest/s6/exports/linux-600-2c958a022b2f.mp4). All five freshly rendered language fixtures match accepted S6 RGBA pixels exactly, with no fallback/clipping; no new owner listening/visual review required for identical fixtures.

Cancellation terminates live FFmpeg group in **0.129s**, no escalation needed, no live group members/orphans, lock released after confirmed cessation, incomplete output unregistered and previous validated export preserved. Django remains reachable. Force-escalation/host-crash limitations remain those of S3/S7; no production supervisor implemented.

Root used beforework **3.779GB**, sampled peak **4.320GB**, after **3.898GB**, free **46.969GB**. This includes preserved V10 guest evidence, not secretly deleted prior exports. Render scratch107.97MB, final59.49MB, temporary archive426.79MB; candidate moved to final, not double-counted. Backup staging/collection tar are not retained project assets. The50GiB root is an experiment disk allocation, not a frozen production requirement.

## Integrity and verification

[Commands](v11/COMMANDS.md), [plan](v11/PLAN.md), [actual VM inspection](v11/vm-inspection.json), [source adaptation](v11/controller-diff.patch), raw telemetry/probes/kernel logs, hashes and aggregate [RESULTS](v11/RESULTS.json) retained. Phase/web scripts identical to V10; only controller's CPU/RAM assertions changed. Classification is an explicit fixture-specific evidence assessment pinned to summary SHA256; it cannot override failed phases/OOM/swap/probes. No universal percentage threshold selected.

Initial post-run hash inspection assumed the old `/tmp` receipt survived reboot; Ubuntu had cleared it. The empty receipt was correctly rejected, not accepted as source proof. [Initial diagnostic](v11/hash-proof-initial-error.txt). Rebooted the **same** VM solely for byte inspection, re-copied the immutable501-file manifest and confirmed every input hash, then stopped it. No workload or second sizing experiment rerun. Both stop receipts and final process list retained. VM now stopped.

**25 deterministic verification checks PASS**, including actual whole-guest allocation/services, zero swap, phases/serialization/OOM logs, full media hash/validator, source501hashes, five-language equality, cancellation/no orphans, classification/owner stop rule, cost arithmetic/unknown separation and historical preservation. **2,932 pre-existing evidence/script files preserved**, including V10. Only current S9 index updated, with exact prior bytes archived. Earlier uncertainty/failures remain historical rather than rewritten as passes.

## Economics and S9 status

The nominal ~$24/month2-vCPU/4GiB class is now **locally resource-qualified at this finite serialized workload scope**. Actual provider hardware/availability, supervision/network/storage behavior and performance remain untested limitations; no provider selected/provisioned or paid benchmark. Per the owner's stop rule, these caveats do not automatically authorize another sizing experiment. One-host Django/worker/SQLite/local media/FFmpeg topology remains supported; no architecture freeze.

Unchanged V8 nominal price plus illustrative two copies of this measured archive at preserved backup-only tariff = **$24.005932/month partial fixed cost**. $30 ceiling leaves **$5.994068 nominal** before unknown fees/reserve/complete generation costs.10%/20% total-uplift sensitivities leave$3.266795/$0.994068. Uplifts/zero reserve are sensitivities, not owner policy; actual cash fixed cost remains unknown. No subscription prices or allowances selected.

Preserved five-minute image/TTS partial proxy$2.074188 would allow optimistic floors2/1/0 under those sensitivities, **not complete capacity, spending authority or tester allowances**. Expected text/search/image overhead/failures/fees, enforceable whole-project maximum, actual off-machine backup and retention costs remain unresolved. Optional discovery costs do not enter every video; tier names do not become allowances.

**S9: NOT_YET_PASS.** Local resource sizing is closed at the4GiB class. Remaining gates: V7 complete-request token-preflight/expected text usage (untouched), real image size/failure/retry evidence, full expected and maximum exposure, off-machine recovery/purge/independent authority/key custody, retained-volume/version/traffic bounds, actual account prices/taxes/payment/FX/owner reserve, final credit/correction debit and cost-grounded Alpha allowances.

**Single smallest next S9 step:** close the V7 model-specific complete-request input-token preflight gap using retained request envelopes under separately scoped authorization. Not started here. **No further host-sizing experiment unless a failure occurs**, as the owner explicitly directed.

Boundary:0provider/API generation calls,$0paid spend,0new downloads,production/TASKS untouched,no cloud provisioning/public deployment/purchases,original media/history preserved,$30unchanged,no token-preflight/final credits/allowances/architecture freeze. Stop after V11.
