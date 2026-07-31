# Agent Workflow

Use this workflow when an agent is helping turn unclear product work into buildable planning artifacts and implementation handoffs.

The workflow is tool-neutral. It works with Claude Code, Cursor, Codex, Gemini CLI, and other agentic environments. The exact invocation differs by tool; the planning discipline should stay the same.

For machine-readable orchestration, use `.agent-orchestration.yaml`.

This is not a conveyor belt. Shaping can invoke candidate-shape breadboarding or focused spikes before selection. Selected-design breadboarding can return consequential discoveries to shaping after selection.

## 0. Wayfinding, optional outer loop

Use when a bounded planning destination requires multiple dependent decisions, investigations, or prototypes across sessions.

Outputs:

- one low-resolution Wayfinding map
- precise decision, evidence, prototype, and prerequisite tickets
- blockers and a queryable frontier
- in-scope fog and explicit out-of-scope work
- an exit check tied to a canonical artifact or human gate

Use `wayfinding` or `/wayfind`. Keep the map and tickets as coordination records. Route each active ticket to one leaf planning skill, write accepted results into canonical artifacts, and preserve every human gate. Do not use Wayfinding for ordinary shaping or implementation sequencing.

## 1. Explore

Use when the problem, source material, or existing system is not yet understood.

Outputs:

- source notes
- current-state summary
- open questions
- relevant files or artifacts
- risks and unknowns

Do not implement code in Explore mode.

## 2. Frame

Use when the team needs to name the current situation, problem, outcome, and boundaries.

Outputs:

- source
- trigger or context
- current approach, workaround, or nonconsumption
- current result and struggle
- problem
- outcome
- less-about / more-about boundaries
- criteria candidates

Use `framing-doc`.

## 3. Criteria

Use when the team needs standards for judging fit before proposing mechanisms.

Outputs:

- requirements / criteria table
- must-have / nice-to-have / out / undecided statuses
- mechanism parking lot
- open criteria questions

Use `shaping` or `/criteria` where supported. Do not propose shapes or breadboards yet.

## 4. Set Appetite

Use after requirements are accepted and before shape selection.

Outputs:

- fixed time or scope budget
- team shape and review point
- explicit cut line
- accepted uncertainty
- must-resolve unknowns or spike threshold

Use `shaping`, `/appetite`, and `templates/appetite-card.md` when the decision needs its own artifact.

Do not derive Appetite from a preferred shape.

## 5. Sketch shapes

Use when multiple solution directions are possible.

Outputs:

- CURRENT baseline when applicable
- 2–4 alternative shapes
- shape parts
- flagged unknowns
- candidate-breadboard requests
- focused spike candidates

Use `shaping` or `/sketch-shapes`.

Use the cheapest representation that makes each candidate judgeable: mechanism tables, rough sketches, candidate breadboards, or focused spikes. Do not select a direction in this mode.

## 6. Candidate-shape breadboard, as needed

Use when one named unselected candidate cannot be judged from its mechanism list or sketch alone.

Inputs:

- accepted requirements
- accepted Appetite and cut line
- one named candidate and shape-part IDs
- one decision-relevant behavioral or structural uncertainty

Outputs:

- `mode: candidate-shape`
- only the places, affordances, stores, consequences, branches, and wiring needed to resolve the question
- supported, missing, or contradictory mechanisms
- rabbit holes and Appetite risks
- spike candidates
- implications for fit, reverse fit, and Appetite fit

Use `breadboarding` and `breadboarding/references/candidate-shape-mode.md`.

This mode is exploratory evidence subordinate to shaping. It cannot select itself, feed slicing, produce build scope, or become accepted future intent.

Not every candidate needs a breadboard. Candidates do not need equal detail.

## 7. Fit check

Use when the team needs to compare alternatives before choosing.

Outputs:

- fit check
- reverse fit check
- Appetite fit and required cuts
- failed or undecided requirement rows
- unjustified mechanisms
- candidate-evidence summary
- decision-readiness note

Use `shaping` or `/fit-check`.

Candidate breadboards and spikes support the judgment but do not decide which shape wins.

## 8. Select shape

Use when the human is ready to choose a direction.

Outputs:

- selected shape
- rejected alternatives
- trade-offs
- remaining unknowns
- candidate-breadboard reconciliation plan
- next handoff

Use `shaping` or `/select-shape`. Do not invent a human decision or automatically promote candidate evidence.

## 9. Reconcile visual evidence, as needed

Use whenever a sketch, screenshot, wireframe, mockup, or whiteboard may clarify or contradict the active frame, candidate, selected shape, breadboard, or slices.

Outputs:

- visible observations separated from interpretations
- observation-to-plan mapping with stable IDs
- missing, conflicting, clarifying, covered, and ambiguous items
- proposed deltas with fit and scope impact
- human accept, revise, reject, or defer decision
- synchronized accepted updates and ripple status

Use `sketch-reconciliation` or `/reconcile-sketch`.

Do not let a visual silently override selected behavior or scope.

## 10. Selected-design breadboard

Use after a human selects a shape and Appetite.

Inputs:

- selected shape and parts
- accepted requirements, Appetite, and cut line
- existing system behavior that must remain or connect
- any candidate breadboard that needs reconciliation

Outputs:

- `mode: selected-design`
- reconciled places
- UI and non-UI affordances
- stores
- wiring
- product-relevant branches
- shaping conflicts
- candidate slice boundaries after acceptance

Use `breadboarding`.

A candidate breadboard does not automatically become selected-design. Remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance.

When detailed behavior exposes a conflict with requirements, Appetite, or the selected shape, stop and return the issue to shaping. The human may revise the shape, cut behavior, run a focused spike, reopen selection, or stop the bet.

## 11. Statechart, optional

Use only when a selected stateful portion of an accepted selected-design breadboard is difficult to reason about from wiring alone.

Outputs:

- state inventory
- transition table
- Mermaid statechart
- gaps and proposed breadboard updates

Use `statechart`. The selected-design breadboard remains authoritative.

## 12. Select slice

Use after the selected-design breadboard is accepted and a demoable increment must be chosen.

Outputs:

- selected slice ID and boundary
- demo path and `Produces` line
- exclusions and dependencies
- verification target

Use `breadboarding`. Never slice a current-state or candidate-shape breadboard for implementation.

## 13. Interface contracts

Use when the selected slice crosses meaningful boundaries.

Outputs:

- contract IDs
- boundary names
- inputs and outputs
- branches and errors
- open decisions

Use `interface-contracts`. Keep it in plain language unless production schema is explicitly requested.

## 14. Executable breadboard

Use when the selected slice needs examples, fixtures, expected outputs, edge cases, or tests before build handoff.

Outputs:

- fixtures / starting data
- example runs
- expected visible results and state changes
- expected side effects
- edge cases
- acceptance tests

Use `executable-breadboards`. Do not invent missing expected behavior.

## 15. Dumplink, optional

Use when work inside the selected slice needs vertical task groups, dependency-aware sequencing, risk states, or Appetite-based cuts.

Outputs:

- task dump and vertical task groups
- risk states
- dependency map and build sequence
- scope cuts
- acceptance checks
- bounded agent handoff packet

Use `dumplink`. Without a selected slice, Dumplink remains exploratory and cannot create a committed build sequence or handoff.

## 16. Kickoff reference, optional

Use when builders need a durable human-readable map after selected artifacts converge.

Outputs:

- selected direction and boundaries
- system areas and important behavior
- first slice and verification target

Use `kickoff-doc` or `/kickoff`. It is orientation, not build scope.

## 17. Feed context

Use before implementation, especially when planning artifacts are long or numerous.

Outputs:

- compact context packet
- authority order
- must-preserve constraints
- accepted Appetite and cut line
- selected slice
- relevant selected-design rows, statechart, contracts, examples, and task group
- non-goals
- execution contract
- verification target

Use `feed-planning-context`.

Exclude candidate breadboards as active build scope. Include a candidate finding only when it explains an explicit unresolved or accepted shaping decision.

## 18. Build

Use only after a slice is selected and bounded context exists.

Rules:

- implement only the selected slice
- preserve selected-design intent
- keep stable IDs intact
- map work back to accepted artifacts
- propose a planning update if implementation reality conflicts with the plan
- create an agent run log for meaningful runs

## 19. Check drift

Use during or after implementation when the agent may have drifted.

Output exactly one of:

```text
No planning drift found.
```

or:

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

Do not implement in Check Drift mode.

## 20. Reflect

Use after implementation exists.

Outputs:

- implementation reality recorded separately from accepted intent
- drift, missing behavior, accidental behavior, and design smells
- planning-update and implementation-follow-up options
- human drift decision or clearly pending decision

Use `breadboard-reflection`.

## Mode transition checklist

Before moving forward, ask:

- Is the current mode clear?
- Is there a source artifact for the next step?
- Are requirements separate from mechanisms?
- Is Appetite explicit before selection?
- Is candidate evidence labeled and subordinate to shaping?
- Has unequal candidate detail been prevented from implying preference?
- Was the shape selected explicitly?
- Was candidate evidence reconciled rather than automatically promoted?
- Is the active breadboard accepted in selected-design mode before slicing?
- Are rejected alternatives and non-goals visible?
- Are stable IDs preserved?
- Were consequential visuals reconciled explicitly?
- Does a build step have a selected slice and compact context packet?
- Are optional statechart and Dumplink artifacts used only when triggered?
- Does meaningful implementation need a drift check or run log?

## Common failure modes

Avoid:

- jumping from notes directly to implementation
- treating a rejected shape as selected
- selecting before criteria, Appetite, and alternatives are visible
- forbidding all breadboarding before selection even when a candidate is not judgeable
- treating a candidate breadboard as accepted intent or build scope
- automatically promoting candidate rows after selection
- silently changing a selected shape when detailed breadboarding exposes a conflict
- treating a newer-looking sketch as authority
- pasting all raw context instead of feeding a compact packet
- using build mode before a slice exists
- silently rewriting accepted intent to match implementation
