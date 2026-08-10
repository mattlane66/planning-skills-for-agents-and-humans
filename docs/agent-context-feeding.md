# Agent Context Feeding

Planning artifacts are most useful to agents when they are fed at the right fidelity. Do not paste the whole planning stack by default. Package the small amount of **accepted** context the agent needs for the current implementation phase, name the source artifacts, and preserve stable IDs so work can be traced back to planning.

Collaborative shaping deliberately creates Working R/S/fit/Appetite, spikes, candidate breadboards, sketches, and prototypes. Those are useful during shaping but are not active build scope unless an accepted decision explicitly promotes their implications.

When a sketch-reconciliation record exists, feed accepted changes only after they have been written into the authoritative frame, shaping, breadboard, or slice artifacts. Keep pending, rejected, ambiguous, and Working deltas out of the build contract.

## Why this exists

The skills in this repo produce human-readable planning artifacts. Agent context feeding turns accepted portions of those artifacts into machine-usable working context without flattening them into generic instructions.

The goal is to prevent common agent failures:

- treating Working brainstorms or candidate shapes as selected direction
- treating candidate breadboards as build scope
- losing non-goals and constraints
- implementing mechanisms that no longer fit accepted requirements or Appetite
- changing the breadboard silently when code reality pushes back
- treating raw notes, Working R, selected requirements, and build instructions as equal authority
- inventing interface details such as field names, nullability, enum values, or error cases
- coding from an ordinary breadboard when an executable breadboard is needed

## Core rule

Feed the agent the smallest **authoritative** context packet that can support the next move.

A good context packet tells the agent:

1. what task it is doing now
2. which accepted artifacts govern the work and how conflicts are resolved
3. which selected sections matter first
4. which Working/exploratory sections must be ignored unless needed for a named unresolved decision
5. what constraints, IDs, Accepted Appetite, cut line, and non-goals must be preserved
6. which slice is current and which executable breadboard or interface contracts must be preserved, when present
7. what execution contract governs the build loop
8. what verification target proves the work stayed aligned

## Artifact roles

Working shaping material = provisional R/S/Appetite/fit and exploratory evidence used to make decisions. It is not build scope.

Candidate-shape breadboard = exploratory behavioral evidence about one unselected candidate. It is not build scope even when its candidate is later selected; surviving rows must be reconciled into selected-design intent.

Selected-design breadboard = accepted structure and behavior after explicit selection and reconciliation.

Statechart = optional derived behavioral view of a selected stateful portion of the selected-design breadboard.

Interface contract = what crosses a selected boundary.

Executable breadboard = selected structure plus fixtures, example runs, expected outputs, edge cases, and tests.

Dumplink = decomposition of a selected project into vertical task groups with risk/dependency sequence and scope cuts; a human-selected group becomes the active implementation slice.

Context packet = the exact accepted subset handed to the build agent.

## Context packet template

Use [`templates/context-packet.md`](../templates/context-packet.md) as the canonical copyable template. Its required structure is summarized here:

```md
# Context Packet

## Task
What the next implementation move should do.

## Source artifacts
- Only the relevant accepted shaping decision, selected-design breadboard, slice, contract, executable-breadboard, Dumplink, kickoff, or accepted reconciliation artifacts.

## Authority order
1. User's latest explicit instruction
2. Selected project boundary
3. Selected Dumplink task group or other selected slice, for active implementation scope
4. Executable breadboard, when present
5. Selected interface contract, for boundary-level details
6. Accepted selected-design breadboard
7. Accepted shaping decisions: selected direction, Accepted requirements, Accepted Appetite, cuts
8. Kickoff doc, for builder orientation only
9. Accepted frame / problem boundary
10. Working shaping material, candidate evidence, raw notes, transcripts, rejected alternatives — discovery context only, never active build scope

## Use these sections first
- ...

## Do not use as build scope
- Working requirements or Appetite
- candidate shapes or Working fit checks
- candidate-shape breadboards and exploratory prototypes
- rejected shapes
- raw notes
- unaccepted reconciliation deltas

## Must preserve
- stable IDs
- Accepted requirements
- Accepted Appetite and cut line
- explicit non-goals
- selected project boundary
- active task-group or slice boundary
- demo path
- relevant contracts, examples, or statechart rows

## Selected requirements
- ...

## Relevant selected-design places / affordances / stores
- ...

## Relevant statechart
- ...

## Relevant executable breadboard
- ...

## Relevant interface contracts
- ...

## Relevant Dumplink plan
- ...

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
1. Restate accepted constraints.
2. Identify implementation implications.
3. Ask at most 3 blocking questions.
4. Propose a plan before editing code.
5. Propose a planning update instead of silently drifting.
6. Flag missing contract or executable-example details instead of inventing them.
7. Run the required checks and report incomplete verification directly.

## Verification target
- ...
```

## Standard context card

Add a short context card near the top of important planning artifacts. This lets the artifact explain how it should be read.

```yaml
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
```

### Must preserve

- selected slice boundary
- demo path
- place and affordance IDs
- fixtures and example runs
- expected outputs
- acceptance tests
- explicit non-goals
- contract IDs and boundary details, when present

### Ignore unless asked

- Working R/S/Appetite/fit
- candidate breadboards and exploratory prototypes
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

Preserve established legacy IDs rather than translating them only for style. Avoid renaming IDs merely to improve wording. If the meaning changes materially, create a new ID or explicit planning delta.

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

Preserve contract IDs, boundary names, field names, required/optional distinctions, enum values, nullability, units, branches/errors, and open decisions. Do not invent missing details.

## Artifact-specific feeding prompts

### Shaping doc to agent

Use `@planning/shaping.md`. Extract only **Accepted** requirements, Accepted Appetite/cut line, the explicitly selected shape, cuts, non-goals, and accepted remaining uncertainty. Treat Working R/S/fit and candidate evidence as historical/discovery context unless a named unresolved decision requires them. Do not implement from a candidate shape merely because it appears first or is more detailed.

### Selected-design breadboard to agent

Use `@planning/breadboard.md`. Confirm `mode: selected-design` and acceptance. Treat Places, Affordances, Stores, Wiring, and selected boundary candidates as the source of truth for structure. Do not substitute an earlier `candidate-shape` artifact.

### Executable breadboard to agent

Use `@planning/executable-breadboard.md`. Treat it as the build handoff for the selected slice. Before coding, restate the slice boundary, list fixtures and example runs, identify interface contracts to preserve, list expected results/state changes/side effects, and flag missing decisions. Implement only the selected slice.

### Interface contract to agent

Use `@planning/interface-contracts.md`. Extract contract IDs, boundaries, fields, required/optional distinctions, enum values, nullability, branches/errors, and open decisions. Do not invent missing details.

### Slice plan to agent

Use `@planning/slices.md`. Focus only on the human-selected slice. Restate boundary, demo path, Produces line, exclusions, and verification target before coding.

### Kickoff doc to agent

Use `@planning/kickoff.md` for builder orientation. Resolve scope and sequence against higher-authority accepted build artifacts. A kickoff document is not build scope or task order.

### Breadboard reflection to agent

Use `@planning/breadboard-reflection.md` plus the accepted selected-design/executable breadboard. Record current implementation reality without overwriting accepted intent. Return matches, drift, missing behavior, accidental behavior, correction options, and the explicit decision needed before either truth changes.

## Chunking rules

When feeding large planning material to an agent:

1. Start with the Context Card.
2. Include only the accepted artifact sections needed for the current phase.
3. Prefer selected sections over whole documents.
4. Keep raw notes and Working shaping material out unless the task is discovery or reconstruction.
5. Use stable IDs so the agent can request missing sections by name.
6. If the artifact is long, ask the agent to summarize it into an implementation packet before coding.
7. Keep rejected/candidate alternatives available only when needed for rationale, clearly labeled as non-authoritative.
8. Keep non-goals close to the task so the agent does not expand scope.

## Authority order

When artifacts disagree, use this default authority order unless the user says otherwise:

1. user's latest explicit instruction
2. selected project boundary
3. selected Dumplink task group or other selected slice
4. executable breadboard
5. selected interface contract for its named boundary
6. accepted selected-design breadboard
7. accepted shaping decisions: selected direction, Accepted R, Accepted Appetite, cuts
8. kickoff document for orientation only
9. accepted frame / problem boundary
10. Working shaping material and candidate evidence for discovery only
11. raw notes, transcripts, rejected alternatives, brainstorming

A statechart is derived from the selected-design breadboard and never outranks it.

## Drift protocol

If implementation reality conflicts with accepted planning, the agent should not silently patch around the plan.

```md
## Planning drift found

The selected artifact says:
- ...

The implementation reality is:
- ...

Options:
1. Update the code to match the artifact.
2. Update the artifact because the original assumption was wrong.
3. Split/cut the slice.
4. Create a new bet.

Recommended move:
- ...
```

## Anti-patterns

Avoid:

- pasting the full transcript and asking the agent to infer the plan
- feeding Working R/S/fit/Appetite as selected truth
- mixing candidate/rejected alternatives with selected direction without authority labels
- treating a candidate breadboard as selected-design intent or build scope
- asking for code before the agent has restated the selected slice boundary
- letting the agent rename IDs during implementation
- coding from an ordinary breadboard when fixtures/examples/tests are needed
- inventing missing fields, enum values, nullability, fixtures, expected outputs, edge cases, or error cases
- allowing implementation reality to silently rewrite accepted intent
