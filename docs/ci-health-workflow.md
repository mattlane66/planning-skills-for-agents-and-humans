# CI health workflow

The repository runs `.github/workflows/repo-health.yml` on pull requests, pushes to `main`, and manual dispatches from the Actions tab.

The workflow first builds and validates the uploadable Claude skill ZIPs, then runs the full repository health check.

The workflow checks:

- Claude upload descriptions match the canonical skill inventory, remain within the metadata limit, and clearly state what each skill does and when to use it
- packager safety tests cover hidden orchestration files, protected output targets, and preservation of unrelated files
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
- pinned Python validation dependencies and their vulnerability audit
- moderate-or-higher dependency audit findings in either Node package

Run the same checks locally from the repository root:

```bash
python3 scripts/build_claude_skills.py
bash scripts/check-repo-health.sh
```

Use the workflow's **Run workflow** control when an explicit GitHub-hosted verification is needed without a new code change.

## Main-branch protection contract

Repository administration should require the stable checks below before changes
land on `main`. These names are part of the repository's governance contract
and are regression-tested so a workflow refactor cannot silently invalidate an
existing ruleset:

- Repo Health: `health`
- Repo Health: `Real browser smoke`
- Repo Health: `Release install smoke`
- Repo Health: `Site on minimum supported Node`
- CodeQL: `Analyze javascript-typescript`
- CodeQL: `Analyze python`

The branch ruleset should target the default/`main` branch, block deletion and
non-fast-forward updates, and require those checks. A mandatory pull-request
review rule is a maintainer policy choice rather than an assumed project
requirement.

The workflow files can define and test this contract, but enabling a GitHub
repository ruleset is an administrative setting outside repository contents.
After changing repository settings, verify that the ruleset is active and that
all six contexts above appear as required checks before treating `main` as
protected.

## External documentation availability

`.github/workflows/external-links.yml` is intentionally separate from
deterministic PR health. It runs weekly and on manual dispatch, retries/rate
limits network checks, and retains its report. A successful scheduled run proves
the scheduler and live-link path have executed; external availability can still
change later and is not a reason to make ordinary PR validation network-dependent.

After a successful push-triggered Repo health run on `main`, the auto-tag workflow validates the coordinated package version and matching changelog section and creates that version tag only when it does not already exist. It then calls the reusable release workflow directly; manually pushed tags invoke the same workflow. The release path reruns the full health suite before publication, accepts only exact stable SemVer tags whose commit is on `main`, requires version parity and an exact changelog section, builds deterministic Claude skill and plugin ZIPs, writes `SHA256SUMS`, and publishes only the validated payload.

Preview a release payload without publishing it:

```bash
python3 scripts/release.py preflight --tag v1.3.1
python3 scripts/release.py assets
```

When editing a canonical root skill, update its packaged copy with:

```bash
bash scripts/sync-packaged-skills.sh
```

CI runs the sync script in check mode and fails if a packaged copy has drifted.

## Validation dependency

The health workflow installs `requirements-dev.txt` so canonical and Claude-specific frontmatter are parsed as YAML rather than with an ad hoc line parser. Run `python3 -m pip install -r requirements-dev.txt` before `bash scripts/check-repo-health.sh` locally.
