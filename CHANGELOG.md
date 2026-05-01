# Changelog

All notable changes to this repository will be documented here.

This project uses semantic version-style tags for reusable skill/plugin releases.

## [v0.1.0] - 2026-05-01

Initial reusable release of Planning Skills for Agents and Humans.

### Included

- Six planning skills:
  - `framing-doc`
  - `shaping`
  - `breadboarding`
  - `kickoff-doc`
  - `feed-planning-context`
  - `breadboard-reflection`
- Root-level `SKILL.md` folders for direct skill use.
- Mirrored `skills/` directory for plugin-style clients that expect a centralized skills folder.
- Claude plugin metadata under `.claude-plugin/plugin.json`.
- Codex plugin metadata under `.codex-plugin/plugin.json`.
- Repo-local Codex marketplace metadata under `.agents/plugins/marketplace.json`.
- Gemini/MCP integration guidance under `integrations/gemini/`.
- Optional TypeScript MCP adapter under `mcp-server/`.
- Example artifacts under `examples/simple-grocery-list/`.
- Agent-facing repo instructions in `AGENTS.md` and `CLAUDE.md`.

### Notes

- This release is primarily a reusable planning-method, skills, and plugin-packaging release.
- The MCP adapter is optional and can be built from `mcp-server/` with `npm install` and `npm run build`.
- Future hardening should add CI validation for skill frontmatter, plugin manifests, MCP build, and root-to-`skills/` sync.
