---
description: Turn kickoff notes or transcripts into a builder-facing reference document organized by shaped territory.
argument-hint: [kickoff notes/transcript paths and desired output path]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `kickoff-doc/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when a project has already been discussed and shaped enough that builders need a durable reference document.

User request and source context:

$ARGUMENTS

Produce or update a kickoff artifact organized by the product or system territory, not by conversation chronology. Include, as applicable:

- Frame
- Shape
- System / product areas
- Decisions attached to the areas they affect
- Constraints
- Open questions
- Explicit exclusions
- Self-check

Do not turn the kickoff doc into an implementation task list unless the user explicitly asks for a handoff plan after the reference document is complete.
