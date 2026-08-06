# Context Packet

## Task
What the next planning or implementation move should do.

## Source artifacts
- @planning/frame.md
- @planning/shaping.md
- @planning/appetite.md, when Appetite is recorded separately from shaping
- @planning/breadboard.md, accepted in `selected-design` mode
- @planning/statechart.md, when a selected stateful scope needs it
- @planning/slices.md
- @planning/executable-breadboard.md, when the selected slice is ready for build handoff
- @planning/interface-contracts.md, when boundary detail is split out separately
- @planning/dumplink.md, when task groups, risk states, dependencies, or sequence matter
- applicable product-repository instructions, glossary, architecture notes, ADRs, tests, and public interfaces

Candidate-shape breadboards are not governing source artifacts for implementation. Restate only an implication that was explicitly accepted into shaping or the selected-design breadboard.

## Authority order
1. User's latest explicit instruction
2. Selected project boundary
3. Selected Dumplink task group or other selected slice, for active implementation scope
4. Executable breadboard, when present
5. Selected interface contract, for boundary-level input/output details
6. Accepted selected-design breadboard
7. Selected shaping direction
8. Kickoff doc, for builder orientation only
9. Framing doc
10. Raw notes and transcripts
11. Candidate-shape breadboards, rejected alternatives, and brainstorming

A statechart is derived from the selected-design breadboard and never outranks it.
The selected project governs outer scope. The selected Dumplink task group or other selected slice governs active implementation scope. Within that slice, the executable breadboard governs expected behavior and examples, and a contract governs its named exchange. The Dumplink plan governs project-wide grouping and order. None may expand the selected project or active slice. A kickoff doc is not build scope or sequence. A candidate breadboard is exploratory evidence, not selected behavior.

## Use these sections first
- ...

## Do not use unless needed
- candidate-shape breadboards
- raw interview notes
- old discarded alternatives
- brainstorming notes
- rejected shapes
- unaccepted sketch-reconciliation deltas

## Must preserve
- stable requirement IDs
- stable place and affordance IDs from the accepted selected-design breadboard
- store IDs
- accepted Appetite and cut line
- selected project boundary and active task-group or slice boundary
- canonical project terms and relevant architectural decisions
- existing interfaces or seams the selected work preserves or intentionally changes
- executable breadboard fixtures, example runs, expected outputs, and acceptance tests, when present
- contract IDs and boundary names, when present
- field names, required/optional distinctions, enum values, nullability, and error cases, when specified
- Dumplink task group IDs, dependency order, risk states, and cuts, when present
- statechart state and transition IDs with their source selected-design breadboard IDs, when present
- explicit non-goals
- demo path
- accepted visual changes as written into authoritative artifacts; do not promote pending reconciliation proposals
- accepted candidate findings only as incorporated into shaping or selected-design intent

## Project language and decisions
- Canonical terms:
- Relevant architectural decisions:
- Existing interfaces or seams:
- Terms or decisions this work may introduce:
- Documentation updates proposed but not yet authorized:

## Selected requirements
- ...

## Relevant selected-design places / affordances / stores
- ...

## Relevant statechart
- Selected scope:
- States and transitions:
- Source selected-design breadboard IDs:
- Explicit gaps:

## Relevant executable breadboard
- Selected slice:
- Example starting data / fixtures:
- Example runs:
- Expected user-visible results:
- Expected state changes:
- Expected side effects:
- Edge cases:
- Acceptance tests:
- Open decisions:

## Relevant interface contracts
- Contract:
- Boundary:
- Input shape:
- Output shape:
- Branches / errors:
- Open decisions:

## Relevant Dumplink plan
- Active task group:
- Relevant tasks:
- Risk state:
- Dependencies:
- Cuttable scope:
- Acceptance checks:
- Stop condition:

## Current slice
- Slice:
- Demo:
- Produces:
- Exclusions:

## Execution contract
- Goal condition:
- Required checks:
- Allowed files / areas:
- Out-of-scope changes:
- Return-to-planning conditions:
- Checkpoint cadence:
- Verification caveats:

## Open questions
- ...

## Build-handoff behavior
1. Restate the relevant constraints, selected-design behavior, and project language.
2. Confirm that no candidate-shape breadboard is being treated as build scope.
3. Identify implementation implications and existing seams.
4. Ask at most 3 blocking questions.
5. Propose a plan before editing code.
6. If implementation reality changes the plan, propose a planning update instead of silently drifting.
7. Flag missing authority decisions, field names, nullability, enum values, error cases, fixtures, expected outputs, acceptance tests, or durable terminology decisions instead of inventing them.
8. Work toward the goal condition, run the required checks, and report incomplete verification directly.

## Verification target
- ...
