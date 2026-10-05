# S9 revision 10 — whole-Linux-guest 1 vCPU / 2 GiB

2026-10-05. **Resource verdict: MARGINAL. S9: NOT_YET_PASS.** All measured phases completed without swap or OOM, but serialized full-memory backup reduced available RAM to **31,903,744 bytes (30.43 MiB; 1.486% of configured RAM)**. Completion does not establish safe operating headroom. **The approximately $12/month 2-GiB host class is not resource-qualified.** No hosting provider selected; no architecture/budget/credit/allowance change.

## Scope and source evidence

Read current docs index/Alpha specification, architecture/cost/spike requirements, S9 v8/v9/index and underlying V9 scripts/results, S6 renderer/benchmarks/validator, S2 SQLite, S3 child supervision, S7 publication and S8 encryption/restore evidence. Reused existing S6 112-scene ten-minute assets, original Call4 WAV, local Whisper base weights, Noto fonts, historical images and an existing five-minute export. No provider media regeneration. Historical V1–V9 reports/scripts/results remain intact; earlier uncertainty is not rewritten.

[Raw evidence](v10/), [aggregate verification](v10/RESULTS.json), [plan](v10/PLAN.md), [exact commands](v10/COMMANDS.md), [disposable implementation](../../../../../spikes/operating-economics/v10/). This is a local/free feasibility witness, not a production service, deployment or Alpha invitation-quality test. V7 token preflight was not performed.

## Complete guest mechanism and environment

**Lima 2.2.1 + Apple's native Virtualization.framework (`vz`)**, ARM64 Linux on an ARM64 Apple M5/macOS 26.5 host, 16 GiB host RAM. [Official mechanism](https://lima-vm.io/docs/config/vmtype/vz/) and [installation](https://lima-vm.io/docs/installation/), retrieved2026-10-05. No Rosetta/x86 emulation, Docker/application container, separate application-memory limit or changed Docker settings. A genuine separate Linux kernel boots in the constrained VM.

Guest: **Ubuntu 24.04.5 LTS**, **6.8.0-142-generic** kernel, **aarch64**, Python **3.12.3**, FFmpeg **6.1.1-3ubuntu5**, Django **5.2.17**, Gunicorn **23.0.0**, faster-whisper **1.2.1**, CTranslate2 **4.8.2**, PyAV **19.0.1**, Pillow **12.0.0**, HarfBuzz binding **0.52.0**, cryptography **46.0.3**. Exact native package freeze and FFmpeg build in [environment](v10/guest/environment.json).

[Actual VM inspection](v10/vm-inspection.json), effective config and guest inspection establish **1 vCPU**, **2,147,483,648 bytes configured RAM (2 GiB)** and **50 GiB sparse virtual disk**. Guest `MemTotal` is **2,053,734,400 bytes**; **93,749,248 bytes** of configured RAM are guest-reserved/non-MemTotal memory. No swap device/file/zram/zswap use: `SwapTotal=0`, swap-in/out counters zero throughout. No swap-assisted completion, cache dropping, overcommit change or OOM suppression.

Systemd/init, SSH, network/resolver/time services, journald/rsyslog, cron, D-Bus, normal guest administration/services and monitoring run inside the same RAM envelope. All 20 running service names are retained. Scheduled apt maintenance timers are paused **only in this disposable guest** to honor serialized heavy maintenance; ordinary services were not stripped out to obtain a pass. Web binds guest loopback; no public app port is deployed. Lima's SSH administration is host-loopback only; no primary SSH keys/agent forwarded.

All fixtures/model/fonts/work/scratch are copied onto guest **ext4**, with **no host shared mounts**. Thus guest filesystem/page cache participates in global measurement. Host hypervisor/APFS caching can affect timing and is outside guest RAM, as underlying hypervisor resources would also be outside a VPS; this does not exclude the Linux kernel/services from the measured envelope. Actual provider CPU/storage/kernel behavior is untested.

## Downloads and preservation

[Download record](v10/downloads.json), bootstrap/setup logs and official checksums: Lima **38,328,082 bytes**, Ubuntu ARM64 server image **620,224,512 bytes**, apt metadata ~39.3 MB, apt packages ~108 MB, native PyPI wheels ~124.3 MB; **~930.2 MB material transfer**, plus small metadata, with display-size rounding rather than an exact network byte meter. No QEMU/second guest-agent archive needed. Faster-whisper's software wheel includes its bundled VAD asset; **no separate Whisper base weights, font or provider-media download**. Existing weights/fonts were copied locally. Lima cache/tool/VM files remain disposable under `/private/tmp` and the normal verified-image cache; VM is now **stopped**.

**501 copied input files** (494 repository media/renderer/font-metadata files + four model files + three font binaries) hash-match the originals inside the guest after execution. [Source proof](v10/guest-source-verification.json). All **2,646 pre-existing evidence/script files** remain unchanged except the live S9 index, whose exact prior bytes are archived. [Preservation results](v10/preservation-result.json). Production and TASKS.md were not touched.

## Measurement definitions and limits

Telemetry uses **global** `/proc/meminfo`, `/proc/vmstat`, kernel logs and memory/CPU/I/O PSI, not container RSS/cgroup alone. Capture guest total/free/available RAM, cache/buffers/slab, swap, OOM counters, all-process and application-tree RSS sums, CPU, output bytes and filesystem usage. RSS sums may double-count shared pages and are diagnostic only.

Primary whole-guest pressure below = **configured 2-GiB RAM minus MemAvailable**. This explicitly includes guest-reserved RAM; the aggregate also records the conventional kernel-visible `MemTotal - MemAvailable` and raw `MemTotal - MemFree`. `MemAvailable` estimates reclaimable headroom rather than declaring every cached byte irrecoverably consumed. Samples nominally every0.1s: actual median **0.1052s**, max **0.1465s**; **3,453 samples**. Peaks/minima are **sampled**, not an exact kernel memory high-water mark. Probes/controller/diagnostic overhead are inside the guest; 10-second baselines include the lightweight measurement worker. No universal safe-memory percentage or production SLA is invented.

## Phase results

Decimal GB/MB; headroom percent uses configured2GiB. Web/worker/SQLite remain active across heavy phases. Fresh scene encodes, not V9's reused encode set.

| Phase | Wall seconds | Peak whole unavailable GB | Minimum available MB | Headroom | Swap | Result |
|---|---:|---:|---:|---:|---:|---|
| Guest idle baseline | 9.92 sampled | 0.4400 | 1707.44 | 79.51% | 0 | Measured |
| Django + worker baseline | 10.06 sampled | 0.3956 | 1751.88 | 81.58% | 0 | Measured |
| Whisper alignment | 67.738 | 0.8654 | 1282.08 | 59.70% | 0 | Completed |
| Fresh ten-minute render | 254.701 | 0.6079 | 1539.57 | 71.69% | 0 | Completed |
| Full output validation | 17.853 | 0.9160 | 1231.49 | 57.35% | 0 | Completed |
| Serialized encrypted backup | 1.521 | **2.1156** | **31.90** | **1.486%** | 0 | Completed, marginal headroom |
| Cancellation/cleanup scenario | 2.176 | 0.4898 | 1657.72 | 77.19% | 0 | Completed |

Idle baselines need not rise monotonically: normal services/cache reclaim continue. Application-tree RSS peaks: alignment ~629.6 MB; render ~336.7 MB; validation ~605.6 MB; backup **~1,824.0 MB**. At minimum backup headroom, anonymous pages were ~1,879.0 MB; cached+buffers only **~16.48 MB**, indicating this was not merely a large easily reclaimable media cache. Kernel-visible used-minus-available reached **2,021,830,656 bytes**, versus **2,115,579,904 bytes** including guest-reserved RAM.

Guest CPU busy approximately alignment99.97%, render97.64%, validation99.94%, backup99.28%. No render-time SLA claimed. **1,406 live Django status requests, zero failures/timeouts**. Render p95 **3.18ms**, max **6.73ms**; alignment p95 **3.03ms**; backup maximum **7.58ms** (six sampled requests, not a statistically strong latency distribution). These are loopback minimal-status checks, not authenticated3–5-user/browser/HTTPS load certification. Memory PSI during sampled backup increased **some157,345µs / full116,537µs**: real reclaim/stall pressure, despite quick successful completion. All raw PSI preserved.

**Zero OOM-kill counter increase and no kernel OOM event**; complete before/after dmesg/journal and vmstat retained. Kernel logs/probes cannot prove unobserved future loads safe. Physical RAM completion is established for this fixture without swap; no swap-assisted alternative required.

## Backup behavior and risk

Unchanged V9 full-memory behavior, serialized after validated production is idle: SQLite backup API; **311 files**, **426,718,638 payload bytes**, **426,785,130 encrypted archive bytes**, ZIP_STORED, AES-GCM, authenticated full decrypt and every-file hash roundtrip. Core archive/encrypt/decrypt verification **1.260s**, whole subprocess1.521s. A temporary test key is not retained; archive/snapshot staging is removed only after verified success. No off-machine upload/independent deletion journal/key-recovery claim.

This is the same conservative full-volume V9 witness, which uses ZIP_STORED instead of S8's ZIP_DEFLATED. It preserves the crucial full-archive-in-memory encryption behavior and avoids compression hiding memory demand; it is not a redesigned backup or a production-policy selection. The ~4KB payload difference from V9 is the additional disposable SQLite lock table/page, not regenerated media.

Archive/plaintext/ciphertext/decrypted buffers coexist, so memory scales with retained payload. **Serialization solves overlap, not size-proportional RAM.** Extra asset versions/larger genuine provider images/retention growth can exhaust the small remaining margin; a safe production volume bound is unestablished. No streaming redesign was used to make this implementation pass. A future streaming implementation would need its own evidence and implementation authorization.

## Cancellation, disk and media validation

Live FFmpeg process-group SIGTERM confirmed cessation in **0.162s**; no escalation needed (bounded3s SIGKILL fallback remains). Start identity/PGID recorded, no live group member left, disposable lock released **only after confirmed cessation**, incomplete output never registered, previous validated export hash preserved. Django status succeeds while cancellation work is active. Post-run process list shows no FFmpeg/Gunicorn/Python orphan, and VM stop receipt is retained. Forced escalation/crash/recovery limits remain those of S3/S7, not newly certified production supervision.

Guest root filesystem **50,884,108,288 usable bytes** from50GiB virtual disk. Used beforework **3.628 GB**, sampled peak **4.173 GB**, after **3.751 GB**, free after **47.116 GB**. All reused inputs/model/runtime live on this root. Render scratch peak **107,973,159 bytes**, final MP4 **59,491,123 bytes**; validated candidate is moved, not counted twice as final+candidate. Peak `/out` **542,783,421 bytes** includes temporary426.785-MB encrypted backup plus output/intermediates/logs. Backup staging is transient, not retained project storage. Evidence collection tar after measurement is separately disposable, not a second backup workload or retained project asset.

Unchanged S6 validator passes: MP4, H.264/AAC,1920×1080, exact30/1fps,600s, full successful decode,18,000 frames,111 correctly ordered mapped transitions within original1/30s tolerance, zero blank frames,28,800,000 continuous audio samples, **56.9456dB** reference-mix SNR, no clipping/gaps, beginning/middle/end captions. Continuous narration is muxed once; scene mappings control visuals, never cut narration. Motion/captions/music enabled. V9's documented exact-frame `setts` packet-grid repair is retained in the disposable adaptation; no threshold relaxation or frame/audio edits. [Final receipt](v10/guest/render-result.json), immutable export `v10/guest/s6/exports/linux-600-2c958a022b2f.mp4`, SHA256 **2c958a022b2f905255c1cba13647e0f2fc89ec98ae820863848404cf90a4a63e**.

Cheap native five-language caption regression also passes: English/Spanish/French/Bangla/Hindi **identical decoded RGBA bytes** to visually accepted S6 references, no fallback/clipping. Synthetic narration validates media continuity, not narration quality; existing S5 accepted mappings/fidelity remain unchanged. Whisper phase is a resource witness using existing Call4, not replacement S5 mapping evidence.

## Classification and economic consequence

**MARGINAL**, not UNSAFE (the required fixture completed), and not SAFE_ENOUGH_FOR_ALPHA. About30.43MiB available with reclaim pressure is little demonstrated reserve for extra service load, retained media and sampling uncertainty. No source-of-truth numerical operational safety threshold/retained-volume policy exists; that final policy remains unresolved instead of inventing a universal percentage. This single run cannot certify a real2GiB VPS. No artificial service removal/swap/backup rewrite/quality weakening was used.

The ~$12 one-vCPU/2GiB category is **not qualified by V10** and cannot support an asserted safe Alpha configuration. Next evidence-supported **application** category is ~$24 two-vCPU/4GiB from V8/V9; its **whole-guest** qualification remains untested, and no provider is selected. This does not prove the topology infeasible under$30.

Reuse V8 nominal official pricing, not a new purchase/price selection. Illustrative two stored copies of **this measured** archive =0.85357026decimalGB. At preserved B2 backup-only tariff$0.00695/GB/month, storage-only paid equivalent **$0.005932313307/month**; free cash remains account-conditional. This supersedes only this sensitivity's older smaller V8 archive estimate, not history, a retention policy or complete backup cost.

| $24 candidate + measured backup partial | 0% uplift sensitivity | 10% sensitivity | 20% sensitivity |
|---|---:|---:|---:|
| Nominal partial recurring subtotal | $24.005932 | $24.005932 | $24.005932 |
| Nominal generation headroom:30/(1+uplift)-fixed | $5.994068 | $3.266795 | $0.994068 |
| Optimistic floor using **partial**5min$2.074188 proxy | 2 | 1 | 0 |

**Not allowances or guaranteed capacity.** Complete project expected cost, actual reserve/fees/taxes/FX, enforceable maximum and total backup/fixed cost remain UNKNOWN; sensitivity reserve$0/uplifts are not owner-approved policy. The V7$0.410964 bound remains conditional/unvalidated and is not added as expected spend. Optional suggestion costs and theoretical3/week or1/day volumes are not assigned to Alpha. $30 owner ceiling unchanged.

## Verification, remaining gates and next step

**23 deterministic verification assertions PASS**: actual VM allocation and global OS measurement, no swap, all measured phases, nonoverlap, kernel check, headroom/probes/disk, unchanged full S6 media checks/export hash, five-language equality, cessation/previous export/no orphans,501 input hashes,2,646-file historical preservation, classification guard, measured-backup/envelope arithmetic, unknown total capacity and zero generation. Test PASS verifies the evidence; **it does not turn the MARGINAL resource outcome into SAFE or S9 PASS**. Run `python3 spikes/operating-economics/v10/verify.py`; writes only V10 aggregate/preservation receipts.

Remaining S9: whole-guest4GiB/actual-host margins and performance; safe retained-volume/backup memory bounds, off-machine restoration/purge/independent authority and key custody; V7 token preflight and expected text usage (untouched); real image endpoint/size/failure/retry economics; full expected cost/enforceable exposure; tax/payment/FX/owner reserve; storage/version/traffic and correction volume; final credit/edit debit and cost-grounded Alpha capacity/allowances. No hosting, production or architecture freeze follows.

**Exactly one smallest next step:** separately authorize an equivalent **local/free whole-Linux-guest2-vCPU/4-GiB resource validation**, reusing these assets with maintenance serialized, before qualifying the ~$24 host class. Not started here.

Completed boundary: **zero provider/API generation calls; $0 paid spend; production/TASKS.md untouched; no cloud resource/account/public deployment/purchase; material local software/OS downloads recorded; original media unchanged; no V7 preflight; S9 NOT_YET_PASS.** One public GitHub release-metadata request and ordinary official software downloads are distinct from provider generation. Stop after V10; no V11, implementation planning or architecture freeze.
