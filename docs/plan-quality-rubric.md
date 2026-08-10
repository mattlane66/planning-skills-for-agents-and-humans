# Plan quality rubric

Use this rubric to evaluate whether planning has become authoritative enough to guide human and AI implementation work.

This rubric evaluates **build readiness**, not whether collaborative shaping followed a particular exploration order. R-first, S-first, evidence-first, and uncertainty-first paths are all valid if the resulting accepted artifacts satisfy the same promotion standards.

Score each line as:

- `0` — missing or misleading
- `1` — present but weak or ambiguous
- `2` — clear enough to guide work

## Rubric

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Frame / problem boundary preserved | No clear current situation or problem/outcome | Boundary is partly understood but consequential ambiguity remains | Current approach/result, problem, outcome, and boundaries are explicit enough for the selected bet |
| Source traceability | Claims are unsupported | Some claims trace to source | Important claims are traceable or marked as inference |
| Requirements vs mechanisms | Mixed together | Mostly separated with some leakage | Requirements describe needs; mechanisms live in shapes even when R was extracted from S |
| Working vs Accepted authority | Exploratory material is presented as committed truth | Some authority is labeled but promotion status is ambiguous | Working R/S/fit/Appetite are visibly distinct from Accepted judging inputs and selected intent |
| Appetite and cut line | Missing or derived from a preferred shape | Budget exists but cuts, authority, or uncertainty are vague | Accepted Appetite, cut line, accepted uncertainty, and revisit conditions are explicit before selection |
| Alternatives considered | Only one solution is asserted without showing whether alternatives genuinely exist | Alternatives are shallow or the reason not to compare is unclear | Meaningful alternatives are compared when they exist; no fake alternatives were manufactured for ceremony |
| Fit evidence | No fit/reverse-fit evidence for the selected direction | Working fit exists but judging inputs or Appetite implications remain provisional | Decision-ready fit, reverse fit, and Appetite implications are validated against Accepted judging inputs |
| Selected direction | Not explicit | Implied but not named | Selected shape is explicit, human-chosen, and stable |
| Rejected alternatives | Hidden or mixed into active work | Mentioned but not clearly rejected | Rejected ideas remain labeled as rejected |
| Unknowns | Hidden or treated as solved | Some unknowns noted | Unknowns are resolved, explicitly accepted, or bounded/spikeable |
| Candidate evidence authority | Candidate prototype/breadboard is treated as selected intent | Candidate status is visible but promotion/revalidation is incomplete | Candidate evidence is clearly exploratory, provisional claims are revalidated, and selected rows were reconciled explicitly |
| Breadboard concreteness | Too abstract to build or candidate evidence is being used as build scope | Some selected-design places/affordances are concrete | Accepted selected-design places, affordances, stores, and wiring explain behavior |
| Slice quality | No slice or horizontal tasks only | Slice exists but is hard to demo | Slice is human-selected, vertical, demoable, and bounded |
| Produces line | Missing | Vague | Names the output the next slice needs |
| Non-goals | Missing | Present but detached | Close to the work and preserved in handoff |
| Stable IDs | Missing | Present but inconsistent | IDs are stable and traceable across artifacts |
| Verification target | Missing | Vague | Clear behavior, test, or demo target |
| Human gates | Agent decides implicitly | Some decisions surfaced | Acceptance, Appetite, selection, promotion, and build-scope decisions are explicit where required |
| Drift handling | Plan changes silently | Drift is noted but unresolved | Drift options are stated and require a decision |

## Optional artifact checks

Score these only when the corresponding artifact is present or clearly needed. They do not change the readiness-band total above.

| Artifact | 0 | 1 | 2 |
|---|---|---|---|
| Focused spike | Investigation drifts into a product decision or produces unbounded research | Useful evidence exists but implications are not returned to shaping | Questions are bounded and explicit R/S/fit/Appetite implications are returned without deciding the direction |
| Candidate-shape breadboard | Candidate is treated as accepted behavior or build scope | Candidate status is visible but input authority or provisional claims are unclear | Named uncertainty, R/Appetite authority, provisional implications, and non-promotion boundary are explicit |
| Statechart | Replaces or contradicts the breadboard | Partly traceable or contains assumptions | Every state and transition traces to selected-design breadboard IDs; gaps are explicit |
| Sketch reconciliation | Visual is treated as truth or hidden behavior is guessed | Observations exist but mappings or decisions are incomplete | Observations and interpretations are separate; deltas cite evidence, map to stable IDs, pass a human gate, and ripple to affected artifacts |
| Interface contracts | Agent must guess fields or error behavior | Main path exists but edge decisions are missing | Inputs, outputs, branches, errors, and open decisions are explicit |
| Executable breadboard | No judgeable examples | Examples exist but expected results are vague | Fixtures, example runs, expected outputs, edge cases, and checks are complete |
| Dumplink | Horizontal discipline backlog | Some vertical grouping but unclear cuts or risk | Groups are judgeable, risk-aware, dependency-aware, and cuttable |
| Context packet | Whole planning stack or exploratory alternatives are dumped | Relevant scope exists but authority/execution boundaries are weak | Only accepted relevant context is included with authority, non-goals, execution contract, and verification |

## Readiness bands

| Score | Interpretation |
|---:|---|
| 0–15 | Not ready. Continue the smallest useful shaping or evidence move. |
| 16–28 | Directional but risky. Clarify weak spots before building. |
| 29–38 | Ready for slice planning or tightly bounded implementation, subject to the required passes below. |

## Required passes before implementation

Before build work starts, these dimensions should score `2`:

- Working vs Accepted authority
- Appetite and cut line
- Fit evidence
- selected direction
- candidate evidence authority when candidate evidence exists
- breadboard concreteness or equally clear accepted behavior boundary
- slice quality
- non-goals
- verification target
- human gates

For agent implementation, the optional Context packet check must also score `2`; build mode requires a compact packet with an execution contract.

## Quick review prompt

```text
Use docs/plan-quality-rubric.md to review this planning artifact for build readiness. Do not penalize a valid R-first, S-first, evidence-first, or uncertainty-first exploration path. Score each dimension 0/1/2, name the top three authority or implementation risks, and recommend the smallest next planning move before implementation.
```
