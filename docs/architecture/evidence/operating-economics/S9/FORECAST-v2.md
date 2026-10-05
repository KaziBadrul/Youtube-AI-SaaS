# S9 forecast continuation — 2026-10-05

**S9: NOT_YET_PASS.** Local deterministic scenarios only. Owner's $0.0336 per
1K image is fixed. Current Free tier image capacity is zero; no pilot/upgrade
is requested. Preserve the original baseline and proposed pilot as history.

## Evidence classes

- Owner-fixed: image-output tariff, Free 0/0/0 and conditional Tier 1
  150 RPM / 100K input TPM / 1K RPD. No Batch discount assumed.
- Measured: S5 historical usage/audio and S6 synthetic render CPU, scratch,
  exports; all eight original S5 WAV hashes checked unchanged by this witness.
- Official advertised terms: hosting, search and object-storage prices below.
- Scenarios: actual scene counts, edits/failed attempts, image bytes, future
  paid usage, text tokens and full-volume backup traffic remain unmeasured.
  No scenario is labeled an established affordable production project.

## Per-project sensitivity

| Minutes | Initial images | Extra image outputs at 10%, rounded up | Image output total | Illustrative variable subtotal |
|---|---:|---:|---:|---:|
| 3 | 34 | 4 | $1.2768 | $1.4078 |
| 5 | 56 | 6 | $2.0832 | $2.2375 |
| 10 | 112 | 12 | $4.1664 | $4.3789 |

These are scenario values, not quotations/actual bills. The subtotal includes
historical Call 4 TTS usage scaled by duration, one Call 6-sized coherent
segment correction ($0.033128), four paid-equivalent Basic searches ($0.032),
and illustrative aggregate text 20K input/10K output ($0.031). The text reference
is S4-R's Gemini 3.5 Flash-Lite at $0.30/$2.50 per M tokens; no model selection
or production token budget is made here. Search $0.008/Basic credit and reference
text rates were rechecked against [Tavily](https://docs.tavily.com/documentation/api-credits)
and [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing).

TTS duration-scaling is a projection from one historical delivery, not an
optimal segment-size policy or refreshed universal price claim. The selected
B architecture regenerates the affected full coherent segment and realigns it;
the one-correction scenario uses the historical 171-second scope only.
No preserved sibling image is regenerated because narration changes.

Additional image attempts include successful corrections/outputs; failures
charged without an image remain a separate unknown. Input/thinking, taxes/fees,
other account use, actual text/research usage, render/alignment target-host
capacity and infrastructure are excluded from the variable subtotal. Verified
free entitlements may reduce cash spending but are not assumed permanent.

## Hosting comparison

| Candidate | Base monthly quote | Resources | What remains unresolved |
|---|---:|---|---|
| DigitalOcean Basic regular | $12 | 1 vCPU, 2 GiB, 50 GiB SSD | Target-host render/alignment performance, fees, actual retained assets |
| DigitalOcean Basic regular | $18 | 2 vCPU, 2 GiB, 60 GiB SSD | Same; CPU does not prove RAM sufficiency |
| DigitalOcean Basic regular | $24 | 2 vCPU, 4 GiB, 80 GiB SSD | Very little budget left for generation |
| Hetzner CX23 EU | $6.49, excluding IPv4/VAT | 2 shared vCPU, 4 GB, 40 GB NVMe | Page marks unavailable; account/region availability and IP/fees unverified |

[DigitalOcean published table](https://www.digitalocean.com/pricing/droplets).
Hetzner price found in its [June adjustment table](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/);
[plan page](https://www.hetzner.com/cloud/cost-optimized/) supplies resources and
the current unavailable marker. This resolves the prior extraction gap but
does not make the candidate deployable or selected. No currency conversion or
IPv4 cost invented. No short-lived deployment, purchase or host benchmark run.

Existing macOS measurements cannot guarantee equivalent Linux/shared-CPU times.
Python worker peak ~639 MB during S6 excludes final web/OS/alignment coexistence;
do not infer a 2 GiB host passes solely from FFmpeg RSS. Existing alignment uses
local faster-whisper-base, but target-host memory/runtime is not measured here.

## Monthly envelope — five-minute examples

Assume $12 host, the variable sensitivity above, hypothetical 3 MB images,
two audio versions, two exports and eight full snapshot copies resident for the
entire month. Backup byte-month rate $6.95/TB from
[Backblaze B2](https://www.backblaze.com/cloud-storage/pricing), before fees/extra
egress. No paid vendor or product-wide storage limit is selected.

| Projects/month | Host + initial image output alone | Illustrative subtotal with edits/TTS/text/search/backup | Remaining from $30 for excluded costs |
|---|---:|---:|---:|
| 3 | $17.6448 | $18.7582 | $11.2418 |
| 5 | $21.4080 | $23.2637 | $6.7363 |
| 10 | $30.8160 | $34.5273 | −$4.5273 |
| 20 | $49.6320 | $57.0546 | −$27.0546 |

**10 five-minute projects plus this $12 host cannot fit**, even before other
costs. **20 initial five-minute image sets alone cost $37.632**, so cannot fit
the $30 ceiling even without hosting. Smaller scenarios leave headroom; that
is not proof that excluded costs/unknown liability fit. No tester allowances
or invitation workload have been finalized. An owner workload question is
pending; these scenarios do not silently define meaningful use.

## Storage / traffic

Five-minute retained media sensitivity (62 generated images, two 24kHz mono
PCM16 source versions, two synthetic S6 exports): 149.66 / 273.66 / 583.66 MB
per project for 1 / 3 / 8 MB images. One S6 attempt scratch adds 53.38 MB.
Exclude OS, model weights, logs/metadata, uploads and higher-real-image MP4 size;
these cannot set a production disk quota. Count one shared source once, not
once per mapped scene. Restore costs no new provider generation, but retained
versions and restoration/render compute still use resources.

At five projects and 3MB/image, eight full snapshots model 10.946 GB retained,
~$0.0761/month, and daily full uploads model 41.049 GB/month. One export download
each is 147.14 MB using synthetic compressibility. This is intentionally a
monthlong/high-retention sensitivity, not observed backup traffic or an
instruction to retain expired content. Deduplication/compression not assumed.
Production purge must remove expired source content from every recoverable
snapshot by the accepted deadline. Default seven-day VM backups are not proof
of that requirement; deletion/version purge still needs provider-specific proof.

## Quotas / maximum liabilities

Tier 1 RPD request-only upper bounds 29/17/8 initial projects for 34/56/112 images
exclude edits/retries and input TPM. Free capacity is zero now. Monthly budget
is tighter than this hypothetical daily image quota for the scenarios above.
Text/TTS/search quotas and execution latency must also fit; no project completion
guarantee follows from RPM pacing. Batch-specific quotas are not used.

Fixed $0.0336 output tariff is not maximum possible billable attempt exposure.
The retained S4 conservative image bound $0.139264/attempt gives 56 × 3 attempts
= $23.396352 before fees. Combined with a $12 host, reserving that full exposure
cannot fit $30. This is a maximum-liability stress case, not expected spend;
do not implicitly promise every possible retry or silently relax reservations.
Final request/plan caps need explicit bounded configuration and available budget.

Local arithmetic tests verify edit-cost monotonicity, preserved unknown holds,
settlement replacing rather than double-counting holds, lower-bound infeasibility,
and rejection of affordability PASS while full costs are unknown. Fake arithmetic
does not implement or independently certify the production spending ledger.

## Verdict / remaining work

The cost model now quantifies useful operating sensitivities and rules out
specific oversized workloads under $30. It does not establish the complete
meaningful-use envelope. Need owner intended volume, actual current obligations
and fees, final text/search configurations or explicit bounded scenario policy,
target-host resource validation and off-host purge/traffic contract evidence.
Image quality/bytes/failure rates stay uncertainty on Free; no live experiment
is requested. No architecture freeze, new allowance or budget increase inferred.

Reproduce `python3 spikes/operating-economics/forecast.py` from root.
[Raw scenarios and checks](forecast-v2.json); original [baseline](baseline-v1.json)
preserved. Zero provider calls, source WAV modifications, paid services,
downloads, production implementation, TASKS.md, deployments or purchases.
