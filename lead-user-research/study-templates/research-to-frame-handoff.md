# Proposed Research-to-Planning Handoff

This is evidence input to planning, not accepted product truth and not build scope.

Read `../PACKAGE_BOUNDARY.md` for the package and authority boundary.

## Gate

- Contract: `research-to-planning-v1`
- Status: `PROPOSED | ACCEPTED | REJECTED | REVISE`
- Human decision:
- Decision date:
- Research workspace:
- Decision Brief:
- Phase F material: `NONE | PRESENT`

Do not invoke `framing-doc`, `shaping`, or another downstream planning skill from this handoff until the status is `ACCEPTED`.

## Decision the research informed

[Original human decision]

## Evidence-backed current situation inputs

- [Observation or finding with F## / E## / LU## references]

## Current approaches and results

- [Observed approach, result, workaround, or counterexample with references]

## Future-facing needs and desired outcomes

- [Solution-independent need with N## and supporting references]

## Forces and boundaries suggested by the evidence

- [Force, constraint, discoverability limitation, or scope boundary]

## Candidate planning criteria

- [Outcome, constraint, or quality bar—not a mechanism]

## Phase F research-local planning material

Complete this section only when Phase F ran. These records remain research evidence even when their local state says `ACCEPTED`, `PASS`, or `SELECTED`.

### Research concept-evaluation frame

- Research frame ref: `LUR:<workspace>:SF##`
- Research-local status: `PROVISIONAL | ACCEPTED`
- Human review/provenance:
- x / current situation:
- y / desired outcome:
- gap:
- boundaries:
- evidence refs:

### Research-local fit criteria

| Research ref | Criterion | Research status | Evidence refs | Proposed planning mapping |
|---|---|---|---|---|
| `LUR:<workspace>:R##` | ... | `PASS | FAIL | PROVISIONAL` | ... | existing project R## / new Working R## / do not carry |

Research `R##` IDs are workspace-local. Preserve the namespaced research ref as provenance. Map to an existing project requirement when the meaning is materially the same; otherwise mint a new **Working** project-local R##. Once a project requirement exists, preserve its project ID through Working → Accepted promotion unless its meaning materially changes.

### Research-local candidate mechanisms

| Research ref | Mechanism | Research state | Human research-selection provenance | Proposed planning role |
|---|---|---|---|---|
| `LUR:<workspace>:M##` | ... | `CANDIDATE | SELECTED | REJECTED` | ... | candidate shape / rejected evidence / do not carry |

A research-local `SELECTED` mechanism is not a selected project shape. Preserve its human provenance so downstream shaping can reuse the decision evidence instead of asking the human to reconstruct the same judgment from memory.

## Contradictions and consequential unknowns

- [Contradiction, counterexample, coverage gap, or disconfirming evidence]

## Explicitly not carried into planning

- Rejected, speculative, derivative-only, or unsupported implication:
- Proposed mechanism that must not be mistaken for a requirement:
- Research-local state that is intentionally not promoted:

## Layer-preserving rejection

If downstream design/engineering rejects something for technical, economic, safety, regulatory, operational, or timing reasons, identify whether the rejected layer is the **need, principle, requirement, mechanism, or implementation part**.

A lower-layer rejection does not automatically invalidate a higher layer. In particular:

> reject mechanism ≠ reject requirement ≠ reject need

Any change to an evidenced need/principle/research criterion needs its own rationale and evidence. Any change to an accepted project requirement follows the planning workflow's requirement-lineage rules.

## Proposed next move

Choose the smallest planning move after this handoff is ACCEPTED:

- **Phase F material = NONE:** normally invoke `framing-doc` to create or revise the product frame from the accepted evidence implications.
- **Phase F material = PRESENT and useful:** normally invoke `shaping` in collaborative mode. Import the research frame, fit criteria, and candidate mechanisms as **Working** material with their namespaced research provenance. Do not reconstruct the same frame or concepts merely because they crossed a package boundary.

The planning step may reject, revise, or remap any proposed implication. It must still enforce the planning promotion gates that Phase F did not satisfy—especially accepted project requirements, Appetite/cut line, decision-ready fit, explicit project shape selection when needed, selected-design reconciliation, and active scope.

Do not ask the human to repeat a Phase F frame or mechanism decision solely because the handoff occurred. Revisit the decision when the relevant planning gate was not actually met or when a consequential planning input has changed.
