# Alpha visual and interaction design

## Topic discovery extension — owner decision, 2026-10-05

Follow the [canonical entitlement matrix](ALPHA_PRODUCT_SPEC.md#owner-decision--research-entitlement-and-topic-discovery-2026-10-05).
This extends the Warm Creator / Direction C Refined concept for future discovery
surfaces; it does not schedule suggestion features for the first Private Alpha
or authorize prototype/production changes.

Keep the New Video composer dominant. A quiet **Need an idea?** area adjacent to
the composer can offer distinctly labeled Topic Suggestions, Custom Topic
Suggestions and Expert Topic Suggestions. Keep discovery optional and contextual,
without a new dashboard/sidebar, full-screen redesign or required setup step.
Reveal category selection or channel/niche input only for the selected feature.
Stored-topic discovery uses **Surprise me** and allows another suggestion or
use of the topic. Custom discovery supports multiple selected interests;
Expert discovery supports channel/name/link or niche context. Preserve typed
composer content; an explicit use action installs the chosen topic rather than
silently overwriting a script or starting production.

For unavailable features, show a clear readable plan requirement: Research,
Topic Suggestions and Custom Topic Suggestions require 3 videos/week or
1 video/day; Expert Topic Suggestions requires 1 video/day. Avoid deceptive
inert buttons, repeated upgrade banners, popups, AI sparkles and analytics-card
layouts. Exact paywall/upgrade interaction is unresolved until plans/prices are
defined. Accessible labels, focus, busy/failure states and restrained existing
typography/surfaces apply. Research absence must not look like successful research.

Status: Direction C Refined visual and motion exploration accepted by the user; Alpha Design Discovery and visual exploration are closed. This document reconciles that evidence into the accepted design baseline. The user reconfirmed one-tap creation with optional cost review during reconciliation. Application implementation, architecture spikes, paid provider calls, deployment purchases and implementation task graphs remain unauthorized.

This is the accepted visual and interaction design source of truth. [Alpha product specification](ALPHA_PRODUCT_SPEC.md) controls scope and product semantics; accepted ADRs and [artifact](ARTIFACT_MODEL.md), [job](JOB_EXECUTION_MODEL.md) and [cost](COST_MODEL.md) models control their respective contracts. [UX flows](UX_FLOWS.md) describes behavior. Design does not establish technical feasibility.

## Spending authorization

Owner S9 v5 display amendment: the existing compact estimate/optional Details
pattern shows both credit estimates and approximate USD cost during Private
Alpha. After work executes, distinguish consumed recorded usage, remaining
estimate and projected total; expose unknown/pending portions honestly. This
supersedes credits-only presentation without a new layout, final UI copy or
mandatory review screen. Scope admission remains separate deterministic policy.

The user explicitly resolved the reconciliation request's financial-review conflict in favor of the final accepted one-tap prototype: cost review stays optional. Create Video authorizes bounded production directly and moves in place to queued/running progress, with no mandatory estimate screen, confirmation modal or post-click interpretation step. See more and optional Details expose estimated usage and maximum authorized spend without making the initial surface a financial form.

Visual simplicity does not remove authority or enforcement. Internally bind the submitted input/settings, finite request ceiling and permitted scope; apply ownership, budget/allowance reservations, retry limits and reconciliation before paid submission. Exceeding existing authority, required translation/adaptation and changed approved scope still follow their explicit approval requirements. No provider call is authorized by accepting this documentation.

## Principles and agreed direction

The promise is: “I provide an idea or script, the system makes the video, and I can easily correct the parts I don't like.” Creation requires minimal input; the editor is a correction environment. Optional choices use progressive disclosure. No provider knowledge, prompt engineering or pipeline configuration is required.

The user selected subtle plum dark foundations, system-following light/dark themes, olive primary actions in both themes, a dedicated New Video page, a compact app header, a three-column desktop workspace, selected-scene preview, full mobile scene corrections and a guided public demo as the landing page's primary action. Simple production automatically renders; optional manual review stops before rendering. Neither path creates a separate editor or project type.

The accepted foundation is Direction C Refined: warm and approachable during discovery and creation; focused and professional during production and correction. The editor is deliberately denser and quieter than the landing and creation surfaces. The visual character is premium, calm, creative and approachable. Typography and actual project imagery carry identity; surfaces and controls stay restrained. Editing density is useful rather than sparse. State clarity earns trust more than decoration.

## Reference interpretation

All ten images in [design motivation](../design-motivation/README.md) were inspected. Screenshots demonstrate appearance, not implemented behavior. The annotated references retain their assigned roles. The accepted final [Direction C Refined exploration](../design-prototypes/direction-c/README.md) supplies visual and interaction evidence; its HTML/CSS/JavaScript is disposable, not a production foundation. Earlier competing directions are superseded, and no additional direction is needed.

| Reference and assigned role | Relevant principles | Adaptation and exclusions |
| --- | --- | --- |
| `products/dashboard.png` — dashboard structure | Creation surface above a thumbnail-led project collection; strong heading/action hierarchy; generous separation between creation and browsing. | Provide New Video above recent projects, then recognizable thumbnails, names and statuses. Compress the oversized greeting/empty space. Do not inherit its cyan search controls, dark colors, pills, dots or typography as system authority; no analytics tiles. |
| `products/details-button.png` — detail disclosure | Summary trigger, chevron, anchored expanded surface, grouped rows, separators and a compact theme selector. Comfortable control spacing; subtle border separates elevated dark surfaces. | Use contextual Details and account menus with explicit expanded state, keyboard support and dismiss behavior. Reduce exaggerated radii. Exclude Pro/billing, invented shortcuts and mandatory avatars. A static image does not establish animation behavior. |
| `products/video-editor.png` — workspace structure | Dominant visual preview, adjacent contextual tools, playback directly below, ordered media sequence; clear selected content. | Scene list left, preview center, correction panel right; a simple scene sequence may show order and durations. Exclude multi-track/keyframe editing, crop/transform handles, clip editing, neon outlines, glow, sparkles, floating promotional callouts and decorative cursors. Its cream/green coloring does not replace the palette references. |
| `products/landing-page-1.png` — entry composition | One bold message, supporting copy, one dominant CTA and rich video imagery. Strong contrast and controlled centered hero composition. | Concise outcome headline, Try the workflow, secondary Sign in, supplied demo imagery and a short correction explanation. Exclude fabricated social proof, service-agency copy, red pill styling, excessive image tilting, dark overlays that impair reading and an oversized empty hero. |
| `products/button.png` — button styling | Solid high-contrast fill, clear label, moderate rounding and a compact rectangular silhouette. | Olive primary and quiet secondary buttons, consistent proportions and visible interaction states. Do not copy rainbow edge/glow, unlimited-access language or pill-like exaggeration. |
| `products/audio-editor.png` — narration interaction | Readable editable narration, voice context, Settings/History separation, secondary controls apart from text, prominent generation action. Thin dividers and relatively dense useful content. | Narration text is primary in its correction view; audio playback and effective voice remain nearby; history opens contextually. Exclude model selectors, stability sliders, format controls, voice cloning, promotional panels, credits and provider-specific inline tags. Do not introduce unrestricted delivery-tag editing. |
| `typography/typography-1.png` — headings | Heavy clean sans-serif, tight but legible tracking, confident compact heading shape. | Scale appropriately for marketing and workspace headings; no giant type in routine editing. Exact font identity is unverified. |
| `typography/typography-2.png` — interface/body | Clear sans-serif, semibold subheading, regular supporting text, comfortable line spacing and obvious hierarchy. | Sentence-case labels, readable prose and compact interface text. Avoid inheriting low-contrast muted text without verification; no serif subheading copied from dashboard. |
| `colors/palette-light.png` — light color direction | Cream `#FEFAE0`, forest `#283618`, olive `#606C38`, warm sand `#DDA15E`, copper `#BC6C25`. | Cream canvas, forest text, olive actions, restrained warm supporting accents. Derive accessible surface/border/state shades; do not distribute all five colors equally or use sand as default body text. |
| `colors/palette-dark.png` — dark color direction | Deep tonal progression: `#11001C`, `#190028`, `#220135`, `#32004F`, `#3A015C`. | The final refinement neutralizes the dark canvas/panels; plum remains restrained in selected, hover and contextual elevation tones. Brighter shades are restrained selected/hover foundations, not glowing accents. Olive remains the shared action identity. Add readable warm light text; five dark swatches cannot supply all semantic roles. |

Resolve references through one typography, spacing, radius and control system. Use each only for its annotated role, not as a template or a competing product identity.

## Theme and semantic colors

Support Light, Dark and System from the beginning; first visit follows the system preference. An explicit choice persists and overrides system changes; System follows them. Provide labeled theme controls in the account/details menu, also accessible on the public entry surface. Theme changes preserve input, focus, selection and playback. Media and rendered video colors do not change with interface theme.

| Role | Light direction | Dark direction |
| --- | --- | --- |
| Canvas | Cream `#FEFAE0` | Near-black neutral foundation with subtle plum character |
| Elevated surface | Near-cream/light neutral derived from canvas | Quiet neutral-plum elevation |
| Secondary surface | Slightly darker cream | Restrained tonal separation from canvas |
| Primary text | Forest `#283618` | Warm off-white |
| Secondary / muted text | Derived dark olive/neutral shades with sufficient contrast | Derived warm gray, distinguishable from primary text |
| Border / divider | Quiet olive-neutral line | Subtle neutral-plum line |
| Accent / primary action | Olive `#606C38` with verified contrasting label | Accessible olive treatment with verified contrasting label |
| Hover | Small olive/cream tonal shift | Subtle plum or olive tonal shift according to control |
| Selected | Olive-tinted surface plus marker/label | Restrained plum/olive treatment plus marker/label |
| Success | Distinct green treatment with icon and text | Accessible green treatment with icon and text |
| Warning | Warm amber/copper family with readable foreground | Accessible warm warning treatment |
| Error | Distinct red family with readable foreground | Accessible red treatment |
| Disabled | Muted surface/text plus explanation when useful | Muted surface/text plus explanation when useful |

Light keeps warm cream, forest typography and olive actions. Dark keeps warm readable text and olive actions without making every surface equally purple. Reference hex values indicate origin, not immutable final tokens. These are semantic assignments, not a contrast-certified token set. Derive exact text, borders, hover, focus and status shades during separately authorized exploration, then verify contrast in both themes during implementation. Do not force palette swatches into roles they cannot readably serve. Copper may support imagery/secondary emphasis but must not ambiguously indicate a warning. No unrelated decorative accent palette.

## Typography, spacing and surfaces

Use a clean sans-serif with substantial bold headings, open counters and legible regular interface text. A practical candidate is a system sans-serif stack for Alpha; Inter is an optional candidate if licensing, availability and multilingual coverage are verified separately. No font dependency is selected or installed. Provide verified Bangla/Devanagari fallbacks before enabling corresponding experimental languages. Interface fonts and rendered-caption fonts have separate validation requirements.

Working scale for later exploration: body/interface around 16px; secondary metadata 13–14px; section headings 18–24px; page headings 28–36px; landing headline larger only where its content and viewport warrant it. Use regular body, medium labels and semibold/bold headings; avoid all-caps micro-labels. Body line-height around 1.5, headings around 1.1–1.25. Narration uses proportional text, readable line lengths and comfortable line spacing; time values can use tabular numerals. These are reversible starting ranges, not fixed acceptance pixel values.

Use a consistent small spacing unit (approximately 4px) with purposeful increments. Compact spacing groups related controls; larger gaps separate decisions. Wide desktop workspace uses available width; creation pages constrain reading/input width. Do not center routine workspace content.

Canvas and thin dividers do most grouping. Elevated surfaces are for menus, sheets, dialogs and contextual panels; cards are justified for project thumbnails or selectable visual assets. Moderate, consistent control rounding; slightly larger rounding for dialogs/media containers, never giant rounded sections. Shadows communicate elevation only and remain subtle. Avoid shadows on every section, thick outlines and nesting panels inside repeated cards.

## Controls and navigation

Primary buttons are solid olive with a clear verb: Create Video, Regenerate narration, Render video, Download MP4. Secondary buttons use quiet borders or surfaces. Destructive actions are labeled and distinct, separated from primary work. Icons supplement labels; icon-only controls need accessible names. Loading states retain the action's meaning and prevent duplicate submission without replacing the whole screen.

Inputs have accessible persistent labels, visible focus and adjacent help. The New Video composer accepts a short idea or long pasted text without permanent Topic/Script tabs. A quiet interpretation hint says the current input is being used as an idea; See more exposes an explicit approved-script choice. Switching interpretation preserves entered text. Paste opens options without classifying or rewriting text. Language defaults to English and is exposed within See more. Do not use placeholders as the only accessible label or add AI sparkles.

Compact header contains Projects, New Video and account/details access. No persistent global sidebar competes with scenes. Workspace header adds Back to Projects, editable project name, autosave state, production status and Render/Export access. Owner reconciliation and spending details are role-specific; testers see their allowance and relevant pending usage, not infrastructure administration. No teams, public sharing, subscription navigation or public signup is introduced.

## Core surfaces

### Landing and demo

Try the workflow is primary; Sign in is secondary for invited creators. Communicate idea/script → generated video → easy scene corrections through concise copy and actual example media. Avoid unverified quality, completion-time or customer-count claims. No public pricing or billing.

Three generated-video images are visible together in the landing carousel; the middle image is slightly larger than its neighbors. Preserve an editorial media composition, not a generic slideshow card. Motion and interaction are specified below. Typography and copy clearly separate words/punctuation and emphasize small input → generated production → easy corrections.

The demo is an account-free, isolated guided walkthrough using `demo-video-example/` in this repository: scripts, 49 images, narration WAV, scene JSON, timestamp data, captions and final MP4. Demonstration progress is explicitly labeled as prepared example progress, not live provider activity. Visitors inspect scenes and play the supplied result. Simulated edits/regeneration do not overwrite the supplied files, submit paid work or imply the MP4 reflects newly typed words. Unavailable prepared alternatives show an explanation rather than fabricated regenerated media. Reset is available. Demo download is not a required new capability; playback suffices.

Demo files are legacy evidence, not acceptance proof or product contracts. Existing recurring characters do not promise character consistency. Before public exposure, verify permission to publish the content and that media contains no private material; this documentation does not publish anything. Check scene/audio/caption correspondence before binding them in a demo; historical paths and raw/humanized/TTS scripts are not interchangeable authority.

### Dashboard and New Video

Dashboard uses a coherent, consistent thumbnail-led recent-project collection with comparable project prominence, rather than one oversized project and tiny remaining rows. New Video stays prominent. Each project shows name, meaningful status and recent modification/activity when useful. Active/queued production is visible without becoming an analytics dashboard. Failed, waiting and partially complete projects remain reopenable. Empty state provides one clear creation action. Deleted projects live in a recoverable Deleted projects view, outside the active collection.

New Video is composer-first. Its centered initial state has a concise creation heading, dominant input, quiet See more and an integrated Create Video action. It communicates “Tell us what you want. We’ll handle the rest.” Optional settings do not compete with input. The empty input cannot submit; typing enables the action without suggesting AI has interpreted the text.

See more expands within the composer; See less collapses it without losing text or selected controls. Paste also opens this extension, but does not automatically select Script. Accepted interpretation is explicit: idea/instructions by default, or My approved script chosen in the extension. No length-based classification, automatic rewrite or post-click interpretation dialog is accepted. Approved scripts retain authoritative preservation, translation/adaptation and factual-warning requirements.

The extension exposes output language, topic duration (replaced by words-based duration information for Script), visual style, voice, captions, gentle motion, music, Review before rendering, financial details and Details. Accepted product controls remain bounded by the product specification; disabled/single-choice prototype options do not reduce the accepted curated style/voice/language scope or establish availability. Defaults remain English, five-minute topic, Minimal Illustration, default supported voice, captions/motion on, music off, manual review off. No provider/model settings leak into the default path.

The final prototype's Create Video collapses options and moves in place to a queued progress presentation without another screen. This establishes the accepted authorization interaction and spatial continuity; the static example is not proof of paid execution or backend feasibility. Simple production includes the initial render; optional manual review pauses before it. Do not turn the prototype's read-only composer or manual state buttons into a new global project-edit lock or production control.

### Production and workspace

Progress names creator outcomes: Gathering sources (only when Research is entitled and applicable), Writing script, Planning scenes, Creating images, Creating narration, Preparing timing and captions, Rendering video. Script mode uses Checking facts rather than topic research/script rewriting. Optional/unneeded stages are not presented as mandatory. Show completed counts where known, active scene/scope and preserved outputs; never invent provider percentages or completion estimates. Render percentages use real measured progress and distinguish validation from encoding completion.

Desktop workspace: scene list left, dominant selected-scene preview center with playback below, correction panel right. Scene navigation uses consistent thumbnail frames, tabular scene numbering, a restrained selected surface with an olive edge marker, short narration excerpt and essential status text. Keep compact editor headings, aligned controls and useful density. Desktop scene navigation, preview and inspector can scroll independently while project actions remain reachable. Use a compact project-level readiness disclosure such as “2 issues before rendering”. Expanded blockers are actionable: select the scene and Narration/Visual context and focus the relevant correction. Ordinary issues sit locally beside affected controls, not in a dominant full-width warning strip. Serious global failures may use stronger presentation; no blocker becomes hidden or toast-only. Full-video playback is a clear action; identify whether playback is current project preview or a previous export. A static image/audio view is not falsely labeled a fully composed video preview; representative preview feasibility remains gated.

Correction panel has Narration and Visual as primary views. Narration exposes approved words, autosave, audio playback, effective voice and regeneration. Visual exposes current image, plain-language visual description, generation prompt through detail disclosure, image regeneration/replacement and history. Preserve the distinction between description and actual generation prompt; do not invent separate model controls. Captions, scene timing, motion and project music/settings are secondary views. Caption editing never edits narration. No freeform professional timeline or new scene/add/duplicate controls.

Show outdated audio alongside edited words only with an explicit mismatch notice. After narration edits, image remains visible with Keep image / Replace or regenerate review actions. Before regeneration, explain the actual affected scene scope in creator language, including sibling scenes sharing audio: “Regenerating this narration will update audio for Scenes 7–11. Their words stay unchanged.” This is an example, not a fixed segmentation rule. A Scene remains the editing unit even when a paid narration request covers several scenes. Estimated usage and maximum spend remain available through optional financial details; affected content scope stays clear before the action. Avoid “regenerate only this scene” unless verified policy actually provides that scope.

## Status, history and recovery

Use plain labels, short reasons and the next safe action. Prototype-only labels such as Fixture, Static design preview and Illustrative state, sample monetary values, manual state controls and unverified segment examples are not normal production vocabulary or data. Distinguish asset compatibility, review flags and last attempt outcome; a failed retry does not mean a prior valid image failed. Autosave uses Saving / Saved / Could not save; unsaved content is not presented as safely persisted.

| State | Presentation and action |
| --- | --- |
| Queued | Queue position when known; cancellation available; no promised completion time. |
| Running | Actual stage/scope and completed work; edits allowed for asset generation. |
| Waiting for approval | Explain the specific changed scope/text and provide review; do not conceal material scope changes; routine financial review is optional; material scope approval remains explicit. |
| Budget / allowance / storage blocked | Name the constraint, preserve work and explain eligible next action; no upgrade/payment CTA. |
| Partial failure | Name failed scenes/components and show successes; targeted retry/replacement/delete where permitted. |
| Failed | Specific failure and retry/recovery action; previous compatible assets/exports remain visible. |
| Cancelling / canceled | Distinguish requested cancellation from confirmed cessation; explain pending usage and history-only late outputs. |
| Recovering / unknown outcome | Explain uncertainty, retained allowance hold and owner reconciliation; disable unsafe duplicate retry. |
| Outdated | Explain which edit caused it, preserved version and necessary refresh. |
| Review needed | Specific creator decision, distinct from technical failure. |
| Completed | Scope-specific success; assets ready is distinct from export ready or publishable video. |

History opens predictably from the correction context as an edge panel/sheet with accessible dismissal and return focus. Image history uses thumbnails; narration history uses listenable entries with associated words and voice. Mark Current, date/source and usage where useful. Details reveals generation provenance and pending/settled cost. No branch graph, commits or Git-like revision language. Restore confirmation lists affected words/settings and compatibility consequences. Restoring existing assets costs no generation allowance; separately quote any necessary regeneration. Single-scene audio restoration cannot silently restore sibling scenes.

Failures use inline scene messages plus a project-level summary, never toast-only reporting. An entitled Research/checking failure is a private non-blocking notice with retained sources and authorized retry access. Research non-entitlement instead explains the plan requirement and offers no bypass retry; the separate checking policy remains unchanged. Missing images/audio or invalid timing block rendering; no silent placeholders. Render failure retains the last export and offers local retry after the lock releases. Concurrent-edit late results remain history with usage visible. Interrupted work says Recovering until safe resumption is established.

## Render and export

Render readiness lists missing/outdated required assets, unresolved enabled captions and timing conflicts with links to affected scenes. Disabled captions do not block; audio/scene timing always must be valid. Rendering locks all content controls and explains why, while viewing, previous-export download and cancel remain usable. Queued render does not lock editing; relevant edits require a refreshed plan. Do not use a UI-only lock as authorization.

Progress distinguishes rendering, output validation and export ready. Successful export shows 1080p MP4, download and prior exports. Previous exports remain downloadable after edits with a “Before your latest changes” indication. Cancel/failure/completion releases the lock only after confirmed cessation; recovery handles interrupted locks. Retrying rendering reuses assets and consumes no generation allowance, while operating budget constraints still apply.

## Motion

Motion communicates hierarchy, cause and effect, state changes, progress, selection and spatial relationships. Landing and creation may be slightly more expressive; production uses faster, quieter functional feedback. Never delay input or require waiting for an animation. Use restrained color/border/opacity changes and small local settling, not glow, bounce, elastic motion, exaggerated scale, parallax, decorative background motion or AI sparkles. Do not animate every card or control continuously.

### Entry and carousel

Hero hierarchy is reinforced by a brief heading entrance followed by slightly softer copy/actions/media settling. All content and controls remain immediately usable; no cinematic intro or hidden wait.

Carousel rhythm is show → pause → smooth right-to-left advance by about one image → settle → pause → repeat. Keep three images visible with slightly larger middle imagery and a clean visually matched loop; no obvious reset or continuous marquee. The final exploration uses a faster rhythm than its first version, while retaining a meaningful viewing pause. Exact interval, duration and center-size ratio are reversible details, not production constants.

Provide quiet Previous/Next and Pause/Play controls. Pointer hover and keyboard focus pause automatic advancement; it resumes after interaction ends unless explicitly paused. Touch interaction pauses until explicit resumption. Hidden tabs stop advancement. Announce manual image changes accessibly without continuously announcing automatic movement. Media content/color remains independent of theme. Playback audio requires deliberate action.

### Controls, creation and dashboard

Hover/focus/press feedback uses restrained color, border and subtle media-brightness shifts. Focus remains clearly visible independently of motion. Tabs and selected scene rows respond immediately; no large travel or bouncing. Project hover/focus feedback does not move the layout. Only relevant active-production status may have a small restrained pulse, accompanied by readable text; no fake percentage.

Composer focus emphasizes its frame; nonempty input quietly enables the primary action. See more/less smoothly expands/collapses the same connected composer body, preserves selections and tolerates reversal without a separate settings-page transition. Create Video itself grants bounded authority; do not insert a mandatory financial-review modal. The demonstrated creation-to-queued transition stays local to the composer and preserves context.

### Production and correction

Selecting a scene updates content immediately; preview and correction inspector settle together with a quick local fade/minimal movement. Narration/Visual switching uses equally restrained context feedback for the same scene. Preserve navigation/scroll context and avoid dramatic page transitions or stale media masquerading as the new scene.

Render issues disclose/collapse smoothly and quickly. Choosing a blocker navigates/focuses its correction context with clear local feedback. History uses a predictable short edge-sheet entrance; closing/Escape returns focus. Scene navigation on narrow screens remains a functional sheet, not a cinematic reveal.

Queued → running → complete/failed uses plain status text with small local transition feedback. An optional restrained pulse indicates running activity, never completion percentage. Saved → outdated communicates the cause beside affected assets and in readiness; regeneration/render start preserve successful work and indicate actual scope. Real execution evidence drives production statuses. Prototype state buttons, sample completion/failure and canned progress are evaluation aids only: never promote them to product controls or treat them as asset generation.

### Reduced motion and timing

Observe prefers-reduced-motion, including changes during the session. Remove nonessential entrances, spatial settling, smooth scrolling and pulses; disclosures become effectively immediate. Automatic carousel movement stops; three-image presentation and manual navigation remain, with immediate changes. Keep readable text, focus, selected markers and all actions available.

Routine editor actions feel immediate, disclosures smooth but fast, entry slightly more expressive, and carousel movement more deliberate. Exact milliseconds/easing, breakpoints and rendering technology are not frozen. Prefer efficient transform/opacity feedback; bounded disclosure geometry may animate without repeated layout measurement. No animation framework or component architecture is selected by the exploration.

## Responsive priorities

Desktop is primary but mobile supports the complete scene-correction workflow. Responsive breakpoints follow available content width rather than device names; exact widths are exploration details.

| Width condition | Composition and preserved actions |
| --- | --- |
| Wide | Three columns; selected preview and corrections simultaneously visible; compact global header. |
| Intermediate | Scene navigation becomes a collapsible panel/sheet; preview and correction area retain readable widths. |
| Narrow / mobile | Preview above active Narration/Visual view; scene chooser opens a sheet. Secondary captions/timing/history/settings open dedicated views or sheets. Preserve Create, approval, cancellation, recovery, render and download. |

Mobile uses explicit Move up / Move down for ordering; drag is optional, never the only interaction. Timing uses labeled numeric/time fields and accessible adjustments, not tiny waveform handles. Avoid dense multi-column history dialogs. Long scripts scroll naturally; sticky primary actions must not obscure input, software keyboard, focused fields or safe-area content. Header collapses labels/actions into a labeled menu while retaining project identity, status and a route back. No essential functionality silently disappears or says desktop required. Mobile preview may reduce size but keeps current/outdated identification and playback accessible.

## Accessibility baseline

Target WCAG 2.2 AA behavior and contrast, with verification during implementation. Normal text at least 4.5:1; large text and meaningful controls at least 3:1 as applicable. Visible keyboard focus in both themes, non-color-only statuses, persistent form labels and semantic buttons/links are required. Touch targets meet the AA minimum and favor comfortable larger areas on mobile.

Keyboard reaches every scene, playback control, correction, reorder action and disclosure. Logical focus order follows visible composition. Dialogs/sheets have an accessible name, appropriate focus management, Escape dismissal where safe and return focus to the trigger; confirmations cannot disappear as if accepted. Tabs/disclosures expose selected/expanded state. Status updates use polite live announcements without reading every progress tick; urgent actionable failures are announced appropriately. Disabled actions explain blockers in reachable text, not hover-only tooltips. Playback includes keyboard controls; preview overlays and warnings must not obscure captions. Zoom/reflow preserve controls and reading order. Reduced motion is supported throughout.

## Anti-patterns and deferred details

No purple/blue AI gradients, glowing borders, glassmorphism, excessive pills/cards, decorative sparkles, arbitrary badges, empty giant heroes, analytics dashboards, provider settings in the default flow, professional timelines or fake progress. No public pricing, billing, publishing, collaboration, voice cloning, custom style studio, recurring-character guarantees, vertical workflow or Emphasis Text in the initial release.

Visual, motion and one-tap authorization choices are accepted; no high-impact design choice remains unresolved. No additional competing design direction is required. Exact accessible tokens, font package, pixel measurements, breakpoints, animation timings/easing, frontend technology and component architecture remain reversible implementation details rather than decisions frozen by this prototype. Provider capability, preview/audio-join feasibility, upload limits, storage caps, allowances and hosting remain their existing operational/architecture gates, not design decisions silently resolved here. Public demo media permission/compatibility must be checked before publishing. Discovery/exploration is closed. These documents do not authorize further prototypes, production implementation, paid calls, deployment purchases, TASKS.md generation or architecture spikes.
