# Claude Code Plugin Packaging

This repo already contains Claude-compatible `SKILL.md` files as the canonical source of truth:

- `framing-doc/SKILL.md`
- `shaping/SKILL.md`
- `breadboarding/SKILL.md`
- `kickoff-doc/SKILL.md`
- `feed-planning-context/SKILL.md`
- `breadboard-reflection/SKILL.md`

Use this file when preparing the repo for Claude Code plugin submission or when creating a distributable plugin bundle.

## Important principle

Do not maintain a second hand-edited copy of the skills under `skills/`.

The top-level skill folders are the source of truth. If a plugin bundle needs a `skills/` directory, generate it from the top-level folders so skill content cannot drift.

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
  skills/framing-doc/SKILL.md
  skills/shaping/SKILL.md
  skills/breadboarding/SKILL.md
  skills/kickoff-doc/SKILL.md
  skills/feed-planning-context/SKILL.md
  skills/breadboard-reflection/SKILL.md
```

## Submit to the Claude Code plugin marketplace

Use the public GitHub repository URL for both fields unless Anthropic's current submission form asks for something more specific:

| Field | Value |
|---|---|
| GitHub repo | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |
| Plugin homepage | `https://github.com/mattlane66/planning-skills-for-agents-and-humans` |

## Install from GitHub

After the plugin structure is accepted by Claude Code, users should be able to install from the repository URL:

```bash
/plugin install https://github.com/mattlane66/planning-skills-for-agents-and-humans
```

## Maintenance checklist

When adding or renaming a skill:

1. Add or update the canonical top-level skill folder.
2. Ensure the skill has a valid `SKILL.md` with frontmatter.
3. Update `scripts/build-claude-plugin.sh` if the folder name changed.
4. Run the build script.
5. Inspect `dist/claude-code-plugin` before packaging or submission.
6. Keep marketplace copy aligned with the README and plugin manifest.
