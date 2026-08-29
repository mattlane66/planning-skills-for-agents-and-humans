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

Persist the five gate tests as `concept_gate_checks` booleans. PASS requires all five
true, a relevant trend ref, and a supporting finding that links to a QUALIFIED LU
episode.

If no need passes, stop and say:

> No opportunity is currently supported strongly enough for concept generation.

That is a successful outcome.

## Fit Check

Where a passing need depends materially on one or more traced LU episodes, reopen those traces and their evidence refs before deriving fitness conditions.

Do not infer x, y, the gap, or constraints from missing chronology, motivation, or outcome. If those gaps make the fitness conditions non-defensible, return the need to the Concept Generation Gate rather than completing the story.

For each passing need derive:

- x — current state;
- y — desired state;
- gap;
- constraints;
- R## — fitness conditions.

Each requirement must explicitly record:

- traceability to evidence;
- implementation independence;
- solution plurality;
- causal relevance to the gap;
- altitude check — stated at the need rather than workaround altitude;
- information gain — a mechanism adds implementation information rather than merely restating R.

Persist these six checks as booleans. Mark a requirement PASS only when all six are true and supporting evidence refs exist.

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

## Phase handoff

After writing and validating this phase, follow
`references/phase-handoff.md`. For a file-backed study, derive the next move with
`scripts/next_research_move.py`; do not advance from invocation history alone.
