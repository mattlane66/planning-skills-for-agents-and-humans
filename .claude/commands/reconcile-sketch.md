---
description: Reconcile an attached sketch, screenshot, mockup, wireframe, or whiteboard with existing planning artifacts without silently changing scope.
argument-hint:
- visual plus frame
- shaping
- breadboard
- or slice artifact paths
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `sketch-reconciliation/SKILL.md` first and follow it as the primary instruction for this command.

User request, visual, and source context:

$ARGUMENTS

Inspect the visual, separate observations from interpretations, map observations to stable planning IDs, and show proposed deltas.

Stop for a human decision before changing requirements, selected mechanisms, scope, or behavior unless the user explicitly authorized those changes in this request.

After acceptance, update every affected planning layer together and rerun fit checks when requirements or shape parts changed. Do not implement production code.
