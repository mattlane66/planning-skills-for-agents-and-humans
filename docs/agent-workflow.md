# Agent Workflow

Use this workflow when an agent is helping turn unclear product work into buildable planning artifacts and implementation handoffs.

The workflow is tool-neutral. It works with Claude Code, Cursor, Codex, Gemini CLI, and other agentic environments. The exact invocation differs by tool; the planning discipline should stay the same.

For machine-readable orchestration, use `.agent-orchestration.yaml`.

## 1. Explore

Use this mode when the problem, source material, or existing system is not yet understood.

Outputs:
- source notes
- current-state summary
- open questions
- relevant files or artifacts
- risks and unknowns

Do not implement code in Explore mode.

## 2. Frame

Use this mode when the team needs to name the problem, outcome, and boundaries.

Outputs:
- source
- problem
- outcome
- less-about / more-about boundaries
- criteria or requirements candidates

Use the `framing-doc` skill.

## 3. Criteria

Use this mode when the team needs to define the standards for judging fit before proposing mechanisms.

Outputs:
- requirements / criteria table
- must-have / nice-to-have / out / undecided statuses
- mechanism parking lot
- open criteria questions

Use the `shaping` skill or the `/criteria` command where supported.

Do not propose shapes in Criteria mode.

## 4. Sketch shapes

Use this mode when multiple solution directions are possible.

Outputs:
- CURRENT baseline when applicable
- 2-4 alternative shapes
- shape parts
- flagged unknowns
- spike candidates

Use the `shaping` skill or the `/sketch-shapes` command where supported.

Do not select a direction in Sketch Shapes mode.

## 5. Fit check

Use this mode when the team needs to compare alternatives before choosing.

Outputs:
- fit check
- reverse fit check
- failed or undecided requirement rows
- unjustified mechanisms
- decision-readiness note

Use the `shaping` skill or the `/fit-check` command where supported.

Do not select a direction unless the human explicitly chooses one.

## 6. Select shape

Use this mode when the human is ready to choose a direction.

Outputs:
- selected shape
- rejected alternatives
- trade-offs
- remaining unknowns
- next handoff

Use the `shaping` skill or the `/select-shape` command where supported.

Do not invent a human decision.

## 7. Reconcile visual evidence, as needed

Use this mode whenever a sketch, screenshot, wireframe, mockup, or whiteboard may clarify or contradict the active frame, shape, breadboard, or slices.

Outputs:
- visible observations separated from interpretations
- observation-to-plan mapping with stable IDs
- missing, conflicting, clarifying, covered, and ambiguous items
- proposed deltas with fit and scope impact
- human accept, revise, reject, or defer decision
- synchronized accepted updates and ripple status

Use the `sketch-reconciliation` skill or `/reconcile-sketch` command where supported.

Do not let the visual silently override selected behavior or scope. Do not infer hidden behavior from appearance alone.

## 8. Breadboard

Use this mode when the selected shape needs to become concrete enough to slice.

Outputs:
- places
- UI affordances
- non-UI affordances
- stores
- wiring
- demoable slices

Use the `breadboarding` skill.

## 9. Statechart, optional

Use this mode only when a selected stateful portion of an accepted breadboard is difficult to reason about from wiring alone.

Outputs:
- state inventory
- transition table
- Mermaid statechart projection
- gaps and proposed breadboard updates

Use the `statechart` skill. The breadboard remains authoritative.

Do not invent retry, timeout, cancellation, hierarchy, or parallel behavior.

## 10. Interface contracts

Use this mode when the selected slice crosses meaningful boundaries.

Outputs:
- contract IDs
- boundary names
- inputs
- outputs
- branches and error cases
- open decisions

Use the `interface-contracts` skill.

Keep this in plain language unless the user explicitly asks for production schema or contract files.

## 11. Executable breadboard

Use this mode when the selected slice is ready for build handoff and needs examples, fixtures, expected outputs, edge cases, or tests.

Outputs:
- fixtures / starting data
- example runs
- expected visible results
- expected state changes
- expected side effects
- edge cases
- acceptance tests

Use the `executable-breadboards` skill.

Do not invent missing expected outputs or edge cases. Flag them before build work.

## 12. Dumplink, optional

Use this mode when selected work needs vertical task groups, dependency-aware sequencing, risk states, or appetite-based cuts.

Outputs:
- task dump and vertical task groups
- risk states
- dependency map and build sequence
- scope cuts
- acceptance checks
- bounded agent handoff packet

Use the `dumplink` skill. Do not turn the output into a horizontal discipline backlog.

## 13. Feed context

Use this mode before implementation work, especially when planning artifacts are long or numerous.

Outputs:
- compact context packet
- authority order
- must-preserve constraints
- selected slice
- relevant statechart rows, contracts, executable examples, and Dumplink task group when present
- non-goals
- execution contract
- verification target

Use the `feed-planning-context` skill.

## 14. Build

Use this mode only after a slice is selected and the relevant planning context has been fed.

Rules:
- implement only the selected slice
- preserve shaped intent
- keep stable IDs intact
- map implementation work back to requirements, affordances, stores, statechart transitions, contracts, example runs, edge cases, task groups, or slices
- propose a planning update if implementation reality conflicts with the plan
- create an agent run log for meaningful implementation runs

## 15. Check drift

Use this mode during or after implementation work when the agent may have drifted from the selected planning artifacts.

Outputs must be exactly one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

Use `/check-drift`, `templates/drift-check.md`, and `docs/loop-prompting.md` where supported.

Do not implement code in Check Drift mode.

## 16. Reflect

Use this mode after implementation exists.

Outputs:
- synced implementation reality
- drift
- missing behavior
- accidental behavior
- planning updates
- implementation follow-ups

Use the `breadboard-reflection` skill.

## Mode transition checklist

Before moving forward, ask:

- Is the current mode clear?
- Is there a source artifact for the next step?
- Are requirements still separate from mechanisms?
- Are rejected alternatives clearly marked?
- Are non-goals visible?
- Are stable IDs preserved?
- If a visual changed the understanding, were observations mapped and deltas accepted explicitly?
- Is the next output useful to both humans and agents?
- Does a build step have a selected slice and compact context packet?
- Are optional statechart or Dumplink artifacts being used only where their triggering complexity exists?
- Does meaningful implementation need a drift check or run log?

## Common failure modes

Avoid:

- jumping from notes directly to implementation
- treating a rejected shape as the selected direction
- selecting a shape before criteria and alternatives are visible
- treating a newer-looking sketch as authority or inferring hidden behavior from a static image
- pasting all raw context instead of feeding a compact context packet
- silently changing the plan when code reality pushes back
- using build mode before a slice exists
- treating reflection as critique before syncing the breadboard to reality
- letting hooks become a hidden method instead of a reminder layer
