# Planning Skills for Agents and Humans

A set of planning skills for turning fuzzy requests, messy transcripts, and partial designs into artifacts that humans and agents can actually build from. These skills are perfect for when considering meaningfully large and strategically important feature development (discrete bets that have time budgets of 2, 3, 4, 5, or 6 weeks for small launch teams).

The emphasis is on legibility:
- frame the problem before racing to implementation
- compare alternatives before locking in a solution
- map places, affordances, state, and wiring before losing the plot
- keep high-level and low-level planning artifacts aligned as the work evolves

## Planning Skills vs. Spec Kit

This repo is not a replacement for [Spec Kit](https://github.com/github/spec-kit). It is a complementary planning layer. Use these skills earlier in the process to frame the problem, separate requirements from mechanisms, compare shapes, breadboard the system, and slice the work into demoable scopes. Then use a broader spec-driven workflow like Spec Kit when you want project-level specs, plans, tasks, and implementation orchestration.
More directly (including [HumanLayer](https://www.humanlayer.dev)):
- Planning Skills = figure out what to build and how to structure it
- Spec Kit = turn that decision into a structured build plan
- HumanLayer = help agents carry out the work reliably in real code

## Skills

### `/framing-doc`
Turn source material such as interview transcript syntheses, strategy notes, stakeholder messages, etc. into a frame that captures the living world context and boundaries, current approach and result, and desired outcome.

### `/shaping`
Collaboratively define requirements/criteria, list alternative approaches, compare their fit, and detail the selected direction. (NOTE: I use requirements and criteria interchangeably, which I define as unit items that give us the fitness for solving the problem, i.e., standards or rules used to judge the quality of a solution, e.g., various '-ilities', customer forces, costs (time, dev effort, $), risks, compatibility and complexity, purpose-built for problem (reflective), etc.). I also determine if a criterion is a Must Have or not.)

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
