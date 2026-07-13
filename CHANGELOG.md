# Changelog

## v1.1.0 — Release integrity

### Fixed

- Added the MIT license text referenced by the plugin manifests.
- Established root skill folders as the canonical source and synchronized all packaged `skills/` copies.
- Added byte-for-byte packaged-skill parity checks.
- Fixed broken artifact references in `.agent-orchestration.yaml`.
- Aligned drift-check authority order with Dumplink task-group precedence.
- Unified Claude, Codex, and MCP package versions.

### Improved

- Added the optional Statechart skill across packaged skills, templates, commands, MCP routing, documentation, examples, and health checks.
- Reworked the README around a 10-minute entry path and the Frame → Shape → Breadboard core workflow.
- Updated Claude, Codex, Gemini, MCP, and invocation documentation to cover the complete skill set.
- Made the generated Claude bundle self-contained, removed duplicate command/skill names, and updated command permissions to current Claude tool names.
- Made MCP artifact tools read canonical template files instead of hard-coded duplicates.
- Made MCP skill and template exposure track the canonical inventory and orchestration manifest.
- Replaced the MCP workflow recommender's default Dumplink step with prerequisite-aware routing.
- Added reproducible MCP installs, compilation tests, recommendation tests, and package locking.
- Made lifecycle hooks executable and non-blocking by default, with explicit strict mode for blocking behavior.
- Strengthened repository health checks for manifests, references, generated bundles, docs, and MCP verification.
- Clarified that `evals/` contains structural contract fixtures, not behavioral model benchmarks.

## v0.1.0 — Initial public release

Initial reusable release of Planning Skills for Agents and Humans.

### Included

- Framing, shaping, breadboarding, kickoff, context-feeding, and reflection skills.
- Root canonical skill folders and packaged plugin copies.
- Tool-neutral `AGENTS.md` instructions and Claude, Codex, Gemini, and MCP adapters.
- A small grocery-list walkthrough and canvas-export guidance.
