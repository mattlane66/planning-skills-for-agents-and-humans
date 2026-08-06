# Full modern agent workflow

This is the complete path for using the repo as a modern planning and harness layer.

Use it when work is large enough that a coding agent should not jump directly from a fuzzy request to implementation.

## Flow

Messy notes → frame → criteria → Appetite → sketch shapes ↔ candidate-shape breadboards or focused spikes when needed → fit check → reconcile visual evidence when present → human selects a bounded project and shape → reconcile selected-design breadboard ↔ return to shaping if detailed behavior exposes a consequential conflict → optional statechart → optional Dumplink creates sequenced vertical task groups → human selects the active task group or another demoable slice → contracts and executable examples as needed → optional kickoff reference → context packet with execution contract → build with drift checks → run log → reflection.

This is iterative, not a conveyor belt. Candidate breadboarding may support shaping before selection. Only an accepted selected-design breadboard can feed slicing and implementation.

When the bounded planning route itself spans multiple sessions, Wayfinding wraps the relevant planning stages as a coordination layer. Its map and tickets index work; accepted decisions still live in the stage artifacts below.

## Stages

| Stage | Purpose | Output |
| --- | --- | --- |
| Wayfinding, optional outer loop | Coordinate dependent planning decisions, evidence, prototypes, and prerequisites across sessions without creating a second source of truth. | `planning/wayfinding/<map>/map.md` and tickets |
| Frame | Name the current situation, problem, outcome, forces, and boundaries. | `planning/frame.md` |
| Criteria | Define the standards for judging fit before mechanisms take over. | requirements / criteria table |
| Appetite | Set the fixed time or scope budget, cut line, accepted uncertainty, and spike threshold before selection. | shaping Appetite section or `planning/appetite.md` |
| Sketch shapes | Make multiple solution shapes visible without selecting one; identify which candidates need deeper evidence. | candidate shapes + candidate-evidence requests |
| Candidate-shape breadboard, as needed | Clarify one named unselected candidate when its places, affordances, stores, consequences, or wiring must be understood before comparison. | exploratory candidate breadboard + fit implications; never build scope |
| Fit check | Compare shapes against criteria and Appetite, using candidate breadboards or spikes only as subordinate evidence. | fit check + reverse fit check + candidate-evidence summary |
| Sketch reconciliation, as needed | Map visual evidence to planning IDs, expose gaps or conflicts, and apply only accepted deltas. | `planning/sketch-reconciliation.md` plus synchronized source artifacts |
| Select shape | Record the human-selected direction and the candidate evidence to retain, revise, or discard. | selected direction + rejected alternatives + reconciliation plan |
| Selected-design breadboard | Reconcile the selected shape into accepted normative places, affordances, stores, consequences, branches, and wiring. Return consequential conflicts to shaping. | accepted `planning/breadboard.md` |
| Statechart, optional | Derive a precise behavioral view when a selected stateful scope is hard to reason about from wiring alone. | `planning/statechart.md` |
| Select project | Confirm the selected project as the discrete outer unit of work, with explicit outcome, boundary, exclusions, and Appetite. | `planning/shaping.md` |
| Dumplink, optional | Decompose the selected project into vertical task groups, dependency sequence, risk states, scope cuts, and a task-group approval gate. | `planning/dumplink.md` |
| Select active slice | Approve the Dumplink plan and choose an active task group, or choose another demoable slice when Dumplink is unnecessary. | `planning/slices.md` |
| Interface contracts | Define boundary-crossing data exchanges before agents guess field-level details. | `planning/interface-contracts.md` |
| Executable breadboard | Add fixtures, examples, expected outputs, edge cases, and acceptance tests. | `planning/executable-breadboard.md` |
| Kickoff, optional | Create a durable human-readable orientation map after selected artifacts converge; do not use it as build scope or sequence. | `planning/kickoff.md` |
| Context packet | Feed only the authoritative context relevant to the implementation agent; exclude candidate breadboards as active build scope. | `planning/context-packet.md` |
| Drift check | Keep implementation inside the selected slice and active task group. | strict drift-check output |
| Run log | Leave a durable audit trail after meaningful agent work. | `planning/runs/YYYY-MM-DD-short-task.md` |
| Reflection | Compare implementation reality to accepted intent and prepare or apply the explicit human drift decision. | `planning/breadboard-reflection.md` |

## Breadboard authority

- `current-state` is descriptive evidence about what exists.
- `candidate-shape` is exploratory evidence about one unselected shape during shaping.
- `selected-design` is normative intent after explicit human selection and reconciliation.

Candidate breadboards cannot select themselves, produce slices, govern implementation, or automatically become selected-design artifacts.

## Context packet must include

- active task
- source artifacts and authority order
- accepted requirements, Appetite, and cut line
- accepted selected-design behavior
- current slice
- relevant statechart rows, contracts, executable examples, and Dumplink task group when present
- explicit non-goals
- execution contract
- verification target

It must not treat a current-state or candidate-shape breadboard as selected build scope.

## Drift check output

A drift check must return only one of these two forms:

`No planning drift found.`

or:

`Planning drift found:` followed by selected artifact, current implementation direction, risk, and recommended move.

## Done standard

A modern agent workflow is complete when:

- any Wayfinding resolution is reflected in its canonical artifact and no map is treated as product truth
- requirements stayed separate from mechanisms
- Appetite and the cut line were explicit before shape selection
- candidate breadboards were used only where decision-relevant uncertainty justified them
- exploratory candidate evidence remained separate from accepted future intent
- the human-selected shape is explicit
- candidate rows were reconciled rather than automatically promoted
- consequential visual evidence was reconciled without silent scope or behavior changes
- only an accepted selected-design breadboard fed slice selection
- detailed breadboarding returned consequential conflicts to shaping for an explicit decision
- statechart states and transitions remain traceable to the selected-design breadboard when a statechart is present
- boundary contracts are explicit where needed
- executable examples and edge cases exist where needed
- Dumplink task groups are vertical and risk-aware
- the context packet excludes candidate breadboards as build scope and includes an execution contract
- drift checks use the strict output format
- meaningful agent work leaves a run log
- reflection preserves accepted intent and implementation reality separately, with an explicit decision governing any update
