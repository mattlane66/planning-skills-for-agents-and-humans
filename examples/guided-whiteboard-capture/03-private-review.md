# Private narrated revision (synthetic; proposal only)

**PENDING** human decision. No accepted artifact has been modified.

### New guided correction (TOUR-4, NARRATED)

> “After Confirm, keep me on the Request screen and show a **Confirmed** message. Don't send me straight back to Queue. When I return to Queue later, the request still shouldn't be pending.”

Baseline: [candidate A](./02-candidate-breadboard.md), working only.

## Model-first semantic delta

| Delta | Kind | IDs | Before | Proposed | Decision |
| --- | --- | --- | --- | --- | --- |
| D1 | substantive | N1, P2, U3; new U4 | N1 updates S1 then returns to P1 | N1 updates S1, remains in P2, shows U4 Confirmed; P1/U3 excludes done requests upon later return | **pending** |
| D2 | no change | U1, U2, S1 | Review, Confirm, pending/done marker | Preserve IDs and behavior | no change |
| D3 | unresolved | “Cancel?” | Open | Still open; no invented ID | deferred |

**Private proposed table rows; not canonical yet:**

| ID | Place | Proposed wiring/meaning | Evidence |
| --- | --- | --- | --- |
| N1 | P2 | Mark done → S1 → U4; stay in P2 | TOUR-4 |
| U4 | P2 | Show Confirmed status after N1 | TOUR-4 |
| U3 | P1 | On later unspecified return, exclude done requests | TOUR-4 |

## Visual before / proposed after

```text
BEFORE                                    PROPOSED (not accepted)
P1 Queue → P2 Request                      P1 Queue → P2 Request
                U2 Confirm                                 U2 Confirm
                    ↓                                          ↓
                N1 → S1                                  N1 → S1
                    │                                          │
                    └────→ P1/U3                               └──→ U4 Confirmed
                                                                 (stay in P2)
                                            P1/U3 hides request on future return
                                            Return navigation: UNKNOWN
```

## Prose diff (same place order)

**P1 Queue/U3:** ~~Confirm immediately returns to Queue with the item removed.~~ **Proposed:** After a later return by an as-yet-unknown path, U3 excludes done requests.

**P2 Request/U2/N1/U4:** ~~Confirm returns to Queue.~~ **Proposed:** Confirm updates S1 through N1, remains on P2, and shows U4 Confirmed; failed-confirmation behavior is UNKNOWN.

## Human gate

Ask the human to **accept / revise / reject / defer** D1. No decision was recorded here. If working material is revised, preserve traceable IDs and mark remaining unknowns. If the baseline were accepted, follow `planning-change-reconciliation` (and `sketch-reconciliation` for visual changes), keep the accepted source untouched until explicit authorization, update canonical tables first, rerun affected traces/fit/scope checks, and then regenerate projections. No implementation or publishing is authorized.
