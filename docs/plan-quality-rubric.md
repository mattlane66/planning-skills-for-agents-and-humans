# Plan quality rubric

Use this rubric to evaluate whether a planning artifact is ready to guide human and AI implementation work.

Score each line as:

- `0` — missing or misleading
- `1` — present but weak or ambiguous
- `2` — clear enough to guide work

## Rubric

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Frame preserved | No clear current situation or problem/outcome | Current approach, current result, problem, or outcome is vague | Current approach/result, problem, outcome, and boundaries are explicit |
| Source traceability | Claims are unsupported | Some claims trace to source | Important claims are traceable or marked as inference |
| Requirements vs mechanisms | Mixed together | Mostly separated with some leakage | Requirements describe needs; mechanisms live in shapes |
| Appetite and cut line | Missing or derived from a preferred shape | Budget exists but cuts or uncertainty are vague | Appetite, cut line, accepted uncertainty, and revisit conditions are explicit before selection |
| Alternatives considered | Only one solution asserted | Alternatives are shallow | Meaningful alternatives are compared |
| Selected direction | Not explicit | Implied but not named | Selected shape is explicit and stable |
| Rejected alternatives | Hidden or mixed into active work | Mentioned but not clearly rejected | Rejected ideas remain labeled as rejected |
| Unknowns | Hidden or treated as solved | Some unknowns noted | Unknowns are flagged and spikeable |
| Breadboard concreteness | Too abstract to build | Some places/affordances are concrete | Places, affordances, stores, and wiring explain behavior |
| Slice quality | No slice or horizontal tasks only | Slice exists but is hard to demo | Slice is vertical, demoable, and bounded |
| Produces line | Missing | Vague | Names the output the next slice needs |
| Non-goals | Missing | Present but detached | Close to the work and preserved in handoff |
| Stable IDs | Missing | Present but inconsistent | IDs are stable and traceable across artifacts |
| Verification target | Missing | Vague | Clear behavior, test, or demo target |
| Human gates | Agent decides implicitly | Some decisions surfaced | Scope/appetite/direction decisions are explicit |
| Drift handling | Plan changes silently | Drift is noted but unresolved | Drift options are stated and require a decision |

## Optional artifact checks

Score these only when the corresponding artifact is present or clearly needed. They do not change the readiness-band total above.

| Artifact | 0 | 1 | 2 |
|---|---|---|---|
| Statechart | Replaces or contradicts the breadboard | Partly traceable or contains assumptions | Every state and transition traces to breadboard IDs; gaps are explicit |
| Sketch reconciliation | Visual is treated as truth or hidden behavior is guessed | Observations exist but mappings or decisions are incomplete | Observations and interpretations are separate; deltas cite evidence, map to stable IDs, pass a human gate, and ripple to affected artifacts |
| Interface contracts | Agent must guess fields or error behavior | Main path exists but edge decisions are missing | Inputs, outputs, branches, errors, and open decisions are explicit |
| Executable breadboard | No judgeable examples | Examples exist but expected results are vague | Fixtures, example runs, expected outputs, edge cases, and checks are complete |
| Dumplink | Horizontal discipline backlog | Some vertical grouping but unclear cuts or risk | Groups are judgeable, risk-aware, dependency-aware, and cuttable |
| Context packet | Whole planning stack is dumped | Relevant scope exists but execution boundaries are weak | Only relevant context is included with authority, non-goals, execution contract, and verification |

## Readiness bands

| Score | Interpretation |
|---:|---|
| 0–13 | Not ready. Continue framing or shaping. |
| 14–24 | Directional but risky. Clarify weak spots before building. |
| 25–32 | Ready for slice planning or tightly bounded implementation. |

## Required passes before implementation

Before build work starts, these dimensions should score `2`:

- selected direction
- appetite and cut line
- slice quality
- non-goals
- verification target
- human gates

For agent implementation, the optional Context packet check must also score `2`; build mode requires a compact packet with an execution contract.

## Quick review prompt

```text
Use docs/plan-quality-rubric.md to review this planning artifact. Score each dimension 0/1/2, name the top three risks, and recommend the next planning move before implementation.
```
