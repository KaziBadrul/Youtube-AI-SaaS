# Private Alpha implementation execution contract

Planning baseline: **2026-10-05**, frozen architecture **v1**. This file plans core Private Alpha implementation only. **No implementation has begun; every task starts NOT_STARTED.** Task IDs become immutable when implementation begins; never renumber completed IDs. Add approved changes with new IDs and explicit dependencies, never silently change accepted requirements.

## Authority and scope

The baseline is [Architecture Freeze](docs/architecture/ARCHITECTURE_FREEZE.md) and its [audit bundle](docs/architecture/freeze/v1/README.md). S1–S9 are closed; S9 **PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY**, closure V14. Do not reopen spikes, create V15, rerun historical writers or edit freeze/evidence to ease a task.

Authority: current explicit owner instructions → accepted scoped ADRs with later explicit amendments → [Alpha specification](docs/ALPHA_PRODUCT_SPEC.md) → [architecture](docs/ARCHITECTURE.md), delegated [artifact](docs/ARTIFACT_MODEL.md), [job](docs/JOB_EXECUTION_MODEL.md) and [financial](docs/COST_MODEL.md) contracts, scoped [UX](docs/UX_FLOWS.md)/[design](docs/DESIGN.md) → [glossary](GLOSSARY.md)/[validation](docs/VALIDATION_PLAN.md) → dated [decisions](docs/PRODUCT_DECISIONS.md) → provisional [roadmap](docs/FEATURE_ROADMAP.md) → adopted feasibility evidence → historical experiments/prototypes/existing code. TASKS.md defines execution decomposition beneath those contracts, never new product authority. See [AGENTS.md](AGENTS.md).

Core: owned editable English landscape 16:9 image-based educational videos from topic or approved script; primary range 3–10 minutes, 1920×1080 MP4/30 fps; shorter pasted words preserved. Defaults: five-minute topic, Minimal Illustration, English, supported voice, captions/motion ON, music/manual review OFF. Include three curated presets, entitlement-aware Research, separate pasted factual checking/consent, images/replacement/history, B initial/B affected-segment narration corrections, local mapping/timing/captions, gentle motion/library music, scene-based corrections/reorder/delete/restoration, cancellation/recovery, protected exports and recoverable project lifecycle. English invitation quality remains future acceptance, not proven by spikes.

One codebase: Django server-rendered web/API plus focused browser interaction, a separate controlled Python production worker and coordinated maintenance on one persistent host. SQLite WAL/short durable transactions; immutable private host-local media. One active production request globally; serialize memory-heavy maintenance. No durable work in HTTP, broker, separate frontend/render deployment or new managed service. Suggested reversible layout: `config/`, one Django application namespace `alpha/` with typed `models/`, domain/services and subsystem modules, `templates/alpha/`, `static/alpha/`, categorized `tests/`. Foundation may refine names without changing boundaries or introducing a generic workflow engine.

## Execution and status authority

Exactly **ONE active implementation task**. Dependencies must independently PASS before activation. Codex receives only the active task, relevant frozen sections, relevant existing code and prior reviewer feedback. It reads requirements, implements that task only, runs its tests, reports changed files/results/blockers and stops. It must not advance TASKS.md, start another task, resolve material policy by guessing or silently fix unrelated work.

| Status | Meaning / authority |
| --- | --- |
| NOT_STARTED | No execution authorized; initial state for all tasks |
| IN_PROGRESS | Orchestrator assigns the single active task |
| REVIEW | Codex reports IMPLEMENTATION_COMPLETE; orchestrator requests independent review |
| PASS | Orchestrator records independent OpenCode PASS after required evidence |
| FAIL | Orchestrator records independent blocking reviewer findings; repair same task |
| BLOCKED | Orchestrator pauses for missing owner decision/evidence or exhausted repair loop |

**Codex cannot mark its own task PASS.** Implementation evidence is not acceptance. OpenCode independently reads cited requirements, inspects actual diff, runs/verifies required tests, checks regressions and every acceptance criterion. For UI it independently inspects screenshots/browser behavior; for finance/security it inspects negative paths and races. It evaluates the active task and caused regressions only, does not implement fixes or expand scope.

Reviewer output:

```text
VERDICT: PASS
```

or:

```text
VERDICT: FAIL
REASONS:
- Concrete blocking finding and violated requirement.
REQUIRED_FIXES:
- Exact correction within the active task.
BLOCKER: Optional exact missing decision/evidence.
```

Repair loop: implementation → review → FAIL → Codex repairs **SAME task** → independent rereview. Recommended maximum **3 automatic repair attempts after initial review**; then BLOCKED / HUMAN_REVIEW_REQUIRED and explicit human resumption. These are future execution contracts, not permission to build/configure an orchestrator now.

Before a task: clean or explicitly documented known baseline, including pre-existing unrelated changes. After reviewer PASS: one scoped Git checkpoint, e.g. `T013: implement private media registration`. Exclude unrelated files/secrets/generated assets. Failed attempts need not be committed. Codex does not self-accept or create a PASS checkpoint before review; checkpoint advancement belongs to the designated orchestrator/operator. This planning pass makes no commit.

## Blocked tasks and scope control

A material conflict preventing coherent planning is **SPEC_BLOCKED**; do not edit frozen contracts to bypass it. During execution report:

```text
TASK_BLOCKED
Missing decision/evidence: ...
Why required now: ...
Frozen documents/sections checked: ...
Smallest owner decision/evidence needed: ...
```

Orchestrator pauses. Ordinary reversible implementation choices may use the simplest documented option consistent with freeze. Gate tasks are real prerequisites, not blanks to be guessed: implementation can prepare disabled boundaries/fakes first, but capability activation and invitation readiness require the specified actual evidence. Absence of a live account, chosen vendor, upload/style limit or acoustic proof never converts UNKNOWN to zero/validated. Optional conditional tasks are not silently marked PASS: they remain NOT_STARTED until separately requested and are not dependencies of core readiness.

## Financial and provider safety

Active ceiling: **$40 USD per Asia/Dhaka calendar month**, total owner cash spend. Credits/entitlement/creator allowance/project authority cannot override it. Finite complete per-attempt bounds, current certificates, committed reservations and persisted attempt/fence identity precede every paid send. No DB transaction spans a provider call, FFmpeg or large media work. At most two safe automatic retries per logical operation, each independently admitted; manual retry cannot reset history. Unknown submission/billing retains liability, prohibits blind retry and cannot prove lane release. Failed paid output counts owner expense; valid delivered historical output consumes applicable allowance once. Local render/alignment/restore transforms consume no provider-generation allowance while infrastructure costs still count.

V14 planning reference, not production pricing/default caps: ~$24 host-class sensitivity (locally qualified **2 vCPU / 4 GiB**, host sizing closed unless failure) + $0.017182 capped backup storage/download exposure + $6.598836 conservative initial three-minute provider reservation + $9.383982 **required cash-coverage capacity** = $40. Those remaining dollars are not a generation allowance. Supported taxes/fees/FX/extras/reserve/current spending/holds/liabilities must fit. UNKNOWN required coverage blocks commitment. Conditional initial provider formula: topic `1.380532 + N*0.139264 + K*0.102400`, pasted candidate base `1.045479`; actual reviewed sentences N/coherent sources K and endpoint proofs required. Three-minute N≤36/K≤2 is useful reference; five-minute N≤60/K≤2 gives $9.941172 provider maximum with $6.041646 residual cash capacity; ten-minute fallback N≤120/K≤2 gives $18.297012 and exceeds nominal fixed envelope by $2.314194 before coverage. Block/replan/separately admit sufficient verified funding **within the active ceiling**; format support never grants affordability. No automatic budget amendment. Blanket three-attempt reservation is not initially affordable in that reference.

Topic preliminary images≈12/minute; once script exists use deterministic reviewed sentence count. Preserve earlier incurred work on revised scope. Preliminary credits=minutes/5; final post-script debit/correction conversion remains pending. Never adopt `credits = images / 60` or arbitrary stage percentages. UI credits AND USD in compact optional Details; Create Video directly authorizes bounded scope, without mandatory cost-review modal. Required changed-scope/text/translation/restoration consent remains explicit.

**Default for all implementation/review tests: ZERO external provider/API calls, network denied, ZERO paid spend, no free quota assumption.** Fake outcomes/receipts are labeled synthetic, never actual empirical proof. Gate/owner-validation tasks are not blanket live execution permission: any live request/remote operation requires separate explicit owner authorization plus persisted bounded authority and current account/endpoint proof. No task automatically purchases credits, creates paid accounts, selects/provisions hosting or deploys. Owner-provided separately authorized operational environments are prerequisites to actual remote readiness evidence. Do not claim provider readiness from passing fakes.

## Test and review strategy

| Category | Required behavioral focus |
| --- | --- |
| Unit | Exact money/time conversions, bounded parsers, pure helpers |
| Domain / contract | Typed versions, projections, invalidation/preservation, consent and configuration |
| Database | Constraints, migrations, WAL/CAS races, rollback and durability |
| Integration | Fake providers through admission → registration/accounting and current selection |
| Worker / recovery | Global lane, fences, crash windows, restart, unknown outcomes and process cessation |
| Security | Sessions/CSRF, cross-user resources/ranges, uploads/paths, owner-only authority and lock bypass |
| Financial | Shared/project/creator limits, reservations, billed failure, uncertainty, replay and scope expansion |
| Media / render | Hash/decode/range coverage, continuous narration, caption shaping, frame order, effects and invalid outputs |
| UI | Desktop/mobile themes, concrete layout, keyboard/focus, contrast/reflow, state truth and reduced motion |
| End-to-end | Core fake journeys, selective correction, interruption, deletion/restore and final regression |
| Manual / owner | Acoustic review, visual screenshot review, permitted asset evidence, real projects and remote operational verification |

T003 establishes executable standard commands for these categories and full regression. Each later task adds required tests to its listed suite(s) and runs affected regression; never fabricate commands before scaffolding exists. Live test suite must be separate, opt-in, disabled by default and separately authorized. Foundation and test infrastructure establish reproducible dependencies; no installation occurs during this planning pass. Fakes first; later activation certificates permit only proven scope.

UI review gates are concrete: warm creation/quiet dark workspace roles, composer dominance, no global dashboard sidebar, desktop scene/preview/inspector, stacked mobile corrections, actual versus history media clear, contrast 4.5:1 normal text and applicable 3:1 controls/large text, keyboard focus/consent, no horizontal reflow loss, reduced motion, no gradients/glow/glass/pill-card repetition/fake progress. Compare accepted references, not an invented design direction. Major UI tasks cannot PASS on functional tests alone.

## Phases and task contracts

All listed filenames are expected boundaries, not a mandate to duplicate domain services. Gate evidence records may be operational configuration/tests rather than application feature code. Requirements, acceptance criteria and tests in each task are cumulative with this header's safety contracts. Out-of-scope boundaries override convenience. Source citations name exact existing headings.


## Phase 1: Foundation and design

### T001: Establish the Django application and process boundaries

Status: NOT_STARTED

Phase: 1 — Foundation and design

Objective: Establish the Django application and process boundaries within the frozen boundaries.

Why: Satisfies the frozen Runtime shape contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- None

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Runtime shape**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Scope and frozen boundaries**

Likely Files:
- config/
- alpha/
- templates/alpha/
- static/alpha/
- tests/
- dependency manifest

Requirements:
- Create one Python codebase with Django configuration and domain/service boundaries under alpha; separate web, worker and maintenance entry points.
- Provide owner-local and invited-Alpha configuration profiles, secret loading and disabled-by-default provider settings; no credentials in source.
- Document reproducible dependency and test commands; do not add a frontend deployment, broker, Redis or durable work in HTTP handlers.

Acceptance Criteria:
- Web startup and configuration validation run without provider credentials or import-time network calls.
- Worker and maintenance entry points are separate and initially refuse unconfigured execution; production behavior is not simulated in HTTP.

Required Automated Tests:
- Configuration profiles, missing secrets and unknown settings.
- Import/startup network prohibition and separate process entry points.
- Django system checks and smoke request.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Establish safe session/CSRF settings and secret redaction boundaries; do not create public signup.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Domain features, production scheduler, orchestrator and hosting configuration.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T002: Implement SQLite durability and short-transaction primitives

Status: NOT_STARTED

Phase: 1 — Foundation and design

Objective: Implement SQLite durability and short-transaction primitives within the frozen boundaries.

Why: Satisfies the frozen Relational state contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T001

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Relational state**

Likely Files:
- config/database settings
- alpha/persistence/
- tests/database/

Requirements:
- Use local SQLite WAL, foreign keys, durable synchronous settings and bounded busy handling; migrations must establish required constraints.
- Provide short transactional compare-and-swap/exclusion helpers compatible with SQLite, not assumed row locks.
- Keep network calls, FFmpeg and large filesystem work outside database transactions.

Acceptance Criteria:
- Independent connections reject conflicting updates without double transition and retain consistent foreign keys.
- Interrupted transactions roll back; committed state survives reconnect; contention fails visibly within configured bounds.

Required Automated Tests:
- Multiprocess CAS/unique-constraint and concurrent writer tests inspired by S2.
- Rollback, integrity and foreign-key checks across reopen.
- Instrumented test proves external callbacks run outside transactions.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
NONE beyond integrity; helpers must not bypass service-level authorization.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
PostgreSQL migration, arbitrary-scale benchmarking or reopening S2.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T003: Establish offline test suites and fixture discipline

Status: NOT_STARTED

Phase: 1 — Foundation and design

Objective: Establish offline test suites and fixture discipline within the frozen boundaries.

Why: Satisfies the frozen Scope and frozen boundaries contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T001
- T002

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Scope and frozen boundaries**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**

Likely Files:
- tests/
- test configuration
- developer test-command documentation

Requirements:
- Establish named unit/domain, database, integration, financial, worker/recovery, security, media/render, UI and full-regression command categories.
- Deny external network in ordinary suites; provide deterministic fake clocks, provider responses, process controls and isolated databases/media roots.
- Reuse historical assets read-only or copied to disposable workspaces; hash original fixtures and forbid accidental provider/model downloads.

Acceptance Criteria:
- The documented offline suite runs without keys and deliberately fails an outbound network attempt.
- Temporary paths are isolated; a fixture modification is detected; full regression includes relevant suite categories.

Required Automated Tests:
- Network trap including SDK initialization and model fetch.
- Fixture hash preservation and cleanup on failed tests.
- Fake clock/restart/process fixtures and command-discovery smoke tests.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Tests never consume real secrets or expose private source artifacts.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Paid/live tests, installation during this planning pass or historical witness reruns.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T004: Implement Warm Creator tokens, themes and accessible primitives

Status: NOT_STARTED

Phase: 1 — Foundation and design

Objective: Implement Warm Creator tokens, themes and accessible primitives within the frozen boundaries.

Why: Satisfies the frozen Principles and agreed direction contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T001
- T003

Source of Truth:
- [docs/DESIGN.md](docs/DESIGN.md), section **Principles and agreed direction**
- [docs/DESIGN.md](docs/DESIGN.md), section **Theme and semantic colors**
- [docs/DESIGN.md](docs/DESIGN.md), section **Accessibility baseline**

Likely Files:
- static/alpha/design.css
- templates/alpha/components/
- tests/ui/

Requirements:
- Establish a restrained token system for cream/forest/olive creation and near-black subtle-plum workspace, readable typography, spacing, moderate radii and surfaces.
- Implement persisted Light/Dark/System, visible focus, semantic controls, accessible dialogs/disclosures and reduced-motion behavior.
- Use server-rendered templates plus focused browser interaction; reference accepted Direction C and annotated design images without copying prototype orchestration.

Acceptance Criteria:
- Both themes meet frozen text/control contrast rules and System responds without losing input, focus or selection.
- Keyboard dialogs restore focus; reduced motion removes nonessential movement; no generic dashboard gradients/glow/pill-card treatment.

Required Automated Tests:
- Theme preference persistence/system changes.
- Keyboard focus/dialog/disclosure and reduced-motion tests.
- Contrast checks and desktop/mobile component screenshots.

Manual Verification:
Reviewer inspects both-theme screenshots against DESIGN.md and Direction C; verifies restrained surfaces and legibility.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
No client theme setting changes authorization.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Full component marketplace, new visual direction or large application screens.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 2: Typed persistence

### T005: Persist projects, original input and lifecycle settings

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Persist projects, original input and lifecycle settings within the frozen boundaries.

Why: Satisfies the frozen Domain relationships contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T002
- T003

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Domain relationships**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**

Likely Files:
- alpha/models/projects.py
- alpha/services/projects.py
- alpha/migrations/
- tests/domain/projects/

Requirements:
- Model owned Project and immutable Original Input separately, with input interpretation, requested duration/language, defaults and lifecycle state.
- Support create/rename/reopen and version-aware autosave service contracts; persist defaults of five-minute topic, Minimal Illustration, English, captions/motion on and music off.
- Represent deletion/retention metadata, a persisted content-mutation guard and storage attribution without deleting media; expose a guard check for later render locking and implement deletion procedures in later tasks.

Acceptance Criteria:
- Original input remains byte/word faithful when current content/settings change; unrelated projects stay isolated.
- Repeated create tokens do not duplicate projects and stale autosave cannot overwrite a newer accepted edit.

Required Automated Tests:
- Create/defaults/rename/reopen and original-versus-current data separation.
- Concurrent autosave, revision conflict and rollback.
- Lifecycle state constraints and cross-project access rejection.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Public signup, project duplication/archive and deletion execution.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T006: Persist script versions and stable scene projections

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Persist script versions and stable scene projections within the frozen boundaries.

Why: Satisfies the frozen Domain relationships contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T005

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Domain relationships**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Typed content with a shared version envelope**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Correction workflow**

Likely Files:
- alpha/models/scripts.py
- alpha/models/scenes.py
- alpha/services/script_projection.py
- alpha/migrations/
- tests/domain/scripts/

Requirements:
- Represent Script versions, approved/current text and ordered Scenes with stable identifiers and source spans; distinguish narration text, visual description and generation prompt.
- Maintain current script projection from active scene order/narration while Original Input remains immutable.
- Provide atomic persistence primitives for accepted text revisions and scene ordering; do not infer scenes from filenames or line numbers.

Acceptance Criteria:
- Reopened projects reproduce exact accepted words/order; scene identity survives reordering independently of index.
- Projection updates commit atomically with scene text and reject mismatched source versions.

Required Automated Tests:
- Projection and source-span round trips including Unicode and punctuation.
- Stable IDs after order changes and persistence reload.
- Conflicting text/projection transactions and original-input preservation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Sentence policy, provider scene planning, arbitrary scene addition/duplication and user-facing reorder controls.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T007: Implement deterministic sentence segmentation and scope review

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Implement deterministic sentence segmentation and scope review within the frozen boundaries.

Why: Satisfies the frozen Owner-accepted staged estimation and sentence-driven image scope contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T006

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted staged estimation and sentence-driven image scope**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**

Likely Files:
- alpha/scripts/segmentation.py
- tests/domain/segmentation/

Requirements:
- Define a versioned deterministic local rule producing exact script spans/count; reuse appropriate witness cases but do not use LLM counting.
- Cover abbreviations, decimals, quotations, ellipses, Unicode punctuation and pathological one-word/many-sentence scripts; ambiguous scope requires explicit review/rejection instead of silent guessing.
- Once approved initial script exists, one planned generated image corresponds to each counted sentence; stable correction scenes are not automatically re-created after every edit.

Acceptance Criteria:
- Same script/version yields identical spans/count and preserves all approved characters.
- Known pasted/generated script reports its exact sentence-derived image scope, without using a topic-density heuristic; downstream scope admission tests prove that enlarged count cannot grant authority.

Required Automated Tests:
- 3/5/10 heuristics versus known N and deterministic repetitions.
- Exact punctuation/Unicode spans and documented ambiguity fixtures.
- 47/214/pathological count, review-required handling and no LLM calls.

Manual Verification:
Reviewer checks the documented rule/edge-case policy; unresolved material segmentation behavior is TASK_BLOCKED, not guessed.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Universal sentence cap, arbitrary new scenes or final credit conversion.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T008: Persist typed artifact versions and immutable provenance

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Persist typed artifact versions and immutable provenance within the frozen boundaries.

Why: Satisfies the frozen Typed content with a shared version envelope contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T006

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Typed content with a shared version envelope**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Provenance, compatibility and staleness**

Likely Files:
- alpha/models/artifacts.py
- alpha/migrations/
- tests/domain/artifacts/

Requirements:
- Use typed image, audio, timing, caption and related content payloads with a shared immutable version/provenance envelope; binary media stays outside SQLite.
- Record exact source-version references, model/configuration, hashes, validation, creation metadata and generation outcome separately.
- Keep Valid, Selected, Compatible/Outdated and Review Needed as independent axes; failed attempts cannot overwrite selected good content.

Acceptance Criteria:
- Domain constraints reject impossible cross-owner/source references and mutation of registered version content.
- A failed newer generation leaves prior valid selection and its provenance intact.

Required Automated Tests:
- Immutability and typed-payload validation.
- Independent state axes and failed-attempt preservation.
- Source-version/hash/config round trips and incompatible foreign-key rejection.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Universal arbitrary-JSON domain table, selection policy and invalidation execution.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T009: Persist research evidence, factual findings and proposals

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Persist research evidence, factual findings and proposals within the frozen boundaries.

Why: Satisfies the frozen Generation and factual handling contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T006
- T008

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Typed content with a shared version envelope**

Likely Files:
- alpha/models/research.py
- alpha/migrations/
- tests/domain/research/

Requirements:
- Model Research Result, source evidence, Factual Warning and proposed corrections tied to exact script/input versions.
- Separate retrieval time from publication time, private warnings from export content, and proposed words from approved script text.
- Represent incomplete/failed research and factual check provenance without implying success or changing approved words.

Acceptance Criteria:
- Proposal persistence never mutates current script and can retain partial sources after failure.
- Warnings and evidence remain associated with the examined version and cannot leak across projects.

Required Automated Tests:
- Partial evidence, no-source and unavailable states.
- Version-bound proposal records and original-word preservation.
- Private serialization excludes warnings from render/export payloads.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Actual search, model checking and correction acceptance.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T010: Persist coherent narration, mappings and assembly records

Status: NOT_STARTED

Phase: 2 — Typed persistence

Objective: Persist coherent narration, mappings and assembly records within the frozen boundaries.

Why: Satisfies the frozen Narration generation granularity — frozen B policy contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T006
- T008

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Narration generation granularity — frozen B policy**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Segment, mapping and assembly contracts**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Typed content with a shared version envelope**

Likely Files:
- alpha/models/narration.py
- alpha/migrations/
- tests/domain/narration/

Requirements:
- Model Narration Segment memberships, immutable Source Audio versions, Scene Audio Mappings and derived project assembly as distinct typed records.
- Pin spoken text/configuration/source hashes; store speech ranges, visual intervals and extraction/join ranges separately.
- Represent effective voice/delivery overrides, mapping method/confidence/review and accepted variation records without overwriting approved script.

Acceptance Criteria:
- Multiple scenes can share one coherent source without independent scene speech files.
- Mappings cannot reference another source version or confuse a visual transition with a validated audio extraction endpoint.

Required Automated Tests:
- Multi-scene memberships and source-version mismatches.
- Range/interval constraints and effective-config inheritance.
- Accepted variation remains separate from approved words and ASR.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
TTS generation, alignment algorithms or assuming acoustic boundaries are validated.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 3: Identity and private media

### T011: Implement invited identity and secure sessions

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Implement invited identity and secure sessions within the frozen boundaries.

Why: Satisfies the frozen Authentication and isolation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T005
- T004

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Authentication and isolation**

Likely Files:
- alpha/accounts/
- templates/alpha/auth/
- tests/security/auth/

Requirements:
- Use Django identity/session infrastructure with operator-provisioned invited accounts and sign-in/sign-out.
- Enforce session/CSRF requirements and least-privilege owner/admin access in local versus invited profiles.
- Provide no public registration or external authentication provider; redact secrets in errors.

Acceptance Criteria:
- Invited users authenticate; anonymous/private routes redirect or reject consistently; public signup does not exist.
- Cross-site unsafe requests are rejected and sign-out invalidates access as expected.

Required Automated Tests:
- Session lifecycle, anonymous access and inactive account tests.
- CSRF unsafe-request rejection and owner/admin role negatives.
- Secret-safe error responses and cookie/profile configuration.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Social login, billing identities or sending invitations.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T012: Enforce resource ownership and persisted feature entitlements

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Enforce resource ownership and persisted feature entitlements within the frozen boundaries.

Why: Satisfies the frozen Authentication and isolation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T011
- T008
- T009
- T010

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Authentication and isolation**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner decision — Research entitlement and topic discovery, 2026-10-05**

Likely Files:
- alpha/authorization.py
- alpha/models/entitlements.py
- alpha/migrations/
- tests/security/ownership/

Requirements:
- Centralize server-side ownership for project, artifact, operation, render/export and media lookup; workers resolve owner from persisted state.
- Persist feature eligibility: Research/Topic/Custom only 3/week and 1/day; Expert only 1/day; lower tier none.
- Treat entitlement separately from USD authority; tests may seed synthetic assignments but production assignment remains owner-controlled.

Acceptance Criteria:
- Guessed IDs, client plan names and hidden-route calls cannot grant access or entitlement.
- The exact four-feature matrix passes and no suggestion-generation product routes are added.

Required Automated Tests:
- Two-user negative object access tests.
- Full entitlement matrix including forged client plan and absent state.
- Privileged worker lookup cannot accept a client-supplied owner override.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Commercial billing, plan prices/quotas or implementation of any suggestion feature.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T013: Implement private staging and immutable media registration

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Implement private staging and immutable media registration within the frozen boundaries.

Why: Satisfies the frozen Media and storage contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T008
- T012

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**

Likely Files:
- alpha/media/storage.py
- alpha/media/registration.py
- tests/security/media/

Requirements:
- Use private host-local storage, opaque logical keys and server-generated staging identifiers; reject user-controlled filesystem paths.
- Validate/hash then durably install immutable bytes before transactional registration; preserve attempt-to-file recovery metadata.
- Unregistered files remain inaccessible and not successful artifacts; exact input and owner references accompany registration.

Acceptance Criteria:
- Path traversal, symlinks and forged keys cannot escape the private root.
- A crash between install and registration retains recoverable bytes without exposing a successful artifact.

Required Automated Tests:
- Traversal, symlink, key forgery and ownership negatives.
- Duplicate registration/hash mismatch and partial-write failures.
- Durable install/registration crash-window recovery fixtures.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Quarantine incomplete files; retain paid-response identity for later persistence recovery, never regenerate merely because save failed.

Out of Scope:
Public filesystem serving, arbitrary URL imports and provider generation.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T014: Serve protected image/audio/export media including ranges

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Serve protected image/audio/export media including ranges within the frozen boundaries.

Why: Satisfies the frozen Authentication and isolation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T013
- T011

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Authentication and isolation**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**

Likely Files:
- alpha/web/media.py
- tests/security/media_delivery/

Requirements:
- Implement protected logical-key resolution and ownership checks on every full and ranged request.
- Support required audio/video range semantics, content types and caching without a public media directory route.
- Reject deleted/unregistered/inaccessible content and keep error messages from disclosing other creators metadata.

Acceptance Criteria:
- Authorized range playback works; unauthorized full, range and conditional requests never return private bytes.
- Traversal and stale/deleted media references fail safely; no private storage path appears in responses.

Required Automated Tests:
- Valid/suffix/invalid/unsatisfiable range requests.
- Cross-owner/anonymous/deleted/unregistered access.
- Conditional request, content length/type and cache privacy checks.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Public sharing, arbitrary downloadable server files or signed universal media links.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T015: Define and validate the image-upload capability configuration

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Define and validate the image-upload capability configuration within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T013

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**

Likely Files:
- alpha/media/upload_policy.py
- tests/security/upload_policy/
- operational capability record

Requirements:
- Represent required image allowlist, byte/dimension/pixel/decode-resource limits and approval/provenance as configuration, initially absent/disabled.
- Require an explicit supported operational policy before replacement upload is enabled; do not guess owner-sensitive limits in implementation.
- Validate policy consistency and expose actual configured limits; synthetic limits in tests are labeled fixtures.

Acceptance Criteria:
- Unset, contradictory or unsupported upload bounds disable upload before accepting bytes.
- A reviewed owner policy can enable only image replacement, never audio/video/remote URL ingestion.

Required Automated Tests:
- Missing/invalid/expired policy fails closed.
- Fixture limits at boundary and over boundary.
- Allowed feature scope excludes audio/video and URL imports.

Manual Verification:
Owner supplies/approves material operational limits; reviewer checks evidence. If unavailable report TASK_BLOCKED; do not invent numerical limits.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Choosing limits from convenience, handling actual uploads or expanding media scope.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T016: Implement retained storage accounting and byte reservations

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Implement retained storage accounting and byte reservations within the frozen boundaries.

Why: Satisfies the frozen Media and storage contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T013
- T005

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Current S9 planning envelope**

Likely Files:
- alpha/storage/accounting.py
- alpha/models/storage.py
- alpha/migrations/
- tests/domain/storage/

Requirements:
- Account current/prior artifacts, retained deleted assets, exports, metadata where material and staging/scratch commitments without double counting files.
- Require owner-configured capacity before new asset creation; atomically reserve conservative bytes and reconcile actual allocation.
- Overflow or unknown required space blocks creation; never prune versions, delete exports or provision paid storage automatically.

Acceptance Criteria:
- Concurrent reservations cannot exceed the configured cap; shared references do not count the same bytes twice.
- Old versions/deleted retention count; released scratch does not erase retained source usage.

Required Automated Tests:
- Concurrent reservations, missing cap and insufficient disk scenarios.
- Version/deleted/export/staging versus scratch accounting.
- Crash/reservation recovery and duplicate reference tests.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Pause creation visibly while preserving existing files and reservations until reconciled.

Out of Scope:
Final cap selection, retention purge and external storage provisioning.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T017: Implement validated image replacement

Status: NOT_STARTED

Phase: 3 — Identity and private media

Objective: Implement validated image replacement within the frozen boundaries.

Why: Satisfies the frozen Image regeneration and replacement contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T015
- T016
- T014

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**

Likely Files:
- alpha/media/uploads.py
- alpha/services/image_replacement.py
- tests/security/uploads/

Requirements:
- Stage approved image uploads under server keys and enforce configured limits using decoded bytes, not extension or client MIME alone.
- Register immutable validated image versions and reject corrupt/decompression/resource-exhausting files.
- Expose replacement service preserving narration/timing; selection/invalidation hooks are integrated in the artifact-contract task.

Acceptance Criteria:
- Only a validated in-policy image is registerable; failures preserve the selected image and do not consume generation allowance.
- Cross-owner replacements and replacements against an active persisted project content guard are rejected; T036 and T070 integrate the complete artifact/render lock lifecycle.

Required Automated Tests:
- Corrupt image, MIME mismatch, excessive dimensions/bytes and decode-resource fixtures.
- Cross-owner replacement and duplicate-submit behavior.
- Prior version preservation and storage hold release on confirmed local failure.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Image-generation calls, arbitrary audio/video upload and UI controls.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 4: Financial authority

### T018: Implement exact monetary units and monthly financial events

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Implement exact monetary units and monthly financial events within the frozen boundaries.

Why: Satisfies the frozen Distinct concepts contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T002
- T012

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Distinct concepts**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Month boundary and budget revisions**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Current S9 planning envelope**

Likely Files:
- alpha/finance/money.py
- alpha/models/finance.py
- alpha/migrations/
- tests/financial/ledger/

Requirements:
- Use integer USD subunits and exact decimal conversion with conservative liability rounding, never binary floats for authority.
- Create append-only financial events with idempotent transactionally maintained balances and separate spend, holds, liabilities and successful-output allowance.
- Use a configurable active $40 USD Asia/Dhaka calendar-month ceiling; preserve invoice currency/basis/certainty and auditable amendments.

Acceptance Criteria:
- Month boundary does not erase old liabilities or spending history; lowering a cap blocks further admission without rewriting charges.
- Repeated event identity cannot double count and unknown cost never becomes zero.

Required Automated Tests:
- Exact arithmetic/rounding and Dhaka calendar rollover.
- Event idempotency, correction entries and cap revision.
- Old liabilities and invoice-period reconciliation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Implements financial representation only; no external calls, fabricated receipts or credit exchange rate.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Commercial credits/prices, actual payments and provider activation.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T019: Implement project/creator authority and cash-coverage controls

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Implement project/creator authority and cash-coverage controls within the frozen boundaries.

Why: Satisfies the frozen Plan and admission contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T018
- T005

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Plan and admission**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Current S9 planning envelope**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Distinct concepts**

Likely Files:
- alpha/finance/authority.py
- alpha/models/authorizations.py
- tests/financial/authority/

Requirements:
- Keep shared total budget, creator successful-output USD allowance, project/request scope authorization and entitlement distinct.
- Reserve supported recurring obligations, taxes/fees/FX/extras and configured owner reserve before generation capacity; missing coverage fails closed.
- Record actor, input/config signatures, ceiling and period for approval; credits and client balances never authorize spending.

Acceptance Criteria:
- Creator/project grants cannot exceed shared authority; missing owner coverage prevents paid commitments.
- Historical V14 sensitivities are labeled planning, not permanent prices, approved reserves or tester allocations.

Required Automated Tests:
- Forged credits/client allowance and cross-owner authorization.
- Unknown coverage, changed obligations and negative residual.
- Period/version-bound grants and auditable owner revision.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Implements internal USD authority; fixture allocations only. Final allowances and reserve percentages remain undecided.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Choosing tester amounts, vendors, reserve percentages or final credit formula.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T020: Implement atomic attempt and allowance reservations

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Implement atomic attempt and allowance reservations within the frozen boundaries.

Why: Satisfies the frozen Plan and admission contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T019

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Plan and admission**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Completion and failed attempts**

Likely Files:
- alpha/finance/reservations.py
- tests/financial/reservations/

Requirements:
- Atomically validate current request/project/creator/shared authority and commit maximum attempt exposure before any submission.
- Hold owner financial liability separately from possible successful-output allowance; include committed infrastructure obligations.
- Provide idempotent reserve/release/conversion operations and conservative concurrency handling; no database transaction spans external execution.

Acceptance Criteria:
- Two concurrent requests competing for the last capacity cannot both be admitted.
- No permitted submission identity exists without a persisted sufficiently funded reservation; stale quote/configuration is rejected.

Required Automated Tests:
- Multiprocess competing reservation and duplicate-click tests.
- Missing/insufficient/stale scope or rate basis.
- Release only unsubmitted canceled work and ensure callback outside transaction.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Critical admission boundary; fake providers only.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Database/reservation failure launches no paid work and retains existing holds.

Out of Scope:
Provider transport and probabilistic spending decisions.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T021: Implement spend settlement and unresolved-liability retention

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Implement spend settlement and unresolved-liability retention within the frozen boundaries.

Why: Satisfies the frozen Completion and failed attempts contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T020
- T008

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Completion and failed attempts**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Month boundary and budget revisions**

Likely Files:
- alpha/finance/settlement.py
- tests/financial/settlement/

Requirements:
- Reconcile authoritative charges exactly once, retaining maximum exposure when billing/submission outcome is unknown.
- Charge valid delivered outputs, including history-only results, once against applicable allowance; unusable failed output releases allowance hold but retains paid owner expense.
- Keep successful response/save failure recoverable; cancellation, crash, lease expiry and month rollover never imply a refund or zero billing.

Acceptance Criteria:
- Failed paid output is not selectable and its owner spend remains accounted; late valid delivery has one allowance event.
- Restart retains unresolved liability and no balance double-counts the same settled charge plus live hold.

Required Automated Tests:
- Known success/failure/unknown billing and allowance distinctions.
- Crash between success/install/registration/settlement and replay.
- Cancellation/month/restart retention and late history-only delivery.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Implements financial certainty and reconciliation; no invented provider receipt or failure rate.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Automatic optimistic settlement or wiping old liabilities.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T022: Implement versioned financial manifests and rate/cap evidence

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Implement versioned financial manifests and rate/cap evidence within the frozen boundaries.

Why: Satisfies the frozen Creator estimates and scope contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T019
- T020
- T006
- T007

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Creator estimates and scope**
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md), section **Provider financial bound used in the planning proof**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**

Likely Files:
- alpha/finance/manifests.py
- alpha/finance/rates.py
- tests/financial/manifests/

Requirements:
- Build deterministic per-operation expected-versus-maximum manifests with all billable dimensions, exact rate evidence and admitted attempt/request bounds.
- Topic preliminary scope is approximately 12 images/minute with credits minutes/5; known script image scope is deterministic sentences; narration uses actual coherent groups.
- Keep research entitlement paths and pasted-script differences, consumed/remaining/projected amounts and UNKNOWN components explicit; conditional V14 arithmetic is a fixture, not a live certificate.

Acceptance Criteria:
- 3/5/10-minute heuristic produces 36/60/120 images and 0.6/1/2 preliminary credits; no images/60 debit formula exists.
- Expired/unsupported rates or incomplete exposure block paid eligibility rather than generating a misleading all-in total.

Required Automated Tests:
- V14 conditional topic/pasted formula and exact maximum arithmetic.
- Unknown expected components, separate retry exposure and expired rate/cap evidence.
- Optional discovery exclusion and consumed plus replacement remaining estimate.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
No provider calls; current configured verified tariff required for live eligibility. Captured sensitivities never activate models.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Final credit debit, choosing rates/models or measuring expected failure frequencies.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T023: Enforce post-script scope recalculation and renewed admission

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Enforce post-script scope recalculation and renewed admission within the frozen boundaries.

Why: Satisfies the frozen Owner-accepted staged estimation and sentence-driven image scope contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T022
- T021
- T006
- T007

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted staged estimation and sentence-driven image scope**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Creator estimates and scope**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Plan and admission**

Likely Files:
- alpha/finance/scope_changes.py
- tests/financial/scope_changes/

Requirements:
- Replace topic image heuristic with actual reviewed script sentences and actual B group scope before further paid work.
- Compare scope/version/configuration against recorded authorization and shared/project/creator capacity; insufficient or changed authority pauses affected work.
- Preserve consumed research/script operations and compatible results; model-generated additional scenes cannot expand authority.

Acceptance Criteria:
- A 60-to-214 image fixture reports changed scope and submits no image work without refreshed sufficient authority.
- A 47-sentence update retains prior valid consumption and cannot double count old and replacement quotes.

Required Automated Tests:
- 3/5/10 preliminary versus known pasted/generated counts.
- 47 and 214 sentence fixtures with retained spent/holds.
- Concurrent edits and refreshed approval, no arbitrary materiality threshold.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Controls deterministic financial scope; no AI-created authority.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Final materiality policy, automatic shortening or expanding approved scene count.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T024: Verify adversarial financial authority with persistent fake providers

Status: NOT_STARTED

Phase: 4 — Financial authority

Objective: Verify adversarial financial authority with persistent fake providers within the frozen boundaries.

Why: Satisfies the frozen Fake-provider financial witness contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T023

Source of Truth:
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v13.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v13.md), section **Fake-provider financial witness**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Completion and failed attempts**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Retries**

Likely Files:
- tests/financial/adversarial/
- offline financial witness fixtures

Requirements:
- Port behavior contracts from S9 V13/V14 without copying witness code wholesale; use durable SQLite and fake outcomes.
- Exercise normal success; before-send failure/timeout; possible-acceptance timeout; 429; 5xx; corrupt/invalid output; crash before registration and after registration; confirmed nonbillable retry; unknown billing/restart; exhausted attempts; near shared/creator cap; expanded scope; stale duplicate worker; cancellation and late canceled success.
- Prove no reservation bypass, finite attempts, exactly-once spend/delivery, persistent uncertainty and no free-quota assumption.

Acceptance Criteria:
- All listed scenarios preserve budget and successful-output allowance invariants after crash/replay.
- Expected costs remain distinct from maximum liability; unknown outcomes forbid blind retry.

Required Automated Tests:
- Durable fake-provider scenario matrix and randomized event-order invariants.
- Concurrent reservation/settlement and worker-fence negatives.
- Month/restore/cancel replay with no external network.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Financial safety proof using fake providers only; passing is implementation evidence, not acceptance by Codex.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
S9 reopening, empirical rates or live provider validation.

Reviewer Notes:
Independently run the witness and inspect adversarial transitions, including allowance versus owner spend and pending liability.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 5: Durable production worker

### T025: Persist jobs, scoped operations, concrete attempts and progress

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Persist jobs, scoped operations, concrete attempts and progress within the frozen boundaries.

Why: Satisfies the frozen Job, operation and attempt contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T021
- T005
- T008

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Job, operation and attempt**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Job state machine**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Minimum progress and history**

Likely Files:
- alpha/models/jobs.py
- alpha/migrations/
- alpha/jobs/states.py
- tests/domain/jobs/

Requirements:
- Model Generation Job as authorized request, Operation as bounded logical step and Attempt as concrete execution with immutable starting signatures.
- Persist queue/execution/result certainty, cancellation intent, progress checkpoints and last outcomes independently of artifact selection.
- Include request/model/config identities, transport timestamps, usage certainty and failure classification; avoid private text in routine logs.

Acceptance Criteria:
- Jobs expose truthful waiting/queued/running/partial/failed/unknown/canceled/completed states after reopen.
- One attempt result cannot count as another operation or imply export readiness before validation.

Required Automated Tests:
- State transition table and invalid transitions.
- Independent operation/attempt outcomes and progress recovery.
- Redacted serialization and owner-filtered status.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Worker loop, queue acquisition and provider submission.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T026: Implement the relational queue and one global production lane

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Implement the relational queue and one global production lane within the frozen boundaries.

Why: Satisfies the frozen One active production lane contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T025
- T020

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **One active production lane**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**

Likely Files:
- alpha/jobs/queue.py
- alpha/models/lane.py
- tests/worker/queue/

Requirements:
- Atomically claim one eligible production request globally; include generation, checks, regeneration, alignment and render workloads.
- Waiting for approval/budget releases the lane only after active provider/process cessation is confirmed.
- Persist queue order and waiting reasons; unknown remote execution retains exclusion rather than being treated as stopped.

Acceptance Criteria:
- Concurrent claimants produce one lane owner and blocked never-started requests do not occupy the lane.
- Heartbeat expiry/timeout alone never authorizes another executing request.

Required Automated Tests:
- Multiprocess queue claim and crash replay.
- Waiting/release versus unknown execution matrix.
- Queue fairness, cancellation and failed claim atomicity.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Keep unresolved execution guarded and visible; no optimistic lane release.

Out of Scope:
Parallel generation, external queue services or distributed scheduling.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T027: Implement worker supervision, ownership and stale-worker fencing

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Implement worker supervision, ownership and stale-worker fencing within the frozen boundaries.

Why: Satisfies the frozen Idempotency and checkpoints contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T026
- T002

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Failure matrix**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Runtime shape**

Likely Files:
- alpha/jobs/ownership.py
- alpha/management/commands/run_worker.py
- tests/worker/fencing/

Requirements:
- Use controlled single-host worker startup exclusion and persisted fencing/generation tokens at all authoritative writes/submissions.
- Record process/boot/start identity for child control; require confirmed old-process cessation before replacement execution.
- Use bounded progress/health reporting without treating a missed heartbeat as permission to duplicate paid work.

Acceptance Criteria:
- Stale workers cannot start a reserved attempt, publish selection or release a new owner lock.
- Restart discovers unresolved execution and pauses safely instead of issuing replacement calls.

Required Automated Tests:
- Double worker startup and stale fence races.
- PID reuse/boot identity and process disappearance.
- Crash ownership recovery with active versus stopped children.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Protects concrete submission authority; fake external execution only.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Multi-host leases, orchestrator construction or host sizing experiments.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T028: Implement transactional attempt preparation and operation dispatch

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Implement transactional attempt preparation and operation dispatch within the frozen boundaries.

Why: Satisfies the frozen Plan and admission contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T027
- T024
- T025

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Plan and admission**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Job, operation and attempt**

Likely Files:
- alpha/jobs/executor.py
- alpha/jobs/handlers.py
- tests/worker/executor/

Requirements:
- Revalidate ownership, scope, cancellation, provider enablement, storage and financial authority before committing an attempt identity/reservation.
- Commit before dispatching outside a database transaction; provider/local handlers have narrow typed inputs/results.
- Persist successful data then validate/register/settle once; input/config changes make valid late results history-only.

Acceptance Criteria:
- The dispatch spy sees no call without current persisted reservation and fence.
- Relevant queued edits cause refreshed authority; unrelated edits do not discard valid scoped work.

Required Automated Tests:
- Before-send crash/DB failure and no-submit guarantees.
- Dispatch outside transactions, stale/canceled signatures.
- Current-versus-historical result and idempotent dispatch replay.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Paid dispatcher is fail-closed; no actual external submission during implementation tests.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Provider-specific SDK logic and generic workflow engines.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T029: Implement finite retries and cancellation admission intent

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Implement finite retries and cancellation admission intent within the frozen boundaries.

Why: Satisfies the frozen Retry and cancellation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T028

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Retry and cancellation**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Retries**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Job state machine**

Likely Files:
- alpha/jobs/retries.py
- alpha/jobs/cancellation.py
- tests/worker/retries/

Requirements:
- Persist at most two automatic retries per logical operation across restarts, individually reserved and only for evidenced safe outcomes.
- Record cancellation intent atomically, cancel never-started queued work and stop admission of further steps.
- Classify 429/5xx/timeout by submission/billing certainty rather than HTTP code alone; manual retry preserves attempts/spend history.

Acceptance Criteria:
- Attempt exhaustion blocks further automatic execution and an unknown outcome never causes a duplicate retry.
- Repeated cancel/retry commands do not reset counters or erase held liability.

Required Automated Tests:
- Initial plus two attempts and restart exhaustion.
- Known nonbillable versus possible accepted 429/5xx/timeouts.
- Queued cancellation and manual retry renewed-authority negatives.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Unknown outcomes enter recovery; cancellation remains intent until cessation is verified by later process/provider integration.

Out of Scope:
Actual process termination, optimistic refunds and hidden adapter retries.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T030: Implement crash-safe artifact publication and response recovery

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Implement crash-safe artifact publication and response recovery within the frozen boundaries.

Why: Satisfies the frozen Idempotency and checkpoints contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T028
- T013
- T021

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**

Likely Files:
- alpha/artifacts/publication.py
- alpha/jobs/recovery_spool.py
- tests/worker/publication/

Requirements:
- Persist attempt-linked response metadata and staged valid bytes, durably install immutable media, then transactionally register/account results.
- Fence selection against current input versions and user intent; stale/canceled valid output remains delivery history.
- Recover install-before-register and register-before-worker-exit windows; retry local persistence instead of reissuing generation.

Acceptance Criteria:
- Every tested crash point yields either recoverable private bytes or one registered valid output, never false success.
- Repeated recovery neither resubmits paid work nor double charges; previous selection remains on invalid output.

Required Automated Tests:
- S7-style publication crash matrix using real disposable files.
- Hash mismatch, partial write, full disk and invalid validation.
- Late result/fence races and exactly-once settlement.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Preserve source/attempt identity and quarantine unusable data; recovery requires evidence before financial release.

Out of Scope:
Acoustic restoration, provider retrieval capabilities not verified or overwriting historical evidence.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T031: Expose durable health, progress and redacted operation inspection

Status: NOT_STARTED

Phase: 5 — Durable production worker

Objective: Expose durable health, progress and redacted operation inspection within the frozen boundaries.

Why: Satisfies the frozen Observability contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T030
- T004
- T012

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Observability**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Minimum progress and history**

Likely Files:
- alpha/observability/
- alpha/web/status.py
- tests/integration/status/

Requirements:
- Provide lightweight structured logs and persisted job/attempt/financial/progress inspection, lane health and recovery reasons.
- Creator status reveals only owned request and truthful completed stages; owners can inspect provider IDs, failures and unresolved liabilities.
- Log correlation IDs and certainty, not secrets or full private scripts; show unknown progress without fabricated percentage/time estimates.

Acceptance Criteria:
- Restart/status probes reflect durable state and remain ownership filtered.
- Incomplete generation, received-but-unmapped audio and unvalidated render are never reported export-ready.

Required Automated Tests:
- Owned/foreign status and operator-role negatives.
- Crash reload, stage counts and unknown outcome status.
- Secret/private-content log redaction.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
External observability platform or large admin dashboard.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 6: Provider boundaries

### T032: Define narrow provider contracts and deterministic fake adapters

Status: NOT_STARTED

Phase: 6 — Provider boundaries

Objective: Define narrow provider contracts and deterministic fake adapters within the frozen boundaries.

Why: Satisfies the frozen Provider capabilities contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T028
- T030
- T003

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Job, operation and attempt**

Likely Files:
- alpha/providers/contracts.py
- alpha/providers/fakes.py
- tests/integration/providers/

Requirements:
- Define typed boundaries for text/planner, search, image and TTS, including complete request scope, outcome certainty, usage and validation metadata.
- Adapters cannot grant money, entitlement, retries or workflow authority; executor owns them.
- Provide scripted fakes for successful, malformed, billed-failure, unknown and late responses, with optional durable request identity.

Acceptance Criteria:
- Fake operations can drive the durable pipeline without any SDK/network initialization.
- Adapters cannot invoke an unreserved nested paid operation or retry internally.

Required Automated Tests:
- Contract validation and unsupported modality/field rejection.
- Scripted unknown/crash/cancel/late response outcomes.
- Network trap and unauthorized nested submission.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Universal provider marketplace or selecting a new provider/model.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T033: Implement one-send, bounded provider transport while disabled

Status: NOT_STARTED

Phase: 6 — Provider boundaries

Objective: Implement one-send, bounded provider transport while disabled within the frozen boundaries.

Why: Satisfies the frozen Transport evidence contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T032
- T029

Source of Truth:
- [docs/architecture/evidence/provider-feasibility/S4.md](docs/architecture/evidence/provider-feasibility/S4.md), section **Transport evidence**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**

Likely Files:
- alpha/providers/transport.py
- tests/integration/transport/

Requirements:
- Prepare bounded request transport with explicit timeout, response-size handling and secret-safe identifiers, but disabled live configuration.
- Disable, bound or surface hidden retries; specifically do not assume interactions attempts=1 means one HTTP send.
- Use local synthetic transport inspection to prove one concrete reserved attempt cannot send twice; preserve ambiguous acceptance outcome.

Acceptance Criteria:
- Injected 429/5xx/connection loss produces the documented send count and uncertainty, never an invisible retry.
- Transport supports cancellation request without claiming provider termination or billing settlement.

Required Automated Tests:
- SDK/direct-transport local one-send probes inspired by S4.
- Timeout before/after send, lost request ID and response truncation.
- Redaction, allowed endpoint configuration and disabled-live tests.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
No provider API calls; only fake HTTP/local stub transport. Live endpoint proof is a later gate.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Assumed API idempotency, endpoint activation or automatic external fallback.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T034: Implement fail-closed capability certificates and request bounds

Status: NOT_STARTED

Phase: 6 — Provider boundaries

Objective: Implement fail-closed capability certificates and request bounds within the frozen boundaries.

Why: Satisfies the frozen Failure, restoration and limits of enforcement contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T033
- T022

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**

Likely Files:
- alpha/providers/capabilities.py
- tests/financial/capabilities/

Requirements:
- Persist reviewed provider/model/account/rate/endpoint certificates with complete input/output/thinking/modality/tool/count/attempt bounds and expiry.
- Require complete-request preflight or an evidenced conservative supported serving-input bound; an unvalidated tokenizer is not a certificate.
- Validate prepared requests/configuration against the certificate and recalculate reservation on rate/scope changes; disallow unpriced tools/cache/background/add-ons.

Acceptance Criteria:
- Absent, expired, mismatched or incomplete certificates prevent submission before transport.
- Model output cannot increase caps/query count; configured output limits and price basis are pinned in attempts.

Required Automated Tests:
- All missing charged dimensions and unsupported output-cap fixtures.
- Expired TTS introductory rate, changed model/endpoint/account.
- Narrow-tokenizer unvalidated path and full fallback support rejection.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Finite complete exposure gate implemented offline; captured historical sensitivity cannot enable a capability.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Provider/tokenizer experiment, silently choosing final text model or assuming free tier.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T035: Implement explicit capability decision records and disabled catalogs

Status: NOT_STARTED

Phase: 6 — Provider boundaries

Objective: Implement explicit capability decision records and disabled catalogs within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T034
- T012

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Deferred operational and commercial specification**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Language**

Likely Files:
- alpha/providers/configuration.py
- alpha/models/capability_decisions.py
- tests/domain/configuration/

Requirements:
- Represent pending owner decisions for normal text model, upload/style/voice limits and experimental language activation without choosing values.
- Retain selected image gemini-3.1-flash-lite-image and TTS gemini-3.8-flash-lite-tts identifiers; do not substitute models.
- Expose controlled disabled reasons and validated configuration versions, separate decision acceptance from financial and technical activation.

Acceptance Criteria:
- Unselected normal text model remains pending, while fake workflows can be built without live adoption.
- Spanish/French/Bangla/Hindi remain experimental disabled unless separate verified activation exists.

Required Automated Tests:
- Pending/accepted/revoked decision state and owner-role enforcement.
- No client override or candidate-to-selected promotion.
- Config changes invalidate relevant quotes without enabling paid execution.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Resolving owner choices, commercial quotas or implementing topic suggestions.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 7: Artifact contracts

### T036: Implement guarded artifact selection and deterministic invalidation

Status: NOT_STARTED

Phase: 7 — Artifact contracts

Objective: Implement guarded artifact selection and deterministic invalidation within the frozen boundaries.

Why: Satisfies the frozen Invalidation matrix contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T030
- T006
- T010

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Invalidation matrix**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Provenance, compatibility and staleness**

Likely Files:
- alpha/artifacts/selection.py
- alpha/artifacts/invalidation.py
- alpha/services/mutations.py
- tests/domain/invalidation/

Requirements:
- Implement the frozen typed invalidation matrix with transactional selected-version CAS and reusable centralized content-mutation guard hooks.
- Words/voice/language/delivery invalidate affected narration/timing/captions/render; keep images and flag visual review. Visual prompt changes mark image incompatibility/review; image replace/restore affects render only.
- Caption text/style/toggle, motion/music and manual timing affect only defined dependents; research findings do not change words without approval. Disabled caption-only staleness cannot block otherwise valid render.

Acceptance Criteria:
- Table-driven tests verify both invalidated dependents and unaffected assets for every frozen mutation class, including reorder/delete and restoration interfaces.
- Failed or stale attempts never replace current selection; explicit keep-image review is version-bound.

Required Automated Tests:
- Complete invalidation matrix with narration/voice/language/prompt/image/caption/motion/music/order/delete/factual/restore cases.
- CAS concurrency and user-intent/fence selection races.
- Disabled captions, preserved manual corrections and required narration/timing blocking.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject mutation during a held final-render guard once render integration is added; retain manual/history versions.

Out of Scope:
Generic workflow engine, user-facing editor or automatic paid regeneration.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 8: Research and approved scripts

### T037: Implement entitlement-aware bounded research planning

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Implement entitlement-aware bounded research planning within the frozen boundaries.

Why: Satisfies the frozen Recommended complete flow contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T035
- T036
- T009
- T032

Source of Truth:
- [docs/architecture/evidence/research-feasibility/S4-R.md](docs/architecture/evidence/research-feasibility/S4-R.md), section **Recommended complete flow**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner decision — Research entitlement and topic discovery, 2026-10-05**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**

Likely Files:
- alpha/research/planner.py
- tests/integration/research_planner/

Requirements:
- Prepare a tool-free bounded planner from approved topic/script scope only after server entitlement and financial admission.
- Validate proposed queries against application-controlled count/length/uniqueness and expected schema; excess output cannot grant search authority.
- Skip topic Research with accurate non-entitlement notice; keep the separate pasted checking policy unchanged.

Acceptance Criteria:
- An over-limit query proposal is rejected or admitted only under explicitly configured bounded policy, never executed in full.
- Lower-tier forged calls do not reach planner/search and failure never looks like researched success.

Required Automated Tests:
- Matrix entitlement and fake query injection/over-limit/duplicate cases.
- Malformed responses and model-output budget expansion.
- Reservation requirements and no research before authorization.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Live planning, automatic generated-script second fact pass or arbitrary web agents.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T038: Integrate bounded Tavily Basic search and evidence normalization

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Integrate bounded Tavily Basic search and evidence normalization within the frozen boundaries.

Why: Satisfies the frozen Recommended complete flow contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T037
- T033
- T016

Source of Truth:
- [docs/architecture/evidence/research-feasibility/S4-R.md](docs/architecture/evidence/research-feasibility/S4-R.md), section **Recommended complete flow**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**

Likely Files:
- alpha/research/search.py
- alpha/research/evidence.py
- tests/integration/search/

Requirements:
- Prepare application-controlled Basic REST searches, one admitted query per request, with pinned call/results/chunk/evidence bounds.
- Disable auto_params, raw page/image/answer expansion and Extract/Crawl/grounding; normalize source IDs/URLs/titles/retrieval and publication dates.
- Treat returned pages as untrusted data; bounded truncation has provenance and no source content can trigger another request.

Acceptance Criteria:
- Fake search call count never exceeds configured admitted query authority; each request is separately reserved.
- Malformed/oversized evidence produces incomplete findings, not arbitrary follow-up retrieval or fabricated sources.

Required Automated Tests:
- Query count/results/chunks cap and disabled tools.
- Source instruction injection, duplicate URLs and truncated evidence.
- Paid failure/unknown outcome with retained sources and liability.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Tavily adapter disabled live until activation; no assumed free quota.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
New search vendor, channel retrieval or unbounded scraping.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T039: Implement tool-free research synthesis, warnings and failure notices

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Implement tool-free research synthesis, warnings and failure notices within the frozen boundaries.

Why: Satisfies the frozen Recommended complete flow contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T038
- T009

Source of Truth:
- [docs/architecture/evidence/research-feasibility/S4-R.md](docs/architecture/evidence/research-feasibility/S4-R.md), section **Recommended complete flow**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Failure and recovery paths**

Likely Files:
- alpha/research/synthesis.py
- tests/integration/synthesis/

Requirements:
- Synthesize only bounded stored evidence through a financially admitted tool-free text operation.
- Persist creator-private sources/warnings, distinguish incomplete/research-unavailable states and retain useful evidence.
- Allow approved non-blocking factual progression without implying checks succeeded; entitled retry still requires financial/lane eligibility.

Acceptance Criteria:
- Generated findings reference actual retrieved evidence; invented citations are rejected or identified as unsupported.
- Research failure leaves sources and valid prior work intact and no warnings leak into narration/render.

Required Automated Tests:
- Unsupported source IDs/URLs and prompt injection.
- Partial retrieval/synthesis failure and nonblocking notice.
- Entitled retry versus no-entitlement bypass; private export exclusion.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Mandatory extra humanization, rewriting approved pasted words or weakening factual acceptance.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T040: Implement pasted-script factual checking without rewriting

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Implement pasted-script factual checking without rewriting within the frozen boundaries.

Why: Satisfies the frozen Pasted script → video contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T039
- T006

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Pasted script → video**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Approvals**

Likely Files:
- alpha/research/script_check.py
- tests/integration/script_check/

Requirements:
- Apply the separate pasted-script checking policy to immutable approved words, using bounded evidence/checking operations.
- Create version-bound warnings and proposed individual/all corrections; keep original/current text unchanged until explicit approval.
- Checking failure preserves available evidence and displays incomplete notice; no claimed successful research for a non-entitled topic.

Acceptance Criteria:
- Provider-proposed text cannot replace approved words or independently authorize downstream regeneration.
- A stale proposal cannot be accepted against an incompatible script version.

Required Automated Tests:
- Word/punctuation preservation and source-bound proposals.
- Failure/incomplete check and malicious rewrite output.
- Version mismatch, owner isolation and no paid downstream side effects.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Topic research eligibility changes or automatic correction acceptance.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T041: Implement factual, translation and adaptation approval commands

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Implement factual, translation and adaptation approval commands within the frozen boundaries.

Why: Satisfies the frozen Approvals contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T040
- T036
- T023

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Approvals**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Pasted script → video**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**

Likely Files:
- alpha/services/script_approvals.py
- tests/domain/approvals/

Requirements:
- Implement individual and accept-all factual proposals against exact examined versions with explicit actor approval.
- For language mismatch or over-range pasted script, require approved proposed translation/adaptation; preserve original words when declined.
- Accepted words update current script/projection and deterministic invalidation; paid proposal generation uses existing bounded adapters and must remain blocked without authority.

Acceptance Criteria:
- Approval changes only reviewed content and does not grant downstream generation spending.
- Dismissal/rejection preserves words; stale, cross-owner or render-locked approvals cannot apply.

Required Automated Tests:
- Individual/all acceptance and decline/dismissal.
- Translation/adaptation approval/version and >10-minute handling.
- Atomic projection/invalidation, stale proposal and no provider side effect.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Automatic rewriting, tiny-script expansion or mandatory routine topic script approval.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T042: Extract topic-to-script generation under frozen authority

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Extract topic-to-script generation under frozen authority within the frozen boundaries.

Why: Satisfies the frozen Default topic → video contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T007
- T039
- T032
- T041

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Default topic → video**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Generation and factual handling**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**

Likely Files:
- alpha/scripts/generation.py
- alpha/providers/text.py
- tests/integration/topic_script/

Requirements:
- Extract suitable create_content.py prompt-loading/request ideas into explicit approved configuration, no CLI/global clients or filename resume.
- Generate a bounded language/duration-appropriate script using entitled research where applicable; persist immutable generated version and consumed operation provenance.
- Validate text/structured response before selecting; immediately count/recalculate scope and preserve completed research cost.

Acceptance Criteria:
- Fake topic production uses one admitted writing operation with no mandatory humanization, generated-script fact-check or paid TTS-preparation extra call.
- Invalid/truncated output fails honestly, cannot spawn paid fallback or silently shorten to fit budget.

Required Automated Tests:
- Factual entitled/non-entitled topic paths and default duration.
- Malformed/incomplete output and version-bound registration.
- Scope expansion pause, paid-write failure and no import-time network.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Adopting gemini-3.5-flash-lite without owner decision or copying prototype orchestration.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T043: Implement source-faithful scenes, visual descriptions and curated presets

Status: NOT_STARTED

Phase: 8 — Research and approved scripts

Objective: Implement source-faithful scenes, visual descriptions and curated presets within the frozen boundaries.

Why: Satisfies the frozen Creative controls and script fidelity contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T042
- T007
- T036

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted staged estimation and sentence-driven image scope**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**

Likely Files:
- alpha/scripts/scene_planning.py
- alpha/visuals/presets.py
- alpha/visuals/prompts.py
- tests/domain/scenes/

Requirements:
- Decompose accepted script deterministically into sentence-linked planned visuals/stable scenes and verify exact approved narration coverage.
- Use bounded tool-free planning for visual description/prompt where configured; preserve separate visual description and generation prompt provenance.
- Provide Minimal Illustration, Storybook and Documentary Illustration configuration; remove hardcoded prototype recurring-character/style promises.

Acceptance Criteria:
- No approved words are dropped/reordered/rewritten by planning; sentence-derived initial image scope matches the reviewed plan.
- Malformed or enlarged model scene proposals do not authorize additional images or modify approved script.

Required Automated Tests:
- Exact scene/span/script coverage and stable IDs.
- Preset prompt provenance and model-proposed scope expansion.
- Invalid JSON/truncation and no blanket retry or raw-invalid-output resume.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Full Style Studio, character identity system, scene add/duplicate or final provider adoption.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 9: Images

### T044: Extract the image adapter with disabled live capability

Status: NOT_STARTED

Phase: 9 — Images

Objective: Extract the image adapter with disabled live capability within the frozen boundaries.

Why: Satisfies the frozen Provider capabilities contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T043
- T033
- T034

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md), section **Provider financial bound used in the planning proof**

Likely Files:
- alpha/providers/images.py
- tests/integration/image_adapter/

Requirements:
- Extract request/prompt primitives from generate_images.py behind the narrow image interface, retaining selected gemini-3.1-flash-lite-image.
- Remove import-time clients, filename resume, recurring-character reference assumptions, hidden duplicate sends and save-failure regeneration.
- Require complete configured input/output/modality/count bounds; $0.0336 is output-only sensitivity, not full financial exposure.

Acceptance Criteria:
- Synthetic transport returns image bytes/usage/certainty with one admitted send and no live activation.
- A response requiring unknown billable scope is rejected before submission; no substitute model is chosen.

Required Automated Tests:
- Prepared request contract, one-send and disabled capability.
- Missing/invalid image response and separate usage certainty.
- Wrong model/rate/modality/reference-input cap negatives.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Image provider boundary remains disabled; no Gemini credits or calls required.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Live generation, measured image quality/failure rate or final provider-price hardcoding.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T045: Integrate image generation, validation and scoped failure recovery

Status: NOT_STARTED

Phase: 9 — Images

Objective: Integrate image generation, validation and scoped failure recovery within the frozen boundaries.

Why: Satisfies the frozen Image regeneration and replacement contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T044
- T030
- T016
- T036

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Completion and failed attempts**

Likely Files:
- alpha/visuals/generation.py
- tests/integration/image_pipeline/

Requirements:
- Execute one approved scene image operation with scope/config/fence/reservations and private staged decoded-media validation.
- Register immutable versions, account delivered output once and select only if still current; preserve prior selection and other scenes on failure.
- Expose independent failed-image retry through durable bounded retry policy; reuse recoverable paid bytes after local save failure.

Acceptance Criteria:
- Fake success produces a valid current or history-only image according to starting versions.
- Corrupt/invalid/unknown output never becomes selectable and cannot trigger unreserved regeneration.

Required Automated Tests:
- Independent failure/retry with unaffected scene preservation.
- Stale edit, canceled late result and exactly-once spend.
- Corrupt decode/full disk/crash registration recovery.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Per-image maximum required before any enabled paid attempt; ordinary tests use fake bytes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Broad media generation, automatic all-scene regeneration or live image testing.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T046: Implement image restoration and explicit visual review

Status: NOT_STARTED

Phase: 9 — Images

Objective: Implement image restoration and explicit visual review within the frozen boundaries.

Why: Satisfies the frozen Selection, restoration and concurrent edits contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T045
- T017

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Version inspection and restoration**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**

Likely Files:
- alpha/visuals/history.py
- tests/domain/image_history/

Requirements:
- Inspect previous valid image versions and restore through guarded selected-version commands.
- Restore/replace invalidates render only; preserve narration, timing and captions and record compatibility/provenance.
- After narration/prompt changes require explicit keep-image review or validated replacement/regeneration; never claim old output matches changed instructions.

Acceptance Criteria:
- Existing compatible restoration consumes no generation allowance and leaves unrelated scene assets untouched.
- Failed last generation remains distinct from selected valid image; restoring cannot mutate immutable historical configuration.

Required Automated Tests:
- Restore/replace/keep-image invalidation matrix.
- Cross-owner, stale-version and render-locked restoration.
- No provider calls or allowance debit on existing-asset restore.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Narration restoration, deleting history or automatic paid replacement.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 10: Narration and timing

### T047: Implement effective narration settings and validated cached previews

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Implement effective narration settings and validated cached previews within the frozen boundaries.

Why: Satisfies the frozen Creative controls and script fidelity contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T010
- T035
- T014

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Scene correction and narration**

Likely Files:
- alpha/narration/configuration.py
- alpha/narration/voice_catalog.py
- tests/domain/voices/

Requirements:
- Represent supported project voice/delivery defaults and scoped overrides with exact effective configuration/provenance.
- Require supported selected-model voice metadata, permitted cached preview assets and format/privacy validation before enabling catalog entries.
- Missing live-supported catalog remains disabled while tests use labeled fixtures; literal bracketed approved words are not silently interpreted as delivery instructions.

Acceptance Criteria:
- Changing effective voice invalidates affected narration dependencies without changing other scene defaults.
- Preview playback is local cached media and never makes a hidden TTS call.

Required Automated Tests:
- Inheritance/override/default return and config changes.
- Unverified entry/missing preview and disabled controls.
- Approved literal tags/word fidelity and zero provider preview calls.

Manual Verification:
Owner supplies or approves supported catalog/preview rights; reviewer verifies provenance before enabled entries.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Voice cloning, extensive provider controls or guessing supported voices.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T048: Implement bounded coherent multi-scene segment planning

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Implement bounded coherent multi-scene segment planning within the frozen boundaries.

Why: Satisfies the frozen Narration generation granularity — frozen B policy contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T043
- T047
- T022

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Narration generation granularity — frozen B policy**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Narration segment authorization — accepted amendment**

Likely Files:
- alpha/narration/segments.py
- tests/domain/segments/

Requirements:
- Create deterministic coherent contiguous multi-scene groups with explicit membership/text/effective configuration and complete request bounds.
- Group whole approved scenes at suitable boundaries; no fixed 500-word/3000-byte production policy inherited from prototype.
- Correction planning regenerates the whole affected B segment, quotes all affected scenes and preserves unrelated sources; incompatible configuration/oversized scope pauses for explicit plan handling.

Acceptance Criteria:
- Each planned scene belongs to an admitted coherent source and no one-call-per-scene fallback appears silently.
- Grouping changes recalculate authority and cannot introduce unreserved extra context/fallback calls.

Required Automated Tests:
- Whole-scene membership, config transitions and oversized sentence/group.
- B whole affected-segment correction and unrelated preservation.
- Financial K recalculation and no AI-expanded grouping authority.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Surgical C1 paid repair, unvalidated final grouping constants or hidden provider fallback.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T049: Extract bounded TTS request and validated source-audio handling

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Extract bounded TTS request and validated source-audio handling within the frozen boundaries.

Why: Satisfies the frozen Provider capabilities contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T048
- T033
- T034

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Narration generation granularity — frozen B policy**

Likely Files:
- alpha/providers/tts.py
- alpha/narration/audio_validation.py
- tests/integration/tts_adapter/

Requirements:
- Extract create_tts.py request/format ideas into an explicit adapter for gemini-3.8-flash-lite-tts, disabled live until verified.
- Preserve approved words, explicit delivery metadata and original coherent source audio; remove global clients, 20 retries, file-existence skipping and audio directory deletion.
- Validate MIME/container/sample format/full decoding and input/output/thinking/rate bounds, retaining usage uncertainty.

Acceptance Criteria:
- Fake valid audio is registered only after complete decode and source/config equality checks.
- Unsupported/missing/truncated audio fails without deleting prior sources or initiating generation again.

Required Automated Tests:
- Container/sample format, truncated bytes and unsupported modality.
- One-send/rate expiry/complete cap negatives.
- Approved word/delivery preparation equality and source preservation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
TTS capability disabled until gate; introductory pricing expiry must invalidate certificates.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Live narration generation, narration quality claims or per-scene TTS.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T050: Integrate initial and correction B narration operations

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Integrate initial and correction B narration operations within the frozen boundaries.

Why: Satisfies the frozen Narration generation granularity — frozen B policy contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T049
- T030
- T036

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Narration generation granularity — frozen B policy**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Scene correction and narration**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Narration segment authorization — accepted amendment**

Likely Files:
- alpha/narration/generation.py
- tests/integration/narration_pipeline/

Requirements:
- Execute initial coherent B sources and regenerate entire affected coherent segment for corrections under exact scope/financial authority.
- Store immutable source versions/effective config and previous selections; audio receipt is not mapped narration readiness.
- Any member edit while an affected segment executes makes its arriving full source history-only; do not select unchanged sibling ranges silently.

Acceptance Criteria:
- B correction preserves unrelated segments/images and charges one source delivery once rather than each scene reference.
- Source generation failure leaves compatible prior work and reports all affected scenes.

Required Automated Tests:
- Initial/correction group memberships and exactly-once allowance.
- Member-edit/cancel/stale fence result selection.
- Paid success/local save failure and missing source validation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Coherent source per-attempt reservation; tests reuse existing/local synthetic audio, no provider generation.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Automatic audio slicing or unquoted fallback generation.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T051: Extract local supervised Whisper alignment

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Extract local supervised Whisper alignment within the frozen boundaries.

Why: Satisfies the frozen Segment, mapping and assembly contracts contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T050
- T027

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Segment, mapping and assembly contracts**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**

Likely Files:
- alpha/narration/alignment.py
- alpha/jobs/local_process.py
- tests/media/alignment/

Requirements:
- Extract make_timestamps.py local faster-whisper interface using explicit cached weights/configuration and controlled child lifetime.
- Use Unicode-aware source-bound transcript/timing output; remove ASCII-only normalization, line identity and fuzzy-score-only success.
- Missing weights/configuration is an actionable block, not automatic model download; persist local checkpoints and resource bounds.

Acceptance Criteria:
- Local alignment produces source-hash/text-version-linked word ranges or review/failure, never fabricated timing.
- Cancellation/crash preserves source audio and does not consume generation allowance.

Required Automated Tests:
- Unicode/punctuation/repeated phrase transcript fixtures.
- Missing cached model, malformed timestamps and child interruption.
- Source-version mismatch and no network/model-fetch guard.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Local transform, no provider allowance; infrastructure usage still counts operating costs.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
New hosted alignment service, unsafe fuzzy acceptance or host sizing reruns.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T052: Validate scene mappings and version-bound narration fidelity review

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Validate scene mappings and version-bound narration fidelity review within the frozen boundaries.

Why: Satisfies the frozen Segment, mapping and assembly contracts contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T051
- T010

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Segment, mapping and assembly contracts**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted narration fidelity amendment — 2026-10-05**
- [docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/README.md](docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/README.md), section **Mandatory mapping audit**

Likely Files:
- alpha/narration/mappings.py
- alpha/narration/review.py
- tests/media/mappings/

Requirements:
- Validate complete ordered speech coverage and exact source/text/config references; separate next-start visual markers from extraction endpoints.
- Represent ASR discrepancy, accepted meaning-preserving variation, material error and uncertain mapping separately, with version-bound creator review.
- Material omitted/repeated/fact/name/number/negation errors or uncertain required boundaries block affected selection/export; no automatic paid repair.

Acceptance Criteria:
- Each visual starts at the next mapped narration start with first at zero/final through source end; ordinary narration is not cut.
- Approved minor variation does not rewrite script/provenance or certify unresolved boundaries.

Required Automated Tests:
- S5 damaged/repeated/omitted/reordered/ambiguous mapping fixtures.
- Meaning-preserving accepted variation versus material/unreviewed findings.
- Word coverage, exact source hash and caption association.

Manual Verification:
Reviewer listens to existing fixture boundary examples when algorithmic evidence cannot establish acoustic truth; no new TTS calls.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Keep source audio and expose actionable local review; block incompatible export without crashing the application.

Out of Scope:
Claiming ASR absolute truth or accepting silence/energy as word-boundary proof.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T053: Implement continuous narration assembly and global timing projection

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Implement continuous narration assembly and global timing projection within the frozen boundaries.

Why: Satisfies the frozen Segment, mapping and assembly contracts contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T052

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Segment, mapping and assembly contracts**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Narration generation granularity — frozen B policy**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Invalidation matrix**

Likely Files:
- alpha/narration/assembly.py
- tests/media/assembly/

Requirements:
- Assemble whole coherent selected sources continuously for ordinary scene playback/render; Scene Audio Mappings drive visuals/captions without independent speech cuts.
- Project local scene/word timings into global offsets and reproject later offsets after source duration changes without regenerating unaffected audio.
- Preserve legitimate pauses and pin assembly/source versions; reject gaps, overlaps or incompatible ordering.

Acceptance Criteria:
- Scene visual boundaries never truncate ordinary B narration; complete source samples remain accounted.
- An earlier segment duration change shifts later offsets while preserving later source identity/validity.

Required Automated Tests:
- Sample/scene/word coverage and nonuniform mapped visual starts.
- Duration shift/global projection with unchanged later sources.
- Truncation/gap/overlap and incompatible assembly rejection.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Intentional scene-only extraction/restoration before join validation.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T054: Validate intentional audio ranges and joins for correction capabilities

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Validate intentional audio ranges and joins for correction capabilities within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T053

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Segment, mapping and assembly contracts**

Likely Files:
- alpha/narration/joins.py
- tests/media/joins/
- capability evidence for acoustic correction

Requirements:
- Implement bounded source-bound range/join validation for scoped restoration and reorder/delete; distinguish intentional transformations from ordinary B continuity.
- Use existing real audio/local fixtures to prove speech coverage and assess joins; silent S7 WAVs are not acoustic proof.
- Enable only validated transformations, with uncertain endpoints/joins blocked and safe local repair offered; never silently restore siblings or regenerate paid sources.

Acceptance Criteria:
- Representative joins preserve approved surviving speech without omission/repetition/conspicuous cut-off/glitch according to recorded review.
- Unsafe/ambiguous extraction returns a blocked capability with source assets preserved.

Required Automated Tests:
- Boundary/range/order coverage, overlapping/repeated and missing ranges.
- Single-scene versus segment scope and preserved unrelated selections.
- Validated/invalid/uncertain join capability gating.

Manual Verification:
Independent listening to existing/local acoustic fixtures is required; document evidence and unresolved calibration rather than infer quality from silent tests.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
New provider audio, automatic paid repair or weakening core restoration/reorder requirements.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T055: Implement compound narration restoration and scene reorder/delete

Status: NOT_STARTED

Phase: 10 — Narration and timing

Objective: Implement compound narration restoration and scene reorder/delete within the frozen boundaries.

Why: Satisfies the frozen Selection, restoration and concurrent edits contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T054
- T036
- T041

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Version inspection and restoration**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Reorder and delete scenes**

Likely Files:
- alpha/narration/restoration.py
- alpha/services/scene_order.py
- tests/domain/restoration/

Requirements:
- Different-word restoration requires reviewed text+audio+compatible timing/captions adoption and current script projection update.
- Same-word/different-delivery restoration shows effective recorded settings, applies only approved scope, preserves project defaults/siblings and supports return to default.
- Reorder/delete preserves stable surviving scene assets, reassembles validated ranges and offsets; unsafe joins block, not silently change scope or authorize paid work.

Acceptance Criteria:
- No restored audio speaks different words against unchanged current text; single-scene restore cannot restore the whole segment invisibly.
- Reorder/delete updates active script/order/render dependencies and preserves compatible surviving assets/history.

Required Automated Tests:
- Different/same words, override/default and compound atomic restoration.
- Reorder/delete coverage plus preserved image/local caption/source versions.
- Cross-owner, render-lock, unreviewed join and no allowance debit.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Adding/duplicating scenes, changing project default silently or restoring incompatible manual captions without review.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 11: Captions and render settings

### T056: Implement caption versions, manual corrections and timing compatibility

Status: NOT_STARTED

Phase: 11 — Captions and render settings

Objective: Implement caption versions, manual corrections and timing compatibility within the frozen boundaries.

Why: Satisfies the frozen Captions, timing, motion and music contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T053
- T055

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Captions, timing, motion and music**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Invalidation matrix**
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**

Likely Files:
- alpha/captions/domain.py
- tests/domain/captions/

Requirements:
- Generate local source-linked caption cues with exact approved/accepted speech association; persist manual caption text/timing versions separately.
- Support correction, style/toggle configuration and manual-review retention when audio changes.
- Enabled outdated/unresolved captions block export; disabled caption-only incompatibility does not waive required narration/visual timing.
- Reuse the pure seconds_to_srt formatting helper only for already validated nonnegative cue times where subtitle metadata needs it; it is not the caption burn-in renderer.

Acceptance Criteria:
- Caption edits do not regenerate audio/images and manual corrections are never silently discarded.
- Finite ordered within-duration cues and compatibility determine readiness correctly for ON/OFF.

Required Automated Tests:
- Caption-only invalidation and enabled/disabled readiness.
- Manual-versus-refreshed cues, source change and review-required state.
- Invalid ranges, overlap, coverage and accepted spoken variation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Emphasis Text or arbitrary font uploads.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T057: Integrate shaped caption PNGs and approved style/font bounds

Status: NOT_STARTED

Phase: 11 — Captions and render settings

Objective: Integrate shaped caption PNGs and approved style/font bounds within the frozen boundaries.

Why: Satisfies the frozen Runtime contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T056
- T035

Source of Truth:
- [docs/architecture/evidence/rendering-feasibility/S6/README.md](docs/architecture/evidence/rendering-feasibility/S6/README.md), section **Runtime**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Captions, timing, motion and music**

Likely Files:
- alpha/captions/shaping.py
- alpha/captions/styles.py
- tests/media/caption_shaping/

Requirements:
- Adopt S6 HarfBuzz/FreeType plus Pillow shaped PNG overlay approach, preserving licensing/version/hash and Unicode fallback metadata.
- Represent supported caption styling with verified readability/placement/resource bounds; unresolved material style policy is gated rather than invented.
- Validate English wrap/safe placement and technical Latin/Bangla/Devanagari shaping using existing strings; no SRT-alone or unavailable FFmpeg drawtext assumption.

Acceptance Criteria:
- Long text cannot clip, silently shrink beyond approved policy or render missing glyphs.
- Enabled captions have reproducible shaped assets and OFF requires no caption font/timing branch; technical multilingual tests do not activate languages.

Required Automated Tests:
- English normal/long/punctuation/number two-line and over-limit fixtures.
- Spanish/French/Bangla conjunct/Hindi glyph and PNG alpha/hash tests.
- Font missing/license/version mismatch, unsafe position/style and OFF.

Manual Verification:
Reviewer inspects decoded caption images for readability/shaping; owner resolves any material style-bound decision before enabling it.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Font uploads, language quality claims or pretending S6 witness pixel values are final product policy.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T058: Implement optional gentle motion and deterministic visual recipes

Status: NOT_STARTED

Phase: 11 — Captions and render settings

Objective: Implement optional gentle motion and deterministic visual recipes within the frozen boundaries.

Why: Satisfies the frozen Creative controls and script fidelity contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T036
- T043

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**
- [docs/architecture/evidence/rendering-feasibility/S6/README.md](docs/architecture/evidence/rendering-feasibility/S6/README.md), section **Runtime**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Captions, timing, motion and music**

Likely Files:
- alpha/rendering/motion.py
- tests/media/motion/

Requirements:
- Provide bounded basic/gentle image motion ON/OFF render configuration, default on.
- Extract validated scale/zoompan ideas with S6 smoothing fix and per-scene applicability; timing stays mapping-driven.
- Do not add timeline/keyframes/custom animation controls or affect image/narration generation.

Acceptance Criteria:
- ON/OFF yields deterministic recipes with full-frame coverage for every scene and no first-image-only effect.
- Toggling motion invalidates render only and leaves selected audio/images compatible.

Required Automated Tests:
- Every-scene recipe and no black corners/frame escape.
- S6-style smooth-motion and stable OFF local controls.
- Configuration bounds and dependency preservation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Advanced motion, paid video generation or invented visual-timing changes.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T059: Implement licensed library music configuration and safe mixing policy

Status: NOT_STARTED

Phase: 11 — Captions and render settings

Objective: Implement licensed library music configuration and safe mixing policy within the frozen boundaries.

Why: Satisfies the frozen Creative controls and script fidelity contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T036
- T035

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Creative controls and script fidelity**
- [docs/architecture/evidence/rendering-feasibility/S6/README.md](docs/architecture/evidence/rendering-feasibility/S6/README.md), section **Runtime**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Captions, timing, motion and music**

Likely Files:
- alpha/music/catalog.py
- alpha/rendering/audio_mix.py
- tests/media/music/

Requirements:
- Provide optional music OFF by default, with enabled entries only from verified permitted library assets and bounded volume/mix configuration.
- Use existing local controls to preserve full narration, intentional pauses and no clipping; disclose missing/unlicensed library as unavailable.
- Music changes affect render only; no custom audio upload, stochastic provider selection or automatic paid licensing.

Acceptance Criteria:
- OFF contributes no music and ON covers intended duration without shortening narration.
- Only permitted catalog entries are selectable and missing/invalid entries cannot silently replace audio.

Required Automated Tests:
- Music ON/OFF/full-duration and clipping/narration-preservation fixtures.
- Volume/config bounds, catalog permission and missing asset.
- Render-only invalidation and no generation allowance charge.

Manual Verification:
Verify library asset rights/provenance and listen to existing speech/music controls before enabling entries.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Custom user audio, purchasing tracks or establishing final music catalog by guessing.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 12: Creation experience

### T060: Build owned project dashboard and honest autosave experience

Status: NOT_STARTED

Phase: 12 — Creation experience

Objective: Build owned project dashboard and honest autosave experience within the frozen boundaries.

Why: Satisfies the frozen Dashboard and New Video contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T012
- T004
- T005
- T031

Source of Truth:
- [docs/DESIGN.md](docs/DESIGN.md), section **Dashboard and New Video**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Project lifecycle and allowance access**

Likely Files:
- alpha/web/projects.py
- templates/alpha/projects/
- static/alpha/projects.js
- tests/ui/projects/

Requirements:
- Build thumbnail-led recent projects with clear New Video action, compact header, empty state and reopen/rename routes.
- Show actual saved/saving/error, owned queue/failure/readiness and actual storage/allowance disclosure; no analytics/billing dashboard.
- Preserve unsaved input where practical on failed save and prevent stale response overwriting newer accepted text.

Acceptance Criteria:
- Two identities see only their own projects; rename/reopen/autosave behave truthfully under failure.
- Desktop/mobile screenshots retain comparable thumbnail prominence and warm restrained hierarchy.

Required Automated Tests:
- Owned dashboard/create/reopen and rename concurrency.
- Autosave failure/reconnect and stale response tests.
- Keyboard/theme/reflow screenshots and empty state.

Manual Verification:
Reviewer independently inspects dashboard in both themes and desktop/mobile against DESIGN.md.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Archive/duplicate, deleted recovery before deletion task or public signup.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T061: Build composer-first New Video and explicit input semantics

Status: NOT_STARTED

Phase: 12 — Creation experience

Objective: Build composer-first New Video and explicit input semantics within the frozen boundaries.

Why: Satisfies the frozen Default topic → video contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T060
- T047
- T043

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Default topic → video**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Pasted script → video**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Optional customization and manual review**
- [docs/DESIGN.md](docs/DESIGN.md), section **Dashboard and New Video**

Likely Files:
- alpha/web/creation.py
- templates/alpha/creation/
- static/alpha/composer.js
- tests/ui/composer/

Requirements:
- Use frozen heading/supporting concept, dominant input, integrated Create Video and See more/less; empty input cannot submit.
- Default idea/instructions with quiet hint; paste opens options but never infers Script; explicit My approved script preserves entered words and switches duration semantics.
- Progressively disclose duration/language/voice/style/captions/motion/music/manual review; preserve choices when collapsed and experimental features stay gated.

Acceptance Criteria:
- No permanent mandatory Topic/Script setup, post-click classification or cost confirmation modal appears.
- Input/selection survives disclosure/theme changes; defaults match frozen scope and disabled controls explain actual gates.

Required Automated Tests:
- Topic/paste/explicit-script switching, empty input and word preservation.
- Optional settings/defaults and no length-based classification.
- Keyboard/mobile/reduced-motion/theme screenshots.

Manual Verification:
Reviewer inspects composer hierarchy and complete mobile form behavior against accepted Direction C.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Suggestion product UI, new advanced mode, custom models/styles or provider calls.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T062: Connect Create Video to bounded durable production plans

Status: NOT_STARTED

Phase: 12 — Creation experience

Objective: Connect Create Video to bounded durable production plans within the frozen boundaries.

Why: Satisfies the frozen Default topic → video contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T061
- T043
- T045
- T050
- T056
- T026
- T023

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Default topic → video**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Authorization, queue and progress**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Plan and admission**

Likely Files:
- alpha/services/production_plan.py
- alpha/web/production.py
- tests/integration/creation/

Requirements:
- Create Video directly authorizes exact bounded submitted input/settings, rechecks ownership/entitlement/storage/coverage and admits a durable job without executing providers in HTTP.
- Compose only frozen applicable research/write/check/scene/image/B/timing/caption/local-render steps; manual review pauses before final render and initial simple path queues it when ready.
- Handle known-script versus topic scope and post-script pauses; expose actual admitted/waiting state and idempotent click behavior.

Acceptance Criteria:
- Offline fake pipeline reaches assets-ready with consumed work preserved and correct manual-review choice; later renderer integration verifies initial auto-render.
- Insufficient/unknown financial authority shows waiting/blocked without submission or falsely holding a lane.

Required Automated Tests:
- Topic entitled/non-entitled and pasted-script operation manifests.
- Duplicate clicks, stale settings, 214 sentence expansion and missing caps.
- No durable HTTP execution, manual pause and queued initial-render contract.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
UI click does not bypass internal finite admission; ordinary execution tests use fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Live generation, mandatory routine script review or auto-rerender after corrections.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T063: Build actual progress, scope approvals and credits/USD Details

Status: NOT_STARTED

Phase: 12 — Creation experience

Objective: Build actual progress, scope approvals and credits/USD Details within the frozen boundaries.

Why: Satisfies the frozen Authorization, queue and progress contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T062
- T031
- T041

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Authorization, queue and progress**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Approvals**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Failure and recovery paths**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Creator estimates and scope**

Likely Files:
- templates/alpha/production/
- static/alpha/progress.js
- tests/ui/progress/

Requirements:
- Show in-place actual stages, completed asset counts, queue/wait/recovery and actionable private factual notices; no fabricated provider percentages or ETA.
- Compact optional Details separates credits/USD estimates, recorded consumption, pending liability, remaining estimate and projected total; unresolved debit stays pending.
- Implement explicit revised-scope/translation/adaptation/factual approvals where required; dismissal never grants consent and completed work survives.

Acceptance Criteria:
- One-tap creation has no mandatory cost-review step while exceptional revised authority still requires approval.
- Unknown cost/credit is not displayed as zero and history usage cannot be mistaken for a current successful export.

Required Automated Tests:
- Waiting/partial/unknown/failed/success stage presentation.
- Consumed plus remaining estimate, pending credit and optional Details.
- Scope approval/dismissal, cross-owner progress and mobile/focus handling.

Manual Verification:
Reviewer inspects concise state clarity and verifies no credit formula or fake progress was invented.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Checkout, upgrade banners, subscription pricing or infrastructure controls for creators.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 13: Correction workspace

### T064: Build desktop scene correction workspace and truthful previews

Status: NOT_STARTED

Phase: 13 — Correction workspace

Objective: Build desktop scene correction workspace and truthful previews within the frozen boundaries.

Why: Satisfies the frozen Production and workspace contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T063
- T014
- T046
- T053
- T004

Source of Truth:
- [docs/DESIGN.md](docs/DESIGN.md), section **Production and workspace**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Scene correction and narration**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**

Likely Files:
- alpha/web/workspace.py
- templates/alpha/workspace/
- static/alpha/workspace.js
- tests/ui/workspace/

Requirements:
- Implement left scene list, central selected preview and right Narration/Visual contexts; stable selection updates all panes.
- Keep selected image/audio preview distinct from full-video playback and previous export; outdated/current states remain explicit.
- Show ready/generating/failed/outdated/review/history and compact readiness links without teaching an artifact graph.

Acceptance Criteria:
- Long scripts/many scenes remain usable and preview never claims a prior export contains current edits.
- Keyboard scene selection/context switching preserves focus and each preview uses authorized exact selected versions.

Required Automated Tests:
- Scene selection, preview source/current-history identity.
- Status/readiness blocker focus and two-user media isolation.
- Desktop both-theme screenshot/layout and keyboard tests.

Manual Verification:
Reviewer independently checks three-column hierarchy, useful density, restrained surfaces and preview truth.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Professional timeline editor or speculative dashboard redesign.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T065: Build narration correction, effective settings and compound history UX

Status: NOT_STARTED

Phase: 13 — Correction workspace

Objective: Build narration correction, effective settings and compound history UX within the frozen boundaries.

Why: Satisfies the frozen Scene correction and narration contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T064
- T055
- T047

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Scene correction and narration**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Version inspection and restoration**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Selection, restoration and concurrent edits**

Likely Files:
- templates/alpha/workspace/narration/
- static/alpha/narration.js
- tests/ui/narration/

Requirements:
- Autosave narration words through guarded invalidation; explain images preserved/review needed and actual affected coherent segment scope before regeneration.
- Show effective voice/delivery versus project default and cached playback; history supports listening and compound different-word/config restoration approvals.
- Current edits during active generation are allowed; valid stale arrival is historical and regeneration is explicit rather than automatic.

Acceptance Criteria:
- Regenerating one member clearly lists affected B scenes; no UI implies a per-scene paid cut.
- Restoring changed words adopts reviewed text/audio together, preserves siblings and displays pending incompatible timing/captions.

Required Automated Tests:
- Edit/keep-image/regenerate scope and concurrent member-edit late arrival.
- Same/different words, effective settings and decline restoration.
- History focus return, keyboard controls and no silent paid side effects.

Manual Verification:
Reviewer listens to fixture previews and checks restoration scope/word agreement visually.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Voice cloning, custom delivery tags or hiding expanded segment scope.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T066: Build image correction, replacement and version restoration UX

Status: NOT_STARTED

Phase: 13 — Correction workspace

Objective: Build image correction, replacement and version restoration UX within the frozen boundaries.

Why: Satisfies the frozen Image regeneration and replacement contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T064
- T017
- T046

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Image regeneration and replacement**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Version inspection and restoration**

Likely Files:
- templates/alpha/workspace/visual/
- static/alpha/visuals.js
- tests/ui/visuals/

Requirements:
- Expose visual description and disclosed generation prompt with current compatibility/review state.
- Wire explicit scoped regeneration, configured validated upload replacement and thumbnail history restoration.
- Preserve earlier compatible image on failure and show missing-image blocker; replacing/restoring must not regenerate narration.

Acceptance Criteria:
- Failed/corrupt uploads/generation never appear as ready selection; prior versions remain inspectable.
- Actual configured upload limits and financial scope are shown without model controls or guessing policies.

Required Automated Tests:
- Prompt edit/incompatibility, explicit keep/retry and preserved narration.
- Upload validation/ownership and selected/history restore.
- Concurrent visual edit, rendering guard and keyboard/sheet focus.

Manual Verification:
Reviewer inspects thumbnail comparison and clear valid/selected/failure separation.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Arbitrary media upload, Style Studio or automatic all-images regeneration.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T067: Build caption, timing, motion/music and scene order corrections

Status: NOT_STARTED

Phase: 13 — Correction workspace

Objective: Build caption, timing, motion/music and scene order corrections within the frozen boundaries.

Why: Satisfies the frozen Captions, timing, motion and music contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T064
- T056
- T057
- T058
- T059
- T055

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Captions, timing, motion and music**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Reorder and delete scenes**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Render, retry and export**

Likely Files:
- templates/alpha/workspace/secondary/
- static/alpha/corrections.js
- tests/ui/corrections/

Requirements:
- Provide secondary caption text/style/toggle, timing fields and approved motion/music controls with real configured limits.
- Implement accessible Move up/down and delete-scene confirmation, using validated assembly/range rules and stable IDs.
- Show blocked unsafe timing/joins and enabled-caption outdated state; keep manual versions for review and no silent regeneration/rerender.

Acceptance Criteria:
- Caption edits never alter narration; caption OFF removes only its readiness blocker.
- Reorder/delete/timing changes preserve compatible assets, update projection and either yield validated readiness or explain required repair.

Required Automated Tests:
- Caption ON/OFF and manual correction preservation.
- Move/delete/timing gap/overlap/cut-off negatives.
- No automatic provider calls, render-only settings and full keyboard actions.

Manual Verification:
Reviewer checks numeric timing fields and explicit correction consequences, not miniature timeline controls.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Scene adding/duplicating, waveform editor, custom motion or Emphasis Text.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T068: Implement complete mobile correction flows

Status: NOT_STARTED

Phase: 13 — Correction workspace

Objective: Implement complete mobile correction flows within the frozen boundaries.

Why: Satisfies the frozen Responsive priorities contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T065
- T066
- T067

Source of Truth:
- [docs/DESIGN.md](docs/DESIGN.md), section **Responsive priorities**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Mobile and accessibility behavior**
- [docs/DESIGN.md](docs/DESIGN.md), section **Accessibility baseline**

Likely Files:
- templates/alpha/workspace/
- static/alpha/responsive.css
- tests/ui/mobile/

Requirements:
- Stack preview above active Narration/Visual view; use accessible scene chooser and secondary history/caption/timing/settings sheets.
- Keep Create, approval, cancellation, recovery, render/download and all meaningful corrections available; explicit reorder/time controls replace drag-only patterns.
- Preserve entered content/focus/selection across sheet navigation and respect keyboard/safe-area/reflow constraints.

Acceptance Criteria:
- No core correction requires desktop and there is no page-wide horizontal overflow at supported narrow/reflow sizes.
- Dialogs return focus and sticky controls do not obscure active fields or software keyboard.

Required Automated Tests:
- Mobile correction, approval/history/reorder and navigation flows.
- Narrow/zoom/long-text screenshots in both themes.
- Focus/reduced-motion/touch targets and preserved input.

Manual Verification:
Reviewer independently exercises mobile browser corrections and inspects screenshots, including long scripts and history.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Shrinking desktop three-column layout intact or separate mobile product semantics.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 14: Prepared public demo

### T069: Build landing carousel and isolated prepared example walkthrough

Status: NOT_STARTED

Phase: 14 — Prepared public demo

Objective: Build landing carousel and isolated prepared example walkthrough within the frozen boundaries.

Why: Satisfies the frozen Landing and demo contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T004
- T064
- T068

Source of Truth:
- [docs/DESIGN.md](docs/DESIGN.md), section **Landing and demo**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Mobile and accessibility behavior**

Likely Files:
- templates/alpha/landing/
- alpha/demo/
- static/alpha/demo.js
- tests/ui/demo/

Requirements:
- Use Try the workflow as primary and invited Sign in secondary; three-image carousel has larger middle image and restrained right-to-left show/pause/advance.
- Build account-free isolated prepared walkthrough from read-only demo-video-example assets with reset and truthful cached playback/progress.
- Public exposure requires permission/privacy/correspondence verification; demo edits cannot change recorded narration or imply new media was generated.

Acceptance Criteria:
- Demo never writes source assets, creates real jobs/reservations, calls providers or leaks private projects.
- Hover/focus/touch/hidden tab/reduced-motion pause rules and manual navigation work; unavailable alternatives are explained honestly.

Required Automated Tests:
- Demo isolation, immutable asset hashes and network/financial traps.
- Prepared media correspondence/missing asset and reset per visitor.
- Carousel accessibility/pause states and both-theme/mobile screenshots.

Manual Verification:
Verify demo publication rights/privacy and listen/check source-scene-caption correspondence before enabling public exposure; otherwise keep it unavailable.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Only explicitly approved demo assets may be public; private project media stays protected.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Publishing this deployment, fabricated regenerated outputs, testimonials/pricing or paid demo generation.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 15: Rendering and exports

### T070: Persist immutable render manifests and transactional content locks

Status: NOT_STARTED

Phase: 15 — Rendering and exports

Objective: Persist immutable render manifests and transactional content locks within the frozen boundaries.

Why: Satisfies the frozen Render manifest contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T067
- T062
- T016

Source of Truth:
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Render manifest**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Project edits, locks and deletion**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Render, retry and export**

Likely Files:
- alpha/models/renders.py
- alpha/rendering/manifests.py
- alpha/rendering/locks.py
- tests/domain/render_contract/

Requirements:
- Create Render and Final Export records separately; immutable manifest pins exact scene order, selected versions/source hashes/timing/settings and contract version.
- Validate missing/invalid/incompatible required assets with disabled-caption exception; revalidate queued manifest at execution and acquire lock atomically.
- Apply centralized mutation guard to all narration/visual/config/restore/approval/reorder/delete mutations; viewing, previous downloads and cancel stay permitted.

Acceptance Criteria:
- Queued rendering does not lock content, but execution locks all content mutations server-side.
- A stale manifest cannot execute without refreshed authorization; no missing/outdated narration export can be admitted.

Required Automated Tests:
- All prohibited mutation classes versus allowed reads/download/cancel.
- Concurrent render-start/edit/delete and double lock claim.
- Manifest hashes/version/order compatibility and enabled/disabled captions.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Lock release requires confirmed controlled execution cessation; uncertain process state stays recovery-guarded.

Out of Scope:
FFmpeg execution, exit-code-only success or modifying selected source versions.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T071: Extract controlled FFmpeg execution and scratch isolation

Status: NOT_STARTED

Phase: 15 — Rendering and exports

Objective: Extract controlled FFmpeg execution and scratch isolation within the frozen boundaries.

Why: Satisfies the frozen Architecture Freeze v1 reuse classification — 2026-10-05 contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T070
- T027

Source of Truth:
- [docs/PIPELINE_INVESTIGATION.md](docs/PIPELINE_INVESTIGATION.md), section **Architecture Freeze v1 reuse classification — 2026-10-05**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Runtime shape**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Render, retry and export**

Likely Files:
- alpha/rendering/process.py
- alpha/rendering/ffmpeg.py
- tests/render/process/

Requirements:
- Extract make_video.py argv/scale/concat ideas behind server-controlled resolved private paths, subprocess groups and structured progress.
- Assign unique scratch reservations/paths, persist process/boot/start identity and support bounded TERM/KILL escalation with confirmed cessation.
- Remove mutable fixed output names, shell interpolation, audio cleanup and file-existence resume; no transactions around subprocess/media work.

Acceptance Criteria:
- Hostile input cannot inject FFmpeg arguments/paths; child groups terminate under cancellation and no orphan remains.
- Interrupted output is private/incomplete while selected source media and prior exports stay intact.

Required Automated Tests:
- Argument/path traversal/injection and safe manifest resolution.
- Real local process group cancellation/escalation/PID identity.
- Crash/full disk/scratch cleanup and execution outside DB transaction.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Local rendering consumes infrastructure, not provider-generation allowance; no generation calls.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Separate render service, pipeline-wide rewrite or host sizing experiments.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T072: Integrate continuous 1080p/30fps rendering with captions and effects

Status: NOT_STARTED

Phase: 15 — Rendering and exports

Objective: Integrate continuous 1080p/30fps rendering with captions and effects within the frozen boundaries.

Why: Satisfies the frozen Runtime contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T071
- T053
- T057
- T058
- T059

Source of Truth:
- [docs/architecture/evidence/rendering-feasibility/S6/README.md](docs/architecture/evidence/rendering-feasibility/S6/README.md), section **Runtime**
- [docs/ARTIFACT_MODEL.md](docs/ARTIFACT_MODEL.md), section **Render manifest**

Likely Files:
- alpha/rendering/encoder.py
- tests/render/encoding/

Requirements:
- Render ordered still-image visual intervals at 1920x1080/30fps MP4 using exact mapping starts, complete continuous narration and validated intentional assembly.
- Integrate gentle motion ON/OFF, shaped PNG captions and optional permitted music with safe mixing and full frame coverage.
- Use corrected disposable Linux timestamp behavior where applicable; no scene boundaries cut ordinary narration and no -shortest completeness inference.

Acceptance Criteria:
- Existing/local 3/5/10-minute fixtures produce expected ordered full-coverage video/audio in disposable paths.
- Caption/motion/music toggles change only rendering; enabled captions are present/readable and music OFF contributes none.

Required Automated Tests:
- Nonuniform next-start scene timing and frame markers.
- Continuous narration sample coverage and effect ON/OFF controls.
- Timestamp/pixel format consistency and malformed/missing required asset rejection.

Manual Verification:
Reviewer inspects decoded beginning/middle/end and representative caption/motion frames; listens to existing speech control.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Advanced video editing, S9/S6 reruns as gates or generating paid fixture assets.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T073: Implement final media validation beyond FFmpeg exit status

Status: NOT_STARTED

Phase: 15 — Rendering and exports

Objective: Implement final media validation beyond FFmpeg exit status within the frozen boundaries.

Why: Satisfies the frozen Runtime contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T072

Source of Truth:
- [docs/architecture/evidence/rendering-feasibility/S6/README.md](docs/architecture/evidence/rendering-feasibility/S6/README.md), section **Runtime**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Render, retry and export**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Quality evidence**

Likely Files:
- alpha/rendering/validation.py
- tests/render/validation/

Requirements:
- Validate full decode/playability, MP4 dimensions/fps, expected duration/scene order/coverage, complete narration and no unintended blank gaps.
- Validate readable enabled captions and narration/music clipping/truncation against source/mapping contract; preserve intended silence.
- Use declared reproducible tolerances linked to render contract, not permissive values chosen after failures; exit 0/-shortest is insufficient.

Acceptance Criteria:
- Damaged, truncated, wrong fps/dimension/order, blank visual and missing-audio fixtures cannot become Final Export.
- Caption OFF is accepted when other required timing remains valid; legitimate pauses are not mistaken for missing narration.

Required Automated Tests:
- Full damaged-media fixture matrix and all-frame representative order coverage.
- Audio sample/duration/coverage versus real silence and clipped mix.
- Caption bounds/glyphs/ON-OFF and predeclared timestamp tolerance.

Manual Verification:
Independent decoded frame inspection and fixture playback; subjective publishability remains owner-validation evidence.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Calling technically valid output publishable or silently dropping narration to pass.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T074: Publish validated exports and complete simple/manual rendering UX

Status: NOT_STARTED

Phase: 15 — Rendering and exports

Objective: Publish validated exports and complete simple/manual rendering UX within the frozen boundaries.

Why: Satisfies the frozen Render, retry and export contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T073
- T030
- T063
- T064

Source of Truth:
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Render, retry and export**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**

Likely Files:
- alpha/rendering/publication.py
- alpha/web/exports.py
- templates/alpha/exports/
- tests/integration/exports/

Requirements:
- Register immutable validated Final Export and release lock only after confirmed cessation; preserve every last successful export on failure/cancel.
- Complete initial Simple Mode auto-render integration when current ready; manual review requires explicit Render and later corrections never auto-rerender.
- Offer protected download/history with date/version context and Before your latest changes label; render retry reuses source assets without generation allowance.

Acceptance Criteria:
- Initial offline topic/pasted pipelines reach validated export in simple mode and pause in manual mode.
- New failed render does not replace successful export; history download stays available during edit/render/cancel.

Required Automated Tests:
- End-to-end simple/manual initial and explicit correction render.
- Publication crash/validation failure and previous-export preservation.
- Protected ranges, lock release and no provider debit on render retry.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
YouTube publishing, public sharing or treating prior export as current content.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 16: Cancellation, recovery and security

### T075: Integrate cancellation across provider and local process phases

Status: NOT_STARTED

Phase: 16 — Cancellation, recovery and security

Objective: Integrate cancellation across provider and local process phases within the frozen boundaries.

Why: Satisfies the frozen Retry and cancellation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T074
- T029
- T051

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Retry and cancellation**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Failure and recovery paths**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **One active production lane**

Likely Files:
- alpha/jobs/cancel_execution.py
- tests/worker/cancellation/

Requirements:
- Wire durable cancel intent to queued, active provider, local alignment and render execution, with actual stopped-state confirmation.
- Use only verified provider cancellation capability; unknown possible remote execution retains lane and liability; no further steps start.
- Late valid paid output after cancel is registered/delivered as history and accounted once; partial successes remain available.

Acceptance Criteria:
- Queued cancel never submits; local active cancel stops all children before unlock/lane release.
- Unknown provider cancel does not claim refund/cessation and cannot blindly retry or permit overlapping production.

Required Automated Tests:
- Queued/alignment/render group cancel and cleanup latency evidence.
- Possible-accepted provider cancellation, late valid/invalid outputs.
- Repeated cancel and canceled success registration/financial reconciliation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Cancellation cannot erase paid or unresolved exposure.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Assuming provider cancel refunds cost or releasing locks on timeout alone.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T076: Implement restart reconciliation across jobs, media, finance and renders

Status: NOT_STARTED

Phase: 16 — Cancellation, recovery and security

Objective: Implement restart reconciliation across jobs, media, finance and renders within the frozen boundaries.

Why: Satisfies the frozen Idempotency and checkpoints contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T075
- T030
- T027

Source of Truth:
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Idempotency and checkpoints**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Failure matrix**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**

Likely Files:
- alpha/jobs/recovery.py
- alpha/management/commands/reconcile_execution.py
- tests/worker/restart/

Requirements:
- Reconcile worker/web restart, prepared/submitted/unknown attempts, response spools, installed/unregistered files and stale ownership using persisted evidence.
- Resume only proven safe remaining work; retain unknown liabilities and reuse recovered paid output rather than duplicate submission.
- Recover render locks through confirmed process state, preserving previous exports and preventing permanent abandoned lock or overlapping execution.

Acceptance Criteria:
- Crash-point restart tests produce no duplicate paid request, lost liability or false successful artifact.
- Successful committed outputs survive and relevant new inputs require refreshed authority before queued continuation.

Required Automated Tests:
- Before/after submission/install/registration/settlement/lock crash matrix.
- Stale worker/reused PID/boot evidence and unknown remote execution.
- Resumed local render reuse, no permanent lock and source preservation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Automatic unknown settlement, orchestrator implementation or external paid recovery experiments.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T077: Harden cross-cutting ownership, media, lock and financial races

Status: NOT_STARTED

Phase: 16 — Cancellation, recovery and security

Objective: Harden cross-cutting ownership, media, lock and financial races within the frozen boundaries.

Why: Satisfies the frozen Authentication and isolation contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T076
- T017
- T055

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Authentication and isolation**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Project edits, locks and deletion**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**

Likely Files:
- tests/security/
- alpha/authorization.py
- affected subsystem fixes only

Requirements:
- Independently exercise cross-user/role/CSRF/media range/upload/path/FFmpeg and client-entitlement/credit bypass attempts.
- Test stale-worker submission, render-lock bypass, deletion intent races and concurrent finance/reservation attacks against implemented boundaries.
- Fix only discovered regressions within frozen contracts; security findings cannot be deferred because happy paths pass.

Acceptance Criteria:
- No tested bypass exposes another creator media/content or performs an unauthorized mutation/submission.
- Negative-path suite proves shared authority and lock checks remain enforced through all public/service entry points.

Required Automated Tests:
- Two-identity object-ID/range/upload/CSRF security matrix.
- Stale-fence/concurrent reservation/credit-entitlement injection.
- All render mutation paths including restore, accepted corrections and deletion.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
New auth vendor, penetration of external systems or unrelated refactors.

Reviewer Notes:
Reviewers inspect negative paths and transaction races independently; test success alone is insufficient if an uncovered unsafe entry point exists.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 17: Retention and maintenance

### T078: Implement recoverable deletion and independent deletion authority

Status: NOT_STARTED

Phase: 17 — Retention and maintenance

Objective: Implement recoverable deletion and independent deletion authority within the frozen boundaries.

Why: Satisfies the frozen Rendering and project lifecycle contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T077
- T005

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Project lifecycle and allowance access**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **Project edits, locks and deletion**

Likely Files:
- alpha/retention/deletion.py
- alpha/retention/journal.py
- tests/integration/deletion/

Requirements:
- Require confirmation, hide eligible project immediately and atomically cancel never-started queued work; active/unknown work requires cancel and confirmed cessation first.
- Persist independently recoverable non-content deletion journal/current head before acknowledging deletion; ambiguous journal failure fails closed.
- Allow recovery for seven days without restarting canceled paid jobs; retain necessary non-content accounting/liabilities/audit and announced Alpha-end plus 14-day download state.

Acceptance Criteria:
- Deleted content cannot be read through private media routes; valid seven-day recovery restores content but no spending authority.
- Race between delete/start cannot launch work for deleted project; expired recovery is rejected.

Required Automated Tests:
- Seven-day boundary, immediate hide, media access and recovery.
- Delete/claim/render/unknown-outcome races.
- Journal write/head ambiguity and Alpha-end 14-day handling.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Do not acknowledge recoverable deletion without durable authority; keep access blocked if journal/head is uncertain.

Out of Scope:
Historical backup purge implementation or deleting necessary financial records.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T079: Implement bounded encrypted consistent backup snapshots

Status: NOT_STARTED

Phase: 17 — Retention and maintenance

Objective: Implement bounded encrypted consistent backup snapshots within the frozen boundaries.

Why: Satisfies the frozen Development and invited deployment contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T078
- T016
- T076

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Media and storage**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**

Likely Files:
- alpha/maintenance/backup.py
- alpha/maintenance/backup_destination.py
- tests/integration/backup/

Requirements:
- Build consistent SQLite snapshot plus immutable media manifest with authenticated encryption and separately recoverable deletion authority/key metadata.
- Implement a narrow off-machine destination abstraction and local fake destination; preserve licenses/secrets separation and verify bounds before allocation/upload.
- Require archive/input/working-memory and remote stored-version/transfer limits independently of disk capacity; size-proportional unbounded in-memory archive is forbidden.

Acceptance Criteria:
- Snapshot restores matching DB/media hashes and tampering/wrong key is rejected.
- Missing/insufficient byte/memory/transfer bounds prevents backup commitment; no automatic paid overage or assumption of permanent free storage.

Required Automated Tests:
- Concurrent local writes versus consistent snapshot.
- Archive/header/manifest/version bytes and memory-preflight edge cases.
- Encryption/authentication, failed upload and bounded destination contract.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Backup obligations count operating budget; fake destination only until operational gate.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Selecting/provisioning backup vendor or claiming local destination proves off-machine readiness.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T080: Implement fail-closed restore and financial reconciliation

Status: NOT_STARTED

Phase: 17 — Retention and maintenance

Objective: Implement fail-closed restore and financial reconciliation within the frozen boundaries.

Why: Satisfies the frozen Failure, restoration and limits of enforcement contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T079
- T021

Source of Truth:
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Failure, restoration and limits of enforcement**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**

Likely Files:
- alpha/maintenance/restore.py
- tests/integration/restore/

Requirements:
- Verify snapshot/immutable media/key integrity and independently current deletion authority before granting restored content access.
- Keep paid work paused until actual spend/reservations/unresolved liabilities and execution state are reconciled; restored stale balance cannot recreate money.
- Provide operator evidence/reconciliation workflow with preserved audit history, no inferred refunds or deleted-project resurrection.

Acceptance Criteria:
- Older valid snapshot cannot restore purged content or enable unreconciled paid jobs.
- Missing/ambiguous current journal/key/provider financial evidence produces safe blocked restore state.

Required Automated Tests:
- Old snapshot versus current deletion head and missing/tampered authority.
- Restored ledger with out-of-snapshot paid spend/liability.
- Key loss, media mismatch and reconciliation idempotency.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Purchasing key custody service or declaring remote restore verified.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T081: Implement seven-day content purge and next-cycle backup purge

Status: NOT_STARTED

Phase: 17 — Retention and maintenance

Objective: Implement seven-day content purge and next-cycle backup purge within the frozen boundaries.

Why: Satisfies the frozen Rendering and project lifecycle contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T080
- T078

Source of Truth:
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Project lifecycle and allowance access**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**

Likely Files:
- alpha/retention/purge.py
- tests/integration/purge/

Requirements:
- Purge active project content after seven days; purge every historical backup/object version on next daily cycle within at most 24 additional hours.
- Keep purge execution independent of new-backup success and maintain current anti-resurrection journal/head.
- Preserve only necessary non-content financial/deletion/audit data, including unresolved liability; storage accounting reconciles retained/purged bytes.

Acceptance Criteria:
- Backup creation failure does not postpone deletion deadlines and restored older snapshots cannot resurrect purged content.
- Destinations without verified historical-version purge remain ineligible for invitation configuration.

Required Automated Tests:
- Deadline clock and failed new backup versus purge execution.
- All historical versions/metadata/keys-content references and no resurrection.
- Partial purge retry/status, remaining liability and storage reconciliation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Surface unfulfilled purge as operational failure; never promise deletion succeeded while copies remain.

Out of Scope:
Silent pruning for capacity or deleting immutable finance authority.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T082: Implement serialized daily maintenance and health checks

Status: NOT_STARTED

Phase: 17 — Retention and maintenance

Objective: Implement serialized daily maintenance and health checks within the frozen boundaries.

Why: Satisfies the frozen Development and invited deployment contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T081
- T026
- T031

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**
- [docs/JOB_EXECUTION_MODEL.md](docs/JOB_EXECUTION_MODEL.md), section **One active production lane**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Rendering and project lifecycle**

Likely Files:
- alpha/maintenance/coordinator.py
- alpha/management/commands/run_maintenance.py
- tests/worker/maintenance/

Requirements:
- Coordinate memory-heavy backup with the same heavy-work exclusion used for render/alignment, without adding another scheduler service.
- Provide daily encrypted backup/purge execution, due/failure/lag health and <=24-hour catastrophic-loss objective monitoring.
- Bound working-set/storage/transfer before maintenance and retain independent purge progress even if backup fails.

Acceptance Criteria:
- Backup cannot overlap memory-heavy production; progress/owner health records distinguish overdue backup and failed purge.
- No backup absence or budget exhaustion is hidden as a completed maintenance cycle.

Required Automated Tests:
- Production/backup concurrent acquisition and restart fencing.
- Due/overdue/failure clocks and independent purge scheduling.
- Input-memory/remote-transfer cap and missing configuration.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
Configured backup/traffic costs remain inside shared $40 budget; no actual remote calls in ordinary tests.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Additional host sizing experiments, silent concurrency policy change or buying services.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 18: Operational activation

### T083: Implement minimal owner operating controls and activation audit

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Implement minimal owner operating controls and activation audit within the frozen boundaries.

Why: Satisfies the frozen Observability contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T082
- T031
- T035

Source of Truth:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Observability**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Current S9 planning envelope**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**

Likely Files:
- alpha/admin.py
- alpha/operations/controls.py
- tests/security/owner_controls/

Requirements:
- Use Django admin or similarly small operator surface for invited accounts, entitlements, authority/coverage, storage, provider enablement, attempt/liability and backup health.
- Require auditable role-checked changes and documented rate/cap/config versions; unknown required values stay disabled.
- Provide halt-new-paid-work incident control and safe reconciliation inspection, keeping creator UX free of infrastructure controls.

Acceptance Criteria:
- Owner can inspect and pause authoritative state without editing history or granting budget beyond active period ceiling.
- Tester/admin forgery cannot activate providers, alter money/caps or reconcile liabilities.

Required Automated Tests:
- Role matrix, config/audit idempotency and secret redaction.
- Ceiling lowering, unresolved liabilities and pending capability controls.
- Owner halt versus active paid/maintenance execution preservation.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Large SaaS admin dashboard, final allowance selection or public billing.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T084: Gate live text and research/search capability activation

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Gate live text and research/search capability activation within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T083
- T042
- T038
- T034

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/architecture/evidence/research-feasibility/S4-R.md](docs/architecture/evidence/research-feasibility/S4-R.md), section **Recommended complete flow**
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md), section **Provider financial bound used in the planning proof**

Likely Files:
- operational text/search capability records
- alpha/providers/activation.py
- tests/integration/activation/

Requirements:
- Require explicit owner normal-text model adoption; retain candidate status until chosen, with no silent substitute.
- Before enabling text/search, verify account/privacy/terms/quota, current all-in rates, complete input/output/thinking/query/tool bounds, one-send behavior, identifiers/timeouts and financial certainty.
- Use existing evidence where applicable and reviewed current endpoint proof; absent reliable complete maximum keeps relevant operation disabled. No free quota reliance.

Acceptance Criteria:
- Reviewer verifies each certificate and runtime enforcement supports the actual chosen endpoint/model, not merely fake proof.
- Unverified text/search cannot submit, while completed fake-provider development remains usable.

Required Automated Tests:
- Certificate completeness/expiry/model/account/output/thinking/query enforcement.
- Hidden send/retry and unknown-outcome contract fixtures.
- Enable/revoke versus stored quotes/reservations and no unauthorized activation.

Manual Verification:
Owner decision and supported current account/endpoint evidence required. External validation needs separate explicit authorization and bounded cash authority; absent evidence returns TASK_BLOCKED.

Financial / Provider Impact:
This gate is not permission to make generation calls, buy credits or create accounts; any live work requires separate owner authorization.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
S9 reopening, buying provider access or adopting optional discovery models.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T085: Gate live image capability activation

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Gate live image capability activation within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T083
- T045
- T034

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Provider capabilities**
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md), section **Provider financial bound used in the planning proof**

Likely Files:
- operational image capability record
- tests/integration/activation/images/

Requirements:
- Verify selected gemini-3.1-flash-lite-image endpoint/account support and every input/output/thinking/reference/modality/turn/request charge dimension.
- Prove complete enforceable per-attempt maximum, output resource validation, one-send/timeouts/unknown outcome behavior and current rate provenance.
- Keep output-only $0.0336 sensitivity distinct from full cap; fake images and S6 synthetic frames are not evidence of real provider quality.

Acceptance Criteria:
- No image submission is enabled by a partial tariff, unknown dimension or assumed free-tier capacity.
- Certificate and financial manifest reflect actual supported request contract and expire/revoke safely.

Required Automated Tests:
- Incomplete modality/reference/thinking cap and expired price rejection.
- One qualifying output versus expanded candidates/turns.
- Activation/revocation/quote invalidation and pending unknown liability.

Manual Verification:
Owner provides supported account/endpoint/billing evidence. Real generation, if needed, is separately authorized and bounded; otherwise TASK_BLOCKED, not invented certification.

Financial / Provider Impact:
No automatic paid request or purchase from this gate.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Provider image-quality calibration, empirical failure rates or model substitution.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T086: Gate live coherent TTS capability and voice activation

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Gate live coherent TTS capability and voice activation within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T083
- T050
- T047
- T034

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Narration segment authorization — accepted amendment**
- [docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md](docs/architecture/evidence/operating-economics/S9/CREDITS-v14.md), section **Provider financial bound used in the planning proof**

Likely Files:
- operational TTS capability record
- tests/integration/activation/tts/

Requirements:
- Verify selected gemini-3.8-flash-lite-tts account/endpoint, supported effective voices/delivery/audio format and complete input/audio-output/thinking/request limits.
- Revalidate current tariff including introductory expiry, hidden retry behavior, request identities, unknown billing and segment-level financial maxima.
- Enabled B groups must fit proven complete prepared-request bounds; no silent per-scene/fallback generation.

Acceptance Criteria:
- Expired pricing or incomplete TTS scope blocks activation; supported voice preview metadata does not grant spending authority.
- Each enabled segment has current certificate/config/maximum and compatible validated output/mapping workflow.

Required Automated Tests:
- Rate expiry, unsupported voice/format and complete bounds.
- B membership/output duration/request fallback rejection.
- Certificate revocation, segment quote changes and unknown outcome.

Manual Verification:
Owner supplies account/voice/format/billing proof and separately authorizes any needed live verification. No credits purchase required by plan itself.

Financial / Provider Impact:
Live generation remains separately authorized, never an automatic gate side effect.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Speech quality acceptance for 10 projects or changing selected narration architecture.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T087: Gate bounded invited-host, cash, storage and transfer configuration

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Gate bounded invited-host, cash, storage and transfer configuration within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T084
- T085
- T086
- T083
- T082

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/COST_MODEL.md](docs/COST_MODEL.md), section **Current S9 planning envelope**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**

Likely Files:
- operational configuration/runbook
- tests/integration/operational_bounds/

Requirements:
- Require owner-supplied deployment/backup/private access choices on locally qualified 2-vCPU/4-GiB class; no vendor selection or host-sizing experiment by Codex.
- Record supported all-in fixed obligations, tax/payment/FX/reserve/carried-liability coverage, included disk/egress and bounded in-flight transfer with no automatic upgrades.
- Require approved retained-version/scratch/archive/memory/storage caps and current $40 Asia/Dhaka authority; use V14 amounts only as planning sensitivity.

Acceptance Criteria:
- Unknown required cash/infrastructure/transfer bound blocks paid commitment or invitations rather than being treated zero.
- Configuration fits supported total exposure, preserves serialized heavy maintenance and does not turn tier names into allowances.
- Owner-provided environment evidence confirms persistent Linux runtime, supervised web/worker/maintenance, protected access/TLS and restart configuration; a price quote alone is insufficient.

Required Automated Tests:
- $40 envelope exact arithmetic, unknown coverage and negative residual.
- Fixed-versus-variable/reservation separation and 3/5/10 qualification.
- Configured bytes/memory/transfer including backup historical versions and in-flight exposure.
- Operational environment-manifest and service/health/restart evidence validation without reopening host sizing.

Manual Verification:
Owner provides chosen operational configuration and supported quotes/terms; no provider/host is selected by this task. Provisioning/deployment/purchases require separate authorization outside the gate.

Financial / Provider Impact:
Required coverage C is supported/configured, not guessed reserve percentage; no commitment during review without owner authorization.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Renting/provisioning cloud, changing ceiling or final commercial policy.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T088: Gate actual off-machine backup, restore, key recovery and purge

Status: NOT_STARTED

Phase: 18 — Operational activation

Objective: Gate actual off-machine backup, restore, key recovery and purge within the frozen boundaries.

Why: Satisfies the frozen Remaining decisions and activation prerequisites contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T087
- T080
- T081

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), section **Development and invited deployment**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Reliability and access evidence**

Likely Files:
- operational backup/restore/purge evidence
- tests/integration/destination_contract/

Requirements:
- Require an owner-provided separately authorized off-machine destination/deployment, permitted bounded transfer and independent journal/head/key custody.
- Verify actual daily snapshot retrieval/restore, current financial reconciliation, key recovery and deletion of all historical copies within required deadline.
- Local fake/S8 protocol PASS is insufficient for this invitation gate; verify monitoring and response to destination failure/quota exhaustion.

Acceptance Criteria:
- Reviewer can verify recorded actual remote restore/purge evidence and <=24-hour objective procedure without a fabricated remote receipt.
- Unsupported destination purge/version/cost semantics keep invitations blocked and paid resume disabled after restore.

Required Automated Tests:
- Destination contract negative fixtures: unknown version purge, quotas, key/head and tamper.
- Restore reconciliation and anti-resurrection integration.
- Daily due/failure monitoring and serialized-maintenance tests.

Manual Verification:
Actual off-machine restore/purge evidence is necessary. Owner must separately authorize environment and any remote operations; unavailable environment is TASK_BLOCKED.

Financial / Provider Impact:
All remote storage/read/retry/traffic exposure is pre-authorized inside $40; this task does not authorize purchase or provisioning.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Vendor selection, deployment or treating local backup as remote acceptance.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.


## Phase 19: Owner validation and readiness

### T089: Implement owner-validation records and quality rubric reporting

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Implement owner-validation records and quality rubric reporting within the frozen boundaries.

Why: Satisfies the frozen Quality evidence contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T074
- T077
- T082

Source of Truth:
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Quality evidence**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Reliability and access evidence**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Measured invitation limits**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted narration fidelity amendment — 2026-10-05**

Likely Files:
- alpha/validation/records.py
- alpha/validation/report.py
- tests/integration/owner_validation/

Requirements:
- Record ten-project inputs/durations/features, technical validation, private factual findings, narrative/visual/audio defects, active correction time and publishable judgment.
- Capture actual/pending costs, paid failures/retries, regeneration, N/images, text/TTS usage, correction costs, storage/render time/traffic/unknown outcomes with certainty/provenance.
- Evaluate ≥8/10 publishable within ≤15 active correction minutes each, treating disabled captions and accepted minor variations correctly; no fabricated measured values.

Acceptance Criteria:
- Report distinguishes completeness, quality judgment and cost certainty; synthetic trials cannot count toward real English acceptance.
- Missing evidence fails the affected acceptance/calibration record rather than defaulting to zero or publishable.

Required Automated Tests:
- Quality rubric,8/10 threshold/time boundaries and defect classification.
- Pending receipts/correction/traffic fields and no fake empirical data.
- Topic/pasted/duration coverage and reproducible report.

Manual Verification:
None; automated evidence is sufficient.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Executing real projects, deciding credit formula/pricing or reopening S9.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T090: Verify complete offline Alpha journeys and visual/accessibility quality

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Verify complete offline Alpha journeys and visual/accessibility quality within the frozen boundaries.

Why: Satisfies the frozen Scope and frozen boundaries contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T089
- T069
- T068
- T076
- T081

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Scope and frozen boundaries**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Quality evidence**
- [docs/UX_FLOWS.md](docs/UX_FLOWS.md), section **Mobile and accessibility behavior**

Likely Files:
- tests/end_to_end/
- tests/ui/
- regression fixes within active scope

Requirements:
- Run complete fake topic/pasted creation, manual/simple render, selective corrections/history, stale edit, cancel/restart, budget/storage block and deletion/recovery/purge journeys.
- Independently inspect desktop/mobile both-theme screenshots against Warm Creator/Direction C; ensure all core controls and focus paths work.
- Verify prepared demo isolation, ownership, finance, media coverage and operational negative paths in full regression without external calls.

Acceptance Criteria:
- All required offline journeys preserve assets, locks, authorizations and honest UI state; no critical security/financial failure remains.
- Screenshots/browser review show composer dominance, three-column desktop, stacked mobile, contrast/reflow/reduced motion and no forbidden generic AI decorations.

Required Automated Tests:
- Full offline E2E journey matrix and network trap.
- Cross-user security/finance/storage/deletion/render-lock regression.
- Browser desktop/mobile, keyboard, reduced-motion and screenshot suite.

Manual Verification:
Independent reviewer exercises browser journeys and inspects screenshots; fixture render playback is technical evidence, not real-project publishability.

Financial / Provider Impact:
NONE in task execution: external provider calls are prohibited; use local fixtures/fakes.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Live generation, new design direction or invitation authorization.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T091: Gate ten real English owner-validation projects

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Gate ten real English owner-validation projects within the frozen boundaries.

Why: Satisfies the frozen Quality evidence contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T090
- T084
- T085
- T086

Source of Truth:
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Quality evidence**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Reliability and access evidence**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Product range and financial admission**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner-accepted narration fidelity amendment — 2026-10-05**

Likely Files:
- owner-validation evidence records
- quality/cost/reliability report

Requirements:
- After separate explicit owner authorization and finite per-project budgets, record ten real English 16:9 topic/pasted projects spanning 3–10 minutes; trials may span calendar months but each admission obeys that month’s $40 authority.
- Owner-local trials may precede invited-host/remote setup, but must have supported coverage of their actual monthly obligations. Owner evaluates publishability/correction time; reviewer independently verifies technical/quality evidence including narration fidelity and serious factual failures.
- Demonstrate interrupted resumption, targeted failed-image retry, unaffected asset preservation, isolation and financial authority; financially inadmissible10-minute fallback must be replanned or independently admitted within $40, never bypassed.

Acceptance Criteria:
- At least 8/10 are publishable with ≤15 active correction minutes each and required input/duration coverage has genuine evidence.
- Actual cost/quality/retry/correction/storage/traffic measurements are recorded honestly; absent funded/admissible real trials keep gate blocked.

Required Automated Tests:
- Validation-report threshold, evidence completeness and duration/input coverage.
- Reliability/isolation/allowance scenarios independently rerun offline.
- Per-trial admission and $40 accounting consistency.

Manual Verification:
Ten real projects require owner participation and independent review. Each live request must be separately authorized; cannot substitute fake media or auto-buy credits.

Financial / Provider Impact:
No blanket spend authority. Real provider work is prohibited until separately owner-authorized with current certificates, scope and coverage.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Automatic provider purchase, invitations or choosing final commercial economics.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T092: Gate measured temporary Alpha allocations and operating windows

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Gate measured temporary Alpha allocations and operating windows within the frozen boundaries.

Why: Satisfies the frozen Measured invitation limits contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T091
- T087

Source of Truth:
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Measured invitation limits**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Owner decision — Research entitlement and topic discovery, 2026-10-05**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**

Likely Files:
- owner-approved Alpha operating configuration
- tests/integration/alpha_limits/

Requirements:
- Require explicit owner-assigned temporary successful-output USD allowances and account entitlements for approximately 3–5 invited creators based on measurements.
- Record approved storage/transfer/backup working limits, availability windows, Alpha end date and 14-day download notice.
- Keep shared authority hard-bound;3/week and1/day eligibility is not a promise of free theoretical throughput; credits remain pending product abstraction.

Acceptance Criteria:
- Each account has recorded compatible bounded allowance/entitlement and no allocation can override shared40-dollar authority.
- Absent assignments/windows/end/cap configuration blocks readiness; no guessed numerical allocation is applied.

Required Automated Tests:
- Missing owner allocation/entitlement and forged tier labels.
- Shared exhaustion versus remaining creator allowance.
- End-window notices/storage limits and immutable assignment audit.

Manual Verification:
Owner explicitly assigns measured temporary allowances/entitlements/windows; reviewer verifies records and enforcement, not invented policy.

Financial / Provider Impact:
Owner assignments remain subject to financial admission; no credit conversion or subscription quantity is decided.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Commercial pricing/rollover/overage and promising full tier capacity.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T093: Conditional gate for each experimental language enablement

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Conditional gate for each experimental language enablement within the frozen boundaries.

Why: Satisfies the frozen Non-English availability contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T091
- T057
- T041

Source of Truth:
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Non-English availability**
- [docs/ALPHA_PRODUCT_SPEC.md](docs/ALPHA_PRODUCT_SPEC.md), section **Language**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**

Likely Files:
- per-language capability validation records
- tests/integration/language_enablement/

Requirements:
- Conditional branch only, outside core invitation dependencies; leave NOT_STARTED until separately requested. English remains the validated default.
- For each Spanish/French/Bangla/Hindi language independently verify selected-language script/approved translation, narration fidelity, caption glyph/timing/display and exported MP4.
- Enable only that verified language with evidence/versioned configuration; S6 technical glyph PASS alone does not prove end-to-end quality.

Acceptance Criteria:
- Unverified languages remain experimental disabled; one language approval never enables all four.
- Core English readiness can pass while this task remains NOT_STARTED; failed non-English check does not invent English regression.

Required Automated Tests:
- Per-language certificate/enablement/expiry and cross-language no-promotion.
- Narration/caption/export records and translation consent.
- Default English unchanged and readiness independence.

Manual Verification:
Language-specific real narration/export review needs separate owner authorization; no provider calls without it.

Financial / Provider Impact:
Optional validation separately authorized/bounded; not core invitation spending requirement.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
All-five-language publishability claim or invitations blocked solely on non-English.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

### T094: Gate Private Alpha invitation readiness without inviting or deploying

Status: NOT_STARTED

Phase: 19 — Owner validation and readiness

Objective: Gate Private Alpha invitation readiness without inviting or deploying within the frozen boundaries.

Why: Satisfies the frozen Scope and frozen boundaries contract and provides the independently reviewable capability needed by dependent tasks.

Dependencies:
- T092
- T088

Source of Truth:
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Scope and frozen boundaries**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Reliability and access evidence**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Measured invitation limits**
- [docs/VALIDATION_PLAN.md](docs/VALIDATION_PLAN.md), section **Quality evidence**
- [docs/architecture/ARCHITECTURE_FREEZE.md](docs/architecture/ARCHITECTURE_FREEZE.md), section **Remaining decisions and activation prerequisites**

Likely Files:
- readiness evidence report
- tests/integration/readiness/

Requirements:
- Verify all mandatory predecessor tasks independently PASS, including owner trials, actual remote backup/restore/purge, storage/allowances/windows and verified live provider bounds.
- Require authentication/isolation, finance/coverage, private media, deletion, output validation, cancel/restart, monitoring and English quality with no critical unresolved security failure.
- Report readiness only; no invitations, deployment, vendor purchase, subscription policy or next task begins automatically. Optional language task is not required.

Acceptance Criteria:
- Gate fails closed on any missing/invalid prerequisite or unresolved operational blocker; evidence maps each invitation requirement to actual independent acceptance.
- PASS means ready for separately authorized invitations, not invitation sending/deployment, commercial profitability or unlimited generation.

Required Automated Tests:
- Readiness checklist with each missing/expired/failed prerequisite.
- Independent PASS/status/evidence references and no self-acceptance.
- Optional-language exclusion and hard40-dollar configuration.

Manual Verification:
Independent reviewer audits real owner/remote operational evidence and confirms owner-configured prerequisites; owner separately authorizes any invitations/deployment.

Financial / Provider Impact:
Readiness does not grant spending beyond persisted period/project/creator authority.

Security / Ownership Impact:
Server-side ownership and role checks apply to all exposed project records and actions; never trust client ownership or plan claims.

Failure / Recovery Behavior:
Reject invalid input/state without losing committed work; report the tested failure clearly.

Out of Scope:
Actually inviting users, deploying, choosing vendors or executing deferred features.

Reviewer Notes:
Independently inspect the diff and listed negative-path tests against the cited contracts; do not infer acceptance from Codex evidence.

Completion Authority:
- Codex may implement the task.
- Codex may NOT mark it accepted.
- Acceptance requires independent reviewer PASS.

## Dependency summary and critical path

Dependencies, not visual order, are authoritative. The file has a topological default order. A dependency is required independent PASS, not “code exists.” Core readiness requires every mandatory task's transitive completion; the conditional experimental-language task is excluded. A decision/evidence gate may remain blocked until owner input is supplied; do not mark it passed to advance the plan.

| Task | Direct dependencies |
| --- | --- |
| T001 | None |
| T002 | T001 |
| T003 | T001, T002 |
| T004 | T001, T003 |
| T005 | T002, T003 |
| T006 | T005 |
| T007 | T006 |
| T008 | T006 |
| T009 | T006, T008 |
| T010 | T006, T008 |
| T011 | T005, T004 |
| T012 | T011, T008, T009, T010 |
| T013 | T008, T012 |
| T014 | T013, T011 |
| T015 | T013 |
| T016 | T013, T005 |
| T017 | T015, T016, T014 |
| T018 | T002, T012 |
| T019 | T018, T005 |
| T020 | T019 |
| T021 | T020, T008 |
| T022 | T019, T020, T006, T007 |
| T023 | T022, T021, T006, T007 |
| T024 | T023 |
| T025 | T021, T005, T008 |
| T026 | T025, T020 |
| T027 | T026, T002 |
| T028 | T027, T024, T025 |
| T029 | T028 |
| T030 | T028, T013, T021 |
| T031 | T030, T004, T012 |
| T032 | T028, T030, T003 |
| T033 | T032, T029 |
| T034 | T033, T022 |
| T035 | T034, T012 |
| T036 | T030, T006, T010 |
| T037 | T035, T036, T009, T032 |
| T038 | T037, T033, T016 |
| T039 | T038, T009 |
| T040 | T039, T006 |
| T041 | T040, T036, T023 |
| T042 | T007, T039, T032, T041 |
| T043 | T042, T007, T036 |
| T044 | T043, T033, T034 |
| T045 | T044, T030, T016, T036 |
| T046 | T045, T017 |
| T047 | T010, T035, T014 |
| T048 | T043, T047, T022 |
| T049 | T048, T033, T034 |
| T050 | T049, T030, T036 |
| T051 | T050, T027 |
| T052 | T051, T010 |
| T053 | T052 |
| T054 | T053 |
| T055 | T054, T036, T041 |
| T056 | T053, T055 |
| T057 | T056, T035 |
| T058 | T036, T043 |
| T059 | T036, T035 |
| T060 | T012, T004, T005, T031 |
| T061 | T060, T047, T043 |
| T062 | T061, T043, T045, T050, T056, T026, T023 |
| T063 | T062, T031, T041 |
| T064 | T063, T014, T046, T053, T004 |
| T065 | T064, T055, T047 |
| T066 | T064, T017, T046 |
| T067 | T064, T056, T057, T058, T059, T055 |
| T068 | T065, T066, T067 |
| T069 | T004, T064, T068 |
| T070 | T067, T062, T016 |
| T071 | T070, T027 |
| T072 | T071, T053, T057, T058, T059 |
| T073 | T072 |
| T074 | T073, T030, T063, T064 |
| T075 | T074, T029, T051 |
| T076 | T075, T030, T027 |
| T077 | T076, T017, T055 |
| T078 | T077, T005 |
| T079 | T078, T016, T076 |
| T080 | T079, T021 |
| T081 | T080, T078 |
| T082 | T081, T026, T031 |
| T083 | T082, T031, T035 |
| T084 | T083, T042, T038, T034 |
| T085 | T083, T045, T034 |
| T086 | T083, T050, T047, T034 |
| T087 | T084, T085, T086, T083, T082 |
| T088 | T087, T080, T081 |
| T089 | T074, T077, T082 |
| T090 | T089, T069, T068, T076, T081 |
| T091 | T090, T084, T085, T086 |
| T092 | T091, T087 |
| T093 | T091, T057, T041 |
| T094 | T092, T088 |

**Graph-longest dependency chain (task-count proxy, not duration forecast):** T001 → T002 → T003 → T005 → T006 → T008 → T009 → T012 → T018 → T019 → T020 → T021 → T025 → T026 → T027 → T028 → T030 → T032 → T033 → T034 → T035 → T037 → T038 → T039 → T040 → T041 → T042 → T043 → T048 → T049 → T050 → T051 → T052 → T053 → T054 → T055 → T056 → T062 → T063 → T064 → T067 → T070 → T071 → T072 → T073 → T074 → T075 → T076 → T077 → T078 → T079 → T080 → T081 → T082 → T089 → T090 → T091 → T092 → T094.

Likely delivery risks on that chain are complete provider/account cap proof, acoustic join acceptance, real remote restore/purge and authorized real owner trials. No timing estimate is invented. Design/media/storage branches can be completed when their prerequisites pass; one active implementation task still applies. Gate evidence can be gathered by the owner independently, never by unapproved paid agent work. No dependency is added solely to force phase serialization.

## Requirements-to-task coverage

Every major core requirement has implementation and/or acceptance coverage; deferred product decisions are not implemented as features.

| Frozen requirement | Implementing tasks | Acceptance / activation tasks |
| --- | --- | --- |
| Runtime, configuration and SQLite | T001, T002, T003 | T090 |
| Project create/rename/autosave/reopen and original input | T005, T006, T060 | T090 |
| Topic and approved pasted-script inputs | T061, T062, T042, T040 | T091 |
| Entitlement-aware Research and sources | T012, T037, T038, T039 | T084, T091 |
| Factual warnings/proposals and individual/all consent | T009, T040, T041, T063 | T091 |
| Translation/adaptation and approved word fidelity | T041, T006, T052 | T091 |
| Deterministic sentence/image scope and scene planning | T007, T043, T023 | T024, T091 |
| Three curated presets | T043, T061 | T090 |
| Image generation/validation/selective retry | T044, T045 | T085, T091 |
| Image replacement/restoration/review | T015, T017, T046, T066 | T090 |
| Built-in voice/effective config/cached previews | T047, T048, T065 | T086 |
| B initial and whole affected B correction | T010, T048, T049, T050 | T086, T091 |
| Continuous narration/local alignment/scene mappings | T051, T052, T053 | T091 |
| Accepted spoken variation/material-error handling | T052, T063, T089 | T091 |
| Different/same-word restoration and validated joins | T054, T055, T065 | T091 |
| Caption correction/style/toggle/Unicode technical path | T056, T057, T067 | T073, T091 |
| Timing correction/manual retention/global offsets | T053, T056, T067 | T091 |
| Optional gentle motion | T058, T072 | T073 |
| Optional permitted library music | T059, T072 | T073 |
| Scene reorder/delete, stable assets/projection | T006, T055, T067 | T091 |
| Version provenance/state axes/history | T008, T030, T036, T046, T055 | T090 |
| Deterministic invalidation and unaffected preservation | T036 | T024, T090, T091 |
| Concurrent generation edits/stale historical result | T028, T030, T036, T050 | T076, T090 |
| Desktop scene editor/selected preview/history | T064, T065, T066, T067 | T090 |
| Meaningful mobile corrections | T068 | T090 |
| Composer Simple Mode/optional Details/no mandatory cost review | T061, T062, T063, T074 | T090 |
| Warm Creator themes/accessibility/reduced motion | T004, T060, T061, T064, T068, T069 | T090 |
| Prepared isolated public demo and publication permission | T069 | T090 |
| Immutable render manifest/lock/all mutation guards | T070 | T077, T090 |
| 1080p/30fps complete MP4/effects/validation | T071, T072, T073 | T091 |
| Export history/protected download/initial auto versus manual render | T074, T014 | T090 |
| Cancellation/confirmed cessation/late output | T029, T075 | T076, T091 |
| Restart/spool recovery/no duplicate paid attempts | T027, T030, T076 | T077, T091 |
| Global production lane/serialized maintenance | T026, T027, T082 | T090 |
| Deletion confirmation/hiding/seven-day recovery | T078 | T081, T090 |
| Daily backup/<=24h objective/verified restore | T079, T080, T082 | T088, T094 |
| Next-cycle purge/all historical copies/no resurrection | T078, T081, T080 | T088 |
| Storage cap/retained versions/deleted bytes/scratch/no pruning | T016, T082 | T087, T092 |
| Invited identity/session/no public signup | T011 | T077 |
| Server ownership/resource/media isolation | T012, T014 | T077, T091 |
| Private media/staging/ranges/upload/path safety | T013, T014, T015, T017, T071 | T077 |
| Money/shared month/coverage/project/creator authority | T018, T019, T020 | T024, T087 |
| Reservations/settlement/unknown liabilities/allowance | T021, T028 | T024, T076 |
| Bounded retries/one-send/model scope/paid enablement | T029, T033, T034, T035 | T084, T085, T086 |
| Credits AND USD/expected versus maximum/no final formula | T022, T063 | T024, T090 |
| Expanded scope recalculation/reauthorization | T023, T062 | T024, T091 |
| Lightweight observability/owner operation controls | T031, T083, T082 | T094 |
| Experimental languages disabled and independently gated | T035, T057 | T093 |
| Invited infrastructure/cash/transfer/caps/remote readiness | T087, T088 | T094 |
| Real owner quality/calibration/reliability validation | T089, T091 | T094 |
| Measured temporary allocations/windows/end notice | T092 | T094 |
| Private Alpha invitation readiness | T094 | T094 |

## Existing pipeline reuse boundaries

The authoritative external source is `/Users/kazibadrul/Python Codes/YoutubeAI/python-scripts`; inspect static source, do not import credential-bearing prototype entry points. Existing code is below frozen specifications.

| Freeze classification | Planned adoption |
| --- | --- |
| A: pure seconds_to_srt arithmetic for validated times | T056 |
| B: create_content.py prompt loading/script request extraction | T042 |
| B: generate_images.py prompt/request primitives, no character promises | T043 |
| B: image request primitive and decoded validation | T044 |
| B: create_tts.py grouping/request ideas, retain coherent sources | T048 |
| B: TTS format/request extraction without blanket retries/cleanup | T049 |
| B: make_timestamps.py cached local Whisper interface, replace ASCII/fuzzy authority | T051 |
| B: make_video.py argv/scale/concat/mix ideas behind manifest/process control | T071 |
| C: CLI/global clients, raw paths, filename-only resume, blanket retries, mutable exports/audio cleanup, ASCII fuzzy boundaries and raw invalid JSON | Do not adopt these behaviors; extraction tasks replace authority/orchestration with tested domain contracts. |
| D: make_video_noeffects.py whole pipeline, older copies and demo/design/spike prototypes | Historical/reference fixtures only; no wholesale production copy. S6 validated ON/OFF behavior informs the single renderer. |

## Activation gates and unresolved owner decisions

A task can implement a disabled safe boundary without settling future live economics. The following exact gates require evidence/decisions before their capability can operate; none reopens feasibility. UNKNOWN must never be treated as zero or an implicit approval.

| Prerequisite | Gate / boundary | Resolution authority |
| --- | --- | --- |
| Image upload type/size/dimension/decode bounds | T015 | Owner-supported operational limits; disabled if absent |
| Voice/preview support and rights | T047 | Verified permitted catalog/configuration, not inferred from source constants |
| Caption style/font readability/resource bounds | T057 | Supported tested policy; owner decision if material |
| Acoustic source ranges/joins for restore/reorder/delete | T054 | Existing/local evidence and independent listening; fail closed on uncertainty |
| Normal text model adoption, text/search live endpoint/account/cap/price proof | T084 | Explicit owner model choice plus complete certificate |
| Selected image model complete modality/turn/billing proof | T085 | Supported live request contract, not partial output tariff |
| Selected TTS format/voice/cap/current price proof | T086 | Supported coherent-source contract; revalidate expiry |
| Host/backup/private access choices, all-in cash, reserve, storage/transfer/memory caps | T087 | Owner supplies choices/bounds; no vendor automatically selected |
| Actual daily off-machine restore/key/purge/current journal proof | T088 | Actual separately authorized environment evidence |
| Ten real English quality/reliability/calibration projects | T091 | Per-project owner-authorized funded/admissible trials and independent acceptance |
| Temporary tester allowance/entitlements/availability/end/caps | T092 | Owner assignments based on measurements, not tier promises |
| Each experimental language narration/caption/export | T093 | Conditional separate owner authorization; not core invitation blocker |
| All core invitation prerequisites | T094 | Independent review evidence, never Codex self-certification |

Final post-script credits/correction debit policy, commercial plan names/prices/quotas/rollover/overages, topic-suggestion shipping/count/usage/history/collection/paywall and Expert channel retrieval/model/data/retention remain **deferred product decisions**. No executable core task resolves them. Display known/pending credit information; determine a debit policy before presenting determined debit amounts. USD correctness does not wait for a commercial formula.

## Deferred / not scheduled

No executable Txxx tasks for timeline editor, Director/AI Director, reusable Style Studio/custom styles, extensive model controls/marketplace, recurring-character identity, uploaded video/custom audio, arbitrary scene addition/duplication, project duplication/archive, public signup/external auth, direct YouTube publishing/derived short-form, collaboration/marketplace/templates, commercial billing/final commercial credits/pricing, arbitrary font uploads or custom animation.

Topic Suggestions (stored random collection, no per-click LLM), Custom Topic Suggestions (categories/interests; owner model `gemini-3.8-flash`) and Expert Topic Suggestions (channel/name/link/niche; bounded retrieval/model unresolved) remain distinct accepted roadmap features with no first-Alpha delivery commitment. Only persisted feature eligibility infrastructure is scheduled. Research/Topic/Custom: lower No,3/week Yes,1/day Yes; Expert: lower No,3/week No,1/day Yes. Those labels are not Private Alpha throughput promises. Optional discovery is not charged to every video's production manifest.

Post-core follow-up Alpha milestones **Emphasis Text** and standalone **9:16 vertical validation** are not scheduled and receive no task IDs in this core plan. They do not block invitations; a future authorized plan must specify their unresolved details.

## Private Alpha readiness definition

**T094** is the final mandatory invitation-readiness gate. It requires independently accepted core tasks, ten real English landscape topic/pasted projects spanning 3–10-minute format support with ≥8/10 publishable after ≤15 active scene-correction minutes each, reliability/selective preservation/isolation/allowance enforcement, current finite provider bounds, supported $40 cash coverage, configured private host/media/storage, actual daily encrypted off-machine backup/verified restore/key recovery/purge, deletion/anti-resurrection, render/cancel/restart and no critical security failures. Duration quality trials remain independently financially admitted; no 10-minute budget bypass. Approximately 3–5 invited creators get explicit measured temporary assignments, not invented plan-volume promises. T093 is optional and excluded. PASS authorizes no sending invitations, deployment, purchase, new experiment or additional implementation without the designated owner's execution instructions.

## Planning verification and size audit

The planning verifier checks sequential unique IDs, initial statuses, all contract fields, exact existing source headings/paths, nonempty acceptance/test/manual/out-of-scope/reviewer/completion fields, valid prior dependencies, cycles, mandatory readiness closure, optional-language independence and requirement coverage. Size audit reviews cohesive capability boundaries and negative-path acceptance, not a target task count. Repository preservation checks compare existing-file hashes against the pre-planning snapshot and the freeze's protected-file manifest; no frozen verifier writer is rerun.

No task is an untestable “build backend/editor” bundle or a one-line mechanical change. Larger adversarial/quality tasks are bounded verification gates over prior features, not new feature construction; UI tasks cover one defined surface/context. Backup snapshot/restore/purge and finance representation/admission/settlement are separate. Provider activation and real operational/owner evidence are separate from disabled adapter implementation. Missing gate evidence yields TASK_BLOCKED, not acceptance by assumption. Planning verification result: **2,972/2,972 checks passed**, **52 requirement-coverage rows**, **zero dependency cycles**; all 94 tasks retain every required contract field and NOT_STARTED status. Task contracts span 266–381 words, with no unresolved size/reviewability flags after the capability-boundary audit. All 3,518 pre-existing repository files and 3,453 protected freeze evidence/media/pipeline files are hash-identical; only TASKS.md is added. These are planning/preservation checks, not application tests or independent acceptance of future implementation.

**STOP after planning. Do not activate T001, implement code, install dependencies, commit implementation, configure the orchestrator/agents, provision or deploy.**
