# Gemini CLI usage

When maintaining this repository, Gemini CLI should use `GEMINI.md` as its project context file.

This repo includes a root `GEMINI.md` that imports `AGENTS.md`, so Gemini gets the same tool-neutral planning instructions as Claude Code, Codex, and other agents.

For product work, copy or symlink the needed skill folders into the product repository, or use the MCP adapter. Preserve that product repository's own `GEMINI.md`, `AGENTS.md`, and other local instructions instead of replacing them with this repository's files. The TOML commands in this repo contain repo-local `@{...}` includes; treat them as adapter examples and update those includes if the skills or supporting docs live at different paths in the product repository.

## Project commands

Gemini CLI discovers project-local custom commands from:

```text
.gemini/commands/
```

This repo includes Gemini-native command wrappers for shaping gates, sketch reconciliation, optional statecharts, vertical task grouping, and drift checks:

| Command | Purpose |
|---|---|
| `/criteria` | Create or update only the requirements / criteria table before sketching shapes. |
| `/appetite` | Set the fixed time or scope budget and cut line before selecting a shape. |
| `/sketch-shapes` | Sketch alternative shapes against accepted criteria without selecting one. |
| `/fit-check` | Run fit checks and reverse fit checks across existing shapes without choosing for the human. |
| `/select-shape` | Record or prepare a human shape-selection decision after alternatives and fit checks are visible. |
| `/reconcile-sketch` | Map a dropped visual to planning IDs, surface proposed deltas, and apply only accepted changes. |
| `/statechart` | Derive a transition table and Mermaid projection for a selected stateful portion of an accepted breadboard. |
| `/dumplink` | Turn selected shaped work into vertical task groups, dependency order, risk states, and scope cuts. |
| `/check-drift` | Check implementation direction against selected planning artifacts and stop if drift is found. |

These commands use Gemini's TOML command format and inject the files named by their `@{...}` includes. In this repository those paths are already correct; in a product repository, verify or adapt them before use.

## Usage

From a Gemini CLI session in that active repository, run:

```text
/criteria planning/frame.md
```

```text
/appetite planning/shaping.md "Two weeks, one engineer; cut reporting before core capture"
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
/reconcile-sketch planning/shaping.md planning/breadboard.md /path/to/sketch.png
```

You can instead attach or paste the image in the same command prompt when Gemini CLI supports image input.

```text
/statechart planning/breadboard.md "Scope: V2 retry and cancellation"
```

```text
/dumplink planning/shaping.md planning/breadboard.md
```

```text
/check-drift planning/context-packet.md src/features/onboarding/
```

## Drift check output

`/check-drift` should return only one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
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
templates/appetite-card.md
sketch-reconciliation/SKILL.md
statechart/SKILL.md
docs/human-decision-gates.md
docs/loop-prompting.md
templates/drift-check.md
```

Update Gemini command files only when the invocation behavior, stopping point, or user-facing command name changes.
