---
planning: true
shaping: true
artifact_type: executable-breadboard
status: draft
source_of_truth: true
feeds:
  - context-packet
  - implementation
  - reflection
---

# [Project] — Executable Breadboard

# Context Card

## Use this when
An agent or engineer is ready to implement a selected slice and needs concrete examples, fixtures, expected outputs, and tests.

## Must preserve
- selected slice ID and boundary
- stable place, affordance, store, contract, and state IDs
- field names, required/optional distinctions, enum values, and nullability when specified
- example starting data
- expected outputs and visible consequences
- edge cases and acceptance tests
- open decisions the agent must not invent

## Ignore unless asked
- rejected shapes
- future slices
- production schemas
- framework-specific implementation details
- broad refactors outside the selected slice

## Source references
- Framing artifact:
- Shaping artifact:
- Breadboard artifact:
- Slice artifact:
- Interface contract artifact, if split out separately:

## Selected slice

| ID | Slice | Demo path | Produces | Explicit exclusions |
|---|---|---|---|---|
| SLICE-01 | ... | ... | ... | ... |

## Relevant breadboard structure

### Places

| ID | Place | Why it matters for this slice |
|---|---|---|
| P1 | ... | ... |

### UI affordances

| ID | Place | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|
| U1 | P1 | ... | ... | -> N1 | ... |

### Non-UI affordances

| ID | Place | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|
| N1 | P1 | ... | call | -> S1 | -> U1 |

### Stores and state

| ID | Store / State | Starting value | Expected change |
|---|---|---|---|
| S1 | ... | ... | ... |

## Rules for this slice

- ...

## Interface contracts

Use this section when the slice crosses a meaningful boundary: UI -> backend, frontend -> API, service -> store, agent -> tool, import -> parser, or external integration.

| ID | Trigger / Wire | From | To | Input shape | Output shape | Branches / errors | Open decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | ... | ... | ... | ... | ... | ... |

## Example starting data / fixtures

Describe concrete records, users, objects, stores, or external responses the implementation can use as test fixtures.

- user_1: ...
- record_1: ...
- starting state: ...

## Example runs

### Run 1 — Happy path

**Given**
- ...

**When**
- ...

**Then**
- ...

**Expected user-visible result**
- ...

**Expected state changes**
- ...

**Expected side effects**
- ...

### Run 2 — Edge case

**Given**
- ...

**When**
- ...

**Then**
- ...

## Edge cases

| Case | Starting condition | Action | Expected result | Test needed? |
|---|---|---|---|---|
| E1 | ... | ... | ... | yes/no |

## Acceptance tests

Write acceptance tests in plain language or Gherkin-style prose.

- Given ...
- When ...
- Then ...

## Verification target

This slice is complete when:

- [ ] ...
- [ ] ...
- [ ] ...

## Open decisions the agent must not invent

- ...

## Agent handoff prompt

Use this executable breadboard as the build contract for the selected slice.

Before writing code, restate the selected slice, list the fixtures or starting data, identify the interface contracts that must be preserved, identify edge cases and tests implied by the example runs, and flag any missing decisions you would otherwise have to invent.

Then implement only the selected slice.

Do not rename stable IDs, fields, states, enum values, or boundary names unless explicitly asked. If implementation reality conflicts with the executable breadboard, stop and propose a planning update.

## Self-check

- [ ] The selected slice is explicit.
- [ ] The example starting data is concrete enough to run mentally or in tests.
- [ ] Expected outputs are observable.
- [ ] State changes and side effects are named.
- [ ] Boundary-crossing data shapes are specified or flagged as open decisions.
- [ ] Edge cases are listed.
- [ ] Acceptance tests prove the slice works.
- [ ] Open decisions are flagged instead of invented.
