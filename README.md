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
- `/kickoff-doc` for preparing the build team
- `/feed-planning-context` for giving AI agents bounded context
- `/breadboard-reflection` for repairing drift between plan and implementation

Get a quick lightweight feel for these design skills with this Custom GPT [here](https://chatgpt.com/g/g-699222e353288191afb01ea178db6da6-shape-to-slice-assistant).

<img width="1453" height="713" alt="Screenshot 2026-04-24 at 10 05 13 PM" src="https://github.com/user-attachments/assets/8b3848cc-3968-4792-8d77-5c38b81ce3b1" />

The emphasis is on pre-development legibility:
- frame the problem before racing to implementation
- compare alternatives before locking in a solution
- map places, affordances, state, and wiring before losing the plot while maintaining latitude
- keep high-level and low-level planning artifacts aligned as the work evolves
- feed planning artifacts to agents at the right fidelity so they preserve shaped intent instead of drowning in context

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
3. Planning Skills: shaping
   Output: options, fit checks, selected approach, non-goals
   ↓
4. Planning Skills: breadboarding
   Output: places, affordances, stores, state, wiring
   ↓
5. Planning Skills: slices
   Output: demoable vertical slices, risk/dependency order
   ↓
6. Planning Skills: feed-planning-context
   Output: compact implementation packet
   ↓
7. Spec Kit
   Output: spec.md, plan.md, data-model.md, contracts, tasks.md
   ↓
8. HumanLayer / CodeLayer / Claude Code / Codex
   Output: implementation, tests, PRs, review loops
   ↓
9. Breadboard reflection
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

## Cross-agent setup

Use [`AGENTS.md`](./AGENTS.md) as the tool-neutral instruction surface for agents that understand repo-level instruction files. It captures the default mode, workflow, authority order, context-feeding rules, stable ID handling, drift protocol, and completion standard.

Claude Code users can install the skills natively. Other tools such as Cursor, Codex, and similar agent environments can use the same `SKILL.md` files as repo-local rules, prompt files, or reusable docs. The method is tool-agnostic even when some packaging details are tool-specific.

## Skills

### `/framing-doc`
Turn source material such as interview transcript syntheses, strategy notes, stakeholder messages, etc. into a frame that captures the living world context and boundaries, current approach and result, and desired outcome. (NOTE: I use requirements and criteria interchangeably, which I define as unit items that give us the fitness for solving the problem, i.e., standards or rules used to judge the quality of a solution, e.g., various '-ilities', customer forces, costs (time, dev effort, $), risks, compatibility and complexity, purpose-built for problem (reflective), etc.). I also determine if a criterion is a Must Have or not.)

### `/shaping`
Collaboratively define requirements/criteria, list alternative approaches, compare their fit, and detail the selected direction.

### `/breadboarding`
Map a system into places/screens/states, affordances, stores, and the wiring so behavior is concrete and vertically sliced and sequenced (based on unknowns/most risky parts and dependencies first) before implementation gets fragmented.

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
3. Shape the problem and compare options.
4. Choose a direction.
5. Breadboard the chosen shape.
6. Feed the selected planning artifacts into the agent as a compact context packet.
7. Reflect against implementation later when code exists.

What changes across tools is just **how you invoke the instructions**, not the method itself.

### Plain markdown workflow

The simplest portable setup is to keep the skill files in your repo and point your tool at them explicitly.

Example structure:

```text
docs/planning-skills/
  framing-doc.md
  shaping.md
  breadboarding.md
  kickoff-doc.md
  breadboard-reflection.md
  feed-planning-context.md

planning/
  frame.md
  shaping.md
  breadboard.md
  slices.md
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

### Codex

In Codex-style workflows, these skills work best as reusable prompt files or planning docs checked into the repo.

Example prompt:

```text
Read docs/planning-skills/framing-doc.md first.
Turn these notes into a frame with Source, Problem, Outcome, and Boundaries.
Write the result to planning/frame.md.
```

### Summary

- **Claude Code**: native skill packaging
- **Other tools**: prompt-template or repo-doc packaging
- **All agents**: use `AGENTS.md` as the neutral repo-level instruction surface when supported

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
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/breadboard-reflection ~/.claude/skills/breadboard-reflection
ln -s ~/.local/share/planning-skills-for-agents-and-humans/skills/feed-planning-context ~/.claude/skills/feed-planning-context
```

Each skill should be a direct child of `~/.claude/skills/`.

## Optional Claude Code hook

This repo includes a small hook that reminds the agent to update related planning artifacts when a planning document changes.

```bash
mkdir -p ~/.claude/hooks
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/planning-ripple.sh ~/.claude/hooks/planning-ripple.sh
```

Then add the hook in your Claude settings:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/planning-ripple.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The hook checks markdown files whose frontmatter includes either `planning: true` or `shaping: true`.

When a planning artifact changes, check whether updates are needed in:

- frame
- shaping.md
- requirements table
- shape parts / mechanisms
- CURRENT baseline or selected Detail X
- fit checks
- unknowns / spikes
- breadboard tables
- wiring table
- Mermaid diagram
- slices.md
- slice definitions and sequencing
- slice plan files
