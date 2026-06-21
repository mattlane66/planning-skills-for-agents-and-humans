# Executable Breadboards

An ordinary breadboard is a thinking artifact.

An executable breadboard is a building artifact.

The ordinary breadboard explains how the feature should work. The executable breadboard turns the selected slice into something a coding agent and engineer can build, test, and verify.

## Difference

| | Breadboard | Executable breadboard |
|---|---|---|
| Purpose | Explain how the feature should work | Make the feature buildable and testable |
| Main audience | Product, design, engineering humans | Coding agent and engineer |
| Contains | Places, affordances, stores, states, rules, branches, connections | Same, plus examples, fixtures, interface contracts, expected outputs, edge cases, and tests |
| Verification | Does this make sense? | Can we prove this works? |
| Failure mode | Still too interpretive | More upfront work, much less ambiguity |
| Best for | Shaping the solution | Getting an agent to implement correctly |

## Where this fits

```text
Framing
  -> Shaping
  -> Breadboard
  -> Slice selection
  -> Executable breadboard, when ready to build
  -> Feed planning context
  -> Build agent
  -> Reflect
```

The breadboard says what exists.

The slice says what is being built now.

The interface contract says what crosses a boundary.

The executable breadboard says what should happen with real input, what output should result, and what tests prove it.

The context packet tells the agent which subset to use now.

## Relationship to interface contracts

An interface contract is field-level boundary detail.

An executable breadboard is the selected slice made runnable in plain language.

Interface contracts can live in three places:

1. embedded as candidates inside an ordinary breadboard
2. split into a separate interface-contract artifact when boundary detail is complex
3. included inside an executable breadboard when preparing a build handoff

Do not treat every interface contract as a full executable breadboard. A contract only says what moves across a boundary. An executable breadboard also includes fixtures, example runs, expected results, edge cases, and acceptance tests.

## When to use each

Use an ordinary breadboard when you are still shaping:

- What are the parts?
- What does the system need to do?
- What states and rules exist?
- What wires connect the parts?
- What slices might be demoable?

Use an executable breadboard when you are ready to build:

- What should happen with real input?
- What output should result?
- What should the UI display?
- What state should change?
- What logs, events, or side effects should exist?
- What edge cases must pass?
- What tests prove the selected slice works?

## What to include

An executable breadboard should include:

1. selected slice
2. relevant places, affordances, stores, and wires
3. interface contracts for meaningful boundaries
4. example starting data or fixtures
5. example runs
6. expected outputs and visible consequences
7. edge cases
8. acceptance tests
9. open decisions the agent must not invent

## Example

### Ordinary breadboard

```md
Objects:
- User
- Argument
- Objection
- Evidence

Actions:
- User creates an argument
- User adds an objection
- User attaches evidence

States:
- Draft
- Published
- Contested
- Resolved

Rules:
- Published arguments are visible publicly
- Objections must attach to a specific claim
- Evidence can support or weaken a claim
```

This explains the system shape, but it still leaves the implementation agent guessing about data, outputs, edge cases, and verification.

### Executable breadboard

```md
# Executable Breadboard

## Selected slice

SLICE-01: Add an objection to a published argument.

## Relevant objects

- User
- Argument
- Claim
- Objection
- Activity log entry

## Example starting data

User:
  id: user_1
  name: Matt

Argument:
  id: arg_1
  status: published
  thesis: AI agents need executable product specs.

Claim:
  id: claim_1
  argument_id: arg_1
  text: Breadboards reduce ambiguity before coding.

## Action

User adds objection:
  claim_id: claim_1
  text: This creates too much upfront overhead.

## Expected result

- New objection is created.
- Argument status changes from published to contested.
- Objection appears under the relevant claim.
- Activity log records the change.

## Acceptance test

Given a published argument with one claim
When the user adds an objection to that claim
Then the objection should appear under that claim
And the argument status should become contested
And the activity log should include Objection added
```

This gives the implementation agent a runnable scenario in plain language.

## Agent handoff prompt

```text
Use this executable breadboard as the build contract for the selected slice.

Before writing code:
1. restate the selected slice
2. list the fixtures or starting data you will use
3. identify the interface contracts that must be preserved
4. identify edge cases and tests implied by the example runs
5. flag any missing decisions you would otherwise have to invent

Then implement only the selected slice.

Do not rename stable IDs, fields, states, enum values, or boundary names unless explicitly asked. If implementation reality conflicts with the executable breadboard, stop and propose a planning update.
```

## Planning-mode rule

Do not create executable breadboards for every idea during early shaping. They are heavier artifacts for moments when a selected slice is close to implementation.

During planning, keep executable breadboards in plain language. Do not create production code, full schemas, test files, or framework-specific artifacts unless the user explicitly asks or the slice has moved into implementation.

## Quality check

A good executable breadboard should let a builder answer:

- What slice are we building?
- What starting data exists?
- What action happens?
- What crosses each important boundary?
- What state changes?
- What should the user see?
- What edge cases matter?
- What test proves the slice works?
- Which decisions remain open?
