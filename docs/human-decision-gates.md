# Human decision gates

Agents can help create planning artifacts, compare options, investigate uncertainty, and preserve context. Humans still own the decisions that commit scope, Appetite, selected direction, and trade-offs.

> **These gates control promotion and commitment, not the order in which shaping exploration may occur.**

During collaborative shaping, requirements, shapes, fit checks, spikes, sketches, and candidate breadboards may be created or revised in any useful order while they remain working material. A user may start from R, start from S, or start from evidence. The gates below become mandatory when working material is promoted into accepted planning truth or build scope.

When a gated/orchestrated profile is explicitly selected, additional prerequisite ordering may be enforced earlier. The hard human gates do not change.

Wayfinding coordinates decision work across sessions but creates no additional authority. Claiming, resolving, or closing a Wayfinding ticket never substitutes for the applicable gate below; record the accepted result in its canonical planning artifact before treating the ticket as complete.

## Working material — no commitment gate

Working material can include:

- provisional requirements
- candidate shapes
- a tentative Appetite
- working fit checks
- focused spikes
- candidate-shape breadboards
- sketches and prototypes

The agent may help revise these directly during exploration, provided it keeps requirements separate from mechanisms, labels provisional inputs, preserves stable IDs where useful, and does not present working material as accepted truth.

When a proposed change would modify already accepted material, stop and show the delta instead of silently rewriting it.

## Gate 1 — Frame accepted

Human confirms or intentionally waives the need for a more formal frame because the problem boundary is already clear:

- this is the real problem or opportunity
- this is the desired outcome
- the boundaries and non-goals are correct
- the source evidence is represented fairly

A rough solution may be explored before Gate 1 in collaborative shaping. Do not **select** a shape until the problem boundary is clear enough for honest judgment.

## Gate 2 — Requirements accepted

Human confirms:

- the requirements describe needs, not mechanisms
- must-haves and nice-to-haves are separated
- rejected or out-of-scope criteria are visible
- no important stakeholder constraint is missing enough to invalidate comparison

Working requirements may be extracted from an existing solution shape, prototype, or fit failure before this gate. Gate 2 means they are now good enough to judge selection against.

Do not select a shape until requirements are accepted enough to judge fit.

## Gate 2A — Appetite accepted

Human decides how much time and scope the bet deserves before a shape is selected.

Human confirms:

- time budget or other fixed scope budget
- team shape and review point
- explicit cut line
- how much uncertainty is acceptable
- which unknowns require a candidate breadboard or focused spike before selection or build

Collaborative shaping may sketch shapes, run working fit checks, or investigate candidate behavior before Appetite is accepted. When it does, Appetite-dependent claims remain provisional.

Do not let an agent select an attractive shape first and turn its implied scope into the budget. Selection waits until Appetite is explicit and accepted.

## Gate 2B — Candidate evidence ready, when needed

Use this gate only when a named candidate needs extra evidence before selection.

In collaborative shaping, the candidate breadboard or spike may have started while requirements or Appetite were still working. Before using that evidence to support selection, confirm:

- the candidate and question being tested are explicit
- the breadboard is declared `candidate-shape` or the spike is clearly scoped
- the authority of its R and Appetite inputs is stated
- only decision-relevant detail was added
- current-state evidence remains separate from proposed behavior
- fit, reverse-fit, and Appetite implications are returned to shaping
- any claims based on provisional inputs have been rerun or revalidated against accepted inputs
- the candidate evidence has not selected itself, produced slices, or become build scope

This is an evidence-readiness gate, not a commitment gate. Not every candidate needs a breadboard, and candidates do not need equal detail.

## Gate 3 — Shape selected

Human chooses a direction after seeing enough accepted judging material and comparison evidence.

Human confirms:

- accepted requirements are visible
- accepted Appetite and cut line are visible
- the selected shape is explicit
- rejected shapes remain marked as rejected
- important unknown mechanisms are resolved, accepted, or flagged
- unequal exploratory depth did not substitute for judgment
- candidate evidence to retain, revise, or discard is named
- fit, reverse fit, and Appetite implications are decision-ready
- the selected shape is worth detailing

Do not infer selection from enthusiasm, recency, polish, or the fact that the user started from a particular solution.

Do not automatically promote a candidate breadboard merely because its shape was selected.

## Gate 3A — Visual deltas accepted, when needed

Use this gate when a sketch, screenshot, wireframe, mockup, prototype, or whiteboard appears to add or contradict accepted behavior.

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
- accepted shape parts, requirements, Appetite, and cuts are cited
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
4. stop or create a new bet

Agents should surface drift; humans decide which truth changes.

## Universal rule of thumb

Pause for a human gate when a change would:

- promote working requirements to accepted criteria
- accept or materially change Appetite or the cut line
- select a direction
- promote candidate evidence into selected-design authority
- accept consequential visual deltas to selected intent
- select or expand build scope
- resolve planning drift by changing accepted truth

Do **not** pause merely because the collaborative shaping loop moved from R to S, S to fit, fit to spike, spike to candidate breadboard, or back again.
