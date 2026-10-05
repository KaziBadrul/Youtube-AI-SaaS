# S9 revision 6 — variable production cost basis

2026-10-05. **S9: NOT_YET_PASS.** Local arithmetic and existing receipts plus official public pricing only. No generation/provider API requests, paid spend, account activation, production implementation, TASKS.md, deployment or purchase. $30/month total ceiling unchanged. No final credit formula or Alpha allowance selected.

## Authority and evidence

Read docs index, Alpha specification, architecture/spike gates, cost/artifact/job contracts, design/UX, pipeline investigation, AGENTS.md, S4/S4-R, S5 generation/ledger/final B mapping closure, S6 rendering report and all earlier S9 revisions/results. v5's decisions remain authoritative: topic preliminary images ~12/minute, credits minutes/5; known-script images equal deterministically counted sentences; credits and USD authority are separate; consumed work survives estimate replacement. Nothing here changes those decisions.

Historical v1–v5 reports/results/scripts are preserved. v2's four searches, 20K/10K text tokens, 10% image additions and one correction were illustrative sensitivities, **not evidence of normal successful project usage**. v5's $0.008/$0.012 consumed events were synthetic accounting fixtures, not observed research/script costs. Neither is promoted to an expected-production measurement. No universal image-density choice is reopened.

Pricing rechecked **2026-10-05**, Standard service, official public pages only:

- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing): image input $0.25/M, text/thinking output $1.50/M, image output $30/M; owner-fixed **$0.0336 per 1K-resolution image**, not per thousand images. TTS Lite input $0.50/M and audio $6/M through 2026-12-31; announced 2027 rates double both. Tool-free Gemini 3.5 Flash-Lite reference text $0.30/M input and $2.50/M output including thinking. This text reference is conditional S4-R economics, **not final model adoption**. No Batch discount, caching or grounding assumed.
- [Tavily credits](https://docs.tavily.com/documentation/api-credits): Basic Search one credit; PAYGO $0.008/credit; advertised no-card allowance 1,000 credits/month. No subscription/account activation or verified remaining free entitlement.

Machine-readable [pricing record](pricing-v6.json) identifies dates, rates, source URLs, free-tier qualification and expiry. Serving caps used below are **historical conditional S4/S5 evidence**, not a fresh endpoint/account certification. Refresh enforceable capabilities, rates and applicable fees before any future paid admission.

## Required operations: topic vs pasted script

| Operation | Factual topic workflow | Approved pasted-script workflow | Cost evidence / missing input |
|---|---|---|---|
| Research/check query planner | Bounded tool-free text plan | Bounded claim/query plan | Text model/config, prepared input/output/thought usage unknown |
| Application-owned Basic Search | Research before writing | Factual checking | $0.008 per first-pass query; representative query count UNKNOWN |
| Evidence synthesis/checking | Research synthesis | Private warnings/correction proposals | Text usage UNKNOWN; combined vs separate synthesis/writing calls not frozen |
| Script writing | Required | Not applicable: preserve supplied words | Topic text usage UNKNOWN; pasted initial writing cost explicitly $0, not unknown |
| Scene/visual descriptions and image prompts | Required content preparation | Same | May share a bounded text operation; concrete request inventory and usage UNKNOWN |
| Generated images | Planned sentence images | Known sentence images | Output tariff known; input/reference and text/thinking usage UNKNOWN |
| Coherent B narration | Initial contiguous segments | Same | Call 4 measured, duration proxy below; production grouping/config not frozen |
| Expected charged failures/retries | Applicable | Applicable | No defensible failure probability or mean failed-attempt charge |
| Local alignment/captions/motion/music/render | No AI generation request required | Same | No separate provider API fee in tested runtime; allocated host resource cost UNKNOWN |
| Retained assets/versions, backup, egress | Applicable | Applicable | Actual image bytes/retention/traffic and host allocation UNKNOWN |
| Taxes, fees, FX | Account/location dependent | Same | Applicable financial uplift/bound UNKNOWN |

Separate factual checking is **only for pasted scripts**; do not add another mandatory topic check on top of research. Non-factual topics may omit research according to scope; the representative rows below retain the factual educational workflow. No required standalone humanization, character-planning, AI voice-tagging, hosted ASR, AI Director or paid music service is inferred from legacy code. Conditional approved translation/adaptation and correction proposals can add text operations; they are not normal baseline charges. Optional library music uses the selected local render path; this does not prove a commercial library's licensing cost is zero.

For any conditional reference text operation, `C_text = (0.30*input_tokens + 2.50*output_and_thinking_tokens)/1,000,000`. Image non-image overhead is `(0.25*input_tokens + 1.50*text_and_thinking_tokens)/1,000,000`; do not add image tokens twice. Research first-pass search fee is `0.008*N`. Rates give arithmetic; they do not supply missing normal quantities.

## S5 receipts and legitimate extrapolation

[Existing ledger](../../narration-feasibility/runs/approved-lite-v1/ledger.json) records eight successful Standard Lite TTS submissions, zero retries/unknown outcomes/capacity failures. Total 1,580 prompt and 13,030 audio tokens: **$0.078970 paid-tariff equivalent**, not a settled invoice or one-project price.

- **Call 4 B initial**: 498 words, 32 historical scene memberships; 664 prompt tokens, 5,488 audio tokens, 171.48 seconds. `664*0.5/M + 5488*6/M = $0.033260`.
- **Call 6 B correction**: entire affected coherent segment, 498 words, 664 prompt tokens, 5,466 audio tokens, 170.80 seconds. **$0.033128**. Other segments/sibling assets need not be regenerated. Mapping and dependent timing/render work must be recomputed locally.
- Calls 1–3/5/7/8 test other strategies/restoration, not mandatory extra production calls in B+B. Do not spread the whole experiment total over a project.

Duration proxy: `TTS(d seconds) ~= 0.033260 * d / 171.48`. It includes proportionally scaled prompt cost; fixed per-segment style overhead, delivery, segment count and pacing may differ. This is a useful **projection from one initial segment**, not a measured 3/5/10-minute bill or proven universal mean. Reported audio density is ~32.0037 tokens/s, while the pricing page's duration equivalent uses 25/s. Use actual receipt tokens for this witness; do not replace them with the cheaper advertised duration approximation. Billing discrepancy/invoice settlement remains unverified. Eight mixed successful samples cannot establish zero production failure risk or a retry distribution.

## Representative topic projects — paid equivalent

USD, rounded for display; exact Decimal arithmetic in [results](credits-v6.json).

| Required component | 3 minutes | 5 minutes | 10 minutes |
|---|---:|---:|---:|
| Preliminary planned images | ~36 | ~60 | ~120 |
| Research/search | UNKNOWN | UNKNOWN | UNKNOWN |
| Research planner/synthesis | UNKNOWN | UNKNOWN | UNKNOWN |
| Script generation | UNKNOWN | UNKNOWN | UNKNOWN |
| Separate pasted factual check | N/A | N/A | N/A |
| Scene/visual/prompt planning | UNKNOWN | UNKNOWN | UNKNOWN |
| Image output subtotal | $1.209600 | $2.016000 | $4.032000 |
| Image input/text/thinking | UNKNOWN | UNKNOWN | UNKNOWN |
| Initial B TTS duration proxy | ~$0.034913 | ~$0.058188 | ~$0.116375 |
| Other required standalone AI | None identified | None identified | None identified |
| Expected charged failure/retry reserve | UNKNOWN | UNKNOWN | UNKNOWN |
| Compute/storage/backup/egress allocation | UNKNOWN | UNKNOWN | UNKNOWN |
| Applicable tax/fees/FX | UNKNOWN | UNKNOWN | UNKNOWN |
| **Image output + TTS proxy ONLY** | **~$1.244513** | **~$2.074188** | **~$4.148375** |
| **Complete expected variable cost** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |

These partial proxies are neither full expected cost, maximum liability, UI quote nor authorized scope. Requested duration need not equal eventual narration duration. Once text exists replace preliminary image scope rather than adding a second image estimate. Retain already consumed valid research/script receipts separately. Retry reserve remains unknown rather than silently zero; optional discretionary edits are additional scope, not automatically baked into a normal first-success estimate.

### Known-script witness

Reuse exact Call 4 approved `block_original` from [fixture manifest](../../narration-feasibility/fixture-manifest.json). The unchanged v5 deterministic counter returns **38 sentences**, not 32 historical scene memberships. Ellipses and quotations flag **REVIEW_REQUIRED**: this is reproducible local economics scope, not certification of the future production sentence parser. Original approved text and request provenance stay unchanged.

Conditional 38-image output subtotal **$1.2768** + measured initial TTS **$0.033260** = **$1.310060**, excluding checking, planning, image overhead, failures and infrastructure. As pasted input it needs no initial script-writing charge, but factual checking is still UNKNOWN and not automatically cheaper than topic research. A reused already-generated S5 WAV incurs no new spend in this task; its receipt illustrates historical generation economics only. Sentence count does not force 38 TTS requests or cut continuous narration.

## Corrections

- One regenerated image: **$0.0336 output** plus UNKNOWN request input/reference/thinking and charged-failure costs. Conditional full-cap bound **$0.139264/attempt**, **$0.417792** for three admitted attempts, before fees. Prompt regeneration can add separately authorized text cost.
- B narration edit: regenerate only the **affected coherent segment**, preserve previous audio/mappings as history and unaffected sources; never revert to isolated surgical scene stitching. Historical Call 6 costs **$0.033128** for its ~171-second segment. General segment cost uses actual prompt/audio usage or the qualified duration proxy; no universal segment size set. Conditional cap **$0.102400/attempt**, **$0.307200** for three attempts, before fees. Changed wording may invalidate relevant planning/images as defined by dependencies, not automatically every sibling image.
- Research/checking retry, approved script correction/translation/adaptation, scene/prompt revision: scoped query/text formula applies, usage UNKNOWN. Restoring compatible existing versions makes no new generation request; retained history, alignment and rerender resources still count operationally.

Final correction-credit debit policy remains unresolved.

## Maximum authorized exposure — conditional, not expected spending

Historic S4 image cap basis: input 65,536 tokens at $0.25/M plus output 4,096 at highest modality $30/M => **$0.139264/attempt**. TTS input 8,192/output 16,384 at $0.50/$6 => **$0.102400/attempt**. Reference text full-cap 1,048,576 input/65,536 output at $0.30/$2.50 => **$0.4784128/attempt**. Caps/rates must be valid for pinned endpoint/config before live use.

| Image scope only | Initial full-cap liability | Up to three attempts/image |
|---|---:|---:|
| 36 | $5.013504 | $15.040512 |
| 60 | $8.355840 | $25.067520 |
| 120 | $16.711680 | $50.135040 |

Three-attempt image liability for a 10-minute preliminary scope alone exceeds the unchanged $30/month ceiling. This rejects that particular full-cap reservation scenario, not all 10-minute production: fewer admitted attempts or independently validated tighter bounds may differ. No permission to relax ceilings or promise retries that do not fit.

For admitted queries N, bounded reference text operations J and coherent TTS segments K, conditional all-three-attempt bound before fees is:

`L = 0.417792*images + 0.024*N + 1.4352384*J + 0.307200*K`

This formula counts each text operation once (including planner/synthesis/script/planning where distinct), no separate duplicated retry reserve. It is deliberately conservative serving-cap fallback, not a likely cost. N/J/K and validated endpoint/cap/fee basis remain unresolved, so **maximum authorized variable exposure for each complete representative project is UNKNOWN**. Model output cannot supply authorization. A normal successful cost is not multiplied by three. Persist every attempt, including chargeable invalid outputs; uncertain outcomes retain their liability/quota holds and do not trigger blind duplicate requests. Actual admitted attempts may be 1–3 and must fit request authority and shared funds after other obligations. New manual corrections need new authority, not a reset of the failed operation.

## Paid equivalent vs possible Alpha cash

Paid-equivalent values above persist even if some operations use free quotas. Tavily published free credits and Gemini published free text/TTS can reduce cash **only after verified available account entitlement, allocation and usage reconciliation**. Search cash formula for otherwise allowed Basic requests is `0.008*max(0, requests - allocated_free_credits)`; token/request quotas constrain eligibility separately. No complete cash total is established.

Owner's current image Free account has zero RPM/TPM/RPD; official image tariff lists Free unavailable. Therefore image production is **BLOCKED**, not a successful zero-cost video. Conditional Tier 1 quotas are not active access or free credits; no upgrade is authorized. If paid images become independently authorized, image-output cash subtotal remains $1.2096/$2.016/$4.032 absent evidenced discounts, plus overhead/fees/failures. Advertised free access alone cannot support long-term viability or Alpha allowance promises.

## Local verification and preservation

Run from repo root: `python3 spikes/operating-economics/variable_cost_v6.py`.

**37 checks PASS**: image scope/rates at three durations, TTS receipts and eight-call total, per-token/search arithmetic, known and unknown-safe sums, conditional maximum aggregation, no expected-cost retry multiplier, topic vs pasted, deterministic sentence scope, correction costs, free/cash distinction, partial-free arithmetic, zero quota rejection, invalid attempt-count rejection and unresolved final credits. Synthetic known-input arithmetic checks are identified as fixtures, not normal production assumptions. Stdlib only; imports the existing disposable v5 counter without running its writer. No network, SDK/client, credential or production imports.

[Revision manifest](revision-v6-manifest.json) records source/generated hashes and unchanged prior S9 reports/results/scripts; exact pre-v6 index preserved in `history-v6/s9-index-before-v6.md`. Public website inspection is not a model generation/API call. No dependency or model download.

## Closure assessment and smallest next step

Established: required cost-bearing paths, current tariff basis, exact historical B initial/correction charges, qualified duration proxy, sentence-based known-script scope, conditional finite component exposure, unknown-safe arithmetic and cash/paid separation. Cost information now available for eventual credit policy is image output tariff, observed coherent narration receipts and per-query/per-token formulas; no complete stage-cost proportions or final conversion follow from them.

Still unresolved:

1. Final text model/config and concrete normal operation inventory; representative research query and input/output/thought usage for topic and pasted workflows. No corresponding real production receipts found.
2. Image input/thinking usage, real charged failure/retry/quality/size evidence and expected failed-attempt distribution. Free image capacity blocks new evidence now; no live pilot requested.
3. Final B segment sizing/count and validated cap/account/quota basis; maximum whole-project exposure with taxes/fees and unresolved liabilities.
4. Final post-script credit recalculation, actual consumption/debit, edits/regeneration/reset policy and material-scope handling threshold.
5. Hosting choice/availability/current obligations; target-host render/alignment RAM/CPU/disk, storage/versions, backups/purge, bandwidth/egress, taxes/fees/FX. S6's 3/5/10-minute local synthetic renders (44.64/79.42/237.20 seconds; 17.88/29.43/59.55 MB exports) establish feasibility, not target-host costs or real image compressibility. Fixed shared hosting is not itself a per-project API charge; allocation requires a stated workload.
6. Complete $30 operating envelope and cost-grounded meaningful Alpha capacity/allowances; future paid tiers are not free Alpha allocations. Current account cannot generate the required images.

**S9: NOT_YET_PASS.** Partial output costs cannot satisfy the complete operating gate.

**Single smallest useful next step:** pin a disposable, tool-free **text/research operation manifest for one five-minute factual topic**, reusing a local fixture: specify conditional model, distinct steps, deterministic query cap and bounded prompt/output/thinking caps. Prepare inputs locally and identify any already-existing compatible usage receipts. This supplies auditable N/J and the missing text/search exposure structure without provider calls; prepared-input token counts need a validated local tokenizer or serving-cap fallback and do not pretend to predict generated output usage. Normal expected text/search usage remains unknown until adequate receipts or explicitly labeled planning assumptions exist. No production implementation or new phase is authorized by this suggestion.
