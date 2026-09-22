---
planning: true
shaping: true
artifact_type: shaping
status: accepted
source_of_truth: true
---

# Checkout Assist — Shaping

## Working mode
- Profile: gated
- Current move: selection
- Entry point: requirements

## Frame reference
- Transformation frame: x → f() → y
- Frame artifact: alpha.md
- Frame authority: Accepted
- Outcome: one clear checkout flow
- Non-goals: account migration

## Operating model (M, optional)
- Authority: Accepted
- Relevant operating conditions: checkout submits into the existing downstream system
- Causal assumptions / projected dynamics: invalid totals are rejected downstream and require correction before successful completion
- Evidence refs: alpha.md
- Revisit conditions: downstream validation or submission behavior changes

## Requirements

| ID | Requirement | Status | Authority | Origin | Evidence refs | Notes |
|---|---|---|---|---|---|---|
| R0 | Staff can complete checkout from one visible flow. | Core goal | Accepted | FROM_GAP | alpha | — |
| R1 | Staff see a clear confirmation after submission. | Must-have | Accepted | FROM_Y | alpha | — |
| R2 | Invalid totals are stopped before submission. | Must-have | Accepted | FROM_M | alpha | — |

## Appetite
- Authority: Accepted
- Time budget: one week
- Team shape: one builder
- Review point: working end-to-end demo
- Cut line: no account migration or inventory redesign
- Accepted uncertainty: visual polish may remain rough
- Must-resolve unknowns: none
- Revisit conditions: validation cannot stay local

## Shapes

### CURRENT: Existing handoff

| Part | Mechanism | Flag |
|---|---|:---:|
| CURRENT1 | Copy between tools | |

### A: Single checkout workspace

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | One checkout workspace keeps order context visible | |
| A2 | Inline total validation blocks invalid submission | |
| A3 | Confirmation state appears in the same workspace | |

### B: Step-by-step wizard

| Part | Mechanism | Flag |
|---|---|:---:|
| B1 | Multi-screen wizard guides each field group | |
| B2 | Final confirmation screen | |

## Fit check
- Authority: Decision-ready

| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | Staff can complete checkout from one visible flow. | Core goal | ❌ | ✅ | ❌ |
| R1 | Staff see a clear confirmation after submission. | Must-have | ❌ | ✅ | ✅ |
| R2 | Invalid totals are stopped before submission. | Must-have | ❌ | ✅ | ✅ |

## Reverse fit check

| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| A1 | One checkout workspace | R0 | ✅ |
| A2 | Inline validation | R2 | ✅ |
| A3 | Confirmation state | R1 | ✅ |

## Appetite fit

| Shape | Evidence quality | Fits Appetite? | Required cuts | Uncertainty / spike |
|---|---|:---:|---|---|
| A | decision-ready | ✅ | none | none |
| B | decision-ready | ❌ | wizard complexity | none |

## Decision
- Status: selected
- Chosen direction: A
- Why: smallest shape that satisfies the accepted requirements inside the appetite
- Rejected directions: CURRENT, B
- Cuts / non-goals: account migration, inventory redesign
- Remaining unknowns: none
- Candidate evidence to reconcile: none
