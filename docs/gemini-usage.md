# Gemini CLI usage

Gemini CLI should use `GEMINI.md` as its project context file.

This repo includes a root `GEMINI.md` that imports `AGENTS.md`, so Gemini gets the same tool-neutral planning instructions as Claude Code, Codex, and other agents.

## Project commands

Gemini CLI discovers project-local custom commands from:

```text
.gemini/commands/
```

This repo includes Gemini-native command wrappers for the shaping gates:

| Command | Purpose |
|---|---|
| `/criteria` | Create or update only the requirements / criteria table before sketching shapes. |
| `/sketch-shapes` | Sketch alternative shapes against accepted criteria without selecting one. |
| `/fit-check` | Run fit checks and reverse fit checks across existing shapes without choosing for the human. |
| `/select-shape` | Record or prepare a human shape-selection decision after alternatives and fit checks are visible. |

These commands use Gemini's TOML command format and inject the relevant repo instructions and source files.

## Usage

From a Gemini CLI session in the repository, run:

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

## Reloading commands

After adding or changing command files, reload Gemini commands:

```text
/commands reload
```

To inspect available commands:

```text
/commands list
```

## Design principle

Gemini commands should remain thin wrappers around the canonical repo method.

Keep the workflow details in:

```text
AGENTS.md
shaping/SKILL.md
docs/human-decision-gates.md
```

Update Gemini command files only when the invocation behavior, stopping point, or user-facing command name changes.
