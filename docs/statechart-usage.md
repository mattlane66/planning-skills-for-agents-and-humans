# Statechart usage

Use the Statechart skill only when a selected portion of an accepted breadboard has enough state complexity that the wiring tables are hard to reason about by themselves.

Good signals include retries, timeouts, approvals, lifecycle stages, background messages, cancellation, or several valid actions from the same state.

## Inputs

- an accepted breadboard
- a selected scope or slice
- the relevant place, affordance, store, and wiring IDs

## Output

1. State inventory
2. Transition table
3. Mermaid `stateDiagram-v2` projection
4. Gaps and proposed breadboard updates

The transition table is primary. Mermaid is a visual projection. The accepted breadboard remains authoritative.

## Invocation

Claude Code with the installed plugin:

```text
/planning-skills:statechart planning/breadboard.md "Scope: V2 retry and cancellation"
```

When the repo-local `.gemini/commands/` wrappers are present, Gemini CLI can use:

```text
/statechart planning/breadboard.md "Scope: V2 retry and cancellation"
```

A native Gemini Agent Skills install does not install that wrapper. In that case, use the same natural-language skill request shown for Codex or another agent below.

Codex or another agent:

```text
Use the installed `statechart` skill and follow this product repository's own instructions.
Derive a statechart for [selected scope] from [accepted breadboard].
Preserve source breadboard IDs, mark unsupported behavior as inferred or missing,
and propose breadboard updates for gaps. Do not implement code.
```

## Boundary

Do not use a statechart as a second source of truth or as a mandatory step before slicing. If it conflicts with the breadboard, update the breadboard first and regenerate the statechart.
