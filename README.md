# Planning Skills for Agents and Humans

These planning skills turn fuzzy requests, messy transcripts, and partial designs into artifacts that humans and agents can actually build from. They help you clarify what the thing must be, so you are free to explore all the ways it might be.
They are best suited to meaningfully large, strategically important feature work: discrete bets with 2–6 week time budgets for small launch teams.
The skills are most powerful when grounded in your codebase. That context provides the ground truth humans and agents need to execute with confidence, especially during the spiking work inside shaping.
AI may be able to one-shot a simple app without this process. But for larger bets, the process gives you and your team a shared view of how the solution works. It also makes your prompts better as the work gets more concrete. And it leaves behind documents you can question later, so you can understand how and why the system was put together before you change it.
Ideally, you use these skills to help run, or process data from, a collaborative [shaping session](https://www.figma.com/community/file/1490786031847199566/shaping-session-playing-field-copy-me-template).

AI coding tools have become powerful new prototyping instruments, but they work best after good upstream/uphill shaping. Humans need to own the planning stack.

## Operating philosophy

Start here: [The Work Should Get Clearer](./MANIFESTO.md).

This repo helps teams preserve intent as work moves from idea to implementation. Use the skills at the handoffs where meaning is most likely to get lost:

- `/framing-doc` for turning raw notes or requests into a clear problem frame
- `/shaping` for comparing paths and selecting a bounded direction
- `/breadboarding` for making behavior, state, affordances, and wiring visible (aka as an Interaction Schematic)
- `/statechart` for deriving a transition table and Mermaid statechart from a selected stateful portion of an accepted breadboard
- `/interface-contracts` for making boundary-crossing data exchanges explicit
- `/executable-breadboards` for adding examples, fixtures, expected outputs, edge cases, and acceptance tests before build handoff
- `/kickoff-doc` for preparing the build team
- `/feed-planning-context` for giving AI agents bounded context
- `/breadboard-reflection` for repairing drift between plan and implementation

Claude Code and Gemini CLI users can also use thinner project slash commands when they want to stop at human decision gates instead of one-shotting the whole shape: `/criteria`, `/sketch-shapes`, `/fit-check`, `/select-shape`, and `/check-drift`. Codex users can use the equivalent prompt forms in [`docs/codex-usage.md`](./docs/codex-usage.md). See [`docs/claude-slash-commands.md`](./docs/claude-slash-commands.md) and [`docs/gemini-usage.md`](./docs/gemini-usage.md).

Get a quick lightweight feel for these design skills with this Custom GPT [here](https://chatgpt.com/g/g-699222e353288191afb01ea178db6da6-shape-to-slice-assistant).

<img width="1453" height="713" alt="Screenshot 2026-04-24 at 10 05 13 PM" src="https://github.com/user-attachments/assets/8b3848cc-3968-4792-8d77-5c38b81ce3b1" />

The emphasis is on pre-development legibility:
- frame the problem before racing to implementation
- compare alternatives before locking in a solution
- map places, affordances, state, and wiring before losing the plot while maintaining latitude
- derive a statechart only when a selected scope has enough state complexity to justify one
- keep high-level and low-level planning artifacts aligned as the work evolves
- feed planning artifacts to agents at the right fidelity so they preserve shaped intent instead of drowning in context
- check drift during implementation before accidental scope becomes product behavior

## Planning Skills vs. Spec Kit

This repo is not a replacement for [Spec Kit](https://github.com/github/spec-kit). It is a complementary planning layer. Use these skills earlier in the process to frame the problem, separate requirements from mechanisms, compare shapes, breadboard the system, and slice the work into demoable scopes. Then use a broader spec-driven workflow like Spec Kit when you want project-level specs, plans, tasks, and implementation orchestration.
Comparatively (including [HumanLayer](https://www.humanlayer.dev)):
- Planning Skills = figure out what to build to get people from where they are to where they ought to be and how to structure and derisk it
- Spec Kit = turn planning skills' vertical slices into an agent-specific implementation build plan while specifying exact file paths, dependencies, order, and test structure.
- HumanLayer = help agents carry out the build work reliably in real complex codebases

1. Raw notes / customer evidence / idea
   ↓
2. Planning Skills: framing
   Output: problem, forces, outcome, boundaries
   ↓
3. Planning Skills: criteria, shape sketches, fit checks, selected approach
   Output: requirements, options, fit checks, selected approach, non-goals
   ↓
4. Planning Skills: breadboarding
   Output: places, affordances, stores, state, wiring
   ↓
5. Optional Planning Skills: statechart for a selected stateful scope
   Output: state inventory, transition table, Mermaid statechart, gaps
   ↓
6. Planning Skills: slices, contracts, executable breadboard
   Output: demoable vertical slices, boundary contracts, examples, fixtures, expected outputs, edge cases, acceptance tests
   ↓
7. Planning Skills: feed-planning-context
   Output: compact implementation packet
   ↓
8. Spec Kit
   Output: spec.md, plan.md, data-model.md, contracts, tasks.md
   ↓
9. HumanLayer / CodeLayer / Claude Code / Gemini CLI / Codex
   Output: implementation, tests, PRs, review loops
   ↓
10. Drift checks and breadboard reflection
   Output: detect drift, update artifacts, repair intent/code mismatch

## Mode discipline

These skills are primarily for planning before implementation.

Default mode is planning/shaping:
- do not write runnable implementation code
- do not create full schemas, framework code, or production files
- use plain language, tables, lightweight pseudo-structures, and Mermaid where useful

Only move into implementation when the user or team explicitly selects a slice to build.

When building:
- implement only the selected slice
- preserve the shaped intent
- update planning artifacts if implementation discoveries change the plan
- leave a run log or handoff note after meaningful agent work

## Cross-agent setup

Use [`AGENTS.md`](./AGENTS.md) as the tool-neutral instruction surface for agents that understand repo-level instruction files. It captures the default mode, workflow, authority order, context-feeding rules, stable ID handling, drift protocol, and completion standard.

Use [`.agent-orchestration.yaml`](./.agent-orchestration.yaml) as the machine-readable workflow and harness contract for tools that can consume structured mode, gate, artifact, hook, and command metadata.

Claude Code users can install the skills natively and use `.claude/commands/` for slash-command wrappers. Gemini CLI users can use `GEMINI.md` and `.gemini/commands/`. Codex users should rely on `AGENTS.md` plus the prompt equivalents in [`docs/codex-usage.md`](./docs/codex-usage.md). Other tools such as Cursor and similar agent environments can use the same `SKILL.md` files as repo-local rules, prompt files, or reusable docs.

## Agent orchestration and harnessing

This repo is not a full agent runtime. It is the planning and harness contract layer.

Use these files when wiring the repo into an agent harness:

- [`.agent-orchestration.yaml`](./.agent-orchestration.yaml) — machine-readable modes, gates, allowed outputs, forbidden moves, artifacts, and hooks
- [`docs/agent-workflow.md`](./docs/agent-workflow.md) — human-readable workflow modes
- [`docs/loop-prompting.md`](./docs/loop-prompting.md) — recurring planning-alignment checks
- [`templates/drift-check.md`](./templates/drift-check.md) — strict drift-check output format
- [`templates/agent-run-log.md`](./templates/agent-run-log.md) — audit trail for meaningful agent runs
- [`docs/agent-run-records.md`](./docs/agent-run-records.md) — when and how to record agent runs
- [`docs/lifecycle-hooks.md`](./docs/lifecycle-hooks.md) — optional hook setup for context and drift reminders

The intended harness loop is:

```text
Choose mode
  ↓
Load only relevant artifacts
  ↓
Run the skill or command for that mode
  ↓
Stop at the human gate
  ↓
Feed compact context before build
  ↓
Check drift during build
  ↓
Reflect after implementation exists
```

For exact tool-by-tool invocation differences, see [`docs/agent-invocation-matrix.md`](./docs/agent-invocation-matrix.md). Claude supports project slash commands in this repo; Codex and Gemini-style clients use plugin, local skill, MCP, or prompt-recipe invocation rather than Claude-style slash commands.

## Skills

### `/framing-doc`
Turn source material such as interview transcript syntheses, strategy notes, stakeholder messages, etc. into a frame that captures the living world context and boundaries, current approach and result, and desired outcome. (NOTE: I use requirements and criteria interchangeably, which I define as unit items that give us the fitness for solving the problem, i.e., standards or rules used to judge the quality of a solution, e.g., various '-ilities', customer forces, costs (time, dev effort, $), risks, compatibility and complexity, purpose-built for problem (reflective), etc.). I also determine if a criterion is a Must Have or not.)

### `/shaping`
Collaboratively define requirements/criteria, list alternative approaches, compare their fit, and detail the selected direction.

In Claude Code and Gemini CLI, the shaping work can also be run as smaller gate commands when the team wants to pause between moves: `/criteria`, `/sketch-shapes`, `/fit-check`, and `/select-shape`. In Codex, use the equivalent prompt forms in [`docs/codex-usage.md`](./docs/codex-usage.md).

### `/breadboarding`
Map a system into places/screens/states, affordances, stores, and the wiring so behavior is concrete and vertically sliced and sequenced (based on unknowns/most risky parts and dependencies first) before implementation gets fragmented.

### `/statechart`
Turn a selected stateful portion of an accepted breadboard into a state inventory, transition table, and Mermaid statechart. Preserve breadboard IDs, mark unsupported interpretations as inferred or missing, and keep the breadboard tables authoritative.

Use it only when state complexity warrants it—for example, retries, timeouts, approvals, lifecycle stages, background messages, or several valid actions from the same state.

### `/interface-contracts`
Turn selected breadboard wires or slices into plain-language contracts for boundary-crossing data exchanges.

### `/executable-breadboards`
Turn a selected slice into a buildable, testable handoff with examples, fixtures, expected outputs, edge cases, and acceptance tests.

### `/breadboard-reflection`
Compare a breadboard to the implementation, repair drift, and look for design smells such as hidden state, weak boundaries, or missing steps.

### `/kickoff-doc`
Turn a kickoff conversation into a builder-facing reference doc organized around the territory being built.

### `/feed-planning-context`
Prepare framing, shaping, breadboard, kickoff, slice, or reflection artifacts for agent implementation work without overloading context. This skill packages the active task, source artifacts, authority order, must-preserve constraints, stable IDs, non-goals, current slice, and verification target into a compact context packet. It does not implement code.

## Agent context feeding

Planning artifacts are most useful to coding agents when they are fed at the right fidelity. Do not paste the whole planning stack by default. Use a compact context packet that tells the agent what to use, what to ignore, what to preserve, and how to verify alignment.

See [`docs/agent-context-feeding.md`](./docs/agent-context-feeding.md) for:

- context packet templates
- artifact-specific prompts for framing docs, shaping docs, breadboards, slice plans, kickoff docs, and reflections
- stable ID conventions for requirements, places, affordances, stores, and slices
- chunking rules for large artifacts
- drift-handling protocol when implementation reality conflicts with the plan

## Canvas export

Breadboard tables are the source of truth. Mermaid diagrams are portable visual projections. Canvas tools such as TLDraw, Excalidraw, FigJam, and Miro are review and collaboration surfaces.

See [`docs/canvas-export.md`](./docs/canvas-export.md) for the canvas export contract:

- stable ID rules for canvas-friendly diagrams
- Mermaid-to-canvas adapter pattern
- static image export versus semantic object export
- guidance for keeping tables authoritative over diagrams and canvases

## Examples

If you want to see the skills used step by step, start in [`examples/`](./examples).

The included `simple-grocery-list` example walks through:
- raw source notes
- a frame
- shaping with competing directions
- an optional kickoff doc
- a breadboard
- a post-implementation breadboard reflection

## Using these skills across agent tools

The `SKILL.md` files are plain Markdown instructions. Use them as native skills where supported, or as reusable prompt templates / repo-local instruction docs elsewhere.

The core workflow stays the same:

1. Start with raw notes or transcripts.
2. Create a frame.
3. Shape the problem: criteria, alternative shapes, fit checks, and selected direction.
4. Breadboard the chosen shape.
5. Optionally derive a statechart for a selected stateful scope.
6. Add contracts and executable breadboard details when the selected slice needs them.
7. Feed the selected planning artifacts into the agent as a compact context packet.
8. Check drift during implementation.
9. Reflect against implementation later when code exists.

What changes across tools is just **how you invoke the instructions**, not the method itself. See [`docs/agent-invocation-matrix.md`](./docs/agent-invocation-matrix.md) for the current support matrix and prompt recipes.

### Plain markdown workflow

The simplest portable setup is to keep the skill files in your repo and point your tool at them explicitly.

Example structure:

```text
docs/planning-skills/
  framing-doc.md
  shaping.md
  breadboarding.md
  statechart.md
  interface-contracts.md
  executable-breadboards.md
  kickoff-doc.md
  breadboard-reflection.md
  feed-planning-context.md

planning/
  frame.md
  shaping.md
  breadboard.md
  statechart.md
  interface-contracts.md
  executable-breadboard.md
  context-packet.md
  runs/
```

Example prompt:

```text
Read docs/planning-skills/shaping.md first.
Then help me shape this feature.
Separate requirements from mechanisms, compare options, run a fit check, and write the result to planning/shaping.md.
```

### Cursor

In Cursor, these skills work best as repo-local rules, prompt files, or docs the agent is told to read before acting.

Example prompt:

```text
Use the breadboarding instructions from docs/planning-skills/breadboarding.md.
Create a breadboard for the chosen shape in planning/breadboard.md.
Focus on places, affordances, visible consequences, and hidden system behavior that matters.
```

### Gemini CLI

Gemini CLI uses the root [`GEMINI.md`](./GEMINI.md), which imports [`AGENTS.md`](./AGENTS.md), and the project-local commands in `.gemini/commands/`.

See [`docs/gemini-usage.md`](./docs/gemini-usage.md) for:

- `/criteria`
- `/sketch-shapes`
- `/fit-check`
- `/select-shape`
- `/check-drift`

### Codex

Codex-style workflows should use [`AGENTS.md`](./AGENTS.md), [`.agent-orchestration.yaml`](./.agent-orchestration.yaml), and the prompt equivalents in [`docs/codex-usage.md`](./docs/codex-usage.md).

Example prompt:

```text
Use AGENTS.md and shaping/SKILL.md.
Run the fit-check gate only.
Compare the existing criteria and candidate shapes in planning/shaping.md.
Do not select a direction unless I explicitly choose one.
Do not breadboard or implement.
```

### MCP server

The included MCP server exposes planning skills and starter artifact templates to tools that prefer capability discovery over pasted docs.

It can return:

- planning skill instructions
- artifact templates
- the orchestration manifest

See `mcp-server/src/index.ts` for the exposed tool surface.

### Summary

- **Claude Code**: native skill packaging, `.claude/commands/`, `.claude/loop.md`, optional hooks
- **Gemini CLI**: `GEMINI.md` plus `.gemini/commands/`
- **Codex**: `AGENTS.md`, `.agent-orchestration.yaml`, plugin skills, and prompt equivalents in `docs/codex-usage.md`
- **MCP-compatible tools**: MCP server for skill and template discovery
- **Other tools**: prompt-template or repo-doc packaging
- **All agents**: preserve the same planning gates and source-of-truth artifacts

So the workflow is tool-agnostic in substance, with optional tool-specific packaging.

## Install for Claude Code

### As a Claude Code plugin

Use the repository root as the plugin directory:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans
cd ~/.local/share/planning-skills-for-agents-and-humans
claude --plugin-dir .
```

Then reload plugins in Claude Code:

```text
/reload-plugins
```

### As direct local skills

If you prefer direct skill symlinks, link each folder from the repo's `skills/` directory:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans

ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/framing-doc ~/.claude/skills/framing-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/kickoff-doc ~/.claude/skills/kickoff-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/shaping ~/.claude/skills/shaping
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/breadboarding ~/.claude/skills/breadboarding
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/statechart ~/.claude/skills/statechart
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/interface-contracts ~/.claude/skills/interface-contracts
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/executable-breadboards ~/.claude/skills/executable-breadboards
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/breadboard-reflection ~/.claude/skills/breadboard-reflection
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/feed-planning-context ~/.claude/skills/feed-planning-context
```

Each skill should be a direct child of `~/.claude/skills/`.

## Optional Claude Code hooks

This repo includes small hooks that remind the agent to keep planning artifacts and implementation aligned.

```bash
mkdir -p ~/.claude/hooks
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/planning-ripple.sh ~/.claude/hooks/planning-ripple.sh
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/pre-build-context-check.sh ~/.claude/hooks/pre-build-context-check.sh
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/planning-drift-check.sh ~/.claude/hooks/planning-drift-check.sh
```

See [`docs/lifecycle-hooks.md`](./docs/lifecycle-hooks.md) for setup examples.

The hooks are reminders, not a hidden planning method. They help check whether updates are needed in:

- frame
- shaping.md
- requirements table
- shape parts / mechanisms
- CURRENT baseline or selected Detail X
- fit checks
- unknowns / spikes
- breadboard tables
- statechart tables and Mermaid projection, when present
- interface contracts
- executable breadboard examples
- wiring table
- Mermaid diagram
- slices.md
- slice definitions and sequencing
- context packet
- agent run log
