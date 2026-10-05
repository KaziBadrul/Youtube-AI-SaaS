# Project, artifact and dependency model

Current S5 decision, 2026-10-05: **PASS at the owner-defined existing B + B mapping scope**; see [final evidence](architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/README.md). Coherent initial sources and whole affected-segment replacements retain immutable source/text/mapping provenance. Scene mappings govern visual/caption timing without cutting continuous narration. This supersedes older S5 pending notes, not accepted restoration safeguards or unexecuted extraction/broader-protocol evidence.

Status: accepted authoritative Private Alpha architecture model, confirmed on 2026-10-03 with [ARCHITECTURE.md](ARCHITECTURE.md), subject to its evidence gates. Design acceptance does not authorize implementation or establish feasibility. This is the authoritative location for entity relationships, version compatibility and invalidation rules. No schema or application code is being created.

Narration amendment: **accepted by the user**, 2026-10-03. Other accepted policies remain in force. The narration sections replace the prior scene-local leading-contract recommendation. The owner's latest S5 decision selects B for initial generation and whole affected-segment correction, superseding B + C1 because of disliked stitching. Surgical correction is not the selected policy. S5 remains NOT_YET_PASS pending validated scene/audio mapping; segment sizing remains conditional. Existing scene-only restoration semantics remain in force and require validated ranges/joins; B correction does not waive them.

User clarification: creator review or display of estimated cost and maximum spend is optional, not a prerequisite for paid authorization. Create Video itself authorizes bounded production and starts generation directly, with no intervening estimate, confirmation or review screen. Financial details may remain in optional Details. Server-side cost bounds, allowance/budget reservations, retry limits and reconciliation remain mandatory. Required script-preservation/translation/adaptation approvals and material scope changes remain distinct from routine cost review.

## Domain relationships

| Concept | Meaning, ownership and relationships |
| --- | --- |
| User | Private identity. Owns projects and an Alpha allowance; an owner/operator role additionally controls shared budget and reconciliation. No team membership model is required. |
| Project | One user's editable production. Holds stable identity, ordered active scene IDs, selected settings, lifecycle state and current render-lock reference. |
| Original Input | Immutable submitted topic or pasted-script snapshot and its input mode/language context. Approval/adaptation does not overwrite the original. |
| Script | Approved production words. Before scene planning this is a project-scoped version; after scenes exist, current script is an ordered projection of current scene narration. Do not independently edit two conflicting sources of truth. |
| Scene | Stable project-owned identity independent of order, filenames and generated versions. Holds selected narration/visual inputs, asset selections, presentation settings and review flags. Deletion removes it from active order; provenance remains available to old renders/history. No Alpha scene-add/duplicate workflow is introduced. |
| Artifact | A stable typed content/asset role scoped to a project, scene or narration-generation segment. Examples: narration text, image prompt, narration audio, alignment, captions and image. It is not interchangeable with a Scene or Job. |
| Artifact Version | Immutable successful content/result plus exact source references, configuration and provenance. Selection chooses a version without deleting previous versions. Typed validation and compatibility determine whether it can be used. |
| Scene Narration Text | Immutable approved words for one stable scene, independently editable. A scene does not imply a TTS request. |
| Narration Generation Segment | Project-owned, versioned provider-facing request scope: ordered contiguous scene narration versions plus effective voice/language/delivery and segmentation policy. One scene may form a segment, but multiple scenes can share one. |
| Source Narration Audio | Immutable validated provider output for one exact segment version/attempt; retained independently of local assembly. |
| Alignment / Scene Audio Mapping | Versioned validated mapping from approved scene text to word/range offsets in a specific source audio version; includes method/configuration, confidence/validity and boundary metadata. |
| Derived Project Narration | Locally assembled ordered source ranges with an immutable assembly manifest and derived project offsets. No new paid TTS operation is implied. |
| Research Result | Project-scoped versioned summary/source collection tied to topic/request inputs, plus complete/partial/unavailable outcome. Sources are evidence, not automatic factual approval. |
| Factual Warning | Private claim concern tied to the checked pasted-script version and supporting sources. Corrections are proposals requiring consent; warnings never grant spending or modify words. |
| Generation Job | An authorized execution request over specified project scope. Contains operations, not the project itself. See [job model](JOB_EXECUTION_MODEL.md). |
| Operation / Attempt | Scoped work and its concrete executions. Failures/unknown outcomes live here, so a failed regeneration does not destroy a valid asset. |
| Render | Local execution over an immutable input manifest, linked to its job/attempt and recoverable project lock. |
| Final Export | A validated immutable MP4/media registration from a render manifest. Old successful exports remain downloadable. Export currentness and technical success are different properties. |
| Allowance / Authorization / Reservation | Identity usage allocation, explicit action authority, and held financial exposure. None is an artifact. See [cost model](COST_MODEL.md). |

Every record's project scope is explicit and verifiable. Global licensed music/curated style/font/voice configuration is separate from private project assets; project selections reference a pinned definition/configuration rather than mutable defaults silently changing old output.

## Typed content with a shared version envelope

**Decision:** Use typed project/scene records and typed artifact payloads, sharing only common version/provenance/selection metadata. Do not make all domain entities arbitrary JSON artifacts. Small structured payloads can use validated, schema-versioned database content; binary media use immutable file registrations.

**Requirements:** Inspectable/editable outputs, individual versions/restoration, sources/model/config/cost tracking, stable scene identities and explicit domain semantics.

**Alternatives:** Separate unrelated version implementations for every media type; one universal artifact table containing arbitrary documents/workflows/users/money.

**Tradeoffs:** Shared invariants avoid duplicated version logic while typed contracts preserve meaningful validation. Adding a new artifact kind requires deliberate schema/domain rules; it is not a user-configurable graph engine. Financial and authorization records stay relational and distinct.

**Reversibility:** Moderate data migration cost. Stable IDs, schema versions and typed payloads reduce later ambiguity.

**Evidence needed:** Fixtures for edits/restores, asset registration crash windows, scene deletion/order and provider-output validation. Detailed physical table layout is an implementation concern after architecture confirmation.

A common version envelope records artifact/project identity and scene/segment scope where applicable, kind and schema version, immutable content or blob key, byte hash/type/size where relevant, created time, source type (generated/edited/uploaded/restored selection), operation/attempt identity, pinned source versions, effective configuration signature, provider/model/configuration and validation metadata. Link to cost events rather than copying mutable accounting totals into every artifact. Unknown/reconciled costs remain inspectable through the attempt ledger.

Generation failures do not create selectable valid versions. A diagnostic response can remain in private attempt staging. Each artifact slot has a selected version or none; failed last attempt is displayed separately. Thus a failed image retry can leave an earlier compatible image selected, while a missing image with failed attempts remains incomplete.

## Provenance, compatibility and staleness

**Decision:** Persist exact direct source-version references for provenance and use explicit deterministic domain rules to calculate required compatibility/invalidation. The resulting dependencies form a DAG, but do not build a generic graph execution service. Persist current selections/review state; derive compatibility from recorded signatures and relevant current inputs, with invalidation updates applied in the same transaction as edits.

**Requirements:** Selective regeneration, safe restore, stale asynchronous results, no unnecessary invalidation, no AI authority over dependencies.

**Alternatives:** Persist a fully configurable graph and run it generically; hardcode only dirty booleans with no provenance; let AI infer dependency effects; compare one whole-project revision for every operation.

**Tradeoffs:** Exact references explain origin; effective input signatures allow restoration/reuse when content/configuration is compatible even if unrelated project settings changed. Domain rules avoid accidental regeneration of every scene. A changed global project revision alone is insufficient reason to discard an unrelated scene result.

**Reversibility:** Moderate rule/data migration. Version the compatibility rules/contract when their meaning changes; do not silently reinterpret prior provenance.

**Evidence needed:** Invalidation/restoration matrix, concurrent-edit compare-and-select and disabled-feature fixtures.

Separate dimensions:

- **Available/valid:** bytes/content passed this type's technical checks and persist.
- **Selected:** creator/application currently chooses this version.
- **Compatible/outdated:** required inputs still match, or do not match.
- **Review needed:** a semantic/override concern needs creator action; this is distinct from a failed provider attempt.
- **Last generation outcome:** complete, failed, canceled or uncertain attempt history; not a replacement for asset compatibility.

Currentness is not an immutable property of a version. Provenance never changes when a creator selects/restores an old version. Keep exact historical sources and separately record explicit selections/approved overrides. Do not pair audio with materially different approved words through an override. The owner-accepted 2026-10-05 fidelity amendment permits explicit acceptance of a meaning-preserving minor spoken variation as a separate record pinning source audio/version, approved text/version, actual difference, reviewer/approval and evidence. It does not rewrite script/request provenance; changed text or different audio requires fresh review. Material differences retain compound restoration requirements.

## Invalidation matrix

| Change | Required effect | Preserve |
| --- | --- | --- |
| Scene narration text | Affected selected generation segment becomes outdated for the current plan; source audio compatibility and mappings/timing/captions relying on that changed segment branch become outdated. Derived project narration/global offsets and render outdated. Flag edited scene visual review; follow-up highlights affected by text/range changes need review. | Images, all prior sources/mappings/manual versions, and compatible segments unrelated to the edit. Unchanged ranges within the old segment are recoverable only through validated explicit reuse, not assumed current. |
| Voice/language/delivery configuration used by narration | Affected segment plan/audio compatibility and dependents outdated; replan boundaries if configuration cannot be expressed within a shared request; render outdated | Unrelated visuals/segments and previous versions; never silently change sibling scene settings |
| Visual description/image prompt used for generation | Generated-image compatibility/review changes; render cannot silently claim new visual instructions are fulfilled by an old generated image | Narration and timing; prior images; explicit user replacement provenance |
| Image regeneration/replacement/explicit restoration | Selected image changes; render outdated | Narration, timing and captions |
| Caption text edit | New caption version; render outdated; narration unchanged | Audio and underlying timing when compatible |
| Caption style/font/position or toggle | Render effective configuration changes | Images, narration and source caption text |
| Motion settings | Render outdated | Provider assets and narration/timing |
| Music choice/volume | Render outdated | Narration/images/timing |
| Manual scene timing | Render and timeline-dependent caption placement updated/outdated as required; flag speech cut-off conflicts | Provider assets; prior automatic/manual timings |
| Scene reorder/delete | Current-script projection, local assembly/order/global offsets and render change; revalidate audio joins and mapped speech coverage | Existing source audio and valid surviving scene ranges/images/local captions; no automatic paid resegmentation. Unsupported joins block with an explicit correction plan. |
| Research/checking completion or failure | Update private provenance/warnings; does not silently rewrite narration or invalidate images | Approved script and assets unless creator accepts a text change |
| Accept factual correction/translation/adaptation | Version approved words, then apply ordinary narration/script dependency rules | Original input and prior versions; no paid regeneration without authority |
| Emphasis font/animation/selection/layout edits (follow-up) | Render outdated; selection/timing compatibility checked where relevant | Images/narration; prior highlights |

Only enabled branches are required in a render manifest. Disabled captions or Emphasis Text can retain outdated content without blocking export; disabling them never bypasses required audio/scene-timing validity. Settings irrelevant to an operation do not invalidate it. Deterministic rules decide staleness; AI may suggest content or flag quality, but not mutate dependency/authority rules.

Image selection/review must respect accepted “keep or replace” behavior. An explicitly retained/restored/uploaded image is a creator choice with provenance, not proof it was generated from the current prompt. Record the current review/selection context; do not rewrite its historical prompt or automatically pay for replacement. Different narration words remain a hard audio-compatibility violation regardless of visual overrides.

## Narration generation granularity — accepted amendment

**Decision:** Separate scene-level approved narration from provider request granularity. Use coherent contiguous multi-scene segments as the leading **conditional candidate**, informed by legacy approximately 500-word batching; do not fix 500 words as a domain invariant. Keep per-scene generation as an S5 comparator and surgical correction as an optional evidence-gated strategy, not an Alpha promise.

**Requirements:** Scene editing, transparent actual regeneration scope, continuity/word fidelity, bounded spending, rate-limit efficiency, selective correction, exact provenance and preservation of unaffected compatible work.

**Alternatives:**

| Strategy | Requests / continuity | Correction / constraints | Cost, accounting and failure surface |
| --- | --- | --- | --- |
| A — per scene | Nominally one initial submission per scene; many joins and potentially inconsistent delivery. Short scope can fit request bounds. | Direct scene-only regeneration; best granularity if joins/voice are publishable. Many scenes pressure request quotas; short calls do not inherently improve alignment. | More attempts/reservations/timeout opportunities; small failure/correction blast radius. Actual cost depends on usage/minimums, not request count alone. |
| B — coherent segments | Nominally one submission per segment; fewer cross-request joins, with larger-context continuity a hypothesis to validate. | Edit requires regeneration of the affected segment, potentially several unchanged sibling scenes; other segments stay reusable. Must fit verified input/output/duration limits and stable configuration boundaries. | Fewer initial attempt records, but larger failed/ambiguous liability and correction cost. Alignment must reliably split/map returned audio. |
| C — segmented initial + surgical correction | Initial requests as B, then one scene or small context-window correction where plausible. | Preserve old unaffected ranges only if voice, prosody, pacing, transitions and exact-word alignment pass. Extra context words must be mapped and excluded from the delivered range without omission/repetition. | May reduce correction cost/blast radius; adds range/assembly compatibility complexity and can require fallback to segment regeneration. Crossfading alone does not solve semantic/prosodic mismatch. |

**Tradeoffs:** B better addresses request pressure without sacrificing creator scene editing, but it cannot promise scene-only paid regeneration. The existing implementation proves the batching mechanism exists, not that its quality, safety or chosen size is optimal. S5 must select the viable policy; fewer requests are not sufficient to pass. If no candidate preserves the accepted quality/correction contract, surface the failed gate rather than weaken it.

**Reversibility:** Moderate version/mapping contract migration; no implemented data exists here. Immutable source audio, explicit segment memberships and assembly range references allow switching policies without rewriting historical provenance. New policy versions affect newly planned requests, not retrospective membership changes.

**Evidence needed:** S4 request/cost/capability bounds and S5's A/B/C comparison, including correction, restored single-scene ranges and reorder/delete joins. No policy, size or surgical feature is proven or executable yet.

### Segment, mapping and assembly contracts

A segment version pins ordered stable scene IDs and exact narration version IDs, approved text spans, effective per-scene voice/language/delivery, request metadata, policy/version and all contextual inputs that actually influence generation. Its provider submission has an explicit operation/attempt; a multipart style request is not several paid requests. Conversely, multiple submissions must never be hidden inside one segment operation. Begin with whole contiguous scenes and natural sentence boundaries; oversized scenes or configuration conflicts require an explicit bounded subsegment/multi-range plan, not a truncated request or silently changed settings. The legacy sentence batching lacks these scene contracts.

Persist membership instead of re-batching the entire project after every edit. Plan a replacement for affected segments only. A changed size policy, model limit or voice override may require bounded local repartitioning; show exact changed membership/request/cost scope and reauthorize before paid work. Do not cascade segmentation drift into otherwise compatible segments.

Alignment processing may be probabilistic; dependency and selection rules are deterministic. A mapping pins source audio hash/version, segment membership/text versions, spoken-word correspondence, ordered finite sample/time ranges, boundary pauses, format/sample metadata and the alignment method/configuration version. Account for all approved narration and explicitly accepted minor spoken variations without missing/repeated passages, overlapping contradictory speech or unassigned speech. Mappings/captions link accepted variation records and actual spoken-token correspondence. Variation acceptance alone establishes no timestamp or boundary. Persist failed/uncertain mappings as non-exportable outcomes rather than guessing boundaries. One scene may reference several validated source ranges when an explicitly supported subsegment/correction policy requires it.

Derived project narration pins the selected ranges in scene order, local transforms and join/pause policy, source hashes and mapping versions. Compute project offsets locally; duration changes can move all later project offsets/caption positions without invalidating their source audio or scene-local mappings. Preserve source audio, mappings and prior assemblies as versions; scratch cuts can be rebuilt. Reorder/delete must reuse surviving approved ranges without paid generation when validated joins permit it. If range extraction/joins fail quality, report the failure and propose an authorized fix; do not silently regenerate narration, cut speech or waive the product's preservation requirement.

Visual timing clarification accepted 2026-10-05: image i remains visible until the mapped narration start of scene i+1, including intervening pauses. Maintain speech start/end, visual interval and any extraction range as separate values. Do not infer a visual transition from the preceding spoken end or a pause midpoint; do not cut coherent source audio for ordinary image changes. Caption timings follow actual words independently. First/last visuals cover leading/trailing narration duration.

### Deterministic invalidation example

If Scenes 13–21 share segment G and Scene 17's approved words change, G's selected generation branch becomes outdated. Its historical audio is still valid for its historical inputs, but not a current complete source for G. Mappings/captions dependent on the replaced branch require validation/refresh; unrelated segment H's source and local mappings stay compatible. The project assembly/render become outdated, and later global offsets need local recomputation. Images stay preserved with Scene 17 visual review. A proven surgical policy may explicitly retain compatible old ranges for other scenes within G; baseline B does not assume it can splice them safely.

The correction plan must state, for example, “Regenerate narration for Scenes 13–21 because they share a generated segment,” with request count, voice/configuration, preserved scope and affected manual work before authorization; estimated/max cost is available optionally. A Scene does not automatically cause one paid TTS request.

## Selection, restoration and concurrent edits

Capture exact relevant inputs when an operation starts. On completion, persist a valid result and cost once. Select it only if the current inputs/selection intent still match and worker ownership is valid. After a relevant edit, retain it as history and show allowance usage; never overwrite newer work. Edits outside all pinned segment/context inputs do not veto a compatible result. An edit to one member makes the arriving complete segment response history-only; do not auto-select sibling ranges from that stale response. Explicit compatible-range reuse needs validated mappings and selection intent.

Queued relevant input changes invalidate that authorization's plan and require refresh before paid execution. Running edited operations may finish into history, but do not continue downstream from an outdated branch as if it were current.

Restore existing valid versions without generation allowance. If restored audio has different words, show the associated text and require compound text/audio approval; update current script and select compatible timings/captions. Preserve incompatible manual versions for review. If audio words match but recorded voice/delivery differs, show those settings in restoration confirmation. Approval adopts the recorded voice/delivery for the restored scene only, preserving other scenes and project defaults. This explicit scoped selection satisfies voice/delivery compatibility without rewriting generation provenance. Subsequent regeneration displays the effective voice/configuration before authorization. Timing/caption compatibility still requires validation, and restoration cannot bypass required-content checks.

### Segment restoration and A15

A historical segment restore shows its full affected scene/text/configuration scope and requires approval for every changed approved text selection. It cannot silently restore sibling words. A single-scene restore selects only that scene’s validated historical source range(s), with compound text/audio approval where needed; it does not select the full segment for other scenes. Approval adopts recorded voice/delivery for that scene only under A15, leaving other selections and project defaults unchanged. Keep source provenance immutable, validate new joins/assembly and restore compatible local timing/captions or preserve manual versions for review. If a single-scene range cannot be extracted and joined safely, block that restore and disclose the affected scope; do not substitute a silent multi-scene restore. Subsequent paid generation shows the effective scene configuration and actual segment scope; a scene-only override may require a configuration boundary/replan, never silently changing sibling voices. S5/S7 must test these cases.

## Render manifest

A manifest pins active scene order, selected compatible text/image/source-audio/range-mapping/timing/caption versions and derived narration assembly, effective render settings, music/font references where used, resolved file hashes and the render-contract version. Required missing/outdated components reject final rendering; previous exports remain history. Validate while holding the transaction that checks project eligibility and acquires the render lock. Never resolve mutable filenames halfway through FFmpeg.

The manifest is also export provenance and recovery input. A new valid export becomes the selected export transactionally after validation; earlier exports remain. A later relevant edit marks its relationship to current project content outdated without altering the file or preventing download as a clearly identified historical export.
