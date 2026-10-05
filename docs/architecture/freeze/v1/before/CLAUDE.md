# CLAUDE.md

## Mandatory Repository Instructions

Read `AGENTS.md` before performing repository work.

`AGENTS.md` contains the canonical agent behavior, source-of-truth hierarchy, scope rules, testing expectations, cost constraints, security requirements, and development workflow for this repository.

Follow it unless the user explicitly provides a higher-priority instruction.

Do not duplicate or reinterpret those rules here.

---

## Claude-Specific Working Style

When working in this repository:

1. Read the relevant specification before editing code.
2. Inspect existing code before proposing rewrites.
3. Prefer focused changes over broad refactors.
4. Do not silently expand Alpha scope.
5. Do not make unresolved product decisions on the user's behalf.
6. Use `SPEC_BLOCKED` when an unresolved material product or architecture decision prevents correct implementation, as defined in `AGENTS.md`.
7. Do not start subsequent tasks automatically.
8. Do not mark your own implementation as independently accepted.
9. Report tests and verification actually performed. Never imply a test was run if it was not.
10. Treat external AI/API spending as a correctness constraint.

---

## Planning

For substantial implementation tasks:

- identify relevant requirements
- inspect affected existing code
- identify dependencies
- form a concise implementation plan
- then implement

Do not create large speculative plans for trivial changes.

---

## Existing Code

This project contains or may contain existing Python video-generation code.

Do not rewrite existing pipeline components solely to standardize technology or style.

First determine whether the existing component satisfies the current product contract.

Preserve useful, tested behavior where practical.

---

## UI Work

Before significant UI implementation:

- read the current design documentation
- inspect provided reference screenshots/assets
- follow the anti-generic-AI-SaaS requirements in `AGENTS.md`

Do not substitute generic dashboard patterns for unresolved design decisions.

---

## Completion Report

When completing an implementation task, report:

### Implemented
What changed.

### Files
Files materially changed.

### Verification
Commands/tests/checks actually run and their results.

### Acceptance
Map results to the task's acceptance criteria.

### Remaining
Known limitations, risks, or unresolved issues.

End with:

`IMPLEMENTATION_COMPLETE`

when implementation is complete.

This is not equivalent to independent acceptance.