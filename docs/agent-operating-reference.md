# Agent Operating Reference

Use this document when an active skill needs detailed authority, preservation, or drift rules. It is not intended to sit in every agent context.

## Planning levels

1. Frame / problem boundary — source, current situation, problem, desired outcome, boundary
2. Working shaping — provisional requirements, candidate shapes, Working Appetite, Working fit checks, focused spikes, and candidate evidence
3. Accepted shaping decisions — Accepted requirements, Accepted Appetite/cut line, selected shape, cuts, and explicit human selection
4. Selected-design behavior — reconciled accepted breadboard and any derived state model
5. Selected project — the bounded discrete unit of work
6. Dumplink and slices — project decomposition into vertical task groups and human-selected active scope
7. Contracts and executable evidence — selected detail for complex behavior or boundaries
8. Implementation reality — code, tests, logs, and observed behavior

A lower level may reveal that a higher-level assumption was wrong, but it does not silently rewrite accepted higher-level truth.

Collaborative shaping may move fluidly within level 2: R, S, fit, spikes, sketches, and candidate breadboards can inform one another in any useful order. Promotion from Working shaping into level 3 requires the applicable human gates. The gated/orchestrated profile may impose stricter prerequisites within level 2, but it does not change authority.

Wayfinding sits outside these authority levels. Its maps and tickets coordinate questions across sessions and link to the applicable level; they never replace the artifact that owns a decision.

## Concern-specific authority

- problem and outcome: accepted frame or explicit selected project boundary
- exploratory requirements and mechanisms: Working shaping material
- fitness used for selection: Accepted requirements + decision-ready fit evidence
- budget and cut line: Accepted Appetite
- selected mechanisms: human-selected shape
- concrete accepted future behavior: selected-design breadboard
- outer scope: selected project boundary
- active scope: selected Dumplink task group or other selected slice
- state semantics: selected-design breadboard, with statechart as a derived view
- boundary fields and errors: selected interface contract
- expected examples and results: executable breadboard
- task grouping and order: approved Dumplink plan
- actual behavior: implementation evidence

When two artifacts disagree, first identify which concern is in conflict and whether each claim is Working or Accepted. Working material can be revised directly when the user is still exploring. Accepted material requires a proposed delta and explicit decision.

## Shaping authority

### Working material

May include:

- Working R
- candidate S
- Working Appetite
- Working fit/reverse-fit
- focused spikes
- candidate breadboards
- exploratory sketches/prototypes

These are legitimate inputs to one another. A solution can reveal a requirement; a fit failure can revise a shape; a spike can change both. None of this grants build authority.

### Accepted shaping decisions

Before shape selection, require:

- clear-enough problem boundary
- Accepted requirements
- Accepted Appetite and cut line
- decision-ready fit/reverse-fit/Appetite implications
- explicit human selection

Candidate evidence may support this decision but cannot make it or promote itself.

### Candidate evidence

A candidate breadboard or prototype may use Working R or Unset/Working Appetite in collaborative mode. If so, dependent fit/Appetite claims remain provisional and must be revalidated before final selection.

After selection, candidate rows become selected-design intent only through explicit reconciliation.

## Advanced artifact preservation

### Wayfinding

Preserve:

- one bounded destination and exit check
- ticket names, blockers, claims, and canonical targets
- the distinction between precise tickets, in-scope fog, and out-of-scope work
- one linked gist per resolved route decision

Do not treat ticket closure as acceptance, duplicate full decisions into the map, or convert unresolved planning questions into an implementation backlog.

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

- selected project outcome, boundary, exclusions, and Appetite
- all proposed vertical task groups and their included task IDs
- active task group and vertical boundary
- dependencies and risk states
- build sequence
- appetite-based cuts
- acceptance checks and stop condition

Do not ask for a pre-existing slice, flatten vertical groups into a generic horizontal backlog, or let a group expand the selected project. Deferred groups remain out of active scope until a human selects them or changes the project or Appetite.

### Kickoff document

Use for durable orientation. It may summarize accepted artifacts but does not govern build scope, field-level behavior, or task sequence.

### Run log

Use as an audit record of files changed, decisions made, verification performed, and unresolved issues. It never replaces an authoritative planning artifact.

## Change ripple procedure

When a planning or implementation discovery changes a material assumption:

1. identify the authoritative concern
2. identify whether the affected material is Working or Accepted
3. record what the current artifact says
4. record what the new evidence shows
5. name affected upstream and downstream artifacts
6. if material is Working, revise it visibly and continue the shaping loop
7. if material is Accepted, propose one of: update plan, cut/split scope, update code, or create a new bet, and obtain the required human decision
8. update authoritative artifacts and regenerate derived views
9. mark stale artifacts explicitly when they cannot be updated in the same operation

## Context packet authority

A context packet is a projection, not a new source of truth. It should:

- cite source artifacts
- state authority order
- include only Accepted sections needed for the task
- exclude Working alternatives and candidate breadboards as active build scope
- preserve canonical project terms and relevant ADRs
- keep non-goals close to the active task
- include return-to-planning conditions
- report incomplete verification directly

## Implementation return conditions

Stop and return to planning when:

- the selected slice cannot be implemented within the Accepted Appetite
- required behavior is absent from selected artifacts
- field-level contract decisions are missing
- a prototype or code path contradicts a material accepted assumption
- a required test seam or architectural boundary does not exist
- implementing the next step would expand scope or reverse an explicit non-goal

## No silent drift

The acceptable outcomes are:

- implementation changes to match accepted intent
- accepted intent changes because evidence disproved an assumption and a human authorizes the delta
- scope is cut or split
- a new bet is created

Continuing while allowing accepted plan and code to diverge silently is not an acceptable outcome.
