# Sketch reconciliation

Use sketch reconciliation when a screenshot, wireframe, mockup, whiteboard, or hand-drawn sketch makes you notice something that the current frame, shape, breadboard, or slices may not express.

The visual is evidence, not an automatic planning update.

## Quick use

Claude Code with the installed plugin:

```text
/planning-skills:reconcile-sketch path/to/shaping.md path/to/breadboard.md /path/to/sketch.png
```

When using the repository-local project command instead of the installed plugin, use `/reconcile-sketch`. Attach or paste the image in the same prompt when the client supports image input; otherwise pass a readable local image path as an argument.

Gemini CLI project command:

```text
/reconcile-sketch path/to/shaping.md path/to/breadboard.md /path/to/sketch.png
```

Codex or another agent:

```text
Use AGENTS.md and sketch-reconciliation/SKILL.md.
Reconcile this attached sketch with path/to/shaping.md and path/to/breadboard.md.
Separate observations from interpretations, map observations to stable IDs, and show proposed deltas.
Do not change selected behavior or scope until I accept the deltas.
```

## Procedure

1. Inspect the visual and record only visible facts as `OBS1`, `OBS2`, and so on.
2. Map every observation to existing requirement, shape-part, place, affordance, store, or slice IDs.
3. Mark each observation as `covered`, `clarifies`, `missing`, `conflicts`, or `ambiguous` at each relevant layer; for example, `R2: covered; Shape: missing`.
4. Separate newly discovered needs from proposed UI or implementation mechanisms.
5. Show explicit deltas with evidence and fit/scope impact.
6. Stop for a human accept/revise/reject/defer decision unless the user already gave an explicit update instruction. Keep undecided deltas marked `pending`.
7. Apply accepted changes across every affected artifact and rerun fit checks when requirements or shape parts changed.

Use [`templates/sketch-reconciliation.md`](../templates/sketch-reconciliation.md) when the reconciliation creates durable decisions.

Use ripple statuses consistently: `current` means inspected and aligned, `updated` means changed now, `stale` means accepted follow-up work remains, `not affected` means inspected but untouched, `not provided` means absent from the inputs, and `not assessed` means outside the inspected scope.

## Authority

A reconciliation record is not a new source of truth. The selected frame, shaping, breadboard, and slice artifacts remain authoritative until accepted deltas are written back to them.

The user's words outrank an inference from the visual. A static image cannot prove hidden behavior such as persistence, validation, navigation, parsing, or error handling.

## Example

See [`examples/sketch-reconciliation`](../examples/sketch-reconciliation/) for a visual that reveals a missing always-visible date affordance, the observation-to-plan mapping, and the accepted ripple update.
