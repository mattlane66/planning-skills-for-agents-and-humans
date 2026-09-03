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
An agent is comparing implementation reality against accepted intent and preparing an explicit decision about what should change.

## Must preserve
- accepted intent and current implementation reality as separate records
- observed drift
- missing behavior
- accidental behavior
- proposed fixes
- the authorized or still-needed drift decision

## Ignore unless asked
- speculative redesigns not grounded in inspected implementation evidence

## Inputs
- Breadboard artifact:
- Implementation files or system notes:
- Selected slice:

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
2. Update the plan because the original assumption was wrong.
3. Split the slice and defer the conflicting part.

Recommended move:
- ...

Decision status:
- Pending / authorized by current user instruction / decided by [name or record]

Artifacts or implementation allowed to change after this decision:
- ...

## Realized fit

Use only when outcome evidence from actual use exists. Implementation conformance alone is not realized-fit evidence.

| Req | Accepted requirement | Embedded refs | Reality evidence | Status | Implication |
|---|---|---|---|---|---|
| R1 | ... | U2, N3 | ... | NOT_ASSESSED / SUPPORTED / WEAKENED / CONTRADICTED | ... |

If reality weakens or contradicts accepted planning, preserve the evidence and propose the upstream delta; do not silently rewrite the requirement or frame.

## Self-check
- [ ] Implementation reality was inspected before critique.
- [ ] Accepted intent and current reality remain separate.
- [ ] Proposed fixes are grounded in concrete drift or smells.
- [ ] Planning updates and implementation follow-ups are separated.
- [ ] Realized-fit claims use outcome evidence from actual use; absent evidence remains NOT_ASSESSED.
- [ ] No accepted artifact was rewritten before an explicit decision.
