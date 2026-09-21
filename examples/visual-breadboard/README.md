---
planning: true
shaping: true
artifact_type: breadboard
status: example
source_of_truth: false
---

# Import + Merge — Mixed-Fidelity Visual Breadboard Example

This example exists to demonstrate visual composition, not to define a real product.

The canonical tables would remain authoritative. The board below is a derived human-readable projection.

## Primary scenario

```text
P1 Programs                    P2 Import review                         P3 Program detail
────────────                   ────────────────                        ─────────────────
U1 Add / Import ─────────────► U2 Imported exercises                  U7 Program preview
                               U3 Existing-program match
                                      │
                                      ▼
                              N1 check duplicate / match
                                │                │
                           no match            match
                                │                │
                                ▼                ▼
                           N2 create        SK1 Merge chooser
                                │                │
                                └──────┬─────────┘
                                       ▼
                                  N3 save result ─────────────────────► U7
                                       │
                                       ▼
                                   S1 programs
```

### System rail

- `N1` is below the visible review place because it explains the branch but is not itself a user destination.
- `S1` sits below the save consequence because persistence matters to later behavior without dominating the board.

## SK1 — Merge chooser

Elaborates: `P2 / U4 / U5 / U6 / S1`

Question resolved: how the user compares imported material with an existing program before choosing what to keep.

```text
┌──────────────────────────── Merge chooser ────────────────────────────┐
│ Existing program                    Imported material                 │
│ ┌──────────────────────┐           ┌──────────────────────┐          │
│ │ Exercise A           │           │ Exercise A           │          │
│ │ Exercise B           │           │ Exercise C           │          │
│ └──────────────────────┘           └──────────────────────┘          │
│                                                                      │
│ [Keep existing]   [Use imported]   [Merge selected items]            │
└──────────────────────────────────────────────────────────────────────┘
```

The sketch deliberately stops there. It does not specify colors, typography, exact spacing, animation, or unrelated program-detail UI.

## Why this is mixed fidelity

- Routine navigation stays as low-detail place stacks.
- The duplicate/match decision is explicit because it changes the path.
- Persistence appears as a system-rail store because it affects later behavior.
- Only the merge chooser receives a targeted sketch because spatial comparison is the unresolved interaction.
- No behavior exists only in the sketch.
