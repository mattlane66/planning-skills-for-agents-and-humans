# Agent Workflow

Use this workflow when an agent is helping turn unclear product work into buildable planning artifacts and implementation handoffs.

The workflow is tool-neutral. It works with Claude Code, Cursor, Codex, Gemini CLI, Claude/Claude Design when the skills are available, and other agentic environments. The exact invocation differs by tool; the planning discipline should stay the same.

For machine-readable orchestration, use `.agent-orchestration.yaml`.

## Governing model

> **Exploration is fluid. Commitment is gated.**

Interactive shaping does not have to proceed through a fixed sequence. A user can enter with:

- requirements or constraints (**R-first**)
- a proposed solution (**S-first**)
- a prototype, sketch, workflow, or current-system evidence
- a fit question or focused technical unknown

Within collaborative shaping, these moves may repeat in any useful order:

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

The sequence becomes strict only when working material is promoted to accepted intent or build scope.

## Profiles

### Collaborative — default for human-guided work

- provisional inputs are allowed
- exploration order is flexible
- a shape can come before requirements
- fit checks can be Working before they are decision-ready
- candidate breadboards can use Working R or Unset/Working Appetite
- accepted material cannot be silently changed
- human selection, selected-design promotion, slicing, and build remain gated

### Gated / orchestrated

Use when a team, CI harness, multi-agent planner, or user explicitly wants deterministic prerequisites.

Controlled default:

```text
[optional Lead User Research when future-facing opportunity evidence is missing]
→ explicit human acceptance of proposed research-to-frame implications
→ accepted frame
→ accepted requirements
→ accepted Appetite
→ candidate shapes
↔ candidate breadboards / focused spikes
→ decision-ready fit
→ explicit human selection
→ selected-design breadboard
→ selected slice
→ bounded context
→ build
```

The gated profile may restrict exploratory moves that collaborative mode allows provisionally. It never weakens the hard human promotion gates.

## 0. Wayfinding, optional outer loop

Use when a bounded planning destination requires multiple dependent decisions, investigations, or prototypes across sessions.

Outputs:

- one low-resolution Wayfinding map
- precise decision, evidence, prototype, and prerequisite tickets
- blockers and a queryable frontier
- in-scope fog and explicit out-of-scope work
- an exit check tied to a canonical artifact or human gate

Use `wayfinding` or `/wayfind`. Keep the map and tickets as coordination records. Route each active ticket to one leaf planning skill, write accepted results into canonical artifacts, and preserve every human gate. Do not use Wayfinding for ordinary shaping or implementation sequencing.

## 1. Explore — optional

Use when source material, a proposed solution, the current system, or an unknown needs investigation before the next shaping move is obvious.

Outputs may include:

- source notes
- current-state summary
- provisional R or S
- open questions
- relevant files or artifacts
- risks and unknowns

Do not implement production code in Explore mode.

## 1A. Lead User Research — optional upstream evidence

Use when the consequential uncertainty is whether a future-facing need or
opportunity is real enough to frame, and the decision requires trends, pyramiding,
qualified Lead User Need Episodes, or advanced analogs. Do not use it as a generic
label for ordinary customer or market research.

Use `lead-user-research` or `/lead-user`. The skill derives one next phase from
persisted state, may loop back when sufficiency fails, and skips concept work when
no need passes the gate. After completion, propose a research-to-frame handoff and
stop for explicit human acceptance. The study is cited evidence, not an accepted
frame.

## 2. Frame — when needed

Use when the team cannot yet name the situation, problem, outcome, evidence, or boundary well enough to judge proposed solutions.

Outputs:

- source
- trigger or context
- current approach and result
- problem
- outcome
- boundaries and non-goals
- criteria candidates

Use `framing-doc`.

A concrete solution idea may be explored before a formal frame in collaborative mode. Do not select it until the problem boundary is clear enough for honest judgment.

## 3. Collaborative shaping loop

Use `shaping` or `/shape` as the main working surface.

### R move — requirements / criteria

Create or revise requirements when that is the current useful move.

Outputs:

- requirements / criteria table
- Working or Accepted authority
- must-have / nice-to-have / out / undecided statuses
- mechanism parking lot
- requirements extracted from existing shapes when useful

Use `/criteria` when you want to constrain the current move to R.

### S move — shapes

Capture or revise solution directions when that is the current useful move.

Outputs:

- CURRENT baseline when applicable
- user's existing proposed shape when present
- materially useful alternatives
- shape parts and flagged unknowns
- provisional requirements revealed by mechanisms
- candidate breadboard or spike opportunities

Use `/sketch-shapes` when you want to constrain the current move to S.

S may be the first shaping move.

### Appetite move

Set, revise, or accept the fixed time/scope budget and cut line.

Outputs:

- Appetite authority: Unset | Working | Accepted
- fixed budget
- team shape and review point
- cut line
- accepted uncertainty
- must-resolve unknowns

Use `/appetite` when the current question is the size of the bet.

Collaborative shaping may explore S before Appetite is accepted. Shape selection may not.

### Fit move

Run fit and reverse-fit checks whenever they would clarify the work.

Outputs:

- Working or Decision-ready fit check
- reverse fit check
- Appetite fit when Appetite exists
- failed requirements
- unjustified mechanisms
- missing R exposed by the comparison
- next uncertainty to resolve

Use `/fit-check`.

A Working fit check is useful evidence but cannot support final selection until the judging inputs are accepted.

### Spike move

Use when one technical or empirical unknown blocks honest judgment.

Outputs:

- focused questions and evidence
- mechanism understanding
- explicit R implications
- explicit S implications
- fit rows to rerun
- Appetite implications when known
- remaining uncertainty

Use `/spike` or `templates/spike.md`.

A spike may begin from R, S, fit, a sketch, candidate breadboard, or implementation reality. It does not select the product direction.

### Candidate-shape breadboard move

Use when one named unselected candidate cannot be judged from its mechanism list or sketch alone.

Inputs in collaborative mode:

- named candidate and shape-part IDs
- decision-relevant uncertainty
- current R authority: Working or Accepted
- current Appetite authority: Unset, Working, or Accepted

Outputs:

- `mode: candidate-shape`
- only the places, affordances, stores, consequences, branches, and wiring needed to resolve the question
- unsupported mechanisms and rabbit holes
- R/S/fit implications
- Appetite implications when supportable
- spike candidates

Use `breadboarding` or `/breadboard` in `candidate-shape` mode.

If R or Appetite is provisional, final fit claims remain provisional. Candidate evidence cannot select itself, feed slicing, produce build scope, or become accepted future intent.

### Return loops

Any of the above moves may return to another:

- fit exposes a missing R
- a spike invalidates an S part
- a candidate breadboard exposes a new constraint
- a shape reveals the real requirement
- Appetite forces a cut and reshaping
- a sketch clarifies or contradicts R/S

Update Working material visibly. If the discovery would change Accepted material, propose the delta and stop for the human gate.

## 4. Shape selection — hard gate

Use only when the work is decision-ready.

Require:

- accepted frame or intentionally lightweight clear boundary
- accepted requirements
- accepted Appetite and cut line
- decision-ready candidates and evidence
- visible fit, reverse-fit, and Appetite implications
- explicit human choice

Outputs:

- selected shape
- rejected alternatives
- trade-offs
- remaining unknowns
- candidate-evidence reconciliation plan
- next handoff

Use `shaping` or `/select-shape`. Do not invent a human decision.

## 5. Reconcile visual evidence, as needed

Use whenever a sketch, screenshot, wireframe, mockup, prototype, or whiteboard may clarify or contradict accepted planning.

Outputs:

- visible observations separated from interpretations
- observation-to-plan mapping with stable IDs
- proposed deltas with fit and scope impact
- human accept, revise, reject, or defer decision
- synchronized accepted updates and ripple status

Use `sketch-reconciliation` or `/reconcile-sketch`.

## 6. Selected-design breadboard

Use after a human selects a shape and the judging inputs are accepted.

Inputs:

- selected shape and parts
- accepted requirements
- accepted Appetite and cut line
- existing system behavior that must remain or connect
- candidate evidence that needs reconciliation

Outputs:

- `mode: selected-design`
- reconciled places
- UI and non-UI affordances
- stores
- wiring
- product-relevant branches
- shaping conflicts
- candidate slice boundaries after acceptance

A candidate breadboard does not automatically become selected-design. Remove unselected mechanisms, reconcile surviving rows against accepted intent, preserve unresolved gaps explicitly, and obtain acceptance.

When detailed behavior exposes a conflict with requirements, Appetite, or the selected shape, return the issue to shaping for an explicit decision.

## 7. Statechart, optional

Use only when a selected stateful portion of an accepted selected-design breadboard is difficult to reason about from wiring alone.

Outputs:

- state inventory
- transition table
- Mermaid statechart
- gaps and proposed breadboard updates

Use `statechart`. The selected-design breadboard remains authoritative.

## 8. Select slice

Use after selected-design behavior is accepted and a demoable increment must be chosen.

Outputs:

- selected slice ID and boundary
- demo path and `Produces` line
- exclusions and dependencies
- verification target

Never slice a current-state or candidate-shape breadboard for implementation.

## 9. Interface contracts, optional

Use when the selected slice crosses meaningful boundaries.

Outputs:

- contract IDs
- boundary names
- inputs and outputs
- branches and errors
- open decisions

Use `interface-contracts`.

## 10. Executable breadboard, optional

Use when the selected slice needs examples, fixtures, expected outputs, edge cases, or tests before build handoff.

Outputs:

- fixtures / starting data
- example runs
- expected visible results and state changes
- side effects
- edge cases
- acceptance tests

Use `executable-breadboards`. Do not invent missing expected behavior.

## 11. Dumplink, optional

Use when a selected, bounded project needs vertical task groups, dependency-aware sequencing, risk states, or Appetite-based cuts.

Outputs:

- task dump and vertical task groups
- risk states
- dependency map and build sequence
- scope cuts
- acceptance checks
- task-group approval gate
- bounded handoff for the human-selected active group

Use `dumplink`. It cannot expand the selected project or substitute for selection.

## 12. Kickoff reference, optional

Use when builders need a durable human-readable map after selected artifacts converge.

Outputs:

- selected direction and boundaries
- system areas and important behavior
- first slice and verification target

Use `kickoff-doc` or `/kickoff`. It is orientation, not build scope.

## 13. Feed context

Before implementation, package only the authoritative subset relevant to the active slice.

Outputs:

- compact context packet
- authority order
- accepted requirements, Appetite, cut line, and non-goals
- selected slice
- relevant selected-design rows and supporting contracts/examples
- execution contract
- verification target

Exclude Working alternatives and candidate breadboards as active build scope.

## 14. Build

Rules:

- implement only the selected slice
- preserve accepted selected-design intent
- keep stable IDs intact
- map work back to accepted artifacts
- propose a planning update if implementation reality conflicts with the plan
- create an agent run log for meaningful runs

## 15. Check drift

Use during or after implementation when the agent may have drifted.

Return only:

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

## 16. Reflect

Use after implementation exists.

Outputs:

- implementation reality recorded separately from accepted intent
- drift, missing behavior, accidental behavior, and design smells
- planning-update and implementation-follow-up options
- human drift decision or clearly pending decision

Use `breadboard-reflection`.

## Mode transition checklist

Before a **promotion** step, ask:

- Is the current material Working or Accepted?
- Are requirements separate from mechanisms?
- Is Appetite accepted before selection?
- Is candidate evidence labeled and subordinate to shaping?
- Have provisional fit claims been revalidated against accepted judging inputs?
- Was the shape selected explicitly?
- Was candidate evidence reconciled rather than automatically promoted?
- Is selected-design behavior accepted before slicing?
- Is the active slice selected before build?
- Are rejected alternatives and non-goals visible?
- Are stable IDs preserved?
- Were consequential visuals reconciled explicitly?
- Does the build step have bounded context and a verification target?

Do not use this checklist to prevent ordinary movement among R, S, fit, spikes, or candidate breadboards during collaborative exploration.

## Common failure modes

Avoid:

- forcing an S-first idea back through ceremony when the solution itself is useful shaping material
- treating a rough solution as accepted strategy
- treating provisional R as final judging criteria
- selecting before requirements and Appetite are accepted
- treating a Working fit check as decision-ready
- treating a candidate breadboard as accepted intent or build scope
- automatically promoting candidate rows after selection
- silently changing accepted R, Appetite, or selected shape when evidence changes
- treating a newer-looking sketch as authority
- pasting all raw context instead of feeding a compact packet
- using build mode before a slice exists
- silently rewriting accepted intent to match implementation
