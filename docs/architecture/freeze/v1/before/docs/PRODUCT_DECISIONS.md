# Product decisions

## Accepted owner budget amendment — 2026-10-05

The active total prelaunch / Private Alpha operating ceiling is **US$40/month**, explicitly increased by the owner from US$30. This supersedes prior $30 wording wherever it described current financial authority. Historical interview/discovery notes and S9 V1–V11 evidence retain the $30 ceiling applicable when recorded; they do not control the current limit.

The $40 is a total owner cash-spend ceiling, not a generation-only allocation, creator credit balance or per-project authorization. Fixed obligations, actual spending, financial reservations and unresolved liabilities remain accounted for; safety/tax/payment/FX reserves and creator allowances remain unresolved. No automatic increase in credits/allowances, provider purchase/call or production implementation follows. See [current S9 reassessment](architecture/evidence/operating-economics/S9/CREDITS-v12.md). The owner’s rule ending host-sizing experiments unless failure remains in force.

## Accepted owner amendment — 2026-10-05, Research and topic discovery

The [current specification amendment](ALPHA_PRODUCT_SPEC.md#owner-decision--research-entitlement-and-topic-discovery-2026-10-05)
is authoritative. Research, stored/random Topic Suggestions and category-driven
Custom Topic Suggestions are available only to 3 videos/week and 1 video/day;
channel/niche-informed Expert Topic Suggestions only to 1 video/day. Custom uses
`gemini-3.8-flash`; Expert model/retrieval are unresolved. All entitlements are
server-side persisted authority, separate from financial authorization.

This supersedes universal topic-Research availability, not its quality or bounded
retrieval requirements, and does not change separate pasted-script checking.
Suggestions are distinct optional discovery features, with Alpha shipping
unresolved; no acceptance-gate expansion or public billing commitment. Their
costs are separate from normal per-video production. Prices, exact credits,
suggestion quotas/counts, collection design, Expert data source/retention,
history/saving, upgrade UX and private-Alpha entitlement assignment remain open.
Historical interview and S9 evidence below remain historical; no revision 7,
production implementation, provider/API call or spending authorized.

Status: closed product interview; accepted Alpha decisions are consolidated in the confirmed [Alpha product specification](ALPHA_PRODUCT_SPEC.md). Historical unresolved statements are superseded by later decisions.
Decisions below were accepted by the user on 2026-10-03. The supplied product brief remains the source for proposed capabilities; release boundaries are provisional.

## Accepted decisions — Round 1

1. **Initial customer and job.** Serve solo faceless educational YouTube creators using narrated images. Round 2 expands the initial 3–8-minute scope to 3–10 minutes and introduces optional one-minute vertical output; platform integrations and repurposing remain deferred.
2. **Quality target.** Aim for at least eight of ten representative generated videos to become publishable with no more than 15 minutes of scene-level corrections each. Missing narration, broken timing, unreadable captions, and serious factual errors fail acceptance. These are hypotheses to validate, not demonstrated results. Evaluation inputs, reviewers, timing measurements, and defect thresholds remain to be defined.
3. **Release strategy.** Establish a narrow private-alpha milestone. Measure actual generation costs and correction effort before committing to public-launch scope or pricing. Round 2 settles staffing and the monthly prelaunch budget; a maximum cost per video remains open.
4. **Spending authority.** Create Video authorizes bounded production directly. Display/review of estimated cost and the spending ceiling is optional; no separate confirmation screen is required. Pause for approval if completion or retries would exceed it. Advanced Mode may expose the detailed plan without requiring a separate plan-review step for every Simple Mode generation.

## Accepted decisions — Round 2

5. **Production envelope.** Accept a topic or pasted script. Support 3–10-minute 16:9 videos, with optional one-minute TikTok-aspect-ratio output. Use generated still images, built-in narration, optional basic motion, captions that can be toggled on/off, and optional library music. Defer uploaded video clips, custom audio, recurring-character management, and platform variants. Whether vertical output is an alpha gate or a later option is unresolved. Language was not specified in the user's answer.
6. **Alpha correction tools.** Allow editing scene narration and visual prompts, individual image/narration regeneration, image replacement, caption correction, timing adjustment, scene reordering/deletion, and rerendering. Preserve previous image/narration versions. Defer the Director, timeline, reusable style studio, and extensive model controls. These correction capabilities move from candidate V1 into alpha.
7. **Non-blocking factual warnings.** Apply the same warning policy to disputed general facts and unsupported sensitive-topic claims. Show warnings only to the creator, never in the rendered video. The creator may review them, but generation proceeds automatically without requiring review. The proposed sensitive-topic exclusion and factual approval gate were not accepted. Whether and how pasted scripts are checked remains open. Warnings do not make serious factual errors acceptable under the quality target.
8. **Alpha allowance accounting.** Provide free, capped alpha allowances with visible estimated usage and actual cost tracking. Count successfully delivered assets against allowances, release reservations for failed operations, and retain charges for successful assets when another part fails. Automatic retries stay within the approved ceiling. The exact meaning of a successfully delivered asset remains open.
9. **Delivery constraints.** One solo engineer; no fixed public-launch date; prioritize reliability and quality. Prelaunch spending must not exceed US$30/month, ideally US$0. Which expenses count toward this cap, alpha cohort size, and behavior at budget exhaustion remain open.

## Accepted decisions — Round 3

10. **Total prelaunch budget.** The US$30/month cap includes AI generation, hosting, storage, research, and all alpha tester usage. The owner may invest more if there are enough users. No automatic budget increase, user-count threshold, or exhaustion behavior has been agreed.
11. **Vertical output sequencing.** One-minute 9:16 output is a follow-up alpha milestone after landscape generation meets the quality target. It is a standalone project format; deriving short-form variants from longer videos remains deferred.
12. **Multilingual scope.** Support many languages, with English as the default. This replaces the proposed English-only alpha. Supported languages, minimum launch coverage, and language-specific acceptance criteria remain open.
13. **Script checking and consent.** Factual checking applies only to pasted scripts. The app may change a pasted script only after asking the user and receiving approval. Findings remain non-blocking under Round 2. Whether separate pre-writing research also remains part of topic generation is unresolved; no exemption from the factual quality target was agreed.
14. **Alpha access.** The owner first tests extensively on real video projects. Once end-to-end production is stable, invite approximately 3–5 target creators, preferably faceless YouTubers, Shorts/TikTok creators, or creators already experimenting with AI video. Each has a private account/access identity, isolated projects and generated assets, no access to another tester's projects/files, and a predefined generation allowance. Owner-only validation precedes invited testing; isolation and allowance controls are prerequisites to invitations.
15. **Chargeable success.** Technically valid, delivered assets consume allowance even if subjectively unsatisfactory. Elective regeneration consumes additional allowance. Corrupt, missing, or technically invalid outputs are failures. Technical validity checks and charging units remain to be defined.

## Accepted decisions — Round 4

16. **Topic research.** Research factual topics before writing a script. A separate factual-checking pass applies only to pasted scripts. Both are automatic and non-blocking; sources and warnings are private to the creator.
17. **Language support contract.** Offer an explicit supported-language list, defaulting to English. The selected language applies to script, narration, and captions. Validate English and two priority languages before inviting testers; label other available languages experimental. The two priority languages were not named and remain unresolved.
18. **Budget authorization.** Pause new paid operations at the monthly ceiling. Only the owner can explicitly raise it; user count never automatically authorizes additional spending.
19. **Invitation gate.** Evaluate ten real landscape projects spanning topic and pasted-script inputs and the 3–10-minute range. At least eight must meet the publishability target with no more than 15 minutes of corrections each. Demonstrate interrupted-generation resumption, independent failed-image retry, and preservation of unaffected assets after a scene edit. Evaluate captions when enabled; intentionally disabled captions are not a defect. Language-specific testing coverage and concrete technical acceptance checks remain open.
20. **Narration edit consequences.** Save edits immediately. Mark the affected scene's narration audio, timing, captions, and final render outdated. Show cost before regeneration. Preserve the scene image unless its visual description changes. Never silently export outdated narration. Broader dependency and edit-during-generation behavior remain open.
21. **Factual correction consent.** Show proposed wording changes and allow individual or all-change acceptance. Approval changes the script only; paid regeneration requires authorization within a displayed ceiling. Ignoring suggestions preserves original wording and generation continues.

## Accepted decisions — Round 5

22. **Required languages.** Validate English, Spanish, French, Bangla, and Hindi for alpha, replacing the English-plus-two proposal. English remains default. Per-language coverage remains open.
23. **Creative defaults.** Simple Mode requires input and an output-language setting defaulted to English. Style, voice, duration, captions, motion, and music controls are optional. Start with three curated visual presets and maintain one coherent style per project. Defer custom styles and guaranteed recurring-character identity. Preset identities and initial settings remain open.
24. **Script fidelity.** Preserve pasted scripts. Above ten minutes, show estimated duration and require creator shortening or approval of a proposed adaptation. Translation requires approval when pasted language differs from output language. Topic scripts may be written to selected duration and language automatically. Below-three-minute landscape handling remains open.
25. **Partial failures.** Preserve successful work and identify failed scenes. Allow retry or image replacement; do not silently export missing visuals or substitute placeholders. The creator may explicitly delete failed scenes and render the remaining video.
26. **Concurrent editing.** Allow edits during generation. Operations use their starting input version. If that input changes, retain the arriving result as a previous version rather than making it current, and show consumed allowance. Paid regeneration requires authorization.
27. **Unavailable research/checking.** Continue with a private research-unavailable or checking-incomplete notice. Keep collected sources, offer retry, and never imply checking succeeded.

## Accepted decisions — Round 6

28. **Initial creative settings.** Presets: Minimal Illustration, Storybook, Documentary Illustration. Default: Minimal Illustration, five-minute target for topic input, captions on, gentle motion on, music off. Pasted scripts retain natural duration. Offer a small set of previewable voices per supported language.
29. **Asset restoration.** Restore compatible timing/captions alongside an earlier narration when available; otherwise mark them outdated. Never combine restored narration with incompatible timing. Existing-asset restoration consumes no generation allowance; required regeneration has separately displayed cost.
30. **Final render edit lock.** While final rendering is ongoing, editing is grayed out and prohibited. This replaces the proposed editing-during-render behavior. Concurrent editing during asset generation remains permitted under Round 5. Cancellation, retry, and retention of previous successful exports were not explicitly accepted in this answer and remain open.
31. **Short scripts.** The 3–10-minute range describes the primary job, with ten minutes the alpha maximum. Allow shorter landscape scripts unchanged, show estimated duration, and never pad narration without approval.
32. **Project lifecycle and storage.** Include create, rename, autosave, reopen, and delete; defer duplication and archiving. Preserve assets during active alpha testing, show storage usage, and require an owner-set storage cap before invitations. At the cap, pause new asset creation rather than silently deleting previous versions. Confirm project deletion explicitly. Exact cap, deletion timing and post-alpha retention remain open.
33. **English-only acceptance set.** The ten-project quality acceptance test covers English only. This replaces the proposed two-projects-per-language test. English remains default; Spanish, French, Bangla, and Hindi remain requested languages, but the invitation gate does not establish their quality. Whether they are labeled experimental and receive basic smoke checks remains open. Round 5's all-five-language validation prerequisite is superseded by this English-only test decision.

## Accepted decisions — Round 7

34. **Experimental languages.** Label Spanish, French, Bangla, and Hindi experimental during alpha. Before enabling each, check narration generation, correct caption display, and successful export. The publishability claim applies only to validated English output.
35. **Render recovery.** Include cancel/retry and preserve the last successful export. Release the edit lock on completion, failure, or confirmed cancellation. Recover interrupted renders without permanently locked projects. Rendering retry reuses generated assets.
36. **Technical export standard.** Export 1080p MP4 at 30 fps. Require a playable file, complete narration, decodable scene images, correct scene order, no unintended blank gaps and readable enabled captions. Failed checks mean incomplete production rather than successful final export. Already delivered valid assets retain their separate usage charges; no render charge was established by this decision.
37. **Presentation dependencies.** Caption styling/toggle, motion, music, and scene order affect rendering without regenerating images/narration. Image replacement affects rendering only. Caption text edits preserve narration. Manual timing must not silently cut off speech; flag conflicts for correction.
38. **Allowance units and retries.** Show estimated/consumed US-dollar-equivalent alpha allowance; do not sell credits yet. Permit at most two automatic retries per failed operation, within approved spending ceilings, then offer manual retry. Separately record actual provider spending, including chargeable failed attempts.
39. **Deletion/retention.** Hide confirmed deleted projects immediately, retain them for seven days for restoration, then permanently delete them. Explain the window during confirmation. Retained deleted assets count against storage. Keep active alpha projects until an announced end date, then allow 14 days for download before deletion.

## Accepted decisions — Round 8

40. **Reservations and admission.** Reserve tester allowance and shared operating budget before admitting work. Admit requests in order and queue requests that cannot fit. Shared-budget reservations include paid failures and permitted retries even though failed assets do not consume tester allowance. Do not start an operation whose expected maximum cost exceeds authorized limits. If a provider cannot supply a bounded cost, the product must not imply the ceiling is guaranteed; provider feasibility remains unverified.
41. **Alpha availability.** Owner-only testing can run locally. Invited testing uses private web access during announced availability windows, one active production job at a time, with queue status. Do not promise completion times before measurement.
42. **Measured limits.** Do not pick fixed allowance or storage amounts before measuring real production costs and asset sizes. Concrete invitation limits remain prerequisites, not guessed values. The user did not explicitly settle reserve size or allocation formula.
43. **Quality rubric refinement.** The user names unreadable enabled captions, broken pacing, narration not matching audio, narration not good enough, and narration not matching visuals as failures. Minor aesthetic preferences are acceptable within 15 minutes of active correction. Record defects and correction time for every test. Exact narration quality definitions and whether omission of serious factual errors supersedes the earlier criterion remain open.
44. **Structural consistency.** Keep current script consistent with scene narration and order; preserve original input separately. Reorder/delete updates the current script and invalidates final render, retaining surviving images and narration. Defer scene addition/duplication to public MVP.
45. **Public scope.** Use validated alpha as the public MVP foundation. Decide public readiness from creator evidence, operating costs and support needs. Recurring characters, broader uploads, custom styles and extensive model controls are candidates, not launch obligations. Pricing/payments require later decisions after cost measurement.

## Accepted decisions — Round 9

46. **Factual acceptance.** Serious factual errors remain a publishability failure despite non-blocking generation warnings.
47. **Narration rubric.** Spoken words must match approved narration without missing/repeated passages. Speech must be intelligible, with appropriate pronunciation and no conspicuous glitches or unnatural pauses. Subjective delivery is judged within the 15-minute active-correction budget.
48. **Visual review after narration edits.** Preserve images when narration changes and flag the scene for visual review. Offer prompt editing or regeneration with cost displayed. Do not automatically spend image allowance; let the creator explicitly keep or replace the image.
49. **Render-lock scope.** Disable all project-content changes while rendering, including deletion, restoration and accepting script corrections. Keep viewing, downloading existing exports and cancellation available. Unlock after completion, failure or confirmed cancellation.
50. **Rendering allowance.** Do not deduct tester generation allowance for rendering/retries during alpha. Count actual rendering operating costs against the shared monthly budget, and apply queue/spending protection.

## New requirement — animated narration emphasis

The user requests optional animated text appearing over/with scene images, using important or appealing narration words and a user-selected font. The feature can be toggled on/off. Caption independence, editable text versus image-embedded text, animation scope, selection/timing controls, initial defaults and release priority require interview decisions. Do not treat these as settled implementation details.

## Accepted decisions — Round 10

51. **Emphasis Text representation.** Use editable text overlays over scene images rather than permanently embedding words in generated images. Canonical name: Emphasis Text. Font, animation and text corrections do not require image regeneration.
52. **Independent captions.** Captions and Emphasis Text have separate toggles and can be enabled simultaneously. Captions present narration text; Emphasis Text highlights selected words/short phrases. Keep their placement separate to avoid collisions.
53. **Selection and editing.** Automatically select a few important/appealing words or short phrases per scene, synchronized with spoken narration. Allow selection editing, item removal and timing adjustment. Font, animation and selection changes invalidate rendering without regenerating images/narration.
54. **Emphasis milestone.** Add Emphasis Text after the core workflow works, as a follow-up alpha milestone rather than a first owner-test prerequisite. Provide a small curated font library covering the five languages and Pop, Fade, Slide animation presets. Use one project-wide font and animation preset; default off. Defer uploaded fonts/custom animation design.

## Accepted decisions — Round 11

55. **Emphasis reconciliation.** After narration changes, preserve previous highlights, mark affected selections/timings outdated and propose updates. Preserve manual choices that still match. Require review of unresolved items before export with Emphasis Text enabled; disabling it permits export without resolving those items.
56. **Emphasis layout/fonts.** Use readable automatic placement within frame-safe margins, separate from captions. Allow project-wide size, color and position settings. Offer fonts compatible with selected language; flag incompatible existing selections and propose a supported replacement. Never silently omit characters.
57. **Emphasis cost.** Include paid selection operations in estimates and approved ceilings. Run selection only when enabled or explicitly requested. Manual edits, font changes and animation changes consume no generation allowance. Actual rendering costs still count against the shared operating budget.

## Current design tree

- Audience, input/output range, creative defaults and language expectations — settled.
- Owner validation, invited alpha isolation/access and English quality gate — settled; operational evidence not yet collected.
- Scene corrections, dependencies, concurrent generation edits, render locks/recovery and asset restoration — settled at product level.
- Budget authority, allowance accounting, retries and admission queue — settled; cost estimates/provider bounds require feasibility evidence.
- Project lifecycle, storage protection and retention — settled; numerical limits require measurement.
- Emphasis Text representation, caption independence, selection/editing, reconciliation, layout/fonts, cost and follow-up-alpha placement — settled.
- Public MVP is based on validated alpha; additional candidates remain optional, not inherited V1 commitments.

## Explicitly deferred work

- **Before inviting testers:** measure operating costs and asset sizes; choose concrete allowance/storage limits; substantiate bounded provider spending; choose providers/deployment; specify file-upload limits/technical per-asset validation details and operational acceptance procedures. These were not decided in this product interview.
- **Follow-up alpha milestones:** standalone one-minute vertical output and Emphasis Text. Their relative order and exact delivery dates are not committed; neither blocks initial core owner testing.
- **After alpha evidence:** public readiness, pricing/payments, support expectations and optional feature additions.
- **Later roadmap:** Director, reusable identity/templates/styles, richer media, AI video, timeline, publishing, repurposing, batch, collaboration and ecosystem capabilities require their own interviews.

## Final confirmation — 2026-10-03

The user confirmed the current documentation as the Alpha product definition and closed the product interview. The US$30/month total prelaunch ceiling is a strict Alpha constraint unless the owner explicitly approves an increase; architecture must not assume that it remains permanent after validation.

Providers, exact storage/generation allowances, deployment, actual generation costs, public pricing and subscription structure remain deferred until sufficient implementation or Alpha data is available. Vertical video and animated Emphasis Text remain follow-up Alpha milestones, not requirements for the first end-to-end Alpha release.

This confirmation does not authorize application implementation. No application code was written.

User clarification: creator review or display of estimated cost and maximum spend is optional, not a prerequisite for paid authorization. Create Video itself authorizes bounded production and starts generation directly, with no intervening estimate, confirmation or review screen. Financial details may remain in optional Details. Server-side cost bounds, allowance/budget reservations, retry limits and reconciliation remain mandatory. Required script-preservation/translation/adaptation approvals and material scope changes remain distinct from routine cost review.
