# Artifact Consistency Reference

Load this reference when an accepted planning stack already exists, a lower-level discovery changes an assumption, or multiple artifacts disagree.

## Levels

1. Frame — source, problem, outcome, boundary
2. Shaping — requirements, appetite, candidate shapes, selection
3. Breadboard and slices — concrete behavior and increments
4. Contracts and executable evidence — boundary detail and expected examples
5. Implementation plans — build grouping and sequence

Each lower level adds detail without gaining authority over concerns owned above it.

## Change procedure

Whenever changing an artifact:

1. identify the level and concern being changed
2. identify upstream assumptions and downstream dependents
3. preserve the current accepted truth before proposing a change
4. show the proposed delta and its evidence
5. obtain the required human decision
6. update all affected authoritative artifacts in the same operation when practical
7. regenerate derived views after their source changes

## Concern-specific authority

Authority is not simply newest-file-wins.

- the frame governs the problem, desired outcome, and boundary
- accepted requirements govern fitness
- appetite governs budget and cut line
- the selected shape governs mechanisms
- the selected slice governs active scope
- a boundary contract governs its named exchange
- executable examples govern expected results for their selected slice
- a task-group plan governs build grouping and order without expanding scope

Raw notes, rejected alternatives, sketches, generated diagrams, kickoff documents, and run logs do not silently outrank accepted artifacts.

## Lower-level discoveries

A breadboard, prototype, contract, or implementation may reveal that an earlier assumption was wrong. Preserve both truths:

- what the accepted artifact currently says
- what reality now shows

Then choose one explicit move:

- update the lower-level work to match the plan
- update the upstream artifact because the assumption was wrong
- cut or split the selected scope
- create a new bet

Silent drift is the failure.

## Visual evidence

When a sketch, screenshot, wireframe, mockup, or whiteboard introduces behavior or scope not present in accepted artifacts, use `sketch-reconciliation`. Separate observation from interpretation and apply only accepted deltas.

## Stable IDs

Preserve established IDs so changes remain traceable. Do not rename IDs for style. When meaning changes materially, create a new ID or an explicit planning update.

## Completion check

An artifact update is complete only when:

- the changed concern has one clear authoritative source
- affected downstream artifacts are updated or explicitly marked stale
- derived views are regenerated when needed
- rejected or superseded material remains legible as history
- no implementation scope was introduced without a human decision
