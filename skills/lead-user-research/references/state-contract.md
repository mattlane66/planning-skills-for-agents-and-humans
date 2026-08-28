# Study State Contract

The study state is deliberately plain JSON so any tool-using AI can read and write it.

The files, not chat memory, are authoritative when file tools are available.

## Core files

### `manifest.json`

Tracks:

- protocol version;
- mode;
- current phase;
- study execution level — `DESK_RESEARCH | FIELDWORK_ENRICHED | FULL_LEAD_USER_PROJECT`;
- study execution basis;
- human review;
- deterministic validation;
- interpretive status;
- model-check status;
- timestamps.

### `decision.json`

Tracks:

- domain / problem space;
- target market;
- what the research should understand;
- human decision the research should inform;
- innovation altitude;
- starting hypotheses;
- discovery seeds;
- candidate-profile hypotheses;
- search constraints;
- scope;
- assumptions;
- consequential unknowns;
- disconfirming evidence;
- out-of-scope questions.

The learning objective (`what_to_understand`) and decision are separate fields and must not be silently merged.

`discovery_seeds`, `candidate_profile_hypotheses`, and `search_constraints` are arrays that preserve the human's supplied wording. Seeds and candidate-profile hypotheses guide discovery but do not count as LU1/LU2 evidence or close the search universe. Search constraints are the only one of these three fields that impose hard discovery boundaries.

### `trends.json`

Array of:

- `trend_id` — `T##`;
- statement;
- direction;
- evidence refs;
- observable indicators;
- importance;
- status.

### `candidates.json`

Experts, referral nodes, Lead User candidates, or user innovators discovered before qualification.

### `sources.json`

Array of:

- `source_id` — `SRC##`;
- title;
- creator;
- URL or immutable identifier;
- source type;
- coverage — `FULL | PARTIAL | UNREADABLE | UNKNOWN`;
- coverage note;
- access date.

### `evidence.json`

Array of atomic evidence:

- `evidence_id` — `E###`;
- `source_id`;
- exact location when available;
- evidence type;
- verbatim excerpt or bounded observation;
- user/entity;
- `trend_id` when known;
- `lu_id` when known;
- caveat.

### `lu_episodes.json`

Array of bounded Lead User Need Episodes:

- `lu_id` — `LU##`;
- user/entity;
- `trend_id`;
- need statement;
- context;
- status — `CANDIDATE | QUALIFIED | REJECTED`;
- `lu1_evidence`;
- `lu2_evidence`;
- baseline;
- alternatives;
- user response;
- desired progress;
- observed result;
- optional `trace` for pivotal episodes;
- unknowns.

When present, `trace` contains:

- `status` — `NOT_ASSESSED | PARTIAL | SUFFICIENT`;
- `initiating_condition`;
- `prior_approach`;
- `switch_or_change_trigger`;
- `expected_improvement`;
- `sequence` — ordered steps with action, context, result, and `evidence_refs`;
- `fit_points` — consequential points with step reference, observed behavior, compensating behavior, stated purpose, inferred purpose, UNKNOWNs, and `evidence_refs`;
- `actual_outcome`;
- `evidence_refs` — episode-level trace support when evidence applies across multiple trace fields;
- `unknowns`.

`SUFFICIENT` means sufficient for the intended downstream interpretation, not complete knowledge of the episode.

A trace is optional and is not part of Lead User qualification. A QUALIFIED episode must contain valid evidence references for both LU1 and LU2 regardless of trace status.

A QUALIFIED episode must also record:

- `lu1_rationale` — why the cited evidence establishes advancement on the relevant trend;
- `advancement_indicator` — the observable indicator placing this user/episode ahead;
- `lu2_rationale` — why the cited evidence establishes unusually high expected benefit;
- `benefit_signal` — the concrete signal of unusually high expected benefit;
- `qualification_caveats` — unresolved weaknesses or alternate explanations.

The same atomic evidence may support LU1 and LU2 only when the rationales show why it legitimately bears on both.

### `lineage.json`

Array of lineage / independence assessments:

- `lineage_id` — `L##`;
- `member_refs` — source or LU refs being assessed together;
- `relationship` — `SAME_CREATOR | FORK | DEPENDENCY | ADAPTATION | COPIED_TECHNIQUE | COMMON_UPSTREAM | SHARED_ORGANIZATION | SHARED_COMMUNITY | INDEPENDENT_REDISCOVERY | OTHER`;
- `independence` — `INDEPENDENT | DERIVATIVE | RELATED | UNKNOWN`;
- `evidence_refs`;
- rationale.

Use one `INDEPENDENT` record per genuinely independent innovation lineage when counting independent support.

### `coverage.json`

Tracks discovery bias:

- likely overrepresented populations;
- likely underrepresented populations;
- inaccessible/private areas;
- languages/regions searched;
- corrective discovery actions;
- interview/fieldwork referrals.

### `search_log.json`

Major search families, pyramiding hops, analog pivots, and abandoned branches.

Do not record every trivial query.

### `sufficiency.json`

For STANDARD/FULL, records the interpretive stopping decision before Evidence Freeze:

- overall status — `NOT_ASSESSED | SUFFICIENT | INSUFFICIENT`;
- trend support;
- LU qualification;
- contradiction search;
- lineage resolution;
- pyramid coverage;
- marginal value of another evidence batch;
- rationale;
- unresolved actions.

The six dimensions use the same `NOT_ASSESSED | SUFFICIENT | INSUFFICIENT` values.

`SUFFICIENT` is a decision-relative judgment, not a quota. It means the evidence corpus is adequate for the intended interpretation and another proportionate evidence batch is unlikely to change the decision enough to justify delaying synthesis. Unresolved high-value branches may instead be recorded as fieldwork referrals.

### `change_log.json`

Material analytical changes:

- merges;
- splits;
- renames;
- recoding;
- requalification;
- lineage corrections;
- cluster changes;
- requirement changes;
- decision changes.

### `freeze.json`

For STANDARD/FULL, only after `sufficiency.status = SUFFICIENT`:

- status — `OPEN | FROZEN`;
- freeze timestamp;
- evidence counts;
- qualified episode count;
- independent lineage count;
- unresolved gaps;
- post-freeze evidence log.

### `findings.json`

Array of:

- `finding_id` — `F##`;
- claim;
- epistemic label — `VERIFIED | INFERRED | SPECULATIVE | UNKNOWN`;
- evidence refs;
- LU refs;
- contradictions;
- confidence rationale.

A VERIFIED finding requires at least one valid evidence reference.

### `needs.json`

Array of:

- `need_id` — `N##`;
- statement;
- supporting finding IDs;
- relevant trends;
- propagation status;
- contradictions;
- concept gate status — `PASS | FAIL | NOT_ASSESSED`;
- concept gate rationale.

### `principles.json`

Transferable solution principles, expressed without prescribing one implementation.

### `fit_criteria.json`

Array of:

- `requirement_id` — `R##`;
- `need_id`;
- requirement;
- evidence refs;
- `traceability` — boolean;
- `implementation_independence` — boolean;
- `solution_plurality` — boolean;
- `causal_relevance` — boolean;
- `altitude_check` — boolean;
- `information_gain` — boolean;
- status — `PASS | FAIL | PROVISIONAL`.

A PASS requirement must have evidence refs and all six checks true.

### `concepts.json`

Array of:

- `concept_id` — `M##`;
- `need_id`;
- mechanism;
- requirement IDs;
- assumptions;
- risks;
- evidence needed next.

No minimum concept count is required.

### `decision_outcome.json`

Structured human-action state written before rendering the Decision Brief:

- status — SCOUT: `STOP | INVESTIGATE | ESCALATE`; STANDARD/FULL: `ACT | TEST | HOLD | REJECT`;
- recommendation;
- why;
- decisive finding refs;
- decisive LU refs;
- critical uncertainties;
- action now;
- conditions that would change the decision;
- what the evidence supports;
- what the evidence does not support;
- contradictions / alternate explanations;
- recommended next evidence;
- priority human review.

When file tools are available, render `outputs/decision-brief.md` from this state with `scripts/render_decision_brief.py` so the human-facing report cannot silently diverge from the structured decision.

## Study execution level

`manifest.study_execution_level` describes what the study actually did, not its ambition:

- `DESK_RESEARCH` — public/documentary/AI-assisted research without material direct fieldwork;
- `FIELDWORK_ENRICHED` — direct interviews, observation, or other fieldwork materially informs the research;
- `FULL_LEAD_USER_PROJECT` — direct Lead User/expert participation supports both need/solution learning and collaborative concept development.

`FULL_LEAD_USER_PROJECT` requires `study_execution_basis` to include `direct_lead_user_participation` and `direct_concept_development_participation`. AI-generated concept shaping from public evidence remains `DESK_RESEARCH`.

## Authority

When records disagree:

1. latest explicit human decision;
2. persisted reviewed/validated state;
3. current structured state;
4. narrative summaries;
5. conversational memory.

Never silently rewrite reviewed human decisions.
