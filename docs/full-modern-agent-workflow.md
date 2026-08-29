# Full modern agent workflow

This document shows the complete planning-to-build system, including both the fluid collaborative shaping loop and the stricter promotion path used when work becomes accepted scope.

Use it when work is large enough that a coding agent should not jump directly from fuzzy or provisional intent to implementation.

## Two layers, not one conveyor belt

### Collaborative shaping layer

Start from whatever is already useful: requirements, a proposed solution, evidence/prototype, or a focused unknown.

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

R, S, fit, spikes, sketches, candidate breadboards, and Working Appetite may iterate in any useful order. Working material can change directly; accepted material requires an explicit delta decision.

### Promotion and build layer

Once the team is ready to commit, the gates become strict:

```text
clear-enough problem boundary
→ accepted requirements
→ accepted Appetite + cut line
→ decision-ready candidates and evidence
→ fit + reverse fit + Appetite implications
→ explicit human selection
→ selected-design reconciliation
→ accepted behavior
→ human-selected slice
→ bounded context
→ implementation with drift checks
```

These are promotion gates, not navigation locks.

When the **gated/orchestrated profile** is explicitly selected, the controlled path can also be enforced during exploration:

```text
[optional Lead User Research when future-facing opportunity evidence is missing]
→ accepted research-to-frame implications
→ accepted frame
→ accepted requirements
→ accepted Appetite
→ candidate shapes
↔ candidate-shape breadboards or focused spikes
→ decision-ready fit
→ human selection
→ selected-design breadboard
→ selected slice
→ bounded build
```

## Full flow after shaping converges

Working shaping → accepted R/Appetite → explicit human shape/project selection → reconcile selected-design breadboard ↔ return to shaping if detailed behavior exposes a consequential conflict → optional statechart → optional Dumplink creates sequenced vertical task groups → human selects the active task group or another demoable slice → contracts and executable examples as needed → optional kickoff reference → context packet with execution contract → build with drift checks → run log → reflection.

When the bounded planning route itself spans multiple sessions, Wayfinding wraps the relevant planning moves as a coordination layer. Its map and tickets index work; accepted decisions still live in their canonical artifacts.

## Planning moves and promotion stages

| Move / stage | Purpose | Output / authority |
| --- | --- | --- |
| Wayfinding, optional outer loop | Coordinate dependent planning decisions, evidence, prototypes, and prerequisites across sessions without creating a second source of truth. | coordination map and tickets, never product truth |
| Lead User Research, optional upstream lane | Establish decision-useful evidence about important trends, advanced users, unusually high-benefit needs, and analogs before framing when that evidence is genuinely missing. | authoritative research record plus proposed handoff; not accepted planning intent until the human accepts the handoff |
| Frame, when needed | Name the current situation, problem, outcome, forces, and boundaries when those are not clear enough for judgment. | Working or Accepted `planning/frame.md` |
| R move | Create, extract, or revise requirements. R may come first or be extracted from S/prototype/fit evidence. | Working or Accepted requirements table |
| Appetite move | Set, revise, or accept the budget, cut line, accepted uncertainty, and spike threshold. | Unset / Working / Accepted Appetite |
| S move | Capture or revise candidate shapes; valid as an S-first entry point. | candidate shapes + parts + unknowns |
| Working fit | Compare current R and S early enough to expose missing requirements or unjustified mechanisms. | Working fit/reverse-fit evidence; not sufficient for selection |
| Focused spike | Resolve one technical or empirical unknown and return explicit implications to R, S, fit, or Appetite. | exploratory spike evidence |
| Candidate-shape breadboard | Clarify one named candidate's behavior/structure. In collaborative mode it may use provisional R/Appetite; final fit claims remain provisional. | exploratory candidate breadboard + R/S/fit implications; never build scope |
| Sketch reconciliation, as needed | Map a visual to planning IDs and apply only accepted deltas when it may change accepted planning. | reconciliation record + synchronized accepted updates |
| Accept requirements / Appetite | Promote judging inputs from Working to Accepted. | accepted R and accepted Appetite/cut line |
| Decision-ready fit | Re-run or validate fit/reverse-fit/Appetite implications against accepted judging inputs. | decision-ready comparison |
| Select shape | Record the explicit human-selected direction and candidate evidence to retain, revise, or discard. | selected direction + rejected alternatives + reconciliation plan |
| Selected-design breadboard | Reconcile the selected shape into accepted normative places, affordances, stores, consequences, branches, and wiring. Return consequential conflicts to shaping. | accepted `planning/breadboard.md` |
| Statechart, optional | Derive a precise behavioral view when selected stateful scope is hard to reason about from wiring alone. | `planning/statechart.md` derived from the breadboard |
| Select project | Confirm the discrete outer unit of work, outcome, boundary, exclusions, and Appetite. | accepted project boundary |
| Dumplink, optional | Decompose the selected project into vertical task groups, dependency sequence, risk states, scope cuts, and a task-group approval gate. | `planning/dumplink.md` |
| Select active slice | Approve the Dumplink plan and choose an active task group, or choose another demoable slice when Dumplink is unnecessary. | selected `planning/slices.md` boundary |
| Interface contracts | Define boundary-crossing exchanges before agents guess field-level details. | `planning/interface-contracts.md` |
| Executable breadboard | Add fixtures, examples, expected outputs, edge cases, and acceptance tests. | `planning/executable-breadboard.md` |
| Kickoff, optional | Create a durable human-readable orientation map after selected artifacts converge; not build scope or sequence. | `planning/kickoff.md` |
| Context packet | Feed only the authoritative context relevant to the implementation agent; exclude Working alternatives and candidate breadboards as active scope. | `planning/context-packet.md` |
| Drift check | Keep implementation inside the selected slice and active task group. | strict drift-check output |
| Run log | Leave a durable audit trail after meaningful agent work. | `planning/runs/YYYY-MM-DD-short-task.md` |
| Reflection | Compare implementation reality to accepted intent and prepare/apply the explicit human drift decision. | `planning/breadboard-reflection.md` |

## Breadboard authority

- `current-state` is descriptive evidence about what exists.
- `candidate-shape` is exploratory evidence about one unselected shape during shaping. In collaborative mode it may use Working R or Unset/Working Appetite, but must label that authority and keep final fit claims provisional.
- `selected-design` is normative intent after explicit human selection and reconciliation against accepted R/Appetite/cuts.

Candidate breadboards cannot select themselves, produce slices, govern implementation, or automatically become selected-design artifacts.

## Context packet must include

- active task
- source artifacts and authority order
- accepted requirements, Appetite, and cut line
- accepted selected-design behavior
- current selected slice
- relevant statechart rows, contracts, executable examples, and Dumplink task group when present
- explicit non-goals
- execution contract
- verification target

It must not treat Working shapes, current-state maps, or candidate-shape breadboards as selected build scope.

## Drift check output

A drift check must return only one of these two forms:

`No planning drift found.`

or:

`Planning drift found:` followed by selected artifact, current implementation direction, risk, and recommended move.

## Done standard

A modern agent workflow is complete when:

- people were allowed to start from the material that actually existed rather than a mandatory first artifact
- Working and Accepted planning material stayed distinguishable
- requirements stayed separate from mechanisms even when R was extracted from S
- Appetite and cut line were Accepted before shape selection
- Working fit checks were not mistaken for final decision evidence
- focused spikes returned evidence to shaping rather than making product decisions
- candidate breadboards were used only for decision-relevant uncertainty and labeled provisional judging inputs when applicable
- exploratory candidate evidence remained separate from accepted future intent
- the human-selected shape is explicit
- candidate rows were reconciled rather than automatically promoted
- consequential visual evidence was reconciled without silent scope or behavior changes
- only accepted selected-design behavior fed slice selection
- detailed breadboarding returned consequential conflicts to shaping for an explicit decision
- statecharts remain traceable to the selected-design breadboard when present
- boundary contracts and executable examples exist where needed
- Dumplink task groups are vertical and risk-aware
- context packets exclude Working/candidate material as build scope and include an execution contract
- drift checks use the strict output format
- meaningful agent work leaves a run log
- reflection preserves accepted intent and implementation reality separately, with an explicit decision governing any update
