# Changelog

## Unreleased

### Added

- Added deterministic Lead User next-phase routing, a `/lead-user` start/resume
  controller, and focused Phase A–H wrappers for Claude Code and Gemini CLI.
- Added an explicit research-to-frame handoff template and human acceptance gate.
- Added a complete synthetic Lead User v1.7 reference study with qualified, derivative,
  contradictory, concept-shaping, operational-action, and privacy-safe drill-down state.
- Added a blind real-runtime assurance harness that scores generated study artifacts
  independently of adapter self-report, plus a manual GitHub Actions workflow.

### Improved

- Integrated Lead User Research into the planning router, orchestration contract,
  cross-platform invocation guidance, and optional upstream planning flow without
  making research a mandatory predecessor to framing.
- Made source content explicitly `UNTRUSTED_DATA`, persisted instruction-risk handling,
  and added a malicious-source regression fixture.
- Strengthened structural validation for source, evidence, trends, lineage, findings,
  concept gates, sufficiency dimensions, decision status, completion, and cross-format
  privacy/state markers, including a deterministic brief-to-state fingerprint.
- Replaced narrative action strings with evidence-oriented A## execution contracts and
  made the Decision Brief action-first, evidence-linked, and privacy-safe by default.
- Made Lead User assurance cover every authoritative registry, explicit synthetic-fixture
  isolation, falsification/observability ledgers, pyramiding, lineage conflicts,
  transitive concept/ACT evidence, shaping-frame output, and human selection provenance.

### Fixed

- Prevented empty negative interpretations and completed insufficiency repairs from
  looping forever by persisting explicit interpretation and repair transitions.
- Refused non-empty initializer targets, required adversarial and discovery registries,
  required evidence bases, and rejected unsafe outward URLs and Markdown injection.
- Made private-identity detection token-aware, prevented derivative lineage from also
  counting as independent, and enforced evidence-backed trend/LU paths at decision gates.
- Rewrote every Lead User support path in the generated Claude plugin to a resolvable
  bundle-local path and added bundle regression checks.
- Rendered accepted shaping frames, real candidate/selected mechanism states, human
  selection provenance, rotated parts, and prominent synthetic-fixture warnings.

## v1.3.1 — Routing safety and reproducible releases — 2026-08-11

### Fixed

- Made MCP workflow recommendations honor explicit skill exclusions, negated prerequisite states, and clearly labeled untrusted quoted material.
- Required an accepted breadboard before recommending Statechart and added regression coverage for routing, prompt-injection, and source-trust boundaries.
- Derived the MCP server version from its package manifest so runtime metadata cannot drift from coordinated plugin versions.
- Defined `active_scope` as the canonical machine-readable alias for either one selected slice or one selected Dumplink task group.

### Added

- Added deterministic release tooling for all Claude upload ZIPs, the Claude Code plugin bundle, and a `SHA256SUMS` manifest.
- Added success-gated automatic version tagging after Repo health passes on `main`; existing tags are never moved or recreated.
- Added CodeQL analysis, weekly Dependabot updates, Python dependency auditing, and an opt-in blind real-runtime behavior-evaluation workflow.
- Added contribution, security, conduct, issue, and pull-request guidance plus Dumplink source attribution.

### Security

- Separated trusted routing instructions from untrusted transcripts, issue bodies, web content, pasted files, quoted text, and tool output across canonical and packaged skill surfaces.
- Pinned every GitHub Action to a full commit SHA, applied least-privilege workflow permissions, disabled persisted checkout credentials, and added bounded workflow timeouts and concurrency.
- Documented that non-loopback visualizer hosting has no authentication and is appropriate only on trusted networks.

### Changed

- Hardened tag releases to require exact stable SemVer, coordinated versions, an exact changelog section, ancestry on `main`, a passing full health suite, and prebuilt checksummed assets before publication.
- Isolated npm verification in a task-scoped cache so health checks do not depend on a writable user-level npm cache.
- Updated the MCP SDK and `tsx` within their existing major-version compatibility boundaries.

## v1.3.0 — Fluid shaping, Wayfinding, and verifiable breadboards — 2026-08-11

### Improved

- Made collaborative shaping fluid by default: teams can start R-first, S-first, evidence-first, or uncertainty-first and move among requirements, shapes, fit checks, focused spikes, sketches, and candidate breadboards while material remains Working.
- Reframed human gates as promotion/commitment gates rather than navigation locks; Accepted requirements and Appetite still constrain selection, candidate evidence still requires reconciliation, and selected behavior/scope still gate implementation.
- Added explicit `collaborative` and `gated` orchestration profiles so interactive human shaping can stay flexible while automation and policy-controlled workflows retain deterministic prerequisites.
- Allowed collaborative candidate-shape breadboarding to use Working requirements or Unset/Working Appetite while keeping final fit/Appetite claims provisional and build scope forbidden.
- Updated Claude Code, Codex, Gemini CLI, Claude Design, MCP integration guidance, runtime adapters, README/start-here/workflow docs, quality rubric, eval corpora, and health checks to describe the same profile behavior.
- Declared the MIT license in every canonical skill and split breadboarding's detailed notation and slicing material into an on-demand reference.
- Separated portable Agent Skills metadata from Claude Code, Codex, Gemini CLI, Claude Design, and MCP adapter behavior.
- Made Claude human-gate aliases manual-only, hid alias-backed generated skills from duplicate slash-menu discovery, and added operational metadata to direct-only Claude skills.
- Added native Gemini skill installation guidance, Codex skill-only boundary checks, Claude Design example packaging, and shared activation fixtures across all skills.
- Replaced ad hoc frontmatter parsing with YAML validation and added runtime adapter regression tests.
- Added CI validation for every generated Claude upload package, including ZIP roots, metadata, cross-skill references, and required local resources.
- Clarified when Claude Design should invoke a skill directly and when repository-aware work must return to Claude Code.
- Made custom package-output cleanup non-recursive and fail closed around protected paths, unrelated content, directories, and symlinks.
- Expanded repository health checks to run packager tests and dependency audits.
- Unified root, Claude upload, and MCP skill descriptions behind `skill-metadata.json`, with parity and boundary regression checks.

### Added

- Added `/spike` focused shaping wrappers for Claude Code and Gemini CLI; spikes can originate from R, S, fit, sketches, candidate breadboards, or implementation reality and return explicit R/S/fit/Appetite implications without deciding the product direction.
- Added Gemini `/shape` and `/breadboard` wrappers for parity with the collaborative Claude shaping surface.
- Added a solution-first shaping walkthrough showing rough Shape A → Working R → Working fit → spike/candidate breadboard → Accepted judging inputs → explicit human selection → selected-design reconciliation.
- Added workflow and activation eval cases for S-first shaping, Working fit checks, provisional candidate breadboarding, focused spikes, gated-profile prerequisites, and hard selection gates.
- Added the `wayfinding` skill and `/wayfind` wrappers for coordinating dependent planning decisions across sessions without creating a second source of product truth.
- Added portable local-Markdown and optional issue-tracker adapters, Wayfinding map and ticket templates, MCP routing, and cross-runtime activation coverage.
- Added a Claude and Claude Design workflow that separates canonical skills from Claude Code command wrappers.
- Added uploadable Claude skill ZIP generation with optimized trigger metadata and bundled supporting resources.
- Added positive, automatic-selection, near-neighbor, negative-trigger, command-wrapper, and cross-surface fallback tests for Claude skill invocation.
- Added packager safety tests and regression coverage for hidden support files and malformed visualizer paths.

### Fixed

- Removed the implicit requirement that ordinary interactive shaping must proceed through criteria → Appetite → shapes before useful solution exploration can occur, while preserving the same strict selection and build gates.
- Preserved dot-prefixed support-file references in generated Claude skill packages and made piped CI failures propagate correctly.
- Reconciled frame, appetite, shape-selection, kickoff-authority, context-feeding, and breadboard-reflection rules across canonical artifacts and adapters.
- Removed task grouping and slicing from shaping, separated descriptive and normative breadboarding, and made Dumplink ingest one selected project, create its vertical task-group slices, then stop for human plan approval and active-group selection.
- Upgraded repository-health Actions to their Node 24-based major versions and added manual workflow dispatch for explicit CI verification.
- Removed moderate-or-higher MCP dependency vulnerabilities and made the visualizer return a bounded `400` response for malformed encoded paths.

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
