# Changelog

## v1.2.0 - Planning gates, visual reconciliation, and live planning views

### Added

- Added the `sketch-reconciliation` skill and `/reconcile-sketch` wrappers for Claude Code and Gemini CLI.
- Added a durable sketch-reconciliation template with observation, mapping, delta, decision, fit-impact, and ripple sections.
- Added a local Mermaid viewer that watches one or more planning Markdown files and hot-reloads every diagram in the browser.
- Added exact MCP routing for `R x A`, `A x R`, spike, shape-update, sketch-reconciliation, slicing, slice-planning, and execution-verification shorthand.
- Added an explicit appetite gate plus `/appetite` wrappers for Claude Code and Gemini CLI.

### Improved

- Extended the tool-neutral orchestration contract with an explicit visual-reconciliation gate.
- Added regression coverage for the conversational prompts used in an end-to-end shaping session.
- Extended repository health checks to validate the new skill, command surfaces, visualizer package, and viewer documentation.
- Made the generated Claude bundle self-contained for skill, agent-instruction, template, documentation, orchestration, and hook references.
- Synchronized context-packet requirements and cross-platform installation guidance for product-repository use.

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
