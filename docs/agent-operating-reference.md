# Agent Operating Reference

Use this document when an active skill needs detailed authority, preservation, or drift rules. It is not intended to sit in every agent context.

## Planning levels

1. Frame — source, current situation, problem, desired outcome, boundary
2. Shaping — accepted requirements, Appetite, candidate mechanisms, fit, human selection
3. Breadboard and slices — concrete behavior and active scope
4. Statechart, contracts, and executable evidence — selected detail for complex behavior or boundaries
5. Dumplink — task grouping and sequence inside a selected slice
6. Implementation reality — code, tests, logs, and observed behavior

A lower level may reveal that a higher-level assumption was wrong, but it does not silently rewrite that higher-level truth.

## Concern-specific authority

- problem and outcome: frame
- fitness: accepted requirements
- budget and cut line: Appetite
- mechanisms: selected shape
- active scope: selected slice
- state semantics: selected breadboard, with statechart as a derived view
- boundary fields and errors: selected interface contract
- expected examples and results: executable breadboard
- task grouping and order: selected Dumplink plan
- actual behavior: implementation evidence

When two artifacts disagree, first identify which concern is in conflict. Then preserve both claims and prepare an explicit decision.

## Advanced artifact preservation

### Statechart

Preserve:

- selected scope
- source breadboard IDs
- states, events, guards, effects, and destinations
- explicit gaps and assumptions

Do not invent retries, cancellation, timeout, failure, hierarchy, or parallel behavior. Update the breadboard first when the model changes.

### Interface contract

Preserve:

- contract ID and boundary
- field names
- required and optional distinctions
- enum values and nullability
- units
- branches and errors
- open decisions

Flag missing field-level decisions instead of inventing them during implementation.

### Executable breadboard

Preserve:

- selected slice
- relevant places, affordances, stores, and wires
- fixtures or starting data
- example runs
- expected visible results
- state changes and side effects
- edge cases and acceptance tests
- open decisions

Examples are authoritative for their named slice but may not expand it.

### Dumplink

Preserve:

- active task group and vertical boundary
- dependencies and risk states
- build sequence
- appetite-based cuts
- acceptance checks and stop condition

Do not flatten vertical groups into a generic horizontal backlog. Deferred groups remain out of scope until a human changes the slice or Appetite.

### Kickoff document

Use for durable orientation. It may summarize accepted artifacts but does not govern build scope, field-level behavior, or task sequence.

### Run log

Use as an audit record of files changed, decisions made, verification performed, and unresolved issues. It never replaces an authoritative planning artifact.

## Change ripple procedure

When a planning or implementation discovery changes a material assumption:

1. identify the authoritative concern
2. record what the accepted artifact says
3. record what the new evidence shows
4. name affected upstream and downstream artifacts
5. propose one of: update code, update plan, cut or split scope, or create a new bet
6. obtain the required human decision
7. update authoritative artifacts and regenerate derived views
8. mark stale artifacts explicitly when they cannot be updated in the same operation

## Context packet authority

A context packet is a projection, not a new source of truth. It should:

- cite source artifacts
- state authority order
- include only the selected sections needed for the task
- preserve canonical project terms and relevant ADRs
- keep non-goals close to the active task
- include return-to-planning conditions
- report incomplete verification directly

## Implementation return conditions

Stop and return to planning when:

- the selected slice cannot be implemented within the accepted Appetite
- required behavior is absent from the selected artifacts
- field-level contract decisions are missing
- a prototype or code path contradicts a material assumption
- a required test seam or architectural boundary does not exist
- implementing the next step would expand scope or reverse an explicit non-goal

## No silent drift

The acceptable outcomes are:

- implementation changes to match intent
- intent changes because evidence disproved an assumption
- scope is cut or split
- a new bet is created

Continuing while allowing plan and code to diverge is not an acceptable outcome.
