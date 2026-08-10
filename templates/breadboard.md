---
planning: true
shaping: true
artifact_type: breadboard
status: draft
source_of_truth: false
feeds: []
---

# [Project] — Breadboard

# Context Card

## Mode and authority

- Mode: `current-state`, `candidate-shape`, or `selected-design`
- Authority:
  - `current-state`: descriptive evidence only
  - `candidate-shape`: exploratory evidence subordinate to one unselected candidate and the shaping artifact
  - `selected-design`: accepted normative intent after human selection and reconciliation
- Requirements authority: `Working` | `Accepted` | `Not applicable`
- Appetite authority: `Unset` | `Working` | `Accepted` | `Not applicable`
- Evidence references: required for non-obvious current-state claims
- Candidate shape and uncertainty: required for candidate-shape mode
- Selected shape, Accepted requirements, and Accepted Appetite/cut line: required for selected-design mode

Set frontmatter `source_of_truth: true` and downstream `feeds` only after the artifact is accepted in `selected-design` mode.

Current-state mode cannot define selected future intent. Candidate-shape mode cannot select itself, feed slices, or become build scope. In collaborative shaping, candidate mode may use Working requirements or Unset/Working Appetite; any fit or Appetite implications must remain provisional until revalidated against Accepted judging inputs. Only an accepted selected-design breadboard can produce buildable slice candidates.

## Use this when

An agent is mapping current behavior, clarifying one unselected candidate during shaping, reconciling a selected design, slicing an accepted selected-design breadboard, preparing downstream contracts, or checking whether code still matches selected intent.

## Must preserve

- declared mode and authority
- Requirements/Appetite authority when they affect candidate judgments
- stable place IDs
- stable affordance IDs
- store IDs
- wiring and visible consequences
- source shape-part IDs for proposed elements
- selected demo path in selected-design mode
- interface contract candidate IDs when present

## Ignore unless asked

- rejected shapes unrelated to the named candidate
- raw brainstorms
- candidate breadboards when preparing selected build context unless they explain an unresolved shaping decision

## Shape reference

- Shaping artifact:
- Candidate or selected shape:
- Shape-part IDs:
- Requirements authority:
- Appetite authority:
- Appetite:
- Cut line:
- Decision-relevant uncertainty for candidate-shape mode:
- Reconciliation status for selected-design mode:

## Places

| ID | Authority | Shape part | Place | Description |
|---|---|---|---|---|
| P1 | current / candidate / selected | — | ... | ... |

## UI affordances

| ID | Place | Authority | Shape part | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|---|---|
| U1 | P1 | candidate | A1 | ... | ... | ... | -> N1 | — |

## Non-UI affordances

| ID | Place | Authority | Shape part | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|---|---|
| N1 | P1 | candidate | A1 | ... | ... | call | -> S1 | -> U1 |

## Stores

| ID | Place | Authority | Shape part | Store | Description |
|---|---|---|---|---|---|
| S1 | P1 | current | — | ... | ... |

## Product-relevant branches

| Branch | Trigger | User-visible consequence | Shape part | Status |
|---|---|---|---|---|
| ... | ... | ... | A1 | supported / gap / conflict |

## Candidate-shape findings

Use only in `candidate-shape` mode.

- Question resolved:
- Judging-input authority: Requirements = Working/Accepted; Appetite = Unset/Working/Accepted
- Supported mechanisms:
- Missing or contradictory mechanisms:
- Rabbit holes / Appetite risks when Appetite is known:
- Focused spike candidates:
- Proposed requirement changes:
- Proposed shape changes:
- Requirement-fit implication: Working / decision-ready / not yet supportable
- Reverse-fit implication:
- Appetite-fit implication: provisional / decision-ready / not yet supportable
- Remaining uncertainty:

If Requirements or Appetite are not Accepted, label dependent conclusions provisional. Return useful R/S changes to shaping. Do not silently rewrite Accepted material.

## Selected-design reconciliation

Use when promoting or rebuilding from candidate evidence after human selection.

| Candidate row / finding | Selected action | Resulting selected-design ID | Rationale |
|---|---|---|---|
| ... | keep / revise / remove / defer | ... | ... |

A candidate row is never promoted merely because its candidate was selected. Reconcile it against the Accepted requirements, selected shape, Accepted Appetite/cuts, and remaining unknowns.

## Interface contract candidates (selected-design only)

Use this section when an accepted wire crosses a meaningful boundary: UI -> backend, frontend -> API, service -> store, agent -> tool, import -> parser, or external integration.

| ID | Trigger / Wire | From | To | Request / Input Shape | Response / Output Shape | Branches / Errors | Open Decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | UI | API | user_id: string | status: string | invalid user | nullable or omitted? |

## Slice candidates (accepted selected-design only)

| Slice | Affordances / stores included | Demo | Produces | Unknowns |
|---|---|---|---|---|
| V1 | ... | ... | ... | ... |

## Shaping conflict

When detailed selected-design breadboarding exposes a consequential conflict, stop and return:

- Selected shape says:
- Concrete behavioral implication:
- Conflict or Appetite risk:
- Evidence:
- Options: revise shape / cut behavior / focused spike / reopen selection / stop bet

## Build handoff note

Once a selected-design breadboard is accepted and a slice is selected, convert the relevant part into an executable breadboard with examples, expected results, edge cases, and acceptance tests.

## Notes

- ...

## Self-check

- [ ] The mode and authority are explicit.
- [ ] Candidate-shape mode names one candidate and one decision-relevant uncertainty.
- [ ] Candidate-shape mode states Requirements/Appetite authority.
- [ ] Provisional inputs do not produce final fit/Appetite claims.
- [ ] Candidate evidence has not selected itself or produced build scope.
- [ ] Candidate rows were reconciled before becoming selected-design rows.
- [ ] Selected-design mode cites Accepted requirements, selected shape, Accepted Appetite, and cuts.
- [ ] Every displayed UI element that depends on data has a source.
- [ ] Every non-UI affordance connects by Wires Out or Returns To.
- [ ] Stores exist for meaningful side effects.
- [ ] Product-relevant branches are explicit.
- [ ] Only accepted selected-design behavior produces interface contracts or slice candidates.
- [ ] Any shaping conflict is surfaced rather than silently absorbed.
