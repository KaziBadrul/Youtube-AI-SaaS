# Disposable S4-R bounded research witness

Documentation/local transport only. No production adapter, provider SDK, credentials or live search. Reuses the S4 temporary dependency pin. From repository root:

```sh
/private/tmp/alpha-s4-venv/bin/python spikes/research-feasibility/witness.py
```

If recreating the environment, use Python 3.12 and `spikes/provider-feasibility/requirements.lock` as documented in the S4 README; package downloads are not provider calls. No new package is needed for S4-R.

Output: `docs/architecture/evidence/research-feasibility/witness.json`. Environment cleared; sockets/DNS denied; HTTPX MockTransport only. Synthetic fixture URLs use example.org; no factual claim evaluated. SQLite is temporary, not an application schema. Witness monetary values are integer microUSD and quota values are integer credits.

Cases test finite plan/sends/attempts, persisted recovery guard, bounded receipt/evidence, unknown holds, no redirect/retry, source IDs, proposed-change approval boundary and quota admission. Tighter token-budget examples are conditional arithmetic, not a verified tokenizer or real-model output behavior. Complete legacy S4 tests are not rerun.

Read [S4-R report](../../docs/architecture/evidence/research-feasibility/S4-R.md). A fixture pass does not certify live quality, terms activation, effective quotas, provider deletion or operating economics. No live API calls are authorized by these instructions.
