# Conditional SQLite for the single-host Alpha

Status: accepted conditional decision in the architecture baseline confirmed on 2026-10-03. SQLite concurrency/recovery evidence remains unproven. This ADR is authoritative for database selection; failure requires explicit reconsideration rather than a silent infrastructure change. Acceptance does not authorize implementation or spike execution.

**Decision:** SQLite on local persistent disk for the single-host Alpha, conditional on the concurrency/recovery gate. Use short serialized write transactions, enabled relational constraints, durable settings and integer monetary units. Queue admission, financial reservation, render locking and version selection require explicit transactions. Never hold a transaction while calling providers, running FFmpeg, copying uploads or backing up media.

**Requirements:** Atomic multi-record state/cost transitions, one executing job, simultaneous web edits and low operational overhead.

**Alternatives:** Local or managed PostgreSQL; JSON/files as authoritative state; external broker as workflow authority.

**Tradeoffs:** SQLite avoids a database service but permits one writer and requires same-host WAL access. PostgreSQL offers row locking/multi-host access but adds operational burden not yet warranted. File-only state cannot supply the required relational/accounting atomicity. Lock errors must be handled without repeating external calls. Use PostgreSQL if the spike fails or topology genuinely becomes multi-host; that is an explicit architecture revision.

**Reversibility:** Moderate migration effort. Portable IDs/relations, logical media keys and integer money preserve a reasonable path; no speculative dual-database layer is needed.

**Evidence needed:** Concurrent autosave/admission/publish/cancel tests, durable transaction behavior and backup/restore. [SQLite WAL](https://www.sqlite.org/wal.html) documents one-writer/same-host limits. [Django SQLite notes](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes) explain unsupported row locking and decimal behavior. Do not assume `select_for_update` provides exclusion or use floating-point money.

