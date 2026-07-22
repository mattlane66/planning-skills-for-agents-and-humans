# CI health workflow

The repository runs `.github/workflows/repo-health.yml` on pull requests and pushes to `main`.

The workflow first builds and validates the uploadable Claude skill ZIPs, then runs the full repository health check.

The workflow checks:

- Claude upload descriptions match the canonical skill inventory, remain within the metadata limit, and clearly state what each skill does and when to use it
- every Claude upload ZIP has the correct root folder, canonical skill name, optimized description, bundled supporting resources, and no Claude Code-only or explicit cross-skill file references
- plugin manifests and the repository license
- strict skill frontmatter
- canonical skill inventory coverage, including optional Statechart and Sketch Reconciliation
- Bash 3-compatible inventory loading for macOS and Linux environments
- byte-for-byte parity between canonical root skills and packaged `skills/` copies
- current Claude command frontmatter/tool names and valid Gemini wrappers
- executable modes for shell scripts and hooks
- artifact templates, every path referenced by `.agent-orchestration.yaml`, and matching MCP exposure
- required documentation and README discovery links
- local Markdown links
- example-local inline Markdown file references
- version parity across Claude, Codex, and MCP packages
- contract fixtures for execution contracts, Statechart authority, vertical task groups, and drift output
- the generated Claude Code plugin bundle, including canonical skills, non-duplicate commands, license, and bundle-local supporting references
- reproducible visual-viewer installation and hot-reload server tests using the pinned Mermaid package
- reproducible MCP installation, TypeScript compilation, recommendation tests, and stdio tool smoke tests using `npm ci`

Run the same checks locally from the repository root:

```bash
python3 scripts/build_claude_skills.py
bash scripts/check-repo-health.sh
```

When editing a canonical root skill, update its packaged copy with:

```bash
bash scripts/sync-packaged-skills.sh
```

CI runs the sync script in check mode and fails if a packaged copy has drifted.
