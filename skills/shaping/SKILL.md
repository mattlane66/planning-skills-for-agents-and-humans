---
name: shaping
description: Shape ambiguous product work before implementation by iterating among requirements, solution shapes, fit checks, spikes, and candidate evidence while keeping commitment gates explicit.
license: MIT
---

# Shaping

Use this skill when the team needs to make ambiguous product work concrete enough to judge before implementation.

Shaping supports two legitimate ways of working:

- **collaborative shaping** — start from whatever is already known and move fluidly among requirements, shapes, fit checks, spikes, sketches, and candidate breadboards
- **gated shaping** — use an explicit ordered sequence when a team or automation needs stronger procedural control

The governing rule is:

> **Exploration is fluid. Commitment is gated.**

A rough solution is a valid place to start thinking. It is not automatically an accepted requirement, selected direction, or build instruction.

## Goal

Produce a durable shaping document that keeps four things separate but connected:

- requirements: what must be true
- appetite: the fixed budget and cut line
- shapes: materially different ways to satisfy the requirements
- selection evidence: why a human chose one direction

Shaping may use prose, sketches, candidate breadboards, fit checks, and focused spikes to make the work clearer. These moves may repeat in any useful order during exploration. None of them automatically promotes exploratory material into accepted intent.

Shaping ends when a direction is explicitly selected or the work stops at a decision-ready comparison. It does not create implementation tasks or begin coding.

## Inputs

Use whichever sources are available:

- an accepted or provisional frame
- research, interviews, notes, or requests
- a rough solution already in someone's head
- an existing prototype, sketch, or interface
- current product behavior or constraints
- existing requirements or proposed mechanisms
- current-state or candidate-shape breadboards
- focused spike results
- an existing shaping document

When working in an existing product repository, first inspect the applicable project language and durable decisions. Look for `AGENTS.md`, `CONTEXT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, ADR or decision folders, existing tests, and public interfaces. Reuse established terms and identify existing seams rather than creating parallel vocabulary. Do not create or change a glossary or ADR without authorization.

## Authority and document hierarchy

From high to low:

1. latest explicit human instruction
2. accepted frame and selected project boundary
3. accepted shaping decisions — requirements, appetite, selected direction, cuts
4. candidate-shape breadboards and focused spikes — exploratory evidence subordinate to their named question or candidate
5. accepted selected-design breadboard or slices — concrete selected behavior and increments
6. implementation plans — build detail

A lower-level discovery may require an upstream planning update. Do not silently rewrite a higher-authority accepted artifact.

Read [artifact consistency](references/artifact-consistency.md) when changing an existing planning stack or reconciling discoveries across levels.

## Working state versus accepted state

Shaping becomes easier to navigate when working material and committed material are visibly different.

Use these concepts even if the artifact does not add a literal status column:

- **working requirement** — useful enough to test, but still open to revision
- **accepted requirement** — explicitly good enough to judge selection against
- **working appetite** — a tentative budget or cut line used to explore consequences
- **accepted appetite** — the human-approved budget that constrains selection
- **candidate shape** — an unselected solution direction
- **decision-ready shape** — concrete enough for honest comparison
- **selected shape** — explicitly chosen by a human

During collaborative exploration, the agent may revise working material directly and show what changed. Once material is accepted, consequential changes require an explicit proposed delta and human decision.

## Entry points and working loop

There is no required order for exploration.

### Start from R — requirements first

Use this when the problem, needs, or constraints are easier to express than the solution.

1. capture provisional requirements
2. sketch one or more shapes
3. fit-check them
4. use spikes, sketches, or candidate breadboards where needed
5. revise R and S as discoveries emerge

### Start from S — shape first

Use this when someone already has a solution in mind.

1. capture the proposed solution as a named candidate such as `A`
2. extract the needs, constraints, and desired outcomes it appears to serve into provisional requirements
3. separate mechanism from requirement
4. run fit and reverse-fit checks as soon as they are useful
5. revise both R and S as contradictions or missing needs appear

Do not force an S-first conversation back through framing ceremony unless the missing frame prevents honest judgment.

### Start from evidence or a prototype

Treat an existing screen, prototype, code path, or workflow as evidence. Extract provisional R and S, map current behavior when needed, and continue through the same loop.

### The collaborative shaping loop

These moves may happen in any useful order:

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

Typical actions:

- populate or revise R
- capture or revise S
- compare whole shapes or alternatives within one part
- run fit or reverse-fit checks
- extract a missing R exposed by a failed fit
- remove an unjustified shape part exposed by reverse fit
- run a focused spike
- breadboard one candidate enough to answer a decision-relevant question
- set, revise, or accept appetite
- return to framing if the problem itself turns out to be wrong

Do not add ceremony merely to make the loop look complete.

## Commitment sequence

Exploration can be fluid. Promotion cannot.

Before **selecting a shape**, require:

1. the frame is accepted or intentionally waived because the problem boundary is already clear
2. requirements are accepted enough to judge fit
3. appetite and cut line are accepted
4. viable shapes are concrete enough to compare
5. decision-relevant unknowns are resolved, accepted, or visible
6. fit, reverse-fit, and appetite implications are visible
7. the human explicitly selects, revises, or stops

Before **promoting candidate behavior to selected-design intent**, require explicit shape selection and reconciliation.

Before **slicing or implementation**, require accepted selected-design behavior or an equally clear accepted behavior boundary plus a human-selected slice.

These are promotion gates, not navigation locks.

## Requirements

Requirements describe needs, outcomes, or constraints independently of one implementation approach.

When a frame is the judging basis, represent it as `x → f() → y`:

- `x` = trigger/context + current approach + current result + breakdowns;
- `f()` = the solution/shape variable being explored;
- `y` = desired outcome;
- gap = what must change from x to y;
- boundaries = constraints an acceptable f() must respect.

### Identify the unknown before choosing the next move

- If `x` is unclear, investigate the current situation.
- If `y` is unclear, clarify the desired outcome.
- If `f()` is unclear, shape candidate solutions.
- When solving for `f()`, hold accepted `x` and `y` constant. Requirements constrain the acceptable solution space.

Do not use solution exploration to compensate for an unclear current situation or desired outcome.

Requirements may come `FROM_X`, `FROM_Y`, `FROM_GAP`, or `FROM_BOUNDARY`. Hold x and y constant during one comparative Fit Check. If discovery changes x or y materially, update the frame explicitly, invalidate the affected comparison, and rerun it rather than allowing a candidate shape to redefine its own judging conditions.

When an R arrives from framing or another accepted upstream artifact, preserve its stable ID, origin, and evidence refs. Promotion from candidate to Working to Accepted changes authority, not identity. Create a new ID only when the requirement's meaning materially changes; do not mint a new ID because it was accepted, selected against, mapped to a mechanism, or carried into implementation.

Use stable IDs such as `R0`, `R1`, and `R2`. Prefer no more than nine top-level requirements; use sub-requirements when needed.

Recommended statuses:

- Core goal
- Must-have
- Nice-to-have
- Undecided
- Out

If useful, add an authority marker such as `Working` or `Accepted` without replacing the requirement status above.

Before keeping a requirement, ask whether it would still need to be true if the interface, vendor, runtime, storage method, or architecture changed completely. If not, it is probably a mechanism and belongs in a shape.

A mechanism can reveal a requirement. When starting S-first, ask: "What need or constraint makes this mechanism seem necessary?" Record the answer as provisional R, not as retroactive proof that the mechanism is correct.

Read [requirements and shapes](references/requirements-and-shapes.md) for smell tests, notation, examples, current-system baselines, and flagged unknowns.

## Appetite and cut line

Appetite is the fixed time or scope budget the team is willing to spend on the bet. It constrains selection; it is not an estimate produced after a preferred solution has already won.

Record:

- time or fixed scope budget
- team shape and review point
- explicit cut line
- uncertainty the team accepts
- unknowns that require a spike before selection or build
- conditions that would cause the appetite to be revisited

Use the Appetite section in `templates/shaping.md` for a compact record or `templates/appetite-card.md` when ownership, rationale, and revisit conditions need a separate durable artifact.

In collaborative shaping, you may explore shapes before appetite is accepted. When appetite is missing or provisional:

- label appetite-dependent judgments as provisional
- do not claim that a shape fits the bet
- do not select a direction

In gated shaping, set and accept appetite before comparative shape sketching if that is the chosen procedural policy.

## Shapes

Shapes are competing or composable solution directions. Use `CURRENT` as the baseline for an existing product, then letters such as `A`, `B`, and `C` for alternatives. Use numbered parts such as `B1`, `B2`, and `B3` for mechanisms inside a direction.

Each serious shape should:

- have a short title that characterizes the approach
- name concrete mechanisms rather than wishes
- expose meaningful tradeoffs
- flag mechanisms that are still only understood in outline
- state appetite implications when appetite is known

Use the cheapest representation that makes the shape judgeable:

- mechanism tables for a straightforward candidate
- fat-marker or rough sketches when spatial arrangement matters
- a `candidate-shape` breadboard when places, affordances, consequences, stores, or wiring must be understood before comparison
- a focused spike when a technical or empirical unknown blocks honest judgment

Candidate breadboards may be partial and may differ in depth. Do not add detail merely to make alternatives look symmetrical. Read `breadboarding/references/candidate-shape-mode.md` and invoke the breadboarding skill in candidate-shape mode when that technique is needed.

Do not create nominal variations that differ only in cosmetic detail.

## Candidate evidence without selection

For each candidate, identify the smallest unanswered question that could change its fit, viability, or appetite implications.

Use candidate breadboarding when the uncertainty is behavioral or structural. Use a focused spike when the uncertainty is technical or empirical.

In collaborative shaping, candidate breadboarding may use provisional requirements and an unset or provisional appetite. The output must state which judging inputs were provisional and must not claim final requirement fit or appetite fit that cannot yet be known.

Return candidate evidence to shaping as implications about:

- requirement fit
- reverse fit
- appetite fit, when appetite exists
- cuts or rabbit holes
- assumptions that remain unresolved
- requirements or mechanisms that should be revised

A candidate breadboard is subordinate to its named shape. It cannot select itself, feed slice selection, define build scope, or become accepted future intent.

## Fit and reverse-fit checks

Run these checks whenever they would clarify the work; they are not reserved for the end of shaping.

1. **Fit Check — Requirements × Shapes:** which overall candidate shape satisfies the accepted requirements?
2. **Rotated Fit Check / reverse fit — Parts × Requirements:** why does each part of a selected or deeply examined shape exist?
3. each viable shape against appetite, when appetite exists

Use binary `✅` or `❌` values for requirement fit. Unknown is not a pass. Put explanations below the table rather than weakening the cells with prose.

When requirements are still provisional, label the table **working fit check**. A working fit check may reveal missing requirements or bad mechanisms; it is not sufficient evidence for selection until the relevant requirements and appetite are accepted.

The Rotated Fit Check is the existing reverse-fit discipline viewed as Parts × Requirements. It asks whether every mechanism is justified by at least one requirement and whether every accepted requirement has supporting parts. Remove, cut, or explicitly justify mechanisms that have no requirement. Also surface duplicated mechanisms and cases where one part carries disproportionate responsibility. When rotation reveals a genuine missing need, add it as a provisional R and rerun the check; do not silently rewrite accepted R to rescue the shape.

For a selected shape, also record the inverse view so requirement coverage is explicit:

```md
| Req | Supporting selected part(s) | Coverage | Realization question |
|---|---|:---:|---|
| R1 | A1, A3 | ✅ | What would we observe if R1 is actually true in use? |
| R2 | — | ❌ | ... |
```

Every Accepted R must have at least one selected part that claims to make it true. Coverage is not realized fit: it records the design's claimed support, not evidence that the requirement is true in use. When a requirement is meaningfully observable after implementation, state the realization question that later outcome evidence should answer; do not manufacture a metric for an unobservable requirement.

Candidate breadboards and spike results may support the judgment, but they do not outrank the shaping document or decide which shape wins.

Read [fit checks](references/fit-checks.md) for tables, local component comparisons, failure handling, and decision-ready summaries.

## Focused spikes

A spike gathers information needed to shape honestly. It does not make the product decision.

Use a spike to:

- understand how the current system works
- determine what concrete changes a proposed mechanism would require
- test feasibility or a technical assumption
- surface a constraint that may alter R, S, fit, or appetite

A spike may be triggered from R, S, fit, a sketch, a breadboard, or implementation reality. It does not require a selected shape.

When substantial, record it with `templates/spike.md` and return the result to the shaping artifact with explicit implications:

- R to add, revise, remove, or leave unchanged
- S parts to add, revise, remove, or leave unchanged
- fit rows to rerun
- appetite implications, if known
- remaining uncertainty

## Human selection

When the work is decision-ready, present the comparison and ask the human to:

- select one direction
- request another iteration
- change criteria or appetite
- run another focused candidate breadboard or spike
- stop the bet

Do not infer selection from enthusiasm, recency, visual polish, or the fact that one shape was explored in more detail.

## Record the decision and hand off

When a direction is selected, record:

- chosen direction and relevant parts
- rationale tied to accepted requirements and appetite
- explicit cuts and non-goals
- accepted uncertainty
- spikes or decisions still required
- any established project terms, ADRs, interfaces, or seams that the selected direction must preserve or intentionally change

Then reconcile the selected mechanisms into a `selected-design` breadboard. A candidate breadboard does not automatically become authoritative: remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance before slicing.

Detailed selected-design breadboarding may expose a shaping conflict. When it does, return the conflict to shaping for an explicit decision to revise the shape, cut behavior, run a focused spike, reopen selection, or stop the bet. Do not silently change the selected shape.

Do not dump or cluster implementation tasks, select committed slices, create a build sequence, or write production code inside shaping.

## Gated / orchestrated profile

Use the gated profile when a team, CI harness, multi-agent planner, or automation needs deterministic prerequisites and stopping points.

Default controlled sequence:

```text
accepted frame (x → f() → y)
→ accepted requirements
→ accepted appetite
→ candidate shapes
↔ candidate breadboards / focused spikes as needed
→ fit + reverse fit + appetite fit
→ explicit human selection
→ selected-design reconciliation
```

The gated profile may forbid moves that collaborative shaping allows provisionally. It must never weaken the universal human gates around selection, promotion to selected-design, slicing, or scope expansion.

The machine-readable contract is in `.agent-orchestration.yaml`.

## Minimal shaping document

```md
# [Project] — Shaping

## Working mode
- Profile: collaborative | gated
- Current move: R | S | fit | spike | candidate breadboard | appetite | selection

## Frame source
- ...
- x — current situation:
- f() — solution/shape variable:
- y — desired outcome:
- gap:
- boundaries:

## Project language and decisions
- Canonical terms:
- Relevant ADRs or decisions:
- Existing interfaces or seams:

## Requirements
| ID | Requirement | Status | Authority | Origin | Evidence refs |
|---|---|---|---|---|---|
| R0 | ... | Core goal | Working | FROM_X | ... |

## Appetite
- Authority: Unset | Working | Accepted
- Budget:
- Team / review point:
- Cut line:
- Accepted uncertainty:
- Must-resolve unknowns:
- Revisit conditions:

## Shapes
### CURRENT: [baseline, when relevant]
| Part | Mechanism | Flag |
|---|---|:---:|
| CURRENT1 | ... | |

### A: [short title]
| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | ... | |

## Candidate evidence
| Candidate | Evidence | Question resolved | R/S implication | Appetite implication | Remaining uncertainty |
|---|---|---|---|---|---|
| A | candidate breadboard or spike | ... | ... | ... | ... |

## Fit check
- Authority: Working | Decision-ready

| Req | Requirement | Status | CURRENT | A |
|---|---|---|:---:|:---:|
| R0 | ... | Core goal | ✅ | ✅ |

## Reverse fit check
| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| A1 | ... | R0 | ✅ |

## Requirement coverage
| Req | Supporting selected part(s) | Coverage | Realization question |
|---|---|:---:|---|
| R0 | A1 | ✅ | ... |

## Appetite fit
| Shape | Fits? | Required cuts | Uncertainty / spike |
|---|:---:|---|---|
| A | ... | ... | ... |

## Decision
- Status: exploring | decision-ready | selected | stopped
- Chosen direction:
- Rationale:
- Cuts / non-goals:
- Remaining unknowns:
- Candidate breadboard reconciliation:

## Next useful move
- revise R | revise S | fit-check | spike | candidate-breadboard | set/revisit appetite | select | stop
```

## Guardrails

- Start where the useful thinking already is: R, S, evidence, or prototype.
- Keep requirements separate from mechanisms even when extracting R from S.
- Let R, S, fit, spikes, sketches, and candidate breadboards iterate freely while material is working.
- Make accepted-versus-working state legible.
- Set and accept appetite before selection, even if shape exploration began earlier.
- Compare more than one serious path when alternatives genuinely exist; do not manufacture alternatives when they do not.
- Use candidate breadboards only to resolve decision-relevant uncertainty.
- Keep candidate breadboards subordinate to the shaping artifact and named candidate.
- Do not let unequal exploratory depth imply selection.
- Treat `CURRENT` as evidence, not automatically as future intent.
- Preserve stable IDs and rejected alternatives as an audit trail.
- Use a focused spike only for an unknown that matters to the decision.
- Reconcile consequential sketches through `sketch-reconciliation` before silently changing accepted artifacts.
- Stop at the human selection gate.
- Promote or reconcile a candidate breadboard only after explicit selection.
- Do not create implementation tasks or code.