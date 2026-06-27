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
| `/shape` | `shaping/SKILL.md` | Separate requirements from mechanisms, compare directions, fit-check alternatives, and select a bounded direction. |
| `/criteria` | `shaping/SKILL.md` | Create or update only the requirements / criteria table before sketching shapes. |
| `/sketch-shapes` | `shaping/SKILL.md` | Sketch alternative shapes against accepted criteria without selecting one. |
| `/fit-check` | `shaping/SKILL.md` | Run fit checks and reverse fit checks across existing shapes without choosing for the human. |
| `/select-shape` | `shaping/SKILL.md` | Record or prepare a human shape-selection decision after alternatives and fit checks are visible. |
| `/breadboard` | `breadboarding/SKILL.md` | Map places, affordances, stores, wiring, and demoable slices. |
| `/kickoff` | `kickoff-doc/SKILL.md` | Turn kickoff notes or transcripts into a builder-facing reference document. |
| `/feed-context` | `feed-planning-context/SKILL.md` | Package planning artifacts into a compact context packet for implementation work. |
| `/reflect-breadboard` | `breadboard-reflection/SKILL.md` | Sync a breadboard to implementation reality and identify design smells or drift. |

## Shaping gate commands

Use `/shape` when you want the broad shaping workflow in one pass.

Use the smaller shaping gate commands when you want to prevent the agent from one-shotting the shape:

1. `/criteria` — define the standards for judging fit.
2. `/sketch-shapes` — make multiple possible directions visible.
3. `/fit-check` — compare shapes against criteria and check whether each mechanism is justified.
4. `/select-shape` — record the human decision or stop with a decision-ready summary.
5. `/breadboard` — make the selected shape concrete only after selection.

These commands are intentionally thin wrappers around `shaping/SKILL.md`. They narrow the stopping point; they do not create a second copy of the method.

## Usage

From a Claude Code session in the repository, run commands with arguments:

```text
/frame notes/product-discovery.md
```

```text
/shape "We need to improve activation for new workspace users"
```

```text
/criteria planning/frame.md
```

```text
/sketch-shapes planning/shaping.md
```

```text
/fit-check planning/shaping.md
```

```text
/select-shape planning/shaping.md "Choose B"
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

When changing the method, update the skill first. Update the slash command only when the invocation behavior, stopping point, or user-facing command name changes.
