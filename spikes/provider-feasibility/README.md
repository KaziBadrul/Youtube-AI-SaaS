# Disposable S4 provider feasibility witnesses

No production integration. Do not import legacy provider scripts, read .env files or substitute real credentials. All SDK HTTP is routed to HTTPX MockTransport; environment is cleared and sockets/DNS denied. SDK imports and synthetic audio bytes are not S5 audio tests.

Reproduce from the repository root using Python 3.12:

```sh
python3.12 -m venv /private/tmp/alpha-s4-venv
/private/tmp/alpha-s4-venv/bin/python -m pip install -r spikes/provider-feasibility/requirements.lock
/private/tmp/alpha-s4-venv/bin/python spikes/provider-feasibility/witness.py
/private/tmp/alpha-s4-venv/bin/python spikes/provider-feasibility/tts_wire.py
/private/tmp/alpha-s4-venv/bin/python spikes/provider-feasibility/accounting.py
```

Package installation requires registry network access, never provider access. Output JSON goes to `docs/architecture/evidence/provider-feasibility/`. Source hashes identify the tested SDK. The attempt guard is a temporary single-process feasibility witness, not a production durable ledger implementation; S2/S3 cover local transactional/recovery structures separately. The full-cap accounting examples exclude tools and account-specific taxes/fees. Missing metadata and unknown outcomes cannot be settled as zero. Read [S4 report](../../docs/architecture/evidence/provider-feasibility/S4.md) before interpreting passing fixtures as provider feasibility.
