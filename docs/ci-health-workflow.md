# CI health workflow

The repository runs `.github/workflows/repo-health.yml` on pull requests and pushes to `main`.

The workflow checks:

- plugin manifests and the repository license
- strict skill frontmatter
- byte-for-byte parity between canonical root skills and packaged `skills/` copies
- Claude and Gemini command wrappers
- artifact templates and every path referenced by `.agent-orchestration.yaml`
- required documentation and README discovery links
- local Markdown links
- version parity across Claude, Codex, and MCP packages
- contract fixtures for execution contracts, vertical task groups, and drift output
- the generated Claude plugin bundle
- reproducible MCP installation, TypeScript compilation, and tests using `npm ci`

Run the same checks locally from the repository root:

```bash
bash scripts/check-repo-health.sh
```

When editing a canonical root skill, update its packaged copy with:

```bash
bash scripts/sync-packaged-skills.sh
```

CI runs the sync script in check mode and fails if a packaged copy has drifted.
