# Runtime adapters

The canonical `SKILL.md` files are the portable method layer. Runtime-specific invocation, permissions, discovery controls, hooks, and packaging belong in adapters.

| Layer | Owns |
|---|---|
| Canonical Agent Skill | `name`, `description`, `license`, optional compatibility/metadata, method, references, examples |
| Claude Code adapter | command aliases, `disable-model-invocation`, `user-invocable`, argument hints, pre-approved tools, plugin-local paths |
| Codex plugin adapter | plugin discovery, skill inventory, display metadata, optional app dependencies |
| Gemini CLI adapter | native skill installation, `GEMINI.md`, TOML command wrappers, Gemini hooks or extension packaging |
| Claude / Claude Design upload | self-contained ZIPs, visual examples, natural-language invocation, repository fallback |
| MCP adapter | callable tools and resources; it does not replace skill instructions |

## Rules

- Do not put Claude-only fields in canonical skill frontmatter.
- Do not assume a skill grants access to an external system. Codex and ChatGPT plugins need an enabled app for that capability.
- Keep command wrappers thin and manual-only when they represent a human decision gate.
- Keep canonical descriptions model-discoverable so compatible runtimes can route to the right method.
- Generate runtime copies from canonical sources and test that they do not drift.
