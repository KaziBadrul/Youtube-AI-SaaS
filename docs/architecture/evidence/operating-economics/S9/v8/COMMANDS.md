# S9 v8 reproduction and boundaries

Run from the repository root:

```sh
python3 spikes/operating-economics/infrastructure_v8.py
```

Standard library only. It does not load provider clients, tokenizers or models. It reads prior S5 ledger/S6 final benchmark receipts, existing fixture/legacy media and the captured preservation manifest. It measures file bytes/SHA-256, parses PNG/JPEG signatures and WAV metadata, compares historical source hashes, recomputes Decimal storage/backup/traffic/capacity sensitivities, and rewrites only the three v8 result JSON files. No S2–S8/v1–v7 experiment is executed. No rerender or download is needed.

Public pricing was retrieved with the web browser tool from the exact URLs in `official-pricing-v8.json` on 2026-10-05, not provider generation/API submission or account login. Facts are dated snapshots, not account quotes; refresh and verify account/region/payment terms before future admission. Public sources contain conflicting B2 storage text; preserve the conflict and higher-rate calculation.

The before manifest was captured before v8 writes; the live index's previous bytes were archived. Verification checks the archive instead of expecting the current index to remain unchanged. Source receipt hashing is repeated within each run; S5 WAV/S6 export historical hashes must match. The current index, docs README/COST_MODEL/ARCHITECTURE_SPIKES intentionally receive only new v8 pointer/status paragraphs. Do not rewrite old evidence to reproduce results.

No production code, TASKS.md, deployments, purchases, provisioning, model/runtime installation, paid calls or token-preflight experiment are part of this command. These tests establish arithmetic and evidence integrity, not remote backup or Linux host feasibility.
