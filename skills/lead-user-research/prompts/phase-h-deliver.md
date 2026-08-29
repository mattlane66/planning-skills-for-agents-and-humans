# Phase H — Deliver

Use only when proportionate and when the environment actually supports the requested artifacts.

Reopen the complete structured state before rendering.

## Canonical source

The structured research state is the authoritative analytical record. The Markdown Decision Brief is the canonical human-facing report.

When file tools are available, regenerate the Decision Brief from `decision_outcome.json` with `scripts/render_decision_brief.py` before producing derived views.

After delivery checks pass, set `manifest.phase` to `H`, `manifest.study_status` to
`COMPLETE`, and `manifest.model_check` to `COMPLETED`. Regenerate the brief after final
state changes and run deterministic validation again so its completion markers are
current. COMPLETE does not imply human review; keep `human_review` separate.

PDF and HTML are derived from the same research state and must not introduce new substantive claims.

## SCOUT

Normally skip this phase.

A Decision Brief is usually enough.

## STANDARD

Canonical Markdown + structured state are the default.

Generate PDF/HTML only when requested or clearly useful.

## FULL

When supported, produce:

1. Markdown Decision Brief + structured state;
2. polished PDF;
3. interactive HTML.

FULL run mode does not itself imply FULL_LEAD_USER_PROJECT. Surface the actual study execution level in outward-facing delivery.

The HTML may support progressive disclosure:

> conclusion → finding → LU episode → evidence → source

Useful filters include:

- trend;
- need;
- LU episode;
- evidence strength;
- source coverage;
- review status;
- contradictions;
- lineage.

## Cross-format checks

Verify mechanically where possible:

- IDs match;
- numerical values match;
- epistemic labels match;
- source coverage matches;
- UNKNOWN stays UNKNOWN;
- contradictions remain visible;
- derived outputs contain no substantive claim absent from canonical Markdown.
- internal identities and non-approved source URLs remain absent;
- PASS, PROVISIONAL, and FAIL shaping records remain visibly distinct;
- structured operational actions remain complete across formats.

## Capability honesty

If PDF generation, HTML generation, interactive validation, browser testing, or another delivery capability is unavailable:

- say so;
- deliver the strongest supported subset;
- never fabricate the artifact or verification result.
