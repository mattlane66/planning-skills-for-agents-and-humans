# Human Decision Gates

Agents can help create planning artifacts, but they should not quietly make every product decision. Use these gates to decide when a human must choose before the workflow moves forward.

## Gate 1 — Frame accepted

Human confirms:

- this is the real problem
- this is the desired outcome
- the boundaries and non-goals are right
- the source evidence supports the frame

Do not move to shaping if the frame is still contested.

## Gate 2 — Requirements accepted

Human confirms:

- the requirements describe what must be true, not how to implement it
- must-haves, nice-to-haves, and out-of-scope items are labeled
- important constraints are visible
- no major requirement is missing

Do not select a shape if the requirements are unstable.

## Gate 3 — Shape selected

Human chooses among alternatives after seeing:

- the current baseline, when relevant
- at least two meaningfully different directions, when possible
- a fit check
- a reverse fit check for the selected direction
- flagged unknowns and spikes

The agent may recommend, but the human chooses.

## Gate 4 — Appetite set

Human decides:

- how much time or scope the bet deserves
- what must be included in this cycle
- what should be cut, deferred, or spiked
- what level of polish is appropriate

Without appetite, the plan can expand into an unbounded spec.

## Gate 5 — Breadboard accepted

Human confirms:

- the places are the right interaction contexts
- affordances map to real user-visible or product-relevant behavior
- hidden system behavior is represented where it matters
- stores and wiring explain the intended behavior
- important branches are explicit

Do not slice from a breadboard the human does not trust.

## Gate 6 — Slice selected

Human chooses:

- the first demoable slice
- explicit exclusions
- the demo path
- what the slice must produce for the next slice
- verification target

The agent may propose slice order based on dependencies and unknowns, but the human owns the cut.

## Gate 7 — Drift decision

Human decides what to do when implementation reality conflicts with the plan.

Options:

1. Update the code to match the artifact.
2. Update the artifact because the original assumption was wrong.
3. Split the slice and defer the conflicting part.

Agents should surface drift; humans decide which truth changes.

## Short rule

If the decision changes the problem, requirements, appetite, selected direction, slice boundary, or source of truth, stop and ask for a human decision.
