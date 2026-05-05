# Claude slash commands

This repo includes project-level Claude slash commands that delegate to the canonical planning skills.

The commands live in:

```text
.claude/commands/
```

## Commands

| Command | Uses skill | Purpose |
|---|---|---|
| `/frame` | `framing-doc/SKILL.md` | Create a framing document from notes, messages, or transcripts. |
| `/shape` | `shaping/SKILL.md` | Separate requirements from mechanisms, compare directions, and fit-check alternatives. |
| `/breadboard` | `breadboarding/SKILL.md` | Map places, affordances, stores, wiring, and demoable slices. |
| `/kickoff` | `kickoff-doc/SKILL.md` | Turn kickoff notes or transcripts into a builder-facing reference document. |
| `/feed-context` | `feed-planning-context/SKILL.md` | Package planning artifacts into a compact context packet for implementation work. |
| `/reflect-breadboard` | `breadboard-reflection/SKILL.md` | Sync a breadboard to implementation reality and identify design smells or drift. |

## Usage

From a Claude Code session in the repository, run commands with arguments:

```text
/frame notes/product-discovery.md
```

```text
/shape "We need to improve activation for new workspace users"
```

```text
/breadboard planning/selected-shape.md
```

```text
/kickoff transcripts/kickoff-call.md
```

```text
/feed-context planning/frame.md planning/shaping.md planning/breadboard.md
```

```text
/reflect-breadboard planning/breadboard.md src/features/onboarding/
```

## Design principle

The slash commands are thin invocation wrappers. They should not become a second copy of the method.

Keep the canonical workflow details in the skill files:

```text
framing-doc/SKILL.md
shaping/SKILL.md
breadboarding/SKILL.md
kickoff-doc/SKILL.md
feed-planning-context/SKILL.md
breadboard-reflection/SKILL.md
```

When changing the method, update the skill first. Update the slash command only when the invocation behavior or user-facing command name changes.
