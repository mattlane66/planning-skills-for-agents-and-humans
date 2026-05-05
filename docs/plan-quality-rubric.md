# Plan quality rubric

Use this rubric to evaluate whether a planning artifact is ready to guide human and AI implementation work.

Score each line as:

- `0` — missing or misleading
- `1` — present but weak or ambiguous
- `2` — clear enough to guide work

## Rubric

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Frame preserved | No clear problem/outcome | Problem or outcome is vague | Problem, outcome, and boundaries are explicit |
| Source traceability | Claims are unsupported | Some claims trace to source | Important claims are traceable or marked as inference |
| Requirements vs mechanisms | Mixed together | Mostly separated with some leakage | Requirements describe needs; mechanisms live in shapes |
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

## Readiness bands

| Score | Interpretation |
|---:|---|
| 0–12 | Not ready. Continue framing or shaping. |
| 13–22 | Directional but risky. Clarify weak spots before building. |
| 23–30 | Ready for slice planning or tightly bounded implementation. |

## Required passes before implementation

Before build work starts, these dimensions should score `2`:

- selected direction
- slice quality
- non-goals
- verification target
- human gates

## Quick review prompt

```text
Use docs/plan-quality-rubric.md to review this planning artifact. Score each dimension 0/1/2, name the top three risks, and recommend the next planning move before implementation.
```
