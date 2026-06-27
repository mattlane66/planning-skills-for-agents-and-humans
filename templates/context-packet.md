# Context Packet

## Task
What the next planning or implementation move should do.

## Source artifacts
- @planning/frame.md
- @planning/shaping.md
- @planning/breadboard.md
- @planning/slices.md
- @planning/executable-breadboard.md, when the selected slice is ready for build handoff
- @planning/interface-contracts.md, when boundary detail is split out separately
- @planning/dumplink.md, when task groups, risk states, dependencies, or sequence matter

## Authority order
1. User's latest explicit instruction
2. Selected slice or kickoff doc
3. Executable breadboard, when present
4. Selected interface contract, for boundary-level input/output details
5. Selected breadboard
6. Selected shaping direction
7. Framing doc
8. Raw notes and transcripts
9. Rejected alternatives and brainstorming

## Use these sections first
- ...

## Do not use unless needed
- raw interview notes
- old discarded alternatives
- brainstorming notes
- rejected shapes

## Must preserve
- stable requirement IDs
- stable place and affordance IDs
- store IDs
- selected slice boundary
- executable breadboard fixtures, example runs, expected outputs, and acceptance tests, when present
- contract IDs and boundary names, when present
- field names, required/optional distinctions, enum values, nullability, and error cases, when specified
- Dumplink task group IDs, dependency order, risk states, and cuts, when present
- explicit non-goals
- demo path

## Selected requirements
- ...

## Relevant places / affordances / stores
- ...

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
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
6. Flag missing field names, nullability, enum values, error cases, fixtures, expected outputs, or acceptance tests instead of inventing them.
7. Work toward the goal condition, run the required checks, and report incomplete verification directly.

## Verification target
- ...
