---
planning: true
shaping: true
artifact_type: slices
status: accepted
source_of_truth: true
feeds:
  - implementation
---

# Checkout Assist — Slices

## Breadboard reference
- Breadboard artifact: gamma.md
- Selected shape: A
- Appetite: one week

## Slice inventory

| Slice | Name | Included affordances / stores | Demo | Produces | Dependencies | Unknowns |
|---|---|---|---|---|---|---|
| V1 | Validate checkout locally | P1, U1, U2, U3, N1, S1 | Enter an order and stop an invalid total locally | validated checkout draft | none | none |
| V2 | Complete checkout | P1, P2, P3, U2, U4, N1, N2, N3, S1, S2 | Submit a valid order and see confirmation | completed checkout | V1 | none |

## Selected slice
- Slice: V1
- Demo path: enter order -> submit -> local invalid feedback
- Produces: validated checkout draft
- Exclusions: payment completion
- Verification target: invalid total never reaches payment
