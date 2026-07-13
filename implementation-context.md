# Implementation Context

Compatibility template for handing one selected slice to an implementation agent.

Prefer [`templates/context-packet.md`](./templates/context-packet.md) for new work. This file uses the same authority order and execution-contract rules so older links do not create a competing source of truth.

## When to use this

Use it after a human has selected a direction and demoable slice, immediately before implementation. Reference upstream artifacts by path and include only the rows needed for the active slice.

## Template

```md
# Implementation Context

## Active task

### Selected slice
`V1`

### Build now
What this implementation pass must produce.

### Do not build now
Explicit exclusions and non-goals.

### Demo path
The smallest user-visible path that proves the slice works.

## Source artifacts

- `planning/frame.md`
- `planning/shaping.md`
- `planning/breadboard.md`
- `planning/statechart.md`, when relevant to this slice
- `planning/interface-contracts.md`, when relevant
- `planning/executable-breadboard.md`, when present
- `planning/dumplink.md`, when an active task group governs scope or sequence
- `planning/kickoff.md`, when present

## Authority order

1. User's latest explicit instruction
2. Selected slice or kickoff doc
3. Executable breadboard, when present
4. Selected interface contract, for boundary-level input/output details
5. Selected Dumplink task group and sequence, for task-group scope and build order
6. Selected breadboard
7. Selected shaping direction
8. Framing doc
9. Raw notes and transcripts
10. Rejected alternatives and brainstorming

A statechart is derived from the selected breadboard and never outranks it. Existing code and tests are implementation evidence, not automatic authority to silently override selected product behavior. When reality conflicts with the packet, stop and use the drift protocol.

## Must preserve

- selected requirement IDs
- relevant place, affordance, and store IDs
- selected slice ID and boundary
- relevant statechart and transition IDs, when present
- relevant contract IDs and field-level decisions, when present
- executable examples, fixtures, expected outputs, and acceptance tests, when present
- active Dumplink task-group boundary and sequence, when present
- explicit non-goals
- visible demo path

## Relevant behavior

| Source ID | Actor or system | Action / event | Expected response | Visible consequence |
| --- | --- | --- | --- | --- |

## Relevant statechart

- Selected scope:
- States and transitions:
- Source breadboard IDs:
- Explicit gaps:

## Data and interface contracts

| Contract ID | Boundary | Inputs | Outputs | Branches / errors | Open decisions |
| --- | --- | --- | --- | --- | --- |

Do not invent missing field names, nullability, enum values, units, or error behavior.

## Fixtures and example runs

| Run ID | Starting state | Action | Expected visible result | Expected state change |
| --- | --- | --- | --- | --- |

## Acceptance checks

| Check ID | Proves | How to verify |
| --- | --- | --- |

## Execution contract

- Goal condition:
- Required checks:
- Allowed files / areas:
- Out-of-scope changes:
- Return-to-planning conditions:
- Checkpoint cadence:
- Verification caveats:

## Verification target

What observable result proves the selected slice is complete.

## Drift protocol

If implementation reality conflicts with this packet:

1. Name what the selected artifact says.
2. Name what the implementation currently does or requires.
3. Explain the product or scope risk.
4. Recommend updating the code, updating the planning artifact, or splitting/cutting the slice.
5. Do not silently change intent.
```
