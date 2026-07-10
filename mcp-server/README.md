# Planning Skills MCP Server

This optional MCP adapter exposes the repository's canonical planning skills, artifact templates, and orchestration manifest to MCP-compatible clients.

It reads root `SKILL.md` files and `templates/` at runtime. The server does not maintain separate copies of either source.

## Tools

- `list_planning_skills` — list every available planning skill and its purpose.
- `get_planning_skill` — return the canonical instructions for one skill.
- `recommend_planning_workflow` — recommend the next skill or sequence while respecting prerequisites and human decision gates.
- `get_artifact_template` — return a canonical starter template from `templates/`.
- `get_orchestration_manifest` — return `.agent-orchestration.yaml`.

The recommender does not assume every project needs every step. In particular, Dumplink is recommended only when task grouping, risk, dependency, or scope-cut signals are present. A generic request to build something is routed through the core planning workflow unless the situation says a selected slice or context packet already exists.

## Install and verify

From this directory:

```bash
npm ci
npm run check
npm start
```

Use `npm run dev` while editing the server.

## Example MCP client configuration

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

Use an absolute path unless the client explicitly runs from the repository root.

## Boundary

This is a generic stdio MCP server, not a hosted service or full agent runtime. Individual clients have their own configuration and capability-discovery conventions.
