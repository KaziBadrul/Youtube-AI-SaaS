# Private Alpha architecture

Frozen Private Alpha baseline v1 — 2026-10-05. Architecture Freeze reconciles accepted decisions; it authorizes neither implementation nor capability activation.

S1–S8 PASS at their documented scope (S4 after remediation); **S9: PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY**, closed at [V14](architecture/evidence/operating-economics/S9/CREDITS-v14.md). No spikes are reopened. [Product](ALPHA_PRODUCT_SPEC.md) owns scope; detailed architecture contracts have one home: [artifacts](ARTIFACT_MODEL.md), [jobs](JOB_EXECUTION_MODEL.md), [finance](COST_MODEL.md), [UX](UX_FLOWS.md), [design](DESIGN.md). [Freeze record](architecture/ARCHITECTURE_FREEZE.md) summarizes these and classifies activation prerequisites.

Active financial authority is **$40 USD per Asia/Dhaka calendar month**, governed by COST_MODEL.md; estimates, reservations, liabilities and creator credits are distinct. S9 V14 is conditional planning feasibility, never automatic paid activation.

## Runtime shape

One application codebase runs on one persistent host. Separate the short-lived web request process from one production worker. Provider, alignment and FFmpeg work execute through that worker; they do not run inside an HTTP request or framework request-background callback. Rendering is a worker capability, not a separately deployed service.

```mermaid
flowchart LR
    B[Creator browser] --> H[HTTPS gateway]
    H --> W[Django web and API]
    W --> D[(Local SQLite: project state, queue, ledger)]
    W --> M[Private persistent media]
    P[Single Python production worker] --> D
    P --> M
    P --> A[External capability adapters]
    P --> C[Controlled alignment and FFmpeg child processes]
    C --> M
    K[Scheduled backup and purge maintenance] --> D
    K --> M
    K --> O[Encrypted off-host backup]
```

The gateway may be host software or a deployment facility; no vendor is selected. Static UI files may be public. Project media, database files, scratch and credentials never have public filesystem routes. Background maintenance has no generation authority and must coordinate storage/snapshots with the running app. Memory-heavy backup/maintenance must be serialized with rendering, alignment and other heavy production work; daily backup/purge deadlines remain mandatory. It is not another production worker.

### Runtime and application boundary decision

[ADR-0002](adr/0002-python-web-and-controlled-worker.md) is authoritative for the Python/Django runtime choice, existing-pipeline A/B/C comparison, alternatives, tradeoffs and evidence gates. The browser UI remains an interaction requirement, not a separately deployed frontend service.

## Relational state

SQLite with WAL, foreign keys, FULL synchronous durability and bounded busy handling stores users/sessions, ownership, project and scene metadata, typed artifact content/versions, selections and provenance, jobs/operations/attempts, progress events, render locks/manifests, export registrations, research/warnings, financial ledgers/reservations and deletion state. Large media bytes do not live in the database.

### Database decision

[ADR-0003](adr/0003-single-host-sqlite-alpha.md) is authoritative for the conditional SQLite choice, alternatives, transaction/money constraints and evidence gates. PostgreSQL is the explicit reconsideration path if the gate fails or a demonstrated multi-host requirement arises.

Financial admission uses integer monetary units and conservative bound rounding. Use short explicit write transactions/CAS rather than assuming SQLite row locks; never hold a transaction across provider calls, FFmpeg, upload copies or media backups.

## Project domain and ownership

One User owns each Project; there are no teams/workspaces in Alpha. Every scene, artifact/version, operation, warning, upload and export resolves to that project. There is no public project sharing. The [artifact model](ARTIFACT_MODEL.md) defines Original Input, current Script, stable Scenes, typed Artifacts/Versions, Research Results and Factual Warnings without collapsing them into an MP4.

Jobs are execution requests; Operations are scoped units of work; Attempts record concrete executions/provider submissions. Render is an execution over a fixed manifest; Final Export is its successfully validated persisted output. An Allowance belongs to an identity. Shared operating Budget belongs to the owner and period. Authorization is user/owner authority; Reservation is a held liability, not actual consumption. See the dedicated models for relationships.

## Media and storage

### Storage decision

**Decision:** Use private host-local persistent file storage initially, referenced by opaque logical keys in database metadata. Keep an explicit media boundary so later object storage is a migration, not a domain rewrite. Backups live encrypted in a separate location; no storage provider or quota selected.

**Requirements:** Images/audio/intermediates/exports/previous versions, safe FFmpeg access, retention, isolated delivery and low-cost single-host operation.

**Alternatives:** Object storage immediately; database BLOBs; public project directories; ephemeral deployment filesystem.

**Tradeoffs:** Local files simplify media processing but share the host's failure domain. Object storage adds transfer/authorization/egress complexity. Persistent media and the database must be backed up consistently. Database rows are authoritative references, not filename scans.

**Reversibility:** Moderate bulk migration; retain logical keys, byte hashes/sizes/types and original provenance rather than absolute paths in domain records.

**Evidence needed:** Per-project and peak scratch sizes, storage admission margins, backup/restore and hosting durability. Owner-set operational caps are required before invitations, informed by measurements; fail closed until configured.

Storage classes:

| Content | Authoritative location and lifecycle |
| --- | --- |
| Original inputs, current scripts, narration text, prompts, settings | Typed database content/versions; immutable originals and versioned edits |
| Research summaries, source references, warnings, word/scene timings, editable captions | Database structured content with source/version provenance; bounded capture of provider responses where needed |
| Generated/replaced images, narration audio, reusable audio components | Private durable media; database metadata and immutable versions |
| Provider response recovery spool | Durable attempt-scoped private staging until safely published/reconciled; not served to users |
| Rebuildable scene clips, concat lists, render scratch | Attempt-scoped temporary files; safely discard/rebuild after confirmed termination |
| MP4 exports and optional derived subtitle files | Private durable versioned media; only registered validated exports are deliverable |
| Deleted projects in seven-day recovery | Hidden but retained metadata/media; counts against storage; restore only within window |
| Backups | Consistent database snapshot plus referenced immutable media and manifest; encrypted off-host, with accepted purge deadlines |

Never pass user filenames/paths into FFmpeg or let the worker infer project ownership from folders. Uploads stage under server-generated IDs; image replacement is the only current media-upload scope. Validate allowed bytes/type/decoding/dimensions/resources before selection. Exact upload allowlists/limits remain an operational specification gate; no arbitrary local path or remote URL import is implied.

Atomically install validated bytes under a new immutable key, then register/select transactionally. The filesystem and database are not one transaction: durable attempt manifests allow recovery of a file installed before its database registration. Unregistered files are private, not automatic successful exports. Reuse recovered paid output rather than issuing another paid call because persistence failed.

## Authentication and isolation

### Authorization decision

**Decision:** Use Django identity/session facilities with operator-provisioned invited accounts and application-enforced project ownership. No external auth vendor/public signup needed. Every read/write/media request checks the authenticated identity against database ownership and deletion state. Render/generation locks are enforced server-side, not only in disabled controls.

**Requirements:** Private identities, isolated projects/assets, no cross-tester access, reversible seven-day deletion and protected credentials.

**Alternatives:** External identity vendor; shared access password; client ownership checks; unguessable/public media URLs.

**Tradeoffs:** Local identities minimize integrations but require password/session/recovery hygiene. Django identity is not object ownership authorization; explicit checks remain required. The operator is privileged, while testers cannot access other tenants.

**Reversibility:** Identity providers can be added behind internal user IDs; permission semantics must remain independent of vendor IDs.

**Evidence needed:** Cross-user endpoint/file/range-download tests, CSRF/session behavior, deleted-project denial and operator recovery. [Django authentication](https://docs.djangoproject.com/en/5.2/topics/auth/default/) provides facilities; [object-permission notes](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/) explain core does not implement tenant access checks.

Workers are privileged service processes with secrets outside public media/logs/client bundles. They claim server-created job IDs, resolve ownership from persisted records, validate scope and check fencing before persistence. They do not trust an LLM or browser-provided owner ID. Private asset delivery uses an authenticated controller or an authorization-checked internal gateway route, including range requests for video. No direct public media mount or long-lived bearer URL bypass is required.

## Rendering

S6 local feasibility update, 2026-10-05: [PASS report](architecture/evidence/rendering-feasibility/S6/README.md). The current FFmpeg still lacks text/subtitle filters; deterministic HarfBuzz/FreeType caption PNGs plus FFmpeg overlay demonstrated a viable five-language local path. Validated 3/5/10-minute outputs, continuous narration, visual mapping, controls, cancellation/recovery and measured resources support this runtime boundary. Target-host packaging, production font/layout and economics remain unfrozen; no extra paid service or production implementation was introduced.

Rendering executes inside the production lane through a controlled FFmpeg process group, using a fixed manifest of selected compatible scene/audio/timing/caption/settings versions. Acquire the project render lock transactionally when execution begins, not throughout its queue wait. Recheck queued inputs before locking; changed inputs follow the accepted refresh-authorization rule.

All content changes—including deletion/restoration/correction acceptance—are blocked while rendering. Viewing, previous-export downloads and cancel remain available. Track machine-readable progress and confirmed process exit. Cancellation terminates the child group with bounded escalation; unlock only after confirmed cessation. Worker restart must inspect/terminate the old group before claiming a new render, not infer termination from a stale heartbeat.

Use unique render output/scratch paths. Validate playable 1080p/30 fps MP4, complete narration, scene order/coverage and readable enabled captions before registration. Never use `-shortest` or success exit alone as proof of full narration. Preserve previous exports; retry local assembly from existing assets. Rendering costs count against actual operating budget, not tester generation allowance.

Caption burn-in requires a verified build/layout path. Inspection found `zoompan`, `amix` and `loudnorm` but no `subtitles`, `ass` or `drawtext` filters in this workstation's FFmpeg. S6 closed this gap using HarfBuzz + FreeType shaping, Pillow caption PNG composition and timed FFmpeg overlays. Use that deterministic worker-local caption path; no extra service or assumption of subtitles/ass/drawtext support. Package licensed Noto Sans, Bengali and Devanagari coverage with verified hashes/shaping; exact supported package versions are pinned during implementation. S9 V9–V11 supplied Linux regressions. Experimental-language narration remains independently gated. FFmpeg's [progress facility](https://www.ffmpeg.org/ffmpeg.html) supports structured progress, but cancellation/recovery require application control.

## Provider capabilities

### Adapter decision

**Decision:** Narrow capability adapters for research/search, text/script/scene planning, pasted-script checking, images and TTS; local alignment is a separate media capability. Preserve provider-specific options in validated configuration, not a universal least-common-denominator API. Deterministic orchestration selects adapters and authorizes each concrete attempt.

**Requirements:** Validated structured output, model/config provenance, accurate spending/retry control, reuse and future model changes without a universal provider framework.

**Alternatives:** Direct SDK calls in views/domain logic; all-powerful agent orchestration; universal provider marketplace abstraction.

**Tradeoffs:** A few explicit contracts avoid leakage of SDK retry/format behavior. Provider-specific capabilities and unsupported guarantees remain visible. The existing Gemini source is evidence, not a vendor commitment. Research may require a separate provider capability because current code does not implement it.

**Reversibility:** Moderate integration cost; versioned capability configuration and recorded provider identities allow migration without changing project semantics.

**Evidence needed:** Request cost bounds, response formats, actual usage, timeouts/idempotency/retrieval/cancellation and SDK retry controls. No paid capability is enabled merely because an SDK method exists.

Every attempt records prepared input signature, provider/model/config, request/correlation IDs where available, timestamps, transport outcome, output-validation outcome, observed usage and cost certainty. Disable hidden SDK paid retries or expose every billable attempt to the same authorization boundary. Never log keys or unrestricted prompt/user content. Unknown submission outcomes follow A1.

The accepted narration contract separates Scene Narration Text, Narration Generation Segment, immutable Source Narration Audio, Scene Audio Mapping and Derived Project Narration. **B coherent initial generation and B whole affected-segment corrections are selected.** Scene editing does not imply one request per scene. Deterministic grouping pins contiguous scene/text/configuration membership; preserve memberships and unrelated segments across edits. No final word/byte constant is selected. Delivery instructions remain metadata over approved words. Scene mappings govern visual/caption timing, never ordinary destructive cuts of B audio. Safe exceptional restoration/reorder composition is separately validated under ARTIFACT_MODEL.md.

Research uses the remediated S4-R boundary: topic/script → bounded Gemini planner → validated query list → application-controlled Tavily Basic searches → bounded evidence → tool-free bounded synthesis/checking. The application admits query count, endpoints, evidence/token bounds and attempts; model output cannot expand searches. Research entitlement is checked before execution. Pasted-script checking remains distinct and cannot rewrite words without consent. No unbounded grounding, crawling or free quota assumption.

Selected image model: `gemini-3.1-flash-lite-image`. Selected TTS model: `gemini-3.8-flash-lite-tts`. Normal text/research model remains a pre-capability decision; `gemini-3.5-flash-lite` is the S4/S9 candidate, not silently adopted. Custom Topic Suggestions records `gemini-3.8-flash` as its owner-selected roadmap model; no substitution without explicit amendment. No provider is enabled merely by naming a model.

TTS capability metadata must represent verified request/input-token/output-token or audio-duration limits, relevant request/token rate quotas and reset scopes, supported formats/delivery/context constraints, and segmentation policy constraints. Record provider/model/account tier, source and verification time; unknown limits stay unknown. Word count is only a planning heuristic. Before invocation revalidate the pinned policy/capability basis; changed limits that invalidate a plan require refresh and renewed authorization, not hidden splitting or additional calls. Known quota waits use durable cancelable scheduling in the existing global lane model; a 429 alone does not establish safe zero-charge failure. No permanent Gemini RPM/RPD is a domain invariant. The [current official rate-limit page](https://ai.google.dev/gemini-api/docs/rate-limits) directs account-specific active limits to AI Studio; none was verified for this owner. See the dated pipeline audit for source evidence and limitations.

## Observability

### Observability decision

**Decision:** Persist job/operation/attempt histories and financial events; use rotated structured host logs with correlation IDs and basic disk/backup/worker health. Provide an owner view of pending reconciliation, failures and actual/reserved spending. No separate observability service required.

**Requirements:** Debugging by one engineer, partial recovery, provider attempts, performance/cost measurement and auditability.

**Alternatives:** Console-only logs; production-scale tracing/metrics stack from day one.

**Tradeoffs:** Simple operation; log rotation, redaction and health checks still need explicit configuration. Debug metadata is useful without logging all private scripts/media.

**Reversibility:** Structured event IDs can feed external observability later.

**Evidence needed:** Failure traces and retention/storage measurements. Record project/job/operation/attempt IDs, stage, provider/model, durations, safe error codes, retries, estimates, incurred/unknown spend and backup age. Progress is stage-based; do not invent a completion percentage for a provider without progress support.

## Development and invited deployment

### Deployment decision

**Decision:** Same conceptual topology locally and on a dedicated persistent invited-Alpha host, with portable runtime/configuration and coordinated supervision of web, worker and media children. The locally qualified host class is **2 vCPU / 4 GiB**; host sizing is closed unless later evidence reveals failure. Vendor/SKU and reproducible packaging remain gated choices. Owner-only validation may use an existing local machine; invited Alpha requires a persistent privately accessible host.

**Requirements:** Scheduled private availability, long-running jobs, durable local files/SQLite, Python/FFmpeg dependencies, one active job and low operating cost.

**Alternatives:** Personal-machine access; persistent VM; container/PaaS with durable volume and long-running worker; split managed services or request-only serverless execution.

**Tradeoffs:** A small VM is a candidate, not an endorsed purchase. A persistent container service is also viable if disk/process/timeout and total billing behavior satisfy the gates. Request-only/ephemeral hosting cannot be the sole execution/storage substrate. Split services may solve operational needs but consume budget and add transfer/state complexity.

**Reversibility:** Moderate deployment move if persistent state/media and worker ownership are separated from vendor-specific APIs.

**Evidence needed:** Hardware render/alignment measurements; supervision/cancellation; persistent disk/backup; HTTPS/private access; full cost including fixed fees, egress, tax, backup and generation. No hosting price or free-tier suitability is assumed.

Daily encrypted off-host snapshots must restore metadata and referenced media consistently. Recovery from catastrophic storage loss accepts up to 24 hours of lost work and manual restoration. Keep the restored system unavailable for paid work until spending, deletion records and uncertain attempts are reconciled; a backup must not roll back real charges. Reapply deletion deadlines before serving data. Project content purges from active storage at seven days and from backups within at most 24 additional hours; backup failure does not extend that deadline. S8 supports this local protocol; actual off-machine destination, historical-copy purge and key/restore acceptance must establish it before invitations without resurrecting private/deleted content.

Deletion/purge authority must survive independently of the database snapshot being restored. Maintain an independently recoverable non-content deletion/purge journal or verified equivalent, with event identities and recovery cutoff. Do not acknowledge a completed deletion without its durable recovery authority; locally hidden projects remain inaccessible while journal persistence is unresolved. Reconcile this authority before enabling restored media/project access. Missing or incomplete deletion history fails closed, rather than resurrecting a project from an older snapshot. The exact journal storage mechanism is an implementation/operational choice constrained by accepted S8 independent-current-authority semantics; no vendor is selected.
