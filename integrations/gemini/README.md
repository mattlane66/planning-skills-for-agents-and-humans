# Gemini / MCP integration

This directory describes a conservative way to use the planning skills from Gemini-style or MCP-capable environments.

The canonical `SKILL.md` files remain the source of truth. Gemini-specific files are adapters around those skills, not a replacement for the planning method.

The default interactive behavior is **collaborative shaping**: start from R, S, evidence, or a focused unknown and move among R/S/fit/spikes/candidate breadboards as useful. The **gated/orchestrated profile** remains available when strict prerequisites are explicitly required.

## Usage modes

### 1. Markdown skill usage

Where a Gemini or agent environment supports local skill folders, copy or symlink each skill folder so the `SKILL.md` file is a direct child of the configured skills directory.

Example workspace layout:

```text
.gemini/
  skills/
    planning-router/
      SKILL.md
    wayfinding/
      SKILL.md
    framing-doc/
      SKILL.md
    shaping/
      SKILL.md
    sketch-reconciliation/
      SKILL.md
    breadboarding/
      SKILL.md
    statechart/
      SKILL.md
    interface-contracts/
      SKILL.md
    executable-breadboards/
      SKILL.md
    dumplink/
      SKILL.md
    breadboard-reflection/
      SKILL.md
    kickoff-doc/
      SKILL.md
    feed-planning-context/
      SKILL.md
```

When applying the method to a real product, create this layout in the product repository rather than opening the Planning Skills repository as the work target. Preserve the product's existing `GEMINI.md` and `AGENTS.md`; add only the skill and command adapters you need.

The TOML files under `.gemini/commands/` are repository-local adapter examples, not path-independent packages. To reuse one in a product repository, copy or symlink it into that repository's `.gemini/commands/` directory and update every `@{...}` include to the installed skill and support-file paths. Do not replace the product's `AGENTS.md`.

Available wrappers include:

- `/plan`
- `/wayfind`
- `/shape`
- `/criteria`
- `/appetite`
- `/sketch-shapes`
- `/fit-check`
- `/spike`
- `/breadboard`
- `/select-shape`
- `/reconcile-sketch`
- `/statechart`
- `/dumplink`
- `/check-drift`

The shaping wrappers constrain the **current move**, not a mandatory exploration sequence. `/shape` is the broad collaborative front door. `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/spike`, and `/breadboard` can be used in the order that best resolves uncertainty while material remains Working.

Example collaborative prompt:

```text
Use the shaping skill from .gemini/skills/shaping/SKILL.md in collaborative mode.
I already have a rough solution. Capture it as Shape A, extract the provisional requirements it implies, and move among R, S, fit checks, spikes, and candidate breadboarding as useful.
Keep Working material separate from Accepted intent and do not select for me.
```

Example gated prompt:

```text
Use the gated/orchestrated profile from .agent-orchestration.yaml.
Enforce accepted requirements and accepted Appetite before comparative shape work or candidate breadboarding, and stop at every human promotion gate.
```

### 2. MCP tool usage

For clients that support MCP servers, use the optional server in `mcp-server/`.

The MCP server exposes the planning skills and orchestration metadata as callable tools:

- `list_planning_skills`
- `get_planning_skill`
- `recommend_planning_workflow`
- `get_artifact_template`
- `get_orchestration_manifest`

This lets an agent retrieve the right planning instructions on demand instead of requiring the whole repo to be pasted into context. The orchestration manifest exposes both collaborative and gated profiles; clients should not silently choose the gated profile for an ordinary human-guided shaping session.

## Example client config

See [`gemini-extension.example.json`](./gemini-extension.example.json) for a client-side example. Treat it as a starting point, not an official Google manifest. Different Gemini and MCP clients may use different configuration shapes.

## Important boundary

This integration does not claim official Gemini Extension marketplace compatibility. It is a practical adapter for environments that can either read local `SKILL.md` folders or call MCP tools.
