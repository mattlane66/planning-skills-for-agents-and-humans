# Agent Instructions

Use this repo to turn fuzzy requests, messy transcripts, partial designs, and implementation discoveries into planning artifacts that humans and agents can build from.

These instructions are tool-neutral. They are intended for Claude Code, Cursor, Codex, Gemini CLI, and other agentic coding or writing environments.

## Default mode

Default to planning before implementation.

Do not write production code unless the user explicitly selects a slice to build or asks for implementation.

When planning, prefer:

- plain language
- tables
- lightweight pseudo-structures
- Mermaid diagrams when helpful
- stable IDs for requirements, places, affordances, stores, contracts, states, transitions, example runs, edge cases, task groups, and slices

When implementing, preserve shaped intent and update planning artifacts if implementation discoveries change the plan.

## Orchestration manifest

Use `.agent-orchestration.yaml` as the machine-readable workflow and harness contract.

It defines:

- modes
- required source artifacts
- allowed outputs
- forbidden moves
- human decision gates
- command aliases
- artifact templates
- optional lifecycle hooks

If `AGENTS.md` and `.agent-orchestration.yaml` disagree, prefer the more specific instruction for the active mode. If the conflict changes product scope or implementation behavior, stop and ask for a planning update.

## Canonical workflow

1. Frame the problem.
2. Shape requirements and alternatives.
3. Select a direction.
4. Breadboard places, affordances, stores, and wiring.
5. Optionally derive a statechart for a selected stateful scope when the wiring alone is hard to reason about.
6. Slice into demoable increments.
7. Add plain-language interface contracts when the selected slice crosses meaningful boundaries.
8. Create an executable breadboard when the selected slice is ready for build handoff and needs examples, fixtures, expected outputs, edge cases, or tests.
9. Use Dumplink when the selected work needs vertical task groups, risk states, dependencies, sequencing, or appetite-based cuts.
10. Feed only the relevant planning context to the implementation agent.
11. Check for drift during implementation.
12. Reflect against implementation and repair drift.

The statechart step is optional. It is a derived view of the accepted breadboard, not a new source of truth or a prerequisite for slicing.

## Shaping gates

The broad shaping step can be run all at once, but agents should not collapse it into an automatic decision when the user wants deliberation.

When finer control is useful, split shaping into these gates:

1. Criteria — define the requirements / criteria before proposing mechanisms.
2. Shape sketches — make multiple possible directions visible without selecting one.
3. Fit check — compare shapes against criteria and check whether each mechanism is justified.
4. Shape selection — record the human choice or stop with a decision-ready summary.
5. Breadboard handoff — only breadboard after the selected shape is explicit.

Do not one-shot from fuzzy request to selected shape when the user asks for a fit check, sketches, alternatives, or gate-by-gate shaping.

## Skill map

Use the repo skills as reusable instructions:

- `framing-doc/` — turn raw material into a frame with context, current approach/result, desired outcome, boundaries, and criteria.
- `shaping/` — define requirements/criteria, compare alternative shapes, run fit checks, and detail the selected direction.
- `breadboarding/` — map places, affordances, stores, wiring, diagrams, and demoable slices.
- `statechart/` — turn a selected stateful portion of an accepted breadboard into a transition table and Mermaid statechart while surfacing missing behavior.
- `interface-contracts/` — turn selected breadboard wires or slices into plain-language contracts for boundary-crossing data exchanges.
- `executable-breadboards/` — turn a selected slice into a buildable, testable handoff with examples, fixtures, expected outputs, edge cases, and acceptance tests.
- `dumplink/` — turn a shaped project into vertical task groups, risk states, dependencies, scope cuts, acceptance checks, and a bounded agent handoff.
- `kickoff-doc/` — create a builder-facing reference after the team has converged.
- `breadboard-reflection/` — compare implementation to the breadboard and repair drift.
- `feed-planning-context/` — package planning artifacts into a compact context packet for implementation work.

## Artifact taxonomy

Breadboard = structure of the solution.

Statechart = optional derived behavioral view of a selected stateful portion of the breadboard.

Interface contract = what crosses a boundary.

Executable breadboard = breadboard + interface contracts + fixtures + example runs + expected outputs + tests.

Dumplink = vertical task grouping + risk/dependency sequencing + scope cuts for a selected shaped project.

Context packet = the exact subset handed to the build agent.

Execution contract = the goal condition, required checks, allowed files, out-of-scope changes, return-to-planning conditions, checkpoint cadence, and verification caveats inside a context packet.

Drift check = a point-in-time alignment check during implementation.

Agent run log = a lightweight audit trail of a meaningful agent run.

## Authority order

When artifacts disagree, use this default authority order unless the user says otherwise:

1. the user’s latest explicit instruction
2. selected slice or kickoff doc
3. executable breadboard, when present
4. selected interface contract, for boundary-level input/output details
5. selected Dumplink task group and sequence, for task-group scope and build order
6. selected breadboard
7. selected shaping direction
8. framing doc
9. raw notes and transcripts
10. rejected alternatives and brainstorming

A statechart is derived from the selected breadboard and never outranks it. If they disagree, update the breadboard first and regenerate the statechart.

Do not treat a newer brainstorming note as a higher-authority artifact unless it explicitly changes the selected direction.

## Mode discipline

Planning artifacts should preserve latitude. Avoid prematurely turning requirements into mechanisms.

Requirements and criteria describe what must be true. Mechanisms describe one way to make it true.

Do not collapse:

- problems into solutions
- requirements into UI choices
- selected shapes into implementation details
- rejected alternatives into active requirements
- raw notes into source-of-truth instructions
- Dumplink task groups into disconnected horizontal tickets

During planning, keep interface contracts and executable breadboards in plain language. Do not create full OpenAPI, JSON Schema, database schema, framework code, production contract files, production test files, or mocks unless the user explicitly asks or the selected slice has moved into implementation preparation.

## Context feeding

Do not paste or load the whole planning stack by default.

Before implementation work, create or request a compact context packet that includes:

- current task
- source artifacts
- authority order
- sections to use first
- sections to ignore unless needed
- must-preserve constraints
- selected requirements
- relevant places, affordances, stores, and wiring
- relevant statechart rows when a statechart exists and the task depends on that behavior
- relevant executable breadboard examples, when present
- relevant interface contracts, when present
- relevant Dumplink task group, dependencies, cuts, and acceptance checks, when present
- current slice
- non-goals and exclusions
- execution contract
- verification target

Use `docs/agent-context-feeding.md` and `feed-planning-context/SKILL.md` for the detailed protocol.

## Drift checks and loops

During implementation or refactoring, use a drift check when there is risk that the agent has moved away from the selected planning artifacts.

A drift check must return only one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

Do not implement inside a drift check. Do not update planning artifacts silently. If implementation reality conflicts with the plan, recommend a planning update, contract update, executable breadboard update, Dumplink sequence update, or slice split before continuing.

Use `docs/loop-prompting.md`, `templates/drift-check.md`, and `/check-drift` where supported.

## Agent run logs

Create an agent run log after meaningful agent runs that change implementation files, planning artifacts, or durable decisions.

Use `templates/agent-run-log.md` and `docs/agent-run-records.md`.

A run log should not replace source-of-truth planning artifacts. If the run discovers a planning issue, update or request an update to the relevant artifact.

## Lifecycle hooks

Optional lifecycle hooks live in `hooks/` and are documented in `docs/lifecycle-hooks.md`.

Use hooks as reminders and guardrails only. They should not become a hidden planning method or implementation harness.

## Stable IDs

Preserve IDs such as:

- `REQ-01`
- `P-01`
- `AFF-01`
- `STORE-01`
- `ST-01`
- `TR-01`
- `CONTRACT-01` or `C1`
- `RUN-01`
- `EDGE-01`
- `T1`
- `TG1`
- `CUT-01`
- `SLICE-01`

Do not rename stable IDs just to improve wording. If the meaning changes, create a planning update or new ID.

## Statecharts

Use a statechart only for a selected scope or slice whose behavior is difficult to understand from breadboard wiring alone.

Preserve:

- source breadboard IDs for every state and transition
- the selected scope boundary
- events and trigger types
- guards
- product-relevant effects
- destination states
- explicit gaps and assumptions

Do not invent retry, cancellation, timeout, failure, hierarchy, or parallel behavior. Mark unsupported interpretations as inferred or missing and recommend a breadboard update.

The state-transition table is the primary statechart output. Mermaid is a visual projection of that table.

## Executable breadboards

When an executable breadboard is present, preserve:

- selected slice ID and boundary
- relevant breadboard structure
- interface contracts
- example starting data or fixtures
- example runs
- expected user-visible results
- expected state changes
- expected side effects
- edge cases
- acceptance tests
- open decisions

Do not invent missing fixtures, expected outputs, edge cases, or acceptance tests. Flag them before coding.

## Interface contracts

When an interface contract is present, preserve:

- contract IDs
- boundary names
- field names
- required vs optional distinctions
- enum values
- nullability
- units, such as cents instead of dollars
- branches and error cases
- open decisions

Do not invent missing field names, nullability, enum values, or error cases. Flag them before coding.

## Dumplink plans

When a Dumplink plan is present, preserve:

- task IDs
- task group IDs
- risk states
- dependency links
- build sequence
- scope cuts
- acceptance checks
- active task group boundary
- stop condition
