# S9 credit estimates / cost-derived capacity — revision 4

2026-10-05. **S9: NOT_YET_PASS.** Owner states creator estimates are credits,
not dollars, and private Alpha capacity should depend on costs. This revision
adds local arithmetic/scope tests; no paid call or production implementation.

## Creator estimates versus internal authority

Topic estimate is requested minutes / 5, default requested duration five minutes.
Examples: three minutes 0.6 credit, five 1, six 1.2, ten 2. Creator interface
shows only estimated credits. Approved amendments are recorded in the product,
cost and UX docs; historical dollar-display wording is explicitly superseded.
No forced confirmation/review screen is added.

An estimated credit is not a maximum financial liability or a final debit.
Internal reservations still track USD exposure, account quotas and concrete
attempts. Paid planning must itself be admitted under bounded authority.
Plan output cannot authorize extra images, tools, output tokens or retries.
Final debit duration measurement and credit rounding precision, corrections,
reset/carryover and consumption points are open future decisions. This evidence
does not implement credits or adopt final paid-plan prices.

## Image density dominates the available range

At fixed $0.0336/image, assuming full tier use:

| Images/five-minute credit (scenario) | Initial output per credit | 1/week average month | 3/week average month | 1/day average month |
|---|---:|---:|---:|---:|
| 30 | $1.0080 | $4.3680 | $13.1040 | $30.6600 |
| 40 | $1.3440 | $5.8240 | $17.4720 | $40.8800 |
| 56 | $1.8816 | $8.1536 | $24.4608 | $57.2320 |
| 80 | $2.6880 | $11.6480 | $34.9440 | $81.7600 |

Weekly annual averages use 52 weeks/12 months, daily 365 days/12. These are
not reset-period rules or allowances. All values exclude other billing/correction
costs. The 56 count is the S6 synthetic extrapolation from 32 scenes/171.48 sec,
not a real default scene count. No displayed initial estimate can guarantee a
price until generation scope is separately bounded. Lower image density has
not been demonstrated to maintain publishability for actual scripts.

## Deriving possible free-Alpha capacity

Owner direction: derive capacity from costs, rather than set workload first.
Image-only capacity bound:

`floor(max(0, 30 - recurring_host - all_other_cost_reserve) / image_output_per_credit)`

Example with hypothetical $12 monthly host:

| Images/credit | Assume $5 for all other costs | Assume $10 for all other costs |
|---|---:|---:|
| 30 | At most 12 initial image sets | At most 7 |
| 40 | At most 9 | At most 5 |
| 56 | At most 6 | At most 4 |
| 80 | At most 4 | At most 2 |

Those reserves are **sensitivity parameters**, not verified all-in costs or
approved allowances. They must cover all other generated stages, extra images,
fees/taxes, backup, historical liability and paid failures. Consequently these
numbers cannot yet be promised to testers. Actual maximum-request reservation
may bind earlier than expected output spending. The raw witness includes
host 0/12/18/24 and other reserves 0/5/10 without selecting any combination.
Host=0 is a local owner scenario, not free electricity/backup/resources.

Existing S9 variable sensitivity at 56 images suggests approximately $23.26 for
five five-minute projects plus a $12 host and modeled backup, before exclusions.
This leaves $6.74, not proof all exclusions fit. No final subscription tier is
automatically offered free during Alpha, and future paid revenue does not
silently raise the $30 owner ceiling.

## Pathological script / plan test

Synthetic input case: 500 one-word sentences; synthetic planner output requests
500 scenes for a five-minute topic scope. A disposable test cap of 40 images per
credit rejects that plan before spending: **BLOCKED_SCENE_SCOPE**, zero requests.
The same test also rejects additional output scope when previous paid spending
has already exhausted that fixture's image allocation. A bounded 40-scene case
passes only the fixture image-scope check, **not provider authorization**.

The number 40 is solely a witness parameter, not selected production policy.
This test establishes deterministic financial rejection is feasible; it does
not prove coherent grouping, narratability detection, model adherence, natural
scene pacing or affordable full provider liability. Sentence count is not
scene count or TTS request count. Approved pasted words must not be silently
rewritten to force scope to fit. Material scene-density or adaptation decisions
require explicit policy/creator handling before implementation.

## Closure assessment

Established: immediate proportional credit estimates; internal USD accounting
remains separate; conditional density/tier/capacity ranges; local rejection of
excessive generated scope; retained earlier forecasts and source evidence.

Not established: final bounded scene-density policy, complete expected and
maximum per-project exposure, cost-grounded Alpha allowance, real image quality/
failure/bytes, target-host resources, off-host purge/fees/traffic. Free image
account is currently zero-capacity; future Tier 1 quotas stay conditional.
No live pilot/upgrade is sought. S9 cannot be marked PASS from partial-cost
headroom, a credit label or commercial tier descriptions alone.

Smallest useful next step is to establish a bounded, quality-compatible image
generation scope per five-minute equivalent and fill the remaining internal
cost/reservation components. The density choice is not frozen here to make
the economics fit. Final credit-debit/correction rules matter before commercial
implementation, but are not used as a reason to stop this local cost analysis.

Reproduce `python3 spikes/operating-economics/credits.py`; [raw witness](credits-v4.json).
Default/fractional estimates, invalid duration, excessive scene count, spent
scope preservation and positive fixture checks PASS. Zero provider calls,
source WAV modifications, model downloads, paid services, production
implementation, TASKS.md, purchases or deployment.
