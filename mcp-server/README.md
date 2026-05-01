# Planning Skills MCP Server

This is an optional MCP adapter for Planning Skills for Agents and Humans.

The server exposes the repository's `SKILL.md` files and a few starter artifact templates as MCP tools. It does not replace the skills; it gives MCP-capable clients a clean way to retrieve and use them.

## Tools

- `list_planning_skills` — list available planning skills and short descriptions.
- `get_planning_skill` — return the full `SKILL.md` instructions for one skill.
- `recommend_planning_workflow` — recommend a sequence of skills based on a situation description.
- `get_artifact_template` — return a starter Markdown template for a frame, shaping doc, breadboard, kickoff doc, or context packet.

## Install

From this directory:

```bash
npm install
npm run build
npm start
```

## Example MCP client config

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

Use an absolute path in real client configs unless your client explicitly runs from the repository root.

## Boundary

This package is a generic MCP server. It may be used by Gemini-style, Claude-style, Cursor-style, or other MCP-capable environments, but each client has its own configuration format and support surface.
