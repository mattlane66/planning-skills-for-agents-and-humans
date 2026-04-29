# Agent Instructions

Use this repo to turn fuzzy requests, messy transcripts, partial designs, and implementation discoveries into planning artifacts that humans and agents can build from.

These instructions are tool-neutral. They are intended for Claude Code, Cursor, Codex, and other agentic coding or writing environments.

## Default mode

Default to planning before implementation.

Do not write production code unless the user explicitly selects a slice to build or asks for implementation.

When planning, prefer:

- plain language
- tables
- lightweight pseudo-structures
- Mermaid diagrams when helpful
- stable IDs for requirements, places, affordances, stores, and slices

When implementing, preserve shaped intent and update planning artifacts if implementation discoveries change the plan.

## Canonical workflow

1. Frame the problem.
2. Shape requirements and alternatives.
3. Select a direction.
4. Breadboard places, affordances, stores, and wiring.
5. Slice into demoable increments.
6. Feed only the relevant planning context to the implementation agent.
7. Reflect against implementation and repair drift.

## Skill map

Use the repo skills as reusable instructions:

- `framing-doc/` — turn raw material into a frame with context, current approach/result, desired outcome, boundaries, and criteria.
- `shaping/` — define requirements/criteria, compare alternative shapes, run fit checks, and detail the selected direction.
- `breadboarding/` — map places, affordances, stores, wiring, diagrams, and demoable slices.
- `kickoff-doc/` — create a builder-facing reference after the team has converged.
- `breadboard-reflection/` — compare implementation to the breadboard and repair drift.
- `feed-planning-context/` — package planning artifacts into a compact context packet for implementation work.

## Authority order

When artifacts disagree, use this default authority order unless the user says otherwise:

1. the user’s latest explicit instruction
2. selected slice or kickoff doc
3. selected breadboard
4. selected shaping direction
5. framing doc
6. raw notes and transcripts
7. rejected alternatives and brainstorming

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
- current slice
- non-goals and exclusions
- verification target

Use `docs/agent-context-feeding.md` and `feed-planning-context/SKILL.md` for the detailed protocol.

## Stable IDs

Preserve IDs such as:

- `REQ-01`
- `P-01`
- `AFF-01`
- `STORE-01`
- `SLICE-01`

Do not rename stable IDs just to improve wording. If the meaning changes, create a planning update or new ID.

## Drift protocol

If implementation reality conflicts with the selected planning artifact, do not silently patch around the plan.

Return:

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

## Completion standard

Before declaring work complete, check:

- the task stayed within the selected mode
- active requirements are separated from mechanisms
- rejected alternatives stayed marked as rejected
- non-goals were preserved
- stable IDs were preserved
- planning artifacts were updated if implementation discoveries changed the plan
- implementation work, when present, maps back to requirement/affordance/store/slice IDs
