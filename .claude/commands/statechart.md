---
description: Derive a transition table and Mermaid statechart for a selected stateful portion of an accepted breadboard.
argument-hint:
- accepted breadboard
- selected scope or slice
- and optional target statechart file
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `AGENTS.md` and `statechart/SKILL.md` first.

Source context:

$ARGUMENTS

Create or update a statechart artifact for only the selected stateful scope.

Include:

1. Source breadboard and selected scope
2. State inventory
3. Transition table
4. Mermaid `stateDiagram-v2` projection
5. Gaps and proposed breadboard updates

Preserve source breadboard IDs. Mark unsupported behavior as inferred or missing. Do not invent retries, timeouts, cancellation, hierarchy, or parallel regions. The accepted breadboard remains authoritative. Do not implement code.
