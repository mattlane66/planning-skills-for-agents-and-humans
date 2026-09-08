# Phase F — Shape

This phase is optional.

Read `../PACKAGE_BOUNDARY.md` before running this phase. Phase F is a **research-local concept-shaping exercise**. It may make evidence-backed design implications concrete enough to learn from them, but it does not create accepted product-planning truth, selected-design intent, active scope, or build authorization.

At the start, reopen:

- frozen evidence;
- findings;
- needs;
- principles;
- existing `shaping_frame.json`;
- existing fit criteria and concepts.

## Planning-authority boundary

The v1.x state schema retains `ACCEPTED`, `R##`, and `SELECTED` fields for compatibility. Interpret them only inside the research study:

- `SF## status = ACCEPTED` means the human accepted the frame as a defensible **research concept-evaluation frame**. It is not an accepted planning frame or `framing-doc`.
- `R##` rows in `fit_criteria.json` are **research-local fit criteria**. Downstream planning cites them with a namespaced research reference such as `LUR:<workspace>:R1`; they do not automatically own the project's `R##` namespace.
- `M## selection_status = SELECTED` means a human selected or preferred a mechanism within the research study for the decision being informed. It is not a selected project shape, selected-design breadboard, selected slice, or implementation instruction.

Do not claim that Phase F satisfies planning Appetite, project shape-selection, selected-design reconciliation, slicing, or build gates.

## Concept Generation Gate

A need may proceed only when:

1. its trend is credible;
2. at least one qualified LU episode supports it;
3. the need is separable from the observed workaround;
4. evidence is sufficient to derive meaningful fitness conditions;
5. no unresolved contradiction makes concept work premature;
6. the underlying need/principle has a defensible transferability assessment and is not merely an artifact of exceptional Lead User constraints.

Record PASS / FAIL / NOT_ASSESSED and rationale in `needs.json`.

Persist the six gate tests as `concept_gate_checks` booleans, including `transferability_supported`. PASS requires all six
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

This is the research study's concept-evaluation frame, not the Phase A research frame and not an accepted product-planning frame.

When the frame is first constructed, write it as PROVISIONAL and stop for explicit human review before treating it as the stable basis for research concept comparison. A model must not set `status = ACCEPTED` or `accepted_by_human = true` without an explicit human decision.

Only after the research-local frame is ACCEPTED derive R## fitness conditions. Each criterion must explicitly record:

- `frame_ref` — the accepted research-local SF##;
- `origin` — `FROM_X | FROM_Y | FROM_GAP | FROM_BOUNDARY`;
- traceability to evidence;
- implementation independence;
- solution plurality;
- causal relevance to the gap;
- altitude check — stated at the need rather than workaround altitude;
- information gain — a mechanism adds implementation information rather than merely restating the criterion.

Persist these six checks as booleans. Mark a criterion PASS only when all six are true, supporting evidence refs exist, and its research-local frame is accepted by a human.

Freeze the research-local criteria before evaluating mechanisms. Hold x and y constant while comparing candidate f()s. If the accepted research-local frame changes materially, invalidate the prior comparison and re-derive affected criteria.

Do not treat these R## rows as accepted project requirements. Their identity is local to the research workspace until the research-to-planning handoff maps them into project planning with explicit provenance.

## Concept generation

Generate enough materially different candidate mechanisms to test the research-local fit criteria.

There is **no minimum concept quota**.

Do not invent weak alternatives merely to make the output symmetrical.

If only one credible mechanism emerges:

- say so;
- re-examine whether the criteria are too mechanism-specific;
- preserve the result if they are still valid.

## Compare

Run the first Fit Check as **Research-local criteria × candidate mechanisms**.

For every M## record a binary `requirement_fit` result for every frozen PASS R## belonging to the same need. Unknown is not a pass. `requirement_ids` must match the criteria the candidate actually passes. The legacy field names remain for workspace compatibility.

Do not alter x, y, or criteria merely to make a preferred mechanism win.

Selection is optional. Every M## records `selected_by_human` and `selection_note`.
The model must leave candidates and rejected mechanisms with
`selected_by_human = false`. If a human explicitly selects or prefers a mechanism **for the research study**, mark it SELECTED,
set `selected_by_human = true`, record the human's bounded research rationale in
`selection_note`, and run the **Rotated Fit Check / reverse fit** as **Parts × criteria**:

- decompose the selected research mechanism into concrete parts;
- map every part to the R## it serves;
- remove or justify parts that serve no criterion;
- expose criteria with no supporting part;
- call out duplicated mechanisms or a single part carrying disproportionate responsibility.

A research-local selected mechanism cannot remain selected without explicit human provenance or with an unrun rotation. Its SELECTED state still does not authorize a project shape or implementation.

## Layer-preserving rejection

If a candidate mechanism or implementation part is rejected for technical, economic, safety, regulatory, operational, or timing reasons, persist a `rejection_record` with:

- `layer`: NEED | PRINCIPLE | REQUIREMENT | MECHANISM | IMPLEMENTATION_PART;
- rationale;
- evidence refs when applicable.

A lower-layer rejection does not automatically invalidate a higher evidence layer. In particular:

> reject mechanism ≠ reject requirement ≠ reject need

Changing an evidenced need, principle, or research-local fit criterion requires separate evidence/rationale.

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

When the completed research is handed into product planning, preserve the Phase F records and human provenance as research evidence. Do not rebuild them merely because the package boundary changed. An accepted handoff with useful Phase F material normally enters `shaping` in collaborative mode as **Working** planning material; planning promotion gates still govern acceptance, Appetite, project selection, and build scope.
