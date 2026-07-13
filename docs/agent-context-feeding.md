# Agent Context Feeding

Planning artifacts are most useful to agents when they are fed at the right fidelity. Do not paste the whole planning stack by default. Package the small amount of context the agent needs for the current phase, name the source artifacts, and preserve stable IDs so the agent can trace implementation work back to the plan.

## Why this exists

The skills in this repo produce human-readable planning artifacts. Agent context feeding turns those artifacts into machine-usable working context without flattening them into generic instructions.

The goal is to prevent common agent failures:

- treating old brainstorms as selected direction
- losing non-goals and constraints
- implementing mechanisms that no longer fit the frame
- changing the breadboard silently when code reality pushes back
- treating raw notes, selected requirements, and build instructions as equal authority
- inventing interface details such as field names, nullability, enum values, or error cases
- coding from an ordinary breadboard when an executable breadboard is needed

## Core rule

Feed the agent the smallest context packet that can support the next move.

A good context packet tells the agent:

1. what task it is doing now
2. which planning artifacts are source material
3. which sections matter first
4. which sections should be ignored unless needed
5. what constraints, IDs, and non-goals must be preserved
6. which executable breadboard or interface contracts must be preserved, when present
7. what verification target proves the work stayed aligned

## Artifact roles

Breadboard = structure of the solution.

Statechart = optional derived behavioral view of a selected stateful portion of the breadboard.

Interface contract = what crosses a boundary.

Executable breadboard = structure plus interface contracts, fixtures, example runs, expected outputs, edge cases, and tests.

Dumplink = vertical task grouping, risk/dependency sequence, and scope cuts for selected shaped work.

Context packet = the exact subset handed to the build agent.

Use ordinary breadboards while shaping. Use executable breadboards when a selected slice is ready for implementation preparation.

## Context packet template

# Context Packet

## Task
What the agent should do now.

## Source artifacts
- @planning/frame.md
- @planning/breadboard.md
- @planning/statechart.md, when the selected scope needs it
- @planning/slices.md
- @planning/executable-breadboard.md, when the selected slice is ready for implementation
- @planning/interface-contracts.md, when boundary contracts are split out separately
- @planning/dumplink.md, when task-group scope or sequence matters

## Use these sections first
- frame.md: Outcome, Constraints, Non-goals
- breadboard.md: Places, Affordances, Stores, Wiring, Interface contract candidates
- statechart.md: Relevant states, transitions, source breadboard IDs, and explicit gaps
- slices.md: Selected slice, Demo, Produces
- executable-breadboard.md: Selected slice, Relevant breadboard structure, Interface contracts, Example starting data, Example runs, Edge cases, Acceptance tests, Open decisions, Verification target
- interface-contracts.md: Contract IDs, boundaries, input shapes, output shapes, branches, errors, open decisions
- dumplink.md: Active task group, dependencies, risk state, cuts, acceptance checks, and stop condition

## Do not use unless needed
- raw interview notes
- old discarded alternatives
- brainstorming notes
- rejected shapes

## Must preserve
- stable requirement IDs
- stable place and affordance IDs
- explicit non-goals
- selected slice boundary
- demo path
- executable-breadboard fixtures, example runs, expected outputs, edge cases, and acceptance tests, when present
- contract IDs and boundary names, when present
- field names, required/optional distinctions, enum values, nullability, units, and error cases, when specified
- statechart state and transition IDs with their source breadboard IDs, when present
- active Dumplink task group, dependency order, risk state, cuts, and acceptance checks, when present

## Required behavior
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
6. Do not invent missing field names, nullability, enum values, expected outputs, fixtures, edge cases, or error cases; flag them.

## Standard context card

Add a short context card near the top of important planning artifacts. This lets the artifact explain how it should be read.

---
artifact_type: executable-breadboard
project: example-project
status: selected
source_of_truth: true
feeds:
  - implementation
  - tests
  - reflection
---

# Context Card

## Use this when
The agent is implementing or testing the selected slice.

## Must preserve
- selected slice boundary
- demo path
- place and affordance IDs
- fixtures and example runs
- expected outputs
- acceptance tests
- explicit non-goals
- contract IDs and boundary details, when present

## Ignore unless asked
- rejected shapes
- early brainstorming
- unresolved nice-to-haves

## Stable ID convention

Use stable IDs for anything the agent may need to trace from planning into implementation.

For new artifacts, use the compact conventions from `AGENTS.md`:

- R1: User can recover from an incomplete plan.
- P1: Planning dashboard.
- U3: Continue selected slice.
- S2: Slice status.
- C1: Resume slice request/response.
- V1: Resume unfinished work.
- RUN1: Happy path for resuming a slice.
- E1: Missing saved slice state.

Preserve established legacy IDs rather than translating them only for style.

Avoid renaming IDs just to improve wording. If the meaning changes, create a new ID or add a short change note.

## Executable breadboards in context packets

Use an executable breadboard when the selected slice is ready to be handed to a coding agent or engineer.

Treat it as the source of truth for the buildable behavior of the selected slice: structure, fixtures, example runs, expected outputs, edge cases, acceptance tests, and open decisions.

Preserve:

- selected slice ID and boundary
- demo path
- relevant places, affordances, stores, states, rules, and wiring
- interface contracts embedded in the executable breadboard
- fixture names and starting data
- example runs
- expected user-visible results
- expected state changes and side effects
- edge cases
- acceptance tests
- verification target
- open decisions the agent must not invent

Do not expand beyond the selected slice. If implementation reality conflicts with the executable breadboard, surface the drift instead of silently changing the plan.

## Interface contracts in context packets

Use an interface contract when a selected slice crosses a meaningful boundary and field-level guessing would create rework.

Examples:

- UI -> backend
- frontend -> API
- service -> store
- agent -> tool
- import -> parser
- parser -> normalized object
- canvas object -> markdown artifact
- MCP server -> client
- app -> external integration

When present, an interface contract should be treated as the source of truth for boundary-level input/output details unless the user's latest instruction, selected slice, or executable breadboard says otherwise.

Preserve:

- contract IDs
- boundary names
- field names
- required vs optional distinctions
- enum values
- nullability
- units, such as cents instead of dollars
- branches and error cases
- open decisions

Do not invent missing details. If a field-level decision is missing, surface it as an open decision before coding.

## Artifact-specific feeding prompts

### Framing doc to agent

Use @planning/frame.md. First extract desired outcome, current struggle, constraints, non-goals, and open questions. Then tell me whether the requested implementation fits the frame. Do not edit code yet.

### Shaping doc to agent

Use @planning/shaping.md. Treat the selected shape as the current direction. Use rejected shapes only to understand tradeoffs, not as implementation instructions. Before coding, produce selected requirements, shape parts that must be preserved, known unknowns or spikes, build risks implied by the shape, and any mismatch between the requested task and the selected direction.

### Breadboard to agent

Use @planning/breadboard.md. Treat Places, Affordances, Stores, Wiring, and Interface contract candidates as the source of truth for structure. Before coding, identify files likely affected, code responsibilities implied by each affordance, risks where the existing code may not support the breadboard, first slice to implement, and boundary crossings where an interface contract would reduce guessing. Do not change the breadboard silently.

### Executable breadboard to agent

Use @planning/executable-breadboard.md. Treat it as the build handoff for the selected slice. Before coding, restate the slice boundary, list fixtures and example runs, identify interface contracts to preserve, list expected user-visible results, state changes, side effects, and acceptance tests, and flag missing decisions. Implement only the selected slice.

### Interface contract to agent

Use @planning/interface-contracts.md. Before coding, extract contract IDs, boundaries, input fields, output fields, required vs optional fields, enum values, nullable fields, branches and error cases, and open decisions. Then report which decisions are fully specified, which are missing, and which tests should prove the contract is satisfied. Do not invent missing field names, nullability, enum values, or error cases.

### Slice plan to agent

Use @planning/slices.md. Focus only on the selected slice. Before coding, restate slice boundary, demo path, Produces line, explicit exclusions, and verification target. Implement only this slice unless the user explicitly expands scope.

### Kickoff doc to agent

Use @planning/kickoff.md. Summarize the build appetite, selected slice, demo path, exclusions, and verification target. Then produce an implementation plan.

### Breadboard reflection to agent

Use @planning/breadboard-reflection.md plus the selected breadboard and executable breadboard if present. Compare implementation reality to the intended places, affordances, stores, wiring, interface contracts, example runs, acceptance tests, and slices. Return matches, drift, missing behavior, accidental behavior, planning artifacts that need repair, and implementation follow-ups.

## Chunking rules

When feeding large planning material to an agent:

1. Start with the Context Card.
2. Include only the artifact needed for the current phase.
3. Prefer selected sections over whole documents.
4. Keep raw notes out unless the task is discovery or reconstruction.
5. Use stable IDs so the agent can request missing sections by name.
6. If the artifact is long, ask the agent to summarize it into an implementation packet before coding.
7. Keep rejected alternatives available, but clearly mark them as rejected.
8. Keep non-goals close to the task so the agent does not expand scope.

## Authority order

When artifacts disagree, use this default authority order unless the user says otherwise:

1. the user's latest explicit instruction
2. selected slice or kickoff doc
3. executable breadboard, when present
4. selected interface contract, for boundary-level input/output details
5. selected Dumplink task group and sequence, for task-group scope and build order
6. selected breadboard
7. selected shaping direction
8. framing doc
9. raw notes and transcripts
10. rejected alternatives and brainstorming

A statechart is derived from the selected breadboard and never outranks it.

## Drift protocol

If implementation reality conflicts with the planning artifact, the agent should not silently patch around the plan.

Use this structure:

## Planning drift found

The selected artifact says:
- ...

The implementation reality is:
- ...

Options:
1. Update the code to match the artifact.
2. Update the artifact because the original assumption was wrong.
3. Split the slice and defer the conflicting part.

Recommended move:
- ...

## Anti-patterns

Avoid:

- pasting the full transcript and asking the agent to infer the plan
- mixing rejected alternatives with selected direction without labels
- asking for code before the agent has restated the slice boundary
- letting the agent rename IDs during implementation
- treating raw notes as more authoritative than selected artifacts
- coding from an ordinary breadboard when fixtures, example runs, expected outputs, or acceptance tests are needed
- inventing missing field names, enum values, nullability, fixtures, expected outputs, edge cases, or error cases
- treating plain-language interface contracts as permission to create production schemas during planning
- using `CLAUDE.md` as a dumping ground for project-specific details that should live in planning artifacts
