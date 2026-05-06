# Agent invocation matrix

Use this guide to understand how the same planning skills are invoked across Claude, Codex, Gemini-style clients, Cursor, and plain Markdown workflows.

The planning method is shared. The invocation surface differs by tool.

## Support matrix

| Environment | Best-supported invocation | Native slash commands? | Status | Notes |
|---|---|---:|---|---|
| Claude Code | Project slash commands + plugin/skills | Yes | Supported | Use `.claude/commands/*`, `.claude-plugin/plugin.json`, and `skills/*/SKILL.md`. |
| Codex | Plugin/skills + prompt recipes | No | Supported as plugin/skills | Use `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and the `skills/` directory. Do not claim Claude-style slash commands here. |
| Gemini-style clients | Local skill folders or MCP tools | No | Adapter-ready | Use `.gemini/skills/*/SKILL.md` where supported, or the MCP server in `mcp-server/`. This repo does not claim official Gemini Extension marketplace compatibility. |
| Cursor | Repo-local docs/rules + prompt recipes | No | Prompt-template ready | Point Cursor at the relevant `SKILL.md`, `AGENTS.md`, or template. |
| Plain Markdown / any agent | Read the relevant `SKILL.md` directly | No | Portable fallback | Use the skill files as reusable prompt documents. |

## Claude command equivalents

Claude has project slash commands for the main workflows:

| Claude command | Canonical skill |
|---|---|
| `/frame` | `framing-doc/SKILL.md` |
| `/shape` | `shaping/SKILL.md` |
| `/breadboard` | `breadboarding/SKILL.md` |
| `/kickoff` | `kickoff-doc/SKILL.md` |
| `/feed-context` | `feed-planning-context/SKILL.md` |
| `/reflect-breadboard` | `breadboard-reflection/SKILL.md` |

## Codex prompt recipes

Codex uses the plugin/skills package and natural-language prompts rather than Claude-style project slash commands.

```text
Use Planning Skills for Agents and Humans to frame this request before implementation. Use the framing-doc skill and keep source evidence separate from interpretation.
```

```text
Use the shaping skill to compare possible solution directions. Keep requirements separate from mechanisms, model CURRENT if there is an existing system, run a fit check, and stop before implementation.
```

```text
Use the breadboarding skill to map places, UI affordances, non-UI affordances, stores, wiring, and likely demoable slices for the selected shape.
```

```text
Use the feed-planning-context skill to package the active planning artifacts into a compact context packet for an implementation agent. Do not implement code.
```

```text
Use the breadboard-reflection skill to compare the implementation against the intended breadboard. Sync reality first, then identify drift and design smells.
```

## Gemini-style prompt recipes

Gemini-style clients can use local skill folders or MCP tools. Use explicit prompts that point to the relevant skill.

```text
Use .gemini/skills/framing-doc/SKILL.md to turn these notes into a frame with Source, Problem, Outcome, and Boundaries.
```

```text
Use .gemini/skills/shaping/SKILL.md to create requirements, compare alternatives, run a fit check, and choose a direction. Do not implement code.
```

```text
Use .gemini/skills/breadboarding/SKILL.md to map the selected direction into places, affordances, stores, wiring, and slice candidates.
```

```text
Use the planning-skills MCP server to recommend the next planning workflow for this situation, then retrieve the relevant skill instructions.
```

## Maintenance rule

Do not invent platform-specific slash-command claims for tools that do not support that convention.

Keep the source of truth in the skills:

```text
framing-doc/SKILL.md
shaping/SKILL.md
breadboarding/SKILL.md
kickoff-doc/SKILL.md
feed-planning-context/SKILL.md
breadboard-reflection/SKILL.md
```

Tool-specific wrappers should stay thin. They should invoke or point to the canonical skill, not duplicate the method.
