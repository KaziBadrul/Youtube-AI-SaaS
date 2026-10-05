# Python web application and controlled production worker

Status: accepted conditional decision in the architecture baseline confirmed on 2026-10-03. Evidence gates remain unexecuted; Django/Python/runtime feasibility is not established. This ADR is authoritative for runtime/framework/reuse choice, not authorization to implement or execute spikes.

**Decision:** Python-first, with Django web/API and Python worker sharing domain services. Start with server-rendered pages and focused browser-side editing/progress interactions. Retain Python provider/media primitives after validation; replace their interactive/file-existence orchestration. See the complete A/B/C comparison in the [investigation notebook](../ARCHITECTURE_DISCOVERY.md#pipeline-boundary-comparison--accepted-direction).

**Requirements:** One engineer, private identities, project editing/persistence, existing Python components, FFmpeg/local alignment, durable long-running jobs.

**Alternatives:** FastAPI/Flask plus assembled web/auth/persistence components; TypeScript application orchestration with Python media; substantial pipeline rewrite; separate web/API/render/generation services.

**Tradeoffs:** One runtime and codebase reduce boundary duplication. Django supplies web/auth/persistence facilities, not project ownership rules or durable production scheduling. A focused browser editor still needs ergonomic validation. Separate processes isolate request handling from CPU-bound media and worker crashes; one host remains a shared failure domain.

**Reversibility:** Moderate web-framework migration cost; keep business rules independent of views. Browser UI and worker deployment can evolve without a media-engine rewrite.

**Evidence needed:** Dependency/runtime compatibility, scene-workspace interaction feasibility, resource isolation and recovery spikes. Django is not installed in the inspected environment. Exact dependency versions are deferred until a reproducible runtime is validated.

