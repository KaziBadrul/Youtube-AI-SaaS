# Private alpha product specification

## Accepted owner budget amendment — 2026-10-05

The active total prelaunch / Private Alpha operating ceiling is **US$40/month**, explicitly increased by the owner from US$30. This supersedes prior $30 wording wherever it described current financial authority. Historical interview/discovery notes and S9 V1–V11 evidence retain the $30 ceiling applicable when recorded; they do not control the current limit.

The $40 is a total owner cash-spend ceiling, not a generation-only allocation, creator credit balance or per-project authorization. Fixed obligations, actual spending, financial reservations and unresolved liabilities remain accounted for; safety/tax/payment/FX reserves and creator allowances remain unresolved. No automatic increase in credits/allowances, provider purchase/call or production implementation follows. See [current S9 reassessment](architecture/evidence/operating-economics/S9/CREDITS-v12.md). The owner’s rule ending host-sizing experiments unless failure remains in force.

## Owner decision — Research entitlement and topic discovery, 2026-10-05

This accepted amendment supersedes universal factual-topic Research availability.
Research means the existing bounded factual-topic research/search capability,
not a new service. Usage offerings **3 videos/week** and **1 video/day** are
allowance-tier descriptions, not final plan names or prices. The previously
recorded 1 video/week offering remains historical future-plan context, not a
newly named commercial lower tier. No prices, exact credit allocations,
rollover, overages, upgrade prices or launch dates are decided here.

| Feature | Lower tier | 3 videos/week | 1 video/day |
|---|---|---|---|
| Research | No | Yes | Yes |
| Topic Suggestions | No | Yes | Yes |
| Custom Topic Suggestions | No | Yes | Yes |
| Expert Topic Suggestions | No | No | Yes |

“Lower tier” means any offering below 3 videos/week; its final identity/name
remains unresolved. Yes means feature entitlement, not unlimited usage or
sufficient spending authority. This is the canonical entitlement matrix.

### Three distinct discovery levels — product decisions, release unassigned

1. **Topic Suggestions**: random discovery from a large curated, stored topic
   database/collection. The creator requests a suggestion with **Surprise me**,
   requests another, or uses a suggestion as the starting topic for a new video.
   No per-click LLM is required. Final storage technology/schema, collection
   size, curation/moderation and random-selection/recommendation details remain open.
2. **Custom Topic Suggestions**: creator selects one or more categories/interests
   and requests tailored YouTube video ideas. Owner-selected model:
   **`gemini-3.8-flash`**, subject to provider availability/feasibility at
   implementation time. Do not silently substitute another model; unavailability
   or unacceptable economics requires an explicit product/architecture update.
3. **Expert Topic Suggestions**: channel- or niche-informed ideas from a specific
   YouTube channel, creator/channel name, channel link, or described niche.
   Only the 1 video/day offering is eligible. A channel URL is not proof that
   Gemini can inspect the channel. Model selection and any bounded permitted
   channel retrieval remain unresolved. A described niche may need no retrieval.

The three levels have distinct behavior, entitlements, economics and provider
requirements; do not collapse them into a generic AI Ideas feature. Returned
suggestions do not authorize video generation or spending; the creator chooses
whether to use an idea in the existing New Video flow.

### Alpha scope and factual policy

Research is already in the Alpha workflow and is now entitlement-gated. For
eligible users, factual-topic research remains automatic before script writing,
with unchanged bounded retrieval, private provenance/warnings, failure behavior
and factual-quality requirements. Users below the eligible offerings do not
receive Research: make that absence clear and never claim the topic was researched.
Non-entitlement is not a failed Research attempt and cannot offer a retry that
bypasses entitlement. The existing separate pasted-script factual-check policy
is unchanged; this decision does not silently extend the Research gate to it.

The three topic-suggestion features are accepted product/entitlement decisions,
**not required first Private Alpha deliverables**. Their Alpha-versus-later
shipping decision is unresolved. Do not expand the Alpha acceptance gate or
introduce public billing. Mapping private-Alpha accounts/validation identities
onto these feature entitlements still needs an explicit policy before activation;
free Alpha allowance alone does not imply an eligible commercial tier.
Existing factual-quality criteria are not waived for lower-tier output.

Entitlements must be checked server-side from authoritative persisted account/
subscription state, before any Research, suggestion generation or potentially
paid Expert retrieval. Frontend controls, routes and client plan names are not
authority. Entitlement alone never grants financial, quota or retry authority.

### Open discovery and entitlement decisions

Final plan names/prices and lower-tier identity; exact allowances, rollover and
overages; suggestions per generation; request frequencies/quotas; video-credit
versus separate suggestion allowance; database size/curation/moderation;
Expert model and channel name/URL resolution, official/permitted data API,
retrieval bounds/costs, retained data and unavailable/private-channel behavior;
suggestion history/saving; Alpha release timing; exact paywall/upgrade UX and
private-Alpha entitlement assignment. No values are inferred by this amendment.

Owner S9 revision 5, 2026-10-05: Private Alpha estimates show **both credits
and estimated USD cost**, superseding the prior credits-only display decision.
Credits remain separate from internal financial authority. Topic preliminary
credits = requested minutes / 5, default five minutes; preliminary image count
is approximately 12 per requested minute (36/60/120 for 3/5/10 minutes). Once a
script exists, predicted generated images = its deterministic sentence count,
one planned image per sentence, for generated and pasted scripts alike. The
12/minute heuristic is neither a scene cap nor spending permission.
Consumed valid research/script work remains accounted for when the remaining
estimate changes. Post-script predicted credits, operation-specific debit and
correction credit rules remain unresolved; do not assume images / 60. Future
paid subscription tiers remain separate from free Alpha allocations. The
$40/month ceiling now applies under the owner budget amendment; internal USD bounds and reservation rules remain unchanged.

Status: confirmed Alpha product definition, approved by the user on 2026-10-03 after Round 11. Deferred choices below remain undecided. See [decision history](PRODUCT_DECISIONS.md), [provisional roadmap](FEATURE_ROADMAP.md), and [domain language](../GLOSSARY.md).

User clarification: creator review or display of estimated cost and maximum spend is optional, not a prerequisite for paid authorization. Create Video itself authorizes bounded production and starts generation directly, with no intervening estimate, confirmation or review screen. Financial details may remain in optional Details. Server-side cost bounds, allowance/budget reservations, retry limits and reconciliation remain mandatory. Required script-preservation/translation/adaptation approvals and material scope changes remain distinct from routine cost review.

## Outcome and audience

A solo creator supplies a topic or complete script and receives an editable, fully narrated image-based video. The initial production job is a faceless educational YouTube explainer, 3–10 minutes in 16:9. One-minute 9:16 output follows landscape quality validation. Platform publishing and deriving short-form variants are deferred.

Support built-in narration, generated still images, optional basic motion, toggleable captions, and optional library music. Uploaded video clips, custom audio, and recurring-character management are deferred. Image replacement is included; file-upload limits and technical per-asset validation details are deferred to the pre-invitation operational specification.

## Release sequence

1. Owner-only validation on real projects.
2. Invite approximately 3–5 target creators after the acceptance gate passes and private identities, project/asset isolation, and allowances are available.
3. Deliver standalone vertical output and animated Emphasis Text as follow-up Alpha milestones, not requirements for the first end-to-end Alpha release; their relative order is uncommitted.

One solo engineer delivers the product. There is no fixed public-launch date. The current strict total prelaunch Alpha operating ceiling is US$40/month, ideally zero, including generation, research, hosting, storage, and tester usage. The ceiling is owner-configurable: explicit owner approval can revise it; it is not a permanent or hardcoded budget. Architecture decisions must not assume this ceiling remains permanent after validation. Pause new paid operations at the ceiling; only an explicit owner decision raises it. Do not choose fixed allowance/storage amounts before measuring actual production cost and asset sizes. Concrete limits must be recorded before invitations; no per-video cost or allocation formula has been agreed.

## Alpha operating experience

Owner-only validation may run locally. Invited testers use private web access during announced availability windows. Permit one active production job at a time and show queue status. Do not promise completion times before measuring them.

Reserve tester allowance and shared operating budget before admitting work. Admit requests in order; queue work that cannot fit. Shared-budget reservations account for paid failed attempts and permitted retries. Do not start operations whose expected maximum cost exceeds authorized limits. Provider cost-bounding feasibility is unverified; this is a requirement, not evidence of a guaranteed implementation.

## Generation and factual handling

### Owner-accepted staged estimation and sentence-driven image scope

For topic input, display preliminary duration credits and an approximate USD
estimate using the 12-images/minute heuristic, with unresolved cost components
identified. Proceed only under bounded authorization for script/research work.
Those executed operations record applicable USD and credit usage; missing credit
conversion policy does not imply zero usage. Once script generation completes,
deterministically count the script's sentences and recalculate remaining image/
production cost and predicted credits. Keep consumed usage, remaining estimate
and projected total distinct; never reset already-spent work or add the obsolete
preliminary estimate to the replacement estimate.

For approved pasted scripts, count sentences immediately; predicted generated
images equal that count. Do not apply the 60-image heuristic to known text or
rewrite submitted words silently. Factual checking retains its existing policy.
Production sentence parsing is not selected by this economics amendment; the
S9 local witness records versioned rules and ambiguity cases for implementation.

Sentence count proposes planned image scope; it does not grant financial
authority. If a five-minute topic produces 214 sentences, report 214 predicted
images and the revised cost. Block further paid production when request-specific
authority, shared budget, quotas or required scope approval do not suffice,
preserving consumed valid work. Final material-scope thresholds remain open;
neither model output nor the preliminary heuristic can enlarge authority.
Sentence-driven planned images do not imply one sentence per TTS request: B
coherent narration generation/correction and continuous narration remain.

Simple Mode starts production directly when Create Video is clicked. Estimate and spending-ceiling display/review are optional; the action authorizes production within the system-enforced request ceiling. Additional approval is required to exceed it, including through retries.

For users entitled to Research, research factual topics before script writing. Users below 3 videos/week do not receive Research; disclose that it is unavailable under their offering. Run the separate factual check only on pasted scripts; its existing policy is unchanged. Entitled Research and applicable checking are automatic and non-blocking. Warnings and sources appear privately to the creator, never inside the exported video. The same non-blocking warning policy applies to disputed general facts and sensitive-topic claims.

Preserve pasted script wording unless the creator approves proposed changes. Show proposed factual corrections and allow individual or all-change acceptance. Approval changes script text; it does not independently authorize paid regeneration. Research failure and translation/adaptation behavior are defined below.

## Language

English is the default. The selected language controls script, narration, and captions. Offer English, Spanish, French, Bangla, and Hindi. The ten-project invitation acceptance set covers English only and does not establish quality in the other four languages. The earlier all-five-language validation gate is superseded. Label Spanish, French, Bangla and Hindi experimental. Before enabling each, verify narration generation, correct caption display, and export. The publishability claim applies only to validated English output; additional languages remain experimental.

## Creative controls and script fidelity

Simple Mode requires input and an output-language setting defaulted to English. Style, voice, duration, captions, motion, and music controls are optional. Start with three curated visual presets and one coherent style per project. Presets are Minimal Illustration, Storybook, and Documentary Illustration. Default to Minimal Illustration, five-minute topic videos, captions on, gentle motion on, and music off. Offer a small set of previewable voices per supported language. Custom styles and guaranteed recurring-character identity are deferred.

Preserve pasted scripts. Above ten minutes, show estimated duration and require creator shortening or approval of a proposed adaptation. Translation requires approval when pasted language differs from selected output language. Topic scripts may be written to selected duration and language automatically. Allow shorter landscape scripts unchanged; show duration and never pad without approval. The three-minute lower bound describes the primary job, not an enforced minimum.

## Failure and concurrent-edit behavior

If an entitled Research operation or applicable checking is unavailable, continue with a private research-unavailable or checking-incomplete notice, preserve collected sources, and offer retry within entitlement and authority. If Research is not entitled, explain its plan requirement without submitting work or offering a bypass retry. Never imply checking succeeded.

Preserve successful work after partial failure and identify failed scenes. Offer retry or image replacement. Do not silently export missing visuals or substitute placeholders. The creator may explicitly delete failed scenes and render the remaining video.

Allow edits during asset generation. Operations use their starting input version. If that input changes, retain the arriving result as a previous version rather than making it current, and show consumed allowance. Paid regeneration requires authorization. Queued authorization is bound to reviewed input/settings versions; changed queued inputs pause affected work for an updated plan and confirmation while compatible completed assets survive.

## Correction workflow

Creators can edit narration and visual prompts; regenerate individual images or narration; replace images; correct captions; adjust timing; reorder/delete scenes; and rerender. Preserve previous image/narration versions. The Director, timeline, reusable style studio, and extensive model controls are deferred.

Save narration edits immediately. Mark affected narration audio, timing, captions, and the final render outdated. Keep its image unless its visual description changes. Offer cost details optionally for regeneration and never silently export outdated narration. Restore compatible timing/captions with earlier narration when available; otherwise mark them outdated. If an older audio version contains different words, show its associated text and require approval to restore text/audio together, updating current script consistently. Restoration also displays recorded voice/delivery: approval adopts those settings for the restored scene only, preserving other scenes and project defaults. Subsequent regeneration displays its effective voice before authorization. Preserve incompatible manual caption/timing corrections and propose refreshed output; resolve enabled-caption blockers before export, while required audio/video timing remains valid regardless of caption toggle. Restoring existing assets costs no generation allowance, but any regeneration shows its cost separately. Caption styling/toggle, motion, music, and scene order affect rendering without regenerating images/narration. Image replacement affects rendering only. Caption text edits preserve narration. Flag manual timing conflicts rather than silently cutting off speech. After narration edits, preserve images and flag visual review; let the creator explicitly keep or replace them, with optional image-generation cost details. Keep the current script consistent with remaining scene narration and order while preserving original input separately. Reorder/delete invalidates the final render and preserves surviving images/narration. Defer adding/duplicating scenes to public MVP.

## Rendering and project lifecycle

Owner timing clarification, 2026-10-05: automatic image transitions occur at the next scene's mapped narration start, not at the previous scene's spoken end or the midpoint of a pause. Keep the previous scene's image visible through the intervening pause. This visual timing rule does not cut continuous narration or redefine word/caption timestamps. The first scene image covers any leading narration silence and the last scene image covers remaining narration duration; manual timing changes must retain the accepted conflict checks.

While final rendering is ongoing, all project-content changes are grayed out and prohibited, including deletion, asset restoration and accepting script corrections. Viewing, downloading existing exports and cancellation remain available. Asset generation allows concurrent edits; final rendering does not. Include cancel/retry and retain the last successful export. Release the edit lock on completion, failure, or confirmed cancellation. Recover interrupted renders without permanent locks. Rendering retry reuses generated assets.

Include create, rename, autosave, reopen and delete. Defer project duplication and archiving. Preserve assets during active alpha testing, show storage usage and require an owner-set storage cap before invitations. Pause new asset creation at that cap rather than silently deleting previous versions. Project deletion requires explicit confirmation. Hide confirmed deleted projects immediately, retain them for seven days for restoration, then permanently delete them; explain this window in confirmation. Retained deleted assets count against storage. Keep active alpha projects until an announced end date, then give testers 14 days to download before deletion. The exact storage cap remains open. Deletion is prohibited during active generation as well as rendering; cancel and wait for confirmed cessation first. Under accepted architecture-discovery clarification A9, active project content is purged at the seven-day deadline and backup copies within the next daily purge cycle, at most 24 hours later. Purged content must not be restored from older backups. Non-content accounting/deletion records may remain for reconciliation.

## Allowances

Invited testers receive predefined free allowances. Technically valid, delivered generated assets consume allowance even if subjectively unsatisfactory. Elective regeneration consumes additional allowance. Failed operations release reservations; corrupt, missing, or technically invalid outputs are failures. Successful assets still count if another project operation fails. Automatic retries stay inside the authorized ceiling.

Show estimated and consumed US-dollar-equivalent allowance; do not sell credits yet. Allow at most two automatic retries per failed operation within approved ceilings, then offer manual retry. Track actual provider spending separately, including failed attempts that cost money. Per-tester allocation remains deferred until measurement; reservation and one-job queue rules are defined above. Free allowances do not override the shared monthly operating ceiling. Successful paid text, research and factual-checking results also count against allowance, with optional cost details. Failed/unusable results consume actual operating budget but not successful-output allowance. Local transformations and rendering do not consume generation allowance.

After cancellation, stop new work and attempt provider cancellation where supported. Valid late output already paid for is retained in history, not automatically selected, and counts against allowance if delivered. Keep unknown paid outcomes/reservations pending reconciliation rather than blindly retrying.

Monthly accounting uses calendar months in Asia/Dhaka. Reserve recurring infrastructure before generation. Retain unresolved previous-month liabilities; authorize new paid attempts against the new period. Include actual fees, taxes and currency conversion in accounting. Provider invoice timing still requires evidence and reconciliation.

## Invitation acceptance gate

Evaluate ten real English landscape projects spanning both input types and the 3–10-minute range. At least eight must be publishable after no more than 15 minutes of scene-level corrections each. Missing narration, broken timing, unreadable enabled captions, and serious factual errors fail acceptance. Disabled captions do not fail acceptance. Non-blocking factual warnings do not waive factual quality requirements.

Also demonstrate interrupted-generation resumption, independent failed-image retry, and preservation of unaffected assets after a scene edit. Before invitations, verify that one tester cannot access another tester's projects or files and that predefined allowances are enforced.

This is a target to validate, not evidence of existing capability. Export 1080p MP4 at 30 fps. Require playability, complete narration, decodable images, correct scene order, no unintended blank gaps, and readable enabled captions. Failed checks mean incomplete production, not successful final export; delivered valid assets still count against allowance. Rendering and render retries do not consume tester generation allowance in alpha; actual rendering costs count against the shared budget, and queue/spending protection still applies. The quality rubric below is settled. Completion-time guarantees are deferred until measurement. Non-English quality is not measured by this acceptance set.

## Quality rubric refinement

### Owner-accepted narration fidelity amendment — 2026-10-05

This amendment supersedes strict exact-word matching below. Use severity-based fidelity review rather than raw ASR edit distance. Accept ASR formatting/recognition differences when evidence establishes the audio matches. Retain minor meaning-preserving spoken variations (such as `out of mug` spoken as `out of a mug`) as reviewable findings; permit explicit creator acceptance without paid regeneration. Unresolved variations remain pending review, not application crashes or automatic acceptance.

Changed facts, numbers, names or negation; missing/repeated passages; material unexpected speech/context leakage; and unintelligible speech block publishable selection of affected narration. Preserve history, current valid selections and unaffected successful artifacts; expose repair/review without automatic paid regeneration. ASR uncertainty alone does not prove a spoken error. Similarity percentages cannot waive material errors.

Keep approved script text, recognized transcript and accepted spoken variations separate. Acceptance pins source audio/version, approved text/version, actual difference, reviewer/approval and evidence. It does not rewrite approved text or request provenance. Captions and alignment must account for accepted actual speech. Acceptance does not waive complete accounted narration, independently valid scene boundaries or rejection of ambiguous mappings.

Fail videos with serious factual errors, unreadable enabled captions, broken pacing, narration/audio mismatch, insufficient narration quality, or narration/visual mismatch. Spoken words must match approved narration without missing/repeated passages. Speech must be intelligible, with appropriate pronunciation and no conspicuous glitches or unnatural pauses. Minor aesthetic preferences and subjective delivery are acceptable if total active correction stays within 15 minutes. Record defects and correction time for every test. Non-blocking factual warnings do not waive factual acceptance.

## Emphasis Text — follow-up alpha milestone

Editable animated text overlays highlight important/appealing narration words or short phrases over scene images. Text remains separate from generated images. Captions and Emphasis Text have independent toggles and can coexist, with separate placement to avoid collisions.

Automatically select a few highlights per scene and synchronize them with spoken narration. Creators can edit selections, remove items and adjust timing. Font, animation and selection changes invalidate rendering without regenerating images/narration.

Provide a small curated font library covering English, Spanish, French, Bangla and Hindi, and Pop, Fade, Slide animation presets. Use one project-wide font and animation preset; default off. Defer font uploads and custom animation design.

After narration changes, preserve previous highlights and mark affected selections/timings outdated. Propose updates while preserving matching manual choices. Review unresolved items before exporting with Emphasis Text enabled; turning it off permits export without resolving them.

Use readable automatic placement within frame-safe margins, separate from captions. Allow project-wide size, color and position settings. Offer fonts compatible with the selected language; flag incompatible existing selections and propose supported replacements. Never silently omit characters.

Include paid highlight selection in displayed estimates and spending ceilings. Run selection only when enabled or explicitly requested. Manual edits/font/animation changes consume no generation allowance. Actual rendering costs still count against the shared monthly budget.

This is a follow-up Alpha milestone after the core workflow works, not a requirement for the first end-to-end Alpha release. Its order relative to the vertical milestone is not committed.

## Public MVP boundary

The validated alpha is the foundation. Public readiness depends on creator evidence, operating costs and support needs. Recurring characters, broader uploads, custom styles and extensive model controls are candidates, not mandatory launch scope. Pricing/payments are deferred until actual cost evidence exists.

## Deferred operational and commercial specification

Before invitations: measure costs/asset sizes and set allowance/storage limits; substantiate provider cost bounds; choose providers/deployment; specify file-upload limits, technical per-asset checks and operational acceptance procedures. The US$40/month ceiling is a constraint, not a demonstrated feasibility result.

Providers, deployment, exact storage and generation allowances, actual generation costs, public pricing and subscription structure remain deferred until sufficient implementation or Alpha data exists. After Alpha evidence, decide public readiness, support expectations and optional additions. Later roadmap capabilities require separate discovery. No implementation stack or provider choice has been made.

## Review status

The user confirmed shared understanding on 2026-10-03 and designated this documentation the confirmed Alpha product definition. The product interview is closed. This confirmation does not authorize application implementation.
