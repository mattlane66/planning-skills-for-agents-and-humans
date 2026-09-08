# Planning Skills Lab

`index.html` is the distributable, hands-on companion to the repository. Its primary experience lets the reader click through eight predetermined stages of the Simple Grocery List example. At each stage it shows what the human supplied or decided, what the planning agent did, the artifact that resulted, and the plan accumulated so far. A compact invocation layer shows the portable prompt and supported runtime shortcut for the current move; contextual optional branches show where the remaining skills would be useful without presenting all fourteen skills as a mandatory workflow. The walkthrough includes the accepted requirements matrix, two shaped paths that both pass fit before a human selects between their tradeoffs, a rendered selected-design breadboard, and a Dumplink-style view of tasks clustered into sequenced vertical groups. The handoff stage separates the resolved planning subset from the target-repository context that must be inspected before coding, then exposes the complete packet fields; the final stage shows how implementation drift returns to a human decision.

This is a walkthrough, not a quiz. The Compass, Model, and Reference remain available behind it. The walkthrough teaches what the collaboration feels like and how its outputs compound; the Reference lets readers select any canonical skill and copy an accurate invocation. Portable natural-language prompts are primary. Claude Code and Gemini shortcuts appear only where the repository actually supplies them, and Codex is correctly described as plugin plus natural-language invocation rather than Claude-style slash commands.

## Open it

1. Download `site/index.html`, or clone the repository.
2. Open the file in a modern browser with JavaScript enabled.

No web server or network connection is required. GitHub's source-code viewer does not execute HTML, so download the file instead of expecting the repository file view to behave like a deployed website.

The JavaScript bundle targets Safari 15.4 and newer. The responsive layout includes iPhone safe-area handling, dynamic viewport-height fallbacks, thumb-friendly stage controls, a horizontally scrollable progress rail, collapsible input/output/plan panels, a single-column mobile model, and collapsible reference navigation. Current Safari, Chrome, Firefox, and Edge are the recommended browsers.

## Rebuild it

Use Node.js 20.19+, 22.13+, or 24+ (matching the committed dependency lock):

```bash
cd site
npm install
npm run check
```

`npm run check` regenerates the content index, rebuilds the standalone HTML, checks the walkthrough and promotion model against canonical repository rules, exercises the complete eight-stage collaboration in JSDOM, and crawls every generated route for heading, table-of-contents, embedded-link, search, semantic, accessibility, and mobile regressions.

CI also runs `npm run test:browser` under a real Chrome/Chromium process. That smoke opens the tracked `index.html` directly over `file://`, activates a focused control from the keyboard, waits for Mermaid to render an SVG, repeats the app at a 390 px viewport, and fails on browser runtime errors. It intentionally sits outside `npm run check` because Node 20 remains supported for deterministic build checks while the CDP smoke uses Node 22's built-in WebSocket client and a locally installed browser.

The hosted deployment model is documented in [`../docs/site-deployment.md`](../docs/site-deployment.md). Pull-request validation is read-only; a failing portal-drift check uploads the regenerated `index.html` and patch as an artifact instead of granting PR code write credentials. GitHub Pages deploys only from a trusted `main` commit after the tracked standalone file is reproduced exactly.

The tracked source is organized as follows:

- `src/app.js` — portal routes and interactions
- `src/planning-model.js` — walkthrough stages, concise skill roles, promotion gates, map order, and example story
- `src/styles.css` — responsive visual system
- `scripts/generate-content.mjs` — canonical Markdown and asset indexing
- `scripts/build-standalone.mjs` — single-file bundling
- `scripts/validate-build.mjs` — standalone artifact checks
- `scripts/test-interactions.mjs` — JSDOM interaction checks
- `scripts/test-browser-smoke.mjs` — real Chrome/Chromium direct-file, keyboard, Mermaid, narrow-screen, and runtime-error smoke
- `scripts/test-planning-model.mjs` — canonical sequencing and authority checks
- `scripts/test-integrity.mjs` — full route, content, accessibility-semantic, search, and mobile-safeguard checks

The generated `src/generated/` and temporary `.build/` directories are intentionally ignored. The finished `index.html` remains tracked so it can be downloaded and opened immediately.
