---
planning: true
---

# Simple Grocery List — Shaping

## Appetite

- Time budget: a few focused days for a deliberately small first version
- Team shape: one builder
- Review point: a working same-device demo
- Cut line: no accounts, sharing, categories, pricing, recipes, or store-specific behavior
- Accepted uncertainty: lightweight visual polish can remain rough for the demo
- Must-resolve unknowns: none before shape selection

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | User can add a grocery item quickly from one place. | Core goal |
| R1 | User can mark an item as bought and undo that state if needed. | Must-have |
| R2 | User can see what is still needed at a glance while shopping. | Must-have |
| R3 | Bought items can be hidden without being deleted. | Must-have |
| R4 | The list persists between sessions on the same device. | Must-have |
| R5 | Exact duplicate item names are prevented or made obvious at add time. | Nice-to-have |

## Requirement smell check

Early idea that was kept out of `R`:
- "Maybe this is just a tiny web page"

Why it stayed out:
- the underlying need is fast capture and clear in-store use
- a web page is one possible shape, not a requirement

## Shapes

### A: Single list with bought toggle and hide-bought filter

| Part | Mechanism |
|------|-----------|
| A1 | One list view with quick-add input at the top |
| A2 | Each item stored once with a `bought` boolean |
| A3 | Inline checkbox toggles bought/unbought state |
| A4 | Hide-bought toggle filters the list without deleting bought items |
| A5 | Local persistence restores items on load |
| A6 | Duplicate check runs when adding a new item |

### B: Separate Needed and Bought sections

| Part | Mechanism |
|------|-----------|
| B1 | Quick-add input at the top |
| B2 | Items move between a Needed section and a Bought section |
| B3 | Bought section can be collapsed |
| B4 | Local persistence restores both sections on load |
| B5 | Duplicate check runs when adding a new item |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | User can add a grocery item quickly from one place. | Core goal | ✅ | ✅ |
| R1 | User can mark an item as bought and undo that state if needed. | Must-have | ✅ | ✅ |
| R2 | User can see what is still needed at a glance while shopping. | Must-have | ✅ | ✅ |
| R3 | Bought items can be hidden without being deleted. | Must-have | ✅ | ✅ |
| R4 | The list persists between sessions on the same device. | Must-have | ✅ | ✅ |
| R5 | Exact duplicate item names are prevented or made obvious at add time. | Nice-to-have | ✅ | ✅ |

## Notes

- Shape A keeps all item state in one list and uses filtering to control what is visible.
- Shape B gives stronger visual separation between needed and bought items, but it introduces more structure than this first version needs.
- Both shapes fit the requirements. The difference is mostly about simplicity versus stronger categorization.

## Appetite Fit

| Shape | Fits appetite? | Required cuts | Uncertainty / spike |
|---|:---:|---|---|
| A | ✅ | Keep duplicate handling simple and same-device only | None before selection |
| B | ✅ | Avoid section-management features beyond collapse | None before selection |

## Reverse Fit Check

| Shape part | Requirement served | Justified? | Notes |
|---|---|---|---|
| A1 quick-add input | R0 | Yes | Directly supports fast capture. |
| A2 single item store | R1, R2, R3, R4 | Yes | Keeps bought state and visibility behavior legible in one model. |
| A3 bought checkbox | R1 | Yes | Supports bought and undo behavior. |
| A4 hide-bought toggle | R2, R3 | Yes | Hides without deleting. |
| A5 local persistence | R4 | Yes | Required for return visits on the same device. |
| A6 duplicate check | R5 | Yes, but cuttable | Serves the nice-to-have duplicate criterion and can be deferred if appetite tightens. |

No Shape A mechanism is currently unsupported by a requirement.

## Human Decision

Recorded human choice: **A**

Reason:
- It satisfies all current requirements.
- It keeps the state model simpler for a first version.
- It supports the clearest path to a breadboard and small vertical slices.

## Detail A

The first version should be a simple single-surface list with:
- quick-add input
- item rows with bought toggle
- hide-bought filter
- local persistence
- duplicate prevention at add time
