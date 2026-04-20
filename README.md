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
