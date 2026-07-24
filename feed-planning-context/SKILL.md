---
name: feed-planning-context
description: Prepare a compact context packet when an implementation agent needs the authoritative planning subset, execution contract, non-goals, and verification target for one slice.
license: MIT
---

# Feed Planning Context

Use this skill when an implementation agent needs the exact authoritative context for one selected slice or active task group.

This skill packages context only. It does not implement code, change scope, or resolve missing product decisions.

## Goal

Create a compact context packet that tells the next agent:

- what task is active
- which artifacts govern it
- which project terms and decisions to preserve
- what behavior and boundaries matter
- what is out of scope
- when to return to planning
- what proves the task is complete

## Inputs

Use whichever authoritative sources exist:

- frame and shaping document
- Appetite card, when separate
- selected breadboard and slice
- relevant statechart rows
- interface contracts
- executable breadboard examples
- selected Dumplink task group
- kickoff document, for orientation only
- implementation evidence when the task is a correction

When working in an existing product repository, inspect the applicable `AGENTS.md`, `CONTEXT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, ADR or decision directories, existing tests, and public interfaces. Include only the terms and decisions relevant to the active task. Do not create or modify durable documentation without authorization.

## Authority order

Unless the user specifies otherwise:

1. user's latest explicit instruction
2. selected slice
3. executable breadboard, for expected examples and results within that slice
4. selected interface contract, for its named boundary
5. selected Dumplink task group, for grouping and sequence inside the slice
6. selected breadboard
7. selected shaping direction
8. kickoff document, for orientation only
9. frame
10. raw notes
11. rejected alternatives and brainstorming

A statechart is derived from the selected breadboard and never outranks it. No lower artifact may expand the selected slice.

## Procedure

1. Name the current task and selected slice.
2. List source artifacts and their concern-specific authority.
3. Extract only the sections required for the next move.
4. Preserve stable IDs and accepted Appetite, cut line, and non-goals.
5. Preserve canonical project language, relevant ADRs, and existing interfaces or seams.
6. Include relevant statechart rows, contracts, examples, edge cases, acceptance tests, or task-group details only when present and needed.
7. Exclude rejected alternatives, raw transcripts, pending visual deltas, and unrelated planning history.
8. Flag missing field-level, example-level, or terminology decisions instead of inventing them.
9. Add an execution contract.
10. Add a verification target.
11. Stop after writing the context packet.

## Output

Use `templates/context-packet.md`.

At minimum include:

```md
# Context Packet

## Task
- ...

## Source artifacts
- ...

## Authority order
1. ...

## Use these sections first
- ...

## Do not use unless needed
- ...

## Must preserve
- Accepted requirements:
- Appetite and cut line:
- Selected slice:
- Non-goals:

## Project language and decisions
- Canonical terms:
- Relevant architectural decisions:
- Existing interfaces or seams:
- Terms or decisions this work may introduce:

## Relevant behavior
- Places / affordances / stores:
- Statechart rows, when present:
- Contracts, when present:
- Fixtures, runs, edge cases, and acceptance tests, when present:
- Active task group and dependencies, when present:

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

## Verification target
- ...
```

## Project language rules

- Reuse terms already established by the product repository.
- Prefer existing public interfaces and test seams to newly invented ones.
- State when selected work intentionally changes an architectural seam.
- Keep proposed glossary or ADR changes separate from authorized changes.
- Do not let a compact summary rename concepts in ways that break traceability.

## Advanced artifact rules

When present, preserve only the relevant subset:

- statechart: source breadboard IDs, states, transitions, guards, effects, and explicit gaps
- interface contract: boundary, fields, optionality, enum values, nullability, units, branches, and errors
- executable breadboard: fixtures, example runs, expected visible results, state changes, side effects, edge cases, and tests
- Dumplink: active task group, dependencies, risk, cuts, acceptance checks, and stop condition

Do not activate deferred groups or fill missing details with guesses.

## Execution contract

The execution contract must name:

- the concrete goal condition
- checks required before completion
- files or areas the agent may touch
- out-of-scope changes
- conditions that return work to planning
- checkpoint expectations for multi-step work
- verification caveats that must be reported

## Return to planning when

- implementation would expand the selected slice
- required behavior is absent from accepted artifacts
- a field, enum, nullability, unit, error case, fixture, expected result, or acceptance test is missing
- project terminology or an architectural decision is materially ambiguous
- implementation evidence disproves a planning assumption
- the work no longer fits the accepted Appetite

## Completion criterion

The packet is complete when the next agent can act without loading the entire planning stack, can identify every governing source, can preserve the product repository's language and seams, and knows exactly when to stop and return to planning.
