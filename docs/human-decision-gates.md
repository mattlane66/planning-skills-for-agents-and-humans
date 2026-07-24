# Human decision gates

Agents can help create planning artifacts, compare options, and preserve context. Humans still own the decisions that commit scope, Appetite, and trade-offs.

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

## Gate 2A — Appetite set

Human decides how much time and scope the bet deserves before a shape is selected.

Human confirms:

- time budget or other fixed scope budget
- team shape and review point
- explicit cut line
- how much uncertainty is acceptable
- which unknowns require a candidate breadboard or focused spike before selection or build

Do not let an agent choose an attractive shape first and turn its implied scope into the budget. Premature mechanism ideas may be parked while Appetite is undecided, but comparative shape work and selection wait until Appetite is explicit.

## Gate 2B — Candidate evidence ready, when needed

Use this gate only when a named candidate cannot be judged from its mechanism list or sketch alone.

Human or team confirms:

- the candidate and question being tested are explicit
- the breadboard is declared `candidate-shape`
- only decision-relevant detail was added
- current-state evidence remains separate from proposed behavior
- fit, reverse-fit, and Appetite implications are returned to shaping
- the candidate breadboard has not selected itself, produced slices, or become build scope

This is an evidence-readiness gate, not a commitment gate. Not every candidate needs a breadboard, and candidates do not need equal detail.

## Gate 3 — Shape selected

Human chooses a direction after seeing alternatives, fit checks, and any necessary candidate evidence.

Human confirms:

- the selected shape is explicit
- rejected shapes remain marked as rejected
- unknown mechanisms are flagged
- unequal exploratory depth did not substitute for judgment
- candidate evidence to retain, revise, or discard is named
- the selected shape is worth detailing

Do not automatically promote a candidate breadboard merely because its shape was selected.

## Gate 3A — Visual deltas accepted, when needed

Use this gate when a sketch, screenshot, wireframe, mockup, or whiteboard appears to add or contradict behavior.

Human confirms:

- visible observations are separated from agent interpretations
- proposed deltas map to existing planning IDs or add explicit new IDs
- requirements remain needs rather than drawn controls
- selected behavior and scope change only where intended
- accepted deltas should ripple to the named downstream artifacts

Do not let visual recency silently override the selected shape or breadboard.

## Gate 4 — Selected-design breadboard accepted

Human confirms the intended behavior before slicing.

Human checks:

- the mode is `selected-design`
- accepted shape parts, Appetite, and cuts are cited
- any candidate rows were explicitly reconciled rather than automatically promoted
- places match the intended user/operator experience
- affordances are concrete
- hidden system consequences are visible
- stores and wiring explain the behavior
- product-relevant branches are explicit
- consequential conflicts were returned to shaping and decided
- any derived statechart remains traceable to the breadboard and exposes rather than invents missing behavior

Do not slice from a current-state, candidate-shape, vague, or partially understood breadboard.

## Gate 5 — Slice selected

Human chooses what gets built first.

Human confirms:

- selected slice
- demo path
- `Produces` line
- exclusions
- verification target
- active Dumplink task group and cuts, when task grouping governs the build pass

Do not implement outside the selected slice unless the human expands scope.

## Gate 6 — Drift decision

When implementation reality conflicts with the plan, human chooses the correction.

Options:

1. update code to match the plan
2. update the plan because the original assumption was wrong
3. split the slice and defer the conflicting part

Agents should surface drift; humans decide which truth changes.

## Rule of thumb

If a decision changes scope, Appetite, selected direction, candidate-to-selected authority, or source-of-truth artifacts, pause for a human gate.