# Phase D — Evidence Freeze

Use for STANDARD and FULL studies.

Reopen:

- all source/evidence/LU/lineage/coverage state;
- `../PROTOCOL.md`.

Do not perform opportunity ideation.

## Sufficiency gate

Before freezing, write `sufficiency.json` and assess each dimension as NOT_ASSESSED | SUFFICIENT | INSUFFICIENT:

- trend support;
- pivotal LU qualification;
- contradiction search, including targeted hypothesis refutation and contrastive cases;
- lineage resolution;
- pyramid coverage;
- marginal value of another proportionate evidence batch.

For each dimension record its own rationale, supporting structured refs when
available, and exact next actions when insufficient. Do not rely on one overall
rationale to justify six separate judgments.

Do not substitute a source/user quota for this judgment. SUFFICIENT means the corpus is adequate for the intended decision and another proportionate batch is unlikely to change the decision enough to justify delaying synthesis.

If a consequential branch now requires direct contact, record the fieldwork referral rather than pretending more public search resolves it.

## Audit

Check:

- source coverage honesty;
- evidence IDs and references;
- LU1/LU2 qualification;
- trend references;
- derivative versus independent evidence;
- unresolved UNKNOWNs;
- contradictions and outliers;
- coverage bias;
- important inaccessible/private populations;
- whether advanced analogs were meaningfully investigated;
- hypothesis ledgers and important contrastive cases;
- whether decision-critical observability questions are resolved by traces, explicitly accepted as unknown, or converted into targeted fieldwork referrals;
- whether every AI analysis run referenced by frozen evidence passed sampled validation.

Run deterministic validation when available.

Do not claim the model independently verified its own interpretation.

Record separately:

- human review status;
- deterministic validation status;
- interpretive status;
- model checklist completion if performed.

## Freeze decision

If and only if `sufficiency.status = SUFFICIENT` and the evidence corpus is structurally coherent enough for synthesis:

- set `sufficiency.repair_status = NOT_REQUIRED`;
- set `freeze.status = FROZEN`;
- record exact evidence, qualified-LU, and independent-lineage counts from current state;
- record unresolved gaps;
- refuse freeze while a decision-critical observability item remains OPEN;
- refuse freeze when evidence depends on an AI analysis run whose sampled validation has not PASSED.

If not:

- leave OPEN;
- set sufficiency to INSUFFICIENT on the relevant dimensions;
- set `sufficiency.repair_status = REQUIRED` before returning to Phase B or C;
- mark interpretive status PROVISIONAL;
- identify the exact highest-information evidence work or fieldwork referral needed.

When Phase D follows a completed repair, reassess all six dimensions rather than
copying the prior result. A still-insufficient result starts a new repair cycle by
setting `repair_status = REQUIRED`; a sufficient result clears it to `NOT_REQUIRED`.

## Post-freeze rule

Later evidence may be added, but every post-freeze search must record:

- why it was sought;
- what interpretation/question triggered it;
- what state changed as a result.

## Phase handoff

After writing and validating this phase, follow
`references/phase-handoff.md`. For a file-backed study, derive the next move with
`scripts/next_research_move.py`; do not advance from invocation history alone.
