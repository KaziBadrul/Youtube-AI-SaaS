# S5 offline preparation

Disposable standard-library witnesses, not narration infrastructure. No SDK/client/key/environment loading or provider endpoint. No dependency installation, ASR model download or network access.

Run from repository root:

```sh
python3 spikes/narration-feasibility/prepare.py
```

Recreates pinned fixture/call manifests, request projections and local results under `docs/architecture/evidence/narration-feasibility/`. Reads immutable existing demo text/media; never writes to demo files. DNS/socket connections are denied. Uses temporary in-memory synthetic PCM to verify range-preservation/offset mechanics; this says nothing about audible joins.

`score_alignment.py approved.txt observed.json` scores externally supplied ASR or manually reviewed word timestamps, full transcript word edit distance, monotonic ranges and boundary errors. No transcriber or speech-quality oracle. Synthetic positive/negative scoring cases run in prepare.py. Results require human validation; punctuation and case are not spoken words, numbers/pronunciation require listening adjudication. No permissive fuzzy threshold or missing-scene skip can declare complete fidelity.

There is deliberately **no live execution runner**. See the experiment plan for the explicit authorization boundary, future one-send runtime and prerequisite checks. S4's exact installed SDK/transport witnesses must be rerun if that runtime changes.

Flash-Lite local wire verification (existing S4 pinned runtime):

```sh
/private/tmp/alpha-s4-venv/bin/python spikes/narration-feasibility/verify_lite.py
```

Checks immutable hashes, model/voice/configuration and one send on synthetic HTTP 429 for all eight calls. Environment cleared, dummy key, HTTPX MockTransport, DNS/socket denial. No live endpoint or runner. SDK 2.3.0 rejects typed speech_metadata; public extra_body injects the exact structured wire metadata. This is a local transport witness, not live API schema proof.

## Isolated bounded execution preparation

See [runner readiness](../../docs/architecture/evidence/narration-feasibility/S5-RUNNER-READINESS.md). `runner.py` uses direct documented REST and existing isolated HTTPX 0.28.1, not the old SDK. Default invocation is dry-run. Explicit, distinct Stage 1/2 tokens are required for eventual owner-authorized execution; **neither live stage has been authorized or invoked**.

```sh
/private/tmp/alpha-s4-venv/bin/python spikes/narration-feasibility/test_runner.py
python3 spikes/narration-feasibility/runner.py
```

Do not regenerate/modify sealed manifests or reset the fixed execution ledger. Unknown outcomes stop; safe 429 retry simulation is not a claim that real HTTP 429 is unbilled. Full transport/counter/recovery limitations are in the report. Historical SDK wire witness is retained; direct REST is the new isolated runner choice, not a repository-wide provider-adapter implementation.
