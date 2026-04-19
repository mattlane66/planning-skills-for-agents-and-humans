---
planning: true
---

# Simple Grocery List — Breadboard Reflection

This is a post-implementation example.

Assume the code was built, and now the team wants to compare the implementation to the breadboard.

## What was synced to reality

After reading the implementation, the following differences were found:

- Bought items are moved into a separate `boughtItems` array instead of being kept in one `items` store with a `bought` boolean.
- The UI removes bought items immediately, so the `hide bought` toggle no longer controls visibility.
- Duplicate checking only catches exact case-sensitive matches, so `Milk` and `milk` are treated as different items.

## Smells found

| ID | Smell | Where | Why it matters |
|----|-------|-------|----------------|
| BF1 | Drift from chosen shape | Item state model | The chosen shape used one item store plus a visibility filter. The implementation changed the state model and lost that simplicity. |
| BF2 | Mixed responsibility | Bought toggle handler | Toggling bought state also removes items from the visible list, which mixes state change with display control. |
| BF3 | Hidden state split | Needed vs bought arrays | Separating the arrays makes the data model harder to reason about and weakens the original single-list concept. |
| BF4 | Incomplete duplicate normalization | Add-item flow | Users can still create duplicates that differ only by capitalization. |

## Proposed fixes

| ID | Change | Expected improvement |
|----|--------|----------------------|
| F1 | Return to one `items` store with a `bought` boolean | Matches the chosen shape and simplifies state reasoning |
| F2 | Restore the `hide bought` toggle as a display-only filter | Re-separates item state from visibility control |
| F3 | Normalize text before duplicate comparison | Makes duplicate detection behave consistently |
| F4 | Update the breadboard tables to reflect the actual implementation before any further critique | Prevents design discussion from being based on stale artifacts |

## Updated breadboard notes

- The intended design works best when item state and visibility are separate concerns.
- The implementation drift suggests the toggle flow was optimized for immediacy instead of maintaining the cleaner model chosen during shaping.
- Before any additional slicing or planning, the breadboard and code should be brought back into the same story.
