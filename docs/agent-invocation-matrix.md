# Agent invocation matrix

The planning method is shared across tools. Invocation surfaces differ.

## Support matrix

| Environment | Recommended invocation | Project commands | Notes |
| --- | --- | --- | --- |
| Claude Code | Plugin skills plus `.claude/commands/` | Yes | Command wrappers point to canonical root skills and shared orchestration docs. |
| Codex | Codex plugin plus natural-language prompts | No Claude-style slash commands | The manifest packages the generated `skills/` directory; the active product repository's own `AGENTS.md` remains authoritative. |
| Gemini CLI | Skill folders plus adapted `.gemini/commands/` | Yes, using Gemini TOML commands | Preserve product instructions and update repo-local `@{...}` includes when installed paths differ. |
| MCP-compatible clients | Tools exposed by `mcp-server/` | Client-dependent | The server reads canonical root skills and artifact templates at runtime. |
| Cursor and other agents | `AGENTS.md`, root `SKILL.md` files, and templates | Tool-dependent | Point the agent explicitly at the relevant canonical skill. |
| Plain Markdown | Read the relevant root `SKILL.md` | No | Portable fallback with no plugin dependency. |

## Workflow mapping

| Planning move | Canonical skill or artifact | Claude | Gemini | Codex and plain prompt |
| --- | --- | --- | --- | --- |
| Frame | `framing-doc/SKILL.md` | `/frame` | Prompt the skill directly | “Use the framing-doc skill…” |
| Define criteria | `shaping/SKILL.md` | `/criteria` | `/criteria` | “Run the criteria gate only…” |
| Set appetite | `shaping/SKILL.md` + `templates/appetite-card.md` | `/appetite` | `/appetite` | “Set the bounded appetite and cut line…” |
| Sketch alternatives | `shaping/SKILL.md` | `/sketch-shapes` | `/sketch-shapes` | “Sketch shapes without selecting…” |
| Fit-check | `shaping/SKILL.md` | `/fit-check` | `/fit-check` | “Run the fit-check gate only…” |
| Select shape | `shaping/SKILL.md` | `/select-shape` | `/select-shape` | “Record my selected shape…” |
| Full shaping pass | `shaping/SKILL.md` | `/shape` | Prompt the skill directly | “Use the shaping skill…” |
| Reconcile a visual | `sketch-reconciliation/SKILL.md` | `/reconcile-sketch` | `/reconcile-sketch` | “Reconcile this attached sketch with the active planning artifacts…” |
| Breadboard | `breadboarding/SKILL.md` | `/breadboard` | Prompt the skill directly | “Use the breadboarding skill…” |
| Model complex state | `statechart/SKILL.md` | `/statechart` | `/statechart` | “Use the statechart skill…” |
| Define boundary contracts | `interface-contracts/SKILL.md` | Prompt the skill directly | Prompt the skill directly | “Use interface-contracts…” |
| Create build handoff | `executable-breadboards/SKILL.md` | Prompt the skill directly | Prompt the skill directly | “Use executable-breadboards…” |
| Group and sequence work | `dumplink/SKILL.md` | `/dumplink` | `/dumplink` | “Use the dumplink skill…” |
| Package build context | `feed-planning-context/SKILL.md` | `/feed-context` | Prompt the skill directly | “Use feed-planning-context…” |
| Check drift | `templates/drift-check.md` | `/check-drift` | `/check-drift` | “Run a strict drift check…” |
| Reflect after implementation | `breadboard-reflection/SKILL.md` | `/reflect-breadboard` | Prompt the skill directly | “Use breadboard-reflection…” |
| Create kickoff reference | `kickoff-doc/SKILL.md` | `/kickoff` | Prompt the skill directly | “Use kickoff-doc…” |

## Maintenance rule

Root skill folders are canonical. Tool-specific wrappers stay thin. The packaged `skills/` directory is generated with:

```bash
bash scripts/sync-packaged-skills.sh
```

Do not hand-edit packaged skill copies or duplicate the method inside command wrappers.
