# Authorized local feasibility experiment plan

This plan is recorded before gate execution. Authority: current user authorization for S1, S2, S3, S7 and S8 only, in that order. These are disposable experiments, not production application code or implementation acceptance. No provider SDK, credentials, external generation, FFmpeg rendering, deployment or purchases are used. S4/S5/S6/S9 remain unexecuted.

## Inventory and source basis

Read AGENTS.md, CLAUDE.md, docs/README.md, product, architecture, design, UX, artifact/job/cost models, feasibility gates, accepted runtime/SQLite ADRs and narration amendments. Repository has no Python app/dependency manifest/test suite; scripts/orchestrator.ts is empty. Existing external canonical scripts are identified in PIPELINE_INVESTIGATION.md; inspected imports/functions show provider clients initialized at module level, so they will not be imported. A pure SRT helper can be AST-extracted for a free runtime check. Demo media/design prototypes are interaction evidence only; no source assets will be mutated.

Existing workstation: Python 3.12.14, SQLite 3.53.4, OpenSSL available. No Django, cryptography, pytest or alignment packages in the inspected environment. Install only Django 5.2.x and cryptography 46.x into a temporary dedicated venv; record exact versions. No frontend framework. Test media will be small valid WAV/SVG and synthetic export bytes; no video quality or caption/render capability claim is made.

Scaffold: spikes/local-feasibility/. Evidence: this directory. Run data: disposable temporary directories. Existing user/untracked files are preserved. Artifact/job schema is a deliberately small invariant witness, not a proposed production schema.

## S1

Claim: server-rendered Django plus focused vanilla JS can support the representative correction/composer interaction, authenticated private assets, autosave and polling without a separate frontend deployment.
Failure sought: request-bound generation, ownership/CSRF bypass, lost/stale autosave, render-lock bypass, whole-page refresh dependence.
Minimum: Django session/auth facilities and template with composer, scene list, correction inspector; narrow HTTP endpoints sharing a fixture service with a separate fake worker. Tests use authenticated HTTP clients plus JS interaction checks; browser inspection if available. Compile safe legacy Python helpers without client imports. Record runtime/library versions.
Pass: private and cross-user/anonymous/deleted access denied including Range; CSRF enforced; autosave version conflicts explicit; only changed scene invalidated; content edit rejected under render lock while reads/cancel remain available; command queues promptly and separate worker persists progress; same-origin enhancement preserves current input/selection. No claim about real provider/alignment/media dependency compatibility until S4/S5/S6.

## S2

Claim: same-host WAL SQLite with foreign keys, FULL durability and short BEGIN IMMEDIATE/CAS transactions can enforce Alpha invariants.
Failure sought: double claim/reservation/ledger, silently lost accepted edits, cross-project selection, invalid current assets, stale/canceled/deleted completion, leaked render locks and partial commits.
Minimum: real independent Python processes/connections; 8-way simultaneous races, 20 repeats per race family; 8 writers x 100 progress/edit transactions for contention; forced process exit inside a multi-record transaction. Integer monetary units. No external wait inside transactions.
Pass: all invariants hold in every repetition, integrity/foreign-key checks clean, no unhandled lock error, each stress transaction <5 seconds and p99 <2 seconds (fixture evaluation thresholds, not product SLA). An expected version conflict/rejected deletion is not a lost accepted edit. Failure triggers PostgreSQL reconsideration; later dependent results cannot be presented as passing.

## S3

Claim: persisted attempts/fencing plus confirmed child/external outcomes prevent overlapping execution, retain liability and reuse recoverable output.
Failure sought: crash-induced duplicate paid submission, lease expiry permitting overlap, unknown outcomes releasing liability, stale selection, cancellation losing good work.
Minimum: separate fake provider state, real worker processes killed at named checkpoints, independently surviving local process group, fake known-failure/pre-submit-timeout/ambiguous-timeout/delayed/replayed outcomes. At least three repeats per crash boundary. Durable file operations are resumed without another provider submission.
Pass: no blind duplicate fake billable request; uncertainty blocks new lane claims/unsafe retry; prepared ambiguity retained absent evidence; old child stop observed before replacement; stale fencing/text/cancel cannot select current; successful unrelated work unchanged; callbacks/ledger exactly once. Host supervision and real-provider reconciliation remain deployment/S4 gates.

## S7

Claim: staged bytes -> validation -> immutable durable install -> transactional metadata/ledger -> guarded selection is recoverable despite filesystem/database non-atomicity.
Failure sought: orphan success, invalid files replacing current, metadata without durable bytes, duplicate charges, replaced export lost, restoration silently altering sibling words/settings.
Minimum: real subprocess exits at response/stage/validation/install/metadata/ledger/selection/export boundaries; three repeats; valid tiny WAV fixture and hashes; synthetic export publication (not S6 validation). Restore shared-source scene ranges with approved matching/different words, scene-only voice adoption and compatible/incompatible manual timing/caption fixtures.
Pass: incomplete/unregistered bytes are not deliverable/current; old export retained; recoverable bytes reused once; transactional financial registration; restoration approval required for changed words/voice, sibling settings unchanged; manual versions preserved/outdated; invalid/missing bytes cannot replace current. Audio join quality/real speech mapping remains S5, actual MP4 validation S6.

## S8

Claim: coordinated DB/media snapshots encrypted to an independent local destination, with independently durable deletion authority and fail-closed reconciliation, support the <=24-hour recovery/purge procedure structurally.
Failure sought: inconsistent snapshot, plaintext backup, forgotten spend, lost deletion history, older-snapshot resurrection, interrupted backup extending purge deadline.
Minimum: SQLite backup API under local maintenance exclusion, copied immutable referenced media/hash manifest, authenticated AES-GCM encryption; local destination represents off-host storage; restore into empty storage. Controlled clock for seven-day restoration/expiry and next-cycle backup purge. Old and failed snapshots, missing/corrupt deletion authority, interrupted backup/deletion operations.
Pass: complete authenticated restore; tampered ciphertext fails; restored execution/spend remains disabled until reconciliation; current independently recoverable deletion journal reapplied before private access; seven-day cutoff exact; purged active and recoverable local backup content eliminated by next <=24-hour cycle even when new backup fails; missing journal fails closed. Snapshot-age >24 hours detected as failed recovery target, not hidden. Real off-host durability, vendor historical copies, scheduling/monitoring and full-sized timing remain unproven S9/operational gates.

## Reporting

Commands, case results, counts/timings, environment and source/plan hashes are stored in JSON and per-gate Markdown, without dumping huge logs into documents. PASS is a local experiment verdict with stated limits, not independent production acceptance. Failures are retained. Source-of-truth semantics will not be silently changed.
