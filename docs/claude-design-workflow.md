# Using Claude Design with the Planning Skills Repository

Use Claude Code to create and preserve authoritative planning artifacts. Use Claude Design when the work benefits from a visual, spatial, or interactive surface.

The key change in this workflow is that **you do not have to start from a frame or requirements list**.

> **Enter with what you have. Exploration is fluid. Commitment is gated.**

You can begin with:

- requirements or constraints (R-first)
- a solution already in your head (S-first)
- a rough interface, screen, or prototype
- current-system evidence
- a fit question, technical unknown, or risky interaction

Claude Design is especially useful for S-first and evidence-first shaping because it gives the human and agent a concrete surface to inspect together. Claude Code remains the preferred place to preserve the authoritative planning artifacts in the product repository.

## Before you begin

Direct invocation in Claude or Claude Design requires the relevant Planning Skills ZIPs to be uploaded and enabled. See [Install Planning Skills in Claude and Claude Design](./claude-skills-installation.md).

When a skill is available in Claude Design, invoke it by its canonical skill name or by an explicit natural-language request. If it is unavailable—or if the work requires reading or modifying the product repository—run it in Claude Code and bring the resulting artifact into Claude Design.

## Skill names versus command wrappers

The uploadable canonical skills are:

- `planning-router`
- `framing-doc`
- `shaping`
- `sketch-reconciliation`
- `breadboarding`
- `statechart`
- `interface-contracts`
- `executable-breadboards`
- `dumplink`
- `kickoff-doc`
- `feed-planning-context`
- `breadboard-reflection`

Claude Code also provides shorter command wrappers such as `/plan`, `/frame`, `/shape`, `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/spike`, `/select-shape`, `/breadboard`, and `/check-drift`. These wrappers expose focused moves within the canonical skills; they are not separate uploaded Claude skills.

In Claude Design, request the corresponding canonical skill and mode in plain language.

## The collaborative shaping surface

During collaborative shaping, the human and agent may move among:

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

This is the default interactive model. The surface is fluid; promotion gates remain strict.

## Entry path A — Start from R

**What you likely have:**

Research, stakeholder needs, constraints, a problem statement, or explicit requirements.

**Claude Code:**

Use `shaping` to capture Working R with stable IDs. Use framing only if the actual problem boundary is still too unclear to judge solutions honestly.

**Claude Design:**

Keep R visible while you sketch or prototype candidate solutions. Let the visual work reveal missing requirements, contradictions, or unnecessary constraints.

**Loop:**

R → S → fit → sketch / candidate breadboard / spike → revise R or S.

## Entry path B — Start from S

**What you likely have:**

A solution already in your head, a flow you want to try, or a strong product concept.

**Claude Code:**

Use `shaping` in collaborative S-first mode. Capture the idea as a named candidate such as Shape A rather than treating it as accepted intent.

Then extract the provisional requirements it appears to serve:

- what outcome is this mechanism trying to create?
- what constraint makes this mechanism seem necessary?
- which parts are merely preferences?
- which needs would still exist if the mechanism changed completely?

Record those as Working R.

**Claude Design:**

Render or sketch Shape A. Interact with it. Use concrete behavior to discover missing R, bad assumptions, and alternative mechanisms.

**Loop:**

S → provisional R → working fit → prototype / candidate breadboard / spike → revise S and R.

Do not force S-first work back through a formal frame merely because a frame document was not written first. Return to framing only when the missing problem boundary prevents honest judgment.

## Entry path C — Start from a prototype or visual

**What you likely have:**

Screens, a prototype, wireframe, whiteboard, Claude Design concept, or an interface someone expects to build.

Treat the visual as evidence, not accepted truth.

**Claude Design:**

Inspect what the visual actually implies:

- places and modes
- user actions
- hidden consequences
- implied data/state
- edge cases
- interaction assumptions

**Claude Code:**

Use shaping to extract provisional R and S. Use `sketch-reconciliation` only when the visual may change already accepted intent.

If one candidate is hard to judge behaviorally, use `breadboarding` in `candidate-shape` mode.

## Entry path D — Start from an uncertainty

**What you likely have:**

A shape mostly makes sense, but one unknown could change the decision.

Use the smallest evidence move:

- **focused spike** for a technical or empirical unknown
- **candidate-shape breadboard** for a behavioral or structural unknown
- **Claude Design prototype** for a visual or interaction uncertainty

Return the result to shaping as explicit R/S/fit/Appetite implications.

## Working versus accepted material

Claude Design can be extremely persuasive because visual polish makes ideas feel decided. Counteract that by labeling authority.

During exploration, keep visible:

- Requirements: Working | Accepted
- Appetite: Unset | Working | Accepted
- Shapes: Candidate | Selected
- Fit check: Working | Decision-ready
- Breadboard: current-state | candidate-shape | selected-design

A beautiful candidate prototype remains a candidate.

## Candidate-shape breadboarding in Claude Design

Use when one named candidate cannot be judged from a mechanism list or static sketch alone.

In collaborative mode, accepted R and Appetite are not prerequisites. Supply:

- candidate / shape-part IDs
- specific uncertainty
- current R authority
- current Appetite authority

Map or visualize only enough to resolve that uncertainty.

Claude Design can help exercise:

- navigation and places
- modal/blocking behavior
- local versus global state
- edge cases
- hidden system consequences
- transitions and visible outcomes

Return the implications to shaping. If R or Appetite is provisional, do not present final fit or selection readiness.

Candidate breadboards and prototypes cannot select themselves, produce slices, or become build scope.

## Working fit checks

You can run fit checks before R or Appetite are accepted when the comparison itself will improve the thinking.

Label them **Working fit checks**.

Use them to:

- expose missing requirements
- reveal unjustified mechanisms
- compare candidate behavior
- identify what needs a spike or prototype

Do not use a Working fit check as final selection evidence until the judging inputs are accepted.

## Appetite during exploration

Appetite may be:

- **Unset** — useful for early solution exploration, but no final fit claim
- **Working** — a tentative budget used to expose likely cuts
- **Accepted** — the human-approved budget that constrains selection

Claude Design can show what gets cut under a Working Appetite, but a shape is not selected until Appetite is Accepted.

## Hard promotion gate — select a shape

Before selection, use Claude Code to verify:

- the problem boundary is clear enough
- requirements are Accepted
- Appetite and cut line are Accepted
- candidate evidence is decision-ready
- fit and reverse-fit are visible
- Appetite implications are visible
- the human explicitly chooses

Claude Design may support the discussion. It does not infer the selection.

## Reconcile and develop the selected shape

After selection, invoke `breadboarding` in `selected-design` mode.

Do not automatically promote the candidate breadboard or prototype.

1. confirm selected shape parts, accepted R, Appetite, cuts, and remaining unknowns
2. remove candidate mechanisms that were not selected
3. reconcile surviving places, affordances, stores, branches, and wires against accepted intent
4. revise rows whose meaning changed
5. preserve unresolved gaps explicitly
6. obtain human acceptance

If detailed behavior exposes a consequential conflict, return to shaping. Decide whether to revise the shape, cut behavior, run a focused spike, reopen selection, or stop the bet.

Only after acceptance should the selected-design breadboard produce candidate slices.

## Select and exercise a vertical slice

Use Claude Code for the authoritative slice boundary and test contract; use Claude Design for interactive exercise.

Select the smallest vertical slice that produces an observable result and tests consequential uncertainty. Record:

- boundary
- demo path
- exclusions
- `Produces` line
- verification target

Use `executable-breadboards` only after the slice is selected. Add realistic data, normal cases, difficult cases, ambiguous cases, expected outputs, and acceptance tests without expanding scope.

## Validate and reconcile

Use the executable breadboard to test states, failures, interruptions, recovery paths, and acceptance scenarios.

Then run `/check-drift`, or use `breadboard-reflection` for a fuller comparison against:

- accepted frame / boundary
- accepted requirements and Appetite
- selected shape
- accepted selected-design breadboard
- intended slice

Make preserved intent, deliberate changes, accidental drift, missing behavior, invented behavior, and discoveries visible. Decide whether to correct implementation or revise planning; use Claude Code to preserve the accepted decision.

## Collaborative versus gated/orchestrated mode

### Collaborative — default

Use when a person is actively steering the work.

- start R-first, S-first, evidence-first, or uncertainty-first
- move freely among R, S, fit, spike, candidate breadboard, and visual prototype
- keep authority labels visible
- keep promotion gates strict

### Gated / orchestrated

Use when a team or automation needs deterministic order.

```text
accepted frame
→ accepted requirements
→ accepted Appetite
→ candidate shapes
↔ spikes / candidate breadboards
→ decision-ready fit
→ human selection
→ selected-design breadboard
→ selected slice
```

Tell Claude Code or Claude Design explicitly to use the gated profile and follow `.agent-orchestration.yaml`.

## The roles of Claude Design and Claude Code

### Claude Code is the primary environment for

- invoking repository-aware skills and command wrappers
- reading the product repository
- creating authoritative planning artifacts
- maintaining stable IDs and traceability
- recording Working versus Accepted authority
- recording candidate versus selected-design authority
- comparing plans with implementation
- writing accepted discoveries back into version control
- moving from planning into working code

### Claude Design is the working surface where you

- bring visual source material together
- explore R-first or S-first ideas visually
- keep requirements beside candidate shapes
- place candidate shapes side by side
- inspect candidate and selected-design breadboards
- annotate specific misfits
- interact with risky behavior before selection
- expose states and failures
- compare prototypes with accepted intent

The skills structure the reasoning. Claude Code preserves and executes it. Claude Design makes it visible, editable, and testable.
