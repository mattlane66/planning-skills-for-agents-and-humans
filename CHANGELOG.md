# Changelog

## v0.1.0 - Initial public release

Initial reusable release of Planning Skills for Agents and Humans.

### Included

- Six planning skills:
  - `framing-doc`
  - `shaping`
  - `breadboarding`
  - `breadboard-reflection`
  - `kickoff-doc`
  - `feed-planning-context`
- Root-level `SKILL.md` folders for direct use as portable planning skills.
- Mirrored `skills/` directory for plugin-style consumers.
- Tool-neutral `AGENTS.md` instructions and `CLAUDE.md` adapter.
- Claude plugin manifest in `.claude-plugin/plugin.json`.
- Codex plugin manifest in `.codex-plugin/plugin.json`.
- Local Codex marketplace entry in `.agents/plugins/marketplace.json`.
- Optional Gemini and MCP integration scaffold.
- Optional TypeScript MCP server exposing planning skills and artifact templates.
- Example planning walkthrough for a simple grocery list.
- Canvas export guidance for Mermaid, FigJam, Excalidraw, TLDraw, and Miro-style workflows.

### Notes

This release is intended as the first stable reference point for reuse, installation, and comparison. Future releases should add automated validation for skill metadata, plugin manifests, and the optional MCP server build.
