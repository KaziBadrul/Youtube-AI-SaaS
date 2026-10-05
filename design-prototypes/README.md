# Alpha static visual exploration

Open `design-prototypes/index.html` directly in a browser. No installation, build or server is required. Each direction is independent: open its `index.html` and use Projects / New Video, or open `workspace.html` directly. Relative media links require keeping this folder in the repository.

Each direction includes `index.html`, `projects.html`, `create.html`, `workspace.html`, `style.css` and `prototype.js`. The root includes this README and the comparison index.

## A — Editorial Creative

An editorial interpretation with left-aligned headline/media columns, a project ledger separated by rules, a generous border-light idea field and a flat, compact workspace. Typography and alignment carry hierarchy rather than container decoration.

Tradeoff: project rows prioritize scanning titles and states over a large gallery. The restrained workspace provides less surface separation; spacing and dividers do more work.

Reference influence: typography-1 drives bold heading hierarchy; typography-2 drives readable interface text. The dashboard reference informs creation and recent-project priorities, interpreted as rows. The landing reference informs strong outcome text beside rich media. The video-editor reference informs three workspace regions; audio-editor informs text-first narration correction.

## B — Production Studio

A preview-led landing composition, compact project board, bounded creation surface and tighter workspace with a narrow scene rail and stronger panel hierarchy. The center preview has more room; correction controls remain contextual.

Tradeoff: denser controls and smaller scene thumbnails favor repeated production work but require more visual scanning on first use. Surfaces provide stronger separation without introducing timeline or keyframe complexity.

Reference influence: products/video-editor drives preview prominence, scene navigation and contextual correction; products/audio-editor informs compact text/settings organization. The dashboard reference informs the thumbnail board, the landing reference supplies the outcome-to-media relationship, and details-button informs disclosure.

## C — Warm Creator (selected, refined)

Direction C is the selected foundation. Its focused refinement keeps welcoming imagery and cream/forest/olive identity, adds a consistent thumbnail-led project grid, emphasizes the idea input, and tightens the professional correction workspace. Dark mode uses a more neutral near-black plum foundation. Readiness is compact and scene issues contextual.

Tradeoff: the consistent grid gives each project comparable prominence; local issue placement requires a clearly visible project readiness summary to keep blockers discoverable.

Reference influence: palette references define the warm light / subtle plum dark relationship; landing and dashboard references inform media and collection hierarchy; typography references keep confident headings and readable controls; editor and audio references preserve preview-led correction and narration scope. See [focused refinement notes](direction-c/README.md).

## Shared system and limits

All directions retain the same palette roles: cream, forest and olive in light; subtle deep plum, warm text and olive in dark. Both typography references inform a heavy sans heading / clean regular interface pairing. System fonts are reversible candidates, not assertions about commercial font identity. The button reference informs solid actions and moderate corners, excluding glow. Details-button informs Customize, cost details and secondary settings. The dark palette is a foundation, not an AI accent. Every supplied visual reference contributes within its annotated role.

Theme is prototype-only, optionally remembered locally. Topic / Script, Customize, scene selection, Narration / Visual, original scene-audio playback, full-video playback, notices and disclosures are local demonstrations. `create.html?customize=1` opens the expanded customization example. The original demo export remains distinct from edited narration.

The workspace opens Scene 8 with an illustrative local narration edit, outdated audio/export and image review state. Its Scenes 7–11 narration scope is illustrative, not a finding about demo TTS segmentation. Other scenes show current images. `workspace.html?ready=1` demonstrates the alternative render-ready state with original narration. Dashboard examples demonstrate generating, partial failure and completed export; workspace render controls explain readiness blockers. No provider percentages are invented. Quote amounts are layout fixtures, not pricing or actual estimates. Existing media is reused without mutation.

At narrow widths the scene rail becomes a sheet, followed by preview and correction controls stacked vertically. Keyboard Escape closes the sheet; focus returns to its trigger. Controls remain semantic, labeled and focus-visible. Reduced-motion preference disables optional transition/entrance motion. Static notices stand in for actions requiring real project state; this is not a production frontend foundation.

Verification: all local HTML links and media paths resolve, HTML IDs are unique, and all three JavaScript files pass `node --check`. The Production Studio workspace was inspected in the browser in dark mode. Subsequent browser inspection was interrupted by a native connection failure; a full page/theme/narrow-width visual sweep remains unverified.

The user selected Direction C. Directions A and B are retained unchanged as historical explorations. Accepted DESIGN.md and UX_FLOWS.md remain unchanged. Exact tokens, fonts, breakpoints and timings remain exploration details.
