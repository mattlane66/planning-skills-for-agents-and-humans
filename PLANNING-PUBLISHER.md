# Planning Publisher

Planning Publisher compiles canonical planning artifacts into a single normalized package for agents and a visual shaped-work package for humans.

The planning Markdown remains authoritative. Every published file is a derived projection.

## Outputs

The publisher can emit:

- `PlanningPackage` JSON for agents and downstream tools
- one self-contained responsive `shaped-work.html`
- a system-level SVG board
- one SVG board per vertical slice
- optional PNG boards and a PDF overview when CairoSVG is installed

The HTML embeds the complete `PlanningPackage`, keeps stable planning IDs clickable, exposes authority state, collapses unselected candidates by default, and lets a reviewer isolate a slice on the full system board.

The package also contains a renderer-neutral `visual_model` derived from the canonical model plus validated presentation hints. That model is the handoff point for future semantic canvas adapters; individual renderers do not own product-planning logic.

## Architecture

```text
canonical planning Markdown
  -> normalized PlanningPackage
  -> validated presentation model
  -> HTML / SVG renderers
  -> optional PNG / PDF adapters
  -> future semantic canvas adapters
```

Skills create and update planning truth. The publisher does not select a shape, accept a requirement, promote a candidate breadboard, or expand build scope.

## Run it

From the Planning Skills repository:

```bash
python3 scripts/publish-shaped-work.py \
  --planning-dir examples/simple-grocery-list \
  --output /tmp/grocery-shaped-work.html \
  --json-output /tmp/grocery-planning-package.json \
  --svg-dir /tmp/grocery-boards
```

Validate inputs without writing output:

```bash
python3 scripts/publish-shaped-work.py --planning-dir planning --check
```

Optional image exports:

```bash
python3 scripts/publish-shaped-work.py \
  --planning-dir planning \
  --png-dir planning/shaped-work-png \
  --pdf-output planning/shaped-work.pdf
```

PNG/PDF export requires the optional `cairosvg` Python package. HTML, JSON, and SVG have no non-standard Python dependency.

## Inputs

The compiler discovers a frame, shaping artifact, and selected-design breadboard from the planning directory. Explicit `--frame`, `--shaping`, and `--breadboard` paths override discovery.

When present, it also discovers supporting shaped-work artifacts such as:

- Appetite
- slice records
- statecharts
- interface contracts
- executable breadboards
- Dumplink plans
- kickoff documents
- context packets

Supporting artifacts are surfaced as context. They do not change the canonical authority order.

## Presentation model

A planning directory may contain optional `presentation.json`. It controls only how canonical truth is shown.

Supported presentation hints include:

- `hero_place` — which place should dominate the overview
- `journey_scenarios` — which behavior traces lead the board
- `annotations` — terse callouts tied to stable IDs
- `visual_hints` — optional `kind`, `region`, and `order` for places or affordances
- `slice_scopes` — stable IDs to foreground for each canonical slice
- `sketch_assets` — optional relative SVG/PNG/JPEG/WebP files for canonical `SK#` targeted sketches; assets must stay inside the planning directory and are embedded into the self-contained HTML

Example:

```json
{
  "schema_version": 2,
  "hero_place": "P1",
  "visual_hints": {
    "P1": {"kind": "screen", "order": 1},
    "U1": {"kind": "input", "region": "header", "order": 1}
  },
  "slice_scopes": {
    "V1": ["P1", "U1", "U2", "N1", "S1"]
  },
  "sketch_assets": {
    "SK1": "sketches/add-item.svg"
  }
}
```

Every referenced ID must already exist in canonical planning artifacts. Unknown IDs fail publication.

## Visual grammar

The renderer is intentionally closer to a shaped-work wall than a dependency graph:

1. Problem → Outcome → Appetite → Selected Shape
2. authority state visible before the visuals
3. representative journey across the top
4. major places rendered as rough product surfaces
5. controls grouped by optional header/body/footer regions
6. selected mechanisms and decisions as local annotations
7. hidden behavior and stores on a secondary system rail
8. targeted `SK#` sketches preserved when present
9. requirements × shapes retained as decision evidence
10. unselected candidates collapsed by default
11. selected build scope emphasized and deferred accepted slices kept visible
12. each slice gets its own zoomed board and can be isolated on the overview

The visual artifact should pass the same finger-trace test as the breadboard: a reviewer should be able to follow the primary behavior and understand what changes without reading every table row.

## Authority and reconciliation

The visual package must never be used to silently update planning truth.

If a visual review reveals that behavior, scope, or a decision is wrong:

1. update the owning canonical artifact through the relevant planning move
2. reconcile consequential visual changes when required
3. regenerate the published package

The publisher is deliberately one-way:

```text
planning truth -> presentation

not

presentation -> planning truth
```

Semantic FigJam, Figma, Excalidraw, TLDraw, and Miro adapters can be added later against the same `PlanningPackage` without moving planning logic into those tools.
