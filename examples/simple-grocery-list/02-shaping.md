---
planning: true
---

# Simple Grocery List — Shaping

## Accepted transformation frame (x → f() → y)

- x: Partners capture grocery items in messages, producing a list whose pending/bought state is difficult to recover.
- f(): intentionally unspecified solution/shape variable
- y: Capture remains quick while the current needed/bought state is legible and reversible on the same device.
- Gap and boundaries: Add state without accounts, sharing, categories, pricing, recipes, or store-specific behavior.

## Operating model (M)
- Authority: Accepted
- Relevant operating conditions: one-device runtime with local state available between ordinary sessions
- Causal assumptions / projected dynamics: local state remains available across ordinary returns unless storage is cleared or unavailable
- Evidence refs: 01-frame.md
- Revisit conditions: cross-device use, accounts, or a runtime without dependable local persistence enters scope

## Accepted Appetite

Human acceptance recorded before shape selection.

- Time budget: a few focused days for a deliberately small first version
- Team shape: one builder
- Review point: a working same-device demo
- Cut line: no accounts, sharing, categories, pricing, recipes, or store-specific behavior
- Accepted uncertainty: lightweight visual polish can remain rough for the demo
- Must-resolve unknowns: none before shape selection

## Accepted Requirements

Human acceptance recorded before fit comparison and shape selection.

| ID | Requirement | Status | Authority |
|----|-------------|--------|-----------|
| R0 | User can add a grocery item quickly from one place. | Core goal | Accepted |
| R1 | User can mark an item as bought and undo that state if needed. | Must-have | Accepted |
| R2 | User can see what is still needed at a glance while shopping. | Must-have | Accepted |
| R3 | Bought items can be hidden without being deleted. | Must-have | Accepted |
| R4 | The list persists between sessions on the same device. | Must-have | Accepted |
| R5 | Item names that differ only by case or surrounding spaces are treated as duplicates at add time. | Nice-to-have | Accepted |

### R5 decision record

- **Superseded revision 1 (Working):** “Exact duplicate item names are prevented or made obvious at add time.” It left the treatment of case and surrounding spaces unresolved.
- **Accepted revision 2:** names are compared after trimming surrounding spaces and converting to lower case. `Milk`, `milk`, and ` milk ` match; `Oat milk` remains distinct. This explicitly supersedes the earlier wording of R5 while preserving its ID and history.
- **Human decision before selection:** accept revision 2 and its visible duplicate feedback for this bet. Preserve the original item name for display; do not add fuzzy matching, synonyms, or ingredient equivalence.
- A6 and B5 embody this rule. Selected-design behavior and V1 verification must carry it forward; normalization is not a new requirement discovered after implementation.

## Requirement smell check

Early idea that was kept out of `R`:
- "Maybe this is just a tiny web page"

Why it stayed out:
- the underlying need is fast capture and clear in-store use
- a web page is one possible shape, not a requirement

### Optional discovery replay: one question changes the plan

This illustrative replay happens **before requirements acceptance and shape selection**. Its fixtures explain the decision; they are not user-research findings or a claim that a production spike ran.

1. **Working question:** does R5 revision 1 mean literal string equality, or should `Milk`, `milk`, and ` milk ` count as one item?
2. **Focused check, SP1:** compare those fixtures with raw equality and with trimmed, lower-case equality. Raw equality distinguishes all three; the normalized comparison treats them as one. `Oat milk` remains different under either rule.
3. **Proposed change:** revise R5 to state the intended case-and-space behavior and revise A6 / B5 to use that comparison. Keep fuzzy matching and synonyms outside the bet.
4. **Human acceptance and recheck:** accept R5 revision 2, preserve revision 1 as superseded, and rerun fit and reverse fit for both candidates. Both now pass; choosing a shape remains a separate human decision.

The question returned to the requirement and mechanisms. It did not authorize implementation. The accepted matrices below show the result of that loop; their presentation order is not a mandatory exploration sequence.

## Shapes

### A: Single list with bought toggle and hide-bought filter

| Part | Mechanism |
|------|-----------|
| A1 | One list view with quick-add input at the top |
| A2 | Each item stored once with a `bought` boolean |
| A3 | Inline checkbox toggles bought/unbought state |
| A4 | Hide-bought toggle filters the list without deleting bought items |
| A5 | Local persistence restores items on load |
| A6 | Duplicate check compares trimmed, lower-case names when adding a new item |

### B: Separate Needed and Bought sections

| Part | Mechanism |
|------|-----------|
| B1 | Quick-add input at the top |
| B2 | Items move between a Needed section and a Bought section |
| B3 | Bought section can be collapsed |
| B4 | Local persistence restores both sections on load |
| B5 | Duplicate check compares trimmed, lower-case names when adding a new item |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | User can add a grocery item quickly from one place. | Core goal | ✅ | ✅ |
| R1 | User can mark an item as bought and undo that state if needed. | Must-have | ✅ | ✅ |
| R2 | User can see what is still needed at a glance while shopping. | Must-have | ✅ | ✅ |
| R3 | Bought items can be hidden without being deleted. | Must-have | ✅ | ✅ |
| R4 | The list persists between sessions on the same device. | Must-have | ✅ | ✅ |
| R5 | Item names that differ only by case or surrounding spaces are treated as duplicates at add time. | Nice-to-have | ✅ | ✅ |

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
| A6 normalized duplicate check | R5 | Yes, but cuttable | Implements accepted R5 revision 2; may be deferred only through a scope decision. |

No Shape A mechanism is currently unsupported by a requirement.

### Shape B — candidate evidence only

| Shape part | Requirement served | Justified? | Notes |
|---|---|---|---|
| B1 quick-add input | R0 | Yes | Directly supports fast capture. |
| B2 Needed ↔ Bought sections | R1, R2 | Yes | Moving an item either way supports bought / undo and separates needed items. |
| B3 collapsible Bought section | R2, R3 | Yes | Hides bought items without deleting them. |
| B4 local persistence | R4 | Yes | Saves and restores the section state. |
| B5 normalized duplicate check | R5 | Yes, but cuttable | Implements accepted R5 revision 2; may be deferred only through a scope decision. |

Every accepted requirement has supporting parts in each candidate; no part is currently unjustified. Multiple supporting parts express distinct contributions, not automatically redundant mechanisms. A2 carries several requirements and deserves particular scrutiny when behavior is mapped. Coverage claims are design evidence, not proof of sufficiency, realized conformance, or effect. Inspecting B's reverse fit does not select B or make it build scope.

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
- duplicate prevention with visible feedback under accepted R5 revision 2
