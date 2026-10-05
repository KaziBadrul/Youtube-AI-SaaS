# S5 — narration strategy experiment plan

2026-10-04. **READY_FOR_REAL_CALLS as an experiment design, not authorization or S5 PASS. REAL_CALL_REQUIRED.** Execution is gated on explicit owner authorization, active account/tier/quota and price/fee checks, and reviewed one-send runtime. No provider request, including free-tier TTS or CountTokens, was made. S6/S9 remain unexecuted. Original S4 FAIL and S4-R conditional PASS are preserved unchanged.

## Claim, failures and predeclared criteria

Claim: approved scene words can be generated in a bounded scene/segment policy, mapped to immutable source ranges and assembled/corrected/restored without unacceptable speech discontinuity or uncontrolled requests. Failures sought: changed/missing/repeated words; unextractable scene boundaries; voice/prosody drift; unnatural splices; excessive requests; broad hidden correction costs; context speech leaking into corrected scenes; unapproved restoration of sibling words/configuration.

Minimum controlled screen: three actual contiguous scenes independently generated versus their identical passage inside a 498-word source; one edited scene; whole-segment replacement versus isolated/context-assisted correction; one alternate-delivery scene-only restoration. Reuse scientifically identical source audio. Eight primary submissions plus at most two shared safe-failure retry submissions. Do not spend retries on extra variants or ambiguous failures.

A candidate passes this screen only with complete approved-word fidelity, reviewed non-clipping scene mappings, publishable joins/continuity and recorded bounded scope. Listening anchors below apply to every tested initial/corrected assembly. C additionally must preserve unaffected source bytes and exclude context words. Local mechanics do not satisfy acoustic criteria. Successful screening does **not** complete the accepted full S5 protocol: representative distinct 3/5/10-minute approved scripts, other segment-size boundaries and heterogeneous/oversized configurations remain conditional follow-up if they affect selection. No strategy is selected now, and no eight-call experiment can establish arbitrary long-form quality.

## Source inspection and fixture

Read AGENTS.md, CLAUDE.md, docs/README.md, ALPHA_PRODUCT_SPEC.md, ARCHITECTURE.md, ARCHITECTURE_SPIKES.md, ARTIFACT_MODEL.md and its accepted narration amendment; provider S4 report/inventories/local evidence and S4-R closure; historical TTS/alignment source. Applicable job/cost/restoration constraints remain unchanged.

Canonical external sources inspected read-only:
- `../YoutubeAI/python-scripts/create_tts.py`: sentence extension after ~500 words, tail <200 words merged up to hardcoded 700; inline directions converted to speech_metadata; FFmpeg concat demuxer stream-copy assembly. Does not persist stable scene/segment mapping. Legacy initial plus twenty retries, credential initialization on import, no explicit timeout/output cap: do not import/run it.
- `../YoutubeAI/python-scripts/make_timestamps.py`: faster-whisper base CPU/int8, VAD and word timestamps; rapidfuzz scene matching accepts score>=55; skips unmatched scenes and extends preceding scene to next matched start. This can conceal missing speech/gaps. ASCII/contraction normalization even maps “were” to “we're.” Fuzzy score is not complete word fidelity.
- External loose requirements do not establish a pinned alignment runtime. Current preparation Python lacks faster_whisper and rapidfuzz; no weights downloaded. Manual word/boundary annotation is the independent reference; actual ASR runtime/source pin and cached weights must be verified offline before running it. If unavailable, compact manual mapping can score the screen, but automated alignment reliability remains unresolved and cannot pass S5.

[Fixture manifest](fixture-manifest.json) pins script/media/timestamp hashes, every exact scene, configuration and controlled edit. The immutable source is `demo-video-example/script.txt`: 49 scenes, 750 regex spoken words; existing audio is mono 24 kHz PCM16, 265 seconds. About 169.8 words/minute and 11.1 scenes/minute. These are measured fixture properties, not standard creator pacing.

Initial block: Scenes 1–32, 498 words, 2,891 UTF-8 bytes, exact text SHA256 `333db790f6e8dda32f42fd40bd03ddd29998128ab59aff9d60197494a39e6b95`. Comparison Scenes 19/20/21: 41/23/9 words. They expose long/short utterances, expressive punctuation, a Wizard of Oz analogy and a topic transition. Their 73-word matched excerpt is scored identically across strategies; also listen to the entire larger source for drift/pacing.

Controlled Scene 20 edit: “three weeks” → “a month”; all other words/configuration unchanged. Original and edited versions are separately hashed. This is an experimental fixture edit, not alteration of project source files. Script and `03_scenes.json` disagree on Scene 35; the initial run discovered this and stopped its equality assertion. We explicitly pin script.txt; never substitute JSON words. Scene 35 is outside the live comparison block. Historical audio model/voice/memberships are unverified: use it for duration/runtime calibration only, not a fair provider strategy baseline. Initial failure is retained in [preparation findings](README.md).

## Strategies and deterministic segmentation

A: one scene/request. Precise regeneration scope but many independent starts/joins, request pressure and retry records. A is not assumed to fail acoustically; at this measured scene density it cannot provide a full project in one 10-RPD day.

B: whole contiguous scenes grouped under exact UTF-8 payload ceilings, homogeneous effective voice/language/delivery, then verified provider token/output limits. Natural scene sentence boundaries preserved; no punctuation rewrite or sentence splitting across ordinary scenes. Tested local exploratory payload caps: 2,000/3,000/4,000 bytes (roughly 500/750/1,000 chars/4 token proxies, approximately 340/500/680 words for this fixture). These are **not certified token counts**, production settings or optimal sizes. Actual request includes style/configuration overhead; input hard serving cap remains 8,192 tokens, output 16,384. Size estimates never establish liability. Oversized individual scenes are blocked for explicit bounded subsegment planning; no truncation. Configuration conflicts form boundaries, not silently unified settings. Freeze memberships before edits, replace only the affected segment; no global rebatching.

C: initial source as B; replace only Scene 20's validated range. C1 uses the same edited isolated source as A. C2 generates Scenes 19–21 including edited Scene 20 as a natural context window; retain only Scene 20 after verified alignment. Context speech is never repeated in assembly. Compare hard natural-pause joins first. A local pause-only fade is permissible only if it cannot touch speech and is recorded; no automatic crossfade may hide word/prosody defects. C fallback to B is an additional accounted operation, not a cost-free trick.

## Request projections before live work

[Machine-readable counts](request-counts.json) repeat measured scene distribution and extrapolate scene count from audio duration; they are projections, not fabricated independent 3/5/10-minute recordings. Estimated words: 510/850/1,699; discrete repeated-scene fixture actual words: 526/857/1,659. Final approved representative projects may differ.

| Minutes | A initial | A + one correction + two safe retries | B/C initial at 3,000-byte cap | B/C + one correction + two safe retries | C + failed surgical correction + B fallback + two retries |
|---|---:|---:|---:|---:|---:|
| 3 | 34 | 37 | 2 | 5 | 6 |
| 5 | 56 | 59 | 2 | 5 | 6 |
| 10 | 111 | 114 | 4 | 7 | 8 |

At 2,000 bytes B/C initial =2/3/5; at 4,000 =1/2/3. Voice/configuration boundaries can increase counts. Two retries here are **shared scenario headroom**, not a guarantee every failed operation can retry twice within 10 RPD. Worst case three attempts for every initial/correction operation: A=105/171/336 and B at 3,000 bytes=9/9/15. Larger failures may require another day; never reset operation counters at midnight. Initial A alone requires at least 4/6/12 quota days if all ten daily calls are available, before correction/retry. B/C plausible, not proven optimal or economical.

Supplied account evidence is 3 RPM / 10,000 TPM / 10 RPD for both TTS models, not universal Gemini guarantees. Earlier usage rows were Flash 2/10 daily and Lite 11/10 daily; tier and reset timestamp unknown. Do not assume ten remaining requests, combine model pools, or guarantee same-day execution. Eight base calls can fit a fresh ten-call day with two shared retries if actual remaining quota supports it. At most one in-flight submission; schedule no more than three in any rolling minute and respect the active TPM accounting, conservatively reserving full 8,192 input tokens if tokenizer information is unavailable. Use at least a minute between starts under that fallback and wait longer if the account includes other token dimensions; timings are pacing, not a guarantee of provider availability. Record limiter delays and quota receipts. Missing current capacity prevents execution, not a reason to change strategy.

## Local witnesses and alignment evaluation

Reproduce: `python3 spikes/narration-feasibility/prepare.py` (standard library, DNS/socket connections denied, no credentials/SDK). [Local results](local-results.json): exact ordered once-only scene membership, verbatim text, byte caps, oversized rejection; synthetic sample-exact replacement/prefix/suffix preservation, later-offset recomputation, reorder/delete range reuse; alignment-scoring positives and missing/repeated/overlap/normalization negatives. No narration output or quality simulated. File registration/crash/accounting/restoration authorization remain S3/S7's already tested scope; not reimplemented here.

Five contracts remain distinct: Scene Narration Text; Narration Generation Segment; immutable Source Narration Audio; Alignment/Scene Audio Mapping; Derived Project Narration. Live evidence must record each source hash/attempt/receipt/configuration/membership; mappings contain scene text hash, source hash, sample ranges, word correspondences, method/version/confidence; assembly contains ordered ranges/offsets/join transforms. No mutable merged WAV is the source of truth.

`score_alignment.py` accepts approved text plus reviewed word start/end JSON. It reports exact normalized spoken-word edit distance/WER, finite ordered word ranges and boundary-error distribution. Independently annotate first/last spoken samples, pause ownership and internal scene cuts by listening/waveform inspection; compare ASR to that reference. Report missing/repeated/substituted words, uncertain pronunciation, drift at scene/segment boundaries and after correction; do not infer zero defects from fuzzy score. Numeric boundary errors are measured, not invented acceptance thresholds. Human reference must confirm no clipped/repeated/unassigned speech or context leakage before a range is exportable. Preserve ASR raw results/confidence; failed/ambiguous mappings remain non-exportable. A word count alone does not prove pronunciation or mapping.

For corrections, report provider submissions, approved/context words and exact usage, actual duration delta, unaffected source hashes/ranges, changed mapping/caption scope, global offset delta, local labor, maximum/recorded cost. B regenerates 498 words including unchanged siblings; A/C1 23; C2 73 but selects 23. Local later-offset changes do not regenerate later sources. Incompatible manual timing/captions stay preserved/outdated.

Restore the old Scene 20 range after its edit only with explicit compound old-words+audio approval; compare old words versus current edit visibly. Restore call 8's same words/different recorded delivery only for Scene 20, leaving project defaults/siblings intact. Validate new joins and compatible scene-local captions/timing. Restore full old segment only with full affected-scope approval. Test reorder Scenes 19/21 and deletion of Scene 20 locally using validated ranges, listening for changed joins. If unsafe, block and report; no silent paid repair. No new S7 state-machine implementation needed.

## Blind listening rubric (predeclared)

Randomize neutral clip labels with a saved concealed mapping; listener gets approved words and edit intent but no strategy or predicted winner. Include matched initial excerpt, edited A/B/C1/C2, full B source, and restoration/order variants. Same device, comfortable fixed level, no speed adjustment/music. Two listening passes; record time-coded observations before revealing labels. If only owner listens, report single-listener limitation, not independent panel validation. Record actual correction time; 15-minute product target remains, but a compact screen cannot prove full-project correction effort.

Score each dimension 2=PASS, 1=NOTICEABLE BUT ACCEPTABLE, 0=FAIL. A 1 means audible on attentive listening yet listener would publish unchanged; 0 requires intervention to publish. Intentional alternate delivery is assessed against its chosen configuration, not penalized merely for being different.

| Dimension | 2 | 1 | 0 |
|---|---|---|---|
| Voice consistency | Same apparent narrator/timbre through joins | Slight timbre/room shift, publish unchanged | Sounds like unintended speaker change/drift |
| Prosody continuity | Emphasis/intention flows across boundaries | Minor reset, meaning intact | Emphasis reset or delivery contradicts passage |
| Pacing continuity | Natural cadence and pause progression | Small speed/pause change | Jarring tempo or awkward silence requiring edit |
| Boundary naturalness | Complete words with natural transitions | Detectable boundary, speech intact | Clipped syllable, glued speech or unnatural break |
| Word fidelity | All approved spoken words correct | **Not allowed as a fidelity pass**; pronunciation uncertainty requires review | Omitted/repeated/changed words, extra context/directions, material mispronunciation |
| Audible joins/splices | No audible technical splice | Small harmless texture/level change | Click, abrupt cut, overlap or distracting level jump |
| Correction naturalness | Edited region belongs in surrounding performance | Detectable but publishable correction | Edit sounds inserted/semantically unnatural |
| Overall publishability | Would publish unchanged | Would publish; note small blemish | Requires correction before publication |

Acceptance: fidelity=2, all relevant other dimensions>=1, overall>=1, reviewed complete mapping and no unresolved clipping/context leakage. Do not average a 0 away. Log repeatable failures; evidence needed after a disputed rating instead of optimistic selection.

## Proposed real-call manifest — NOT AUTHORIZED

All calls: `gemini-3.8-flash-lite-tts`, Charon, English, standard unary generateContent, one candidate, AUDIO, exact fixture content only, structured speech_metadata style (not spoken instructions), no tools/cache/history. Calls 1–7 share identical conversational documentary style; 8 changes only delivery to calm reflective. Serving bounds 8,192 input /16,384 output tokens. Request `max_output_tokens=16384`, but financial safety uses documented serving cap, not an unverified tighter audio cap. Current model defaults WAV: detect actual MIME/header/sample format rather than wrapping returned WAV as raw PCM. Preserve receipt/bytes before decode. S4 2.3.0 synthetic wire pin is not live schema acceptance; rerun its one-send witness if any SDK change is necessary. No endpoint fallback or hidden second submission on schema error.

| Call | Strategy/purpose | Exact fixture | Spoken words / UTF-8 bytes | Max provider tariff USD |
|---|---|---|---:|---:|
| 1 | A initial | Scene 19 original | 41 / 240 | 0.102400 |
| 2 | A initial | Scene 20 original | 23 / 124 | 0.102400 |
| 3 | A initial | Scene 21 original | 9 / 43 | 0.102400 |
| 4 | B and C shared initial | Scenes 1–32 original | 498 / 2,891 | 0.102400 |
| 5 | A edit and C1 reuse | Scene 20 edited | 23 / 120 | 0.102400 |
| 6 | B edit | Scenes 1–32, Scene 20 edited | 498 / 2,887 | 0.102400 |
| 7 | C2 context correction | Scenes 19–21, Scene 20 edited | 73 / 407 | 0.102400 |
| 8 | Narration-specific restore | Scene 20 original, alternate delivery | 23 / 124 | 0.102400 |
| 9–10 | Shared safe retry reserve only | Exact failed authorized call/config, never new variant | <=largest authorized payload | 0.102400 each |

[Exact JSON](real-call-manifest.json) includes all payloads/hashes and style bytes: 70 bytes normal, 69 alternate. JSON/schema overhead is not equated to speech input tokens. Chars/4 proxies are recorded for sizing only; not a token guarantee. Exact text/style bytes bound submitted content, full model limits bound billed units. No live CountTokens or key/project query is part of this authorization proposal. Call 4 supplies both initial B and C; call 5 supplies both edited A and C1. Call 8 tests the remaining audible scene-only restoration assumption rather than duplicating S7 approval logic. Without that requirement the A/B/C core is seven calls.

Finite conservative ceiling: ceil(8,192 × $0.50/1M + 16,384 × $6/1M) = **102,400 microUSD/request**. Eight primary = **$0.819200**, two shared retries = **$0.204800**, maximum ten submissions = **$1.024000 provider tariff**. Full output bound corresponds to 655.36s at documented 25 audio tokens/s; not a promise of requested narration duration. Actual successful usage may be much lower; expected audio duration is not a hard financial bound. Account taxes/fees must be captured: total maximum is $1.024000 × (1 + applicable maximum tax fraction) + bounded account fees. If these cannot be established or fit remaining $30 monthly budget, do not execute. Thus no unconditional all-in account bill is claimed.

Pricing retrieved 2026-10-04; refresh before calls. Introductory prices end 2026-12-31; subsequent listed rates double this ceiling ($2.048000 for ten). Free tier is documented but actual key/project/tier/remaining quota not established: **free execution possible, not assumed; liability reserved at paid standard tariff**. No key possession implies authorization. Retry ceiling is two per failed operation **and** two shared across this experiment, ten total; no guaranteed retry reserve per every operation.

One local attempt = one outbound submission, explicit attempts=1 generateContent, lower transport retries=0, no redirects/tool turns, persisted receipt and send-start, explicit phase timeouts plus whole-attempt deadline. Timeout after possible submission/unknown outcome retains liability and quota hold and blocks automatic overlapping retry. Record response/request IDs, usage, finish status, source hash before local decode; missing usage remains unknown. Gemini lost-ack outcomes are only partially reconcilable: saved response/log/account/support evidence where available; absence from logs does not prove no charge. Owner-assisted resolution or explicit duplicate-risk authorization required; this plan does not authorize risky resubmission. Safe known failure retries only within limits. Local installation/alignment failures reuse recovered bytes, not a TTS retry.

## Decision rule and remaining evidence

Eliminate candidates failing any hard fidelity/mapping/quality requirement. Among passing strategies prefer simplest, with measured meaningful quality/correction/operational benefit required for extra complexity. A remains quality comparator but its measured-density one-day quota infeasibility must be disclosed; no silent relaxing cohort requirements or switching account tier. B cannot win only on count. C may be selected only if both joins and correction mappings pass and measurable source preservation/correction savings justify extra complexity; if only context correction passes, pin that scope, not isolated capability. If C fails, consider B/A only if they pass independently. Hybrid needs demonstrated scope, not an invented fallback policy.

This compact screen can reject a strategy, identify a conditional leading candidate or require narrow additional evidence; cannot certify final segment size or entire S5 by itself. Full protocol still needs distinct approved 3/5/10 fixtures (currently projections), additional boundary/configuration/oversized cases as relevant, automated alignment runtime/reliability, model variability and actual usage/quota observations. No strategy is selected today. If none passes, S5 FAIL; if ambiguity remains, propose smallest separate bounded follow-up, never consume live-call reserve as unapproved exploration. User confirms any resulting architecture revision before implementation.

Internal policy remains behind scene-facing editing. Shared regeneration scope is explained truthfully (“Scenes 1–32; their unchanged words are preserved in the regenerated request”), with spending available optionally under one-tap authorization; no mandatory financial-review screen reintroduced. Prototype examples are not actual membership proof.

## Authoritative documentation sources

Retrieved 2026-10-04; documentation only, not provider inference calls:
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-lite-tts — serving caps, WAV default, structured style/transcript behavior.
- https://ai.google.dev/gemini-api/docs/pricing — standard/free rates, dated introductory transition, audio-token conversion.
- https://ai.google.dev/gemini-api/docs/speech-generation — voice catalog/Charon and formats/style guidance.
- S4 account/source/transport inventory is referenced without rerunning other capability investigations. Account quotas remain supplied evidence, not universal guarantees.

## Scope and conclusion

Local preparation complete; audible and alignment evidence requires separately authorized TTS. No accepted product/design/architecture requirement modified. No production code, live provider call, S6/S9, TASKS.md, deployment or purchase.

## Owner-directed model update

All eight planned calls now use Flash-Lite, unchanged voice/text/styles. Owner reports Free tier and ten remaining requests, 3 RPM/10K TPM/10 RPD. Report has no observation timestamp; reconfirm freshness before execution. Historical preflight UNKNOWN findings remain historical. No live call authorized. The updated conservative tariff is $0.102400/request, $0.819200 for eight and $1.024000 for ten before applicable fees. A live runner is still absent; executable cap/pacing/unknown-outcome enforcement is not verified.
