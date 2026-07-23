---
description: Create or update only the requirements / criteria table before sketching solution shapes.
argument-hint:
- problem
- notes
- transcript
- frame
- or existing shaping file
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the user needs the judging criteria made explicit before the agent proposes or selects a shape.

Also read `docs/human-decision-gates.md` and stop at Gate 2: Requirements accepted.

User request and source context:

$ARGUMENTS

Produce or update only the requirements / criteria portion of a shaping artifact.

Include:

- requirement IDs such as `R0`, `R1`, `R2`
- requirement text stated as needs, outcomes, constraints, or quality bars
- status values such as Core goal, Must-have, Nice-to-have, Undecided, or Out
- source notes or assumptions when useful
- rejected or out-of-scope criteria when they clarify boundaries

Apply the requirement smell test from `shaping/SKILL.md`:

- requirements must not name a specific UI, runtime, vendor, protocol, storage method, or architecture unless that mechanism is truly a constraint
- rewrite mechanisms as needs when possible
- move mechanism-like ideas into a parking lot for later shape work

Do not propose solution shapes.
Do not run a fit check.
Do not select a direction.
Do not breadboard.
Do not write production code.

End with a short Gate 2 readiness note:

- `Ready for /appetite` when the criteria are good enough to bound the bet
- `Needs human decision` when criteria are still missing, conflicting, or mechanism-heavy
