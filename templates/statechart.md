# [Project] — Statechart

Use this only for a selected stateful portion of an accepted breadboard. The breadboard tables remain authoritative.

## Source

- Breadboard:
- Selected scope or slice:
- Source place, affordance, store, and wiring IDs:

## State inventory

| State ID | Source breadboard IDs | State | Parent state | Meaning | Status |
| --- | --- | --- | --- | --- | --- |

Use `explicit`, `inferred`, or `missing` for Status.

## Transition table

| Transition ID | From | Trigger type | Event | Guard | Effect | To | Source wiring | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Mermaid statechart

```mermaid
stateDiagram-v2
```

The diagram is a projection of the transition table, not a separate source of truth.

## Gaps and proposed breadboard updates

| Gap | Missing or ambiguous behavior | Affected breadboard IDs | Recommended breadboard update |
| --- | --- | --- | --- |
