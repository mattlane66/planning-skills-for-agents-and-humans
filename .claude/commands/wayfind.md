---
description: Chart or advance a bounded multi-session planning effort as a shared map of dependent decision, evidence, prototype, and prerequisite tickets.
argument-hint:
- loose idea or accepted frame
- map path or issue
- optional ticket
- optional tracker
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
- Skill
disable-model-invocation: true
---

Read `AGENTS.md` and `wayfinding/SKILL.md` first.

Source context:

$ARGUMENTS

If the source names an existing Wayfinding map, work through that map and resolve at most one non-evidence frontier ticket. Otherwise chart a new map only when the destination is bounded and the planning route genuinely spans sessions.

Use local Markdown unless the user or product repository explicitly selects an available external tracker. Route every active ticket to exactly one canonical local planning skill or evidence move. Never invoke another skills repository.

Keep the map and tickets as coordination records. Write accepted decisions into their canonical planning artifacts, preserve all human gates, and stop before production code or implementation backlog creation.
