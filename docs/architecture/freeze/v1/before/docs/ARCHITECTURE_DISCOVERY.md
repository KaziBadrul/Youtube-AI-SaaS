# Architecture discovery

## Accepted owner budget amendment — 2026-10-05

The active total prelaunch / Private Alpha operating ceiling is **US$40/month**, explicitly increased by the owner from US$30. This supersedes prior $30 wording wherever it described current financial authority. Historical interview/discovery notes and S9 V1–V11 evidence retain the $30 ceiling applicable when recorded; they do not control the current limit.

The $40 is a total owner cash-spend ceiling, not a generation-only allocation, creator credit balance or per-project authorization. Fixed obligations, actual spending, financial reservations and unresolved liabilities remain accounted for; safety/tax/payment/FX reserves and creator allowances remain unresolved. No automatic increase in credits/allowances, provider purchase/call or production implementation follows. See [current S9 reassessment](architecture/evidence/operating-economics/S9/CREDITS-v12.md). The owner’s rule ending host-sizing experiments unless failure remains in force.

Status: historical architecture-discovery interview record. Consolidated recommendations live in [ARCHITECTURE.md](ARCHITECTURE.md); this notebook is not a competing current contract, implementation plan or task list. Product authority remains the [confirmed Alpha specification](ALPHA_PRODUCT_SPEC.md). Source evidence is in [PIPELINE_INVESTIGATION.md](PIPELINE_INVESTIGATION.md).

## Accepted discovery policies — A1–A4

### A1: Reconcile unknown paid outcomes before retry

**Decision:** Pause the affected operation after an ambiguous paid-provider outcome, retain its budget reservation and require reconciliation before another paid attempt.

**Requirements:** Strict Alpha ceiling, paid-failure accounting, duplicate-call prevention.

**Alternatives:** Automatically retry inside remaining authorization while accepting possible duplicate charges.

**Tradeoffs:** Financial safety requires occasional owner intervention. Application idempotency alone does not establish provider-side exactly-once execution.

**Reversibility:** Policy adjustable; already incurred charges are not reversible.

**Evidence needed:** Provider request identity, result retrieval, actual billing visibility and documented idempotency behavior. None was verified by the source audit.

### A2: Local owner testing; evaluate a dedicated persistent host for invitations

**Decision:** Owner-first testing remains local. Evaluate a dedicated persistent host for invited testing, conditional on measured total costs fitting US$30/month. No vendor or machine size selected.

**Requirements:** Scheduled private access, Python/FFmpeg, persistence, one engineer.

**Alternatives:** Expose an existing personal machine during announced sessions; split managed web/worker/database services.

**Tradeoffs:** A dedicated host avoids dependence on the owner's workstation but consumes the generation budget. Budget feasibility remains unproven.

**Reversibility:** Moderate if paths, runtime configuration and owned storage references remain portable.

**Evidence needed:** FFmpeg/alignment resources, persistent disk behavior, hosting/backup/egress costs and actual generation costs.

### A3: Daily encrypted off-machine backups

**Decision:** Back up project state and retained media daily to a separate location. Accept up to 24 hours of lost work after catastrophic storage failure and manual restoration during Alpha. Ordinary process restarts must preserve committed state.

**Requirements:** Persistence, versions, recovery and retention.

**Alternatives:** More frequent backup, replication or no catastrophic-loss recovery.

**Tradeoffs:** Lower operational complexity at the cost of a recovery gap; backup expense remains inside the ceiling. A missed backup cannot silently extend the agreed recovery promise.

**Reversibility:** Frequency adjustable; lost work irreversible.

**Evidence needed:** Consistent database/media snapshot, restore verification, size/cost, deletion semantics and spending reconciliation after restoring older state.

### A4: One active request owns the global production lane

**Decision:** One request owns the slot throughout active generation/rendering. Start with sequential operations within it. Waiting-for-approval or budget-blocked jobs release the slot only once running operations have stopped; other eligible jobs may proceed.

**Requirements:** One active production job, queue visibility, concurrent edits and resumability.

**Alternatives:** Interleave projects at stage boundaries or parallelize scene operations inside a request.

**Tradeoffs:** Simpler recovery/resource/spend control, potentially longer waits. An unknown external outcome is not proof that the remote operation stopped; do not infer slot release from an HTTP timeout alone.

**Reversibility:** Internal scheduling can change without abandoning the global constraint.

**Evidence needed:** Stage duration, cancellation behavior and provider limits.

## Pipeline boundary comparison — accepted direction

| Criterion | A: Python generation/orchestration behind a controlled worker | B: Main application orchestrates; Python handles specialized media/ML | C: Substantial rewrite into the application language |
| --- | --- | --- | --- |
| Effort/reuse | Reuse provider/media primitives; replace unsafe CLI/file-existence orchestration | Reuse primitives but add inter-language execution/data contracts if the app differs | Recreate provider, parsing and orchestration behavior; most media dependencies still remain |
| Reliability/job control | One Python orchestration authority; durable job/attempt records still required | Can be reliable with one authority, but duplicated retries/state ownership across boundaries must be avoided | No intrinsic reliability advantage from changing language |
| Deployment | One Python runtime plus FFmpeg/local alignment dependencies | Usually two runtimes if the app is JavaScript/TypeScript | Potentially two runtimes remain for local alignment; rewrite does not remove FFmpeg |
| Testing | Fixtures/fake providers and subprocess tests around existing primitives | Contract tests plus stage tests across runtime boundary | Wider behavior revalidation; tests cannot assume preservation of legacy quality |
| Maintainability | Low conceptual overhead if web and worker share Python domain services | Good if a non-Python UI/server has independently justified value; more boundary ownership | Higher initial burden for one engineer; consistency alone is insufficient justification |
| FFmpeg | Existing command construction can be adapted | Python subprocess boundary or main-language process control | Commands must be recreated/validated; FFmpeg remains external |
| AI providers | Narrow Python capability adapters can retain provider-specific features | Main-language SDKs and Python adapters risk duplicate feature/cost logic | Rebuild integrations and reverify timeouts, retries, formats and billing |

**Decision recommended:** A, with deterministic Python orchestration in a separate worker process sharing domain services with the web application. Reuse narrow functions/algorithms where validated, not the interactive script entry points. Avoid an entire-project CLI subprocess as the only unit of recovery.

**Requirements:** One engineer, existing Python evidence, selective regeneration, long-running media, partial recovery, controlled spending.

**Alternatives:** B and C as compared above; direct execution of unchanged scripts.

**Tradeoffs:** Stage contracts and orchestration still need redesign. Narration must support independent scene correction; whole-script batching cannot simply be retained unchanged. Language consistency is a consequence, not the reason for this recommendation.

**Reversibility:** Stage contracts allow later relocation of orchestration; rewriting a second time remains costly.

**Evidence needed:** Per-scene narration continuity/cost, Unicode alignment, provider request controls, output validation and cancellable FFmpeg boundaries.

## Minimum topology hypothesis — not accepted

**Decision recommended:** One persistent host, one application codebase, separate web and single-production-worker processes. The web process provides browser UI, API, authentication and authorized asset delivery; the worker orchestrates stages and invokes controlled media child processes. Keep rendering in this worker lane rather than a separate render service. Use relational state for queue/checkpoints instead of an external broker initially. Backups run as scheduled operational maintenance, not a second production worker.

**Requirements:** Web responsiveness during CPU-bound media, long-running jobs beyond request lifetime, one active production job and modest invited usage.

**Alternatives:** Everything inside the HTTP process; independent API/generation/render microservices; managed broker plus separate workers.

**Tradeoffs:** A single host is a failure domain, addressed by accepted backups rather than high availability. A durable queue is still required even though an external broker is not. Maintenance must coordinate disk and snapshot activity; it cannot be allowed to trigger paid generation.

**Reversibility:** Moderate; preserve process boundaries and portable records so worker/storage can move later without speculative distributed infrastructure today.

**Evidence needed:** Resource limits leaving the web responsive, worker exclusion/fencing and crash recovery, render peak scratch space and hosting costs.

## Application framework and database candidates — subsequently accepted conditionally in A10/A11

### Python web application

**Decision recommended:** Evaluate Django with server-rendered pages and focused browser-side interaction for the Alpha scene workspace. Share Python domain services with the worker. Do not choose a client framework or add a separate frontend service without interaction evidence.

**Requirements:** Private identities/sessions, ownership checks, relational persistence/migrations, solo maintenance and reuse of Python stages.

**Alternatives:** FastAPI plus separately assembled auth/session/admin/persistence components; JavaScript/TypeScript web application plus Python worker; Flask with similar assembly needs.

**Tradeoffs:** Django offers authentication/session and persistence facilities, reducing components to assemble; scene ownership authorization remains application responsibility. Server rendering must still satisfy autosave, progress and editing ergonomics. FastAPI remains a credible alternative if an independently justified API-heavy UI benefits from it. Framework-provided request background tasks are not the durable job system.

**Reversibility:** Moderate for web framework, lower if business rules remain independent of views. A later richer browser editor does not require moving the generation engine.

**Evidence needed:** Representative scene-workspace interaction feasibility and dependency/runtime compatibility; no framework has been installed. Official [Django authentication documentation](https://docs.djangoproject.com/en/5.2/topics/auth/default/) describes session/auth facilities; [customization documentation](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/) explains that object-permission enforcement is not supplied by the core implementation.

### Relational state

**Decision recommended:** Evaluate SQLite on the same persistent host for this single-worker Alpha, with short serialized write transactions and integer monetary units. Do not choose PostgreSQL only because it is familiar. Use PostgreSQL if concurrency/recovery evidence makes SQLite unacceptable or the topology actually requires separate hosts.

**Requirements:** Atomic allowance/budget reservations, durable jobs, owner/version relationships, multiple simultaneous web edits but only one executing production job.

**Alternatives:** PostgreSQL on the host or managed PostgreSQL; document files/JSON as primary state; external queue as state authority.

**Tradeoffs:** SQLite eliminates a database service, but has one writer and requires same-host local-disk WAL. It does not provide PostgreSQL-style row locks. Short transactions must serialize admission, render locks and compare-and-select updates; never hold a database transaction across provider/FFmpeg execution. File/JSON state does not satisfy required atomic relationships and accounting.

**Reversibility:** Moderate database migration cost. Use explicit relational contracts, IDs, integer money and logical storage keys rather than SQLite-specific behavior leaking into domain rules. The migration trigger is a demonstrated need, not hypothetical scale.

**Evidence needed:** Concurrent autosave/admission/worker commits, lock contention, durable settings, consistent backup and crash/fencing tests. [SQLite WAL documentation](https://www.sqlite.org/wal.html) establishes same-host and single-writer limits. [Django SQLite notes](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes) document transaction modes, unsupported `select_for_update`, and decimal limitations. Monetary values therefore must not rely on floating-point/SQLite decimal arithmetic. Use the [SQLite backup API](https://www.sqlite.org/backup.html) or another verified snapshot mechanism, not an uncoordinated copy of the live database file.

## Accepted discovery policies — A5–A9

The user accepted A5–A9. A9 explicitly clarifies the product deletion promise. At that discovery interview, the US$30 ceiling was owner-configurable rather than permanent or hardcoded; no revised amount or unlimited spending was authorized then. The later owner budget amendment above supplies the current US$40 authority.

### A5: Cancellation after paid submission

**Decision:** Stop launching new operations; cancel the active provider operation where supported. Retain technically valid output already paid for as history, and count it against allowance if delivered, even if it arrives after cancellation. Do not automatically select it after cancellation. Show any unresolved cost and reconcile under A1.

**Requirements:** Paid failures, successful-asset accounting, cancellation, version safety.

**Alternatives:** Owner absorbs every canceled request; discard late successful outputs; promise provider refunds.

**Tradeoffs:** Cancellation prevents future work but cannot guarantee reversal of submitted costs. History preserves value without overwriting creator decisions.

**Reversibility:** Future charging policy adjustable; historical spend/charges immutable except explicit correction entries.

**Evidence needed:** Provider cancellation support, request state retrieval, actual charge and delivery semantics.

### A6: Edits while queued

**Decision:** Bind queued authorization to its reviewed input/configuration versions. If those inputs change before execution, pause the affected work for an updated plan/confirmation rather than generating superseded content or silently enlarging the scope. Preserve compatible completed work.

**Requirements:** Editable projects, stale-result prevention, transparent authorization.

**Alternatives:** Always execute the original snapshot; automatically use latest content within the old ceiling.

**Tradeoffs:** An extra confirmation avoids surprising spend on obsolete or newly changed instructions.

**Reversibility:** Admission policy adjustable; provenance records must retain which input was actually authorized.

**Evidence needed:** Deterministic input signatures and authorization revocation/refresh tests; no paid spike needed.

### A7: Monthly budget period

**Decision:** Use calendar months in Asia/Dhaka, the owner's timezone. Attribute generation spend/reservations to the request attempt's accounting period; at a month boundary reauthorize new paid attempts against the new period without releasing old unresolved liabilities. Reserve known recurring infrastructure costs before admitting generation. Include tax/fees/currency-conversion margins in the owner-approved USD-equivalent accounting basis.

**Requirements:** Strict total monthly Alpha ceiling, durable actual-spend accounting and approval before excess spending.

**Alternatives:** UTC calendar months; rolling 30-day window; provider invoice cycles.

**Tradeoffs:** Owner-readable periods require explicit timezone/billing reconciliation; request-start attribution is not a claim about provider invoice timing. Actual invoices may need correction entries and must not be ignored.

**Reversibility:** Period policy can change prospectively; closed history should not be rewritten silently.

**Evidence needed:** Provider billing timing and tax/FX basis; exact recurring amounts remain deferred.

### A8: Which generated outputs consume allowance

**Decision:** Count successfully delivered paid text/research/checking results as well as valid images/narration. Offer this breakdown in optional Details; routine cost display/review is not required for authorization. Local deterministic transformations and rendering do not consume generation allowance. A paid attempt yielding an unusable/failed result counts only toward actual operating spend, not successful-output allowance.

**Requirements:** Model-dependent operation estimates, successful-output accounting and separate actual spend.

**Alternatives:** Images/narration only; owner absorbs all text/research cost; deduct allowance for every provider attempt regardless of output.

**Tradeoffs:** More complete usage attribution needs clear inspectable operation results and technical success definitions.

**Reversibility:** Prospective allowance policy adjustable; Alpha is not a paid commercial credit system.

**Evidence needed:** Capability-specific success checks, provider usage/pricing metadata; numerical allowance values remain deferred.

### A9: Deleted media in backups

**Decision:** At seven days, permanently remove project content from active storage and make it non-restorable through the application. Purge its backup copies in the next daily backup/purge cycle, at most 24 additional hours later. Never restore a purged project from an older snapshot; retain non-content accounting/deletion records needed for reconciliation.

**Requirements:** Seven-day recoverable deletion, daily backup recovery, private media isolation, actual-spend history.

**Alternatives:** Immediate physical deletion from every backup at the seven-day deadline; longer backup retention with content excluded from user restore.

**Tradeoffs:** A bounded backup purge lag simplifies daily backups and explicitly changes the interpretation of permanent deletion; the user approved this clarification in A9. Backup failure must not silently extend this lag.

**Reversibility:** Future retention policy adjustable; erased content cannot be recovered.

**Evidence needed:** Backup layout/purge behavior and deletion records surviving database restoration. No indefinite backup retention is implied.

## Discovery answers — A10–A14

### A10: Python-first application boundary

**Decision:** Choose boundary option A: Python orchestration and media behind a separate worker, with Django providing the web/API in the same codebase. Use server-rendered pages and focused browser interactions initially; do not add a separate frontend deployment. This is a proposed baseline, not permission to implement.

**Requirements:** Existing reusable Python primitives, one engineer, private sessions/ownership, persistent relational state, scene editing and long-running jobs.

**Alternatives:** FastAPI plus explicitly assembled auth/persistence/web tools; a JavaScript/TypeScript web application orchestrating Python media; substantial rewrite. The earlier comparisons explain effort, reliability and deployment implications.

**Tradeoffs:** Lower runtime/component count and built-in web facilities; rich editing ergonomics still need a representative interaction check. A later browser editor can become richer without moving generation.

**Reversibility:** Moderate framework cost; keep domain rules outside views and preserve typed stage contracts.

**Evidence needed:** Workspace interaction feasibility, library/media compatibility and worker recovery. Exact dependency versions remain unspecified.

### A11: SQLite versus PostgreSQL for the single-host Alpha

**Decision:** SQLite on local persistent disk is the initial candidate, contingent on a concurrency/recovery spike. Use short serialized write transactions, relational constraints and integer financial units. If the spike fails, revisit PostgreSQL explicitly rather than masking locking errors.

**Requirements:** One host/production worker, atomic admission/accounting, multiple web users/edits, durable state and low operational overhead.

**Alternatives:** PostgreSQL from the start, locally or managed; files as primary state.

**Tradeoffs:** Avoid a database server but accept one-writer constraints and a single-host boundary. PostgreSQL buys stronger multi-host/concurrent-write facilities at operational cost; current scope does not demonstrate that need.

**Reversibility:** Moderate migration cost; logical media keys, portable IDs/relations and integer money ease migration.

**Evidence needed:** Simultaneous autosave/reservation/claim/publish/cancel/lock tests and consistent recovery/backup. No choice is justified by familiarity alone.

### A12: Restore narration whose words differ from current narration

**Decision:** Show the associated older narration text before restoring its audio. Require approval to restore that text with the audio and compatible timing/captions; then update current script consistently. Never make audio with different spoken words current under unchanged narration text.

**Requirements:** Restoration, narration/audio agreement, script consistency and safe edits.

**Alternatives:** Refuse the restore until text matches; restore audio as outdated/unexportable; silently change current words.

**Tradeoffs:** Explicit compound restore protects approved wording. A matching-text audio restore needs no text-change consent.

**Reversibility:** Reversible by version selection; original input remains unchanged.

**Evidence needed:** Deterministic compatibility signatures, source text provenance and restoration validation; no paid-provider experiment required.

### A13: Manual captions/timing after narration changes

**Decision:** Preserve manual caption text and timing corrections as versions. When changed narration/audio makes them incompatible, mark them outdated and propose refreshed timing/captions rather than silently replacing manual work. Require resolution before exporting with captions enabled; disabling captions bypasses caption-only blockers. Narration/timing required for the video itself must still be valid.

**Requirements:** Editable captions/timing, dependency invalidation, no outdated required output and preserved versions.

**Alternatives:** Overwrite manual edits with regenerated captions; retain incompatible captions as current; disallow manual corrections.

**Tradeoffs:** Some edits add review work, but manual changes are not silently lost. Compatible automatic captions can update automatically within authorized work.

**Reversibility:** Versioned corrections are reversible; source compatibility must remain explicit.

**Evidence needed:** Caption/audio mapping tests, multilingual timing fixtures and enabled/disabled export checks.

### A14: Deleting a project while generation is active

**Decision:** The user rejected deletion during active generation. Disable deletion until the creator cancels and execution cessation is confirmed. Deletion during final rendering remains prohibited. Queued, never-started work must be canceled transactionally before an otherwise permitted deletion; claim/delete races cannot launch work for a deleted project.

**Requirements:** Explicit A14 rejection, private/deleted assets, one active job and safe cancellation.

**Alternatives:** The rejected proposal hid a project and canceled generation automatically while retaining late results; no such behavior is adopted.

**Tradeoffs:** The creator must cancel first; this avoids deletion while paid work or media children are still running. Unknown execution cannot be treated as stopped.

**Reversibility:** The UI policy could change after explicit product approval; actual deletion remains irreversible after the recovery window.

**Evidence needed:** Confirmed-cancellation eligibility, worker/deletion races and render-lock checks.

## Accepted discovery policy — A15

The user accepted the scoped voice/delivery restoration policy. This resolves compatibility when older audio has unchanged words but a different voice, without silently changing the whole project.

**Decision:** Show the recorded voice/delivery in restore confirmation and let approval adopt it for the restored scene only. Preserve other scenes and project defaults; use a scoped explicit restoration choice, not an unannounced project-wide voice change. Original generation provenance remains unchanged. Future regeneration must expose the effective voice/configuration it will use before authorization.

**Requirements:** Restore earlier versions, maintain narration/configuration agreement, preserve unaffected assets and make important creative choices explicit.

**Alternatives:** Refuse restore when voice differs; require changing the project voice, affecting other scenes; silently ignore voice compatibility.

**Tradeoffs:** A scoped restored voice may intentionally differ from other scenes, but avoids broad invalidation or hidden changes.

**Reversibility:** Creator can restore another version or authorize regeneration; history persists.

**Evidence needed:** Restoration compatibility/selection fixtures under S7. No provider calls required to decide the policy.

## Status and boundaries

A1–A13 are accepted discovery directions; A14 was rejected and deletion during active generation is prohibited. Python/Django and SQLite are conditional on evidence gates. A15 is accepted. The user confirmed the consolidated architecture baseline on 2026-10-03; feasibility gates remain unexecuted. Providers, deployment vendor, exact allowances/storage caps and public economics remain deferred. Necessary feasibility spikes will be specified with question, method, success criteria and evidence; none is authorized for execution by this document.

## Final architecture confirmation — 2026-10-03

The user accepted [ARCHITECTURE.md](ARCHITECTURE.md) and its referenced authoritative models/ADRs as the Private Alpha baseline, subject to all documented evidence gates. Conditional decisions remain conditional, with no implied runtime, provider, backup, deployment or operating-budget feasibility. Failed gates require explicit reconsideration or scope/budget decisions; no silent infrastructure additions, requirement weakening, spending-control bypass or ceiling increase.

Providers, hosting vendor, exact allowances/storage limits, actual costs and public commercial decisions remain deferred. Design confirmation does not authorize application implementation, paid experiments, deployment purchases, spike execution or an implementation task graph. Architecture discovery is closed at the design-definition level; feasibility evidence has not been collected through execution.
