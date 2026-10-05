# S9 revision 7 — bounded text/research manifest

2026-10-05. **S9: NOT_YET_PASS.** Local fixture, candidate manifest and deterministic witness only. Zero provider/API calls, spend, downloads, production implementation, TASKS.md, deployment or purchases. $30/month ceiling unchanged. No final credits, tester allowances, image-density change or narration change.

**Result:** the operation inventory and a finite **candidate** text/search envelope are now explicit: **$0.410964 before fees**, allowing up to three admitted attempts per logical operation. This is **not an enforceable live authorization**. The candidate model lacks an established complete-request input-token validator in this environment; live usable text/search maximum remains **UNKNOWN**, and paid admission fails closed. Expected text/search usage/cost also remains **UNKNOWN**. Do not promote the candidate arithmetic to an established maximum or use a provider's enormous context window to hide the missing input proof.

## Authority and reused evidence

Read the documentation index/AGENTS, current Alpha specification, UX/architecture/spike/cost contracts, owner Research/discovery entitlement amendment, S4/S4-R, S5 receipts and final B mapping closure, S6 runtime evidence and S9 v5/v6. Existing pricing snapshot [pricing-v6.json](pricing-v6.json), retrieved from official sources 2026-10-05, is reused without a new public fetch or API call. [S4-R](../../research-feasibility/S4-R.md) supplies bounded application-owned Basic searches, provenance and safe attempts; [S4](../../provider-feasibility/S4.md) supplies conditional text cap semantics, one-send retry isolation and reconciliation. No historical file/result is rerun or rewritten.

Normal text model candidate is **`gemini-3.5-flash-lite`**, the existing S4-R reference at $0.30/M input and $2.50/M output including thinking. This is not final production selection. The owner's `gemini-3.8-flash` decision is for **Custom Topic Suggestions**, not automatic selection for script/research. Discovery operations are excluded from this production manifest. Tavily Basic is $0.008/credit, one credit/request; no free allowance assumed for financial bounds.

## Representative five-minute factual fixture

Reuse the existing topic **“The Moment You Realize Your Parents Are Just Guys”**, from `demo-video-example/01_script_raw.txt`, with its full `02_script_humanized.txt` as a downstream **historical size/content fixture**, not as newly researched or newly approved output. Educational focus: parental de-idealization, adolescent/emerging-adult autonomy, and emotional/relationship variation. This is the same intended faceless educational use case as the narration example, not a two-sentence cheap case.

Full historical narration: **762 words, 4,376 UTF-8 bytes**. The unchanged v5 counter yields **59 sentences**, with ellipses/quotation flags and **REVIEW_REQUIRED**. Its 49 historical scenes do not override the newer sentence-driven scope. No script is rewritten. The five-minute target is a requested fixture duration, not a measured new TTS duration. Actual generated script, sentence count, factual coverage and quality remain unmeasured.

The primary manifest assumes Research entitlement for 3 videos/week or 1 video/day, then factual-topic Research is automatic under the existing rules. This is a synthetic eligible-feature fixture, not a commercial/private-Alpha entitlement grant. A separate branch removes Research for unentitled topic users; pasted-script checking remains unchanged.

## Which stages require paid requests?

| Investigated stage | Candidate implementation boundary | Paid operation |
|---|---|---|
| A Research planning | Tool-free query planner, validated locally and pinned | One Gemini logical operation |
| B External search | One application-owned Basic Search per admitted query ID | At most six Tavily logical operations |
| C Research synthesis | Tool-free synthesis over bounded evidence, producing private Research Results/source IDs | One Gemini logical operation |
| D Script generation | Requested-duration/language script using research; preserve artifact boundaries | One Gemini logical operation |
| E Generated-script factual checking/validation | Separate factual checking is specified only for pasted scripts; local schema/source-ID/text validation still required | No additional mandatory generated-script checking call |
| F Scene splitting/planning membership | Deterministic sentence spans and immutable narration membership; review ambiguous parsing | Local; no paid sentence counter |
| G Visual descriptions | Proposed descriptions keyed to the admitted scene IDs | Combined in next operation |
| H Image prompts | Same structured output request as visual descriptions; no narration rewriting | One Gemini planning logical operation |
| I TTS preparation | Approved text, delivery metadata, deterministic coherent grouping | Local; no required paid voice-tag/humanization call |

Total candidate first-attempt ceiling: **four Gemini calls + up to six searches**, not nine mandatory AI stages. With all three attempts admitted: at most **12 Gemini submissions + 18 searches**. These are maximum counts, not expected usage, mandatory retries or authority to execute.

Separate research synthesis/script writing follows the already accepted Research Results → Script boundary and S4-R flow; it is not a new production redesign. Combining them into a validated response carrying both artifacts might be possible, but needs contract/quality validation and is not adopted to lower this witness's cost. Combining visual descriptions and image prompts is a bounded candidate batching choice, not a frozen production parser/adapter. If the batch cannot produce complete valid output within its cap, preserve valid artifacts and report failure/scope repair; do not spawn per-scene calls without new admission.

## Candidate operation manifest

Full names, dependencies, artifacts, attempts and configuration: [text-research-manifest-v7.json](text-research-manifest-v7.json). All text requests are single-turn, single-candidate, tool-free, no paid grounding/cache/history/background work, using the S4 one-send guard if adopted. All input caps cover **the entire prepared request's token-bearing content**, including system/schema/instructions, not just narration. Output limits include thinking, not an extra unbounded thought budget.

| Logical operation | Max logical operations | Input tokens/attempt | Output incl. thinking/attempt | Max attempts/op | Candidate max/attempt | Candidate group maximum |
|---|---:|---:|---:|---:|---:|---:|
| Research planner | 1 | 4,096 | 1,024 | 3 | $0.003789 | $0.011367 |
| Tavily Basic Search | 6 | N/A: request-billed | N/A | 3 | $0.008000 | $0.144000 |
| Research synthesis | 1 | 16,384 | 4,096 | 3 | $0.015156 | $0.045468 |
| Script generation | 1 | 12,288 | 8,192 | 3 | $0.024167 | $0.072501 |
| Visual + image-prompt planning | 1 | 16,384 | 16,384 | 3 | $0.045876 | $0.137628 |
| **Total** | | | | | | **$0.410964** |

Research stages are conditional on entitlement/applicability; script writing and planning are required for the topic path. Expected tokens and costs for **each** paid operation are UNKNOWN. Candidate ceilings are not final owner-approved production defaults or current spend authorization. Three attempts is an upper limit; only attempts fitting original authority and budget may proceed.

Dependencies/artifacts:

`Topic + eligible Research state → Query Plan → admitted Basic queries → bounded source evidence → Research Results → Script → reviewed local sentence/scene membership → Visual Descriptions + Image Prompts → image operations`

`Script → deterministic coherent grouping → B TTS → immutable source audio → fresh mappings → captions/continuous narration/render`

The latter path reuses S5; it adds no paid preparatory text call. Retain original input, script/research/prompt versions and successful work; rejected model output never becomes new budget authority.

### Query maximum and evidence limits

**Six is a conservative fixture-specific candidate maximum, not expected usage.** Three coverage axes have at most two slots each:

1. Definition/terminology and the research basis for parental de-idealization.
2. Developmental timing/autonomy in adolescence and emerging adulthood.
3. Emotional/relationship consequences and individual/cultural variation.

Two search slots per axis allow different phrasing/source routes without an adaptive search agent. [Example query plan](fixtures-v7/query-plan-example.json) is locally authored, not provider output or evidence of what typical projects need. It is within S4-R's explored 2–8 range without automatically selecting eight. This defines a finite authorized-candidate scope; **adequate factual coverage is unproven**. The planner may propose fewer queries; missing coverage is explicit. Over-six, malformed, duplicate or scope-changing proposals are **rejected before search**, not silently turned into an apparently complete research plan. No follow-up expansion, pagination, Extract, Crawl, Tavily Research or Gemini grounding.

Reused S4-R controls: <=400 UTF-8 bytes and <=50 words/query; explicit Basic, `auto_parameters=false`; pin `max_results=3`, `chunks_per_source=1`, usage included and answers/raw pages/images disabled. Each response <=32,768 bytes; title <=256 bytes, URL <=2,048 bytes, snippet <=1,500 bytes. New aggregate evidence envelope <=32,768 bytes across the six queries (up to 18 results), normalized in deterministic query/result order. Truncation is marked partial; rejecting overflow never refunds an already submitted charge or proves zero liability. Source identifiers, query, provider request/attempt IDs and usage provenance remain attached. No full external page fetch introduced.

### Token and payload cap rationale — candidate, not sufficient proof

- **Planner 4,096/1,024:** small topic/brief plus three axes and bounded six-query JSON; output 1,024 reuses S4-R's illustrative cap. Prepared local envelope is 880 bytes. Input 4,096 supplies generous candidate room for instructions/schema, not a chars-to-tokens proof. Complete request byte envelope <=8,192.
- **Synthesis 16,384/4,096:** reuses S4-R's narrower-input illustrative scale and synthesis output cap. Up to 18 bounded snippets and <=32KiB aggregate evidence, with explicit limitations/private provenance. Complete serialized request <=49,152 bytes. The 4,305-byte prepared placeholder is **not typical evidence usage**; full evidence and actual tokenizer fit must be validated.
- **Script 12,288/8,192:** research summary plus topic/duration/language and instructions. Historical example's 762 words/4,376 bytes establishes representative narrative size only. Output 8,192 leaves candidate room for narration plus billable thoughts; no assumed tiny budget or extra humanization. Script-result envelope <=12,000 bytes; it is a disposable rejection boundary, not a production duration/word policy. Complete request <=49,152 bytes. Prepared placeholder is 1,023 bytes; no real research summary/output-token usage exists.
- **Planning 16,384/16,384:** existing script plus exact sentence IDs/spans, preset and instructions; fixture envelope 8,238 bytes for 59 memberships. Output needs descriptions **and** prompts for all admitted scenes plus thinking. Historical 49 visual descriptions average ~104 bytes, max 144; actual image-prompt and reasoning sizes are not measured. Per-description <=1,024 bytes, per-prompt <=2,048 bytes are safety rejection limits, **not a promise every maximum-length field can fit the shared token cap**. Complete request <=49,152 bytes. Complete structured output/fidelity/quality within the shared output limit is unproven.

All candidate input/output caps are substantially below the evidenced model serving windows; none uses the million-token context as application authority. The local byte envelopes, hypothetical words/4 estimates and successful old TTS token counts do **not** certify text input-token limits.

### Exact remaining input-bound blocker

[Environment/source inspection](environment-v7.json): default Python lacks text tokenizer packages; the installed S4 SDK's `_local_tokenizer_loader.py` maps legacy 2.x / 3 Pro Preview IDs, **not `gemini-3.5-flash-lite`**. Its local model cache is absent, and invoking its loader can download assets. We only AST/read-inspected the source: no SDK client/tokenizer construction, install, model download or token API call.

A validated local tokenizer or independently justified conservative upper-bound mechanism covering the **selected model and full prepared request** is not established. Provider endpoint support and total-output/thinking enforcement for the selected wire configuration also remain conditional S4 evidence, not newly certified by this witness. Therefore every text operation records `usable_authorized_max_USD = null`. Missing proof blocks admission; no enormous serving-cap substitution or prompt-byte guess silently certifies a narrow bound. The **$0.410964 figure is conditional arithmetic**, not live finite liability established at these application caps. Search-only request-count envelope is $0.144 under the pinned S4 Basic price contract, before fees/account activation conditions.

## Cost arithmetic and retries

`candidate attempt USD = ceil_microUSD((0.30*I + 2.50*O_total)/1,000,000)`.

Round **up per attempt** before summing. One-attempt-each candidate maximum, with all six searches, is **$0.136988**. At all three admitted attempts, text alone is **$0.266964**, search **$0.144000**, total **$0.410964**. Unrounded arithmetic would be $0.4109568; it is not the integer-microUSD reservation total.

**Expected text/search subtotal = UNKNOWN**, not $0.136988 and not three times an invented average. No expected query count, output/thinking distribution, charged-failure probability or real text receipts were found. Successful first-attempt quantity may be below the caps. An unknown possibly successful submission keeps monetary/quota holds and blocks duplicate/unsafe overlapping work until supported reconciliation or separately authorized duplicate-risk handling. Safe retries keep the same operation identity/counters across restarts; never reset a plan to gain three more calls. Known charged failures still count financial exposure; unusable output is not free. No extra retry reserve is added to the three-attempt maximum.

## V6 + V7 five-minute economics

| Expected-cost component | USD | Evidence status |
|---|---:|---|
| Text/research/search | UNKNOWN | Required quantities unmeasured |
| ~60 image outputs | $2.016000 | Owner-fixed output tariff × preliminary heuristic |
| Initial B narration | ~$0.058188 | V6 duration proxy from Call 4 |
| Other new known variable provider charges | None identified | Not a zero-cost claim for unknown components |
| **Preserved image-output + TTS partial proxy** | **~$2.074188** | Unchanged; excludes image overhead/failures/resources/fees |
| **Complete expected variable cost** | **UNKNOWN** | Missing components not zero-filled |

| Maximum-exposure component | USD / status |
|---|---|
| Text/search candidate three-attempt envelope | $0.410964, conditional input/cap proof |
| Text/search usable authorized maximum | UNKNOWN |
| 60-image full-cap three-attempt envelope | $25.067520, historical conditional S4 bound |
| B narration per segment, up to three attempts | $0.307200, conditional S4 serving-cap bound |
| Number/scope of B narration segments | UNKNOWN; S5 intentionally did not freeze grouping |
| Image count after generated script | UNKNOWN; replace 60 heuristic with reviewed sentence scope and re-admit |
| Other fees/resources/unresolved liabilities | UNKNOWN |
| **Complete whole-project usable maximum** | **UNKNOWN** |

Sensitivity only: if 60 images and **one** B source segment were independently admitted at those caps, provider components sum **$25.785684** before fees/resources. This does not establish a whole-project bound or $30 affordability. One segment is not a selected production constant; actual script scope, input enforcement, fees and remaining obligations are unresolved. No credits/USD conversion follows from these numbers.

## Pasted-script and unentitled-topic differences

Pasted script: **no script-generation operation**, no humanization; replace topic Research planner/synthesis with claim/check planner and tool-free factual warnings/source synthesis, retaining applicable bounded Basic retrieval. Preserve exact pasted words and original version; proposed corrections require existing creator approval. Planning starts only over reviewed, admitted sentence memberships. For this same narrow fixture, if checking shares the candidate token/query envelopes, candidate maximum is **$0.338463** (saving only writing's $0.072501 maximum). This is **not** proof typical checking is cheaper or complete; expected usage and usable maximum remain UNKNOWN. Unrelated long pasted scripts need their own bounded plan, not this manifest by inheritance. If the historical 59-count segmentation is eventually accepted, image output arithmetic would be $1.9824; no images generated and no scene allowance silently granted here.

Unentitled topic: remove Research planner, Basic searches and Research synthesis entirely, leaving bounded script and visual/prompt work. Same-cap candidate maximum is **$0.210129**; expected and usable totals still UNKNOWN. Never falsely claim research or weaken factual quality. Pasted checking does not disappear by inferring a new entitlement decision. Optional Topic/Custom/Expert Suggestions do not enter either per-video manifest.

## Local witness and reproducibility

Run `python3 spikes/operating-economics/text_manifest_v7.py` from repo root. Stdlib only; no provider/app imports. Imports the unchanged v5 sentence counter without running its writer. Socket/DNS access is explicitly denied. The script writes only new v7 evidence/fixtures.

**48 checks PASS**; [results](witness-v7.json). Covers finite candidate bounds with explicit unknown live proof, exact operation inventory, query expansion/duplicate/size/authority rejection, narration/scene scope preservation, narrow caps and byte envelopes, absent/stale/excess token proof, output/tool expansion, attempts across restarts, unknown holds/blocked duplicate and other work, successful replay rejection, charged failures, tariff/rounding/sums, expected-vs-maximum distinction, UNKNOWN propagation, pasted and no-Research differences, unchanged V6 components and incomplete combined maximum. Token-proof fixtures are **synthetic trusted-oracle test data**, not a real tokenizer or a secure production proof-verification implementation. Semantic factual quality and real provider enforcement are not certified.

[Fixtures](fixtures-v7/fixture.json), exact locally prepared request envelopes, query example and deterministic sentence mappings are retained. Evidence slots use `example.invalid` and explicitly say synthetic, never pretend to be researched facts. Source/prepared hashes, dependency inspection and [preservation manifest](revision-v7-manifest.json) make history reviewable. Previous S9 non-index files and scripts remain unchanged; pre-v7 live index archived exactly.

## Verdict, unknowns and smallest next step

**S9: NOT_YET_PASS.** Closed the concrete operation-inventory/candidate-scope modeling gap; **did not close enforceable narrow input-token authority or measured expected text costs**. Remaining exact blockers include compatible complete-request token validation and selected wire output/one-send cap assurance, candidate scope quality/sizing, real text/search usage, generated scene scope, final B segment count, image endpoint/failure/retry/size evidence, whole-project exposure, credit policy, hosting/target-host compute, storage/backups/purge/egress/taxes/fees/FX and cost-grounded Alpha capacity. The image Free tier still has zero capacity; no upgrade or paid pilot requested.

**Single smallest useful next step:** establish a validated, model-specific **complete-request input-token preflight** for the candidate text model, starting with these retained request envelopes. An existing compatible local tokenizer or documented upper-bound method is preferred; absent one, any download or provider token-counting request needs separately defined/authorized scope. Do not treat one successful count as proof of all future requests. Until then, the manifest's narrow live text bound remains UNKNOWN and admission is blocked. This task performs no further phase or provider call.
