---
planning: true
artifact_type: breadboard-reflection
status: draft
source_of_truth: false
feeds:
  - planning-update
  - implementation-followup
---

# [Project] — Breadboard Reflection

# Context Card

## Use this when
An agent is comparing implementation reality against accepted intent, checking realized conformance, assessing effect from outcome evidence, or diagnosing a surprising result.

## Must preserve
- accepted intent and current implementation reality as separate records
- observed drift, missing behavior, and accidental behavior
- the authorized or still-needed drift decision
- realized-conformance evidence and status
- effect evidence and status
- backward diagnosis when effect is surprising
- the operating model M when it affects interpretation

## Ignore unless asked
- speculative redesigns not grounded in inspected implementation or outcome evidence

## Inputs
- Frame artifact:
- Shaping artifact:
- Operating model M:
- Breadboard artifact:
- Implementation files or system notes:
- Selected slice:
- Outcome evidence:

## Current implementation reality

Record what the system does now and cite the inspected evidence. Do not rewrite the accepted breadboard in this phase.

- ...

## Matches

| ID | Planned behavior | Implementation reality |
|---|---|---|
| ... | ... | ... |

## Drift

| ID | Planned artifact says | Implementation reality | Impact |
|---|---|---|---|
| DRIFT-01 | ... | ... | ... |

## Missing behavior

| ID | Missing behavior | Where it should appear | Why it matters |
|---|---|---|---|
| ... | ... | ... | ... |

## Accidental behavior

| ID | Behavior | Evidence | Risk |
|---|---|---|---|
| ... | ... | ... | ... |

## Smells found

| ID | Smell | Where | Why it matters |
|---|---|---|---|
| ... | ... | ... | ... |

## Proposed fixes

| ID | Change | Expected improvement | Type |
|---|---|---|---|
| FIX-01 | ... | ... | Planning update / implementation follow-up |

## Drift decision needed

Options:
1. Update code to match the plan.
2. Update the plan because an original assumption was wrong.
3. Split the slice and defer the conflicting part.

Recommended move:
- ...

Decision status:
- Pending / authorized by current user instruction / decided by [name or record]

Artifacts or implementation allowed to change after this decision:
- ...

## Realized conformance

Use direct implementation/runtime evidence to judge whether the built artifact satisfies each relevant Accepted R under the relevant M.

| Req | Accepted requirement | Selected-design refs | Build/runtime evidence | Status | Implication |
|---|---|---|---|---|---|
| R1 | ... | U2, N3 | ... | NOT_ASSESSED / CONFORMS / UNCERTAIN / DOES_NOT_CONFORM | ... |

If M may have changed during implementation, revisit it before declaring conformance.

## Effect (realized fit)

Use outcome evidence from actual use to judge whether deployment moved reality from x toward y. If outcome evidence is absent, record `NOT_ASSESSED`; realized conformance alone is not effect evidence.

- x baseline:
- y desired outcome:
- Evidence window / comparison:
- Effect status: NOT_ASSESSED / SUPPORTED / WEAKENED / CONTRADICTED
- Interpretation:
- Attribution assumptions from M:

If effect evidence would change accepted planning, stop at an `effect-decision` before changing accepted truth.

## Backward diagnosis

Complete when effect is weakened, contradicted, or unexpectedly successful.

| Check | Evidence | Finding | Proposed correction, if any |
|---|---|---|---|
| Effect inference | ... | sound / uncertain / wrong | ... |
| Realized conformance | ... | conforms / uncertain / does not conform | ... |
| Implementation realized selected design | ... | yes / partly / no | ... |
| Design conformance / selection | ... | sound / uncertain / wrong | ... |
| Requirements R | ... | adequate / incomplete / wrong | ... |
| Operating model M | ... | adequate / stale / wrong | ... |
| Frame x / y | ... | adequate / stale / wrong | ... |

## Self-check
- [ ] Implementation reality was inspected before critique.
- [ ] Accepted intent and current reality remain separate.
- [ ] Drift, realized conformance, and effect are separate judgments.
- [ ] Realized conformance uses build/runtime evidence and the relevant M.
- [ ] Effect uses outcome evidence from actual use; absent evidence remains NOT_ASSESSED.
- [ ] Surprising effect triggers backward diagnosis before upstream rewriting.
- [ ] Planning updates and implementation follow-ups are separated.
- [ ] No accepted artifact was rewritten before an explicit decision.
