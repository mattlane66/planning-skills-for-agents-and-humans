---
planning: true
artifact_type: kickoff
status: selected
source_of_truth: true
feeds:
  - implementation-packet
  - context-packet
---

# Simple Grocery List — Kickoff

# Context Card

## Use this when
An agent needs the builder-facing reference for the selected grocery-list direction.

## Must preserve
- one main list surface
- quick-add input at the top
- inline bought/unbought toggling
- hide-bought as a display-only filter
- local persistence without accounts
- duplicate prevention at add time

## Ignore unless asked
- separate Needed and Bought sections
- build sequence beyond the first-version constraints
- categories, sharing, pricing, recipes, or store-specific behavior

## Frame

### Problem
- The current grocery list lives in ad hoc messages, so the state of what is still needed is easy to lose.
- The list is not easy to use while shopping because bought and unbought items blur together.
- The user wants something much smaller than a full shopping or meal-planning system.

### Outcome
- The user can add items quickly.
- The user can mark items bought and optionally hide them.
- The list persists on the same device between sessions.

### Constraints
- No accounts or sign-in
- No pricing, recipes, categories, or store-specific behavior
- First version should stay intentionally small

## Shape

### List surface
- There is one main list surface.
- The add input lives at the top of this surface.
- Each item appears in the same list rather than being moved to a separate screen.
- The chosen direction is a single-list model with filtering, not separate Needed and Bought sections.

### Item state changes
- Each item can be toggled between bought and unbought inline.
- Bought items are not deleted when hidden.
- Duplicate prevention happens when the user tries to add an exact duplicate item name.

### Visibility control
- A hide-bought toggle controls whether bought items remain visible.
- This is a display concern only. It should not change the underlying item state.

### Persistence and startup
- The list restores from local persistence on load.
- The initial state should be usable immediately without account setup or onboarding.

## Notes for the builder
- Keep the first version centered on one screen and one list model.
- Do not add secondary features such as categories or sharing.
- The most important user test is whether the list is fast to update and easy to scan while shopping.
