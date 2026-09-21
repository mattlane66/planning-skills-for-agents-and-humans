# Canvas Export

Breadboards can be rendered into visual canvas tools for review, zooming, walkthroughs, and collaboration.

The planning artifact stays the source of truth. Canvas views are derived projections.

## Source of truth

The canonical breadboard model is:

- Places table
- UI Affordances table
- Non-UI Affordances table
- Stores table
- Wiring captured in `Wires Out` and `Returns To`

If a canvas view disagrees with the tables, update the tables first and regenerate the view.

## Derived views

Derived views can include:

- Mermaid diagrams
- TLDraw boards
- Excalidraw scenes
- FigJam boards
- Miro boards
- exported SVG or PNG diagrams

The **visual breadboard** is the primary human projection for nontrivial interactive work. It should use deliberate spatial composition and may include targeted sketches. Mermaid remains a useful compact fallback when automatic layout is sufficient.

```text
Canonical tables = planning model
Visual breadboard = primary human projection
Mermaid = compact / portable fallback
Canvas or SVG = preferred deliberate rendering surface
```

## Included live viewer

The repository ships a local hot-reload viewer for the Mermaid layer:

```bash
bash scripts/watch-planning-diagrams.sh examples/simple-grocery-list/03-breadboard.md
```

It watches one or more Markdown files, renders every Mermaid block with the pinned local Mermaid package, and updates the browser after each save. See [visual hot reload](./visual-hot-reload.md).

This closes the live visual review loop without making the browser view authoritative. TLDraw, FigJam, Miro, and Excalidraw remain optional target adapters.

## Export contract

To support reliable export into canvas tools:

- Keep stable IDs in node labels: `P1`, `U1`, `N1`, `S1`.
- Group visible affordances by place and preserve the place-as-stack composition.
- Preserve diagram labels from headings.
- Preserve targeted-sketch IDs and their mappings to canonical breadboard IDs.
- Keep the representative user journey visually dominant.
- Keep hidden logic and stores on a secondary system rail when possible.
- Keep branches local to the decision that causes them and minimize wire crossings.
- Use solid arrows for control flow / `Wires Out`.
- Use dashed arrows for returns, data flow, and visible consequences.
- Do not add behavior to a diagram that is missing from the tables.
- Do not treat a rearranged canvas as a planning update until the tables have been updated.
- If the canvas diverges, update the tables first, then regenerate.

## Adapter pattern

A canvas exporter should be structured as adapters around a shared pipeline:

```text
Breadboard Markdown tables
  -> normalized breadboard model
  -> visual-composition objects (places, rails, branches, notes, SK# sketches)
  -> target adapter
  -> optional Mermaid fallback
```

The normalized breadboard model is an in-memory typed graph derived from the tables. It may be serialized as JSON when a downstream tool needs machine-readable graph data, but JSON is not a required planning artifact.

For the **whole shaped-work package**, use [Planning Publisher](./planning-publisher.md). It extends the same separation across frame, shaping, selected-design breadboard, decision evidence, and slice state:

```text
Canonical planning Markdown
  -> normalized PlanningPackage
  -> validated presentation model
  -> standalone shaped-work HTML
  -> future SVG / PNG / canvas adapters
```

The `PlanningPackage` is useful to agents; the HTML is the human projection. Optional `presentation.json` may choose what to foreground, but every referenced stable ID is validated against canonical planning artifacts and cannot create new behavior or authority.

Target adapters may include:

- TLDraw adapter
- Excalidraw adapter
- FigJam adapter
- Miro adapter

The target adapter should not own the planning logic. It should only project the canonical breadboard into the target canvas.

## Static image export

The simplest deliberate renderer produces an SVG or HTML-canvas visual breadboard directly from the normalized model and its composition hints. Mermaid-to-SVG remains acceptable as a fallback for flows that do not need local fidelity or deliberate placement.

Pros:

- portable and easy to review
- supports explicit placement, whitespace, annotations, and targeted-sketch regions
- preserves the canonical tables as the planning source
- good for pan, zoom, walkthrough, and review

Cons:

- not editable as individual canvas objects unless the target supports semantic objects
- visual edits do not automatically flow back into the breadboard tables

Start with direct SVG/HTML rendering when the interaction benefits from spatial composition; use Mermaid when auto-layout is genuinely sufficient.

## Semantic object export

A more advanced adapter converts breadboard elements into real canvas objects:

- places become frames or sections
- affordances become cards or nodes
- stores become database/state nodes
- wiring becomes connectors

Pros:

- editable board objects
- closer to native FigJam, Excalidraw, and Miro collaboration
- can preserve stable IDs on each object

Cons:

- harder to implement
- each canvas has a different object model
- layout becomes part of the system
- round-tripping changes back to Markdown is risky

Use semantic export only when the team needs editable canvas objects.

## Breadboarding rule

Canvas export should not make the diagram more authoritative than the breadboard.

Use this rule:

> Canonical model first. Human-readable visual second. Target canvas third.

Mermaid may serve as the visual layer when it is clear enough, but it should not force an interaction into a generic dependency-graph layout. A canvas is useful because it makes the system easier to inspect; it is not a substitute for a well-formed breadboard.
