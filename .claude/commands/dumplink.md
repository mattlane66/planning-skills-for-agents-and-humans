---
description: Organize work inside a selected slice into vertical task groups, dependency-aware sequence, risk states, cuts, and a bounded handoff.
argument-hint: [shaping doc, breadboard, selected slice, appetite, or notes]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `AGENTS.md` and `dumplink/SKILL.md` first.

Use full Dumplink mode only after the project has been framed, shaped, given a fixed appetite, and narrowed to a selected slice.

Source context:

$ARGUMENTS

Create or update a Dumplink plan with:

1. Project boundary
2. Task dump
3. Task groups
4. Unknowns / knowns / done states
5. Dependency map
6. Build sequence
7. Scope cuts
8. Acceptance checks
9. Agent handoff packet

If no selected slice is present, switch to pre-slice exploration: label all groups as candidates, surface risks and slice-selection questions, and stop before sections 6–9 become build commitments.

Rules:

- Preserve the selected shape and non-goals.
- Keep every committed task group, dependency, cut, and sequence inside the selected slice.
- Cluster vertically by judgeable behavior, not by discipline.
- Mark risk state by the riskiest important task in each group.
- Sequence by risk and dependency, not convenience.
- Name scope cuts before panic.
- Give the implementation agent one bounded task group at a time.
- Never create a build sequence or agent handoff before a human selects the slice.
- Do not implement code.
