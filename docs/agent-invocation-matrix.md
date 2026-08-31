# Agent invocation matrix

The planning method is shared across tools. Invocation surfaces differ.

The default interactive profile is **collaborative shaping**: start from R, S, evidence, or a focused uncertainty and move among R/S/fit/spikes/candidate breadboards as useful. Use the **gated/orchestrated profile** when strict prerequisites are explicitly required.

## Support matrix

| Environment | Recommended invocation | Project commands | Notes |
| --- | --- | --- | --- |
| Claude Code | Plugin skills plus `.claude/commands/` | Yes | `/shape` is the broad collaborative front door; `/lead-user` starts or resumes the next valid research phase. Focused wrappers constrain the current move, not the whole exploration order. |
| Codex | Codex plugin plus natural-language prompts | No Claude-style slash commands | Use collaborative or gated prompt recipes; the active product repository's own `AGENTS.md` remains authoritative. |
| Gemini CLI | Skill folders plus adapted `.gemini/commands/` | Yes, using Gemini TOML commands | Supports `/shape`, `/spike`, and `/breadboard` in addition to focused shaping/gate commands. Preserve product instructions and adapt repo-local includes when installed paths differ. |
| Claude / Claude Design | Uploaded canonical skills plus natural-language mode requests | No repo-local command wrappers | Start R-first, S-first, evidence-first, or uncertainty-first; use Claude Code to preserve repo-authoritative artifacts when needed. |
| MCP-compatible clients | Tools exposed by `mcp-server/` | Client-dependent | The server reads canonical root skills and artifact templates at runtime; profile behavior comes from the canonical instructions/orchestration contract. |
| Cursor and other agents | `AGENTS.md`, root `SKILL.md` files, and templates | Tool-dependent | Point the agent explicitly at the relevant canonical skill and profile. |
| Plain Markdown | Read the relevant root `SKILL.md` | No | Portable fallback with no plugin dependency. |

## Workflow mapping

| Planning move | Canonical skill or artifact | Claude | Gemini | Codex and plain prompt |
| --- | --- | --- | --- | --- |
| Choose the smallest next move | `planning-router/SKILL.md` | `/plan` | `/plan` | “Use the planning-router skill; respect my current entry point…” |
| Start or resume future-facing opportunity research | `lead-user-research/SKILL.md` | `/lead-user` | `/lead-user` | “Use the lead-user-research skill; derive the next valid phase from [workspace]…” |
| Research brief — Phase A | `lead-user-research` | `/lead-user-frame` | `/lead-user-frame` | “Use lead-user-research Phase A…” |
| Trend-first discovery — Phase B | `lead-user-research` | `/lead-user-discover` | `/lead-user-discover` | “Use lead-user-research Phase B…” |
| Bounded evidence batch — Phase C | `lead-user-research` | `/lead-user-evidence` | `/lead-user-evidence` | “Use lead-user-research Phase C…” |
| Sufficiency and Evidence Freeze — Phase D | `lead-user-research` | `/lead-user-freeze` | `/lead-user-freeze` | “Use lead-user-research Phase D…” |
| Interpret frozen evidence — Phase E | `lead-user-research` | `/lead-user-interpret` | `/lead-user-interpret` | “Use lead-user-research Phase E…” |
| Evidence-gated concept shaping — Phase F | `lead-user-research` | `/lead-user-shape` | `/lead-user-shape` | “Use lead-user-research Phase F only for a passing need…” |
| Decision outcome and actions — Phase G | `lead-user-research` | `/lead-user-decide` | `/lead-user-decide` | “Use lead-user-research Phase G…” |
| Delivery and proposed frame handoff — Phase H | `lead-user-research` | `/lead-user-deliver` | `/lead-user-deliver` | “Use lead-user-research Phase H…” |
| Coordinate multi-session planning | `wayfinding/SKILL.md` | `/wayfind` | `/wayfind` | “Use Wayfinding to chart this bounded planning destination…” |
| Frame when genuinely needed | `framing-doc/SKILL.md` | `/frame` | Prompt skill directly | “Use the framing-doc skill…” |
| Collaborative shaping from R, S, evidence, or uncertainty | `shaping/SKILL.md` | `/shape` | `/shape` | “Use the shaping skill in collaborative mode…” |
| Work on requirements now | `shaping/SKILL.md` | `/criteria` | `/criteria` | “For this move, work on R; it may be extracted from existing S…” |
| Work on Appetite now | `shaping/SKILL.md` + `templates/appetite-card.md` | `/appetite` | `/appetite` | “Set, revise, or accept Appetite and cut line…” |
| Work on shapes now / S-first | `shaping/SKILL.md` | `/sketch-shapes` | `/sketch-shapes` | “For this move, capture or revise S; this may be the entry point…” |
| Run Working or decision-ready fit | `shaping/SKILL.md` | `/fit-check` | `/fit-check` | “Run fit/reverse-fit; label provisional evidence Working…” |
| Resolve one focused unknown | `shaping/SKILL.md` + `templates/spike.md` | `/spike` | `/spike` | “Run a focused spike and return R/S/fit/Appetite implications…” |
| Candidate-shape breadboard | `breadboarding/SKILL.md` | `/breadboard` | `/breadboard` | “Use candidate-shape mode; label Working/Accepted/Unset judging inputs…” |
| Select shape — hard gate | `shaping/SKILL.md` | `/select-shape` | `/select-shape` | “Record my selected shape after verifying accepted R/Appetite and decision-ready fit…” |
| Reconcile a visual | `sketch-reconciliation/SKILL.md` | `/reconcile-sketch` | `/reconcile-sketch` | “Reconcile this attached visual with accepted planning…” |
| Current-state or selected-design breadboard | `breadboarding/SKILL.md` | `/breadboard` | `/breadboard` | “Use breadboarding in current-state / selected-design mode…” |
| Model complex state | `statechart/SKILL.md` | `/statechart` | `/statechart` | “Use the statechart skill…” |
| Define boundary contracts | `interface-contracts/SKILL.md` | Prompt skill directly | Prompt skill directly | “Use interface-contracts…” |
| Create build handoff | `executable-breadboards/SKILL.md` | Prompt skill directly | Prompt skill directly | “Use executable-breadboards…” |
| Group and sequence work | `dumplink/SKILL.md` | `/dumplink` | `/dumplink` | “Use the dumplink skill…” |
| Package build context | `feed-planning-context/SKILL.md` | `/feed-context` | Prompt skill directly | “Use feed-planning-context…” |
| Check drift | `templates/drift-check.md` | `/check-drift` | `/check-drift` | “Run a strict drift check…” |
| Reflect after implementation | `breadboard-reflection/SKILL.md` | `/reflect-breadboard` | Prompt skill directly | “Use breadboard-reflection…” |
| Create kickoff reference | `kickoff-doc/SKILL.md` | `/kickoff` | Prompt skill directly | “Use kickoff-doc…” |

## Profile mapping

| Profile | Claude / Gemini | Codex / other agents |
| --- | --- | --- |
| Collaborative | Invoke `/shape` or canonical `shaping` and state collaborative mode; focused commands may be used in any useful order. | “Use collaborative shaping. Start from what is already concrete and keep Working material separate from Accepted intent.” |
| Gated / orchestrated | Invoke `/shape` and explicitly request the gated profile; wrappers enforce `.agent-orchestration.yaml` prerequisites. | “Use the gated/orchestrated profile and enforce `.agent-orchestration.yaml` prerequisites.” |

Hard promotion gates are identical across profiles even when exploration order differs.

## Maintenance rule

Root skill folders are canonical. Tool-specific wrappers stay thin. The packaged `skills/` directory is generated with:

```bash
bash scripts/sync-packaged-skills.sh
```

Do not hand-edit packaged skill copies or duplicate the method inside command wrappers.
