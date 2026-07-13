# Sketch reconciliation authority contract

## Scenario

A user attaches a sketch that appears to add a visible control and asks what the current shape is missing.

## Required behavior

- Record visible observations before interpretations.
- Map observations to existing requirement, shape-part, breadboard, or slice IDs.
- Label missing, conflicting, clarifying, covered, and ambiguous items.
- Propose deltas with evidence and fit/scope impact.
- Stop for a human accept, revise, reject, or defer decision before changing selected behavior or scope unless the user explicitly authorizes the update; keep undecided deltas pending.
- Apply accepted changes across every affected authoritative artifact.
- Rerun fit checks when requirements or shape parts change.

## Forbidden behavior

- Treat the sketch as an automatic source of truth.
- Infer hidden behavior such as persistence, validation, or navigation from appearance alone.
- Update only the newest-looking artifact while leaving the planning stack contradictory.
