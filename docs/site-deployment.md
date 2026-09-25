# Documentation portal deployment and trust model

The documentation site has two tracked outputs with different jobs:

- `site/index.html` is the generated, self-contained Planning Skills Lab artifact. It must be reproducible from canonical repository content and `site/src/`.
- `site/fit-check-error-model/` is a tracked static interactive companion for the Fit Check Error Model. Its HTML, CSS, and JavaScript are deployed as committed.
- GitHub Pages hosts those trusted tracked outputs. It is a deployment surface, not a second source of truth.

## Pull requests: build with read-only authority

`Repo health` checks every pull request with `contents: read` only. The minimum-Node job installs dependencies with lifecycle scripts disabled, runs the full deterministic portal suite, rebuilds `site/index.html`, and requires the rebuilt bytes to match the tracked file.

If they differ, CI uploads two diagnostics:

- the regenerated `site/index.html`;
- `site-index.patch`, the exact diff against the PR's tracked file.

This is also the dependency-PR regeneration path. Dependabot or another dependency PR may cause the generated standalone file to change, but PR code is never given repository write credentials merely to update that generated file. A maintainer can apply the uploaded patch or regenerate locally and push the result to the PR branch. The PR remains red until the tracked artifact and its source agree.

Do **not** replace this with `pull_request_target` that executes dependency code or repository build scripts while holding a write token. A dependency update changes executable code by definition; it belongs in the read-only trust domain until merged.

## `main`: deploy only trusted, reproduced bytes

`.github/workflows/pages.yml` runs only for pushes to `main` or manual dispatch. It:

1. checks out the exact trusted `main` commit without persisted credentials;
2. installs the locked site dependencies with lifecycle scripts disabled;
3. runs the deterministic site checks;
4. rejects the deployment if rebuilding changes tracked `site/index.html`;
5. stages the reproduced `site/index.html` plus the tracked `site/fit-check-error-model/` companion;
6. uploads only those staged files as the Pages artifact;
7. gives `pages: write` and `id-token: write` only to the final deploy job.

The build job has read-only repository authority. The deploy job never checks out or executes repository code. This keeps publication credentials out of untrusted build contexts.

Repository settings should configure **Pages → Build and deployment → Source: GitHub Actions**. The workflow's `github-pages` environment can additionally require environment protection if desired.

## Local verification

For the generated Planning Skills Lab:

```bash
cd site
npm ci --ignore-scripts
npm run check
CHROME_BIN=/path/to/chrome npm run test:browser
```

The real-browser smoke uses Chrome DevTools Protocol against the self-contained Lab file and checks direct `file://` opening, keyboard activation/focus, Mermaid SVG rendering, a 390 px viewport, and browser runtime errors.

The Fit Check Error Model companion is ordinary tracked static content under `site/fit-check-error-model/`; Pages copies that directory without transforming it.
