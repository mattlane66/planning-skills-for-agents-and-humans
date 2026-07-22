---
name: executable-breadboards
description: Turn a selected slice into fixtures, example runs, expected outputs, edge cases, and acceptance tests when it is ready for a buildable behavioral handoff.
---

# Executable Breadboards

Use this skill when the user has a selected slice and wants to hand it to a coding agent or engineer with much less ambiguity.

An ordinary breadboard is a thinking artifact.

An executable breadboard is a building artifact.

This skill prepares the build handoff. It does not implement code.

## Goal

Turn the selected slice of a breadboard into a plain-language build contract with:

- relevant structure
- interface contracts
- example starting data
- example runs
- expected outputs
- edge cases
- acceptance tests
- open decisions the agent must not invent

## Use this when

Use this after a breadboard and slice selection when the next move is implementation preparation.

Good signals:

- the slice is selected
- the demo path is known
- field-level guessing would cause rework
- the agent needs fixtures or examples to test against
- the UI, state, or side effects need concrete expected results
- multiple agents or layers must stay aligned

Do not use this during early shaping when the team is still deciding what the feature should be.

## Inputs

Use whichever artifacts are available:

- frame
- shaping doc
- selected breadboard
- selected slice
- interface contract candidates or separate interface contracts
- known UI expectations
- known data examples
- known branches or edge cases
- implementation constraints

## Default behavior

1. Identify the selected slice.
2. Pull only the breadboard places, affordances, stores, wires, states, and rules needed for that slice.
3. Include interface contracts for meaningful boundary crossings.
4. Create concrete example starting data or fixtures.
5. Write one happy-path example run.
6. Write important edge-case runs.
7. Name expected user-visible results, state changes, and side effects.
8. Write acceptance tests in plain language or Gherkin-style prose.
9. Flag open decisions instead of inventing them.
10. Stop after producing the executable breadboard.

## Output format

# [Project] — Executable Breadboard

## Source references
- Breadboard artifact:
- Selected slice:
- Interface contract artifact, if split out separately:

## Selected slice

| ID | Slice | Demo path | Produces | Explicit exclusions |
|---|---|---|---|---|
| SLICE-01 | ... | ... | ... | ... |

## Relevant breadboard structure

### Places
- ...

### Affordances
- ...

### Stores and state
- ...

### Rules
- ...

## Interface contracts

| ID | Trigger / Wire | From | To | Input shape | Output shape | Branches / errors | Open decisions |
|---|---|---|---|---|---|---|---|
| C1 | ... | ... | ... | ... | ... | ... | ... |

## Example starting data / fixtures
- ...

## Example runs

### Run 1 — Happy path

Given:
- ...

When:
- ...

Then:
- ...

Expected user-visible result:
- ...

Expected state changes:
- ...

Expected side effects:
- ...

## Edge cases

| Case | Starting condition | Action | Expected result | Test needed? |
|---|---|---|---|---|
| E1 | ... | ... | ... | yes/no |

## Acceptance tests

- Given ...
- When ...
- Then ...

## Open decisions the agent must not invent
- ...

## Verification target
- ...

## Relationship to other artifacts

Breadboard = structure of the solution.

Interface contract = what crosses a boundary.

Executable breadboard = structure plus examples, fixtures, expected outputs, edge cases, and tests.

Context packet = the exact subset handed to the build agent.

## Acceptance test guidance

Acceptance tests should prove behavior, not implementation style.

Prefer:

- Given a published argument with one claim
- When the user adds an objection to that claim
- Then the objection appears under that claim
- And the argument status becomes contested
- And the activity log includes Objection added

Avoid:

- naming internal functions unless the user already selected them
- over-specifying database tables during planning
- asserting framework-specific mechanisms too early

## Agent handoff guidance

When an implementation agent receives an executable breadboard, it should:

1. restate the selected slice
2. list the fixtures or starting data it will use
3. identify the interface contracts that must be preserved
4. identify tests implied by the example runs
5. flag missing decisions before coding
6. implement only the selected slice
7. stop and propose a planning update if implementation reality conflicts with the artifact

## Do not

- convert every ordinary breadboard into an executable breadboard automatically
- create production schemas or test files during planning unless explicitly asked
- invent missing field names, enum values, nullability, edge cases, or expected outputs
- expand beyond the selected slice
- treat the executable breadboard as more authoritative than the user's latest explicit instruction
