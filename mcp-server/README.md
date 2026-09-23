# Planning Skills MCP Server

This adapter exposes the repository's canonical planning skills, artifact templates, contracts, and orchestration rules to MCP-compatible clients.

The same tool definitions are available through two transports:

- **stdio** for local clients such as Codex, Claude Code, Gemini CLI, and other desktop/CLI MCP hosts
- **Streamable HTTP** for hosted MCP clients and public OpenAI Plugins

The server reads the repository's canonical `SKILL.md` files, templates, contracts, skill metadata, and `.agent-orchestration.yaml` at runtime. It does not maintain separate copies of planning truth.

## Tools

- `list_planning_skills` — list every available planning skill and its intended use.
- `get_planning_skill` — return the canonical instructions for one skill.
- `get_skill_resource` — return a referenced text support file from inside one skill directory, with traversal and size checks.
- `recommend_planning_workflow` — recommend the smallest next planning move while respecting prerequisites, explicit exclusions, input trust boundaries, and human decision gates.
- `get_artifact_template` — return a canonical starter template from `templates/`.
- `get_artifact_contracts` — return the machine-readable artifact contracts and promotion-gate mappings.
- `get_orchestration_manifest` — return `.agent-orchestration.yaml`.

Every tool is explicitly annotated as:

- `readOnlyHint: true`
- `destructiveHint: false`
- `openWorldHint: false`
- `idempotentHint: true`

Those annotations match the implementation: the tools only read or compute from the deployed Planning Skills bundle, do not mutate user or external state, and do not access the public internet.

## Install and verify

From this directory:

```bash
npm ci
npm run check
```

The test suite verifies both stdio and Streamable HTTP behavior.

## Local stdio server

Build and start:

```bash
npm run build
npm start
```

Example client configuration:

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

## Local Streamable HTTP server

Build and start:

```bash
npm run build
npm run start:http
```

Defaults:

- MCP endpoint: `http://localhost:3000/mcp`
- health endpoint: `http://localhost:3000/healthz`
- host: `0.0.0.0`
- port: `3000`

Override with environment variables:

```bash
HOST=127.0.0.1 PORT=8787 npm run start:http
```

Inspect locally with MCP Inspector using the **Streamable HTTP** transport and the `/mcp` URL.

## Deploy for an OpenAI public Plugin

OpenAI public MCP plugins require a stable public **HTTPS** Streamable HTTP endpoint. This repository includes `mcp-server/Dockerfile`, which intentionally copies the full repository because the MCP runtime reads canonical skills, templates, contracts, and orchestration files outside `mcp-server/`.

Build from the repository root:

```bash
docker build -f mcp-server/Dockerfile -t planning-skills-mcp .
docker run --rm -p 3000:3000 planning-skills-mcp
```

Deploy that container behind HTTPS on the host of your choice. The production URL should end in `/mcp`, for example:

```text
https://planning.example.com/mcp
```

Do **not** add a root `mcp.json` with a placeholder URL. Once the real production endpoint exists, either:

1. enter that endpoint directly in **Platform → Plugins → Create plugin → With MCP**, or
2. add a portable root `mcp.json` that points to the real URL:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "planning-skills": {
      "type": "streamable-http",
      "url": "https://planning.example.com/mcp"
    }
  }
}
```

For the public Plugin, upload the repository's existing `skills/` bundle alongside the scanned MCP tools. The server intentionally does not implement MCP skill-import discovery; the repository contains more skills than the current import path is designed to snapshot reliably, while the packaged skills already remain the canonical workflow layer.

## Skill/tool boundary

The MCP server is deterministic infrastructure underneath the skills:

- use `recommend_planning_workflow` to validate routing and exclusions
- use `get_artifact_template`, `get_artifact_contracts`, and `get_orchestration_manifest` to retrieve canonical planning structure and gates
- keep product judgment, tradeoffs, candidate generation, and human promotion decisions in the skills and the human interaction

The MCP server must never choose a solution, accept a requirement, promote a candidate breadboard, select scope, or claim realized effect.

## Trust boundary

Pass only trusted user instructions and trusted project state in `situation`. Put transcripts, issue bodies, web content, pasted notes, and other evidence in the optional `source_material` field; the deterministic router deliberately ignores that field so embedded instructions cannot select a workflow. Use `excluded_skills` for explicit user or host exclusions.

## Production notes

- Terminate TLS at the hosting platform or reverse proxy; the Node process itself serves HTTP.
- Keep the full runtime bundle available to the container because tools load canonical repository files at runtime.
- The server does not require OAuth today because every exposed tool is read-only and serves public/open-source planning material.
- Keep infrastructure logs to request/transport failures and do not log user tool arguments or returned planning content.
- Use `GET /healthz` for platform health checks.
