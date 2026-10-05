# Static Alpha design exploration

Standalone HTML/CSS study, created under the separate visual-exploration authorization on 2026-10-04. The accepted [design](../../docs/DESIGN.md) and [flows](../../docs/UX_FLOWS.md) control its direction. Proposed tokens, breakpoints and proportions remain reviewable exploration choices.

Open [index.html](index.html) directly in a browser; no framework, server, install, build or network dependency is required. Relative paths use the existing `demo-video-example/` directory; keep the study in this repository.

- [Landing](index.html): outcome message, real example imagery and guided-demo entry.
- [Projects](projects.html): creation action, thumbnail-led projects and representative status.
- [New Video](create.html): topic/script switch, Customize, visible English and authorization placement.
- [Progress](progress.html): prepared walkthrough and links to queued, partial-failure, budget-blocked, unknown-outcome and render-lock descriptions.
- [Workspace](workspace.html): 49 selectable scenes, narration/visual views, recorded scene audio, full example MP4 and local edit/outdated behavior.

Theme supports Light / Dark / System; only this preference uses local storage. Script, narration and visual changes stay in the current page and are lost on reload. The generic “Video studio” label is a placeholder, not a product-name decision. Dollar values, segmentation boundaries, previous asset versions and provider outputs are deliberately not invented.

This is a visual study, not a complete functional application or architecture spike. Paid actions, uploads, sign-in, history, reorder/delete and rendering explain their intended behavior without executing it. Exceptional-state links show copy/composition; the render-lock example does not simulate a running process or enforce a project lock. Existing MP4 playback never represents current locally edited words. No production source, demo media, provider integration, deployment or TASKS.md is changed.

Exploration choices: system sans-serif; 4px spacing basis; 6–12px radii; light cream/forest/olive and dark plum/olive semantic tokens; columns collapse at 1100px and stack at 700px; 120–140ms optional state transitions with reduced-motion handling. These values are candidates, not newly accepted requirements.

Verification performed: JavaScript syntax check; static local-link/media-path checks on all five pages; core body/muted/button text contrast calculations passed 4.5:1 in both themes. Desktop Brave inspection confirmed landing/media display, workspace display and changing scene selection. Mobile CSS is supplied but has not been visually verified on a narrow device; audio boundary accuracy, complete media quality, full keyboard/screen-reader behavior and all semantic color pairs remain unverified. Legacy timing metadata is used only for example playback and is not certified alignment evidence.

Review priorities: creation-page simplicity, preview/correction balance, dark surface tone, readability of scene navigation and narrow-screen layout. This study awaits visual feedback; it does not establish product acceptance or authorize application work.
