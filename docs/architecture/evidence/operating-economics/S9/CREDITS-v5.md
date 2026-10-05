# S9 owner economics/credit amendment — revision 5

**S9: NOT_YET_PASS.** 2026-10-05. Documentation, disposable economics modeling
and deterministic local tests only. The $30/month prelaunch ceiling is unchanged.
No provider/API calls, paid spend, model/dependency downloads, production code,
TASKS.md, deployment or purchases. No other architecture phase is executed.

## Owner decisions and supersession

1. Private Alpha displays **both estimated credits and estimated USD** through
   the existing compact estimate and optional Details pattern. It supersedes
   v4's credits-only decision, not one-tap creation or optional financial review.
2. Preliminary topic credits remain duration / 5, default five minutes. Before
   script exists, expected images are approximately **12/requested minute**:
   36/60/120 for 3/5/10 minutes. This is an estimate, not a count mandate, cap,
   request ceiling or paid permission.
3. Topic research/script executes only with bounded authority and records its
   applicable cost/credit usage. Once the script exists, replace the heuristic
   with **one planned generated image per deterministic sentence**. Pasted
   scripts use that known scope immediately, without a topic image heuristic.
4. Preserve consumed valid operations when recalculating remaining production.
   Distinguish preliminary credits, updated predicted credits, consumed credits
   and internal USD authority; do not assume credits = images / 60.
5. Sentence scope is proposed work, not financial authority. Greater scope
   requires sufficient request/budget/quota admission and existing approval
   handling. No final materiality threshold is invented.

The three future paid subscription capacities stay separate from free Alpha
allocations; this revision sets neither retail prices nor tester allowances.
B coherent initial/corrected narration, continuous source audio and visual/
caption mapping semantics remain. One sentence/image does not imply a TTS call.

Preserved v1–v4 evidence and scripts: 30/40/56/80-image scenarios are historical
sensitivities, not competing production policies. The v4 40-image cap remains
a disposable financial witness; 56 remains the S6 extrapolation. Their older
"choose a universal density" next-step blocker is superseded. Historical tier
costs and capacity tables are not current sentence-derived forecasts.
[Old index](history-v5/s9-index-before-v5.md) preserves the full pre-v5 index.

## Source inspection / local sentence counter

Read the relevant product/architecture/gate/design/UX/cost documentation,
AGENTS.md, all existing S9 reports/JSON and spike scripts. No authoritative
production sentence parser was found. The legacy sibling `create_tts.py:202–210`
splits punctuation plus optional closing quotes/brackets followed by whitespace;
it is TTS preprocessing, not approved-script scope authority, and its regex may
consume punctuation. It was inspected as text, never imported or executed.

The smallest witness lives only in
`spikes/operating-economics/sentence_scope_v5.py`, standard-library Python.
Version **s9-local-terminal-punctuation-v1**:

- End a span at a run of `. ! ? । ॥`, followed by zero or more closing quotes/
  brackets, then whitespace or end of input. Preserve terminal/closing characters.
- Ignore surrounding whitespace. Count spans containing an alphanumeric
  character; punctuation-only/empty input produces no sentence scope.
- Count a nonempty unterminated tail as one local fragment and flag review.
- Preserve exact original-text start/end offsets and SHA-256; do not rewrite
  approved words, normalize away punctuation or ask an LLM to count.
- Deterministic edge-case flags cover abbreviations/initials, decimal punctuation,
  ellipses, quotes/brackets, missing boundary whitespace, line/list structure and
  unterminated tails. Flagged scope is not trusted for paid continuation by this
  witness. This is not a final production/parser/materiality policy.

For example, `Dr. Smith arrived. Next.` counts three under this limited rule
and flags review; it is **not** claimed to be linguistically three sentences.
`Price is 3.14 units. Next.` counts two but still flags numeric punctuation.
Closing quotes remain intact; simple Bangla/Hindi danda fixtures count correctly,
without certifying complete multilingual segmentation. Abbreviations, initials,
URLs/versions, dialogue, ellipses, headings/bullets, absent spaces/terminators
and language-specific conventions remain production parser planning cases.

## Economics with provenance / no invented total

Use S9's **owner-fixed $0.0336/1K image** for expected image-output cost. The
witness loads the rate from existing `analysis.json`, hashes that source and
records provenance. No Batch discount is used. This quote is image output only,
not all billable modalities, a per-attempt maximum or settled invoice.

| Input/scope | Predicted images | Preliminary credits | Expected image-output subtotal |
|---|---:|---:|---:|
| Topic, 3 requested min | ~36 | 0.6 | $1.2096 |
| Topic, 5 requested min | ~60 | 1 | $2.0160 |
| Topic, 10 requested min | ~120 | 2 | $4.0320 |
| Generated script fixture | 47 | Updated requirement unresolved | $1.5792 |
| Pasted script fixture | 7 | Actual-scope requirement unresolved | $0.2352 |
| Unexpected large script fixture | 214 | Updated requirement unresolved | $7.1904 |

The preliminary heuristic alone gives average monthly image-output sensitivities
$8.736 / $26.208 / $61.320 for the three future full-use plans. Actual scripts
replace those image counts; these are not subscription prices or forecasts of
complete bills. Actual script scope, not a universal duration-density constant,
now controls planned initial images.

The model maintains:

`Expected total = recorded incurred cost + updated remaining expected cost`

`Maximum financial exposure = retained unknown liabilities + reserved future maximum attempts/fees`

Check both against the distinct request authority and shared budget without
double-counting liabilities as settled charges. Full expected and maximum
project totals remain unresolved. Complete estimates eventually include applicable
research/script/checking, image input/thinking/output, TTS, justified retries,
compute/rendering, storage/backups/egress and tax/fees/FX. Unestablished components
remain null/pending rather than fabricated zero or hidden extra charges. The
prior rough text/TTS/search scenarios are historical sensitivity evidence, not
observed all-in project costs or refreshed production prices.

## Consumed / remaining / projected witness

Synthetic valid research and script events record $0.008 and $0.012, respectively
($0.020 total). These values are test inputs, not provider-rate claims or real
spend. Credit fields are pending policy, not zero. A separate test supplies
explicit synthetic 0.1/0.2 credit usages, verifies preservation and totaling,
and preserves partial-known versus pending credit usage without defining debit.

For the 47-sentence update:

- Consumed: $0.020 recorded fixture cost; total consumed credits unresolved.
- Remaining known image-output subtotal: $1.5792; predicted credits unresolved.
- Projected known subtotal: $1.5992. Full USD/credit totals still pending.

The obsolete 60-image quote is replaced, not added. Prior paid operations are
not reset/refunded/erased. A pasted-script estimate does not invent previous
script-generation spend; factual-checking work remains applicable independently.
Creator-facing fields can coexist while each reflects its certainty; existing
Details/progress patterns are reused without final UI copy or a new screen.

## Unexpected scope and independent authority

An explicit **synthetic** authority fixture permits 60 image attempts, with
image maximum $8.355840, whole-request $8.50, recurring obligations $12 and
unknown holds $0.50. It is supplied by deterministic fixture setup, never
inferred from 12/minute or trusted model output. No numeric materiality threshold
or production 60-image cap is adopted.

The historical conditional S4 full-serving-cap attempt bound, loaded from S9
evidence, is $0.139264 before fees. It is **not refreshed/certified live authority**:
endpoint/billable-cap enforcement, fees and final attempt constraints remain open.
One initial attempt per planned image is used solely in this bound test; retries
would require additional separately admitted exposure and quota.

- 47-sentence case: within those fixture image bounds only; cannot submit real
  provider requests, since full project/endpoint/credit policy is not established.
- 214-sentence case: proposed scope is measured exactly, expected image output
  $7.1904, conditional image exposure **$29.802496**. Although the known expected
  subtotal $7.2104 is below $8.50, scope and maximum exposure exceed the original
  authority; shared budget/quota also fail. State:
  **ADDITIONAL_AUTHORIZATION_OR_BUDGET_HANDLING_REQUIRED**.
- Prior valid consumption, unknown holds and authority remain unchanged. No
  image requests occur. The model cannot enlarge ceilings/attempt counts.
- Separate tests show retained unknown liability and the current Free zero
  image quota block otherwise smaller plans. Changing displayed credits alone
  cannot change USD admission.

## Tests / reproduction / evidence integrity

Run from repository root:

```sh
python3 spikes/operating-economics/sentence_scope_v5.py
```

**40 local checks PASS**: required A–F topic/generated/pasted/large/deterministic/
credits-USD cases, consumed work preservation, no stale-quote addition, pending
credits, punctuation/quote/decimal/danda/abbreviation fixtures, invalid duration,
budget/quota/exposure blocking and immutable authority. No imports of provider
clients, sockets, HTTP, subprocess execution, model downloads or dependencies.
The witness contains no request-sending path. This is not a production parser,
spending ledger or end-to-end provider test, nor independent application acceptance.

[Raw results](credits-v5.json), exact text fixtures `fixtures-v5/`,
[revision manifest](revision-v5-manifest.json). Prior S9 report/JSON/script hashes
are preserved; only the index gains current status. No source narration/media
is rewritten. Earlier S9 scripts are not rerun to overwrite their results.

## Remaining S9 requirements / verdict

| Requirement | Current evidence / unresolved portion |
|---|---|
| Expected representative project cost | Image-output arithmetic established; complete real/validated 3/5/10-minute components and distributions unresolved |
| Maximum project financial exposure | Conditional image-only fixture demonstrated; full stage/attempt/fee caps and active endpoint/account evidence unresolved |
| Post-script credit recalculation/debit | Open owner product-policy item; consumed script/research conversion and final duration basis also unresolved |
| Corrections/regeneration credits | Unresolved; B affected-segment costs and image edits still require bounded authority |
| Image failure/retries/quality/bytes | Not measured on current Free zero-capacity account; future evidence or explicit accepted bounded scenario policy needed, no calls requested |
| Hosting / target-host resources | Candidate historical quotes/S6 local resources only; no selected validated one-host render/alignment deployment economics |
| Storage / backup / traffic | v2 sensitivity/S8 local proof only; actual retained sizes, off-host purge and provider-volume/egress terms remain open |
| Taxes / fees / FX / current obligations | Account-specific basis and remaining real budget unknown |
| Cost-grounded Alpha allowances | Cannot derive a defensible complete allowance from partial image tariff/heuristic alone; no fixed numerical allowance chosen |
| Full monthly operating envelope | Not established within unchanged $30 including fixed obligations, all generation, corrections and paid failures |

**S9 stays NOT_YET_PASS.** Selecting a universal 30/40/56/80-image density is no
longer an open production-policy decision. One planned image per deterministic
sentence resolves that rule, not full economics or paid authority. No blanket
INFEASIBLE verdict is established for all compliant workloads.

**Single smallest useful next step:** resolve the operation/scope-to-credit
recalculation/debit policy, including how already-valid script/research usage
is credited. This allows the four separate creator credit fields to be modeled
numerically without assuming images / 60; financial/runtime evidence still
remains afterward. No implementation plan or further phase follows this revision.
