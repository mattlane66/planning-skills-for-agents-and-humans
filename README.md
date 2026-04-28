# Planning Skills for Agents and Humans

A set of planning skills for turning fuzzy requests, messy transcripts, and partial designs into artifacts that humans and agents can actually build from. These skills are perfect for when considering meaningfully large and strategically important feature development (discrete bets that have time budgets of 2, 3, 4, 5, or 6 weeks for small launch teams). These skills are at their most potent (especially the spiking aspect in shaping) when grounded in the context of your codebase, providing the essential 'ground truth' needed for both humans and agents to execute with high confidence.
Now, maybe AI could one-shot a simple app instead of using these skills. But, going through this process means you and your team will have a view of how the solution works (and will render better results as you get more concrete in your prompts). You can understand the system and can ask questions about all of the documents that explain how and why it's put together the way it is so when you want to make improvements and changes later you can. Ideally, you use these skills to help manage a collaborative [shaping session](https://www.figma.com/community/file/1490786031847199566/shaping-session-playing-field-copy-me-template).

AI coding tools have become powerful new prototyping instruments, but they work best after good upstream/uphill shaping.

Get a quick lightweight feel for these design skills [here](https://chatgpt.com/g/g-699222e353288191afb01ea178db6da6-shape-to-slice-assistant).

<img width="1453" height="713" alt="Screenshot 2026-04-24 at 10 05 13 PM" src="https://github.com/user-attachments/assets/8b3848cc-3968-4792-8d77-5c38b81ce3b1" />

The emphasis is on pre-development legibility:
- frame the problem before racing to implementation
- compare alternatives before locking in a solution
- map places, affordances, state, and wiring before losing the plot while maintaining latitude
- keep high-level and low-level planning artifacts aligned as the work evolves

## Planning Skills vs. Spec Kit

This repo is not a replacement for [Spec Kit](https://github.com/github/spec-kit). It is a complementary planning layer. Use these skills earlier in the process to frame the problem, separate requirements from mechanisms, compare shapes, breadboard the system, and slice the work into demoable scopes. Then use a broader spec-driven workflow like Spec Kit when you want project-level specs, plans, tasks, and implementation orchestration.
Comparatively (including [HumanLayer](https://www.humanlayer.dev)):
- Planning Skills = figure out what to build to get people from where they are to where they ought to be and how to structure and derisk it
- Spec Kit = turn planning skills' vertical slices into an agent-specific implementation build plan while specifying exact file paths, dependencies, order, and test structure.
- HumanLayer = help agents carry out the build work reliably in real complex codebases 

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

## Examples

If you want to see the skills used step by step, start in [`examples/`](./examples).

The included `simple-grocery-list` example walks through:
- raw source notes
- a frame
- shaping with competing directions
- an optional kickoff doc
- a breadboard
- a post-implementation breadboard reflection

## Using these skills outside Claude Code

These skills are packaged for Claude Code, but the method is portable.

The `SKILL.md` files are plain Markdown instructions. In tools like Cursor, Codex, or other agent environments, use them as reusable prompt templates or repo-local instruction docs.

The core workflow stays the same:

1. Start with raw notes or transcripts.
2. Create a frame.
3. Shape the problem and compare options.
4. Choose a direction.
5. Breadboard the chosen shape.
6. Reflect against implementation later when code exists.

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

planning/
  frame.md
  shaping.md
  breadboard.md
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

So the workflow is tool-agnostic in substance, but Claude-specific in packaging.

## Install

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans

ln -s ~/.local/share/planning-skills-for-agents-and-humans/framing-doc ~/.claude/skills/framing-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/kickoff-doc ~/.claude/skills/kickoff-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/shaping ~/.claude/skills/shaping
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboarding ~/.claude/skills/breadboarding
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboard-reflection ~/.claude/skills/breadboard-reflection
```

Each skill should be a direct child of `~/.claude/skills/`.

## Hook

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
