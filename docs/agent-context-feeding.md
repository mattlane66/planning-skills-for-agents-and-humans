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

## Core rule

Feed the agent the smallest context packet that can support the next move.

A good context packet tells the agent:

1. what task it is doing now
2. which planning artifacts are source material
3. which sections matter first
4. which sections should be ignored unless needed
5. what constraints, IDs, and non-goals must be preserved
6. what verification target proves the work stayed aligned

## Context packet template

```md
# Context Packet

## Task
What the agent should do now.

## Source artifacts
- @planning/frame.md
- @planning/breadboard.md
- @planning/slices.md

## Use these sections first
- frame.md: Outcome, Constraints, Non-goals
- breadboard.md: Places, Affordances, Stores, Wiring
- slices.md: Selected slice, Demo, Produces

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

## Required behavior
1. Restate the relevant constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. If implementation reality changes the plan, propose a planning update instead of silently drifting.
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
  - implementation
---

# Context Card

## Use this when
The agent is implementing, slicing, or checking whether code still matches the planned interaction.

## Must preserve
- P1, P2, P3 place IDs
- selected affordance names
- user-visible demo path
- explicit non-goals

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
SLICE-01: Resume unfinished work.
```

Avoid renaming IDs just to improve wording. If the meaning changes, create a new ID or add a short change note.

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

Treat Places, Affordances, Stores, and Wiring as the source of truth.
Before coding, produce:
1. files likely affected
2. code responsibilities implied by each affordance
3. risks where the existing code may not support the breadboard
4. first slice to implement

Do not change the breadboard silently. If implementation reality changes it, propose a planning update.
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

Compare implementation reality to the intended places, affordances, stores, wiring, and slices.
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
3. selected breadboard
4. selected shaping direction
5. framing doc
6. raw notes and transcripts
7. rejected alternatives and brainstorming

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
- using `CLAUDE.md` as a dumping ground for project-specific details that should live in planning artifacts
