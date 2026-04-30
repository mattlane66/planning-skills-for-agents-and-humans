# Gemini and MCP usage

These planning skills are Markdown-first. Gemini-compatible usage should keep the skill folders as the source of truth and treat any extension or MCP layer as an adapter.

## Usage modes

### 1. Local skill folders

Where a Gemini or agent environment supports `SKILL.md`-style skill discovery, copy or symlink the existing skill folders into that environment's skill directory.

Example workspace layout:

```text
.gemini/skills/
  framing-doc/
    SKILL.md
  shaping/
    SKILL.md
  breadboarding/
    SKILL.md
  breadboard-reflection/
    SKILL.md
  kickoff-doc/
    SKILL.md
  feed-planning-context/
    SKILL.md
```

The exact install path and activation behavior are client-specific. Verify the current Gemini CLI or workspace documentation for the environment you are using.

### 2. MCP adapter

For environments that support Model Context Protocol tools, use the optional MCP server in `mcp-server/`.

The MCP server exposes the repo's planning skills as callable tools:

- `list_planning_skills` — list available planning skills and descriptions
- `get_planning_skill` — return the selected `SKILL.md`
- `recommend_planning_workflow` — suggest a planning sequence for a given situation
- `get_artifact_template` — return a starter artifact template

This adapter does not replace the skills. It only gives an MCP-capable model a tool interface for retrieving and applying them.

## Gemini extension manifest

`gemini-extension.example.json` is intentionally an example, not a claim of official marketplace compatibility. Gemini and Google AI Studio extension support can change. Use it as a starting point for clients that expect a local MCP server configuration, and check the current Gemini documentation before publishing or distributing it.
