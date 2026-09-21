---
description: Compile canonical planning artifacts into a normalized PlanningPackage plus a responsive visual shaped-work package.
argument-hint:
- planning directory
- optional output paths
- optional --svg-dir
- optional --png-dir
- optional --pdf-output
allowed-tools:
- Read
- Glob
- Bash
disable-model-invocation: true
---

Read `AGENTS.md` and `PLANNING-PUBLISHER.md` first.

This command publishes existing planning truth. It does not create or revise requirements, select a shape, accept a breadboard, choose build scope, or reconcile visual changes.

User request / arguments:

$ARGUMENTS

Resolve the planning directory from the arguments. If none is supplied and `planning/` exists, use `planning/`.

Run the deterministic publisher from the installed plugin:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/publish-shaped-work.py" \
  --planning-dir "<planning-dir>" \
  --output "<planning-dir>/shaped-work.html" \
  --json-output "<planning-dir>/planning-package.json" \
  --svg-dir "<planning-dir>/shaped-work-assets"
```

Pass `--png-dir` or `--pdf-output` only when explicitly requested. If the optional CairoSVG dependency is unavailable, report that HTML/JSON/SVG succeeded and explain the optional dependency rather than changing the plan.

Do not edit canonical planning artifacts to make publication pass. If the publisher reports an unknown stable ID or ambiguous/missing canonical input, surface that as a planning/presentation mismatch and stop.
