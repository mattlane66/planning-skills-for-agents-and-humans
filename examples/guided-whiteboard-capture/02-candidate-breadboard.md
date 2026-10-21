---
planning: true
shaping: true
artifact_type: breadboard
mode: candidate-shape
status: working
source_of_truth: false
---

# Queue Review — candidate A (synthetic)

## Mode, authority, and sources

- Mode: **candidate-shape**, unselected A. Question: how does one pending request become visibly done?
- Requirements: provisional/unspecified. Appetite: unset. Human selection: none. Slice: none.
- Sources: [rough sketch](./01-rough-whiteboard.svg) and [guided tour](./01-guided-tour.md); both synthetic, not observed product evidence.
- **Canonical tables within this candidate mode** are below. The visual and prose are read-only projections; none is selected-design truth.

## Canonical places

| ID | Place | Purpose | Source |
| --- | --- | --- | --- |
| P1 | Queue | Pending requests | IMG-1, TOUR-1 |
| P2 | Request | Review one request | IMG-1, TOUR-1 |

## Canonical affordances, systems, and stores

| ID | Place | Type | Function | Wiring | Source |
| --- | --- | --- | --- | --- | --- |
| U1 | P1 | UI | Review pending request | → P2 | IMG-1, TOUR-1 |
| U2 | P2 | UI | Confirm | → N1 | IMG-1, TOUR-2 |
| N1 | P2 | Non-UI intent | Mark done; implementation UNKNOWN | → S1, → P1 | TOUR-2 |
| S1 | — | Conceptual state | Pending/done marker; storage UNKNOWN | read by U3 | TOUR-2 |
| U3 | P1 | UI | Pending list excludes done request | reads S1 | TOUR-2 |

“Cancel?” (TOUR-3) remains an unresolved question, **not** an affordance. Persistence, error handling, permissions, and navigation mechanics are **UNKNOWN**.

## Representative causal trace

`P1 → U1 → P2 → U2 → N1 → S1 → P1/U3`. The expected consequence is a narrated proposal, **not an observed result**.

## Human visual projection

```text
P1 QUEUE                                P2 REQUEST
────────                                ──────────
U3 Pending list                         Request details
    │                                        │
U1 Review ──────────────────────────────► U2 Confirm
    ▲                                        │
    │                                        ▼
    └─────────────────────────────────── N1 mark done
                                             │
                                             ▼
                                        S1 marker
                                   (storage UNKNOWN)

P2 side note: “Cancel?” — undecided; no control yet
```

## Mirrored prose (same places and order)

**P1 Queue:** Pending items are listed through U3. The user chooses U1 Review; the tour says this enters P2.

**P2 Request:** Details are visible, and U2 Confirm triggers candidate effect N1. N1 changes conceptual S1; TOUR-2 proposes returning to P1, where U3 excludes that request. There is no evidence for storage, validation, retries, or Cancel behavior.

## Review checks

All visual IDs resolve to tables. The entry-to-consequence path is narratively complete but system implementation is OPEN. Candidate status is unchanged; no shape, requirement, or slice was accepted.
