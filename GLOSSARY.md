# AI Video Production

Product language for an AI video production system serving solo creators.

## Language

**Primary creator**:
A solo faceless educational YouTube creator producing narrated, image-based explainers of approximately 3–10 minutes.

**Publishable video**:
A video the creator judges ready to publish after checking its content and presentation. Successful MP4 export alone does not establish publishability.
_Avoid_: Render success as a synonym for publishability

**Correction effort**:
The creator's active time spent correcting a generated video before it becomes publishable.

**Simple Mode**:
The production experience in which the creator supplies an idea or script and authorizes the AI to produce a complete video within an internally enforced authorized spending ceiling, with cost review available optionally.

**Advanced Mode**:
The experience for inspecting and controlling creative decisions within the same project used by Simple Mode.

**Spending ceiling**:
The maximum spending a creator authorizes for a generation request. Further spending requires additional approval.
_Avoid_: Estimated cost as a synonym for spending ceiling

**Private alpha**:
A limited creator-testing release used to validate production quality, correction effort, and actual generation costs before committing to public-launch scope and pricing.

**Factual warning**:
A creator-visible indication that a claim may be inaccurate, disputed, or unsupported. It is absent from the exported video and does not require review before generation continues.

**Alpha allowance**:
A capped amount of free generation usage allocated to an alpha tester.

**Vertical video**:
A standalone video in a portrait aspect ratio intended for short-form viewing. It is distinct from a platform variant derived from an existing video.

**Factual check**:
An assessment of claims in a pasted script that can produce private factual warnings. It is distinct from research used to prepare a new script.

**Chargeable asset**:
A technically valid generated asset delivered to the creator and counted against their allowance. Creator dissatisfaction alone does not make the asset a failed operation.

**Outdated artifact**:
A project output that no longer reflects the current content or settings it depends on.
_Avoid_: Failed asset as a synonym for outdated artifact

**Research**:
Source gathering used to inform the writing of a script from a factual topic. It is distinct from assessing claims in a pasted script.

**Actual operating spend**:
The owner's incurred costs for generation, research, hosting, storage and tester usage, including paid failed attempts. It is distinct from the successful-asset usage counted against a tester's allowance.

**Final export**:
A rendered MP4 representing a particular project version. Technical completion does not by itself establish publishability.

**Emphasis Text**:
Editable animated word or short-phrase overlays that highlight important or appealing parts of spoken narration over scene visuals. It is independent of captions.
_Avoid_: Captions or image-embedded text as synonyms

**Caption**:
Text presenting the spoken narration for reading alongside the video. It is distinct from selective Emphasis Text highlights.

**Project**:
A creator-owned editable video production containing original input, scenes, assets, settings and output history.

**Original Input**:
The preserved topic or script initially submitted for a project. It is distinct from the current production script.

**Script**:
The approved narration words for a project, following the current scene order once scenes exist.

**Scene**:
An identifiable unit of video production pairing narration with visual and presentation choices. Its identity is distinct from its position in the video.

**Artifact**:
An identifiable typed input or output within a project's production, such as narration text, an image, audio, timing or captions.

**Artifact Version**:
A preserved revision or generated result of an artifact, with its origin and production context. Selection of a version does not erase prior versions.

**Job (Production Job / Generation Job)**:
An authorized request to generate, regenerate or render a defined project scope. It may contain several operations and pause without discarding completed work.
_Avoid_: Project as a synonym

**Operation (Generation Operation)**:
A scoped unit of production work with specified inputs and an expected result. It is distinct from an attempt to execute that work.

**Attempt (Provider Attempt / Local Attempt)**:
One recorded concrete execution or attempted provider submission for an Operation, with execution identity, validation outcome and possible spending liability. A local render attempt is also an Attempt; it is not a paid provider call.

**Spending Authorization**:
Explicit permission for specified production work within an approved maximum cost.

**Reservation**:
Held allowance or operating-budget capacity for authorized work or unresolved financial exposure. It is distinct from consumed usage or settled spending.

**Render**:
The assembly of selected project content and presentation into a video. It is distinct from the resulting final export.


**Entitlement**: Persisted server-side eligibility to use a feature; separate from financial permission or UI visibility.

**Allowance**: Identity-assigned successful-output usage limit. Alpha allowance amounts remain owner-configured; creator credits never override shared USD authority.

**Liability**: Unresolved maximum possible external charge retained until evidence-backed reconciliation. It survives cancellation, restart and period changes; do not double-count it as both a live hold and settled spend.

**Selected**: Currently chosen version, separate from validation and compatibility.

**Valid**: Content/media passes its typed technical checks; does not mean selected, current, compatible or publishable.

**Compatible / Outdated**: Relevant source versions/effective inputs do or do not match the current required contract. Historical provenance stays immutable.

**Review Needed**: Explicit unresolved semantic/acoustic decision, distinct from invalid bytes or a failed attempt.

**Narration Generation Segment**: Versioned contiguous approved scene/configuration membership submitted as coherent B narration; not one scene per TTS request.

**Source Narration Audio**: Immutable validated audio from a concrete narration attempt.

**Scene Audio Mapping**: Source-bound text/scene/audio-range correspondence, with alignment version, confidence and validation/review provenance. Visual transitions and speech/extraction endpoints are distinct.

**Derived Project Narration**: Validated current ordered composition referencing immutable source audio and mappings. Ordinary scene transitions do not cut continuous B audio.

**Accepted Spoken Variation**: Version-bound creator acceptance of a minor meaning-preserving audio difference, separate from approved Script and recognized ASR text. It does not waive material errors or mapping validation.
