# V13 reproduction

From repository root, with Python standard library only:

```sh
python3 spikes/operating-economics/v13/financial_authority.py
```

Writes only V13 RESULTS/manifest/preservation files; creates and removes disposable SQLite WAL databases outside production. No provider SDK, HTTP, tokenizer, model or media execution. Sockets/DNS forbidden. Previous witnesses are imported only for the pure local sentence function, never rerun as writers.

Read `RESULTS.json` for per-check and per-scenario event traces. All fake receipts/cost limits are synthetic. Invariant checks are actual transactions and a two-thread/two-connection competition, not provider idempotency tests. SQLite close/reopen and transaction fault injection simulate recovery boundaries; this is not OS power-loss or production acceptance evidence.

Do not rerun V1–V12 generators: their outputs are historical. Verify V13 preservation against `preservation-before.json`; the only permitted old evidence change is live S9 README, archived byte-for-byte under `before/`.
