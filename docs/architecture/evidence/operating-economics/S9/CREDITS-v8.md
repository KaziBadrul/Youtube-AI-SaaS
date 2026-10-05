# S9 revision 8 — fixed infrastructure and operating envelope

2026-10-05. **S9: NOT_YET_PASS.** Public official pricing, existing local media measurements and disposable arithmetic only. **No host or backup vendor selected.** Invited Alpha looks plausible at a low volume on list-price arithmetic, but a defensible complete owner-cash configuration is not established. Neither PASS nor topology-wide INFEASIBLE is supported. The $30/month ceiling, architecture, credits and unresolved Alpha allowances remain unchanged.

## Evidence, scope and authority

Read current docs index, Alpha specification, accepted architecture/ADRs and spike/cost contracts, S9 index/v1–v7/entitlement clarification, S2/S3/S7/S8 protocol results, S5 source receipts and B+B closure, and S6 raw/final resource/export evidence. Historical experiments remain historical. V7's input-token/preflight experiment is explicitly **not executed** here. Product/UX/design semantics do not change, so those documents receive no cosmetic revision.

Architecture being costed: one persistent Linux host, Django web/API, one Python production worker, SQLite WAL on local persistent disk, private host-local media and FFmpeg; one active production job, announced private availability, encrypted daily off-machine backup with independent deletion authority and verified recovery. No Redis/PostgreSQL/separate render/frontend service, paid TLS/encryption service or hosted ASR is introduced. Object storage below is **backup-only**, not relocation of active project media. One codebase remains compatible with candidate VMs, conditionally on actual runtime validation.

Artifacts:

- [Official pricing record](v8/official-pricing-v8.json): sources, retrieval date, units, account uncertainty and conflicting B2 note.
- [Measurements](v8/measurements-v8.json): byte/hash inventory, WAV formats, images, fixture DB, S6 exports/scratch and 3/5/10-minute extrapolations.
- [Arithmetic/results](v8/arithmetic-results-v8.json): backup, bandwidth, monthly sensitivities and checks.
- [Preservation manifest](v8/preservation-results-v8.json): all 209 pre-existing evidence/script files intact; the live S9 index's exact prior bytes are archived in [prior index](v8/S9-index-before-v8.md). Old revisions/results/scripts were not rerun/rewritten.
- [Disposable witness](../../../../../spikes/operating-economics/infrastructure_v8.py). Reproduce from repository root: `python3 spikes/operating-economics/infrastructure_v8.py`. Standard library only, reads existing assets, writes only v8 results, no network/SDK/tokenizer/model loading.

## A. Owner-local versus B. invited Alpha

**A — Owner-only/local validation:** incremental host rental **$0**, using existing owner-supplied hardware and connectivity. This is a cash classification, not economically free CPU, disk, electricity, hardware depreciation or broadband. Incremental electricity, backup destination/account charges and other actual bill effects are UNKNOWN. The tiny backup sensitivity below applies only if that volume is retained; owner-local complete monthly cost remains UNKNOWN. No public tunnel/home-server deployment, public availability, security or uptime is proved or selected.

**B — Approximately 3–5 invited creators:** requires credible persistent private web deployment. Full-month VM + off-machine backup + applicable extras + paid generation/failures/unknown liabilities + taxes/payment/FX + reserve must fit $30. Owner-local $0 rental cannot establish this scenario. Announced availability windows do not make a retained/stopped VM free; destroying it to reduce billing conflicts with the intended persistent substrate unless separately designed/validated.

## Resource envelope from underlying evidence

S6 tested macOS 26.5 arm64, Apple M5 ten cores (4P/6E), 16 GiB RAM, Python 3.12.14, FFmpeg 9.0.2 H.264/AAC. Installed FFmpeg lacked ass/subtitles/drawtext; the passed caption path used deterministic PNG overlays with Pillow 12.0.0, HarfBuzz 11.3.2, FreeType 2.13.2, Noto Sans 2.015, Bengali 3.011 and Devanagari 2.007 (SIL OFL). No font binaries or runtime downloads added here. Linux build/encoder/shaping compatibility and any redistributed licenses still need verification.

| Render | S6 scenes (fixture only) | Wall time | CPU seconds | FFmpeg peak RSS | Final recorded scratch peak | Scratch retained now |
|---|---:|---:|---:|---:|---:|---:|
| 3 min | 34 | 44.644s | 59.593s | 142.69 MiB | 32.470 MB | 14.593 MB |
| 5 min | 56 | 79.420s | 105.421s | 143.00 MiB | 53.382 MB | 23.954 MB |
| 10 min | 112 | 237.205s | 314.230s | 143.03 MiB | 108.159 MB | 108.159 MB |

The raw 5-minute benchmark's sampled 50,630,283 bytes is lower than the final S6 aggregate's **53,382,263**. Its final evidence script reconciles retained intermediates and candidate-export coexistence; this report uses the final aggregate, not the lower raw sample. Ten-minute scratch currently includes a candidate duplicate; it is not baseline retained project storage or another unique narration source. Historical scratch is left untouched.

The 10-minute worker/web-boundary witness observed **638,615,552 bytes (~609 MiB)** peak worker/process-tree RSS, 973 Django test-client status requests and no open render HTTP request. This excludes full operating-system/reverse-proxy/live-network, alignment model, concurrent backup and production state requirements. FFmpeg's ~143 MiB alone is **not a host RAM minimum**. Average render CPU was about 133% on that Mac; shared vCPU performance, thermals/throttling and architecture differences prevent extrapolating the same wall time to a VPS.

| Resource | Evidence-backed constraint | Not established |
|---|---|---|
| CPU | General-purpose CPU, no demonstrated GPU requirement; single render job, child process control; shared CPU may support intermittent jobs | Minimum vCPU count, shared-host sustained performance/acceptable latency |
| RAM | Observed process tree ~609 MiB; 2 GiB is a candidate to test, 4 GiB offers more candidate headroom | Full-system/ASR/backup coexistence peak; neither 2 nor 4 GiB certified |
| Persistent disk | Local WAL/fsync-capable root disk; immutable assets/versions, scratch, old/current exports, backup staging | OS/app/dependencies/model cache/base disk, long-term logs/version volume, operational free-space margin |
| Runtime | Linux-compatible Python/Django/SQLite/FFmpeg + Unicode shaping/fonts; process groups, start identities, supervision/restart | Linux stack correctness and platform-specific cancellation/recovery in this host envelope |
| Processes | Web + worker + coordinated maintenance/backup; no request-open render | Backup overlap/scheduling and RAM/CPU ceilings, live 3–5-user responsiveness |
| Network | Private authenticated HTTPS, previews/downloads, API traffic and off-host backup | Domain/hostname availability/cost, actual traffic, connectivity/latency/account terms |

S2's 1,280 actors plus writes demonstrated short SQLite WAL transactions on the workstation, not small-host resource sizing. S3/S7 prove local controlled recovery/publication, not Linux supervisor configuration or host power/controller faults. Do not place SQLite WAL on unvalidated network storage to get cheaper space.

**Important backup sizing discovery:** `spikes/local-feasibility/backup.py` makes the ZIP archive in `BytesIO`, reads media files, obtains raw archive bytes and encrypts the full archive in memory. Multiple archive-sized buffers can coexist. S8's tiny successful fixture proves the protocol, **not bounded large-backup RAM**. Peak RAM/throughput versus retained volume is UNKNOWN. A bounded implementation must preserve S8 while proving memory limits (e.g. appropriately bounded staging/streaming); no production implementation choice is frozen or implemented here.

## Candidate persistent hosts — official public prices

Retrieved **2026-10-05**, before unverified account taxes/payment costs. No trial credits deducted. Root storage included; no separate managed service assumed.

| Candidate | CPU / RAM | Included root disk | Transfer | Monthly list price | Runtime/economic status |
|---|---|---|---|---:|---|
| DigitalOcean regular Basic | 1 vCPU / 2 GiB | 50 GiB | 2,000 GiB | $12 | Topology-compatible candidate; lowest headroom/RAM/performance unvalidated |
| DigitalOcean regular Basic | 2 vCPU / 2 GiB | 60 GiB | 3,000 GiB | $18 | Topology-compatible candidate; more CPU, same unvalidated RAM |
| DigitalOcean regular Basic | 2 vCPU / 4 GiB | 80 GiB | 4,000 GiB | $24 | Topology-compatible candidate; better candidate RAM, very little generation budget |
| Hetzner EU CX23 | 2 Intel/AMD vCPU / 4 GB | 40 GB NVMe | 20 TB | $6.49 excluding IPv4/VAT | **Currently unavailable**; cannot underpin an available Alpha configuration |
| Akamai/Linode shared 4 GB, North America | 2 CPU / 4 GB | 80 GB | 4 TB | $24 | Topology-compatible candidate; target runtime/shared-CPU behavior unvalidated |

[DO pricing](https://www.digitalocean.com/pricing/droplets), [Hetzner rate adjustment](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/), [Hetzner availability](https://www.hetzner.com/cloud/cost-optimized/), [Akamai regional pricing](https://www.akamai.com/cloud/pricing/north-america). GB/GiB labels above follow each source; no silent unit substitution. No candidate is validated as fully viable for this actual workload, and cheapest is not automatically selected.

DO uses per-second charges/monthly cap; Linode $0.036/hour/monthly cap; Hetzner hourly/monthly cap until deletion. Shared CPU has variable contention: sustained media jobs need validation, not an assumption of dedicated cores. Region/account availability, acceptable use/workload, persistent root semantics and tax invoice must be confirmed before selection. No independent extra network service is assumed.

Additional disk: [DO volumes](https://docs.digitalocean.com/products/volumes/details/pricing/) $0.10/GiB-month, network attached; [Akamai pricing](https://www.akamai.com/cloud/pricing/north-america) block storage $0.10/GB-month. Hetzner additional-disk/IPv4 exact add-on charge not established here (UNKNOWN). These are optional price facts, **not adoption**. Included root disk is the current candidate substrate; overflow cannot silently move the DB or introduce a separate active object-storage architecture. Extra disk is not charged twice alongside already included root capacity.

Free/hobby classification: [Render free web](https://render.com/docs/free) is **B: useful for owner/mock development; C: unsuitable for this invited Alpha**, due to idle sleep, ephemeral filesystem and lack of persistent disk. No inspected free host is established as A (credible invited Alpha). Advertised introductory cloud credits are temporary, not permanent economics.

## Existing media measurements and storage extrapolations

All sizes below are **decimal MB**. Hashes match all eight S5 ledger sources and the three final S6 export receipts. Source files are unchanged. No new media generation or rerender was needed.

- 49 historical images: **22,204,412 bytes**, mean **453,151.265** bytes, median 435,275, range 221,174–770,643. Inspection found JPEG content despite `.png` filenames (1376×768 examples); this is a historical fixture, **not selected new image-model byte/format evidence**. No files were corrected. Provider-specific expected image size remains UNKNOWN.
- S5 Call 4: **8,237,106 bytes**, 171.48 seconds; Call 6: **8,204,466 bytes**, 170.8 seconds. Both 24 kHz mono PCM16, preserved versions. The cohort's measured container overhead is 6,066 bytes/WAV, used rather than assuming a 44-byte header.
- S6 narration: 48 kHz mono synthetic PCM16, 28,800,044 bytes/5 minutes. S6 full-duration music WAV is a synthetic fixture, **not a required private copy of the shared library track per project**. Shared music/app/font/model files belong to base/shared disk, actual licensed library volume/cost UNKNOWN.
- Historical final MP4 **19,441,752 bytes**, SRT **5,939**, timestamp JSON **13,683**. This is another real legacy size, not a five-minute new-model export guarantee. Its measured source narration is 265 seconds, not a five-minute new-project receipt.
- S6 5-minute caption PNG cache **993,132 bytes**, manifest **71,566**; SQLite web fixture **8,192 bytes**. Metadata includes mappings/cues; media is not database storage. S6 logs/manifests/scratch file receipts are in the inventory; no production job/accounting/log retention/growth bound follows from an 8 KiB toy DB.

Clean sensitivity assumes historical mean-image bytes × preliminary 36/60/120 counts, one unique 24 kHz mono PCM16 source lasting requested duration + measured WAV overhead, caption-cache/manifest bytes scaled by S6 scene count, and one corresponding measured synthetic export. Not an observed new project and not a byte maximum. Actual sentence count replaces preliminary topic count; S6's 34/56/112 scene density is not production policy.

| Requested | Images heuristic | Images MB | Source WAV MB | Caption cache MB | Metadata MB | Active excluding export MB | Export MB (measured synthetic) | Clean retained MB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 min | 36 | 16.313 | 8.646 | 0.625 | 0.046 | 25.631 | 17.877 | 43.508 |
| 5 min | 60 | 27.189 | 14.406 | 1.064 | 0.077 | 42.736 | 29.428 | 72.164 |
| 10 min | 120 | 54.378 | 28.806 | 2.128 | 0.153 | 85.465 | 59.553 | 145.018 |

**No double-counting:** active project excludes export/scratch; clean retained = active + one export. Shared source referenced by many scenes counts once. No additional concatenated narration copy is mandatory if the source already serves continuous narration. If a derived assembly file is physically created, add its actual bytes separately. S5 evaluation/comparison WAVs, debug fixtures, images.zip and duplicate historical manifests are not normal production project storage.

Marginal versions: one extra image is 0.453 MB using historical mean (0.771 MB measured largest, neither production expectation nor cap); one extra B segment is 8.204 MB for measured Call 6, or approximately 14.406 MB for a hypothetical 5-minute whole segment at this PCM format. Each additional successful retained five-minute export adds measured-synthetic 29.428 MB. An optional separate five-minute derived PCM copy adds approximately 14.406 MB. Unaffected shared ranges add mappings, not duplicate source bytes. Expected correction counts, final grouping size and export-retention volume **UNKNOWN**.

Render scratch is separate and one active job only. During a rerender, previous valid export stays available while new intermediates/candidate coexist. S6 peak scratch includes that candidate; do not add the same candidate again. Safe disk equation:

`base OS/app/models/library/DB/logs + retained assets/current & historical exports + one job's scratch/new candidate + backup staging/DB-copy + free-space margin`.

For example, five clean modeled five-minute projects retain ~0.361 GB before shared data/history; add up to the **observed** 0.108 GB ten-minute scratch for this fixture, not 5× scratch. Existing candidate root sizes look ample for these payloads but **safe production margin UNKNOWN** due to base disk, real outputs, corrections, archive staging and workloads. Peak scratch with real complex images may differ; these historical measurements are not an application ceiling. Backup staging is not permanent retained media and is never counted as another project.

## Off-machine encrypted backup economics

Requirements remain S8: consistent SQLite/media snapshot, daily successful monitored backup/<=24h loss window, independently recoverable authenticated non-content journal/latest head, encryption key outside archive, verified restore, seven-day active purge and <=24h further backup purge. Failed replacement backups do **not** extend deletion deadlines. Restore rechecks current deletion authority and spending/unknown attempts before access/paid work. No vendor or final retention scheme selected.

Candidates [B2 pricing](https://www.backblaze.com/cloud-storage/pricing) and [R2 Standard pricing](https://developers.cloudflare.com/r2/pricing/) are off-host destinations only:

- B2 main price $6.95/TB/30 days ($0.00695/GB), upload and ordinary A/B/C API operations free; restore egress allowance 3× average stored bytes, excess $0.01/GB. Advertised first 10 GB free is conditional on verified account allowance. [API mapping](https://www.backblaze.com/cloud-storage/transaction-pricing) covers upload/read/list/delete-version; D event notifications excluded. Its storage note conflicts at $0.005/GB: use the **higher main price** conservatively, flag account tariff confirmation rather than silently selecting cheaper text. No minimum file size/duration.
- R2 Standard $0.015/GB-month, $4.50/M Class A and $0.36/M B, with rounded-up billing units; no retrieval/egress charge, deletes free. Advertised 10 GB + 1M A + 10M B allowance is separately qualified. Removing free allowance, even 1,000 A + 1,000 B operations incurs **$4.86 request units**, not naive fractional microcosts. Do not rely on IA's cheaper rate/minimum 30-day charge or trial credits.

One sensitivity: **five clean five-minute projects**, one/two/eight complete encrypted snapshots present throughout a 30-day billing period. Counts are alternatives, not chosen retention or creator allowances. No compression/dedup savings assumed. Candidate ZIP_STORED upper packaging uses <=128-byte internal filenames, <=1024 manifest bytes/file, header allowances and S8's 12-byte nonce + 16-byte tag. Proposed packaging limits are **local sensitivity assumptions, not enforced production policy**. DB/journal/logs/shared data/history still UNKNOWN and excluded from this partial footprint. AES alone adds 28 bytes/archive; complete ZIP/manifest overhead is separately reserved. No paid encryption service needed.

| Copies sensitivity | Partial stored GB | B2 paid-equivalent storage/month | R2 no-free-equivalent storage+1000A/1000B/month | Possible free cash for either |
|---:|---:|---:|---:|---|
| 1 | 0.361657 | $0.002514 | $4.875 | $0 if allowance verified |
| 2 | 0.723313 | $0.005027 | $4.875 | $0 if allowance verified |
| 8 | 2.893253 | $0.020108 | $4.905 | $0 if allowance verified |

Two-copy partial payload+packaging is **0.723313272 GB**, B2 $0.00502702724040/month before extras. One full upload/day is approximately **10.85 GB/month**, not 30 stored copies. One restore of one ~0.362 GB archive falls below B2 3× average storage in these steady-state scenarios; multiple restores use `max(0, restoreGB - 3*averageStoredGB)*0.01`. Early-month/time-weighted storage and account bandwidth terms matter. R2 restore egress is zero but billable read units remain. Full backup cash cost remains UNKNOWN until account, retained contents, traffic, taxes, purge and actual backup scheme are known.

At generic 10/50/100 GB retained backup sensitivities B2 paid-equivalent storage is $0.0695/$0.3475/$0.695 per 30-day period; R2 storage is $0.15/$0.75/$1.50 before rounded request charges or qualified free allowances. This is not assumed project volume. Ordinary API/egress terms are recurring price features; promotional/free storage allowances are not a long-term viability proof.

**Purge compatibility is conditional:** [B2 file versions](https://www.backblaze.com/docs/cloud-storage-file-versions) distinguish hide from actual version deletion. Enumerate and delete every affected archive/version, no immutable lock blocking S8 deadlines. [R2 direct deletion/listing](https://developers.cloudflare.com/r2/reference/consistency/) is strongly consistent; a cached public custom domain can retain data, so no cached/public backup exposure is contemplated. No actual remote purge or restore was performed. Entire archives containing purged content may have to be removed/rebuilt **before attempting replacement**, including when the new backup fails; rolling retention alone does not satisfy S8. Independent journal/head/key custody and failure-domain independence remain unvalidated operational requirements, not solved by a cheap storage invoice.

S8's full in-memory archive has unmeasured RAM/copy overhead. A candidate filesystem-staged path may require one full encrypted archive plus SQLite snapshot and transient plain archive (up to two archive payloads + DB), depending on implementation. These are **staging sensitivities**, not measured scratch bounds or another retained backup copy. Do not run it automatically alongside render/alignment until resource and locking behavior is validated. Upload throughput/backup completion within daily RPO remains UNKNOWN.

## Bandwidth and database/app economics

[DO traffic](https://docs.digitalocean.com/platform/billing/bandwidth/) applies included accrued outbound pool before $0.01/GiB extra; ingress free. [Akamai NA](https://www.akamai.com/cloud/pricing/north-america) includes 4 TB on the comparison plan then $0.005/GB. Hetzner EU allowance 20 TB, excess price UNKNOWN here; unavailable candidate excluded from budget calculations. Full-month pools must not be assumed after partial-month creation.

Per five-minute project, one measured-synthetic export download ~29.428 MB; each additional download adds that again. One full historical-mean image preview set + one source audio ~41.595 MB. Sensitivities: 5/10/20 projects, 1/2/10 export downloads each, one preview set each, daily full upload of the five-project archive. Modeled outbound **11.204–17.566 GB/month**, comfortably below listed candidate allowances → **$0 incremental egress for these explicitly modeled bytes**. This is not measured user demand or a complete traffic estimate. Pages/scripts/request and protocol overhead, repeat previews, provider request traffic, corrections/failed transfers, DB/journal updates and abuse are UNKNOWN; controls must prevent unbounded downloads from gaining budget authority.

Backup upload leaves host (counts host outbound) but enters backup store (typically free). Restore leaves backup store (apply its allowance) and enters host (free ingress); do not double-charge both directions as paid outbound. Provider generated assets usually enter host; outbound prompts/reference uploads/API messages remain infrastructure traffic. There is no assumed extra paid gateway or CDN. Sampled toy DB/manifests are small but actual SQLite/WAL/accounting/research/log-growth and retention policy stay UNKNOWN, not $0 or included as binary media.

## Fixed versus variable versus contingent

- **Fixed/recurring:** full-month host; included root disk has $0 extra charge; any selected backup/storage minimum or paid-equivalent retained-byte recurring cost; actual unavoidable domain/shared-library charges if applicable. Host-only list price known; complete fixed owner-cash subtotal UNKNOWN.
- **Variable/project:** images, TTS, required bounded text/research as entitled, edits, retained-byte growth and usage-related backup/egress. Local render/ASR has no separate provider charge but consumes the already budgeted host; do not charge host again per video without a defined allocation.
- **Contingent/uncertain:** tax, bank/FX/fees, reserve, charged failures/unknown liabilities, excess transfer, correction/version volume, exceptional restore/purge rewrite traffic. No average probability invented.
- Suggestions are distinct optional discovery operations. Stored random topics need no per-click LLM; Custom/Expert quotas/model/retrieval costs remain unresolved. No unavoidable dedicated fixed service established, so none is silently added to normal video economics. Research entitlement still qualifies whether the factual-topic research branch applies.

## Taxes, owner cash and reserve

Prices are nominal USD, not proven all-in Bangladesh owner cash. Hetzner explicitly excludes VAT/IPv4. [DO country/account taxes](https://docs.digitalocean.com/platform/billing/taxes/) do not establish the owner's invoice; Bangladesh not shown is not permission to use zero. [Official EBL card FAQ](https://www.ebl.com.bd/downloads/Debit_card_awareness_FAQ_CUSTOMER_004.pdf) refers conversion markup/fees to the applicable current card schedule; the owner's bank/card, currency, payment eligibility, exchange spread, applicable tax/withholding and statement rate are **UNKNOWN**. No blanket 15% VAT, 3% FX, live BDT/USD conversion or exact fee has been applied.

Method: nominal invoices + verified provider tax + verified payment/FX/other charges + **owner-approved reserve** must remain <=$30 including generation and liabilities. Reserve amount/percentage UNKNOWN. The witness shows **0/10/20/30% uniform total-spend uplifts**, strictly sensitivities, not policy or guarantees. It also models explicit cash reserve separately and fails closed when reserve/uplift is unknown. A uniform sensitivity must uplift generation as well as hosting, rather than spending untaxed leftover dollars after uplifting just fixed costs.

`nominal generation headroom = (30 - cash reserve)/ (1 + sensitivity uplift) - nominal fixed partial costs`.

Domain/HTTPS: private access needs secure reachable hostname/configuration. No evidence of existing usable domain or incremental registration fee; that cost is UNKNOWN if required. Free certificates/open-source components do not require a new paid TLS service, but deployment correctness has not been tested. Existing expenditure during the same budget month and outstanding reservations must also be deducted; not assumed absent.

## $30 monthly envelope and capacity sensitivity

Use two-copy five-project B2 partial storage charge above, ordinary free API classes, included traffic for modeled bytes. **This is a partial nominal scenario**, not selected provider/backup/retention/allowances or complete fixed cost. Actual cash reserve, tax, domain/shared overhead and other unknown charges are not silently $0; zero in this table is deliberately a labeled sensitivity.

| Host/month | Fixed partial/month | Remaining nominal budget (0% uplift, $0 reserve sensitivity) | Upper count using only $2.074188 partial/video | At hypothetical $3/video | At $4/video | At $6/video |
|---:|---:|---:|---:|---:|---:|---:|
| $12 | $12.005027 | $17.994973 | 8 | 5 | 4 | 2 |
| $18 | $18.005027 | $11.994973 | 5 | 3 | 2 | 1 |
| $24 | $24.005027 | $5.994973 | 2 | 1 | 1 | 0 |

**None is an allowance or guaranteed capacity.** Complete expected video cost UNKNOWN; upper counts use a partial proxy excluding text/image input/thinking/charged failures etc. Hypothetical $3/$4/$6 are sensitivity totals, not measured prices. Integer `floor` is used and negative budget yields no admission. Unknown costs yield unknown capacity, not infinity/zero-cost capacity.

| Host | 0% uplift | 10% uplift | 20% uplift | 30% uplift |
|---:|---:|---:|---:|---:|
| $12 | $17.994973 (8) | $15.267700 (7) | $12.994973 (6) | $11.071896 (5) |
| $18 | $11.994973 (5) | $9.267700 (4) | $6.994973 (3) | $5.071896 (2) |
| $24 | $5.994973 (2) | $3.267700 (1) | $0.994973 (0) | $-0.928104 (0) |

Parentheses are optimistic partial-cost-only counts. $0 cash reserve is still hypothetical in every column; no reserve approved. The $24 candidate falls to ~**$0.995 nominal generation headroom** at 20% uplift, enough for **zero** modeled five-minute partial-cost projects. This disqualifies that **specific scenario**, not every $24-host workload or the whole architecture. The cheaper $12 candidate has ~**$12.995** at that uplift but is not yet resource-qualified. The unavailable Hetzner plan is not used to claim headroom.

Current generation basis remains V6/V7: five-minute topic ~60 image outputs **$2.016** + initial B narration duration proxy **$0.058187543736878936319104269** = **$2.074187543736878936319104269 partial**. Complete expected variable USD UNKNOWN; text/search expected UNKNOWN; V7 candidate maximum **$0.410964** is **conditional** and not expected/usable live authority. Image input/thinking/real failures/fees remain unknown. Conditional 60-image three-attempt + one-B-segment + V7 arithmetic **$25.785684** is not a complete enforced project bound; production segment count/caps and other components still unresolved. Combining that hold with even $12 host exceeds $30, so cannot promise all such retries fit. Admission must reserve only validated, affordable scope and stop/reconcile unknown outcomes, never multiply normal expected cost by three or automatically grant every allowed retry.

3/week and 1/day are product entitlement tiers, **not free Alpha allowances or promised full monthly throughput**. One active job and the $30 ceiling remain stronger admission constraints. No tester grants, final dollar-to-credit conversion, stage percentages or `images/60` formula are introduced.

## Verification and preservation

**48 deterministic checks PASS.** Cover unknown propagation, category/scenario separation, 3/5/10-minute count/storage/scratch arithmetic, shared source counted once, backup copies versus upload bytes, packaging/encryption overhead, B2/R2 paid-equivalent versus qualified free cash, R2 rounding, included-bandwidth-first, unit conversion, total-spend uplift/unapproved policy, reserve, $30 subtraction, negative/floor capacity, incomplete expected costs, conditional retry exposure, tier/allowance distinction, optional discovery exclusion and original hashes. Local arithmetic PASS is not S9 independent acceptance or host/runtime/backup certification.

All 209 pre-existing evidence/script files match the captured preservation ledger, except the intentionally updated live S9 index whose exact prior bytes are preserved. Source/media receipts are rehashed; all eight S5 sources and three S6 exports match historical ledger hashes. No earlier uncertainty is erased. No old evidence writer, generation call, installation, download, Linux/target-host benchmark, token preflight or rerender was run.

## Verdict, unresolved requirements and next step

**S9: NOT_YET_PASS.** Candidate list-price configurations leave plausible low-volume room; full cash viability/reserve and sufficient host resources are not established. This does not prove INFEASIBLE. No architecture freeze/vendor choice/implementation authorized.

Still UNKNOWN/unvalidated:

1. Linux runtime/caption/alignment/process recovery and bounded RAM/CPU/disk for web + worker + render/alignment/backup; actual base installation/library/model size and operational margins.
2. Real selected image size/acceptability/charged failures/retry evidence; expected total project cost and safely enforceable whole-project maximum. V7 text input preflight remains unchanged and untested here.
3. Actual off-machine consistent backup, retention volume/cadence/throughput, purge of every historical copy even on failure, latest independent journal/head/key recovery, verified remote restore/failure-domain independence.
4. Account prices/availability, tax/payment/FX/withholding and owner-approved reserve; remaining current-month cash/holds; domain/shared library costs where required.
5. Expected corrections/version retention, DB/WAL/log/research storage growth, download/user traffic, expected/maximum unknown liabilities and costs.
6. Final credits/edit debit policy and cost-grounded Alpha tester capacity/allowances; tier names do not resolve these.

**Single smallest useful next step:** a separately authorized **local/free Linux resource-envelope validation using existing assets**, initially testing the 2-vCPU/4-GiB candidate envelope with Django + one worker and the ten-minute render, local alignment and full-volume backup phases. Establish peak whole-system RAM/scratch and scheduling needs before choosing/buying a host. No paid host benchmark or token-preflight experiment is implied. Any required new runtime/model download needs its own applicable approval; none performed here.

Completed boundary: **zero provider/API generation calls; $0 paid spend; zero dependency/model/media downloads (public document browsing only); production untouched; TASKS.md untouched; no deployment/provisioning/accounts/purchases.** Stop after Revision 8; no Revision 9, task planning or architecture freeze.
