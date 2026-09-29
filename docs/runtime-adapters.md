# Runtime adapters

The canonical `SKILL.md` files are the portable method layer. Runtime-specific invocation, permissions, discovery controls, hooks, and packaging belong in adapters.

| Layer | Owns |
|---|---|
| Canonical Agent Skill | `name`, `description`, `license`, optional compatibility/metadata, method, references, examples |
| Shared orchestration contract | collaborative/gated profiles, hard promotion gates, machine-readable prerequisites and forbidden moves |
| Claude Code adapter | command aliases, `disable-model-invocation`, `user-invocable`, argument hints, pre-approved tools, plugin-local paths |
| Codex plugin adapter | plugin discovery, skill inventory, display metadata, natural-language profile recipes, optional app dependencies |
| Gemini CLI adapter | native skill installation, `GEMINI.md`, TOML command wrappers, Gemini hooks or extension packaging |
| Claude / Claude Design upload | self-contained ZIPs, visual examples, natural-language profile invocation, repository fallback |
| MCP adapter | callable tools and resources; it exposes canonical skills/orchestration but does not replace their instructions |

## Cross-runtime profile contract

Every runtime should represent the same two shaping profiles:

- **collaborative** — default for interactive human-guided shaping; R, S, fit, spikes, sketches, and candidate breadboards can iterate in the order that best resolves uncertainty while material is Working
- **gated/orchestrated** — explicit stricter profile for automation or policy-controlled work; enforce `.agent-orchestration.yaml` prerequisites

Runtime adapters must not turn focused commands into a mandatory pipeline. A `/criteria`, `/sketch-shapes`, `/fit-check`, `/spike`, or `/breadboard` wrapper constrains the current move. It does not redefine the canonical exploration order.

The hard human promotion gates are identical across runtimes and profiles: accepted judging inputs before selection, explicit human selection, explicit candidate-to-selected reconciliation, accepted selected-design behavior before slicing, selected scope before build, and explicit human acceptance of the run-level execution appetite before implementation starts.

## Rules

- Do not put runtime-only fields in canonical skill frontmatter.
- Do not assume a skill grants access to an external system. Codex and ChatGPT plugins need an enabled app for that capability.
- Keep command wrappers thin and manual-only when they represent a human decision gate.
- Make collaborative versus gated behavior explicit rather than relying on different hidden defaults in different runtimes.
- Keep canonical descriptions model-discoverable so compatible runtimes can route to the right method.
- Generate runtime copies from canonical sources and test that they do not drift.
- When a canonical method change affects entry points, prerequisites, or stopping points, patch every adapter and its documentation in the same change.


## Compile execution appetite into runtime controls

The durable planning method names the boundary; each runtime adapter enforces it with whatever controls that runtime currently provides. Do not make a vendor control part of the canonical method.

| Planning intent | Adapter / harness behavior | Claude example today |
|---|---|---|
| Human accepts the run appetite | Block implementation until the acceptance is recorded; the model may propose but cannot self-approve or enlarge the bet. | This is a planning/harness gate, not a Claude API parameter. Preserve the accepted `Worth / Needed by / Protect / Cut first / Stop when` packet before invoking the model. |
| Pace gracefully as machine budget narrows | Make the remaining advisory budget visible to the model so it can protect MUST, cut NICE, checkpoint state, and land cleanly. | Claude Messages API `output_config.task_budget` on supported models is an advisory full-agentic-loop token countdown. It is not a hard stop and is not currently supported on Claude Code or Cowork surfaces. |
| Bound a self-hosted agent loop | Enforce a hard turn and/or spend backstop outside the model. | Claude Agent SDK `max_turns` and `max_budget_usd` terminate the run when exceeded; a request may finish after crossing the spend threshold. |
| Bound a hosted agent session | Enforce a session-level spend ceiling at the hosted platform boundary. | Claude Managed Agents `budget.max_list_cost` stops new model requests after the running list-cost ceiling is reached; the request that crosses the threshold finishes first. |
| Preserve continuity without replaying everything | Persist bounded decisions, verified invariants, blockers, next objective, and no-go boundaries. | Use a durable handoff artifact or the runtime's state mechanism; do not treat full transcript replay as a planning requirement. |
| Learn from the run | Record human cost, runtime evidence, cuts, and shaping signals independently of the vendor meter. | Write the canonical agent run log; token/spend/turn fields remain optional runtime evidence. |

Current Claude references:

- Task budgets: https://platform.claude.com/docs/en/build-with-claude/task-budgets
- Agent SDK bounded-loop example: https://platform.claude.com/cookbook/claude-agent-sdk-scheduled-repository-reviewer-scheduled-repository-reviewer
- Managed Agents session budgets: https://platform.claude.com/docs/en/managed-agents/sessions

These examples are intentionally non-canonical. Verify the active runtime's current controls before relying on a specific parameter, model, price, or limit.
