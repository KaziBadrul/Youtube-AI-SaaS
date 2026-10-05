# Product and architecture documentation

S9 revision 9, 2026-10-05: **NOT_YET_PASS**. [Local Linux resource envelopes](architecture/evidence/operating-economics/S9/CREDITS-v9.md): one-CPU/2-GB serialized application phases pass at 1.972 GB peak; backup/render overlap causes OOM. Two-CPU/4-GB phases including overlap pass at 2.253 GB peak. Documented exact-frame mux repair preserves source audio; full scene/audio validator and five-language reference pixels pass. Emulated container tests exclude full VM OS overhead; no host selection, production, provider generation or token preflight. $30/credits/allowances unchanged.

S9 revision 8, 2026-10-05: **NOT_YET_PASS**. [Infrastructure/storage/backup envelope](architecture/evidence/operating-economics/S9/CREDITS-v8.md) records official candidate prices and unchanged-media measurements. $12–$24 persistent hosts are topology-compatible candidates, not resource-qualified selections; cheaper Hetzner candidate currently unavailable. Complete owner-cash fixed cost/reserve and full video economics remain UNKNOWN. $30 ceiling/credits/allowances unchanged; no token-preflight experiment, provisioning, production or provider generation.

S9 revision 7, 2026-10-05: **NOT_YET_PASS**. [Candidate text/research manifest](architecture/evidence/operating-economics/S9/CREDITS-v7.md) specifies four text operations plus <=6 Basic queries for an eligible five-minute factual topic. Conditional maximum $0.410964 before fees; expected cost and live usable maximum UNKNOWN pending validated model-specific input-token preflight. No provider calls or production changes; Research entitlement and v5/v6 product decisions remain unchanged.

Owner product decisions, 2026-10-05: [Research and topic discovery amendment](ALPHA_PRODUCT_SPEC.md#owner-decision--research-entitlement-and-topic-discovery-2026-10-05)
records the authoritative entitlement matrix: Research, Topic Suggestions and
Custom Topic Suggestions for 3 videos/week + 1 video/day only; Expert Topic
Suggestions for 1 video/day only. Custom uses `gemini-3.8-flash`. Suggestion
features are accepted product decisions with first-Alpha release scope unresolved.
[Roadmap](FEATURE_ROADMAP.md), [design](DESIGN.md), [flows](UX_FLOWS.md) and
[architecture](ARCHITECTURE.md) document their distinct boundaries. [S9 clarification](architecture/evidence/operating-economics/S9/OWNER-ENTITLEMENTS.md)
qualifies Research cost by entitlement without changing historical evidence or
executing revision 7. S9 remains NOT_YET_PASS; no prices/credits or implementation.

S9 revision 6, 2026-10-05: **NOT_YET_PASS**. [Current economics evidence](architecture/evidence/operating-economics/S9/CREDITS-v6.md) records required paid paths, exact existing B narration receipts, qualified 3/5/10-minute partial proxies and conditional retry exposure. Complete expected/maximum costs remain UNKNOWN; v5 product/credit decisions stay unchanged. No provider generation, production implementation, allowances or final credit formula.

Owner S9 revision 5, 2026-10-05: Alpha creator estimates show **both credits and
estimated USD**; internal financial authority remains separate. Preliminary
topic images ~12/minute; known-script predicted images = deterministic sentence
count. Retain consumed script/research work when revising remaining estimates.
Post-script credit/debit rules and complete economics remain open. **S9:
NOT_YET_PASS**; [current v5 evidence](architecture/evidence/operating-economics/S9/CREDITS-v5.md)
supersedes credits-only/universal-density assumptions, preserving v1–v4 history.

S9 started, 2026-10-05: **NOT_YET_PASS**. [Local economics baseline](architecture/evidence/operating-economics/S9/README.md) records the owner-selected `gemini-3.1-flash-lite-image`, verified public tariffs, existing S5/S6 measurements, image-only projections and remaining full-budget evidence. Supersedes S9-unexecuted notes below for local/public-source analysis only; paid experiments require separate bounded authorization. No production implementation or purchases.

S6 execution update, 2026-10-05: **PASS at local rendering/caption feasibility scope**. [S6 report](architecture/evidence/rendering-feasibility/S6/README.md) records 3/5/10-minute validated exports, five-language shaping, controls, cancellation/recovery, failures and resources. This supersedes historical S6-unexecuted notes below. S9 remains unexecuted; no production implementation, host/vendor selection or purchases.

Current S5 status, 2026-10-05: **PASS at the owner-defined existing B + B narration/mapping evidence scope**. [Final closure and limitations](architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/README.md). This supersedes older NOT_YET_PASS status notes below, not historical broader-protocol limitations. S6/S9 remain unexecuted; no architecture freeze or implementation authorized.

- [Alpha product specification](ALPHA_PRODUCT_SPEC.md): consolidated current product decisions; start here.
- [Validation plan](VALIDATION_PLAN.md): evidence required before creator invitations.
- [Decision history](PRODUCT_DECISIONS.md): interview answers, superseded choices and deferred work.
- [Provisional feature roadmap](FEATURE_ROADMAP.md): original candidate releases and interviewed boundaries.
- [Glossary](../GLOSSARY.md): canonical product terms.
- [Editable Emphasis Text decision](adr/0001-editable-emphasis-text.md): why text remains separate from images.
- [Existing pipeline investigation](PIPELINE_INVESTIGATION.md): read-only source evidence for architecture discovery; not an accepted architecture.
- [Architecture discovery history](ARCHITECTURE_DISCOVERY.md): interview decisions and alternatives; the consolidated architecture documents below are the accepted baseline.

## Accepted architecture baseline

- [Alpha architecture](ARCHITECTURE.md): runtime boundaries, state/storage, authentication, rendering, providers, observability and deployment conditions. Start here for architecture.
- [Artifact and dependency model](ARTIFACT_MODEL.md): domain relationships, version selection, deterministic invalidation and restoration.
- [Job execution and failures](JOB_EXECUTION_MODEL.md): queue, state machines, exclusion, retries, cancellation and crash recovery.
- [Cost and reservation model](COST_MODEL.md): authority, accounting, shared budget, allowances and reconciliation.
- [Architecture feasibility gates](ARCHITECTURE_SPIKES.md): accepted experiments and required evidence; local/free S1/S2/S3/S7/S8 executed, with limits; S4-R conditionally passed; S5 was evaluated and remains NOT_YET_PASS; S6/S9 remain unexecuted.
- [Python/Django and controlled-worker ADR](adr/0002-python-web-and-controlled-worker.md): accepted conditional runtime direction.
- [Single-host SQLite ADR](adr/0003-single-host-sqlite-alpha.md): accepted database direction conditional on concurrency/recovery evidence.

## Alpha design discovery

- [Visual and interaction design](DESIGN.md): accepted design direction, reference interpretation, themes, workspace, mobile and accessibility requirements.
- [Creator UX flows](UX_FLOWS.md): simple/manual creation, demo, authorization, corrections, restoration, rendering and recovery.

Status: DESIGN.md and UX_FLOWS.md confirmed as the accepted Alpha design and UX baseline on 2026-10-04. Static HTML/CSS exploration is separately authorized. Application implementation, architecture spikes, paid provider calls, deployment purchases and task graphs remain unauthorized.

- [Static design exploration](../design-exploration/alpha/README.md): local linked visual studies; proposed tokens and interactions are not production implementation.

Status: confirmed Alpha product definition as of 2026-10-03; product interview closed. Only documentation has been produced. Application implementation is not authorized. No product capability, measured operating cost or existing pipeline reliability has been demonstrated by this interview.

Architecture was confirmed on 2026-10-03 as the accepted Private Alpha design baseline, subject to all evidence gates. Conditional runtime, database, deployment, narration, media, cost and backup decisions remain unproven. Failed gates require reconsideration or an explicit scope/budget decision. Providers, hosting vendor, exact allowances/storage limits, actual costs and public economics remain deferred. No application implementation, paid experiments, deployment purchases, spike execution or implementation task graph is authorized.

## Accepted targeted narration amendment

The owner accepted [severity-based narration fidelity](ALPHA_PRODUCT_SPEC.md#owner-accepted-narration-fidelity-amendment--2026-10-05) on 2026-10-05: explicitly accepted minor meaning-preserving variations may pass; material errors and ambiguous mappings remain blocking. This changes the fidelity requirement deliberately, without passing S5 or authorizing implementation/provider calls.

Current S5 owner policy: **B coherent initial generation + B whole affected-segment correction**, superseding the earlier B + C1 preference because the owner disliked stitching. [Current evidence/remaining blocker](architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-only-review-v1/README.md). S5 remains NOT_YET_PASS; no new provider call or implementation is authorized.

The user confirmed the targeted narration amendment on 2026-10-03. It amends narration granularity only; all other accepted policies and evidence gates remain in force. [Artifact model](ARTIFACT_MODEL.md#narration-generation-granularity--accepted-amendment) is authoritative for the accepted separation of scene words, generation segments, source audio, mappings and derived assembly. [Pipeline investigation](PIPELINE_INVESTIGATION.md#targeted-current-tts-batching-reassessment--2026-10-03) records the freshly inspected batching behavior. [S5](ARCHITECTURE_SPIKES.md#s5-measurement-and-selection-protocol--accepted-amendment) compares per-scene, coherent segments and evidence-gated surgical correction. Job/cost models reflect only the resulting scope/provenance clarifications. Segment sizing and surgical correction remain conditional and unproven. Product scope and runtime/database ADRs remain unchanged; no implementation, paid provider experiments, deployment purchases, spike execution or implementation task graph is authorized.

## Local architecture feasibility evidence — 2026-10-04

The user separately authorized S1, S2, S3, S7 and S8 using local/free resources only. [Evidence reports](architecture/evidence/local-feasibility/README.md) record PASS at the stated fixture scope, reproducible commands, retained initial failures and remaining limits. [Isolated spike scaffolding](../spikes/local-feasibility/README.md) is disposable and not a production application foundation.

This execution update supersedes earlier pre-execution status statements above and in discovery-era document/ADR status notes. Accepted product, design, architecture, spending, narration and recovery requirements are unchanged. Runtime/media/provider/off-host/cost feasibility remains conditional; S5 generation/evaluation completed but remains NOT_YET_PASS because technical scene/audio mapping evidence is unresolved; S6/S9 have not been executed. No production implementation, infrastructure purchase, deployment or implementation TASKS.md is authorized by this phase.

## S4 provider feasibility evidence — 2026-10-04

S4 was separately authorized for documentation/source/local fake-transport investigation only. [Report and evidence](architecture/evidence/provider-feasibility/S4.md): **FAIL**, required research candidate lacks an established finite search-fee bound. Other candidates have explicit conditions, retry isolation and partial reconciliation limitations. No provider selected or substituted. This supersedes prior S4-unexecuted status notes only; S5 was later separately evaluated and remains NOT_YET_PASS, while S6/S9 remain unexecuted. No additional provider call, production implementation, purchase, deployment or TASKS.md occurred during this update.

## S4-R bounded research remediation — 2026-10-04

Original S4 remains **FAIL** in its historical evidence. Separately authorized S4-R documentation/local-fixture investigation: **PASS** for application-bounded Tavily Basic Search REST plus tool-free bounded Gemini planning/reasoning. **Overall S4 after remediation: PASS at conditional architecture evidence scope**; see [report and limitations](architecture/evidence/research-feasibility/S4-R.md). This supersedes the earlier overall-S4-open status, not original results or accepted requirements. Final query tuning, terms/account activation, real factual quality and operating economics remain validation work; no provider was activated. S5 was subsequently evaluated with eight authorized TTS submissions and remains NOT_YET_PASS pending technical mapping evidence. S6/S9, implementation, purchase, deployment and TASKS.md remain unauthorized and unexecuted.
