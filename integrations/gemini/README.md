# Gemini and MCP integration

This folder documents a conservative Gemini integration path for the planning skills in this repository.

The skills remain the source of truth. The MCP server is only an adapter that lets an MCP-aware client list, retrieve, and apply the existing `SKILL.md` files as tools.

## Usage modes

### 1. Markdown skill usage

If your Gemini or agent environment supports skill-style prompt folders, copy or symlink the existing skill folders directly:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans

mkdir -p ~/.gemini/skills
ln -s ~/.local/share/planning-skills-for-agents-and-humans/framing-doc ~/.gemini/skills/framing-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/shaping ~/.gemini/skills/shaping
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboarding ~/.gemini/skills/breadboarding
ln -s ~/.local/share/planning-skills-for-agents-and-humans/breadboard-reflection ~/.gemini/skills/breadboard-reflection
ln -s ~/.local/share/planning-skills-for-agents-and-humans/kickoff-doc ~/.gemini/skills/kickoff-doc
ln -s ~/.local/share/planning-skills-for-agents-and-humans/feed-planning-context ~/.gemini/skills/feed-planning-context
```

Workspace-local installation can follow the same pattern under a project-local `.gemini/skills/` directory when supported by the target environment.

### 2. MCP tool usage

For Gemini or other clients that support MCP tools, use the optional server in [`../../mcp-server`](../../mcp-server).

The server exposes these tools:

- `list_planning_skills` — list the available planning skills.
- `get_planning_skill` — return the source `SKILL.md` for a named skill.
- `recommend_planning_workflow` — suggest a planning sequence from a short situation description.
- `get_artifact_template` — return a starter Markdown template for common planning artifacts.

## Example client configuration

See [`gemini-extension.example.json`](./gemini-extension.example.json) for a deliberately non-authoritative example of how an MCP-aware client might point to the local server.

The exact Gemini or AI Studio configuration shape may change. Treat that file as an adapter example, not as a claim of official marketplace readiness.

## Design rule

Do not duplicate the skill instructions inside the integration layer. Keep the canonical instructions in the root skill folders and let adapters read from them.
