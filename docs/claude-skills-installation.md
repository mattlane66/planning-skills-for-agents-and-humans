# Install Planning Skills in Claude and Claude Design

Use this guide when you want Claude or Claude Design to invoke the repository's skills directly rather than running every planning move through Claude Code.

## Prerequisites

- Code execution and file creation must be enabled for your Claude account or organization.
- Skills must be enabled.
- Each uploaded skill must remain toggled on in **Customize → Skills**.

If those controls are unavailable, ask your Team or Enterprise administrator to enable Skills and code execution. Otherwise, use Claude Code as the invocation surface and bring the resulting artifacts into Claude Design.

## Build the upload packages

From the repository root, run:

```bash
python3 scripts/build_claude_skills.py
```

This command:

- validates that every canonical skill has exactly one upload description;
- checks the description length and trigger language;
- builds one ZIP per skill;
- includes shared templates, documentation, hooks, and orchestration references used by the skill;
- removes Claude Code-only cross-skill file references from the uploaded copy;
- validates the ZIP root, metadata, and referenced files.

The default output is `dist/claude-skills/`. A custom output directory must either be empty or contain only packages from the canonical inventory plus the packager marker. The builder removes only generated ZIP files; it refuses repository roots, home directories, unrelated files, and unexpected nested content instead of recursively deleting the target.

The packages are written to:

```text
dist/claude-skills/
```

Each ZIP contains the matching skill folder as its root. The packages are generated from the canonical top-level skill folders and shared repository resources; do not maintain separate hand-edited Claude copies.

To validate packages that have already been built without rebuilding them, run:

```bash
python3 scripts/build_claude_skills.py --check
```

## Upload to Claude

1. Open **Customize → Skills**.
2. Select **+ → Create skill → Upload a skill**.
3. Upload the ZIPs you expect to use.
4. Confirm each skill appears and is enabled.
5. Open Claude Design only after the relevant skills are enabled.

You do not need to upload every skill at once. Start with:

- `framing-doc.zip`
- `shaping.zip`
- `breadboarding.zip`
- `executable-breadboards.zip`

Add the advanced skills when their triggering complexity exists.

## Invoke a skill

Claude may load an enabled skill automatically when the request matches its description. You can also be explicit:

```text
Use my framing-doc skill to turn these notes into a frame. Do not design a solution yet.
```

Inside Claude Design, use the skill directly when it is available and the work is primarily visual or interactive. Otherwise, invoke it in Claude Code and import the resulting artifact into Claude Design.

A slash command is not guaranteed to appear for every uploaded custom skill in every Claude surface. Treat explicit natural-language invocation as the portable default.

## Authority and synchronization

Claude Design is a visual and interactive working surface. Project planning files in the product repository remain authoritative.

After Claude Design reveals a useful correction, tradeoff, requirement, or behavior:

1. decide whether to accept it;
2. write the accepted change back through Claude Code;
3. update the authoritative planning artifact;
4. rerun the relevant fit or drift check.

Do not allow the canvas to become a second, conflicting source of truth.

## Verify the installation

Use the prompts in [Claude Design skill test prompts](./claude-design-skill-tests.md). Confirm that Claude:

- loads the intended skill;
- does not load a planning skill for unrelated work;
- distinguishes canonical skills from Claude Code command wrappers;
- stops at required human decision gates;
- produces the expected artifact;
- does not invent implementation scope;
- falls back cleanly to Claude Code when repository access is required.

If Claude does not load a skill, first confirm that it is enabled, then make the request more explicit. If it still fails, refine the upload description in `claude-skill-descriptions.tsv` and rebuild the ZIP.
