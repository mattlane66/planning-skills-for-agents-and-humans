---
planning: true
shaping: true
artifact_type: breadboard
status: draft
source_of_truth: true
feeds:
  - slices
  - interface-contracts
  - executable-breadboard
  - context-packet
  - implementation
---

# [Project] — Breadboard

# Context Card

## Mode and authority

- Mode: `current-state` or `selected-design`
- Authority: descriptive current-state evidence or accepted selected intent
- Evidence references: required for non-obvious current-state claims
- Selected shape and appetite: required for selected-design mode

Current-state mode cannot define selected future intent or feed slice selection. Only an accepted selected-design breadboard can produce buildable slice candidates.

## Use this when
An agent is mapping current behavior, detailing a selected design, slicing an accepted selected-design breadboard, preparing downstream contracts, or checking whether code still matches selected intent.

## Must preserve
- stable place IDs
- stable affordance IDs
- store IDs
- wiring and visible consequences
- selected demo path
- interface contract candidate IDs when present

## Ignore unless asked
- rejected shapes
- raw brainstorms

## Selected shape reference
- Shaping artifact:
- Selected shape:
- Appetite:
- Cut line:

## Places

| ID | Place | Description |
|---|---|---|
| P1 | ... | ... |

## UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| U1 | P1 | ... | ... | ... | -> N1 | — |

## Non-UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| N1 | P1 | ... | ... | call | -> S1 | -> U1 |

## Stores

| ID | Place | Store | Description |
|---|---|---|---|
| S1 | P1 | ... | ... |

## Product-relevant branches

| Branch | Trigger | User-visible consequence |
|---|---|---|
| ... | ... | ... |

## Interface contract candidates (optional)

Use this section when a wire crosses a meaningful boundary: UI -> backend, frontend -> API, service -> store, agent -> tool, import -> parser, or external integration.

These candidates may later be split into a separate interface-contract artifact or embedded inside an executable breadboard.

| ID | Trigger / Wire | From | To | Request / Input Shape | Response / Output Shape | Branches / Errors | Open Decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | UI | API | user_id: string; items: array | order_id: string; status: pending | missing item, invalid quantity | Should promo codes be nullable or omitted? |

## Slice candidates

| Slice | Affordances / stores included | Demo | Produces | Unknowns |
|---|---|---|---|---|
| V1 | ... | ... | ... | ... |

## Build handoff note

Once a slice is selected and ready for implementation, convert the relevant part of this breadboard into an executable breadboard with examples, expected results, edge cases, and acceptance tests.

## Notes
- ...

## Self-check
- [ ] Every displayed UI element that depends on data has a source.
- [ ] Every non-UI affordance connects by Wires Out or Returns To.
- [ ] Stores exist for meaningful side effects.
- [ ] Product-relevant branches are explicit.
- [ ] Meaningful boundary crossings have interface contract candidates when field-level detail would reduce agent guessing.
- [ ] Slices are vertical and demoable.
- [ ] The selected slice can be converted into an executable breadboard before build handoff.
