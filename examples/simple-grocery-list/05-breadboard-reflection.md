---
planning: true
---

# Simple Grocery List — Breadboard Reflection

This illustrative post-implementation example compares **only human-selected V1 — Add and persist grocery items** with the accepted selected-design breadboard in `03-breadboard.md`.

## Scope at the handoff

Assume the builder resolved the target-repository context, obtained human acceptance of the execution appetite, and implemented V1. V2 was never selected: bought/unbought controls and hide-bought filtering remain deferred. Their absence is not drift. No later slice is implicitly authorized by this reflection.

V1 carries R0, R4, and **accepted R5 revision 2**. The case-and-space duplicate rule was accepted before shape selection and recorded in N2 behavior before implementation; it is not a new expectation added after seeing the result.

## Current implementation reality

The following illustrative behaviors were recorded without changing the accepted breadboard:

- Adding `Milk` shows it immediately, but reloading the page loses the item.
- Duplicate checking catches a second `Milk`, but allows `milk` and ` milk ` as additional items.
- Bought/unbought controls and the hide-bought filter are absent, as expected for V1.

## Smells found

| ID | Smell | Where | Why it matters |
|----|-------|-------|----------------|
| BF5 | Persistence behavior missing | Save / restore path | R4 and V1 require added items to survive reload; an in-memory list is insufficient. |
| BF6 | Accepted comparison rule missing | N2 duplicate check | Case-sensitive equality violates accepted R5 revision 2 and the selected-design behavior. |

BF5–BF6 and F5–F7 replace the earlier full-product reflection's BF1–BF4 and F1–F4. The earlier findings and fixes are superseded because they assumed work beyond selected V1; their IDs are not reused for these different claims.

These are failures of realized conformance inside V1. They do not establish whether the product improves shopping outcomes; effect has not been assessed here.

## Proposed fixes

| ID | Change | Expected improvement |
|----|--------|----------------------|
| F5 | Restore V1 save-and-reload behavior using the existing persistence seam | Saved items return on the same device. |
| F6 | Apply the accepted trimmed, lower-case comparison and visible duplicate feedback | `Milk`, `milk`, and ` milk ` resolve to one stored item; `Oat milk` remains distinct. |
| F7 | Preserve the current-state record separately until correction is verified | Reality remains evidence rather than silently replacing the plan. |

## Drift decision

Options prepared for the human:

1. Correct V1 against the already accepted behavior and rerun its checks.
2. Propose an explicit change to R4 or R5 and the selected-design behavior, with consequences shown before acceptance.
3. Narrow the active slice only through a new human scope decision.

**Recorded human decision in this worked example:** choose option 1. Restore save-and-reload behavior and the agreed normalized duplicate check. Keep V2 deferred. The accepted requirements and breadboard remain unchanged.

## Verify before closing

Add `Milk`; attempt `Milk`, `milk`, and ` milk ` and confirm visible rejection with one stored item; add `Oat milk` and confirm it stays distinct; reload and confirm both saved items return. Do not mark the correction complete until those checks pass. Do not add V2 controls as part of this fix.
