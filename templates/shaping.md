---
planning: true
shaping: true
artifact_type: shaping
status: draft
source_of_truth: true
feeds:
  - breadboard
  - context-packet
---

# [Project] — Shaping

# Context Card

## Use this when
An agent needs the selected direction, active requirements, fit checks, unknowns, and scope boundaries before detailing or implementation.

## Must preserve
- stable requirement IDs
- selected shape and rejected alternatives
- unknown flags
- non-goals and appetite

## Ignore unless asked
- rejected shapes as implementation instructions
- raw brainstorms

## Frame reference
- Frame artifact:
- Outcome:
- Non-goals:

## Requirements

| ID | Requirement | Status | Notes |
|---|---|---|---|
| R0 | ... | Core goal | ... |
| R1 | ... | Must-have | ... |

## Appetite
- Time budget:
- Team shape:
- Review point:
- Cut line:
- Accepted uncertainty:
- Must-resolve unknowns:

## Shapes

### CURRENT: [Existing baseline]

| Part | Mechanism | Flag |
|---|---|:---:|
| CURRENT1 | ... | |

### A: [Short title]

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | ... | |

### B: [Short title]

| Part | Mechanism | Flag |
|---|---|:---:|
| B1 | ... | |

## Fit check

| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | ... | Core goal | ✅ | ✅ | ✅ |
| R1 | ... | Must-have | ❌ | ✅ | ❌ |

## Reverse fit check

| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| B1 | ... | R1 | ✅ |

## Appetite fit

| Shape | Fits appetite? | Required cuts | Uncertainty / spike |
|---|:---:|---|---|
| A | ... | ... | ... |
| B | ... | ... | ... |

## Decision

Chosen direction:

Why:

Rejected directions:

## Unknowns / spikes

| ID | Question | Why it matters | Acceptance |
|---|---|---|---|
| SP1 | ... | ... | ... |

## Next move
- [ ] Breadboard selected shape
- [ ] Run spike
- [ ] Revise frame or requirements
