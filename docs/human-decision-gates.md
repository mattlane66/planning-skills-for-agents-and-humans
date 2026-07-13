# Human decision gates

Agents can help create planning artifacts, compare options, and preserve context. Humans still own the decisions that commit scope, appetite, and trade-offs.

Use these gates to keep collaboration explicit.

## Gate 1 — Frame accepted

Human confirms:

- this is the real problem
- this is the desired outcome
- the boundaries and non-goals are correct
- the source evidence is represented fairly

Do not shape deeply until the frame is accepted or intentionally revised.

## Gate 2 — Requirements accepted

Human confirms:

- the requirements describe needs, not mechanisms
- must-haves and nice-to-haves are separated
- rejected or out-of-scope criteria are visible
- no important stakeholder constraint is missing

Do not select a shape until requirements are good enough to judge fit.

## Gate 3 — Shape selected

Human chooses a direction after seeing alternatives and fit checks.

Human confirms:

- the selected shape is explicit
- rejected shapes remain marked as rejected
- unknown mechanisms are flagged
- the selected shape is worth detailing

Do not breadboard every option unless the human asks for more exploration.

## Gate 4 — Appetite set

Human decides how much time and scope the bet deserves.

Human confirms:

- time budget or appetite
- what is intentionally cut
- how much uncertainty is acceptable
- whether a spike is needed before build work

Do not let an agent turn an open-ended plan into an unbounded spec.

## Gate 5 — Breadboard accepted

Human confirms the intended behavior before slicing.

Human checks:

- places match the actual user/operator experience
- affordances are concrete
- hidden system consequences are visible
- stores and wiring explain the behavior
- product-relevant branches are explicit
- any derived statechart remains traceable to the breadboard and exposes rather than invents missing behavior

Do not slice from a vague or partially understood breadboard.

## Gate 6 — Slice selected

Human chooses what gets built first.

Human confirms:

- selected slice
- demo path
- `Produces` line
- exclusions
- verification target
- active Dumplink task group and cuts, when task grouping governs the build pass

Do not implement outside the selected slice unless the human expands scope.

## Gate 7 — Drift decision

When implementation reality conflicts with the plan, human chooses the correction.

Options:

1. update code to match the plan
2. update the plan because the original assumption was wrong
3. split the slice and defer the conflicting part

Agents should surface drift; humans decide which truth changes.

## Rule of thumb

If a decision changes scope, appetite, selected direction, or source-of-truth artifacts, pause for a human gate.
