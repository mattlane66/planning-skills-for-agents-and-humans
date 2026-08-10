# Claude Code Plugin Packaging

This repo contains Claude-compatible `SKILL.md` files as the canonical source of truth, including:

- `planning-router/SKILL.md`
- `wayfinding/SKILL.md`
- `framing-doc/SKILL.md`
- `shaping/SKILL.md`
- `sketch-reconciliation/SKILL.md`
- `breadboarding/SKILL.md`
- `statechart/SKILL.md`
- `interface-contracts/SKILL.md`
- `executable-breadboards/SKILL.md`
- `dumplink/SKILL.md`
- `kickoff-doc/SKILL.md`
- `feed-planning-context/SKILL.md`
- `breadboard-reflection/SKILL.md`

Use this file when preparing the repo for Claude Code plugin submission or when creating a distributable plugin bundle.

## Important principles

Do not maintain a second hand-edited copy of the skills under `skills/`.

The top-level skill folders are the source of truth. If a plugin bundle needs a `skills/` directory, generate it from the top-level folders so skill content cannot drift.

Run `bash scripts/sync-packaged-skills.sh` after editing a canonical skill. CI uses the same script in check mode and fails when packaged content differs.

The runtime must also preserve the planning profile contract:

- **collaborative** is the default interactive profile: `/shape` can start from R, S, evidence, or a focused uncertainty and move among R/S/fit/spikes/candidate breadboards as useful
- **gated/orchestrated** is explicit: deterministic prerequisites come from `.agent-orchestration.yaml`
- both profiles preserve the same hard human promotion gates before selection, selected-design authority, slicing, and build

Slash commands in `.claude/commands/`, `.claude/loop.md`, lifecycle hooks, and orchestration docs are invocation surfaces around the skills. Human-facing aliases are manual-only, while generated canonical skills remain model-discoverable. Alias-backed canonical skills are hidden from the slash menu to avoid duplicate entries; direct-only skills receive Claude-specific argument hints and conservative file tools during packaging. Wrappers should stay thin and should not become a second copy of the method.

Focused shaping wrappers such as `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/spike`, and `/breadboard` constrain the current move. They are not a mandatory sequence. `/select-shape` remains a hard promotion gate.

## Plugin manifest

The plugin manifest lives at:

```text
.claude-plugin/plugin.json
```

Before submitting to the official marketplace, verify that the manifest schema still matches the current Claude Code plugin documentation.

## Build a local plugin bundle

Run:

```bash
./scripts/build-claude-plugin.sh
```

This creates a self-contained bundle with:

```text
dist/claude-code-plugin/
  .claude-plugin/plugin.json
  .agent-orchestration.yaml
  AGENTS.md
  LICENSE
  commands/*.md
  hooks/*.sh
  docs/*.md
  templates/*
  examples/*
  skills/*/SKILL.md
  skills/*/references/*
```

Test the generated bundle locally:

```bash
claude --plugin-dir dist/claude-code-plugin
```

Building first ensures that both canonical skills and command wrappers use Claude's plugin directory layout.

Claude namespaces installed plugin entries with the manifest name. For example, use `/planning-skills:shape` for the collaborative shaping wrapper, `/planning-skills:spike` for a focused spike, `/planning-skills:framing-doc` for the canonical Framing skill, or `/planning-skills:frame` for its shorter command wrapper. Exact-name flat wrappers for `statechart` and `dumplink` are omitted from the bundle because Claude gives the same-named directory skill precedence; invoke `/planning-skills:statechart` or `/planning-skills:dumplink` directly.

The build rewrites support paths in skills, commands, and the bundled `AGENTS.md` to `${CLAUDE_PLUGIN_ROOT}`. It includes the orchestration manifest, reusable docs, templates, hooks, and examples those instructions reference, so the plugin does not depend on same-named files in the target project.

## Marketplace publication

This repository does not claim that the plugin is already published in a Claude marketplace. Before publishing, add or update the marketplace metadata required by the current Claude Code documentation and verify the generated bundle.

Use the public repository URL for submission fields that request the source or homepage:

| Field | Value |
|---|---|
| Source repository | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |
| Plugin homepage | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |

## Maintenance checklist

When changing a skill, profile, command, or runtime behavior:

1. Update the canonical top-level skill first when method behavior changes.
2. Keep `skill-inventory.txt` and `skill-metadata.json` aligned with canonical skills.
3. Run `scripts/sync-packaged-skills.sh` so packaged skills match canonical sources.
4. Update `.agent-orchestration.yaml` when profile prerequisites, hard gates, or machine-readable behavior changes.
5. Update thin command wrappers only when invocation behavior or stopping points change.
6. Update cross-runtime docs/adapters so Claude, Codex, Gemini, Claude Design, and MCP describe the same method.
7. Run the build and repository health scripts.
8. Inspect `dist/claude-code-plugin` before packaging or submission.
9. Keep marketplace copy aligned with the README and plugin manifest.
