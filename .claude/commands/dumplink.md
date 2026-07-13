---
description: Turn a selected shaped project into vertical task groups, dependency-aware sequence, risk states, scope cuts, and an agent handoff packet.
argument-hint: [shaping doc, breadboard, selected slice, appetite, or notes]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `AGENTS.md` and `dumplink/SKILL.md` first.

Use Dumplink only after the project has been framed, shaped, and selected for a fixed appetite or bounded build pass.

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

Rules:

- Preserve the selected shape and non-goals.
- Cluster vertically by judgeable behavior, not by discipline.
- Mark risk state by the riskiest important task in each group.
- Sequence by risk and dependency, not convenience.
- Name scope cuts before panic.
- Give the implementation agent one bounded task group at a time.
- Do not implement code.
