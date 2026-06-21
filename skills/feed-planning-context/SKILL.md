---
name: feed-planning-context
description: Prepare framing, shaping, breadboard, executable breadboard, kickoff, slice, interface contract, or reflection artifacts for agent implementation work without overloading context.
---

# Feed Planning Context

Use this skill when the user wants to give an agent a planning artifact and have it act on the artifact without losing the shaped intent.

This skill prepares context only. It does not implement code.

## Goal

Create a compact context packet from the provided planning artifacts so an agent can understand the current task, the authority of each artifact, the selected direction, the slice boundary, executable breadboard examples when present, interface contracts when present, and the verification target.

## Inputs

Use whichever artifacts the user provides or points to:

- framing doc
- shaping doc
- selected shape
- fit check
- reverse fit check
- breadboard
- executable breadboard
- interface contract sketch or plain-language interface contract
- slice plan
- kickoff doc
- breadboard reflection
- raw notes or transcripts, only when needed

## Default behavior

1. Identify the current task.
2. Identify the source artifacts and their authority.
3. Extract only the context needed for the next move.
4. Preserve stable IDs for requirements, places, affordances, stores, contracts, example runs, edge cases, and slices.
5. Preserve executable breadboard fixtures, example runs, expected outputs, state changes, side effects, edge cases, and acceptance tests when present.
6. Preserve field names, required/optional distinctions, enum values, nullability, and error cases when interface contracts are present.
7. Keep rejected alternatives and raw notes out of the active packet unless the user asks for discovery or reconstruction.
8. Name explicit non-goals and exclusions.
9. Add a verification target.
10. Stop after preparing the context packet.

## Output format

```md
# Context Packet

## Task
...

## Source artifacts
- ...

## Authority order
1. ...
2. ...
3. ...

## Use these sections first
- ...

## Do not use unless needed
- ...

## Must preserve
- ...

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

## Current slice
- Slice: ...
- Demo: ...
- Produces: ...
- Exclusions: ...

## Open questions
- ...

## Build-handoff behavior
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
6. Flag missing field names, nullability, enum values, error cases, fixtures, expected outputs, or acceptance tests instead of inventing them.

## Verification target
- ...
```

## Authority order

When artifacts disagree, use this default authority order unless the user says otherwise:

1. the user's latest explicit instruction
2. selected slice or kickoff doc
3. executable breadboard, when present
4. selected interface contract, for boundary-level input/output details
5. selected breadboard
6. selected shaping direction
7. framing doc
8. raw notes and transcripts
9. rejected alternatives and brainstorming

## Chunking rules

When artifacts are large:

1. Start with the Context Card or top summary.
2. Include only the artifact needed for the current phase.
3. Prefer selected sections over whole documents.
4. Keep raw notes out unless the task is discovery or reconstruction.
5. Use stable IDs so the agent can request missing sections by name.
6. If the artifact is long, summarize it into an implementation packet before coding.
7. Keep rejected alternatives available, but clearly mark them as rejected.
8. Keep non-goals close to the task so the agent does not expand scope.

## Stable ID handling

Preserve IDs such as:

- REQ-01
- P-01
- AFF-01
- STORE-01
- CONTRACT-01 or C1
- RUN-01
- EDGE-01
- SLICE-01

Do not rename IDs for style. If meaning changes, mark it as a planning update.

## Executable breadboard handling

When an executable breadboard is present, preserve:

- selected slice ID and boundary
- relevant places, affordances, stores, and wires
- fixtures or example starting data
- example runs
- expected user-visible results
- expected state changes
- expected side effects
- edge cases
- acceptance tests
- open decisions

The executable breadboard is the build-handoff artifact for a selected slice. It is more authoritative than the ordinary breadboard for the examples and expected results of that slice.

## Interface contract handling

When interface contracts are present, preserve:

- contract IDs
- boundary names
- field names
- required vs optional distinctions
- enum values
- nullability
- units, such as cents instead of dollars
- branches and error cases
- open decisions

If a field-level decision is missing, flag it. Do not invent it during context packaging.

## Drift handling

If implementation reality conflicts with a planning artifact, return:

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

## Do not

- implement code
- turn rejected alternatives into active requirements
- paste entire transcripts into the active context unless needed
- silently drop non-goals
- silently change the selected slice boundary
- silently change specified executable breadboard examples or interface contracts
- invent missing field names, enum values, nullability, error cases, fixtures, expected outputs, or acceptance tests
- rename stable IDs during packaging
- treat raw notes as more authoritative than selected artifacts
