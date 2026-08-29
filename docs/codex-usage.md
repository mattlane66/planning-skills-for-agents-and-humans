# Codex usage

When maintaining this repository, Codex should use its `AGENTS.md` and `.agent-orchestration.yaml`. When the plugin is installed and Codex is working in a product repository, invoke the installed skills and keep that product repository's own `AGENTS.md` authoritative.

Codex follows the same planning authority, promotion gates, context-feeding rules, stable ID rules, drift protocol, and completion standard as other agents.

## Default interaction model

For human-guided product shaping, default to **collaborative mode**:

> **Start where the useful thinking already is. Exploration is fluid. Commitment is gated.**

Codex may begin from requirements, a rough solution, a prototype, current-system evidence, a fit question, or a focused unknown. During shaping, requirements (R), shapes (S), fit checks, focused spikes, sketches, and candidate breadboards may iterate in any useful order while they remain Working.

The hard gates remain:

- accepted requirements before final shape selection
- accepted Appetite and cut line before final shape selection
- explicit human selection
- explicit candidate-to-selected-design reconciliation
- accepted selected-design behavior before slicing
- explicit human slice selection before implementation

Use the **gated/orchestrated profile** only when the user, team policy, or automation explicitly wants strict prerequisites.

## Lead User research

Codex exposes the canonical `lead-user-research` skill rather than repository-style
slash commands. Use it as an optional upstream evidence move when a consequential
decision depends on future-facing trends, advanced users, unusually high-benefit
needs, pyramiding, or advanced analogs.

```text
Use the installed `lead-user-research` skill.
Start or resume the study at [workspace].
Derive the next valid phase from persisted state and perform only that phase.
Use real sources and preserve exact citations, source coverage, evidence lineage,
privacy controls, and outward-citation eligibility.
End with the standardized phase handoff and one next move or stop condition.
Do not invoke framing automatically after completion; propose the research-to-frame
handoff and wait for my acceptance.
```

To request a specific phase, name it explicitly—for example, “Use
`lead-user-research` Phase C on the next bounded evidence batch.” If persisted state
does not satisfy its prerequisites, Codex should stop or treat the request as an
explicit repair move rather than claiming progression.

## Collaborative shaping prompt

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Work in collaborative mode.

Start from whatever is already most concrete in my material: requirements, a proposed solution, a prototype, current-system evidence, or a specific unknown.
Move among R, S, fit checks, focused spikes, sketches, and candidate-shape breadboards whenever that is the smallest useful move.
Keep Working material separate from Accepted intent.
Do not force a fixed exploration sequence.
Do not select a shape until requirements and Appetite are accepted and the comparison is decision-ready.
Do not treat candidate evidence as selected intent or build scope.
Do not implement unless I explicitly select a bounded slice to build.

Source material:
[context]
```

### S-first example

```text
Use the installed `shaping` skill in collaborative mode.
I already have a solution idea. Capture it as Shape A first.
Then extract the provisional requirements it appears to serve, separate needs from mechanisms, and help me iterate among R, S, fit checks, spikes, and candidate breadboarding as useful.
Do not force me to complete framing or requirements before we can inspect the shape.
Do not select for me.
```

### R-first example

```text
Use the installed `shaping` skill in collaborative mode.
Start from these requirements and constraints, then let solution shapes emerge.
Move back to R whenever fit checks, spikes, or candidate breadboards reveal a missing or bad requirement.
Do not select for me.
```

## Gated / orchestrated prompt

```text
Use the installed planning skills in gated/orchestrated mode.
Follow `.agent-orchestration.yaml` strictly.
Require accepted frame, accepted requirements, and accepted Appetite before comparative shape work or candidate breadboarding.
Require decision-ready fit evidence and an explicit human choice before selection.
Require accepted selected-design behavior and a selected slice before implementation.
Stop at every human promotion gate.
```

## Focused shaping moves

Codex does not need Claude slash commands. Use natural-language equivalents when you want to constrain the current move without turning the entire process into a pipeline.

### Requirements / criteria

```text
Use the installed `shaping` skill.
For this move, work only on R.
Create, extract, or revise requirements from [problem / existing shape / prototype / fit failure / spike].
Keep needs separate from mechanisms and mark each requirement Working or Accepted when known.
Do not delete existing shapes, select a direction, or implement.
End by naming the smallest next useful shaping move.
```

### Appetite

```text
Use the installed `shaping` skill.
For this move, work on Appetite and the cut line.
Record whether Appetite is Working or Accepted.
Do not derive the budget from a preferred solution as if that were already selected.
Selection must wait for accepted Appetite.
```

### Shapes

```text
Use the installed `shaping` skill.
For this move, work on S.
Capture or revise the proposed solution shapes in [context].
This may be an S-first entry point.
If a shape reveals a missing need or constraint, propose it as Working R.
If Appetite is not accepted, keep Appetite-fit claims provisional.
Do not select or implement.
```

### Fit check

```text
Use the installed `shaping` skill.
Run the fit and reverse-fit checks that would clarify the current uncertainty.
If R or Appetite is provisional, label the result a Working fit check.
Use candidate breadboards and spikes as subordinate evidence.
Identify missing R or unjustified S rather than hiding them.
Do not select unless I explicitly choose and the hard selection gate is satisfied.
```

### Focused spike

```text
Use the installed `shaping` skill and `templates/spike.md`.
Investigate only this focused unknown: [question].
It may have been triggered by R, S, fit, a sketch, a candidate breadboard, or implementation reality.
Return explicit implications for R, S, fit, Appetite, and remaining uncertainty.
The spike gathers evidence; it does not choose the product direction.
```

### Candidate breadboard

```text
Use the installed `breadboarding` skill in `candidate-shape` mode.
Candidate: [shape / parts].
Question to resolve: [uncertainty].
Requirements authority: [Working | Accepted].
Appetite authority: [Unset | Working | Accepted].

In collaborative mode, provisional judging inputs are allowed. Map only enough places, affordances, stores, consequences, branches, and wiring to answer the question.
Return R/S/fit implications to shaping and label provisional claims.
Do not select, slice, create build scope, or implement.
```

### Select shape

```text
Use the installed `shaping` skill.
Record this human decision: [chosen shape].
First verify that requirements and Appetite are Accepted and the fit evidence is decision-ready.
Preserve rejected alternatives, cuts, and remaining unknowns.
Do not automatically promote candidate breadboard rows.
```

## Visual reconciliation

```text
Use the installed `sketch-reconciliation` skill.
Reconcile the attached visual with [frame, shaping, breadboard, or slice artifacts].
Separate observations from interpretations, map them to stable planning IDs, and show proposed deltas.
Do not change accepted behavior or scope until I accept the delta unless this prompt explicitly authorizes it.
```

## Selected-design breadboard

```text
Use the installed `breadboarding` skill in `selected-design` mode.
Use the explicitly selected shape, accepted requirements, accepted Appetite, and cut line.
Reconcile any candidate evidence instead of promoting it automatically.
Map accepted places, affordances, stores, wiring, branches, and candidate slice boundaries.
If concrete behavior exposes a shaping conflict, stop and return it to shaping.
Do not implement.
```

## Statechart

```text
Use the installed `statechart` skill.
Derive a statechart for [selected stateful scope] from [accepted breadboard].
Preserve source breadboard IDs and mark unsupported behavior as inferred or missing.
Treat the breadboard as authoritative and do not implement code.
```

## Interface contract

```text
Use the installed `interface-contracts` skill.
Create plain-language interface contracts only for the selected slice boundaries in [breadboard or slice artifact].
Do not create production schemas unless I explicitly ask.
```

## Executable breadboard

```text
Use the installed `executable-breadboards` skill.
Create an executable breadboard for [selected slice].
Include fixtures, example runs, expected visible results, expected state changes, edge cases, and acceptance tests.
Flag missing expected behavior instead of inventing it.
Do not implement yet.
```

## Dumplink

```text
Use the installed `dumplink` skill.
Turn [selected project] into a Dumplink plan when it needs vertical task groups, dependency-aware sequence, risk states, or scope cuts.
Preserve the selected project's outcome, direction, accepted Appetite, boundary, exclusions, and non-goals.
Do not expand the project or implement code.
Stop for approval and active task-group selection.
```

## Context packet before implementation

```text
Use the installed `feed-planning-context` skill.
Create a compact context packet for implementing [selected slice].
Include only accepted requirements, selected direction, accepted Appetite/cuts, relevant selected-design rows, optional contracts/examples/task group, non-goals, execution contract, and verification target.
Exclude Working alternatives and candidate breadboards as active build scope.
Do not implement yet.
```

Then give Codex the packet and explicitly name the selected slice to build.

## Drift check during implementation

```text
Check drift between [context packet / selected planning artifacts] and [changed files or implementation direction].
Return only one of:

No planning drift found.

or

Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:

Do not implement changes inside this drift check.
```

## Agent run log after meaningful work

```text
Create a concise agent run log for this session.
Include task, mode/profile, source artifacts used, files inspected, files changed, decisions made, drift checks, verification run, planning updates needed, and handoff notes.
Do not make the run log the source of truth for product decisions; point to the canonical planning artifacts.
```

## Key Codex behavior

- do not force R-first when the user starts from S
- do not treat S-first as permission to skip accepted judging inputs before selection
- do not confuse a focused move with a mandatory stage
- keep Working and Accepted authority visible
- do not one-shot from fuzzy or provisional shaping material into implementation
- preserve planning artifacts and update them when accepted discoveries change the plan
- keep implementation bounded to the selected slice
