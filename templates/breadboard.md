---
planning: true
shaping: true
artifact_type: breadboard
status: draft
source_of_truth: true
feeds:
  - slices
  - context-packet
  - implementation
---

# [Project] — Breadboard

# Context Card

## Use this when
An agent is implementing, slicing, or checking whether code still matches the planned interaction.

## Must preserve
- stable place IDs
- stable affordance IDs
- store IDs
- wiring and visible consequences
- selected demo path

## Ignore unless asked
- rejected shapes
- raw brainstorms

## Selected shape reference
- Shaping artifact:
- Selected shape:
- Appetite:

## Places

| ID | Place | Description |
|---|---|---|
| P1 | ... | ... |

## UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| U1 | P1 | ... | ... | ... | → N1 | — |

## Non-UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| N1 | P1 | ... | ... | call | → S1 | → U1 |

## Stores

| ID | Place | Store | Description |
|---|---|---|---|
| S1 | P1 | ... | ... |

## Product-relevant branches

| Branch | Trigger | User-visible consequence |
|---|---|---|
| ... | ... | ... |

## Slice candidates

| Slice | Affordances / stores included | Demo | Produces | Unknowns |
|---|---|---|---|---|
| V1 | ... | ... | ... | ... |

## Notes
- ...

## Self-check
- [ ] Every displayed UI element that depends on data has a source.
- [ ] Every non-UI affordance connects by Wires Out or Returns To.
- [ ] Stores exist for meaningful side effects.
- [ ] Product-relevant branches are explicit.
- [ ] Slices are vertical and demoable.
