# Loop Prompting for Planning Hygiene

Claude Code includes `/loop` for repeatedly running a prompt during a live session. This repo does not replace `/loop`. It gives `/loop` a planning-specific use: periodically checking whether implementation work is still aligned with the selected planning artifacts.

Use loop prompting during long implementation or refactor sessions where an agent may drift from the frame, selected shape, breadboard, selected slice, interface contracts, executable breadboard, non-goals, or verification target.

## What this is

Loop prompting is a planning-hygiene loop.

It asks the agent to keep checking:

- are we still building the selected slice?
- are we preserving the must-preserve constraints?
- are we respecting explicit non-goals?
- are we implementing the selected shape, not a discarded alternative?
- are we preserving interface contracts and executable breadboard examples?
- has implementation reality revealed a conflict that should update the plan?
- does the current code still satisfy the verification target?

## What this is not

Do not use loop prompting to:

- create new requirements
- expand scope
- silently rewrite the selected shape
- turn implementation discoveries into unreviewed product decisions
- replace `/check-drift`
- replace `/breadboard-reflection`

Use `/check-drift` for an explicit point-in-time drift check. Use `/breadboard-reflection` when there is already implementation to compare against the breadboard. Use `/loop` while the implementation session is still running and drift can still be caught early.

## Basic prompt

```text
/loop 10m Check whether the current work still matches the selected slice, must-preserve constraints, non-goals, breadboard, interface contracts, executable breadboard, and verification target. If there is drift, stop and return a "Planning drift found" note instead of continuing.
```

## Stronger prompt

```text
/loop 10m Check planning alignment against the active context packet, selected slice, shaping doc, breadboard, interface contracts, executable breadboard, non-goals, and verification target.

Return only one of:

1. No planning drift found.
2. Planning drift found:
   - Selected artifact says:
   - Current implementation direction is:
   - Risk:
   - Recommended move:

Do not expand scope. Do not invent new requirements. If implementation reality conflicts with the plan, propose a planning update or slice split instead of silently drifting.
```

## `/check-drift`

Use `/check-drift` when you want a direct drift check without setting up a recurring loop.

```text
/check-drift planning/context-packet.md src/features/onboarding/
```

Expected output is only one of:

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

## Recommended `.claude/loop.md`

Claude Code can use `.claude/loop.md` when `/loop` is run without an inline prompt. This repo includes a default `.claude/loop.md` that checks planning alignment against the active context packet, selected slice, shaping doc, breadboard, interface contracts, executable breadboard, non-goals, and verification target.

## When to use it

Use loop prompting for:

- long-running Claude Code sessions
- implementation after shaping
- implementation from a compact context packet
- risky refactors where intent can drift
- multi-agent or background-ish work where the agent may continue without fresh human review
- places where the selected slice is narrow and easy to accidentally expand

## How it fits the workflow

```text
Frame
  ↓
Shape
  ↓
Breadboard
  ↓
Slice
  ↓
Feed planning context
  ↓
Implement with /loop planning checks and /check-drift checkpoints
  ↓
Breadboard reflection when code exists
```

The loop does not make the plan more detailed. It protects the plan while work is in motion.

## Example with a context packet

```text
Use @planning/context-packet.md as the source of truth for this implementation session.

/loop 10m Check whether implementation is still aligned with @planning/context-packet.md. Pay special attention to Must preserve, Non-goals, Selected slice, and Verification target. If drift appears, stop and summarize it instead of continuing.
```

## Good loop output

```text
Planning drift found:
- Selected artifact says: V1 only supports creating a draft plan, not publishing it.
- Current implementation direction is: adding a Publish button and publish-state handling.
- Risk: expands scope beyond the selected slice and creates new product behavior not shaped yet.
- Recommended move: remove publish behavior from this slice or update the shaping/slice artifact before continuing.
```

## Bad loop output

```text
I noticed a publishing flow would be useful, so I added it.
```

That is exactly the drift this pattern is meant to prevent.
