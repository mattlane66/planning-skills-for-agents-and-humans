# Gemini and MCP integration

This repo is Markdown-first. The planning skills remain the source of truth in the root skill folders and their `SKILL.md` files.

Gemini-style usage has two practical modes:

1. **Markdown skill usage** — copy or symlink the skill folders into a local agent environment that supports `SKILL.md`-style skill discovery.
2. **MCP adapter usage** — run the optional MCP server in `mcp-server/` so an MCP-compatible client can list, retrieve, and apply the planning skills as tools.

This directory is intentionally conservative. It does not claim that any specific Gemini surface accepts this exact manifest format. Treat `gemini-extension.example.json` as a client configuration example to adapt to the current Google/Gemini or MCP host documentation.

## Local skill install pattern

If your Gemini or agent environment supports local skill folders, install the root skill directories directly:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans

mkdir -p .gemini/skills
ln -s ~/.local/share/planning-skills-for-agents-and-humans/framing-doc .gemini/skills/framing-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/kickoff-doc .gemini/skills/kickoff-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/shaping .gemini/skills/shaping
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboarding .gemini/skills/breadboarding
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboard-reflection .gemini/skills/breadboard-reflection
ln -s ~/.local/share/planning-skills-for-agents-and-humans/feed-planning-context .gemini/skills/feed-planning-context
```

For a global install, use the global skills directory for your target client if it supports one.

## MCP adapter pattern

The optional server in `mcp-server/` exposes the planning skills as callable tools:

- `list_planning_skills`
- `get_planning_skill`
- `recommend_planning_workflow`
- `get_artifact_template`

The adapter does not replace the skills. It gives MCP-compatible clients a structured way to discover and retrieve them.

## Example client config

See [`gemini-extension.example.json`](./gemini-extension.example.json). Adapt the command and args to wherever you run the server.

A local Node command usually points at the built server entrypoint:

```json
{
  "mcpServers": {
    "planning-skills": {
      "command": "node",
      "args": ["/absolute/path/to/planning-skills-for-agents-and-humans/mcp-server/dist/index.js"]
    }
  }
}
```

## Recommended agent prompt

```text
Use the Planning Skills MCP server.
First call list_planning_skills.
Then choose the smallest relevant workflow.
Retrieve only the needed skill instructions.
Default to planning mode unless I explicitly ask you to implement a selected slice.
```
