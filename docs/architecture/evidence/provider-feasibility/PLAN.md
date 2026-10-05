# S4 documentation/source/local transport plan — 2026-10-04

Execution authorization: S4 only, documentation and free/local witnesses. No provider request, credential discovery, S5/S6/S9, production application, TASKS.md, deployment or purchase. Dependencies installed only in /tmp/alpha-s4-venv. Explicit dummy API key and fake transports; deny sockets and clear environment while running witnesses. Existing scripts are read/AST-inspected, never imported.

## Claim and failure modes

Test whether the evidenced Gemini Developer API text, image, research/checking candidate and TTS paths can satisfy finite request liability, one submission per application attempt, observed provenance/usage, bounded application retries and honest unknown-outcome handling. Existing provider choices/model IDs/rates are evidence, not commitments. Look for SDK retries beneath application accounting; timeout-after-receipt mistaken for zero liability; apparent idempotency without a transmitted/supported key; output caps that omit other billable dimensions; invisible tools/function-call turns; and undocumented quota guarantees.

## Minimum experiment

Inspect google-genai 2.3.0 (documented Interactions API minimum) and pin its resolved transport dependencies. Check the actual installed source, not mutable main, for both generateContent and the separate Stainless Interactions client. Exercise actual SDK public calls against HTTPX MockTransport: retryable/nonretryable statuses, read/connect timeout injection, explicit retry config, default/capped timeouts, synthetic response IDs/status/usage/modality metadata, known-ID interaction retrieval/cancel/delete and image/TTS wire parameters. Count every transport submission. Test a disposable public custom-HTTPX transport gate if SDK config alone cannot enforce one paid POST per persisted attempt. No fake failure is evidence that the real provider billed or did not bill it.

Record static capability/pricing/model/rate docs and retrieval date, source URLs, installed-source hashes, finite conservative equations using integer subunits, and missing account-specific evidence. Do not infer production rates from remembered quotas, word estimates, local output truncation, estimated cost, budget alerts or free-tier labels. Research is absent from the pipeline; evaluate Google Search grounding on the evidenced Gemini models before considering replacement. No broad provider shopping or automatic replacement.

## Pass/fail criteria declared before witness execution

Each proposed Alpha capability needs: credible finite pre-authorization liability including all inputs/output/modalities/tools/candidates/attempts; application retry authority (initial + at most two known-safe automatic retries), no unaccounted outbound retry; pinned input/config/attempt/provider IDs where available; complete usage capture with missing values remaining unknown; observed usage/rate-derived charges distinguished from settled actual billing; and either evidence-backed reconciliation or explicitly blocked uncertainty requiring owner intervention. Local witnesses must prove their asserted wire counts and metadata paths; network denial must remain intact.

A passing local transport witness is not S4 PASS. Missing finite liability for a required candidate, or missing evidence needed to claim account request feasibility, prevents overall PASS. Classify cost BOUNDED/CONDITIONALLY_BOUNDED/NOT_CREDIBLY_BOUNDED/UNKNOWN and unknown outcomes RECONCILABLE/PARTIALLY_RECONCILABLE/NOT_RECONCILABLE/UNKNOWN per capability. Required provider reconsideration is reported, never silently adopted. No real call can prove a universal hard upper bound from a small sample. If a real experiment is necessary, stop before it and propose exact count/input/output/maximum/risk; never invent its bound.

## Evidence conventions

Scaffold: spikes/provider-feasibility/. Reports and JSON: docs/architecture/evidence/provider-feasibility/. Retain material failed witness runs. Record source/plan hashes, runtime versions, deterministic cases, commands, findings, limitations and architecture consequence. Update only documentation status/evidence links if appropriate; preserve all accepted policies and prior gate results.
