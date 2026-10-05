# S5 isolated execution preparation — 2026-10-04

**READY_FOR_CALL_1 at documentation/local-witness scope. SERVER_ACCEPTANCE_UNPROVEN.** This does not authorize live execution. Earlier NOT_READY results remain historical and unchanged in S5-PREFLIGHT.md/preflight.json. Approved model/voice/fixtures/call count/cost remain unchanged.

## Compatibility resolution: D — DIRECT_REST_REQUIRED

For this disposable experiment, direct documented REST is the simplest reliable bounded path. Use Python 3.12 and already isolated **HTTPX 0.28.1**, no Google SDK on the execution path, no dependency upgrade. The inspected Google Gen AI **2.3.0** installation remains unchanged. Its typed Part rejects speech_metadata, and its older nested voice configuration serializes snake_case where the current REST schema documents camelCase. Earlier extra_body mock success was not server-acceptance evidence. Public overrides could carry an entire REST body but add unnecessary schema conversion authority here.

The current official TTS guide recommends Python SDK >=2.25.0 **or REST**. No newer SDK installed, no claim that its retry behavior inherits S4 guarantees. Other repository Gemini usage unaffected. No unsupported/private SDK internals used.

Direct endpoint fixed:
`POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-lite-tts:generateContent`

Payload uses `contents[].parts[].text`, `speechMetadata.style`, `generationConfig.responseModalities=[AUDIO]`, `candidateCount=1`, `maxOutputTokens=16384`, `speechConfig.voiceConfig.prebuiltVoiceConfig.voiceName=Charon`. No tools/system instructions/history/cache or alternative endpoint. Model page documents GenerateContent speech metadata as well as the model's serving caps. Current REST reference documents every selected field. Documentation establishes request expressibility, not live model/server acceptance. Call 1 is the later authorized acceptance witness; 400/404/405/422 stops for schema/model/endpoint investigation without variation retries or Calls 2–8.

Authoritative sources retrieved 2026-10-04:
- https://ai.google.dev/gemini-api/docs/speech-generation — modern SDK minimum or REST, structured styling, WAV default.
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-lite-tts — exact model, 8192/16384 serving caps, schema direction.
- https://ai.google.dev/api/generate-content — Part.speechMetadata, GenerationConfig and camelCase voice fields, inlineData response.
- https://ai.google.dev/gemini-api/docs/rate-limits — input TPM, project-scoped quota.
- https://ai.google.dev/gemini-api/docs/pricing — already verified standard Lite $0.50/$6 per million, same financial ceiling.

## Runner and hard guards

`spikes/narration-feasibility/runner.py` is a disposable standalone script; no production or legacy pipeline imports. SHA256 seals of both approved call manifest and fixture inventory are embedded in code. Texts are also reconstructed read-only from the pinned script to validate exact eight payloads, edit, style, sizes and hashes. Changed sources/manifests cause rejection, not regeneration of approvals. Offline prepare.py should not rewrite sealed manifests during an execution run.

| Guard | Enforcement |
|---|---|
| Exact model/voice | Hardcoded endpoint/model and Charon; manifest validation before admission |
| Exact fixtures/input/configuration | Sealed manifests, source/media hashes, reconstructed text, byte counts, styles, 8192/16384 caps, AUDIO/single candidate |
| Calls 1–8; <=8 primary | Exact ordered call set; one persisted primary per call |
| <=10 total /<=2 retries | Persisted intent counts checked before each POST; independently revalidated ledger |
| No hidden retries/fallbacks | Single HTTPX POST; HTTPTransport(retries=0), redirects/proxies disabled; no SDK or fallback path |
| RPM/TPM | Persist last intent timestamp; >=61 seconds between submissions, full 8192 input-token reservation per request; at most one in-flight under lock |
| RPD/no day reset | <=10 intents for entire experiment lifetime; no calendar rollover reset; owner reports 10 available, shared external project use remains a condition |
| Persistence before send | Atomic fsynced ledger intent+liability, then transport entry; advisory exclusive lock held across execution |
| States | prepared/rejected_locally events; submitting/succeeded/definite_failure/unknown_outcome attempt records |
| Unknown outcome | Persisted halt; submitting after interruption becomes unknown on reopen; no retry or further stage execution |
| IDs/usage/receipts | Allowlisted request IDs plus response ID and usage where supplied; sanitized receipt saved before decode |
| Maximum finance | 102400 integer microUSD per intent, lifetime liability <=1024000; never release reservations just because failure/timeout/day change |
| Fees | Nonzero fee parameter rejected before submission; larger required reservation needs owner decision |
| Isolated outputs | Fixed runs/approved-lite-v1 root, no custom live root; symlink ancestry rejected, private file modes |
| Validate audio | One STOP candidate containing one decodable, nonempty PCM WAV, complete frames, finite duration and bounded bytes; invalid response stops, not success |
| Secrets | Key loaded only after explicit live token; header only, not URL; allowlist/redaction and generic exception handling; no .env loading in tests/dry-run |
| Resume | Skip successful calls; check saved audio hash, halt if missing/changed; lost ledger beside execution evidence rejected |
| No unrelated work | Only TTS REST payload, local JSON/base64/WAV inspection; no image/text/search/render/job execution |

No automatic retry loop: independently established safe failed attempts may be retry candidates on explicit restart within the original two shared slots. Fake transport models confirmed safe 429/non-execution. **A live 429 alone is not evidence of non-execution or zero charge:** real transport marks it uncertain and halts. Schema rejection retains liability but stops separately from acoustic failure. Successful HTTP with invalid WAV retains receipt and exposure, blocks retry; local installation errors/unknown persist conservatively. No automatic reconciliation, schema variation or duplicate-risk override is provided. A halted experiment requires separately reviewed reconciliation/owner decision before any future recovery change; do not hand-edit counters.

Timeouts: connect 15s, phase inactivity 120s, bounded streamed response; monotonic response-duration check at 900s on chunks. This is not guaranteed provider cessation and not a strict independent process-level total deadline; any timeout/interruption is unknown and blocks replacement. A truly unresponsive transport can require owner interrupt, whose persisted intent prevents unsafe retry. No completion-time promise.

## Mathematical bounds

Let P be primary intents and R retry intents. Admission checks `P<8`, `R<2` for a retry, and `P+R<10` independently before fsynced intent. One intent invokes transport at most once. Unknown/interrupted intent remains counted even if no packet actually left. Single exclusive lock prevents overlapping admission. Therefore outbound submissions <= intents <= P+R <=10, with P<=8 and R<=2. Dry-run performs zero sends. A ten-intent ledger is still exhausted on a later day.

Financial bound per submission =8192×$0.50/1M +16384×$6/1M = **$0.102400**. Eight primaries **$0.819200**; ten intents **$1.024000**, before applicable fees. Retained per-attempt maximum liability is independent of usage missing/unknown outcomes. No currently known extra fee was supplied; Free tier is owner-reported and no paid activation occurs. If account charges/fees alter this ceiling, runner refuses nonzero extra fees rather than enlarging authority. Reconfirm current account/prices/quota before eventual execution; existing owner report is not a live balance guarantee.

## Reproducible local verification

Run:
```sh
/private/tmp/alpha-s4-venv/bin/python spikes/narration-feasibility/test_runner.py
python3 spikes/narration-feasibility/runner.py
python3 spikes/narration-feasibility/runner.py --stage 2
```

Only tests and dry-run were invoked. Test harness denies DNS/socket connection, uses dummy secrets, in-memory WAV and temporary local ledgers. The HTTPX path itself is exercised with public MockTransport; one POST on synthetic 429, no SDK retries. [Machine results](runner-verification.json) record **27 PASS cases**, maximum ten fake submissions in any scenario, **zero real requests**. Synthetic interrupted-process hooks represent exact persistence windows, not OS SIGKILL testing; full power-loss filesystem durability remains bounded by earlier local S3/S7 evidence. No voice/quality/alignment result inferred from a tone WAV.

Retained preparation finding: an ancestry guard initially rejected macOS's standard /var symlink in temporary test paths. Tests now resolve the temporary root before runner creation, matching canonical live evidence storage; all scenarios rerun. No provider request occurred on the failed witness.

Dry-run records exact calls/model/voice/input hashes and sizes, eligible timestamps, counts/slots, remaining maximum tariff and output paths. Stage 2 dry-run is a preview only: live Stage 2 is blocked before validated Call 1 plus its distinct authorization. Actual persistent live ledger created by dry-run has **zero intents**; no calls executed.

## Stage 1 — later explicit authorization only

Command design (NOT RUN):
```sh
/private/tmp/alpha-s4-venv/bin/python spikes/narration-feasibility/runner.py --stage 1 --live-authorization AUTHORIZE_S5_LITE_CALL_1
```

Only Call 1: original Scene 19, 41 words, 240 UTF-8 text bytes plus 70 style bytes, Charon/Flash-Lite, text hash `2128518f2844aec57552b45d5206407426fe19288377b01428682b9e4fbb30b2`. Checks ledger/seals/pacing/budget; persists intent before one POST; captures receipt; validates WAV; stops. Schema/model/endpoint failure or uncertainty halts. Success is technical format success, not word-fidelity or narration-quality acceptance.

## Stage 2 — separate later continuation only

Command design (NOT RUN):
```sh
/private/tmp/alpha-s4-venv/bin/python spikes/narration-feasibility/runner.py --stage 2 --live-authorization AUTHORIZE_S5_LITE_CALLS_2_8
```

Requires persisted valid Call 1 and distinct authorization. Does not start automatically after Stage 1. Executes remaining approved calls only, stops at first failure/unknown, skips completed calls on resume. Typing these flags is operator authorization, not permission conferred by preparation or this report.

## Exact output locations

Root: `docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/`
- `ledger.json`: persisted intents, reservations, events, outcomes and halt.
- `runner.lock`: single-run exclusion.
- `dry-run.json`: latest dry preview (Stage 1/2).
- `attempts/attempt-NN-receipt.json`: sanitized provider response/available IDs.
- `audio/call-NN/attempt-NN/source.wav`: validated immutable source output, never production project state.
- `rejected-locally.json`: sanitized CLI setup/guard rejection, when applicable.

Local tests create their WAV/ledger fixtures in temporary directories, removed on exit. No real generated audio exists. Fixed root prevents casually creating another quota budget via a --run-id parameter; deleting/resetting execution evidence is not a supported operation.

## Remaining uncertainty

API/server: SERVER_ACCEPTANCE_UNPROVEN; official schema and mock wire verified, no key tested. Authorized Call 1 can witness actual acceptance and format; no tiny preliminary call.

Audio: synthetic decoding proves validation behavior only; approved-word fidelity, continuity, mapping and A/B/C listening remain S5 real evidence.

Account/quota: Free tier/3 RPM/10K TPM/10 RPD/ten remaining supplied by owner without observation timestamp. No programmatic balance query. Other project activity/provider accounting can change remaining allowance; internal lifetime cap cannot control unrelated API clients. Runtime does not switch tiers or assume a new day. No new product decision introduced.

Earlier plan/preflight/provider findings preserved. Added runner.py/test_runner.py, this report and runner-verification.json; README instructions and zero-submission dry-run evidence only. No authoritative specification changed.

ZERO real Gemini requests; key not exposed; Calls 1–8 unexecuted; S6/S9/production/TASKS.md/deployment/purchases unexecuted.

## Recorded cases

| Case | Result | Fake submissions |
|---|---|---:|
| eight successes; default dry-run; staged continuation; duplicate invocation idempotent | PASS | 8 |
| confirmed safe fixture 429 retries; absolute ten submissions; resume preserves counters | PASS | 10 |
| two-retry budget exhausted stops third retry | PASS | 3 |
| timeout unknown holds liability and halts restart | PASS | 1 |
| interruption before_intent | PASS | 1 |
| interruption after_intent | PASS | 0 |
| interruption after_response | PASS | 1 |
| concurrent runner denied by process lock | PASS | 0 |
| resume partial success skips completed audio | PASS | 9 |
| sealed manifest rejects text | PASS | 0 |
| sealed manifest rejects model | PASS | 0 |
| sealed manifest rejects voice | PASS | 0 |
| sealed manifest rejects money | PASS | 0 |
| missing audio stops; receipt retained; no technical success | PASS | 1 |
| undecodable audio stops | PASS | 1 |
| Call 1 schema rejection prevents further calls and schema variants | PASS | 1 |
| unconfirmed live-style 429 is not assumed unbilled | PASS | 1 |
| secret redaction in receipts and ledger | PASS | 1 |
| fake clock enforces RPM and conservative 8192-token TPM reserve | PASS | 8 |
| fees cannot silently enlarge reservation | PASS | 0 |
| stage2 prerequisite and distinct authorization enforced | PASS | 0 |
| actual HTTPX public transport path: one POST, camelCase REST schema, synthetic 429 no retry | PASS | 1 |
| independent financial admission check before submission | PASS | 0 |
| saved audio missing on restart halts without repeat generation | PASS | 1 |
| clock rollback cannot bypass persisted pacing | PASS | 1 |
| new calendar day never resets experiment budget or quota counters | PASS | 10 |
| missing ledger with execution evidence blocks reset/resubmit | PASS | 1 |
