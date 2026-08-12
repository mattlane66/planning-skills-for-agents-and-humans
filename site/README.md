# Interactive documentation portal

`index.html` is the distributable portal. It contains its application code, styles, ranked search index, canonical guides and skills, linked repository references, all canonical templates and skill references, example artifacts, Mermaid renderer, and referenced image assets in one file.

## Open it

1. Download `site/index.html`, or clone the repository.
2. Open the file in a modern browser with JavaScript enabled.

No web server or network connection is required. GitHub's source-code viewer does not execute HTML, so download the file instead of expecting the repository file view to behave like a deployed website.

The JavaScript bundle targets Safari 15.4 and newer. The responsive layout includes iPhone safe-area handling, dynamic viewport-height fallbacks, 44-pixel mobile controls, collapsible documentation navigation, and touch-friendly horizontal trails. Current Safari, Chrome, Firefox, and Edge are the recommended browsers.

## Rebuild it

Use Node.js 20 or newer:

```bash
cd site
npm install
npm run check
```

`npm run check` regenerates the content index from the repository, rebuilds the standalone HTML, verifies that no external runtime scripts or stylesheets remain, exercises the primary interactions, and crawls every generated route for heading, table-of-contents, embedded-link, search, semantic, and mobile-safeguard regressions.

The tracked source is organized as follows:

- `src/app.js` — portal routes and interactions
- `src/styles.css` — responsive visual system
- `scripts/generate-content.mjs` — canonical Markdown and asset indexing
- `scripts/build-standalone.mjs` — single-file bundling
- `scripts/validate-build.mjs` — standalone artifact checks
- `scripts/test-interactions.mjs` — direct-open interaction checks
- `scripts/test-integrity.mjs` — full route, content, accessibility-semantic, search, and mobile-safeguard checks

The generated `src/generated/` and temporary `.build/` directories are intentionally ignored. The finished `index.html` remains tracked so it can be downloaded and opened immediately.
