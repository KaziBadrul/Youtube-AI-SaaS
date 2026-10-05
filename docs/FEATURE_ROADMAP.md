# Provisional feature roadmap

## Accepted owner budget amendment — 2026-10-05

The active total prelaunch / Private Alpha operating ceiling is **US$40/month**, explicitly increased by the owner from US$30. This supersedes prior $30 wording wherever it described current financial authority. Historical interview/discovery notes and S9 V1–V11 evidence retain the $30 ceiling applicable when recorded; they do not control the current limit.

The $40 is a total owner cash-spend ceiling, not a generation-only allocation, creator credit balance or per-project authorization. Fixed obligations, actual spending, financial reservations and unresolved liabilities remain accounted for; safety/tax/payment/FX reserves and creator allowances remain unresolved. No automatic increase in credits/allowances, provider purchase/call or production implementation follows. See [current S9 closure](architecture/evidence/operating-economics/S9/CREDITS-v14.md). The owner’s rule ending host-sizing experiments unless failure remains in force.

## Accepted topic-discovery product decisions — 2026-10-05

The [Alpha specification's owner amendment](ALPHA_PRODUCT_SPEC.md#owner-decision--research-entitlement-and-topic-discovery-2026-10-05)
is authoritative for feature behavior and the entitlement matrix. These are
accepted product decisions; **shipping in the first Private Alpha is unresolved**.
They are not assigned to a numbered release or an implementation task list.

- Level 1 **Topic Suggestions**: large curated stored collection, random
  discovery, Surprise me / another suggestion / use as New Video topic;
  no LLM per click required. Eligible: 3 videos/week and 1 video/day only.
- Level 2 **Custom Topic Suggestions**: category/interest-driven YouTube ideas,
  owner-selected **`gemini-3.8-flash`**. Eligible: 3 videos/week and 1 video/day
  only. No silent model substitution; feasibility and bounded usage required.
- Level 3 **Expert Topic Suggestions**: supplied channel/name/link or described
  niche context; potentially bounded permitted retrieval plus AI generation.
  Eligible: 1 video/day only. Expert model/retrieval are not selected.

Existing **Research** is available only to 3 videos/week and 1 video/day users.
Prices, exact credits/quotas, lower-tier name, upgrade/paywall behavior, collection
size/curation, Expert data source/retention, history/saving and release timing
remain open. Optional discovery operations have their own bounded authority;
they are not automatically charged to every video's production plan.

This is a condensed record of the user-supplied AI Video Production SaaS brief. It is a candidate capability inventory, not an authoritative assignment of features to releases or an implementation checklist. The original supplied brief provides the detailed feature list. Accepted interview decisions are recorded in [PRODUCT_DECISIONS.md](PRODUCT_DECISIONS.md) and take precedence over conflicting roadmap assumptions.

## Confirmation status

The current documentation is the confirmed Alpha product definition as of 2026-10-03; the product interview is closed. The original candidate release table remains provisional. The strict US$40/month Alpha ceiling can only increase with explicit owner approval and must not be assumed permanent in architecture decisions. Live provider adapters/account activation, hosting/backup vendors, exact storage/generation allowances, actual costs, public pricing and subscription structure remain deferred until sufficient implementation or Alpha data exists. This confirmation does not authorize application implementation.

## Freeze scope relationship

Architecture Freeze v1 does not promote this roadmap into Alpha. Core product scope is ALPHA_PRODUCT_SPEC.md. Follow-up standalone vertical and Emphasis Text remain outside the invitation gate; suggestion shipping remains unassigned. Explicitly deferred: professional timeline, Director, reusable Style Studio/custom visual styles, extensive model controls, recurring-character identity, uploaded video/custom audio, arbitrary scene addition/duplication, project duplication/archive, public signup/external auth, YouTube publishing, derived short-form variants, commercial billing/credits/pricing, advanced templates/model marketplace, arbitrary font uploads/custom animation.

## Product promise

Idea or script → usable, fully narrated video with consistent visuals, captions, pacing, motion, and music. Creators can correct individual AI decisions without starting over.

Initial focus: solo faceless educational YouTube creators producing 3–10-minute narrated, image-based explainers in 16:9. One-minute 9:16 output follows landscape quality validation as a later alpha milestone. Platform integrations and derived platform variants remain deferred.

## Candidate releases from the supplied brief

| Version | Theme | Candidate capabilities |
| --- | --- | --- |
| 0.1 | Pipeline | Topic-to-script, scene planning, prompts, TTS, images, alignment, timing, subtitles, image motion, music, FFmpeg rendering, MP4 export; persistence, background jobs, status, retries, resume, assets, provider abstraction, logs; basic project and preview UI. |
| 0.5 | Private alpha | Accounts and project lifecycle, autosave and history; topic/script input and validation; research, sources, factual warnings and provenance; creative briefs; generation plans, models and cost estimates. |
| 1.0 | Public MVP | Simple/Advanced Modes on one project; scene editing and selective regeneration; artifact dependencies and invalidation; asset versions and restore; styles, characters, voices, captions, music, motion, uploads; rendering lifecycle; credits, reservations, reconciliation, spending protection and usage limits. |
| 1.5 | Creator Pro | Structured AI Director with proposals, scoped changes and undo; asset/scene locks; multi-scene operations; reusable styles and production templates; model overrides; possible BYOK; richer asset management. |
| 2.0 | Advanced production | AI-generated video clips mixed with image scenes; project critique and improvement plans; optional timeline mode and basic multiple-track editing. |
| 2.5 | Publishing | YouTube connection, upload and scheduling; publishing metadata and thumbnail assistance; potential platform-specific variants. |
| 3.0 | Creator operating system | Reusable creator identity, repurposing, batch generation and credit budgeting; potential team collaboration and review. |
| 3.x+ | Ecosystem | Community styles and templates, marketplace; possible voice cloning with consent and abuse protections. These are long-term ideas, not commitments. |

## Interviewed release boundaries

### Core owner-tested alpha

Topic or pasted script → editable narrated still-image video; primary format 3–10-minute 16:9, with shorter pasted scripts permitted. Three curated styles, previewable voices, optional motion/music and toggleable captions. English is default and the quality-gate language; Spanish, French, Bangla and Hindi are experimental with basic narration/caption/export checks.

Bring essential scene correction, selective regeneration, previous-asset restoration, dependency invalidation, persistence, retry/resume and render recovery forward into alpha. Keep current script consistent with scene order/narration while preserving original input. Defer scene addition/duplication to public MVP.

Research factual topics before writing only for Research-entitled users (3 videos/week or 1 video/day); run the separate check only on pasted scripts under its unchanged policy. Sources/warnings remain private and non-blocking. Script rewriting/translation/adaptation needs approval. Generation warnings do not waive factual quality acceptance.

Offer credits/USD and ceiling details optionally; Create Video grants bounded authority directly; count valid delivered assets against free dollar-equivalent allowances. Failed assets do not consume allowance, but actual paid failures count against the owner's shared budget. Permit two automatic retries within ceilings. Rendering/retries consume operating budget but no tester generation allowance.

Allow concurrent editing during asset generation; late outputs based on changed inputs become previous versions. Disable all content changes during final rendering; keep viewing/download/cancel available. Export technically complete 1080p MP4 at 30 fps, preserve the last successful export, and support cancel/retry/lock recovery.

### Invited alpha prerequisites

Owner validates ten real English projects; at least eight become publishable with no more than 15 minutes of active correction each. Demonstrate resumption, selective retry and preservation of unaffected assets.

Invite approximately 3–5 creators only with private identities, isolated projects/assets and predefined allowances. Use announced availability windows, one active production job and queue status. Measure real costs/asset sizes before setting allowance/storage numbers. Include storage protection, seven-day recoverable deletion and a 14-day download window after an announced alpha end. Active content purges at seven days; backup copies purge within at most 24 additional hours, with no restoration of purged content.

One solo engineer, no fixed public-launch date, US$40/month total prelaunch operating ceiling ideally zero. The amount is owner-configurable; only explicit owner authorization revises it. S9 V14 passed conditional architecture planning feasibility; complete live provider bounds and cash coverage remain activation prerequisites.

### Follow-up alpha milestones

- Standalone one-minute 9:16 output after landscape quality validation; no derived platform variants yet.
- Emphasis Text after the core workflow works: editable narration-synchronized word/phrase overlays, independent of captions, default off. Curated compatible fonts, project-wide font/size/color/position controls, Pop/Fade/Slide presets, automatic selection with manual corrections. Reconcile narration changes before enabled export. Paid selection is estimated/authorized and runs only when enabled or requested. Defer font uploads/custom animations.

Neither follow-up is required for the first end-to-end Alpha release. Their relative order is not committed.

### Public MVP and later releases

Build public MVP on validated alpha, creator evidence, operating costs and support needs. Recurring characters, broader uploads, custom styles and extensive model controls remain candidates, not launch obligations. Decide pricing/payments after cost measurement. The candidate release table above preserves the original brief and does not override these boundaries. Later capabilities require separate specification.

## Explicitly outside the supplied V1 scope

Full professional timeline editing, AI video generation, voice cloning, marketplace, collaboration, batch production, direct YouTube/TikTok publishing, advanced analytics, a full creator operating system, and complex multi-track editing.

## Product principles to preserve during scope review

AI does the production work; automation retains creator control; regenerate only affected work; important outputs remain inspectable and replaceable; preserve previous versions where practical; make expensive actions transparent; tolerate partial failures and support resumption; the Director acts on structured projects; professional editors remain available for advanced work; interface design emphasizes intentional typography, hierarchy, spacing, density, feedback and purposeful motion.

## Evidence limitations

The brief describes an existing local Python pipeline, but the canonical six-script source resides in the external YoutubeAI/python-scripts directory, inspected in PIPELINE_INVESTIGATION.md. Its legacy orchestration is not production-ready; historical feasibility results have their own scoped claims. This document does not imply that any proposed feature exists.
