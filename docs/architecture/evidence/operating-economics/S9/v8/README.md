# S9 v8 evidence bundle

Current report: [CREDITS-v8](../CREDITS-v8.md). Verdict **NOT_YET_PASS**.

Official source facts: [pricing](official-pricing-v8.json). Existing immutable media receipts and qualified extrapolations: [measurements](measurements-v8.json). Deterministic models/checks: [results](arithmetic-results-v8.json). Historical protection: [before](preservation-before.json), [verification](preservation-results-v8.json), [prior index archive](S9-index-before-v8.md).

Reproduce from repository root: `python3 spikes/operating-economics/infrastructure_v8.py` (standard-library-only; no network/provider/model calls). This reruns only v8 read-only measurements and arithmetic, not prior spikes. Target host/process/backup feasibility remains unvalidated.
