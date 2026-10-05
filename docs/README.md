# Private Alpha source of truth

Architecture Freeze v1, 2026-10-05. Start with [product scope](ALPHA_PRODUCT_SPEC.md), then the contract for the work being considered. [Freeze record](architecture/ARCHITECTURE_FREEZE.md) is a summary/index, not another full specification. S1–S8 PASS (S4 after remediation); **S9: PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY**, closed at [V14](architecture/evidence/operating-economics/S9/CREDITS-v14.md). No spike is reopened. Active total ceiling is **$40 USD per Asia/Dhaka calendar month**.

## Authority

[AGENTS.md](../AGENTS.md) owns conflict handling: explicit current owner instructions; accepted scoped ADRs interpreted with explicit later amendments; current product specification; architecture and its delegated domain/job/finance contracts plus UX/design within product scope; glossary/validation; dated decision rationale; provisional roadmap; adopted feasibility evidence; historical evidence/prototypes; existing code. Current contracts outrank historical status paragraphs and code. Unresolved material contradictions require SPEC_BLOCKED; fail-closed activation prerequisites are not automatically task-planning blockers.

| Canonical document | Owns |
| --- | --- |
| [ALPHA_PRODUCT_SPEC.md](ALPHA_PRODUCT_SPEC.md) | Included/deferred Alpha, creator behavior, language/quality, canonical entitlement matrix |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Runtime, persistence, providers, private media, supervision and deployment boundaries |
| [ARTIFACT_MODEL.md](ARTIFACT_MODEL.md) | Typed domain, version provenance, compatibility, invalidation and restoration |
| [JOB_EXECUTION_MODEL.md](JOB_EXECUTION_MODEL.md) | Jobs/operations/attempts, one lane, retries, cancellation and recovery |
| [COST_MODEL.md](COST_MODEL.md) | USD authority, reservations/liabilities, $40 cash envelope, estimates vs maxima |
| [UX_FLOWS.md](UX_FLOWS.md) | Composer, correction flows, approvals, mobile and exceptional states |
| [DESIGN.md](DESIGN.md) | Warm Creator, themes, interactions, accessibility and responsive composition |
| [GLOSSARY.md](../GLOSSARY.md) | Canonical terms and intentionally equivalent names |
| [VALIDATION_PLAN.md](VALIDATION_PLAN.md) | Future ten-real-English-project invitation gate and calibration |
| [PRODUCT_DECISIONS.md](PRODUCT_DECISIONS.md) | Dated owner rationale/history with current baseline pointer |
| [FEATURE_ROADMAP.md](FEATURE_ROADMAP.md) | Future features; not automatic first-Alpha scope |
| [ARCHITECTURE_SPIKES.md](ARCHITECTURE_SPIKES.md) | Completed gate status, authoritative evidence pointers and limits |

Accepted ADRs: [runtime](adr/0002-python-web-and-controlled-worker.md), [SQLite](adr/0003-single-host-sqlite-alpha.md), [follow-up Emphasis Text](adr/0001-editable-emphasis-text.md). Original dated decisions remain, with explicit freeze status addenda where needed.

[Pipeline investigation](PIPELINE_INVESTIGATION.md) records static source observations and freeze reuse classification. [Discovery notebook](ARCHITECTURE_DISCOVERY.md) is historical, not current policy. [Design references](../design-motivation/README.md) and [accepted Direction C](../design-prototypes/direction-c/README.md) are visual evidence, not production implementations.

All prior feasibility reports/indexes remain unchanged, including old pending-status/$30 statements applicable then. Read current status here/ARCHITECTURE_SPIKES.md rather than treating an old experiment index as active authority. [Freeze audit/preservation](architecture/freeze/v1/README.md) retains the original current-document bytes and scoped diff; no S9 V15, new spike, implementation, deployment or spend follows this freeze.
