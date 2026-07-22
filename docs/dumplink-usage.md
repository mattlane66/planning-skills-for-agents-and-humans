# Dumplink usage

Dumplink organizes work inside a selected slice into vertical task groups, dependency-aware sequence, risk states, scope cuts, acceptance checks, and a bounded agent handoff packet.

Use its full mode after framing, shaping, breadboarding, and human slice selection. Do not use it to replace framing, shaping, or slice selection.

## When to use it

Use Dumplink when:

- a shaped project has been selected
- there is a fixed appetite or bounded build pass
- a selected slice and its exclusions are explicit
- the work is too large for a single implementation move
- horizontal tickets would lose the intended behavior
- risk, dependency order, or scope cuts need to be visible before coding

## Command forms

Claude Code:

```text
/dumplink planning/shaping.md planning/breadboard.md planning/slices.md "Appetite: 4 weeks"
```

Gemini CLI:

```text
/dumplink planning/shaping.md planning/breadboard.md planning/slices.md "Appetite: 4 weeks"
```

Codex prompt:

```text
Use AGENTS.md and dumplink/SKILL.md.
Create a Dumplink plan inside the selected slice.
Cluster tasks into vertical task groups, mark risk states, map dependencies, sequence the build, define scope cuts, write acceptance checks, and end with one bounded agent handoff packet.
Preserve the slice boundary and exclusions. If no slice is selected, produce candidate groups and slice-selection questions only; do not create a build sequence or handoff.
Do not implement code.
```

## Output shape

A Dumplink plan should include:

1. Project boundary
2. Task dump
3. Task groups
4. Unknowns / knowns / done states
5. Dependency map
6. Build sequence
7. Scope cuts
8. Acceptance checks
9. Agent handoff packet

The full output requires a selected slice. Before slice selection, exploration may include only a rough dump, candidate groups, risks, dependencies, cut options, and the decision question needed to select a slice.

## Core rule

Dumplink should preserve the selected slice whole while making implementation sequence clear.

It should not flatten the work into a generic ticket backlog, enlarge the selected slice, or turn exploratory candidates into a build commitment.
