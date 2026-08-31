# Phase E — Interpret

At the start, reopen the persisted frozen evidence state.

Do not synthesize from conversational recollection.

For STANDARD/FULL, do not proceed if `freeze.status` is not FROZEN.

## 1. Need abstraction

For each major case distinguish:

> observed situation → emerging need → user mechanism → transferable principle

Do not copy the workaround into the need.

Trace first; isolate now. For traced episodes, decide only after Evidence Freeze which fit points represent consequential problems or emerging needs. When a finding or need materially derives from a trace, persist exact `trace_refs` such as `LU1:S1` or `LU1:FP1`.

## 2. Limited Christensen lens

Only now ask:

- circumstance;
- struggle;
- prior solution;
- desired progress;
- compensating behavior.

When an LU episode has a trace, run this interpretation against the traced sequence and its cited atomic evidence.

Keep separate:

- OBSERVED behavior;
- STATED purpose;
- INFERRED purpose;
- UNKNOWN elements.

Do not fill missing circumstance, chronology, struggle, prior solution, desired progress, motivation, or compensating purpose merely because they would make the story coherent.

Do not turn this into a separate JTBD study.

## 3. Findings

Create `F##` with:

- VERIFIED / INFERRED / SPECULATIVE / UNKNOWN;
- evidence refs;
- LU refs;
- trace refs when materially derived from a trace;
- contradictions.

## 4. Emerging needs

Create `N##` based on evidence, not mention count. Persist `trace_refs` when the need materially depends on one or more traced steps or fit points.

Cluster at LU-episode level when useful.

Valid outcomes include:

- one cluster;
- several;
- provisional groups;
- outliers;
- no useful clustering.

Do not force 3–5 themes.

## 5. Backcoding

When a need definition materially changes:

- revisit earlier episodes;
- revisit uncoded evidence;
- record the change.

## 6. Solution principles

Create implementation-flexible `SP##`.

## 7. Propagation and transferability

Classify propagation for each important need:

- strong propagation evidence;
- plausible propagation;
- Lead-user-specific.

Do not infer prevalence.

Separately create `transferability_assessment` for each important need:

- `status`: SUPPORTED | PLAUSIBLE | LEAD_USER_BOUND | UNKNOWN;
- rationale;
- evidence refs;
- `target_market_differences`: consequential differences in cost tolerance, expertise, maintenance burden, safety, regulation, infrastructure, workflow disruption, or other constraints.

Transferability asks whether the underlying need/principle plausibly survives outside the extreme user's special conditions. It is not a prevalence estimate. A Lead User workaround may be non-transferable while the underlying need remains transferable.

## 8. Contradictions and hypothesis disposition

Actively test the strongest interpretations against contrary evidence, formal contrastive cases, rival explanations, and coverage gaps.

After the frozen corpus has been interpreted, update each consequential H## to exactly one of:

UNTESTED | SURVIVED_CURRENT_TESTS | WEAKENED | REJECTED | UNTESTABLE

Record the update rationale and boundary conditions. Never use CONFIRMED.

## Write state

Update:

- `findings.json`;
- `needs.json`;
- principles.json;
- hypotheses.json;
- change_log.json.

After the entire frozen corpus has been interpreted, set
`manifest.interpretation_completion = COMPLETED`. This marker is required even when
the supported result is explicitly negative and `findings.json`, `needs.json`, and
`principles.json` are all empty. Do not use empty arrays alone to imply that Phase E
ran. Leave the marker `NOT_STARTED` until the full frozen corpus has actually been
considered.

Do not create concepts in this phase.

## Phase handoff

After writing and validating this phase, follow
`references/phase-handoff.md`. For a file-backed study, derive the next move with
`scripts/next_research_move.py`; do not advance from invocation history alone.
