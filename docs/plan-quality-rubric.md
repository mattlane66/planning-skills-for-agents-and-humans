# Plan Quality Rubric

Use this rubric to check whether a planning artifact is ready to guide humans and agents.

Score each row:

- `0` = missing or misleading
- `1` = present but weak or ambiguous
- `2` = clear, useful, and actionable

## Rubric

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Frame preserved | No clear problem/outcome | Problem or outcome is vague | Problem, outcome, and boundaries are explicit |
| Evidence separated | Source and interpretation are mixed | Some claims trace to source | Source evidence and interpretation are clearly separated |
| Requirements separated from mechanisms | Requirements name UI/vendor/implementation choices | Some requirements are mechanism-flavored | Requirements state needs, constraints, or outcomes |
| Alternatives visible | Only one solution is assumed | Alternatives are superficial | Meaningfully different directions are compared |
| Fit check present | No fit check | Fit check exists but is incomplete | Requirements are checked against alternatives with clear pass/fail values |
| Reverse fit check present | Shape parts are not justified | Some parts map to requirements | Every selected part is justified or cut |
| Unknowns flagged | Unknowns are hidden | Unknowns are mentioned loosely | Unknowns are flagged and converted into spikes where needed |
| Appetite clear | Scope is unbounded | Appetite is implied | Time/scope appetite and cut line are explicit |
| Breadboard concrete | Behavior remains abstract | Some places/affordances are mapped | Places, affordances, stores, and wiring explain behavior |
| Slices demoable | Slices are horizontal tasks | Some slices have visible output | Each slice has a demo path and produces line |
| Context packet scoped | Agent receives everything | Context packet is too broad or underspecified | Agent receives only the needed context with authority order |
| Drift protocol visible | Plan/code conflicts are hidden | Drift is mentioned without options | Drift options are explicit and require a decision |
| Human gates clear | Agent can decide everything silently | Some gates are implied | Human decision points are explicit |
| Verification target clear | No way to know if work fits | Verification is vague | Verification target maps back to requirements/slices |

## Interpreting the score

| Score | Meaning |
|---:|---|
| 0–10 | Not ready. Reframe or reshape before implementation. |
| 11–20 | Partially ready. Good enough for discussion, not safe for autonomous build work. |
| 21–26 | Mostly ready. Feed a scoped context packet before implementation. |
| 27–28 | Strong. Ready for a selected-slice implementation handoff. |

## Minimum bar before implementation

Before an agent writes code, the plan should have:

- accepted frame
- selected shape
- explicit appetite or cut line
- concrete breadboard or equivalent behavior map
- selected slice
- compact context packet
- verification target
- drift protocol

If any of these are missing, the next move is planning, not implementation.
