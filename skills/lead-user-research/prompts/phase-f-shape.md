# Phase F — Shape

This phase is optional.

At the start, reopen:

- frozen evidence;
- findings;
- needs;
- principles;
- existing fit criteria and concepts.

## Concept Generation Gate

A need may proceed only when:

1. its trend is credible;
2. at least one qualified LU episode supports it;
3. the need is separable from the observed workaround;
4. evidence is sufficient to derive meaningful fitness conditions;
5. no unresolved contradiction makes concept work premature.

Record PASS / FAIL / NOT_ASSESSED and rationale in `needs.json`.

If no need passes, stop and say:

> No opportunity is currently supported strongly enough for concept generation.

That is a successful outcome.

## Fit Check

For each passing need derive:

- x — current state;
- y — desired state;
- gap;
- constraints;
- R## — fitness conditions.

Each requirement must be:

- evidence-traceable;
- implementation-independent;
- plausibly satisfiable by different mechanisms;
- causally relevant to the gap;
- stated at the need rather than workaround altitude.

Freeze requirements before evaluating mechanisms.

## Concept generation

Generate enough materially different mechanisms to test the requirements.

There is **no minimum concept quota**.

Do not invent weak alternatives merely to make the output symmetrical.

If only one credible mechanism emerges:

- say so;
- re-examine whether the requirements are too mechanism-specific;
- preserve the result if they are still valid.

## Compare

Assess each M## against frozen R##.

Do not alter requirements merely to make a preferred mechanism win.

## Write state

Update:

- `needs.json`;
- `fit_criteria.json`;
- `concepts.json`;
- `change_log.json`.
