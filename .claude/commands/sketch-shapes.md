---
description: Sketch alternative solution shapes against accepted criteria without selecting one.
argument-hint: [accepted criteria, frame, notes, or existing shaping file]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the user wants multiple possible directions made visible before committing to one.

Also read `docs/human-decision-gates.md` and stop before Gate 3: Shape selected.

User request and source context:

$ARGUMENTS

Produce or update the Shapes section of a shaping artifact.

Include:

- `CURRENT` when the work touches an existing system
- 2-4 serious alternative shapes such as `A`, `B`, and `C`
- short titles that characterize each approach
- numbered shape parts such as `A1`, `A2`, `B1`, `B2`
- flagged unknowns with `⚠️` where a mechanism is still not concretely understood
- spike candidates for unresolved mechanics when needed

Keep requirements and mechanisms separate:

- do not rewrite criteria into UI choices
- do not treat a vague intention as a shape part
- do not silently turn one option into the selected direction

If sketching reveals missing or changed criteria, add a short `Possible criteria discovered` section instead of silently changing accepted requirements.

Do not run the full fit check unless the user explicitly asks.
Do not select a direction.
Do not breadboard.
Do not write production code.

End with a short Gate 3 readiness note:

- `Ready for /fit-check` when the alternatives are concrete enough to compare
- `Needs spike or more sketching` when one or more important shape parts remain too vague
