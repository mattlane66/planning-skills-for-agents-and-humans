---
description: Turn kickoff notes or transcripts into a builder-facing reference document organized by shaped territory.
argument-hint: "[kickoff notes, transcript, or planning artifact path]"
---

Use the canonical planning skill at `kickoff-doc/SKILL.md`.

Create a kickoff document from the user's input or referenced files.

Default behavior:
- organize by system area or shaped territory, not transcript order
- preserve the team's real language where it helps recognition
- attach decisions to the area they affect
- keep build sequence, slice order, and implementation tasks separate unless clearly requested
- do not invent new conclusions beyond the source material
- stop with a builder-facing reference doc unless the user asks to build

Input:
$ARGUMENTS
