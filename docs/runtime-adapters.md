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

The hard human promotion gates are identical across runtimes and profiles: accepted judging inputs before selection, explicit human selection, explicit candidate-to-selected reconciliation, accepted selected-design behavior before slicing, and selected scope before build.

## Rules

- Do not put runtime-only fields in canonical skill frontmatter.
- Do not assume a skill grants access to an external system. Codex and ChatGPT plugins need an enabled app for that capability.
- Keep command wrappers thin and manual-only when they represent a human decision gate.
- Make collaborative versus gated behavior explicit rather than relying on different hidden defaults in different runtimes.
- Keep canonical descriptions model-discoverable so compatible runtimes can route to the right method.
- Generate runtime copies from canonical sources and test that they do not drift.
- When a canonical method change affects entry points, prerequisites, or stopping points, patch every adapter and its documentation in the same change.
