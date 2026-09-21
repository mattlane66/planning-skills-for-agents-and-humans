---
planning: true
shaping: true
artifact_type: statechart
status: draft
source_of_truth: false
---

# Checkout Assist — Statechart

## State inventory

| State ID | Source breadboard IDs | State | Parent state | Meaning | Status |
|---|---|---|---|---|---|
| ST1 | P1, S1 | Editing | — | Checkout is editable | explicit |
| ST2 | P2, S2 | Confirmed | — | Checkout completed | explicit |

## Transition table

| Transition ID | From | Trigger type | Event | Guard | Effect | To | Source wiring | Status |
|---|---|---|---|---|---|---|---|---|
| TR1 | ST1 | user | submit | valid total | record result | ST2 | U2 -> N1 -> N2 -> N3 | explicit |
