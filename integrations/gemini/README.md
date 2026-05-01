# Gemini / MCP integration

This directory describes a conservative way to use the planning skills from Gemini-style or MCP-capable environments.

The `SKILL.md` files remain the source of truth. Gemini-specific files are adapters around those skills, not a replacement for the planning method.

## Usage modes

### 1. Markdown skill usage

Where a Gemini or agent environment supports local skill folders, copy or symlink each skill folder so the `SKILL.md` file is a direct child of the configured skills directory.

Example workspace layout:

```text
.gemini/
  skills/
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

Example prompt:

```text
Use the shaping skill from .gemini/skills/shaping/SKILL.md.
Help me compare directions, preserve requirements separately from mechanisms, and produce a shaping artifact.
```

### 2. MCP tool usage

For clients that support MCP servers, use the optional server in `mcp-server/`.

The MCP server exposes the planning skills as callable tools:

- `list_planning_skills`
- `get_planning_skill`
- `recommend_planning_workflow`
- `get_artifact_template`

This lets an agent retrieve the right planning instructions on demand instead of requiring the whole repo to be pasted into context.

## Example client config

See [`gemini-extension.example.json`](./gemini-extension.example.json) for a client-side example. Treat it as a starting point, not an official Google manifest. Different Gemini and MCP clients may use different configuration shapes.

## Important boundary

This integration does not claim official Gemini Extension marketplace compatibility. It is a practical adapter for environments that can either read local `SKILL.md` folders or call MCP tools.
