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

## Core rule

Feed the agent the smallest context packet that can support the next move.

A good context packet tells the agent:

1. what task it is doing now
2. which planning artifacts are source material
3. which sections matter first
4. which sections should be ignored unless needed
5. what constraints, IDs, and non-goals must be preserved
6. which interface contracts must be preserved, when present
7. what verification target proves the work stayed aligned

## Context packet template

```md
# Context Packet

## Task
What the agent should do now.

## Source artifacts
- @planning/frame.md
- @planning/breadboard.md
- @planning/slices.md
- @planning/interface-contracts.md, when boundary detail matters

## Use these sections first
- frame.md: Outcome, Constraints, Non-goals
- breadboard.md: Places, Affordances, Stores, Wiring, Interface contract candidates
- slices.md: Selected slice, Demo, Produces
- interface-contracts.md: Contract IDs, boundaries, input shapes, output shapes, branches, errors, open decisions

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
- contract IDs and boundary names, when present
- field names, required/optional distinctions, enum values, nullability, and error cases, when specified

## Required behavior
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
6. Do not invent missing field names, nullability, enum values, or error cases; flag them.
```

## Standard context card

Add a short context card near the top of important planning artifacts. This lets the artifact explain how it should be read.

```md
---
artifact_type: breadboard
project: example-project
status: selected
source_of_truth: true
feeds:
  - slice-plan
  - interface-contracts
  - implementation
---

# Context Card

## Use this when
The agent is implementing, slicing, creating interface contracts, or checking whether code still matches the planned interaction.

## Must preserve
- P1, P2, P3 place IDs
- selected affordance names
- user-visible demo path
- explicit non-goals
- contract IDs and boundary details, when present

## Ignore unless asked
- rejected shapes
- early brainstorming
- unresolved nice-to-haves
```

## Stable ID convention

Use stable IDs for anything the agent may need to trace from planning into implementation.

```md
REQ-01: User can recover from an incomplete plan.
P-01: Planning dashboard.
AFF-03: Continue selected slice.
STORE-02: Slice status.
CONTRACT-01: Resume slice request/response.
SLICE-01: Resume unfinished work.
```

Avoid renaming IDs just to improve wording. If the meaning changes, create a new ID or add a short change note.

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

When present, an interface contract should be treated as the source of truth for boundary-level input/output details unless the user's latest instruction or selected slice says otherwise.

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

```md
Use @planning/frame.md.

First extract:
1. desired outcome
2. current struggle
3. constraints
4. non-goals
5. open questions

Then tell me whether the requested implementation fits the frame.
Do not edit code yet.
```

### Shaping doc to agent

```md
Use @planning/shaping.md.

Treat the selected shape as the current direction.
Use rejected shapes only to understand tradeoffs, not as implementation instructions.

Before coding, produce:
1. selected requirements
2. shape parts that must be preserved
3. known unknowns or spikes
4. build risks implied by the shape
5. any mismatch between the requested task and the selected direction
```

### Breadboard to agent

```md
Use @planning/breadboard.md.

Treat Places, Affordances, Stores, Wiring, and Interface contract candidates as the source of truth.
Before coding, produce:
1. files likely affected
2. code responsibilities implied by each affordance
3. risks where the existing code may not support the breadboard
4. first slice to implement
5. boundary crossings where an interface contract would reduce guessing

Do not change the breadboard silently. If implementation reality changes it, propose a planning update.
```

### Interface contract to agent

```md
Use @planning/interface-contracts.md.

Before coding, extract:
1. contract IDs
2. boundaries
3. input fields
4. output fields
5. required vs optional fields
6. enum values
7. nullable fields
8. branches and error cases
9. open decisions

Then report:
- which decisions are fully specified
- which decisions are still missing
- which tests should prove the contract is satisfied

Do not invent missing field names, nullability, enum values, or error cases. Flag them.
```

### Slice plan to agent

```md
Use @planning/slices.md.

Focus only on the selected slice.
Before coding, restate:
1. slice boundary
2. demo path
3. Produces line
4. explicit exclusions
5. verification target

Implement only this slice unless I explicitly expand scope.
```

### Kickoff doc to agent

```md
Use @planning/kickoff.md.

Summarize the build appetite, selected slice, demo path, exclusions, and verification target.
Then produce an implementation plan.
Only code after the plan is accepted.
```

### Breadboard reflection to agent

```md
Use @planning/breadboard-reflection.md and @planning/breadboard.md.

Compare implementation reality to the intended places, affordances, stores, wiring, interface contracts, and slices.
Return:
1. matches
2. drift
3. missing behavior
4. accidental behavior
5. planning artifacts that need repair
6. implementation follow-ups
```

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

1. the user’s latest explicit instruction
2. selected slice or kickoff doc
3. selected interface contract, for boundary-level input/output details
4. selected breadboard
5. selected shaping direction
6. framing doc
7. raw notes and transcripts
8. rejected alternatives and brainstorming

## Drift protocol

If implementation reality conflicts with the planning artifact, the agent should not silently patch around the plan.

```md
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
```

## Anti-patterns

Avoid:

- pasting the full transcript and asking the agent to infer the plan
- mixing rejected alternatives with selected direction without labels
- asking for code before the agent has restated the slice boundary
- letting the agent rename IDs during implementation
- treating raw notes as more authoritative than selected artifacts
- inventing missing field names, enum values, nullability, or error cases
- treating plain-language interface contracts as permission to create production schemas during planning
- using `CLAUDE.md` as a dumping ground for project-specific details that should live in planning artifacts
