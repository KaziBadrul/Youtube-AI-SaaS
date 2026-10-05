# S9 workload / future subscription scenarios — revision 3

2026-10-05. **S9 NOT_YET_PASS.** Owner defines these as **future paid
subscription plans**, not free private-Alpha allowances. No billing system,
subscription price, checkout, budget increase or production work authorized.

## Owner decisions

- Default topic script targets approximately five minutes (already Alpha default).
- One video credit represents five approximate video minutes.
- Proportional conversion: minutes / 5; six minutes = 1.2 credits, ten = 2.
- Proposed plan capacities: one five-minute equivalent per week; three per
  week; one per day. Longer videos consume the corresponding number of units.

Credit units are workload entitlement, not USD or a provider liability cap.
They do not replace the accepted private-Alpha USD allowance/reservation ledger.
Exact authoritative duration measurement, precision, reset/carryover, charging
point and correction policy remain future product decisions. This spike only
needs workload equivalents, so no implementation decision is invented.

## Per-subscriber economics

Fixed image-output tariff $0.0336; scenario 56 initial images per five-minute
unit. Each unit's initial image output is $1.8816. Actual scene density is not
fixed by duration; 30/56/80 images imply $1.0080/$1.8816/$2.6880 respectively.
Default five-minute script target does not guarantee 56 provider requests.

| Future plan | Five-minute units in 28 days | Average units/month* | Initial image outputs/month | Illustrative variable subtotal/month** |
|---|---:|---:|---:|---:|
| 1 per week | 4 | 4.33 | $8.1536 | $9.6959 |
| 3 per week | 12 | 13 | $24.4608 | $29.0877 |
| 1 per day | 28 | 30.42 | $57.2320 | $68.0578 |

*Annual planning averages: 52/12, 156/12, 365/12. A month is not assumed four
weeks. Exact calendar entitlements and leap-year/reset rules are not decided.
**Reuses FORECAST-v2's explicitly hypothetical 10% additional images rounded
up per five-minute project, historical-sized B narration correction, scaled
initial TTS and illustrative text/search costs. Assumes use as separate five-minute
projects. Equal credit duration split into different projects need not have
identical text/research/correction overhead. Excludes host/backup, image
input/thinking, taxes, charged failures without output, payment fees, support,
refunds and other production uncertainties. These are not subscription prices,
measured actual totals or guaranteed cost floors for all scene densities.

Charging two credits for a ten-minute project matches twice the initial image
output in the 112-image scenario. It does not prove all production stages scale
linearly or that edits have zero cost. Retained versions/local rendering continue
to cost storage/compute even where no new provider image is requested.

## Private Alpha comparison — distinct from subscription economics

With a hypothetical shared $12 host, average full usage by just one creator
costs $20.1536 / $36.4608 / $69.2320 for host + initial image outputs across
the three tiers. The latter two exceed $30 before other stages. Three creators
on the lowest tier likewise total $36.4608; five total $52.7680. Shared hosting
is counted once, not once per subscriber.

Consequently these future capacities must not automatically become free Alpha
allowances under the unchanged $30 total ceiling. Paid revenue is not assumed
to increase that owner-configured prelaunch ceiling. Public operation and its
budget/prices remain deferred. No owner workload for the free Alpha cohort has
yet been specified by this future-plan clarification.

## Pricing implication / remaining evidence

Image outputs alone are significant in the higher plans. Future sustainable
prices must account for full variable cost, shared fixed costs at realistic
subscriber counts, payment/tax obligations, paid failures, correction scope and
margin. Do not advertise the table's illustrative subtotal as an all-in cost or
select retail prices from it alone. No subscription/payment infrastructure
research, purchase or implementation is undertaken here.

S9 has owner-defined future demand scenarios but still lacks a complete
defensible private-Alpha operating envelope and target-host/backup evidence.
Keep Free-tier image quality/latency/bytes as explicit unknowns; no upgrade or
live pilot required/requested by this analysis. Further commercial policy is
separate from closing the existing Alpha architecture gate.

Reproduce `python3 spikes/operating-economics/tiers.py`.
[Raw tier/cohort scenarios](tiers-v3.json). Tests cover duration arithmetic,
weekly ratios, shared-host accounting and fail-closed budget conclusions.
Zero provider calls, purchases, deployment, production implementation or TASKS.md.
