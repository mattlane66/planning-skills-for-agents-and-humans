# Phase F — Shape

This phase is optional.

At the start, reopen:

- frozen evidence;
- findings;
- needs;
- principles;
- existing `shaping_frame.json`;
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

Where a passing need depends materially on one or more traced LU episodes, reopen those traces and their evidence refs before framing the transformation.

Do not infer the current situation, desired outcome, gap, or boundaries from missing chronology, motivation, or outcome. If those gaps make the frame non-defensible, return the need to the Concept Generation Gate rather than completing the story.

For each passing need construct `SF##` in `shaping_frame.json`:

- `x.trigger_or_context`;
- `x.current_approach`;
- `x.current_result`;
- `x.breakdowns`;
- `f.status = UNSPECIFIED`;
- `y.desired_outcome`;
- `gap`;
- `boundaries`;
- `evidence_refs`;
- `status = PROVISIONAL | ACCEPTED`;
- `accepted_by_human`;
- `acceptance_note`.

This is the shaping/design frame, not the Phase A research frame.

When the frame is first constructed, write it as PROVISIONAL and stop for explicit human review. A model must not set `status = ACCEPTED` or `accepted_by_human = true` without an explicit human decision.

Only after the frame is ACCEPTED derive R## fitness conditions. Each requirement must explicitly record:

- `frame_ref` — the accepted SF##;
- `origin` — `FROM_X | FROM_Y | FROM_GAP | FROM_BOUNDARY`;
- traceability to evidence;
- implementation independence;
- solution plurality;
- causal relevance to the gap;
- altitude check — stated at the need rather than workaround altitude;
- information gain — a mechanism adds implementation information rather than merely restating R.

Persist these six checks as booleans. Mark a requirement PASS only when all six are true, supporting evidence refs exist, and its frame is accepted by a human.

Freeze requirements before evaluating mechanisms. Hold x and y constant while comparing candidate f()s. If the accepted frame changes materially, invalidate the prior comparison and re-derive affected requirements.

## Concept generation

Generate enough materially different candidate shapes to test the requirements.

There is **no minimum concept quota**.

Do not invent weak alternatives merely to make the output symmetrical.

If only one credible mechanism emerges:

- say so;
- re-examine whether the requirements are too mechanism-specific;
- preserve the result if they are still valid.

## Compare

Run the first Fit Check as **Requirements × Shapes**.

For every M## record a binary `requirement_fit` result for every frozen PASS R## belonging to the same need. Unknown is not a pass. `requirement_ids` must match the requirements the candidate actually passes.

Do not alter x, y, or requirements merely to make a preferred mechanism win.

Selection is optional. Every M## records `selected_by_human` and `selection_note`.
The model must leave candidates and rejected mechanisms with
`selected_by_human = false`. If a human explicitly selects a shape, mark it SELECTED,
set `selected_by_human = true`, record the human's bounded selection rationale in
`selection_note`, and run the **Rotated Fit Check / reverse fit** as **Parts × Requirements**:

- decompose the selected shape into concrete parts;
- map every part to the R## it serves;
- remove or justify parts that serve no R;
- expose R with no supporting part;
- call out duplicated mechanisms or a single part carrying disproportionate responsibility.

A selected shape cannot remain selected without explicit human provenance or with an
unrun rotation.

## Write state

Update:

- `needs.json`;
- `shaping_frame.json`;
- `fit_criteria.json`;
- `concepts.json`;
- `change_log.json`.

## Phase handoff

After writing and validating this phase, follow
`references/phase-handoff.md`. For a file-backed study, derive the next move with
`scripts/next_research_move.py`; do not advance from invocation history alone.
