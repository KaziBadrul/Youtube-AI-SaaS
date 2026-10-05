# S5 real-call preflight — 2026-10-04

**NOT_READY. No Gemini API request, Calls 1–8, or live quota/key verification performed.** Public documentation retrieval only. No live runner created during this verification.

## Local configuration and account status

Repository .env contains a nonempty GEMINI_API_KEY; current process environment does not. Values were not printed or recorded. No relevant local project ID/tier/billing setting was available in .env/process. An API key does not establish project identity, billing state, quota or permission; authenticity/active status unverified. Account tier **UNKNOWN**, remaining quota **UNKNOWN**, applicable taxes/fees **UNKNOWN**. Historical owner quota row is not current balance; no authenticated dashboard inspected and no provider endpoint queried.

Manually in Google AI Studio, identify the existing key by its local entry privately, select its associated project on API Keys/Projects and inspect billing/usage tier (Free or paid Tier 1/2/3). Then open that same project's active rate-limit/usage view for exact `gemini-3.8-flash-tts`, not Flash-Lite. Report dated/time-zoned tier, RPM, TPM, RPD limit, today's used RPD and remaining RPD if explicitly shown, dashboard refresh time and any pending/unsettled requests. Ten available slots are needed to reserve eight primary plus two retries. If dashboard is stale or only provides a usage estimate, report remaining UNKNOWN; don't infer exact balance. Other keys on this project share quota; keep other activity paused. Check billing account currency/tax/fees and available monthly budget without enabling/upgrading billing. Do not share keys or project secrets. RPD resets midnight Pacific, per official documentation.

## Published pricing and limits

Reverified authoritative sources 2026-10-04:
- https://ai.google.dev/gemini-api/docs/pricing — standard Flash TTS input $0.50/million, output audio $9/million through Dec 31, 2026; free tier listed but not established for this key. Starting Jan 1, 2027 rates double.
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts — 8,192 input /16,384 output serving tokens; default unary WAV.
- https://ai.google.dev/gemini-api/docs/rate-limits — RPM/TPM/RPD, project scope and Pacific midnight reset; active limits in AI Studio vary by tier/model/account.

Finite tariff unchanged: 8192×0.50/1M +16384×9/1M = $0.151552/submission; eight $1.212416, ten $1.515520. These exclude unestablished taxes/account fees; cannot claim all-in liability. Experimental plan requests standard service only, no caching/tools. Account evidence 3 RPM /10,000 input TPM /10 RPD remains historical supplied evidence, not today's verified entitlement or remaining balance.

## Fixtures and executable safeguards

[Read-only validation](preflight.json): all four pinned demo source hashes and all eight text hashes/content/byte counts/styles/model/voice match. No preparation regeneration or fixture mutation performed. Calls all specify gemini-3.8-flash-tts, Charon, AUDIO, one candidate, 8192/16384 serving bounds and max_output_tokens=16384. Exact tokenization remains unmeasured; chars/4 proxy is not a hard tokenizer.

**There is no live runner.** prepare.py and score_alignment.py are offline only. Therefore 8-primary/10-total/2-retry limits, cross-restart admission, pacing, manifest pinning, no fallback/expansion, durable attempt evidence and unknown-outcome stop are not executable safeguards yet. JSON declarations are not enforcement. They must be implemented in an isolated experiment runner and locally tested before real authorization/execution.

S4 separately demonstrated generateContent attempts=1 with one synthetic send on the pinned SDK/HTTPX path. Interactions has different hidden retry behavior and is not allowed here. This is historical local evidence, not proof a nonexistent S5 runner disables hidden retries. SDK/source pin must match and witnesses be rerun on change. No legacy generation script should be invoked: importing it creates credential-bearing clients and its excessive retry policy is incompatible.

Accepted unknown-outcome requirement remains: persist send-start/attempt IDs and receipt identifiers, retain maximum liability/quota, halt unsafe retry/overlapping work after possible receipt, reconcile or obtain explicit duplicate-risk owner authority. Local decode/alignment errors reuse received bytes. Policy verified against plan; runner enforcement **not verified**.

## Output isolation

Existing preparation evidence: docs/architecture/evidence/narration-feasibility/.

Exact proposed future convention, not yet enforced/created:
- docs/architecture/evidence/narration-feasibility/runs/<run-id>/audio/call-01/attempt-01/source.wav (or recorded actual-format source file)
- same run root /attempts/call-01/attempt-01.json and /manifest.json, /ledger.json
- same run root /derived/ for comparison cuts/assemblies and /evaluation/ for reviewed alignments/listening scores.

Raw provider bytes and metadata must survive before normalization. No credentials in receipts; sanitized allowlisted headers only. Run root must be exclusive/non-overwriting, private/git-excluded for any sensitive audio/content. No production DB/project selection or demo source mutation. These names clarify the previously unspecified output layout; no runtime binds writes there yet.

The currently executable prep/scorer invoke no image/text/research/render/production stage. No live runner exists to audit for those exclusions, so full live-stage isolation is a prerequisite, not an accomplished finding.

## Changes from plan and blockers

No fixture, price, model, voice, experiment size, or accepted policy changed. Preflight exposes the plan-to-execution gap: missing executor, unknown tier/quota/fees, no verified live output routing. New proposed run subdirectories are documentation only. Source-of-truth specifications and S5-PLAN.md unchanged. Added this report and preflight.json only.

No provider request, production implementation, S6/S9, TASKS.md, deployment or purchase occurred. Stop pending manual account evidence and separately scoped isolated runner preparation; no call authorization inferred.

## Owner report and Flash-Lite manifest update

Owner reports Free tier, 3 RPM /10K TPM /10 RPD for both models and all ten requests available. No observation timestamp supplied; this is owner evidence, not a programmatic balance query or guarantee at execution. All eight calls now pin gemini-3.8-flash-lite-tts/Charon and unchanged fixtures/styles. Ceiling is $0.102400/request, $0.819200/eight and $1.024000/ten before applicable fees. Local fake-transport verification: eight exact payload/model/voice/cap cases, each one send on synthetic 429. The original typed-style test failed before submission because SDK 2.3.0 Part does not accept speech_metadata; the public HttpOptions.extra_body path preserves structured style in the tested wire body. Live schema acceptance is unproven. No dependencies changed. Still NOT_READY: no live runner, hence hard caps/pacing/persistent unknown-outcome safeguards and output routing remain unenforced. Earlier findings above are historical; no live call authorized or executed.

Additional retained local finding: the first wire assertion expected camelCase nested voice fields, while pinned SDK 2.3.0 serializes voice_config/prebuilt_voice_config/voice_name inside speechConfig. The witness now verifies the exact emitted object. This is not evidence that the current service accepts that older wire shape; resolve schema compatibility offline before a live runner is declared ready.
