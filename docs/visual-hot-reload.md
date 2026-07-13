# Visual hot reload

The repository includes a working local viewer for Mermaid diagrams inside planning Markdown files. It watches the files, renders every fenced `mermaid` block in a browser, and refreshes the diagrams after each save.

## Start the viewer

From the repository root:

```bash
bash scripts/watch-planning-diagrams.sh examples/simple-grocery-list/04-breadboard.md
```

The first run installs the pinned local Mermaid dependency. The viewer then opens `http://127.0.0.1:3456` and prints every watched file.

Watch several artifacts together:

```bash
bash scripts/watch-planning-diagrams.sh \
  examples/simple-grocery-list/04-breadboard.md \
  examples/statechart-retry-workflow/02-derived-statechart.md
```

Choose another port or prevent automatic browser opening:

```bash
bash scripts/watch-planning-diagrams.sh --port 4567 --no-open examples/simple-grocery-list/04-breadboard.md
```

Replace the example path with any Markdown planning artifact that contains fenced `mermaid` blocks.

## Behavior

- extracts all backtick- or tilde-fenced Mermaid blocks
- labels each diagram with the nearest preceding Markdown heading
- serves Mermaid from the pinned local package rather than a CDN
- watches files through a portable polling loop that survives editor atomic-save behavior
- sends reload events to the browser without a page refresh
- binds to localhost by default and uploads nothing
- displays parse or rendering errors without stopping the watcher

The Markdown tables remain authoritative. The viewer is a live visual projection for inspection and collaboration.

## Direct package commands

```bash
cd visualizer
npm ci
npm test
npm start -- --no-open ../examples/simple-grocery-list/04-breadboard.md
```

Use `--port 0` in automation to select any available local port.

## Relationship to canvas tools

The included viewer closes the visual hot-reload loop for Mermaid. TLDraw, FigJam, Miro, and Excalidraw remain optional projection targets described in [`docs/canvas-export.md`](./canvas-export.md); they are not required for live review.
