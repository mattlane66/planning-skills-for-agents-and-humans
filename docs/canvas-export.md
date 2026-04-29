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

Mermaid is the portable visual projection. Canvas tools are review and collaboration surfaces.

```text
Tables = canonical model
Mermaid = portable visual projection
Canvas = review / collaboration surface
```

## Export contract

To support reliable export into canvas tools:

- Keep stable IDs in node labels: `P1`, `U1`, `N1`, `S1`.
- Group nodes by place.
- Preserve diagram labels from headings.
- Use solid arrows for control flow / `Wires Out`.
- Use dashed arrows for returns, data flow, and visible consequences.
- Do not add behavior to a diagram that is missing from the tables.
- Do not treat a rearranged canvas as a planning update until the tables have been updated.
- If the canvas diverges, update the tables first, then regenerate.

## Adapter pattern

A canvas exporter should be structured as adapters around a shared pipeline:

```text
Markdown source
  -> Mermaid block extractor
  -> Mermaid renderer
  -> Canvas-neutral diagram objects
  -> Target adapter
```

Target adapters may include:

- TLDraw adapter
- Excalidraw adapter
- FigJam adapter
- Miro adapter

The target adapter should not own the planning logic. It should only project the canonical breadboard into the target canvas.

## Static image export

The simplest adapter renders Mermaid to SVG or PNG and places that image on the canvas.

Pros:

- easy to support across tools
- preserves Markdown and Mermaid as the source pipeline
- good for pan, zoom, walkthrough, and review

Cons:

- not editable as individual canvas objects
- canvas edits do not automatically flow back into the breadboard tables

Use this first.

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

> Tables first. Mermaid second. Canvas third.

A canvas is useful because it makes the system easier to inspect. It is not a substitute for a well-formed breadboard.
