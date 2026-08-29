# Claude slash commands

This repo includes project-level Claude slash commands that delegate to the canonical planning skills.

The commands live in:

```text
.claude/commands/
```

The unqualified names below apply when Claude Code is running in this repository. When using the generated plugin bundle, Claude namespaces entries as `/planning-skills:<name>`; see [Claude Code plugin packaging](./claude-code-plugin.md).

## Governing principle

The command wrappers constrain the **current move**, not the entire order of exploration.

> **Start where the useful thinking already is. Exploration is fluid. Commitment is gated.**

Use `/shape` as the broad collaborative front door. Use focused commands when you want to work on R, S, fit, a spike, or a breadboard without implying that the other moves had to happen first.

Use `/lead-user` when a consequential decision depends on future-facing opportunity evidence. It starts or resumes one valid research phase from persisted state; it is not a mandatory step before `/frame`.

## Commands

| Command | Uses skill | Purpose |
|---|---|---|
| `/plan` | `planning-router/SKILL.md` | Choose the smallest next planning move while respecting R-first, S-first, evidence-first, or uncertainty-first entry. |
| `/lead-user` | `lead-user-research/SKILL.md` | Start or resume the next valid Lead User research phase from persisted state. |
| `/lead-user-frame` | `lead-user-research` Phase A | Establish or revise the decision-relative research brief. |
| `/lead-user-discover` | `lead-user-research` Phase B | Establish trends, pyramiding paths, candidates, referrals, and advanced analogs. |
| `/lead-user-evidence` | `lead-user-research` Phase C | Inspect the next bounded real-source evidence batch. |
| `/lead-user-freeze` | `lead-user-research` Phase D | Judge sufficiency and freeze evidence only when justified. |
| `/lead-user-interpret` | `lead-user-research` Phase E | Interpret frozen evidence into findings, needs, principles, and gate results. |
| `/lead-user-shape` | `lead-user-research` Phase F | Shape only needs that pass the Concept Generation Gate. |
| `/lead-user-decide` | `lead-user-research` Phase G | Prepare the evidence-backed human decision and operational actions. |
| `/lead-user-deliver` | `lead-user-research` Phase H | Render supported outputs and a proposed research-to-frame handoff. |
| `/wayfind` | `wayfinding/SKILL.md` | Chart or advance a bounded multi-session planning effort through one shared map and frontier. |
| `/frame` | `framing-doc/SKILL.md` | Clarify the problem, outcome, evidence, and boundary when they are genuinely unclear. |
| `/shape` | `shaping/SKILL.md` | Main collaborative shaping surface: iterate among R, S, Appetite, fit, spikes, and candidate evidence without forcing a fixed exploration order. |
| `/criteria` | `shaping/SKILL.md` | Work on R for the current move; may extract requirements from an existing shape or prototype. |
| `/appetite` | `shaping/SKILL.md` | Set, revise, or accept the fixed time/scope budget and cut line. |
| `/sketch-shapes` | `shaping/SKILL.md` | Work on S for the current move; valid as an S-first entry point. |
| `/fit-check` | `shaping/SKILL.md` | Run Working or decision-ready fit and reverse-fit checks across existing shapes. |
| `/spike` | `shaping/SKILL.md` | Resolve one focused technical or empirical unknown and return R/S/fit/Appetite implications. |
| `/select-shape` | `shaping/SKILL.md` | Record or prepare a human shape-selection decision after the hard selection gate is satisfied. |
| `/reconcile-sketch` | `sketch-reconciliation/SKILL.md` | Reconcile a sketch, screenshot, wireframe, prototype, or whiteboard with planning IDs and apply only accepted deltas. |
| `/breadboard` | `breadboarding/SKILL.md` | Map current-state, candidate-shape, or selected-design behavior. |
| `/statechart` | `statechart/SKILL.md` | Derive a transition table and Mermaid statechart for a selected stateful scope. |
| `/dumplink` | `dumplink/SKILL.md` | Create vertical task groups, dependency-aware sequence, risk states, scope cuts, and a bounded handoff. |
| `/kickoff` | `kickoff-doc/SKILL.md` | Create a builder-facing orientation reference from accepted planning artifacts. |
| `/feed-context` | `feed-planning-context/SKILL.md` | Package accepted planning artifacts into a compact context packet for implementation work. |
| `/check-drift` | `AGENTS.md` + `docs/loop-prompting.md` | Check implementation direction against selected planning artifacts and stop if drift is found. |
| `/reflect-breadboard` | `breadboard-reflection/SKILL.md` | Compare accepted intent with implementation reality and prepare an explicit drift decision. |

## `/shape`: the broad collaborative surface

Use `/shape` when you want the agent to stay with the shaping conversation instead of treating planning as a pipeline.

Valid starts:

```text
/shape "I have a rough solution idea. Capture it as Shape A, tease out the requirements it implies, and help me refine both."
```

```text
/shape planning/notes.md "Start from these requirements, but move into shapes, fit, spikes, or candidate breadboarding whenever useful."
```

```text
/shape planning/prototype-notes.md "Treat this prototype as candidate evidence. Extract provisional R and S and help me work out what is actually worth keeping."
```

The agent may move among:

```text
R ↔ S ↔ fit
↑   ↕    │
└─ spikes / candidate breadboards / sketches
```

It must keep Working versus Accepted authority visible and stop at hard promotion gates.

## Focused shaping commands

These commands are **not** required stages.

### `/criteria`

Use when the current useful move is R.

It can:

- create R from problem/evidence
- extract R from an existing S
- revise Working R after a fit failure, spike, or candidate breadboard

It should not delete existing S or pretend that R necessarily came first.

### `/appetite`

Use when the current useful move is the budget, cut line, accepted uncertainty, or revisit condition.

Appetite may be Working during exploration. It must be Accepted before final shape selection.

### `/sketch-shapes`

Use when the current useful move is S.

It may be the first shaping command when the user already has a solution in mind. In collaborative mode, accepted R or Appetite are not prerequisites merely to capture or refine a candidate.

### `/fit-check`

Use whenever comparison itself will clarify the work.

If R or Appetite is provisional, label the output **Working fit check**. A Working fit check can expose missing R or unjustified S but cannot support final selection until the judging inputs are accepted.

### `/spike`

Use for one focused technical or empirical unknown.

A spike may be triggered from R, S, fit, a sketch, a candidate breadboard, or implementation reality. It returns explicit implications to the shaping artifact; it does not choose the direction.

### `/breadboard`

Declare one mode:

- `current-state`
- `candidate-shape`
- `selected-design`

In collaborative candidate-shape mode, requirements may be Working and Appetite may be Unset or Working. The breadboard must state those authority levels and cannot claim final fit, produce slices, or become build scope.

Selected-design mode remains strict: selected shape + accepted R + accepted Appetite/cuts + explicit candidate reconciliation.

## Human promotion commands

### `/select-shape`

This is a hard gate, not just another exploratory move.

Before recording selection, verify:

- accepted requirements
- accepted Appetite and cut line
- decision-ready fit / reverse-fit evidence
- important unknowns resolved, accepted, or visible
- explicit human choice

Do not infer selection from enthusiasm or from the fact that one shape was explored first.

### `/reconcile-sketch`

Use when a visual may change accepted planning. Working sketches can be explored freely; accepted intent changes only through an explicit delta decision.

## Gated / orchestrated mode

If the user wants stronger procedural control, use `/shape` with an explicit profile request:

```text
/shape "Use the gated/orchestrated profile. Enforce .agent-orchestration.yaml prerequisites and stop at every human promotion gate."
```

The controlled default is:

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

The focused commands can still be invoked directly, but the active profile decides whether their stricter prerequisites apply.

## Usage examples

```text
/plan "I have an idea for a new time-zone TUI but haven't written requirements yet."
```

```text
/shape "Build the shaping artifact from this rough solution idea; start S-first."
```

```text
/criteria planning/shaping.md
```

```text
/appetite planning/shaping.md "Two weeks, one engineer; cut reporting before core capture"
```

```text
/sketch-shapes planning/shaping.md
```

```text
/fit-check planning/shaping.md
```

```text
/spike planning/shaping.md "Can the current persistence layer support restore-on-launch without a new store?"
```

```text
/breadboard planning/shaping.md "mode: candidate-shape; candidate: A; question: restore behavior; requirements: Working; Appetite: Unset"
```

```text
/select-shape planning/shaping.md "Choose B"
```

```text
/reconcile-sketch planning/shaping.md planning/breadboard.md /path/to/sketch.png
```

```text
/statechart planning/breadboard.md "Scope: V2 retry and cancellation"
```

```text
/dumplink planning/shaping.md planning/breadboard.md "Selected project: onboarding; Appetite: 4 weeks"
```

```text
/feed-context planning/frame.md planning/shaping.md planning/breadboard.md
```

```text
/check-drift planning/context-packet.md src/features/onboarding/
```

## Design principle

Slash commands are thin invocation wrappers. They should not become a second copy of the method.

Keep the canonical workflow details in:

```text
AGENTS.md
.agent-orchestration.yaml
planning-router/SKILL.md
shaping/SKILL.md
breadboarding/SKILL.md
docs/human-decision-gates.md
```

When changing the method, update the canonical skill first. Update a wrapper only when invocation behavior, stopping point, profile behavior, or user-facing command name changes.
