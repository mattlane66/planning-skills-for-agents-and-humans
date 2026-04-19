# Planning Skills for Agents and Humans

A clean-room set of planning skills for turning fuzzy requests, messy transcripts, and partial designs into artifacts that humans and agents can actually build from.

The emphasis is on legibility:
- frame the problem before racing to implementation
- compare alternatives before locking in a solution
- map places, affordances, state, and wiring before losing the plot
- keep high-level and low-level planning artifacts aligned as the work evolves

## Planning Skills vs. Spec Kit

This repo is not a replacement for Spec Kit. It is a complementary planning layer. Use these skills earlier in the process to frame the problem, separate requirements from mechanisms, compare shapes, breadboard the system, and slice the work into demoable scopes. Then use a broader spec-driven workflow like Spec Kit when you want project-level specs, plans, tasks, and implementation orchestration.

## Skills

### `/framing-doc`
Turn source material such as transcripts, notes, stakeholder messages, or call recordings into a frame that captures the problem, desired outcome, and boundaries.

### `/kickoff-doc`
Turn a kickoff conversation into a builder-facing reference doc organized around the territory being built rather than the order people happened to speak.

### `/shaping`
Collaboratively define requirements, sketch alternative approaches, compare their fit, and detail the selected direction.

### `/breadboarding`
Map a system into places, affordances, stores, and wiring so behavior is concrete before implementation gets fragmented.

### `/breadboard-reflection`
Compare a breadboard to the implementation, repair drift, and look for design smells such as hidden state, weak boundaries, or missing steps.

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
