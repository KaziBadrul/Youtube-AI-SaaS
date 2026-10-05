# AGENTS.md

## Project

This repository contains an AI-native video production SaaS.

The core product promise is:

> A creator provides an idea or script and receives an editable, narrated, image-based video with visuals, narration, captions, pacing, motion, and optional music, while retaining the ability to correct individual parts without regenerating the entire project.

The initial product is aimed primarily at faceless YouTube creators and similar AI-assisted video creators.

This repository is currently being developed toward a private alpha.

---

# 1. Read Before Acting

Before making product, architecture, implementation, or task-planning decisions, read the relevant project documentation.

Start with:

1. `docs/README.md`
2. `docs/ALPHA_PRODUCT_SPEC.md`

Then read any documents referenced by `docs/README.md` that are relevant to the task.

Do not treat every document as equally authoritative.

---

# 2. Source-of-Truth Hierarchy

When documents disagree, use the following authority, within each document's stated scope:

1. Explicit current-session owner instructions.
2. Accepted current ADR decisions for their specific scope, read with explicit later accepted amendments recorded in the frozen contracts. Dated pre-execution statements are historical, not current gate status.
3. `docs/ALPHA_PRODUCT_SPEC.md`: current Private Alpha scope and product semantics.
4. `docs/ARCHITECTURE.md` and its delegated `ARTIFACT_MODEL.md`, `JOB_EXECUTION_MODEL.md`, `COST_MODEL.md` contracts: runtime/domain/execution/financial authority. `UX_FLOWS.md` and `DESIGN.md` own interaction/presentation within that product scope. A contract cannot silently remove a product requirement.
5. `GLOSSARY.md`: canonical terminology; `VALIDATION_PLAN.md`: invitation acceptance, not a new scope definition.
6. `docs/PRODUCT_DECISIONS.md`: dated owner rationale/history; only its current accepted clarification applies prospectively.
7. `docs/FEATURE_ROADMAP.md`: future direction, not automatic Alpha scope.
8. Feasibility reports adopted by the current contracts: bounded evidence and limitations, not independent product authority. Earlier/superseded evidence and discovery/prototypes remain historical.
9. Existing code: reusable implementation material, never the specification.

Start at `docs/README.md`; `docs/architecture/ARCHITECTURE_FREEZE.md` is the v1 freeze index/summary, not another full specification. S1–S9 are closed; S9 V14 is PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY. Active ceiling is $40 USD per Asia/Dhaka calendar month. Do not reopen spikes because empirical activation/operational prerequisites remain pending.

Resolve only conflicts settled by explicit accepted decisions; otherwise report `SPEC_BLOCKED` with the precise material contradiction. Open decisions behind fail-closed capability/invitation gates do not automatically block task planning. Freeze does not authorize implementation or TASKS.md generation. Historical reports, including their earlier $30 ceiling, must remain unchanged.

---

# 3. Current Alpha Scope

The private Alpha currently focuses on:

- topic or complete script input
- research where required
- factual checking and warnings
- script generation
- scene generation
- generated still images
- built-in TTS narration
- automatic timing/alignment
- captions
- optional basic image motion
- optional library music
- scene-based corrections
- selective regeneration
- asset version restoration
- failure recovery
- final rendering
- 1080p MP4 export

The primary initial production job is an English, image-based, faceless educational YouTube video approximately 3–10 minutes long in 16:9.

Refer to `docs/ALPHA_PRODUCT_SPEC.md` for exact current requirements.

---

# 4. Do Not Silently Expand Scope

Do not implement a roadmap feature merely because it sounds useful.

Examples of capabilities that may exist in the long-term product vision but are not automatically part of the initial Alpha include:

- AI Director
- professional timeline editor
- AI-generated video clips
- voice cloning
- direct YouTube publishing
- collaboration
- marketplace
- reusable custom style studio
- guaranteed recurring-character identity
- extensive model controls
- public subscription billing
- broad media-management features

Check the current specification before implementing any such feature.

Architecture may preserve a reasonable path toward future capabilities, but do not build speculative infrastructure solely for uncommitted roadmap features.

---

# 5. Specification Gaps

Never silently invent important product requirements.

If successful completion of a task requires a product decision that is not resolved by the source-of-truth documentation:

1. Determine whether the choice is merely a local implementation detail or a product/architecture decision.
2. For ordinary reversible implementation details, choose the simplest solution consistent with the existing architecture and document the choice.
3. For unresolved decisions that materially affect user behavior, data contracts, cost, security, architecture, acceptance criteria, or future compatibility, stop.

Report:

`SPEC_BLOCKED`

Then explain:

- the unresolved question
- why it blocks correct implementation
- the relevant existing documentation
- the smallest decision needed from the user

Do not use `SPEC_BLOCKED` for trivial implementation choices.

---

# 6. Preserve Product Semantics

Important product concepts must remain explicit in the architecture.

Do not collapse distinct concepts merely because doing so makes implementation easier.

Examples include:

- original user input
- current derived script
- scene narration text
- generated narration audio
- visual description
- image-generation prompt
- generated image
- timing/alignment
- captions
- rendered output
- artifact version
- current artifact
- stale artifact
- failed artifact

Use canonical terminology from `GLOSSARY.md` when available.

If terminology is missing or contradictory, flag it rather than silently creating competing vocabulary.

---

# 7. Artifact-Based Generation

The product must not be modeled as:

`prompt → MP4`

A project contains intermediate artifacts with dependencies.

Conceptually:

`Input → Research → Script → Scenes → Assets → Timing → Render`

Individual artifacts may be regenerated or restored independently.

Changing one artifact should invalidate only the downstream artifacts that actually depend on it.

Do not unnecessarily regenerate unaffected work.

Preserve successful artifacts after partial failures.

---

# 8. Versioning and Staleness

Generated assets may have multiple versions.

Where required by the specification:

- preserve previous valid versions
- identify the current version
- prevent stale asynchronous results from silently replacing newer work
- mark dependent artifacts outdated when their inputs change
- reuse compatible existing artifacts where possible

Do not silently export known-outdated required content.

---

# 9. Long-Running Operations

AI generation and rendering are long-running operations.

Do not design them as if they were ordinary short synchronous HTTP requests.

The system must eventually account for:

- queued work
- progress
- retries
- cancellation
- partial failure
- resumption
- idempotency
- stale results
- spending authorization
- provider failures

Exact architecture must follow the accepted architecture documents once those exist.

Do not prematurely choose infrastructure solely from this file.

---

# 10. Cost Is a Correctness Constraint

The private Alpha has a strict total prelaunch operating ceiling defined in the product specification.

Treat external API and infrastructure spending as a correctness concern.

Paid operations must not accidentally run without appropriate authorization.

Do not:

- silently retry paid operations beyond authorized limits
- duplicate paid generation because of naive retry behavior
- ignore failed provider attempts that still incurred real cost
- assume estimated provider cost equals actual provider spending

Where required, distinguish:

- estimated cost
- authorized spending ceiling
- reserved allowance
- consumed user allowance
- actual provider cost

Do not hardcode public pricing or commercial credit economics before those decisions are explicitly made.

---

# 11. Failure Is Expected

A multi-stage generation pipeline will fail partially.

Design for partial failure rather than treating it as an exceptional impossible state.

A failure in one scene should not automatically destroy successful work from other scenes.

Where supported by the specification:

- retain successful outputs
- expose failed operations
- allow targeted retry
- allow safe cancellation
- recover interrupted operations
- reconcile spending correctly

Never report incomplete production as successful.

---

# 12. Existing Python Pipeline

An existing local Python pipeline may already implement portions of:

- content generation
- scene generation
- image prompting
- TTS
- image generation
- narration alignment
- subtitles
- image motion
- background music
- FFmpeg rendering

Treat this implementation as reusable evidence and code, not as the product specification.

Before reusing a component:

1. understand what it does
2. identify hardcoded assumptions
3. compare behavior against current specifications
4. preserve useful tested behavior
5. refactor only when required

Do not rewrite working pipeline components merely to make the code look cleaner.

Do not preserve incorrect legacy behavior merely because it already exists.

---

# 13. Architecture Principles

Prefer:

- explicit boundaries
- deterministic orchestration
- resumable operations
- idempotent jobs
- observable state
- narrow interfaces
- validated external-provider responses
- provider adapters where provider-specific behavior would otherwise leak into product logic
- straightforward designs appropriate for one engineer

Avoid:

- unnecessary distributed systems
- premature microservices
- speculative abstractions
- hidden global state
- uncontrolled agent authority
- architecture built primarily for hypothetical future scale

This is a solo-engineer Alpha.

Complexity must justify itself.

---

# 14. AI Authority

AI models generate or propose content.

They should not silently control system authority.

Where relevant, deterministic application code should control:

- spending authorization
- permissions
- project ownership
- state transitions
- queue admission
- retries
- cancellation
- version selection
- artifact invalidation
- final persistence

Do not delegate security-sensitive or financial authority to probabilistic model output.

Validate model responses before using them as structured application data.

---

# 15. Security and Isolation

Invited Alpha creators must not be able to access another creator's private projects or assets.

Treat authorization as a server-side requirement.

Never rely only on:

- hidden UI controls
- client-provided ownership identifiers
- obscurity of asset URLs

Do not expose:

- provider API keys
- server credentials
- secrets
- internal privileged operations

Do not commit secrets to the repository.

---

# 16. User Uploads

Where uploads are supported, treat them as untrusted input.

Validate relevant:

- file type
- file size
- decoding
- storage behavior
- ownership
- lifecycle

Exact limits must come from accepted operational specifications rather than being invented during implementation.

---

# 17. UI Direction

The product should feel like an intentional creative tool, not a generic AI SaaS dashboard.

Avoid defaulting to:

- purple/blue AI gradients
- excessive glowing elements
- excessive glassmorphism
- giant rounded cards
- pill-shaped everything
- every section inside a card
- generic dashboard templates
- excessive gradients
- unnecessary badges
- repetitive icon-heading-description grids
- arbitrary decorative elements
- excessive centered layouts

Prefer:

- strong typography
- clear hierarchy
- intentional whitespace
- useful information density
- restrained surfaces
- subtle borders
- consistent radius system
- purposeful motion
- strong editing/workspace ergonomics

Reference project design documentation and supplied visual references before making significant UI decisions.

Do not invent a complete design language independently if reference material exists.

---

# 18. Motion

Animation must communicate something useful, such as:

- state change
- progress
- hierarchy
- navigation
- cause and effect
- generation activity
- successful completion
- failure

Avoid decorative motion that harms usability.

Respect reduced-motion preferences.

---

# 19. Responsive Behavior

Do not assume every desktop creative-tool interaction can simply shrink onto mobile.

Desktop is the primary editing environment unless current specifications say otherwise.

Responsive behavior should preserve critical project visibility and prevent broken layouts.

If a complex editing interaction does not have a defined mobile behavior, do not invent a radically different product workflow without specification.

---

# 20. Testing Philosophy

Test behavior, not implementation trivia.

Prioritize tests around:

- artifact state transitions
- dependency invalidation
- version restoration
- retry behavior
- idempotency
- cancellation
- partial failures
- stale asynchronous results
- permissions and project isolation
- spending/allowance enforcement
- queue behavior
- render locking
- persistence and recovery

Provider integrations should be testable without repeatedly spending real money.

Use mocks/fakes/fixtures where appropriate, while preserving separate acceptance paths for real integrations.

---

# 21. Acceptance Criteria

A task is not complete merely because:

- code compiles
- a page renders
- the happy path works once
- the implementing agent believes it is complete

Task completion is determined by its documented acceptance criteria and independent verification.

Do not weaken acceptance criteria to make a task pass.

---

# 22. Multi-Agent Development Workflow

The intended implementation workflow is:

`Task → Codex implementation → OpenCode independent review → PASS or repair`

Codex is the primary implementation agent.

OpenCode is an independent reviewer/tester.

A deterministic orchestrator will eventually control progression between tasks.

The implementing agent must not mark its own task as accepted merely because implementation is finished.

---

# 23. Implementation Agent Responsibilities

When assigned one task:

1. Read the task completely.
2. Read referenced specifications.
3. Inspect existing implementation.
4. Confirm dependencies are satisfied.
5. Implement only the task's intended scope.
6. Add/update required tests.
7. Run relevant verification.
8. Report changed files.
9. Report verification results.
10. Report unresolved risks or blockers.

Do not begin the next task unless explicitly instructed by the orchestrator or user.

---

# 24. Reviewer Responsibilities

Independent reviewers should:

- read the task and source requirements
- inspect the actual diff
- run relevant tests
- inspect likely regressions
- verify acceptance criteria individually
- look for scope expansion
- look for security/cost/state-management problems
- distinguish blocking failures from optional improvements

Reviewers should not modify implementation when operating in review-only mode.

The final review result should be unambiguous:

`VERDICT: PASS`

or:

`VERDICT: FAIL`

A failure should identify concrete blocking findings.

---

# 25. No Self-Certification

Implementation and acceptance are separate authorities.

An implementation agent may report:

`IMPLEMENTATION_COMPLETE`

but that does not mean the task has passed independent acceptance.

Only the designated review/gating process should advance task state.

---

# 26. Git Discipline

Keep changes scoped to the active task.

Avoid unrelated refactors.

Before completing a major task:

- inspect the diff
- ensure generated files/secrets are not accidentally committed
- run required verification

Major implementation phases should end with a clear Git checkpoint.

Do not rewrite unrelated history.

---

# 27. Documentation Discipline

If implementation reveals that an accepted specification is impossible, contradictory, or materially incomplete:

Do not silently change product behavior.

Report the issue.

Documentation changes that alter product semantics should be explicit and reviewable.

Implementation details may be documented as architecture evolves, but product requirements remain controlled by the product specification process.

---

# 28. Deferred Decisions

Do not prematurely freeze decisions that the product documentation intentionally leaves open.

Examples may include:

- providers
- deployment platform
- exact storage caps
- exact tester allowances
- public pricing
- subscriptions
- public launch infrastructure

When a deferred decision becomes necessary for implementation, surface it explicitly.

---

# 29. Definition of Done

Unless a task defines stricter requirements, completion generally requires:

- requested behavior implemented
- relevant tests passing
- no known regression in affected functionality
- error/failure paths considered
- security boundaries preserved
- spending boundaries preserved where applicable
- documentation updated when required
- acceptance criteria demonstrably satisfied
- independent review passed when the workflow requires it

---

# 30. Core Principle

Optimize for this outcome:

> A creator can go from an idea or script to a usable video with dramatically less work, while retaining control over individual AI-generated decisions.

Do not optimize for feature count.

Do not optimize for architectural cleverness.

Do not optimize for making the demo look complete while core generation reliability remains weak.

Build the smallest reliable system that proves the product.
