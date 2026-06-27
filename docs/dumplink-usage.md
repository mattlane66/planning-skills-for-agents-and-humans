# Dumplink usage

Dumplink turns shaped work into vertical task groups, dependency-aware sequence, risk states, scope cuts, acceptance checks, and a bounded agent handoff packet.

Use it after framing, shaping, selection, and usually breadboarding. Do not use it to replace framing or shaping.

## When to use it

Use Dumplink when:

- a shaped project has been selected
- there is a fixed appetite or bounded build pass
- the work is too large for a single implementation move
- horizontal tickets would lose the intended behavior
- risk, dependency order, or scope cuts need to be visible before coding

## Command forms

Claude Code:

```text
/dumplink planning/shaping.md planning/breadboard.md "Appetite: 4 weeks"
```

Gemini CLI:

```text
/dumplink planning/shaping.md planning/breadboard.md "Appetite: 4 weeks"
```

Codex prompt:

```text
Use AGENTS.md and dumplink/SKILL.md.
Create a Dumplink plan for the selected shaped project.
Cluster tasks into vertical task groups, mark risk states, map dependencies, sequence the build, define scope cuts, write acceptance checks, and end with one bounded agent handoff packet.
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

## Core rule

Dumplink should preserve the shaped project whole while making implementation sequence clear.

It should not flatten the work into a generic ticket backlog.
