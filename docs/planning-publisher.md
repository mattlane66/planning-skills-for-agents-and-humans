# Planning Publisher

Planning Publisher compiles canonical planning Markdown into two synchronized derived outputs: a normalized PlanningPackage for agents and a self-contained responsive shaped-work HTML document for humans.

The Markdown remains authoritative. The package and HTML are projections, not a new planning layer.

## Why this exists

Planning Skills already produces strong artifacts for agents, but humans often need to understand a shaped bet by looking at it rather than reading several files in sequence. The publisher gives both audiences the same compiled source:

- agents can consume normalized PlanningPackage JSON
- humans get one mobile-friendly HTML document
- stable planning IDs remain traceable in both
- Accepted, Selected, Deferred, Working, and rejected material can stay visibly distinct
- presentation cannot silently become new product truth

The visual target is a shaping board, not a generic dependency graph: representative journey, dominant product surface, selected-mechanism annotations, hidden behavior on a secondary rail, decision evidence, requirements, and selected/deferred slices.

## Run it

From this repository:

    python3 scripts/publish_shaped_work.py \
      --planning-dir examples/simple-grocery-list \
      --output /tmp/simple-grocery-list-shaped-work.html \
      --json-output /tmp/simple-grocery-list-planning-package.json

For a product repository, point --planning-dir at that product's planning directory.

The publisher automatically discovers a frame Markdown file, a shaping Markdown file, and a mode: selected-design breadboard when one exists. Use --frame, --shaping, or --breadboard when discovery would be ambiguous.

Validate without writing:

    python3 scripts/publish_shaped_work.py --planning-dir planning --check

## PlanningPackage

The normalized package includes frame problem/outcome/transformation, Appetite, requirements and authority, candidate shapes and parts, fit evidence, the explicit human-selected shape, breadboard places and affordances, stores, behavior traces, candidate slices, the selected active slice, presentation hints, and derived authority labels.

The HTML embeds the complete package in an application/json script element with id planning-package. An agent can inspect the same compiled data without reverse-engineering the page layout.

## Presentation hints

A planning directory may contain optional presentation.json. It is presentation metadata, not planning truth. It may choose what to foreground, but it cannot invent a requirement, mechanism, place, affordance, store, or slice.

Example fields:

    {
      "schema_version": 1,
      "hero_place": "P1",
      "journey_scenarios": ["Add a new item", "Mark bought or undo"],
      "featured_ids": ["A1", "A3", "A4"],
      "annotations": [{"ref": "A1", "text": "Keep quick-add on the main surface."}]
    }

Every ID reference is validated against canonical artifacts. An unknown ID fails publication. If presentation.json is absent, the publisher derives conservative defaults from the selected shape and breadboard.

## Authority rule

Skills create and update planning truth. The publisher compiles planning truth into an inspectable visual artifact.

A visual rearrangement is not a planning update. If review reveals missing or wrong behavior, change the owning planning artifact through the appropriate skill or reconciliation step and regenerate.

## Visual grammar

The first renderer follows these rules:

- Problem → Outcome → Appetite → Selected Shape at the top
- representative behavior before implementation detail
- one dominant place/surface when supported by the breadboard
- selected shape mechanisms as local annotations
- hidden consequences and stores on a secondary rail
- requirements × shapes retained as decision evidence
- selected build scope emphasized
- deferred accepted behavior muted but still visible
- stable IDs clickable so the visual traces back to planning

For interactions where spatial arrangement matters, breadboarding should still produce targeted SK# sketches. Future renderers can add richer support for those sketches without changing the canonical model.

## Renderer boundary

The compiler boundary is deliberately renderer-neutral:

    Markdown -> PlanningPackage -> presentation model -> renderer

The current renderer is standalone HTML. Future adapters can target SVG/PNG, FigJam, Figma, Excalidraw, TLDraw, or Miro without moving planning logic into those surfaces.
