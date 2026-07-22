# Planning Skills MCP Server

This optional MCP adapter exposes the repository's canonical planning skills, artifact templates, and orchestration manifest to MCP-compatible clients.

It reads root `SKILL.md` files and `templates/` at runtime. The server does not maintain separate copies of either source.

## Tools

- `list_planning_skills` — list every available planning skill and its purpose.
- `get_planning_skill` — return the canonical instructions for one skill.
- `recommend_planning_workflow` — recommend the next skill or sequence while respecting prerequisites and human decision gates.
- `get_artifact_template` — return a canonical starter template from `templates/`.
- `get_orchestration_manifest` — return `.agent-orchestration.yaml`.

The skill list follows `skill-inventory.txt`, titles and descriptions come from the canonical `skill-metadata.json`, and the artifact tool covers every template named in `.agent-orchestration.yaml`. The recommender does not assume every project needs every step. Statechart is recommended only for explicit state-complexity signals. Dumplink is recommended for task grouping, risk, dependency, or scope-cut signals, but a committed sequence or handoff routes back to breadboarding when no slice is selected. A generic request to build something is routed through the core planning workflow unless the situation says a selected slice or context packet already exists.

Conversational shorthand from an active shaping session is routed directly instead of restarting the workflow:

- `show me R x A`, `A x R`, `rotate the fit check` -> `shaping`
- `spike A2`, `update A`, `add R` -> `shaping`
- `see this sketch`, attached screenshot/wireframe reconciliation -> `sketch-reconciliation`
- `let's slice it` -> `breadboarding`
- implementation planning for the first/next/active slice -> `executable-breadboards`, then `feed-planning-context`
- run/interact/verify execution requests -> `feed-planning-context` before the host agent executes

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
