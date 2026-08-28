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
- contradiction search;
- lineage resolution;
- pyramid coverage;
- marginal value of another proportionate evidence batch.

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
- whether advanced analogs were meaningfully investigated.

Run deterministic validation when available.

Do not claim the model independently verified its own interpretation.

Record separately:

- human review status;
- deterministic validation status;
- interpretive status;
- model checklist completion if performed.

## Freeze decision

If and only if `sufficiency.status = SUFFICIENT` and the evidence corpus is structurally coherent enough for synthesis:

- set `freeze.status = FROZEN`;
- record exact evidence, qualified-LU, and independent-lineage counts from current state;
- record unresolved gaps.

If not:

- leave OPEN;
- set sufficiency to INSUFFICIENT on the relevant dimensions;
- mark interpretive status PROVISIONAL;
- identify the exact highest-information evidence work or fieldwork referral needed.

## Post-freeze rule

Later evidence may be added, but every post-freeze search must record:

- why it was sought;
- what interpretation/question triggered it;
- what state changed as a result.
