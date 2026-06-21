# Context Packet

## Task
What the implementation or planning agent should do now.

## Source artifacts
- @planning/frame.md
- @planning/shaping.md
- @planning/breadboard.md
- @planning/slices.md
- @planning/interface-contracts.md, when boundary detail matters

## Authority order
1. User's latest explicit instruction
2. Selected slice or kickoff doc
3. Selected interface contract, for boundary-level input/output details
4. Selected breadboard
5. Selected shaping direction
6. Framing doc
7. Raw notes and transcripts
8. Rejected alternatives and brainstorming

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
- contract IDs and boundary names, when present
- field names, required/optional distinctions, enum values, nullability, and error cases, when specified
- selected slice boundary
- explicit non-goals
- demo path

## Selected requirements
- ...

## Relevant places / affordances / stores
- ...

## Relevant interface contracts
- Contract:
- Boundary:
- Input shape:
- Output shape:
- Branches / errors:
- Open decisions:

## Current slice
- Slice:
- Demo:
- Produces:
- Exclusions:

## Open questions
- ...

## Required behavior for the implementation agent
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
6. Do not invent missing field names, nullability, enum values, or error cases; flag them.

## Verification target
- ...
