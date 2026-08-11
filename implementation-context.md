# Implementation Context

Compatibility template for handing one selected Dumplink task group or other selected slice to an implementation agent.

Prefer [`templates/context-packet.md`](./templates/context-packet.md) for new work. This file uses the same authority order and execution-contract rules so older links do not create a competing source of truth.

## When to use this

Use it after a human has selected a direction and demoable slice, immediately before implementation. Requirements and Appetite used to govern the build must be Accepted, not Working. Reference upstream artifacts by path and include only the accepted rows needed for the active slice.

Working shaping material, candidate-shape breadboards, focused spikes, and exploratory prototypes are not active build scope.

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

- `planning/frame.md`, when the accepted problem boundary matters
- `planning/shaping.md` — Accepted R/Appetite/selection only
- `planning/breadboard.md` — accepted selected-design behavior
- `planning/statechart.md`, when relevant to this slice
- `planning/interface-contracts.md`, when relevant
- `planning/executable-breadboard.md`, when present
- `planning/dumplink.md`, when an active task group governs scope or sequence
- `planning/kickoff.md`, when present

## Authority order

1. User's latest explicit instruction
2. Selected project boundary
3. Selected Dumplink task group or other selected slice, for active implementation scope
4. Executable breadboard, when present
5. Selected interface contract, for boundary-level input/output details
6. Accepted selected-design breadboard
7. Accepted shaping decisions: selected direction, Accepted requirements, Accepted Appetite/cut line, and cuts
8. Kickoff doc, for builder orientation only
9. Accepted frame / problem boundary
10. Working shaping material, candidate evidence, raw notes, rejected alternatives, and brainstorming — discovery context only

A statechart is derived from the selected-design breadboard and never outranks it. The selected project governs outer scope; the selected Dumplink task group or other selected slice governs active implementation scope. Within that slice, the executable breadboard governs expected behavior and examples, and a contract governs its named exchange. The Dumplink plan governs project-wide grouping and order. None may expand the selected project or active slice. A kickoff doc is not build scope or sequence. Working R/S/fit/Appetite and candidate breadboards are exploratory, not selected behavior. Existing code and tests are implementation evidence, not automatic authority to silently override selected product behavior. When reality conflicts with the packet, stop and use the drift protocol.

## Must preserve

- Accepted requirement IDs
- Accepted Appetite and cut line
- selected shape and cuts
- relevant selected-design place, affordance, and store IDs
- selected project boundary and active task-group or slice ID and boundary
- relevant statechart and transition IDs, when present
- relevant contract IDs and field-level decisions, when present
- executable examples, fixtures, expected outputs, and acceptance tests, when present
- active Dumplink task-group boundary and sequence, when present
- explicit non-goals
- visible demo path

## Do not use as build scope

- Working requirements, Appetite, or fit checks
- candidate shapes not explicitly selected
- candidate-shape breadboards or focused spikes
- exploratory sketches/prototypes
- rejected alternatives or raw brainstorms

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
