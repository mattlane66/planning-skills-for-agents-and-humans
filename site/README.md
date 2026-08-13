# Planning Skills Lab

`index.html` is the distributable, hands-on companion to the repository. Its primary experience lets the reader click through eight predetermined stages of the Simple Grocery List example. At each stage it shows what the human supplied or decided, what the planning agent did, the artifact that resulted, and the plan accumulated so far. The walkthrough includes the accepted requirements matrix, two shaped paths that both pass fit before a human selects between their tradeoffs, a rendered selected-design breadboard, and a Dumplink-style view of tasks clustered into sequenced vertical groups. The handoff stage separates the resolved planning subset from the target-repository context that must be inspected before coding, then exposes the complete packet fields; the final stage shows how implementation drift returns to a human decision.

This is a walkthrough, not a quiz. The Compass, Model, and Reference remain available behind it. The walkthrough teaches what the collaboration feels like and how its outputs compound; the embedded repository material supplies the canonical detail and evidence.

## Open it

1. Download `site/index.html`, or clone the repository.
2. Open the file in a modern browser with JavaScript enabled.

No web server or network connection is required. GitHub's source-code viewer does not execute HTML, so download the file instead of expecting the repository file view to behave like a deployed website.

The JavaScript bundle targets Safari 15.4 and newer. The responsive layout includes iPhone safe-area handling, dynamic viewport-height fallbacks, thumb-friendly stage controls, a horizontally scrollable progress rail, collapsible input/output/plan panels, a single-column mobile model, and collapsible reference navigation. Current Safari, Chrome, Firefox, and Edge are the recommended browsers.

## Rebuild it

Use Node.js 20 or newer:

```bash
cd site
npm install
npm run check
```

`npm run check` regenerates the content index, rebuilds the standalone HTML, checks the walkthrough and promotion model against canonical repository rules, exercises the complete eight-stage collaboration, and crawls every generated route for heading, table-of-contents, embedded-link, search, semantic, accessibility, and mobile regressions.

The tracked source is organized as follows:

- `src/app.js` — portal routes and interactions
- `src/planning-model.js` — walkthrough stages, concise skill roles, promotion gates, map order, and example story
- `src/styles.css` — responsive visual system
- `scripts/generate-content.mjs` — canonical Markdown and asset indexing
- `scripts/build-standalone.mjs` — single-file bundling
- `scripts/validate-build.mjs` — standalone artifact checks
- `scripts/test-interactions.mjs` — direct-open interaction checks
- `scripts/test-planning-model.mjs` — canonical sequencing and authority checks
- `scripts/test-integrity.mjs` — full route, content, accessibility-semantic, search, and mobile-safeguard checks

The generated `src/generated/` and temporary `.build/` directories are intentionally ignored. The finished `index.html` remains tracked so it can be downloaded and opened immediately.
