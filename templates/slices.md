---
planning: true
shaping: true
artifact_type: slices
status: draft
source_of_truth: true
feeds:
  - context-packet
  - implementation
---

# [Project] — Slices

# Context Card

## Use this when
An agent needs the selected slice boundary, sequencing, demo path, and verification target before implementation.

## Must preserve
- selected slice
- demo path
- Produces line
- exclusions
- dependency order

## Breadboard reference
- Breadboard artifact:
- Selected shape:
- Appetite:

## Slice inventory

| Slice | Name | Included affordances / stores | Demo | Produces | Dependencies | Unknowns |
|---|---|---|---|---|---|---|
| V1 | ... | ... | ... | ... | none | ... |
| V2 | ... | ... | ... | ... | V1 | ... |

## Dependency pass

| Slice | Depends on | Why |
|---|---|---|
| V1 | none | ... |

## Unknowns pass

| Slice | Unknown | Can move earlier? | Spike needed? |
|---|---|:---:|:---:|
| V1 | ... | ✅ | ❌ |

## Selected slice

- Slice:
- Demo path:
- Produces:
- Exclusions:
- Verification target:

## Cut candidates

| Candidate | Reason to cut | Revisit when |
|---|---|---|
| ... | ... | ... |

## Self-check
- [ ] Every slice is vertical and demoable.
- [ ] The selected slice has an observable output.
- [ ] The Produces line is clear.
- [ ] Dependencies are sequenced before unknowns are optimized.
- [ ] Cut candidates are explicit.
