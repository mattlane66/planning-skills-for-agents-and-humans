# Claude Code Plugin Packaging

This repo already contains Claude-compatible `SKILL.md` files as the canonical source of truth:

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

## Important principle

Do not maintain a second hand-edited copy of the skills under `skills/`.

The top-level skill folders are the source of truth. If a plugin bundle needs a `skills/` directory, generate it from the top-level folders so skill content cannot drift.

Run `bash scripts/sync-packaged-skills.sh` after editing a canonical skill. CI uses the same script in check mode and fails when packaged content differs.

Slash commands in `.claude/commands/`, `.claude/loop.md`, lifecycle hooks, and orchestration docs are invocation surfaces around the skills. They should stay thin and should not become a second copy of the method.

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

This creates:

```text
dist/claude-code-plugin/
  .claude-plugin/plugin.json
  AGENTS.md
  LICENSE
  commands/*.md
  docs/human-decision-gates.md
  docs/loop-prompting.md
  templates/drift-check.md
  skills/framing-doc/SKILL.md
  skills/shaping/SKILL.md
  skills/sketch-reconciliation/SKILL.md
  skills/breadboarding/SKILL.md
  skills/statechart/SKILL.md
  skills/interface-contracts/SKILL.md
  skills/executable-breadboards/SKILL.md
  skills/dumplink/SKILL.md
  skills/kickoff-doc/SKILL.md
  skills/feed-planning-context/SKILL.md
  skills/breadboard-reflection/SKILL.md
```

Test the generated bundle locally:

```bash
claude --plugin-dir dist/claude-code-plugin
```

Building first ensures that both canonical skills and command wrappers use Claude's plugin directory layout.

Claude namespaces installed plugin entries with the manifest name. For example, use `/planning-skills:framing-doc` for the canonical skill or `/planning-skills:frame` for its shorter command wrapper. Exact-name flat wrappers for `statechart` and `dumplink` are omitted from the bundle because Claude gives the same-named directory skill precedence; invoke `/planning-skills:statechart` or `/planning-skills:dumplink` directly.

The build rewrites command references to `${CLAUDE_PLUGIN_ROOT}` and includes the small set of supporting files they read. This keeps the generated commands independent of the clone path and the target project's contents.

## Marketplace publication

This repository does not claim that the plugin is already published in a Claude marketplace. Before publishing, add or update the marketplace metadata required by the current Claude Code documentation and verify the generated bundle.

Use the public repository URL for submission fields that request the source or homepage:

| Field | Value |
|---|---|
| Source repository | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |
| Plugin homepage | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |

## Maintenance checklist

When adding or renaming a skill:

1. Add or update the canonical top-level skill folder.
2. Add its folder name to `skill-inventory.txt`.
3. Ensure the skill has a valid `SKILL.md` with frontmatter.
4. Run `scripts/sync-packaged-skills.sh`.
5. Update `.claude-plugin/plugin.json` if the packaged capability set changed.
6. Add or update thin command wrappers only when needed.
7. Run the build and repository health scripts.
8. Inspect `dist/claude-code-plugin` before packaging or submission.
9. Keep marketplace copy aligned with the README and plugin manifest.
