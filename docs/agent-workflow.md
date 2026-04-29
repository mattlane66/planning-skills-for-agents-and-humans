# Agent Workflow

Use this workflow when an agent is helping turn unclear product work into buildable planning artifacts.

The workflow is tool-neutral. It works with Claude Code, Cursor, Codex, and other agentic environments. The exact invocation differs by tool; the planning discipline should stay the same.

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

## 3. Shape

Use this mode when multiple solution directions are possible.

Outputs:
- requirements or criteria
- alternative shapes
- selected shape
- fit check
- reverse fit check
- unknowns or spikes

Use the `shaping` skill.

## 4. Detail

Use this mode when the selected shape needs to become concrete enough to slice.

Outputs:
- places
- UI affordances
- non-UI affordances
- stores
- wiring
- demoable slices

Use the `breadboarding` skill.

## 5. Feed context

Use this mode before implementation work, especially when planning artifacts are long or numerous.

Outputs:
- compact context packet
- authority order
- must-preserve constraints
- selected slice
- non-goals
- verification target

Use the `feed-planning-context` skill.

## 6. Build

Use this mode only after a slice is selected.

Rules:
- implement only the selected slice
- preserve shaped intent
- keep stable IDs intact
- map implementation work back to requirements, affordances, stores, or slices
- propose a planning update if implementation reality conflicts with the plan

## 7. Reflect

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
- Is the next output useful to both humans and agents?

## Common failure modes

Avoid:

- jumping from notes directly to implementation
- treating a rejected shape as the selected direction
- pasting all raw context instead of feeding a compact context packet
- silently changing the plan when code reality pushes back
- using build mode before a slice exists
- treating reflection as critique before syncing the breadboard to reality
