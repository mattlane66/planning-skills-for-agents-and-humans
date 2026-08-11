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
An agent and human need a shared shaping surface for requirements, solution shapes, fit checks, unknowns, Appetite, and selection before implementation.

## Governing rule
**Exploration is fluid. Commitment is gated.** Start from R, S, evidence, or an uncertainty. Keep working material visibly distinct from accepted material.

## Must preserve
- stable requirement and shape IDs
- working versus accepted authority
- selected shape and rejected alternatives once selection occurs
- unknown flags
- non-goals and Appetite

## Ignore unless asked
- rejected shapes as implementation instructions
- raw brainstorms as accepted intent

## Working mode
- Profile: collaborative | gated
- Current move: R | S | fit | appetite | spike | candidate breadboard | selection
- Entry point: requirements | solution | evidence/prototype | existing artifact | other

## Frame reference
- Frame artifact:
- Frame authority: Working | Accepted | Intentionally lightweight
- Outcome:
- Non-goals:

## Requirements

| ID | Requirement | Status | Authority | Notes |
|---|---|---|---|---|
| R0 | ... | Core goal | Working | ... |
| R1 | ... | Must-have | Working | ... |

## Appetite
- Authority: Unset | Working | Accepted
- Time budget:
- Team shape:
- Review point:
- Cut line:
- Accepted uncertainty:
- Must-resolve unknowns:
- Revisit conditions:

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

## Candidate evidence

| Candidate / part | Evidence | Question resolved | R implication | S implication | Appetite implication | Remaining uncertainty |
|---|---|---|---|---|---|---|
| A | spike / candidate breadboard / sketch | ... | ... | ... | ... | ... |

## Fit check
- Authority: Working | Decision-ready

| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | ... | Core goal | ✅ | ✅ | ✅ |
| R1 | ... | Must-have | ❌ | ✅ | ❌ |

## Reverse fit check

| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| B1 | ... | R1 | ✅ |

## Appetite fit

| Shape | Evidence quality | Fits Appetite? | Required cuts | Uncertainty / spike |
|---|---|:---:|---|---|
| A | provisional | ... | ... | ... |
| B | decision-ready | ... | ... | ... |

## Decision
- Status: exploring | decision-ready | selected | stopped
- Chosen direction:
- Why:
- Rejected directions:
- Cuts / non-goals:
- Remaining unknowns:
- Candidate evidence to reconcile:

## Unknowns / spikes

| ID | Question | Triggered by | Why it matters | Acceptance |
|---|---|---|---|---|
| SP1 | ... | R / S / fit / breadboard | ... | ... |

## Next useful move
Choose the move that resolves the current uncertainty; this is not a checklist.

- [ ] Revise requirements (R)
- [ ] Revise or sketch a shape (S)
- [ ] Run or rerun fit / reverse-fit
- [ ] Set, revise, or accept Appetite
- [ ] Run focused spike
- [ ] Breadboard one candidate question
- [ ] Reconcile visual evidence
- [ ] Prepare for human selection
- [ ] Reopen framing
- [ ] Stop
