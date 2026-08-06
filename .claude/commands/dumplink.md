---
description: Turn a selected project into vertical task groups, dependency-aware sequence, risk states, cuts, and a bounded handoff.
argument-hint:
- shaping doc
- breadboard
- selected project boundary
- appetite
- or notes
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `AGENTS.md` and `dumplink/SKILL.md` first.

Use Dumplink only after the project has been framed, shaped, selected, bounded, and given a fixed appetite. Dumplink creates the vertical implementation slices as task groups; it does not require one as input.

Source context:

$ARGUMENTS

Create or update a Dumplink plan with:

1. Project boundary
2. Task dump
3. Vertical task groups
4. Unknowns / knowns / done states
5. Dependency map
6. Build sequence
7. Scope cuts
8. Acceptance checks
9. Task-group approval gate
10. Active task-group handoff, only after human selection

If no selected project boundary is present, stop and name the missing project decision. Do not create task groups, a sequence, or a handoff.

Rules:

- Preserve the selected project's outcome, shape, appetite, boundary, exclusions, and non-goals.
- Keep every task group, dependency, cut, and sequence inside the selected project.
- Cluster vertically by judgeable behavior, not by discipline.
- Treat each task group as a vertical slice of the project.
- Mark risk state by the riskiest important task in each group.
- Sequence by risk and dependency, not convenience.
- Name scope cuts before panic.
- Stop for approval of the task-group plan and selection of the active task group.
- Give the implementation agent one selected task group at a time.
- Do not implement code.
