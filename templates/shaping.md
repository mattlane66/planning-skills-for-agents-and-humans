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
An agent is comparing directions or checking whether a proposed mechanism satisfies the selected requirements.

## Must preserve
- requirement IDs
- selected shape
- rejected alternatives as rejected
- flagged unknowns
- non-goals from the frame

## Ignore unless asked
- raw brainstorms not promoted into requirements or shape parts

## Frame source

- Frame: `@planning/frame.md`
- Outcome: ...
- Non-goals: ...

## Requirements

| ID | Requirement | Status | Notes |
|---|---|---|---|
| R0 | ... | Core goal | ... |
| R1 | ... | Must-have | ... |

## Shapes

### CURRENT: [Existing system baseline]

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

## Fit Check

| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | ... | Core goal | ❌ | ✅ | ✅ |

## Reverse Fit Check

| Shape Part | Mechanism | Requirement(s) Served | Justified? |
|---|---|---|:---:|
| B1 | ... | R1 | ✅ |

## Decision

Chosen direction: ...

Why:
- ...

## Unknowns / Spikes

| ID | Unknown | Why it matters | Spike needed? |
|---|---|---|:---:|
| U1 | ... | ... | ✅ |

## Breadboard handoff

- Selected shape: ...
- Parts to preserve: ...
- Non-goals: ...
- First thing to make concrete: ...

## Self-check

- [ ] Requirements are needs or constraints, not mechanisms.
- [ ] Shapes are meaningfully different directions.
- [ ] CURRENT is modeled when there is an existing system.
- [ ] Unknowns are flagged instead of treated as solved.
- [ ] Every selected shape part is justified by at least one requirement.
- [ ] Rejected alternatives remain marked as rejected.
