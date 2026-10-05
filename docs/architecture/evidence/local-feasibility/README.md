# Local/free architecture feasibility evidence — 2026-10-04

The user authorized **S1 → S2 → S3 → S7 → S8 only**, sequentially. Final local experiment verdicts are **PASS** for all five. These results support the existing conditional architecture; they do not establish production acceptance, creator invitations, arbitrary SQLite scale or full runtime/provider/media/hosting feasibility. No product/design/spending/recovery policy was changed.

| Gate | Result | Strongest local evidence | Important boundary |
| --- | --- | --- | --- |
| [S1](S1.md) | PASS | Real Django session/CSRF/ownership/Range requests; versioned autosave; separate fake worker; executed focused JS | Deterministic DOM, not browser-device acceptance; native narration/media stack deferred |
| [S2](S2.md) | PASS | 160 eight-process race rounds, 800 contended writes, interrupted transactions | Tiny same-host fixtures; no arbitrary throughput promise |
| [S3](S3.md) | PASS | 30 worker crash cases, five fake outcomes, three surviving child-group recovery cases | Fake receipts; real provider reconciliation and target-host supervisor remain unproven |
| [S7](S7.md) | PASS | 27 export/publication crash cases, corrupted/missing bytes, shared-response staleness and scoped restoration | Synthetic export and silent WAV ranges, not MP4/audio quality |
| [S8](S8.md) | PASS | Authenticated encrypted snapshot/restore, independent deletion authority, controlled seven-day/next-day purge | Local destination models off-host storage; real backup vendor and full-size reliability/cost deferred |

Each report states claim, failure mode, experiment, predeclared criteria, commands, results, failures, limitations and consequence. [PLAN.md](PLAN.md) was written before experiments; its hash is in each final JSON. JSON captures measured observations and scaffold hashes. Initial failures are retained in [S2-first-run.json](S2-first-run.json) and [S3-first-run.json](S3-first-run.json). Neither failure was concealed by relaxing accepted requirements.

## Reproduction and provenance

See [isolated scaffold README](../../../../spikes/local-feasibility/README.md) and its pinned requirements. Environment: macOS 26.5 arm64, Python 3.12.14, SQLite 3.53.4, Django 5.2.17, cryptography 46.0.7 and Node 26.9.0. These are observed experiment versions, not frozen production dependencies. No provider SDK/model or frontend framework installed. [Source inventory](source-inventory.json) records authority/reference paths and hashes; spike scaffolds are evidence, never higher authority than those documents.

Runtime checks compile only isolated Python files and parse the two JS witnesses. Final gates were repeated sequentially after shared witness corrections. S3 required approved access to inspect/terminate its own temporary process groups because the macOS sandbox denied `ps`. No deployment or privileged service was created.

## Architecture consequences

Evidence continues to support Django/server-rendered pages with focused enhancement; one Python production worker; local persistent same-host WAL SQLite with short explicit transactions; private immutable media with durable registration; fenced crash recovery; and the documented independently recoverable deletion/backup model. No fundamental failure required PostgreSQL reconsideration. These remain conditional on implementing the tested invariants and completing the remaining gates. The disposable schema, conservative fake compatibility checks and local backup mechanism are not adopted as production architecture.

No material policy gap or contradiction required `SPEC_BLOCKED`. One-tap creation with optional cost inspection remains accepted. Unknown spending/remote execution still blocks unsafe retry; restoration still requires compound approval when words/configuration change. Seven-day/next-day deletion deadlines are unchanged.

## Remaining gates and prerequisites

- **S4 — provider/transport/cost/reconciliation:** not executed. Requires separate authorization; identify candidate SDK/provider and account-specific capabilities, finite request bounds, disabled/accounted hidden retries, known/unknown submission outcomes, retrieval/cancellation and actual billing reconciliation. Existing local fakes show how to fail closed; they supply no real-provider guarantees. No newly discovered design/policy blocker prevents an authorized S4 investigation. Paid calls still require separate owner approval with a finite maximum; this authorization supplies none.
- **S5 — narration A/B/C quality and correction:** not executed. Requires S4 finite financial/capability bounds and separate authorization before paid calls; real 3/5/10-minute approved scripts, mapped shared ranges, scoped restore and audible joins remain necessary. S7's silent range tests cannot select a granularity policy.
- **S6 — render/captions/resources:** not executed. Requires a caption-capable FFmpeg/font/native runtime and representative target-hardware measurements. The previously inspected workstation build lacks required text/subtitle filters; pure Python/fixture checks do not repair or prove this stack.
- **S9 — operating envelope/hosting/storage:** not executed. Depends on measured generation/failure/correction costs, retained source/version sizes, render resources and backup traffic; actual hosting/backup terms must cover deletion/history/key custody, fees/tax/egress and the current ceiling. No purchase/deployment or invented allowances are authorized.

No production Alpha implementation, paid provider call, infrastructure purchase, deployment, architecture redesign or `TASKS.md` generation occurred. Existing user files, demo media and design prototypes were preserved; documentation edits only update evidence/status links. Stop here; do not begin S4 automatically.
